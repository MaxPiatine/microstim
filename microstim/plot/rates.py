import matplotlib.pylab as plt
import numpy as np

from microstim.globals import T_RANGE, intensity, sigma, weights, start_boost
from microstim.main import depolarizationModel

# amp
weights["e->i"], weights["i->i"], start_boost["inh"] = 200, 100, 0.5
_, _, v_e, v_i = depolarizationModel(intensity, weights, sigma, start_boost)

plt.plot(T_RANGE, np.clip(np.max(v_i, axis=1), -20, 20), color="tab:red")
plt.xlabel("normalized time")
plt.ylabel("max. pot. [mV]")

plt.tight_layout()
plt.savefig("microstim/plot/figures/vectorize/DMmaxtime.svg", format="svg", bbox_inches="tight")
plt.show()