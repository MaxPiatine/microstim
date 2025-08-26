import matplotlib.pylab as plt
import numpy as np
import seaborn as sns

from microstim.main import model
from microstim.utils import rect
from microstim.plot.cell.utils import setup

def main():
    global config, is_depol, is_prod
    weights, boost, sigma, typeModel = setup(config, is_depol)
    ranges = np.arange(0, 500, 25)
    heatmap = np.zeros((len(ranges), len(ranges)))

    for x, inh_boost in enumerate(ranges):
        boost["inh"] = inh_boost
        for y, exc_boost in enumerate(ranges):
            boost["exc"] = exc_boost
            
            _, _, rho_e, rho_i, _, _ = model(config["intensity"], weights, sigma, rect, boost, is_depolarized=is_depol)
            heatmap[x][y] += max(rho_e)

            print(boost)

    # Create the heatmap using seaborn
    plt.figure(figsize=(8, 6))
    ax = sns.heatmap(
        heatmap,
        xticklabels=np.round(ranges, 2),  
        yticklabels=np.round(ranges, 2),  
        linewidths=0.5, 
    )

    ax.invert_yaxis()

    ax.set_xlabel(r"$\alpha_e$")
    ax.set_ylabel(r"$\alpha_i$")

    if is_prod:
        plt.savefig(f"results/{typeModel}/svg/heatmap.svg", format="svg", bbox_inches="tight")
        plt.savefig(f"results/{typeModel}/heatmap.png", format="png", bbox_inches="tight")

    plt.show()