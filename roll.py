# roll.py
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
g = 9.81
# ===========================(data)

t = 1.25 # 輪距
w = 1.462 # 寬度

l = 1.55 # 軸距
df = 0.96
k_tire =  122.5*1000 # 輪胎剛性 N/m
k_rolls = 594.6# NM/deg
k_heave_fs = 64.5*1000# N/m
k_heave_rs = 64.5*1000#56.5*1000# N/m
Cl = 2.4
rho = 1.225
A = 0.587


# ============================(計算)
# # 計算輪胎等效 roll 剛性

k_rollt = np.deg2rad(k_tire*t**2/2)# NM/deg
print("輪胎等效roll剛性: ",k_rollt)

k_roll = (k_rolls*k_rollt)/(k_rollt+k_rolls)# 計算彈簧串聯# NM/deg
print("總roll剛性: ",k_roll)

k_heave_f = (k_heave_fs*k_tire)/(k_heave_fs+k_tire)# 彈簧串聯# N/m
k_heave_r = (k_heave_rs*k_tire)/(k_heave_rs+k_tire)# 彈簧串聯# N/m
print("前heave剛性: ",k_heave_f)
print("後heave性: ",k_heave_r)

l_pcf = l*k_heave_r/(k_heave_r+k_heave_f)# pitch center >> fw
l_pcr = l*k_heave_f/(k_heave_f+k_heave_r)# pitch center >> rw
k_pitch = np.deg2rad((k_heave_f*l_pcf**2+k_heave_r*l_pcr**2))# NM/deg

C_air = 0.5*Cl*rho*A
# ===========================()
class car:# 車輛定義
    def __init__(self):
        """fl,fr,rl,rr"""
        self.h_roll = 0.024
        self.h_cg = 0.29
        self.m = 370
        self.CG_rate = np.array([0.48,0.52])
        self.k_roll = k_roll# NM/deg
        self.k_pitch = k_pitch# NM/deg
        self.P_ay = np.array([-w/2,w/2,0,0])
        self.P_ax = np.array([l_pcf+df,l_pcf+df,0,0])
        self.C_air = C_air#7.4
        self.k_heave_f = k_heave_f
        self.k_heave_r = k_heave_r
        self.COP = np.array([0.4,0.6])
        self.h_fw = 54.5

LP2 = car()

def roll_angle(a,car):# roll 角度與加速度關係
    M = car.m*a*car.h_cg*car.CG_rate
    theta = -M*(car.h_cg-car.h_roll)/car.h_cg/car.k_roll
    #print("roll: ",theta)
    return theta

def pitch_angle(a,car):# pitch 角度與加速度關係
    M = car.m*a*car.h_cg
    
    theta= -M*(car.h_cg-car.h_roll)/car.h_cg/car.k_pitch
    
    #print("pitch: ",theta)
    return theta

def attitude_dh(ax,ay,car):
    theta_roll_deg = roll_angle(ay,car)
    theta_pitch_deg = pitch_angle(ax,car)
    theta_pitch = np.deg2rad(theta_pitch_deg)
    theta_roll = np.deg2rad(theta_roll_deg)
    dh_roll = [theta_roll[0]*car.P_ay[0],theta_roll[0]*car.P_ay[1],
                theta_roll[1]*car.P_ay[2],theta_roll[1]*car.P_ay[3]]
    dh_pitch = theta_pitch*car.P_ax

    dh = (dh_pitch+dh_roll)*1000

    return dh,theta_pitch_deg,theta_roll_deg

def aero_dh(v,car):

    F = car.C_air*v**2
    dhf = F*car.COP[0]/car.k_heave_f
    dhr = F*car.COP[1]/car.k_heave_r
    dh = np.array([dhf,dhf,dhr,dhr])*1000
    return dh

def aero_data(v,ax,ay,car):
    dhv = aero_dh(v,car)
    dha,theta_pitch_deg,theta_roll_deg = attitude_dh(ax,ay,LP2)
    h = (car.h_fw-dha-dhv)
    hf = np.array((h[0],h[1]))
    return hf,theta_pitch_deg,theta_roll_deg

#print(LP2.C_air*15**2)


print("="*40)
hf,theta_pitch_deg,theta_roll_deg = aero_data(15,-1.45*g,0*g,LP2)
print("hf",hf)
print("pitch",theta_pitch_deg)
print("roll",theta_roll_deg)


# ==========================================
# 1. 數據掃描與準備 (網格化掃描)
# ==========================================
# 建立 加速度 陣列
ay_range = np.linspace(-1.6 * g, 1.6 * g, 50)
ax_range = np.linspace(-1.6 * g, 1.2 * g, 50)

# 用於 3D 圖與多變數儲存的矩陣 (Meshgrid)
AY, AX = np.meshgrid(ay_range, ax_range)
HF_LEFT = np.zeros_like(AY)
HF_RIGHT = np.zeros_like(AY)
PITCH_MAP = np.zeros_like(AY)
ROLL_MAP_L = np.zeros_like(AY) # 前左 Roll 角度

# 預設固定速度 V = 15 m/s 進行 ax, ay 掃描
V_fixed = 0.0

for i in range(len(ax_range)):
    for j in range(len(ay_range)):
        hf, p_deg, r_deg = aero_data(V_fixed, AX[i,j], AY[i,j], LP2)
        HF_LEFT[i,j] = hf[0]
        HF_RIGHT[i,j] = hf[1]
        PITCH_MAP[i,j] = p_deg
        ROLL_MAP_L[i,j] = r_deg[0]

