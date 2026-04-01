# Data Filter

這個工具處要進行以下步驟 : 

1. 頭尾清洗（Trim）
2. 布林遮罩（Boolean Mask）
3. 自動低通濾波（Auto Low-pass Filter）
4. 資料轉換

工具位於 : [這裡](../filter.py)

本工具會自動讀取 : [這個json檔案](json.md)


## 1. 頭尾清洗（Head / Tail Trimming）

### 目的

在量測資料（特別是輪胎試驗、動態量測）中，資料序列的**起始與結尾**常包含：

* 系統尚未穩定的過渡狀態
* 感測器尚未進入正常量測範圍
* 減速、停止、或人為干擾

這些資料通常不具物理代表性，因此在進入任何分析前必須先移除。

---

### 數學描述

假設原始資料為一個時間序列：

$$
\mathbf{X} = {x_1, x_2, \dots, x_N}
$$

定義：

* $n_h$：要移除的開頭樣本數
* $n_t$：要移除的結尾樣本數

頭尾清洗後的資料定義為：

$$
\tilde{x}_i =
\begin{cases}
\text{NaN}, & i \le n_h \
\text{NaN}, & i > N - n_t \
x_i, & \text{otherwise}
\end{cases}
$$

此操作等價於：

* **保留資料長度不變**
* 但明確標記「不可用區段」

這樣的設計可確保後續遮罩與濾波在時間對齊上不會產生偏移。

---

### 為何使用 NaN 而非直接刪除

* NaN 可被視為「數學上不存在」
* 可自然被遮罩、濾波、統計運算排除
* 保留原始時間索引結構，避免錯位

---

## 2. 布林遮罩（Boolean Mask）

### 目的

布林遮罩的核心思想是：

> **在時間軸上標記哪些樣本「符合物理與實驗條件」**

每一筆資料最終只會有兩種狀態：

* `True`：可信、可用
* `False`：剔除、不參與後續分析

---

### 2.1 基本範圍遮罩（Range Mask）

對於任一物理量 $x(t)$（例如 $F_z, \alpha, \kappa$），定義允許範圍：

$$
x_{\min} \le x(t) \le x_{\max}
$$

其布林遮罩定義為：

$$
m(t) = \begin{cases}
\text{True}, & x_{\min} \le x(t) \le x_{\max} \
\text{False}, & \text{otherwise}
\end{cases}
$$

---

### 2.2 最小連續長度約束（Minimum Segment Length）

單點或極短區段即使落在合法範圍內，往往只是雜訊或瞬態。

因此引入：

* $L_{\min}$：最小連續有效長度

對遮罩序列 $m(t)$，若某一連續 True 區段長度 $L$ 滿足：

$$
L < L_{\min}
$$

則該整段會被重新設為 False：

$$
m(t) = \text{False}, \quad \forall t \in \text{segment}
$$

此操作在數學上等價於：

* 一維布林訊號的「形態學去雜訊（opening-like operation）」

---

### 2.3 斜率遮罩（Slope-based Mask）

此遮罩用於處理如 slip ratio、slip angle 等「**應呈現線性趨勢**」的訊號。

---

#### (1) 區段定義

首先定義資料允許落入的正負範圍：

$$
x(t) \in [x^+*{\min}, x^+*{\max}] \cup [x^-*{\min}, x^-*{\max}]
$$

落在範圍外的資料點被視為「分段邊界」。

---

#### (2) 區段斜率計算

對每一個連續區段 ${x_1, \dots, x_n}$，以最小平方法擬合：

$$
x(t) \approx a t + b
$$

其中斜率 $a$ 為：

$$
a = \frac{\sum (t_i - \bar{t})(x_i - \bar{x})}{\sum (t_i - \bar{t})^2}
$$

---

#### (3) 斜率條件

若斜率滿足：

$$
a_{\min} \le a \le a_{\max}
$$

則整個區段被視為有效：

$$
m(t) = \text{True}
$$

---

#### (4) 退化與例外處理

* 若區段為常數（$\sigma_x < \varepsilon$）

  * 視為穩態資料，**直接通過**
* 若包含 NaN / Inf

  * 區段捨棄

---

### 2.4 多遮罩合成邏輯

* **同一欄位內多條件**：

$$
m_{\text{col}} = m_1 \lor m_2 \lor \dots
$$

* **不同欄位之間**：

$$
m_{\text{total}} = \bigwedge_k m_k
$$

最終遮罩 $m_{\text{total}}$ 決定資料是否保留。

## 3. 布林遮罩的集合論數學詮釋

### 時間索引集合與資料映射

令離散量測時間索引集合為：

$$
\mathcal{T} = \{ t_1, t_2, \dots, t_N \}
$$

