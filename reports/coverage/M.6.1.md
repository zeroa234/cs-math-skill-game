# M.6.1 概率论：覆盖表

**状态（2026-11-19）：已写完（v2 重写，按零基础与知识覆盖面标准），等用户验收。** 初稿由云端 Gemini 在另一个仓库写成（16 课），主代理引入后做了三件事：把长卡按“一张卡一个想法”切开（39 张卡切成 68 张，卡片讲解中位数从 617 字降到 325 字），去掉感叹号和夸张措辞，补了这张覆盖表。依据 `../cs-math-skill-tree/output/outlines.json` 的 M.6.1 大纲：A = Grinstead & Snell《Introduction to Probability》第 1–10 章，B = Durrett《Probability: Theory and Examples》第 5 版第 1–3 章与 4.1（大纲编号 11–14）。表里的“原文”是大纲给出的节名，课和节的对应按课的内容判断，没有逐页对照原书。数值核对：`tests/content/M.6.1.verify.py`（只用标准库，88 条，59 道数字题逐一和包里的答案比对）。

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Simulation of Discrete Probabilities | `sample-space`（用频率估计概率）、`inequalities-lln`（两颗骰子抽样演示与操作题） |
| 1.2 | Discrete Probability Distributions | `sample-space`、`rv-discrete-cdf` |
| 2.1 | Simulation of Continuous Probabilities | `counting-prob`（蒙特卡洛估算 π） |
| 2.2 | Continuous Density Functions | `rv-continuous-transform` |
| 3.1 | Permutations | `counting-prob` |
| 3.2 | Combinations | `counting-prob` |
| 4.1 | Discrete Conditional Probability | `cond-prob`、`bayes-paradox` |
| 4.2 | Continuous Conditional Probability | `cond-prob`（均匀分布截断）、`continuous-dist`（无记忆性） |
| 4.3 | Paradoxes | `bayes-paradox`（两孩问题、三门问题、基础率谬误） |
| 5.1 | Important Distributions | `discrete-dist` |
| 5.2 | Important Densities | `continuous-dist`、`normal-joint` |
| 6.1 | Expected Value | `expectation-variance`、`cond-expectation` |
| 6.2 | Variance of Discrete Random Variables | `expectation-variance` |
| 6.3 | Continuous Random Variables | `expectation-variance`（指数分布的期望与方差） |
| 7.1 | Sums of Discrete Random Variables | `normal-joint`（离散卷积）、`mgf-transforms`（泊松之和） |
| 7.2 | Sums of Continuous Random Variables | `normal-joint`（连续卷积、正态之和） |
| 8.1 | Discrete Random Variables | `inequalities-lln` |
| 8.2 | Continuous Random Variables | `inequalities-lln` |
| 9.1 | Bernoulli Trials | `clt-normal-approx`（硬币次数的正态近似） |
| 9.2 | Discrete Independent Trials | `clt-normal-approx` |
| 9.3 | Continuous Independent Trials | `clt-normal-approx`（连续变量的样本均值） |
| 10.1 | Discrete Distributions | `mgf-transforms`（概率生成函数、矩母函数） |
| 10.2 | Branching Processes | 不教：分支过程属于随机过程，归 M.6.3 |
| 10.3 | Continuous Densities | `mgf-transforms`（指数分布的矩母函数） |
| 11.1 | Probability Spaces | `sample-space`（三元组与 σ-代数）、`continuity-measure` |
| 11.2 | Distributions | `rv-discrete-cdf`（分布与 CDF 的性质） |
| 11.3 | Random Variables | `rv-discrete-cdf`（随机变量是可测函数） |
| 11.4 | Expected Value | `expectation-variance`（期望是关于 P 的积分） |
| 11.5 | Inequalities | `inequalities-lln`（马尔可夫、切比雪夫） |
| 11.6 | Integration to the Limit | `continuity-measure`（尖峰反例、单调收敛与控制收敛定理） |
| 12.1 | Weak Laws of Large Numbers | `inequalities-lln` |
| 12.2 | L2 Weak Laws | `inequalities-lln`（方差有限时用切比雪夫证明，就是 L2 弱大数定律） |
| 12.3 | Truncation | 不教：截断是去掉“方差有限”这个条件的证明技巧，超出入门层 |
| 12.4 | Strong Law of Large Numbers | `strong-law-series` |
| 12.5 | Convergence of Random Series | `strong-law-series`（柯尔莫哥洛夫单级数定理） |
| 13.1 | Weak Convergence | `clt-normal-approx`（定义与三种收敛的强弱） |
| 13.2 | Theory | 不教：弱收敛的一般理论（Helly 选择定理、胎紧）超出入门层 |
| 13.3 | Characteristic Functions | 不教：特征函数要用复指数，入门层用矩母函数代替（`mgf-transforms`），超出入门层 |
| 13.4 | Central Limit Theorems | `clt-normal-approx` |
| 13.5 | i.i.d. Sequences | `clt-normal-approx`（独立同分布情形的中心极限定理） |
| 13.6 | Rates of Convergence (Berry-Esseen) | `clt-normal-approx` |
| 14.1 | Examples | `cond-expectation`（掷骰子决定抛硬币次数等例子） |
| 14.2 | Properties | `cond-expectation`（塔性质、提出已知项、独立、线性） |

## 写法上的取舍

