# 基于 Transformer 的 A 股预测 · Personal Project

本个人项目旨在探索 Transformer 在 A 股预测中的应用。

**当前进展：** 目前已完成数据清洗、滑动窗口构建及训练集、验证集和测试集划分，正在搭建 Transformer 预测模型。

已完成的数据处理包括股票日频数据清洗、复权价格计算、60 个交易日滑动窗口筛选，以及按日期划分训练、验证和测试窗口。

## 文件说明

| 脚本 | 功能 |
| --- | --- |
| `clean.py` | 从每只股票首个完整有效日开始保留数据，标记价格关系、非正数、缺失值及成交均价异常，并计算复权价格。 |
| `cut.py` | 生成交易日序号，构建 60 日滑动窗口，剔除含异常记录的窗口。 |
| `convert.py` | 将 `cut.csv` 和 `windows.csv` 转换为 Parquet。 |
| `test.py` | 按窗口结束日期划分训练集（2021 年以前）、验证集（2021 年）及测试集（2022 年起）。 |

## 开发记录

- [2026-10-26 数据准备与 Transformer 后续计划](personal/2026-10-26_数据准备与Transformer计划.md)（历史记录，以当前脚本为准）

2026-10-29 同步：更新了 	est.py 的标签处理代码；原有 8 个结果文件经 SHA-256 比对均未变化，继续使用下方结果包。

当前标签代码尚未跑通：合并键使用 nd_date，而窗口清单使用 nd_one；目前输出了 7 项标签的代码，与计划中的四价格目标也尚待统一。此次同步保留本地代码原样。

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