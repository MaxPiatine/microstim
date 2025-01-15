from math import sqrt
from scipy.special import erf
import matplotlib.pylab as plt
import numpy as np

from microstim.globals import N, i_RANGE, X_RANGE, THRESHOLD, ALPHA, DT, R, P


def KernelConvolution(rho, weight, sigma):
    return weight * ( erf( (X_RANGE + rho) / (sqrt(2) * sigma) ) - erf( (X_RANGE - rho) / (sqrt(2) * sigma) ) ) * 0.5

def kernalExp(intensity, weights, sigma, gamma):
    constants = weights * gamma * np.log(intensity) / np.sqrt(4 * np.pi * sigma**2)
    return  constants * np.exp(-X_RANGE**2/(4 * sigma**2))

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
    

def normal(sigma):
    return np.exp(-X_RANGE**2/(2 * sigma**2)) / (2 * np.pi * sigma**2)

def sigmoid(v):
    return np.where(v >= 0, 1 / (1 + np.exp(-(THRESHOLD - v))), np.exp(THRESHOLD - v) / (1 + np.exp(THRESHOLD - v)))

def activationModel(intensity, weights, sigma, gamma):
    nu_e, nu_i = np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE)))
    v_e, v_i = np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE)))

    nu_e[0] = np.log(intensity) * gamma["exc"] * normal(sigma=150)
    nu_i[0] = np.log(intensity) * gamma["inh"] * normal(sigma=100)

    wee = weights["e->e"] * normal(sigma["ee"])
    wie = weights["i->e"] * normal(sigma["ie"])
    wei = weights["e->i"] * normal(sigma["ei"])
    wii = weights["i->i"] * normal(sigma["ii"])
    
    for i in range(0, len(i_RANGE)-1):

        v_e[i+1] = v_e[i] + DT * (-v_e[i] + np.convolve(wee, nu_e[i], mode="same") - np.convolve(wie, nu_i[i], mode="same"))
        v_i[i+1] = v_i[i] + DT * (-v_i[i] + np.convolve(wei, nu_e[i], mode="same") - np.convolve(wii, nu_i[i], mode="same"))
        
        nu_e[i+1] = sigmoid(v_e[i+1])
        nu_i[i+1] = sigmoid(v_i[i+1])

    _, ax = plt.subplots(1, 2)
    for j in range(0, 200, 50):
        ax[0].plot(X_RANGE, v_e[j], label="v_e " + str(j))
        ax[0].plot(X_RANGE, v_i[j], label="v_i " + str(j))

        ax[1].plot(X_RANGE, nu_e[j], label="nu_e " + str(j))

    ax[0].legend()
    ax[1].set_ylim([-0.2, 1.2])
    ax[1].legend()

    plt.tight_layout()
    plt.show()

    return v_e, v_i
    
