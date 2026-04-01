%% 最小作用量原理求解靜不定系統
function  N = Four_wheel_load_LSM(car,check)

    az = -9.81;        % 垂直加速度 (重力)
    
    % 車輛坐標系(重心當作0,0) 因為CG定義是比例分配所以必須與槓桿關係相反
    x_pos = car.L*[car.CG_x(2),car.CG_x(2),-car.CG_x(1),-car.CG_x(1)];       % FL, FR, RL, RR
    y_pos = car.d*[-car.CG_y(2),car.CG_y(1),-car.CG_y(2),car.CG_y(1)]; 
    z_pos = [1,1,1,1];% 垂直力平衡
    
    % 建立平衡方程
    A = [z_pos;y_pos;x_pos];
    
    % 慣性力相反 F + ma = 0 >> F = -ma
    b = car.m*[az ; car.ay*car.h ; car.ax*car.h];
    
    % 若有外力，加入外力作用
    if isfield(car,'F_add') && isfield(car,'CF_rela')
        r = car.CF_rela; % 外力作用點相對重心
        F = car.F_add;   % 外力向量 [Fx,Fy,Fz]
        % 外力對力矩的貢獻
        Mx_add = r(2)*F(3) - r(3)*F(2);
        My_add = r(3)*F(1) - r(1)*F(3);
        % 加到右邊
        b = b + [F(3); Mx_add; My_add];
    end

    % 利用最小作用量原理求解
    N = A' * ((A*A')\-b);

    %% 檢查
    if check == true
        
        fprintf('輪胎載重 (N):\n');
        fprintf('FL = %.1f, FR = %.1f, RL = %.1f, RR = %.1f\n', N(1), N(2), N(3), N(4));
        %平衡確認
        Fz = sum(N)+car.m*az+(isfield(car,'F_add')*car.F_add(3));
        fprintf('平衡確認 : Fz = %.2f N \n', Fz);

        % 力矩平衡檢查
        Mx = y_pos * N + car.m*car.ay*car.h;
        My = x_pos * N + car.m*car.ax*car.h;
        if isfield(car,'F_add')
            Mx = Mx + Mx_add;
            My = My + My_add;
        end
        fprintf('Roll moment balance (Mx) = %.6f Nm\n', Mx);
        fprintf('Pitch moment balance (My) = %.6f Nm\n', My);
    end
end

%% 使用範例
%N = Four_wheel_load_LSM(car,true);% false
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
