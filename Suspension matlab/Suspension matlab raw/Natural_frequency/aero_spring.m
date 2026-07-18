clc; clear; close all;
g = 9.81;

%% data
m = 300;                 % 直量kg
a = 1.6;          % 最大加速度m/s^2
h = 0.28;                % 重心高m
L = 1.55;                % 軸距m
%% 計算
% ===== sweep allowable deformation =====
theta = deg2rad(1): deg2rad(1): deg2rad(30);
s = L/2*theta;

F = m * a * g * h/(L/2);

% ===== pitch stiffness =====
K = F./s/2;

% ===== plot =====
figure;
plot( K,theta, 'LineWidth', 2);
grid on;

xlabel('K');
ylabel('theta_allowable');
title('Pitch Stiffness Requirement vs Allowable Deformation');
