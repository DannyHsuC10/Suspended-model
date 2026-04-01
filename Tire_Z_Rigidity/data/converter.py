import os
import scipy.io
import pandas as pd
import numpy as np

# === 相對路徑 ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAT_DIR = os.path.join(BASE_DIR, "mat")
CSV_DIR = os.path.join(BASE_DIR, "csv")
EXCEL_DIR = os.path.join(BASE_DIR, "excel")

os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(EXCEL_DIR, exist_ok=True)


def mat_to_dataframe(mat_data):

    data_columns = {}

    # 先找出最大長度（通常是 59962）
    lengths = []

    for key, value in mat_data.items():
        if key.startswith("__"):
            continue

        if isinstance(value, np.ndarray):
            if value.ndim == 2 and (value.shape[0] > 1):
                lengths.append(value.shape[0])

    if not lengths:
        return None

    target_length = max(lengths)

    # 只保留長度等於 target_length 的欄位
    for key, value in mat_data.items():

        if key.startswith("__"):
            continue

        if isinstance(value, np.ndarray):

            # 只接受 column vector
            if value.ndim == 2 and value.shape[0] == target_length:
                data_columns[key] = value.flatten()

    if not data_columns:
        return None

    return pd.DataFrame(data_columns)


def convert_all_mat():

    mat_files = [f for f in os.listdir(MAT_DIR) if f.endswith(".mat")]

    if not mat_files:
        print("⚠ 沒有找到 .mat 檔案")
        return

    for file in mat_files:

        mat_path = os.path.join(MAT_DIR, file)
        filename = os.path.splitext(file)[0]

        print(f"轉換中: {file}")

        try:
            mat_data = scipy.io.loadmat(mat_path)
            df = mat_to_dataframe(mat_data)

            if df is None:
                print(f"⚠ {file} 沒有可轉換資料")
                continue

            csv_path = os.path.join(CSV_DIR, f"{filename}.csv")
            df.to_csv(csv_path, index=False)

            excel_path = os.path.join(EXCEL_DIR, f"{filename}.xlsx")
            df.to_excel(excel_path, index=False)

            print(f"✔ 完成: {filename}")

        except Exception as e:
            print(f"❌ 轉換失敗 {file} : {e}")


if __name__ == "__main__":
    convert_all_mat()