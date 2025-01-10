import matplotlib.pylab as plt
import numpy as np

from microstim.globals import X_RANGE, intensity, sigma, weights, start_boost, gamma
from microstim.main import activationModel

# no amp
_, _, no_v_e, _ = activationModel(intensity, weights, sigma, gamma, start_boost)

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

_, _, v_e, v_i = activationModel(intensity, weights, sigma, gamma, start_boost)

plt.plot(X_RANGE, np.clip(no_v_e[:, 100], -20, 20), color="k")
plt.plot(X_RANGE, np.clip(v_e[:, 100], -20, 20), color="tab:green")
plt.plot(X_RANGE, np.clip(v_i[:, 100], -20, 20), color="tab:red")
plt.xlabel(r"distance [$\mu$m]")
plt.ylabel("max. pot. [mV]")

plt.tight_layout()
plt.savefig("microstim/plot/figures/vectorize/AMmaxpot.svg", format="svg", bbox_inches="tight")
plt.show()