%% ride rate
clear; clc; close all;

%% Parameters

MR = 0.9;                 % motion ratio
Kt = 180000;              % tire stiffness (N/m)

%% Spring stiffness range

Ks = linspace(10000,500000,2000);   % spring stiffness (N/m)

%% Wheel rate

Kw = Ks .* MR.^2;

%% Ride rate (series spring equation)

Kr = (Kw .* Kt) ./ (Kw + Kt);

%% Plot

figure;
plot(Ks/1000,Kr/1000,'LineWidth',2);

grid on;
xlabel('Spring Rate (kN/m)');
ylabel('Ride Rate (kN/m)');
title('Spring Rate vs Ride Rate');

%% Reference line: tire stiffness

hold on;
yline(Kt/1000,'--','Tire Stiffness');

legend('Ride Rate','Tire Stiffness');
