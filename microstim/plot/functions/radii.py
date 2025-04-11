import matplotlib.pylab as plt
import seaborn as sns
import os

from microstim.globals import T_RANGE, intensity, depol_weights, depol_sigma, act_weights, act_sigma, gamma, start_boost, no_boost, no_boost_weights, DT
from microstim.main import model
from microstim.utils import rect, sigmoid, sigmoidalRect

print(DT)
is_depol = True
is_test = True

if is_depol:
    boost = start_boost.copy()
    weights = depol_weights.copy()
    sigma = depol_sigma.copy()
else:
    boost = gamma.copy()
    weights = act_weights.copy()
    sigma = act_sigma.copy()
    
_, _, rho_e, rho_i, _, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=is_depol, radius_only=True)

if not is_test:
    _, _, no_amp, _, _, _ = model(intensity, no_boost_weights, sigma, rect, no_boost, is_depolarized=False)

sns.set_theme(style="ticks")
palette = sns.color_palette("rocket_r", n_colors=3) 

ax = plt.subplot(111) 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

if not is_test:
    plt.plot(T_RANGE, no_amp, color=palette[0], label="No Amp")
plt.plot(T_RANGE, rho_e, color=palette[1], label=r"$\rho_e$")
plt.plot(T_RANGE, rho_i, color=palette[2], label=r"$\rho_i$")

plt.xlabel("time [ms]")
plt.ylabel(r"Radius [$\mu$m]")
plt.title(r"$\Delta t$ = " + str(DT) + " ms")
plt.legend(loc="best")

if not is_test:
    plt.savefig("results/amp1/svg/radii.svg", format="svg", bbox_inches="tight")
    plt.savefig("results/amp1/radii.png", format="png", bbox_inches="tight")
os.system('say "Radii finished"')
plt.show()
