clc; clear;

%% -------------------------------
% 車輛參數
%% -------------------------------
g = 9.81;
car.m = 309.5;
car.h = 0.284;
car.L = 1.55;
car.d = 1.25;

car.CG_x = [0.4;0.6]; 
car.CG_y = [0.5,0.5];

car.F_add = [0.0,0.0,0.0];      % 外力 N
car.CF_rela = [0.0;0.0;0.0];  % 外力作用點

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
for i = 1:numel(AX)
    car.ax = AX(i);  
    car.ay = AY(i);
    
    N = Four_wheel_load_LSM(car,false);  % 使用最小作用量法
    %N = Four_wheel_load(car,false);
    
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