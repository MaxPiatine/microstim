import matplotlib.pylab as plt
import seaborn as sns
import numpy as np

from microstim.axon import axon
from microstim.globals import axon_linspace, RHEOBASE, STEP

prod=True
"""
intensity is a function of distance. Assuming there is an initial intensity I_0 the 
numpy arange is the intensity I_0 changing with respect to distance
"""
intensities = np.arange(RHEOBASE+STEP, max(axon_linspace), 0.05)

ratios = []
for intensity in intensities:
    _, _, ratio_e, ratio_i = axon(intensity)
    ratio_e = round(ratio_e, 2)
    ratio_i = round(ratio_i, 2)
    if ratio_e == 0:
        ratio = ratio_i
    else:
        ratio =  ratio_i/ ratio_e
    
    print(f"exc ratio of {intensity} μA, ratio i: {ratio_i}, ratio e: {ratio_e}, ratio {ratio}")
    ratios.append(ratio)

sns.set_theme(style="ticks")
palette = sns.color_palette("mako_r", n_colors=3) 

ax = plt.subplot(111) 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Shade the region below RHEOBASE
plt.axvspan(0, RHEOBASE, color='gray', alpha=0.2, label="Below Rheobase")
plt.plot(intensities, ratios, color=palette[1], label="Ratio Distribution")
plt.title("intensities")
plt.xlabel("intensity threshold [μA]")
plt.ylabel("I/E Ratio")
if prod:
    plt.savefig("results/axon/svg/EIratio.svg", format="svg", bbox_inches="tight")
    plt.savefig("results/axon/EIratio.png", format="png", bbox_inches="tight")
plt.show()
