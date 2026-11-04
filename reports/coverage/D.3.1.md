# D.3.1 数据科学导论与工具箱：覆盖表

规则见 `docs/content-authoring.md` 的“知识覆盖面标准”。依据：skill-tree 大纲 `../cs-math-skill-tree/data/outlines/D.3.1.json`，四个来源：A = VanderPlas《Python Data Science Handbook》，B = Lau、Gonzalez、Nolan《Learning Data Science》，C = scikit-learn 用户指南 3.4 Metrics and scoring 与 12 Common pitfalls，D = DVC 用户指南 Experiment Management。“节”是技能内部编号，“原文”是来源和它自己的节号。

这一站没有必须前置（推荐前置 P.1.1、P.2.3、M.6.1、M.6.2、M.3.1 都不强制），所以课里用到的编程词都在这一站讲：`python-values`、`python-containers` 两课补上读懂数据分析代码要用的最少内容（变量、数和文字、列表、字典、函数、循环、第三方库），概率和统计只用模拟和数数讲（罐子模型、打乱标签、自助法），不用分布公式。

游戏的章按 skill-tree 的 11 个知识点排，课按章排；同一来源的节会分到不同的章（如 A 第 2 章 NumPy 在“统计包与工作流”，A 第 3 章 pandas 分在“数据获取”“清洗”“探索分析”）。

