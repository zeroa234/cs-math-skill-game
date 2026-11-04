# P.2.3 Python 与科学计算工具：覆盖表

规则见 `docs/content-authoring.md` 的“知识覆盖面标准”。依据：skill-tree 大纲 `../cs-math-skill-tree/data/outlines/P.2.3.json`：A = Scipy Lecture Notes（scipy-lectures.org）的 1.1、1.2、1.4、1.6、3.1 五章，B = Python Packaging User Guide 的两篇教程和三篇指南，共 37 节。“节”是技能内部编号，“原文”是原文的节号和标题。技能的章另列了 MIT Missing Semester（2026）的 Command-line Environment、Packaging and Shipping Code，廖雪峰 Python 教程的 argparse、venv、进程和线程，菜鸟教程 SciPy 的优化器、插值、显著性检验、稀疏矩阵，也按它们核对（见“学习资源的章节”）。

必须前置是程序设计基础 P.1.1，它按 Python 官方教程第 3–8 章教过：数和字符串、列表、字典、元组、集合、切片、别名和 `copy()`、`is` 和 `==`、真假判定、`if`/`for`/`while`、`enumerate`、`zip`、推导式、函数、默认参数（含可变默认值的陷阱）、`*args`/`**kwargs`、`lambda`、PEP 8、模块和包、`__name__`、读写文本文件和 JSON、`try`/`except`/`finally`/`with`、自定义异常。这一站不重讲这些，只补原文讲了而 P.1.1 没讲的部分（下表“课”一栏）。

`node scripts/check-coverage.mjs P.2.3` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | A 1.1.1 Why Python? | `ecosystem` |
| 1.2 | A 1.1.2 The Scientific Python ecosystem | `ecosystem` |
| 1.3 | A 1.1.3 Before starting: Installing a working environment | `install-pip` |
| 1.4 | A 1.1.4 The workflow: interactive environments and text editors | `ipython` |
| 2.1 | A 1.2.1 First steps | `ipython`, `run-scripts` |
| 2.2 | A 1.2.2 Basic types | `complex-numbers`, `in-place` |
| 2.3 | A 1.2.3 Control Flow | `complex-numbers`, `in-place` |
| 2.4 | A 1.2.4 Defining functions | `functions-as-values` |
| 2.5 | A 1.2.5 Reusing code: scripts and modules | `run-scripts`, `argparse`, `own-modules` |
| 2.6 | A 1.2.6 Input and Output | `file-lines` |
| 2.7 | A 1.2.7 Standard Library | `file-lines`, `os-paths`, `batch-files` |
| 2.8 | A 1.2.8 Exception handling in Python | `eafp` |
| 2.9 | A 1.2.9 Object-oriented programming (OOP) | `classes`, `inheritance` |
| 3.1 | A 1.4.1 The NumPy array object | `ndarray`, `make-arrays`, `index-slice`, `masks` |
| 3.2 | A 1.4.2 Numerical operations on arrays | `elementwise`, `reductions`, `broadcasting`, `reshape-sort` |
| 3.3 | A 1.4.3 More elaborate arrays | `dtypes`, `structured-masked` |
| 3.4 | A 1.4.4 Advanced operations | `polynomials`, `save-load` |
| 4.1 | A 1.6.1 File input/output: scipy.io | `save-load` |
| 4.2 | A 1.6.2 Special functions: scipy.special | `scipy-tour` |
| 4.3 | A 1.6.3 Linear algebra operations: scipy.linalg | `linear-systems`, `det-inv-svd` |
| 4.4 | A 1.6.4 Interpolation: scipy.interpolate | `interpolate` |
| 4.5 | A 1.6.5 Optimization and fit: scipy.optimize | `minimize`, `curve-fit` |
| 4.6 | A 1.6.6 Statistics and random numbers: scipy.stats | `distributions`, `t-tests` |
| 4.7 | A 1.6.7 Numerical integration: scipy.integrate | `integrate`, `ode` |
| 4.8 | A 1.6.8 Fast Fourier transforms: scipy.fftpack | `fft` |
| 4.9 | A 1.6.9 Signal processing: scipy.signal | `signal` |
| 4.10 | A 1.6.10 Image manipulation: scipy.ndimage | `ndimage` |
| 5.1.1 | A 3.1.1.1 Data as a table | `dataframe` |
| 5.1.2 | A 3.1.1.2 The pandas data-frame | `dataframe`, `groupby` |
| 5.2 | A 3.1.2 Hypothesis testing: comparing two groups | `t-tests`, `paired-tests` |
| 5.3 | A 3.1.3 Linear models, multiple factors, and analysis of variance | `ols` |
| 5.4 | A 3.1.4 More visualization: seaborn for statistical exploration | `seaborn` |
| 6.1 | B Installing Packages | `install-pip` |
| 6.2 | B Managing Application Dependencies | `dependencies` |
| 7.1 | B Install packages in a virtual environment using pip and venv | `venv` |
| 7.2 | B Installing packages using virtualenv | `venv` |
| 7.3 | B Installing scientific packages | `install-pip` |

