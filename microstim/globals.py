import numpy as np

N = 1000

R = 7 #resistance (change) KOhms
ALPHA = 4 #micron
BETA = 1
DT = 0.01

THRESHOLD = 20 #mV

i_RANGE = np.arange(0, N) #steps
X_RANGE = np.arange(0, 1000)

T = N * DT
intensity = 500 #microA

T_RANGE = np.arange(0, T, T/N)

# Power Law
P = 1

sigma = {
        "ee": 127, #microns
        "ie": 96.6,
        "ei": 99.84,
        "ii": 126.77,
    } 

weights = {
        "ee": 200000,
        "ie": 100000,
        "ei": 70000,
        "ii": 100,
    }

start_boost = {
    "exc": 1,
    "inh": 0.5,
}

gamma = {
    "exc": 10**5,
    "inh": 1,
}