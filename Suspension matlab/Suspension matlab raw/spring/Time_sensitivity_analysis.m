%% Explicit Euler
% Time Step Sensitivity Analysis
clear; clc; close all;

%% Parameters

m = 250/4;      % kg
k = 40000;      % N/m

%% Initial conditions

x0 = 0.05;      % m
v0 = 0;         % m/s

%% Time settings

t_end = 5;

dt_list = [1e-2 1e-3 1e-4 1e-5];

%% Loop for different dt

for d = 1:length(dt_list)

    dt = dt_list(d);

    t = 0:dt:t_end;
    N = length(t);

    %% Initialize

    x = zeros(1,N);
    v = zeros(1,N);
    a = zeros(1,N);

    x(1) = x0;
    v(1) = v0;

    %% Explicit Euler

    for i = 1:N-1

        % acceleration
        a(i) = -(k/m)*x(i);

        % velocity update
        v(i+1) = v(i) + a(i)*dt;

        % position update
        x(i+1) = x(i) + v(i)*dt;

    end

    %% Final acceleration

    a(N) = -(k/m)*x(N);

    %% Energy calculation

    KE = 0.5 * m .* v.^2;
    PE = 0.5 * k .* x.^2;

    E_total = KE + PE;

    E0 = E_total(1);

    %% Energy error %

    E_error_percent = ...
        (E_total - E0)/E0 * 100;

    %% =====================================
    % Plot
    %% =====================================

    figure('Name',['dt = ' num2str(dt)]);

    %% Displacement

    subplot(3,1,1)

    plot(t,x,'LineWidth',2);

    grid on;

    ylabel('Displacement (m)');

    title(['Explicit Euler  |  dt = ' num2str(dt)]);

    %% Total Energy

    subplot(3,1,2)

    plot(t,E_total,'LineWidth',2);

    grid on;

    ylabel('Energy (J)');

    %% Energy Error

    subplot(3,1,3)

    plot(t,E_error_percent,'LineWidth',2);

    grid on;

    xlabel('Time (s)');
    ylabel('Energy Error (%)');

end
