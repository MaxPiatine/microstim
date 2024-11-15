import matplotlib.pylab as plt
import numpy as np

from stim import microstim
from globals import weights, sigma, intensity


# heatmap
Wei_RANGE = np.arange(100, 300, 1)
inh_RANGE = np.arange(0, 200, 1)
heatmap = np.zeros((len(Wei_RANGE), len(inh_RANGE)))

for x, W_ei in enumerate(Wei_RANGE):
    weights["e->i"] = W_ei
    print(x)
    for y, direct_inh in enumerate(inh_RANGE):
        rho_e, rho_i, v_e, v_i = microstim(intensity, weights, sigma, e_amp=1, i_amp=direct_inh/100)
        heatmap[x][y] += max(rho_e)


plt.imshow(heatmap, origin="lower", cmap='plasma', interpolation="nearest", aspect="auto")
plt.colorbar()

# Set x-ticks at intervals of 0.25
x_ticks = np.arange(0, heatmap.shape[1], 1)  # Every unit corresponds to 0.25
x_labels = np.round(x_ticks * 0.25, 2)  # Scale to intervals of 0.25
plt.xticks(ticks=x_ticks, labels=[f"{label:.2f}" for label in x_labels])

# Set y-ticks at intervals of 20, from 100 to 300
y_ticks = np.arange(0, heatmap.shape[0], 1)  # Adjust based on number of rows
y_labels = np.arange(100, 100 + 20 * len(y_ticks), 20)  # Start from 100, step by 20
plt.yticks(ticks=y_ticks, labels=y_labels)

plt.xlabel("ephaptic inh.")
plt.ylabel("exc. to inh. weight")

plt.show()