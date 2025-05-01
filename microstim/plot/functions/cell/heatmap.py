import numpy as np
import argparse

from microstim.main import model
from microstim.globals import intensity, gamma, start_boost, depol_weights, act_weights, act_sigma, depol_sigma
from microstim.utils import rect

parser = argparse.ArgumentParser(description="Run heatmap simulation.")
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

Wei_RANGE = np.arange(100, 300, 25)
inh_RANGE = np.arange(0, 400, 40)
heatmap = np.zeros((len(Wei_RANGE), len(inh_RANGE)))

for y, W_ei in enumerate(Wei_RANGE):
    weights["ei"] = W_ei
    for x, direct_inh in enumerate(inh_RANGE):
        print(y, ": ", x)
        boost["inh"] = direct_inh
        _, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=is_depolarized, radius_only=True)
        heatmap[x][y] += max(rho_i)

np.save(f"results/{typeModel}/heatmap.npy", heatmap)