import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
import argparse

from microstim.globals import intensity, depol_weights, depol_sigma, act_weights, act_sigma, gamma, start_boost, no_boost, no_boost_weights, X_RANGE
from microstim.main import model
from microstim.utils import rect

parser = argparse.ArgumentParser(description="the maximum radius attained at different intensities")
parser.add_argument("--is_depol", action="store_true", help="Run depolarization model")
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
    
max_rho_e = []
max_rho_i = []
max_no_rho = []
intensities = np.arange(0, 300, 25)
for intensity in intensities:
    print("intensity %f" % intensity)
    _, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=is_depolarized)
    _, _, no_rho, _, _, _ = model(intensity, no_boost_weights, sigma, rect, no_boost, is_depolarized=is_depolarized)
    max_rho_e.append(max(rho_e))
    max_rho_i.append(max(rho_i))
    max_no_rho.append(max(no_rho))


sns.set_theme(style="ticks")
palette = sns.color_palette("rocket_r", n_colors=3) 
ax = plt.subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xlabel("intensity")
plt.ylabel("radius")
plt.plot(intensity, max_no_rho, color=palette[0], label="no amp")
plt.plot(intensity, max_rho_e, color=palette[1], label="exc amp")
plt.plot(intensity, max_rho_i, color=palette[2], label="inh amp")
plt.legend(loc="best")  

if is_production:
    plt.savefig(f"results/{typeModel}/svg/intensityRadius.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/intensityRadius.png", format="png", bbox_inches="tight")

plt.show()