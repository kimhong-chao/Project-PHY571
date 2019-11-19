import numpy as np
class laser_linear:
    def __init__(self, L, N, Lz, Nz, wave_nb, K_coef):
        
        self.wave_nb = wave_nb
        self.K_coef = K_coef
        self.intensity_z = np.zeros([Nz, 2*N, 2*N])
        self.E_z = np.zeros([Nz, 2*N, 2*N])
        self.E = np.zeros([N,N])
        
        self.Lz = Lz
        self.Nz = Nz
        
        #discretation for x and y
        r, self.d = np.linspace(-L, L, 2*N, retstep=True) 
        self.x, self.y = np.meshgrid(r,r)
        
        #discretation for kx and ky
        k = 2*np.pi*np.fft.fftfreq(2*N, d=self.d)
        self.kx, self.ky = np.meshgrid(k,k)
        
        norm_vectorized = np.vectorize(self.norm)
        self.kxy2 = norm_vectorized(self.kx,self.ky)
        
        
    def initialize(self, func):
        vectorized_func = np.vectorize(func)
        self.E = vectorized_func(self.x, self.y)
        
    def step(self, dz):
        Ek = np.fft.fft2(self.E)
        Ek *= np.exp(-1j/(2*self.wave_nb)*(self.kxy2)*dz)
        self.E = np.fft.ifft2(Ek)
        
    def propagation(self):
        Ez = []
        intensity_z = []
        Ez.append(self.E)
        intensity_z.append(np.abs(self.E)**2)
        dz = self.Lz/self.Nz
        for l in range(self.Nz-1):
            self.step(dz)
            Ez.append(self.E)
            intensity_z.append(np.abs(self.E)**2)
        self.E_z = np.asarray(Ez)
        self.intensity_z = np.asarray(intensity_z)
        
    def norm(self, x, y):
        return x**2 + y**2
