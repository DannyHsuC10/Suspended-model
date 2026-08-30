# front_view 資料夾說明

`front_view` 是前視懸吊幾何分析工作區，主要用 2D 幾何模型建立左右懸吊，計算輪胎接地點、kingpin、上下控制臂、instant center、roll center 與 camber 變化，並用 Matplotlib 做互動圖與 mapping 圖。

整理日期：2026-08-29

## 整體目的

這個資料夾的目的是把前視懸吊幾何從車輛參數轉成可計算、可視覺化的模型。它可以用來回答幾類問題：

- 靜態前視幾何長什麼樣子。
- 下控制臂角度改變時，輪胎接地點與羊角如何運動。
- 左右輪不同 travel 對 roll angle、camber、roll center 的影響。
- 給定 heave/roll 或左右輪行程時，反算對應的懸吊姿態。
- 批次掃描整個行程範圍，產生 RC/camber map。

## 核心資料流

```text
car.py
  定義車輛、輪胎、前懸吊設計參數
      |
Geometric_Analysis.py
  由參數計算靜態幾何點，建立左右懸吊物件
      |
geometry.py
  提供 Point、Link、RigidBody2D、Wheel 等基礎幾何物件
      |
visualization.py
  將幾何物件轉成 Matplotlib 圖形
      |
sus_fv_v5.py
  互動式前視圖，滑桿調整左右 lower arm angle
      |
sus_fv_maping.py
  批次掃描左右角度，輸出 suspension_kinematics_data.pkl
      |
rc_camber_map.py
  讀取 pkl，畫出 camber surface 與 roll center map
```

## 檔案總覽

| 檔案 | 內容與目的 |
| --- | --- |
| `car.py` | 車輛與前懸吊設計參數。包含 wheelbase、CG、track、輪胎半徑、輪胎寬、scrub radius、KPI、目標 roll center 高度、FVSA、上下輪端接點等。 |
| `geometry.py` | 基礎 2D 幾何物件。包含 `Point`、`Link`、`RigidBody2D`、`Polygon`、`Wheel`、`Body`。 |
| `Geometric_Analysis.py` | 前視懸吊幾何與運動學核心。負責算靜態點位、上下控制臂、羊角、instant center、roll center、camber、行程反算等。 |
| `visualization.py` | Matplotlib 視覺化封裝。把 `Point`、`Link`、`Polygon` 畫成可更新的 plot object。 |
| `sus_fv_v5.py` | 互動式前視懸吊圖。用兩個 slider 控制左右 lower arm angle，並即時更新幾何與 roll center。 |
| `sus_fv_maping.py` | 批次掃描左右 lower arm angle，計算 heave、roll、左右 camber、RC 位置與各點座標，輸出 `.pkl`。 |
| `rc_camber_map.py` | 讀取 `suspension_kinematics_data.pkl`，畫出 camber 3D surface、RC migration cloud 與 RC height surface。 |
| `lab.py` | 直接求解範例。展示如何用 theta、wheel travel、heave/roll 姿態反推 camber 與 roll center。 |
| `suspension_kinematics_data.pkl` | `sus_fv_maping.py` 產生的幾何掃描資料。 |

## 主要概念

| 名稱 | 在此資料夾中的意義 |
| --- | --- |
| `kg` | Kingpin ground 或 kingpin 相關下方點，用於建立 kingpin 幾何。 |
| `kua` | Kingpin/upright 上方接點。 |
| `lak` | Lower arm 與 upright 下方接點。 |
| `gnd` | 輪胎接地點。 |
| `cpb_rl`, `cpb_ru` | 車體側控制臂接點。 |
| `IC` | Instant Center，上下控制臂延長線交點。 |
| `ICo` | 設計目標或初始 instant center 參考點。 |
| `RC` | Roll Center，左右 wheel force line 的交點。 |
| `FVSA` | Front View Swing Arm，用於前視懸吊幾何設計。 |
| `KPI` | Kingpin Inclination，主銷內傾角。 |
| `scrub_radius` | 輪胎接地中心與 kingpin 地面投影的水平距離。 |

## `car.py`

`Car` 類別是前視幾何的參數來源。重要參數包含：

