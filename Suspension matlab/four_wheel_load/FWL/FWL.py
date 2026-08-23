from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "suspension_utils.py").exists())
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "VehicleDynamicsSimulator"))

from suspension_utils import load_data, show_plots
from VehicleDynamicsSimulator import VehicleDynamicsSimulator


def main() -> None:
    p = load_data(Path(__file__).with_name("data.csv"))
    g = p["fwl_g"]

    sim = VehicleDynamicsSimulator(g)
    sim.m = p["fwl_m"]
    sim.h = p["fwl_h"]
    sim.L = p["fwl_L"]
    sim.W = sim.m * sim.g
    sim.L_front = sim.L * p["fwl_rear_axle_ratio"]
    sim.L_rear = sim.L * p["fwl_front_axle_ratio"]
    sim.t_front = p["fwl_t_front"]
    sim.t_rear = p["fwl_t_rear"]
    sim.K = np.diag(
        [
            p["fwl_K_front_left"],
            p["fwl_K_front_right"],
            p["fwl_K_rear_left"],
            p["fwl_K_rear_right"],
        ]
    )

    f_add = p["fwl_F_add"]
    cf_rela = p["fwl_CF_rela"]
    ax_range = np.linspace(p["fwl_ax_min_g"] * g, p["fwl_ax_max_g"] * g, int(p["fwl_grid_count"]))
    ay_range = np.linspace(p["fwl_ay_min_g"] * g, p["fwl_ay_max_g"] * g, int(p["fwl_grid_count"]))
    ax_grid, ay_grid = np.meshgrid(ax_range, ay_range)

    fl = np.zeros_like(ax_grid)
    fr = np.zeros_like(ax_grid)
    rl = np.zeros_like(ax_grid)
    rr = np.zeros_like(ax_grid)

    for idx in np.ndindex(ax_grid.shape):
        loads = sim.solve_lagrange(ax_grid[idx], ay_grid[idx], f_add, cf_rela, check=False)
        fl[idx], fr[idx], rl[idx], rr[idx] = loads

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    colors = [(0.2, 0.6, 0.8), (0.9, 0.4, 0.3), (0.3, 0.9, 0.3), (0.8, 0.2, 0.8)]
    names = ["FL", "FR", "RL", "RR"]
    data = [fl, fr, rl, rr]

    for color, name, wheel_load in zip(colors, names, data):
        ax.plot_surface(ax_grid, ay_grid, wheel_load, color=color, alpha=0.5, linewidth=0, label=name)

    ax.set_xlabel("ax (m/s^2)")
    ax.set_ylabel("ay (m/s^2)")
    ax.set_zlabel("Wheel Load (N)")
    ax.set_title("Four Wheel Loads Overlay vs ax and ay")
    ax.view_init(elev=30, azim=45)
    ax.legend()
    show_plots()


if __name__ == "__main__":
    main()
