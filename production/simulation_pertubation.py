'''
This code is used to simulate the result of intensity of laser
and save it into directory below
'''
import laser
import gaussian
import numpy as np

#Parameter used to initialise the gaussian beam
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
#Spacial disscretization
L = 8*1e-3
N = 200
Lz = 10.
Nz = int(3000*Lz)
nb_save = 100*Lz

#Array of parameter used to call in the analysis code
parameter = [Pcr*1e-16, k, K, L, N, Lz, Nz, nb_save, w0, p]
np.savetxt('../results/parameter_pertu.txt', parameter)

laser = laser.laser(L, N, Lz, Nz, k, K, 'Pertubation', nb_save = nb_save)
laser.initialize(gauss)
laser.propagation()

#print(laser.intensity_z.shape)
with open('../results/intensity_pertubation.txt', 'wb') as outfile:
    #outfile.write('# Array shape: {0}\n'.format(laser.E_z.shape))   
    for data_slice in laser.intensity_z:
        np.savetxt(outfile, data_slice)
        #outfile.write('# New slice\n')
        
np.savetxt('../results/energy_pertu.txt', laser.energy)
np.savetxt('../results/inten_max_pertu.txt', laser.inten_max)