import math

from microstim.utils import intensityPDF, ConvertDiameterMean, ConvertDiameterSigma
from microstim.globals import X_RANGE, mu_e, mu_i, sigma_e, sigma_i

checkNormalized = False

def axon(linspace, rheobase, pulse, thresh_wanted):
    # print("exc threshold mean", ConvertDiameterMean(rheobase, pulse, mu_e, sigma_e))
    # print("inh threshold mean", ConvertDiameterMean(rheobase, pulse, mu_i, sigma_i))
    # print("exc threshold sigma", ConvertDiameterSigma(rheobase, pulse, mu_e, sigma_e))
    # print("inh threshold sigma", ConvertDiameterSigma(rheobase, pulse, mu_i, sigma_i))
    step = linspace[1] - linspace[0]
    if checkNormalized:
        isNormal = 0
        for x in linspace:
                val = intensityPDF(x, rheobase=rheobase, time=pulse, mu_d=mu_e, sigma_d=sigma_e, isTest=checkNormalized)
                if math.isnan(val):
                    continue
                isNormal += val * (linspace[1]-linspace[0])


        print("is it normalized?: ", isNormal)

    lognrml_e = intensityPDF(linspace, rheobase=rheobase, time=pulse, mu_d=mu_e, sigma_d=sigma_e)
    lognrml_i = intensityPDF(linspace, rheobase=rheobase, time=pulse, mu_d=mu_i, sigma_d=sigma_i)

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
            