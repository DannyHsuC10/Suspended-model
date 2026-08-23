from __future__ import annotations

from pathlib import Path
import sys

import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "suspension_utils.py").exists())
sys.path.insert(0, str(ROOT))

from suspension_utils import load_data


def _cfg(config: dict, name: str, default):
    return config.get(name, default)


class VehicleDynamicsSimulator:
    def __init__(self, g_val: float | None = None):
        data_file = Path(__file__).with_name("data.csv")
        config = load_data(data_file) if data_file.exists() else {}

        self.g = _cfg(config, "sim_g", 9.81) if g_val is None else g_val
        self.m = _cfg(config, "sim_m", 360)
        self.h = _cfg(config, "sim_h", 0.286)
        self.W = self.m * self.g
        self.L_rear = _cfg(config, "sim_L_rear", 0.744)
        self.L_front = _cfg(config, "sim_L_front", 0.806)
        self.L = self.L_front + self.L_rear
        self.t_front = _cfg(config, "sim_t_front", 1.25)
        self.t_rear = _cfg(config, "sim_t_rear", 1.25)

        self.K = np.diag(
            [
                _cfg(config, "sim_K_front_left", 30000),
                _cfg(config, "sim_K_front_right", 30000),
                _cfg(config, "sim_K_rear_left", 27000),
                _cfg(config, "sim_K_rear_right", 27000),
            ]
        )
        self.K_modal = np.diag(
            [
                _cfg(config, "sim_K_modal_heave", 3050),
                _cfg(config, "sim_K_modal_roll", 550),
                _cfg(config, "sim_K_modal_pitch", 2500),
            ]
        )
        coupled = _cfg(config, "sim_K_modal_coupled_roll_coupling", 2900)
        self.K_modal_coupled = np.array(
            [
                [_cfg(config, "sim_K_modal_coupled_heave", 3050), 0, 0, 0],
                [0, _cfg(config, "sim_K_modal_coupled_roll_base", 600) + coupled, -coupled, 0],
                [0, -coupled, _cfg(config, "sim_K_modal_coupled_pitch_base", 500) + coupled, 0],
                [0, 0, 0, _cfg(config, "sim_K_modal_coupled_pitch", 2500)],
            ],
            dtype=float,
        )
        self.K_tire = np.ones(4) * _cfg(config, "sim_K_tire", 56000)

    def get_geometry(self):
        x_front = self.L_front
        x_rear = -self.L_rear
        y_left = -self.t_front / 2
        y_right = self.t_front / 2
        y_left_r = -self.t_rear / 2
        y_right_r = self.t_rear / 2
        x_pos = np.array([x_front, x_front, x_rear, x_rear], dtype=float)
        y_pos = np.array([y_left, y_right, y_left_r, y_right_r], dtype=float)
        z_pos = np.ones(4)
        return x_pos, y_pos, z_pos

    def external_effects(self, F_add=None, CF_rela=None):
        if F_add is None or np.asarray(F_add).size == 0:
            return 0.0, 0.0, 0.0
        force = np.asarray(F_add, dtype=float).ravel()
        fx, fy, fz = force[:3]
        r = np.array([0.0, 0.0, self.h]) if CF_rela is None or np.asarray(CF_rela).size == 0 else np.asarray(CF_rela, dtype=float).ravel()
        mx = r[1] * fz - r[2] * fy
        my = r[2] * fx - r[0] * fz
        return fz, mx, my

    def get_Ab(self, ax, ay, F_add=None, CF_rela=None):
        x_pos, y_pos, _ = self.get_geometry()
        fz_add, mx_add, my_add = self.external_effects(F_add, CF_rela)
        A = np.array(
            [
                [1, 1, 1, 1],
                [y_pos[0], y_pos[1], y_pos[2], y_pos[3]],
                [x_pos[0], x_pos[1], x_pos[2], x_pos[3]],
            ],
            dtype=float,
        )
        b = np.array([fz_add - self.m * self.g, self.m * ay * self.h + mx_add, self.m * ax * self.h + my_add], dtype=float)
        return A, b, mx_add, my_add

    def debug_balance(self, ax, ay, F_add, N, x_pos, y_pos, mx_add, my_add):
        force = np.zeros(3) if F_add is None or np.asarray(F_add).size == 0 else np.asarray(F_add, dtype=float).ravel()
        az = -self.g
        print("Wheel loads (N):")
        print(f"FL = {N[0]:.1f}, FR = {N[1]:.1f}, RL = {N[2]:.1f}, RR = {N[3]:.1f}")
        fz = np.sum(N) + self.m * az + force[2]
        print(f"Balance check : Fz = {fz:.6f} N")
        mx = y_pos @ N + self.m * ay * self.h + mx_add
        my = x_pos @ N + self.m * ax * self.h + my_add
        print(f"Roll moment balance (Mx) = {mx:.6f} Nm")
        print(f"Pitch moment balance (My) = {my:.6f} Nm")

    def solve_cg(self, ax, ay, F_add=None, CF_rela=None, check=False):
        f_z_front_static = self.W * (self.L_rear / self.L)
        f_z_rear_static = self.W * (self.L_front / self.L)
        _, mx_add, my_add = self.external_effects(F_add, CF_rela)

        df_z_long = self.m * self.h * ax / self.L + my_add / self.L
        df_z_lat_f = (self.m * ay * self.h * (self.L_rear / self.L)) / self.t_front + (mx_add * self.L_rear / self.L) / self.t_front
        df_z_lat_r = (self.m * ay * self.h * (self.L_front / self.L)) / self.t_rear + (mx_add * self.L_front / self.L) / self.t_rear

        N = np.array(
            [
                0.5 * f_z_front_static - 0.5 * df_z_long + df_z_lat_f,
                0.5 * f_z_front_static - 0.5 * df_z_long - df_z_lat_f,
                0.5 * f_z_rear_static + 0.5 * df_z_long + df_z_lat_r,
                0.5 * f_z_rear_static + 0.5 * df_z_long - df_z_lat_r,
            ]
        )
        if check:
            print("\n=== CG Solver Results ===")
            x_pos, y_pos, _ = self.get_geometry()
            self.debug_balance(ax, ay, F_add, N, x_pos, y_pos, mx_add, my_add)
        return N

    def solve_lsm(self, ax, ay, F_add=None, CF_rela=None, check=False):
        A, b, mx_add, my_add = self.get_Ab(ax, ay, F_add, CF_rela)
        N = A.T @ np.linalg.solve(A @ A.T, -b)
        if check:
            print("\n=== LSM Solver Results ===")
            x_pos, y_pos, _ = self.get_geometry()
            self.debug_balance(ax, ay, F_add, N, x_pos, y_pos, mx_add, my_add)
        return N

    def solve_lagrange(self, ax, ay, F_add=None, CF_rela=None, check=False):
        x_pos, y_pos, _ = self.get_geometry()
        A, b, mx_add, my_add = self.get_Ab(ax, ay, F_add, CF_rela)
        N = self.K @ A.T @ np.linalg.solve(A @ self.K @ A.T, -b)
        if check:
            print("\n=== Weighted Lagrange ===")
            self.debug_balance(ax, ay, F_add, N, x_pos, y_pos, mx_add, my_add)
        return N

    def solve_suspension(self, ax, ay, F_add=None, CF_rela=None, check=False):
        x_pos, y_pos, _ = self.get_geometry()
        B = np.vstack([np.ones(4), y_pos, -x_pos])
        b = self.m * np.array([-self.g, ay * self.h, ax * self.h])
        fz_add, mx_add, my_add = self.external_effects(F_add, CF_rela)
        b = b + np.array([fz_add, mx_add, my_add])
        A = np.vstack([np.ones(4), y_pos, x_pos])
        q = np.linalg.solve(A @ self.K @ B.T, -b)
        N = self.K @ B.T @ q
        if check:
            print("\n=== Suspension Model ===")
            self.debug_balance(ax, ay, F_add, N, x_pos, y_pos, mx_add, my_add)
        return N

    def solve_decoupled(self, ax, ay, F_add=None, CF_rela=None, check=False):
        x_pos, y_pos, _ = self.get_geometry()
        B = np.vstack([np.ones(4), y_pos, -x_pos])
        b = self.m * np.array([-self.g, ay * self.h, ax * self.h])
        fz_add, mx_add, my_add = self.external_effects(F_add, CF_rela)
        b = b + np.array([fz_add, mx_add, my_add])
        A = np.vstack([np.ones(4), y_pos, x_pos])
        q = np.linalg.solve(A @ B.T @ self.K_modal, -b)
        N = B.T @ (self.K_modal @ q)
        if check:
            print("\n=== Decoupled Suspension Model ===")
            self.debug_balance(ax, ay, F_add, N, x_pos, y_pos, mx_add, my_add)
        return N
