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
## 其他分析
以下是其他的簡單分析工具
1. [解法比較](/wheel_load_tools/solution_comparison.m)
1. [共同null space](/wheel_load_tools/null_space.md)
1. [4輪附載平面](Load_changes.m)
1. [4輪負載平面 整合](Load_changes_all.m)