另有几课不对应大纲的某一节：

- `plotting`（Matplotlib 画折线、图例、坐标轴标签、标题、保存图片）：Scipy Lecture Notes 的 1.5 Matplotlib 被大纲的 `omitted` 整章略去，但原技能树的综合练习 (3) 要画 sin、cos 并保存 PNG，按 C4 要教到。写法按 Matplotlib 官方的 pyplot 教程。
- `shell`（参数、选项、通配符、环境变量、退出状态、`&&`/`||`、管道和重定向）：技能第 4 章“环境管理与自动化”列了 Missing Semester 的 Command-line Environment，CS2023 的 FPL-Scripting 核心主题也点名了 System commands 和 Environment variables。
- `subprocess`（进程、在 Python 里运行别的程序、`subprocess.run`、多进程和多线程的区别）：技能第 4 章列了廖雪峰教程的“进程和线程”。

教到什么深度（入门层）：
- 第 1 章只教脚本和工具：IPython 和笔记本的用法、从终端运行脚本、`sys.argv` 和 `argparse`、模块缓存和搜索路径、`os`/`os.path`/`pathlib`/`glob`/`shutil`/`pickle`、类和继承的基本写法。类只讲到原文的范围（`__init__`、方法、属性、继承、类属性），不讲私有属性、多继承、特殊方法，这些属于面向对象程序设计 P.1.2。
- NumPy 讲到原文 1.4 的全部：创建、索引和切片、视图和副本、掩码和下标数组、逐元素运算、汇总和 `axis`、广播、改形状、排序、数据类型和转换、结构化数组、掩码数组、多项式、读写文件。
- SciPy 各子模块讲“这个工具解决什么问题、怎么调用、返回什么、有哪些坑”，不讲背后的数值方法：线性代数讲到解方程组、行列式、逆、SVD 的调用和含义（理论在线性代数 M.3.1）；积分只用“曲线下的面积”的直观意思（定积分在一元积分学 M.1.3）；微分方程只讲“已知每一刻怎么变，算出整条曲线”和 `odeint` 的用法（理论在常微分方程 M.2.1）；傅里叶变换只讲“把信号拆成不同频率的正弦波、找出主频率、去掉高频”（理论在傅里叶分析 M.1.9、信号与系统 H.1.3）；图像处理只用几个小数组演示平移、模糊、膨胀腐蚀和连通区域（领域知识在图像处理与计算机视觉 A.3.2）。
- 统计讲工具的用法和结果怎么读：分布对象、拟合、分位数、t 检验（单样本、两独立样本、配对）、Wilcoxon 和 Mann–Whitney 检验、`statsmodels` 的公式写法和系数表。检验的理论、F 检验和方差分析的细节属于数理统计 M.6.2 和回归与统计建模 M.6.2.2，`ols` 只提一句。
- 环境管理讲到能独立完成综合练习 (4)：装 Python、pip、虚拟环境、`requirements.txt`、版本约束，以及依赖冲突、锁文件、`pyproject.toml`、conda 是什么。打包和发布自己的库（`uv build`、上传 PyPI、容器）只讲概念。

## 和原文的核对

写课前，pi 子代理读了 37 节的原文（Scipy Lecture Notes、Packaging User Guide 的页面，和 Missing Semester 的两讲；笔记 `temp/research/P.2.3-source-notes.md`，不入库），课里的说法和例子按这份笔记写。

Scipy Lecture Notes 写于 Python 2 和较老的 NumPy/SciPy 时期，有些写法和输出现在已经变了。课里一律按现在的版本（Python 3.14、NumPy 2.5、SciPy 1.18、pandas 3.1、statsmodels 0.15、seaborn 0.13、Matplotlib 3.11）写，每个输出都由 `tests/content/P.2.3.verify.py` 实际运行核对：532 处，其中 134 道数字题和文字题、32 道选择题的答案逐题从课包里读出来，和运行结果比较；脚本、命令行参数、`argparse` 的报错、虚拟环境、多进程用真实的子进程运行，bash 的例子用 Git Bash 运行，IPython 的魔术命令用 IPython 自己的 shell 运行。和原文不同的地方：

