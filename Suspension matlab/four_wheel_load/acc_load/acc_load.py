from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "suspension_utils.py").exists())
sys.path.insert(0, str(ROOT))

from suspension_utils import load_data, show_plots


def main() -> None:
    p = load_data(Path(__file__).with_name("data.csv"))
    g = p["acc_g"]
    wheelbase = p["acc_l"]
    l_f = p["acc_l_f"]
    mass = p["acc_m"]
    mu_w = p["acc_mu_w"]
    h_cog = p["acc_h_cog"]

    n_r_static = mass * g * l_f / wheelbase
    n_f_static = mass * g - n_r_static
    print(f"Rear static load  : {n_r_static:.2f} N")
    print(f"Front static load : {n_f_static:.2f} N")

    a_range = np.linspace(0, mu_w * g, int(p["acc_a_count"]))
    n_r = (mass * a_range * h_cog + mass * g * l_f) / wheelbase
    n_f = mass * g - n_r

    print(f"Maximum Rear Load  : {np.max(n_r):.2f} N")
    print(f"Maximum Front Load : {np.max(n_f):.2f} N")
    print(f"Minimum Rear Load  : {np.min(n_r):.2f} N")
    print(f"Minimum Front Load : {np.min(n_f):.2f} N")

    plt.figure()
    plt.plot(a_range / g, n_f, linewidth=2, label="Front Load")
    plt.plot(a_range / g, n_r, linewidth=2, label="Rear Load")
    plt.axhline(n_f_static, linestyle="--", label="Front Static")
    plt.axhline(n_r_static, linestyle="--", label="Rear Static")
    plt.xlabel("Longitudinal Acceleration [g]")
    plt.ylabel("Normal Load [N]")
    plt.title("Normal Load vs Acceleration")
    plt.legend()
    plt.grid(True)
    show_plots()


if __name__ == "__main__":
    main()
