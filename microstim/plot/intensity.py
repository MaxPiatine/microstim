import matplotlib.pylab as plt
import numpy as np

from microstim.main import depolarizationModel
from microstim.globals import intensity, weights, sigma, N, start_boost

intensity *= 10**(-7)
intensity_RANGE = np.arange(0, intensity, intensity/N)

amp_weights = weights.copy()
amp_start_boost = start_boost.copy()

amp_weights["e->i"], amp_weights["i->i"], amp_start_boost["inh"] = 150, 100, 0.5

amp_rho_e, no_amp_rho_e = [], []
for i, stim_intensity in enumerate(intensity_RANGE):
    percentage = (i / N) * 100
    if percentage.is_integer(): 
        print(f"{int(percentage)}%")
    rho_e, _, _, _ = depolarizationModel(stim_intensity, weights, sigma, start_boost)
    no_amp_rho_e.append(np.max(rho_e))
    rho_e, _, _, _ = depolarizationModel(stim_intensity, amp_weights, sigma, amp_start_boost)
    amp_rho_e.append(np.max(rho_e)) 

# plots
_, ax = plt.subplots(1, 1)
ax.plot(intensity_RANGE, no_amp_rho_e, label="no amp.")
ax.plot(intensity_RANGE, amp_rho_e, label="amp. exc.")
ax.set_xlabel("stim. intensity [mA]")
ax.set_ylabel(r"radius [$\mu$m]")
ax.legend()

plt.tight_layout()
plt.show()