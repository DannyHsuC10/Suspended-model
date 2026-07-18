# Magic Formula 基類
模型位置>> [common](../_common.py)
## 歸一化法向力 `_normalize_load`

- **公式**  
  $$F_{z0}' = LFZO \cdot FNOMIN$$
  $$dfz = \frac{F_z - F_{z0}'}{F_{z0}' + \epsilon}$$

- **物理意義**  
  - $F_{z0}'$：基準法向力，通常取名義載荷 (Nominal Load)，作為比較基準。  
  - $dfz$：載荷偏差，描述實際法向力相對於基準載荷的偏移量。這能讓模型在不同載荷下保持一致性。

---

## 歸一化胎壓 `_normalize_pressure`

- **公式**  
  $$dpi = \frac{p - PIO}{PIO}$$
  $$dpi^2 = dpi^2$$

- **物理意義**  
  - $dpi$：胎壓偏差，描述實際胎壓相對於基準胎壓 $PIO$ 的變化比例。  
  - $dpi^2$：平方項，用來捕捉胎壓偏差的非線性影響。這能反映胎壓對剛性與摩擦的二次效應。

---

## 歸一化角度 `_normalize_angles`

- **公式**  
  $$SA_{rad} = \text{radians}(SA)$$
  $$IA_{rad} = \text{radians}(IA)$$
  $$a_{mi} = \tan(SA_{rad})$$
  $$ia_{Mi} = \sin(IA_{rad})$$
  $$ia_{Mi}^2 = (\sin(IA_{rad}))^2$$

- **物理意義**  
  - $a_{mi}$：側偏角的正切值，用來描述滑移角對橫向力的影響。  
  - $ia_{Mi}$：傾角 (camber) 的正弦值，反映輪胎傾斜對力矩與橫向力的影響。  
  - $ia_{Mi}^2$：平方項，用來捕捉 camber 的非線性效應。  
