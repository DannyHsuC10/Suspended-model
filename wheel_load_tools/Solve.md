# 分析力學靜不定問題求解
## 問題定義
我們希望計算4個車輪的附載，在定義受力之後我們可以得知以下資訊:
**力平衡**
$$\sum F_z = 0$$

$$\sum M_x = 0$$

$$\sum M_y = 0$$

**輸入**
$$\sum Fz = \sum N - mg = 0$$

$$\sum Mx = \sum N_iy_i - ma_yh/d = 0$$

$$\sum My = \sum N_ix_i - ma_xh/L = 0$$
## 問題分析
很明顯從以上資訊我們可以發現這是個靜不定問題，假設我們不使用重心幾何分配希望可以更具有物理意義，就必須套用**最小作用量原理**。由此我們可以把輸入與平衡式寫成以下關係。

$$A = \left[ \begin{matrix} y_1&y_2&y_3&y_4\\\ x_1&x_2&x_3&x_4\\\ 1&1&1&1\end{matrix}\right]$$


$$b = \left[ \begin{matrix} ma_yh/d\\\ ma_yh/d\\\ mg\end{matrix}\right]$$

我們希望在滿足線性約束 $A N = b$ 的情況下，找到一個向量 $N$，使得它的範數平方 $\|N\|^2$ 最小，符合最小作用量。這是一個典型的「最小範數解」問題。


## 拉格朗日函數的設計
為了同時考慮目標函數與約束條件，我們引入拉格朗日乘子 $\lambda$，構造函數：
$$\mathcal{L}(N, \lambda) = N^T N + \lambda^T (b - A N)$$

其中：
- 第一項 $N^T N$：代表我們要最小化的範數平方，是純量。展開後就是 $\min(\sum N^2_i)$
- 第二項 $\lambda^T (b - A N)$：將約束 $A N = b$ 強制加入，用 $\lambda$ 進行約束的耦合分配。


## 對 $N$ 微分最佳化
對 $N$ 求偏導：
$$\frac{\partial \mathcal{L}}{\partial N} = 2N - A^T \lambda = 0$$

$$N = \tfrac{1}{2} A^T \lambda$$



## 對 $\lambda$ 微分去除影響
對 $\lambda$ 求偏導：
$$\frac{\partial \mathcal{L}}{\partial \lambda} = b - A N = 0$$

$$A N = b$$


## 代回過程
將 $N = \tfrac{1}{2} A^T \lambda$ 代入 $A N = b$：
$$A \left(\tfrac{1}{2} A^T \lambda \right) = b$$

$$\tfrac{1}{2} (A A^T) \lambda = b$$


## 解出 $\lambda$

$$\lambda = 2 (A A^T)^{-1} b$$


## 最終解
再代回 $N = \tfrac{1}{2} A^T \lambda$：

$$N = \tfrac{1}{2} A^T \lambda = \tfrac{1}{2} A^T ( 2 (A A^T)^{-1} b )$$

$$N = A^T (A A^T)^{-1} b$$
