'''
This class is used for initialisation 
'''
import numpy as np

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