import matplotlib.pylab as plt
import numpy as np

from matplotlib import cm
from microstim.main import model
from microstim.utils import rect
from microstim.plot.cell.utils import setup

def main():
    global config, is_depol, is_prod
    weights, boost, sigma, typeModel = setup(config, is_depol)

    Wei_RANGE = np.linspace(300, 900, 10)
    inh_RANGE = np.linspace(100, 600, 10)
    heatmap = np.zeros((len(Wei_RANGE), len(inh_RANGE)))

    for y, W_ei in enumerate(Wei_RANGE):
        weights["ie"] = W_ei # changing from i->e
        for x, direct_inh in enumerate(inh_RANGE):
            print(y, ": ", x)
            boost["inh"] = direct_inh
            _, _, rho_e, _, _, _ = model(config["intensity"], weights, sigma, rect, boost, is_depolarized=is_depol, radius_only=True)
            heatmap[x][y] += max(rho_e)


    
    fig = plt.figure(num=8,figsize = (4.5,3), facecolor = 'w', dpi = 150, edgecolor = 'w')
    fig.clf()
    ax = plt.axes([0.15, 0.18, 0.8, 0.8])
    ax.set_xlabel("inh rate")
    ax.set_ylabel(r"$w_{ie}$")
    
    cs = ax.contourf(inh_RANGE, Wei_RANGE, heatmap.T, cmap=cm.PuBu_r, vmin=0, vmax=1500, levels=10)
    fig.colorbar(cs)
    # ax.invert_yaxis()

    if is_prod:
        plt.savefig(f"results/{typeModel}/svg/heatmap.svg", format="svg", bbox_inches="tight")
        plt.savefig(f"results/{typeModel}/heatmap.png", format="png", bbox_inches="tight")

    plt.show()

