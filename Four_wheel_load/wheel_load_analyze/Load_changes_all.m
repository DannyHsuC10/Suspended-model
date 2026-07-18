%% 掃描負載分析(全部)
clc; clear; close all;
addpath('data');
addpath('solver');
load_data('data.csv')
%% -------------------------------
% 車輛參數
%% -------------------------------
g = 9.81;
car.m = m;
car.h = h;
car.L = L;
car.d = d;
ax = ax*g;
ay = ay*g;


% 重心
car.CG_x = [CG_xf; CG_xr];  % 前/後軸分布
car.CG_y = [CG_yl, CG_yr];  % 左/右輪分布
% 空力
CF_rela = [CF_relax;CF_relay;CF_relaz];  % 相對於重心(x,y,z)m
F_add = [F_addx,F_addy,F_addz];%(x,y,z)N

%% -------------------------------
% 加速度範圍
%% -------------------------------
ax_range = linspace(-1.5*g, 1.5*g, 50);
ay_range = linspace(-1.5*g, 1.5*g, 50);
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
for i = 1:numel(AX)
    ax = AX(i);  
    ay = AY(i);
    
    N = Four_wheel_load_LSM(ax,ay,F_add,CF_rela,car,false);  % 4x1 LSM 解
    %N = Four_wheel_load_CG(ax,ay,F_add,CF_rela,car,false);     % 4x1 Ratio 解
    
    FL(i) = N(1);
    FR(i) = N(2);
    RL(i) = N(3);
    RR(i) = N(4);
end

%% -------------------------------
% 畫同一個 3D 平面圖
%% -------------------------------
figure('Color','w'); hold on; grid on;

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