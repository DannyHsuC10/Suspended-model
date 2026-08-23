from pathlib import Path
import sys

import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "suspension_utils.py").exists())
sys.path.insert(0, str(ROOT))

from suspension_utils import load_data


def main() -> None:
    params = load_data(Path(__file__).with_name("data.csv"))
    globals().update(params)

    print(f"\n F_driver = {F_driver:.2f}")

    f_mc = F_driver * PR
    print(f"\n F_mc = {f_mc:.2f}")

    bb_r = 1 - balance_bar
    bb_f = balance_bar

    a_mc_f = np.pi * (D_mc_f / 2) ** 2
    a_mc_r = np.pi * (D_mc_r / 2) ** 2

    p_mc_f = f_mc * bb_f / a_mc_f
    p_mc_r = f_mc * bb_r / a_mc_r

    a_caliper_f = N_caliper_f * np.pi * (D_caliper_f / 2) ** 2
    a_caliper_r = N_caliper_r * np.pi * (D_caliper_r / 2) ** 2

    f_caliper_f = p_mc_f * mu_pad * a_caliper_f
    f_caliper_r = p_mc_r * mu_pad * a_caliper_r

    r_disc = r_disc_o / 2 - d_gap
    f_brake_f = f_caliper_f * r_disc * 2 / r_w
    f_brake_r = f_caliper_r * r_disc * 2 / r_w

    print(f"\n F_brake_f = {f_brake_f:.2f}")
    print(f"\n F_brake_r = {f_brake_r:.2f}")
    print(f"\n F_brake = {f_brake_f + f_brake_r:.2f}")


if __name__ == "__main__":
    main()