`node scripts/check-coverage.mjs D.3.1` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | A 1.1 Help and Documentation in IPython | `notebook` |
| 1.2 | A 1.3 IPython Magic Commands | `notebook` |
| 1.3 | A 1.4 Input and Output History | `notebook` |
| 1.4 | A 1.6 Errors and Debugging | `debug-timing` |
| 1.5 | A 1.7 Profiling and Timing Code | `debug-timing` |
| 2.1 | A 2.1 Understanding Data Types in Python | `numpy` |
| 2.2 | A 2.2 The Basics of NumPy Arrays | `numpy` |
| 2.3 | A 2.3 Computation on NumPy Arrays: Universal Functions | `ufuncs` |
| 2.4 | A 2.4 Aggregations: Min, Max, and Everything In Between | `ufuncs`, `summary` |
| 2.5 | A 2.5 Computation on Arrays: Broadcasting | 不教：属于 P.2.3 Python 与科学计算工具（它的“数组与数据框”一章依据 Scipy Lecture Notes 1.4 NumPy，讲数组运算的广播）；这一站的标准化、按组减平均都用 pandas 的写法（`train-test`、`groupby`），不需要广播规则 |
| 2.6 | A 2.6 Comparisons, Masks, and Boolean Logic | `ufuncs`, `select` |
| 2.7 | A 2.7 Fancy Indexing | 不教：属于 P.2.3（同一章的数组索引）；这一站按条件取数用布尔掩码和 loc（`select`、`ufuncs`） |
| 2.8 | A 2.8 Sorting Arrays | 不教：属于 P.2.3（同一章的数组操作）；排名只在 `hypothesis-test` 里当现成结果用 |
| 2.9 | A 2.9 Structured Data: NumPy's Structured Arrays | 不教：属于 P.2.3（同一章讲更复杂的数组类型）；原书本节也说这种场合更适合用 pandas 的数据框 |
| 3.1 | A 3.1 Introducing Pandas Objects | `dataframe` |
| 3.2 | A 3.2 Data Indexing and Selection | `select` |
| 3.3 | A 3.3 Operating on Data in Pandas | `combine` |
| 3.4 | A 3.4 Handling Missing Data | `missing` |
| 3.5 | A 3.5 Hierarchical Indexing | `reshape` |
| 3.6 | A 3.6 Combining Datasets: Concat and Append | `combine` |
| 3.7 | A 3.7 Combining Datasets: Merge and Join | `combine` |
| 3.8 | A 3.8 Aggregation and Grouping | `groupby` |
| 3.9 | A 3.9 Pivot Tables | `pivot` |
| 3.10 | A 3.10 Vectorized String Operations | `text-time` |
| 3.11 | A 3.11 Working with Time Series | `text-time` |
| 3.12 | A 3.12 High-Performance Pandas: eval() and query() | `select` |
| 4.1 | A 4.1 Simple Line Plots | `line-scatter` |
| 4.2 | A 4.2 Simple Scatter Plots | `line-scatter` |
| 4.3 | A 4.3 Visualizing Errors | `figure-parts` |
| 4.4 | A 4.4 Density and Contour Plots | `histogram` |
| 4.5 | A 4.5 Histograms, Binnings, and Density | `histogram` |
| 4.6 | A 4.6 Customizing Plot Legends | `figure-parts` |
| 4.7 | A 4.8 Multiple Subplots | `figure-parts` |
| 4.8 | A 4.14 Visualization with Seaborn | `figure-parts` |
| 5.1 | A 5.1 What Is Machine Learning? | `sklearn` |
| 5.2 | A 5.2 Introducing Scikit-Learn | `sklearn` |
| 5.3 | A 5.3 Hyperparameters and Model Validation | `train-test`, `overfitting`, `cross-validation` |
| 5.4 | A 5.4 Feature Engineering | `pipeline` |
| 5.5 | A 5.9 In Depth: Principal Component Analysis | 不教：属于 A.2.1 监督、无监督与半监督学习（“降维”一章）；PCA 的线性代数在 M.3.1 `svd-uses` |
| 5.6 | A 5.11 In Depth: k-Means Clustering | 不教：属于 A.2.1（“聚类”一章）；这一站在 `sklearn` 里只说出“聚类”是什么 |
| 6.1 | B 1.1 The Stages of the Lifecycle | `lifecycle` |
| 6.2 | B 1.2 Examples of the Lifecycle | `lifecycle` |
| 7.1 | B 2.1 Big Data and New Opportunities | `data-scope` |
| 7.2 | B 2.2 Target Population, Access Frame, and Sample | `data-scope` |
| 7.3 | B 2.3 Instruments and Protocols | `protocols` |
| 7.4 | B 2.5 Accuracy | `poll-bias`, `urn` |
| 7.5 | B 2.4 Measuring Natural Phenomena | `protocols` |
| 8.1 | B 8.1 Data Source Examples | `file-formats` |
| 8.2 | B 8.2 File Formats | `file-formats` |
| 8.3 | B 8.3 File Encoding | `encoding-size` |
| 8.4 | B 8.4 File Size | `encoding-size` |
| 8.5 | B 8.6 Table Shape and Granularity | `granularity` |
| 9.1 | B 9.2 Quality Checks | `quality` |
| 9.2 | B 9.3 Missing Values and Records | `missing` |
| 9.3 | B 9.4 Transformations and Timestamps | `text-time` |
| 9.4 | B 9.5 Modifying Structure | `reshape` |
| 10.1 | B 14.2 JSON Data | `json-http` |
| 10.2 | B 14.3 HTTP | `json-http` |
| 10.3 | B 14.4 REST | `json-http` |
| 11.1 | B 3.1 The Urn Model | `urn` |
| 11.2 | B 3.2 Example: Simulating Election Poll Bias and Variance | `poll-bias` |
| 11.3 | B 3.3 Example: Simulating a Randomized Trial for a Vaccine | `trial-air` |
| 11.4 | B 3.4 Example: Measuring Air Quality | `trial-air` |
| 12.1 | B 16.1 Overfitting | `overfitting` |
| 12.2 | B 16.2 Train-Test Split | `train-test` |
| 12.3 | B 16.3 Cross-Validation | `cross-validation` |
| 12.4 | B 16.4 Regularization | 不教：属于 M.6.2.2 回归与统计建模（“正则化”一章讲岭回归和 lasso）；这一站只讲用验证和交叉验证挑模型的复杂度（`overfitting`、`cross-validation`） |
| 12.5 | B 16.6 Model Bias and Variance | `bias-variance` |
| 13.1 | B 17.1 Distributions: Population, Empirical, Sampling | `three-distributions` |
| 13.2 | B 17.2 Basics of Hypothesis Testing | `hypothesis-test` |
| 13.3 | B 17.3 Bootstrapping for Inference | `bootstrap` |
| 13.4 | B 17.4 Basics of Confidence Intervals | `bootstrap` |
| 13.5 | B 17.5 Basics of Prediction Intervals | `prediction-interval` |
| 14.1 | B 19.2 Modeling and Classification | `confusion` |
| 14.2 | B 19.3 Modeling Proportions (and Probabilities) | 不教：逻辑回归模型（sigmoid、对数几率）属于 M.6.2.2（“线性/广义线性模型”一章）和 A.2.1（“回归/分类”）；这一站只用“模型给出是 1 的概率”这件事（`confusion`、`roc`） |
| 14.3 | B 19.5 From Probabilities to Classification | `confusion`, `roc` |
| 15.1 | C 3.4.1 Which scoring function should I use? | `precision-recall` |
| 15.2 | C 3.4.4 Classification metrics | `confusion` |
| 15.3 | C 3.4.4.2 Accuracy score | `confusion` |
| 15.4 | C 3.4.4.6 Confusion matrix | `confusion` |
| 15.5 | C 3.4.4.9 Precision, recall and F-measures | `precision-recall` |
| 15.6 | C 3.4.4.15 Receiver operating characteristic (ROC) | `roc` |
| 15.7 | C 3.4.6 Regression metrics | `regression-metrics` |
| 15.8 | C 3.4.6.1 R² score, the coefficient of determination | `regression-metrics` |
| 15.9 | C 3.4.6.2 Mean absolute error | `regression-metrics` |
| 15.10 | C 3.4.6.3 Mean squared error | `regression-metrics` |
| 16.1 | C 12.1 Inconsistent preprocessing | `train-test` |
| 16.2 | C 12.2 Data leakage | `leakage` |
| 16.3 | C 12.2.1 How to avoid data leakage | `leakage` |
| 16.4 | C 12.2.2 Data leakage during pre-processing | `pipeline` |
| 16.5 | C 12.3 Controlling randomness | `randomness` |
| 16.6 | C 12.3.3.1 Getting reproducible results across multiple executions | `randomness` |
| 16.7 | C 12.3.3.2 Robustness of cross-validation results | `randomness` |
| 17.1 | D DVC Experiments Overview | `experiments` |
| 17.2 | D How does DVC track experiments? | `experiments` |
| 17.3 | D Save experiments | `experiments` |
| 17.4 | D Metrics, plots, parameters | `experiments` |
| 17.5 | D Models and datasets | `experiments` |

