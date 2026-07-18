clc; clear; close all;
g = 9.81;

%% data
m = 300;                 % 直量kg
ax = 1.6;          % 最大加速度m/s^2
ay = 1.6;             
h = 0.28;                % 重心高m
L = 1.55;                % 軸距m
t = 1.25;               %輪距

%% 計算
% ===== sweep allowable deformation =====
s = 0.01: 0.005: 0.05; % 容許壓縮

Fx = m * ax * g * h/(L/2);
Fy = m * ay * g * h/(t/2);
% ===== pitch stiffness =====
K_pitch = Fx./s/2;
K_roll = Fy./s/2;
% ===== plot =====
figure;
plot(K_pitch, s, '-r');   % 畫 pitch 曲線
hold on;
plot(K_roll, s, '-b');    % 畫 roll 曲線
yline(0.025, '--w');% 賽規限制
grid on;

legend("pitch", "roll");  % 加上圖例


xlabel('K');
ylabel('懸吊壓縮');
title('Pitch Stiffness Requirement vs Allowable Deformation');
