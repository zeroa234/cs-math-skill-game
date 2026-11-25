# H.4.1 控制理论与状态估计：覆盖表

**状态（2026-11-23）：已写完，19 课，等用户验收。** 依据 `../cs-math-skill-tree/data/outlines/H.4.1.json`（主来源 Åström & Murray《Feedback Systems》第 2 版第 1–3、5–10 章的相关节；模型预测控制取 Rawlings, Mayne & Diehl《Model Predictive Control》第 2 版第 1 章和 2.2、2.4）、`data/curation/learning-paths/H.4.1.json`（中国矿业大学《自动控制原理》MOOC 的时域分析、根轨迹、PID 与校正；KalmanFilter.NET 中文教程；MIT 6.302、6.245、16.323；DR_CAN 的 MPC 系列）和原技能树综合练习 5 小题。数值核对脚本 `tests/content/H.4.1.verify.py`。

前置：必须前置 M.2.1（拉普拉斯变换、传递函数、极点、特征方程、一阶线性方程组、矩阵指数、平衡点、渐近稳定、李雅普诺夫稳定、线性化、雅可比矩阵、频率响应、增益、相位滞后、卷积、冲激响应可直接用）和 M.3.1（矩阵、逆矩阵、转置、秩、特征值、正定矩阵、方差、最小二乘可直接用）。推荐前置 H.1.3 的分贝和波特图、E.2.2 的随机变量在用到时简短重述。

## 课的安排

| 课 | 章 | 内容 |
|---|---|---|
| `feedback-intro` | 反馈 | 反馈和控制是什么、开环和闭环、方框图、负反馈的性质（抗扰、跟踪、鲁棒，也会带来不稳定）、前馈加反馈等控制结构 |
| `feedback-principles` | 反馈 | 闭环传递函数、灵敏度函数和补灵敏度函数、用反馈抑制扰动、跟踪参考信号、对对象参数变化的鲁棒性 |
| `time-response` | 反馈 | 一阶系统的阶跃响应和时间常数；二阶系统的自然频率和阻尼比、超调量、调节时间；稳态误差和系统型别（综合练习 1、2） |
| `pid-control` | 反馈 | 比例、积分、微分三项的作用，积分作用消除稳态误差，积分饱和和抗饱和，齐格勒–尼科尔斯整定（综合练习 3） |
| `root-locus-compensation` | 反馈 | 根轨迹的含义和画法要点、超前校正和滞后校正 |
| `stability-routh` | 稳定性 | 稳定的定义、闭环极点和稳定性、劳斯–赫尔维茨判据、由判据求增益范围 |
| `lyapunov` | 稳定性 | 李雅普诺夫函数和李雅普诺夫第二方法、线性系统的李雅普诺夫方程 |
| `bode-plot` | 稳定性 | 频域建模、由状态空间求传递函数、波特图的渐近线和转折频率 |
| `nyquist-margins` | 稳定性 | 回路传递函数、奈奎斯特判据、增益裕度和相位裕度、伯德增益–相位关系和最小相位系统 |
| `state-space-models` | 状态空间 | 状态、输入、输出、状态方程和输出方程；把高阶微分方程写成状态空间；线性系统的基本定义（线性和时不变） |
| `state-response` | 状态空间 | 矩阵指数和卷积给出的完整解、阶跃响应、传递函数 $C(sI - A)^{-1}B + D$、极点就是 $A$ 的特征值 |
| `state-feedback` | 状态空间 | 状态反馈 $u = -Kx + k_rr$、按期望特征多项式配置极点、积分作用的状态反馈 |
| `reachability` | 可控/可观 | 可达性（能控性）、能控性矩阵和秩判据、不能控的例子（综合练习 4） |
| `observability-observer` | 可控/可观 | 能观性和能观性矩阵、状态观测器、分离原理、用估计的状态反馈的控制器设计 |
| `lqr` | 可控/可观 | 线性二次型调节器：代价函数、黎卡提方程、一维例子、布赖森法则选权重 |
| `kalman-filter` | Kalman滤波与模型预测控制 | 一维卡尔曼滤波的预测和更新、卡尔曼增益、多维的方程、扩展卡尔曼滤波和无迹卡尔曼滤波（综合练习 5） |
| `mpc-intro` | Kalman滤波与模型预测控制 | 离散时间模型、滚动时域、代价和约束、二次规划、有限时域线性二次问题的动态规划解（黎卡提递推） |
| `mpc-estimation` | Kalman滤波与模型预测控制 | MPC 里的状态估计：卡尔曼滤波和移动时域估计；跟踪的稳态目标、扰动模型和无静差；每个采样时刻估计和控制的顺序 |
| `mpc-stability` | Kalman滤波与模型预测控制 | MPC 调节问题的一般形式、终端代价和终端约束保证稳定 |

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | What Is Feedback? | `feedback-intro` |
| 1.2 | What Is Control? | `feedback-intro` |
| 1.3 | Feedback Properties | `feedback-intro` |
| 1.4 | Control System Architectures | `feedback-intro` |
| 2.1 | Using Feedback to Attenuate Disturbances | `feedback-principles` |
| 2.2 | Using Feedback to Track Reference Signals | `feedback-principles` |
| 2.3 | Using Feedback to Provide Robustness | `feedback-principles` |
| 3.1 | State Space Models | `state-space-models` |
| 4.1 | Stability | `stability-routh` |
| 4.2 | Lyapunov Stability Analysis | `lyapunov` |
| 5.1 | Basic Definitions | `state-space-models` |
| 5.2 | The Matrix Exponential | `state-response` |
| 5.3 | Input/Output Response | `state-response` |
| 6.1 | Reachability | `reachability` |
| 6.2 | Stabilization by State Feedback | `state-feedback` |
| 6.3 | Integral Action | `state-feedback`、`pid-control` |
| 6.4 | Linear Quadratic Regulators | `lqr` |
| 7.1 | Observability | `observability-observer` |
| 7.2 | State Estimation | `observability-observer` |
| 7.3 | Control Using Estimated State | `observability-observer` |
| 7.4 | Kalman Filtering | `kalman-filter` |
| 7.5 | State Space Controller Design | `observability-observer` |
| 8.1 | Frequency Domain Modeling | `bode-plot`、`state-response` |
| 8.2 | The Bode Plot | `bode-plot` |
| 9.1 | The Loop Transfer Function | `nyquist-margins` |
| 9.2 | The Nyquist Criterion | `nyquist-margins` |
| 9.3 | Stability Margins | `nyquist-margins` |
| 9.4 | Bode's Relations and Minimum Phase Systems | `nyquist-margins` |
| 10.1 | Models and Modeling | `mpc-intro` |
| 10.2.1 | Linear Quadratic Problem | `mpc-intro` |
| 10.2.2 | Dynamic Programming Solution | `mpc-intro` |
| 10.2.3 | Controllability | `reachability` |
| 10.3.1 | Linear Optimal State Estimation | `kalman-filter`、`mpc-estimation` |
| 10.3.2 | Moving Horizon Estimation | `mpc-estimation` |
| 10.3.3 | Observability | `observability-observer` |
| 10.4 | Tracking, Disturbances, and Zero Offset | `mpc-estimation` |
| 11.1 | Model Predictive Control | `mpc-intro`、`mpc-stability` |
| 11.2 | Stability | `mpc-stability` |

