import matplotlib.pylab as plt
import seaborn as sns
import numpy as np

from microstim.globals import X_RANGE, intensity, sigma, weights, start_boost, gamma, T_RANGE
from microstim.main import model
from microstim.utils import rect, sigmoid

v_e, v_i, _, _, _, _ = model(intensity, weights, sigma, rect, is_depolarized=False)

weights = {
        "ee": 150,
        "ie": 150,
        "ei": 150,
        "ii": 150,
    }
no_amp, _, _, _, _, _ = model(intensity, weights, sigma, rect, is_depolarized=False)

# Set the Seaborn theme and palette
sns.set_theme(style="ticks")
palette = sns.color_palette("rocket_r", n_colors=3)  # Reverse 'rocket' palette

# Plot the data with Seaborn colors
ax = plt.subplot(111) 
ax.spines['top'].set_visible(False)
ax.hlines(20, 0 ,1000)
ax.spines['right'].set_visible(False)

# Use the Seaborn palette colors
plt.plot(X_RANGE, np.max(v_e, axis=1), color="black", label="max over time")
plt.plot(X_RANGE, v_e[:][100], color=palette[1], label="amp v_e @ 100")

# Add labels, limits, and legend
plt.xlabel("distance")
plt.ylabel("mV")
plt.legend(loc="best")
plt.show()