- Python 2 的写法和输出（`<type 'int'>`、`raw_input`、`print "…"`、`30L`）一律换成 Python 3；IPython 9 显示类型时写成 `int`，普通 `>>>` 环境是 `<class 'int'>`。`%timeit` 的输出格式换成现在的“mean ± std. dev. of 7 runs”。
- 原文“p 值是两个过程相同的概率”的说法是错的（p 值是在零假设成立的前提下算出的概率，不是零假设成立的概率）。`t-tests` 按正确的定义教，并在一道题的解析里点明原文写错了。菜鸟教程“否则我们接受原假设”也改成“不拒绝零假设，不等于证明相等”。
- 原文 `np.random.seed`/`rand`/`randn` 是旧接口，课里先教 `np.random.default_rng`，旧写法只说明还能用；`seed(3)` 加 `randint` 的那串数和原文一致（旧接口的随机数序列是冻结的）。
- 原文的 `scipy.fftpack` 现在是旧接口，课里用 `scipy.fft`（`fftpack.fft` 结果相同）；`interp1d` 文档标为旧接口，课里加讲 `np.interp`、`CubicSpline`；`interp2d`、`quadrature`、`romberg`、`scipy.misc.face`、`np.recfromcsv`、`np.int`/`np.float` 已删除，课里不用；`odeint` 的文档建议新代码用 `solve_ivp`，课里两个都讲；`basinhopping` 的随机种子参数现在叫 `rng`。
- scipy 顶层已经没有 `scipy.cos` 这类 NumPy 函数（原文说“为历史原因保留”），课里改成“现在会报 AttributeError”。
- SciPy 1.18 的报错原文变了：非方阵求行列式是 `ValueError: Last 2 dimensions of the array must be square but received shape (3, 4).`，奇异矩阵求逆是 `LinAlgError: A singular matrix detected: ...`，课里照现在的写。
- 原文说 `import seaborn` 会改掉 Matplotlib 的默认样式；seaborn 0.8 起不再这样，要调用 `set_theme()`。课里讲现在的行为，并说明原文那句是老版本（核对脚本在新进程里比较导入前后的 `rcParams`，0 处变化）。
- `pandas.tools.plotting` 现在是 `pandas.plotting`；pandas 3 下 groupby 迭代时 `print((gender, value.mean()))` 会显示 `np.float64(…)`，课里改成 `print(gender, value.mean())`。
- 原文的 brain_size.csv（40 行）、工资数据不在本地，课里用原文笔记里抄下的前 5 行做例子，数值由脚本用这 5 行重算；原文 40 行的结果（女 109.45、男 115.25、Intercept 109.45 和 5.80）只在 `ols` 的一道题里按原文引用。
- 原文的 `curve_fit`、`stats.norm.fit` 等用的是不固定种子的随机数，课里固定成 `default_rng(0)`，给出的数字是这个种子下的结果（如 `[2.64198155 1.51346571]`），并说明换了噪声结果会变。
- 廖雪峰教程 argparse 帮助里的 `optional arguments:` 在 Python 3.10 起是 `options:`；venv 一节的 `source activate`（在 bin 里）课里写成 `source .venv/bin/activate` 和 Windows 的 `.venv\Scripts\activate`；GIL“每执行 100 条字节码释放一次”的说法已过时（现在按时间片，`sys.getswitchinterval()` 是 0.005 秒），课里不用这个数，并说明 3.13 起有可选的无 GIL 构建。
- 菜鸟教程说 `ttest_ind()` “获取两个相同大小的样本”，其实两组人数可以不同，课里写明。

写完第一次运行核对脚本时查出三处错，都已改：复数例题里 `-134+352j` 的模写成了约 376（实际约 377）；`masks` 一道题的答案写成 17（实际 18）；`ndimage` 连通区域的面积顺序写成 9、1、1（标号按从上到下、从左到右，面积依次是 1、9、1）。

## CS2023（`data/curation/scope.json`）

| 知识点 | CS2023 主题（scope.json 匹配原文） | 课 |
|---|---|---|
| 脚本 | FPL-Scripting，CS Core：System commands | `run-scripts`, `argparse`, `shell`, `subprocess` |
| 环境管理与自动化 | FPL-Scripting，CS Core：Environment variables | `os-paths`, `shell` |

## 原技能树的综合练习

