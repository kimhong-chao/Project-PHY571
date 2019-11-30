import numpy as np
class laser:
    def __init__(self, L, N, Lz, Nz, wave_nb, K_coef, medium):
        
        self.medium = medium
        self.wave_nb = wave_nb
        self.K_coef = K_coef
        self.nb_save = 10
        
        self.intensity_z = np.zeros([Nz, 2*N, 2*N])
        self.E_z = np.zeros([Nz, 2*N, 2*N])
        self.E = np.zeros([N,N])
        
        self.Lz = Lz
        self.Nz = Nz
        
        #discretization for x and y
        r, self.d = np.linspace(-L, L, 2*N, retstep=True) 
        self.x, self.y = np.meshgrid(r,r)
        
        #discretization for kx and ky
        k = 2*np.pi*np.fft.fftfreq(2*N, d=self.d)
        self.kx, self.ky = np.meshgrid(k,k)
        
        norm_vectorized = np.vectorize(lambda x,y : x**2+y**2 )
        self.kxy2 = norm_vectorized(self.kx,self.ky)
        
        
    def initialize(self, func):
        self.E = func(self.x, self.y)
        
    def step(self, dz):
        if(self.medium == 'Beta'):
            self.E = self.E + self.nonlinear(self.E)*dz
        else:
            Ek = np.fft.fft2(self.E)
            Ek *= np.exp(-1j/(2*self.wave_nb)*(self.kxy2)*dz)
            self.E = np.fft.ifft2(Ek)
            self.E = self.E + self.nonlinear(self.E)*dz
        
    def propagation(self):
        E_z = []
        intensity_z = []
        E_z.append(self.E)
        intensity_z.append(np.abs(self.E)**2)
        dz = self.Lz/self.Nz
        
        for l in range(self.Nz-1):
            self.step(dz)
            if(l % 10 == 0):
                E_z.append(self.E)
                intensity_z.append(np.abs(self.E)**2)
                
        self.E_z = np.asarray(E_z)
        self.intensity_z = np.asarray(intensity_z)
   
    def nonlinear(self, E, cross = 5.1*1e-24, light = 3*1e8 , lamb = 790*1e-9\
        , tau = 3.5*1e-13, beta = 6.5*1e-104, hbar = 6.62*1e-34, n2 = 5.57*1e-23\
        ,K = 7):
        #constant used in nonlinear part of equation
        tp = 85*1e-15
        f = 0.5
        omega = 2*np.pi*light/lamb
        
        const1 = -cross/2*(1 + omega*tau)*beta/(K*hbar*omega)*tp/(8*K)**(1/2)
        const2 = -beta/2
        const3 = 1j*omega/light*n2
        const4 = 1j*omega/light*f*n2
        #normalised the constants 
        const1 = const1*(10**8)**(2*K)
        const2 = const2*(10**8)**(2*K-2)
        const3 = const3*(10**8)**2
        const4 = const4*(10**8)**2

        if(self.medium == 'Linear'):
            return 0
            
        if(self.medium == 'Kerr'):
            return const3*E*np.abs(E)**2
        
        if(self.medium == 'Absorption'):
            return const2*E*np.abs(E)**(2*K - 2)    
         
        if(self.medium == 'Plasma'):
            return const1*E*np.abs(E)**(2*K)
            
        if(self.medium == 'Total'):
            return const1*E*np.abs(E)**(2*K) + const2*E*np.abs(E)**(2*K - 2) \
                    + (const3 - const4)*E*np.abs(E)**2

   

        
        
        