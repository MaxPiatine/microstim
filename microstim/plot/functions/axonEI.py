import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
import math

from microstim.axon import axon
from microstim.utils import  diameter2Threshold, threshold2Diameter, chronoxie
from microstim.globals import X_RANGE, mu_e, mu_i, sigma_e, sigma_i, rheobase

linspace = np.linspace(0.8, 2, len(X_RANGE))
step = linspace[1] - linspace[0]


diameter_wanted = mu_e + 2*sigma_e #microns
pulse = 200 #micro s #chronoxie(diameter_wanted) #10 #ms
thresh_wanted = 0.8028 #diameter2Threshold(diameter_wanted, rheobase, pulse)

print("Between 0.801 microAmp (diameter=", threshold2Diameter(0.801, rheobase, pulse),  " microns) and "
"1 microamp (diameter=", threshold2Diameter(1, rheobase, pulse), " microns) "
"for 0.8 microAmp rheobase and 10 microsecond stim")

print("diameter, ", diameter_wanted, " to threshold: ", diameter2Threshold(diameter_wanted, rheobase, pulse))
print("chronoxie: ", chronoxie(diameter_wanted))

sns.set_theme(style="ticks")
palette = sns.color_palette("mako_r", n_colors=3) 

ax = plt.subplot(111) 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

integral_e, integral_i, _, _ = axon(rheobase, mu_e, mu_i, sigma_e, sigma_i, pulse, thresh_wanted)

plt.plot(linspace, integral_e, color=palette[0], label="exc")
plt.plot(linspace, integral_i, color=palette[1], label="inh")
plt.fill_between(linspace, integral_i, where=(linspace < thresh_wanted), color='grey', alpha=0.3)
plt.axvline(thresh_wanted, color='black', linestyle='--', label=r"$I_T$")
plt.xlabel("intensity threshold [μA]")
plt.ylabel("probability")
plt.legend(loc="best")
plt.show()
