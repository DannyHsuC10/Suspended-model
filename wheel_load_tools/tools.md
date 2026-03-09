# 四輪載重計算方法規格說明
## 最小作用量原理 [Four_wheel_load_LSM](Four_wheel_load_LSM.m)

### 方法概念
- 將四輪垂直力 $N = [N_{FL}, N_{FR}, N_{RL}, N_{RR}]$ 視為未知數。
- 建立平衡方程：
  - 垂直力平衡
  - 橫向 (roll) 力矩平衡
  - 縱向 (pitch) 力矩平衡
- 使用最小平方解求解。

### 方程式
$$
A = 
\begin{bmatrix}
z_{pos} \\
y_{pos} \\
x_{pos}
\end{bmatrix}, \quad
b = m
\begin{bmatrix}
a_z \\
a_y h \\
a_x h
\end{bmatrix}
$$

若有外力 $F = [F_x, F_y, F_z]$，其力矩影響為：
$$
M_x^{add} = r_y F_z - r_z F_y, \quad
M_y^{add} = r_z F_x - r_x F_z
$$

最終解：
$$
N = A^T (A A^T)^{-1} (-b)
$$

### 特點
- 適用於靜不定系統。
- 可直接考慮外力作用點與力矩。
- 精度高，適合動態模擬。

---

## 重心分配法 [Four_wheel_load](Four_wheel_load.m)

### 方法概念
- 先計算靜態重量分配：
$$
F_s = W \cdot (CG_x \cdot CG_y), \quad W = m g
$$
- 再計算載重轉移：
$$
dF = m h \cdot \frac{[a_x, a_y]}{[L, d]}
$$
- 若有外力，轉換成等效力矩再加到 $dF$。

### 方程式
靜態分配矩陣：
$$
F =
\begin{bmatrix}
F_{FL} & F_{FR} \\
F_{RL} & F_{RR}
\end{bmatrix}
$$

最終載重：
$$
N = [F_{FL}, F_{FR}, F_{RL}, F_{RR}]^T
$$

### 特點
- 計算簡單，直觀易懂。
- 適合靜態或近似分析。
- 效率高，但精度有限。

---

## 方法比較

| 特性 | 最小作用量原理 (LSM) | 重心分配法 (CG) |
|------|----------------------|-----------------|
| 數學基礎 | 線性代數，最小平方解 | 力平衡 + 比例分配 |
| 適用範圍 | 靜不定系統、動態模擬 | 靜態近似、簡化分析 |
| 外力影響 | 可直接考慮作用點與力矩 | 需轉換成等效載重轉移 |
| 精確度 | 高 | 中等 |
| 計算複雜度 | 較高 (矩陣運算) | 較低 (代數計算) |

---

## 結論
- **Four_wheel_load_LSM**：適合需要精確考慮力矩平衡與外力影響的情境，例如賽車模擬或研究用途。  
- **Four_wheel_load**：適合快速估算或工程應用，計算簡單但精度有限。