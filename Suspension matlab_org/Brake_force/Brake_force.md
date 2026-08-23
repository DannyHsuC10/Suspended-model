# 煞車力計算

此程式用於計算車輛煞車系統的力學分佈，包含主缸、卡鉗以及煞車力的推導。
* [Brake_force](Brake_force.m)
## 主要流程

1. 載入資料並設定重力加速度 $g = 9.81$
2. 計算駕駛施加的力 $F_{driver}$
3. 經由踏板比率 $PR$ 得到主缸輸入力 $F_{mc}$
4. 依照平衡桿分配比例計算前後壓力
5. 計算主缸面積與壓力
6. 計算卡鉗面積與作用力
7. 推導前後輪煞車力，並合併得到總煞車力

---

## 方程式推導

### 駕駛輸入力
$$F_{driver}$$
由輸入資料讀取。

### 主缸輸入力
$$F_{mc} = F_{driver} \cdot PR$$

### 平衡桿分配
- 前比例：$$bb_f = balance\_bar$$  
- 後比例：$$bb_r = 1 - balance\_bar$$

### 主缸面積
- 前主缸面積：$$A_{mc\_f} = \pi \cdot \left(\frac{D_{mc\_f}}{2}\right)^2$$  
- 後主缸面積：$$A_{mc\_r} = \pi \cdot \left(\frac{D_{mc\_r}}{2}\right)^2$$

### 主缸壓力
- 前壓力：$$P_{mc\_f} = \frac{F_{mc} \cdot bb_f}{A_{mc\_f}}$$  
- 後壓力：$$P_{mc\_r} = \frac{F_{mc} \cdot bb_r}{A_{mc\_r}}$$

### 卡鉗面積
- 前卡鉗面積：$$A_{caliper\_f} = N_{caliper\_f} \cdot \pi \cdot \left(\frac{D_{caliper\_f}}{2}\right)^2$$  
- 後卡鉗面積：$$A_{caliper\_r} = N_{caliper\_r} \cdot \pi \cdot \left(\frac{D_{caliper\_r}}{2}\right)^2$$

### 卡鉗作用力
- 前卡鉗力：$$F_{caliper\_f} = P_{mc\_f} \cdot \mu_{pad} \cdot A_{caliper\_f}$$  
- 後卡鉗力：$$F_{caliper\_r} = P_{mc\_r} \cdot \mu_{pad} \cdot A_{caliper\_r}$$

### 煞車盤半徑
$$r_{disc} = \frac{r_{disc\_o}}{2} - d_{gap}$$

### 前後煞車力
- 前煞車力：$$F_{brake\_f} = \frac{F_{caliper\_f} \cdot r_{disc} \cdot 2}{r_w}$$  
- 後煞車力：$$F_{brake\_r} = \frac{F_{caliper\_r} \cdot r_{disc} \cdot 2}{r_w}$$

### 總煞車力
$$F_{brake} = F_{brake\_f} + F_{brake\_r}$$

---

## 程式輸出
- 駕駛輸入力 $F_{driver}$
- 主缸力 $F_{mc}$
- 前後煞車力 $F_{brake\_f}, F_{brake\_r}$
- 總煞車力 $F_{brake}$
