import numpy as np
from microstim.main import N, DT

def setup(config):
    boost = config["gamma"].copy()
    weights = config["weights"].copy()
    sigma = config["sigmas"].copy()
    return weights, boost, sigma

intensities = np.arange(0.25, 300, 25)
TIME_RANGE = np.arange(0, N * DT, DT)