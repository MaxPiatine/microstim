import math
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

from microstim.utils import intensityPDF, intensityTreshold
from microstim.globals import MU_E, MU_I, STDEV_E, STDEV_I, STEP, RHEOBASE

checkNormalized = False

def axon(intensity_at_axon, axon_diameter=None):
    if axon_diameter:
        threshold_for_diameter = intensityTreshold(axon_diameter)
        axon_linspace = np.arange(RHEOBASE, threshold_for_diameter, STEP)
        print(intensity_at_axon, threshold_for_diameter)
    else:
        # full picture of distribution
        axon_linspace = np.arange(RHEOBASE, 5*RHEOBASE, STEP)


    if checkNormalized and axon_diameter is None:
        isNormal = 0
        for x in axon_linspace:
                val = intensityPDF(x, mu_d=MU_E, sigma_d=STDEV_E, isTest=checkNormalized)
                if math.isnan(val):
                    continue
                isNormal += val * STEP


        print("is it normalized?: ", isNormal)

    lognrml_e = intensityPDF(axon_linspace, mu_d=MU_E, sigma_d=STDEV_E)
    lognrml_i = intensityPDF(axon_linspace, mu_d=MU_I, sigma_d=STDEV_I)

    ratio_e = 0
    for i, x in enumerate(axon_linspace):
        val = lognrml_e[i]
        if math.isnan(val):
            continue
            
        if x < intensity_at_axon:
            ratio_e += val * STEP

    ratio_i = 0
    for i, x in enumerate(axon_linspace):
        val = lognrml_i[i]
        if math.isnan(val):
            continue

        if x < intensity_at_axon:
            ratio_i += val * STEP

    # sns.set_theme(style="ticks")
    # palette = sns.color_palette("mako_r", n_colors=3) 

    # ax = plt.subplot(111) 
    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    # plt.plot(axon_linspace, lognrml_e, color=palette[0], label="exc")
    # plt.plot(axon_linspace, lognrml_i, color=palette[1], label="inh")
    # plt.xlabel("intensity threshold [μA]")
    # plt.ylabel("probability")
    # plt.legend(loc="best")
    # plt.show()

    return lognrml_e, lognrml_i, ratio_e, ratio_i
            