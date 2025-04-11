import matplotlib.pylab as plt
import numpy as np
import seaborn as sns
import os

from microstim.main import model
from microstim.globals import act_weights, act_sigma, depol_weights, depol_sigma, intensity, start_boost, gamma, X_RANGE, T_RANGE
from microstim.utils import rect

is_depol = True
is_test = True

if is_depol:
    boost = start_boost.copy()
    weights = depol_weights.copy()
    sigma = depol_sigma.copy()
else:
    boost = gamma.copy()
    weights = act_weights.copy()
    sigma = act_sigma.copy()
    
v_e, _, _, _, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=is_depol)

# Create figure with high resolution
fig, ax = plt.subplots()
# fig.set_dpi(900)  # increase resolution

# Process the voltage data
# Set spike value (if you have spikes)
v_e[v_e > 20.0] = 20  # set height for spikes
# Set min value
v_e[v_e < -10.0] = -10


# Create custom colormap using seaborn
cmap = sns.color_palette("icefire", as_cmap=True)

# Create contour plot
cs = ax.contourf(T_RANGE, X_RANGE, v_e.T, 
                cmap=cmap,  # or 'bwr', 'seismic', 'berlin', etc.
                extend='both',
                alpha=0.7)

# Add labels
ax.set_xlabel("Time (ms)")
ax.set_ylabel("Distance (μm)")
fig.suptitle("Sub-threshold voltage by distance and time")

# Set axis limits
ax.set_xlim(right=max(T_RANGE))
ax.set_ylim(top=max(X_RANGE))

# Add colorbar
cbar = fig.colorbar(cs, label="Voltage (mV)")

# Save the plot
print("saving")
plt.savefig("results/master/svg/potHeat.svg", format="svg", bbox_inches="tight")
plt.savefig("results/master/potHeat.png", format="png", bbox_inches="tight")

os.system('say "Your program has finished"')

plt.show()