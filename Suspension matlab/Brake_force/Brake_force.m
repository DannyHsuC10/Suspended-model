%% 煞車力

clc; clear; close all;
scriptDir = fileparts(mfilename('fullpath'));
addpath(scriptDir);
params = load_data(fullfile(scriptDir,'data.csv'));
paramNames = fieldnames(params);
for paramIdx = 1:numel(paramNames)
    eval([paramNames{paramIdx} ' = params.(paramNames{paramIdx});']);
end
g = brake_g;

fprintf("\n F_driver = %.2f\n", F_driver);

F_mc = F_driver*PR;

fprintf("\n F_mc = %.2f\n", F_mc);
% balance_bar
bb_r = 1-balance_bar;
bb_f = balance_bar;

% 主缸面積
A_mc_f = pi * (D_mc_f / 2)^2;
A_mc_r = pi * (D_mc_r / 2)^2;

P_mc_f = F_mc*bb_f/A_mc_f;
P_mc_r = F_mc*bb_r/A_mc_r;


% 卡鉗面積
A_caliper_f = N_caliper_f * pi * (D_caliper_f / 2)^2;
A_caliper_r = N_caliper_r * pi * (D_caliper_r / 2)^2;

% 主缸力
F_caliper_f = P_mc_f * mu_pad * A_caliper_f;
F_caliper_r = P_mc_r * mu_pad * A_caliper_r;

r_disc = r_disc_o / 2 - d_gap;

F_brake_f = F_caliper_f*r_disc*2/r_w;
F_brake_r = F_caliper_r*r_disc*2/r_w;

fprintf("\n F_brake_f = %.2f\n", F_brake_f);
fprintf("\n F_brake_r = %.2f\n", F_brake_r);

F_brake = F_brake_r+F_brake_f;
fprintf("\n F_brake = %.2f\n", F_brake);
