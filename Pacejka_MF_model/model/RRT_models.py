# 滾動阻力矩模型
import numpy as np
from ._common import MF612, CalculationInput
from .Fx_models import MF612_Fx

class MF612_RRT_MF(MF612):
    """
    Rolling Resistance Torque (MF6.12)

    Reference:
        MF6.12 - Rolling resistance model
        Coefficients: QSY1 ~ QSY8
    """

    @staticmethod
    def calculate(MF: CalculationInput) -> np.ndarray:
        # --- 需要 Fx ---
        Fx = MF612_Fx.calculate(MF)

        # --- 接地半徑 ---
        Ro = np.asarray(MF.Ro, dtype=float)

        # --- 歸一化 ---
        Fzo_prime, dfz = MF612._normalize_load(MF)
        dpi, _ = MF612._normalize_pressure(MF)

        # --- 物理量 ---
        Fz = MF.FZ
        V = MF.V
        gamma = np.radians(MF.IA)  # camber (rad)

        # --- Rolling resistance coefficient ---
        f_rr = (
            MF.QSY1
            + MF.QSY2 * (Fx / (Fzo_prime + MF.EPSILON))
            + MF.QSY3 * V
            + MF.QSY4 * V**4
            + MF.QSY5 * gamma**2
            + MF.QSY6 * gamma**2 * (Fz / (Fzo_prime + MF.EPSILON))
        )

        # load / pressure correction
        f_rr *= (1.0 + MF.QSY7 * dfz + MF.QSY8 * dpi)

        # --- Rolling resistance torque ---
        PPT = -Ro * Fz * f_rr

        return PPT

class MF612_RRT_SAE(MF612):
    """
    Rolling Resistance Torque with manual mode switch

    mode:
          "SAE" -> use SAE empirical formula
    """

    @staticmethod
    def calculate(MF: CalculationInput) -> np.ndarray:
        """
        計算滾動阻力矩
        Args:
                  "SAE" -> 使用 SAE 經驗公式
        """
        Ro = np.asarray(MF.Ro, dtype=float)
        Fz = MF.FZ
        p = MF.pressure
        v  = np.asarray(MF.V, dtype=float)

        # --- SAE 經驗公式 ---
        # SAE 建議參數
        K_prime = 0.7    # FSAE
        c1 = 1000
        c2 = 5.1
        c3 = 5.5e5
        c4 = 90
        c5 = 1100
        c6 = 0.0388

        # 計算各項
        R1 = K_prime / c1
        R2 = c2
        R3 = (c3 + c4 * Fz) / p
        R4 = (c5 + c6 * Fz) * (v**2) / p

        Crr = R1 * (R2 + R3 + R4)
        Fr = -Ro * Crr * Fz  # 滾動阻力
        return Fr
    