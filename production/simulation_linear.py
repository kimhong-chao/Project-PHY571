import laser_linear
import numpy as np
import matplotlib.pyplot as plt

class Gaussian:
    def __init__(self, width, amplitude, x0):
        self.width = width
        self.amplitude = amplitude
        self.x0 = x0
        
    def __call__(self, x, y):
        A = self.amplitude
        x0 = self.x0
        sigma = self.width
        return A*np.exp(-((x-x0[0])**2 + (y-x0[1])**2)/sigma**2)



w0 = 0.7*1e-3
Pcr = 2*1e9
p = 4
Pin = p*Pcr
AMP = (2*Pin/(np.pi*w0**2))**(1/2)
x0 = [0., 0.]

gauss = Gaussian(w0, AMP, x0)

lamb = 790*1e-9
k = 2*np.pi/lamb
K = 7
L = 1600*1e-6
N = 256
Lz = 1.4
Nz = 512

laser = laser_linear.laser_linear(L, N, Lz, Nz, k, K)
laser.initialize(gauss)
laser.propagation()


for i in [0, 219, 303, Nz-1]:
    fig, ax = plt.subplots()
    mesh = ax.pcolormesh(laser.x, laser.y, laser.intensity_z[i])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    plt.colorbar(mesh, ax=ax)
    fig.show()
