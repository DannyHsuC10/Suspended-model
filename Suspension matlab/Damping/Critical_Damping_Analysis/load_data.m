%% Vehicle parameter loader
function dataStruct = load_data(filename)
    warningState = warning('query', 'all');
    warning('off', 'all');
    cleanup = onCleanup(@() warning(warningState));

    raw = readcell(filename, 'TextType', 'string');
    headers = string(raw(1,:));
    nameCol = find(headers == "name", 1);
    valueCol = find(headers == "value", 1);

    if isempty(nameCol) || isempty(valueCol)
        error('CSV file must contain name and value columns.');
    end

    dataStruct = struct();

    for i = 2:size(raw,1)
        if ismissing(string(raw{i,nameCol})) || strlength(strtrim(string(raw{i,nameCol}))) == 0
            continue;
        end

        varName = matlab.lang.makeValidName(string(raw{i,nameCol}));
        varValue = parse_value(raw{i,valueCol});
        assignin('caller', varName, varValue);
        assignin('base', varName, varValue);
        dataStruct.(varName) = varValue;
    end
end

function value = parse_value(rawValue)
    if ismissing(string(rawValue))
        value = [];
        return;
    end

    if isnumeric(rawValue) || islogical(rawValue)
        value = rawValue;
        return;
    end

    rawText = strtrim(char(rawValue));
    if isempty(rawText)
        value = [];
        return;
    end

    if (startsWith(rawText, "'") && endsWith(rawText, "'")) || ...
       (startsWith(rawText, '"') && endsWith(rawText, '"'))
        value = rawText(2:end-1);
        return;
    end

    [numericValue, ok] = str2num(rawText); %#ok<ST2NM>
    if ok
        value = numericValue;
    else
        value = rawText;
    end
end
