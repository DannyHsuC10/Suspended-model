# 車輪剛性計算與比較
* [最終結果](result.md)

## 主要執行腳本
本工具主要功能為分析輪胎剛性，雖然TTC已經有提供spring rate，但是我們還是可以自行分析看看效果。另外資料處理與資料過濾前兩步驟其實使用與輪胎模型同一個模組，所以使用方法和改進方向是一樣的。

主要執行腳本會進行以下步驟 : 
> 1. 呼叫資料過濾器
> 2. 進行線性回歸
> 3. 繪圖並產生結果報告>>[最終結果](result.md)

## 1. 資料處理
* [mat to csv & excel](data/introduction/mat_to_excel_csv.md) 資料轉換器 : 處理資料轉換成excel和csv

## 2. 資料過濾

1. [json檔](Filter/introduction/json.md)過濾條件 : 這裡是用來改清理資料的條件用的
1. [filter](Filter/introduction/Filter.md) 過濾器 : 過濾資料並整理要用的東西。如果檔名和路徑有改這邊需要更新

* [資料比較圖](Figures/data_comparison.md) : 點下去就可以看，用[data comparator](Filter/introduction/data_comparator.md)可以更新資料，想看什麼自行調整。(但因為數據不外流沒有開放圖形資料，執行後會自動更新)
## 3. 線性回歸
* [線性回歸](Fitter/introduction/linear_regression.md)可以幫助我們從一大堆資料點數據中找出輪胎的線性剛性

## 後續方向
1. 剛性擬和 : 其實真實輪胎其實不一定會是線性剛性，也許可以嘗試(指數、多項式等)並比較殘差。
1. 更多分析 : 工具做好了其實可以用來把同個輪胎的更多找出鋼性關係