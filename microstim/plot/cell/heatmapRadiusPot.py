import matplotlib.pylab as plt
import seaborn as sns

from matplotlib import cm
from microstim.main import model, N, X, DISTANCE_RANGE, TIME_RANGE
from microstim.utils import rect
from microstim.plot.cell.utils import setup

def main():
    global config, is_depol, is_prod
    weights, boost, sigma, typeModel = setup(config, is_depol)
    
    v_e, _, _, _, _, _ = model(config["intensity"], weights, sigma, rect, boost, is_depolarized=is_depol)


    v_e[v_e > 20.0] = 20  
    v_e[v_e < -10.0] = -10

    fig = plt.figure(num=8,figsize = (4.5,3), facecolor = 'w', dpi = 150, edgecolor = 'w')
    fig.clf()
    ax = plt.axes([0.15, 0.18, 0.8, 0.8])
    cs = ax.contourf(TIME_RANGE.cpu().numpy(), DISTANCE_RANGE.cpu().numpy(), v_e.T, 
                    cmap=cm.PuBu_r,
                    extend='both',
                    alpha=0.7,
                    levels=20)

    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Distance (μm)")
    fig.suptitle("Sub-threshold voltage by distance and time")
    ax.set_xlim(0, 70)
    ax.set_ylim(0, 1500)
    cbar = fig.colorbar(cs, label="Voltage (mV)")

    if is_prod:
        plt.savefig(f"results/{typeModel}/svg/potHeat.svg", format="svg", bbox_inches="tight")
        plt.savefig(f"results/{typeModel}/potHeat.png", format="png", bbox_inches="tight")
        
    plt.show()