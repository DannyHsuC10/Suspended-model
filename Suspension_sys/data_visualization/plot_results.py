import numpy as np
import matplotlib.pyplot as plt


def plot_vehicle_results(
    result,
    figsize=(12, 18),
    show=True,
):
    """
    Plot vehicle simulation results.

    Parameters
    ----------
    result : dict
        Simulation result dictionary.

        Required keys:
            t
            zs
            zu
            theta
            s
            N

    figsize : tuple
        Figure size.

    show : bool
        Whether to call plt.show().

    Returns
    -------
    fig, ax
    """

    # ================================
    # Convert data
    # ================================
    t = np.asarray(result["t"])

    zs = np.asarray(result["zs"])
    zu = np.asarray(result["zu"])

    theta = np.asarray(result["theta"])
    s = np.asarray(result["s"])

    N = np.asarray(result["N"])

    wheel_name = ["FL", "FR", "RL", "RR"]

    # ================================
    # Figure
    # ================================
    fig, ax = plt.subplots(
        5,
        1,
        figsize=figsize,
        sharex=True,
    )

    # --------------------------------------------------
    # 1. Sprung displacement
    # --------------------------------------------------
    for i in range(4):
        ax[0].plot(t, zs[:, i], label=wheel_name[i])

    ax[0].set_ylabel("zs (m)")
    ax[0].set_title("Sprung displacement")
    ax[0].grid(True)
    ax[0].legend()

    # --------------------------------------------------
    # 2. Unsprung displacement
    # --------------------------------------------------
    for i in range(4):
        ax[1].plot(t, zu[:, i], label=wheel_name[i])

    ax[1].set_ylabel("zu (m)")
    ax[1].set_title("Unsprung displacement")
    ax[1].grid(True)
    ax[1].legend()

    # --------------------------------------------------
    # 3. Body attitude
    # --------------------------------------------------
    ax[2].plot(
        t,
        np.rad2deg(theta[:, 0]),
        label="Roll",
    )

    ax[2].plot(
        t,
        np.rad2deg(theta[:, 2]),
        label="Pitch",
    )

    ax[2].set_ylabel("Angle (deg)")
    ax[2].set_title("Body attitude")
    ax[2].grid(True)
    ax[2].legend()

    # --------------------------------------------------
    # 4. CG vertical position
    # --------------------------------------------------
    ax[3].plot(
        t,
        s[:, 2],
        label="CG z",
    )

    ax[3].set_ylabel("z (m)")
    ax[3].set_title("CG vertical position")
    ax[3].grid(True)
    ax[3].legend()

    # --------------------------------------------------
    # 5. Tire normal force
    # --------------------------------------------------
    for i in range(4):
        ax[4].plot(
            t,
            N[:, i],
            label=wheel_name[i],
        )

    ax[4].plot(
        t,
        np.sum(N, axis=1),
        "k--",
        linewidth=2,
        label="Total",
    )

    ax[4].set_ylabel("Normal Force (N)")
    ax[4].set_xlabel("Time (s)")
    ax[4].set_title("Tire Normal Force")
    ax[4].grid(True)
    ax[4].legend()

    plt.tight_layout()

    if show:
        plt.show()

    return fig, ax