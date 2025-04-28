import os
import gc
import glob
import matplotlib.pylab as plt
import matplotlib.animation as animation
import seaborn as sns
import numpy as np

from PIL import Image

from microstim.axon import axon
from microstim.globals import axon_linspace, RHEOBASE, STEP, current_dir

files_path = current_dir + "/plot/results/"
"""
intensity is a function of distance. Assuming there is an initial intensity I_0 the 
numpy arange is the intensity I_0 changing with respect to distance
"""
intensities = np.arange(8.7, 12, 0.01)

ratios = []
for index, intensity in enumerate(intensities):
    integral_e, integral_i, ratio_e, ratio_i = axon(intensity)
    ratio_e = round(ratio_e, 2)
    ratio_i = round(ratio_i, 2)
    if ratio_e == 0:
        ratio = ratio_i
    else:
        ratio =  ratio_i/ ratio_e
    
    print(f"exc ratio of {intensity:.2f} μA, ratio i: {ratio_i}, ratio e: {ratio_e}, ratio {ratio}")
    ratios.append(ratio)

    sns.set_theme(style="ticks")
    palette = sns.color_palette("mako_r", n_colors=3) 

    ax = plt.subplot(111) 
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Shade the region below RHEOBASE
    plt.axvspan(0, RHEOBASE, color='gray', alpha=0.2)
    plt.plot(axon_linspace, integral_e, color=palette[0], label="exc")
    plt.plot(axon_linspace, integral_i, color=palette[1], label="inh")
    plt.fill_between(axon_linspace, integral_i, where=(axon_linspace < intensity), color='grey', alpha=0.3)
    plt.fill_between(axon_linspace, integral_e, where=(axon_linspace < intensity), color='grey', alpha=0.3)
    plt.axvline(intensity, color='black', linestyle='--', label=r"$I_T$")
    plt.title(f"{intensity:.2f} μA, ratio i: {ratio_i}, ratio e: {ratio_e}, ratio {ratio:.2f}")
    plt.xlabel("intensity threshold [μA]")
    plt.ylabel("I/E Ratio")
    plt.xlim([8.7, 12])
    plt.legend()
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
animated.save("./results/axon/axon_intensity.gif", writer="pillow", fps=30)
    
list(map(os.remove, glob.glob(os.path.join(files_path, "*.png"))))
os.system('say "Axon Dynamics GIF"')
plt.show()
