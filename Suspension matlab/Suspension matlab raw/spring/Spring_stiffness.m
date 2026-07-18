%% Spring stiffness vs natural frequency
clear; clc; close all;

%% Parameters

m = 250/4;   % quarter car mass (kg)

%% Spring stiffness range

k = linspace(10000,300000,1000); % N/m

%% Natural frequency

fn = (1/(2*pi)) * sqrt(k./m);

%% Plot

figure;
plot(k/1000,fn,'LineWidth',2);

grid on;
xlabel('Spring Stiffness (kN/m)');
ylabel('Natural Frequency (Hz)');
title('Natural Frequency vs Spring Stiffness');
