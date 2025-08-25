import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from microstim.axon import MU_E, MU_I, STDEV_I, STDEV_E
from microstim.utils import gaussian, intensityPDF

def main():
    global config, is_prod, palette

    sns.set_theme(style="ticks")

    _, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8), sharex=False)

    for ax in (ax1, ax2):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    diameterPlot(ax1)
    intensityPlot(ax2)

    plt.tight_layout()
    plt.show()

def diameterPlot(ax):
    xd = np.linspace(0, 1, 1000)
    ax.plot(xd, gaussian(xd, MU_E, STDEV_E), color=palette[0], linewidth=2, label='exc diameters pdf')
    ax.plot(xd, gaussian(xd, MU_I, STDEV_I), color=palette[1], linewidth=2, label='inh diameters pdf')

    ax.set_xlabel('Axon Diameter (μm)')
    ax.set_ylabel('Probability Density')
    ax.set_title('Diameter Distribution')
    ax.legend()

    if is_prod:
        plt.savefig("results/axon/svg/EIdiameters.svg", format="svg", bbox_inches="tight")
        plt.savefig("results/axon/EIdiameters.png", format="png", bbox_inches="tight")


def intensityPlot(ax):
    xIt = np.linspace(8, 12, 1000)
    ax.plot(xIt, intensityPDF(xIt, MU_E, STDEV_E), color=palette[0], linewidth=2, label='exc threshold pdf')
    ax.plot(xIt, intensityPDF(xIt, MU_I, STDEV_I), color=palette[1], linewidth=2, label='inh threshold pdf')

    ax.set_xlabel('Threshold Current (μA)')
    ax.set_ylabel('Probability Density')
    ax.set_title('Threshold Distribution')
    ax.legend()

    if is_prod:
        plt.savefig("results/axon/svg/EIthresholds.svg", format="svg", bbox_inches="tight")
        plt.savefig("results/axon/EIthresholds.png", format="png", bbox_inches="tight")
