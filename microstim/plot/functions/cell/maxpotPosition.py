import matplotlib.pylab as plt
import seaborn as sns
import argparse
import numpy as np

from microstim.globals import intensity, depol_weights, depol_sigma, act_weights, act_sigma, gamma, start_boost, no_boost, no_boost_weights, T_RANGE, DX
from microstim.main import model
from microstim.utils import rect

parser = argparse.ArgumentParser(description="the maximum potential function attained at a distance away from stim site")
parser.add_argument("--is_depol", action="store_true", help="Run model with depolarization")
parser.add_argument("--is_prod", action="store_true", help="Run for production")
parser.add_argument("--position", type=int, default=250, help="Position index (default: 250 microns)")

args = parser.parse_args()

is_depolarized = args.is_depol
is_production = args.is_prod
position = args.position/DX
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

v_e, v_i, _, _, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=is_depolarized)
no_amp, _, _, _, _, _ = model(intensity, no_boost_weights, sigma, rect, no_boost, is_depolarized=is_depolarized)

sns.set_theme(style="ticks")
palette = sns.color_palette("rocket_r", n_colors=3)  # Reverse 'rocket' palette

ax = plt.subplot(111) 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Use the Seaborn palette colors
plt.plot(T_RANGE, np.clip(v_e[:, position], -100, 20), color=palette[1], label=r"amp $v_e$")
plt.plot(T_RANGE, np.clip(v_i[:, position], -100, 20), color=palette[2], label=r"amp $v_i$")
plt.plot(T_RANGE, np.clip(no_amp[:, position], -100, 20), color=palette[0], label="no amp")

# Add labels, limits, and legend
plt.xlabel("Normalized Time")
plt.ylabel("mV")
plt.ylim([-20,20])
plt.legend(loc="best")

if is_production:
    plt.savefig(f"results/{typeModel}/svg/maxpotX={args.position}microns.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/maxpotX={args.position}microns.png", format="png", bbox_inches="tight")

plt.show()
