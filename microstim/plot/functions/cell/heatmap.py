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
    Wei_RANGE = np.linspace(100, 300, 10)
    inh_RANGE = np.linspace(0, 1.25, 10)
else:
    Wei_RANGE = np.linspace(0, 1000, 10)
    inh_RANGE = np.linspace(0, 500, 10)
    typeModel += "Histed"

path = f"results/{typeModel}/heatmap.npy"
heatmap = np.load(path)

# Create the heatmap using seaborn
plt.figure(figsize=(8, 6))
ax = sns.heatmap(
    heatmap.T,
    yticklabels=np.round(Wei_RANGE, 2),  
    xticklabels=np.round(inh_RANGE, 2),  
    linewidths=0.5, 
)

ax.invert_yaxis()

ax.set_xlabel("inh boost")
ax.set_ylabel(r"$w_{ei}$")

if is_production:
    plt.savefig(f"results/{typeModel}/svg/heatmap.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/heatmap.png", format="png", bbox_inches="tight")

plt.show()