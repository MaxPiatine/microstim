import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
import argparse

from microstim.globals import intensity, depol_weights, depol_sigma, act_weights, act_sigma, gamma, start_boost, no_boost, no_boost_weights, DX
from microstim.main import model
from microstim.utils import rect


parser = argparse.ArgumentParser(description="the maximum potential attained at different intensities")
parser.add_argument("--is_depol", action="store_true", help="Run depolarization model")
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

max_pot = []
no_pot = []
intensities = np.arange(0.25, 300, 25)

for intensity in intensities:
    print("intensity %f" % intensity)
    v_e, _, _, _, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=is_depolarized)
    no_amp, _, _, _, _, _ = model(intensity, no_boost_weights, sigma, rect, no_boost, is_depolarized=is_depolarized)
    max_pot.append(max(np.clip(v_e[:, position], -100, 20)))
    no_pot.append(max(np.clip(no_amp[:, position], -100, 20)))


sns.set_theme(style="ticks")
palette = sns.color_palette("rocket_r", n_colors=3) 
ax = plt.subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xlabel("intensity")
plt.ylabel("mV")
plt.plot(intensity, no_pot, color=palette[0], label="no amp")
plt.plot(intensity, max_pot, color=palette[1], label="exc amp")
plt.legend(loc="best")  

if is_production:
    plt.savefig(f"results/{typeModel}/svg/intensityPotentialX={args.position}microns.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/intensityPotentialX={args.position}microns.png", format="png", bbox_inches="tight")

plt.show()