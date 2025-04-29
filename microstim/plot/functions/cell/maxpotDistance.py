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

path = f"results/{typeModel}/potHeat.npz"
data = np.load(path)

x_range = data["x"]
v_e = data["y1"]
v_i = data["y2"]
no_amp = data["y3"]

sns.set_theme(style="ticks")
palette = sns.color_palette("rocket_r", n_colors=3)  # Reverse 'rocket' palette

ax = plt.subplot(111) 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Use the Seaborn palette colors
plt.plot(x_range, np.clip(np.max(v_e, axis=0), 0, 20), color=palette[1], label=r"amp $v_e$")
plt.plot(x_range, np.clip(np.max(v_i, axis=0), 0, 20), color=palette[2], label=r"amp $v_i$")
plt.plot(x_range, np.clip(np.max(no_amp, axis=0), 0, 20), color=palette[0], label="no amp")

# Add labels, limits, and legend
plt.xlabel("distance")
plt.ylabel("mV")
plt.legend(loc="best")

if is_production:
    plt.savefig(f"results/{typeModel}/svg/maxpotDistance.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/maxpotDistance.png", format="png", bbox_inches="tight")

plt.show()
