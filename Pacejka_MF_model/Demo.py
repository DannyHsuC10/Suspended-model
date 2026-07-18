from model import api as tire # 套用api接口

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
# MF_Universal_solver可以解出 FX FY MX RRT MZ等多個輸出，第一個參數為輸出類型，第二個參數為MF物件
Fx = tire.MF_Universal_solver("FX", MF) # 呼叫MF_Universal_solver函數，計算FX，第一個參數為"FX"，第二個參數為MF物件
Fy = tire.MF_Universal_solver("FY", MF) # 呼叫MF_Universal_solver函數，計算FY，第一個參數為"FY"，第二個參數為MF物件

print("Fx:", Fx) # 印出
print("Fy:", Fy)