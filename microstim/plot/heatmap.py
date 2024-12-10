import matplotlib.pylab as plt
import numpy as np

from microstim.main import microstim
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
        heatmap[x][y] += max(rho_i)


plt.imshow(heatmap, origin="lower", cmap='plasma', interpolation="nearest", aspect="auto")
plt.colorbar()

plt.xlabel("ephaptic inh.")
plt.ylabel("exc. to inh. weight")

plt.show()