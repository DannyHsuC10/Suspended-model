# Suspension_sys 懸吊模型說明

`Suspension_sys` 是本專案中最接近「全車懸吊系統」的主模型資料夾。它把四輪簧上/簧下動態、輪胎垂向剛度、彈簧阻尼 K&C、heave/roll/warp modal force、車架扭轉、roll center 幾何力、anti-dive/anti-squat 幾何力、外力矩與視覺化整合在同一套模擬流程裡。

整理日期：2026-08-29

## 一句話總覽

這個資料夾的目的，是用四輪全車模型計算懸吊受到路面、輪胎力、幾何力與外部力作用後，車身 heave、front roll、rear roll、pitch、yaw，以及四個輪端的簧上/簧下位移與力的時間域反應。

## 整體模型流程

核心流程在 `model/Suspension_model_v12.py`。檔案開頭也印了一張流程圖，簡化後如下：

```text
Road input
  |
  v
Tire KC force
  用輪胎位移/速度計算輪胎垂向力 Ft_kc
  |
  v
Suspension relative motion
  dz = zs - zu
  dv = vzs - vzu
  |
  +-----------------------------+
  |                             |
  v                             v
Suspension KC model       Geometry force
  heave/roll/warp          roll center force
  spring + damper          anti force
  |                             |
  v                             |
Modal to corner force <--------+
  |
  v
corner_to_body
  四角力量轉成 Fz 與 Mx/My/Mz
  |
  v
external_moment
  CG 外力與外部力矩
  |
  v
Body dynamics
  a, alpha
  |
  v
body_to_corner
  車身 heave/roll/pitch 轉回四角 zs/vzs/azs
  |
  v
State integration
```

## 主要入口

| 檔案 | 內容與目的 |
| --- | --- |
| `lab_fullsus.py` | 目前最完整的全車模擬範例。建立 `Suspension_A` 與 `full_suspension_state`，載入 `static_state.json`，跑 2 秒模擬，儲存 `final_state.json` 與 `data.pkl`，並開啟 `SuspensionDashboard`。 |
| `Suspension_LP03.py` | 建立懸吊系統與車輛參數的主要設定檔，目前核心類別是 `Suspension_A`。 |
| `Vehicle_status.py` | 全車 state 類別，保存四輪、車身、輪胎、姿態、外力與控制命令等狀態，並負責積分更新。 |
| `model/Suspension_model_v12.py` | 全車懸吊動態核心函式庫，負責把 K&C、幾何力、外力與車身動態串起來。 |
| `road.py` | 路面與外部輸入範例，例如 FL bump、四輪側向/縱向力輸入。 |
| `Data_extraction.py` | 將 full result 轉成 quarter、pitch、roll visualizer 可用的資料格式。 |
| `data_visualization/` | logger、dashboard 與 quarter/roll/pitch 視覺化工具。 |

## 資料夾結構

| 路徑 | 內容與目的 |
| --- | --- |
| `model/KC_sys/` | 彈簧、阻尼、motion ratio 與 shock/KC system。 |
| `model/sus_geo/` | roll center、anti geometry、camber 與 geometry force 模型。 |
| `model/data_manager/` | CSV/Excel 查表資料載入、資料路徑與備份工具。 |
| `data_visualization/` | 模擬資料記錄、結果擷取後的圖表與 dashboard。 |
| `STL/` | 車體與四輪 STL，用於 3D 顯示。 |

## 全車狀態 `full_suspension_state`

`Vehicle_status.py` 中的 `full_suspension_state` 是模擬狀態容器。它的 wheel order 依程式使用慣例為：

```text
[FL, FR, RL, RR]
```

### 四輪垂向狀態

| 變數 | 意義 |
| --- | --- |
| `zs` | 四輪位置對應的簧上位移。 |
| `zu` | 四輪簧下位移。 |
| `vzs`, `vzu` | 簧上/簧下速度。 |
| `azs`, `azu` | 簧上/簧下加速度。 |
| `Fs` | 懸吊作用到簧上/角落的力。 |
| `Ft` | 輪胎/簧下相關力。 |
| `zr`, `vzr` | 路面高度與路面速度輸入。 |
| `N` | 輪胎法向力。 |

### 輪胎與外部輪端力

