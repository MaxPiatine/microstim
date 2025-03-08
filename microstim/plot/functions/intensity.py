import matplotlib.pylab as plt
import seaborn as sns
import os

from microstim.globals import T_RANGE, intensity, sigma, weights, sigma, gamma, start_boost, X_RANGE
from microstim.main import model
from microstim.utils import rect, sigmoid, sigmoidalRect



boost = gamma.copy()
_, _, _, _, nu_e, _ = model(intensity, weights, sigma, rect, boost, is_depolarized=False)
_, _, _, _, nu_ee, _ = model(intensity, weights, sigma, sigmoidalRect, boost, is_depolarized=False)

sns.set_theme(style="ticks")
palette = sns.color_palette("mako_r", n_colors=3) 
ax = plt.subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.plot(X_RANGE, nu_e[2], color=palette[0], label=r"$\Pi$")
plt.plot(X_RANGE, nu_ee[2], color=palette[1], label="S")
plt.legend()
plt.show()         