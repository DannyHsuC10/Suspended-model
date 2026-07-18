# MF 測試器
"""
主要功能:
- 測試tir參數對於不同輸出(FX, FY, MX, MZ, RRt)的影響
- 比較曲面差異
- 摩擦圓判斷


還有優化空間，圖片產生時沒有用到MF擬和模型的特性
MF模型有辦法直接輸入矩陣輸出力量矩陣，並不需要大量迴圈疊帶
"""

from model._common import CalculationInput
from model.api import calculate_fx, calculate_fy,load_tir, MF_Universal_solver
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
from scipy.interpolate import griddata
from pathlib import Path
base_dir = Path(__file__).resolve().parent  # magic_formula/

# 解出曲面
Slip_range = np.linspace(-1, 1, 50)
Slip_fix = 0.1# 原先預設
alpha_range = np.linspace(-15, 15, 50)
alpha_fix = 6
Fz_range = np.linspace(0, 2000, 50)
Fz_fix = 800

def MF_set(i,j,X,Y,fix,tir_params,pressure=82319,IA=0.0):#MF設定改這邊
    if fix =="alpha":
        MF = CalculationInput(
            FZ=Y[i, j],
            SA=alpha_fix,      # 固定滑移角，可改變查看角度影響
            SL=X[i, j],
            IA=IA,
            V = tir_params["LONGVL"],
            Ro = tir_params["UNLOADED_RADIUS"],
            pressure=pressure,
            tir_params=tir_params
        )
    if fix =="kappa":
        MF = CalculationInput(
            FZ=Y[i, j],
            SA=X[i, j],
            SL=Slip_fix,
            IA=IA,
            V = tir_params["LONGVL"],
            Ro = tir_params["UNLOADED_RADIUS"],
            pressure=pressure,
            tir_params=tir_params
        )
    if fix =="Fz":
        MF = CalculationInput(
            FZ=Fz_fix,
            SA=Y[i, j],
            SL=X[i, j],
            IA=IA,
            V = tir_params["LONGVL"],
            Ro = tir_params["UNLOADED_RADIUS"],
            pressure=pressure,
            tir_params=tir_params
        )
    return MF

def fig_set(fix,out):#圖片範圍設定
    if fix =="alpha":
        xlabel = "Slip"
        x_range =Slip_range
        ylabel = "Fz"
        y_range = Fz_range
    elif fix =="kappa":
        xlabel = "alpha"
        x_range = alpha_range
        ylabel = "Fz"
        y_range = Fz_range
    elif fix =="Fz":
        xlabel = "kappa"
        x_range = Slip_range
        ylabel = "alpha"
        y_range = alpha_range
    else:
        print("fix tag錯誤")
    zlabel = out
    
    return xlabel,ylabel,zlabel,x_range,y_range

def plot_tire_surfaces(out, fix, tir_params_list, labels=None, save_plt = False):# MF 曲面通用繪製
    xlabel, ylabel, zlabel, x_range, y_range = fig_set(fix, out)
    X, Y = np.meshgrid(x_range, y_range)

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    cmaps = ['viridis', 'plasma', 'inferno', 'cividis', 'magma']
    alphas = np.linspace(0.5, 0.7, len(tir_params_list))

    legend_patches = []

    for idx, tir_params in enumerate(tir_params_list):
        Z = np.zeros_like(X)

        for i in range(Y.shape[0]):
            for j in range(X.shape[1]):
                MF = MF_set(i, j, X, Y, fix, tir_params)
                Z[i, j] = MF_Universal_solver(out, MF)

        cmap = cmaps[idx % len(cmaps)]
        alpha = alphas[idx]

        surf = ax.plot_surface(
            X, Y, Z,
            cmap=cmap,
            edgecolor='none',
            alpha=alpha
        )

        # 建立 proxy artist 給 legend 用
        label = labels[idx] if labels else f"Tire {idx+1}"
        legend_patches.append(
            Patch(facecolor=plt.get_cmap(cmap)(0.6), label=label)
        )

    # 繪製曲面
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    ax.set_title(f"{zlabel} - Tire Model Comparison")
    ax.legend(handles=legend_patches, loc='best')
    # 判斷是否儲存
    if save_plt == True:# 必須同時要資料夾存在
        fig_path = base_dir / "Figures" / f"{zlabel}_{fix}fix.png"
        fig.savefig(fig_path, dpi=300, bbox_inches='tight')
    else:
        plt.tight_layout()
        plt.show()

