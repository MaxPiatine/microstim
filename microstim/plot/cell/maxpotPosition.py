import matplotlib.pylab as plt
import seaborn as sns
import numpy as np

from microstim.main import model, TIME_RANGE
from microstim.utils import rect
from microstim.plot.cell.utils import setup

def main():
    global config, is_depol, is_prod, position
    weights, boost, sigma, typeModel = setup(config, is_depol)

    v_e, v_i, _, _, _, _ = model(config["intensity"], weights, sigma, rect, boost, is_depolarized=is_depol)

    if is_prod:
        no_amp, _, _, _, _, _ = model(config["intensity"], config["no_boost_weights"], sigma, rect, config["no_boost"], is_depolarized=is_depol)

    # Use the Seaborn palette colors
    sns.set_theme(style="ticks")
    palette = sns.color_palette("rocket_r", n_colors=3)  # Reverse 'rocket' palette

    ax = plt.subplot(111) 
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.plot(TIME_RANGE.cpu().numpy(), np.clip(v_e[:, position], -100, 20), color=palette[1], label=r"amp $v_e$")
    plt.plot(TIME_RANGE.cpu().numpy(), np.clip(v_i[:, position], -100, 20), color=palette[2], label=r"amp $v_i$")
    if is_prod:
        plt.plot(TIME_RANGE, np.clip(no_amp[:, position], -100, 20), color=palette[0], label="no amp")

    # Add labels, limits, and legend
    plt.xlabel("Normalized Time")
    plt.ylabel("mV")
    plt.ylim([-20,20])
    plt.legend(loc="best")

    if is_prod:
        plt.savefig(f"results/{typeModel}/svg/maxpotX={position}microns.svg", format="svg", bbox_inches="tight")
        plt.savefig(f"results/{typeModel}/maxpotX={position}microns.png", format="png", bbox_inches="tight")

    plt.show()
