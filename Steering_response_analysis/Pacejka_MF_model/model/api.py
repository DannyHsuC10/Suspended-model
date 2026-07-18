"""
MF 6.1.2 輪胎模型 - 統一接口
Magic Formula 6.1.2 Tire Model - Unified API

提供統一的接口函數和便利函數：
- create_calculation_input_from_config() - 從配置建立計算輸入
- calculate_* 便利函數 - 簡化的計算函數
- 測試和日誌
"""

import numpy as np
from typing import Union, Dict
import logging

from pathlib import Path
base_dir = Path(__file__).resolve().parent .parent  # up to Pacejka_MF_model/
from ._common import (
    CalculationInput
)

from .Mx_models import MF612_Mx
from .Mz_models import MF612_Mz
from .RRT_models import MF612_RRT_SAE, MF612_RRT_MF
from .Fy_models import MF612_Fy
from .Fx_models import MF612_Fx



logger = logging.getLogger(__name__)

def create_calculation_input_from_config(
    *,
    FZ: Union[float, np.ndarray],
    SA: Union[float, np.ndarray],
    SL: Union[float, np.ndarray],
    IA: Union[float, np.ndarray],
    pressure: Union[float, np.ndarray],
    tir_params: Dict[str, float],
    V: Union[float, np.ndarray] = None,
    Ro: Union[float, np.ndarray] = None,
    Fx: Union[float, np.ndarray] = None,
    Fy: Union[float, np.ndarray] = None,
) -> CalculationInput:
    """
    建立 CalculationInput（工況為主，TIR 參數完整注入）
    """

    calc_input = CalculationInput(
        FZ=FZ,
        SA=SA,
        SL=SL,
        IA=IA,
        pressure=pressure,
        V=V,
        Ro=Ro,
        Fx=Fx,
        Fy=Fy,
        tir_params=tir_params,
    )

    return calc_input

# ============================================================================
# 混合工況便利函數
# ============================================================================

def calculate_fx(calc_input: CalculationInput) -> np.ndarray:
    """便利函數: 計算混合縱向力
    
    Args:
        calc_input: CalculationInput 對象
        Rx: 混合滑移相互作用係數向量 (7個)
    Returns:
        Fx: 混合縱向力 [N]
    """
    return MF612_Fx.calculate(calc_input)


def calculate_fy(calc_input: CalculationInput) -> np.ndarray:
    """便利函數: 計算混合橫向力
    
    Args:
        calc_input: CalculationInput 對象
        Ry: 混合滑移相互作用係數向量 (15個)
    Returns:
        Fy: 混合橫向力 [N]
    """
    return MF612_Fy.calculate(calc_input)


def calculate_mz(calc_input: CalculationInput) -> np.ndarray:
    """便利函數: 計算混合回正力矩
    Args:
        calc_input: CalculationInput 對象
        Py: 側向力係數向量 (27個)
        Ry: 混合滑移相互作用係數向量 (15個)
        Sz: 混合滑移力矩移位係數向量 (4個)
    
    Returns:
        Mz: 混合回正力矩 [N·m]
    """
    return MF612_Mz.calculate(calc_input)


# ============================================================================
# 可選公式便利函數
# ============================================================================

def calculate_mx(calc_input: CalculationInput) -> np.ndarray:
    """便利函數: 計算顛覆力矩 (可選)
    Args:
        calc_input: CalculationInput 對象 (需要 Fy)
    Returns:
        Mx: 顛覆力矩 [N·m]
    """
    return MF612_Mx.calculate(calc_input)

def calculate_rrt(calc_input: CalculationInput) -> np.ndarray:
    """便利函數: 計算滾動阻力(可選)
    Args:
        calc_input: CalculationInput 對象 (需要 Fx)
    Returns:
        RRT: 滾動阻力矩 [N·m]
    """
    return MF612_RRT_SAE.calculate(calc_input)

# ============================================================================
# 模組初始化和通用求解器
# ============================================================================

def MF_Universal_solver(out,MF):# 通用求解器選擇
    if out =="FX":
        result = MF612_Fx.calculate(MF)
    if out =="FY":
        result = MF612_Fy.calculate(MF)
    if out =="MZ":
        result = MF612_Mz.calculate(MF)
    if out =="MX":
        result = MF612_Mx.calculate(MF)
    if out =="RRT":
        result = MF612_RRT_SAE.calculate(MF)
    
    # 純量與向量輸出兼容：
    '''
    - 若為 0 維或單一元素陣列，回傳純標量 (item)
    - 若為一般 1 維/多維陣列，直接回傳 ndarray
    '''
    if isinstance(result, np.ndarray):
        if result.ndim == 0 or result.size == 1:
            return result.item()
        return result
    return result

def _parse_value(raw: str):# 參數處理函數
    """將字串轉為 int / float / str"""
    raw = raw.strip()

    # 字串（有單引號）
    if raw.startswith("'") and raw.endswith("'"):
        return raw.strip("'")

    # 嘗試數值
    try:
        if "." in raw or "e" in raw.lower():
            return float(raw)
        else:
            return int(raw)
    except ValueError:
        return raw

def load_tir(filename: str) -> dict:# 讀取 TIR 參數
    """
    讀取 .tir 檔，回傳 flat dict：
    tir_params["PCX1"] = 1.9
    """
    filepath = base_dir /"tir"/ filename
    tir_params = {}

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()

            # 忽略空行
            if not line:
                continue

            # 忽略註解
            if line.startswith("$"):
                continue

            # 忽略 section header
            if line.startswith("[") and line.endswith("]"):
                continue

            # 移除行內註解
            if "$" in line:
                line = line.split("$", 1)[0].strip()

            # 必須包含 =
            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            tir_params[key] = _parse_value(value)

    return tir_params

def _print_module_info():
    logger.info("="*70)
    logger.info("MF612 公式模組已載入")
    logger.info("="*70)

    logger.info("\n📚 支援的公式類型:")
    logger.info("  • Fy0  - Pure side slip lateral force")
    logger.info("  • Fx0  - Pure longitudinal slip force")
    logger.info("  • Mz0  - Pure aligning torque")
    logger.info("  • Fx   - Combined slip longitudinal force")
    logger.info("  • Fy   - Combined slip lateral force")
    logger.info("  • Mz   - Combined slip aligning torque")

_print_module_info