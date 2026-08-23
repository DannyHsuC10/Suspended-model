clear; clc; close all;
scriptInfo = dbstack('-completenames');
scriptDir = fileparts(scriptInfo(1).file);
addpath(scriptDir);
params = load_data(fullfile(scriptDir,'data.csv'));
paramNames = fieldnames(params);
for paramIdx = 1:numel(paramNames)
    eval([paramNames{paramIdx} ' = params.(paramNames{paramIdx});']);
end

%% =========================
% ISO 8608 Road Generation
%% =========================

% road length
L = psd_L;         % m

% spatial resolution
dx = psd_dx;       % m

x = 0:dx:L;
N = length(x);

% ISO road parameters

n0 = psd_n0;       % reference spatial freq

% ISO road class C
% A:16
% B:64
% C:256
% D:1024
Gd0 = psd_Gd0;

w = psd_w;

% Spatial frequency

dn = 1/L;

n = (0:N/2)*dn;

% avoid zero
n(1) = n(2);

% PSD

Gd = Gd0*(n/n0).^(-w);

% Random phase

phi = 2*pi*rand(size(n));

% Amplitude

A = sqrt(2*Gd*dn);

% Build spectrum

X = A .* exp(1i*phi);

% mirror
X_full = [X conj(fliplr(X(2:end-1)))];

% IFFT
road = real(ifft(X_full))*N;
x = x(1:length(road));
% Plot

figure;
plot(x,road)
xlabel('Distance (m)')
ylabel('Road Height (m)')
title('ISO Road Profile')
grid on

%% =========================
% Load velocity trace
%% =========================
data = readtable(fullfile(scriptDir, psd_speed_file));

t = data.time;
V = data.speed;
% vt plot
figure

plot(t,V,'LineWidth',1.5)

xlabel('Time (s)')
ylabel('Speed (m/s)')
title('Vehicle Speed Trace')

grid on

% Speed Distribution
figure

histogram(V,30)

xlabel('Speed (m/s)')
ylabel('Counts')

title('Speed Distribution')

grid on

% Probability Density
figure

histogram(V,30,'Normalization','pdf')

xlabel('Speed (m/s)')
ylabel('Probability Density')

title('Speed Probability Density')

grid on

%% =========================
% Excitation Frequency Analysis
%% =========================

% spatial frequencies from road PSD
n_spatial = n;

% remove very low frequency
n_spatial = n_spatial(2:end);

% speed PDF weighting
[counts,edges] = histcounts(V,psd_speed_hist_bins,'Normalization','pdf');

V_center = (edges(1:end-1)+edges(2:end))/2;

%% Build excitation frequency database

f_all = [];
w_all = [];

for i = 1:length(V_center)

    Vi = V_center(i);

    % probability weight from speed PDF
    Pv = counts(i);

    % convert spatial -> temporal frequency
    f_exc = n_spatial * Vi;

    % road PSD weighting
    road_weight = Gd(2:end);

    % total weight
    weight = Pv * road_weight;

    % accumulate
    f_all = [f_all ; f_exc(:)];

    w_all = [w_all ; weight(:)];

end


% Weighted excitation spectrum


% frequency bins
f_bins = psd_f_bins;

% weighted histogram
weighted_counts = histcounts( ...
    f_all,...
    f_bins,...
    'Normalization','count');

% apply weights manually
%weighted_counts = zeros(1,length(f_bins)-1);

for i = 1:length(f_all)

    fi = f_all(i);

    wi = w_all(i);

    idx = find(fi >= f_bins(1:end-1) & fi < f_bins(2:end),1);

    if ~isempty(idx)

        weighted_counts(idx) = weighted_counts(idx) + wi;

    end

end

%% Normalize

weighted_counts = weighted_counts / max(weighted_counts);

%% Plot

f_center = (f_bins(1:end-1)+f_bins(2:end))/2;

figure

plot(f_center,weighted_counts,'LineWidth',2)

xlabel('Excitation Frequency (Hz)')
ylabel('Normalized Energy')

title('Weighted Excitation Frequency Spectrum')

grid on

xlim([0 50])

%% =========================
% Frequency Energy Relation
%% =========================

% normalize total energy
energy = weighted_counts / sum(weighted_counts);

%% Plot

figure

plot(f_center,energy,'LineWidth',2)

xlabel('Frequency (Hz)')
ylabel('Normalized Energy')

title('Frequency vs Excitation Energy')

grid on
xlim([0 30])

%% =========================
% Cumulative Energy
%% =========================

cum_energy = cumsum(energy);

figure

plot(f_center,cum_energy,'LineWidth',2)

xlabel('Frequency (Hz)')
ylabel('Cumulative Energy')

title('Cumulative Excitation Energy')

grid on
xlim([0 30])
ylim([0 1])

%% =========================
% Find dominant energy band
%% =========================

threshold = psd_energy_threshold_factor * max(energy);

idx = energy >= threshold;

dominant_freq = f_center(idx);

fprintf('Dominant excitation band:\n')
fprintf('%.2f Hz ~ %.2f Hz\n', ...
    min(dominant_freq), ...
    max(dominant_freq));

%% 基本上iso 資料沒有特定特徵所以應該看不太出來大概確認一下
V = mean(data.speed);   % 或固定速度先看結構
t = x / V;
road_t = road;

Fs = 1/mean(diff(t));   % sampling frequency

N = length(road_t);

Y = fft(road_t);

P2 = abs(Y/N);
P1 = P2(1:floor(N/2));
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:floor(N/2)-1)/N;

figure
plot(f,P1,'LineWidth',1.5)
xlabel('Frequency (Hz)')
ylabel('Amplitude')
title('Road Profile FFT')
grid on
xlim([0 50])

figure
loglog(f,P1,'LineWidth',1.5)
grid on
xlabel('Frequency (Hz)')
ylabel('Amplitude')
title('Road FFT (log-log)')
