import matplotlib.pylab as plt
import numpy as np

from microstim.stim import microstim
from microstim.globals import intensity, weights, sigma, N

intensity_RANGE = np.arange(0, intensity, intensity/N)

# no amp
no_amp_rho_e, no_amp_v_e  = [], []
for i in intensity_RANGE:
    print("no amp %i", i)
    rho_e, _, v_e, _ = microstim(intensity, weights, sigma)
    no_amp_rho_e.append(rho_e), no_amp_v_e.append(v_e)

# amp
weights["e->i"], weights["i->i"] = 150, 0
amp_rho_e, amp_rho_i, amp_v_e, amp_v_i  = [], [], [], []
for i in intensity_RANGE:
    print("amp %i", i)
    rho_e, rho_i, v_e, v_i = microstim(intensity, weights, sigma, e_amp=1, i_amp=0.5)
    amp_rho_e.append(rho_e), amp_rho_i.append(rho_i), amp_v_e.append(v_e), amp_v_i.append(v_i)

# plots
_, ax = plt.subplots(1, 2)

ax[0].plot(intensity_RANGE, no_amp_rho_e, label="no amp.")
ax[0].plot(intensity_RANGE, amp_rho_e, label="amp. exc.")
ax[0].plot(intensity_RANGE, amp_rho_i, label="amp. inh.")
ax[0].set_xlabel("stim. intensity [mA]")
ax[0].set_ylabel(r"radius [$\mu$m]")
ax[0].legend()

# ax[1].plot(intensity_RANGE, no_amp_v_e[:, 100], label="no amp.")
# ax[1].plot(intensity_RANGE, amp_v_e[:, 100], label="amp. exc.")
# ax[1].plot(intensity_RANGE, amp_v_i[:, 100], label="amp inh.")
# ax[1].set_xlabel("stim. intensity [mA]")
# ax[1].set_ylabel("max. pot. [mV]")
# ax[1].legend()

plt.tight_layout()
plt.show()