import laser as l
import gaussian
import numpy as np

def find_div(p):
    w0 = 0.7*1e-3
    Pcr = 1.7*1e9
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
    nb_save = 10
    laser = l.laser(L, N, Lz, Nz, k, K, 'Kerr', nb_save = 1)
    laser.initialize(gauss)
    laser.propagation(f = 0.0)
    
    
    list_div = []
    for i in range(laser.intensity_z.shape[0]):
        max_div = np.max(laser.intensity_z[i])
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

    
                    

    