# 另外準備速度掃描數據 (假設 ax=0, ay=0)
v_range = np.linspace(0, 30, 50) # 速度從 0 到 40 m/s
hf_v_list = []
for v in v_range:
    hf, _, _ = aero_data(v, 0, 0, LP2)
    hf_v_list.append(hf[0]) # 沒側傾時左右對稱，取左輪即可

# ==========================================
# 2. 開始繪圖
# ==========================================

# --- 圖一：Roll vs ay (2D) 與 Pitch vs ax (2D) ---
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 側傾角與側向加速度關係 (取 ax=0 的切面比較直觀)
ay_g = ay_range / g
# roll_angle 回傳一組長度2的陣列，取左側 [0] 繪製
roll_v_ay = [roll_angle(ay, LP2)[0] for ay in ay_range]
ax1.plot(ay_g, roll_v_ay, color='blue', linewidth=2)
ax1.set_title('Roll vs ay')
ax1.set_xlabel(' ay (g)')
ax1.set_ylabel('Roll  (deg)')
ax1.grid(True)

# 俯仰角與縱向加速度關係
ax_g = ax_range / g
pitch_v_ax = [pitch_angle(ax, LP2) for ax in ax_range]
ax2.plot(ax_g, pitch_v_ax, color='red', linewidth=2)
ax2.set_title('Pitch vs ax')
ax2.set_xlabel(' ax (g)')
ax2.set_ylabel('Pitch (deg)')
ax2.grid(True)

plt.tight_layout()

# --- 圖二：ax, ay 與 前翼離地高度 (hf) 的 3D 關係圖 ---
fig2 = plt.figure(figsize=(10, 8))
ax3d = fig2.add_subplot(111, projection='3d')

# 1. 繪製原本的前左翼高度 Aero Map 曲面
surf = ax3d.plot_surface(AY/g, AX/g, HF_LEFT, cmap='viridis', edgecolor='none', alpha=0.8, zorder=2)

# 2. 建立並繪製 z = 0 的平面
Z_zero = np.zeros_like(AY) 
zero_plane = ax3d.plot_surface(AY/g, AX/g, Z_zero, color='red', alpha=0.15, edgecolor='gray', linewidth=0.3, zorder=1)
# 註：稍微調低了 alpha (0.15)，好讓焦點集中在相交線上

# 3. 【新增】繪製面相交的 z = 0 線 (透過 contour 等高線功能)
# levels=[0] 代表只抓取高度為 0 的那條線，zdir='z' 代表投影在 z 軸方向，offset=0 固定線的 3D 高度在 0
contour_line = ax3d.contour(AY/g, AX/g, HF_LEFT, levels=[0], colors='red', linewidths=3, zdir='z', offset=0, zorder=3)
# 註：這裡用 colors='red' 且 linewidths=3 讓這條相交的「觸底邊界」非常醒目

ax3d.set_title(f'front wing (left side h) Map (constant speed = {V_fixed} m/s)')
ax3d.set_xlabel('ay (g)')
ax3d.set_ylabel('ax (g)')
ax3d.set_zlabel(' hf (mm)')

# 設定 z 軸顯示範圍，確保能看到 0 平面與相交線
current_zmin, current_zmax = ax3d.get_zlim()
ax3d.set_zlim(min(-5, current_zmin), current_zmax)

fig2.colorbar(surf, ax=ax3d, shrink=0.5, aspect=5, label='h (mm)')

# --- 圖三：速度與前翼離地高度關係 (2D) ---
fig3, ax3 = plt.subplots(figsize=(7, 5))
ax3.plot(v_range, hf_v_list, color='green', linewidth=2)
ax3.set_title('down force vs front wing (h) (ax=0, ay=0)')
ax3.set_xlabel('v (m/s)')
ax3.set_ylabel('hf (mm)')
ax3.grid(True)

# 顯示所有圖表
plt.show()

# ==========================================
# 3. 數據導出為 CSV 檔案
# ==========================================
import pandas as pd

# 1. 匯出 ay_roll.csv (側向加速度與 Roll 角度關係，以單位 g 儲存)
df_ay_roll = pd.DataFrame({
    'ay_(g)': ay_g,
    'roll_(deg)': roll_v_ay
})
df_ay_roll.to_csv('ay_roll.csv', index=False)
print("已成功匯出：ay_roll.csv")


# 2. 匯出 ax_pitch.csv (縱向加速度與 Pitch 角度關係，以單位 g 儲存)
df_ax_pitch = pd.DataFrame({
    'ax_(g)': ax_g,
    'pitch_(deg)': pitch_v_ax
})
df_ax_pitch.to_csv('ax_pitch.csv', index=False)
print("已成功匯出：ax_pitch.csv")


# 3. 匯出 hf_v.csv (純速度變化下，前翼高度關係)
df_hf_v = pd.DataFrame({
    'v_(m/s)': v_range,
    'hf_(mm)': hf_v_list
})
df_hf_v.to_csv('hf_v.csv', index=False)
print("已成功匯出：hf_v.csv")


# 4. 匯出 ay_ax_hf.csv (3D Aero Map 數據攤平，包含前後左右輪的高度與車身姿態)
# 將 2D 網格資料（50x50）攤平成一維陣列（2500筆資料），方便在 Excel 裡做篩選或畫圖
df_3d_map = pd.DataFrame({
    'ay_(g)': (AY / g).flatten(),
    'ax_(g)': (AX / g).flatten(),
    'hf_left_(mm)': HF_LEFT.flatten(),
    'hf_right_(mm)': HF_RIGHT.flatten(),
    'pitch_(deg)': PITCH_MAP.flatten(),
    'roll_left_(deg)': ROLL_MAP_L.flatten()
})
df_3d_map.to_csv('ay_ax_hf.csv', index=False)
print("已成功匯出：ay_ax_hf.csv")