| 變數 | 意義 |
| --- | --- |
| `Fx`, `Fy`, `Fz` | 四輪外部輪胎力輸入。 |
| `Mx_w`, `Mz_w`, `RRT_w` | 四輪力矩/滾阻相關輸入。 |
| `omega_w`, `alpha_w` | 車輪角速度與角加速度。 |
| `IA`, `steer`, `SL`, `SA` | camber/inclination、轉角、slip ratio、slip angle 等輪胎狀態。 |

### 車身狀態

| 變數 | 意義 |
| --- | --- |
| `theta` | 車身姿態角，定義為 `[front_roll, rear_roll, pitch, yaw]`。 |
| `omega` | 車身角速度。 |
| `alpha` | 車身角加速度。 |
| `s` | CG 位移 `[x, y, z]`。 |
| `v` | CG 速度 `[vx, vy, vz]`。 |
| `a` | CG 加速度 `[ax, ay, az]`。 |
| `F_cg` | 作用在 CG 的外力。 |
| `M` | 外部力矩輸入。 |

### 積分方式

`Integration()` 使用目前 state 中的 `a`、`alpha`、`azu` 做時間更新：

- 由 `body_to_corner()` 把 CG 與車身姿態轉成四角 `zs`、`vzs`、`azs`。
- 對簧下位移 `zu` 做速度與位移積分。
- 對車身姿態 `theta` 與 CG 位移 `s` 做積分。
- 對車輪角速度 `omega_w` 做積分。

## 懸吊設定 `Suspension_A`

`Suspension_LP03.py` 的 `Suspension_A` 是目前全車模型的主設定。它定義：

| 類別/變數 | 說明 |
| --- | --- |
| `shock_list` | 10 個 K&C 元件，順序為 heave_f、heave_r、roll_f、roll_r、roll_c、warp、FL、FR、RL、RR。 |
| `tire_list` | 四個輪胎垂向 K&C 元件，順序為 FL、FR、RL、RR。 |
| `body_twist` | 車架前後 roll 差的扭轉剛性與阻尼。 |
| `mu_list` | 四輪簧下質量。 |
| `m`, `ms` | 全車質量與簧上質量。 |
| `tf`, `tr`, `lf`, `lr`, `l` | 前後輪距、CG 到前後軸距離與軸距。 |
| `h_cg` | 重心高度。 |
| `I_rate` | front/rear roll inertia 分配比例。 |
| `geometry` | 幾何力模型，由 `create_basic_geometry()` 建立。 |
| `I` | 姿態慣量，格式為 `[front_roll_I, rear_roll_I, pitch_I, yaw_I]`。 |
| `R_tire` | 輪胎半徑。 |
| `W` | 車重。 |

目前 `Suspension_A` 使用多個 `LinearKC` 與 `NullKC` 組合：

- heave front/rear：線性彈簧阻尼。
- roll front/rear：線性彈簧阻尼。
- roll coupling：目前是 `NullKC()`。
- warp：線性彈簧阻尼。
- 直推 corner FL/FR/RL/RR：目前是 `NullKC()`。
- tire FL/FR/RL/RR：線性輪胎剛度與小阻尼。

## K&C 系統 `model/KC_sys/`

K&C 在這裡代表彈簧、阻尼與 motion ratio 的組合，統一由 `KCSystem.force(displacement, velocity)` 輸出力與診斷資訊。

### 組成

| 檔案 | 內容 |
| --- | --- |
| `spring.py` | 彈簧模型：`NullSpring`、`LinearSpring`、`SeriesSpring`、`LookupSpring`。 |
| `damper.py` | 阻尼模型：`NullDamper`、`LinearDamper`、高低速切換、速度加權、查表阻尼等。 |
| `MotionRatio.py` | motion ratio 模型：固定值 `ConstantMR` 或查表 `LookupMR`。 |
| `Shock_Absorbers.py` | `KCSystem`，把 spring、damper、motion ratio 組合成同一個 force interface。 |
| `KC_builder.py` | factory function：`LinearKC()`、`SeriesKC()`、`Ohlins()`、`LookupKC()`、`NullKC()`。 |
| `KC_library.py` | 避震器/K&C 設定範例，例如 linear、Ohlins style、LP03 template、lookup model。 |

### `KCSystem.force()` 輸出

`KCSystem.force(displacement, velocity)` 會計算：

