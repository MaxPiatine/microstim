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
        "ee": 120,
        "ie": 120,
        "ei": 120,
        "ii": 120,
    } #microns

weights = {
        "e->e": 150,
        "i->e": 150,
        "e->i": 150,
        "i->i": 150,
    }

start_boost = {
    "exc": 1,
    "inh": 1,
}

gamma = {
    "exc": 1,
    "inh": 1,
}