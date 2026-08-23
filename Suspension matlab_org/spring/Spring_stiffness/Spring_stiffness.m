%% Spring stiffness vs natural frequency
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

m = spring_stiffness_m;   % quarter car mass (kg)

%% Spring stiffness range

k = spring_stiffness_k; % N/m

%% Natural frequency

fn = (1/(2*pi)) * sqrt(k./m);

%% Plot

figure;
plot(k/1000,fn,'LineWidth',2);

grid on;
xlabel('Spring Stiffness (kN/m)');
ylabel('Natural Frequency (Hz)');
title('Natural Frequency vs Spring Stiffness');
