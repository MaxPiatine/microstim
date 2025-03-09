import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
import os

from microstim.globals import sigma, weights, sigma, gamma, start_boost, no_boost, no_boost_weights
from microstim.main import model
from microstim.utils import rect, sigmoid, sigmoidalRect



boost = gamma.copy()
max_rho_e = []
max_rho_i = []
max_no_rho = []
intensity = np.arange(0.25, 300, 25)
for i in intensity:
    print("intensity %f" % i)
    _, _, rho_e, rho_i, _, _ = model(i, weights, sigma, rect, boost, is_depolarized=False)
    _, _, no_rho, _, _, _ = model(i, no_boost_weights, sigma, rect, no_boost, is_depolarized=False)
    max_rho_e.append(max(rho_e))
    max_rho_i.append(max(rho_i))
    max_no_rho.append(max(no_rho))


sns.set_theme(style="ticks")
palette = sns.color_palette("rocket_r", n_colors=3) 
ax = plt.subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xlabel("intensity")
plt.ylabel("radius")
plt.plot(intensity, max_no_rho, color=palette[0], label="no amp")
plt.plot(intensity, max_rho_e, color=palette[1], label="exc amp")
plt.plot(intensity, max_rho_i, color=palette[2], label="inh amp")
plt.legend(loc="best")  
plt.savefig("results/amp1/svg/intensityRadius.svg", format="svg", bbox_inches="tight")
plt.savefig("results/amp1/intensityRadius.png", format="png", bbox_inches="tight")
os.system('say "Intensity plot finished"')

plt.show()