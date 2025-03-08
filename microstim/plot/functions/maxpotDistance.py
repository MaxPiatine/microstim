import os
import matplotlib.pylab as plt
import seaborn as sns
import numpy as np

from microstim.globals import X_RANGE, intensity, sigma, weights, start_boost, gamma
from microstim.main import model
from microstim.utils import rect, sigmoid

boost = start_boost.copy()
v_e, v_i, _, _, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=True)

weights = {
        "ee": 150,
        "ie": 150,
        "ei": 150,
        "ii": 150,
    }

no_boost = {
    "exc": 1,
    "inh": 1,
}

no_amp, _, _, _, _, _ = model(intensity, weights, sigma, rect, no_boost, is_depolarized=True)

sns.set_theme(style="ticks")
palette = sns.color_palette("rocket_r", n_colors=3)  # Reverse 'rocket' palette

ax = plt.subplot(111) 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Use the Seaborn palette colors
plt.plot(X_RANGE, np.clip(np.max(v_e, axis=0), 0, 20), color=palette[1], label=r"amp $v_e$")
plt.plot(X_RANGE, np.clip(np.max(v_i, axis=0), 0, 20), color=palette[2], label=r"amp $v_i$")
plt.plot(X_RANGE, np.clip(np.max(no_amp, axis=0), 0, 20), color=palette[0], label="no amp")

# Add labels, limits, and legend
plt.xlabel("distance")
plt.ylabel("mV")
plt.legend(loc="best")
plt.savefig("results/amp2/svg/maxpotDistance.svg", format="svg", bbox_inches="tight")
plt.savefig("results/amp2/maxpotDistance.png", format="png", bbox_inches="tight")
os.system('say "maximum potential finished"')

plt.show()
