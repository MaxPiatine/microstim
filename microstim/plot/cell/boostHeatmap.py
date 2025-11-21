import matplotlib.pylab as plt
import numpy as np
import seaborn as sns
from matplotlib import cm
import os

from microstim.main import model
from microstim.utils import rect
from microstim.plot.cell.utils import setup

def main():
    global config, is_depol, is_prod
    weights, boost, sigma, typeModel = setup(config, is_depol)
    ranges = np.linspace(0, 1000, 20)
    heatmap = np.zeros((len(ranges), len(ranges)))
    resp = np.zeros((len(ranges), len(ranges)))

    for x, inh_boost in enumerate(ranges):
        boost["inh"] = inh_boost
        for y, exc_boost in enumerate(ranges):
            boost["exc"] = exc_boost
            
            _, _, rho_e, _, _, _, is_transient = model(config["intensity"], weights, sigma, rect, boost, is_depolarized=is_depol)
            heatmap[x][y] += max(rho_e)
            resp[x][y] = is_transient

            print(f"the network output is {'transient' if is_transient == 2 else 'unstable' if is_transient == 1 else 'stable'}")
            print(boost)

    # Create a single figure with two subplots (contourf on the left, seaborn heatmap on the right)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), dpi=150, constrained_layout=True)

    # Left: filled contour (transpose so orientation matches seaborn)
    cs = axes[0].contourf(ranges, ranges, heatmap.T, cmap=cm.PuBu_r, vmin=0, vmax=1500, levels=20)
    axes[0].set_xlabel(r"$\gamma_e$")
    axes[0].set_ylabel(r"$\gamma_i$")

    # Right: seaborn heatmap (no colorbar here, we'll use a single shared colorbar)
    sns.heatmap(
        heatmap.T,  # transpose to match contour orientation
        ax=axes[1],
        xticklabels=np.round(ranges, 2),
        yticklabels=np.round(ranges, 2),
        linewidths=0.5,
        cmap=cm.PuBu_r,
        vmin=0,
        vmax=1500,
        cbar=False,
    )
    axes[1].set_xlabel(r"$\gamma_e$")
    axes[1].set_ylabel(r"$\gamma_i$")

    # Shared colorbar for both subplots
    fig.colorbar(cs, ax=axes, orientation="vertical", fraction=0.025, pad=0.02)

    if is_prod:
        plt.savefig(f"results/{typeModel}/svg/heatmap.svg", format="svg", bbox_inches="tight")
        plt.savefig(f"results/{typeModel}/heatmap.png", format="png", bbox_inches="tight")

    plt.show()