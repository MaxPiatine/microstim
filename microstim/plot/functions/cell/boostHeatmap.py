import argparse
import matplotlib.pylab as plt
import numpy as np
import seaborn as sns

from microstim.main import model
from microstim.globals import intensity, gamma, start_boost, depol_weights, act_weights, act_sigma, depol_sigma
from microstim.utils import rect

parser = argparse.ArgumentParser(description="heatmap of excitatory and inhibitory start boosts")
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

ranges = np.arange(0, 500, 25)
heatmap = np.zeros((len(ranges), len(ranges)))

for x, inh_boost in enumerate(ranges):
    boost["inh"] = inh_boost
    for y, exc_boost in enumerate(ranges):
        boost["exc"] = exc_boost
        
        _, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=is_depolarized)
        heatmap[x][y] += max(rho_e)

        print(boost)

# Create the heatmap using seaborn
plt.figure(figsize=(8, 6))
ax = sns.heatmap(
    heatmap,
    xticklabels=np.round(ranges, 2),  
    yticklabels=np.round(ranges, 2),  
    linewidths=0.5, 
)

ax.invert_yaxis()

ax.set_xlabel(r"$\alpha_e$")
ax.set_ylabel(r"$\alpha_i$")

if is_production:
    plt.savefig(f"results/{typeModel}/svg/heatmap.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/heatmap.png", format="png", bbox_inches="tight")

plt.show()