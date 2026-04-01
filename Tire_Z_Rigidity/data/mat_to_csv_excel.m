%% 批次將資料夾中的 .mat 檔轉成 Excel 與 CSV
% 轉換多種資料型態方便資料處理

clear; clc;

% 取得此 .m 檔所在資料夾
scriptDir = fileparts(mfilename('fullpath'));

inputDir  = fullfile(scriptDir, 'mat');
csvDir    = fullfile(scriptDir, 'csv');
excelDir  = fullfile(scriptDir, 'excel');

if ~exist(csvDir, 'dir');   mkdir(csvDir);   end
if ~exist(excelDir, 'dir'); mkdir(excelDir); end

disp('開始轉換')
matFiles = dir(fullfile(inputDir, '*.mat'));

if isempty(matFiles)
    error('找不到任何 .mat 檔案');
end

%% ================= 主迴圈 =================
for k = 1:length(matFiles)
    matName = matFiles(k).name;
    matPath = fullfile(inputDir, matName);
    fprintf('處理中: %s\n', matName);

    S = load(matPath);
    varNames = fieldnames(S);

    T_all = table();   % 最終合併表格

    for i = 1:numel(varNames)
        vName = varNames{i};
        data  = S.(vName);

        try
            T = convertToTable(data, vName);

            % ===== 檢查列數是否可合併 =====
            if isempty(T_all)
                T_all = T;
            else
                if height(T) ~= height(T_all)
                    warning('略過變數 %s (列數不一致)', vName);
                    %fprintf('長度: %g 與表格長度: %g 不同',T, T_all)
                    continue;
                end

                % 避免重複欄名
                T.Properties.VariableNames = matlab.lang.makeUniqueStrings( ...
                    T.Properties.VariableNames, T_all.Properties.VariableNames);

                % 橫向合併
                T_all = [T_all T];
            end

        catch ME
            warning('略過變數 %s (%s)', vName, ME.message);
        end
    end

    if isempty(T_all)
        warning('%s 沒有可輸出的資料', matName);
        continue;
    end

    % ===== 輸出 =====
    [~, baseName, ~] = fileparts(matName);

    csvPath   = fullfile(csvDir,   baseName + ".csv");
    excelPath = fullfile(excelDir, baseName + ".xlsx");

    writetable(T_all, csvPath);
    writetable(T_all, excelPath);
end

fprintf('=== 全部轉換完成 ===\n');

%% ================= 工具函式 =================
function T = convertToTable(data, varName)

    if istable(data)
        T = data;

    elseif isnumeric(data)
        if isvector(data)
            T = table(data(:), 'VariableNames', string(varName));
        else
            T = array2table(data);
            T.Properties.VariableNames = varName + "_" + string(1:width(T));
        end

    elseif isstruct(data)
        T = struct2table(data);

    elseif iscell(data)
        T = cell2table(data);
        T.Properties.VariableNames = varName + "_" + string(1:width(T));

    else
        error('不支援的資料型別');
    end
end
