from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "suspension_utils.py").exists())
sys.path.insert(0, str(ROOT))

from suspension_utils import load_data, show_plots


def main() -> None:
    p = load_data(Path(__file__).with_name("data.csv"))
    mr = p["ride_MR"]
    kt = p["ride_Kt"]
    ks = np.asarray(p["ride_Ks"], dtype=float)

    kw = ks * mr**2
    kr = (kw * kt) / (kw + kt)

    plt.figure()
    plt.plot(ks / 1000, kr / 1000, linewidth=2, label="Ride Rate")
    plt.axhline(kt / 1000, linestyle="--", label="Tire Stiffness")
    plt.grid(True)
    plt.xlabel("Spring Rate (kN/m)")
    plt.ylabel("Ride Rate (kN/m)")
    plt.title("Spring Rate vs Ride Rate")
    plt.legend()
    show_plots()


if __name__ == "__main__":
    main()
