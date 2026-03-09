# [四輪載重線性掃描分析](both_null_space.m)

此方法將 **最小作用量原理解 (LSM)** 與 **重心分配法解 (Ratio)** 作為兩個已知解點，並透過線性插值掃描，分析四輪載重在兩種解法之間的變化。
## 簡介
此方法將 **最小作用量原理解 (LSM)** 與 **重心分配法解 (Ratio)** 作為兩個已知解點，並透過線性插值掃描，分析四輪載重在兩種解法之間的變化。

- 此方法提供一條連續的解線，連接 **LSM解** 與 **Ratio解**。  
- Null space 的存在代表系統解並非唯一，而是存在一族解。  
- Unified Line Scan 可用於比較兩種方法的差異，並觀察四輪載重在不同解法之間的過渡行為。
## 已知解點
- $N_1$: 由 **Four\_wheel\_load\_LSM** 計算得到的四輪載重解。
- $N_2$: 由 **Four\_wheel\_load** 計算得到的四輪載重解。

兩者皆為 $4 \times 1$ 向量：
$$
N_1 = 
\begin{bmatrix}
N_{FL}^{LSM} \\
N_{FR}^{LSM} \\
N_{RL}^{LSM} \\
N_{RR}^{LSM}
\end{bmatrix}, \quad
N_2 = 
\begin{bmatrix}
N_{FL}^{Ratio} \\
N_{FR}^{Ratio} \\
N_{RL}^{Ratio} \\
N_{RR}^{Ratio}
\end{bmatrix}
$$

## 線性掃描方法
定義線向量：
$$
V = N_2 - N_1
$$

定義掃描參數 $\alpha \in [0,1]$，則線性插值解為：
$$
N(\alpha) = N_1 + \alpha V
$$

其中：
- $\alpha = 0 \Rightarrow N(\alpha) = N_1$ (LSM解)
- $\alpha = 1 \Rightarrow N(\alpha) = N_2$ (Ratio解)

## Null Space 的概念
在 LSM 方法中，我們解的是一個 **靜不定系統**。  
矩陣方程：
$$
A N = -b
$$
其中 $A$ 為平衡方程矩陣，$N$ 為四輪載重。

由於方程式可能存在多餘或不足的約束，解 $N$ 並非唯一。  
這時候，解可以表示為：
$$
N = N_p + N_{null}
$$
- $N_p$: 特解 (由最小平方解得到)
- $N_{null}$: 屬於 $A$ 的零空間 (null space) 的向量

零空間的意義：
- 若 $A N_{null} = 0$，則 $N_{null}$ 不影響平衡方程。  
- 不同的 $N_{null}$ 組合，代表不同的載重分配方式，但都能滿足力與力矩平衡。  
- 因此，LSM 解提供一個「最小能量」的特解，而 Ratio 解則是另一種分配方式。  
- Unified Line Scan 則是在 $N_1$ 與 $N_2$ 之間建立一條線，探索可能的解族。

