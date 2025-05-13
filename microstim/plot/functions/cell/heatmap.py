import matplotlib.pylab as plt
from matplotlib import cm
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
    Wei_RANGE = np.linspace(100, 300, 20)
    inh_RANGE = np.linspace(0, 1.25, 20)
else:
    Wei_RANGE = np.linspace(0, 1000, 20)
    inh_RANGE = np.linspace(0, 1000, 20)
    typeModel += "Histed"

path = f"results/{typeModel}/heatmap.npy"
heatmap = np.load(path)
heatmap_capped = np.clip(heatmap, 0, 1500)

fig = plt.figure(num=8,figsize = (4.5,3), facecolor = 'w', dpi = 150, edgecolor = 'w')
fig.clf()
ax = plt.axes([0.15, 0.18, 0.8, 0.8])
cs = ax.contourf(inh_RANGE, Wei_RANGE, heatmap_capped.T, cmap=cm.PuBu_r, vmin=0, vmax=1500, levels=10)
fig.colorbar(cs)

if is_production:
    plt.savefig(f"results/{typeModel}/svg/heatmap.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/heatmap.png", format="png", bbox_inches="tight")

plt.show()