from pathlib import Path
import pandas as pd
# import numpy as np
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
# df_cut = pd.read_parquet(folder / "cut.parquet")
#
# print(df_cut.head(5).to_string(index=False))
# 打标签
target_cols = [
    "adj_open", "adj_close", "adj_high", "adj_low", "turnover_rate", "total_turnover", "volume"
]
new_labels = pd.read_parquet(
    folder / "cut.parquet",
    columns=["order_book_id", "tradedate_no"] + target_cols
)
rename_group = {
    "tradedate_no": "end_date"
}
for col in target_cols:
    rename_group[col] = f"y_{col}"
new_labels = new_labels.rename(columns=rename_group)
new_labels_cols = [f"y_{col}" for col in target_cols]
for name, subset in [
    ["train", train_windows_set],
    ["yanzheng", yanzheng_windows_set],
    ["test", test_windows_set]
]:
    lable_windows = subset.merge(
        new_labels,
        on=["order_book_id", "end_date"],
        how="left",
        validate="many_to_one"
    )
    lable_windows.to_parquet(
        folder / f"windows_{name}_labels.parquet",
        index=False
    )
