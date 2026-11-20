# A.2.1 监督、无监督与半监督学习：课程覆盖表

**状态（2026-11-20）：已定稿并核验（v2，按零基础与知识覆盖面标准）。** 依据 `../cs-math-skill-tree/output/outlines.json` 的 A.2.1 大纲（ISLP = James 等《An Introduction to Statistical Learning》第 1–9、12 章；Zhu = Xiaojin Zhu《Semi-Supervised Learning Literature Survey》第 1–4 章）及技能树补充来源（李宏毅《机器学习》2023 Spring、Google MLCC 数据模块、Goodfellow《Deep Learning》第 15 章表示学习、D2L 4.9 环境与分布偏移）。全包共 18 课，覆盖全部 69 个大纲小节；30 项核对断言与全部 20 道数值题已由 `tests/content/A.2.1.verify.py` 独立核对通过。

| 节 | 原文 | 课 |
|---|---|---|
| 1.1.1 | Why Estimate f? | `statistical-learning-basics` |
| 1.1.2 | How Do We Estimate f? | `statistical-learning-basics` |
| 1.1.3 | The Trade-Off Between Prediction Accuracy and Model Interpretability | `statistical-learning-basics` |
| 1.1.4 | Supervised Versus Unsupervised Learning | `statistical-learning-basics` |
| 1.1.5 | Regression Versus Classification Problems | `statistical-learning-basics` |
| 1.2.1 | Measuring the Quality of Fit | `statistical-learning-basics` |
| 1.2.2 | The Bias-Variance Trade-Off | `statistical-learning-basics` |
| 1.2.3 | The Classification Setting | `logistic-regression` |
| 2.1 | Simple Linear Regression | `linear-regression-gd` |
| 2.2 | Multiple Linear Regression | `linear-regression-gd` |
| 2.3 | Other Considerations in the Regression Model | `feature-engineering` |
| 2.4 | The Marketing Plan | `linear-regression-gd` |
| 2.5 | Comparison of Linear Regression with K-Nearest Neighbors | `linear-regression-gd` |
| 3.1 | An Overview of Classification | `logistic-regression` |
| 3.2 | Why Not Linear Regression? | `logistic-regression` |
| 3.3 | Logistic Regression | `logistic-regression` |
| 3.4 | Generative Models for Classification | `generative-classifiers` |
| 3.5 | A Comparison of Classification Methods | `generative-classifiers` |
| 3.6 | Generalized Linear Models | `logistic-regression` |
| 4.1.1 | The Validation Set Approach | `validation-and-learning-settings` |
| 4.1.2 | Leave-One-Out Cross-Validation | `validation-and-learning-settings` |
| 4.1.3 | k-Fold Cross-Validation | `validation-and-learning-settings` |
| 4.1.4 | Bias-Variance Trade-Off for k-Fold Cross-Validation | `validation-and-learning-settings` |
| 4.1.5 | Cross-Validation on Classification Problems | `validation-and-learning-settings` |
| 4.2 | The Bootstrap | `validation-and-learning-settings` |
| 5.1.1 | Best Subset Selection | `feature-selection-regularization` |
| 5.1.2 | Stepwise Selection | `feature-selection-regularization` |
| 5.1.3 | Choosing the Optimal Model | `feature-selection-regularization` |
| 5.2.1 | Ridge Regression | `feature-selection-regularization` |
| 5.2.2 | The Lasso | `feature-selection-regularization` |
| 5.2.3 | Selecting the Tuning Parameter | `feature-selection-regularization` |
| 5.3.1 | Principal Components Regression | `pcr-pls-highdim` |
| 5.3.2 | Partial Least Squares | `pcr-pls-highdim` |
| 5.4.1 | High-Dimensional Data | `pcr-pls-highdim` |
| 5.4.2 | What Goes Wrong in High Dimensions? | `pcr-pls-highdim` |
| 5.4.3 | Regression in High Dimensions | `pcr-pls-highdim` |
| 5.4.4 | Interpreting Results in High Dimensions | `pcr-pls-highdim` |
| 6.1 | Polynomial Regression | `nonlinear-basis-splines` |
| 6.2 | Step Functions | `nonlinear-basis-splines` |
| 6.3 | Basis Functions | `nonlinear-basis-splines` |
| 6.4 | Regression Splines | `nonlinear-basis-splines` |
| 6.5 | Smoothing Splines | `nonlinear-basis-splines` |
| 6.6 | Local Regression | `nonlinear-basis-splines` |
| 6.7 | Generalized Additive Models | `nonlinear-basis-splines` |
| 7.1 | The Basics of Decision Trees | `trees-and-ensembles` |
| 7.2 | Bagging, Random Forests, Boosting, and Bayesian Additive Regression Trees | `trees-and-ensembles` |
| 8.1 | Maximal Margin Classifier | `svm-and-margins` |
| 8.2 | Support Vector Classifiers | `svm-and-margins` |
| 8.3 | Support Vector Machines | `svm-and-margins` |
| 8.4 | SVMs with More than Two Classes | `svm-and-margins` |
| 8.5 | Relationship to Logistic Regression | `svm-and-margins` |
| 9.1 | The Challenge of Unsupervised Learning | `kmeans-clustering` |
| 9.2.1 | What Are Principal Components? | `pca-and-variance` |
| 9.2.2 | Another Interpretation of Principal Components | `pca-and-variance` |
| 9.2.3 | The Proportion of Variance Explained | `pca-and-variance` |
| 9.2.4 | More on PCA | `pca-and-variance` |
| 9.2.5 | Other Uses for Principal Components | `pca-and-variance` |
| 9.3 | Missing Values and Matrix Completion | `matrix-completion-embeddings` |
| 9.4.1 | K-Means Clustering | `kmeans-clustering` |
| 9.4.2 | Hierarchical Clustering | `hierarchical-and-practical` |
| 9.4.3 | Practical Issues in Clustering | `hierarchical-and-practical` |
| 10 | FAQ | `semi-supervised-learning` |
| 11.1 | Identifiability | `semi-supervised-learning` |
| 11.2 | Model Correctness | `semi-supervised-learning` |
| 11.3 | EM Local Maxima | `semi-supervised-learning` |
| 11.4 | Cluster-and-Label | `semi-supervised-learning` |
| 12 | Self-Training | `semi-supervised-learning` |
| 13.1 | Co-Training | `semi-supervised-learning` |
| 13.2 | Multiview Learning | `semi-supervised-learning` |

