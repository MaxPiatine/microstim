import numpy as np
import time

from microstim.globals import N, i_RANGE, X_RANGE, ALPHA, DT, R, P, TAU, THRESHOLD, D, ee_linspace, ei_linspace, ii_linspace, ie_linspace
from microstim.utils import maxRadius, normal, plot_tn

import matplotlib.pylab as plt
import seaborn as sns

def model(intensity, weights, sigma, rate, boost, is_depolarized=True):
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

        v_e[i+1] = v_e[i] + DT * (-1/TAU * v_e[i] + np.convolve(wee, nu_e[i], mode="same") - np.convolve(wie, nu_i[i], mode="same"))
        v_i[i+1] = v_i[i] + DT * (-1/TAU * v_i[i] + np.convolve(wei, nu_e[i], mode="same") - np.convolve(wii, nu_i[i], mode="same"))
        
        nu_e[i+1] = rate(v_e[i+1])
        nu_i[i+1] = rate(v_i[i+1])
        
        rho_e[i+1], rho_i[i+1] = maxRadius(v_e[i+1], v_i[i+1])
        
        # plot_tn([v_e[i], v_i[i]], i) # animations
        print("time step: ", i)

    print("%s seconds " % (time.time() - start_time))
    return v_e, v_i, rho_e, rho_i, nu_e, nu_i

