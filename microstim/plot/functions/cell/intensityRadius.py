import numpy as np
import argparse

from microstim.globals import intensity, depol_weights, depol_sigma, act_weights, act_sigma, gamma, start_boost, no_boost, no_boost_weights
from microstim.main import model
from microstim.utils import rect

parser = argparse.ArgumentParser(description="the maximum radius attained at different intensities")
parser.add_argument("--is_depol", action="store_true", help="Run depolarization model")

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
    
max_rho_e = []
max_rho_i = []
max_no_rho = []
intensities = np.arange(0, 300, 25)
for intensity in intensities:
    print("intensity %f" % intensity)
    _, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=is_depolarized, radius_only=True)
    _, _, no_rho, _, _, _ = model(intensity, no_boost_weights, sigma, rect, no_boost, is_depolarized=is_depolarized, radius_only=True)
    max_rho_e.append(max(rho_e))
    max_rho_i.append(max(rho_i))
    max_no_rho.append(max(no_rho))


np.savez(f"results/{typeModel}/intensityRadius.npz", x=intensities, y1=max_rho_e, y2=max_rho_i, y3=max_no_rho)
