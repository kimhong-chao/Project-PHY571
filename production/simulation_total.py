import laser
import gaussian
import numpy as np


#Box's parameters
L = 8*1e-3
N = 200
Lz = 10.
Nz = int(3000*Lz)
nb_save = 100

#Laser's parameters
w0 = 0.7*1e-3
n2 = 5.57*1e-23
lamb = 775*1e-9
k = 2*np.pi/lamb
K = 7
Pcr = 3.77*np.pi/(2*k**2*n2)
p = 35
Pin = p*Pcr
AMP = (2*Pin/(np.pi*w0**2))**(1/2)*1e-8
x0 = [0., 0.]

L = 8*1e-3
N = 200
Lz = 10.
Nz = int(3000*Lz)
nb_save = 100*Lz

parameter = [Pcr*1e-16, k, K, L, N, Lz, Nz, nb_save, w0, p]
np.savetxt('../results/parameter_total.txt', parameter)

gauss = gaussian.Gaussian(w0, AMP, x0)
laser = laser.laser(L, N, Lz, Nz, k, K, 'Total', nb_save = nb_save)
laser.initialize(gauss)
laser.propagation()

with open('../results/intensity_total.txt', 'wb') as outfile:
    for data_slice in laser.intensity_z:
        np.savetxt(outfile, data_slice)
        
np.savetxt('../results/energy_total.txt', laser.energy*(L/N)**2)
np.savetxt('../results/inten_max_total.txt', laser.inten_max)
