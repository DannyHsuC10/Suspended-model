# 線性回歸
"""
線性回歸:
解出垂直剛度 k 和 預先負載 b
R = k * (R0 - RL) + b
原點通過線性回歸:
R = k * (R0 - RL)
"""
import numpy as np
import matplotlib.pyplot as plt

def linear_regression(FZ, RL, R0, K0):# 線性回歸計算垂直剛度
    """
    線性回歸計算垂直剛度
    FZ: 垂直力
    RL: 輪輞半徑
    R0: 自由半徑
    K0: 官方資料的線性剛度
    """
    # 計算 deflection
    delta = R0 - RL

    # 若 FZ 為負 (TTC 常見)，取正值
    y = np.abs(FZ)
    x = delta

    # 建立設計矩陣 [x 1]
    X = np.vstack([x, np.ones(len(x))]).T

    # 最小平方法
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    k = beta[0]
    b = beta[1]

    # 預測 (R = kx + F0)
    y_pred = k * x + b

    # R^2
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - ss_res / ss_tot

    # RMSE
    rmse = np.sqrt(np.mean((y - y_pred)**2))

    print("===== 線性回歸結果 =====")
    print(f"R0 (Free Radius) = {R0:.6f}")
    print(f"Vertical stiffness k = {k:.4f} N/mm")
    print(f"預先負載 b = {b:.4f}")
    print(f"預載壓縮 dr0 = {b/k:.4f}")
    print(f"R^2 = {r2:.6f}")
    print(f"RMSE = {rmse:.6f}")

    # 繪圖
    plt.figure(figsize=(8,6))
    plt.scatter(x, y, alpha=0.6, label="Data")
    plt.plot(x, y_pred, color='red', linewidth=2, label="Linear Fit")
    plt.plot(x, x*K0, color='green', linewidth=2, label="Linear ttc")# 官方資料的線性剛度
    plt.xlabel("Deflection (R0 - RL)")
    plt.ylabel("FZ")
    plt.title("Vertical Stiffness Linear Regression")
    plt.legend()
    plt.grid()
    plt.savefig("Figures/Vertical_stiffness.png")
    print("圖表已儲存至 Figures/Vertical_stiffness.png")
    #plt.show()

    return k, b

def linear_regression_origin(FZ, RL, R0, K0):# 強制通過原點的線性回歸 (R = k * delta)
    """
    線性回歸計算垂直剛度
    FZ: 垂直力
    RL: 輪輞半徑
    R0: 自由半徑
    K0: 官方資料的線性剛度
    """
    delta = R0 - RL

    y = np.abs(FZ)
    x = delta

    # 強制通過原點的 least squares
    k = np.dot(x, y) / np.dot(x, x)

    y_pred = k * x

    # R^2
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - ss_res / ss_tot

    rmse = np.sqrt(np.mean((y - y_pred)**2))

    print("===== 線性回歸結果 (through origin) =====")
    print(f"R0 (Free Radius) = {R0:.6f}")
    print(f"Vertical stiffness k = {k:.4f} N/mm")
    print(f"R^2 = {r2:.6f}")
    print(f"RMSE = {rmse:.6f}")

    # plot
    plt.figure(figsize=(8,6))
    plt.scatter(x, y, alpha=0.6, label="Data")
    plt.plot(x, y_pred, color='red', linewidth=2, label="Linear Fit (0 intercept)")
    plt.plot(x, x*K0, color='green', linewidth=2, label="Linear TTC")

    plt.xlabel("Deflection (R0 - RL)")
    plt.ylabel("FZ")
    plt.title("Vertical Stiffness Linear Regression")
    plt.legend()
    plt.grid()
    plt.savefig("Figures/Vertical_stiffness_origin.png")
    print("圖表已儲存至 Figures/Vertical_stiffness_origin.png")
    #plt.show()

    return k
