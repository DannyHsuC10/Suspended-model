from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "suspension_utils.py").exists())
sys.path.insert(0, str(ROOT))

from suspension_utils import load_data, show_plots


def quarter_car_ode(_t, x, ms, mu, ks, kt):
    xs, vs, xu, vu = x
    a_s = -(ks / ms) * (xs - xu)
    a_u = (ks / mu) * (xs - xu) - (kt / mu) * xu
    return [vs, a_s, vu, a_u]


def main() -> None:
    p = load_data(Path(__file__).with_name("data.csv"))
    ms = p["tire_ms"]
    mu = p["tire_mu"]
    ks = p["tire_ks"]
    kt = p["tire_kt"]
    x0 = [p["tire_xs0"], p["tire_vs0"], p["tire_xu0"], p["tire_vu0"]]
    tspan = np.asarray(p["tire_tspan"], dtype=float)
    t_eval = np.linspace(tspan[0], tspan[-1], 1000)

    sol = solve_ivp(quarter_car_ode, (tspan[0], tspan[-1]), x0, t_eval=t_eval, args=(ms, mu, ks, kt))
    t = sol.t
    xs, vs, xu, vu = sol.y

    ke = 0.5 * ms * vs**2 + 0.5 * mu * vu**2
    pe = 0.5 * ks * (xs - xu) ** 2 + 0.5 * kt * xu**2
    energy = ke + pe
    energy_error = (energy - energy[0]) / energy[0] * 100

    fig, axes = plt.subplots(3, 1)
    axes[0].plot(t, xs, linewidth=2, label="Sprung")
    axes[0].plot(t, xu, "--", linewidth=1.5, label="Unsprung")
    axes[0].grid(True)
    axes[0].set_ylabel("Position (m)")
    axes[0].set_title("Quarter Car (No Damping) - ODE Solution")
    axes[0].legend()
    axes[1].plot(t, energy, linewidth=2)
    axes[1].grid(True)
    axes[1].set_ylabel("Total Energy (J)")
    axes[2].plot(t, energy_error, linewidth=2)
    axes[2].grid(True)
    axes[2].set_xlabel("Time (s)")
    axes[2].set_ylabel("Energy Error (%)")
    show_plots()


if __name__ == "__main__":
    main()
