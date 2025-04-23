import matplotlib.pylab as plt
import seaborn as sns
import numpy as np

from microstim.axon import axonMapping
from microstim.globals import ALPHA

"""
we have a slice of 500 x 500 microns and we want to see how many axons will be recruited.
Assume there are ~90,000-100,000 neurons/mm^3 in the cortical region
Excitatory neurons make up ~80-85% of cortical neurons
Inhibitory neurons make up ~15-20%
If we minimally assume that there is 1 axon to each neuron then we would have
1063 excitatory axons vs 188 inhibitory neurons in a slice
"""



intensity = 1.5 #microAmp mm
axons = 100 # number of axons in slice
chunk = 200 # total area in microns (slice x slice) 
stim_radius = 1 + ALPHA  # stimulation radius in microns
resolution = 0.1 # resolution: microns per pixels

axon_map, ratio = axonMapping(intensity, axons, chunk, stim_radius, resolution)

cmap = sns.color_palette("vlag", as_cmap=True).reversed()
extent = [-chunk / 2, chunk / 2, -chunk / 2, chunk / 2]

plt.figure(figsize=(6, 6))
plt.imshow(axon_map, cmap=cmap, vmin=-1, vmax=1, origin='lower', extent=extent)

# Draw stimulation and reference areas
ax = plt.gca()

# Stimulation area
stim_circle = plt.Circle((0, 0), stim_radius, color='black', fill=False,
                         linestyle='--', linewidth=1.5, zorder=2)
ax.add_patch(stim_circle)

# Add reference circles
for r in [25, 50, 100]:
    circle = plt.Circle((0, 0), r, color='gold', fill=False,
                        linestyle=':', linewidth=1.2, alpha=0.7, zorder=0)
    ax.add_patch(circle)


# Draw the stimulation area
stim_circle = plt.Circle((0, 0), stim_radius, color='black', fill=False, linestyle='--', linewidth=1.5)
plt.gca().add_patch(stim_circle)

plt.title(f"{intensity} μA in slice, I/E ratio {ratio:.2f}")
plt.axis("off")
plt.grid(False)
plt.tight_layout()
plt.show()