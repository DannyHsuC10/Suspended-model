%% Unsprung mass
clear; clc; close all;
scriptInfo = dbstack('-completenames');
scriptDir = fileparts(scriptInfo(1).file);
addpath(scriptDir);
params = load_data(fullfile(scriptDir,'data.csv'));
paramNames = fieldnames(params);
for paramIdx = 1:numel(paramNames)
    eval([paramNames{paramIdx} ' = params.(paramNames{paramIdx});']);
end

%% Parameters

Ks = unsprung_Ks;    % spring stiffness (N/m)
MR = unsprung_MR;    % motion ratio
Kt = unsprung_Kt;    % tire stiffness (N/m)

%% Wheel rate

Kw = Ks * MR^2;

%% Unsprung mass range

mu = unsprung_mu;   % kg

%% Wheel hop frequency

fwh = (1/(2*pi)) * sqrt((Kw + Kt)./mu);

%% Plot

figure;
plot(mu,fwh,'LineWidth',2);

grid on;
xlabel('Unsprung Mass (kg)');
ylabel('Wheel Hop Frequency (Hz)');
title('Unsprung Mass vs Wheel Hop Frequency');
