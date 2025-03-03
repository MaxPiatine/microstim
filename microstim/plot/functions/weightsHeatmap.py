import os
import matplotlib.pylab as plt
import numpy as np
import seaborn as sns

from microstim.main import model
from microstim.globals import weights, sigma, intensity, start_boost
from microstim.utils import rect


weights = {
        "ee": 400,
        "ie": 300,
        "ei": 0,
        "ii": 50,
    }
w_ranges = np.arange(0, 500, 25)
# boost_ranges = np.arange(0, 1, 0.1)
print(len(w_ranges), len(w_ranges))
heatmap = np.zeros((len(w_ranges), len(w_ranges)))

for y, ei in enumerate(w_ranges):
    weights["ei"] = ei
    for x, ie in enumerate(w_ranges):
        weights["ie"] = ie
        print(weights)
        _, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, start_boost, is_depolarized=True)

        heatmap[x][y] += max(rho_e)

# Create the heatmap using seaborn
plt.figure(figsize=(8, 6))
ax = sns.heatmap(
    heatmap,
    xticklabels=np.round(w_ranges, 2),  
    yticklabels=np.round(w_ranges, 2),  
    linewidths=0.5, 
)

ax.invert_yaxis()

ax.set_xlabel(r"$w_{ie}$")
ax.set_ylabel(r"$w_{ei}$")

os.system('say "Your program has finished"')

plt.show()