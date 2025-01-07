from math import sqrt
from scipy.special import erf
import matplotlib.pyplot as plt
import numpy as np

from microstim.globals import N, i_RANGE, X_RANGE, THRESHOLD, ALPHA, DT, R, P


def KernelConvolution(rho, weight, sigma):
    return weight * ( erf( (X_RANGE + rho) / (sqrt(2) * sigma) ) - erf( (X_RANGE - rho) / (sqrt(2) * sigma) ) ) * 0.5

def ephapticCoupling(ve, vi):
    e_thresh, i_thresh = [], []
    for distance, e_pot, i_pot in zip(X_RANGE, ve, vi):
        if e_pot > THRESHOLD:
            e_thresh.append(distance)
        if i_pot > THRESHOLD:
            i_thresh.append(distance)
    
    return max(e_thresh, default=0), max(i_thresh, default=0)

def depolarizationModel(intensity, weights, sigma, start_boost):
    rho_e, rho_i = np.zeros(N), np.zeros(N)
    v_e, v_i = np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE)))

    v_e[0] = R*intensity/(X_RANGE + ALPHA)**P * start_boost["exc"]
    v_i[0] = R*intensity/(X_RANGE + ALPHA)**P * start_boost["inh"]

    rho_e[0], rho_i[0] = ephapticCoupling(v_e[0], v_i[0])
    
    # kernal arrays
    ee, ie, ei, ii = np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE)))

    for i in range(0, len(i_RANGE)-1):

        ee[i] = KernelConvolution(rho_e[i], weights["e->e"], sigma["ee"]) 
        ie[i] = KernelConvolution(rho_i[i], weights["i->e"], sigma["ie"])
        ei[i] = KernelConvolution(rho_e[i], weights["e->i"], sigma["ei"])
        ii[i] = KernelConvolution(rho_i[i], weights["i->i"], sigma["ii"])
        
        v_e[i+1] = v_e[i] + DT * (-v_e[i] + ee[i] - ie[i])
        
        v_i[i+1] = v_i[i] + DT * (-v_i[i] + ei[i] - ii[i])
        
        rho_e[i+1], rho_i[i+1] = ephapticCoupling(v_e[i+1], v_i[i+1])

    return rho_e, rho_i, v_e, v_i

def activationRadius(intensity, start_boost):
    r_o = ALPHA * intensity**(1/P)
    return np.where(np.abs(X_RANGE) <= r_o * start_boost, 1, 0)

def activationModel(intensity, weights, sigma, start_boost):
    v_e, v_i = np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE)))
    
    
