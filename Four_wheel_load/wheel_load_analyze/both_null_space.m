%% null space 判斷共同解
% Four wheel load analysis (Unified Line Scan)
% -------------------------------
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
ax = ax*g;
ay = ay*g;


% 重心
car.CG_x = [CG_xf; CG_xr];  % 前/後軸分布
car.CG_y = [CG_yl, CG_yr];  % 左/右輪分布
% 空力
F_add = [F_addx,F_addy,F_addz];%(x,y,z)N
CF_rela = [CF_relax;CF_relay;CF_relaz];  % 相對於重心(x,y,z)m

% -------------------------------
% 計算兩組四輪載重
% -------------------------------
N1 = Four_wheel_load_LSM(ax,ay,F_add,CF_rela,car,true);  % 4x1 LSM 解
N2 = Four_wheel_load_CG(ax,ay,F_add,CF_rela,car,true);     % 4x1 Ratio 解

% -------------------------------
%% 定義線向量 V 與 alpha 掃描
% -------------------------------
V = N2 - N1;            % 四輪載重的線向量

alpha_vec = linspace(0,1,50);   % 50個alpha
N_line = repmat(N1', length(alpha_vec), 1) + alpha_vec'*V';

% -------------------------------
%% 畫線與已知解點疊加
% -------------------------------
figure; hold on; grid on;

colors = ['r','g','b','m'];  % FL, FR, RL, RR

% 先畫線
for i = 1:4
    plot(alpha_vec, N_line(:,i), 'Color', colors(i), 'LineWidth',1.5);
end

% 疊加已知解點
alpha_N1 = 0;  % N1 對應 alpha = 0
alpha_N2 = 1;  % N2 對應 alpha = 1

for i = 1:4
    plot(alpha_N1, N1(i), 'o', 'MarkerSize',8, 'MarkerFaceColor',colors(i), 'MarkerEdgeColor','k');
    plot(alpha_N2, N2(i), 's', 'MarkerSize',8, 'MarkerFaceColor',colors(i), 'MarkerEdgeColor','k');
end

xlabel('\alpha'); ylabel('Wheel Load (N)');
legend('FL','FR','RL','RR','Location','best');
title('Four Wheel Load Scan along Line with Known Solutions');