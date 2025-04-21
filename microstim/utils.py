import gc
import torch
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
from scipy.special import erf
from math import sqrt

from microstim.globals import THRESHOLD, X_RANGE, DT, TAU, SYN

# Boost and Hinder are used to manipulate the intensity pdf 
boost = 1
hinder = 100

"""
helpful functions
"""

@torch.jit.script
def maxRadius(v, x_range: torch.Tensor, threshold: int):
    # Find the last index where value > threshold
    mask = v > threshold
    
    # Get the last index where mask is True
    max_idx = torch.argmax(mask.to(torch.int32) * torch.arange(len(v), device=v.device))
    
    # Get the corresponding x_range values
    x_max = torch.where(torch.any(mask), x_range[max_idx], torch.tensor(0.0, device=v.device))
    
    return x_max  

def lognormal(x, mu, sigma):
    return np.exp(-(np.log(x)-mu)**2/(2*sigma**2))/(x*sigma*np.sqrt(2*np.pi))

def intensityPDF(intensity, rheobase, time, mu_d, sigma_d, isTest=False):
    mean_T = rheobase*(1+np.exp(2.212-0.355*mu_d+(0.355*sigma_d)**2/2)/time)/hinder
    sigma_T = np.sqrt((rheobase/time)**2 * np.exp(4.424 - 0.71*mu_d) * (np.exp((0.71*sigma_d)**2/2)-np.exp((0.355*sigma_d)**2)))
    
    if isTest:
        print(f"\nDebug values:")
        mean_exp = np.exp(2.212-0.355*mu_d+(0.355*sigma_d)**2)
        print(f"mean exp: {mean_exp}", f"rheobase: {rheobase*mean_exp}", f"mean_T: {mean_T}")
        print(f"sigma_T: {sigma_T}")
    log_arg = rheobase*np.exp(2.212)/((intensity-rheobase)*time)
    log_term = np.log(log_arg)
    if isTest:
        print(f"200*log_term/71: {200*log_term/71}")
        print(f"exponent: {-(200*log_term/71 - mean_T)**2/(2*sigma_T**2)}")
        print(f"exp(exponent): {np.exp(-(200*log_term/71 - mean_T)**2/(2*sigma_T**2))}")
        print(f"coefficient: {(200/(71*sigma_T*np.sqrt(2*np.pi))) * 1/(intensity-rheobase)}")
    
    return (200/(71*sigma_T*np.sqrt(2*np.pi))) * 1/(intensity-rheobase) * np.exp(-(boost*200*np.log(rheobase*np.exp(2.212)/((intensity-rheobase)*time))/71 - mean_T)**2/(2*sigma_T**2))

def ConvertDiameterMean(rheobase, time, mu_d, sigma_d):
    return rheobase*(1+np.exp(2.212-0.355*mu_d+(0.355*sigma_d)**2/2)/time)

def ConvertDiameterSigma(rheobase, time, mu_d, sigma_d):
    return np.sqrt((rheobase/time)**2 * np.exp(4.424 - 0.71*mu_d) * (np.exp((0.71*sigma_d)**2/2)-np.exp((0.355*sigma_d)**2)))

"""
Rate functions
"""
def normal(x, sigma):
    sigma_tensor = torch.tensor(sigma, dtype=torch.float32, device=x.device)
    return torch.exp(-(x)**2/(2 * sigma_tensor**2)) / torch.sqrt(2 * torch.pi * sigma_tensor**2)
    
def sigmoid(v):
    return 1 / (1 + np.exp(-(THRESHOLD - v)))

def rect(v):
    return torch.where(v >= THRESHOLD, 1, 0)

def sigmoidalRect(v):
    x = rect(v)
    f = 1
    for index, step in enumerate(x):
        try:
            if x[index] == 1 and x[index+1] == 0:
                f *= 1 / (1 + np.exp(-x + index/len(x)))
            elif x[index] == 0 and x[index+1] == 1:
                f *= 1 / (1 + np.exp(x - index/len(x)))
            else:
                continue
        except IndexError:
            continue
    return f

"""
animation plot
"""
def plot_tn(responses, n):
    sns.set_theme(style="ticks")
    palette = sns.color_palette("rocket_r", n_colors=3) 

    f = plt.figure()
    ax = plt.subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.title("time step "+str(n))
    plt.xlabel("Distance (μm)")
    plt.ylabel("Relative Voltage mV")

    ax.hlines(20, 0 , max(X_RANGE), color="k", linestyles='-.')
    plt.plot(X_RANGE, responses[0], color=palette[1], label=r"$V_e$")
    plt.plot(X_RANGE, responses[1], color=palette[2], label=r"$V_i$")

    f.tight_layout()
    
    save_name = "./microstim/plot/results/"+str(n)+"plot.png"
    
    plt.savefig(save_name, transparent=True)
    
    #close known Matplotlib memory leak
    plt.close()
    gc.collect()


"""
Runge-Kutta
"""
def dv_e_dt(v_e, nu_e, nu_i, wee, wie):
    return (-v_e/TAU + (np.convolve(wee, nu_e, mode="same") - np.convolve(wie, nu_i, mode="same"))/SYN)

def dv_i_dt(v_i, nu_e, nu_i, wei, wii):
    return (-v_i/TAU + (np.convolve(wei, nu_e, mode="same") - np.convolve(wii, nu_i, mode="same"))/SYN)

def k_e(v_e, nu_e, nu_i, wee, wie):
    k1_e = DT * dv_e_dt(v_e, nu_e, nu_i, wee, wie)
    k2_e = DT * dv_e_dt(v_e + 0.5 * k1_e, nu_e, nu_i, wee, wie)
    k3_e = DT * dv_e_dt(v_e + 0.5 * k2_e, nu_e, nu_i, wee, wie)
    k4_e = DT * dv_e_dt(v_e + k3_e, nu_e, nu_i, wee, wie)
    return k1_e + 2*k2_e + 2*k3_e + k4_e

def k_i(v_i, nu_e, nu_i, wei, wii):
    k1_i = DT * dv_i_dt(v_i, nu_e, nu_i, wei, wii)
    k2_i = DT * dv_i_dt(v_i + 0.5 * k1_i, nu_e, nu_i, wei, wii)
    k3_i = DT * dv_i_dt(v_i + 0.5 * k2_i, nu_e, nu_i, wei, wii)
    k4_i = DT * dv_i_dt(v_i + k3_i, nu_e, nu_i, wei, wii)
    return k1_i + 2*k2_i + 2*k3_i + k4_i

def spectral_convolution(signal, kernel):
    signal_fft = np.fft.fft(signal)
    kernel_fft = np.fft.fft(kernel)
    return np.fft.ifft(signal_fft * kernel_fft).real


def KernelConvolution(rho, weight, sigma):
     return erf( (X_RANGE + rho) / (sqrt(2) * sigma) ) - erf( (X_RANGE - rho) / (sqrt(2) * sigma) ) 