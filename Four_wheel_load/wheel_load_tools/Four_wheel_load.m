%% 4輪載重計算 (重心分配法)
function  N = Four_wheel_load(car,check)

    g = 9.81;
    W = car.m*g; % 重量
    dF = car.m*car.h*[car.ax,car.ay]./[car.L,car.d]; % (x,y)方向轉移
    
    % 若有外力
    if isfield(car,'F_add') && isfield(car,'CF_rela')
        r = car.CF_rela; % 外力作用點
        F = car.F_add;   % 外力向量 [Fx,Fy,Fz]
        % 外力對力矩的貢獻
        Mx_add = r(2)*F(3) - r(3)*F(2); % roll
        My_add = r(3)*F(1) - r(1)*F(3); % pitch
        % 對應到 dF
        dF = dF + [My_add/car.L, Mx_add/car.d];
    end

    % 靜態載重 (2x2矩陣: 前/後 × 左/右)
    Fs = W * (car.CG_x * car.CG_y);  % 重量分布
    % F =
    % [FL, FR
    %  RL, RR]
    
    % 縱向載重轉移分y(1,x) + 橫向載重轉移(2,y)分x
    F = Fs + dF(1) * [-car.CG_y; car.CG_y] + dF(2) * [car.CG_x, -car.CG_x];
    
    N = [F(1,1); F(1,2); F(2,1); F(2,2)];
    if check == true

        % 輸出結果
        fprintf('四輪載重 (N):\n');
        fprintf('FL = %.1f, FR = %.1f, RL = %.1f, RR = %.1f\n', F(1,1), F(1,2), F(2,1), F(2,2));
        fprintf('總載重差: %.6f N\n', sum(F(:)) - W);
    end
end

%% 使用範例
%N = Four_wheel_load(car,true);% false
%{
-------------------------------
% 車輛參數

car.m = 309.5; 
g = 9.81; 
car.h = 0.284; 
car.L = 1.55; 
car.d = 1.25;
car.ax = 0.3*g; 
car.ay = 1.5*g;

car.F_add = [0,0,0];%(x,y,z)N

% 重心
car.CG_x = [0.48; 0.52];  % 前/後軸分布
car.CG_y = [0.5, 0.5];  % 左/右輪分布
% 空力
car.CF_rela = [0.0;0.0;0.0];  % 相對於重心(x,y,z)m
%}
