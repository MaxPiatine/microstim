from numpy import arange, zeros
from math import sqrt
from scipy.special import erf

from plot import plot

R = 7 #resistance (change) KOhms
ALPHA = 4 #micron
DT = 0.01

THRESHOLD = 20 #mV

def KernelConvolution(x, rho, weight, sigma):
    return weight * ( erf( (x + rho) / (sqrt(2) * sigma) ) - erf( (x - rho) / (sqrt(2) * sigma) ) ) * 0.5


def microstim(x, i_steps, intensity, weights, sigma, e_amp=1, i_amp=1):
    
    """
    Initial condition is assuming that we stimulate a population of 
    excitatory cells. where the excitatory potential follows monopole
    diapole, and the activation radius is dependent on the intensity
    """

    rho_e[0] = (R*intensity/THRESHOLD - ALPHA) * e_amp
    rho_i[0] = (R*intensity/THRESHOLD - ALPHA) * i_amp

    # direct stimulation
    v_e[0] = (R*intensity/(X_RANGE + ALPHA)) * e_amp #1/sqrt(x)
    v_i[0] = (R*intensity/(X_RANGE + ALPHA)) * i_amp #1/sqrt(x)
    
    # kernal arrays
    ee, ie, ei, ii = zeros((len(i_steps), len(x))), zeros((len(i_steps), len(x))), zeros((len(i_steps), len(x))), zeros((len(i_steps), len(x)))

    for i in range(0, len(i_steps)-1):
        
        ee[i] = KernelConvolution(x, rho_e[i], weights["e->e"], sigma["ee"]) 
        ie[i] = KernelConvolution(x, rho_i[i], weights["i->e"], sigma["ie"])
        ei[i] = KernelConvolution(x, rho_e[i], weights["e->i"], sigma["ei"])
        ii[i] = KernelConvolution(x, rho_i[i], weights["i->i"], sigma["ii"])
        
        v_e[i+1] = v_e[i] + DT * (-v_e[i] + ee[i] - ie[i])
        
        v_i[i+1] = v_i[i] + DT * (-v_i[i] + ei[i] - ii[i])

        e_thresh, i_thresh = [], []
        for distance, e_pot, i_pot in zip(x, v_e[i+1], v_i[i+1]):
            if e_pot > THRESHOLD:
                e_thresh.append(distance)
            if i_pot > THRESHOLD:
                i_thresh.append(distance)
            
        rho_e[i+1], rho_i[i+1] = max(e_thresh, default=0), max(i_thresh, default=0)
        print("At Step %i: excitatory activation radius: %i microns inhibitory activation radius: %i microns"%(i+1, rho_e[i+1], rho_i[i+1]))
        
    return rho_e, rho_i, v_e, v_i


if __name__ == "__main__":
    N = 500
    T = N * DT
    
    i_RANGE = arange(0, N) #steps
    X_RANGE = arange(0, 1000)
    T_RANGE = arange(0, T, T/N)

    v_e, v_i = zeros((len(i_RANGE), len(X_RANGE))), zeros((len(i_RANGE), len(X_RANGE)))
    rho_e, rho_i = zeros(N), zeros(N)
    
    # look up the weights
    weights = {
        "e->e": 200,
        "i->e": 200,
        "e->i": 200,
        "i->i": 200,
    }

    sigma = {
        "ee": 120,
        "ie": 120,
        "ei": 120,
        "ii": 120,
    } #microns
    
    intensity = 500
    
    rho_e, rho_i, v_e, v_i = microstim(X_RANGE, i_RANGE, intensity, weights, sigma)
    
    plot(X_RANGE, T_RANGE, i_RANGE, N//5, rho_e, rho_i, v_e, v_i)
