# Magic Formula Mz
模型位置 >> [Mz](../Mz_models.py)

預先計算輸入力量 : [Fy](Fy_model.md)

預先計算輸入力量 : [Fx](Fx_model.md)

## Fy 基底回正力矩 $Mzt$

### 等效滑移角
$$
\alpha_t^{eq} = \sqrt{\alpha^2 + \kappa^2 \left(\frac{K_{x\kappa}}{K_{y\alpha}'}\right)^2} \cdot \text{sign}(\alpha)
$$

**物理意義**：  
將縱向滑移 $\kappa$ 與側滑角 $\alpha$ 組合成等效滑移角，反映**縱橫耦合效應**（combined slip）。

---

### 側偏剛性（修正）
$$
K_{y\alpha}' = K_{y\alpha} + \epsilon_K
$$

**物理意義**：  
避免數值不穩定（分母為零），同時代表低載荷時的剛性修正。

---

### Pneumatic trail 偏移
$$
S_{ht} = QHZ1 + QHZ2 \cdot dfz + (QHZ3 + QHZ4 \cdot dfz)\cdot ia
$$

$$
\alpha_t = \alpha_m + S_{ht}
$$

**物理意義**：  
描述接地補丁壓力中心偏移，使回正力矩曲線產生水平位移。

---

### 剛性係數 $B_t$
$$
B_t = (QBZ1 + QBZ2 \cdot dfz + QBZ3 \cdot dfz^2)
\cdot (1 + QBZ5|ia| + QBZ4 ia)
\cdot \frac{\lambda_{y\alpha}}{\lambda_{\mu y}}
$$

**物理意義**：  
控制 pneumatic trail 對滑移角的敏感程度。

---

### 形狀因子
$$
C_t = QCZ1
$$

**物理意義**：  
控制曲線整體形狀（類似 Magic Formula 的 shape factor）。

---

### 曲率因子
$$
E_t = (QEZ1 + QEZ2 \cdot dfz + QEZ3 \cdot dfz^2)
\cdot \left[1 + (QEZ4 + QEZ5 ia)\frac{2}{\pi}\arctan(B_t C_t \alpha_t)\right]
$$

**物理意義**：  
控制 pneumatic trail 在大滑移角時的飽和與非線性。

---

### 最大 trail（幅值）
$$
D_t = D_{t0} \cdot (1 + QDZ3 |ia| + QDZ4 ia^2)\cdot \zeta_5
$$

其中
$$
D_{t0} = F_z \cdot \frac{R_0}{F_{z0}'} \cdot (QDZ1 + QDZ2 dfz)
\cdot (1 - PPZ1 \cdot dpi)\cdot \lambda_{MP} \cdot \text{sign}(V_x)
$$

**物理意義**：  
代表 pneumatic trail 的最大值，與載荷、胎壓與輪胎半徑相關。

---

### Pneumatic trail
$$
t = D_t \cdot \cos\left(C_t \cdot \arctan\left(B_t \alpha_t^{eq} - E_t(B_t \alpha_t^{eq} - \arctan(B_t \alpha_t^{eq}))\right)\right)
$$

**物理意義**：  
描述接地力作用點相對輪胎中心的偏移距離。

---

### Fy 基底回正力矩
$$
M_{zt} = -t \cdot F_y
$$

**物理意義**：  
回正力矩來自側向力乘上力臂（pneumatic trail）。  
負號表示力矩方向傾向使車輪回正。

---

## 純側滑回正力矩 $Mz$

### 等效滑移角
$$
\alpha_r^{eq} = \sqrt{\alpha_r^2 + \kappa^2 \left(\frac{K_{x\kappa}}{K_{y\alpha}'}\right)^2} \cdot \text{sign}(\alpha_r)
$$

**物理意義**：  
與 $Mzt$ 類似，考慮縱橫耦合後的等效滑移角。

---

### 偏移修正
$$
S_{hf} = S_{hy} + \frac{S_{vy}}{K_{y\alpha}'}
$$

$$
\alpha_r = \alpha_m + S_{hf}
$$

**物理意義**：  
整合側向力偏移對回正力矩的影響。

---

### 剛性因子
$$
B_r = (QBZ9 \cdot \frac{\lambda_{y\alpha}}{\lambda_{\mu y}} + QBZ10 \cdot B_y C_y)\cdot \zeta_6
$$

**物理意義**：  
控制殘餘回正力矩對滑移角的變化敏感度。

---

### 形狀因子
$$
C_r = \zeta_7
$$

**物理意義**：  
控制殘餘回正力矩曲線形狀。

---

### 幅值
$$
D_r = F_z R_0 \cdot \Big[
(QDZ6 + QDZ7 dfz)\lambda_{RES}\zeta_2
+ ((QDZ8 + QDZ9 dfz)(1 + PPZ2 dpi)
+ (QDZ10 + QDZ11 dfz)|ia|)
\cdot ia \cdot \lambda_{KZC}\zeta_0
\Big]
\cdot \lambda_{\mu y} \cdot \cos(\alpha')
$$

**物理意義**：  
描述殘餘回正力矩的強度，包含：
- 輪胎變形
- 外傾角（camber）效應
- 接地分布不對稱

---

### 殘餘回正力矩
$$
M_{zr} = D_r \cdot \cos\left(C_r \cdot \arctan(B_r \alpha_r^{eq})\right)
$$

**物理意義**：  
即使 pneumatic trail 消失（高滑移），仍存在的回正力矩。

---

### 力矩偏移項
$$
s = R_0 \cdot (SSZ1 + SSZ2 \frac{F_y}{F_{z0}'} + (SSZ3 + SSZ4 dfz) ia)\cdot \lambda_S
$$

$$
M_{z,offset} = s \cdot F_x
$$

**物理意義**：  
縱向力 $F_x$ 透過偏移距離產生額外回正力矩。

---

## 總回正力矩
$$
M_z = M_{zt} + M_{zr} + s \cdot F_x
$$

**物理意義**：  
完整回正力矩由三部分組成：
1. **$M_{zt}$**：側向力 × pneumatic trail（主要來源）
2. **$M_{zr}$**：殘餘力矩（高滑移仍存在）
3. **$sF_x$**：縱向力造成的附加力矩
