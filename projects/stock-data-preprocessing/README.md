# 股票数据清洗与滑动窗口构建 · Personal Project

本个人项目使用 Python 对股票日频数据进行清洗、复权价格计算、60 个交易日滑动窗口筛选，以及按日期划分训练、验证和测试窗口。

## 文件说明

| 脚本 | 功能 |
| --- | --- |
| `clean.py` | 从每只股票首个完整有效日开始保留数据，标记价格关系、非正数、缺失值及成交均价异常，并计算复权价格。 |
| `cut.py` | 生成交易日序号，构建 60 日滑动窗口，剔除含异常记录的窗口。 |
| `convert.py` | 将 `cut.csv` 和 `windows.csv` 转换为 Parquet。 |
| `test.py` | 按窗口结束日期划分训练集（2021 年以前）、验证集（2021 年）及测试集（2022 年起）。 |

## 全部结果文件

[下载 Personal-Project-Results.zip](https://github.com/haha947/portfolio/releases/download/personal-project-v1/Personal-Project-Results.zip)

压缩包保留 `personal` 文件夹中的全部 8 个文件：

- `first_clean.csv`
- `cut.csv`
- `cut.parquet`
- `windows.csv`
- `windows.parquet`
- `windows_train.parquet`
- `windows_valid.parquet`
- `windows_test.parquet`

结果文件较大，因此通过本仓库的 GitHub Release 提供下载。

## 运行说明

依赖 Python、pandas、numpy 和 pyarrow。脚本按 `clean.py` → `cut.py` → `convert.py` → `test.py` 的顺序处理数据。

当前提交保留原始脚本：运行前需要将脚本中的本机绝对路径改为自己的数据路径；输入原始文件为 `500data.csv`，未包含在此次上传范围中。`test.py` 中的三个输出语句目前处于注释状态，重新导出划分结果时需要取消注释。

这些脚本和结果展示数据预处理与窗口划分流程，尚未包含模型训练或效果评估。