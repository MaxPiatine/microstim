import matplotlib.pylab as plt
import numpy as np

from microstim.main import depolarizationModel
from microstim.globals import intensity, weights, sigma, N, start_boost


intensity = 1000 #microA
intensity_RANGE = np.arange(0, intensity, intensity/N)

amp_weights = weights.copy()
amp_start_boost = start_boost.copy()

amp_weights["e->i"], amp_weights["i->i"], amp_start_boost["inh"] = 150, 100, 0.5

amp_rho_e, amp_rho_i, no_amp_rho_e, no_amp_v_e = [], [], [], []
for i, stim_intensity in enumerate(intensity_RANGE):
    rho_e, _, v_e, _ = depolarizationModel(stim_intensity, weights, sigma, start_boost)
    no_amp_rho_e.append(np.max(rho_e))
    rho_e, rho_i, v_e, _ = depolarizationModel(stim_intensity, amp_weights, sigma, amp_start_boost)
    amp_rho_e.append(np.max(rho_e)) 
    amp_rho_i.append(np.max(rho_i)) 

# plots
_, ax = plt.subplots(1, 1)
ax.plot(intensity_RANGE, no_amp_rho_e, label="no amp.", color="k")
ax.plot(intensity_RANGE, amp_rho_e, label="amp. exc.", color="tab:green")
ax.plot(intensity_RANGE, amp_rho_i, label="amp. exc.", color="tab:red")
ax.set_xlabel("stim. intensity [mA]")
ax.set_ylabel(r"radius [$\mu$m]")

plt.tight_layout()
plt.savefig("microstim/plot/figures/vectorize/DMrI.svg", format="svg", bbox_inches="tight")
plt.show()