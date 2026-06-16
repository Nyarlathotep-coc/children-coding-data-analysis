# 少儿编程课程学习行为数据处理与分析

## 项目概述
基于 Python 的数据处理综合训练课程作业。本项目通过 AI 模拟生成少儿编程课程学习行为数据，使用 pandas、matplotlib、seaborn 等库完成完整的数据分析流程。

## 项目结构
```
.
├── data/                   # 数据文件目录
│   ├── students.csv        # 学生信息表
│   ├── courses.csv         # 课程信息表
│   ├── learning_records.csv # 学习记录表
│   ├── assignments.csv     # 作业提交表
│   └── attendance.csv      # 出勤记录表
├── src/                     # 源代码目录
│   ├── generate_data.py    # Mock 数据生成脚本
│   └── data_analysis.py    # 数据分析主脚本
├── output/                  # 输出目录
│   └── figures/            # 可视化图表
│       ├── 01_age_course_preference.png
│       ├── 02_weekly_activity.png
│       ├── 03_age_completion_score.png
│       ├── 04_duration_score_scatter.png
│       ├── 05_course_score_lines.png
│       ├── 06_submission_status_pie.png
│       └── 07_assignment_heatmap.png
├── notebooks/              # Jupyter Notebook 目录
├── REPORT.md               # 项目报告
└── README.md               # 本文件
```

## 运行方法

### 1. 生成模拟数据
```bash
python src/generate_data.py
```

### 2. 执行数据分析
```bash
python src/data_analysis.py
```

## 依赖环境
- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn

## 分析结果
- 共 5 个相关 CSV 文件，约 3200+ 条记录
- 7 张数据可视化图表
- 6 个新构造的分析特征
- 7 个探索性分析问题
- 完整数据清洗流程（缺失值、重复值、异常值、格式问题处理）

## 数据说明
本项目数据为 AI 辅助生成的 Mock 数据，并非真实教学数据。数据中包含人为注入的缺失值、重复值、异常值和格式不统一问题，供数据处理练习使用。
