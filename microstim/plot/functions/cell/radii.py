import matplotlib.pylab as plt
import seaborn as sns
import argparse

from microstim.globals import intensity, depol_weights, depol_sigma, act_weights, act_sigma, gamma, start_boost, no_boost, no_boost_weights, T_RANGE, DT
from microstim.main import model
from microstim.utils import rect

parser = argparse.ArgumentParser(description="maximum action potential propagation attained over time")
parser.add_argument("--is_depol", action="store_true", help="Run model with depolarization")
parser.add_argument("--is_prod", action="store_true", help="Run for production")

args = parser.parse_args()

is_depolarized = args.is_depol
is_production = args.is_prod
typeModel = ""

if is_depolarized:
    boost = start_boost.copy()
    weights = depol_weights.copy()
    sigma = depol_sigma.copy()
    typeModel += "Stoney"
else:
    boost = gamma.copy()
    weights = act_weights.copy()
    sigma = act_sigma.copy()
    typeModel += "Histed"
    
_, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=is_depolarized, radius_only=True)
_, _, no_amp, _, _, _ = model(intensity, no_boost_weights, sigma, rect, no_boost, is_depolarized=is_depolarized, radius_only=True)

sns.set_theme(style="ticks")
palette = sns.color_palette("rocket_r", n_colors=3) 

ax = plt.subplot(111) 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.plot(T_RANGE, no_amp, color=palette[0], label="No Amp")
plt.plot(T_RANGE, rho_e, color=palette[1], label=r"$\rho_e$")
plt.plot(T_RANGE, rho_i, color=palette[2], label=r"$\rho_i$")

plt.xlabel("time [ms]")
plt.ylabel(r"Radius [$\mu$m]")
plt.title(r"$\Delta t$ = " + str(DT) + " ms")
plt.legend(loc="best")

if is_production:
    plt.savefig(f"results/{typeModel}/svg/radii.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/radii.png", format="png", bbox_inches="tight")

plt.show()