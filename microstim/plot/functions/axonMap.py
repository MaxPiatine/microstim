import matplotlib.pylab as plt
from matplotlib.colors import ListedColormap
import seaborn as sns
import numpy as np

from microstim.axon import axon
from microstim.utils import intensityTreshold
from microstim.globals import MU_E, MU_I, STDEV_E, STDEV_I, ALPHA

"""
we have a slice of 500 x 500 microns and we want to see how many axons will be recruited.
Assume there are ~90,000-100,000 neurons/mm^3 in the cortical region
Excitatory neurons make up ~80-85% of cortical neurons
Inhibitory neurons make up ~15-20%
If we minimally assume that there is 1 axon to each neuron then we would have
1063 excitatory axons vs 188 inhibitory neurons in a slice
"""

np.random.seed(2)

intensity = 10 #microAmp mm

# Parameters
micron_range = 200       # total area in microns
res = 0.1               # resolution: microns per pixel
grid_size = int(micron_range / res)  # 500
half_grid = grid_size // 2
num_axons = 100
stim_radius_microns = 1 + ALPHA  # stimulation radius in microns
stim_radius = int(stim_radius_microns / res)  # in pixels

# https://www.eneuro.org/content/5/5/ENEURO.0297-18.2018#:~:text=The%20nodes%20of%20Ranvier%20(Rasband,n%20=%20100%20nonGABA%20nodes%20from
# https://pmc.ncbi.nlm.nih.gov/articles/PMC10068302/#:~:text=The%20axon%20diameter%20of%20myelinated,159%2C%20P%20%3C%200.001).

max_possible_radius_microns = 10
margin = int(np.ceil(max_possible_radius_microns / res)) + 2  # convert to pixels + buffer

# Initialize map and mask
axon_map = np.zeros((grid_size, grid_size), dtype=int)
occupied_mask = np.zeros_like(axon_map, dtype=bool)

# Create an exclusion mask around the center for electrode stimulation
y_indices, x_indices = np.ogrid[:grid_size, :grid_size]
center_mask = (x_indices - half_grid) ** 2 + (y_indices - half_grid) ** 2 <= stim_radius ** 2
occupied_mask[center_mask] = True  # mark as unavailable

# Store axon information for plotting
axons_info = []  # will store (x, y, radius, ratio, axon_type)

# Populate axons
attempts = 0
placed_axons = 0
max_attempts = 10000

ratios_e = 0
ratios_i = 0
while placed_axons < num_axons and attempts < max_attempts:
    attempts += 1

    # Restrict placement to inner grid (to avoid touching edges)
    x_center = np.random.randint(margin, grid_size - margin)
    y_center = np.random.randint(margin, grid_size - margin)

    dx = (x_center - half_grid) * res
    dy = (y_center - half_grid) * res
    distance = np.sqrt(dx**2 + dy**2)  # in microns

    if np.random.random() > 0.4:
        axon_type = 1
        diameter = np.random.lognormal(MU_E, STDEV_E)
        radius_microns = diameter / 2
        radius = int(np.round(radius_microns / res)) 

        _, _, ratio_e, _ = axon(intensity/distance, diameter)
        ratio = ratio_e
        ratios_e += ratio_e
    else:
        axon_type = -1
        diameter = np.random.lognormal(MU_I, STDEV_I)
        radius_microns = diameter / 2
        radius = int(np.round(radius_microns / res)) 
        _, _, ratio_i, _ = axon(intensity/distance, diameter)
        ratio = ratio_i
        ratios_i += ratio_i

    # Calculate bounding box
    x_min = x_center - radius - 1
    x_max = x_center + radius + 2
    y_min = y_center - radius - 1
    y_max = y_center + radius + 2

    # Create mask for axon placement
    y_idx, x_idx = np.ogrid[y_min:y_max, x_min:x_max]
    dist_sq = (x_idx - x_center) ** 2 + (y_idx - y_center) ** 2
    full_disk_mask = dist_sq <= radius ** 2
    ring_mask = (dist_sq <= radius ** 2) & (dist_sq >= (radius - 1) ** 2)

    subregion_mask = occupied_mask[y_min:y_max, x_min:x_max]

    if not np.any(subregion_mask[full_disk_mask]):
        # Store axon info for plotting
        x_pos = (x_center - half_grid) * res
        y_pos = (y_center - half_grid) * res
        axons_info.append((x_pos, y_pos, radius_microns, ratio, axon_type))
        
        # Mark the axon in the map
        if ratio != 0:
            # Fill the entire disk for activated axons
            axon_map[y_min:y_max, x_min:x_max][full_disk_mask] = axon_type
        else:
            # Just the ring for non-activated axons
            axon_map[y_min:y_max, x_min:x_max][ring_mask] = axon_type
        
        occupied_mask[y_min:y_max, x_min:x_max][full_disk_mask] = True
        placed_axons += 1

try:
    ratio = ratios_i/ratios_e
except ZeroDivisionError:
    ratio = ratios_i

print(f"ratio of excitatory {ratios_e}, and inhibitory {ratios_i} => the recruitment ratio {ratio}")

cmap = sns.color_palette("vlag", as_cmap=True).reversed()
extent = [-micron_range / 2, micron_range / 2, -micron_range / 2, micron_range / 2]

plt.figure(figsize=(6, 6))
plt.imshow(axon_map, cmap=cmap, vmin=-1, vmax=1, origin='lower', extent=extent)

# Draw stimulation and reference areas
ax = plt.gca()

# Stimulation area
stim_circle = plt.Circle((0, 0), stim_radius_microns, color='black', fill=False,
                         linestyle='--', linewidth=1.5, zorder=2)
ax.add_patch(stim_circle)

# Add reference circles
for r in [25, 50, 100]:
    circle = plt.Circle((0, 0), r, color='gold', fill=False,
                        linestyle=':', linewidth=1.2, alpha=0.7, zorder=0)
    ax.add_patch(circle)


# Draw the stimulation area
stim_circle = plt.Circle((0, 0), stim_radius_microns, color='black', fill=False, linestyle='--', linewidth=1.5)
plt.gca().add_patch(stim_circle)

plt.title(f"{intensity} μA in slice, I/E ratio {ratio:.2f}")
plt.axis("off")
plt.grid(False)
plt.tight_layout()
plt.show()