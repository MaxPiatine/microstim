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

path = f"results/{typeModel}/intensityRadius.npz"
data = np.load(path)

intensity = data["x"]
max_rho_e = data["y1"]
max_rho_i = data["y2"]
max_no_rho = data["y3"]

sns.set_theme(style="ticks")
palette = sns.color_palette("rocket_r", n_colors=3) 
ax = plt.subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xlabel("intensity")
plt.ylabel("radius")
plt.plot(intensity, max_no_rho, color=palette[0], label="no amp")
plt.plot(intensity, max_rho_e, color=palette[1], label="exc amp")
plt.plot(intensity, max_rho_i, color=palette[2], label="inh amp")
plt.legend(loc="best")  

if is_production:
    plt.savefig(f"results/{typeModel}/svg/intensityRadius.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/intensityRadius.png", format="png", bbox_inches="tight")

plt.show()