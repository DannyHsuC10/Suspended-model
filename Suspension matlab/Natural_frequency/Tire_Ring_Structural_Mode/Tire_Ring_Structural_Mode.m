clc;
clear;
scriptInfo = dbstack('-completenames');
scriptDir = fileparts(scriptInfo(1).file);
addpath(scriptDir);
params = load_data(fullfile(scriptDir,'data.csv'));
paramNames = fieldnames(params);
for paramIdx = 1:numel(paramNames)
    eval([paramNames{paramIdx} ' = params.(paramNames{paramIdx});']);
end

%% data

R = tire_R;        % radius [m]
E = tire_E;        % rubber modulus [Pa]
V = tire_V;        % 體積
m = tire_m;        % 直量
rho = m/V;        % density [kg/m^3]
A = tire_A;      % 截面積
I = tire_I;      % 截面二次矩

mode_max = tire_mode_max;

%% 計算
freq = zeros(mode_max,1);

fprintf('Mode   Frequency (Hz)\n');
fprintf('----------------------\n');

for n = 1:mode_max

    if n == 1
        freq(n) = 0; % rigid-body mode
        fprintf('%2d     %.2f\n', n, freq(n));
        continue;
    end

    % classical ring bending scaling (stable form)
    omega = sqrt( (E*I)/(rho*A*R^4) ) * (n^2*(n^2-1));

    freq(n) = omega/(2*pi);

    fprintf('%2d     %.2f\n', n, freq(n));

end
% plot
figure;
plot(1:mode_max, freq, '-o');
xlabel('Mode Number');
ylabel('Frequency (Hz)');
title('Tire Ring Mode Frequencies');
grid on;
