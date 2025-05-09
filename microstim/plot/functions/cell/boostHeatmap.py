import argparse
import matplotlib.pylab as plt
import numpy as np
from matplotlib import cm

parser = argparse.ArgumentParser(description="heatmap of excitatory and inhibitory start boosts")
parser.add_argument("--is_depol", action="store_true", help="Run model with depolarization")
parser.add_argument("--is_prod", action="store_true", help="Run for production")

args = parser.parse_args()

is_depolarized = args.is_depol
is_production = args.is_prod
typeModel = ""

if is_depolarized:
    typeModel += "Stoney"
    ranges = np.linspace(0, 1, 20)
else:
    typeModel += "Histed"
    ranges = np.linspace(0, 1000, 20)

path = f"results/{typeModel}/boost_heatmap.npy"
heatmap = np.load(path)

fig = plt.figure(num=8,figsize = (4.5,3), facecolor = 'w', dpi = 150, edgecolor = 'w')
fig.clf()
ax = plt.axes([0.15, 0.18, 0.8, 0.8])
cs = ax.contourf(ranges, ranges, heatmap.T, cmap=cm.PuBu_r, vmin=0, vmax=1000, levels=20)
fig.colorbar(cs)

if is_depolarized:
    ax.set_xlabel(r"$k_e$")
    ax.set_ylabel(r"$k_i$")
else:
    ax.set_xlabel(r"$\alpha_i$")
    ax.set_ylabel(r"$\alpha_e$")

if is_production:
    plt.savefig(f"results/{typeModel}/svg/boost_heatmap.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/boost_heatmap.png", format="png", bbox_inches="tight")

plt.show()