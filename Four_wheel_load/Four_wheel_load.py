import numpy as np


class Car:
    def __init__(self,
                 m, h, L, d,
                 ax=0, ay=0,
                 CG_x=(0.5, 0.5),
                 CG_y=(0.5, 0.5),
                 F_add=(0, 0, 0),
                 CF_rela=(0, 0, 0),
                 K=None):

        self.m = m
        self.h = h
        self.L = L
        self.d = d

        self.ax = ax
        self.ay = ay

        self.CG_x = np.array(CG_x)
        self.CG_y = np.array(CG_y)

        self.F_add = np.array(F_add)
        self.CF_rela = np.array(CF_rela)

        self.K = np.eye(4) if K is None else np.array(K)


class FourWheelLoadModel:

    def __init__(self, car: Car):
        self.g = 9.81

        # 核心：展開 car → self
        self.__dict__.update(vars(car))

    # =========================
    # 幾何
    # =========================
    def _get_geometry(self):

        x_pos = self.L * np.array([
            self.CG_x[1], self.CG_x[1],
            -self.CG_x[0], -self.CG_x[0]
        ])

        y_pos = self.d * np.array([
            -self.CG_y[1], self.CG_y[0],
            -self.CG_y[1], self.CG_y[0]
        ])

        z_pos = np.ones(4)

        return x_pos, y_pos, z_pos

    # =========================
    # 建立 A, b
    # =========================
    def _get_Ab(self):

        az = -self.g

        x_pos, y_pos, z_pos = self._get_geometry()

        A = np.vstack([z_pos, y_pos, x_pos])

        b = self.m * np.array([
            az,
            self.ay * self.h,
            self.ax * self.h
        ])

        Mx_add = 0
        My_add = 0

        if self.F_add is not None:
            r = self.CF_rela
            F = self.F_add

            Mx_add = r[1]*F[2] - r[2]*F[1]
            My_add = r[2]*F[0] - r[0]*F[2]

            b += np.array([F[2], Mx_add, My_add])

        return A, b, x_pos, y_pos, Mx_add, My_add

    # =========================
    # Debug
    # =========================
    def _debug(self, N, x_pos, y_pos, Mx_add, My_add):

        az = -self.g

        print("輪胎載重 (N):")
        print(f"FL = {N[0]:.1f}, FR = {N[1]:.1f}, RL = {N[2]:.1f}, RR = {N[3]:.1f}")

        Fz = np.sum(N) + self.m * az + self.F_add[2]
        print(f"平衡確認 : Fz = {Fz:.6f} N")

        Mx = y_pos @ N + self.m * self.ay * self.h + Mx_add
        My = x_pos @ N + self.m * self.ax * self.h + My_add

        print(f"Roll moment balance (Mx) = {Mx:.6f} Nm")
        print(f"Pitch moment balance (My) = {My:.6f} Nm")

    # =========================
    # CG 法
    # =========================
    def solve_cg(self, check=False):

        W = self.m * self.g

        dF = self.m * self.h * np.array([self.ax, self.ay]) / np.array([self.L, self.d])

        if self.F_add is not None:
            r = self.CF_rela
            F = self.F_add

            Mx_add = r[1]*F[2] - r[2]*F[1]
            My_add = r[2]*F[0] - r[0]*F[2]

            dF += np.array([My_add / self.L, Mx_add / self.d])

        CG_x = self.CG_x.reshape(2, 1)
        CG_y = self.CG_y.reshape(1, 2)

        Fs = W * (CG_x @ CG_y)

        F = (
            Fs
            + dF[0] * np.vstack([-CG_y, CG_y])
            + dF[1] * np.hstack([CG_x, -CG_x])
        )

        N = np.array([F[0,0], F[0,1], F[1,0], F[1,1]])

        if check:
            print("=== CG Method ===")
            print(N)

        return N

    # =========================
    # LSM
    # =========================
    def solve_lsm(self, check=False):

        A, b, x_pos, y_pos, Mx_add, My_add = self._get_Ab()

        N = A.T @ np.linalg.solve(A @ A.T, -b)

        if check:
            print("=== LSM ===")
            self._debug(N, x_pos, y_pos, Mx_add, My_add)

        return N

    # =========================
    # 加權 Lagrange
    # =========================
    def solve_lagrange(self, check=False):

        A, b, x_pos, y_pos, Mx_add, My_add = self._get_Ab()
        if self.K is None:
            self.K = np.eye(4)
        N = self.K @ A.T @ np.linalg.solve(A @ self.K @ A.T, -b)

        if check:
            print("=== Weighted Lagrange ===")
            self._debug(N, x_pos, y_pos, Mx_add, My_add)

        return N


if __name__ == "__main__":
    g = 9.81
    car = Car(# 定義物件
        m=309.5,
        h=0.284,
        L=1.55,
        d=1.25,
        ax=0.0 * g,
        ay=1 * g,
        CG_x=(0.48, 0.52),# front, rear
        CG_y=(0.5, 0.5),# left, right
        K=np.diag([30000, 30000, 25000, 25000])# k_fl, k_fr, k_rl, k_rr
    )

    fwl = FourWheelLoadModel(car)

    fwl.solve_cg(check=True)
    fwl.solve_lsm(check=True)
    fwl.solve_lagrange(check=True)