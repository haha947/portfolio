from pathlib import Path
import pandas as pd
folder = Path(r"C:\Users\33459\Desktop\Yuan‘s work\AI\realdatabase\personal")
for name in ["cut", "windows"]:
    df = pd.read_csv(folder / f"{name}.csv")
    output_path = folder / f"{name}.parquet"
    df.to_parquet(output_path, engine="pyarrow", index=False)
# for name in ["cut", "windows"]:
#     df = pd.read_parquet(folder / f"{name}.parquet")
#     print(df.columns.tolist())