另有三课不对应单独的一节：`python-values`、`python-containers`（读懂代码要用的最少 Python：这一站没有必须前置，B1 不能借 P.1.1 的术语）和 `reproducible`（笔记本的可重现性：原技能树综合练习第 4 题；材料来自 A 第 1 章、B 9.4 “笔记本可以乱序运行”的提醒，以及 scikit-learn 12.3 的固定随机性）。

教到什么深度（入门层）：
- Python 只讲读懂数据分析代码需要的写法；条件、循环只讲 for 和 if 的一行用法，函数只讲调用和写一个 `def` 包住几步变换（`text-time` 的 pipe）。
- NumPy 讲数组的类型、形状、取值、两个坑（整数截断、切片共用数据）、整体运算、按轴汇总和掩码；广播、花式索引、排序、结构化数组在 P.2.3。
- pandas 讲读入、loc/iloc、条件筛选和 query、缺失值、类型转换、`.str` 和 `.dt`、按时间汇总和移动平均、对齐、concat、merge、长宽表、多层索引、groupby（含 transform 和 filter）、透视表。eval/query 的提速原理（numexpr）不讲。
- 画图讲每种图回答什么问题和最常见的写法（fig/ax、label、subplots 的编号、bins、KDE 的宽度、errorbar 和 fill_between、seaborn 的几种图），不讲样式定制。
- 统计推断全部用模拟讲：罐子模型、打乱标签的置换检验、自助法；正态法置信区间只用 ±1.96 和 ±2.58 两个倍数。分布公式、t 检验在 M.6.2。
- 指标讲二分类：准确率、混淆矩阵、精确率、召回率、F1、特异度、ROC 和 AUC；多分类的 macro/micro 平均、Brier、log loss、pinball loss 只在 `precision-recall` 里说“指标要配合预测的目标”，不展开。
- DVC 讲为什么要记录实验、记录什么、`dvc exp run / show / push`、代码走 Git 大文件走 DVC；DVCLive、队列、Studio 不讲。

