%% Quarter Car Model with Damping
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

ms = quarter_ms;          % sprung mass (kg)
mu = quarter_mu;             % unsprung mass (kg)

ks = quarter_ks;          % suspension stiffness (N/m)
kt = quarter_kt;         % tire stiffness (N/m)

%% Damping ratio

zeta = quarter_zeta;

%% Critical damping

cc = 2 * sqrt(ks * ms);

%% Suspension damping

cs = zeta * cc;

fprintf('Critical damping = %.2f Ns/m\n',cc);
fprintf('Suspension damping = %.2f Ns/m\n',cs);

%% Initial conditions

xs0 = quarter_xs0;
vs0 = quarter_vs0;

xu0 = quarter_xu0;
vu0 = quarter_vu0;

X0 = [xs0; vs0; xu0; vu0];

%% Time span

t= quarter_tspan;

%% ODE Solve

%% Road profile

xr = zeros(size(t));

xr(t >= quarter_road_step_time) = quarter_road_step_height;

[t,X] = ode45( ...
    @(t,X) quarter_car_damped_ode( ...
    t,X,ms,mu,ks,kt,cs,quarter_road_step_time,quarter_road_step_height), ...
    t, X0);

%% Extract states

xs = X(:,1);
vs = X(:,2);

xu = X(:,3);
vu = X(:,4);

%% Acceleration calculation
xr = zeros(size(t));

xr(t >= quarter_road_step_time) = quarter_road_step_height;% 重建路面，不讓ode影響

dx = xs - xu;
dv = vs - vu;
xt = xu - xr;

as = -(ks/ms).*dx-(cs/ms).*dv;

%% Unsprung acceleration

au =  (ks/mu).*dx+(cs/mu).*dv-(kt/mu).*xt;
%% Energy

KE = 0.5*ms.*vs.^2 + 0.5*mu.*vu.^2;

PE = 0.5*ks.*(xs-xu).^2 + 0.5*kt.*xu.^2;

E = KE + PE;

%% Plot

figure;

subplot(4,1,1)

plot(t,xs,'LineWidth',2);
hold on;
plot(t,xu,'--','LineWidth',1.5);

grid on;

ylabel('Position (m)');

legend('Sprung','Unsprung');

title(['Quarter Car  |  \zeta = ' num2str(zeta)]);

%% Velocity

subplot(4,1,2)

plot(t,vs,'LineWidth',2);
hold on;
plot(t,vu,'--','LineWidth',1.5);

grid on;

ylabel('Velocity (m/s)');

legend('Sprung','Unsprung');

%% Acceleration

subplot(4,1,3)

plot(t,as,'LineWidth',2);
hold on;
plot(t,au,'--','LineWidth',1.5);

grid on;

xlabel('Time (s)');
ylabel('Acceleration (m/s^2)');

legend('Sprung','Unsprung');

title('Acceleration');

%% Energy

subplot(4,1,4)

plot(t,E,'LineWidth',2);

grid on;

xlabel('Time (s)');
ylabel('Energy (J)');

title('Energy Dissipation');

function dX = quarter_car_damped_ode( ...
    t,X,ms,mu,ks,kt,cs,road_step_time,road_step_height)

    %% States
    
    xs = X(1);
    vs = X(2);
    
    xu = X(3);
    vu = X(4);
    
    %% =====================================
    % Road input
    %% =====================================
    
    if t < road_step_time
        xr = 0;
    else
        xr = road_step_height;
    end
    
    %% Relative displacement / velocity
    
    dx = xs - xu;
    dv = vs - vu;
    
    %% Tire deformation
    
    xt = xu - xr;
    
    %% Accelerations
    
    as = -(ks/ms)*dx ...
         -(cs/ms)*dv;
    
    au =  (ks/mu)*dx ...
         +(cs/mu)*dv ...
         -(kt/mu)*xt;
    
    %% State derivatives
    
    dX = zeros(4,1);
    
    dX(1) = vs;
    dX(2) = as;
    
    dX(3) = vu;
    dX(4) = au;

end
