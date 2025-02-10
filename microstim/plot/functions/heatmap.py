import os
import matplotlib.pylab as plt
import numpy as np

from microstim.main import model
from microstim.globals import weights, sigma, intensity, gamma, start_boost
from microstim.utils import rect

boost = start_boost.copy()
ranges = np.arange(0, 1, 0.1)


heatmap = np.zeros((len(ranges), len(ranges)))

for x, inh_boost in enumerate(ranges):
    boost["inh"] = inh_boost
    for y, exc_boost in enumerate(ranges):
        boost["exc"] = exc_boost
        
        _, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, gamma, boost, is_depolarized=True)
        heatmap[x][y] += max(rho_e)

        print(boost)


plt.imshow(heatmap, origin="lower", cmap='plasma', interpolation="nearest", aspect="auto")
plt.colorbar()

plt.xlabel(r"$k_I$")
plt.ylabel(r"$k_E$")


os.system('say "your program has finished"')

plt.show()