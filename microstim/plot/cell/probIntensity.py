# new function

import matplotlib.pylab as plt

from microstim.main import model, DT, DISTANCE_RANGE, DX, N
from microstim.utils import sigmoid
from microstim.plot.cell.utils import setup, TIME_RANGE

def main():
    global config, is_prod
    weights, boost, sigma = setup(config)
    
    intensities = [10, 20, 50, 100, 200, 500, 1000]
    time = N//2
    lst_e, lst_i = [], []
    for intensity in intensities:
        _, _, _, _, nu_e, nu_i = model(intensity, weights, sigma, sigmoid, boost, radius_only=True)

        lst_e.append(nu_e[time])
        lst_i.append(nu_i[time])

    positions = [50, 100, 250, 750]     
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(8, 6))
    ax = axes.flatten()  # make indexing easier
    ax[0].set_xscale('log')
    ax[1].set_xscale('log')

    for pos in positions:
        pidx = int(round(pos / DX))
        probs_e = [row[pidx] for row in lst_e]  # row is tensor (L,)
        ax[0].plot(intensities, probs_e, marker='o', label=f"{pos} μm")

        probs_i = [row[pidx] for row in lst_i]  # row is tensor (L,)
        ax[1].plot(intensities, probs_i, marker='o', label=f"{pos} μm")


    ax[2].plot(DISTANCE_RANGE.cpu().numpy(), lst_e[4], label=r"$\nu_e$", color='blue')
    ax[2].plot(DISTANCE_RANGE.cpu().numpy(), lst_i[4], label=r"$\nu_i$", color='red')
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
    # plt.savefig("results/new/t0.png", format="png", bbox_inches="tight")
    plt.show()