## 写法上的取舍

- 按技能树 5 个核心章的顺序组织课程：第 1 章「回归/分类」（6 课：`statistical-learning-basics` 到 `svm-and-margins`）、第 2 章「聚类」（2 课）、第 3 章「降维」（2 课）、第 4 章「表示」（3 课：`representation-and-autoencoders`、`autoencoders-and-manifolds`、`matrix-completion-embeddings`）、第 5 章「特征工程与学习设置」（5 课）。
- 为满足零基础 B1 规则（先定义再用，不提前引用后章概念），把“监督 vs 无监督、回归 vs 分类、损失函数、过拟合与偏差–方差权衡”放在第 1 课 `statistical-learning-basics` 作为总览起点，而在第 5 章 `validation-and-learning-settings` 集中展开验证集、LOOCV、k 折交叉验证、Bootstrap 与离线/在线等学习设定。
- 因为 A.2.1 必须前置为 `M.3.1`、`M.6.1`、`M.1.4.1`、`P.2.3`（而 `M.6.2` 仅为推荐前置），本包在讲解最小二乘、逻辑回归与正则化时不假设玩家已经修过 `M.6.2.2`，全部用梯度下降、向量内积、SVD/特征分解与条件概率直接推通。
- 同时引入两类交互练习：`kmeans-clustering` 恢复游戏实验室中的 k-means 互动模拟器（`blobs3`、`k=3`），`logistic-regression` 用 Python 执行追踪（`trace`）让学生单步预测并核对 Sigmoid 概率与二元交叉熵梯度公式。

