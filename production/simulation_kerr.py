import laser as l
import gaussian
import numpy as np

w0 = 0.7*1e-3
Pcr = 1.6*1e9
p = 4
Pin = p*Pcr
AMP = (2*Pin/(np.pi*w0**2))**(1/2)*1e-8
x0 = [0., 0.]

gauss = gaussian.Gaussian(w0, AMP, x0)

lamb = 775*1e-9
k = 2*np.pi/lamb
K = 7
L = 16*1e-4
N = 64
Lz = 1.5
Nz = 2000
nb_save = 10

parameter = [Pcr*1e-16, k, K, L, N, Lz, Nz, nb_save, w0, p]

with open('../results/parameter_kerr.txt', 'wb') as outfile:
    np.savetxt(outfile, parameter)

laser = l.laser(L, N, Lz, Nz, k, K, 'Kerr', nb_save = nb_save)
laser.initialize(gauss)
laser.propagation()

#print(laser.intensity_z.shape)
with open('../results/intensity_kerr.txt', 'wb') as outfile:
    #outfile.write('# Array shape: {0}\n'.format(laser.E_z.shape))   
    for data_slice in laser.intensity_z:
        np.savetxt(outfile, data_slice)
        #outfile.write('# New slice\n')
        
#print(laser.intensity_z.shape)
with open('../results/energy_kerr.txt', 'wb') as outfile:
    np.savetxt(outfile, laser.energy)
    
    
    
def find_div(u):
    Pin = u*Pcr
    AMP = (2*Pin/(np.pi*w0**2))**(1/2)*1e-8
    x0 = [0., 0.]
    
    gauss = gaussian.Gaussian(w0, AMP, x0)

    
    laser_f = l.laser(L, N, Lz, Nz, k, K, 'Kerr', nb_save = nb_save)
    laser_f.initialize(gauss)
    laser_f.propagation(f = 0.0)
    
    
    list_div = []
    for i in range(laser_f.intensity_z.shape[0]):
        max_div = np.max(laser_f.intensity_z[i])
        list_div.append(max_div)
    list_div = np.asarray(list_div)
    div = 0
    #print(list_div.shape)
    for i in range(list_div.shape[0]):
        if (np.isinf(list_div[i]) or np.isnan(list_div[i])): 
            div = i-1 
            break
    div = div*(Lz/Nz*nb_save)
    return div

p = np.linspace(1,10,10)
point_div = []
for i in p:
    div = find_div(i)
    print("Complete: ",i/10*100,"%")
    point_div.append(div)
    
with open('../results/intensity_kerr_divergence.txt', 'wb') as outfile:
        np.savetxt(outfile, point_div)

    
                    

    

