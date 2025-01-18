from microstim.globals import intensity, sigma, weights
from microstim.main import model
from microstim.utils import rect, normal, sigmoid


model(intensity, weights, sigma, rect, is_depolarized=False)

