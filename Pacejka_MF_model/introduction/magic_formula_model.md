# Magic Formula 模型

## 模型定位
Magic Formula (MF) 是一個經典的輪胎力學模型，用來描述輪胎在不同工況下的 **縱向力、橫向力、回正力矩、翻轉力矩與滾動阻力矩**。  
版本 **6.1.2** 是針對工程應用的完整公式實現，涵蓋純工況與混合工況。

---

## 模組結構

### 1. **[MF 基類計算](../model/introduction/common.md)**

- **CalculationInput**：封裝輸入工況（法向力、側偏角、縱滑比、胎壓、速度、傾角等）。  
- **MF612 基類**：提供歸一化方法：
  - `_normalize_load()`：載荷歸一化  
  - `_normalize_pressure()`：胎壓歸一化  
  - `_normalize_angles()`：角度歸一化  

**物理意義**：這些歸一化步驟將不同工況轉換成相對基準的無因次量，讓模型能在不同載荷、胎壓、角度下保持一致性。

---

### 2. **[Magic Formula Fx](../model/introduction/Fx_model.md)**
- **Fx0**：純縱滑縱向力  
- **Fx**：混合工況縱向力（考慮側偏角修正）

**物理意義**：描述驅動或制動下，滑移比與縱向力的非線性關係，並在混合工況下考慮側偏角的影響。

---

### 3. **[Magic Formula Fy](../model/introduction/Fy_model.md)**
- **Fy0**：純側滑橫向力  
- **Fy**：混合工況橫向力（考慮縱滑比修正）

**物理意義**：描述側偏角下的橫向力生成，並在混合工況下考慮縱滑比的耦合效應。

---

### 4. **[Magic Formula Mz](../model/introduction/Mz_model.md)**
- **Mz0**：純側滑回正力矩  
- **Mz**：混合工況回正力矩

**物理意義**：描述輪胎在側偏角下產生的回正力矩，包含 **pneumatic trail** 與 **scrub radius** 的效應，並在混合工況下考慮縱滑比的修正。

---

### 5. **[Magic Formula Mx](../model/introduction/Mx_model.md)**
- **Mx**：顛覆力矩 (Overturning Moment)

**物理意義**：描述輪胎因傾角與橫向力作用而產生的翻轉效應，與法向力、橫向力比值及 camber 有關。

---

### 6. **[Magic Formula RRT](../model/introduction/RRT_model.md)**
- **RRT MF**：基於 Magic Formula 的滾動阻力矩  
- **RRT SAE**：基於 SAE 經驗公式的滾動阻力矩

**物理意義**：描述輪胎在滾動過程中的能量損耗，受載荷、胎壓、速度與傾角影響。

---

### 7. **[API 統一接口](../model/api.py)**
提供便利函數：
- `calculate_fx()`：混合縱向力  
- `calculate_fy()`：混合橫向力  
- `calculate_mz()`：混合回正力矩  
- `calculate_mx()`：顛覆力矩  
- `calculate_rrt()`：滾動阻力矩  
- `MF_Universal_solver()` :萬用求解器
- `load_tir` :tir檔案載入工具


簡化使用者操作，只需建立 `CalculationInput`，即可直接呼叫對應的計算模型。

---

### 8. **[init 初始化](../model/__init__.py)**
- 統一導入所有模型與接口  
- 定義 `__all__`，公開主要類別與函數  
- 提供快速開始示例  

讓使用者只需 `import model`，即可使用所有功能。

---

## 整體流程

1. **呼叫並建立輸入**  
這邊必須注意!!!輸入參數除了tir檔案只能用一個，其他所有參數都可以傳入array進行高效運算。傳入參數可以有以下幾種選擇:

   * 純量運算 : 全部輸入都是純量
   * 單一向量運算 : 其中**1個**參數為向量，其他參數為純量
   * 矩陣運算 : 輸入等長度的矩陣進行運算，此方法最高效。建議fitting使用此方法。

   ```python
   import model# 呼叫

   MF = model.CalculationInput(# 參數:這部分之照需求設定
   FZ=800,
   SA=0.6,      
   SL=0.2,
   IA=0.0,
   pressure=80000,
   V = tir_params["LONGVL"],# 可自行改成正確參數
   Ro = tir_params["UNLOADED_RADIUS"],# 可自行改成正確參數
   tir_params=tir_params# 此為TIR檔案中的所有變數
   )
   ```

2. **計算力與力矩**  
   ```python
   Fx = model.MF612_Fx.calculate(MF)   # 縱向力
   Fy = model.MF612_Fy.calculate(MF)   # 橫向力
   Mz = model.MF612_Mz.calculate(MF)   # 回正力矩
   Mx = model.MF612_Mx.calculate(MF)   # 翻轉力矩
   RRT = model.MF612_RRT_MF.calculate(MF) # 滾動阻力矩

   ```

3. **輸出結果**  
   - $Fx$：縱向力  
   - $Fy$：橫向力  
   - $Mz$：回正力矩  
   - $Mx$：翻轉力矩  
   - $RRT$：滾動阻力矩  
