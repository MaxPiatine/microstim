import os
import matplotlib.pylab as plt
import numpy as np

from microstim.main import model
from microstim.globals import weights, sigma, intensity, gamma
from microstim.utils import rect

# heatmap
gamma_RANGE = np.arange(0, 200, 10)
heatmap = np.zeros((len(gamma_RANGE), len(gamma_RANGE)))

for x, g_i in enumerate(gamma_RANGE):
    gamma["inh"] = g_i
    for y, g_e in enumerate(gamma_RANGE):
        gamma["exc"] = g_e
        print(gamma)
        _, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, gamma, is_depolarized=False)
        heatmap[x][y] += max(rho_e)


plt.imshow(heatmap, origin="lower", cmap='plasma', interpolation="nearest", aspect="auto")
plt.colorbar()

plt.xlabel("gamma exc")
plt.ylabel("gamma inh")


os.system('say "your program has finished"')

plt.show()