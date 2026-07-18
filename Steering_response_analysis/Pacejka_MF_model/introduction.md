# Pacejka_MF_model
## 簡介
Pacejka_MF_model是個輪胎模型，如果無法理解他怎麼運作就把它當作一個輸出可以產出輪胎力矩與力量的黑盒子工具。使用方法如下:
* [檔案位置](Demo.py)
```python
from model import api # 套用api接口

tir_params = api.load_tir("D2704_mf612.tir") # 載入tir參數檔案

MF = api.CalculationInput( # 建立MF物件函數
            FZ=800,
            SA=1,
            SL=0.25,
            IA=0.0,
            V = 10,
            pressure=80000,
            tir_params=tir_params
        )
# MF_Universal_solver可以解出 FX FY MX RRT MZ等多個輸出，第一個參數為輸出類型，第二個參數為MF物件
Fx = api.MF_Universal_solver("FX", MF) # 呼叫MF_Universal_solver函數，計算FX，第一個參數為"FX"，第二個參數為MF物件
Fy = api.MF_Universal_solver("FY", MF) # 呼叫MF_Universal_solver函數，計算FY，第一個參數為"FY"，第二個參數為MF物件

print("Fx:", Fx) # 印出
print("Fy:", Fy)

```
## 其他小工具
本模組是輪胎擬合模組magic formula fitting中的精簡工具，這個資料夾中只擷取部分內容

1. [圖形測試器](/Pacejka_MF_model/introduction/MF_tester.md) : 用於簡單分析輪胎性能。
2. [測試結果圖表](/Pacejka_MF_model/Figures/MF_plt.md) : 上個工具的輸出結果，執行之後就會自動更新。
3. [輪胎模型](/Pacejka_MF_model/introduction/magic_formula_model.md) : 輪胎模型說明，如果想了解模組運作可以看這個。