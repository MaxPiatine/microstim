import matplotlib.pylab as plt
import argparse
import seaborn as sns

from microstim.main import model
from microstim.globals import act_weights, act_sigma, depol_weights, depol_sigma, intensity, start_boost, gamma, X_RANGE, T_RANGE
from microstim.utils import rect

parser = argparse.ArgumentParser(description="heatmap of potential over time and space")
parser.add_argument("--is_depol", action="store_true", help="Run model with depolarization")
parser.add_argument("--is_prod", action="store_true", help="Run for production")

args = parser.parse_args()

is_depolarized = args.is_depol
is_production = args.is_prod
typeModel = ""

if is_depolarized:
    boost = start_boost.copy()
    weights = depol_weights.copy()
    sigma = depol_sigma.copy()
    typeModel += "Stoney"
else:
    boost = gamma.copy()
    weights = act_weights.copy()
    sigma = act_sigma.copy()
    typeModel += "Histed"
    
v_e, _, _, _, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=is_depolarized)

fig, ax = plt.subplots()

v_e[v_e > 20.0] = 20  
v_e[v_e < -10.0] = -10

cmap = sns.color_palette("icefire", as_cmap=True)
cs = ax.contourf(T_RANGE, X_RANGE, v_e.T, 
                cmap=cmap,
                extend='both',
                alpha=0.7)

ax.set_xlabel("Time (ms)")
ax.set_ylabel("Distance (μm)")
fig.suptitle("Sub-threshold voltage by distance and time")
ax.set_xlim(right=max(T_RANGE))
ax.set_ylim(top=max(X_RANGE))
cbar = fig.colorbar(cs, label="Voltage (mV)")

if is_production:
    plt.savefig(f"results/{typeModel}/svg/potHeat.svg", format="svg", bbox_inches="tight")
    plt.savefig(f"results/{typeModel}/potHeat.png", format="png", bbox_inches="tight")
    
plt.show()