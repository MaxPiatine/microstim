import numpy as np
from microstim.main import N, DT

def setup(config, is_depol):
    typeModel = ""
    if is_depol:
        boost = config["start_boost"].copy()
        weights = config["depol_weights"].copy()
        typeModel += "Stoney"
    else:
        boost = config["gamma"].copy()
        weights = config["act_weights"].copy()
        typeModel += "Histed"

    sigma = config["sigmas"].copy()
    return weights, boost, sigma, typeModel

intensities = np.arange(0.25, 300, 25)
TIME_RANGE = np.arange(0, N * DT, DT)