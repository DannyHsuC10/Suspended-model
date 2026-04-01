# Four wheel load
## [計算函式](wheel_load_tools/tools.md)
1. 最小作用量原理求解>>[分析力學操作解釋](wheel_load_tools/Solve.md)
2. 重心分配求解
使用範例
``` matlab
% 車輛參數

car.m = 309.5; 
g = 9.81; 
car.h = 0.284; 
car.L = 1.55; 
car.d = 1.25;
car.ax = 0.3*g; 
car.ay = 1.5*g;

% 重心
car.CG_x = [0.48; 0.52];  % 前/後軸分布
car.CG_y = [0.5, 0.5];  % 左/右輪分布

% 空力
car.CF_rela = [0.0;0.0;0.0];  % 相對於重心(x,y,z)m
car.F_add = [0,0,0];%(x,y,z)N

% 求解
N = Four_wheel_load_LSM(car,true);% false
N = Four_wheel_load(car,true);% false

```
## 其他工具
以下是其他的簡單分析工具
1. [解法比較](/wheel_load_tools/solution_comparison.m)
1. [共同null space](/wheel_load_tools/null_space.md)
1. [4輪附載平面](Load_changes.m)
1. [4輪負載平面 整合](Load_changes_all.m)
1. [python模型](Four_wheel_load.py)

## 改進方向
在四輪載重靜不定問題中，使用最小範數解（LSM）與拉格朗日乘數法，本質上是在求解同一個帶約束的最佳化問題，因此數學上等價。

然而，該最小化目標（NᵀN）並不是真正的作用量，而是透過虛功原理隱含假設各輪胎剛性相同的能量最小化模型。但更好的方法是用拉格朗日法假設懸吊剛性($K$)，也就是 $\min(\frac12N^TK^{-1}N)$，所以程式中要加入剛性矩陣如下

```matlab
K = diag([k_FL, k_FR, k_RL, k_RR])
```
最後應該要解成這樣
$$N = KA^T (AK A^T)^{-1} (-b)$$