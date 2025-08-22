import matplotlib.pylab as plt
import numpy as np
import seaborn as sns

from microstim.main import model
from microstim.utils import rect
from microstim.plot.functions.cell.utils import setup

def main():
    global config, is_depol, is_prod
    weights, boost, sigma, typeModel = setup(config, is_depol)

    Wei_RANGE = np.linspace(100, 300, 10)
    inh_RANGE = np.linspace(0, 400, 10)
    heatmap = np.zeros((len(Wei_RANGE), len(inh_RANGE)))

    for y, W_ei in enumerate(Wei_RANGE):
        weights["ei"] = W_ei
        for x, direct_inh in enumerate(inh_RANGE):
            print(y, ": ", x)
            boost["inh"] = direct_inh
            _, _, rho_e, rho_i, _, _ = model(config["intensity"], weights, sigma, rect, boost, is_depolarized=is_depol, radius_only=True)
            heatmap[x][y] += max(rho_e)


    # Create the heatmap using seaborn
    plt.figure(figsize=(8, 6))
    ax = sns.heatmap(
        heatmap,
        annot=True,
        xticklabels=np.round(Wei_RANGE, 2),  
        yticklabels=np.round(inh_RANGE, 2),  
        linewidths=0.5, 
    )

    ax.invert_yaxis()
    ax.set_xlabel("inh boost")
    ax.set_ylabel(r"$w_{ei}$")

    if is_prod:
        plt.savefig(f"results/{typeModel}/svg/heatmap.svg", format="svg", bbox_inches="tight")
        plt.savefig(f"results/{typeModel}/heatmap.png", format="png", bbox_inches="tight")

    plt.show()