## 和原文的核对

2026-11-04 由 pi 子代理逐节整理原文笔记（`temp/research/D.3.1-source-notes.md`，不入库）：98 节全部读到了原文网页，代码和输出照抄。主代理写课时用这份笔记核对定义和数字：生命周期四阶段和四类问题（B 1.1）、维基奖励实验的 144,000 名志愿者、1%、200 人、90 天（B 2.2）、谷歌流感趋势 108 周里高估 100 周（B 2.1）、冒纳罗亚每小时 5 分钟标准气和约 0.30 ppm 的偏离（B 2.4）、四种偏差和三种变异（B 2.5）、急诊调查最多 16 种药、年龄在 34–35 位、-8 表示缺失（B 8.1–8.2）、UTF-8 报错原文和 chardet 的 0.73（B 8.3）、1,024 进位和“5 倍内存”法则（B 8.4）、三张餐厅表的形状、64859 号餐厅同日两个分数、不加权 48.0% 加权 52.3%（B 8.6）、邮编 941033148 和 14,221 比 1 的 type 列（B 9.2）、-99.99 和 -7/-8/-9 缺失码、均值插补让误差范围偏窄（B 9.3）、检查集中在星期二三（B 9.4）、melt 和 pivot_table（B 9.5）、json_normalize 和 read_json 丢掉前导 0（B 14.2）、状态码分组（B 14.3）、令牌过期 401、认证失败 400（B 14.4）、总统身高的统计量（A 2.4）、sum 104 毫秒对 np.sum 442 微秒（A 2.4）、泰坦尼克透视表（A 3.9）、1 近邻在训练数据上 1.0、留出一半 0.907、5 折 0.96（A 5.3）、y = 2x − 1 的拟合系数 1.98 和 −0.90（A 5.2）、罐子模型 0.4032 和燃料箱的 1/12/18/4（B 3.1）、宾州民调模拟 61%、45%、79%、37%（B 3.2）、疫苗试验 117 对 351、50 万次模拟无一次 ≤ 117（B 3.3）、传感器标准差 0.687、相对误差 8%–12%（B 3.4）、标准化前后 62.80 对 0.90（C 12.1）、特征选择泄漏 0.76 对 0.5、流水线交叉验证 0.43 ± 0.05（C 12.2.2）、随机森林 0.84 和两组 5 折分数（C 12.3）、混淆矩阵 [[377, 49], [104, 129]] 和阈值 0.33 的精确率 0.59、召回率 0.81、特异度 0.70（B 19.5）、sklearn 指标例子的 0.5、0.375、0.948 和 AUC 0.75（C 3.4）、维基实验平均排名 113.68、p = 0.00052、秩和检验 0.0013（B 17.2）、湿度系数 0.21 和标准误 0.027（B 17.3–17.4）、螃蟹壳宽 131.53 ± 11.07、n = 452 和增长量的两种区间（B 17.5）、DVC 的实验名、`-S`、`dvc exp show` 的表和 push 的分工（D）。

