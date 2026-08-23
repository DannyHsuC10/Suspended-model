from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "suspension_utils.py").exists())
sys.path.insert(0, str(ROOT))

from suspension_utils import load_data, show_plots


def road_input(t, step_time, step_height):
    return 0.0 if t < step_time else step_height


def quarter_car_damped_ode(t, x, ms, mu, ks, kt, cs, step_time, step_height):
    xs, vs, xu, vu = x
    xr = road_input(t, step_time, step_height)
    dx = xs - xu
    dv = vs - vu
    xt = xu - xr
    a_s = -(ks / ms) * dx - (cs / ms) * dv
    a_u = (ks / mu) * dx + (cs / mu) * dv - (kt / mu) * xt
    return [vs, a_s, vu, a_u]


def main() -> None:
    p = load_data(Path(__file__).with_name("data.csv"))
    ms = p["quarter_ms"]
    mu = p["quarter_mu"]
    ks = p["quarter_ks"]
    kt = p["quarter_kt"]
    zeta = p["quarter_zeta"]
    x0 = [p["quarter_xs0"], p["quarter_vs0"], p["quarter_xu0"], p["quarter_vu0"]]
    tspan = np.asarray(p["quarter_tspan"], dtype=float)
    step_time = p["quarter_road_step_time"]
    step_height = p["quarter_road_step_height"]

    cc = 2 * np.sqrt(ks * ms)
    cs = zeta * cc
    print(f"Critical damping = {cc:.2f} Ns/m")
    print(f"Suspension damping = {cs:.2f} Ns/m")

    t_eval = np.linspace(tspan[0], tspan[-1], 1000)
    sol = solve_ivp(
        quarter_car_damped_ode,
        (tspan[0], tspan[-1]),
        x0,
        t_eval=t_eval,
        args=(ms, mu, ks, kt, cs, step_time, step_height),
    )

    t = sol.t
    xs, vs, xu, vu = sol.y
    xr = np.where(t >= step_time, step_height, 0.0)
    dx = xs - xu
    dv = vs - vu
    xt = xu - xr
    a_s = -(ks / ms) * dx - (cs / ms) * dv
    a_u = (ks / mu) * dx + (cs / mu) * dv - (kt / mu) * xt
    energy = 0.5 * ms * vs**2 + 0.5 * mu * vu**2 + 0.5 * ks * (xs - xu) ** 2 + 0.5 * kt * xu**2

    fig, axes = plt.subplots(4, 1)
    axes[0].plot(t, xs, linewidth=2, label="Sprung")
    axes[0].plot(t, xu, "--", linewidth=1.5, label="Unsprung")
    axes[0].grid(True)
    axes[0].set_ylabel("Position (m)")
    axes[0].set_title(f"Quarter Car  |  zeta = {zeta:g}")
    axes[0].legend()
    axes[1].plot(t, vs, linewidth=2, label="Sprung")
    axes[1].plot(t, vu, "--", linewidth=1.5, label="Unsprung")
    axes[1].grid(True)
    axes[1].set_ylabel("Velocity (m/s)")
    axes[1].legend()
    axes[2].plot(t, a_s, linewidth=2, label="Sprung")
    axes[2].plot(t, a_u, "--", linewidth=1.5, label="Unsprung")
    axes[2].grid(True)
    axes[2].set_xlabel("Time (s)")
    axes[2].set_ylabel("Acceleration (m/s^2)")
    axes[2].set_title("Acceleration")
    axes[2].legend()
    axes[3].plot(t, energy, linewidth=2)
    axes[3].grid(True)
    axes[3].set_xlabel("Time (s)")
    axes[3].set_ylabel("Energy (J)")
    axes[3].set_title("Energy Dissipation")
    show_plots()


if __name__ == "__main__":
    main()