| 小题 | 课 |
|---|---|
| (1) 不用循环算 $1^2 + \dots + (10^6)^2$；1000×3 随机矩阵每列标准化 | `reductions`（平方和与 int64 溢出，分步例题）、`broadcasting`（按列标准化，分步例题） |
| (2) pandas：每个城市每月的平均温度、每个城市最热的一天 | `groupby`（分步例题就是这一题） |
| (3) Matplotlib 画 sin、cos，加图例、坐标轴标签、标题，存成 PNG | `plotting` |
| (4) 用 venv 建环境、装依赖、导出 `requirements.txt`；为什么每个项目要独立的环境 | `venv`、`dependencies` |
| (5) 用 pathlib 给目录里所有 .txt 文件名加上今天的日期前缀 | `batch-files`（分步例题就是这一题） |

## 学习资源的章节（C3）

写课时 pi 子代理又读了技能章列出的中文资料（笔记 `temp/research/P.2.3-zh-notes.md`、`temp/research/P.2.3-zh-scipy-mooc-notes.md`，不入库），逐条核对：

| 资料 | 小节 | 课 |
|---|---|---|
| 廖雪峰 Python 教程 | 16.3 argparse（位置参数、`--` 参数、`default`、`type`、`required`、`store_true`、短选项、`prog`、自动的 `-h`） | `argparse` |
| 廖雪峰 Python 教程 | 16.13 venv（建、激活、提示符、装在哪、`deactivate`、删除） | `venv` |
| 廖雪峰 Python 教程 | 14 进程和线程：subprocess、进程池 Pool、多线程和 GIL、进程与线程的取舍 | `subprocess` |
| 廖雪峰 Python 教程 | 14 的 fork、Queue 进程间通信、ThreadLocal、分布式进程、异步 IO | 不教：进程间通信和并发控制属于操作系统 C.2.1，分布式属于分布式系统；这一站只讲“在脚本里运行别的程序、用进程池并行计算” |
| 廖雪峰 Python 教程 | 16.1 datetime、13.3 操作文件和目录 | `batch-files`、`os-paths`（教程没有 pathlib 一节，pathlib 按 Python 官方文档讲） |
| 菜鸟教程 SciPy | 优化器（root、fsolve、minimize 的 method、constraints、bounds、Nelder-Mead） | `minimize`、`curve-fit` |
| 菜鸟教程 SciPy | 稀疏矩阵（CSR、CSC、data、nnz、toarray、稀疏度） | `det-inv-svd` |
| 菜鸟教程 SciPy | 插值（interp1d、UnivariateSpline、Rbf） | `interpolate`（Rbf 现在是旧接口，只在覆盖表记一笔，课里不讲） |
| 菜鸟教程 SciPy | 显著性检验（零假设、两类错误、显著性水平、单边双边、ttest_ind、kstest、describe、normaltest、skew、kurtosis） | `t-tests`、`paired-tests`、`distributions` |
| 北理工《Python 数据分析与展示》第 1 周 | 数组的创建和变换、运算、CSV 和多维数据存取、随机数、统计函数、梯度函数、图像的数组表示和变换 | `ndarray` 到 `reshape-sort`、`save-load`（`np.gradient` 在 `reductions`，图像反色在 `save-load`） |
| 北理工《Python 数据分析与展示》第 3 周 | Series、DataFrame、按索引对齐的运算、排序、基本统计、累计统计、相关分析 | `dataframe`、`pandas-ops`、`groupby` |
| Missing Semester | Command-line Environment：参数、选项、通配符、变量和引号、环境变量、退出状态、`&&`/`||`、管道和重定向 | `shell`（信号、`trap`、终端复用、SSH 不教：属于版本控制、调试与构建工具 P.2.4 和操作系统 C.2.1） |
| Missing Semester | Packaging and Shipping Code：依赖和间接依赖、依赖冲突、虚拟环境、SemVer 和 `~=`、固定版本和锁文件、库和应用的区别、pyproject.toml、wheel 和平台标签 | `dependencies`、`venv`、`install-pip`（容器、虚拟机、Nix、发布到 PyPI 只在 `dependencies` 提一句工具名，不展开：属于 P.2.4） |

## 后继技能要用的

必须后继是监督、无监督与半监督学习 A.2.1 和推荐系统 A.3.4（都还没有内容包），按它们的综合练习核对：

- A.2.1 的线性回归、梯度下降、k-means、PCA 用 NumPy 写起来要：数组运算和广播（`elementwise`、`broadcasting`）、`mean`/`sum` 和 `axis`（`reductions`）、矩阵乘法 `@`（`elementwise`、`linear-systems`）、解方程组（`linear-systems`）、用 `minimize` 找最小值（`minimize`）。
- A.3.4 的余弦相似度要点积和向量长度（`linear-systems` 的 `np.linalg.norm`），评分矩阵里“0 表示未评分”的处理可以用掩码（`masks`、`structured-masked`）。
