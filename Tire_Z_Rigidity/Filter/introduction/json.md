# Data Filter JSON 設定說明

## 📌 目的

本 JSON 檔用於控制輪胎資料過濾器的篩選邏輯。

它定義了：

* 各資料項目的數值範圍 (`min` / `max`)
* 連續資料點數限制 (`n`)
* 正負區段限制 (`pos_range` / `neg_range`)
* 斜率限制 (`slope_min` / `slope_max`)
* 依 fitting 階段分類資料

你可以透過修改這個 JSON，**精準控制進入 Magic Formula fitting 的資料品質與工況分類**。

---

# 📂 JSON 結構總覽

```json
{
  "分類名稱": {
    "變數名稱": {
      "子分類名稱": {
        "min": 數值,
        "max": 數值,
        "n":   連續點數
      }
    }
  }
}
```

---

# 🧩 第一層：Fitting 階段分類

例如：

```json
"57_1"
"23_234"
```

這些代表不同的：

* 測試 run
* fitting stage
* 不同模型建立階段

👉 若要新增 fitting 階段：

```json
"new_stage_name": {
  ...
}
```

---

# 📊 第二層：物理變數分類

常見變數：

| 變數 | 意義  |
| -- | --- |
| FZ | 法向力 |
| IA | 外傾角 |
| P  | 胎壓  |
| SA | 滑移角 |
| SL | 滑移率 |

若你要新增一個變數限制，例如限制 `V`：

```json
"V": {
  "V_40": {"min": 90, "max": 91, "n": 50}
}
```

---

# 🔢 第三層：數值區段限制 (min / max / n)

範例：

```json
"FZ_10": {
  "min": -1200,
  "max": -700,
  "n": 30
}
```

### 參數說明

| 參數  | 功能           |
| --- | ------------ |
| min | 下限           |
| max | 上限           |
| n   | 需連續滿足條件的資料點數 |

# 🔁 正負斜率區段限制 (pos_range / neg_range)

用於控制例如 SA、SL 這種需要分正負區間的變數。

範例：

```json
"SA": {
  "pos_range": {"min": 10, "max": 20},
  "neg_range": {"min": -20, "max": -10}
}
```

### 用途

* 只取固定 slip angle 工況
* 保證左右對稱資料
* 控制 steady-state cornering 區段

---

# 📈 斜率限制 (slope_min / slope_max)

範例：

```json
"slope_min": -0.05,
"slope_max": -0.00
```

### 用途

* 只取穩定變化區段
* 排除轉場資料
* 排除 ramp-up / ramp-down 過程
