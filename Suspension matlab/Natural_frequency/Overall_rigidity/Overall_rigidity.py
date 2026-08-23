from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "suspension_utils.py").exists())
sys.path.insert(0, str(ROOT))

from suspension_utils import load_data, show_plots


def main() -> None:
    p = load_data(Path(__file__).with_name("data.csv"))
    ks = p["overall_Ks"]
    kt = p["overall_Kt"]
    ratio = np.asarray(p["overall_ratio"], dtype=float)

    kc_list = ratio * ks
    keq_list = 1 / (1 / kt + 1 / ks + 1 / kc_list)
    keq_inf = 1 / (1 / kt + 1 / ks)

    plt.figure()
    plt.plot(ratio, keq_list, "o-", linewidth=2, label="Keq")
    plt.axvline(10, linestyle="--", color="r", linewidth=2, label="10x rule")
    plt.axhline(keq_inf, linestyle="--", color="k", linewidth=2, label="Saturation limit")
    plt.grid(True)
    plt.xlabel("Chassis stiffness / Suspension stiffness ratio (Kc / Ks)")
    plt.ylabel("Equivalent stiffness Keq (N/m)")
    plt.title("Effect of Chassis Stiffness on Overall Stiffness")
    plt.legend()
    show_plots()


if __name__ == "__main__":
    main()
