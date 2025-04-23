import math
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

from microstim.utils import intensityPDF, intensityTreshold
from microstim.globals import MU_E, MU_I, STDEV_E, STDEV_I, STEP, RHEOBASE, axon_linspace

checkNormalized = False

def axon(intensity_at_axon, axon_diameter=None):
    if axon_diameter:
        threshold_for_diameter = intensityTreshold(axon_diameter)
        linspace = np.arange(RHEOBASE, threshold_for_diameter, STEP)
        print(intensity_at_axon, threshold_for_diameter)
    else:
        linspace = axon_linspace


    if checkNormalized and axon_diameter is None:
        isNormal = 0
        for x in linspace:
                val = intensityPDF(x, mu_d=MU_E, sigma_d=STDEV_E)
                if math.isnan(val):
                    continue
                isNormal += val * STEP


        print("is it normalized?: ", isNormal)

    lognrml_e = intensityPDF(linspace, mu_d=MU_E, sigma_d=STDEV_E)
    lognrml_i = intensityPDF(linspace, mu_d=MU_I, sigma_d=STDEV_I)

    ratio_e = 0
    for i, x in enumerate(linspace):
        val = lognrml_e[i]
        if math.isnan(val):
            continue
            
        if x < intensity_at_axon:
            ratio_e += val * STEP

    ratio_i = 0
    for i, x in enumerate(linspace):
        val = lognrml_i[i]
        if math.isnan(val):
            continue

        if x < intensity_at_axon:
            ratio_i += val * STEP

    return lognrml_e, lognrml_i, ratio_e, ratio_i
            