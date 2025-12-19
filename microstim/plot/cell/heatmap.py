import matplotlib.pylab as plt
import numpy as np
import torch

from matplotlib import cm
from microstim.main import model
from microstim.utils import rect, sigmoid
from microstim.plot.cell.utils import setup
from microstim.logging import _timestamp

def main():
    global config, is_prod
    weights, boost, sigma = setup(config)

    Wee_RANGE = np.linspace(300, 1000, 10)
    Wie_RANGE = np.linspace(200, 600, 10)
    heatmap = np.zeros((len(Wee_RANGE), len(Wie_RANGE)))

    for y, W_ee in enumerate(Wee_RANGE):
        weights["ee"] = round(W_ee, 2)
        for x, W_ie in enumerate(Wie_RANGE):
            print(f"Wee: {W_ee:.2f}, Wie: {W_ie:.2f}")
            weights["ie"] = round(W_ie, 2)
            _, _, rho_e, _, _, _ = model(config["intensity"], weights, sigma, sigmoid, boost, radius_only=True, is_gif=True)
            heatmap[x][y] += max(rho_e)

            # free large tensors and cached GPU/MPS memory
            del rho_e
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            elif hasattr(torch, "mps"):
                try:
                    torch.mps.empty_cache()
                except Exception:
                    pass

           # close any figures created during this iteration
            plt.close('all')


    
    fig = plt.figure(num=8,figsize = (4.5,3), facecolor = 'w', dpi = 150, edgecolor = 'w')
    fig.clf()
    ax = plt.axes([0.15, 0.18, 0.8, 0.8])
    ax.set_xlabel(r"$W_{ie}$")
    ax.set_ylabel(r"$w_{ee}$")
    
    cs = ax.contourf(Wie_RANGE, Wee_RANGE, heatmap.T, cmap=cm.PuBu_r, vmin=0, vmax=800, levels=10)
    fig.colorbar(cs)
    # ax.invert_yaxis()

    np.save(f"results/new/data/heatmap_{_timestamp()}.npy", heatmap)
    plt.savefig(f"results/new/svg/heatmap_{_timestamp()}.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/new/heatmap_{_timestamp()}.png", format="png", bbox_inches="tight")

    plt.show()