對於任一量測物理量（如 $F_z, \alpha, \kappa, SL$），其資料可視為一個映射：

$$
x : \mathcal{T} \rightarrow \mathbb{R}
$$

布林遮罩的核心目的，是在時間集合 $\mathcal{T}$ 上定義一個**物理上可接受的子集合**。

---

### 單一條件對應的子集合

給定一組範圍限制：

$$
x_{\min} \le x(t) \le x_{\max}
$$

可定義其對應的時間子集合為：

$$
\mathcal{A}
=
\{\, t \in \mathcal{T} \mid x_{\min} \le x(t) \le x_{\max} \,\}
$$

布林遮罩即為該集合的指示函數（indicator function）：

$$
m(t) = \mathbf{1}_{\mathcal{A}}(t)
=
\begin{cases}
1, & t \in \mathcal{A} \\
0, & t \notin \mathcal{A}
\end{cases}
$$

---

### 同一欄位多條件：聯集（OR）

若同一物理量允許多組操作條件，其可接受集合定義為聯集：

$$
\mathcal{A}_{\text{col}}
=
\bigcup_{i=1}^{k} \mathcal{A}_i
$$

對應的布林運算為：

$$
m_{\text{col}}(t)
=
\bigvee_{i=1}^{k} m_i(t)
$$

其物理意義為：

> 只要資料點屬於任一合理操作狀態，即視為有效。

---

### 不同物理量之間：交集（AND）

對多個物理量同時施加限制時，其最終可接受時間集合為：

$$
\mathcal{A}_{\text{total}}
=
\bigcap_{j} \mathcal{A}_j
$$

布林表示為：

$$
m_{\text{total}}(t)
=
\bigwedge_{j} m_j(t)
$$

代表該時間點**同時滿足所有物理與實驗條件**。

---

### 最小連續長度的集合意義

設 $\mathcal{A}$ 中的一段連續時間子集合為：

$$
\mathcal{S}_i
=
\{ t_k, t_{k+1}, \dots, t_{k+L_i} \}
$$

若其長度滿足：

$$
|\mathcal{S}_i| < L_{\min}
$$

則該集合會被移除：

$$
\mathcal{A} \leftarrow \mathcal{A} \setminus \mathcal{S}_i
$$

此步驟可視為在時間集合上的**結構性濾波**，排除不具物理穩定意義的短暫事件。

---

## 4. 傅立葉自動低通濾波器的

### 4.1 時域與頻域的傅立葉對偶

對離散時間訊號 $x(t)$，其頻域表示為：

$$
X(f)
=
\sum_{t=0}^{N-1}
x(t)\,e^{-j2\pi f t}
$$

其中高頻成分通常對應於量測雜訊、結構振動或非物理快速變化。

---

### 4.2 功率頻譜密度與 Welch 方法

功率頻譜密度（PSD）定義為：

$$
P(f) = |X(f)|^2
$$

Welch 方法透過分段、加窗與平均，得到穩定的能量分佈估計。

---

### 4.3 累積能量與截止頻率選擇

定義累積能量函數為：

$$
E(f)
=
\int_{0}^{f} P(\nu)\,d\nu
$$

選擇截止頻率 $f_c$ 使其滿足：

$$
E(f_c)
\ge
r \cdot E(f_{\text{Nyq}})
$$

其中 $r$ 為能量保留比例。此條件代表：

> 頻率區間 $[0, f_c]$ 已包含大部分具物理意義的訊號能量。

---

### 4.4 Butterworth 低通濾波器

$n$ 階 Butterworth 低通濾波器的幅值響應為：

$$
|H(\omega)|^2
=
\frac{1}{1 + (\omega / \omega_c)^{2n}}
$$

其特性為通帶內最大平坦，避免引入非物理振盪。

---

### 4.5 零相位濾波的數學意義

使用前向–反向濾波（`filtfilt`）等價於：

$$
y(t) = H(z)\,H(z^{-1})\,x(t)
$$

可完全抵銷相位延遲，使濾波後訊號與原始時間軸對齊。

---

### 4.6 數值穩定性限制

- 常數訊號：$P(f)=0,\ \forall f>0$，不進行濾波  
- $f_c > 0$：避免退化為純 DC 濾波  
- $f_c < 0.45 f_s$：確保數位濾波器穩定性

## 5. 資料轉換
資料轉換步驟主要分成以轉換與清除

1. 轉換 : 進行單位換算與坐標系上的正負調換
1. 清除 : 去除目前用不到的資料，這部分未來如果可以改進程定義一個json，然後去讀取直接進行資料修改會比較理想，可以進一步降低未來需要改寫程式碼的機率。