import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="heatmap of excitatory and inhibitory start boosts")
parser.add_argument("--is_depol", action="store_true", help="Run model with depolarization")
parser.add_argument("--is_prod", action="store_true", help="Run for production")

args = parser.parse_args()

is_depolarized = args.is_depol
is_production = args.is_prod
typeModel = ""

if is_depolarized:
    typeModel += "Stoney"
else:
    typeModel += "Histed"

pos = 250 #microns
path = f"results/{typeModel}/intensityPotentialX={pos}microns.npz"
data = np.load(path)

intensity = data["x"]
max_pot = data["y1"]
no_pot = data["y2"]

fig = plt.figure(num=8,figsize = (4.5,3), facecolor = 'w', dpi = 150, edgecolor = 'w')
sns.set_theme(style="ticks")
palette = sns.color_palette("rocket_r", n_colors=3) 
ax = plt.subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xlabel("intensity")
plt.ylabel("mV")
intensities = np.arange(0.25, 300, 25)
plt.plot(intensities, no_pot, color=palette[0], label="no amp")
plt.plot(intensities, max_pot, color=palette[1], label="exc amp")

if is_production:
    plt.savefig(f"results/{typeModel}/svg/intensityPotentialX={pos}microns.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/intensityPotentialX={pos}microns.png", format="png", bbox_inches="tight")

plt.show()