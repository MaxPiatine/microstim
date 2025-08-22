import matplotlib.pylab as plt
import seaborn as sns

from microstim.axon import axon
from microstim.config import AXON_LINSPACE, RHEOBASE

def main():
    global config, is_prod
    distance = 10 #microns 
    intensity_0 = 100 #microAmps
    intensity = intensity_0/distance

    sns.set_theme(style="ticks")
    palette = sns.color_palette("mako_r", n_colors=3) 

    ax = plt.subplot(111) 
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    integral_e, integral_i, _, _ = axon(intensity)

    # Shade the region below RHEOBASE
    plt.axvspan(0, RHEOBASE, color='gray', alpha=0.2)

    plt.plot(AXON_LINSPACE, integral_e, color=palette[0], label="exc")
    plt.plot(AXON_LINSPACE, integral_i, color=palette[1], label="inh")
    plt.title(f"{intensity_0} μA, {distance} μm from axon")
    plt.fill_between(AXON_LINSPACE, integral_i, where=(AXON_LINSPACE < intensity), color='grey', alpha=0.3)
    plt.axvline(intensity, color='black', linestyle='--', label=r"$I_T$")
    plt.xlabel("intensity threshold [μA]")
    plt.ylabel("probability")
    plt.legend(loc="best")
    plt.xlim([4, 15])
    if is_prod:
        plt.savefig("results/axon/svg/EI.svg", format="svg", bbox_inches="tight")
        plt.savefig("results/axon/EI.png", format="png", bbox_inches="tight")
    plt.show()
