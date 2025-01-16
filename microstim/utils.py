import numpy as np
from scipy.special import erf
from math import sqrt
from microstim.globals import THRESHOLD, X_RANGE

def ephapticCoupling(ve, vi):
    e_thresh, i_thresh = [], []
    for distance, e_pot, i_pot in zip(X_RANGE, ve, vi):
        if e_pot > THRESHOLD:
            e_thresh.append(distance)
        if i_pot > THRESHOLD:
            i_thresh.append(distance)
    return max(e_thresh, default=0), max(i_thresh, default=0)


"""
Rate functions
"""
def normal(sigma):
    return np.exp(-(X_RANGE)**2/(2 * sigma**2)) / (2 * np.pi * sigma**2)
    
def sigmoid(v):
    return 1 / (1 + np.exp(-(THRESHOLD - v)))

def rect(v):
    return np.where(v >= THRESHOLD, 1, 0)


"""
convoluted functions
"""
def KernelConvolution(rho, weight, sigma):
    return weight * ( erf( (X_RANGE + rho) / (sqrt(2) * sigma) ) - erf( (X_RANGE - rho) / (sqrt(2) * sigma) ) ) * 0.5
