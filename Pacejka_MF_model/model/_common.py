"""
MF 輪胎模型 - 共享基礎模塊
Magic Formula Tire Model - Common Base Module

提供共享的基礎功能：
- 導入語句和常數定義
- 配置參數載入
- CalculationInput 數據結構
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Union, Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

@dataclass
class CalculationInput:
    """計算輸入結構"""
    
    # 必要輸入
    FZ: Union[float, np.ndarray]
    SA: Union[float, np.ndarray]

    # 可選輸入
    SL: Union[float, np.ndarray] = None
    IA: Union[float, np.ndarray] = None
    pressure: Union[float, np.ndarray] = None
    V: Union[float, np.ndarray] = None
    Ro: Union[float, np.ndarray] = None
    Fx: Union[float, np.ndarray] = None
    Fy: Union[float, np.ndarray] = None

    # 數值穩定性常數
    EPSILON_K = 1e-6         # 避免分母為零
    EPSILON_Y = 1e-6
    EPSILON_X = 1e-6
    epsilonK = 1e-6
    EPSILON = 1e-6          # 數值下限

    # Tire model parameters dict
    tir_params: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        self.FZ = np.atleast_1d(self.FZ)
        self.SA = np.atleast_1d(self.SA)
        self.IA = np.atleast_1d(self.IA) if self.IA is not None else np.zeros_like(self.FZ)
        self.SL = np.atleast_1d(self.SL) if self.SL is not None else None


        # 遍歷 tir_params，把存在的 key 映射成屬性
        for key, value in self.tir_params.items():
            setattr(self, key, value)

        # 特殊情況：改名
        if "NOMPRES" in self.tir_params:
            self.PIO = self.tir_params["NOMPRES"]
        
        self.pressure = np.atleast_1d(self.pressure) if self.pressure is not None else np.full_like(self.FZ, self.PIO, dtype=float)
        self.V = np.atleast_1d(self.V) if self.V is not None else np.full_like(self.FZ, self.tir_params["LONGVL"], dtype=float)
        self.Ro = np.atleast_1d(self.Ro) if self.Ro is not None else np.full_like(self.FZ, self.tir_params["UNLOADED_RADIUS"], dtype=float)
class MF612:
    """Magic Formula 6.1.2 計算引擎基類"""

    @staticmethod
    def _normalize_load(MF: 'CalculationInput') -> tuple:
        """歸一化法向力"""
        Fzo_prime = MF.LFZO * MF.FNOMIN  # 改成 FNOMIN
        dfz = (MF.FZ - Fzo_prime) / (Fzo_prime + MF.EPSILON)
        return Fzo_prime, dfz

    @staticmethod
    def _normalize_pressure(MF: 'CalculationInput') -> tuple:
        """歸一化胎壓"""
        dpi = (MF.pressure - MF.PIO) / MF.PIO
        dpi2 = dpi ** 2
        return dpi, dpi2

    @staticmethod
    def _normalize_angles(SA: np.ndarray, IA: np.ndarray) -> tuple:
        """歸一化滑移角與傾角"""
        SA_rad = np.radians(SA)  # 輸入度數，轉為 
        IA_rad = np.radians(IA)
        ami = np.tan(SA_rad)
        iaMi = np.sin(IA_rad)
        iaMi2 = iaMi ** 2
        return ami, iaMi, iaMi2

