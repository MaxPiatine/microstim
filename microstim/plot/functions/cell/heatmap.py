import matplotlib.pylab as plt
import numpy as np
import seaborn as sns
import os

from microstim.main import model
from microstim.globals import act_weights, act_sigma, intensity, start_boost, gamma
from microstim.utils import rect

Wei_RANGE = np.arange(100, 300, 25)
inh_RANGE = np.arange(0, 400, 40)
heatmap = np.zeros((len(Wei_RANGE), len(inh_RANGE)))

boost = gamma.copy()
for y, W_ei in enumerate(Wei_RANGE):
    weights["ei"] = W_ei
    for x, direct_inh in enumerate(inh_RANGE):
        print(y, ": ", x)
        boost["inh"] = direct_inh
        _, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=False)
        heatmap[x][y] += max(rho_i)


# Create the heatmap using seaborn
plt.figure(figsize=(8, 6))
ax = sns.heatmap(
    heatmap,
    annot=True,
    xticklabels=np.round(Wei_RANGE, 2),  
    yticklabels=np.round(inh_RANGE, 2),  
    linewidths=0.5, 
)

ax.invert_yaxis()

ax.set_xlabel("inh boost")
ax.set_ylabel(r"$w_{ei}$")

plt.savefig("results/master/svg/amHeatmap.svg", format="svg", bbox_inches="tight")
plt.savefig("results/master/amHeatmap.png", format="png", bbox_inches="tight")

os.system('say "Your program has finished"')

plt.show()