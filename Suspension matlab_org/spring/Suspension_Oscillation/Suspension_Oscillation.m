%% Undamped Oscillation
% Analytical vs Numerical
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

m = osc_m;          % kg
k = osc_k;          % N/m

%% Natural frequency

wn = sqrt(k/m);
fn = wn/(2*pi);

fprintf('Natural Frequency = %.2f Hz\n',fn);

%% Initial conditions

x0 = osc_x0;        % m
v0 = osc_v0;        % m/s

%% Time settings

dt = osc_dt;
t_end = osc_t_end;

t = 0:dt:t_end;
N = length(t);

%% =========================================
% Analytical solution
%% =========================================

x_analytical = x0*cos(wn*t) + (v0/wn)*sin(wn*t);

%% =========================================
% Numerical solution (Explicit Euler)
%% =========================================

x_num = zeros(1,N);
v_num = zeros(1,N);
a_num = zeros(1,N);

x_num(1) = x0;
v_num(1) = v0;

for i = 1:N-1

    % acceleration
    a_num(i) = -(k/m)*x_num(i);

    % velocity update
    v_num(i+1) = v_num(i) + a_num(i)*dt;

    % position update
    x_num(i+1) = x_num(i) + v_num(i)*dt;

end

%% Last acceleration

a_num(N) = -(k/m)*x_num(N);

%% =========================================
% Plot comparison
%% =========================================

figure;

plot(t,x_analytical,'LineWidth',2);
hold on;
plot(t,x_num,'--','LineWidth',1.5);

grid on;

xlabel('Time (s)');
ylabel('Displacement (m)');

title('Analytical vs Numerical Solution');

legend('Analytical','Explicit Euler');

%% =========================================
% Error analysis
%% =========================================

% Absolute error
abs_error = abs(x_num - x_analytical);

% Relative error (%)
epsilon = 1e-12;

rel_error = abs_error ./ (abs(x_analytical) + epsilon) * 100;

%% =========================================
% Plot error
%% =========================================

figure;

subplot(2,1,1)

plot(t,abs_error,'LineWidth',2);

grid on;

ylabel('Absolute Error (m)');
title('Numerical Error');

subplot(2,1,2)

plot(t,rel_error,'LineWidth',2);

grid on;

xlabel('Time (s)');
ylabel('Relative Error (%)');
