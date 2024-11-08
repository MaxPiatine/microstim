from numpy import arange, zeros, max
from math import sqrt
from scipy.special import erf
import matplotlib.pyplot as plt

"""
For excitatory potential V_e
"""

R = 7 #resistance (change) KOhms
I = 500 #initial intensity (change) muA
ALPHA = 4 #micron
N = 200
DT = 0.01


E_THRESHOLD, I_THRESHOLD = 20, 20 #mV
 
# look up the weights
weights = {
    "e->e": 200,
    "i->e": 200,
    "e->i": 200,
    "i->i": 200,
}

sigma = {
    "ee": 120,
    "ie": 120,
    "ei": 120,
    "ii": 120,
} #microns


def KernelConvolution(x, rho, weight, sigma, threshold=20):
    return ((weight) / 2) * ( erf( (x + rho) / (sqrt(2) * sigma) ) - erf( (x - rho) / (sqrt(2) * sigma) ) )


i_RANGE = arange(0, N) #steps
X_RANGE = arange(0, 1000)

v_e, v_i = zeros((len(i_RANGE), len(X_RANGE))), zeros((len(i_RANGE), len(X_RANGE)))
rho_e, rho_i = zeros(N), zeros(N)

"""
Initial condition is assuming that we stimulate a population of 
excitatory cells. where the excitatory potential follows monopole
diapole, and the activation radius is dependent on the intensity
"""
rho_e[0] = R*I/E_THRESHOLD - ALPHA

v_e[0][:] = R*I/(X_RANGE + ALPHA) #1/sqrt(x)
v_i[0][:] = R*I/(X_RANGE + ALPHA)

"""
kernal convolution array
"""
ee_erf, ie_erf = zeros((len(i_RANGE), len(X_RANGE))), zeros((len(i_RANGE), len(X_RANGE)))

for i in range(len(i_RANGE)-1):
    
    ee_erf[i][:] = KernelConvolution(X_RANGE, rho_e[i], weights["e->e"], sigma["ee"]) 
    ie_erf[i][:] = KernelConvolution(X_RANGE, rho_i[i], weights["i->e"], sigma["ie"])
    
    v_e[i+1][:] = v_e[i][:] + DT * (-v_e[i][:] + ee_erf[i][:] - ie_erf[i][:])
    
    v_i[i+1][:] = v_i[i][:] + DT * (
        -v_i[i][:] + KernelConvolution(X_RANGE, rho_e[i], weights["e->i"], sigma["ei"]) - KernelConvolution(X_RANGE, rho_i[i], weights["i->i"], sigma["ii"])
        )

    for index, e_potential in enumerate(v_e[i+1][:]):
        if e_potential < E_THRESHOLD:
            rho_e[i+1] = X_RANGE[index]
            break

    for index, i_potential in enumerate(v_i[i+1][:]):
        if i_potential < I_THRESHOLD:
            rho_i[i+1] = X_RANGE[index]
            break
            
    print("At Step %i: excitatory activation radius: %i inhibitory activation radius: %i"%(i, rho_e[i], rho_i[i]))


# plotting
figure, ax = plt.subplots(3, 2, figsize=(10, 8))

# row1
for i in range(0, len(i_RANGE), 20):
    ax[0][0].plot(X_RANGE, v_e[i], label="ve[%i]"%i)
    ax[0][1].plot(X_RANGE, v_i[i], label="vi[%i]"%i)

ax[0][0].set_xlabel(r"distance ($\mu$x)"), ax[0][1].set_xlabel(r"distance ($\mu$x)")
ax[0][0].set_ylabel("potential (mV)")
ax[0][0].set_title("e_potential time steps"), ax[0][1].set_title("i_potential time steps")
ax[0][0].legend(), ax[0][1].legend()
# ax[0][0].set_ylim(0, 50), ax[0][1].set_ylim(0, 50)
# ax[0][0].set_xlim(0, 400), ax[0][1].set_xlim(0, 400)

# row2
ax[1][0].plot(i_RANGE, rho_e)
ax[1][1].plot(i_RANGE, rho_i)

ax[1][0].set_title("e_rho"), ax[1][1].set_title("i_rho")

# row3
ax[2][0].plot(X_RANGE, max(v_e, axis=0), label="amp exc")
ax[2][0].plot(X_RANGE, max(v_i, axis=0), label="amp inh")

ax[2][1].plot(i_RANGE/max(i_RANGE), v_e[:, 100], label="amp exc")
ax[2][1].plot(i_RANGE/max(i_RANGE), v_i[:, 100], label="amp inh")

ax[2][0].set_xlabel(r"distance ($\mu$x)"), ax[2][1].set_xlabel("normalized time")
ax[2][0].set_ylabel("max pot (mV)")
ax[2][0].set_title("Max Potential vs Distance"), ax[2][1].set_title("Max Potential vs Normalized Time")
ax[2][0].set_ylim(0, 20)
ax[2][0].set_xlim(0, 1000)
ax[2][0].legend()

# show
plt.tight_layout()
plt.show()