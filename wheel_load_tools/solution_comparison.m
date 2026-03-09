clc; clear;
% -------------------------------
% 車輛參數
% -------------------------------
g = 9.81;
car.m = 309.5;
car.h = 0.284;
car.L = 1.55;
car.d = 1.25;
car.ax = 0.3*g;
car.ay = 0.0*g;
car.F_add = [0,0,0];%(x,y,z)N

% 重心
car.CG_x = [0.48; 0.52];  % 前/後軸分布
car.CG_y = [0.5, 0.5];  % 左/右輪分布
% 空力
car.CF_rela = [0.0;0.0;0.0];  % 相對於重心(x,y,z)m

% -------------------------------
% 計算兩組四輪載重
% -------------------------------
N = Four_wheel_load_LSM(car,true);  % 4x1 LSM 解
N1 = Four_wheel_load(car,true);     % 4x1 Ratio 解

% -------------------------------
% 畫長條圖比較
% -------------------------------
figure; hold on; grid on;

wheel_labels = {'FL','FR','RL','RR'};
bar_width = 0.2;  % 每組柱子寬度

x = 1:4;  % 四個輪子位置

% 畫第一組
b1 = bar(x - bar_width, N, bar_width, 'FaceColor',[0.2 0.6 0.8], 'DisplayName','LSM');

% 畫第二組
b2 = bar(x + bar_width, N1, bar_width, 'FaceColor',[0.9 0.4 0.3], 'DisplayName','Ratio');

% 比較
b3 = bar(x , abs(N-N1), bar_width, 'FaceColor',[0.5 0.5 0.5], 'DisplayName','delta');

set(gca,'XTick',x,'XTickLabel',wheel_labels);
ylabel('Wheel Load (N)');
title('Comparison of Four Wheel Loads');
legend('Location','best');