import laser
import gaussian
import numpy as np


w0 = 0.7*1e-3
Pcr = 1.7*1e9
p = 4
Pin = p*Pcr
AMP = (2*Pin/(np.pi*w0**2))**(1/2)*1e-8
x0 = [0., 0.]

gauss = gaussian.Gaussian(w0, AMP, x0)

lamb = 775*1e-9
k = 2*np.pi/lamb
K = 7
L = 1600*1e-6
N = 64
Lz = 3.
Nz = int(3000*Lz)
nb_save = 100

parameter = [Pcr*1e-16, k, K, L, N, Lz, Nz, nb_save, w0, p]

with open('../results/parameter_linear.txt', 'wb') as outfile:
    np.savetxt(outfile, parameter)

laser = laser.laser(L, N, Lz, Nz, k, K, 'Linear', nb_save = nb_save)
laser.initialize(gauss)

#print(Pin*1e-16/np.sum(np.abs(laser.E)**2))

laser.propagation()

#print(laser.intensity_z.shape)
with open('../results/intensity_linear.txt', 'wb') as outfile:
    #outfile.write('# Array shape: {0}\n'.format(laser.E_z.shape))   
    for data_slice in laser.intensity_z:
        np.savetxt(outfile, data_slice)
        #outfile.write('# New slice\n')
        
#print(laser.intensity_z.shape)
with open('../results/energy_linear.txt', 'wb') as outfile:
    np.savetxt(outfile, laser.energy)

