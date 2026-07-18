# Magic Formula Fx
模型位置>> [Fx](../Fx_models.py)
## 純縱滑縱向力 $Fx0$
### 曲線偏移
- **水平偏移 (Shx)**  
  $$Shx = (PHX1 + PHX2 \cdot dfz) \cdot \lambda_{Hx}$$
  $$\kappa_x = \kappa + Shx$$
  **物理意義**：修正滑移比 (Slip Ratio)，考慮載荷變化造成的偏移。

- **垂直偏移 (Svx)**  
  $$Svx = F_z \cdot (PVX1 + PVX2 \cdot dfz) \cdot \lambda_{Vx} \cdot \lambda_{\mu_x'} \cdot \zeta_1$$
  **物理意義**：縱向力的偏移量，反映胎壓與載荷對縱向力的影響。

- **曲率 $E_x$**  
  $$E_x = (PEX1 + PEX2 \cdot dfz + PEX3 \cdot dfz^2) \cdot (1 - PEX4 \cdot \text{sign}(\kappa_x)) \cdot \lambda_{Ex}$$
  **物理意義**：曲率因子，控制縱向力曲線在高滑移比下的彎曲程度。
## 主要因子
- **形狀因子 $C_x$**  
  $$C_x = PCX1 \cdot \lambda_{Cx}$$
  **物理意義**：控制縱向力曲線的形狀。

- **剛性 $K_{xk}$**  
  $$K_{xk} = F_z \cdot (PKX1 + PKX2 \cdot dfz) \cdot e^{PKX3 \cdot dfz} \cdot (1 + PPX1 \cdot dpi + PPX2 \cdot dpi^2) \cdot \lambda_{Kxk}$$
  **物理意義**：縱向剛性，描述輪胎在小滑移比下的力增長速率。

- **摩擦係數 $\mu_x$**  
  $$\mu_x = (PDX1 + PDX2 \cdot dfz) \cdot (1 + PPX3 \cdot dpi + PPX4 \cdot dpi^2) \cdot (1 - PDX3 \cdot ia_{Mi}^2) \cdot \lambda_{\mu_xMi} \cdot \lambda_{Mi}$$
  **物理意義**：縱向摩擦係數，反映胎壓、載荷與傾角對摩擦的影響。

- **峰值力 $D_x$**  
  $$D_x = \mu_x \cdot F_z \cdot \zeta_2$$
  **物理意義**：縱向力的最大值，與摩擦係數及法向力成正比。

- **剛性因子 $B_x$**  
  $$B_x = \frac{K_{xk}}{C_x \cdot D_x + \epsilon_x}$$
  **物理意義**：決定曲線初始斜率，與剛性及峰值力相關。
### 主方程式
- **Magic Formula 主方程式**  
  $$Fx0 = D_x \cdot \sin \Big( C_x \cdot \arctan \big( B_x \cdot \kappa_x - E_x \cdot (B_x \cdot \kappa_x - \arctan(B_x \cdot \kappa_x)) \big) \Big) + Svx$$
  **物理意義**：完整的縱向力表達式，描述滑移比與縱向力的非線性關係。

---

## 混合工況縱向力 $Fx$

在混合工況下，縱向力會受到側偏角影響：

- **側偏角偏移**  
  $$SH_{xa} = RHX1$$
  $$\alpha_S = \alpha_{mi} + SH_{xa}$$
  **物理意義**：修正側偏角，考慮載荷與幾何偏移。

- **修正係數 $B_{xa}, C_{xa}, E_{xa}$**  
  $$B_{xa} = (RBX1 + RBX3 \cdot ia_{Mi}^2) \cdot \cos(\arctan(RBX2 \cdot \kappa)) \cdot \lambda_{xa}$$
  $$C_{xa} = RCX1$$
  $$E_{xa} = REX1 + REX2 \cdot dfz$$
  **物理意義**：控制縱向力隨側偏角變化的修正因子。

- **修正函數 $G_x$**  
  $$G_x(x) = \cos \Big( C_{xa} \cdot \arctan \big( B_{xa} \cdot x - E_{xa} \cdot (B_{xa} \cdot x - \arctan(B_{xa} \cdot x)) \big) \Big)$$
  **物理意義**：描述縱向力隨側偏角的衰減。

- **修正比值**  
  $$G_{x0} = G_x(SH_a)$$
  $$G_{xa} = \frac{G_x(\alpha_S)}{G_{x0}}$$
  **物理意義**：將修正函數歸一化，避免數值不穩定。

- **混合工況縱向力**  
  $$Fx = Fx0 \cdot G_{xa}$$
  **物理意義**：最終縱向力，考慮滑移比與側偏角的耦合效應。
