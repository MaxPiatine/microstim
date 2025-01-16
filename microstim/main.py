from math import sqrt
from scipy.special import erf
import matplotlib.pylab as plt
import numpy as np

from microstim.globals import N, i_RANGE, X_RANGE, THRESHOLD, ALPHA, DT, R, P, start_boost, gamma
from microstim.utils import ephapticCoupling, KernelConvolution, rect, normal

def model(intensity, weights, sigma, is_depolarized=True):
    rho_e, rho_i = np.zeros(N), np.zeros(N)
    nu_e, nu_i = np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE)))
    v_e, v_i = np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE)))

    if is_depolarized:
        v_e[0] = R*intensity/(X_RANGE + ALPHA)**P * start_boost["exc"]
        v_i[0] = R*intensity/(X_RANGE + ALPHA)**P * start_boost["inh"]
        
        nu_e[0] = rect(v_e[0])
        nu_i[0] = rect(v_i[0])
        
        rho_e[0], rho_i[0] = ephapticCoupling(v_e[0], v_i[0])
    else:
        nu_e[0] = np.log(intensity) * gamma["exc"] * normal(sigma=150) #random sigma for firing rate
        nu_i[0] = np.log(intensity) * gamma["inh"] * normal(sigma=100)
        
    # synaptic connectivity
    wee = weights["ee"] * normal(sigma["ee"])
    wie = weights["ie"] * normal(sigma["ie"])
    wei = weights["ei"] * normal(sigma["ei"])
    wii = weights["ii"] * normal(sigma["ii"])
        
    for i in range(0, len(i_RANGE)-1):

        v_e[i+1] = v_e[i] + DT * (-v_e[i] + np.convolve(wee, nu_e[i], mode="same") - np.convolve(wie, nu_i[i], mode="same"))
        plt.plot(X_RANGE, np.convolve(wee, nu_e[i], mode="same") - np.convolve(wie, nu_i[i], mode="same"))
        plt.show()
        v_i[i+1] = v_i[i] + DT * (-v_i[i] + np.convolve(wei, nu_e[i], mode="same") - np.convolve(wii, nu_i[i], mode="same"))
        
        nu_e[i+1] = rect(v_e[i+1])
        nu_i[i+1] = rect(v_i[i+1])
        
        rho_e[i+1], rho_i[i+1] = ephapticCoupling(v_e[i+1], v_i[i+1])

    
        
    _, ax = plt.subplots(1, 3)
    for j in range(0, 1000, 200):
        ax[0].plot(X_RANGE, v_e[j], label="v_e " + str(j))
        ax[0].plot(X_RANGE, v_i[j], label="v_i " + str(j))
        
        ax[1].plot(X_RANGE, nu_e[j], label="nu_e " + str(j))

    ax[0].legend()
    ax[1].set_ylim([-0.2, 1.2])
    ax[1].legend()
    ax[2].plot(X_RANGE, rho_e, label="rho_e")
    ax[2].plot(X_RANGE, rho_i, label="rho_i")
    ax[2].legend()

    plt.tight_layout()
    plt.show()

    return rho_e, rho_i, v_e, v_i


def depolarizationModel(intensity, weights, sigma, start_boost):
    rho_e, rho_i = np.zeros(N), np.zeros(N)
    v_e, v_i = np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE)))

    v_e[0] = R*intensity/(X_RANGE + ALPHA)**P * start_boost["exc"]
    v_i[0] = R*intensity/(X_RANGE + ALPHA)**P * start_boost["inh"]

    rho_e[0], rho_i[0] = ephapticCoupling(v_e[0], v_i[0])
    
    # kernal arrays
    ee, ie, ei, ii = np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE)))

    for i in range(0, len(i_RANGE)-1):

        ee[i] = KernelConvolution(rho_e[i], weights["ee"], sigma["ee"]) 
        ie[i] = KernelConvolution(rho_i[i], weights["ie"], sigma["ie"])
        ei[i] = KernelConvolution(rho_e[i], weights["ei"], sigma["ei"])
        ii[i] = KernelConvolution(rho_i[i], weights["ii"], sigma["ii"])
        
        v_e[i+1] = v_e[i] + DT * (-v_e[i] + ee[i] - ie[i])
        
        plt.plot(X_RANGE, ee[i] - ie[i])
        plt.show()
        
        v_i[i+1] = v_i[i] + DT * (-v_i[i] + ei[i] - ii[i])
        
        rho_e[i+1], rho_i[i+1] = ephapticCoupling(v_e[i+1], v_i[i+1])

    return rho_e, rho_i, v_e, v_i