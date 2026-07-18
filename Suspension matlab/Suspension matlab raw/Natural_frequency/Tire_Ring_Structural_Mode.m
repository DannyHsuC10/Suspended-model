clc;
clear;

%% data

R = 0.20;          % radius [m]
E = 8e6;           % rubber modulus [Pa]
V = 2.6e-3;        %體積
m = 3.6;        %直量
rho = m/V;        % density [kg/m^3]
A = 2500e-6;    % 截面積
I = 1.78e-5;   % 截面二次矩

mode_max = 8;

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