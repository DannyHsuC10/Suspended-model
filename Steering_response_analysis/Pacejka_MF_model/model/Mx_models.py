import numpy as np
from ._common import MF612, CalculationInput
from .Fy_models import MF612_Fy

class MF612_Mx(MF612):
    """
    Overturning Moment Mx (MF6.12)

    Reference:
        MF6.12 Eq. (4.E69)
    """

    @staticmethod
    def calculate(MF: CalculationInput) -> np.ndarray:
        # --- 必要力 ---
        Fy = MF612_Fy.calculate(MF)

        # --- 接地半徑 ---
        Ro = MF.Ro

        # --- 歸一化 ---
        Fzo_prime, dfz = MF612._normalize_load(MF)
        dpi, _ = MF612._normalize_pressure(MF)

        # IA 必須使用「實際角度（rad）」
        ia = np.radians(MF.IA)

        # 力比
        Fy_ratio = Fy / (Fzo_prime + MF.EPSILON)
        Fz_ratio = MF.FZ / (Fzo_prime + MF.EPSILON)

        # --- Eq. 4.E69 ---
        Mx = (
            Ro * MF.FZ *
            (
                MF.QSX1
                - MF.QSX2 * ia * (1.0 + MF.PPMX1 * dpi)
                + MF.QSX3 * Fy_ratio
                + MF.QSX4
                  * np.cos(MF.QSX5 * np.arctan(MF.QSX6 * Fz_ratio) ** 2)
                  * np.sin(
                      MF.QSX7 * ia
                      + MF.QSX8 * np.arctan(MF.QSX9 * Fy_ratio)
                  )
                + MF.QSX10 * np.arctan(MF.QSX11 * Fz_ratio) * ia
            )
            * MF.LMX
        )

        return Mx
