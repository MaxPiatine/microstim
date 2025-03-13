import numpy as np
from scipy import signal
import time

from microstim.globals import N, i_RANGE, X_RANGE, ALPHA, R, P, ee_linspace, ei_linspace, ii_linspace, ie_linspace, DT, TAU, SYN
from microstim.utils import maxRadius, normal, plot_tn, k_e, k_i, spectral_convolution, KernelConvolution

import matplotlib.pylab as plt

def model(intensity, weights, sigma, rate, boost, is_depolarized=True, gif=False):
    start_time = time.time()

    rho_e, rho_i = np.zeros(N), np.zeros(N)
    nu_e, nu_i = np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE)))
    v_e, v_i = np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE)))

    if is_depolarized:
        """
        depolarized model
        """
        v_e[0] = R*intensity/(X_RANGE + ALPHA)**P * boost["exc"]
        v_i[0] = R*intensity/(X_RANGE + ALPHA)**P * boost["inh"]
        
        nu_e[0] = rate(v_e[0])
        nu_i[0] = rate(v_i[0])
        
        rho_e[0], rho_i[0] = maxRadius(v_e[0], v_i[0])
    else:
        """
        activation model
        """
        nu_e[0] = np.log(intensity) * boost["exc"] * normal(X_RANGE, sigma["ee"])
        nu_i[0] = np.log(intensity) * boost["inh"] * normal(X_RANGE, sigma["ii"])


    # synaptic connectivity
    wee = weights["ee"] * normal(ee_linspace, sigma["ee"])
    wie = weights["ie"] * normal(ie_linspace, sigma["ie"])
    wei = weights["ei"] * normal(ei_linspace, sigma["ei"])
    wii = weights["ii"] * normal(ii_linspace, sigma["ii"])   

    for i in range(0, len(i_RANGE)-1):

        v_e[i+1] = v_e[i] + DT * (-1/TAU * v_e[i] + signal.convolve(wee, nu_e[i], mode="same")/SYN - np.convolve(wie, nu_i[i], mode="same")/SYN)
        v_i[i+1] = v_i[i] + DT * (-1/TAU * v_i[i] + signal.convolve(wei, nu_e[i], mode="same")/SYN - np.convolve(wii, nu_i[i], mode="same")/SYN)

        # v_e[i+1] = v_e[i] + DT * (-1/TAU * v_e[i] + spectral_convolution(nu_e[i], wee)/SYN - spectral_convolution(nu_i[i], wie)/SYN)
        # v_i[i+1] = v_i[i] + DT * (-1/TAU * v_i[i] + spectral_convolution(nu_e[i], wei)/SYN - spectral_convolution(nu_i[i], wii)/SYN)
        
        nu_e[i+1] = rate(v_e[i+1])
        nu_i[i+1] = rate(v_i[i+1])
        
        rho_e[i+1], rho_i[i+1] = maxRadius(v_e[i+1], v_i[i+1])
        
        if gif:
            plot_tn([v_e[i], v_i[i]], i) # animations

        # fig, axes = plt.subplots(2, 1)

        # # Display images
        # axes[0].plot(X_RANGE, v_e[i])
        # axes[0].plot(X_RANGE, nu_e[i])
        # axes[1].plot(X_RANGE, v_i[i])
        # axes[1].plot(X_RANGE, nu_i[i])

        # plt.tight_layout()
        # plt.show()

    print("%s seconds " % (time.time() - start_time))
    return v_e, v_i, rho_e, rho_i, nu_e, nu_i


def depolModel(intensity, weights, sigma, start_boost):
     rho_e, rho_i = np.zeros(N), np.zeros(N)
     v_e, v_i = np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE)))
 
     v_e[0] = R*intensity/(X_RANGE + ALPHA)**P * start_boost["exc"]
     v_i[0] = R*intensity/(X_RANGE + ALPHA)**P * start_boost["inh"]
 
     rho_e[0], rho_i[0] = maxRadius(v_e[0], v_i[0])
 
     # kernal arrays
     ee, ie, ei, ii = np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE)))
 
     for i in range(0, len(i_RANGE)-1):
        # if i * DT > 2.0:  # Wait for 2ms before updates
        #     rho_e[i+1], rho_i[i+1] = maxRadius(v_e[i+1], v_i[i+1])
        # else:
        #     rho_e[i+1], rho_i[i+1] = rho_e[i], rho_i[i]
 
        ee[i] = KernelConvolution(rho_e[i], weights["ee"], sigma["ee"]) 
        ie[i] = KernelConvolution(rho_i[i], weights["ie"], sigma["ie"])
        ei[i] = KernelConvolution(rho_e[i], weights["ei"], sigma["ei"])
        ii[i] = KernelConvolution(rho_i[i], weights["ii"], sigma["ii"])

        v_e[i+1] = v_e[i] + DT * (-v_e[i]/TAU + (ee[i] - ie[i])/SYN)

        v_i[i+1] = v_i[i] + DT * (-v_i[i]/TAU + (ei[i] - ii[i])/SYN)

        rho_e[i+1], rho_i[i+1] = maxRadius(v_e[i+1], v_i[i+1])

        # fig, axes = plt.subplots(4, 1)

        # # Display images
        # axes[0].plot(X_RANGE, v_e[i])
        # axes[1].plot(X_RANGE, ee[i] - ie[i])
        # axes[2].plot(X_RANGE, v_i[i])
        # axes[3].plot(X_RANGE, ei[i] - ii[i])

        # plt.tight_layout()
        # plt.show()
 
 
     return rho_e, rho_i, v_e, v_i