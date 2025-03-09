import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
import os

from microstim.globals import sigma, weights, sigma, gamma, start_boost, no_boost, no_boost_weights
from microstim.main import model
from microstim.utils import rect, sigmoid, sigmoidalRect



boost = start_boost.copy()
max_pot = []
no_pot = []
intensity = np.arange(0, 300, 25)
for i in intensity:
    print("intensity %i" % i)
    v_e, _, _, _, _, _ = model(i, weights, sigma, rect, boost, is_depolarized=True)
    no_amp, _, _, _, _, _ = model(i, no_boost_weights, sigma, rect, no_boost, is_depolarized=True)
    max_pot.append(max(np.clip(v_e[:, 250], -100, 20)))
    no_pot.append(max(np.clip(no_amp[:,250], -100, 20)))


sns.set_theme(style="ticks")
palette = sns.color_palette("rocket_r", n_colors=3) 
ax = plt.subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xlabel("intensity")
plt.ylabel("mV")
plt.plot(intensity, no_pot, color=palette[0], label="no amp")
plt.plot(intensity, max_pot, color=palette[1], label="exc amp")
plt.legend(loc="best")  
plt.savefig("results/amp2/svg/intensityPotential.svg", format="svg", bbox_inches="tight")
plt.savefig("results/amp2/intensityPotential.png", format="png", bbox_inches="tight")
os.system('say "Intensity plot finished"')

plt.show()