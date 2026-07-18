clc; clear; close all;
scriptInfo = dbstack('-completenames');
scriptDir = fileparts(scriptInfo(1).file);
addpath(scriptDir);
params = load_data(fullfile(scriptDir,'data.csv'));
paramNames = fieldnames(params);
for paramIdx = 1:numel(paramNames)
    eval([paramNames{paramIdx} ' = params.(paramNames{paramIdx});']);
end
g = max_g;

%% data
m = max_m;        % 直量kg
ax = max_ax;      % 最大加速度m/s^2
ay = max_ay;
h = max_h;        % 重心高m
L = max_L;        % 軸距m
t = max_t;        % 輪距

%% 計算
% ===== sweep allowable deformation =====
s = max_s; % 容許壓縮

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
