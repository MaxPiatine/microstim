import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
import math

from microstim.utils import lognormal, lognormalIntensity, diameter2Threshold, normal, threshold2Diameter, chronoxie
from microstim.globals import X_RANGE

checkNormalized = False

def axon(rheobase, mu_e, mu_i, sigma_e, sigma_i, pulse, thresh_wanted):
    linspace = np.linspace(0.8, 2, len(X_RANGE))
    step = linspace[1] - linspace[0]
    if checkNormalized:
        isNormal = 0
        for x in linspace:
                val = lognormalIntensity(x, rheobase=rheobase, time=pulse, mu_d=mu_e, sigma_d=sigma_e)
                if math.isnan(val):
                    continue
                isNormal += val * (linspace[1]-linspace[0])


        print("is it normalized?: ", isNormal)

    lognrml_e = lognormalIntensity(linspace, rheobase=rheobase, time=pulse, mu_d=mu_e, sigma_d=sigma_e)
    lognrml_i = lognormalIntensity(linspace, rheobase=rheobase, time=pulse, mu_d=mu_i, sigma_d=sigma_i)

    ratio_e = 0
    for i, x in enumerate(linspace):
        val = lognrml_e[i]
        if math.isnan(val):
            continue
            
        if x < thresh_wanted:
            ratio_e += val * step

    ratio_i = 0
    for i, x in enumerate(linspace):
        val = lognrml_i[i]
        if math.isnan(val):
            continue

        if x < thresh_wanted:
            ratio_i += val * step

    return lognrml_e, lognrml_i, ratio_e, ratio_i
            