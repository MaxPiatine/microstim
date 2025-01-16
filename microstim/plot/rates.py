import matplotlib.pylab as plt
import numpy as np

from microstim.globals import T_RANGE, intensity, sigma, weights, gamma, start_boost
from microstim.main import model, depolarizationModel

# start_boost["inh"] = 0.5
# depolarizationModel(intensity, weights, sigma, start_boost)
model(intensity, weights, sigma, is_depolarized=True)

