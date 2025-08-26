import matplotlib.pylab as plt
import seaborn as sns
import numpy as np

from microstim.main import model
from microstim.utils import rect
from microstim.plot.cell.utils import setup, intensities

def main():
    global config, is_depol, is_prod, position
    weights, boost, sigma, typeModel = setup(config, is_depol)

    max_pot = []
    no_pot = []

    for intensity in intensities:
        print("intensity %f" % intensity)
        v_e, _, _, _, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=is_depol)
        no_amp, _, _, _, _, _ = model(intensity, config["no_boost_weights"], sigma, rect, config["no_boost"], is_depolarized=is_depol)
        max_pot.append(max(np.clip(v_e[:, position], -100, 20)))
        no_pot.append(max(np.clip(no_amp[:, position], -100, 20)))


    sns.set_theme(style="ticks")
    palette = sns.color_palette("rocket_r", n_colors=3) 
    ax = plt.subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xlabel("intensity")
    plt.ylabel("mV")
    plt.plot(intensities, no_pot, color=palette[0], label="no amp")
    plt.plot(intensities, max_pot, color=palette[1], label="exc amp")
    plt.legend(loc="best")  

    if is_prod:
        plt.savefig(f"results/{typeModel}/svg/intensityPotentialX={position}microns.svg", format="svg", bbox_inches="tight")
        plt.savefig(f"results/{typeModel}/intensityPotentialX={position}microns.png", format="png", bbox_inches="tight")

    plt.show()