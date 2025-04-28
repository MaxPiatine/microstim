import os
import gc
import glob
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
import matplotlib.animation as animation

from PIL import Image

from microstim.axon import axonMapping
from microstim.globals import ALPHA, RHEOBASE, current_dir

files_path = current_dir + "/plot/results/"

intensity = np.arange(RHEOBASE, 6, 0.1) #microAmp mm
axons = 100
chunk = 200
stim_radius = 1 + ALPHA  # stimulation radius in microns
resolution = 0.1 # resolution: microns per pixels

for index, i in enumerate(intensity):
    axon_map, ratio = axonMapping(i, axons, chunk, stim_radius, resolution)

    # GIF
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

    plt.title(f"{i:.2f} μA in slice, I/E ratio {ratio:.2f}")
    plt.axis("off")
    plt.grid(False)
    plt.tight_layout()

    save_name = "./microstim/plot/results/"+str(index)+"plot.png"
    
    plt.savefig(save_name, transparent=True)
    
    #close known Matplotlib memory leak
    plt.close()
    gc.collect()


files = sorted(glob.glob("./microstim/plot/results/*.png"), key=os.path.getmtime)
images = [np.array(Image.open(file)) for file in files]
os.makedirs("results", exist_ok=True)

fig, ax = plt.subplots()
im = ax.imshow(images[0], animated=True)
plt.axis("off") 

def update(i):
    im.set_array(images[i])
    return [im]

# Create the animation
animated = animation.FuncAnimation(
    fig, update, frames=len(images), interval=150, blit=True, repeat_delay=10
)

# Save the animation as a GIF
animated.save("./results/master/axon_map.gif", writer="pillow", fps=30)
    
list(map(os.remove, glob.glob(os.path.join(files_path, "*.png"))))
os.system('say "Axon Dynamics GIF"')
plt.show()

