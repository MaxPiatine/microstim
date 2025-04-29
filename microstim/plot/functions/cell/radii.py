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

t_range = data["x"]
rho_e = data["y1"]
rho_i = data["y2"]
no_amp = data["y3"]

sns.set_theme(style="ticks")
palette = sns.color_palette("rocket_r", n_colors=3) 

ax = plt.subplot(111) 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.plot(t_range, no_amp, color=palette[0], label="No Amp")
plt.plot(t_range, rho_e, color=palette[1], label=r"$\rho_e$")
plt.plot(t_range, rho_i, color=palette[2], label=r"$\rho_i$")

plt.xlabel("time [ms]")
plt.ylabel(r"Radius [$\mu$m]")
plt.legend(loc="best")

if is_production:
    plt.savefig(f"results/{typeModel}/svg/radii.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/radii.png", format="png", bbox_inches="tight")

plt.show()