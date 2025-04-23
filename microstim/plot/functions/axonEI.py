import matplotlib.pylab as plt
import seaborn as sns

from microstim.axon import axon
from microstim.globals import axon_linspace

distance = 1000 #microns 
intensity_0 = 103.8 #microAmps
intensity = intensity_0/distance

sns.set_theme(style="ticks")
palette = sns.color_palette("mako_r", n_colors=3) 

ax = plt.subplot(111) 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

integral_e, integral_i, _, _ = axon(intensity)

plt.plot(axon_linspace, integral_e, color=palette[0], label="exc")
plt.plot(axon_linspace, integral_i, color=palette[1], label="inh")
plt.title(f"{intensity_0} μA, {distance} μm from axon")
plt.fill_between(axon_linspace, integral_i, where=(axon_linspace < intensity), color='grey', alpha=0.3)
plt.axvline(intensity, color='black', linestyle='--', label=r"$I_T$")
plt.xlabel("intensity threshold [μA]")
plt.ylabel("probability")
plt.legend(loc="best")
plt.show()
