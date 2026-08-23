%% Critical Damping Analysis
clear; clc; close all;

%% Parameters

m = 300/4;      % sprung mass (kg)

%% Spring stiffness range

k = linspace(10000,300000,1000);

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

