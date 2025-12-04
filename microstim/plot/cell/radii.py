import matplotlib.pylab as plt
import seaborn as sns

from microstim.main import model, DT
from microstim.utils import sigmoid
from microstim.plot.cell.utils import setup, TIME_RANGE

def main():
    global config, is_prod
    weights, boost, sigma = setup(config)
    
    _, _, rho_e, rho_i, _, _ = model(config["intensity"], weights, sigma, sigmoid, boost, radius_only=True)
    if is_prod:
        _, _, no_amp, _, _, _ = model(config["intensity"], config["no_boost_weights"], sigma, sigmoid, config["no_boost"], radius_only=True)

    sns.set_theme(style="ticks")
    palette = sns.color_palette("rocket_r", n_colors=3) 

    ax = plt.subplot(111) 
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    if is_prod:
        plt.plot(TIME_RANGE, no_amp, color=palette[0], label="No Amp")
    plt.plot(TIME_RANGE, rho_e, color=palette[1], label=r"$\rho_e$")
    plt.plot(TIME_RANGE, rho_i, color=palette[2], label=r"$\rho_i$")

    plt.xlabel("time [ms]")
    plt.ylabel(r"Radius [$\mu$m]")
    plt.title(r"$\Delta t$ = " + str(DT) + " ms")
    plt.legend(loc="best")

    if is_prod:
        plt.savefig("results/new/svg/radii.svg", format="svg", bbox_inches="tight")
        plt.savefig("results/new/radii.png", format="png", bbox_inches="tight")

    plt.show()