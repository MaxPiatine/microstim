import matplotlib.pylab as plt
import seaborn as sns

from microstim.axon import axon
from microstim.globals import axon_linspace, RHEOBASE

prod=False
# distance = 10 #microns 
# intensity_0 = 100 #microAmps
# intensity = intensity_0/distance
intensity=5.2

# Calculate ratios at each point
ratios = []
for point in axon_linspace:
    _, _, ratio_e, ratio_i = axon(point)
    if ratio_e == 0:
        ratio = ratio_i
    else:
        ratio = round(ratio_i / ratio_e, 10)
    ratios.append(ratio)
    
# Get the specific point ratio
_, _, ratio_e, ratio_i = axon(intensity)
try:
    specific_ratio = ratio_i/ratio_e
except ZeroDivisionError:
    specific_ratio = 0
    
print(f"specific ratio: {specific_ratio}")

# print(f"inh ratio of {intensity} μA, {distance} μm from axon: {ratio_i}")
# print(f"exc ratio of {intensity} μA, {distance} μm from axon: {ratio_e}")
print(f"the ratio of i/e: {specific_ratio}")


sns.set_theme(style="ticks")
palette = sns.color_palette("mako_r", n_colors=3) 

ax = plt.subplot(111) 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Shade the region below RHEOBASE
plt.axvspan(0, RHEOBASE, color='gray', alpha=0.2, label="Below Rheobase")
plt.plot([intensity], [specific_ratio], marker="o", color=palette[0], label="Specific Point")
plt.plot(axon_linspace, ratios, color=palette[1], label="Ratio Distribution")
# plt.title(f"{intensity_0} μA, {distance} μm from axon")
plt.xlabel("intensity threshold [μA]")
plt.ylabel("I/E Ratio")
plt.legend(loc="best")

if prod:
    plt.savefig("results/axon/svg/ratios.svg", format="svg", bbox_inches="tight")
    plt.savefig("results/axon/ratios.png", format="png", bbox_inches="tight")
plt.show()

