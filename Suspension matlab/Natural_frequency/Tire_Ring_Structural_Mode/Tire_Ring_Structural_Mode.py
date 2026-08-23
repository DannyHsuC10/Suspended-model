from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "suspension_utils.py").exists())
sys.path.insert(0, str(ROOT))

from suspension_utils import load_data, show_plots


def main() -> None:
    p = load_data(Path(__file__).with_name("data.csv"))
    radius = p["tire_R"]
    youngs_modulus = p["tire_E"]
    volume = p["tire_V"]
    mass = p["tire_m"]
    area = p["tire_A"]
    inertia = p["tire_I"]
    mode_max = int(p["tire_mode_max"])

    rho = mass / volume
    freq = np.zeros(mode_max)

    print("Mode   Frequency (Hz)")
    print("----------------------")
    for n in range(1, mode_max + 1):
        if n == 1:
            freq[n - 1] = 0.0
        else:
            omega = np.sqrt((youngs_modulus * inertia) / (rho * area * radius**4)) * (n**2 * (n**2 - 1))
            freq[n - 1] = omega / (2 * np.pi)
        print(f"{n:2d}     {freq[n - 1]:.2f}")

    plt.figure()
    plt.plot(np.arange(1, mode_max + 1), freq, "-o")
    plt.xlabel("Mode Number")
    plt.ylabel("Frequency (Hz)")
    plt.title("Tire Ring Mode Frequencies")
    plt.grid(True)
    show_plots()


if __name__ == "__main__":
    main()
