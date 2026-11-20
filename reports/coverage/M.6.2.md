# M.6.2 数理统计：覆盖表

**状态（2026-11-20）：已写完（v2 重写，按零基础与知识覆盖面标准）。** 依据 `../cs-math-skill-tree/output/outlines.json` 的 M.6.2 大纲（A = Penn State STAT 415《Introduction to Mathematical Statistics》第 1–11 课）以及技能树章来源（唐聿劼《概率与数理统计》第 6–9 章与附录 C）。全包共 18 课，覆盖全部 65 个大纲小节；数值与概率积分均由 `tests/content/M.6.2.verify.py` 独立核算（74 条断言，43 道数字题逐一比对）并与包内题库对齐。

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | The Basics | `sampling-order` |
| 1.2 | Probability Density Functions | `sampling-dists` |
| 1.3 | Summary | `sampling-order` |
| 2.1.1 | Point Estimator | `point-estimators` |
| 2.1.2 | Point Estimate | `point-estimators` |
| 2.2.1 | Bias | `point-estimators` |
| 2.2.2 | Variance and Mean Squared Error | `point-estimators` |
| 2.3 | Summary | `point-estimators` |
| 3.1.1 | Factorization Theorem | `sufficiency-mom` |
| 3.2 | Method of Moments | `sufficiency-mom` |
| 3.3 | Summary | `sufficiency-mom` |
| 4.1 | The Basic Idea | `likelihood-mle` |
| 4.2.1 | Steps to Find the MLE (One Parameter Case) | `likelihood-mle` |
| 4.3 | Maximize the Likelihood Directly: Support Parameters | `mle-support-multi` |
| 4.4 | Multiparameter Case | `mle-support-multi` |
| 4.5 | Summary | `mle-support-multi` |
| 5.1 | Introduction to R | `numeric-mle`（统计软件与数值优化工作流对照） |
| 5.2.1 | MLE Through Grid Search | `numeric-mle` |
| 5.2.2 | Numerical MLE: The Idea | `numeric-mle` |
| 5.2.3 | Newton’s Method Approach Idea | `numeric-mle` |
| 5.2.4 | Numerical Optimization in R | `numeric-mle` |
| 5.2.5 | Numerical MLE in R | `numeric-mle` |
| 5.3 | Summary | `numeric-mle` |
| 6.1 | Introduction to Confidence Intervals | `ci-normal-exact` |
| 6.2 | Population Mean of a Normal Distribution | `ci-normal-exact` |
| 6.3 | Interpretation | `ci-normal-exact` |
| 6.4 | Large Sample Confidence Intervals | `ci-large-mle` |
| 6.5 | Summary | `ci-large-mle` |
| 7.1 | Properties of MLEs | `consistency-delta`（相合性与渐近正态概念）、`fisher-asymptotic`（MLE 大样本性质） |
| 7.2.1 | Single Parameter Case | `fisher-asymptotic` |
| 7.2.2 | Multiple Parameter Case | `fisher-asymptotic` |
| 7.2.3 | Summary: The Asymptotic 95% Confidence Interval | `ci-large-mle` |
| 7.3.1 | Single Parameter Case | `fisher-asymptotic` |
| 7.3.2 | Multiple Parameter Case | `fisher-asymptotic` |
| 7.4 | Summary | `fisher-asymptotic` |
| 8.1.1 | Asymptotic Normal CIs for t-distributed data | `ci-bootstrap` |
| 8.1.2 | The Parametric Bootstrap | `ci-bootstrap` |
| 8.1.3 | Nonparametric Bootstrap Confidence Intervals | `ci-bootstrap` |
| 8.1.4 | Template Code for Bootstrap Confidence Intervals | `ci-bootstrap` |
| 8.1.5 | A Two-parameter Example with Pareto Distributed Data | `ci-bootstrap` |
| 8.2.1 | The Delta Method | `consistency-delta` |
| 8.2.2 | Bootstrap and Transformations | `ci-bootstrap` |
| 8.3 | Summary | `ci-bootstrap` |
| 9.1.1 | Basic Terms | `hypothesis-logic` |
| 9.1.2 | The Logic of Hypothesis Testing | `hypothesis-logic` |
| 9.1.3 | Power | `power-and-sample-size` |
| 9.1.4 | Steps for Hypothesis Testing | `hypothesis-logic` |
| 9.2 | Tests about Proportions | `tests-normal-duality` |
| 9.3 | Possible Errors | `errors-and-power` |
| 9.4 | The p-value Approach | `hypothesis-logic` |
| 9.5.1 | Variance Known | `tests-normal-duality` |
| 9.5.2 | Variance Unknown | `tests-normal-duality` |
| 9.6 | Summary | `hypothesis-logic` |
| 10.1 | Other Hypothesis Test Examples | `tests-normal-duality` |
| 10.2 | Linking Confidence Intervals to Hypothesis Tests | `tests-normal-duality` |
| 10.3.1 | Definition of Power | `power-and-sample-size` |
| 10.3.2 | Power Functions | `power-and-sample-size` |
| 10.3.3 | Calculating Sample Size | `power-and-sample-size` |
| 10.4.1 | The Step Up | `wald-and-multi` |
| 10.4.2 | A Recipe for Wald Tests | `wald-and-multi` |
| 10.4.3 | Examples of Hypothesis Testing | `wald-and-multi` |
| 10.5 | Summary | `wald-and-multi` |
| 11.1 | Subjective Probability | `bayesian-decision` |
| 11.2 | Bayesian Estimation | `bayesian-decision` |
| 11.3.1 | Summary | `bayesian-decision` |

