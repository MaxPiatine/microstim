import gc
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

from microstim.globals import THRESHOLD, X_RANGE, R


def maxRadius(ve, vi):
    e_thresh, i_thresh = [], []
    for distance, e_pot, i_pot in zip(X_RANGE, ve, vi):
        if e_pot > THRESHOLD:
            e_thresh.append(distance)
        if i_pot > THRESHOLD:
            i_thresh.append(distance)
    return max(e_thresh, default=0), max(i_thresh, default=0)

"""
Rate functions
"""
def normal(x, sigma):
    return np.exp(-(x)**2/(2 * sigma**2)) / np.sqrt(2 * np.pi * sigma**2)
    
def sigmoid(v):
    return 1 / (1 + np.exp(-(THRESHOLD - v)))

def rect(v):
    return np.where(v >= THRESHOLD, 1, 0)

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
    
    save_name = "./microstim/plot/results2/"+str(n)+"plot.png"
    
    plt.savefig(save_name, transparent=True)
    
    #close known Matplotlib memory leak
    plt.close()
    gc.collect()