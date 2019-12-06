'''
This code is used to simulate the result of intensity of laser
and save it into directory below
'''
import laser
import gaussian
import numpy as np

#Box's parameters
L = 3*1e-3
N = 128
Lz = 3
Nz = int(3000*Lz)
nb_save = 10

#Laser's parameters
w0 = 0.7*1e-3
n2 = 5.57*1e-23
lamb = 775*1e-9
k = 2*np.pi/lamb
K = 7
Pcr = 3.77*np.pi/(2*k**2*n2)
p = 4
Pin = p*Pcr
AMP = (2*Pin/(np.pi*w0**2))**(1/2)*1e-8
x0 = [0., 0.]

#Array of parameter used to call in the analysis code
parameter = [Pcr*1e-16, k, K, L, N, Lz, Nz, nb_save, w0, p, n2]

with open('../results/Linear/parameter_linear.txt', 'wb') as outfile:
    np.savetxt(outfile, parameter)

gauss = gaussian.Gaussian(w0, AMP, x0)
laser = laser.laser(L, N, Lz, Nz, k, K, 'Linear', nb_save = nb_save)
laser.initialize(gauss)
laser.propagation()

with open('../results/Linear/intensity_linear.txt', 'wb') as outfile:
    for data_slice in laser.intensity_z:
        np.savetxt(outfile, data_slice)
        
with open('../results/Linear/energy_linear.txt', 'wb') as outfile:
    np.savetxt(outfile, laser.energy)
    

