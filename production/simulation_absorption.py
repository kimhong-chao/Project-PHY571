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

lamb = 790*1e-9
k = 2*np.pi/lamb
K = 7
L = 16*1e-4
N = 64
Lz = 2.0
Nz = 1000

laser = laser.laser(L, N, Lz, Nz, k, K, 'Plasma', nb_save = 10)
laser.initialize(gauss)
laser.propagation()

with open('../results/result_absorption.txt', 'wb') as outfile:
    #outfile.write('# Array shape: {0}\n'.format(laser.E_z.shape))   
    for data_slice in laser.intensity_z:
        np.savetxt(outfile, data_slice)
        #outfile.write('# New slice\n')
                    

