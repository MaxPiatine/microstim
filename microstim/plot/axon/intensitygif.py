import os
import gc
import glob
import matplotlib.pylab as plt
import matplotlib.animation as animation
import seaborn as sns
import numpy as np

from PIL import Image

from microstim.axon import axon, RHEOBASE, STEP
from microstim.config import AXON_LINSPACE, current_dir

files_path = current_dir + "/plot/results/"
os.makedirs(files_path, exist_ok=True)

def main():
    global config, is_prod
    # Intensity sweep range
    intensities = np.arange(8.7, 12, 0.01)

    ratios = []
    intensity_vals = []  # For the lower ratio plot

    for index, intensity in enumerate(intensities):
        integral_e, integral_i, ratio_e, ratio_i = axon(intensity)
        ratio_e = round(ratio_e, 2)
        ratio_i = round(ratio_i, 2)
        if ratio_e == 0:
            ratio = ratio_i
        else:
            ratio = ratio_i / ratio_e

        print(f"exc ratio of {intensity:.2f} μA, ratio i: {ratio_i}, ratio e: {ratio_e}, ratio {ratio}")
        ratios.append(ratio)
        intensity_vals.append(intensity)

        # Plot the top panel (spatial profiles)
        sns.set_theme(style="ticks")
        palette = sns.color_palette("mako_r", n_colors=3) 

        ax = plt.subplot(111) 
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.axvspan(0, RHEOBASE, color='gray', alpha=0.2)
        plt.plot(AXON_LINSPACE, integral_e, color=palette[0], label="exc")
        plt.plot(AXON_LINSPACE, integral_i, color=palette[1], label="inh")
        plt.fill_between(AXON_LINSPACE, integral_i, where=(AXON_LINSPACE < intensity), color='grey', alpha=0.3)
        plt.fill_between(AXON_LINSPACE, integral_e, where=(AXON_LINSPACE < intensity), color='grey', alpha=0.3)
        plt.axvline(intensity, color='black', linestyle='--', label=r"$I_T$")
        plt.title(f"{intensity:.2f} μA, ratio i: {ratio_i}, ratio e: {ratio_e}, ratio {ratio:.2f}")
        plt.xlabel("intensity threshold [μA]")
        plt.ylabel("I/E Ratio")
        plt.xlim([8.7, 12])
        plt.legend()
        plt.tight_layout()

        save_name = os.path.join(files_path, f"{index}plot.png")
        plt.savefig(save_name, transparent=True)
        plt.close()
        gc.collect()

    # Gather saved images
    files = sorted(glob.glob(os.path.join(files_path, "*.png")), key=os.path.getmtime)
    images = [np.array(Image.open(file)) for file in files]

    # === Create the animation with 2 plots ===
    fig = plt.figure(figsize=(6, 8))
    from matplotlib.gridspec import GridSpec
    gs = GridSpec(2, 1, height_ratios=[3, 1])
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])

    im = ax1.imshow(images[0], animated=True)
    ax1.axis("off")

    # Lower plot setup
    line, = ax2.plot([], [], color="purple", label="I/E ratio")
    ax2.set_xlim([8.7, 12])
    ax2.set_ylim([0, max(ratios) + 1])
    ax2.set_xlabel("Intensity [μA]")
    ax2.set_ylabel("I/E Ratio")
    ax2.grid(True)
    ax2.legend()

    # Animation data holders
    growing_x, growing_y = [], []

    def update(i):
        im.set_array(images[i])
        growing_x.append(intensity_vals[i])
        growing_y.append(ratios[i])
        line.set_data(growing_x, growing_y)
        ax2.relim()
        ax2.autoscale_view(scalex=False, scaley=True)
        return [im, line]

    animated = animation.FuncAnimation(
        fig, update, frames=len(images), interval=150, blit=True, repeat_delay=10
    )

    # Save GIF
    os.makedirs("./results/axon", exist_ok=True)
    animated.save("./results/axon/axon_intensity.gif", writer="pillow", fps=30)

    # Clean up PNGs
    list(map(os.remove, files))
    os.system('say "Axon Dynamics GIF"')
    plt.show()