## 核心主题（C2）

`../cs-math-skill-tree/data/curation/scope.json` 列入的 A.2.1 CS2023 主题：

| 知识点 | CS2023 原文 | 课 |
|---|---|---|
| 回归/分类 | Classification and Regression | `linear-regression-gd`、`logistic-regression`、`generative-classifiers`、`trees-and-ensembles`、`svm-and-margins` |
| 聚类 | Clustering | `kmeans-clustering`、`hierarchical-and-practical` |
| 降维 | Dimension reduction | `pca-and-variance`、`pcr-pls-highdim` |
| 表示 | Representations (Hypothesis spaces) | `representation-and-autoencoders`、`autoencoders-and-manifolds`、`matrix-completion-embeddings` |
| 特征工程 | Simple basis feature expansion | `feature-engineering`、`nonlinear-basis-splines` |

## 学习资源的章节（C3）

- James 等 [ISLP](https://www.statlearning.com/) 第 2–9、12 章：全节映射见上表（总计 61 节，除第 10 章深度学习留给 A.2.3、第 11 章生存分析与第 13 章多重检验外）。
- Xiaojin Zhu [Semi-Supervised Learning Literature Survey](https://pages.cs.wisc.edu/~jerryzhu/pub/ssl_survey.pdf) 第 1–4 章（大纲 10–13.2）：`semi-supervised-learning`。
- Goodfellow 等 [Deep Learning 第 15 章 Representation Learning](https://www.deeplearningbook.org/contents/representation.html) 与李宏毅《机器学习》2023 Spring 自编码器单元：`representation-and-autoencoders`、`autoencoders-and-manifolds`、`matrix-completion-embeddings`。
- Google MLCC 数据模块（数值标准化/分箱、独热/哈希/目标均值编码、特征交叉）与《动手学深度学习》4.9 节学习问题分类：`feature-engineering`、`validation-and-learning-settings`。

## 综合练习（C4）

| 小题 | 内容 | 课 |
|---|---|---|
| (1) | 数据 `(1,1),(2,3),(3,2),(4,5)` 正规方程求 $w=1.1, b=0$ 及 MSE 梯度与一步梯度下降（lr=0.01 -> $w=0.165, b=0.055$） | `linear-regression-gd` |
| (2) | Sigmoid 函数、二元交叉熵损失、梯度 $(p-y)x$ 与 $(p-y)$，以及分类不用 MSE 的原因 | `logistic-regression` |
| (3) | 一维 k-means（`1,2,3,10,11,12`，`k=2`，初值 `1,2`）逐轮分配与收敛结果（`{1,2,3},{10,11,12}`，中心 `2,11`） | `kmeans-clustering` |
| (4) | 协方差矩阵 `[[2,1],[1,2]]` 求特征值 `3,1`、第一主成分方向 $(1,1)/\sqrt{2}$ 与解释方差比例 `75%` | `pca-and-variance` |
| (5) | 训练误差 2%、验证误差 15% 的过拟合诊断、三类应对方法与 k 折交叉验证流程 | `statistical-learning-basics`、`validation-and-learning-settings` |

## 后继技能（C5）

- **A.2.3 深度学习**：需要扎实掌握均方误差与交叉熵损失、线性层计算梯度下降、k-means/MLP 对比直觉、L2 正则化/权重收缩直观动机与训练/验证/测试划分及过拟合判据，分别在 `linear-regression-gd`、`logistic-regression`、`feature-selection-regularization`、`validation-and-learning-settings` 打透。
- **A.4.1 机器学习工程与 MLOps**：需要特征编码与防训练–测试泄漏概念、分布偏移与验证评估工作流，已在 `feature-engineering` 与 `validation-and-learning-settings` 讲清。
