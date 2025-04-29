import numpy as np
import argparse

from microstim.globals import intensity, depol_weights, depol_sigma, act_weights, act_sigma, gamma, start_boost, no_boost, no_boost_weights, X_RANGE
from microstim.main import model
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

v_e, v_i, _, _, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=is_depolarized)
no_amp, _, _, _, _, _ = model(intensity, no_boost_weights, sigma, rect, no_boost, is_depolarized=is_depolarized)

np.savez(f"results/{typeModel}/maxpotDistance.npz", x=X_RANGE, y=v_e, y2=v_i, y3=no_amp)