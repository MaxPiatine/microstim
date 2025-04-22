import numpy as np
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

N = 12000

R = 7 #resistance (change) KOhms
ALPHA = 4 #micron
BETA = 1 
TAU = 10 #ms
SYN = 5
DT = 0.01
D = 0.3 #nanometer

THRESHOLD = 20 #mV

i_RANGE = np.arange(0, N) #steps
X_RANGE = np.arange(0, 2000, 0.1)

T = N * DT
intensity = 500 #microA

T_RANGE = np.arange(0, T, DT)

# Power Law
P = 2

act_sigma = {
        "ee": 127, #microns
        "ie": 96.6,
        "ei": 99.84,
        "ii": 126.77,
    } # activation model

act_weights = {
        "ee": 400,
        "ie": 300,
        "ei": 400,
        "ii": 25,
    } # activation model

depol_sigma = {
        "ee": 150, #microns
        "ie": 150,
        "ei": 150,
        "ii": 150,
    } # depol model

depol_weights = {
        "ee": 230,
        "ie": 150,
        "ei": 150,
        "ii": 25,
    } # depol model

no_boost_weights = {
        "ee": 150,
        "ie": 150,
        "ei": 150,
        "ii": 150,
    }

no_boost = {
    "exc": 1,
    "inh": 1,
}

start_boost = {
    "exc": 1,
    "inh": 0.5,
}

gamma = {
    "exc": 150,
    "inh": 20,
}

"""
Axon Dynamics
"""
MU_E, MU_I = 0.45, 0.54 #microns
STDEV_E, STDEV_I = 0.001, 0.001
RHEOBASE = 100 #microAmp
PULSE = 10 #microseconds
STEP = 0.01
axon_linspace = np.arange(RHEOBASE, RHEOBASE*5, STEP)
