import matplotlib.pylab as plt
import seaborn as sns
import numpy as np

from microstim.main import model, DISTANCE_RANGE
from microstim.utils import rect
from microstim.plot.cell.utils import setup

def main():
    global config, is_depol, is_prod
    weights, boost, sigma, typeModel = setup(config, is_depol)

    v_e, v_i, _, _, _, _ = model(config["intensity"], weights, sigma, rect, boost, is_depolarized=is_depol)
    no_amp, _, _, _, _, _ = model(config["intensity"], config["no_boost_weights"], sigma, rect, config["no_boost"], is_depolarized=is_depol)

    # Use the Seaborn palette colors
    sns.set_theme(style="ticks")
    palette = sns.color_palette("rocket_r", n_colors=3)

    ax = plt.subplot(111) 
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.plot(DISTANCE_RANGE.cpu().numpy(), np.clip(np.max(v_e, axis=0), 0, 20), color=palette[1], label=r"amp $v_e$")
    plt.plot(DISTANCE_RANGE.cpu().numpy(), np.clip(np.max(v_i, axis=0), 0, 20), color=palette[2], label=r"amp $v_i$")
    if is_prod:
        plt.plot(DISTANCE_RANGE.cpu().numpy(), np.clip(np.max(no_amp, axis=0), 0, 20), color=palette[0], label="no amp")

    plt.xlabel("distance")
    plt.ylabel("mV")
    plt.legend(loc="best")

    if is_prod:
        plt.savefig(f"results/{typeModel}/svg/maxpotDistance.svg", format="svg", bbox_inches="tight")
        plt.savefig(f"results/{typeModel}/maxpotDistance.png", format="png", bbox_inches="tight")

    plt.show()
