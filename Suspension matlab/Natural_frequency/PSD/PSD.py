from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "suspension_utils.py").exists())
sys.path.insert(0, str(ROOT))

from suspension_utils import load_data, show_plots


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    p = load_data(script_dir / "data.csv")

    road_length = p["psd_L"]
    dx = p["psd_dx"]
    x = np.arange(0, road_length + dx / 2, dx)
    point_count = len(x)

    n0 = p["psd_n0"]
    gd0 = p["psd_Gd0"]
    w = p["psd_w"]
    dn = 1 / road_length
    n = np.arange(0, point_count // 2 + 1) * dn
    n[0] = n[1]
    gd = gd0 * (n / n0) ** (-w)

    phi = 2 * np.pi * np.random.rand(len(n))
    amplitude = np.sqrt(2 * gd * dn)
    spectrum = amplitude * np.exp(1j * phi)
    full_spectrum = np.concatenate([spectrum, np.conj(spectrum[1:-1][::-1])])
    road = np.real(np.fft.ifft(full_spectrum)) * len(full_spectrum)
    x = x[: len(road)]

    plt.figure()
    plt.plot(x, road)
    plt.xlabel("Distance (m)")
    plt.ylabel("Road Height (m)")
    plt.title("ISO Road Profile")
    plt.grid(True)

    data = pd.read_excel(script_dir / p["psd_speed_file"])
    time = data["time"].to_numpy()
    speed = data["speed"].to_numpy()

    plt.figure()
    plt.plot(time, speed, linewidth=1.5)
    plt.xlabel("Time (s)")
    plt.ylabel("Speed (m/s)")
    plt.title("Vehicle Speed Trace")
    plt.grid(True)

    plt.figure()
    plt.hist(speed, bins=30)
    plt.xlabel("Speed (m/s)")
    plt.ylabel("Counts")
    plt.title("Speed Distribution")
    plt.grid(True)

    plt.figure()
    plt.hist(speed, bins=30, density=True)
    plt.xlabel("Speed (m/s)")
    plt.ylabel("Probability Density")
    plt.title("Speed Probability Density")
    plt.grid(True)

    n_spatial = n[1:]
    counts, edges = np.histogram(speed, bins=int(p["psd_speed_hist_bins"]), density=True)
    v_center = (edges[:-1] + edges[1:]) / 2

    f_all = []
    w_all = []
    road_weight = gd[1:]
    for vi, pv in zip(v_center, counts):
        f_exc = n_spatial * vi
        weight = pv * road_weight
        f_all.append(f_exc)
        w_all.append(weight)
    f_all = np.concatenate(f_all)
    w_all = np.concatenate(w_all)

    f_bins = np.asarray(p["psd_f_bins"], dtype=float)
    weighted_counts, _ = np.histogram(f_all, bins=f_bins)
    weighted_counts = weighted_counts.astype(float)
    weighted_counts += np.histogram(f_all, bins=f_bins, weights=w_all)[0]
    if weighted_counts.max() > 0:
        weighted_counts /= weighted_counts.max()

    f_center = (f_bins[:-1] + f_bins[1:]) / 2
    plt.figure()
    plt.plot(f_center, weighted_counts, linewidth=2)
    plt.xlabel("Excitation Frequency (Hz)")
    plt.ylabel("Normalized Energy")
    plt.title("Weighted Excitation Frequency Spectrum")
    plt.grid(True)
    plt.xlim([0, 50])

    energy = weighted_counts / weighted_counts.sum()
    plt.figure()
    plt.plot(f_center, energy, linewidth=2)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Normalized Energy")
    plt.title("Frequency vs Excitation Energy")
    plt.grid(True)
    plt.xlim([0, 30])

    cum_energy = np.cumsum(energy)
    plt.figure()
    plt.plot(f_center, cum_energy, linewidth=2)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Cumulative Energy")
    plt.title("Cumulative Excitation Energy")
    plt.grid(True)
    plt.xlim([0, 30])
    plt.ylim([0, 1])

    threshold = p["psd_energy_threshold_factor"] * np.max(energy)
    dominant_freq = f_center[energy >= threshold]
    print("Dominant excitation band:")
    if dominant_freq.size:
        print(f"{dominant_freq.min():.2f} Hz ~ {dominant_freq.max():.2f} Hz")
    else:
        print("No dominant band found.")

    mean_speed = np.mean(speed)
    t_from_road = x / mean_speed
    fs = 1 / np.mean(np.diff(t_from_road))
    y = np.fft.fft(road)
    p2 = np.abs(y / len(road))
    half_n = len(road) // 2
    p1 = p2[:half_n]
    if p1.size > 2:
        p1[1:-1] *= 2
    freq = fs * np.arange(half_n) / len(road)

    plt.figure()
    plt.plot(freq, p1, linewidth=1.5)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.title("Road Profile FFT")
    plt.grid(True)
    plt.xlim([0, 50])

    plt.figure()
    plt.loglog(freq[1:], p1[1:], linewidth=1.5)
    plt.grid(True)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.title("Road FFT (log-log)")
    show_plots()


if __name__ == "__main__":
    main()
