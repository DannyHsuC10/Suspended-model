%% 加速負載
clc; clear;
scriptInfo = dbstack('-completenames');
scriptDir = fileparts(scriptInfo(1).file);
addpath(scriptDir);
params = load_data(fullfile(scriptDir,'data.csv'));
paramNames = fieldnames(params);
for paramIdx = 1:numel(paramNames)
    eval([paramNames{paramIdx} ' = params.(paramNames{paramIdx});']);
end
g = acc_g;

%% data
l = acc_l; % 軸距
l_f = acc_l_f; % 重心>>前軸
m = acc_m; % 質量
mu_w = acc_mu_w; % 輪胎摩擦係數
h_cog = acc_h_cog; % 重心高度


%% 計算
l_r = l - l_f;   

% =========================
% 靜態附載
% =========================
N_r_static = m * g * l_f / l;
N_f_static = m * g - N_r_static;

fprintf("Rear static load  : %.2f N\n", N_r_static);
fprintf("Front static load : %.2f N\n", N_f_static);

% =========================
% 加速度範圍
% =========================
a_range = linspace(0, mu_w*g, acc_a_count);

N_r = zeros(size(a_range));
N_f = zeros(size(a_range));

% =========================
% 計算不同加速度下附載
% =========================
for i = 1:length(a_range)

    a = a_range(i);

    F_x_total = m * a;

    N_r(i) = (F_x_total * h_cog + m * g * l_f) / l;
    N_f(i) = m * g - N_r(i);

end

% 最大附載
% Calculate maximum normal loads
maxN_r = max(N_r);
maxN_f = max(N_f);

fprintf("Maximum Rear Load  : %.2f N\n", maxN_r);
fprintf("Maximum Front Load : %.2f N\n", maxN_f);

% 最小附載
minN_r = min(N_r);
minN_f = min(N_f);

fprintf("Minimum Rear Load  : %.2f N\n", minN_r);
fprintf("Minimum Front Load : %.2f N\n", minN_f);

%% =========================
% 畫圖
% =========================
figure
plot(a_range/g, N_f, 'LineWidth',2)
hold on
plot(a_range/g, N_r, 'LineWidth',2)

yline(N_f_static,'--')
yline(N_r_static,'--')

xlabel('Longitudinal Acceleration [g]')
ylabel('Normal Load [N]')
title('Normal Load vs Acceleration')
legend('Front Load','Rear Load','Front Static','Rear Static')

grid on
