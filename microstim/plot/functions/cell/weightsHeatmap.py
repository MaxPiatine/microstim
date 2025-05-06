import matplotlib.pylab as plt
import numpy as np
import seaborn as sns
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

path = f"results/{typeModel}/boost_heatmap.npy"
heatmap = np.load(path)

w_ranges = np.linspace(0, 500, 10)

plt.figure(figsize=(8, 6))
ax = sns.heatmap(
    heatmap.T,
    xticklabels=np.round(w_ranges, 2),  
    yticklabels=np.round(w_ranges, 2),  
    linewidths=0.5, 
)

ax.invert_yaxis()

ax.set_xlabel(r"$w_{ie}$")
ax.set_ylabel(r"$w_{ei}$")

if is_production:
    plt.savefig(f"results/{typeModel}/svg/weights_heatmap.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/weights_heatmap.png", format="png", bbox_inches="tight")

plt.show()