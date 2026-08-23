from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "suspension_utils.py").exists())
sys.path.insert(0, str(ROOT))

from suspension_utils import load_data, show_plots


def quarter_car_damped_ode(_t, x, ms, mu, ks, kt, cs):
    xs, vs, xu, vu = x
    dx = xs - xu
    dv = vs - vu
    a_s = -(ks / ms) * dx - (cs / ms) * dv
    a_u = (ks / mu) * dx + (cs / mu) * dv - (kt / mu) * xu
    return [vs, a_s, vu, a_u]


def main() -> None:
    p = load_data(Path(__file__).with_name("data.csv"))
    ms = p["damped_ms"]
    mu = p["damped_mu"]
    ks = p["damped_ks"]
    kt = p["damped_kt"]
    g = p["damped_g"]
    zeta_list = np.asarray(p["damped_zeta_list"], dtype=float)
    x0 = [p["damped_xs0"], p["damped_vs0"], p["damped_xu0"], p["damped_vu0"]]
    tspan = np.asarray(p["damped_tspan"], dtype=float)
    t_eval = np.linspace(tspan[0], tspan[-1], 1000)

    cc = 2 * np.sqrt(ks * ms)
    fz_static = (ms + mu) * g
    fig, axes = plt.subplots(2, 1)

    for zeta in zeta_list:
        cs = zeta * cc
        sol = solve_ivp(
            quarter_car_damped_ode,
            (tspan[0], tspan[-1]),
            x0,
            t_eval=t_eval,
            args=(ms, mu, ks, kt, cs),
        )
        t = sol.t
        xs = sol.y[0]
        xu = sol.y[2]
        dfz = fz_static + kt * xu - fz_static
        label = f"zeta = {zeta:g}"
        axes[0].plot(t, xs, linewidth=2, label=label)
        axes[1].plot(t, dfz, linewidth=2, label=label)

    axes[0].grid(True)
    axes[0].set_xlabel("Time (s)")
    axes[0].set_ylabel("Sprung Displacement (m)")
    axes[0].set_title("Damping Ratio Sweep")
    axes[0].legend()
    axes[1].grid(True)
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Delta Fz (N)")
    axes[1].set_title("Dynamic Tire Load Variation")
    axes[1].legend()
    show_plots()


if __name__ == "__main__":
    main()
