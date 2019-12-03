
import laser
import gaussian
import numpy as np


w0 = 0.7*1e-3
Pcr = 1.7*1e9
p = 35
Pin = p*Pcr
AMP = (2*Pin/(np.pi*w0**2))**(1/2)*1e-8
x0 = [0., 0.]

gauss = gaussian.Gaussian(w0, AMP, x0)

lamb = 775*1e-9
k = 2*np.pi/lamb
K = 7
L = 3*1e-3
N = 64
Lz = 10.
Nz = int(6000*Lz)
nb_save = 200

laser = laser.laser(L, N, Lz, Nz, k, K, 'Pertubation', nb_save = nb_save)
laser.initialize(gauss)
laser.propagation()

#print(laser.intensity_z.shape)
with open('../results/intensity_pertubation.txt', 'wb') as outfile:
    #outfile.write('# Array shape: {0}\n'.format(laser.E_z.shape))   
    for data_slice in laser.intensity_z:
        np.savetxt(outfile, data_slice)
        #outfile.write('# New slice\n')
