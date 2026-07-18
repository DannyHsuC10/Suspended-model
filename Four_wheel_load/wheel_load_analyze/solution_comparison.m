%% 負載解法比較
clc; clear; close all;
addpath('data');
addpath('solver');
load_data('data.csv');
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
% 畫長條圖比較
% -------------------------------
figure; hold on; grid on;

wheel_labels = {'FL','FR','RL','RR'};
bar_width = 0.2;  % 每組柱子寬度

x = 1:4;  % 四個輪子位置

% 畫第一組
b1 = bar(x - bar_width, N1, bar_width, 'FaceColor',[0.2 0.6 0.8], 'DisplayName','LSM');

% 畫第二組
b2 = bar(x + bar_width, N2, bar_width, 'FaceColor',[0.9 0.4 0.3], 'DisplayName','Ratio');

% 比較
b3 = bar(x , abs(N1-N2), bar_width, 'FaceColor',[0.5 0.5 0.5], 'DisplayName','delta');

set(gca,'XTick',x,'XTickLabel',wheel_labels);
ylabel('Wheel Load (N)');
title('Comparison of Four Wheel Loads');
legend('Location','best');
