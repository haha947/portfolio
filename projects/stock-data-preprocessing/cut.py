import pandas as pd
import numpy as np
df_cut = pd.read_csv(r"C:\Users\33459\Desktop\Yuan‘s work\AI\realdatabase\personal\first_clean.csv")
# 设置交易日代号
df_cut["tradedate_no"] = df_cut.groupby("order_book_id").cumcount() + 1
# 输出csv文件
df_cut.to_csv(
    r"C:\Users\33459\Desktop\Yuan‘s work\AI\realdatabase\personal\cut.csv",
    index=False,
    encoding="utf-8-sig"
)
# 开始切分
batch_size = 60
batch = []
for stocks_id, group in df_cut.groupby("order_book_id", sort=False):
    first_one = int(group["tradedate_no"].iloc[0])
    last_one = int(group["tradedate_no"].iloc[-1])
    start_one = np.arange(
        first_one,
        last_one - batch_size + 2
    )
    piece_windows = pd.DataFrame({
        "order_book_id": stocks_id,
        "start_one": start_one,
        "end_one": start_one + batch_size - 1
    })
    batch.append(piece_windows)
All_windows = pd.concat(batch, ignore_index=True)
unnormal_count = (
    df_cut.groupby("order_book_id")["unnormal"].transform(
        lambda s: (
            s.iloc[::-1].rolling(window=batch_size, min_periods=batch_size)
            .sum().iloc[::-1]
        )
    )
)
check_list = df_cut[["order_book_id", "tradedate_no"]].copy()
check_list["unnormal_count"] = unnormal_count
check_list = check_list.rename(
    columns={"tradedate_no": "start_one"}
)
All_windows = All_windows.merge(
    check_list,
    on=["order_book_id", "start_one"],
    how="left",
    validate="one_to_one"
)
# 删除unnormal数大于等于1的窗口
useful_windows = All_windows[
    All_windows["unnormal_count"] == 0
].copy()
useful_windows.to_csv(r"C:\Users\33459\Desktop\Yuan‘s work\AI\realdatabase\personal\windows.csv", index=False)
