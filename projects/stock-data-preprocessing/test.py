from pathlib import Path
import pandas as pd
import numpy as np
folder = Path(r"C:\Users\33459\Desktop\Yuan‘s work\AI\realdatabase\personal")
windows = pd.read_parquet(folder / "windows.parquet")
dates = pd.read_parquet(
    folder / "cut.parquet",
    columns=["order_book_id", "tradedate_no", "date"]
)
dates = dates.rename(columns={
    "tradedate_no": "end_one",
    "date": "target_date"
})
windows = windows.merge(
    dates,
    on=["order_book_id", "end_one"],
    how="left",
    validate="many_to_one"
)
windows["target_date"] = pd.to_datetime(windows["target_date"])
train_windows_set = windows[
    windows["target_date"] < "2021-01-01"
].copy()
yanzheng_windows_set = windows[
    (windows["target_date"] >= "2021-01-01")
    & (windows["target_date"] < "2022-01-01")
].copy()
test_windows_set = windows[
    windows["target_date"] >= '2022-01-01'
].copy()
# train_windows_set.to_parquet(
#     folder / "windows_train.parquet", index=False
# )
#
# yanzheng_windows_set.to_parquet(
#     folder / "windows_valid.parquet", index=False
# )
#
# test_windows_set.to_parquet(
#     folder / "windows_test.parquet", index=False
# )
