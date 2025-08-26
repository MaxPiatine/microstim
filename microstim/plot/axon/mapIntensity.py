import matplotlib.pylab as plt
import seaborn as sns
import numpy as np

from microstim.axon import axonMapping, STEP, RHEOBASE

def main():
    global config

    intensity = np.arange(RHEOBASE+STEP, 20, 0.1) #microAmp mm
    axons = 100
    chunk = 200
    stim_radius = 1 + config["ALPHA"]  # stimulation radius in microns
    resolution = 0.1 # resolution: microns per pixels

    ratios = [axonMapping(i, axons, chunk, stim_radius, resolution)[1] for i in intensity]

    sns.set_theme(style="ticks")
    palette = sns.color_palette("mako_r", n_colors=3) 

    ax = plt.subplot(111) 
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Shade the region below RHEOBASE
    plt.axvspan(0, RHEOBASE, color='gray', alpha=0.2, label="Below Rheobase")
    plt.plot(intensity, ratios, color=palette[0])
    plt.xlabel("intensity threshold [μA]")
    plt.ylabel("ratio I/E")
    plt.xlim([0, max(intensity)])
    plt.show()