| 參數 | 說明 |
| --- | --- |
| `l`, `lf`, `lr` | 軸距與重心到前/後軸距離。 |
| `tf`, `tr` | 前/後輪距。front view 目前主要使用 `tf`。 |
| `h_cog` | 重心高度。 |
| `m`, `w` | 車重與重量。 |
| `bottom` | 車底距地高度。 |
| `body_face_f` | 前視車體截面 polygon。 |
| `free_radius`, `load_Radius`, `tire_width` | 輪胎自由半徑、負載半徑與胎寬。 |
| `scrub_radius_f`, `kpi_f`, `h_rc_f`, `fvsa_f` | 前懸吊幾何設計參數。 |
| `Au_f`, `Al_f` | 上/下輪端接點相對設定。 |
| `sus_contact_f` | 車體側懸吊接點的幾何參考框。 |

## `geometry.py`

這個檔案是幾何物件的底層工具。

| 類別 | 功能 |
| --- | --- |
| `Point` | 2D 點，提供 `x`、`y`、`move()`、`mirror_x()`。 |
| `Link` | 兩點連桿，提供 vector、length、angle、direction、midpoint。 |
| `RigidBody2D` | 用兩個參考點更新剛體姿態，適合讓 upright 與輪胎點一起旋轉/平移。 |
| `Polygon` | 多點 polygon 基底。 |
| `Wheel` | 繼承 `Polygon`，表示輪胎外形。 |
| `Body` | 繼承 `Polygon`，表示車身外形。 |

## `Geometric_Analysis.py`

這是 front view 幾何計算的核心。

### 幾何函式

| 函式 | 功能 |
| --- | --- |
| `rotate_point_about(center, length, theta)` | 給定中心、長度與角度，計算旋轉後的點。 |
| `circle_intersection(c1, r1, c2, r2)` | 求兩圓交點，用於由上下臂長度求解羊角點。 |
| `simulate_side_theta(sus, theta)` | 給定單側懸吊與下臂角度，計算新的 `kua`、`lak`。 |
| `update_upright(sus, kua_new, lak_new)` | 根據新的上下羊角點更新接地點位置。 |
| `calculate_theta_limits(sus, target_travel=0.025)` | 由目標 wheel travel 估算 lower arm angle 可用範圍。 |

### 主要類別

| 類別 | 功能 |
| --- | --- |
| `SusGeometryHelper` | 從 `Car` 參數建立靜態點位，並提供線交點、IC 更新、RC 計算。 |
| `SuspensionSide` | 單側懸吊物件。包含 point、link、force line、wheel、upright body，並可鏡像生成左側。 |
| `SuspensionDirectSolver` | 直接求解器。可用 theta、左右 wheel travel 或 heave/roll 姿態反算 camber 與 RC。 |

## 視覺化腳本

### `sus_fv_v5.py`

這是最直觀的前視圖工具。執行後會開啟 Matplotlib 視窗，包含：

- 車體截面。
- 左右輪胎。
- 上下控制臂。
- upright/kingpin。
- instant center 與 force line。
- CG 與 roll center。
- 兩個 slider：`Right Arm Angle`、`Left Arm Angle`。

滑動 slider 時會更新左右懸吊幾何，並重新計算 roll center。

執行方式：

```powershell
cd D:\Danny\DH3868\Suspension-model\front_view
python sus_fv_v5.py
```

### `sus_fv_maping.py`

這個腳本做批次掃描。流程是：

1. 建立 `Car`、`SusGeometryHelper`。
2. 先建立右側懸吊，再鏡像出左側。
3. 用 `calculate_theta_limits()` 找出約 ±25 mm travel 的角度範圍。
4. 建立 `theta_left_array` 與 `theta_right_array`。
5. 雙重迴圈掃描左右角度。
6. 對每個狀態計算：
   - left/right travel
   - heave
   - roll angle
   - left/right camber
   - roll center
   - IC、GND、KUA、LAK、wheel points
7. 輸出 `suspension_kinematics_data.pkl`。
8. import `rc_camber_map` 直接畫圖。

目前掃描解析度是：

```python
steps = 30
```

所以總共會產生 `30 x 30 = 900` 筆幾何狀態。

