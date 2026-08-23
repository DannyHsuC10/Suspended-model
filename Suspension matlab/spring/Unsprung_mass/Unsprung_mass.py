from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "suspension_utils.py").exists())
sys.path.insert(0, str(ROOT))

from suspension_utils import load_data, show_plots


def main() -> None:
    p = load_data(Path(__file__).with_name("data.csv"))
    ks = p["unsprung_Ks"]
    mr = p["unsprung_MR"]
    kt = p["unsprung_Kt"]
    mu = np.asarray(p["unsprung_mu"], dtype=float)

    kw = ks * mr**2
    fwh = (1 / (2 * np.pi)) * np.sqrt((kw + kt) / mu)

    plt.figure()
    plt.plot(mu, fwh, linewidth=2)
    plt.grid(True)
    plt.xlabel("Unsprung Mass (kg)")
    plt.ylabel("Wheel Hop Frequency (Hz)")
    plt.title("Unsprung Mass vs Wheel Hop Frequency")
    show_plots()


if __name__ == "__main__":
    main()
