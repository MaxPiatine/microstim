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
DX = config['dx']

def V_eph(x, R, I, alpha):
    return R*I/(x+alpha)**2

def zeros(shape):
    return torch.zeros(shape, dtype=torch.float32, device=DEVICE)

def slope(x, v, x0):
    if x0-1 <= 0:
        dx = torch.abs(x[x0+2] - x[x0])
        return (v[x0]-v[x0+2])/dx
    elif x0+1 >= len(v):
        dx = torch.abs(x[x0] - x[x0-2])
        return (v[x0-2]-v[x0])/dx
    dx = torch.abs(x[x0-1] - x[x0+1])
    return (v[x0-1]-v[x0+1])/dx

def x0s(v):
    mask = v >= 20.0
    diff = mask[1:].int() - mask[:-1].int()

    starts = torch.where(diff == 1)[0] + 1
    ends   = torch.where(diff == -1)[0]

    # Handle edge cases
    if mask[0]:
        starts = torch.cat([torch.tensor([0], device=v.device), starts])
    if mask[-1]:
        ends = torch.cat([ends, torch.tensor([len(v) - 1], device=v.device)])

    # Combine into one (N, 2) tensor
    runs = torch.stack([starts, ends], dim=1)

    return runs

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
    
def sigmoid(x, v, x0s):
    nu = torch.zeros_like(x)
    for x0 in x0s:
        tmp = torch.ones_like(x)
        if x0[0] == x0[1]:
            x0 = int(x0[0])
            tmp *= torch.sigmoid(-slope(x, v, x0) * (x - x[x0]))
        else:
            x0_start, x0_end = int(x0[0]), int(x0[1])

            if x0_start != 0:    
                start = slope(x, v, x0_start)
                tmp *= torch.sigmoid(-start * (x - x[x0_start]))

            end = slope(x, v, x0_end)
            tmp *= torch.sigmoid(-end * (x - x[x0_end]))
        nu += tmp
    return nu

def rect(v):
    return torch.where(v >= THRESHOLD, 1, 0)

def sigmoidalRect(v):
    x = rect(v)
    f = 1
    for index in enumerate(x):
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

    plt.ylim(-0.5, 20.5)
    ax.hlines(20, 0 , max(distance), color="k", linestyles='-.')
    ax.hlines(0, 0 , max(distance), color="k", linestyles='-.')
    plt.plot(distance, responses[0], color=palette[1], label=r"$V_e$")
    plt.plot(distance, responses[1], color="blue", label=r"$\nu_e$")
    # plt.plot(distance, responses[1], color=palette[2], label=r"$V_i$")

    f.tight_layout()
    
    save_name = "./microstim/plot/results/"+str(time)+"plot.png"
    plt.savefig(save_name, transparent=True)
    
    plt.close()
    gc.collect()

def make_kernel(sigma_val, weight_val):
        # radius in samples (at spatial resolution DX)
        radius_samples = max(1, int(np.ceil((5 * sigma_val) / DX)))
        # create coordinates in micrometers sampled at DX
        x = torch.linspace(-radius_samples * DX, radius_samples * DX,
                           2 * radius_samples + 1, dtype=torch.float32, device=DEVICE)
        k = normal(x, sigma_val)  # expected to return torch tensor
        k = k / k.sum()           # normalize kernel area to 1
        k = k * weight_val        # scale by synaptic weight
        # ensure odd kernel length so 'same' padding is symmetric
        return k.unsqueeze(0).unsqueeze(0)  # shape (1,1,klen)