from microstim.globals import intensity, sigma, weights
from microstim.main import model
from microstim.utils import rect, normal, sigmoid


v_e, v_i, rho_e, rho_i, nu_e, nu_i = model(intensity, weights, sigma, rect, is_depolarized=True)



