import matplotlib.pylab as plt
import numpy as np

from globals import X_RANGE, T_RANGE, intensity, sigma, weights
from stim import microstim

# unstable
weights["e->i"], weights["i->i"] = 125, 100
unstable_rho_e, unstable_rho_i, unstable_v_e, unstable_v_i = microstim(intensity, weights, sigma, e_amp=1, i_amp=0.5, max_v=False)

# amp
weights["e->i"], weights["i->i"] = 150, 100
rho_e, rho_i, v_e, v_i = microstim(intensity, weights, sigma, e_amp=1, i_amp=0.5, max_v=False)


# plots
_, ax = plt.subplots(1, 3)

ax[0].plot(T_RANGE, unstable_rho_e, label="unstable exc.")
ax[0].plot(T_RANGE, unstable_rho_i, label="unstable inh.")
ax[0].plot(T_RANGE, rho_e, label="amp. exc.")
ax[0].plot(T_RANGE, rho_i, label="amp. inh.")
ax[0].set_xlabel("normalized time")
ax[0].set_ylabel(r"radius [$\mu$m]")
ax[0].legend()

ax[1].plot(X_RANGE, unstable_v_e[:, 100], label="unstable exc.")
ax[1].plot(X_RANGE, unstable_v_i[:, 100], label="unstable inh.")
ax[1].plot(X_RANGE, v_e[:, 100], label="amp. exc.")
ax[1].plot(X_RANGE, v_i[:, 100], label="amp inh.")
ax[1].set_xlabel(r"distance [$\mu$m]")
ax[1].set_ylabel("potential [mV]")
ax[1].legend()

ax[2].plot(T_RANGE, np.max(unstable_v_e, axis=1), label="unstable exc.")
ax[2].plot(T_RANGE, np.max(unstable_v_i, axis=1), label="unstable inh.")
ax[2].plot(T_RANGE, np.max(v_e, axis=1), label="amp. exc.")
ax[2].plot(T_RANGE, np.max(v_i, axis=1), label="amp inh.")
ax[2].set_xlabel("normalized time")
ax[2].set_ylabel("max. pot. [mV]")
ax[2].legend()

plt.tight_layout()
plt.show()