from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "suspension_utils.py").exists())
sys.path.insert(0, str(ROOT))

from suspension_utils import load_data, show_plots


def main() -> None:
    p = load_data(Path(__file__).with_name("data.csv"))
    g = p["aero_g"]
    m = p["aero_m"]
    a = p["aero_a"]
    h = p["aero_h"]
    length = p["aero_L"]
    theta = np.asarray(p["aero_theta"], dtype=float)

    s = length / 2 * theta
    force = m * a * g * h / (length / 2)
    stiffness = force / s / 2

    plt.figure()
    plt.plot(stiffness, theta, linewidth=2)
    plt.grid(True)
    plt.xlabel("K")
    plt.ylabel("theta_allowable")
    plt.title("Pitch Stiffness Requirement vs Allowable Deformation")
    show_plots()


if __name__ == "__main__":
    main()
