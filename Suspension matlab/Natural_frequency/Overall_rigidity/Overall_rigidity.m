%% Overall rigidity
clear; clc; close all;
scriptInfo = dbstack('-completenames');
scriptDir = fileparts(scriptInfo(1).file);
addpath(scriptDir);
params = load_data(fullfile(scriptDir,'data.csv'));
paramNames = fieldnames(params);
for paramIdx = 1:numel(paramNames)
    eval([paramNames{paramIdx} ' = params.(paramNames{paramIdx});']);
end

%% 固定參數
Ks = overall_Ks;      % 懸吊剛性 (N/m)
Kt = overall_Kt;      % 輪胎剛性 (N/m)

%% 車體剛性掃描 (1~20倍懸吊剛性)
ratio = overall_ratio;
Kc_list = ratio * Ks;

Keq_list = zeros(size(Kc_list));

%% 計算等效剛性
for i = 1:length(Kc_list)
    Kc = Kc_list(i);
    
    Keq_list(i) = 1 / (1/Kt + 1/Ks + 1/Kc);
end

%% 畫圖
figure;
plot(ratio, Keq_list, 'o-', 'LineWidth', 2);
grid on;

xlabel('Chassis stiffness / Suspension stiffness ratio (Kc / Ks)');
ylabel('Equivalent stiffness Keq (N/m)');
title('Effect of Chassis Stiffness on Overall Stiffness');

%% 標記 10 倍區域
hold on;

xline(10, '--r', '10x threshold', 'LineWidth', 2);

%% 顯示飽和值
Keq_inf = 1 / (1/Kt + 1/Ks);
yline(Keq_inf, '--k', 'Asymptote', 'LineWidth', 2);

legend('Keq', '10x rule', 'Saturation limit');
