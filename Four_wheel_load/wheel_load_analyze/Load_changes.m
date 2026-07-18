%% 掃描負載分析

clc; clear; close all;
addpath('data');
addpath('solver');
load_data('data.csv')

% -------------------------------
% 車輛參數
% -------------------------------
g = 9.81;
car.m = m;
car.h = h;
car.L = L;
car.d = d;

% 重心
car.CG_x = [CG_xf; CG_xr];  % 前/後軸分布
car.CG_y = [CG_yl, CG_yr];  % 左/右輪分布
% 空力
F_add = [F_addx,F_addy,F_addz];%(x,y,z)N
CF_rela = [CF_relax;CF_relay;CF_relaz];  % 相對於重心(x,y,z)m

% -------------------------------
% 加速度範圍(2~-2)
% -------------------------------
ax_range = linspace(-2*g, 2*g, 50);
ay_range = linspace(-2*g, 2*g, 50);
[AX, AY] = meshgrid(ax_range, ay_range);

% -------------------------------
% 預分配四輪差值矩陣
% -------------------------------
FL = zeros(size(AX));
FR = zeros(size(AX));
RL = zeros(size(AX));
RR = zeros(size(AX));

% -------------------------------
% 計算四輪差值
% -------------------------------
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

% -------------------------------
% 畫差值曲面
% -------------------------------
figure();

wheel_names = {'FL','FR','RL','RR'};
Diff_data = {FL, FR, RL, RR};

for k = 1:4
    subplot(2,2,k)
    surf(AX, AY, Diff_data{k}, 'EdgeColor','none')
    xlabel('ax (m/s^2)'); ylabel('ay (m/s^2)'); zlabel('F(N)');
    title([wheel_names{k} '4W Load']);
    view(45,30);
    grid on;
    shading interp;
end

sgtitle('Four Wheel Load vs ax and ay');