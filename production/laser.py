import numpy as np
import sys
class laser:
    def __init__(self, L, N, Lz, Nz, wave_nb, K_coef, effect, nb_save):
        
        self.effect = effect
        self.wave_nb = wave_nb
        self.K_coef = K_coef
        self.nb_save = nb_save
        
        self.intensity_z = np.zeros([int(Nz/nb_save), 2*N, 2*N])
        self.E = np.zeros([N,N])
        self.total = np.zeros(Nz)
        
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
        if(self.effect == 'Pertubation'):
            self.E += np.max(self.E)*1e-1*np.random.uniform(-1,1)
        
    def step(self, dz, cross, light, lamb, tau, beta, hbar, n2, K, tp, f):
        if(self.effect == 'Linear' or self.effect == 'Kerr'  \
           or self.effect == 'Total' or self.effect == 'Pertubation'):
            Ek = np.fft.fft2(self.E)
            Ek *= np.exp(-1j/(2*self.wave_nb)*(self.kxy2)*dz)
            self.E = np.fft.ifft2(Ek)
        self.E = self.E + self.nonlinear(self.E, cross, light, lamb, tau, beta, hbar, \
                                         n2, K, tp, f)*dz
        
    def propagation(self, cross = 5.1*1e-24, light = 3*1e8 , lamb = 775*1e-9\
        , tau = 3.5*1e-13, beta = 6.5*1e-104, hbar = 6.62*1e-34, n2 = 5.57*1e-23\
        ,K = 7, tp = 85*1e-15, f = 0.5):
        energy = []
        energy.append(np.sum(np.abs(self.E)**2))
        intensity_z = []
        dz = self.Lz/self.Nz
        
        print('Begin propagation')
        for l in range(self.Nz-1):
            self.step(dz, cross, light ,lamb, tau, beta, hbar, n2, K, tp, f) 
            sys.stdout.write('\rCompleted: %.2f %%' %(l/(self.Nz -2)*100))
            sys.stdout.flush()
            energy.append(np.sum(np.abs(self.E)**2))
            if(l % self.nb_save == 0):
                intensity_z.append(np.abs(self.E)**2)
                
        self.energy = np.asarray(energy)
        self.intensity_z = np.asarray(intensity_z)
   
    def nonlinear(self, E, cross, light ,lamb, tau, beta, hbar, n2, K, tp, f):
        #constant used in nonlinear part of equation
        
        omega = 2*np.pi*light/lamb

        if(self.effect == 'Linear'):
            return 0
            
        if(self.effect == 'Kerr'):
            const3 = 1j*omega/light*(1-f)*n2
            const3 = const3*(10**8)**2
            return const3*E*np.abs(E)**2
        
        if(self.effect == 'Absorption'):
            const2 = -beta/2
            const2 = const2*(10**8)**(2*K-2)
            return const2*E*np.abs(E)**(2*K - 2)    
         
        if(self.effect == 'Plasma'):
            const1 = -cross/2*(1 + 1j*omega*tau)*beta/(K*hbar*omega)*tp/(np.pi/(8*K))**(1/2)
            const1 = const1*(10**8)**(2*K)
            return const1*E*np.abs(E)**(2*K)
            
        if(self.effect == 'Total' or self.effect == 'Pertubation'):
            const1 = -cross/2*(1 + 1j*omega*tau)*beta/(K*hbar*omega)*tp*(np.pi/(8*K))**(1/2)
            const2 = -beta/2
            const3 = 1j*omega/light*(1-f)*n2
            
            const1 = const1*(10**8)**(2*K)
            const2 = const2*(10**8)**(2*K-2)
            const3 = const3*(10**8)**2
            
            return const1*E*np.abs(E)**(2*K) + const2*E*np.abs(E)**(2*K - 2) \
                    + const3*E*np.abs(E)**2

   

        
        
        