能在本机重算的数由 `tests/content/D.3.1.verify.py` 用 pandas 3.1、NumPy 2.5、scikit-learn 1.9 实际运行核对（课里的小表、sklearn 文档的例子、泄漏和随机性的对照、罐子模型的精确概率）；要用到原书数据文件的数（餐厅、急诊调查、民调和疫苗的 10 万次模拟、螃蟹）照抄原文，脚本只核对它们之间的算术。课里自己编的小表（共享单车、天气分组等）是主代理选的数。

pandas 3 和原书的差别，课里按新版本写：`to_datetime` 对整数加 format 已不推荐，先 `astype(str)`；`.dt.dayofweek` 改为 `.dt.day_of_week`；文字列的类型显示为 `str`；从字典造 Series 时索引按插入顺序（原书说会排序，是旧版本的行为）。

## CS2023（`data/curation/scope.json`）

| 知识点 | CS2023 主题（scope.json 匹配原文） | 课 |
|---|---|---|
| 问题定义 | DM-Analytics，KA Core：business understanding | `lifecycle`, `data-scope` |
| 数据获取 | DM-Analytics，KA Core：Data acquisition and governance | `file-formats`, `encoding-size`, `json-http`, `protocols` |
| 清洗 | AI-ML，CS Core：Data preprocessing | `quality`, `missing`, `text-time`, `combine`, `reshape`, `pipeline` |
| 探索分析 | DM-Analytics，KA Core：Exploratory data techniques | `summary`, `groupby`, `pivot`, `line-scatter`, `histogram` |
| 抽样偏差 | MSF-Statistics，KA Core：Sampling, bias, adequacy of samples | `data-scope`, `urn`, `poll-bias` |
| 评估指标 | AI-ML，CS Core：Performance metrics for classifiers | `confusion`, `precision-recall`, `roc` |
| 交叉验证 | AI-ML，KA Core：Cross-validation | `cross-validation`, `randomness` |

## 原技能树的综合练习

| 小题 | 课 |
|---|---|
| (1) 共享单车日租量的数据科学流程 | `lifecycle`（四阶段和四类问题）、`data-scope`、`quality`、`line-scatter`、`train-test`（按时间划分见 `leakage`） |
| (2) pandas：转日期、插补 temp、按月平均、相关系数 | `text-time`（to_datetime、`dt.to_period("M")` 的按月平均）、`missing`（interpolate）、`summary`（corr） |
| (3) 2, 3, 3, 4, 5, 100 的均值、中位数、四分位数、IQR 和离群值 | `summary`（分步例题就是这一题；结业挑战也有） |
| (4) 笔记本的可重现性问题和对策 | `reproducible` |
| (5) 三种数据泄漏和修正 | `leakage`（三种泄漏的表就是这一题）、`pipeline` |
| (6) 正类 1% 时准确率为什么误导；TP 40、FP 60、FN 10、TN 890 的精确率、召回率、F1、准确率 | `confusion`、`precision-recall`（分步例题就是这一题） |

## 后继技能要用的

必须后继只有 D.2.2 数据工程与大数据处理（还没有内容包）。它要直接用到：文件格式和编码（`file-formats`、`encoding-size`）、“读不进内存怎么办”的三条路（`encoding-size`）、粒度、主键和外键（`granularity`）、merge 与 concat（`combine`）、长宽表（`reshape`）、分组汇总（`groupby`）、JSON 和 REST 接口（`json-http`）、实验和数据的版本记录（`experiments`）。这一站在 AI 路线上的下一站 M.1.2 不依赖它；A.2.1 会用到 scikit-learn 的套路、训练集和测试集、交叉验证和指标（`sklearn`、`train-test`、`cross-validation`、`confusion` 到 `regression-metrics`）。
