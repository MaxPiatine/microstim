import numpy as np
import matplotlib.pylab as plt
from scipy.integrate import quad

from microstim.globals import N, i_RANGE, X_RANGE, ALPHA, DT, R, P, start_boost, gamma, T_RANGE
from microstim.utils import maxRadius, normal, plot_tn

def model(intensity, weights, sigma, rate, is_depolarized=True):
    rho_e, rho_i = np.zeros(N), np.zeros(N)
    nu_e, nu_i = np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE)))
    v_e, v_i = np.zeros((len(i_RANGE), len(X_RANGE))), np.zeros((len(i_RANGE), len(X_RANGE)))
    
    ee_linspace = np.linspace(-4*sigma["ee"], 4*sigma["ee"], N) 
    ie_linspace = np.linspace(-4*sigma["ie"], 4*sigma["ie"], N) 
    ei_linspace = np.linspace(-4*sigma["ei"], 4*sigma["ei"], N) 
    ii_linspace = np.linspace(-4*sigma["ii"], 4*sigma["ii"], N) 

    if is_depolarized:
        """
        depolarized model
        """
        v_e[0] = R*intensity/(X_RANGE + ALPHA)**P * start_boost["exc"]
        v_i[0] = R*intensity/(X_RANGE + ALPHA)**P * start_boost["inh"]
        
        nu_e[0] = rate(v_e[0])
        nu_i[0] = rate(v_i[0])
        
        rho_e[0], rho_i[0] = maxRadius(v_e[0], v_i[0])
    else:
        """
        activation model
        """
        nu_e[0] = np.log(intensity) * gamma["exc"] * normal(X_RANGE, sigma["ee"])
        nu_i[0] = np.log(intensity) * gamma["inh"] * normal(X_RANGE, sigma["ii"])
        
        # plt.plot(nu_e[0])
        # plt.show()
   
    # synaptic connectivity
    wee = weights["ee"] * normal(X_RANGE, sigma["ee"])
    wie = weights["ie"] * normal(X_RANGE, sigma["ie"])
    wei = weights["ei"] * normal(X_RANGE, sigma["ei"])
    wii = weights["ii"] * normal(X_RANGE, sigma["ii"])
    
    # def integrand(x):
    #     return weights["ee"] * normal(x, sigma["ee"])

    # # Integrate over the desired range
    # result, _ = quad(integrand, -4*sigma["ee"], 4*sigma["ee"])
    # print(result)

    plot_tn(v_e[0], 0)
            
    for i in range(0, len(i_RANGE)-1):

        v_e[i+1] = v_e[i] + DT * (-v_e[i] + np.convolve(wee, nu_e[i], mode="same") - np.convolve(wie, nu_i[i], mode="same"))
        v_i[i+1] = v_i[i] + DT * (-v_i[i] + np.convolve(wei, nu_e[i], mode="same") - np.convolve(wii, nu_i[i], mode="same"))
        
        nu_e[i+1] = rate(v_e[i+1])
        nu_i[i+1] = rate(v_i[i+1])
        
        rho_e[i+1], rho_i[i+1] = maxRadius(v_e[i+1], v_i[i+1])

        plot_tn(v_e[i+1], i+1)
        # print(i)
        # _, ax = plt.subplots(3, 1)
        # ax[0].plot(X_RANGE, v_e[i], label="v_e " + str(i))
        # ax[0].plot(X_RANGE, nu_e[i], label="nu_e " + str(i))
        # ax[0].legend()

        # ax[1].plot(X_RANGE, v_i[i], label="v_i " + str(i))
        # ax[1].plot(X_RANGE, nu_i[i], label="nu_i " + str(i))
        # ax[1].legend()

        # ax[2].plot(X_RANGE, np.convolve(wee, nu_e[i], mode="same") - np.convolve(wie, nu_i[i], mode="same"), label="K_e - K_i " + str(i))
        # plt.tight_layout()
        # plt.show()

    return v_e, v_i, rho_e, rho_i, nu_e, nu_i

