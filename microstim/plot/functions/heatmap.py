import os
import matplotlib.pylab as plt
import numpy as np

from microstim.main import activationModel
from microstim.globals import weights, sigma, intensity, start_boost, gamma

# heatmap
Wei_RANGE = np.arange(0, 500, 1)
gamma_RANGE = np.arange(0, 500, 1)
heatmap = np.zeros((len(Wei_RANGE), len(gamma_RANGE)))

for x, W_ei in enumerate(Wei_RANGE):
    weights["e->i"] = W_ei
    print(x)
    for y, exc_gamma in enumerate(gamma_RANGE):
        gamma["exc"] = exc_gamma
        rho_e, rho_i, v_e, v_i = activationModel(intensity, weights, sigma, gamma, start_boost)
        heatmap[x][y] += max(rho_i)


plt.imshow(heatmap, origin="lower", cmap='plasma', interpolation="nearest", aspect="auto")
plt.colorbar()

plt.xlabel("ephaptic inh.")
plt.ylabel("exc. to inh. weight")


os.system('say "your program has finished"')

plt.show()