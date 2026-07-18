# Magic Formula Fy
模型位置>> [Fy](../Fy_models.py)
## 純側滑橫向力 $Fy0$
### 摩擦與剛性
- **摩擦係數 $\mu_y$ (4.E23)**  
  $$\mu_y = (PDY1 + PDY2 \cdot dfz) \cdot (1 + PPY3 \cdot dpi + PPY4 \cdot dpi^2) \cdot (1 - PDY3 \cdot \sin^2 \gamma) \cdot \lambda_{\mu_yMi}$$
  **物理意義**：橫向摩擦係數，決定輪胎在側偏角下能產生的最大橫向力，受載荷、胎壓與傾角影響。

- **剛性 $K_{y\alpha}$ (4.E25)**  
  $$K_{y\alpha} = PKY1 \cdot F_{z0}' \cdot (1 + PPY1 \cdot dpi) \cdot (1 - PKY3 \cdot |\sin \gamma|) \cdot \sin(PKY4 \cdot \arctan(term)) \cdot \lambda_{Kyia} \cdot \zeta_3$$
  其中  
  $$term = \frac{F_z / F_{z0}'}{(PKY2 + PKY5 \cdot \sin^2 \gamma) \cdot (1 + PPY2 \cdot dpi)}$$
  **物理意義**：橫向剛性，描述小側偏角下橫向力的增長速率。

- **傾角剛性 $K_{y\gamma0}$ (4.E30)**  
  $$K_{y\gamma0} = F_z \cdot (PKY6 + PKY7 \cdot dfz) \cdot (1 + PPY5 \cdot dpi) \cdot \lambda_{Kyia}$$
  **物理意義**：傾角剛性，描述 camber 對橫向力的影響。
### 曲線偏移
- **垂直偏移 $Sv_{\gamma\alpha}$ (4.E28)**  
  $$Sv_{\gamma\alpha} = F_z \cdot (PVY3 + PVY4 \cdot dfz) \cdot \sin \gamma \cdot \lambda_{Kyia} \cdot \lambda_{\mu_y'} \cdot \zeta_2$$
  **物理意義**：由傾角 (camber) 引起的橫向力偏移。

- **水平偏移 $Shy$ (4.E27)**  
  $$Shy = (PHY1 + PHY2 \cdot dfz) \cdot \lambda_{Hy} + \frac{(K_{y\gamma0} \cdot \sin \gamma - Sv_{\gamma\alpha}) \cdot \zeta_0}{K_{y\alpha} + \epsilon_y} + \zeta_4 - 1$$
  **物理意義**：修正側偏角的偏移量，考慮載荷與傾角效應。

- **修正側偏角 $a_y$ (4.E20)**  
  $$a_y = \alpha^* + Shy$$
  **物理意義**：實際作用的側偏角，包含偏移修正。

- **垂直偏移 $Svy$ (4.E29)**  
  $$Svy = F_z \cdot (PVY1 + PVY2 \cdot dfz) \cdot \lambda_{Vy} \cdot \lambda_{\mu_y'} \cdot \zeta_2 + Sv_{\gamma\alpha}$$
  **物理意義**：橫向力的偏移量，反映 camber 與載荷影響。
### 主要因子
- **形狀因子 $C_y$ (4.E21)**  
  $$C_y = PCY1 \cdot \lambda_{Cy}$$
  **物理意義**：控制橫向力曲線的形狀。

- **曲率 $E_y$ (4.E24)**  
  $$E_y = (PEY1 + PEY2 \cdot dfz) \cdot (1 + PEY4 \cdot \sin^2 \gamma - (PEY3 + PEY5 \cdot \sin \gamma) \cdot \text{sign}(a_y)) \cdot \lambda_{Ey}$$
  **物理意義**：曲率因子，控制橫向力曲線在大側偏角下的彎曲程度。

- **峰值力 $D_y$ (4.E22)**  
  $$D_y = \mu_y \cdot F_z \cdot \zeta_2$$
  **物理意義**：橫向力的最大值，與摩擦係數及法向力成正比。

- **剛性因子 $B_y$ (4.E26)**  
  $$B_y = \frac{K_{y\alpha}}{C_y \cdot D_y + \epsilon_y}$$
  **物理意義**：決定曲線初始斜率，與剛性及峰值力相關。
### 主方程式
- **Magic Formula 主方程式 (4.E19)**  
  $$Fy0 = D_y \cdot \sin \Big( C_y \cdot \arctan(B_y \cdot a_y - E_y \cdot (B_y \cdot a_y - \arctan(B_y \cdot a_y))) \Big) + Svy$$
  **物理意義**：完整的橫向力表達式，描述側偏角與橫向力的非線性關係。

---

## 混合工況橫向力 $Fy$

在混合工況下，側向力會受到縱向滑移影響：
### 縮放係數
- **水平偏移 $SH_\kappa$ (4.E64)**  
  $$SH_\kappa = RHY1 + RHY2 \cdot dfz$$
  $$\kappa_S = SL + SH_\kappa$$
  **物理意義**：修正縱滑比，考慮載荷影響。

- **剛性因子 $B_{y\kappa}$ (4.E63)**  
  $$B_{y\kappa} = (RBY1 + RBY4 \cdot \sin^2 \gamma) \cdot \cos(\arctan(RBY2 \cdot (\alpha^* - RBY3))) \cdot \lambda_{Yk}$$
  **物理意義**：縱滑與側偏角耦合下的剛性修正。

- **形狀因子 $C_{y\kappa}$ (4.E65)**  
  $$C_{y\kappa} = RCY1$$
  **物理意義**：控制混合工況下橫向力曲線的形狀。

- **曲率 $E_{y\kappa}$ (4.E65)**  
  $$E_{y\kappa} = REY1 + REY2 \cdot dfz$$
  **物理意義**：控制混合工況下橫向力曲線的彎曲程度。

- **修正函數 $G_{y\kappa}$**  
  $$G_{y\kappa}(x) = \cos \Big( C_{y\kappa} \cdot \arctan(B_{y\kappa} \cdot x - E_{y\kappa} \cdot (B_{y\kappa} \cdot x - \arctan(B_{y\kappa} \cdot x))) \Big)$$
  $$G_{y\kappa0} = G_{y\kappa}(SH_\kappa)$$
  $$G_{y\kappa} = \frac{G_{y\kappa}(\kappa_S)}{G_{y\kappa0} + \epsilon_y}$$
  **物理意義**：描述縱滑比對橫向力的衰減影響。
### 偏移項
- **摩擦係數 $\mu_y$ (for DVκ)**  
  $$\mu_y = (PDY1 + PDY2 \cdot dfz) \cdot (1 + PPY3 \cdot dpi + PPY4 \cdot dpi^2) \cdot (1 - PDY3 \cdot \sin^2 \gamma) \cdot \lambda_{\mu_y}$$
  
  **物理意義**：混合工況下的橫向摩擦係數。

- **修正峰值 $DV_\kappa$ (4.E66)**  
  $$D_{V\kappa} = \mu_y \cdot F_z \cdot (RVY1 + RVY2 \cdot dfz + RVY3 \cdot \sin \gamma) \cdot \cos(RVY4 \cdot \alpha^*)$$
  **物理意義**：縱滑與側偏角耦合下的峰值修正。

- **偏移 $SV_\kappa$ (4.E67)**  
  $$S_{V\kappa }=D_{V\kappa }\cdot \sin (RVY5\cdot \arctan (RVY6\cdot SL))\cdot \lambda_{Vyk}$$

  **物理意義**：縱滑引起的橫向力偏移，反映 slip ratio 對橫向力的附加影響。
### 混合工況力
- **混合工況橫向力**  
  $$Fy = Fy0 \cdot G_{y\kappa} + SV_\kappa$$
  **物理意義**：最終橫向力，綜合了純側滑橫向力、縱滑修正以及偏移效應，描述縱滑與側偏角耦合下的橫向力行為。

