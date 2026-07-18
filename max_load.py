import wheel
from Pacejka_MF_model.model import api as tire
import numpy as np
import Four_wheel_load as fwl
car = fwl.Car()
tir_params = tire.load_tir("FSAE_43075R20.tir")


SA_sweep = np.linspace(-15, 15, 50) # 精細度
SL_sweep = np.linspace(-0.3, 0.3, 50) # 精細度

def solve_ax_ay(SA, SL, car, tir_params, tol=1e-2, max_iter=5):# 條精度
    
    ax = 0.0
    ay = 0.0

    for _ in range(max_iter):

        # 由加速度算四輪負載
        FZ_list = fwl.solve_lagrange(ax, ay, car)

        # 建立四輪 slip (假設四輪相同，可再擴充)
        SA_list = [SA]*4
        SL_list = [SL]*4

        # 輪胎力
        Fx, Fy, Fz, Mx, RRT, Mz = wheel.Four_wheel_output(
            FZ_list, SA_list, SL_list, tir_params
        )

        # 更新加速度
        ax_new = np.sum(Fx) / car.m
        ay_new = np.sum(Fy) / car.m

        # 收斂判定
        if abs(ax_new - ax) < tol and abs(ay_new - ay) < tol:
            break

        ax, ay = ax_new, ay_new

    return ax, ay, Fx, Fy, FZ_list


best_force = 0
best_case = None
best_force = 0

for SA in SA_sweep:
    print(best_force)

    for SL in SL_sweep:

        ax, ay, Fx, Fy, FZ = solve_ax_ay(SA, SL, car, tir_params)
        
        # 計算每個輪胎的合力
        for i in range(4):
            F_comb = np.sqrt(Fx[i]**2 + Fy[i]**2 + FZ[i]**2)
            
            if F_comb > best_force:
                
                best_force = F_comb
                best_case = {
                    "SA": SA,
                    "SL": SL,
                    "wheel": i,
                    "Fx": Fx[i],
                    "Fy": Fy[i],
                    "Fz": FZ[i],
                    "ax": ax,
                    "ay": ay
                }
                print(best_force,"new best_force")
print("===================")
print(best_case)
print(best_force)