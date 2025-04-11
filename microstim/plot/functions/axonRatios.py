import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
import seaborn as sns

from microstim.axon import axon
from microstim.globals import X_RANGE

linspace = np.linspace(0.8, 2, len(X_RANGE))
step = linspace[1] - linspace[0]
checkNormalized = False
mu_e, mu_i = 0.712, 0.465 #microns
sigma_e, sigma_i = 0.292, 0.292
rheobase = 0.8

diameter_wanted = mu_e + 2*sigma_e #microns
pulse = 200 #micro s #chronoxie(diameter_wanted) #10 #ms
thresh_wanted = 0.8028 #diameter2Threshold(diameter_wanted, rheobase, pulse)

integral_e, integral_i, _, _ = axon(rheobase, mu_e, mu_i, sigma_e, sigma_i, pulse, thresh_wanted)

print("ratio between I/E: ", integral_i/integral_e)


sns.set_theme(style="ticks")
palette = sns.color_palette("mako_r", n_colors=3) 

ax = plt.subplot(111) 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.plot([thresh_wanted], [integral_i/integral_e], marker="o", color=palette[0])
plt.xlabel("intensity threshold [μA]")
plt.ylabel("I/E Ratio")
plt.legend(loc="best")
plt.show()
