import pandas as pd
import numpy as np
df_raw = pd.read_csv(r"C:\Users\33459\Desktop\Yuan‘s work\AI\realdatabase\500data.csv")
df_work = df_raw.copy()
# 规则一：保留第一个有效日及以后的数据，删除之前的无效数据
features = ["open", "close", "high", "low", "turnover_rate", "total_turnover", "volume", "adjustment_factor"]
df_work["is_real"] = df_work[features].notna().all(axis=1)
df_work["date"] = pd.to_datetime(df_work["date"])
df_work = df_work.sort_values(["order_book_id", "date"])
valid_date = df_work[df_work["is_real"]]
first_date = valid_date.drop_duplicates(
    subset="order_book_id",
    keep="first"
)
first_date = first_date[["order_book_id", "date"]].rename(
    columns={"date": "first_dates"}
)
df_combine = df_work.merge(
    first_date,
    on="order_book_id",
    how="inner"
)
df_combine = df_combine[df_combine["date"] >= df_combine["first_dates"]].copy()
# 异常清洗
df_combine["unnormal"] = False
# 异常1：最高值小于最低值、开盘价、收盘价
df_combine.loc[
    (df_combine["high"] < df_combine["low"]) |
    (df_combine["high"] < df_combine["close"]) |
    (df_combine["high"] < df_combine["open"]),
    "unnormal"
] = True
# 异常2：最低价不能高于开盘价、收盘价
df_combine.loc[
    (df_combine["low"] > df_combine["open"]) |
    (df_combine["low"] > df_combine["close"]),
    "unnormal"
] = True
# 异常3：features的值都不应该小于0
df_combine.loc[
    df_combine[features].le(0).any(axis=1),
    "unnormal"
] = True
# 异常4：任意值缺失即为异常
df_combine.loc[
    df_combine[features].isna().any(axis=1),
    "unnormal"
] = True
# 检测无穷大、换手率、重复值、无法识别问题
# duplicates = df_combine.duplicated(
#     subset=["order_book_id", "date"],
#     keep=False
# )
#
# print(duplicates.sum())
# suspicious = (
#     (df_combine["volume"] > 0) &
#     (df_combine["total_turnover"] > 0) &
#     (df_combine["turnover_rate"] == 0)
# )
#
# print(suspicious.sum())
# if_inf = df_combine[features].isin(
#     [np.inf, -np.inf]
# ).any(axis=1)
# print(if_inf.sum())
#
# un_read = (
#     df_combine["order_book_id"].isna()
#     | pd.to_datetime(df_combine["date"], errors="coerce").isna()
# )
#
# print(un_read.sum())
# 统计目前有多少异常值和正常值
# print((df_combine["unnormal"] == False).sum())
# print(df_combine["unnormal"].sum())
# 异常值第一次置空
df_combine.loc[
    df_combine["unnormal"], features
] = np.nan
# 成交额成交量
accept_error = 0.01
df_combine["mid_price"] = df_combine["total_turnover"]/df_combine["volume"]
df_combine.loc[
    (df_combine["mid_price"] > df_combine["high"] + accept_error) |
    (df_combine["mid_price"] < df_combine["low"] - accept_error),
    "unnormal"
] = True
df_combine.loc[
    df_combine["unnormal"], features + ["mid_price"]
] = np.nan

need_adj_col = ["open", "close", "high", "low", "mid_price"]
for col in need_adj_col:
    df_combine[f"adj_{col}"] = (df_combine[col] * df_combine["adjustment_factor"])
# 输出csv
df_combine.to_csv(
    r"C:\Users\33459\Desktop\Yuan‘s work\AI\realdatabase\personal\first_clean.csv",
    index=False,
    encoding="utf-8-sig"
)
