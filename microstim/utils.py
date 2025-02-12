import gc
import numpy as np
from microstim.globals import THRESHOLD, X_RANGE

import matplotlib.pylab as plt


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
    f = plt.figure()
    ax = plt.subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(-50, 150)

    plt.title("time step "+str(n))
    plt.xlabel("Distance (μm)")
    plt.ylabel("Relative Voltage mV")

    plt.plot(X_RANGE, responses)

    f.tight_layout()
    
    #for no ephaptic
    save_name = "./microstim/plot/results/"+str(n)+"connectivity.png"
    
    plt.savefig(save_name, transparent=True)
    
    #close known Matplotlib memory leak
    plt.close()
    gc.collect()