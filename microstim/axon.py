import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
import math

from microstim.utils import lognormal, lognormalIntensity, diameter2Threshold, normal, threshold2Diameter, chronoxie
from microstim.globals import X_RANGE

linspace = np.linspace(0.01, 2, len(X_RANGE))
step = linspace[1] - linspace[0]
checkNormalized = True
mu_e, mu_i = 0.712, 0.465 #microns
sigma_e, sigma_i = 0.292, 0.114
rheobase = 0.8

diameter_wanted = mu_e + 2*sigma_e #microns
pulse = 20 #micro s #chronoxie(diameter_wanted) #10 #ms
thresh_wanted = 0.87 #diameter2Threshold(diameter_wanted, rheobase, pulse)

print("Between 0.801 microAmp (diameter=", threshold2Diameter(0.801, rheobase, pulse),  " microns) and 1 microamp (diameter=", threshold2Diameter(1, rheobase, pulse), " microns) for 0.8 microAmp rheobase and 10 microsecond stim")

if checkNormalized:
    isNormal = 0
    for x in linspace:
            val = lognormalIntensity(x, rheobase=rheobase, time=pulse, mu_d=mu_e, sigma_d=sigma_e)
            if math.isnan(val):
                continue
            isNormal += val * (linspace[1]-linspace[0])


    print("is it normalized?: ", isNormal)

print("diameter, ", diameter_wanted, " to threshold: ", diameter2Threshold(diameter_wanted, rheobase, pulse))
print("chronoxie: ", chronoxie(diameter_wanted))

sns.set_theme(style="ticks")
palette = sns.color_palette("mako_r", n_colors=3) 

ax = plt.subplot(111) 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

lognrml_e = lognormalIntensity(linspace, rheobase=rheobase, time=pulse, mu_d=mu_e, sigma_d=sigma_e)
lognrml_i = lognormalIntensity(linspace, rheobase=rheobase, time=pulse, mu_d=mu_i, sigma_d=sigma_i)

integral_e = 0
ratio_e = np.zeros(len(X_RANGE))
for i, x in enumerate(linspace):
    val = lognormalIntensity(x, rheobase=rheobase, time=pulse, mu_d=mu_e, sigma_d=sigma_e)
    if math.isnan(val):
        continue
    else:
        ratio_e[i] = val * step
        
    if x < thresh_wanted:
        integral_e += val * step


# print("Integral from 0 to a: ", integral_e)
print("Ratio of E: ", integral_e)

integral_i = 0
ratio_i = np.zeros(len(X_RANGE))
for i, x in enumerate(linspace):
    val = lognormalIntensity(x, rheobase=rheobase, time=pulse, mu_d=mu_i, sigma_d=sigma_i)
    if math.isnan(val):
        continue
    else:
        ratio_i[i] = val * step
    
    if x < thresh_wanted:
        integral_i += val * step
        
        

# print("Integral from 0 to b: ", integral_b)
print("Ratio of I: ", integral_i)

print("ratio between I/E: ", integral_i/integral_e)


plt.plot(linspace, lognrml_e, color=palette[0], label="exc")
plt.plot(linspace, lognrml_i, color=palette[1], label="inh")
plt.fill_between(linspace, lognrml_i, where=(linspace < thresh_wanted), color='grey', alpha=0.3)
plt.axvline(thresh_wanted, color='black', linestyle='--', label=r"$I_T$")
# plt.plot(linspace, ratio_i/ratio_e, color=palette[0])
# plt.plot([thresh_wanted], [integral_i/integral_e], marker="o", color=palette[1])
plt.xlabel("intensity threshold [μA]")
# plt.ylabel("I/E Ratio")
plt.ylabel("probability")
# plt.plot(a, integral_a/integral_b)
# plt.xlim([0.86,0.88])
# plt.ylim([0.5,20])
# plt.legend(loc="best")
plt.show()
