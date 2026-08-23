%% Unsprung mass
clear; clc; close all;

%% Parameters

Ks = 80000;          % spring stiffness (N/m)
MR = 0.9;            % motion ratio
Kt = 180000;         % tire stiffness (N/m)

%% Wheel rate

Kw = Ks * MR^2;

%% Unsprung mass range

mu = linspace(10,80,1000);   % kg

%% Wheel hop frequency

fwh = (1/(2*pi)) * sqrt((Kw + Kt)./mu);

%% Plot

figure;
plot(mu,fwh,'LineWidth',2);

grid on;
xlabel('Unsprung Mass (kg)');
ylabel('Wheel Hop Frequency (Hz)');
title('Unsprung Mass vs Wheel Hop Frequency');
