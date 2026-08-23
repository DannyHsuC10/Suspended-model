from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "suspension_utils.py").exists())
sys.path.insert(0, str(ROOT))

from suspension_utils import load_data, show_plots


def main() -> None:
    p = load_data(Path(__file__).with_name("data.csv"))
    g = p["max_g"]
    m = p["max_m"]
    ax = p["max_ax"]
    ay = p["max_ay"]
    h = p["max_h"]
    length = p["max_L"]
    track = p["max_t"]
    s = np.asarray(p["max_s"], dtype=float)

    fx = m * ax * g * h / (length / 2)
    fy = m * ay * g * h / (track / 2)
    k_pitch = fx / s / 2
    k_roll = fy / s / 2

    plt.figure()
    plt.plot(k_pitch, s, "-r", label="pitch")
    plt.plot(k_roll, s, "-b", label="roll")
    plt.axhline(0.025, linestyle="--", color="k")
    plt.grid(True)
    plt.legend()
    plt.xlabel("K")
    plt.ylabel("Suspension compression")
    plt.title("Pitch Stiffness Requirement vs Allowable Deformation")
    show_plots()


if __name__ == "__main__":
    main()
