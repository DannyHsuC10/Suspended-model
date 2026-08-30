import numpy as np

g = 9.81
class Car:
    def __init__(self):

        self.m = 360
        self.h = 0.286
        self.W = self.m*g
        self.L_rear = 0.744
        self.L_front = 0.806
        self.L = self.L_front+self.L_rear

        self.t_front = 1.25
        self.t_rear = 1.25
        self.K = np.array([[30000,0,0,0],
                          [0,30000,0,0],
                          [0,0,27000,0],
                          [0,0,0,27000]])# ride rate
        self.K_modal = np.array([[3050,0,0],# K_heave
                                 [0,550,0],# K_roll
                                 [0,0,2500]]) #  K_pitch
        
        self.K_modal_coupled = np.array([
                [3050, 0, 0, 0],# K_heave
                [0, 600 + 2900, -2900, 0],# K_roll_f + K_torsion, -K_torsion
                [0, -2900, 500 + 2900, 0],# -K_torsion, K_roll_r + K_torsion
                [0, 0, 0, 2500]# K_pitch
            ])

        self.K_tire = np.array([56000]*4)

# =========================
# 幾何
# =========================
def _get_geometry(car):

    # =========================
    # axle positions
    # =========================
    x_front = car.L_front
    x_rear  = -car.L_rear

    y_left  = -car.t_front / 2
    y_right =  car.t_front / 2

    # 假設前後 track 不同
    y_left_r  = -car.t_rear / 2
    y_right_r =  car.t_rear / 2

    x_pos = np.array([
        x_front, x_front,
        x_rear,  x_rear
    ])

    y_pos = np.array([
        y_left, y_right,
        y_left_r, y_right_r
    ])

    z_pos = np.ones(4)

    return x_pos, y_pos, z_pos

# =========================
# 外在影響
# =========================
def _external_effects(car, F_add, CF_rela):
    h = car.h

    if F_add is None:
        return np.array([0,0,0]), 0, 0

    Fx, Fy, Fz = F_add
    r = np.array([0, 0, h]) if CF_rela is None else np.array(CF_rela)

    Mx = r[1]*Fz - r[2]*Fy
    My = r[2]*Fx - r[0]*Fz

    return Fz, Mx, My

# =========================
# Debug
# =========================
def _debug(ax, ay, car, F_add, N, x_pos, y_pos, Mx_add, My_add):
    if F_add is None:
            F_add = [0,0,0]
            Mx_add = 0
            My_add = 0
    az = -g

    print("輪胎載重 (N):")
    print(f"FL = {N[0]:.1f}, FR = {N[1]:.1f}, RL = {N[2]:.1f}, RR = {N[3]:.1f}")

    Fz = np.sum(N) + car.m * az + F_add[2]
    print(f"平衡確認 : Fz = {Fz:.6f} N")

    Mx = y_pos @ N + car.m * ay * car.h + Mx_add
    My = x_pos @ N + car.m * ax * car.h + My_add

    print(f"Roll moment balance (Mx) = {Mx:.6f} Nm")
    print(f"Pitch moment balance (My) = {My:.6f} Nm")

# =========================
# _get_Ab
# =========================
def _get_Ab(ax, ay, car, F_add=None, CF_rela=None):
        """
        構造 A 矩陣 (幾何關係) 與 b 向量 (慣性力與外加力項)
        A * N + b = 0
        """
        x_pos, y_pos, _ = _get_geometry(car)
        # 1. 基礎參數
        m = car.m
        h = car.h

        # 2. 外加力矩處理
        Mx_add, My_add, Fz_add = 0, 0, 0
        if F_add is not None:
            # F_add 為 [Fx, Fy, Fz]
            # CF_rela 為力作用點相對於 CG 的向量 [dx, dy, dz]
            r = np.array([0, 0, h]) if CF_rela is None else np.array(CF_rela)
            F = np.array(F_add)
            Mx_add = r[1]*F[2] - r[2]*F[1]
            My_add = r[2]*F[0] - r[0]*F[2]
            Fz_add = F[2]

        # 3. 構造矩陣 A (3x4)
        # Row 0: Sum of Fz = 1*N1 + 1*N2 + 1*N3 + 1*N4
        # Row 1: Sum of Mx = y1*N1 + y2*N2 + y3*N3 + y4*N4
        # Row 2: Sum of My = x1*N1 + x2*N2 + x3*N3 + x4*N4
        A = np.array([
            [1, 1, 1, 1],
            [y_pos[0], y_pos[1], y_pos[2], y_pos[3]],
            [x_pos[0], x_pos[1], x_pos[2], x_pos[3]]
        ])

        # 4. 構造向量 b (3x1)
        # 考慮慣性力與外加項
        b = np.array([
            Fz_add - m*g,           # ΣFz - mg + Fz_ext = 0
            m*ay*h + Mx_add,        # ΣMx + Fy*h + Mx_ext = 0
            m*ax*h + My_add        # ΣMy - Fx*h + My_ext = 0
        ])

        return A, b, Mx_add, My_add