# 摩擦圓判斷
def plot_friction_circle_vs_kappa_surface(Fz=800, pressure=82319, alpha_lim=10, kappa_lim=0.25, tir_params=None, IA=0.0):
    """
    Fx-Fy 摩擦圓隨滑移率 κ 變化
    z 軸為滑移率 κ
    """
    alpha_range = np.linspace(-alpha_lim, alpha_lim, 50)  # 側滑角
    kappa_range = np.linspace(-kappa_lim, kappa_lim, 50)  # 滑移率

    Fx_map = np.zeros((len(kappa_range), len(alpha_range)))
    Fy_map = np.zeros((len(kappa_range), len(alpha_range)))

    # 計算 Fx, Fy
    for i, kappa in enumerate(kappa_range):
        for j, alpha in enumerate(alpha_range):
            calc_input = CalculationInput(
                FZ=Fz,
                SA=alpha,
                SL=kappa,
                IA=IA,
                pressure=pressure,
                tir_params=tir_params
            )
            Fx_map[i, j] = calculate_fx(calc_input)[0]
            Fy_map[i, j] = calculate_fy(calc_input)[0]

    # 將不規則點插值到規則矩形網格
    points = np.column_stack((Fx_map.ravel(), Fy_map.ravel()))   # 原始 Fx, Fy
    values = np.repeat(kappa_range, len(alpha_range))            # 對應的 κ 值

    # 建立規則網格
    Fx_lin = np.linspace(Fx_map.min(), Fx_map.max(), 100)
    Fy_lin = np.linspace(Fy_map.min(), Fy_map.max(), 100)
    FX, FY = np.meshgrid(Fx_lin, Fy_lin)

    # 插值 κ 到規則網格
    KAPPA_grid = griddata(points, values, (FX, FY), method='linear')

    # 畫光滑曲面
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(FX, FY, KAPPA_grid, cmap='viridis', edgecolor='none', alpha=0.8)
    
    title = base_dir / "Figures" / f'Friction_Circle_vs_Slip_Ratio_face'
    ax.set_xlabel('Fx [N]')
    ax.set_ylabel('Fy [N]')
    ax.set_zlabel('Slip Ratio κ')
    ax.set_title(title)
    fig.savefig(title, dpi=300, bbox_inches='tight')
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
    plt.tight_layout()
    plt.show()

def plot_friction_circle_vs_kappa_curves(Fz=800, pressure=82319, alpha_lim=10, kappa_lim=0.25, tir_params=None, IA=0.0):
    alpha_range = np.linspace(-alpha_lim, alpha_lim, 200)  # 側滑角
    kappa_range = np.linspace(-kappa_lim, kappa_lim, 200)  # 滑移率

    Fx_map = np.zeros((len(kappa_range), len(alpha_range)))
    Fy_map = np.zeros((len(kappa_range), len(alpha_range)))

    # 填入 Fx, Fy
    for i, kappa in enumerate(kappa_range):
        for j, alpha in enumerate(alpha_range):
            calc_input = CalculationInput(
                FZ=Fz,
                SA=alpha,
                SL=kappa,
                IA=IA,
                pressure=pressure,
                tir_params=tir_params
            )
            # 強制把 array 轉成單一 float
            Fx_map[i, j] = np.squeeze(calculate_fx(calc_input))
            Fy_map[i, j] = np.squeeze(calculate_fy(calc_input))

    # 畫 3D 曲面 (Fx-Fy 為底，z 軸為滑移率 κ)
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    # 每個 κ 畫一條 Fx-Fy 曲線，堆疊成曲面
    for i, kappa in enumerate(kappa_range):
        ax.plot(Fx_map[i, :], Fy_map[i, :], kappa*np.ones_like(alpha_range),
                color='blue', alpha=0.7)

    title = base_dir / "Figures" / f'Friction_Circle_vs_Slip_Ratio_curves'
    ax.set_xlabel('Fx [N]')
    ax.set_ylabel('Fy [N]')
    ax.set_zlabel('Slip Ratio κ')
    ax.set_title(title)
    fig.savefig(title, dpi=300, bbox_inches='tight')
    plt.tight_layout()
    plt.show()

