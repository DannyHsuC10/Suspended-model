from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "suspension_utils.py").exists())
sys.path.insert(0, str(ROOT))

from suspension_utils import load_data, show_plots


def main() -> None:
    p = load_data(Path(__file__).with_name("data.csv"))
    m = p["osc_m"]
    k = p["osc_k"]
    x0 = p["osc_x0"]
    v0 = p["osc_v0"]
    dt = p["osc_dt"]
    t_end = p["osc_t_end"]

    wn = np.sqrt(k / m)
    fn = wn / (2 * np.pi)
    print(f"Natural Frequency = {fn:.2f} Hz")

    t = np.arange(0, t_end + dt / 2, dt)
    n = len(t)

    x_analytical = x0 * np.cos(wn * t) + (v0 / wn) * np.sin(wn * t)
    x_num = np.zeros(n)
    v_num = np.zeros(n)
    a_num = np.zeros(n)
    x_num[0] = x0
    v_num[0] = v0

    for i in range(n - 1):
        a_num[i] = -(k / m) * x_num[i]
        v_num[i + 1] = v_num[i] + a_num[i] * dt
        x_num[i + 1] = x_num[i] + v_num[i] * dt
    a_num[-1] = -(k / m) * x_num[-1]

    plt.figure()
    plt.plot(t, x_analytical, linewidth=2, label="Analytical")
    plt.plot(t, x_num, "--", linewidth=1.5, label="Explicit Euler")
    plt.grid(True)
    plt.xlabel("Time (s)")
    plt.ylabel("Displacement (m)")
    plt.title("Analytical vs Numerical Solution")
    plt.legend()

    abs_error = np.abs(x_num - x_analytical)
    rel_error = abs_error / (np.abs(x_analytical) + 1e-12) * 100

    fig, axes = plt.subplots(2, 1)
    axes[0].plot(t, abs_error, linewidth=2)
    axes[0].grid(True)
    axes[0].set_ylabel("Absolute Error (m)")
    axes[0].set_title("Numerical Error")
    axes[1].plot(t, rel_error, linewidth=2)
    axes[1].grid(True)
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Relative Error (%)")
    show_plots()


if __name__ == "__main__":
    main()
