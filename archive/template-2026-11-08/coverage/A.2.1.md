# A.2.1 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1.1.1 | Why Estimate f? | `linear` |
| 1.1.2 | How Do We Estimate f? | `linear` |
| 1.1.3 | The Trade-Off Between Prediction Accuracy and Model Interpretability | `linear` |
| 1.1.4 | Supervised Versus Unsupervised Learning | `validation` |
| 1.1.5 | Regression Versus Classification Problems | `linear` |
| 1.2.1 | Measuring the Quality of Fit | `validation` |
| 1.2.2 | The Bias-Variance Trade-Off | `validation` |
| 1.2.3 | The Classification Setting | `classify` |
| 2.1 | Simple Linear Regression | `linear` |
| 2.2 | Multiple Linear Regression | `linear` |
| 2.3 | Other Considerations in the Regression Model | `linear` |
| 2.4 | The Marketing Plan | `linear` |
| 2.5 | Comparison of Linear Regression with K-Nearest Neighbors | `linear` |
| 3.1 | An Overview of Classification | `classify` |
| 3.2 | Why Not Linear Regression? | `classify` |
| 3.3 | Logistic Regression | `classify` |
| 3.4 | Generative Models for Classification | `classify` |
| 3.5 | A Comparison of Classification Methods | `classify` |
| 3.6 | Generalized Linear Models | `classify` |
| 4.1.1 | The Validation Set Approach | `validation` |
| 4.1.2 | Leave-One-Out Cross-Validation | `validation` |
| 4.1.3 | k-Fold Cross-Validation | `validation` |
| 4.1.4 | Bias-Variance Trade-Off for k-Fold Cross-Validation | `validation` |
| 4.1.5 | Cross-Validation on Classification Problems | `validation` |
| 4.2 | The Bootstrap | `validation` |
| 5.1.1 | Best Subset Selection | `select-features` |
| 5.1.2 | Stepwise Selection | `select-features` |
| 5.1.3 | Choosing the Optimal Model | `select-features` |
| 5.2.1 | Ridge Regression | `select-features` |
| 5.2.2 | The Lasso | `select-features` |
| 5.2.3 | Selecting the Tuning Parameter | `select-features` |
| 5.3.1 | Principal Components Regression | `reduced-regression` |
| 5.3.2 | Partial Least Squares | `reduced-regression` |
| 5.4.1 | High-Dimensional Data | `reduced-regression` |
| 5.4.2 | What Goes Wrong in High Dimensions? | `reduced-regression` |
| 5.4.3 | Regression in High Dimensions | `reduced-regression` |
| 5.4.4 | Interpreting Results in High Dimensions | `reduced-regression` |
| 6.1 | Polynomial Regression | `features` |
| 6.2 | Step Functions | `features` |
| 6.3 | Basis Functions | `features` |
| 6.4 | Regression Splines | `features` |
| 6.5 | Smoothing Splines | `features` |
| 6.6 | Local Regression | `features` |
| 6.7 | Generalized Additive Models | `features` |
| 7.1 | The Basics of Decision Trees | `trees-margin` |
| 7.2 | Bagging, Random Forests, Boosting, and Bayesian Additive Regression Trees | `trees-margin` |
| 8.1 | Maximal Margin Classifier | `trees-margin` |
| 8.2 | Support Vector Classifiers | `trees-margin` |
| 8.3 | Support Vector Machines | `trees-margin` |
| 8.4 | SVMs with More than Two Classes | `trees-margin` |
| 8.5 | Relationship to Logistic Regression | `trees-margin` |
| 9.1 | The Challenge of Unsupervised Learning | `clusters` |
| 9.2.1 | What Are Principal Components? | `pca` |
| 9.2.2 | Another Interpretation of Principal Components | `pca` |
| 9.2.3 | The Proportion of Variance Explained | `pca` |
| 9.2.4 | More on PCA | `pca` |
| 9.2.5 | Other Uses for Principal Components | `pca` |
| 9.3 | Missing Values and Matrix Completion | `representation` |
| 9.4.1 | K-Means Clustering | `clusters` |
| 9.4.2 | Hierarchical Clustering | `clusters` |
| 9.4.3 | Practical Issues in Clustering | `clusters` |
| 10 | FAQ | `semi-supervised` |
| 11.1 | Identifiability | `semi-supervised` |
| 11.2 | Model Correctness | `semi-supervised` |
| 11.3 | EM Local Maxima | `semi-supervised` |
| 11.4 | Cluster-and-Label | `semi-supervised` |
| 12 | Self-Training | `semi-supervised` |
| 13.1 | Co-Training | `semi-supervised` |
| 13.2 | Multiview Learning | `semi-supervised` |

## 核心主题、综合练习与后继技能

CS2023 的回归、分类、聚类、降维、表示和基展开依次在 `linear`、`classify`、`clusters`、`pca`、`representation`、`features`。原综合练习的梯度、逻辑回归、k-means、PCA、泛化依次见 `linear`、`classify`、`clusters`、`pca`、`validation`。A.2.3 使用的损失与梯度、A.4.1 使用的特征处理与验证分别在 `linear` / `classify`、`features` / `validation`。依据 [ISLP](https://www.statlearning.com/) 和 [Zhu 半监督学习综述](https://pages.cs.wisc.edu/~jerryzhu/pub/ssl_survey.pdf)。
