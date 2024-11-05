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
N = 10
DT = 0.01


E_THRESHOLD, I_THRESHOLD = 20, 20 #mV
 
# look up the weights
weights = {
    "e->e": 1,
    "i->e": 1,
    "e->i": 1,
    "i->i": 1,
}

sigma = {
    "ee": 300,
    "ie": 150,
    "ei": 150,
    "ii": 100,
} #microns


def KernelConvolution(x, rho, weight, sigma, threshold=20):
    return ((threshold * weight) / 2) * ( erf( (x + rho) / (sqrt(2) * sigma) ) - erf( (x - rho) / (sqrt(2) * sigma) ) )


i_RANGE = arange(0, N)
X_RANGE = arange(-1000, 1000)
rho_e, rho_i = zeros(N), zeros(N)

v_e, v_i = zeros((len(i_RANGE), len(X_RANGE))), zeros((len(i_RANGE), len(X_RANGE)))

# init conditions
rho_e[0] = R*I/E_THRESHOLD - ALPHA

"""
kernal convolution array
"""
ee_erf, ie_erf = zeros((len(i_RANGE), len(X_RANGE))), zeros((len(i_RANGE), len(X_RANGE)))

for i in range(len(i_RANGE)-1):
    print("STEP %i"%i)

    ee_erf[i][:] = KernelConvolution(X_RANGE, rho_e[i], weights["e->e"], sigma["ee"]) 
    ie_erf[i][:] = KernelConvolution(X_RANGE, rho_i[i], weights["i->e"], sigma["ie"])
    v_e[i+1][:] += v_e[i][:] + DT * (-v_e[i][:] + ee_erf[i][:] - ie_erf[i][:])
    
    v_i[i+1][:] += v_i[i][:] + DT * (
        -v_i[i][:] + KernelConvolution(X_RANGE, rho_e[i], weights["e->i"], sigma["ei"]) - KernelConvolution(X_RANGE, rho_i[i], weights["i->i"], sigma["ii"])
        )

    for index, e_potential in enumerate(v_e[i+1][:]):
        if e_potential >= E_THRESHOLD:
            rho_e[i] += 1

    for index, i_potential in enumerate(v_i[i+1][:]):
        if i_potential >= I_THRESHOLD:
            rho_i[i] += 1

    rho_e[i] *= E_THRESHOLD
    rho_i[i] *= I_THRESHOLD


figure, ax = plt.subplots(1, 2)

for i in i_RANGE:
    print(rho_e[i])
    ax[0].plot(X_RANGE, v_e[i], label="ve[%i]"%i)
    ax[1].plot(X_RANGE, v_i[i], label="vi[%i]"%i)

# Display the plot only after all lines are plotted
ax[0].set_title("e_potential time steps")
ax[1].set_title("i_potential time steps")
ax[0].set_ylabel("potential (mV)")
ax[0].set_xlabel(r"distance ($\mu$x)"), ax[1].set_xlabel(r"distance ($\mu$x)")
ax[0].legend(), ax[1].legend()
plt.show()


# Debug Plot
for i in i_RANGE:
    plt.plot(X_RANGE, ee_erf[i], label=f"ee[{i}]")
    plt.plot(X_RANGE, ie_erf[i], label=f"ie[{i}]")
    

plt.title("k_conv over Time")
plt.xlabel(r"Distance ($\mu$x)")
plt.ylabel("k_conv values")
plt.legend()
plt.show()