# Vehicle_parameters.py
import numpy as np

class Car:
    def __init__(self):

        self.m = 360
        self.h = 0.286
        self.W = self.m*g
        self.L_rear = 0.744
        self.L_front = 0.806
        self.L = self.L_front+self.L_rear

        self.t_front = 1.3
        self.t_rear = 1.25

        self.K = np.array([[30000,0,0,0], # 主要先用這個版本分析
                          [0,30000,0,0],
                          [0,0,20000,0],
                          [0,0,0,20000]]) # ride rate
        
        self.K_tire = np.array([56000]*4) # 先不考慮直接用K 解ride rate

        # 工作狀況分類
        self.K_modal = np.array([[3050,0,0], # K_heave
                            [0,550,0],# K_roll
                            [0,0,2500]]) #  K_pitch
        
