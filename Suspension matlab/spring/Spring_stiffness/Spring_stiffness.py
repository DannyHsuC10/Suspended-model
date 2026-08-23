from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "suspension_utils.py").exists())
sys.path.insert(0, str(ROOT))

from suspension_utils import load_data, show_plots


def main() -> None:
    p = load_data(Path(__file__).with_name("data.csv"))
    m = p["spring_stiffness_m"]
    k = np.asarray(p["spring_stiffness_k"], dtype=float)

    fn = (1 / (2 * np.pi)) * np.sqrt(k / m)

    plt.figure()
    plt.plot(k / 1000, fn, linewidth=2)
    plt.grid(True)
    plt.xlabel("Spring Stiffness (kN/m)")
    plt.ylabel("Natural Frequency (Hz)")
    plt.title("Natural Frequency vs Spring Stiffness")
    show_plots()


if __name__ == "__main__":
    main()
