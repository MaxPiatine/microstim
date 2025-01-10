import matplotlib.pylab as plt

from microstim.globals import T_RANGE, intensity, sigma, weights, start_boost
from microstim.main import depolarizationModel

# no amp
no_rho_e, _, _, _ = depolarizationModel(intensity, weights, sigma, start_boost)

# amp
weights["e->i"], weights["i->i"], start_boost["inh"] = 200, 100, 0.5
rho_e, rho_i, _, _ = depolarizationModel(intensity, weights, sigma, start_boost)

plt.plot(T_RANGE, no_rho_e, color="k")
plt.plot(T_RANGE, rho_e, color="tab:green")
plt.plot(T_RANGE, rho_i, color="tab:red")
plt.xlabel("normalized time")
plt.xlim([0,5])
plt.ylabel(r"radius [$\mu$m]")

plt.tight_layout()
plt.savefig("microstim/plot/figures/vectorize/DMradii.svg", format="svg", bbox_inches="tight")
plt.show()
