
import torch.nn.functional as F
import torch
import numpy as np
import time

from microstim.config import config, DEVICE
from microstim.utils import normal, zeros, V_eph, sigmoid, x0s
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
    200: {"inh": {"x0": 243.3, "k": 0.112}, "exc": {"x0": 75, "k": 0.064}},
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
    
    nu_e = torch.tensor(rate(DISTANCE_RANGE, v_e, x0s(v_e)))
    nu_i = torch.tensor(rate(DISTANCE_RANGE, v_i, x0s(v_i)))


    return v_e, v_i, nu_e, nu_i

if __name__ == "__main__":
    _, boost, _ = setup(config)
    intensities = [10, 20, 50, 100, 200, 500, 1000]
    lst_e, lst_i = [], []
    for intensity in intensities:
        _, _, nu_e, nu_i = t_o(intensity, sigmoid, boost)
        lst_e.append(nu_e)
        lst_i.append(nu_i)

    positions = [50, 100, 250, 750]     
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(8, 6))
    ax = axes.flatten()  # make indexing easier
    ax[0].set_xscale('log')
    ax[1].set_xscale('log')

    for pos in positions:
        pidx = int(round(pos / DX))
        probs_e = [row[pidx].cpu().item() for row in lst_e]  # row is tensor (L,)
        ax[0].plot(intensities, probs_e, marker='o', label=f"{pos} μm")

        probs_i = [row[pidx].cpu().item() for row in lst_i]  # row is tensor (L,)
        ax[1].plot(intensities, probs_i, marker='o', label=f"{pos} μm")

    fit_e = fits[200]["exc"]
    fit_i = fits[200]["inh"]
    ax[2].plot(DISTANCE_RANGE.cpu().numpy(), lst_e[4].cpu().numpy(), label=r"$\nu_e$", color='blue')
    ax[2].plot(DISTANCE_RANGE.cpu().numpy(), lst_i[4].cpu().numpy(), label=r"$\nu_i$", color='red')
    ax[2].plot(DISTANCE_RANGE.cpu().numpy(), torch.sigmoid(-fit_e["k"]*(DISTANCE_RANGE-fit_e["x0"])).cpu().numpy(), label=r"exp. $\nu_e$", color='teal')
    ax[2].plot(DISTANCE_RANGE.cpu().numpy(), torch.sigmoid(-fit_i["k"]*(DISTANCE_RANGE-fit_i["x0"])).cpu().numpy(), label=r"exp. $\nu_i$", color='pink')
    ax[2].set_xlabel("Distance (µm)")
    ax[2].set_ylabel("Firing Probability")
    ax[2].legend(title="Intensity 200 µA")
    ax[0].set_xlabel("Intensity (µA)")
    ax[1].set_xlabel("Intensity (µA)")
    ax[0].set_ylabel(r"$\nu_e$")
    ax[1].set_ylabel(r"$\nu_i$")
    ax[0].legend(title="Distance")
    # ax[1].legend(title="Distance")
    ax[0].set_xticks(intensities)
    ax[1].set_xticks(intensities)
    ax[0].get_xaxis().set_major_formatter(plt.ScalarFormatter())  # nicer log tick labels
    plt.tight_layout()
    plt.savefig("results/new/t0.png", format="png", bbox_inches="tight")
    plt.show()

        