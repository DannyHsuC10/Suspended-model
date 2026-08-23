clc; clear; close all;
scriptInfo = dbstack('-completenames');
scriptDir = fileparts(scriptInfo(1).file);
addpath(scriptDir);
params = load_data(fullfile(scriptDir,'data.csv'));
paramNames = fieldnames(params);
for paramIdx = 1:numel(paramNames)
    eval([paramNames{paramIdx} ' = params.(paramNames{paramIdx});']);
end
g = aero_g;

%% data
m = aero_m;       % 直量kg
a = aero_a;       % 最大加速度m/s^2
h = aero_h;       % 重心高m
L = aero_L;       % 軸距m
%% 計算
% ===== sweep allowable deformation =====
theta = aero_theta;
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
