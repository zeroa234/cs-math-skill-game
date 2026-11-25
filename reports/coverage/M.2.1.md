# M.2.1 常微分方程：覆盖表

**状态（2026-11-23）：已写完，17 课，等用户验收。** 依据 `../cs-math-skill-tree/data/outlines/M.2.1.json`（主来源 MIT 18.03SC Unit I–IV；Lebl《Notes on Diffy Qs》1.2.2 存在唯一性、2.3 高阶线性方程）、`data/curation/learning-paths/M.2.1.json`（吉林大学伍卓群/李勇《常微分方程》、台大丁建均《工程数学》）和原技能树综合练习 4 小题。数值核对脚本 `tests/content/M.2.1.verify.py`（本机没有 sympy：解析解用数值积分和有限差分代回方程核对）。

前置：必须前置 M.1.3（定积分、原函数、换元、分部积分可直接用），往下还有 M.1.2（导数、链式法则、自然对数、泰勒多项式）、M.1.1。推荐前置 M.3.1 线性代数不在必须前置链上，照 M.1.4.1 的做法把矩阵、行列式、特征值、特征向量写进 `assumes`，课里用到时提醒怎么算 2×2 的情形。复数只用到 $e^{i\theta} = \cos\theta + i\sin\theta$ 和复数的模与辐角，在 `complex-sinusoid` 现讲。

## 课的安排

