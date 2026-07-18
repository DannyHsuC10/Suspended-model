"""
MF 輪胎模型公式實現包

提供純工況和混合工況的所有計算函數：
- Fy0: Pure side slip lateral force (純側滑橫向力)
- Fx0: Pure longitudinal slip longitudinal force (純縱滑縱向力)  
- Mz0: Pure side slip aligning torque (純側滑回正力矩)
- Fx: Combined slip longitudinal force (混合縱向力)
- Fy: Combined slip lateral force (混合橫向力)
- Mz: Combined slip aligning torque (混合回正力矩)
- Mx: Overturning moment (顛覆力矩 - 可選)
- RRT SAE: SAE 經驗阻力
- RRT MF: magic formula 解出阻力
"""

# ============================================================================
# 導入共享基礎
# ============================================================================
from ._common import (
    CalculationInput,
    MF612
)

from .Fx_models import (
    MF612_Fx0,
    MF612_Fx,
)

from .Fy_models import (
    MF612_Fy0,
    MF612_Fy,
)

from .Mz_models import (
    MF612_Mz
)
# ============================================================================
# 導入可選公式
# ============================================================================
from .Mx_models import (
    MF612_Mx,
)

from .RRT_models import (
    MF612_RRT_MF,
    MF612_RRT_SAE
)

# ============================================================================
# 公開接口定義
# ============================================================================

__all__ = [
    # 數據結構
    'CalculationInput',
    
    # 基類
    'MF612',
    
    # 純工況類
    'MF612_Fy0',
    'MF612_Fx0',
    'MF612_Mz0',
    'MF612_Fx',
    'MF612_Fy',
    'MF612_Mz',
    'MF612_Mx',
    'MF612_RRT_MF',
    'MF612_RRT_SAE',
    
    # 便利函數
    'create_calculation_input_from_config',
    'calculate_fx',
    'calculate_fy',
    'calculate_mz',
    'calculate_mx',
    'calculate_rrt'
]

__version__ = '6.1.2'
__author__ = 'Danny'
__doc__ = """
MF612 - Magic Formula 6.1.2 輪胎模型公式實現

模塊結構：
- _common.py      : 共享基礎（導入、常數、CalculationInput、MF612 基類）
- api.py          : 統一接口（便利函數）
- __init__.py     : 統一導入和導出

快速開始示例：

1. 創建計算輸入
   >>> from mf_formulas import create_calculation_input_from_config
   >>> calc_input = create_calculation_input_from_config(FZ=2000, SA=5, IA=0)

2. 準備 Magic Formula 參數（字典）
   >>> params = {
   ...     'PCY1': 1.3,
   ...     'PDY1': 1.0,
   ...     'PDY2': 0.1,
   ...     ...
   ...     'RBY1': 8.0,
   ...     ...
   ... }

3. 計算純側滑橫向力
   >>> from mf_formulas import calculate_fy0
   >>> Fy0 = calculate_fy0(calc_input, params)

4. 計算混合工況橫向力
   >>> from mf_formulas import calculate_fy
   >>> Fy = calculate_fy(calc_input, params)

"""
