import argparse
import numpy as np

from microstim.globals import intensity, depol_weights, depol_sigma, act_weights, act_sigma, gamma, start_boost, no_boost, no_boost_weights, T_RANGE, DX
from microstim.main import model
from microstim.utils import rect

parser = argparse.ArgumentParser(description="the maximum potential function attained at a distance away from stim site")
parser.add_argument("--is_depol", action="store_true", help="Run model with depolarization")
parser.add_argument("--position", type=int, default=250, help="Position index (default: 250 microns)")

args = parser.parse_args()

is_depolarized = args.is_depol
position = int(args.position/DX)
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
np.savez(f"results/{typeModel}/maxpotX={int(args.position)}microns.npz", x=T_RANGE, y1=np.clip(v_e[:, position], -100, 20), y2=np.clip(v_i[:, position], -100, 20), y3=np.clip(no_amp[:, position], -100, 20))