## CS2023 核心主题（C2）

`scope.json` 对 H.4.1 没有 CS2023 主题；5 个章由上表的课负责。

## 学习资源的章节（C3）

中文主课《自动控制原理》的时域分析（一阶、二阶系统指标，稳态误差）、劳斯判据、根轨迹、PID 与超前滞后校正不在英文大纲里，分别由 `time-response`、`stability-routh`、`root-locus-compensation`、`pid-control` 教；KalmanFilter.NET 的一维例子和 EKF、UKF 由 `kalman-filter` 教；DR_CAN 的代价函数到二次规划由 `mpc-intro` 教。

## 原技能树综合练习（C4）

| 小题 | 内容 | 由哪一课教到 |
|---|---|---|
| (1) | 一阶系统阶跃响应、时间常数和稳态值 | `time-response` |
| (2) | 闭环特征方程、稳定的增益范围、二阶系统的自然频率和阻尼比 | `time-response`、`stability-routh` |
| (3) | PID 三项的作用、积分饱和和抗饱和 | `pid-control` |
| (4) | 状态空间的能控性和开环稳定性 | `reachability`、`state-response` |
| (5) | 一维卡尔曼滤波 | `kalman-filter` |

## 后继技能用到的写法（C5）

必须后继 H.4.6 过程控制还没有内容包；按它的综合练习，PID、阶跃响应、稳态误差、前馈和串级的概念由 `pid-control`、`time-response`、`feedback-intro` 负责。
