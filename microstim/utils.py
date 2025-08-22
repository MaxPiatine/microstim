import gc
import torch
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
# from scipy.special import erf
# from math import sqrt

from microstim.config import config, DEVICE

"""
helpful functions
"""

RHEOBASE = config['RHEOBASE']
STEP = config['STEP']
THRESHOLD = config['THRESHOLD']
PULSE = config['PULSE']
MU_E = config['MU_E']
MU_I = config['MU_I']
STDEV_E = config['STDEV_E']
STDEV_I = config['STDEV_I']

def zeros(shape):
    return torch.zeros(shape, dtype=torch.float32, device=DEVICE)

@torch.jit.script
def maxRadius(v, x_range: torch.Tensor, threshold: int):
    # Find the last index where value > threshold
    mask = v > threshold
    
    # Get the last index where mask is True
    max_idx = torch.argmax(mask.to(torch.int32) * torch.arange(len(v), device=v.device))
    
    # Get the corresponding x_range values
    x_max = torch.where(torch.any(mask), x_range[max_idx], torch.tensor(0.0, device=v.device))
    
    return x_max  
def gaussian(x, mean, std):
    scale = 1.0 / (std * np.sqrt(2 * np.pi))
    return scale * np.exp(-(x - mean)**2 / (2 * std**2))

def lognormal(x, mu, sigma):
    return np.exp(-(np.log(x)-mu)**2/(2*sigma**2))/(x*sigma*np.sqrt(2*np.pi))

def intensityTreshold(diameter):
    return RHEOBASE*(1+np.exp(2.212)/(PULSE*diameter**0.355))

def diameter(threshold):
    return (PULSE*np.exp(-2.212)*(threshold/RHEOBASE-1))**(-200/71)

def diameterDerivative(threshold):
    return (200/71) * (np.exp(2.212)/PULSE)**(200/71) * (1/RHEOBASE) * (threshold/RHEOBASE - 1)**(-271/71)

def intensityPDF(threshold, mu_d, sigma_d):
    d = diameter(threshold)  
    coefficient = 1 / (sigma_d * np.sqrt(2 * np.pi)) * diameterDerivative(threshold)
    return coefficient * np.exp(-(d - mu_d)**2 / (2 * sigma_d**2))

def ConvertDiameterMean(mu_d, sigma_d):
    return RHEOBASE*(1+np.exp(2.212-0.355*mu_d+(0.355*sigma_d)**2/2)/PULSE)

def ConvertDiameterSigma(mu_d, sigma_d):
    return np.sqrt((RHEOBASE/PULSE)**2 * np.exp(4.424 - 0.71*mu_d) * (np.exp((0.71*sigma_d)**2/2)-np.exp((0.355*sigma_d)**2)))

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
def plot_tn(responses, time, distance):
    sns.set_theme(style="ticks")
    palette = sns.color_palette("rocket_r", n_colors=3) 

    f = plt.figure()
    ax = plt.subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.title("time "+str(time)+" ms")
    plt.xlabel("Distance (μm)")
    plt.ylabel("Relative Voltage mV")

    ax.hlines(20, 0 , max(distance), color="k", linestyles='-.')
    plt.plot(distance, responses[0], color=palette[1], label=r"$V_e$")
    plt.plot(distance, responses[1], color=palette[2], label=r"$V_i$")

    f.tight_layout()
    
    save_name = "./microstim/plot/results/"+str(time)+"plot.png"
    
    plt.savefig(save_name, transparent=True)
    
    plt.close()
    gc.collect()
