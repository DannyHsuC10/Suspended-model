# 線性回歸
* [檔案位置](../Linear_Regression.py)
線性回歸是一種統計方法，用來建立自變數與因變數之間的線性關係。在輪胎垂直剛度的物理模型中，線性回歸可用來解出垂直剛度 $k$ 與預先負載 $b$。

## 基本方程式

一般線性回歸模型：
$$R = k \cdot (R0 - RL) + b$$

若強制通過原點：
$$R = k \cdot (R0 - RL)$$

其中：
- $R$: 垂直力 (Vertical Force, FZ)
- $R0$: 自由半徑 (Free Radius)
- $RL$: 輪輞半徑 (Loaded Radius)
- $k$: 垂直剛度 (Vertical Stiffness)
- $b$: 預先負載 (Preload)

## 物理意義

- **垂直剛度 $k$**：代表輪胎在垂直方向上的抗壓縮能力，數值越大表示輪胎越硬。
- **預先負載 $b$**：即使沒有壓縮量，輪胎仍承受的初始力。
- **位移量 $\Delta = R0 - RL$**：表示輪胎因受力而產生的壓縮變形。

## 線性回歸過程

1. **建立設計矩陣**  
   將壓縮量 $x = R0 - RL$ 與垂直力 $y = |FZ|$ 建立矩陣：
   $$X = \begin{bmatrix} x & 1 \end{bmatrix}$$

2. **最小平方法 (Least Squares)**  
   解出參數向量：
   $$\beta = (X^T X)^{-1} X^T y$$
   其中 $\beta = \begin{bmatrix} k \\ b \end{bmatrix}$

3. **強制通過原點**  
   若不考慮截距 $b$，則剛度 $k$ 可由：
   $$k = \frac{\sum (x \cdot y)}{\sum (x^2)}$$

## 評估指標

- **決定係數 $R^2$**：衡量模型解釋資料的比例  
  $$R^2 = 1 - \frac{\sum (y - y_{pred})^2}{\sum (y - \bar{y})^2}$$

- **均方根誤差 (RMSE)**：衡量預測值與真實值的誤差  
  $$RMSE = \sqrt{\frac{1}{n} \sum (y - y_{pred})^2}$$
