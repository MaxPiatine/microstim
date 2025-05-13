import matplotlib.pylab as plt
import argparse
from matplotlib import cm
import numpy as np

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
data = np.load(path, mmap_mode="r")

t_range = data["x"]
x_range = data["y"]
v_e = data["z"]

fig = plt.figure(num=8,figsize = (4.5,3), facecolor = 'w', dpi = 150, edgecolor = 'w')
fig.clf()
ax = plt.axes([0.15, 0.18, 0.8, 0.8])
fig, ax = plt.subplots()
cs = ax.contourf(t_range, x_range, v_e.T, 
                cmap=cm.PuBu_r,
                extend='both',
                alpha=0.7)

ax.set_xlabel("Time (ms)")
ax.set_ylabel("Distance (μm)")
fig.suptitle("Sub-threshold voltage by distance and time")
ax.set_xlim(0, 70)
ax.set_ylim(0, 1500)
cbar = fig.colorbar(cs, label="Voltage (mV)")

if is_production:
    plt.savefig(f"results/{typeModel}/svg/potHeat.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/potHeat.png", format="png", bbox_inches="tight")
    
plt.show()