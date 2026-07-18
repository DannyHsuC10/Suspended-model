%% Critical Damping Analysis
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

m = critical_m;      % sprung mass (kg)

%% Spring stiffness range

k = critical_k;

%% Critical damping

cc = 2 * sqrt(k .* m);

%% Natural frequency

fn = (1/(2*pi)) * sqrt(k./m);

%% Plot

figure;

subplot(2,1,1)

plot(k/1000,fn,'LineWidth',2);

grid on;

xlabel('Spring Stiffness (kN/m)');
ylabel('Natural Frequency (Hz)');

title('Natural Frequency vs Spring Stiffness');

subplot(2,1,2)

plot(k/1000,cc,'LineWidth',2);

grid on;

xlabel('Spring Stiffness (kN/m)');
ylabel('Critical Damping (N·s/m)');

title('Critical Damping vs Spring Stiffness');