def plot_friction_circle_vs_Fz_surface(kappa=0.1, pressure=82319, alpha_lim=10, Fz_max=2000, tir_params=None, IA=0.0):
    """
    Fx-Fy 摩擦圓隨正向力 Fz 變化，生成光滑曲面
    z軸為垂直載荷 Fz
    """
    alpha_range = np.linspace(-alpha_lim, alpha_lim, 50)
    Fz_range = np.linspace(0, Fz_max, 50)

    Fx_list = []
    Fy_list = []
    FZ_list = []

    # 收集不規則點
    for Fz in Fz_range:
        for alpha in alpha_range:
            MF = CalculationInput(
                FZ=Fz,
                SA=alpha,
                SL=kappa,
                IA=IA,
                pressure=pressure,
                tir_params=tir_params
            )
            Fx_val = np.squeeze(calculate_fx(MF))
            Fy_val = np.squeeze(calculate_fy(MF))

            Fx_list.append(Fx_val)
            Fy_list.append(Fy_val)
            FZ_list.append(Fz)

    Fx_array = np.array(Fx_list)
    Fy_array = np.array(Fy_list)
    FZ_array = np.array(FZ_list)

    # 建立規則網格
    Fx_lin = np.linspace(Fx_array.min(), Fx_array.max(), 100)
    Fy_lin = np.linspace(Fy_array.min(), Fy_array.max(), 100)
    FX, FY = np.meshgrid(Fx_lin, Fy_lin)

    # 插值 Fz 到規則網格
    FZ_grid = griddata(
        points=np.column_stack((Fx_array, Fy_array)),
        values=FZ_array,
        xi=(FX, FY),
        method='linear'
    )

    # 畫光滑曲面
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(FX, FY, FZ_grid, cmap='plasma', edgecolor='none', alpha=0.9)

    title = base_dir / "Figures" / f'Friction_Circle_vs_Fz_face'
    ax.set_xlabel('Fx [N]')
    ax.set_ylabel('Fy [N]')
    ax.set_zlabel('Vertical Load Fz [N]')
    ax.set_title(title)
    fig.savefig(title, dpi=300, bbox_inches='tight')
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
    plt.tight_layout()
    plt.show()

def plot_friction_circle_vs_Fz_curves(kappa=0.1,alpha_lim=10,Fz_max=2000.0,pressure=82319.0,tir_params=None,IA=0.0):
    alpha_list = np.linspace(-alpha_lim, alpha_lim, 400)  # 不同線對應不同 α
    Fz_list = np.linspace(0.0, Fz_max, 50)                # 掃描 Fz
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    for alpha in alpha_list:
        Fx_line = []
        Fy_line = []
        for Fz in Fz_list:
            MF = CalculationInput(
                FZ=Fz,
                SA=alpha,
                SL=kappa,
                IA=IA,
                pressure=pressure,
                tir_params=tir_params
            )
            Fx = float(np.asarray(calculate_fx(MF)).flatten()[0])
            Fy = float(np.asarray(calculate_fy(MF)).flatten()[0])
            Fx_line.append(Fx)
            Fy_line.append(Fy)

        ax.plot(Fx_line, Fy_line, Fz_list, color='blue', alpha=0.7)
    title = base_dir / "Figures" / f"Friction_Circle_vs_Fz_curves"
    ax.set_xlabel("Fx [N]")
    ax.set_ylabel("Fy [N]")
    ax.set_zlabel("Fz [N]")
    ax.set_title(title)
    fig.savefig(title, dpi=300, bbox_inches='tight')
    plt.tight_layout()
    plt.show()
    

if __name__ == "__main__":
    D2704_mf612 = load_tir("D2704_mf612.tir")# 紅心13吋
    FSAE_43075R20 = load_tir("FSAE_43075R20.tir")# 新的擬合結果
    #"""
    outputs = ['FX', 'FY', 'MX', 'MZ', 'RRT']
    fix_cases = ['alpha','kappa','Fz']
    tir_params_list = [FSAE_43075R20]
    """
    outputs = ['MZ']
    fix_cases = ['alpha','kappa','Fz']
    tir_params_list = [D2704_mf612]
    #"""

    #plot_friction_circle_vs_kappa_surface(tir_params = FSAE_43075R20)
    #plot_friction_circle_vs_kappa_curves(tir_params = FSAE_43075R20)
    #plot_friction_circle_vs_Fz_surface(tir_params = FSAE_43075R20)
    #plot_friction_circle_vs_Fz_curves(tir_params = FSAE_43075R20)

    for out in outputs:
        for fix in fix_cases:
            plot_tire_surfaces(out,fix,tir_params_list)
            print("out : ",out,"  fix : ",fix)
