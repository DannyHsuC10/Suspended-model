# friction_circle
from model import api as tire # 套用api接口
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 確保 3D 支援
tir_params = tire.load_tir("D2704_mf612.tir") # 載入tir參數檔案

MF = tire.CalculationInput( # 建立MF物件函數
            FZ=800,
            SA=1,
            SL=0.25,
            IA=0.0,
            V = 10,
            pressure=80000,
            tir_params=tir_params
        )

def plot_friction_circle_vs_kappa(Fz=800, pressure=82319, alpha_lim=10, kappa_lim=0.3):#正向力摩擦圓
    alpha_range = np.linspace(-alpha_lim, alpha_lim, 50)
    kappa_range = np.linspace(-kappa_lim, kappa_lim, 50)
    ALPHA, KAPPA = np.meshgrid(alpha_range, kappa_range)
    Fx_map = np.zeros_like(ALPHA)
    Fy_map = np.zeros_like(ALPHA)

    for i in range(ALPHA.shape[0]):
        for j in range(ALPHA.shape[1]):
            MF = tire.CalculationInput( # 建立MF物件函數
                FZ=800,
                SA=ALPHA[i, j],
                SL=KAPPA[i, j],
                IA=0.0,
                V = 10,
                pressure=pressure,
                tir_params=tir_params
            )
            Fx_map[i, j] = tire.MF_Universal_solver("FX", MF) # 呼叫MF_Universal_solver函數，計算FX，第一個參數為"FX"，第二個參數為MF物件
            Fy_map[i, j] = tire.MF_Universal_solver("FY", MF) # 呼叫MF_Universal_solver函數，計算FY，第一個參數為"FY"，第二個參數為MF物件


    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(Fx_map, Fy_map, KAPPA, cmap='viridis', edgecolor='none', alpha=0.6)
    ax.set_xlabel('Fx [N]')
    ax.set_ylabel('Fy [N]')
    ax.set_zlabel('Slip Ratio κ')
    ax.set_title(f'Friction Circle vs Slip Ratio (Fz = {Fz} N)')
    plt.tight_layout()
    plt.show()
    
def plot_friction_circle_vs_Fz(kappa=0.01, pressure=82319, alpha_lim=15, Fz_max=2000):#滑移率摩擦圓
    alpha_range = np.linspace(-alpha_lim, alpha_lim, 50)
    Fz_range = np.linspace(0, Fz_max, 50)
    ALPHA, FZ = np.meshgrid(alpha_range, Fz_range)
    Fx_map = np.zeros_like(ALPHA)
    Fy_map = np.zeros_like(ALPHA)

    for i in range(ALPHA.shape[0]):
        for j in range(ALPHA.shape[1]):
            MF = tire.CalculationInput( # 建立MF物件函數
                FZ=FZ[i, j],
                SA=ALPHA[i, j],
                SL=kappa,
                IA=0.0,
                V = 10,
                pressure=pressure,
                tir_params=tir_params
            )
            Fx_map[i, j] = tire.MF_Universal_solver("FX", MF) # 呼叫MF_Universal_solver函數，計算FX，第一個參數為"FX"，第二個參數為MF物件
            Fy_map[i, j] = tire.MF_Universal_solver("FY", MF) # 呼叫MF_Universal_solver函數，計算FY，第一個參數為"FY"，第二個參數為MF物件

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(Fx_map, Fy_map, FZ, cmap='plasma', edgecolor='none')
    ax.set_xlabel('Fx [N]')
    ax.set_ylabel('Fy [N]')
    ax.set_zlabel('Vertical Load Fz [N]')
    ax.set_title(f'Friction Circle vs Vertical Load (κ = {kappa})')
    plt.tight_layout()
    plt.show()

plot_friction_circle_vs_kappa()
plot_friction_circle_vs_Fz()