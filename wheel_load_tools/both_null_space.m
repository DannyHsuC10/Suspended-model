%% -------------------------------
%% Four wheel load analysis (Unified Line Scan)
%% -------------------------------
clc; clear;


%% -------------------------------
%% 車輛參數
%% -------------------------------
g = 9.81;

car.m = 309.5;
car.h = 0.284;
car.L = 1.55;
car.d = 1.25;

car.ax = 0.3*g;
car.ay = 1.5*g;

% CG比例
car.CG_x = [0.5;0.5];     % 左右
car.CG_y = [0.4,0.6];     % 前後

car.F_add = [0,0,0];      % 外力 N
car.CF_rela = [0.0;0.0;0.0];  % 外力作用點

%% -------------------------------
%% 取得兩個已知載重點
%% -------------------------------
N1 = Four_wheel_load_LSM(car,true); % LSM解 4x1
N2 = Four_wheel_load(car,true);     % Ratio解 4x1

%% -------------------------------
%% 定義線向量 V 與 alpha 掃描
%% -------------------------------
V = N2 - N1;            % 四輪載重的線向量

alpha_vec = linspace(0,1,50);   % 50個alpha
N_line = repmat(N1', length(alpha_vec), 1) + alpha_vec'*V';

%% -------------------------------
%% 畫線與已知解點疊加
%% -------------------------------
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