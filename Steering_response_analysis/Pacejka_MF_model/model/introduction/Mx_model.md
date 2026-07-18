# Magic Formula Mx

模型位置>> [Mx](../Mx_models.py)

預先計算輸入力量 : [Fy](Fy_model.md)
## 基本轉換
- **橫向力比值**  
  $$F_{y_{ratio}} = \frac{F_y}{F_{z0}' + \epsilon}$$
  **物理意義**：將橫向力標準化，消除載荷大小的影響，方便比較不同工況下的力矩表現。

- **法向力比值**  
  $$F_{z_{ratio}} = \frac{F_z}{F_{z0}' + \epsilon}$$
  **物理意義**：將法向力標準化，反映輪胎受力相對於基準載荷的比例。

---

## 翻轉力矩方程式

- **第一項 $Q_1$**  
  $$Q_1 = QSX1 \cdot \lambda_{VMX} - QSX2 \cdot \iota_a \cdot (1 + PPMX1 \cdot dpi)$$
  **物理意義**：基準項與傾角修正，描述 camber 對翻轉力矩的影響。

- **第二項 $Q_2$**  
  $$Q_2 = QSX3 \cdot F_{y_{ratio}} + QSX4 \cdot \cos(QSX5 \cdot \arctan(QSX6 \cdot F_{z_{ratio}})^2)$$
  **物理意義**：橫向力比值與法向力比值的耦合效應，反映載荷與橫向力共同作用下的翻轉力矩。

- **第三項 $Q_3$**  
  $$Q_3 = QSX7 \cdot \iota_a + QSX8 \cdot \arctan(QSX9 \cdot F_{y_{ratio}})$$
  **物理意義**：傾角與橫向力比值的組合修正，描述 camber 與橫向力交互作用對翻轉力矩的影響。

- **第四項 $Q_4$**  
  $$Q_4 = QSX10 \cdot \arctan(QSX11 \cdot F_{z_{ratio}}) \cdot \iota_a$$
  **物理意義**：法向力比值與傾角的耦合效應，反映載荷與 camber 對翻轉力矩的共同影響。

- **合成項 $Q$**  
  $$Q = Q_1 + Q_2 \cdot \sin(Q_3) + Q_4$$
  **物理意義**：綜合各項修正後的翻轉力矩係數，包含基準、橫向力、法向力與傾角的影響。

- **最終翻轉力矩**  
  $$M_x = R_o \cdot F_z \cdot Q \cdot \lambda_{MX}$$
  **物理意義**：翻轉力矩，與接地半徑 $R_o$、法向力 $F_z$ 及修正係數 $Q$ 成正比，描述輪胎在受力下產生的翻轉效應。
