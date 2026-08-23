classdef VehicleDynamicsSimulator
    properties
        g         % 重力加速度
        m         % 車重 (kg)
        h         % 重心高度 (m)
        W         % 車重力 (N)
        L_rear    % 後軸到重心距離 (m)
        L_front   % 前軸到重心距離 (m)
        L         % 軸距 (m)
        t_front   % 前輪距 (m)
        t_rear    % 後輪距 (m)
        K         % Ride rate 矩陣 (4x4)
        K_modal   % 模態剛性矩陣 (3x3)
        K_modal_coupled % 耦合模態剛性矩陣
        K_tire    % 輪胎剛性 (1x4)
    end
    
    methods
        % =====================================================================
        % Constructor (建構子) - 初始化參數
        % =====================================================================
        function obj = VehicleDynamicsSimulator(g_val)
            if nargin < 1
                obj.g = 9.81;
            else
                obj.g = g_val;
            end
            
            % 車輛基本參數定義
            obj.m = 360;
            obj.h = 0.286;
            obj.W = obj.m * obj.g;
            obj.L_rear = 0.744;
            obj.L_front = 0.806;
            obj.L = obj.L_front + obj.L_rear;
            
            obj.t_front = 1.25;
            obj.t_rear = 1.25;
            
            obj.K = [30000, 0, 0, 0;
                     0, 30000, 0, 0;
                     0, 0, 27000, 0;
                     0, 0, 0, 27000];
                 
            obj.K_modal = [3050, 0, 0;
                           0, 550, 0;
                           0, 0, 2500];
                       
            obj.K_modal_coupled = [3050, 0, 0, 0;
                                   0, 600 + 2900, -2900, 0;
                                   0, -2900, 500 + 2900, 0;
                                   0, 0, 0, 2500];
                               
            obj.K_tire = ones(1, 4) * 56000;
        end
        
        % =====================================================================
        % 內部輔助工具 (幾何、外力矩、Debug)
        % =====================================================================
        function [x_pos, y_pos, z_pos] = get_geometry(obj)
            x_front = obj.L_front;
            x_rear  = -obj.L_rear;
            
            y_left  = -obj.t_front / 2;
            y_right =  obj.t_front / 2;
            
            y_left_r  = -obj.t_rear / 2;
            y_right_r =  obj.t_rear / 2;
            
            x_pos = [x_front, x_front, x_rear, x_rear];
            y_pos = [y_left, y_right, y_left_r, y_right_r];
            z_pos = ones(1, 4);
        end
        
        function [Fz_val, Mx, My] = external_effects(obj, F_add, CF_rela)
            if isempty(F_add)
                Fz_val = 0; Mx = 0; My = 0;
                return;
            end
            Fx = F_add(1); Fy = F_add(2); Fz = F_add(3);
            if isempty(CF_rela)
                r = [0, 0, obj.h];
            else
                r = CF_rela;
            end
            Mx = r(2)*Fz - r(3)*Fy;
            My = r(3)*Fx - r(1)*Fz;
            Fz_val = Fz;
        end
        
        function [A, b, Mx_add, My_add] = get_Ab(obj, ax, ay, F_add, CF_rela)
            if nargin < 4, F_add = []; end
            if nargin < 5, CF_rela = []; end
            
            [x_pos, y_pos, ~] = obj.get_geometry();
            [Fz_add, Mx_add, My_add] = obj.external_effects(F_add, CF_rela);
            
            A = [1,        1,        1,        1;
                 y_pos(1), y_pos(2), y_pos(3), y_pos(4);
                 x_pos(1), x_pos(2), x_pos(3), x_pos(4)];
             
            b = [Fz_add - obj.m * obj.g;
                 obj.m * ay * obj.h + Mx_add;
                 obj.m * ax * obj.h + My_add];
        end
        
        function debug_balance(obj, ax, ay, F_add, N, x_pos, y_pos, Mx_add, My_add)
            if isempty(F_add), F_add = [0, 0, 0]; end
            az = -obj.g;
            
            fprintf('輪胎載重 (N):\n');
            fprintf('FL = %.1f, FR = %.1f, RL = %.1f, RR = %.1f\n', N(1), N(2), N(3), N(4));
            
            Fz = sum(N) + obj.m * az + F_add(3);
            fprintf('平衡確認 : Fz = %.6f N\n', Fz);
            
            % 確保這裡 N 是直向量 (4x1) 以利矩陣乘法
            Mx = y_pos * N + obj.m * ay * obj.h + Mx_add;
            My = x_pos * N + obj.m * ax * obj.h + My_add;
            
            fprintf('Roll moment balance (Mx) = %.6f Nm\n', Mx);
            fprintf('Pitch moment balance (My) = %.6f Nm\n', My);
        end
        
        % =====================================================================
        % 核心求解器 (Solvers)
        % =====================================================================
        function N = solve_cg(obj, ax, ay, F_add, CF_rela, check)
            if nargin < 4, F_add = []; end
            if nargin < 5, CF_rela = []; end
            if nargin < 6, check = false; end
            
            F_z_front_static = obj.W * (obj.L_rear / obj.L);
            F_z_rear_static  = obj.W * (obj.L_front / obj.L);
            
            dF_z_long = obj.m * obj.h * ax / obj.L;
            [~, Mx_add, My_add] = obj.external_effects(F_add, CF_rela);
            dF_z_long = dF_z_long + My_add / obj.L;
            
            dF_z_lat_f = (obj.m * ay * obj.h * (obj.L_rear / obj.L)) / obj.t_front;
            dF_z_lat_r = (obj.m * ay * obj.h * (obj.L_front / obj.L)) / obj.t_rear;
            
            dF_z_lat_f = dF_z_lat_f + (Mx_add * obj.L_rear / obj.L) / obj.t_front;
            dF_z_lat_r = dF_z_lat_r + (Mx_add * obj.L_front / obj.L) / obj.t_rear;
            
            N_fl = 0.5 * F_z_front_static - 0.5 * dF_z_long + dF_z_lat_f;
            N_fr = 0.5 * F_z_front_static - 0.5 * dF_z_long - dF_z_lat_f;
            N_rl = 0.5 * F_z_rear_static  + 0.5 * dF_z_long + dF_z_lat_r;
            N_rr = 0.5 * F_z_rear_static  + 0.5 * dF_z_long - dF_z_lat_r;
            
            N = [N_fl; N_fr; N_rl; N_rr]; % 回傳 4x1 直向量
            
            if check
                fprintf('\n=== CG Solver Results ===\n');
                [x_pos, y_pos, ~] = obj.get_geometry();
                obj.debug_balance(ax, ay, F_add, N, x_pos, y_pos, Mx_add, My_add);
            end
        end
        
        function N = solve_lsm(obj, ax, ay, F_add, CF_rela, check)
            if nargin < 4, F_add = []; end
            if nargin < 5, CF_rela = []; end
            if nargin < 6, check = false; end
            
            [A, b, Mx_add, My_add] = obj.get_Ab(ax, ay, F_add, CF_rela);
            % MATLAB 的 \ (backslash) 是最有效率且穩定的矩陣求解法
            % Python 的 A.T @ np.linalg.solve(A @ A.T, -b) 寫成 MATLAB 如下：
            N = A' * ((A * A') \ (-b));
            
            if check
                fprintf('\n=== LSM Solver Results ===\n');
                [x_pos, y_pos, ~] = obj.get_geometry();
                obj.debug_balance(ax, ay, F_add, N, x_pos, y_pos, Mx_add, My_add);
            end
        end
        
        function N = solve_lagrange(obj, ax, ay, F_add, CF_rela, check)
            if nargin < 4, F_add = []; end
            if nargin < 5, CF_rela = []; end
            if nargin < 6, check = false; end
            
            [x_pos, y_pos, ~] = obj.get_geometry();
            [A, b, Mx_add, My_add] = obj.get_Ab(ax, ay, F_add, CF_rela);
            
            N = obj.K * A' * ((A * obj.K * A') \ (-b));
            
            if check
                fprintf('\n=== Weighted Lagrange ===\n');
                obj.debug_balance(ax, ay, F_add, N, x_pos, y_pos, Mx_add, My_add);
            end
        end
        
        function N = solve_suspension(obj, ax, ay, F_add, CF_rela, check)
            if nargin < 4, F_add = []; end
            if nargin < 5, CF_rela = []; end
            if nargin < 6, check = false; end
            
            [x_pos, y_pos, ~] = obj.get_geometry();
            
            B = [ones(1, 4); y_pos; -x_pos]; 
            b = obj.m * [-obj.g; ay * obj.h; ax * obj.h];
            [Fz_add, Mx_add, My_add] = obj.external_effects(F_add, CF_rela);
            b = b + [Fz_add; Mx_add; My_add];
            
            A = [ones(1, 4); y_pos; x_pos];
            M = A * obj.K * B';
            q = M \ (-b);
            
            dz = B' * q;
            N = obj.K * dz;
            
            if check
                fprintf('\n=== Suspension Model ===\n');
                f_add_debug = F_add; if isempty(f_add_debug), f_add_debug = zeros(1,3); end
                obj.debug_balance(ax, ay, f_add_debug, N, x_pos, y_pos, Mx_add, My_add);
            end
        end
        
        function N = solve_decoupled(obj, ax, ay, F_add, CF_rela, check)
            if nargin < 4, F_add = []; end
            if nargin < 5, CF_rela = []; end
            if nargin < 6, check = false; end
            
            [x_pos, y_pos, ~] = obj.get_geometry();
            
            B = [ones(1, 4); y_pos; -x_pos];
            b = obj.m * [-obj.g; ay * obj.h; ax * obj.h];
            [Fz_add, Mx_add, My_add] = obj.external_effects(F_add, CF_rela);
            b = b + [Fz_add; Mx_add; My_add];
            
            A = [ones(1, 4); y_pos; x_pos];
            M = A * B' * obj.K_modal;
            q = M \ (-b);
            
            N = B' * (obj.K_modal * q);
            
            if check
                fprintf('\n=== Decoupled Suspension Model ===\n');
                f_add_debug = F_add; if isempty(f_add_debug), f_add_debug = zeros(1,3); end
                obj.debug_balance(ax, ay, f_add_debug, N, x_pos, y_pos, Mx_add, My_add);
            end
        end
    end
end