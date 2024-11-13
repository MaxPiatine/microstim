from math import sqrt
from scipy.special import erf
import matplotlib.pyplot as plt
import numpy as np
# from plot import plot

N = 1000

R = 7 #resistance (change) KOhms
ALPHA = 4 #micron
DT = 0.01

THRESHOLD = 20 #mV

i_RANGE = np.arange(0, N) #steps
X_RANGE = np.arange(0, 1000)


def KernelConvolution(x, rho, weight, sigma):
    return weight * ( erf( (x + rho) / (sqrt(2) * sigma) ) - erf( (x - rho) / (sqrt(2) * sigma) ) ) * 0.5


def microstim(intensity, weights, sigma, e_amp=1, i_amp=1, max_v=True):
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
        print("At Step %i: excitatory activation radius: %i microns inhibitory activation radius: %i microns"%(i+1, rho_e[i+1], rho_i[i+1]))

    if max_v:
        v_e = np.clip(v_e, -20, 20)
        v_i = np.clip(v_i, -20, 20)
        
    return rho_e, rho_i, v_e, v_i


if __name__ == "__main__":
    T = N * DT
    intensity = 500

    T_RANGE = np.arange(0, T, T/N)

    sigma = {
        "ee": 120,
        "ie": 120,
        "ei": 120,
        "ii": 120,
    } #microns

    weights = {
        "e->e": 150,
        "i->e": 150,
        "e->i": 150,
        "i->i": 150,
    }

    amp_weights = {
        "e->e": 100,
        "i->e": 100,
        "e->i": 150,
        "i->i": 0,
    }


    figure, ax = plt.subplots(1, 3)

    # amp
    rho_e, rho_i, v_e, v_i = microstim(intensity, amp_weights, sigma, e_amp=1, i_amp=0.5)

    # no amp
    no_rho_e, no_rho_i, no_v_e, no_v_i = microstim(intensity, weights, sigma, e_amp=1, i_amp=1)

    ax[0].plot(T_RANGE, no_rho_e, label="no amp.")
    ax[0].plot(T_RANGE, rho_e, label="amp. exc.")
    ax[0].plot(T_RANGE, rho_i, label="amp. inh.")
    ax[0].set_xlabel("normalized time")
    ax[0].set_ylabel(r"radius [$\mu$m]")
    ax[0].legend()

    ax[1].plot(X_RANGE, no_v_e[:, 100], label="no amp.")
    ax[1].plot(X_RANGE, v_e[:, 100], label="amp. exc.")
    ax[1].plot(X_RANGE, v_i[:, 100], label="amp inh.")
    ax[1].set_xlabel(r"distance [$\mu$m]")
    ax[1].set_ylabel("max. pot. [mV]")
    ax[1].legend()

    ax[2].plot(T_RANGE, np.max(no_v_e, axis=1), label="no amp.")
    ax[2].plot(T_RANGE, np.max(v_e, axis=1), label="amp. exc.")
    ax[2].plot(T_RANGE, np.max(v_i, axis=1), label="amp inh.")
    ax[2].set_xlabel("normalized time")
    ax[2].set_ylabel("max. pot. [mV]")
    ax[2].legend()

    plt.tight_layout()
    plt.show()
