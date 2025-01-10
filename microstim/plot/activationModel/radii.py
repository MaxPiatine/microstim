import matplotlib.pylab as plt
import numpy as np

from microstim.globals import T_RANGE, intensity, sigma, weights, start_boost, gamma
from microstim.main import activationModel

# no amp
no_rho_e, _, _, _ = activationModel(intensity, weights, sigma, gamma, start_boost)

# amp
weights = {
        "e->e": 150,
        "i->e": 100,
        "e->i": 200,
        "i->i": 150,
    }

start_boost = {
    "exc": 1,
    "inh": 0.5,
}

gamma = {
    "exc": 10**5,
    "inh": 10**2,
}

rho_e, rho_i, _, _ = activationModel(intensity, weights, sigma, gamma, start_boost)

plt.plot(T_RANGE, no_rho_e, color="k")
plt.plot(T_RANGE, rho_e, color="tab:green")
plt.plot(T_RANGE, rho_i, color="tab:red")
plt.xlim([0,5])
plt.xlabel("normalized time")
plt.ylabel(r"radius [$\mu$m]")

plt.tight_layout()
plt.savefig("microstim/plot/figures/vectorize/AMradii.svg", format="svg", bbox_inches="tight")
plt.show()