```text
spring_force = spring.force(displacement)
damper_force = damper.force(velocity)
MR = motion_ratio.ratio(displacement)
force = (spring_force + damper_force) * MR^2
```

並回傳：

```python
F, {
    "force": F,
    "spring_force": Fs,
    "damper_force": Fd,
    "motion_ratio": MR,
    "spring_k": k,
    "damper_c": c,
}
```

## Modal 懸吊力

`Suspension_model_v12.py` 的 `Hydraulic_system(fl, fr, rl, rr)` 會把四角相對位移或速度轉成 modal 量：

| Modal | 計算概念 |
| --- | --- |
| `heave_f` | `FL + FR` |
| `heave_r` | `RL + RR` |
| `roll_f` | `FL - FR` |
| `roll_r` | `RL - RR` |
| `roll_c` | `roll_f + roll_r` |
| `warp` | `roll_f - roll_r` |

`shocks_KC_force()` 會把這些 modal displacement/velocity 和四個 corner displacement/velocity 組成 10 個輸入，對應 `sus.shock_list` 的 10 個 K&C 元件。

`Modal_to_corner()` 再把 10 個 K&C force 轉回四角：

```text
FL = heave_f + roll_f + corner_fl + roll_c + warp
FR = heave_f - roll_f + corner_fr - roll_c - warp
RL = heave_r + roll_r + corner_rl + roll_c - warp
RR = heave_r - roll_r + corner_rr - roll_c + warp
```

這是整套全車模型的關鍵，因為它讓 heave、roll、warp 與單角直推彈簧/阻尼可以共存在同一個四輪力架構中。

## 幾何力 `model/sus_geo/`

`model/sus_geo/` 負責把 roll center 與 anti geometry 轉成額外的輪端力與車身力矩。

| 檔案 | 內容 |
| --- | --- |
| `roll_center.py` | roll center 高度模型：固定前後相同、固定前後分離、查表。 |
| `anti_rate.py` | anti-dive、anti-lift、anti-squat rate 模型：固定或查表。 |
| `camber_gain.py` | camber 模型：固定 camber 或 travel 查表。 |
| `Geometry_force.py` | `GeometryModel`，把 `Fx`、`Fy` 透過 RC/anti 幾何轉成 `F_geo` 與 `M_geo`。 |
| `Geo_builder.py` | 幾何模型 factory：`create_fast_geometry()`、`create_basic_geometry()`、`create_table_geometry()`。 |
| `Geo_library.py` | 幾何模型範例/資料庫。 |

### Roll center force

`GeometryModel.rc_force()` 會使用四輪 `Fy` 與前後 roll center 高度計算左右載重轉移：

- 前軸：`Fy_front * h_rc_f / tf`
- 後軸：`Fy_rear * h_rc_r / tr`

並回傳四輪 `F_rc` 以及前/後 roll 幾何力矩。

### Anti force

`GeometryModel.anti_force()` 會使用四輪 `Fx` 判斷煞車或驅動狀態，再套用：

- front braking：anti-dive
- front driving：front lift
- rear driving：anti-squat
- rear braking：rear lift

最後得到四輪 anti force 與 pitch 幾何力矩。

## 全車核心函式

| 函式 | 作用 |
| --- | --- |
| `relative_motion(z1, z2, v1, v2)` | 計算相對位移與相對速度。 |
| `tires_KC_force(tires, zu, zr, vzu, vzr)` | 用輪胎 K&C 模型計算四輪輪胎力。 |
| `chassis_torsion(state, sus)` | 由前後 roll 差與 roll rate 差計算車架扭轉力矩。 |
| `Hydraulic_system(fl, fr, rl, rr)` | 把四角量轉成 heave/roll/warp modal 量。 |
| `shocks_KC_force(shock_list, zs, zu, vzs, vzu)` | 計算 10 個懸吊 K&C 元件力。 |
| `Modal_to_corner(F_kc, state)` | 把 modal K&C force 轉回 FL/FR/RL/RR。 |
| `corner_to_body(Fs_fl, Fs_fr, Fs_rl, Fs_rr, sus)` | 把四角懸吊力轉成車身 `Fz` 與 spring moment。 |
| `external_moment(F_cg, M, sus)` | 把 CG 外力與外部力矩轉成車身 moment。 |
| `sprung_moment(M_ext, M_spring, M_geo, state, sus)` | 合成外力矩、彈簧力矩、幾何力矩與車架扭轉。 |
| `unsprung_force(F_geo, F_kc, Fs)` | 計算簧下合力。 |
| `Suspension_output(state, sus)` | 完整懸吊輸出：`Fz`、`M`、`Ft`、`N`、`Fs`。 |
| `motion(state, sus)` | 單步模型更新入口，寫入 body acceleration、angular acceleration、unsprung acceleration、法向力等 state。 |

