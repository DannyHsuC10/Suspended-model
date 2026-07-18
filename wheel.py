# 車輪輸出工具
from Pacejka_MF_model.model import api as tire
import numpy as np
import matplotlib.pyplot as plt
g = 9.81

def slip_angle(delta, vx, vy, omega_yaw, l,out = "d"): # 滑移角
    """
    delta: 前輪轉角
    vx: 車輛前進速度
    vy: 車輛側向速度
    omega_yaw: 車輛偏航角速度
    l: 車輛重心到軸距
    """
    # array運算
    delta = np.array(delta)
    l = np.array(l)

    alpha = delta - np.arctan((vy + l * omega_yaw) / vx)
    if out == "d":
        return np.degrees(alpha)
    elif out == "r":
        return alpha
    else:
        print("slip_angle out wrong")
        return 0

def slip_ratio(vx,omega,r_w): # 滑移率
    """
    vx: 車輛前進速度
    omega: 車輪角速度
    r_w: 車輪半徑
    """
    # array運算
    omega = np.array(omega)
    r_w = np.array(r_w)
    
    kappa = (vx- omega*r_w)/(max(vx,1e-3))
    return kappa

def Four_wheel_output(FZ_list, SA_list, SL_list, tir_params, IA_list = None, P_list = None, V_list = None, Ro_list = None, check = False, sumdata=False):# 四輪輸出
    """
    輸入:
        FZ_list : 四輪的垂直載荷 [fl, fr, rl, rr]
        SA_list : 四輪的側滑角 [fl, fr, rl, rr]
        SL_list : 四輪的縱向滑移 [fl, fr, rl, rr]
        IA_list : 四輪的傾斜角 [fl, fr, rl, rr] (可選)
        P_list  : 四輪的胎壓 [fl, fr, rl, rr] (可選)
        V_list  : 四輪的速度 [fl, fr, rl, rr] (可選)
        Ro_list : 四輪的未載荷半徑 [fl, fr, rl, rr] (可選)
        tire_params : 輪胎參數物件
        check : 是否輸出中間結果 (預設 False)
    輸出:
        Fx, Fy, Mx, Mz, RRT : 四輪的力矩
    """
    #SA_list[1] = -SA_list[1] # 右輪轉角與左輪相反
    #SA_list[3] = -SA_list[3] # 右輪轉角與左輪相反
    SA_list[0] = -SA_list[0] # 右輪轉角與左輪相反
    SA_list[2] = -SA_list[2] # 右輪轉角與左輪相反
    MF = tire.CalculationInput( # 建立MF物件函數
                FZ=FZ_list,
                SA=SA_list,
                SL=SL_list,     
                IA=IA_list,
                pressure=P_list,
                V = V_list,# 特殊項
                Ro = Ro_list,# 特殊項
                tir_params=tir_params
            )

    Fx = tire.MF_Universal_solver("FX", MF) # 同向
    Fy = tire.MF_Universal_solver("FY", MF)
    Fz = np.array(FZ_list) # 同向
    Mx = tire.MF_Universal_solver("MX", MF)
    Mz = tire.MF_Universal_solver("MZ", MF)
    RRT = tire.MF_Universal_solver("RRT", MF) # 同向

    Fy = np.array([Fy[0],-Fy[1],Fy[2],-Fy[3]]) # 統一坐標系方向
    Mz = np.array([Mz[0],-Mz[1],Mz[2],-Mz[3]]) # 統一坐標系方向
    Mx = np.array([-Mx[0],Mx[1],-Mx[2],Mx[3]]) # 統一坐標系方向
    
    sum_Fx = np.sum(Fx)
    sum_Fy = np.sum(Fy)
    if check:
         print("Fx",Fx)
         print("Fy",Fy)
         print("Fz",Fz)
         print("Mz",Mz)
         print("Mx",Mx)
         print("RRT",RRT)
    if sumdata:
        return Fx, Fy, Fz, Mx, RRT, Mz ,sum_Fx, sum_Fy
    else:
        return Fx, Fy, Fz, Mx, RRT, Mz

