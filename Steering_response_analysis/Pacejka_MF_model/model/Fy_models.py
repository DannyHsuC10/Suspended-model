import numpy as np
from ._common import MF612, CalculationInput

zeta0 = 1
zeta1 = 1
zeta2 = 1
zeta3 = 1
zeta4 = 1
class MF612_Fy0(MF612):
    """純側滑橫向力 (SA ≠ 0, SL = 0)"""

    @staticmethod
    def calculate(MF: 'CalculationInput') -> np.ndarray:
        Fzo_prime, dfz = MF612._normalize_load(MF)
        dpi, dpi2 = MF612._normalize_pressure(MF)
        ami,iaMi, iaMi2 = MF612._normalize_angles(MF.SA, MF.IA)
        
        # μy (4.E23)
        muy = (
            (MF.PDY1 + MF.PDY2 * dfz)
            * (1 + MF.PPY3 * dpi + MF.PPY4 * dpi2)
            * (1 - MF.PDY3 * iaMi2)
            * MF.LMUY
        )

        # Kyα (4.E25)
        term = (MF.FZ / Fzo_prime) / (
            (MF.PKY2 + MF.PKY5 * iaMi2) * (1 + MF.PPY2 * dpi)
        )

        Kya = (
            MF.PKY1 * Fzo_prime
            * (1 + MF.PPY1 * dpi)
            * (1 - MF.PKY3 * abs(iaMi))
            * np.sin(MF.PKY4 * np.arctan(term))
            * MF.LYKA * zeta3
        )

        # Svγα (4.E28)
        Svyia = (
            MF.FZ * (MF.PVY3 + MF.PVY4 * dfz)
            * iaMi
            * MF.LYKA * MF.LVY * zeta2
        )

        # Kyγ0 (4.E30)
        Kyiao = (
            MF.FZ * (MF.PKY6 + MF.PKY7 * dfz)
            * (1 + MF.PPY5 * dpi)
            * MF.LYKA
        )

        # Shy (4.E27)
        Shy = (
            (MF.PHY1 + MF.PHY2 * dfz) * MF.LHY
            + (Kyiao * iaMi - Svyia) * zeta0 / (Kya + MF.EPSILON_K) + zeta4 - 1
        )

        # ay (4.E20)
        ay = ami + Shy

        # Cy (4.E21)
        Cy = MF.PCY1 * MF.LCY # >0

        # Dy (4.E22)
        Dy = muy * MF.FZ * zeta2

        # Ey (4.E24)
        Ey = (
            (MF.PEY1 + MF.PEY2 * dfz)
            * (1 + MF.PEY5 * iaMi2
               - (MF.PEY3 + MF.PEY4 * iaMi) * np.sign(ay))
            * MF.LEY
        )

        # By (4.E26)
        By = Kya / (Cy * Dy + MF.EPSILON_Y)

        # Svy (4.E29)
        Svy = (
            MF.FZ * (MF.PVY1 + MF.PVY2 * dfz)
            * MF.LVY * MF.LVY * zeta2
            + Svyia
        )

        # Fy0 (4.E19)
        Fy0 = Dy * np.sin(
            Cy * np.arctan(By * ay - Ey * (By * ay - np.arctan(By * ay)))
        ) + Svy

        return Fy0


class MF612_Fy(MF612):
    """混合工況橫向力 (SA ≠ 0, SL ≠ 0)"""

    @staticmethod
    def calculate(MF: 'CalculationInput') -> np.ndarray:
        Fy0 = MF612_Fy0.calculate(MF)

        Fzo_prime, dfz = MF612._normalize_load(MF)
        dpi, _ = MF612._normalize_pressure(MF)
        ami,iaMi, iaMi2 = MF612._normalize_angles(MF.SA, MF.IA)

        # SHκ (4.E64)
        SHyk = MF.RHY1 + MF.RHY2 * dfz
        kappaS = MF.SL + SHyk

        # Byκ (4.E63)
        Byk = (
            (MF.RBY1 + MF.RBY4 * iaMi2)
            * np.cos(np.arctan(MF.RBY2 * (ami - MF.RBY3)))
            * MF.LYKA
        )

        # Cyκ (4.E65)
        Cyk = MF.RCY1

        # Eyκ (4.E65)
        Eyk = MF.REY1 + MF.REY2 * dfz

        def Gyk_term(x):
            return np.cos(
                Cyk * np.arctan(Byk * x - Eyk * (Byk * x - np.arctan(Byk * x)))
            )


        Gyk0 = Gyk_term(SHyk)
        """
        Gyk0 = Gyk_term(SHyk)+ MF.EPSILON_Y# 強制壓低 MF.EPSILON_Y
        強制壓低 MF.EPSILON_Y ，這不是formula set 裡面的東西但防止fitting過程中出錯導致跳停，用更低的係數讓計算誤差進入可以接受的範圍
        """

        
        Gyk = Gyk_term(kappaS) / Gyk0

        # μy for DVκ
        muy = (
            (MF.PDY1 + MF.PDY2 * dfz)
            * (1 + MF.PPY3 * dpi + MF.PPY4 * dpi**2)
            * (1 - MF.PDY3 * iaMi2)
            * MF.LMUY
        )

        # DVκ (4.E66)
        DVyk = (
            muy * MF.FZ
            * (MF.RVY1 + MF.RVY2 * dfz + MF.RVY3 * iaMi)
            * np.cos(np.atan(MF.RVY4 * ami))*zeta2
        )

        # SVκ (4.E67)
        SVyk = (
            DVyk
            * np.sin(MF.RVY5 * np.arctan(MF.RVY6 * MF.SL))
            * MF.LVYKA
        )

        Fy = Fy0 * Gyk + SVyk
        return Fy
