% Tire + Suspension Coupled System
% ODE-based solver
% 注意!! 這個模型有點偷懶，我在初始狀態直接移動輪胎，讓系統直接從不平衡狀態開始出發

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

ms = tire_ms;      % sprung mass (kg)
mu = tire_mu;      % unsprung mass (kg)

ks = tire_ks;      % suspension spring (N/m)
kt = tire_kt;      % tire stiffness (N/m)

%% Initial conditions

xs0 = tire_xs0;    % body displacement
vs0 = tire_vs0;

xu0 = tire_xu0;    % wheel displacement
vu0 = tire_vu0;

X0 = [xs0; vs0; xu0; vu0];

%% Time span

tspan = tire_tspan;

%% ODE solve

[t,X] = ode45(@(t,X) quarter_car_ode(t,X,ms,mu,ks,kt), tspan, X0);

%% Extract states

xs = X(:,1);
vs = X(:,2);
xu = X(:,3);
vu = X(:,4);

%% Energy (for validation)

KE = 0.5*ms.*vs.^2 + 0.5*mu.*vu.^2;
PE = 0.5*ks.*(xs - xu).^2 + 0.5*kt.*(xu).^2;

E = KE + PE;

E0 = E(1);
E_error = (E - E0)/E0 * 100;

%% Plot

figure;

subplot(3,1,1)
plot(t,xs,'LineWidth',2); hold on;
plot(t,xu,'--','LineWidth',1.5);
grid on;
ylabel('Position (m)');
legend('Sprung','Unsprung');

title('Quarter Car (No Damping) - ODE Solution');

subplot(3,1,2)
plot(t,E,'LineWidth',2);
grid on;
ylabel('Total Energy (J)');

subplot(3,1,3)
plot(t,E_error,'LineWidth',2);
grid on;
xlabel('Time (s)');
ylabel('Energy Error (%)');

function dX = quarter_car_ode(~,X,ms,mu,ks,kt)

xs = X(1);
vs = X(2);
xu = X(3);
vu = X(4);

%% Sprung mass acceleration
as = -(ks/ms)*(xs - xu);

%% Unsprung mass acceleration
au = (ks/mu)*(xs - xu) - (kt/mu)*xu;

%% State derivatives

dX = zeros(4,1);

dX(1) = vs;
dX(2) = as;
dX(3) = vu;
dX(4) = au;

end