# =========================
# CG 法
# =========================
def solve_cg(ax, ay, car, F_add=None, CF_rela=None, check=False):

    # 1. 靜態荷重計算 (考慮重心位置)
    F_z_front_static = car.W * (car.L_rear / car.L)
    F_z_rear_static  = car.W * (car.L_front / car.L)

    # 2. 縱向荷重轉移 (Longitudinal)
    # 加速時前輪減輕，後輪增加
    dF_z_long = car.m * car.h * ax / car.L

    # 3. 外加力矩計算
    Fz_add, Mx_add, My_add = _external_effects(car, F_add, CF_rela)


    # 將外加力矩納入縱向轉移 (My 影響前後)
    dF_z_long += My_add / car.L

    # 4. 側向荷重轉移 (Lateral) - 分別計算前後軸
    # 注意：前軸分配到的側向力與 L_rear 成正比
    dF_z_lat_f = (car.m * ay * car.h * (car.L_rear / car.L)) / car.t_front
    dF_z_lat_r = (car.m * ay * car.h * (car.L_front / car.L)) / car.t_rear
    
    # 若有外加側翻力矩 Mx_add，這裡需假設分配比例 (例如 50/50 或按軸重比)
    dF_z_lat_f += (Mx_add * car.L_rear / car.L) / car.t_front
    dF_z_lat_r += (Mx_add * car.L_front / car.L) / car.t_rear

    # 5. 四輪正向力合成
    # 假設 ax > 0 為加速，ay > 0 為左轉 (右側受壓)
    N_fl = 0.5 * F_z_front_static - 0.5 * dF_z_long + dF_z_lat_f
    N_fr = 0.5 * F_z_front_static - 0.5 * dF_z_long - dF_z_lat_f
    N_rl = 0.5 * F_z_rear_static  + 0.5 * dF_z_long + dF_z_lat_r
    N_rr = 0.5 * F_z_rear_static  + 0.5 * dF_z_long - dF_z_lat_r

    N = np.array([N_fl, N_fr, N_rl, N_rr])
    
    if check:
        print("\n=== CG Solver Results ===")
        x_pos, y_pos, _ = _get_geometry(car)
        _debug(ax, ay, car, F_add, N, x_pos, y_pos, Mx_add, My_add)
    return N

# =========================
# LSM
# =========================
def solve_lsm(ax, ay, car, F_add=None, CF_rela=None, check=False):
        """
        利用最小二乘法求解 (最小化 ||N||^2)
        解法:N = A^T * (A * A^T)^-1 * (-b)
        """
        A, b, Mx_add, My_add = _get_Ab(ax, ay, car, F_add, CF_rela)

        # 標準最小規範解 (Minimum Norm Solution)
        N = A.T @ np.linalg.solve(A @ A.T, -b)

        if check:
            print("\n=== LSM Solver Results ===")
            x_pos, y_pos, _ = _get_geometry(car)
            _debug(ax, ay, car, F_add, N, x_pos, y_pos, Mx_add, My_add)
        return N

# =========================
# 加權 Lagrange
# =========================
def solve_lagrange(ax, ay, car, F_add = None, CF_rela = None, check=False):
    x_pos, y_pos, _ = _get_geometry(car)
    A, b, Mx_add, My_add = _get_Ab(ax, ay, car, F_add, CF_rela)

    if car.K is None:
        car.K = np.eye(4)

    N = car.K @ A.T @ np.linalg.solve(A @ car.K @ A.T, -b)

    if check:
        print("=== Weighted Lagrange ===")
        _debug(ax, ay, car, F_add, N, x_pos, y_pos, Mx_add, My_add)

    return N

# =========================
# 一般懸吊附載模型
# =========================
def solve_suspension(ax, ay, car, F_add=None, check=False, CF_rela=None):
    x_pos, y_pos, _ = _get_geometry(car)

    # =========================
    # 建立幾何矩陣
    # =========================
    # Δz = z + φ*y - θ*x
    B = np.vstack([
        np.ones(4),
        y_pos,
        -x_pos
    ])  # shape (3,4) → transpose later

    # =========================
    # 力平衡 RHS
    # =========================
    b = car.m * np.array([
        -g,
        ay * car.h,
        ax * car.h
    ])

    Fz_add, Mx_add, My_add = _external_effects(car, F_add, CF_rela)
    b += np.array([Fz_add[2], Mx_add, My_add])

    # =========================
    # 解 z, φ, θ
    # =========================
    # N = K * Δz = K * (Bᵀ q)
    # → N = K Bᵀ q
    # 平衡：A N + b = 0
    # → A K Bᵀ q = -b

    A = np.vstack([
        np.ones(4),
        y_pos,
        x_pos
    ])

    M = A @ car.K @ B.T

    q = np.linalg.solve(M, -b)

    # =========================
    # 得到輪胎力
    # =========================
    dz = B.T @ q
    N = car.K @ dz

    if check:
        print("=== Suspension Model ===")
        _debug(ax, ay, car, F_add if F_add is not None else np.zeros(3),
                    N, x_pos, y_pos, Mx_add, My_add)

    return N

