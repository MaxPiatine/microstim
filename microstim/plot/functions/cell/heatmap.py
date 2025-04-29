import matplotlib.pylab as plt
import numpy as np
import seaborn as sns
import argparse

from microstim.main import model
from microstim.globals import intensity, gamma, start_boost, depol_weights, act_weights, act_sigma, depol_sigma
from microstim.utils import rect

parser = argparse.ArgumentParser(description="Run heatmap simulation.")
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

Wei_RANGE = np.arange(100, 300, 25)
inh_RANGE = np.arange(0, 400, 40)
heatmap = np.zeros((len(Wei_RANGE), len(inh_RANGE)))

for y, W_ei in enumerate(Wei_RANGE):
    weights["ei"] = W_ei
    for x, direct_inh in enumerate(inh_RANGE):
        print(y, ": ", x)
        boost["inh"] = direct_inh
        _, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=is_depolarized)
        heatmap[x][y] += max(rho_i)


# Create the heatmap using seaborn
plt.figure(figsize=(8, 6))
ax = sns.heatmap(
    heatmap,
    annot=True,
    xticklabels=np.round(Wei_RANGE, 2),  
    yticklabels=np.round(inh_RANGE, 2),  
    linewidths=0.5, 
)

ax.invert_yaxis()

ax.set_xlabel("inh boost")
ax.set_ylabel(r"$w_{ei}$")

if is_production:
    plt.savefig(f"results/{typeModel}/svg/heatmap.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/heatmap.png", format="png", bbox_inches="tight")

plt.show()