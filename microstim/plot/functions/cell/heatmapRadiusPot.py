import numpy as np
import argparse

from microstim.main import model
from microstim.globals import act_weights, act_sigma, depol_weights, depol_sigma, intensity, start_boost, gamma, X_RANGE, T_RANGE
from microstim.utils import rect

parser = argparse.ArgumentParser(description="heatmap of potential over time and space")
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
    
v_e, _, _, _, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=is_depolarized)


# Process the voltage data
# Set spike value (if you have spikes)
v_e[v_e > 20.0] = 20  # set height for spikes
# Set min value
v_e[v_e < -10.0] = -10


np.savez(f"results/{typeModel}/potHeat.npz", x=T_RANGE, y=X_RANGE, z=v_e)
