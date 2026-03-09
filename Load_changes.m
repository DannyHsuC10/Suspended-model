clc; clear;
addpath('wheel_load_tools');
%% -------------------------------
% 車輛參數
%% -------------------------------
g = 9.81;
car.m = 309.5;
car.h = 0.284;
car.L = 1.55;
car.d = 1.25;

car.CG_x = [0.4;0.6]; 
car.CG_y = [0.5,0.5];

car.F_add = [200,50,20];      % 外力 N
car.CF_rela = [0.0;0.0;0.0];  % 外力作用點

%% -------------------------------
% 加速度範圍
%% -------------------------------
ax_range = linspace(-2*g, 2*g, 50);
ay_range = linspace(-2*g, 2*g, 50);
[AX, AY] = meshgrid(ax_range, ay_range);

%% -------------------------------
% 預分配四輪差值矩陣
%% -------------------------------
FL = zeros(size(AX));
FR = zeros(size(AX));
RL = zeros(size(AX));
RR = zeros(size(AX));

%% -------------------------------
% 計算四輪差值
%% -------------------------------
for i = 1:numel(AX)
    car.ax = AX(i);  
    car.ay = AY(i);
    
    N = Four_wheel_load_LSM(car,false);
    %N = Four_wheel_load(car,false);
    
    FL(i) = N(1);
    FR(i) = N(2);
    RL(i) = N(3);
    RR(i) = N(4);
end

%% -------------------------------
% 畫差值曲面
%% -------------------------------
figure();

wheel_names = {'FL','FR','RL','RR'};
Diff_data = {FL, FR, RL, RR};

for k = 1:4
    subplot(2,2,k)
    surf(AX, AY, Diff_data{k}, 'EdgeColor','none')
    xlabel('ax (m/s^2)'); ylabel('ay (m/s^2)'); zlabel('F(N)');
    title([wheel_names{k} '4W Load']);
    view(45,30);
    grid on;
    shading interp;
end

sgtitle('Four Wheel Load vs ax and ay');