from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "suspension_utils.py").exists())
sys.path.insert(0, str(ROOT))

from suspension_utils import load_data, show_plots


def main() -> None:
    p = load_data(Path(__file__).with_name("data.csv"))
    m = p["time_m"]
    k = p["time_k"]
    x0 = p["time_x0"]
    v0 = p["time_v0"]
    t_end = p["time_t_end"]
    dt_list = np.asarray(p["time_dt_list"], dtype=float)

    for dt in dt_list:
        t = np.arange(0, t_end + dt / 2, dt)
        x = np.zeros_like(t)
        v = np.zeros_like(t)
        a = np.zeros_like(t)
        x[0] = x0
        v[0] = v0

        for i in range(len(t) - 1):
            a[i] = -(k / m) * x[i]
            v[i + 1] = v[i] + a[i] * dt
            x[i + 1] = x[i] + v[i] * dt
        a[-1] = -(k / m) * x[-1]

        ke = 0.5 * m * v**2
        pe = 0.5 * k * x**2
        e_total = ke + pe
        e_error_percent = (e_total - e_total[0]) / e_total[0] * 100

        fig, axes = plt.subplots(3, 1, num=f"dt = {dt:g}")
        axes[0].plot(t, x, linewidth=2)
        axes[0].grid(True)
        axes[0].set_ylabel("Displacement (m)")
        axes[0].set_title(f"Explicit Euler  |  dt = {dt:g}")
        axes[1].plot(t, e_total, linewidth=2)
        axes[1].grid(True)
        axes[1].set_ylabel("Energy (J)")
        axes[2].plot(t, e_error_percent, linewidth=2)
        axes[2].grid(True)
        axes[2].set_xlabel("Time (s)")
        axes[2].set_ylabel("Energy Error (%)")
    show_plots()


if __name__ == "__main__":
    main()
