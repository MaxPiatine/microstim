import math
import numpy as np
from microstim.utils import intensityPDF, intensityTreshold
from microstim.config import config

checkNormalized = False

MU_E = config["MU_E"]
MU_I = config["MU_I"]
STDEV_E = config["STDEV_E"]
STDEV_I = config["STDEV_I"]
STEP = float(config["STEP"])
RHEOBASE = config["RHEOBASE"]
ALPHA = config["ALPHA"]
AXON_LINSPACE = np.arange(RHEOBASE, 20, STEP)

def axon(intensity_at_axon, axon_diameter=None):
    if axon_diameter:
        threshold_for_diameter = intensityTreshold(axon_diameter)
        if intensity_at_axon < threshold_for_diameter:
            return None, None, 0, 0

        linspace = np.arange(RHEOBASE, intensity_at_axon, STEP)    
            
    else:
        linspace = AXON_LINSPACE


    if checkNormalized and axon_diameter is None:
        isNormal = 0
        for x in linspace:
                val = intensityPDF(x, mu_d=MU_E, sigma_d=STDEV_E)
                if math.isnan(val):
                    continue
                isNormal += val * STEP


        print("is it normalized?: ", isNormal)

    lognrml_e = intensityPDF(linspace, mu_d=MU_E, sigma_d=STDEV_E)
    lognrml_i = intensityPDF(linspace, mu_d=MU_I, sigma_d=STDEV_I)

    ratio_e = 0
    for i, x in enumerate(linspace):
        val = lognrml_e[i]
        if math.isnan(val):
            continue
            
        if x < intensity_at_axon:
            ratio_e += val * STEP

    ratio_i = 0
    for i, x in enumerate(linspace):
        val = lognrml_i[i]
        if math.isnan(val):
            continue

        if x < intensity_at_axon:
            ratio_i += val * STEP

    return lognrml_e, lognrml_i, ratio_e, ratio_i
            
        
def axonMapping(intensity, chunk, axons, stim_radii, resoltuion = 0.1):
    np.random.seed(2)

    grid_size = int(chunk / resoltuion)  
    half_grid = grid_size // 2

    stim_radius = int(stim_radii / resoltuion)  # in pixels

    max_possible_radius_microns = 10
    margin = int(np.ceil(max_possible_radius_microns / resoltuion)) + 2  # convert to pixels + buffer

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
    while placed_axons < axons and attempts < max_attempts:
        attempts += 1

        # Restrict placement to inner grid (to avoid touching edges)
        x_center = np.random.randint(margin, grid_size - margin)
        y_center = np.random.randint(margin, grid_size - margin)

        dx = (x_center - half_grid) * resoltuion
        dy = (y_center - half_grid) * resoltuion
        distance = np.sqrt(dx**2 + dy**2)  # in microns

        if np.random.random() > 0.4:
            axon_type = 1
            diameter = np.random.lognormal(MU_E, STDEV_E)
            radius_microns = diameter / 2
            radius = int(np.round(radius_microns / resoltuion)) 

            _, _, ratio_e, _ = axon(intensity/distance, diameter)
            ratio = ratio_e
            ratios_e += ratio_e
        else:
            axon_type = -1
            diameter = np.random.lognormal(MU_I, STDEV_I)
            radius_microns = diameter / 2
            radius = int(np.round(radius_microns / resoltuion)) 
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
            x_pos = (x_center - half_grid) * resoltuion
            y_pos = (y_center - half_grid) * resoltuion
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

    if ratios_e == 0:
        ratio = ratios_i
    else:
        ratio = round(ratios_i / ratios_e, 10)

    print(f"for intensity {intensity} μA, ratio of excitatory {ratios_e}, and inhibitory {ratios_i} => the recruitment ratio {ratio}")
    return axon_map, ratio