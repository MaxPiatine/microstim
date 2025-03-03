import matplotlib.pylab as plt
import numpy as np
import seaborn as sns
import os

from microstim.main import model
from microstim.globals import weights, sigma, intensity, start_boost
from microstim.utils import rect

Wei_RANGE = np.arange(100, 300, 1)
inh_RANGE = np.arange(0, 200, 1)
heatmap = np.zeros((len(Wei_RANGE), len(inh_RANGE)))

for x, W_ei in enumerate(Wei_RANGE):
    weights["ei"] = W_ei
    print(x)
    for y, direct_inh in enumerate(inh_RANGE):
        start_boost["inh"] = direct_inh/100
        _, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, start_boost, is_depolarized=True)
        heatmap[x][y] += max(rho_i)


# Create the heatmap using seaborn
plt.figure(figsize=(8, 6))
ax = sns.heatmap(
    heatmap,
    xticklabels=np.round(Wei_RANGE, 2),  
    yticklabels=np.round(inh_RANGE, 2),  
    linewidths=0.5, 
)

ax.invert_yaxis()

ax.set_xlabel(r"$w_{ie}$")
ax.set_ylabel(r"$w_{ei}$")

os.system('say "Your program has finished"')

plt.show()