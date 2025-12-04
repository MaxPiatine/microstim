
import torch.nn.functional as F
import torch
import numpy as np
import time

from microstim.config import config, DEVICE
from microstim.utils import maxRadius, normal, plot_tn, zeros, make_kernel, V_eph, sigmoid
from microstim.plot.cell.utils import setup

import matplotlib.pylab as plt

usingFFT = False
gif = False

N = config["N"]
X = config["distance"]
P = config["P"]
R = config["R"]
rates = config["rates"]
d_axon = config["d_axon"]
Rm = config["Rm"]
DT = config["dt"]
DX = config["dx"]
TAU = config["TAU"]
ALPHA = config["ALPHA"]
THRESHOLD = config["THRESHOLD"]
DISTANCE_RANGE = torch.tensor(np.arange(0, X, DX), dtype=torch.float32, device=DEVICE)
L = DISTANCE_RANGE.shape[0]

fits = {
    10: {"inh": {"x0": 50, "k": 0.218}, "exc": {"x0": 50, "k": 0.218}},
    20: {"inh": {"x0": 50, "k": 0.218}, "exc": {"x0": 50, "k": 0.218}},
    50: {"inh": {"x0": 50, "k": 0.008}, "exc": {"x0": 50, "k": 0.238}},
    100: {"inh": {"x0": 170.3, "k": 0.012}, "exc": {"x0": 63.9, "k": 0.045}},
    200: {"inh": {"x0": 243.3, "k": 0.012}, "exc": {"x0": 75, "k": 0.064}},
    500: {"inh": {"x0": 253.7, "k": 0.108}, "exc": {"x0": 250, "k": 0.09}},
    1000: {"inh": {"x0": 285.7, "k": 0.056}, "exc": {"x0": 285.7, "k": 0.056}},
}

def t_o(intensity, rate, boost):
    fit = fits[intensity]
    nu_e, nu_i = zeros(L), zeros(L) # firing rates
    v_e, v_i = zeros(L), zeros(L) # membrane potentials
    
    v_e = V_eph(DISTANCE_RANGE, R, intensity, ALPHA) * d_axon["exc"] * boost["exc"] 
    v_i = V_eph(DISTANCE_RANGE, R, intensity, ALPHA) * d_axon["inh"] * boost["inh"] 

    # v_e *= normal(DISTANCE_RANGE, 113)
    # v_i *= normal(DISTANCE_RANGE, 113)
    # x0_exc = maxRadius(v_e, DISTANCE_RANGE, THRESHOLD)
    # x0_inh = maxRadius(v_i, DISTANCE_RANGE, THRESHOLD)

    x0_exc = np.sqrt(R*intensity * d_axon["exc"] * boost["exc"]/THRESHOLD) - ALPHA
    x0_inh = np.sqrt(R*intensity * d_axon["inh"] * boost["inh"]/THRESHOLD) - ALPHA
    print("Pyr")
    nu_e = torch.tensor(rate(DISTANCE_RANGE.cpu().numpy(), x0_exc, 0.064))
    print("PV")
    nu_i = torch.tensor(rate(DISTANCE_RANGE.cpu().numpy(), x0_inh, 0.112))

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(11, 20))
    axes = axes.flatten()  # make indexing easier

    fit_exc = fit["exc"]
    axes[0].plot(DISTANCE_RANGE.cpu().numpy(), np.clip(v_e.cpu().numpy(), 0, 20), label="exc")
    axes[0].plot(DISTANCE_RANGE.cpu().numpy(), nu_e.cpu().numpy(), label="exc rate")
    axes[0].plot(DISTANCE_RANGE.cpu().numpy(), sigmoid(DISTANCE_RANGE.cpu().numpy(), fit_exc["x0"], fit_exc["k"]), label="exc exp rate")
    axes[0].hlines(THRESHOLD, xmin=0, xmax=X, colors='gray', linestyles='dashed', label="threshold")
    axes[0].vlines(x0_exc, ymin=0, ymax=20, colors='gray', linestyles='dashed', label="x0 exc")
    axes[0].legend()

    fit_inh = fit["inh"]
    axes[1].plot(DISTANCE_RANGE.cpu().numpy(), np.clip(v_i.cpu().numpy(),0, 20), label="inh")
    axes[1].plot(DISTANCE_RANGE.cpu().numpy(), nu_i.cpu().numpy(), label="inh rate")
    axes[1].plot(DISTANCE_RANGE.cpu().numpy(), sigmoid(DISTANCE_RANGE.cpu().numpy(), fit_inh["x0"], fit_inh["k"]), label="inh exp rate")
    axes[1].hlines(THRESHOLD, xmin=0, xmax=X, colors='gray', linestyles='dashed', label="threshold")
    axes[1].vlines(x0_inh, ymin=0, ymax=20, colors='gray', linestyles='dashed', label="x0 inh")
    axes[1].legend()
    plt.show()

    return v_e, v_i, nu_e, nu_i

if __name__ == "__main__":
    _, boost, _ = setup(config)
    intensities = [10, 20, 50, 100, 200, 500, 1000]
    lst = []
    for intensity in intensities:
        print(f"Intensity: {intensity} uA")
        _, _, nu_e, nu_i = t_o(intensity, sigmoid, boost)
        lst.append(nu_i)
        print()

    positions = [50, 100, 250, 750]     
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xscale('log')
    # ax.set_title('Intensity vs nu_e at different positions')
    ax.grid(True, which="both", ls="-")
 
    for pos in positions:
        pidx = int(round(pos / DX))
        probs = [row[pidx].cpu().item() for row in lst]  # row is tensor (L,)
        ax.plot(intensities, probs, marker='o', label=f"{pos} μm")

    ax.set_xlabel("Intensity (µA)")
    ax.set_ylabel(r"$\nu_i$")
    ax.legend(title="Distance")
    ax.set_xticks(intensities)
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())  # nicer log tick labels
    plt.tight_layout()
    plt.show()

        