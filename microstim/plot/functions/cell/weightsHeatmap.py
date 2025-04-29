import matplotlib.pylab as plt
import numpy as np
import seaborn as sns
import argparse

from microstim.main import model
from microstim.globals import intensity, depol_weights, depol_sigma, act_weights, act_sigma, gamma, start_boost
from microstim.utils import rect

parser = argparse.ArgumentParser(description="heatmap of ei and ie weights")
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

w_ranges = np.arange(0, 500, 25)
heatmap = np.zeros((len(w_ranges), len(w_ranges)))

for y, ei in enumerate(w_ranges):
    weights["ei"] = ei
    for x, ie in enumerate(w_ranges):
        weights["ie"] = ie
        print(weights)
        _, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, start_boost, is_depolarized=is_depolarized)

        heatmap[x][y] += max(rho_e)

# Create the heatmap using seaborn
plt.figure(figsize=(8, 6))
ax = sns.heatmap(
    heatmap,
    xticklabels=np.round(w_ranges, 2),  
    yticklabels=np.round(w_ranges, 2),  
    linewidths=0.5, 
)

ax.invert_yaxis()

ax.set_xlabel(r"$w_{ie}$")
ax.set_ylabel(r"$w_{ei}$")

if is_production:
    plt.savefig(f"results/{typeModel}/svg/weights_heatmap.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/weights_heatmap.png", format="png", bbox_inches="tight")

plt.show()