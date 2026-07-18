%% 車輛參數讀取器
function dataStruct = load_data(filename)
    % 讀取 CSV 檔案，假設有兩欄：name 和 value
    % filename: CSV 檔案路徑
    % 會直接在 base workspace 建立變數
    
    % 讀取表格
    tbl = readtable(filename, 'TextType', 'string');
    
    % 檢查是否有 name 和 value 欄位
    if ~all(ismember({'name','value'}, tbl.Properties.VariableNames))
        error('CSV 檔案必須包含 name 和 value 欄位');
    end
    
    % 將每一列的 name/value 指派到 base workspace
    for i = 1:height(tbl)
        varName = matlab.lang.makeValidName(tbl.name(i)); % 確保合法變數名稱
        varValue = tbl.value(i);

        assignin('base', varName, varValue);

        %dataStruct.(varName) = varValue; %看要不要回傳
    end
end