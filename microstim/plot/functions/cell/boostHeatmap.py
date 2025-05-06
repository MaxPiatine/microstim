import numpy as np
import argparse

from microstim.main import model
from microstim.globals import intensity, gamma, start_boost, depol_weights, act_weights, act_sigma, depol_sigma
from microstim.utils import rect

parser = argparse.ArgumentParser(description="heatmap of excitatory and inhibitory start boosts")
parser.add_argument("--is_depol", action="store_true", help="Run model with depolarization")

args = parser.parse_args()

is_depolarized = args.is_depol
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

ranges = np.linspace(0, 500, 20) # 10 steps
heatmap = np.zeros((len(ranges), len(ranges)))

for x, inh_boost in enumerate(ranges):
    boost["inh"] = inh_boost
    for y, exc_boost in enumerate(ranges):
        boost["exc"] = exc_boost
        
        _, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=is_depolarized, radius_only=True)
        heatmap[x][y] += max(rho_e)

        print(boost)

np.save(f"results/{typeModel}/boost_heatmap.npy", heatmap)