## `lab_fullsus.py` 執行案例

目前 `lab_fullsus.py` 的流程是：

1. 建立 `SimulationLogger()`。
2. 建立 `sus = Suspension_A()`。
3. 建立 `state = full_suspension_state(sus)`。
4. 從 `static_state.json` 載入初始穩態。
5. 模擬 `0 ~ 2 s`。
6. 每一步呼叫 `road.road_FL_bump(state)`。
7. 呼叫 `sm.motion(state, sus)` 計算全車懸吊反應。
8. 呼叫 `state.Integration(sus)` 更新狀態。
9. 用 logger 記錄完整 state。
10. 儲存 `final_state.json`。
11. 開啟 `SuspensionDashboard(result)`。
12. 儲存 `data.pkl`。

執行方式：

```powershell
cd D:\Danny\DH3868\Suspension-model\Suspension_sys
python lab_fullsus.py
```

## 路面與輸入 `road.py`

| 函式 | 用途 |
| --- | --- |
| `road_FL_bump(state)` | 在 `0.5 s < t < 0.7 s` 時，讓 FL 路面高度 `zr[0] = 0.01 m`。 |
| `road_D(state)` | 0.5 秒後輸入四輪 `Fy`、`Fx` 與 CG 重力，用來測試側向/縱向外力與幾何力。 |

## 結果資料與視覺化

| 檔案/資料夾 | 內容 |
| --- | --- |
| `static_state.json` | 初始穩態 state，可由 `full_suspension_state.load_state_json()` 載入。 |
| `final_state.json` | 模擬結束後輸出的 state。 |
| `data.pkl` | `SimulationLogger` 儲存的完整時間序列資料。 |
| `data_visualization/Simulation_Logger.py` | 遞迴展開 state 物件並記錄每個欄位。 |
| `data_visualization/Dynamic_Visualizer_dashboard.py` | 全車 dashboard。 |
| `data_visualization/Dynamic_Visualizer_quarter.py` | 單輪/quarter 視覺化。 |
| `data_visualization/Dynamic_Visualizer_roll.py` | roll 視覺化。 |
| `data_visualization/Dynamic_Visualizer_pitch.py` | pitch 視覺化。 |
| `data_visualization/plot_results.py` | 一般結果圖表。 |

`Data_extraction.py` 可把 full result 轉成不同 visualizer 使用的資料：

| 函式 | 用途 |
| --- | --- |
| `get_quarter_result(result, wheel)` | 從 full result 擷取單輪資料，`wheel = 0,1,2,3` 對應 FL/FR/RL/RR。 |
| `get_pitch_result(result)` | 整理 front/rear sprung/unsprung、pitch、heave、chassis twist 等資料。 |
| `get_roll_result(result, axle=None)` | 整理 roll visualizer 所需資料，可指定前軸 `"F"` 或後軸 `"R"`。 |

## 資料管理 `model/data_manager/`

這裡提供查表資料的讀取與備份。

| 檔案 | 內容 |
| --- | --- |
| `data_path.py` | 定義資料根目錄，讓相對路徑可從 `model/data_manager/` 解出。 |
| `data_loader.py` | `DataLoader.load_csv()`、`DataLoader.load_excel()`，回傳 `LookupData`。 |
| `backup.py` | 備份資料檔工具。 |
| `data_tester.py` | 資料讀取測試。 |
| `data/spring.csv` | 彈簧查表資料。 |
| `data/damper.csv` | 阻尼查表資料。 |
| `data/motion_ratio.csv` | motion ratio 查表資料。 |

## 液壓模型

`model/Hyd_steady.py` 與 `model/Hyd_Transient .py` 是液壓/互聯系統的實驗模型。

