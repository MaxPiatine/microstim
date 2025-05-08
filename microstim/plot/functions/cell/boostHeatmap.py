import argparse
import matplotlib.pylab as plt
import numpy as np
import seaborn as sns

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

plt.figure(figsize=(8, 6))
ax = sns.heatmap(
    heatmap.T,
    xticklabels=np.round(ranges, 2),  
    yticklabels=np.round(ranges, 2),  
    linewidths=0.5, 
)

ax.invert_yaxis()

if is_depolarized:
    ax.set_xlabel(r"$k_e$")
    ax.set_ylabel(r"$k_i$")
else:
    ax.set_xlabel(r"$\alpha_i$")
    ax.set_ylabel(r"$\alpha_e$")

if is_production:
    plt.savefig(f"results/{typeModel}/svg/heatmap.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/heatmap.png", format="png", bbox_inches="tight")

plt.show()