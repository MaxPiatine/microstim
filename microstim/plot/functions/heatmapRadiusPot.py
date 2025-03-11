import matplotlib.pylab as plt
import numpy as np
import seaborn as sns
import os

from microstim.main import model
from microstim.globals import weights, sigma, intensity, start_boost, gamma, X_RANGE, T_RANGE
from microstim.utils import rect


heatmap = np.zeros((len(X_RANGE), len(T_RANGE)))
boost = start_boost.copy()
v_e, _, _, _, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=True)

for x, t in enumerate(T_RANGE):
    print(t)
    for y, distance in enumerate(X_RANGE):
        heatmap[y][x] += 20 if v_e[x][y] > 20 else (-10 if v_e[x][y] < -10 else v_e[x][y])

print("plotting")
# Create the heatmap using seaborn
plt.figure(figsize=(8, 6))
# ax = sns.heatmap(
#     heatmap,
#     xticklabels=np.round(T_RANGE, 2),  
#     yticklabels=np.round(X_RANGE, 2),  
#     linewidths=0.5, 
# )

plt.imshow(heatmap, origin="lower", cmap="RdBu", interpolation="nearest", aspect="auto")
plt.colorbar()

# ax.invert_yaxis()

# ax.set_xlabel("normalized time")
# ax.set_ylabel(r"distance $\mu m$")

print("saving")
plt.savefig("results/master/svg/potHeat.svg", format="svg", bbox_inches="tight")
plt.savefig("results/master/potHeat.png", format="png", bbox_inches="tight")

os.system('say "Your program has finished"')

plt.show()