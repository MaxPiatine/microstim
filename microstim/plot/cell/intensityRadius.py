import matplotlib.pylab as plt
import seaborn as sns
import numpy as np

from microstim.main import model
from microstim.utils import rect
from microstim.plot.cell.utils import setup

def main():
    global config, is_depol, is_prod
    weights, boost, sigma, typeModel = setup(config, is_depol)
    
    max_rho_e = []
    max_rho_i = []
    max_no_rho = []
    intensities = np.arange(0, 300, 25)
    for intensity in intensities:
        print("intensity %f" % intensity)
        _, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=is_depol)
        _, _, no_rho, _, _, _ = model(intensity, config["no_boost_weights"], sigma, rect, config["no_boost"], is_depolarized=is_depol)
        max_rho_e.append(max(rho_e))
        max_rho_i.append(max(rho_i))
        max_no_rho.append(max(no_rho))


    sns.set_theme(style="ticks")
    palette = sns.color_palette("rocket_r", n_colors=3) 
    ax = plt.subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xlabel("intensity")
    plt.ylabel("radius")

    if is_prod:
        plt.plot(intensity, max_no_rho, color=palette[0], label="no amp")
    plt.plot(intensity, max_rho_e, color=palette[1], label="exc amp")
    plt.plot(intensity, max_rho_i, color=palette[2], label="inh amp")
    plt.legend(loc="best")  

    if is_prod:
        plt.savefig(f"results/{typeModel}/svg/intensityRadius.svg", format="svg", bbox_inches="tight")
        plt.savefig(f"results/{typeModel}/intensityRadius.png", format="png", bbox_inches="tight")

    plt.show()