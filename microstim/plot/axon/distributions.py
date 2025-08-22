import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from microstim.axon import MU_E, MU_I, STDEV_I, STDEV_E
from microstim.utils import gaussian, intensityPDF

def main():
    global config, is_prod

    sns.set_theme(style="ticks")
    palette = sns.color_palette("mako_r", n_colors=3) 

    ax = plt.subplot(111) 
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Plot PDFs
    xd = np.linspace(0, 1, 1000)
    plt.plot(xd, gaussian(xd, MU_E, STDEV_E), color=palette[0], linewidth=2, label='exc diameters pdf')
    plt.plot(xd, gaussian(xd, MU_I, STDEV_I), color=palette[1], linewidth=2, label='inh diameters pdf')

    plt.xlabel('Axon Diameter (μm)')
    plt.ylabel('Probability Density')
    plt.title('Diameter Distribution')
    plt.legend()
    plt.savefig("results/axon/svg/EIdiameters.svg", format="svg", bbox_inches="tight")
    plt.savefig("results/axon/EIdiameters.png", format="png", bbox_inches="tight")
    plt.show()

    sns.set_theme(style="ticks")
    ax = plt.subplot(111) 
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    xIt = np.linspace(8, 12, 1000)
    plt.plot(xIt, intensityPDF(xIt, MU_E, STDEV_E), color=palette[0], linewidth=2, label='exc threshold pdf')
    plt.plot(xIt, intensityPDF(xIt, MU_I, STDEV_I), color=palette[1], linewidth=2, label='inh threshold pdf')

    plt.xlabel('Threshold Current (μA)')
    plt.ylabel('Probability Density')
    plt.title('Threshold Distribution')
    plt.legend()
    plt.tight_layout()
    
    if is_prod:
        plt.savefig("results/axon/svg/EIthresholds.svg", format="svg", bbox_inches="tight")
        plt.savefig("results/axon/EIthresholds.png", format="png", bbox_inches="tight")
    plt.show()
