import numpy as np
import argparse

from microstim.globals import intensity, depol_weights, depol_sigma, act_weights, act_sigma, gamma, start_boost, no_boost, no_boost_weights, T_RANGE
from microstim.main import model
from microstim.utils import rect

parser = argparse.ArgumentParser(description="maximum action potential propagation attained over time")
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
    
_, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=is_depolarized, radius_only=True)
_, _, no_amp, _, _, _ = model(intensity, no_boost_weights, sigma, rect, no_boost, is_depolarized=is_depolarized, radius_only=True)

np.savez(f"results/{typeModel}/radii.npz", x=T_RANGE, y1=rho_e, y2=rho_i, y3=no_amp)
