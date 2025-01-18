import matplotlib.pylab as plt
import numpy as np

from microstim.globals import T_RANGE, intensity, sigma, weights, gamma, start_boost
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

plt.plot(T_RANGE, np.clip(np.max(no_v_e, axis=1), -20, 20), color="k")
plt.plot(T_RANGE, np.clip(np.max(v_e, axis=1), -20, 20), color="tab:green")
plt.plot(T_RANGE, np.clip(np.max(v_i, axis=1), -20, 20), color="tab:red")
plt.xlabel("normalized time")
plt.ylabel("max. pot. [mV]")

plt.tight_layout()
plt.savefig("microstim/plot/figures/vectorize/AMmaxtime.svg", format="svg", bbox_inches="tight")
plt.show()