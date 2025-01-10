import numpy as np
import matplotlib.pyplot as plt

from microstim.globals import X_RANGE, intensity, start_boost, weights, sigma, T_RANGE
from microstim.main import activationModel

# no amp
# no_rho_e, no_rho_i, no_v_e, no_v_i = activationModel(intensity, weights, sigma, start_boost)

# amp
weights = {
        "e->e": 150,
        "i->e": 100,
        "e->i": 200,
        "i->i": 100,
    }
gamma = {
    "exc": 10000,
    "inh": 1000,
}
rho_e, rho_i, v_e, v_i = activationModel(intensity, weights, sigma, gamma, start_boost)


# plots
_, ax = plt.subplots(1, 2)

ax[0].plot(X_RANGE, rho_e, label="amp. exc.")
for i in range(0, len(X_RANGE)-1, 200):
    # ax[0].plot(X_RANGE, no_rho_e[i], label="no amp.")
    # ax[0].plot(X_RANGE, rho_i[i], label="amp. inh.")

    # ax[1].plot(X_RANGE, np.clip(no_v_e[i], -20, 20), label="no amp.")
    ax[1].plot(X_RANGE, np.clip(v_e[i], -20, 20), label="amp. exc.")
    ax[1].plot(X_RANGE, np.clip(v_i[i], -20, 20), label="amp inh.")

# ax[2].plot(T_RANGE, np.clip(np.max(no_v_e, axis=1), -20, 20), label="no amp.")
# ax[2].plot(T_RANGE, np.clip(np.max(v_e, axis=1), -20, 20), label="amp. exc.")
# ax[2].plot(T_RANGE, np.clip(np.max(v_i, axis=1), -20, 20), label="amp inh.")
# ax[2].set_xlabel("normalized time")
# ax[2].set_ylabel("max. pot. [mV]")
# ax[2].legend()


ax[0].set_ylabel(r"radius [$\mu$m]")
ax[0].legend()

ax[1].set_xlabel(r"distance [$\mu$m]")
ax[1].set_ylabel("max. pot. [mV]")
ax[1].legend()

plt.tight_layout()
plt.show()