| 檔案 | 內容 |
| --- | --- |
| `Hyd_steady.py` | 穩態液壓求解範例。包含液壓缸、節點、接頭、輸入、彈簧與 root solver。 |
| `Hyd_Transient .py` | 暫態液壓模型。檔名 `Transient` 後面有空白，命令列與 import 時要特別注意。 |

目前主模型的 modal 轉換函式名稱叫 `Hydraulic_system()`，但它主要做的是 heave/roll/warp 座標轉換；真正的液壓 network 模型仍在 `Hyd_steady.py` 與 `Hyd_Transient .py` 中獨立發展。

## STL 與 3D 顯示

`STL/` 內包含：

| 檔案 | 內容 |
| --- | --- |
| `LP02.stl` | 車體/底盤 STL。 |
| `W_FL.stl` | 前左輪 STL。 |
| `W_FR.stl` | 前右輪 STL。 |
| `W_RL.stl` | 後左輪 STL。 |
| `W_RR.stl` | 後右輪 STL。 |

相關展示腳本：

| 檔案 | 用途 |
| --- | --- |
| `load_and_show.py` | 載入 `data.pkl` 並用 dashboard 顯示。 |
| `load_and_show STL_v2.py` | 載入 STL 並進行 3D 顯示/動畫相關操作。 |
| `LP02_v.py` | LP02 車體/視覺化相關腳本。 |

## 專案環境

`pyproject.toml` 顯示此資料夾使用 Python 專案格式，依賴如下：

```toml
requires-python = ">=3.14"
dependencies = [
    "matplotlib>=3.11.1",
    "numpy>=2.5.1",
    "pandas>=3.0.5",
    "pyvista>=0.48.4",
    "scipy>=1.18.0",
]
```

資料夾內有 `.venv/` 與 `uv.lock`，代表曾使用 uv 或虛擬環境管理依賴。`.venv/` 是本地環境，不屬於模型原始碼。

## 建議閱讀順序

1. 先看 `lab_fullsus.py`，了解目前完整模擬如何被呼叫。
2. 看 `Suspension_LP03.py`，理解車輛、K&C、輪胎、幾何與慣量設定。
3. 看 `Vehicle_status.py`，理解 state 內有哪些物理量，以及積分如何更新。
4. 看 `model/Suspension_model_v12.py`，理解每一步如何由位移/速度算力，再轉成車身加速度。
5. 看 `model/KC_sys/`，理解彈簧、阻尼、MR 與 shock force。
6. 看 `model/sus_geo/`，理解 roll center 與 anti geometry 如何產生幾何力。
7. 看 `Data_extraction.py` 與 `data_visualization/`，理解結果如何轉成圖表。

## 注意事項

- `Suspension_sys/README.md` 原本是空檔，本文件是依目前程式內容整理出的架構說明。
- `model/Hyd_Transient .py` 檔名含空白，建議日後改名成 `Hyd_Transient.py` 並同步修正引用。
- `model/Suspension_model_v12.py` 匯入時會直接 `print("Suspension model Ready!!!")` 與流程圖，作為套件匯入時會有終端輸出。
- `Suspension_LP03.py` 檔案底部直接呼叫 `Suspension_A()`，import 時也會建立一次物件。
- `tire_normal_force()` 目前先做了 `np.maximum()`，但下一行又改回 `N = Ft_kc`，所以實際沒有把法向力限制為非負值。
- `sprung_moment()` 目前會印出 `M_ext, M_spring, M_geo, moment`，長時間模擬時輸出會很多。
- `road_FL_bump()` 註解寫 5 cm，但程式設定 `0.01 m`，實際是 1 cm。

## 這個模型目前能做什麼

`Suspension_sys` 可以用來：

- 驗證四輪懸吊 heave/roll/warp modal 設計。
- 比較不同 K&C 元件設定對車身姿態與輪胎法向力的影響。
- 模擬單輪 bump、四輪外力、側向力與縱向力對全車的影響。
- 分析 roll center 與 anti geometry 對載重轉移的貢獻。
- 產生 full result，再拆成 quarter、roll、pitch 視覺化資料。
- 搭配 STL 或 dashboard 做模型展示與結果檢查。

簡單說，`Suspension_sys` 是整個 `Suspension-model` 工作區裡「完整懸吊系統整合與驗證」的核心。
