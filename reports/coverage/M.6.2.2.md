# M.6.2.2 回归与统计建模：覆盖表

**状态（2026-11-20）：已定稿并核验（v2，按零基础与知识覆盖面标准）。** 依据 `../cs-math-skill-tree/output/outlines.json` 的 M.6.2.2 大纲（A = Penn State STAT 462《Applied Regression Analysis》第 2–12 课；B = James 等《An Introduction to Statistical Learning (ISLP)》第 6 章）以及技能树章来源（上海立信会计金融学院《应用回归分析》与 ISLR/ISLP 第 3、4、6 章）。全包共 13 课，覆盖全部 65 个大纲小节；51 项核对断言与全部 27 道数值题已由 `tests/content/M.6.2.2.verify.py` 独立核对通过。

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | What is Simple Linear Regression? | `simple-linear-regression` |
| 1.2 | What is the "Best Fitting Line"? | `simple-linear-regression` |
| 1.3 | The Simple Linear Regression Model | `simple-linear-regression` |
| 1.4 | What is the Common Error Variance? | `simple-linear-regression` |
| 1.5 | The Coefficient of Determination, r-squared | `simple-linear-regression` |
| 1.6 | R-squared Cautions | `simple-linear-regression` |
| 2.1 | Inference for the Population Intercept and Slope | `regression-inference-anova` |
| 2.2 | Sums of Squares | `regression-inference-anova` |
| 2.3 | Analysis of Variance: The Basic Idea | `regression-inference-anova` |
| 2.4 | The Analysis of Variance (ANOVA) table and the F-test | `regression-inference-anova` |
| 2.5 | The Lack of Fit F-test When There Are Replicates | `regression-inference-anova` |
| 3.1 | Residuals | `residual-diagnostics` |
| 3.2 | Residuals vs. Fits Plot | `residual-diagnostics` |
| 3.3 | Residuals vs. Predictor Plot | `residual-diagnostics` |
| 3.4 | Identifying Specific Problems Using Residual Plots | `residual-diagnostics` |
| 3.5 | Residuals vs. Order Plot | `residual-diagnostics` |
| 3.6 | Normal Probability Plot of Residuals | `residual-diagnostics` |
| 3.7 | Estimation and Prediction Research Questions | `confidence-and-prediction` |
| 3.8 | Confidence Interval for the Mean Response | `confidence-and-prediction` |
| 3.9 | Prediction Interval for a New Response | `confidence-and-prediction` |
| 4.1 | The Multiple Linear Regression Model | `multiple-regression-matrix` |
| 4.2 | A Matrix Formulation of the Multiple Regression Model | `multiple-regression-matrix` |
| 4.3 | Three Types of MLR Parameter Tests | `regression-inference-anova` |
| 4.4 | The General Linear F-Test | `regression-inference-anova` |
| 4.5 | MLR Parameter Tests | `regression-inference-anova` |
| 4.6 | Partial R-squared | `regression-inference-anova` |
| 5.1 | MLR Model Assumptions | `residual-diagnostics` |
| 5.2 | Assessing the Model Assumptions | `residual-diagnostics` |
| 5.3 | Tests for Error Normality | `residual-diagnostics` |
| 5.4 | Tests for Constant Error Variance | `residual-diagnostics` |
| 5.5 | Confidence Interval for the Mean Response | `confidence-and-prediction` |
| 5.6 | Prediction Interval for a New Response | `confidence-and-prediction` |
| 6.1 | Log-transforming Only the Predictor for SLR | `transforms-and-nonlinear` |
| 6.2 | Log-transforming Only the Response for SLR | `transforms-and-nonlinear` |
| 6.3 | Log-transforming Both the Predictor and Response for SLR | `transforms-and-nonlinear` |
| 6.4 | Other Data Transformations | `transforms-and-nonlinear` |
| 6.5 | Further Transformation Advice and Box-Cox | `transforms-and-nonlinear` |
| 6.6 | Interactions Between Quantitative Predictors | `categorical-and-interactions` |
| 6.7 | Polynomial Regression | `transforms-and-nonlinear` |
| 7.1 | The Basics of Indicator Variables | `categorical-and-interactions` |
| 7.2 | Coding Qualitative Variables | `categorical-and-interactions` |
| 7.3 | Additive Effects | `categorical-and-interactions` |
| 7.4 | Interaction Effects | `categorical-and-interactions` |
| 7.5 | Leaving an Important Interaction Out of a Model | `categorical-and-interactions` |
| 8.1 | Distinction Between Outliers and High Leverage Observations | `outliers-leverage` |
| 8.2 | Using Leverages to Help Identify Extreme X Values | `outliers-leverage` |
| 8.3 | Identifying Outliers (Unusual Y Values) | `outliers-leverage` |
| 8.4 | Studentized Residuals | `outliers-leverage` |
| 8.5 | Identifying Influential Data Points | `outliers-leverage` |
| 8.6 | A Strategy for Dealing with Problematic Data Points | `outliers-leverage` |
| 9.1 | Nonconstant Variance and Weighted Least Squares | `heteroscedasticity-collinearity` |
| 9.2 | Autocorrelation and Time Series Methods | `heteroscedasticity-collinearity` |
| 9.3 | Multicollinearity | `heteroscedasticity-collinearity` |
| 9.4 | Detecting Multicollinearity Using Variance Inflation Factors | `heteroscedasticity-collinearity` |
| 9.5 | Reducing Data-based Multicollinearity | `heteroscedasticity-collinearity` |
| 10.1 | Stepwise Regression | `subset-and-model-selection` |
| 10.2 | Best Subsets Regression, Adjusted R-Sq, Mallows Cp | `subset-and-model-selection` |
| 10.3 | Information Criteria and PRESS | `subset-and-model-selection` |
| 10.4 | Cross-validation | `subset-and-model-selection` |
| 10.5 | One Model Building Strategy | `subset-and-model-selection` |
| 11.1 | Logistic Regression | `logistic-poisson-glm` |
| 11.2 | Poisson Regression | `logistic-poisson-glm` |
| 11.3 | Generalized Linear Models | `logistic-poisson-glm` |
| 11.4 | Nonlinear Regression | `transforms-and-nonlinear` |
| 12 | Linear Model Selection and Regularization | `subset-and-model-selection`、`ridge-and-lasso`、`pcr-pls-highdim` |

