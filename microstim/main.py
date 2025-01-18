import numpy as np

from microstim.globals import N, i_RANGE, X_RANGE, ALPHA, DT, R, P, start_boost, gamma, T_RANGE
from microstim.utils import ephapticCoupling

def model(intensity, weights, sigma, rate, is_depolarized=True):
    rho_e, rho_i = np.zeros(N), np.zeros(N)
    nu_e, nu_i = np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE)))
    v_e, v_i = np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE)))

    if is_depolarized:
        v_e[0] = R*intensity/(X_RANGE + ALPHA)**P * start_boost["exc"]
        v_i[0] = R*intensity/(X_RANGE + ALPHA)**P * start_boost["inh"]
        
        nu_e[0] = rate(v_e[0])
        nu_i[0] = rate(v_i[0])
        
        rho_e[0], rho_i[0] = ephapticCoupling(v_e[0], v_i[0])
    else:
        nu_e[0] = np.log(intensity) * gamma["exc"] * normal(sigma["ee"])
        nu_i[0] = np.log(intensity) * gamma["inh"] * normal(sigma["ii"])
        
    # synaptic connectivity
    wee = weights["ee"] * normal(sigma["ee"])
    wie = weights["ie"] * normal(sigma["ie"])
    wei = weights["ei"] * normal(sigma["ei"])
    wii = weights["ii"] * normal(sigma["ii"])
        
    for i in range(0, len(i_RANGE)-1):

        v_e[i+1] = v_e[i] + DT * (-v_e[i] + np.convolve(wee, nu_e[i], mode="same") - np.convolve(wie, nu_i[i], mode="same"))
        v_i[i+1] = v_i[i] + DT * (-v_i[i] + np.convolve(wei, nu_e[i], mode="same") - np.convolve(wii, nu_i[i], mode="same"))
        
        nu_e[i+1] = rate(v_e[i+1])
        nu_i[i+1] = rate(v_i[i+1])
        
        rho_e[i+1], rho_i[i+1] = ephapticCoupling(v_e[i+1], v_i[i+1])

    return rho_e, rho_i, v_e, v_i

