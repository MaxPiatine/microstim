import matplotlib.pyplot as plt
from numpy import max

def plot(x, t, i_steps, step, e_radius, i_radius, v_e, v_i):
    
    figure, ax = plt.subplots(3, 2, figsize=(10, 8))


    # row1
    for i in range(0, len(i_steps), step):
        ax[0][0].plot(x, v_e[i], label="ve[%i]"%i)
        ax[0][1].plot(x, v_i[i], label="vi[%i]"%i)


    ax[0][0].set_xlabel(r"distance ($\mu$x)"), ax[0][1].set_xlabel(r"distance ($\mu$x)")
    ax[0][0].set_ylabel("potential (mV)")
    ax[0][0].set_title("e_potential time steps"), ax[0][1].set_title("i_potential time steps")
    ax[0][0].legend(), ax[0][1].legend()
    # ax[0][0].set_ylim(0, 50), ax[0][1].set_ylim(0, 50)
    # ax[0][0].set_xlim(0, 400), ax[0][1].set_xlim(0, 400)


    # row2
    ax[1][0].plot(t, e_radius)
    ax[1][1].plot(t, i_radius)

    ax[1][0].set_title("e_rho"), ax[1][1].set_title("i_rho")

    ax[1][0].set_xlabel("normalized time"), ax[2][1].set_xlabel("normalized time")
    ax[1][0].set_ylabel(r"radius ($\mu$m)")


    # row3
    # ax[2][0].plot(X_RANGE, max(v_e, axis=0), label="amp exc")
    # ax[2][0].plot(X_RANGE, max(v_i, axis=0), label="amp inh")
    ax[2][0].plot(x, max(v_e, axis=0), label="no amp")

    ax[2][1].plot(t, v_e[:, 100], label="amp exc")
    # ax[2][1].plot(arange(0, DT * N), v_i[:, 100], label="amp inh")

    ax[2][0].set_xlabel(r"distance ($\mu$x)"), ax[2][1].set_xlabel("normalized time")
    ax[2][0].set_ylabel("max pot (mV)")
    ax[2][0].set_title("Max Potential vs Distance"), ax[2][1].set_title("Max Potential vs Normalized Time")
    # ax[2][0].set_ylim(0, 30)
    # ax[2][0].set_xlim(0, 1000)
    ax[2][0].legend()

    # show
    plt.tight_layout()
    plt.show()
