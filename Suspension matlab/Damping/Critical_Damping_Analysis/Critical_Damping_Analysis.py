from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "suspension_utils.py").exists())
sys.path.insert(0, str(ROOT))

from suspension_utils import load_data, show_plots


def main() -> None:
    p = load_data(Path(__file__).with_name("data.csv"))
    m = p["critical_m"]
    k = np.asarray(p["critical_k"], dtype=float)

    cc = 2 * np.sqrt(k * m)
    fn = (1 / (2 * np.pi)) * np.sqrt(k / m)

    fig, axes = plt.subplots(2, 1)
    axes[0].plot(k / 1000, fn, linewidth=2)
    axes[0].grid(True)
    axes[0].set_xlabel("Spring Stiffness (kN/m)")
    axes[0].set_ylabel("Natural Frequency (Hz)")
    axes[0].set_title("Natural Frequency vs Spring Stiffness")
    axes[1].plot(k / 1000, cc, linewidth=2)
    axes[1].grid(True)
    axes[1].set_xlabel("Spring Stiffness (kN/m)")
    axes[1].set_ylabel("Critical Damping (N*s/m)")
    axes[1].set_title("Critical Damping vs Spring Stiffness")
    show_plots()


if __name__ == "__main__":
    main()