### `rc_camber_map.py`

這個腳本讀取 `suspension_kinematics_data.pkl`，再把一維 dataset 還原成 2D grid。它會產生兩組圖：

| 圖 | 內容 |
| --- | --- |
| Camber 3D surface | 以 heave 與 roll angle 為輸入軸，分別畫 left/right camber 曲面。 |
| Roll Center map | 畫 RC X/Y migration cloud，以及 RC height 隨左右 wheel travel 變化的 3D 曲面。 |

### `lab.py`

`lab.py` 是非圖形互動的求解範例，展示 `SuspensionDirectSolver` 的三種用法：

| 方法 | 用途 |
| --- | --- |
| `solve_by_thetas(theta_l, theta_r)` | 已知左右 lower arm angle，直接求 heave、roll、camber、RC。 |
| `solve_by_pose(target_heave_m, target_roll_deg)` | 已知車身 heave/roll，反算左右 lower arm angle，再求 camber、RC。 |
| `solve_by_travels(l_travel_m, r_travel_m)` | 已知左右 wheel travel，反算幾何狀態。 |

## 輸出資料格式

`suspension_kinematics_data.pkl` 是一個 list，每筆資料是一個 dict。每筆狀態包含：

| key | 說明 |
| --- | --- |
| `travel_left`, `travel_right` | 左右輪行程，單位 m。 |
| `heave` | 左右輪平均行程，單位 m。 |
| `roll_deg` | 左右接地點連線相對水平的角度，單位 deg。 |
| `camber_left_deg`, `camber_right_deg` | 左右輪 camber，單位 deg。 |
| `theta_left`, `theta_right` | 左右 lower arm angle，單位 rad。 |
| `rc` | roll center 座標 `[x, y]`，單位 m。 |
| `ic_left`, `ic_right` | 左右 instant center 座標。 |
| `gnd_left`, `gnd_right` | 左右輪胎接地點座標。 |
| `kua_left`, `kua_right` | 左右 upright 上點座標。 |
| `lak_left`, `lak_right` | 左右 lower arm/upright 下點座標。 |
| `wheel_pts_left`, `wheel_pts_right` | 左右輪胎 polygon 點座標。 |

## 建議使用順序

1. 先看 `car.py`，確認車輛與前懸吊參數。
2. 看 `Geometric_Analysis.py` 的 `calc_static_points()`，理解靜態點位如何算出。
3. 執行 `sus_fv_v5.py`，用 slider 看幾何如何動。
4. 執行 `lab.py`，測試指定 theta、travel、heave/roll 的求解結果。
5. 執行 `sus_fv_maping.py` 產生完整掃描資料。
6. 用 `rc_camber_map.py` 查看 camber 與 roll center map。

## 與整體專案的關係

`front_view` 專注在前視幾何與運動學，不直接處理完整車輛動態力學。它比較像是懸吊設計前處理工具：

- 提供靜態懸吊幾何。
- 估算 roll center 高度與遷移。
- 產生 camber gain / camber map。
- 把幾何結果提供給後續的 dynamics 或 full suspension model 參考。

相較於 `dynamics_analyze/` 的彈簧阻尼時間域模擬，`front_view/` 更關心「幾何點位如何移動」；相較於 `Suspension_sys/` 的全車模型，它更適合快速調整與理解前視懸吊設計。

## 注意事項

- `car.py` 檔案底部直接呼叫 `Car()`，所以 import 時會印出 `load_Radius`。
- `Geometric_Analysis.py` 的 `calc_roll_center()` 目前會 `print("rc_pos", rc_pos)`，批次掃描時終端會輸出很多 RC 座標。
- `geometry.Link` 中 `angle` property 定義了兩次，結果相同，但可日後整理。
- `SuspensionSide.update_kinematics()` 內有 `self.upper_force.p2 = self.IC` 等設定，但 `Link` 使用的是 `start/end` 屬性；若 force line 沒有如預期更新，這裡可以檢查是否應改為更新 `end`。
- `.pkl` 是 Python pickle 格式，適合本專案內部使用；若要和其他工具交換資料，建議另外輸出 CSV 或 JSON。
