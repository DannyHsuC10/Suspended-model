%% Damping Ratio Sweep
% Displacement + Tire Normal Load
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

ms = damped_ms;
mu = damped_mu;

ks = damped_ks;
kt = damped_kt;

g = damped_g;

%% Damping ratios

zeta_list = damped_zeta_list;

%% Critical damping

cc = 2*sqrt(ks*ms);

%% Initial conditions

xs0 = damped_xs0;
vs0 = damped_vs0;

xu0 = damped_xu0;
vu0 = damped_vu0;

X0 = [xs0; vs0; xu0; vu0];

%% Time

tspan = damped_tspan;

%% Static tire load

Fz_static = (ms + mu)*g;

%% =========================================
% Plot
%% =========================================

figure;

%% =========================================
% Sprung displacement
%% =========================================

subplot(2,1,1)
hold on;
grid on;

%% =========================================
% Tire load variation
%% =========================================

subplot(2,1,2)
hold on;
grid on;

%% =========================================
% Loop
%% =========================================

for i = 1:length(zeta_list)

    zeta = zeta_list(i);

    cs = zeta * cc;

    %% Solve

    [t,X] = ode45( ...
        @(t,X) quarter_car_damped_ode( ...
        t,X,ms,mu,ks,kt,cs), ...
        tspan,X0);

    %% Extract states

    xs = X(:,1);
    xu = X(:,3);

    %% Road profile
    % fixed ground for free vibration

    xr = zeros(size(t));

    %% Tire normal load

    Fz = Fz_static + kt .* (xu - xr);

    %% Dynamic tire load variation

    dFz = Fz - Fz_static;

    %% =====================================
    % Plot displacement
    %% =====================================

    subplot(2,1,1)

    plot(t,xs,'LineWidth',2);

    %% =====================================
    % Plot tire load variation
    %% =====================================

    subplot(2,1,2)

    plot(t,dFz,'LineWidth',2);

end

%% =========================================
% Labels
%% =========================================

subplot(2,1,1)

xlabel('Time (s)');
ylabel('Sprung Displacement (m)');

title('Damping Ratio Sweep');

legend( ...
    '\zeta = 0', ...
    '\zeta = 0.2', ...
    '\zeta = 0.4', ...
    '\zeta = 0.7', ...
    '\zeta = 1.0');

%% =========================================

subplot(2,1,2)

xlabel('Time (s)');
ylabel('\Delta Fz (N)');

title('Dynamic Tire Load Variation');

legend( ...
    '\zeta = 0', ...
    '\zeta = 0.2', ...
    '\zeta = 0.4', ...
    '\zeta = 0.7', ...
    '\zeta = 1.0');

%% =========================================
% ODE Function
%% =========================================

function dX = quarter_car_damped_ode( ...
    ~,X,ms,mu,ks,kt,cs)

%% States

xs = X(1);
vs = X(2);

xu = X(3);
vu = X(4);

%% Relative displacement / velocity

dx = xs - xu;
dv = vs - vu;

%% Accelerations

as = -(ks/ms)*dx ...
     -(cs/ms)*dv;

au =  (ks/mu)*dx ...
     +(cs/mu)*dv ...
     -(kt/mu)*xu;

%% State derivatives

dX = zeros(4,1);

dX(1) = vs;
dX(2) = as;

dX(3) = vu;
dX(4) = au;

end
 