# =========================
# 解偶懸吊附載模型(傾斜剛性等效模型)
# =========================
def solve_decoupled(ax, ay, car, F_add=None, check=False, CF_rela=None):
    x_pos, y_pos, _ = _get_geometry(car)

    B = np.vstack([
        np.ones(4),
        y_pos,
        -x_pos
    ])  # (3x4)
    # =========================
    # 外力
    # =========================
    b = car.m * np.array([
        -g,
        ay * car.h,
        ax * car.h
    ])

    Fz_add, Mx_add, My_add = _external_effects(car, F_add, CF_rela)
    b += np.array([Fz_add[2], Mx_add, My_add])

    # =========================
    # 解 q（modal DOF）
    # =========================
    # A N + b = 0
    # N = Bᵀ K_modal q
    # → A Bᵀ K_modal q = -b

    A = np.vstack([
        np.ones(4),
        y_pos,
        x_pos
    ])

    M = A @ B.T @ car.K_modal

    q = np.linalg.solve(M, -b)

    # =========================
    # 回算輪胎力
    # =========================
    N = B.T @ (car.K_modal @ q)
    if check:
            print("\n=== Decoupled Suspension Model ===")
            # 確保 F_add 為 None 時傳入 np.zeros(3) 供 debug 顯示
            _debug(ax, ay, car, F_add if F_add is not None else np.zeros(3),
                N, x_pos, y_pos, Mx_add, My_add)
    return N

"""
# =========================
# 耦合彈簧模型
# =========================
def solve_coupled_vehicle(ax, ay, car, k_susp_func,
                         F_add=None, CF_rela=None,
                         tol=1e-6, max_iter=20, check=False):

    x_pos, y_pos, _ = _get_geometry(car)

    # =========================
    # 建立 B matrix
    # =========================
    B = np.zeros((4, 4))
    for i in range(4):
        B[i, 0] = 1.0  # heave
        if i < 2:
            B[i, 1] = y_pos[i]   # front roll
        else:
            B[i, 2] = y_pos[i]   # rear roll
        B[i, 3] = -x_pos[i]      # pitch

    # =========================
    # 外力統一處理（和其他 solver 一致）
    # =========================
    Fz_add, Mx_add, My_add = _external_effects(car, F_add, CF_rela)

    # =========================
    # modal force（正確分配版）
    # =========================
    Mx_total = car.m * ay * car.h + Mx_add
    My_total = car.m * ax * car.h + My_add
    Fz_total = car.m * g - Fz_add[2]   # 注意方向（N 要撐住重量）

    # 👉 roll 前後分配（用軸距比例）
    Mx_front = Mx_total * (car.L_rear / car.L)
    Mx_rear  = Mx_total * (car.L_front / car.L)

    b_modal = np.array([
        Fz_total,     # heave
        Mx_front,     # front roll
        Mx_rear,      # rear roll
        My_total      # pitch
    ])

    # =========================
    # 迭代解 q
    # =========================
    q = np.zeros(4)

    for _ in range(max_iter):

        dz = B @ q

        k_susp = k_susp_func(dz)
        k_eq = 1 / (1/k_susp + 1/car.K_tire)

        K_corner = np.diag(k_eq)

        K_from_tires = B.T @ K_corner @ B

        M = car.K_modal_coupled + K_from_tires

        try:
            q_new = np.linalg.solve(M, b_modal)
        except np.linalg.LinAlgError:
            print("Matrix singular. Check stiffness definition.")
            break

        if np.linalg.norm(q_new - q) < tol:
            q = q_new
            break

        q = q_new

    # =========================
    # 輪載計算（修正重點）
    # =========================
    dz_final = B @ q
    N = k_eq * dz_final   # 👉 直接當最終輪載（不是 delta）

    # =========================
    # 驗證（統一）
    # =========================
    if check:
        print("=== solve_coupled_vehicle ===")
        _debug(ax, ay, car, F_add if F_add is not None else np.zeros(3),
                    N, x_pos, y_pos, Mx_add, My_add)

    return N


# 彈簧簡化模型
def k_susp_func_s(dz):
    return np.array([30000, 30000, 28000, 28000])

# 彈簧模型
def k_susp_func_n(dz):
    base = np.array([30000, 30000, 28000, 28000])

    # 非線性（例如壓縮變硬）
    return base * (1 + 0.1 * np.clip(dz, 0, None))

# 彈簧進階模型
def k_susp_func_a(dz):

    # wheel → spring compression
    mr = np.array([0.9, 0.9, 0.85, 0.85])

    spring_rate = np.array([35000, 35000, 30000, 30000])

    k_wheel = spring_rate * mr**2

    # geometric nonlinearity
    k_wheel *= (1 + 0.2 * np.abs(dz))

    return k_wheel

"""

if __name__ == "__main__":

    car = Car()
    ax=0.0 * g
    ay=1 * g
    F_add=np.array([0, 0, 0])# 外加力量 (Fx, Fy, Fz)

    print("ax:",ax," ay:",ay)
    solve_cg(ax, ay, car, check=True)
    solve_lsm(ax, ay, car, check=True)
    solve_lagrange(ax, ay, car, check=True)# 最優
    solve_suspension(ax, ay, car, check=True)
    solve_decoupled(ax, ay, car, check=True)
