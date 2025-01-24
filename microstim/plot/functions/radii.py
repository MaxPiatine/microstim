import matplotlib.pylab as plt
import seaborn as sns
import numpy as np

from microstim.globals import T_RANGE, intensity, sigma, weights, sigma
from microstim.main import model
from microstim.utils import rect, sigmoid

_, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, is_depolarized=False)
print("done")
# weights = {
#         "ee": 150,
#         "ie": 150,
#         "ei": 150,
#         "ii": 150,
#     }
# _, _, no_amp, _, _, _ = model(intensity, weights, sigma, rect, is_depolarized=False)

# Set the Seaborn theme and palette
sns.set_theme(style="ticks")
palette = sns.color_palette("rocket_r", n_colors=3)  # Reverse 'rocket' palette

# Plot the data with Seaborn colors
ax = plt.subplot(111) 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# plt.plot(T_RANGE, no_amp, color=palette[0], label="No Amp")
plt.plot(T_RANGE, rho_e, color=palette[1], label=r"$\rho_e$")
plt.plot(T_RANGE, rho_i, color=palette[2], label=r"$\rho_i$")

# Add labels, limits, and legend

plt.xlabel("Normalized Time")
plt.xlim([0,5])
plt.ylabel(r"Radius [$\mu$m]")
plt.legend(loc="best")
# plt.savefig("microstim/plot/figures/vectorize/AMradii.svg", format="svg", bbox_inches="tight")
plt.show()
