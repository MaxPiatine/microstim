import matplotlib.pylab as plt
import numpy as np

from globals import X_RANGE, T_RANGE, intensity, sigma, weights
from stim import microstim

# no amp
no_rho_e, no_rho_i, no_v_e, no_v_i = microstim(intensity, weights, sigma, e_amp=1, i_amp=1)

# amp
weights["e->i"], weights["i->i"] = 150, 0
rho_e, rho_i, v_e, v_i = microstim(intensity, weights, sigma, e_amp=1, i_amp=0.5)


# plots
_, ax = plt.subplots(1, 3)

ax[0].plot(T_RANGE, no_rho_e, label="no amp.")
ax[0].plot(T_RANGE, rho_e, label="amp. exc.")
ax[0].plot(T_RANGE, rho_i, label="amp. inh.")
ax[0].set_xlabel("normalized time")
ax[0].set_ylabel(r"radius [$\mu$m]")
ax[0].legend()

ax[1].plot(X_RANGE, no_v_e[:, 100], label="no amp.")
ax[1].plot(X_RANGE, v_e[:, 100], label="amp. exc.")
ax[1].plot(X_RANGE, v_i[:, 100], label="amp inh.")
ax[1].set_xlabel(r"distance [$\mu$m]")
ax[1].set_ylabel("max. pot. [mV]")
ax[1].legend()

ax[2].plot(T_RANGE, np.max(no_v_e, axis=1), label="no amp.")
ax[2].plot(T_RANGE, np.max(v_e, axis=1), label="amp. exc.")
ax[2].plot(T_RANGE, np.max(v_i, axis=1), label="amp inh.")
ax[2].set_xlabel("normalized time")
ax[2].set_ylabel("max. pot. [mV]")
ax[2].legend()

plt.tight_layout()
plt.show()