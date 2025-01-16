import numpy as np

N = 1000

R = 7 #resistance (change) KOhms
ALPHA = 4 #micron
BETA = 1
DT = 0.01

THRESHOLD = 20 #mV

i_RANGE = np.arange(0, N) #steps
X_RANGE = np.arange(0, 1000)
x_linspace = np.linspace(0, 1, N + 2)[1:-1]  # Exclude exact 0 and 1

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
        "ee": 150,
        "ie": 200,
        "ei": 150,
        "ii": 100,
    }

start_boost = {
    "exc": 1,
    "inh": 0.5,
}

# exc gamma can be between 10**10 and 10**11 without it being unreasonable potential
gamma = {
    "exc": 3*10**9,
    "inh": 1,
}