def plot_vehicle_friction_circle(Fz_per_tire=800, alpha_lim=10, kappa_lim=1, resolution=25):
    """
    繪製四輪總合力的摩擦圓圖形 (包含 2D 軌跡、3D 曲面，以及獨立的極限邊界外框)
    """
    m = Fz_per_tire*4# 車重
    # 1. 定義滑移角與滑移率的掃描區間
    alpha_range = np.linspace(-alpha_lim, alpha_lim, resolution)
    kappa_range = np.linspace(-kappa_lim, kappa_lim, resolution)
    
    # 建立 2D 網格
    ALPHA, KAPPA = np.meshgrid(alpha_range, kappa_range)
    
    # 初始化總合力矩陣
    Total_Fx = np.zeros_like(ALPHA)
    Total_Fy = np.zeros_like(ALPHA)
    
    print("正在計算摩擦圓網格點，請稍候...")
    
    # 2. 雙重迴圈掃描
    for i in range(ALPHA.shape[0]):
        for j in range(ALPHA.shape[1]):
            current_alpha = ALPHA[i, j]
            current_kappa = KAPPA[i, j]
            
            SA_list = [current_alpha] * 4
            SL_list = [current_kappa] * 4
            FZ_list = [Fz_per_tire] * 4
            
            _, _, _, _, _, _, sum_Fx, sum_Fy = Four_wheel_output(
                FZ_list, SA_list, SL_list, tir_params, check=False, sumdata=True
            )
            
            Total_Fx[i, j] = sum_Fx
            Total_Fy[i, j] = sum_Fy

    print("計算完成，開始繪圖...")

    # 3. 開始繪圖 (修改為 1 列 3 子圖，寬度調大到 22)
    fig = plt.figure(figsize=(22, 6))
    ax1 = fig.add_subplot(131)
    ax2 = fig.add_subplot(132, projection='3d')
    ax3 = fig.add_subplot(133) # 新增的極限邊界框子圖
    
    # ----------------------------------------------------
    # 圖一：標準 2D 摩擦圓軌跡圖
    # ----------------------------------------------------
    # 繪製不同滑移率(Kappa)下的 Fx-Fy 曲線

    for i in range(0, resolution, max(1, resolution//8)):

        ax1.plot(Total_Fx[i, :], Total_Fy[i, :], label=f'$\\kappa$={KAPPA[i, 0]:.2f}', alpha=0.7)

    # 繪製不同滑移角(Alpha)下的 Fx-Fy 曲線

    for j in range(0, resolution, max(1, resolution//8)):

        ax1.plot(Total_Fx[:, j], Total_Fy[:, j], 'k--', alpha=0.3)
        
    ax1.set_xlabel('Total Longitudinal Force $F_x$ [N]', fontsize=11)
    ax1.set_ylabel('Total Lateral Force $F_y$ [N]', fontsize=11)
    ax1.set_title('2D Friction Circle Paths', fontsize=13)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.axis('equal')
    ax1.legend(loc='upper right', fontsize=8)
    
    # ----------------------------------------------------
    # 圖二：3D 著色曲面圖
    # ----------------------------------------------------
    surf = ax2.plot_surface(Total_Fx, Total_Fy, KAPPA, cmap='plasma', edgecolor='none', alpha=0.8)
    ax2.set_xlabel('$F_x$ [N]')
    ax2.set_ylabel('$F_y$ [N]')
    ax2.set_zlabel('Slip Ratio $\\kappa$')
    ax2.set_title('3D Friction Surface', fontsize=13)
    fig.colorbar(surf, ax=ax2, shrink=0.5, aspect=5, label='Lateral Force $F_y$ [N]')
    
    # ----------------------------------------------------
    # 🔥 圖三：修正後的 2D 極限邊界框 (使用 Convex Hull 尋找真實極限)
    # ----------------------------------------------------
    from scipy.spatial import ConvexHull

    # 1. 把 2D 網格產生的所有 Fx 和 Fy 攤平，組合成 (N, 2) 的二維點雲，然後轉換成加速度
    points = np.column_stack((Total_Fx.ravel(), Total_Fy.ravel()))/m
    
    # 2. 計算這群力的凸包 (自動尋找最外圍的真實極限邊界點)
    hull = ConvexHull(points)
    
    # 3. 提取凸包的頂點，並加上起點使其閉合
    hull_vertices = hull.vertices
    hull_vertices_closed = np.append(hull_vertices, hull_vertices[0])
    
    # 得到邊界框的 X 和 Y 座標
    edge_x = points[hull_vertices_closed, 0]
    edge_y = points[hull_vertices_closed, 1]
    
    # 4. 繪製真實的極限外框 (紅色粗實線)
    ax3.plot(edge_x, edge_y, 'r-', linewidth=2.5, label='True Friction Limit Envelope')
    
    # 5. 淡淡的紅色透明填充內部，突顯車輛極限極限區域
    ax3.fill(edge_x, edge_y, 'r', alpha=0.08)
    
    # 順便把所有計算點以極淡的灰色點點點畫出來，方便你檢查邊界是否完美貼合
    ax3.scatter(points[:, 0], points[:, 1], s=1, color='gray', alpha=0.3, label='Calculated Points')
    
    ax3.set_xlabel('Total Longitudinal accele $a_x$ [N]', fontsize=11)
    ax3.set_ylabel('Total Lateral accele $a_y$ [N]', fontsize=11)
    ax3.set_title(f'Vehicle Friction Limit Box\n(Total Fz = {Fz_per_tire*4} N)', fontsize=13)
    ax3.grid(True, linestyle=':', alpha=0.6)
    ax3.axis('equal')
    ax3.legend(loc='upper right', fontsize=9)

    plt.tight_layout()

    print("最大加速力: ",max(edge_x*m))
    print("最大側向力: ",max(edge_y*m))
    m = Fz_per_tire*4
    print("最大加速度 (x): ",max(edge_x))
    print("最大加速度 (y): ",max(edge_y))

    plt.show()

if __name__ == "__main__":
    """
    # 參數設定
    tir_params = tire.load_tir("D2704_mf612.tir") # 載入tir參數檔案
    SA_test = 5
    #SA : \\
    #Fy : <<
    SA_test = -5
    #SA : // 
    #Fy : >>
    # fl, fr, rl, rr

    SA_list = [SA_fl,SA_fr,SA_rl,SA_rr]= [SA_test]*4
    SL_list = [SL_fl,SL_fr,SL_rl,SL_rr] = [0.01]*4 # 同向
    FZ_list = [FZ_fl,FZ_fr,FZ_rl,FZ_rr] = [800]*4 # 同向

    Fx, Fy, Fz, Mx, RRT, Mz  = Four_wheel_output(FZ_list, SA_list, SL_list, tir_params, check=True)
    """
    tir_params = tire.load_tir("D2704_mf612.tir")
    #tir_params = tire.load_tir("FSAE_43075R20.tir")


    # 掃描滑移角 (deg)
    SA_sweep = np.linspace(-10, 10, 100)

    

    # 儲存結果
    Fx_total = []
    Fy_total = []
    Fz_total = []

    Mx_total = []
    Mz_total = []
    RRT_total = []

    for SA in SA_sweep:
        SA_list = [SA]*4
        SL_list = [0.05]*4
        FZ_list = [785]*4
        V_list = [10]*4
        Fx, Fy, Fz, Mx, RRT, Mz = Four_wheel_output(
            FZ_list, SA_list, SL_list, tir_params, check=True,V_list = V_list
        )

        # 力
        Fx_total.append(np.sum(Fx))
        Fy_total.append(np.sum(Fy))
        Fz_total.append(np.sum(Fz))

        # 力矩
        Mx_total.append(np.sum(Mx))   # overturning moment
        Mz_total.append(np.sum(Mz))   # aligning torque
        RRT_total.append(np.sum(RRT)) # rolling resistance torque

    # 轉 numpy
    Fx_total = np.array(Fx_total)
    Fy_total = np.array(Fy_total)
    Fz_total = np.array(Fz_total)

    Mx_total = np.array(Mx_total)
    Mz_total = np.array(Mz_total)
    RRT_total = np.array(RRT_total)

    # ======================
    # 畫 Force
    # ======================
    plt.figure()
    plt.plot(SA_sweep, Fx_total, label='Fx')
    plt.plot(SA_sweep, Fy_total, label='Fy')
    plt.plot(SA_sweep, Fz_total, label='Fz')
    plt.xlabel('Slip Angle (deg)')
    plt.ylabel('Force (N)')
    plt.legend()
    plt.grid()
    plt.title('Total Tire Forces vs Slip Angle')

    # ======================
    # 畫 Moment
    # ======================
    plt.figure()
    plt.plot(SA_sweep, Mx_total, label='Mx (Overturning)')
    plt.plot(SA_sweep, Mz_total, label='Mz (Aligning)')
    plt.plot(SA_sweep, RRT_total, label='RRT')
    plt.xlabel('Slip Angle (deg)')
    plt.ylabel('Moment (Nm)')
    plt.legend()
    plt.grid()
    plt.title('Total Tire Moments vs Slip Angle')

    #plt.show()

    plot_vehicle_friction_circle(Fz_per_tire=907, alpha_lim=10, kappa_lim=0.4, resolution=25)
    