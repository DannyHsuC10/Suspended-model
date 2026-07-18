%% 掃描負載分析(全部)
clc; clear; close all;

%% -------------------------------
% 車輛參數定義
%% -------------------------------
g = 9.81;

% 1. 初始化動力學模擬器
sim = VehicleDynamicsSimulator(g);

% 2. 複寫模擬器內的參數，與你的腳本參數對齊
sim.m = 300;
sim.h = 0.28;
sim.L = 1.55;
sim.W = sim.m * sim.g;

% 根據你的 car.CG_x = [0.48; 0.52] (前/後軸荷分配比) 自動換算 L_front 與 L_rear
% 重心離前軸距離 = 軸距 * 後軸比例；重心離後軸距離 = 軸距 * 前軸比例
sim.L_front = sim.L * 0.52;  
sim.L_rear  = sim.L * 0.48;

% 輪距 (對應你寫的 car.d = 1.25)
sim.t_front = 1.25;
sim.t_rear  = 1.25;

% 更新內部的剛性矩陣 K (選用：若你有特定 Ride rate 可在此修改)
sim.K = [30000, 0, 0, 0;
         0, 30000, 0, 0;
         0, 0, 27000, 0;
         0, 0, 0, 27000];

% 外加力與力矩作用點（預設為空，若無外力傳 [] 即可）
F_add = [0, 0, 0]; 
CF_rela = []; 

%% -------------------------------
% 加速度範圍
%% -------------------------------
ax_range = linspace(-2*g, 2*g, 50);
ay_range = linspace(-2*g, 2*g, 50);
[AX, AY] = meshgrid(ax_range, ay_range);

%% -------------------------------
% 預分配四輪載重矩陣
%% -------------------------------
FL = zeros(size(AX));
FR = zeros(size(AX));
RL = zeros(size(AX));
RR = zeros(size(AX));

%% -------------------------------
% 計算四輪載重
%% -------------------------------
% 提示：大範圍掃描時，check 務必給 false，否則 Command Window 會噴出 2500 行 log 導致 MATLAB 變很卡
for i = 1:numel(AX)
    ax = AX(i);  
    ay = AY(i);
    
    % 使用物件導向方式呼叫
    N = sim.solve_lagrange(ax, ay, F_add, CF_rela, false);  
    
    FL(i) = N(1);
    FR(i) = N(2);
    RL(i) = N(3);
    RR(i) = N(4);
end

%% -------------------------------
% 畫同一個 3D 平面圖 (保持你精美的繪圖代碼)
%% -------------------------------
figure(); hold on; grid on;
% 四輪對應顏色
colors = {[0.2 0.6 0.8], [0.9 0.4 0.3], [0.3 0.9 0.3], [0.8 0.2 0.8]};
wheel_names = {'FL','FR','RL','RR'};
wheel_data = {FL, FR, RL, RR};

for k = 1:4
    h = surf(AX, AY, wheel_data{k});
    h.FaceColor = colors{k};
    h.EdgeColor = 'none';
    h.FaceAlpha = 0.5;  % 半透明，方便疊加觀察
end

xlabel('ax (m/s^2)'); ylabel('ay (m/s^2)'); zlabel('Wheel Load (N)');
title('Four Wheel Loads Overlay vs ax and ay');
legend(wheel_names,'Location','best');
view(45,30);  % 調整視角
colormap jet;