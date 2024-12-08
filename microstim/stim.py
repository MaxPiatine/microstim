from math import sqrt
from scipy.special import erf
import matplotlib.pyplot as plt
import numpy as np

from microstim.globals import N, i_RANGE, X_RANGE, THRESHOLD, ALPHA, DT, R



def KernelConvolution(x, rho, weight, sigma):
    return weight * ( erf( (x + rho) / (sqrt(2) * sigma) ) - erf( (x - rho) / (sqrt(2) * sigma) ) ) * 0.5


def microstim(intensity, weights, sigma, e_amp=0, i_amp=0, max_v=True):
    rho_e, rho_i = np.zeros(N), np.zeros(N)

    v_e, v_i = np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE)))

    """
    Initial condition is assuming that we stimulate a population of 
    excitatory cells. where the excitatory potential follows monopole
    diapole, and the activation radius is dependent on the intensity
    """

    rho_e[0] = (R*intensity/THRESHOLD - ALPHA) * e_amp
    rho_i[0] = (R*intensity/THRESHOLD - ALPHA) * i_amp

    # direct stimulation
    v_e[0] = R*intensity/(X_RANGE + ALPHA) * e_amp #1/sqrt(x)
    v_i[0] = R*intensity/(X_RANGE + ALPHA) * i_amp #1/sqrt(x)
    
    # kernal arrays
    ee, ie, ei, ii = np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE)))

    for i in range(0, len(i_RANGE)-1):
        
        ee[i] = KernelConvolution(X_RANGE, rho_e[i], weights["e->e"], sigma["ee"]) 
        ie[i] = KernelConvolution(X_RANGE, rho_i[i], weights["i->e"], sigma["ie"])
        ei[i] = KernelConvolution(X_RANGE, rho_e[i], weights["e->i"], sigma["ei"])
        ii[i] = KernelConvolution(X_RANGE, rho_i[i], weights["i->i"], sigma["ii"])
        
        v_e[i+1] = v_e[i] + DT * (-v_e[i] + ee[i] - ie[i])
        
        v_i[i+1] = v_i[i] + DT * (-v_i[i] + ei[i] - ii[i])

        e_thresh, i_thresh = [], []
        for distance, e_pot, i_pot in zip(X_RANGE, v_e[i+1], v_i[i+1]):
            if e_pot > THRESHOLD:
                e_thresh.append(distance)
            if i_pot > THRESHOLD:
                i_thresh.append(distance)
            
        rho_e[i+1], rho_i[i+1] = max(e_thresh, default=0), max(i_thresh, default=0)
        # print("At Step %i: excitatory activation radius: %i microns inhibitory activation radius: %i microns"%(i+1, rho_e[i+1], rho_i[i+1]))

    if max_v:
        v_e = np.clip(v_e, -20, 20)
        v_i = np.clip(v_i, -20, 20)
        
    return rho_e, rho_i, v_e, v_i