| 课 | 章 | 内容 |
|---|---|---|
| `separable-equations` | 一阶与高阶方程 | 微分方程、阶、解和初值问题；分离变量 |
| `linear-first-order` | 一阶与高阶方程 | 一阶线性方程、积分因子（综合练习 1） |
| `complex-sinusoid` | 一阶与高阶方程 | 复数和复指数、正弦函数的振幅相位、一阶常系数方程、指数输入的增益和相位滞后 |
| `second-order-modes` | 一阶与高阶方程 | 特征方程、过阻尼/临界/欠阻尼、线性无关和朗斯基行列式、高阶常系数方程（综合练习 2） |
| `forced-response` | 一阶与高阶方程 | 指数响应公式、增益与相位、待定系数法、线性算子和线性时不变 |
| `resonance-lrc` | 一阶与高阶方程 | 纯共振、频率响应和实际共振、LRC 电路 |
| `fourier-series` | 一阶与高阶方程 | 傅里叶级数、逐项运算、周期输入和共振 |
| `step-delta-convolution` | 一阶与高阶方程 | 阶跃和冲激函数、单位阶跃响应和冲激响应、卷积 |
| `laplace-transform` | 一阶与高阶方程 | 拉普拉斯变换的定义、变换表和平移规则、导数的变换、部分分式、解初值问题 |
| `transfer-function` | 一阶与高阶方程 | 传递函数和权函数、卷积定理和格林公式、极点和稳定性、振幅响应和指数响应公式 |
| `linear-systems-eigen` | 线性方程组 | 一阶线性方程组、特征值法和简正模（综合练习 3） |
| `phase-portraits-matrix-exp` | 线性方程组 | 相图分类（结点、鞍点、焦点、中心）、矩阵指数 |
| `picard-theorem` | 存在唯一性 | 偏导数、Picard 定理、Lipschitz 条件、Peano 定理、Picard 迭代（综合练习 4 后半） |
| `solution-interval` | 存在唯一性 | 解的延展和爆破、线性方程的整体存在性、线性和非线性方程的区别 |
| `geometric-autonomous` | 稳定性与数值求解 | 方向场和等倾线、自治方程、平衡点和稳定性 |
| `numerical-methods` | 稳定性与数值求解 | 欧拉法、改进欧拉法、四阶龙格–库塔，误差阶（综合练习 4 前半） |
| `nonlinear-linearization` | 稳定性与数值求解 | 非线性方程组、平衡点附近线性化、极限环和混沌 |

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Basic DE's and Separable Equations | `separable-equations` |
| 1.2 | Geometric Methods | `geometric-autonomous` |
| 1.3 | Numerical Methods | `numerical-methods` |
| 1.4 | First Order Linear ODE's | `linear-first-order` |
| 1.5 | Solution by Integrating Factors | `linear-first-order` |
| 1.6 | Complex Arithmetic and Exponentials | `complex-sinusoid` |
| 1.7 | Sinusoidal Functions | `complex-sinusoid` |
| 1.8 | First Order Constant Coefficient Linear ODE's | `complex-sinusoid` |
| 1.9 | Exponential Input; Gain and Phase Lag | `complex-sinusoid` |
| 1.10 | First Order Autonomous Differential Equations | `geometric-autonomous` |
| 1.11 | Linear vs. Nonlinear | `solution-interval` |
| 2.1 | Modes and the Characteristic Equation | `second-order-modes` |
| 2.2 | Damped Harmonic Oscillators | `second-order-modes` |
| 2.3 | Exponential Response | `forced-response` |
| 2.4 | Gain and Phase Lag | `forced-response` |
| 2.5 | Undetermined Coefficients | `forced-response` |
| 2.6 | Linear Operators, Linear Time Invariance | `forced-response` |
| 2.7 | Pure Resonance | `resonance-lrc` |
| 2.8 | Frequency Response and Practical Resonance | `resonance-lrc` |
| 2.9 | Applications: LRC Circuits | `resonance-lrc` |
| 3.1 | Fourier Series: Basics | `fourier-series` |
| 3.2 | Operations on Fourier Series | `fourier-series` |
| 3.3 | ODE's with Periodic Input, Resonance | `fourier-series` |
| 3.4 | Step and Delta Functions: Integrals and Generalized Derivatives | `step-delta-convolution` |
| 3.5 | Unit Step and Unit Impulse Response | `step-delta-convolution` |
| 3.6 | Convolution | `step-delta-convolution` |
| 3.7 | Laplace Transform: Basics | `laplace-transform` |
| 3.8 | Partial Fractions and Inverse Laplace Transform | `laplace-transform` |
| 3.9 | Laplace Transform: Solving Initial Value Problems | `laplace-transform` |
| 3.10 | Transfer (System) and Weight Functions, Green's Formula | `transfer-function` |
| 3.11 | Poles, Amplitude Response, Connection to ERF | `transfer-function` |
| 4.1 | Linear Systems | `linear-systems-eigen` |
| 4.2 | Matrix Methods: Eigenvalues and Normal Modes | `linear-systems-eigen` |
| 4.3 | Qualitative Behavior: Phase Portraits | `phase-portraits-matrix-exp` |
| 4.4 | Matrix Exponentials | `phase-portraits-matrix-exp` |
| 4.5 | Nonlinear Systems | `nonlinear-linearization` |
| 4.6 | Linearization Near Critical Points | `nonlinear-linearization` |
| 4.7 | Limitations of the Linear: Limit Cycles and Chaos | `nonlinear-linearization` |
| 5.1 | Existence and uniqueness | `picard-theorem`、`solution-interval` |
| 6.1 | Linear independence | `second-order-modes` |
| 6.2 | Constant-coefficient higher-order ODEs | `second-order-modes` |

## CS2023 核心主题（C2）

`scope.json` 对 M.2.1 只给国标数学类的常微分方程，没有 CS2023 主题；4 个章由上表的课负责。

## 原技能树综合练习（C4）

| 小题 | 内容 | 由哪一课教到 |
|---|---|---|
| (1) | 积分因子法解一阶线性方程 | `linear-first-order` |
| (2) | 常系数二阶方程的通解和长期行为 | `second-order-modes` |
| (3) | 2×2 线性方程组的特征值、通解和平衡点稳定性 | `linear-systems-eigen`、`phase-portraits-matrix-exp` |
| (4) | 欧拉法两步、和精确解比较；Picard 定理的条件 | `numerical-methods`、`picard-theorem`（结业挑战 `b-euler` 就是这一小题的前半） |

## 后继技能用到的写法（C5）

必须后继里和电子电气远征有关的是 H.4.1 控制理论与状态估计（传递函数、极点、拉普拉斯变换、状态方程 $\dot x = Ax$ 和特征值判稳定）和 N.2.1 量子力学基础（二阶线性方程、特征值问题、复指数）。这些写进本包 `terms`。
