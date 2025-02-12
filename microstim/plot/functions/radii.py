import matplotlib.pylab as plt
import seaborn as sns
import os

from microstim.globals import T_RANGE, intensity, sigma, weights, sigma, gamma, start_boost
from microstim.main import model
from microstim.utils import rect, sigmoid


boost = gamma.copy()
_, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=False)

weights = {
        "ee": 150,
        "ie": 150,
        "ei": 150,
        "ii": 150,
    }

no_boost = {
    "exc": 1,
    "inh": 1,
}

_, _, no_amp, _, _, _ = model(intensity, weights, sigma, rect, no_boost, is_depolarized=False)

sns.set_theme(style="ticks")
palette = sns.color_palette("rocket_r", n_colors=3) 

ax = plt.subplot(111) 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.plot(T_RANGE, no_amp, color=palette[0], label="No Amp")
plt.plot(T_RANGE, rho_e, color=palette[1], label=r"$\rho_e$")
plt.plot(T_RANGE, rho_i, color=palette[2], label=r"$\rho_i$")

plt.xlabel("Normalized Time")
plt.ylabel(r"Radius [$\mu$m]")
plt.legend(loc="best")
# plt.savefig("microstim/plot/figures/vectorize/depol__radii.svg", format="svg", bbox_inches="tight")
os.system('say "Radii finished"')
plt.show()
