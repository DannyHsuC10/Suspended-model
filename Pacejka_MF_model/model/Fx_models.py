import numpy as np
from ._common import MF612, CalculationInput

zeta1 = 1
zeta2 = 1

class MF612_Fx0(MF612):
    """純縱滑縱向力 Fx0"""
    @staticmethod
    def calculate(MF: 'CalculationInput') -> np.ndarray:
        # 歸一化法向力
        Fzo_prime, dfz = MF612._normalize_load(MF)

        # 歸一化胎壓
        dpi, dpi2 = MF612._normalize_pressure(MF)

        # 傾角
        _, iaMi, iaMi2 = MF612._normalize_angles(MF.SA, MF.IA)

        # SL 必須提供
        if MF.SL is None:
            raise ValueError("SL (Slip Ratio) 必須提供")

        # 水平偏移 Shx
        Shx = (MF.PHX1 + MF.PHX2 * dfz) * MF.LHX
        kappax = MF.SL + Shx  # 修正滑移

        # 垂直偏移 Svx
        Svx = MF.FZ * (MF.PVX1 + MF.PVX2 * dfz) * MF.LVX * MF.LXAL * zeta1

        # 剛性 Kxk
        Kxk = (MF.FZ * (MF.PKX1 + MF.PKX2 * dfz) *
               np.exp(MF.PKX3 * dfz) *
               (1 + MF.PPX1 * dpi + MF.PPX2 * dpi2) *MF.LKX)

        # 曲率 Ex
        Ex = (MF.PEX1 + MF.PEX2 * dfz + MF.PEX3 * dfz**2) * (1 - MF.PEX4 * np.sign(kappax)) * MF.LEX

        # 摩擦係數 μx
        mux = (MF.PDX1 + MF.PDX2 * dfz) * (1 + MF.PPX3 * dpi + MF.PPX4 * dpi2) * (1 - MF.PDX3 * np.radians(MF.IA)**2) * MF.LMUX * MF.LXAL

        # 峰值力 Dx
        Dx = mux * MF.FZ * zeta2

        # 形狀因子 Cx
        Cx = MF.PCX1 * MF.LCX

        # 剛性因子 Bx
        Bx = Kxk / (Cx * Dx + MF.EPSILON_X)

        # 直接套用 4.E9 Magic Formula
        arg = Bx * kappax
        Fx0 = Dx * np.sin(Cx * np.arctan(arg - Ex * (arg - np.arctan(arg)))) + Svx

        return Fx0


class MF612_Fx(MF612):
    """混合工況縱向力 Fx (Combined Slip)"""

    @staticmethod
    def calculate(MF: 'CalculationInput') -> np.ndarray:
        ami, iaMi, iaMi2 = MF612._normalize_angles(MF.SA, MF.IA)
        Fzo_prime, dfz = MF612._normalize_load(MF)
        Fx0 = MF612_Fx0.calculate(MF)

        # 側偏角偏移
        SHa = MF.RHX1
        alpha_S = ami + SHa
        # B C E
        RB = (MF.RBX1 + MF.RBX3 * iaMi2) * np.cos(np.arctan(MF.RBX2 * MF.SL)) * MF.LVX
        Cxa = MF.RCX1
        Exa = MF.REX1 + MF.REX2 * dfz

        def Gx_term(x):
            arg = RB * x - Exa * (RB * x - np.arctan(RB * x))
            return np.cos(Cxa * np.arctan(arg))

        Gx0 = Gx_term(SHa)

        Gxa = Gx_term(alpha_S) / (Gx0 + MF.EPSILON_X)
        """
        強制壓低 MF.EPSILON_X ，這不是formula set 裡面的東西但防止fitting過程中出錯導致跳停，用更低的係數讓計算誤差進入可以接受的範圍
        """

        Fx = Fx0 * Gxa
        
        return Fx
