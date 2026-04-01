from Filter import filter # 過濾初始資料(沒有要使用函式)
import numpy as np
import matplotlib.pyplot as plt
from Fitter import Linear_Regression as LR # 線性回歸計算剛度
from pathlib import Path
import pandas as pd

# 取得目前這個 .py 檔案所在資料夾
current_dir = Path(__file__).resolve().parent
# 建立相對路徑 (往上一層 -> data -> 檔名)
data_path = "B2356run4_processedK.csv"

K0 = 566.6854*0.175
print("官方資料:", K0, "N/mm")

def load_data(file_name):# 載入檔案
    # 建立相對路徑 (往上一層 -> data -> 檔名)
    file_path = current_dir / "data" / "Filtered_data" / file_name

    # 讀取 Excel
    df = pd.read_csv(file_path)

    # 只取 FZ 和 RL 欄位
    df_selected = df[["FZ", "RL"]].copy()

    # 去除缺失值
    df_selected = df_selected.dropna()

    # 轉成 numpy array
    FZ = df_selected["FZ"].to_numpy()
    RL = df_selected["RL"].to_numpy()

    print("資料讀取成功")
    print(f"共讀取 {len(FZ)} 筆資料")
    
    return FZ, RL

# 計算
FZ, RL = load_data(data_path)
R0 = 16*25.4/2#mm
#R0 = 200
k, b = LR.linear_regression(FZ, RL, R0, K0)
k_origin = LR.linear_regression_origin(FZ, RL, R0, K0)

# 存檔md報告
with open("result.md", "w", encoding="utf-8") as f:
    f.write(f"# Vertical Stiffness Fitting Results\n\n")
    f.write(f"TTC剛性: {K0:.4f} N/mm\n\n")
    f.write(f"## 線性回歸結果 \n\n")
    f.write(f"![RL Comparison](Figures/Vertical_stiffness.png)\n\n")
    f.write(f"R0 (Free Radius) = {R0:.6f}\n\n")
    f.write(f"Vertical stiffness k = {k:.4f} N/mm\n\n")
    f.write(f"預先負載 b = {b:.4f}\n\n")
    f.write(f"預載壓縮 dr0 = {b/k:.4f}\n\n")
    f.write(f"***\n\n")
    f.write(f"## 線性回歸結果 (through origin) \n\n")
    f.write(f"![RL Comparison](Figures/Vertical_stiffness_origin.png)\n\n")
    f.write(f"R0 (Free Radius) = {R0:.6f}\n\n")
    f.write(f"Vertical stiffness k = {k_origin:.4f} N/mm\n\n")
    