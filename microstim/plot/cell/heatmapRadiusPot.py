import matplotlib.pylab as plt
import seaborn as sns

from microstim.main import model, N, X, DISTANCE_RANGE, TIME_RANGE
from microstim.utils import rect
from microstim.plot.cell.utils import setup

def main():
    global config, is_depol, is_prod
    weights, boost, sigma, typeModel = setup(config, is_depol)
    
    v_e, _, _, _, _, _ = model(config["intensity"], weights, sigma, rect, boost, is_depolarized=is_depol)

    fig, ax = plt.subplots()

    v_e[v_e > 20.0] = 20  
    v_e[v_e < -10.0] = -10

    cmap = sns.color_palette("icefire", as_cmap=True)
    cs = ax.contourf(TIME_RANGE.cpu().numpy(), 
                    DISTANCE_RANGE.cpu().numpy(),
                    v_e.T, 
                    cmap=cmap,
                    extend='both',
                    alpha=0.7)

    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Distance (μm)")
    fig.suptitle("Sub-threshold voltage by distance and time")
    ax.set_xlim(right=max(N))
    ax.set_ylim(top=max(X))
    cbar = fig.colorbar(cs, label="Voltage (mV)")

    if is_prod:
        plt.savefig(f"results/{typeModel}/svg/potHeat.svg", format="svg", bbox_inches="tight")
        plt.savefig(f"results/{typeModel}/potHeat.png", format="png", bbox_inches="tight")
        
    plt.show()