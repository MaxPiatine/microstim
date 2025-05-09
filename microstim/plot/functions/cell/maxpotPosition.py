import matplotlib.pylab as plt
import seaborn as sns
import argparse
import numpy as np

from microstim.globals import T_RANGE

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
path = f"results/{typeModel}/maxpotX={pos}microns.npz"
data = np.load(path)

v_e = data["y1"]
v_i = data["y2"]
no_amp = data["y3"]

fig = plt.figure(num=8,figsize = (4.5,3), facecolor = 'w', dpi = 150, edgecolor = 'w')
sns.set_theme(style="ticks")
palette = sns.color_palette("rocket_r", n_colors=3)  # Reverse 'rocket' palette

ax = plt.subplot(111) 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Use the Seaborn palette colors
plt.plot(T_RANGE, v_e, color=palette[1], label=r"amp $v_e$")
plt.plot(T_RANGE, v_i, color=palette[2], label=r"amp $v_i$")
plt.plot(T_RANGE, no_amp, color=palette[0], label="no amp")

# Add labels, limits, and legend
plt.xlabel("Normalized Time")
plt.ylabel("mV")
plt.ylim([-20,20])

if is_production:
    plt.savefig(f"results/{typeModel}/svg/maxpotX={pos}microns.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/maxpotX={pos}microns.png", format="png", bbox_inches="tight")

plt.show()
