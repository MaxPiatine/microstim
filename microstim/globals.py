import numpy as np

N = 3000

R = 7 #resistance (change) KOhms
ALPHA = 4 #micron
BETA = 1
DT = 0.01
TAU = 10 #ms

THRESHOLD = 20 #mV

i_RANGE = np.arange(0, N) #steps
X_RANGE = np.arange(0, 3000, 0.1)

T = N * DT
intensity = 500 #microA

T_RANGE = np.arange(0, T, T/N)

# Power Law
P = 2

sigma = {
        "ee": 127, #microns
        "ie": 96.6,
        "ei": 99.84,
        "ii": 126.77,
    } 

weights = {
        "ee": 400,
        "ie": 300,
        "ei": 400,
        "ii": 25,
    }

start_boost = {
    "exc": 1,
    "inh": 0.5,
}

gamma = {
    "exc": 150,
    "inh": 20,
}