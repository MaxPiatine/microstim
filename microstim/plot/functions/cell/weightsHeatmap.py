import numpy as np
import argparse

from microstim.main import model
from microstim.globals import intensity, depol_weights, depol_sigma, act_weights, act_sigma, gamma, start_boost
from microstim.utils import rect

parser = argparse.ArgumentParser(description="heatmap of ei and ie weights")
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


w_ranges = np.arange(0, 500, 25)
heatmap = np.zeros((len(w_ranges), len(w_ranges)))

for y, ei in enumerate(w_ranges):
    weights["ei"] = ei
    for x, ie in enumerate(w_ranges):
        weights["ie"] = ie
        print(weights)
        _, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, start_boost, is_depolarized=is_depolarized, radius_only=True)

        heatmap[x][y] += max(rho_e)

np.save(f"results/{typeModel}/weights_heatmap.npy", heatmap)