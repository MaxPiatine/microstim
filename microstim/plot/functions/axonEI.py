import matplotlib.pylab as plt
import seaborn as sns
import numpy as np

from microstim.axon import axon

pulse = 10 #microseconds
rheobase = 100 #microAmps
distance = 10 #microns 
intensity_0 = 1500 #microAmps
intensity = intensity_0/distance
linspace = np.arange(rheobase, rheobase*5, 0.01)

sns.set_theme(style="ticks")
palette = sns.color_palette("mako_r", n_colors=3) 

ax = plt.subplot(111) 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

integral_e, integral_i, _, _ = axon(linspace, rheobase, pulse, intensity)

plt.plot(linspace, integral_e, color=palette[0], label="exc")
plt.plot(linspace, integral_i, color=palette[1], label="inh")
plt.title(f"{intensity_0} μA, {distance} μm from axon")
plt.fill_between(linspace, integral_i, where=(linspace < intensity), color='grey', alpha=0.3)
plt.axvline(intensity, color='black', linestyle='--', label=r"$I_T$")
plt.xlabel("intensity threshold [μA]")
plt.ylabel("probability")
plt.legend(loc="best")
plt.show()