## 写法上的取舍

- 游戏章序按中文讲义把「渐近理论与决策」排在「似然」「置信区间」「检验」之前（第 3 章）。为避免未学先用，第 3 章以已经学过的样本均值和矩估计为例讲相合性、Delta 方法和决策错误权衡（同时预先界定零假设、显著性水平、两类错误与功效），第 4 章再展开 MLE 与 Fisher 信息，第 5 章构造各类精确/渐近/自助法置信区间及预测区间，第 6 章完整收束检验步骤、$p$ 值与多参数 Wald 检验。
- R 语言第 5 课与自助法模板代码（5.1、5.2.4、5.2.5、8.1.4）按数值优化算法流程（目标函数设为负对数似然、初值敏感性、Hessian 近似标准误与重抽步骤）讲解，避免硬塞 R 专属语法细节；`M.6.2` 仅必学前置 `M.6.1`，故不用 Python 循环或函数代码块，保持数学表达与结构化步骤自洽。
- 依据中文讲义 §6.2 与 §9.5 补充三大抽样分布（$\chi^2, t, F$）与非参数符号/秩和检验直觉，并针对与样本平均不同维度的新样本，专设“置信区间 vs 预测区间”对比例题。
- 统计用语与 `D.3.1` 保持口径一致（如统计量、抽样分布、偏差、标准误、置信区间、预测区间、零假设、$p$ 值、自助法）。

## 核心主题（C2）

`../cs-math-skill-tree/data/curation/scope.json` 给 M.6.2 匹配的 CS2023 主题（`MSF-Statistics`）：

| 知识点 | 层级 | CS2023 原文 | 课 |
|---|---|---|---|
| 抽样分布 | KA Core | Sampling, bias, adequacy of samples | `sampling-order`、`sampling-dists` |
| 估计 | CS Core | Univariate data: point estimation, confidence intervals | `point-estimators`、`sufficiency-mom` |
| 检验 | KA Core | Hypothesis testing | `errors-and-power`、`power-and-sample-size`、`hypothesis-logic`、`tests-normal-duality`、`wald-and-multi` |
| 似然 | CS Core | Calculate maximum likelihood estimates | `likelihood-mle`、`mle-support-multi`、`numeric-mle`、`fisher-asymptotic` |
| 置信区间 | CS Core | Univariate data: point estimation, confidence intervals | `ci-normal-exact`、`ci-large-mle`、`ci-bootstrap` |

## 学习资源的章节（C3）

- 唐聿劼《概率与数理统计》§6.2–§6.3（三大抽样分布 $\chi^2, t, F$ 与顺序统计量分布）：`sampling-order`、`sampling-dists`。
- §7.2–§7.3（点估计无偏性/MSE/相合性、矩估计与最大似然估计）：`point-estimators`、`sufficiency-mom`、`consistency-delta`、`likelihood-mle`、`mle-support-multi`。
- §8.1–§8.3（单/双总体正态置信区间与大样本区间）：`ci-normal-exact`、`ci-large-mle`。
- §9.1–§9.5 与附录 C（假设检验逻辑、Neyman–Pearson、单/双总体 $z/t/F$ 检验、非参数检验、两类错误与功效）：`errors-and-power`、`hypothesis-logic`、`tests-normal-duality`、`wald-and-multi`。
- Penn State STAT 415 第 1–11 课全章对应见上方大纲映射表。

## 综合练习（C4）

| 小题 | 内容 | 课 |
|---|---|---|
| (1) | 10 个零件长度样本求均值、样本标准差与未知方差下的 95% $t$ 置信区间 | `sampling-dists`、`point-estimators`、`ci-normal-exact` |
| (2) | 检验 $H_0: \mu = 5.3$（$\alpha = 0.05$），计算 $t$ 统计量、结论与 $p$ 值含义 | `hypothesis-logic`、`tests-normal-duality` |
| (3) | $\mathrm{Poisson}(\lambda)$ 的 MLE 推导及无偏性检验 | `likelihood-mle` |
| (4) | 区分 95% 置信区间与新观测 95% 预测区间，解释宽度差异公式 | `ci-normal-exact` |

## 后继技能（C5）

直接后继里有内容包的为 **M.6.2.2 回归与统计建模**（将同批编写）：它需要用到的样本方差无偏性、$t$ 分布与 $F$ 分布、均方误差（偏差–方差分解）、最小二乘/MLE 联系、标准误与置信/预测区间、假设检验、$p$ 值与 Wald 检验均已在本包对应课里铺平；其余后继（M.6.2.1 贝叶斯统计、M.6.2.3 实验设计与因果推断、M.6.2.4 高维统计与统计学习理论、A.1.2、A.2.2）目前尚无内容包，本包已为其留好充分统计量、信息量、贝叶斯共轭更新与偏差-方差分解基础。
