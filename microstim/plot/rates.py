import matplotlib.pylab as plt
import numpy as np

from microstim.globals import T_RANGE, intensity, sigma, weights, gamma
from microstim.main import activationModel


activationModel(intensity, weights, sigma, gamma)

