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
    boost_ranges = np.linspace(0, 1, 10)
    sigma_ranges = np.linspace(-1, 1, 10) # this needs to change
else:
    boost_ranges = np.linspace(0, 1000, 10)
    sigma_ranges = np.linspace(-1, 1, 10)
    typeModel += "Histed"

path = f"results/{typeModel}/sigma.npy"
heatmap = np.load(path)

fig = plt.figure(num=8,figsize = (4.5,3), facecolor = 'w', dpi = 150, edgecolor = 'w')
fig.clf()
ax = plt.axes([0.15, 0.18, 0.8, 0.8])
cs = ax.contourf(sigma_ranges, boost_ranges, heatmap.T, cmap=cm.PuBu_r, vmin=0, vmax=1500, levels=100)
fig.colorbar(cs)

if is_production:
    plt.savefig(f"results/{typeModel}/sigma.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/sigma.png", format="png", bbox_inches="tight")

plt.show()