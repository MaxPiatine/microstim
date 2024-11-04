from numpy import arange, zeros
from math import sqrt
from scipy.special import erf
import matplotlib.pyplot as plt

"""
For excitatory potential V_e
"""

R = 7 #resistance (change) KOhms
I = 45 #initial intensity (change) muA
ALPHA = 4 #micron
N = 1000
DT = 0.01

THRESHOLD = 20 #mV 

# look up the weights
weights = {
    "e->e": 100,
    "i->e": 100,
    "e->i": 100,
    "i->i": 100,
}

sigma = {
    "ee": 100,
    "ie": 100,
    "ei": 100,
    "ii": 100,
}


def KernelConvolution(x, rho, weight, sigma):
    return ((THRESHOLD * weight) / 2) * ( erf( (x + rho) / (sqrt(2) * sigma) ) - erf( (x - rho) / (sqrt(2) * sigma) ) )


I_RANGE = arange(0, N)
X_RANGE = arange(0, N)
rho_e, rho_i = zeros(N), zeros(N)
v_e, v_i = zeros((len(I_RANGE), len(X_RANGE))), zeros((len(I_RANGE), len(X_RANGE)))

v_e[0][:] = R*I/(X_RANGE + ALPHA)
rho_e[0] = R*I/THRESHOLD - ALPHA

for i in range(len(I_RANGE) - 1):
    v_e[i+1][:] += v_e[i][:] + DT * (
        -v_e[i][:] + KernelConvolution(X_RANGE, rho_e, weights["e->e"], sigma["ee"]) - + KernelConvolution(X_RANGE, rho_e, weights["i->e"], sigma["ie"])
        )
    
    v_i[i+1][:] += v_i[i][:] + DT * (
        -v_e[i][:] + KernelConvolution(X_RANGE, rho_i, weights["e->i"], sigma["ei"]) - + KernelConvolution(X_RANGE, rho_i, weights["i->i"], sigma["ii"])
        )

    for index, potential in enumerate(v_e[i+1][:]):
        if potential <= THRESHOLD:
            rho_e[i] = X_RANGE[index]
            break

for i in range(0, N-900, 10):
    print(rho_e[i])
    plt.plot(X_RANGE, v_e[i], label="v[%i]"%i)

# Display the plot only after all lines are plotted
plt.xlabel('distance')
plt.ylabel('v[i](x)')
plt.title('V at different steps')
plt.legend()  # Adds a legend to differentiate between lines
plt.show()