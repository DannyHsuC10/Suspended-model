# Suspension MATLAB 專案說明

本資料夾是一組用 MATLAB 撰寫的懸吊與車輛動態分析小專案，主要涵蓋彈簧剛性、阻尼、自然頻率、路面頻譜與四輪垂直荷重轉移等主題。每個 MATLAB 檔案已拆成獨立子資料夾，並各自包含主程式、參數 CSV、`load_data.m` 與 md 說明。

## 資料夾總覽

```text
Suspension matlab/
├─ Damping/
├─ Brake_force/
├─ four_wheel_load/
├─ Natural_frequency/
└─ spring/
```

## Damping

此資料夾用於分析懸吊阻尼與 quarter-car 模型的暫態響應。目前已拆成三個獨立小專案，每個子資料夾都有自己的 `.m`、`data.csv`、`load_data.m` 與 md 說明。

| 子資料夾 | 說明 |
| --- | --- |
| `Critical_Damping_Analysis/` | 掃描彈簧剛性範圍，計算對應自然頻率與臨界阻尼。 |
| `Damped_oscillation_analysis/` | 以 quarter-car 模型比較不同阻尼比下的簧上位移與動態輪胎荷重變化。 |
| `quarter_suspension/` | 含阻尼的 quarter-car step road input 分析，輸出簧上/簧下位移、速度、加速度與能量消散。 |

## four_wheel_load

此資料夾用於車輛縱向/橫向加速度下的四輪垂直荷重分配計算。目前已拆成三個獨立小專案。

| 子資料夾 | 說明 |
| --- | --- |
| `VehicleDynamicsSimulator/` | 核心 class，封裝車輛幾何、外力矩、平衡方程與多種四輪荷重求解器。 |
| `FWL/` | 使用 `VehicleDynamicsSimulator` 掃描 `ax`、`ay` 範圍，繪製 FL/FR/RL/RR 四輪荷重 3D 疊圖。 |
| `acc_load/` | 計算不同縱向加速度下前後軸 normal load 轉移，並繪製前/後荷重曲線。 |

`VehicleDynamicsSimulator.m` 內建的主要求解方法包含：

- `solve_cg`：以重心與幾何關係估算荷重轉移。
- `solve_lsm`：以最小平方形式解四輪荷重分配。
- `solve_lagrange`：使用剛性矩陣加權的 Lagrange 求解方式。
- `solve_suspension`：以懸吊剛性與車身姿態關係求解。
- `solve_decoupled`：以解耦模態剛性求解。

## Natural_frequency

此資料夾用於自然頻率、車體/輪胎剛性、路面 PSD 與激振頻率分析。目前已拆成五個獨立小專案。

| 子資料夾 | 說明 |
| --- | --- |
| `aero_spring/` | 由最大加速度、重心高度、軸距與允許 pitch 角度估算所需 pitch stiffness。 |
| `Maximum_compression/` | 掃描允許懸吊壓縮量，估算 pitch 與 roll 剛性需求。 |
| `Overall_rigidity/` | 將輪胎、懸吊、車體剛性視為串聯剛性，分析整體等效剛性與車體剛性倍率的關係。 |
| `PSD/` | 產生 ISO 8608 路面 profile，讀取 `PSD/vt_data.xlsx`，建立激振頻率能量分布與 FFT 分析。 |
| `Tire_Ring_Structural_Mode/` | 以簡化 ring bending 模型估算輪胎 ring structural mode 頻率。 |

注意：`PSD` 的速度資料已放在 `PSD/vt_data.xlsx`，腳本會用自身所在路徑讀取，不需手動切換 MATLAB Current Folder。

## spring

此資料夾用於彈簧剛性、ride rate、wheel hop 與數值積分誤差分析。目前已拆成六個獨立小專案。

| 子資料夾 | 說明 |
| --- | --- |
| `Spring_stiffness/` | 掃描彈簧剛性，計算 quarter-car 自然頻率。 |
| `ride_rate/` | 由彈簧剛性、motion ratio 與輪胎剛性計算 ride rate。 |
| `Suspension_Oscillation/` | 比較單自由度無阻尼振動的解析解與 Explicit Euler 數值解，並繪製誤差。 |
| `Time_sensitivity_analysis/` | 比較不同時間步長 `dt` 對 Explicit Euler 位移與能量誤差的影響。 |
| `Tire_suspension_spring/` | 以無阻尼 quarter-car ODE 模型分析簧上/簧下質量耦合振動與能量守恆。 |
| `Unsprung_mass/` | 掃描簧下質量，計算 wheel hop frequency。 |

## 建議執行方式

1. 開啟 MATLAB。
2. 進入欲執行的小專案子資料夾。
3. 直接執行該子資料夾內的 `.m` 檔。
4. 每個小專案的參數都在自己的 `data.csv` 中。

## 主要分析主題

- 彈簧剛性與自然頻率關係。
- 臨界阻尼與阻尼比對懸吊響應的影響。
- 簧上/簧下 quarter-car ODE 模擬。
- 輪胎剛性、懸吊剛性、車體剛性的等效剛性分析。
- 不同縱向/橫向加速度下的四輪垂直荷重變化。
- ISO 8608 路面 profile 與速度資料結合後的激振頻率分析。

## 注意事項

- 多數腳本開頭都有 `clear; clc; close all;`，會清空 workspace 並關閉圖窗。
- 部分腳本內的參數是目前假設值，例如車重、軸距、輪距、重心高度、彈簧剛性與輪胎剛性；正式分析前建議依實車資料更新。
- 多數腳本會直接產生圖表，若需要批次執行或保存圖片，可另外加入 `saveas` 或 `exportgraphics`。
- 若看到中文註解顯示異常，通常是 MATLAB/編輯器的文字編碼設定不同造成；可嘗試以 UTF-8 開啟或重新儲存檔案。
