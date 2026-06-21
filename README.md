# 少儿编程课程学习行为数据处理与分析

基于 Python 的数据处理综合训练项目。通过 AI 模拟生成少儿编程课程学习行为数据，使用 pandas、matplotlib、seaborn 等库完成完整的数据分析流程，并基于 Flask + ECharts 构建交互式 Web 分析系统。

## 功能

- **Mock 数据生成**：模拟生成 5 张业务表（学生、课程、学习记录、作业、出勤），3200+ 条记录
- **数据清洗**：处理缺失值、重复值、异常值、格式不统一等问题
- **特征工程**：构造年龄段、星期、时长类别、成绩等级、课程大类等 7 个新分析维度
- **数据可视化**：生成 7 张统计分析图表（堆叠柱状图、饼图、热力图、散点图等）
- **交互式 Web 系统**：5 步向导式分析面板，支持一键执行数据获取 → 读取 → 清洗 → 特征工程 → 可视化

## 环境要求

| 依赖 | 版本 |
|---|---|
| Python | 3.8+ |
| pandas | ≥1.3 |
| numpy | ≥1.21 |
| matplotlib | ≥3.4 |
| seaborn | ≥0.11 |
| Flask | ≥2.0 |
| ECharts | 5.x（前端 CDN 加载） |

## 快速开始

```bash
# 1. 安装依赖
pip install pandas numpy matplotlib seaborn flask

# 2. 生成模拟数据
python src/generate_data.py

# 3. 执行数据分析（生成图表）
python src/data_analysis.py

# 4. 启动交互式 Web 分析系统
python src/web_app.py
# 浏览器访问 http://127.0.0.1:8080
```

## 项目结构

```
├── data/                        # 数据文件目录
│   ├── students.csv             # 学生信息表（含缺失/重复/异常值）
│   ├── courses.csv              # 课程信息表（20 门课程）
│   ├── learning_records.csv     # 学习记录表（核心行为数据）
│   ├── assignments.csv          # 作业提交记录表
│   └── attendance.csv           # 出勤记录表
├── src/
│   ├── generate_data.py         # Mock 数据生成脚本（含数据质量问题注入）
│   ├── data_analysis.py         # 数据分析主脚本（清洗 + 特征 + 7 张图表）
│   └── web_app.py               # Flask 交互式分析系统（5 步向导）
│   └── templates/
│       └── index.html           # Web 前端页面（ECharts 可视化）
├── output/
│   └── dashboard.html           # 独立数据看板（可选）
├── REPORT.md                    # 项目分析报告
└── README.md                    # 本文件
```

## 数据生成说明

数据为 AI 辅助生成的 Mock 数据，非真实教学数据。数据中人为注入了多种数据质量问题：

| 问题类型 | 示例 |
|---|---|
| 缺失值 | 学生表 age/gender/grade/course_level 列、学习记录 error_count/score 列 |
| 重复值 | 学生表 1 条重复、学习记录 5 条重复 |
| 异常值 | 年龄 3 岁、负分 -10、分数 >100、代码行数 -5 |
| 格式不统一 | 日期格式 Y-m-d vs Y/m/d vs m/d/Y、年级含文字 |
| 业务逻辑异常 | 低龄学生选修高级课程 |

## 分析内容

### 可视化图表（7 张）

| 图表 | 分析维度 |
|---|---|
| 01 年龄段×课程类型堆叠柱状图 | 不同年龄段学生的课程偏好 |
| 02 一周学习活跃度柱状图 | 学生学习时间分布规律 |
| 03 年龄段完成率与得分双轴图 | 各年龄段学习效果对比 |
| 04 学习时长与得分散点图 | 学习投入与成绩相关性 |
| 05 课程大类得分与代码行数对比 | 不同类型课程学习效果 |
| 06 作业提交状态饼图 | 作业完成情况分布 |
| 07 题型×提交状态热力图 | 各题型在不同提交状态下的平均得分 |

### 构造特征（7 个）

- `weekday_name`：学习星期几（类别）
- `is_weekend`：是否周末学习（布尔）
- `age_group`：年龄段分组，5 个区间（类别）
- `duration_category`：学习时长类别（类别）
- `score_level`：成绩等级（类别）
- `category_broad`：课程大类（类别）
- `is_programming`：是否为编程类作业（布尔）

## 技术栈

- **数据处理**：pandas、numpy
- **可视化**：matplotlib、seaborn、ECharts
- **Web 框架**：Flask
- **开发工具**：VS Code、Jupyter
