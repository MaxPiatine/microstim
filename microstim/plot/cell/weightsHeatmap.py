import matplotlib.pylab as plt
import numpy as np
import seaborn as sns

from microstim.main import model
from microstim.utils import rect
from microstim.plot.cell.utils import setup

def main():
    global config, is_depol, is_prod
    weights, boost, sigma, typeModel = setup(config, is_depol)
    

    w_ranges = np.arange(0, 500, 25)
    heatmap = np.zeros((len(w_ranges), len(w_ranges)))

    for y, ei in enumerate(w_ranges):
        weights["ei"] = ei
        for x, ie in enumerate(w_ranges):
            weights["ie"] = ie
            print(weights)
            _, _, rho_e, rho_i, _, _ = model(config["intensity"], weights, sigma, rect, boost, is_depolarized=is_depol)

            heatmap[x][y] += max(rho_e)

    # Create the heatmap using seaborn
    plt.figure(figsize=(8, 6))
    ax = sns.heatmap(
        heatmap,
        xticklabels=np.round(w_ranges, 2),  
        yticklabels=np.round(w_ranges, 2),  
        linewidths=0.5, 
    )

    ax.invert_yaxis()
    ax.set_xlabel(r"$w_{ie}$")
    ax.set_ylabel(r"$w_{ei}$")

    if is_prod:
        plt.savefig(f"results/{typeModel}/svg/weights_heatmap.svg", format="svg", bbox_inches="tight")
        plt.savefig(f"results/{typeModel}/weights_heatmap.png", format="png", bbox_inches="tight")

    plt.show()