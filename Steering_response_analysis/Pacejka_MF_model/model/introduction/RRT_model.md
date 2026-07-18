# Magic Formula 模型計算說明 (滾動阻力矩 $RRT$)
模型位置>> [RRT](../RRT_models.py)

預先計算輸入力量 : [Fx](Fx_model.md)
## MF 模型

- **滾動阻力係數 $f_{rr}$**  
  $$
  f_{rr} = QSY1
  + QSY2 \cdot \frac{F_x}{F_{z0}' + \epsilon}
  + QSY3 \cdot V
  + QSY4 \cdot V^4
  + QSY5 \cdot \gamma^2
  + QSY6 \cdot \gamma^2 \cdot \frac{F_z}{F_{z0}' + \epsilon}
  $$
  **物理意義**：滾動阻力係數，綜合考慮縱向力、車速、傾角與載荷的影響。它描述了輪胎在滾動過程中因變形與摩擦而產生的能量損耗。

- **修正項**  
  $$f_{rr} \leftarrow f_{rr} \cdot (1 + QSY7 \cdot dfz + QSY8 \cdot dpi)$$
  **物理意義**：修正滾動阻力係數，考慮載荷變化 ($dfz$) 與胎壓偏差 ($dpi$) 的影響。

- **滾動阻力矩**  
  $$PPT = -R_o \cdot F_z \cdot f_{rr}$$
  **物理意義**：最終的滾動阻力矩，與接地半徑 $R_o$、法向力 $F_z$ 以及滾動阻力係數成正比。負號表示阻力方向與車輛前進方向相反。

---

## SAE 模型

- **各項計算**  
  $$R1 = \frac{K'}{c1}, \quad R2 = c2$$
  $$R3 = \frac{c3 + c4 \cdot F_z}{p}, \quad R4 = \frac{c5 + c6 \cdot F_z}{p} \cdot v^2$$
  **物理意義**：這些項目分別代表不同的滾動阻力來源：  
  - $R1$：基準比例因子  
  - $R2$：常數項  
  - $R3$：與載荷及胎壓相關的阻力  
  - $R4$：與速度平方相關的阻力（波動與滾動波動的耦合效應）

- **滾動阻力係數**  
  $$C_{rr} = R1 \cdot (R2 + R3 + R4)$$
  **物理意義**：綜合各項影響後的滾動阻力係數。

- **滾動阻力**  
  $$F_r = C_{rr} \cdot F_z$$
  **物理意義**：最終的滾動阻力，與法向力成正比，反映輪胎在滾動過程中消耗的能量。