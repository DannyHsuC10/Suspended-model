# Magic Formula (MF) 測試器與曲面視覺化工具

本模組目標：

* 提供 **Magic Formula 輪胎模型曲面繪圖**
* 比較不同 TIR 參數對力輸出的影響
* 支援 **Fx / Fy / Mx / Mz / RRT** 等輸出
* 可生成 **α–Fz、κ–Fz、Fx–Fy–κ、Fx–Fy–Fz** 等曲面或曲線

# 📂 模組結構

```
MF_tester.py
├─ tir 檔載入函式
├─ MF 計算物件產生器
├─ 曲面生成函式 (plot_tire_surface / plot_tire_surfaces)
├─ 摩擦圓與 κ, Fz 對比曲面 / 曲線
├─ __main__ 範例執行
```

---

# 🔧 功能與主要函式

---

## 1️⃣ TIR 參數載入

```python
load_tir(filename: str) -> dict
```

功能：

* 讀取 `.tir` 檔案
* 將每個參數轉換為 float / int / str
* 返回 **平坦字典** `{param_name: value}`，便於直接輸入 MF 模型

```python
tir_params["PCX1"] = 1.9
tir_params["UNLOADED_RADIUS"] = 0.259
```

---

## 2️⃣ MF 計算物件產生器

```python
MF_set(i, j, X, Y, fix, tir_params, pressure=82319, IA=0.0)
```

功能：

* 根據不同掃描維度 (`alpha`, `kappa`, `Fz`)
* 建立 `CalculationInput` 物件
* 將 **固定量與變動量** 對應到不同軸，方便生成曲面

範例：

* fix = `"alpha"` → α 固定，滑移率 & Fz 變動
* fix = `"kappa"` → κ 固定，α & Fz 變動
* fix = `"Fz"` → Fz 固定，α & κ 變動

---

## 3️⃣ 曲面範圍設定

```python
fig_set(fix, out)
```

功能：

* 根據掃描維度 `fix` 設定 x, y, z 軸範圍
* 返回 `(xlabel, ylabel, zlabel, x_range, y_range)`
* 用於所有曲面繪製函式

---

## 4️⃣ 曲面繪製函式

### 單一模型

```python
plot_tire_surface(out, fix, tir_params=None)
```

* 輸出：三維曲面圖
* 適用於單個 TIR 模型
* 利用 **MF_Universal_solver** 計算每個格點力值

### 多模型比較

```python
plot_tire_surfaces(out, fix, tir_params_list, labels=None)
```

* 支援多個 TIR 模型同時繪製
* 曲面顏色與透明度可區分
* 自動生成 legend
* 可比較 **擬合前 / 擬合後模型差異**

---

## 5️⃣ 摩擦圓 / 滑移率曲面

### Fx-Fy vs κ

```python
plot_friction_circle_vs_kappa_surface(Fz, pressure, alpha_lim, kappa_lim, tir_params, IA)
plot_friction_circle_vs_kappa_curves(Fz, pressure, alpha_lim, kappa_lim, tir_params, IA)
```

功能：

* z 軸為滑移率 κ
* 展示 Fx-Fy 空間內不同 κ 對力的影響
* 可選擇曲面或堆疊曲線形式
* 適用於摩擦圓分析與模型驗證

---

### Fx-Fy vs Fz

```python
plot_friction_circle_vs_Fz_surface(kappa, pressure, alpha_lim, Fz_max, tir_params, IA)
plot_friction_circle_vs_Fz_curves(kappa, alpha_lim, Fz_max, pressure, tir_params, IA)
```

功能：

* z 軸為垂直載荷 Fz
* 分析不同 Fz 對 Fx-Fy 分布的影響
* 可生成光滑曲面或 α 掃描堆疊曲線

---

## 6️⃣ 視覺化特色

* 支援 **3D 曲面與曲線**
* 使用 colormap 區分模型或值大小
* 曲面透明度控制，便於多模型疊加
* 內建 legend 與軸標籤自動生成

---

# 🧠 設計理念

1. **物件繪圖技巧**

   * 透過物件傳入簡化流程
   * 採用高度通用繪圖手法

2. **靈活掃描維度**

   * 可固定 α / κ / Fz 產生不同維度曲面
   * 支援摩擦圓與載荷變化分析

3. **多模型比較**

   * 輕鬆比較擬合前後或不同參數 TIR
   * 可快速評估擬合精度

4. **可擴充性強**

   * Fx/Fy/Mx/Mz/RRT 都可繪製
   * 可增加 RMS、百分比誤差、3D surface heatmap

---

# 🚀 範例執行

```python
if __name__ == "__main__":
    tir_params = load_tir("D2704_mf612.tir")
    tir_params_fit = load_tir("tir_Fitting_results.tir")
    
    outputs = ['FY']
    fix_cases = ['alpha', 'kappa', 'Fz']
    tir_params_list = [tir_params_fit, tir_params]
    
    for out in outputs:
        for fix in fix_cases:
            plot_tire_surfaces(out, fix, tir_params_list)
```

* 對 **FY** 力，分別掃描 α、κ、Fz
* 比較擬合前 (`D2704_mf612.tir`) 與擬合後 (`tir_Fitting_results.tir`) 曲面


# 🏁 總結

此工具提供：

* MF 模型快速曲面生成
* 多模型比較與可視化
* 摩擦圓分析與 κ/Fz 影響研究
* 支援 Fx/Fy/Mx/Mz/RRT輸出
* 比較多種輸入變化對輸出影響
* 易於擴充與整合進完整輪胎擬合流程
