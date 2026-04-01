
% 慣性設定
g = 9.81;% 重力量
ms = 310/4;% 車重
mu = 15-4;% 簧下

% 彈簧設定
ks = 70000;
kt = 99000;
c = 4000;
vs = 0;
vu = 0;


% 初始設定
Fu_i = -(ms+mu)*g; % 簧下力
Fs_i = -ms*g; % 簧上力

zu = Fu_i / kt; % 簧下壓縮
zs = zu + (Fs_i/ ks); % 簧上位移

zr = 0;

dt = 0.00001;
t = 0;

as_list = [];
zs_list = [];
t_list = [];



for i = 1:dt:5

    if t > 1
        zr = 0.05;
    else
        zr = 0;
    end

    Fs = ks*(zu-zs);
    Fd = c*(vu-vs);
    Ft = kt*(zr-zu);
    as = (-ms*g+Fs+Fd)/ms;
    au = (-mu*g-Fs-Fd+Ft)/mu;


    t = t + dt;  % Increment time
    
    % Update velocities and positions
    vs = vs + as * dt;  % Update speed of the spring
    vu = vu + au * dt;  % Update speed of the upper mass
    zs = zs + vs * dt;  % Update position of the spring
    zu = zu + vu * dt;  % Update position of the upper mass
    
    % update list
    as_list(end+1) = as;  % Append current acceleration of the spring to the list
    zs_list(end+1) = zs;  % Append current position of the spring to the list
    t_list(end+1) = t;

end

figure
plot(t_list, zs_list);
xlabel('Time (s)');
ylabel('Position of Spring (m)');
title('Position of Spring Over Time');
grid on;

figure
plot(t_list, as_list);
xlabel('Time (s)');
ylabel('a (m/s^2)');
title('a Over Time');
grid on;