- 测度化表述只讲到入门需要的深度：概率空间三元组、为什么事件族不取全部子集（`why-sigma-algebra`）、随机变量的可测性、期望是积分、积分与极限交换的条件。证明都不展开，这部分属于大纲里的“深入层”。
- 11.5 只讲马尔可夫与切比雪夫两个不等式，Jensen、Hölder 等不收：它们在后面的统计和信息论里才用到。
- 强大数定律只给结论和条件（$E|X_1| < \infty$），用滑块序列说明依概率收敛推不出几乎必然收敛，用柯西分布说明条件不能省。证明不讲。
- Berry–Esseen 定理的常数 $C$ 不给具体值，只讲误差按 $1/\sqrt{n}$ 缩小，以及偏度越大需要的样本越多。
- 引入时改动的内容：演示卡原来写“+10”“+500”按钮、“理论折线”，和抽样组件的实际界面（“再抽 1 / 10 / 100 / 1000 次”、横线表示理论概率）不符，已改；“三种收敛的强弱”排序题原来放在弱收敛定义之前，挪到 `clt-normal-approx` 的弱收敛卡后面；`cond-expectation` 原来在“条件概率”章、`mgf-transforms` 原来在“分布”章，两课都用到期望（条件期望还用到随机变量和联合密度），而期望在“期望与极限定理”章才讲，所以两课都改归“期望与极限定理”章、排在 `expectation-variance` 之后（技能树本来也把矩母函数放在这一章），方差例题里原来引用矩母函数算出的 $E[X^2]$，改成用分部积分就地算；结业题里有 3 道和课里例题数字完全相同，换了新数字；车站等车的连续条件概率例子原来把“到达时刻”和“等待时间”混在一起，改成车到站的时间 $X$。

## 核心主题（C2）

`../cs-math-skill-tree/data/curation/scope.json` 给 M.6.1 匹配的 CS2023 主题（都在 MSF-Probability，CS Core）：

| 知识点 | CS2023 原文 | 课 |
|---|---|---|
| 概率空间 | sample spaces, events, probability | `sample-space`、`counting-prob`、`continuity-measure` |
| 随机变量 | Discrete random variables and distributions | `rv-discrete-cdf`、`discrete-dist` |
| 分布 | Continuous random variables and distributions | `rv-continuous-transform`、`continuous-dist`、`normal-joint` |
| 条件概率 | conditional probability, Bayes | `cond-prob`、`bayes-paradox`、`cond-expectation` |
| 期望与极限定理 | Expectation, variance, law of large numbers, central limit theorem | `expectation-variance`、`inequalities-lln`、`strong-law-series`、`clt-normal-approx` |

## 学习资源的章节（C3）

按 `node scripts/skill-brief.mjs M.6.1` 列出的章节核对，只对照了章节标题，没有逐节读讲义。

- 唐聿劼《概率与数理统计》§1.3–§1.8（样本空间、概率的性质、条件概率、独立性、概率的连续性）：`sample-space`、`counting-prob`、`continuity-measure`、`cond-prob`。
- §2、§3、§4.1（离散与连续随机变量、一般随机变量与分布函数、随机变量函数的分布）：`rv-discrete-cdf`、`rv-continuous-transform`、`discrete-dist`、`continuous-dist`。
- §4.3–§4.5（矩与矩母函数、条件分布与条件期望、二维正态）：`mgf-transforms`、`cond-expectation`、`normal-joint`。二维正态分布的密度公式没有单列，`normal-joint` 只讲联合分布、边缘分布和独立。
- §2.5、§3.4、§5（期望与方差、大数定律与中心极限定理）：`expectation-variance`、`inequalities-lln`、`strong-law-series`、`clt-normal-approx`。
- probabilitycourse.com 的概率公理、条件概率、随机变量、分布、期望与矩母函数、极限定理各章同上。

## 综合练习（C4）

| 小题 | 内容 | 课 |
|---|---|---|
| (1) | 两颗骰子和为 7 的概率；已知至少一颗 6 时的条件概率 2/11 | `counting-prob`（例题原题）、`cond-prob`（先猜和分步例题原题） |
| (2) | 患病率 1%、灵敏度 95%、特异度 90% 时阳性者患病的概率 | `bayes-paradox`（先猜和两张卡的例题原题） |
| (3) | Exp(2) 的 $P(X > 1)$、期望、方差、无记忆性 | `continuous-dist`（`exp-survival-prob`、`exp-memoryless-cond`）、`expectation-variance`（`exp-exponential-mean` 与方差例题） |
| (4) | 硬币 100 次，带连续性修正近似 $P(S \ge 60)$ | `clt-normal-approx`（分步例题原题，并和精确值、不修正的结果对比） |

四题的数值都在 verify.py 里核对过，和原技能树的参考答案一致。

## 后继技能（C5）

直接后继里已有或将有内容包的：A.2.1（监督/无监督学习）。它要用的：条件概率与贝叶斯定理（`bayes-paradox`）、期望和方差及其线性性质（`expectation-variance`）、常用分布（`discrete-dist`、`continuous-dist`、`normal-joint`）、独立同分布与大数定律（`inequalities-lln`）。M.6.2 数理统计要的样本均值的期望与方差、中心极限定理和正态近似在 `inequalities-lln`、`clt-normal-approx`。其余后继（M.6.3 随机过程、M.6.5 信息论、M.8.4 蒙特卡洛方法等）还没有内容包；蒙特卡洛估算 π 和抽样演示已在本包出现。
