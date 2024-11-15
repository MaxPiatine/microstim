import matplotlib.pylab as plt
import numpy as np

from stim import microstim
from globals import intensity, weights, sigma, N

intensity_RANGE = np.arange(0, intensity, intensity/N)

# no amp
no_rho_e, no_rho_i, no_v_e, no_v_i = microstim(intensity, weights, sigma)

# amp
weights["e->i"], weights["i->i"] = 150, 0
rho_e, rho_i, v_e, v_i = microstim(intensity, weights, sigma, e_amp=1, i_amp=0.5)

# plots
_, ax = plt.subplots(1, 2)

ax[0].plot(intensity_RANGE, no_rho_e, label="no amp.")
ax[0].plot(intensity_RANGE, rho_e, label="amp. exc.")
ax[0].plot(intensity_RANGE, rho_i, label="amp. inh.")
ax[0].set_xlabel("stim. intensity [mA]")
ax[0].set_ylabel(r"radius [$\mu$m]")
ax[0].legend()

ax[1].plot(intensity_RANGE, no_v_e[:, 100], label="no amp.")
ax[1].plot(intensity_RANGE, v_e[:, 100], label="amp. exc.")
ax[1].plot(intensity_RANGE, v_i[:, 100], label="amp inh.")
ax[1].set_xlabel("stim. intensity [mA]")
ax[1].set_ylabel("max. pot. [mV]")
ax[1].legend()

plt.tight_layout()
plt.show()