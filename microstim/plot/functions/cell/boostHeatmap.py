import os
import matplotlib.pylab as plt
import numpy as np
import seaborn as sns

from microstim.main import model
from microstim.globals import weights, sigma, intensity, gamma, start_boost
from microstim.utils import rect

boost = gamma.copy()
ranges = np.arange(0, 500, 50)


heatmap = np.zeros((len(ranges), len(ranges)))

for x, inh_boost in enumerate(ranges):
    boost["inh"] = inh_boost
    for y, exc_boost in enumerate(ranges):
        boost["exc"] = exc_boost
        
        _, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=False)
        heatmap[x][y] += max(rho_e)

        print(boost)

# Create the heatmap using seaborn
plt.figure(figsize=(8, 6))
ax = sns.heatmap(
    heatmap,
    xticklabels=np.round(ranges, 2),  
    yticklabels=np.round(ranges, 2),  
    linewidths=0.5, 
)

ax.invert_yaxis()

ax.set_xlabel(r"$\alpha_e$")
ax.set_ylabel(r"$\alpha_i$")

os.system('say "Your program has finished"')

plt.show()