## 写法上的取舍

- 按照游戏章序（第 1 章「线性/广义线性模型」、第 2 章「残差诊断与不确定性」、第 3 章「正则化」），先建立最小二乘、设计矩阵、正规方程、变量变换、定性编码与广义线性模型框架，再集中讲方差分析、系数检验、残差图、置信/预测区间与影响点/共线性诊断，最后以子集选择、信息准则、交叉验证、岭回归、Lasso 与 PCR/PLS 收尾。
- 因为本技能同时要求 `M.6.2`（数理统计）和 `M.3.1`（线性代数），正态回归的标准误与正规方程可以直接衔接 $\mathbf{X}^\top\mathbf{X}\hat{\boldsymbol{\beta}} = \mathbf{X}^\top\mathbf{y}$ 与统计推断，不再重复从零定义矩阵、投影、$t$ 分布和假设检验基础。
- 第 1 章注记说明完整指数族 GLM 属于进一步课程，本包按课标讲透 Logistic 回归（logit 连接与发生比）、泊松回归（对数连接）和非线性参数回归的区别；第 3 章按 ISLP 第 6 章补全岭回归闭式解、Lasso 稀疏几何直觉、弹性网、PCR 与 PLS 对比。

## 核心主题（C2）

`../cs-math-skill-tree/data/curation/scope.json` 给 M.6.2.2 匹配的 CS2023 主题：

| 知识点 | 单位 | 层级 | CS2023 原文 | 课 |
|---|---|---|---|---|
| 线性/广义线性模型 | MSF-Statistics | KA Core | Multivariate data: estimation, correlation, regression | `simple-linear-regression`、`multiple-regression-matrix`、`logistic-poisson-glm` |
| 正则化 | AI-ML | KA Core | Regularization to avoid overfitting | `subset-and-model-selection`、`ridge-and-lasso`、`pcr-pls-highdim` |

## 学习资源的章节（C3）

- ISLR / ISLP 第 3 章（Linear Regression：一元/多元回归、定性预测与交互、残差与杠杆诊断、系数标准误与区间）：`simple-linear-regression`、`multiple-regression-matrix`、`categorical-and-interactions`、`regression-inference-anova`、`residual-diagnostics`、`confidence-and-prediction`、`outliers-leverage`、`heteroscedasticity-collinearity`。
- ISLR / ISLP 第 4 章（Classification：Logistic 回归、连接函数与优势比；注：LDA 可见于多类分类对照，完整判别分析在 A.2.1 展开）：`logistic-poisson-glm`。
- ISLR / ISLP 第 6 章（Linear Model Selection and Regularization：子集选择、$C_p$/AIC/BIC/调整 $R^2$、交叉验证、岭回归、Lasso、PCR/PLS）：`subset-and-model-selection`、`ridge-and-lasso`、`pcr-pls-highdim`。
- STAT 462 第 2–12 课与中国大学 MOOC《应用回归分析》各单元全节对照见上方 65 行大纲表。

## 综合练习（C4）

| 小题 | 内容 | 课 |
|---|---|---|
| (1) | 数据 `(1,2),(2,3),(3,5),(4,4),(5,6)` 求最小二乘直线与决定系数 $R^2$ | `simple-linear-regression` |
| (2) | 写出设计矩阵 $X$ 和正规方程 $X^\top X \beta = X^\top y$ 重新求解系数 | `multiple-regression-matrix` |
| (3) | “漏斗形”残差图诊断（异方差）、对推断的影响及对数/WLS/稳健标准误处理 | `residual-diagnostics`、`heteroscedasticity-collinearity` |
| (4) | 斜率 $b_1$ 的解释与观察数据中关联不等于因果的辨析 | `simple-linear-regression` |

## 后继技能（C5）

直接后继为 **M.6.2.4 高维统计与统计学习理论** 与 **M.6.4 时间序列分析**（目前均无内容包）。依据其综合练习需求：`M.6.2.4` 直接用到岭回归矩阵解 $(\mathbf{X}^\top\mathbf{X} + \lambda \mathbf{I})^{-1}\mathbf{X}^\top\mathbf{y}$ 与 Lasso 稀疏收缩特征选择，`M.6.4` 直接用到残差自相关诊断，均已分别在 `ridge-and-lasso` 与 `heteroscedasticity-collinearity` 中落实。
