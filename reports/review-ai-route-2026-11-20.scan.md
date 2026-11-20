## M.6.2

### 1. 正确项是最长的选项：38/44（86%；结业挑战 2/2）

`sampling-order/guess`、`sampling-order/identify-statistic`、`sampling-dists/t-dist-df-reason`、`point-estimators/guess`、`point-estimators/estimator-vs-estimate`、`point-estimators/bias-variance-tradeoff-choice`、`sufficiency-mom/guess`、`sufficiency-mom/factorization-poisson`、`sufficiency-mom/sufficiency-summary-choice`、`consistency-delta/guess`、`consistency-delta/consistency-vs-unbiased`、`errors-and-power/guess`、`errors-and-power/power-factors-choice`、`bayesian-decision/guess`、`bayesian-decision/credible-vs-confidence`、`likelihood-mle/guess`、`likelihood-mle/prob-vs-likelihood`、`likelihood-mle/mle-second-deriv-check`、`mle-support-multi/guess`、`mle-support-multi/uniform-mle-deriv-fail`、`numeric-mle/guess`、`numeric-mle/why-min-neg-loglik`、`ci-normal-exact/guess`、`ci-normal-exact/ci-interpretation-choice`、`ci-large-mle/guess`、`ci-large-mle/large-sample-caveat`、`ci-large-mle/ci-choice-comparison`、`ci-bootstrap/guess`、`ci-bootstrap/param-vs-nonparam-boot`、`ci-bootstrap/bootstrap-transform-why`、`hypothesis-logic/guess`、`hypothesis-logic/pvalue-meaning-choice`、`hypothesis-logic/statistical-vs-practical`、`tests-normal-duality/nonparametric-when-choice`、`wald-and-multi/guess`、`wald-and-multi/wald-vs-lrt-choice`、`结业/b-pred-vs-ci`、`结业/b-pvalue-wald`

### 2. 从前置技能继承的查词（37 个，逐个确认在这里意思对得上）

- **参数**（首次 `sampling-order/卡「简单随机样本与统计量」`）：刻画一族概率分布具体形状和位置的固定常数，如二项分布的 (n, p) 或指数分布的 λ
- **随机变量**（首次 `sampling-order/卡「简单随机样本与统计量」`）：把样本空间里的每一个基本结果映射为一个实数的规则 X: Ω → ℝ，用来把随机现象变成可计算的数
- **方差**（首次 `sampling-order/卡「简单随机样本与统计量」`）：衡量随机变量取值相对期望的离散程度：偏离期望的平方的期望 Var(X) = E[(X − μ)²]
- **函数**（首次 `sampling-order/卡「抽样分布与顺序统计量」`）：一条规则：每个输入恰好对应一个输出，写作 f(x)
- **独立同分布**（首次 `sampling-order/卡「例子：求样本最大值与最小值的」`）：一列随机变量彼此相互独立，且每一个都服从完全相同的概率分布，常简写为 i.i.d.
- **累积分布函数**（首次 `sampling-order/卡「例子：求样本最大值与最小值的」`）：对任意实数 x 给出随机变量不超过 x 的总概率的函数 F(x) = P(X ≤ x)，单调不减且右连续
- **均匀分布**（首次 `sampling-order/max-order-stat-prob`）：在有限区间 [a, b] 上概率密度处处相等（均为 1/(b − a)）、落在任意等长子区间概率相同的连续分布
- **指数分布**（首次 `sampling-order/min-order-stat-exp`）：刻画泊松过程中相邻两次事件等待时间的连续分布，密度为 λe^(−λx)（x ≥ 0），具有无记忆性
- **标准差**（首次 `sampling-dists/guess`）：方差的算术平方根 σ = √Var(X)，与原随机变量保持相同的量纲单位
- **定积分**（首次 `sampling-dists/order-pdf-expectation`）：分段加细后黎曼和的极限，横轴上方贡献记正、横轴下方贡献记负
- **期望**（首次 `sampling-dists/order-pdf-expectation`）：以概率为权重的加权平均值，反映大量独立重复试验结果的长期中心位置，记作 E[X]
- **原函数**（首次 `sampling-dists/order-pdf-expectation`）：求导之后恰好等于指定被积函数 f(x) 的函数 F(x)，加上任意常数 C 构成完整不定积分族
- **正态分布**（首次 `sampling-dists/卡「样本均值的抽样分布与标准误」`）：钟形对称的连续分布 N(μ, σ²)，由均值 μ 决定中心位置、标准差 σ 决定胖瘦，可标准化为 N(0, 1)
- **变量**（首次 `sampling-dists/卡「卡方分布与 t 分布」`）：在算式或过程里可以取不同数值的符号量（如积分哑变量 t 或上限 x）
- **概率质量函数**（首次 `sufficiency-mom/factorization-poisson`）：给出离散型随机变量取到每一个具体值的概率的函数 p(x) = P(X = x)，所有取值概率之和为 1
- **收敛**（首次 `consistency-delta/guess`）：数列或函数值和某个数 L 的距离能变得要多小有多小，并一直保持
- **导数**（首次 `consistency-delta/卡「Delta 方法：把分布传播」`）：f′(a) = lim_{h→0} [f(a + h) − f(a)]/h：曲线在 a 处切线的斜率，也是 a 处的瞬时变化率
- **绝对值**（首次 `consistency-delta/delta-reciprocal-se`）：去掉负号后的数，|−3| = 3；|a − b| 是 a 和 b 在数轴上的距离
- **整数**（首次 `errors-and-power/卡「例子：同时保住 α 和功效所」`）：没有小数部分的数：…、−2、−1、0、1、2、…
- **贝叶斯定理**（首次 `bayesian-decision/guess`）：已知结果反推原因的公式：P(H | E) = P(H)P(E | H) / P(E)，用新证据把先验概率更新为后验概率
- **联合分布**（首次 `likelihood-mle/卡「似然函数与对数似然」`）：同时描述两个或多个随机变量共同取值规律的概率质量函数或概率密度函数
- **概率密度**（首次 `likelihood-mle/卡「似然函数与对数似然」`）：连续型随机变量在各点附近的概率密集程度 f(x)，在区间 [a, b] 上的定积分才是该区间的概率
- **单调**（首次 `likelihood-mle/卡「似然函数与对数似然」`）：一直不减（单调递增）或一直不增（单调递减）
- **开区间**（首次 `likelihood-mle/卡「求单参数最大似然估计的四个步」`）：(a, b)：a < x < b 的所有数，不含两端
- **自然对数**（首次 `likelihood-mle/卡「求单参数最大似然估计的四个步」`）：ln x：eˣ 的反函数，ln y = x 等价于 eˣ = y；(ln x)′ = 1/x
- **驻点**（首次 `likelihood-mle/卡「求单参数最大似然估计的四个步」`）：导数等于 0 的点
- **二阶导数**（首次 `likelihood-mle/卡「求单参数最大似然估计的四个步」`）：导数的导数 f″ = (f′)′，也写作 d²y/dx²
- **伯努利试验**（首次 `likelihood-mle/mle-bernoulli-calc`）：只有“成功”（记 1，概率 p）和“失败”（记 0，概率 1 − p）两种结果的单次随机试验
- **二次近似**（首次 `numeric-mle/卡「牛顿法：利用曲率快速找根」`）：f(x) ≈ f(a) + f′(a)(x − a) + f″(a)/2·(x − a)²：最贴近曲线的抛物线
- **切线**（首次 `numeric-mle/卡「牛顿法：利用曲率快速找根」`）：割线的两点越靠越近时的极限位置；切线的斜率就是导数
- **有界**（首次 `fisher-asymptotic/卡「单参数 MLE 的渐近分布与」`）：所有项（或函数值）都夹在两个固定的数之间
- **协方差**（首次 `fisher-asymptotic/卡「多参数 MLE 的渐近协方差」`）：衡量两个随机变量协同变化方向和程度的量 Cov(X, Y) = E[(X − μ_X)(Y − μ_Y)]
- **无穷大**（首次 `ci-normal-exact/pred-interval-margin`）：绝对值变得比任何数都大的量，如 x → 0 时的 1/x²
- **中心极限定理**（首次 `ci-large-mle/guess`）：大量独立同分布且方差有限的随机变量之和，经标准化后其分布趋近于标准正态分布 N(0, 1)
- **条件概率**（首次 `hypothesis-logic/卡「p 值的精确含义与常见误区」`）：在已知事件 B 已经发生的前提下，把样本空间缩小到 B 后事件 A 发生的概率，记作 P(A | B) = P(A ∩ B) / P(B)
- **补事件**（首次 `结业/b-order-stat`）：样本空间中不包含在事件 A 里的其余全部结果，记作 Aᶜ，满足 P(Aᶜ) = 1 − P(A)
- **泊松分布**（首次 `结业/b-mle-poisson`）：刻画固定时间或空间内稀有随机事件发生次数的离散分布，期望与方差都等于平均发生率 λ

### 3. 本包没有加粗讲解、也不在 terms 里的英文词（3 个，候选“没讲就用”）

PMF（`likelihood-mle/prob-vs-likelihood`）、Fisher Information（`fisher-asymptotic/卡「Fisher 信息量（Fis」`）、LRT（`wald-and-multi/wald-vs-lrt-choice`）

### 4. 夸张词（30 处）

- 「绝对」23 处：`point-estimators/bias-variance-tradeoff-choice`、`consistency-delta/guess`、`consistency-delta/卡「例子：用 Delta 方法估」`、`consistency-delta/delta-reciprocal-se`、`bayesian-decision/guess`、`bayesian-decision/卡「损失函数与贝叶斯估计」` 等
- 「彻底」3 处：`consistency-delta/guess`、`bayesian-decision/guess`、`mle-support-multi/guess`
- 「极其」2 处：`errors-and-power/guess`、`ci-bootstrap/param-vs-nonparam-boot`
- 「轻松」1 处：`likelihood-mle/卡「似然函数与对数似然」`
- 「狂」1 处：`fisher-asymptotic/guess`

## M.6.2.2

### 1. 正确项是最长的选项：34/40（85%；结业挑战 2/2）

`simple-linear-regression/slr-cautions-choice`、`multiple-regression-matrix/guess`、`multiple-regression-matrix/mlr-ceteris-paribus`、`multiple-regression-matrix/projection-orthogonality`、`categorical-and-interactions/guess`、`categorical-and-interactions/additive-vs-interaction`、`transforms-and-nonlinear/boxcox-choice`、`logistic-poisson-glm/guess`、`logistic-poisson-glm/glm-link-why`、`regression-inference-anova/guess`、`regression-inference-anova/lack-of-fit-choice`、`residual-diagnostics/guess`、`residual-diagnostics/funnel-residual-diag`、`residual-diagnostics/qq-plot-choice`、`confidence-and-prediction/guess`、`confidence-and-prediction/extrapolation-trumpet`、`outliers-leverage/guess`、`outliers-leverage/leverage-vs-outlier`、`outliers-leverage/problem-point-strategy`、`heteroscedasticity-collinearity/guess`、`heteroscedasticity-collinearity/wls-autocorr-choice`、`heteroscedasticity-collinearity/collinearity-consequence-choice`、`subset-and-model-selection/guess`、`subset-and-model-selection/aic-vs-bic`、`subset-and-model-selection/selection-pitfall-choice`、`ridge-and-lasso/ridge-matrix-choice`、`ridge-and-lasso/lasso-vs-ridge-choice`、`ridge-and-lasso/standardize-before-penalty`、`pcr-pls-highdim/guess`、`pcr-pls-highdim/pcr-unsupervised-choice`、`pcr-pls-highdim/highdim-p-gt-n`、`pcr-pls-highdim/pls-vs-pcr-compare`、`结业/b-residual-funnel`、`结业/b-regularization-compare`

### 2. 从前置技能继承的查词（43 个，逐个确认在这里意思对得上）

- **变量**（首次 `simple-linear-regression/卡「简单线性回归模型与误差方差」`）：在算式或过程里可以取不同数值的符号量（如积分哑变量 t 或上限 x）
- **方差**（首次 `simple-linear-regression/卡「简单线性回归模型与误差方差」`）：衡量随机变量取值相对期望的离散程度：偏离期望的平方的期望 Var(X) = E[(X − μ)²]
- **自由度**（首次 `simple-linear-regression/卡「简单线性回归模型与误差方差」`）：计算统计量时能够自由变动的独立信息个数，如样本方差里的 n − 1
- **参数**（首次 `simple-linear-regression/卡「简单线性回归模型与误差方差」`）：刻画一族概率分布具体形状和位置的固定常数，如二项分布的 (n, p) 或指数分布的 λ
- **最小二乘**（首次 `simple-linear-regression/卡「最优拟合直线与决定系数 R²」`）：Ax = b 无解时，取让 ‖b − Ax‖² 最小的 x̂，它满足 AᵀAx̂ = Aᵀb
- **偏差**（首次 `simple-linear-regression/卡「例子：手算最小二乘直线与决定」`）：点估计量的期望减去参数真值的差，即系统性偏离方向；不为零时称为有偏估计
- **标准差**（首次 `simple-linear-regression/slr-error-var`）：方差的算术平方根 σ = √Var(X)，与原随机变量保持相同的量纲单位
- **单调**（首次 `simple-linear-regression/卡「使用 R² 的四个常见注意陷」`）：一直不减（单调递增）或一直不增（单调递减）
- **线性近似**（首次 `simple-linear-regression/slr-cautions-choice`）：用切线代替曲线：x 靠近 a 时 f(x) ≈ f(a) + f′(a)(x − a)
- **矩阵**（首次 `multiple-regression-matrix/卡「多元线性回归与设计矩阵」`）：排成 m 行 n 列的一张数表，叫 m×n 矩阵
- **向量**（首次 `multiple-regression-matrix/卡「几何投影与正规方程」`）：一列有顺序的数，如 (1, 2)；也可以画成从原点出发的箭头
- **长度**（首次 `multiple-regression-matrix/卡「几何投影与正规方程」`）：向量 v 的长度 ‖v‖ = √(v·v)
- **正交**（首次 `multiple-regression-matrix/卡「几何投影与正规方程」`）：两个向量的点积为 0，在图上互相垂直
- **投影**（首次 `multiple-regression-matrix/卡「几何投影与正规方程」`）：b 在一条直线或一个子空间里最接近它的点 p，误差 b − p 和那个子空间正交
- **列空间**（首次 `multiple-regression-matrix/卡「几何投影与正规方程」`）：A 的各列所有线性组合组成的子空间 C(A)；Ax = b 有解当且仅当 b 在里面
- **线性无关**（首次 `multiple-regression-matrix/卡「几何投影与正规方程」`）：只有全取 0 的组合才得到零向量：没有一个向量是其他向量的组合
- **可逆**（首次 `multiple-regression-matrix/卡「几何投影与正规方程」`）：有逆矩阵；n×n 矩阵可逆当且仅当有 n 个主元
- **张成**（首次 `multiple-regression-matrix/卡「多元斜率与投影矩阵视角」`）：一组向量的所有线性组合正好是某个空间时，说它们张成这个空间
- **子空间**（首次 `multiple-regression-matrix/卡「多元斜率与投影矩阵视角」`）：向量空间里的一部分，对加法和数乘封闭，一定包含零向量
- **逆矩阵**（首次 `multiple-regression-matrix/卡「多元斜率与投影矩阵视角」`）：满足 A⁻¹A = AA⁻¹ = I 的矩阵 A⁻¹，把 A 做的事撤销
- **奇异值分解**（首次 `multiple-regression-matrix/卡「多元斜率与投影矩阵视角」`）：A = UΣVᵀ：任何矩阵都能写成 旋转 × 拉伸 × 旋转，简称 SVD
- **多项式**（首次 `transforms-and-nonlinear/卡「多项式回归与真正的非线性回归」`）：由 x 的乘方乘上常数再加起来的式子，如 3x³ − x + 7
- **线性组合**（首次 `transforms-and-nonlinear/卡「多项式回归与真正的非线性回归」`）：把几个向量各乘一个数再加起来：cv + dw
- **函数**（首次 `transforms-and-nonlinear/poly-is-linear-model`）：一条规则：每个输入恰好对应一个输出，写作 f(x)
- **线性变换**（首次 `transforms-and-nonlinear/卡「Box-Cox 变换族与数据」`）：满足 T(cv + dw) = cT(v) + dT(w) 的变换；每个矩阵 A 给出一个：T(x) = Ax
- **自然对数**（首次 `transforms-and-nonlinear/卡「例子：怎样挑选对数、幂变换或」`）：ln x：eˣ 的反函数，ln y = x 等价于 eˣ = y；(ln x)′ = 1/x
- **事件**（首次 `logistic-poisson-glm/logistic-odds-ratio`）：样本空间的子集，也就是你关心的一组基本结果；某次试验落在这个子集里就说事件发生
- **整数**（首次 `logistic-poisson-glm/卡「泊松回归与计数建模」`）：没有小数部分的数：…、−2、−1、0、1、2、…
- **期望**（首次 `logistic-poisson-glm/卡「泊松回归与计数建模」`）：以概率为权重的加权平均值，反映大量独立重复试验结果的长期中心位置，记作 E[X]
- **抽样分布**（首次 `regression-inference-anova/卡「回归系数推断与方差分析表（A」`）：同一个统计量在反复抽样下所有可能取值所服从的概率分布
- **标准误**（首次 `regression-inference-anova/卡「回归系数推断与方差分析表（A」`）：某个估计量或统计量自身抽样分布的标准差，衡量它在不同样本间的波动幅度
- **统计量**（首次 `regression-inference-anova/卡「回归系数推断与方差分析表（A」`）：完全由样本数据算出来的函数或数值，式子里不能含有未知的总体参数
- **置信区间**（首次 `regression-inference-anova/卡「回归系数推断与方差分析表（A」`）：按固定规则由样本算出的随机区间，重复抽样下以预定概率覆盖固定的未知参数真值
- **零假设**（首次 `regression-inference-anova/coef-t-stat`）：假设“没有效果或参数等于基准值”，检验开始时默认站在它这一边看数据是否矛盾
- **正态分布**（首次 `residual-diagnostics/卡「经典线性回归的四大假设（LI」`）：钟形对称的连续分布 N(μ, σ²)，由均值 μ 决定中心位置、标准差 σ 决定胖瘦，可标准化为 N(0, 1)
- **中心极限定理**（首次 `residual-diagnostics/卡「误差正态性检验与 Q-Q 图」`）：大量独立同分布且方差有限的随机变量之和，经标准化后其分布趋近于标准正态分布 N(0, 1)
- **预测区间**（首次 `confidence-and-prediction/guess`）：针对下一次新抽样观测值给出的随机范围，同时包含参数估计误差和个体随机波动
- **维数**（首次 `outliers-leverage/hat-trace-sum`）：空间的任何一组基里向量的个数
- **绝对值**（首次 `outliers-leverage/卡「离群点、学生化残差与影响点」`）：去掉负号后的数，|−3| = 3；|a − b| 是 a 和 b 在数轴上的距离
- **谱定理**（首次 `ridge-and-lasso/ridge-matrix-choice`）：对称矩阵 S 可以写成 QΛQᵀ：特征值都是实数，特征向量可以选成标准正交
- **正定矩阵**（首次 `ridge-and-lasso/ridge-matrix-choice`）：特征值全大于 0 的对称矩阵；等价于 x ≠ 0 时 xᵀSx > 0
- **特征值**（首次 `ridge-and-lasso/ridge-matrix-choice`）：Ax = λx 里的数 λ，是特征向量被拉伸的倍数
- **主成分分析**（首次 `pcr-pls-highdim/guess`）：把数据减去平均后做 SVD，第一个奇异向量是数据散得最开的方向，简称 PCA

### 3. 本包没有加粗讲解、也不在 terms 里的英文词（5 个，候选“没讲就用”）

QR（`multiple-regression-matrix/卡「多元斜率与投影矩阵视角」`）、LINE（`residual-diagnostics/卡「经典线性回归的四大假设（LI」`）、BMI（`heteroscedasticity-collinearity/卡「例子：算出 VIF 并消减多」`）、Mallows Cp（`subset-and-model-selection/卡「调整 R²、Mallows 」`）、OLS（`ridge-and-lasso/卡「例子：对比单特征 OLS 与」`）

### 4. 夸张词（32 处）

- 「绝对」20 处：`simple-linear-regression/卡「使用 R² 的四个常见注意陷」`、`simple-linear-regression/slr-cautions-choice`、`multiple-regression-matrix/guess`、`multiple-regression-matrix/projection-orthogonality`、`regression-inference-anova/guess`、`regression-inference-anova/lack-of-fit-choice` 等
- 「天生」2 处：`logistic-poisson-glm/glm-link-why`、`regression-inference-anova/卡「失拟 F 检验与三类参数检验」`
- 「彻底」5 处：`residual-diagnostics/funnel-residual-diag`、`outliers-leverage/guess`、`heteroscedasticity-collinearity/collinearity-consequence-choice`、`ridge-and-lasso/ridge-matrix-choice`、`pcr-pls-highdim/guess`
- 「足足」1 处：`confidence-and-prediction/卡「例子：对比均值中心处的两条区」`
- 「极度」1 处：`outliers-leverage/guess`
- 「极其」2 处：`outliers-leverage/leverage-vs-outlier`、`ridge-and-lasso/standardize-before-penalty`
- 「一毫秒」1 处：`subset-and-model-selection/selection-pitfall-choice`

## A.2.1

### 1. 正确项是最长的选项：57/64（89%；结业挑战 6/6）

`statistical-learning-basics/guess`、`statistical-learning-basics/task-type-regression-classification`、`linear-regression-gd/guess`、`linear-regression-gd/lr-gd-formula-calc`、`linear-regression-gd/knn-bias-variance`、`logistic-regression/guess`、`logistic-regression/cross-entropy-vs-mse`、`logistic-regression/glm-poisson-choice`、`generative-classifiers/lda-vs-qda-boundary`、`generative-classifiers/compare-classifiers-scenario`、`generative-classifiers/nb-highdim-advantage`、`trees-and-ensembles/guess`、`trees-and-ensembles/rf-mtry-decorrelation`、`trees-and-ensembles/bagging-vs-boosting`、`svm-and-margins/svm-hinge-vs-logistic`、`kmeans-clustering/guess`、`kmeans-clustering/kmeans-convergence-property`、`hierarchical-and-practical/guess`、`hierarchical-and-practical/single-linkage-chaining`、`hierarchical-and-practical/clustering-scaling-issue`、`pca-and-variance/guess`、`pca-and-variance/pca-first-direction-choice`、`pcr-pls-highdim/guess`、`pcr-pls-highdim/pcr-vs-pls-choice`、`pcr-pls-highdim/highdim-p-gt-n-trap`、`pcr-pls-highdim/highdim-causal-warning`、`representation-and-autoencoders/guess`、`representation-and-autoencoders/autoencoder-mechanism`、`representation-and-autoencoders/manifold-autoencoder-vs-pca`、`matrix-completion-embeddings/guess`、`matrix-completion-embeddings/matrix-completion-method`、`matrix-completion-embeddings/dense-embedding-vs-onehot`、`matrix-completion-embeddings/missing-mean-imputation-flaw`、`feature-engineering/guess`、`feature-engineering/feature-cross-purpose`、`feature-engineering/leakage-prevention-choice`、`feature-engineering/log-transform-skew`、`nonlinear-basis-splines/guess`、`nonlinear-basis-splines/spline-vs-poly-vs-gam`、`nonlinear-basis-splines/smoothing-spline-lambda`、`nonlinear-basis-splines/natural-spline-boundary`、`feature-selection-regularization/guess`、`feature-selection-regularization/bic-vs-aic-vs-ols`、`feature-selection-regularization/lasso-vs-ridge-scale`、`validation-and-learning-settings/guess`、`validation-and-learning-settings/bootstrap-prob-choice`、`validation-and-learning-settings/learning-settings-choice`、`semi-supervised-learning/guess`、`semi-supervised-learning/ssl-model-wrong-hurt`、`semi-supervised-learning/co-training-assumptions`、`semi-supervised-learning/self-training-risk`、`结业/b-logistic-ce`、`结业/b-pca-pve`、`结业/b-representation-ae`、`结业/b-tree-svm-compare`、`结业/b-cv-leakage`、`结业/b-ssl-pitfalls`

### 2. 从前置技能继承的查词（58 个，逐个确认在这里意思对得上）

- **参数**（首次 `statistical-learning-basics/卡「为什么要估计 f，以及学习的」`）：刻画一族概率分布具体形状和位置的固定常数，如二项分布的 (n, p) 或指数分布的 λ
- **变量**（首次 `statistical-learning-basics/parametric-vs-interpretable`）：在算式或过程里可以取不同数值的符号量（如积分哑变量 t 或上限 x）
- **分支**（首次 `statistical-learning-basics/卡「监督学习、无监督学习与两大监」`）：if / elif / else 里的每一条路；一次只走其中一条
- **期望**（首次 `statistical-learning-basics/卡「训练、验证与测试分工，以及偏」`）：以概率为权重的加权平均值，反映大量独立重复试验结果的长期中心位置，记作 E[X]
- **方差**（首次 `statistical-learning-basics/卡「训练、验证与测试分工，以及偏」`）：一组数离它们的平均值有多散：各数减平均值后平方、加起来，再除以（个数 − 1）
- **最小二乘**（首次 `linear-regression-gd/guess`）：Ax = b 无解时，取让 ‖b − Ax‖² 最小的 x̂，它满足 AᵀAx̂ = Aᵀb
- **梯度下降**（首次 `linear-regression-gd/guess`）：反复令 x ← x − η∇f(x)，沿负梯度一步步走向函数较小处的方法
- **广播**（首次 `linear-regression-gd/卡「一元/多元线性回归与正规方程」`）：形状不同的数组运算时，NumPy 把长度为 1 的维度自动拉长对齐；形状从右往左比，每一对相等或有一个是 1
- **微分**（首次 `linear-regression-gd/卡「用梯度下降优化 MSE 与 」`）：dy = f′(x)dx：切线上的升高量，是函数增量 Δy 的线性主部
- **链式法则**（首次 `linear-regression-gd/卡「用梯度下降优化 MSE 与 」`）：复合函数的导数：dy/dx = (dy/du)·(du/dx)，即 [f(g(x))]′ = f′(g(x))·g′(x)
- **偏导数**（首次 `linear-regression-gd/卡「用梯度下降优化 MSE 与 」`）：固定其他变量、只让一个变量变时的导数，如 f_x = ∂f/∂x；算法是把其他变量当常数
- **梯度**（首次 `linear-regression-gd/卡「用梯度下降优化 MSE 与 」`）：偏导数构成的向量 ∇f = (f_x, f_y, …)，指向函数增加最快的方向，长度是最大变化率
- **特征值**（首次 `linear-regression-gd/lr-gd-formula-calc`）：Ax = λx 里的数 λ，是特征向量被拉伸的倍数
- **学习率**（首次 `linear-regression-gd/卡「例子：同一组点上的正规方程解」`）：梯度下降每一步 x − η∇f 里的正数 η，决定一步迈多大
- **函数**（首次 `logistic-regression/guess`）：一条规则：每个输入恰好对应一个输出，写作 f(x)
- **严格凸**（首次 `logistic-regression/卡「Sigmoid 函数、逻辑回」`）：图像上任意两点的连线，除了两个端点都严格在图像上方；海森矩阵处处正定就严格凸，反过来不一定
- **导数**（首次 `logistic-regression/卡「例子：推导出简洁的交叉熵梯度」`）：f′(a) = lim_{h→0} [f(a + h) − f(a)]/h：曲线在 a 处切线的斜率，也是 a 处的瞬时变化率
- **整数**（首次 `logistic-regression/卡「例子：推导出简洁的交叉熵梯度」`）：没有小数部分的数：…、−2、−1、0、1、2、…
- **贝叶斯定理**（首次 `generative-classifiers/guess`）：已知结果反推原因的公式：P(H | E) = P(H)P(E | H) / P(E)，用新证据把先验概率更新为后验概率
- **协方差**（首次 `generative-classifiers/卡「LDA、QDA 与朴素贝叶斯」`）：衡量两个随机变量协同变化方向和程度的量 Cov(X, Y) = E[(X − μ_X)(Y − μ_Y)]
- **矩阵**（首次 `generative-classifiers/卡「LDA、QDA 与朴素贝叶斯」`）：排成 m 行 n 列的一张数表，叫 m×n 矩阵
- **相关系数**（首次 `trees-and-ensembles/rf-mtry-decorrelation`）：把协方差除以两个标准差之积得到的无量纲指标 ρ = Cov(X, Y) / (σ_X σ_Y)，取值落在 [−1, 1]
- **采样**（首次 `trees-and-ensembles/卡「梯度提升（Boosting）」`）：每隔一段固定的时间记一个数，把连续的信号变成数组；每秒记几个叫采样率
- **异常**（首次 `svm-and-margins/卡「最大间隔分类器、软间隔与支持」`）：运行到一半才发现的错误，如 ZeroDivisionError；可以用 try / except 接住
- **向量**（首次 `svm-and-margins/svm-support-vector-and-c`）：一列有顺序的数，如 (1, 2)；也可以画成从原点出发的箭头
- **依赖**（首次 `svm-and-margins/svm-support-vector-and-c`）：程序运行要用到的库；那些库自己用到的库是间接依赖，pip 会一起装上
- **多项式**（首次 `svm-and-margins/卡「核技巧非线性 SVM、多分类」`）：由 x 的乘方乘上常数再加起来的式子，如 3x³ − x + 7
- **长度**（首次 `svm-and-margins/卡「例子：计算二维最大间隔平面的」`）：向量 v 的长度 ‖v‖ = √(v·v)
- **维数**（首次 `kmeans-clustering/卡「例子：一维 6 点数据上的 」`）：空间的任何一组基里向量的个数
- **收敛**（首次 `kmeans-clustering/卡「例子：一维 6 点数据上的 」`）：数列或函数值和某个数 L 的距离能变得要多小有多小，并一直保持
- **迭代**（首次 `kmeans-clustering/kmeans-blobs-run`）：一遍遍重复同样的计算，每次都用上一次的结果，一步步逼近答案
- **切线**（首次 `hierarchical-and-practical/dendrogram-cut-height-num`）：割线的两点越靠越近时的极限位置；切线的斜率就是导数
- **内存**（首次 `pca-and-variance/guess`）：程序运行时存放数据的地方，电脑的“工作台”；NumPy 数组把数一个挨一个排在一整块内存里
- **投影**（首次 `pca-and-variance/guess`）：b 在一条直线或一个子空间里最接近它的点 p，误差 b − p 和那个子空间正交
- **正交**（首次 `pca-and-variance/卡「主成分分析（PCA）的双重等」`）：两个向量的点积为 0，在图上互相垂直
- **特征向量**（首次 `pca-and-variance/卡「主成分分析（PCA）的双重等」`）：经过 A 变换后方向不变（或正好反向）的非零向量 x：Ax = λx
- **正交补**（首次 `pca-and-variance/卡「主成分分析（PCA）的双重等」`）：和子空间 V 里每个向量都正交的所有向量组成的子空间 V⊥
- **张成**（首次 `pca-and-variance/卡「主成分分析（PCA）的双重等」`）：一组向量的所有线性组合正好是某个空间时，说它们张成这个空间
- **标准差**（首次 `pca-and-variance/pca-properties-choice`）：方差的算术平方根 σ = √Var(X)，与原随机变量保持相同的量纲单位
- **线性组合**（首次 `pcr-pls-highdim/卡「主成分回归（PCR）与偏最小」`）：把几个向量各乘一个数再加起来：cv + dw
- **线性无关**（首次 `pcr-pls-highdim/卡「高维困境（p 远大于 n）与」`）：只有全取 0 的组合才得到零向量：没有一个向量是其他向量的组合
- **数组**（首次 `pcr-pls-highdim/卡「例子：对照 p > n 时训」`）：一组类型相同的数，排成一行、一张表或更多维；NumPy 的核心
- **程序**（首次 `representation-and-autoencoders/guess`）：写给电脑的一串命令，电脑从上到下一行一行照做
- **互斥**（首次 `representation-and-autoencoders/卡「例子：为什么 10 个分布式」`）：两个事件不可能在同一次试验中同时发生，即交集为空集 A ∩ B = ∅
- **类型**（首次 `representation-and-autoencoders/卡「例子：为什么 10 个分布式」`）：值的种类（int、float、str、bool……），决定它能做哪些运算
- **缩进**（首次 `representation-and-autoencoders/卡「无监督自编码器与线性 PCA」`）：行首空出来的空格（通常 4 个）。Python 靠缩进判断哪几行属于 if、for 等
- **子空间**（首次 `representation-and-autoencoders/卡「无监督自编码器与线性 PCA」`）：向量空间里的一部分，对加法和数乘封闭，一定包含零向量
- **奇异值**（首次 `matrix-completion-embeddings/卡「缺失值、矩阵补全与硬迭代算法」`）：SVD 里 Σ 对角线上的数 σ₁ ≥ σ₂ ≥ … ≥ 0，是 AᵀA 特征值的平方根
- **奇异值分解**（首次 `matrix-completion-embeddings/matrix-completion-method`）：A = UΣVᵀ：任何矩阵都能写成 旋转 × 拉伸 × 旋转，简称 SVD
- **循环**（首次 `matrix-completion-embeddings/matrix-completion-method`）：把同一段代码重复执行，for 和 while 都是循环
- **二阶导数**（首次 `nonlinear-basis-splines/卡「多项式、阶梯函数、基函数与回」`）：导数的导数 f″ = (f′)′，也写作 d²y/dx²
- **绝对值**（首次 `feature-selection-regularization/卡「岭回归（L2 正则）与 La」`）：去掉负号后的数，|−3| = 3；|a − b| 是 a 和 b 在数轴上的距离
- **随机种子**（首次 `validation-and-learning-settings/guess`）：随机数生成器的起点；种子相同，得到的“随机数”就完全一样，结果可以重现
- **集合**（首次 `validation-and-learning-settings/bootstrap-prob-choice`）：花括号里只写值的一堆不重复、没有顺序的值，如 {1, 2, 3}；类型叫 set
- **局部极大值**（首次 `semi-supervised-learning/卡「为什么有效与模型假设翻车的风」`）：f(c) 不小于 c 附近所有点的函数值
- **视图**（首次 `semi-supervised-learning/卡「自训练（Self-Train」`）：数组的切片不复制数据，只是换一种方式看原来那块内存；改视图就是改原数组
- **主成分分析**（首次 `结业/b-pca-pve`）：把数据减去平均后做 SVD，第一个奇异向量是数据散得最开的方向，简称 PCA
- **单位向量**（首次 `结业/b-pca-pve`）：长度为 1 的向量；v/‖v‖ 是和 v 同方向的单位向量

### 3. 本包没有加粗讲解、也不在 terms 里的英文词（11 个，候选“没讲就用”）

RBF（`svm-and-margins/svm-support-vector-and-c`）、OLS（`pcr-pls-highdim/highdim-causal-warning`）、SVD（`matrix-completion-embeddings/卡「缺失值、矩阵补全与硬迭代算法」`）、Dense Embedding（`matrix-completion-embeddings/dense-embedding-vs-onehot`）、Feature Cross（`feature-engineering/feature-cross-purpose`）、ID（`feature-engineering/feature-cross-purpose`）、SSE（`feature-selection-regularization/卡「子集选择与调整后模型评价准则」`）、AIC（`feature-selection-regularization/卡「子集选择与调整后模型评价准则」`）、BIC（`feature-selection-regularization/卡「子集选择与调整后模型评价准则」`）、CT（`semi-supervised-learning/guess`）、EM（`semi-supervised-learning/卡「为什么有效与模型假设翻车的风」`）

### 4. 夸张词（58 处）

- 「飙」2 处：`statistical-learning-basics/guess`、`statistical-learning-basics/卡「例子：用训练和验证表现诊断过」`
- 「极其」9 处：`statistical-learning-basics/parametric-vs-interpretable`、`linear-regression-gd/knn-bias-variance`、`generative-classifiers/nb-highdim-advantage`、`trees-and-ensembles/bagging-vs-boosting`、`svm-and-margins/guess`、`representation-and-autoencoders/manifold-autoencoder-vs-pca` 等
- 「极度」7 处：`linear-regression-gd/knn-bias-variance`、`pca-and-variance/pca-properties-choice`、`matrix-completion-embeddings/matrix-completion-method`、`matrix-completion-embeddings/dense-embedding-vs-onehot`、`feature-engineering/guess`、`nonlinear-basis-splines/spline-vs-poly-vs-gam` 等
- 「天生」3 处：`generative-classifiers/lda-vs-qda-boundary`、`kmeans-clustering/kmeans-convergence-property`、`feature-engineering/guess`
- 「彻底」16 处：`trees-and-ensembles/卡「决策树分裂准则、不纯度与剪枝」`、`svm-and-margins/svm-hinge-vs-logistic`、`kmeans-clustering/卡「例子：一维 6 点数据上的 」`、`kmeans-clustering/卡「动手试试：观察三团点上的 k」`、`kmeans-clustering/kmeans-blobs-run`、`pcr-pls-highdim/卡「高维困境（p 远大于 n）与」` 等
- 「死死」2 处：`hierarchical-and-practical/guess`、`nonlinear-basis-splines/guess`
- 「绝对」13 处：`hierarchical-and-practical/卡「聚类实践的四条工程细节与陷阱」`、`hierarchical-and-practical/clustering-scaling-issue`、`pca-and-variance/pca-properties-choice`、`pcr-pls-highdim/highdim-causal-warning`、`matrix-completion-embeddings/matrix-completion-method`、`feature-engineering/feature-cross-purpose` 等
- 「轻松」1 处：`representation-and-autoencoders/guess`
- 「铁律」2 处：`feature-engineering/卡「数值特征工程的缩放、对数与分」`、`feature-selection-regularization/lasso-vs-ridge-scale`
- 「暴跌」2 处：`feature-engineering/leakage-prevention-choice`、`nonlinear-basis-splines/guess`
- 「竟然」1 处：`semi-supervised-learning/guess`

## A.2.3

### 1. 正确项是最长的选项：39/39（100%；结业挑战 5/5）

`perceptron-and-sigmoid-neuron/guess`、`perceptron-and-sigmoid-neuron/perceptron-vs-sigmoid-choice`、`perceptron-and-sigmoid-neuron/xor-by-nand-choice`、`mlp-architecture-and-digits/guess`、`mlp-architecture-and-digits/mlp-why-nonlinear-hidden`、`mlp-architecture-and-digits/deep-hierarchy-advantage`、`loss-sgd-and-minibatch/guess`、`loss-sgd-and-minibatch/softmax-output-property`、`loss-sgd-and-minibatch/minibatch-benefit-choice`、`optimizers-momentum-adam/guess`、`optimizers-momentum-adam/adam-bias-correction-choice`、`optimizers-momentum-adam/lr-symptoms-choice`、`optimizers-momentum-adam/adam-vs-sgd-advantage`、`initialization-hyperparams-vanishing/guess`、`initialization-hyperparams-vanishing/relu-vs-sigmoid-reasons`、`initialization-hyperparams-vanishing/he-vs-xavier-why-2`、`initialization-hyperparams-vanishing/hyperparam-search-practice`、`regularization-dropout-batchnorm/guess`、`regularization-dropout-batchnorm/weight-decay-update-calc`、`regularization-dropout-batchnorm/batchnorm-train-vs-eval`、`universal-approximation/guess`、`universal-approximation/universality-two-caveats`、`universal-approximation/relu-universality-note`、`universal-approximation/single-wide-overfit-risk`、`cnn-deep-representations/guess`、`cnn-deep-representations/cnn-weight-sharing-reason`、`cnn-deep-representations/cnn-feature-hierarchy`、`backprop-computation-graph/guess`、`backprop-computation-graph/cost-two-assumptions-choice`、`backprop-computation-graph/delta-definition-choice`、`backprop-four-equations/guess`、`backprop-speed-and-pytorch-loop/guess`、`backprop-speed-and-pytorch-loop/zero-grad-why-choice`、`backprop-speed-and-pytorch-loop/backprop-complexity-compare`、`结业/b-mlp-linear-vs-xor`、`结业/b-relu-he-init`、`结业/b-adam-vs-lr-diagnosis`、`结业/b-reg-techniques-compare`、`结业/b-pytorch-backprop-order`

### 2. 从前置技能继承的查词（49 个，逐个确认在这里意思对得上）

- **梯度下降**（首次 `perceptron-and-sigmoid-neuron/卡「感知机与 Sigmoid 神」`）：反复令 x ← x − η∇f(x)，沿负梯度一步步走向函数较小处的方法
- **函数**（首次 `perceptron-and-sigmoid-neuron/卡「感知机与 Sigmoid 神」`）：一条规则：每个输入恰好对应一个输出，写作 f(x)
- **参数**（首次 `perceptron-and-sigmoid-neuron/perceptron-vs-sigmoid-choice`）：刻画一族概率分布具体形状和位置的固定常数，如二项分布的 (n, p) 或指数分布的 λ
- **梯度**（首次 `perceptron-and-sigmoid-neuron/perceptron-vs-sigmoid-choice`）：偏导数构成的向量 ∇f = (f_x, f_y, …)，指向函数增加最快的方向，长度是最大变化率
- **不定**（首次 `perceptron-and-sigmoid-neuron/xor-by-nand-choice`）：有的方向 hᵀHh > 0、有的方向 < 0；对称矩阵不定等价于特征值有正有负
- **矩阵**（首次 `mlp-architecture-and-digits/卡「神经网络架构与隐藏层前向计算」`）：排成 m 行 n 列的一张数表，叫 m×n 矩阵
- **向量**（首次 `mlp-architecture-and-digits/卡「手写数字分类、简单实现与迈向」`）：一列有顺序的数，如 (1, 2)；也可以画成从原点出发的箭头
- **图像**（首次 `mlp-architecture-and-digits/卡「手写数字分类、简单实现与迈向」`）：所有点 (x, f(x)) 画在平面上连成的曲线
- **学习率**（首次 `mlp-architecture-and-digits/mlp-circle-sim`）：梯度下降每一步 x − η∇f 里的正数 η，决定一步迈多大
- **表示学习**（首次 `mlp-architecture-and-digits/deep-hierarchy-advantage`）：从原始观测数据中自动提取低维、紧凑且解耦的有效特征表示，使后续分类或预测更容易的方法
- **收敛**（首次 `loss-sgd-and-minibatch/guess`）：数列或函数值和某个数 L 的距离能变得要多小有多小，并一直保持
- **均方误差**（首次 `loss-sgd-and-minibatch/卡「神经网络里的交叉熵 vs 平」`）：各样本预测值与真实目标差值的平方平均值 MSE = (1/n) Σ (yᵢ − ŷᵢ)²
- **导数**（首次 `loss-sgd-and-minibatch/卡「神经网络里的交叉熵 vs 平」`）：f′(a) = lim_{h→0} [f(a + h) − f(a)]/h：曲线在 a 处切线的斜率，也是 a 处的瞬时变化率
- **交叉熵**（首次 `loss-sgd-and-minibatch/卡「神经网络里的交叉熵 vs 平」`）：用真实标签与预测概率对数的加权负值衡量分类预测误差的凸损失函数
- **训练集**（首次 `loss-sgd-and-minibatch/卡「小批量随机梯度下降（Mini」`）：专门拿来给模型反复拟合参数的那部分带标注数据
- **循环**（首次 `loss-sgd-and-minibatch/卡「小批量随机梯度下降（Mini」`）：把同一段代码重复执行，for 和 while 都是循环
- **互斥**（首次 `loss-sgd-and-minibatch/softmax-output-property`）：两个事件不可能在同一次试验中同时发生，即交集为空集 A ∩ B = ∅
- **单调**（首次 `optimizers-momentum-adam/卡「例子：手动推算一步动量更新与」`）：一直不减（单调递增）或一直不增（单调递减）
- **元素**（首次 `optimizers-momentum-adam/adam-vs-sgd-advantage`）：列表（或其他容器）里装的每一个值
- **正态分布**（首次 `initialization-hyperparams-vanishing/guess`）：钟形对称的连续分布 N(μ, σ²)，由均值 μ 决定中心位置、标准差 σ 决定胖瘦，可标准化为 N(0, 1)
- **赋值**（首次 `initialization-hyperparams-vanishing/guess`）：用 = 让左边的名字指向右边算出的值：先算右边，再贴名字
- **方差**（首次 `initialization-hyperparams-vanishing/guess`）：一组数离它们的平均值有多散：各数减平均值后平方、加起来，再除以（个数 − 1）
- **鞍点**（首次 `initialization-hyperparams-vanishing/卡「为什么放弃 Sigmoid 」`）：多元函数梯度为 0、却不是局部极值的点，如 x² − y² 的原点
- **标准差**（首次 `initialization-hyperparams-vanishing/卡「例子：用数值估算体验 Sig」`）：方差的算术平方根 σ = √Var(X)，与原随机变量保持相同的量纲单位
- **维数**（首次 `initialization-hyperparams-vanishing/卡「例子：用数值估算体验 Sig」`）：空间的任何一组基里向量的个数
- **期望**（首次 `initialization-hyperparams-vanishing/卡「例子：用数值估算体验 Sig」`）：以概率为权重的加权平均值，反映大量独立重复试验结果的长期中心位置，记作 E[X]
- **正则化**（首次 `initialization-hyperparams-vanishing/hyperparam-search-practice`）：在损失函数后面加上惩罚系数幅度的约束项，牺牲少量偏差以显著降低方差、缓解过拟合与共线性的方法
- **验证集**（首次 `regularization-dropout-batchnorm/guess`）：在训练阶段从可用数据中留出、专门用于挑选超参数与比较不同候选模型的独立子集
- **过拟合**（首次 `regularization-dropout-batchnorm/guess`）：模型容量过高，把训练集里的偶然噪声也背了下来，导致训练误差极低而新样本误差飙升的现象
- **损失函数**（首次 `regularization-dropout-batchnorm/卡「权重衰减（L2 正则）、早停」`）：用来量化单个或整批样本上“模型预测与真实答案相差有多远”的非负代价函数
- **依赖**（首次 `regularization-dropout-batchnorm/卡「暂退法（Dropout）、批」`）：程序运行要用到的库；那些库自己用到的库是间接依赖，pip 会一起装上
- **采样**（首次 `regularization-dropout-batchnorm/卡「暂退法（Dropout）、批」`）：每隔一段固定的时间记一个数，把连续的信号变成数组；每秒记几个叫采样率
- **调用**（首次 `regularization-dropout-batchnorm/batchnorm-train-vs-eval`）：写 函数名(值) 让函数用这些值执行一遍
- **有界**（首次 `universal-approximation/卡「万能近似定理的构造直觉与核心」`）：所有项（或函数值）都夹在两个固定的数之间
- **断言**（首次 `universal-approximation/卡「万能近似定理的构造直觉与核心」`）：assert 条件：条件为 True 什么都不发生，为 False 立刻报 AssertionError
- **长度**（首次 `cnn-deep-representations/max-pool-size-calc`）：向量 v 的长度 ‖v‖ = √(v·v)
- **特征工程**（首次 `cnn-deep-representations/cnn-feature-hierarchy`）：结合领域知识与数学变换，对原始数值、分类与缺失字段进行缩放、编码和组合以提升模型效果的过程
- **偏导数**（首次 `backprop-computation-graph/guess`）：固定其他变量、只让一个变量变时的导数，如 f_x = ∂f/∂x；算法是把其他变量当常数
- **链式法则**（首次 `backprop-computation-graph/guess`）：复合函数的导数：dy/dx = (dy/du)·(du/dx)，即 [f(g(x))]′ = f′(g(x))·g′(x)
- **点积**（首次 `backprop-computation-graph/卡「例子：体验简单计算图上的乘加」`）：两个向量对应位置相乘再相加：(1, 2)·(3, 4) = 3 + 8 = 11
- **下标**（首次 `backprop-computation-graph/hadamard-product-calc`）：写在字母右下角的小字，如 f_xy 里的 xy；偏导数的下标从左往右是求导的先后
- **表达式**（首次 `backprop-four-equations/four-equations-match`）：能算出一个结果的写法，如 3 * 4 + 1
- **转置**（首次 `backprop-four-equations/four-equations-match`）：把行变成列得到的矩阵 Aᵀ：Aᵀ 的 (i, j) 位置是 A 的 (j, i) 位置
- **微分**（首次 `backprop-speed-and-pytorch-loop/guess`）：dy = f′(x)dx：切线上的升高量，是函数增量 Δy 的线性主部
- **分支**（首次 `backprop-speed-and-pytorch-loop/卡「例子：Python 追踪单个」`）：if / elif / else 里的每一条路；一次只走其中一条
- **程序**（首次 `backprop-speed-and-pytorch-loop/autograd-trace-sim`）：写给电脑的一串命令，电脑从上到下一行一行照做
- **异常**（首次 `backprop-speed-and-pytorch-loop/zero-grad-why-choice`）：运行到一半才发现的错误，如 ZeroDivisionError；可以用 try / except 接住
- **发散**（首次 `结业/b-adam-vs-lr-diagnosis`）：数列不收敛：越来越大，或者来回跳、不靠近任何一个数
- **迭代**（首次 `结业/b-adam-vs-lr-diagnosis`）：一遍遍重复同样的计算，每次都用上一次的结果，一步步逼近答案

### 3. 本包没有加粗讲解、也不在 terms 里的英文词（14 个，候选“没讲就用”）

AND（`perceptron-and-sigmoid-neuron/卡「感知机与 Sigmoid 神」`）、NAND（`perceptron-and-sigmoid-neuron/perceptron-vs-sigmoid-choice`）、MNIST（`mlp-architecture-and-digits/卡「手写数字分类、简单实现与迈向」`）、GPU（`loss-sgd-and-minibatch/guess`）、MSE（`loss-sgd-and-minibatch/卡「例子：对比预测大错时均方误差」`）、SGD（`loss-sgd-and-minibatch/卡「小批量随机梯度下降（Mini」`）、GD（`loss-sgd-and-minibatch/minibatch-benefit-choice`）、Training Loss（`optimizers-momentum-adam/lr-symptoms-choice`）、Batch Size（`optimizers-momentum-adam/lr-symptoms-choice`）、RMSProp（`optimizers-momentum-adam/adam-vs-sgd-advantage`）、Batch Norm（`regularization-dropout-batchnorm/卡「暂退法（Dropout）、批」`）、Inverted Dropout（`regularization-dropout-batchnorm/卡「例子：对照训练与推理期的暂退」`）、Early Stopping（`regularization-dropout-batchnorm/four-reg-techniques-match`）、BN（`结业/b-pytorch-backprop-order`）

### 4. 夸张词（56 处）

- 「轻松」3 处：`perceptron-and-sigmoid-neuron/卡「感知机与 Sigmoid 神」`、`perceptron-and-sigmoid-neuron/xor-by-nand-choice`、`mlp-architecture-and-digits/mlp-circle-sim`
- 「极其」11 处：`mlp-architecture-and-digits/deep-hierarchy-advantage`、`loss-sgd-and-minibatch/卡「神经网络里的交叉熵 vs 平」`、`loss-sgd-and-minibatch/卡「例子：对比预测大错时均方误差」`、`optimizers-momentum-adam/guess`、`optimizers-momentum-adam/卡「例子：手动推算一步动量更新与」`、`initialization-hyperparams-vanishing/卡「为什么放弃 Sigmoid 」` 等
- 「红利」1 处：`loss-sgd-and-minibatch/guess`
- 「彻底」12 处：`loss-sgd-and-minibatch/guess`、`initialization-hyperparams-vanishing/relu-vs-sigmoid-reasons`、`regularization-dropout-batchnorm/guess`、`regularization-dropout-batchnorm/batchnorm-train-vs-eval`、`universal-approximation/卡「例子：用一对反号高斜率神经元」`、`backprop-computation-graph/hadamard-product-calc` 等
- 「死死」2 处：`loss-sgd-and-minibatch/卡「神经网络里的交叉熵 vs 平」`、`universal-approximation/single-wide-overfit-risk`
- 「吐出」2 处：`loss-sgd-and-minibatch/卡「例子：对比预测大错时均方误差」`、`regularization-dropout-batchnorm/batchnorm-train-vs-eval`
- 「足足」2 处：`loss-sgd-and-minibatch/卡「例子：对比预测大错时均方误差」`、`loss-sgd-and-minibatch/ce-vs-mse-ratio`
- 「狂」6 处：`loss-sgd-and-minibatch/卡「小批量随机梯度下降（Mini」`、`loss-sgd-and-minibatch/minibatch-benefit-choice`、`optimizers-momentum-adam/guess`、`optimizers-momentum-adam/adam-bias-correction-choice`、`optimizers-momentum-adam/lr-symptoms-choice`、`cnn-deep-representations/cnn-weight-sharing-reason`
- 「极度」1 处：`loss-sgd-and-minibatch/minibatch-benefit-choice`
- 「绝对」10 处：`optimizers-momentum-adam/adam-vs-sgd-advantage`、`initialization-hyperparams-vanishing/hyperparam-search-practice`、`universal-approximation/guess`、`universal-approximation/single-wide-overfit-risk`、`backprop-computation-graph/cost-two-assumptions-choice`、`backprop-speed-and-pytorch-loop/卡「例子：Python 追踪单个」` 等
- 「飙」2 处：`initialization-hyperparams-vanishing/卡「为什么放弃 Sigmoid 」`、`结业/b-adam-vs-lr-diagnosis`
- 「竟然」1 处：`cnn-deep-representations/guess`
- 「一毫秒」1 处：`backprop-speed-and-pytorch-loop/zero-grad-why-choice`
- 「毁掉」1 处：`backprop-speed-and-pytorch-loop/zero-grad-why-choice`
- 「当场」1 处：`结业/b-pytorch-backprop-order`

## A.4.1

### 1. 正确项是最长的选项：35/37（95%；结业挑战 5/5）

`ml-systems-and-versioning/guess`、`ml-systems-and-versioning/ml-system-glue-choice`、`ml-systems-and-versioning/versioning-why-choice`、`data-prep-and-exploration/guess`、`data-prep-and-exploration/eda-before-model`、`data-prep-and-exploration/leakage-time-or-target`、`data-prep-and-exploration/group-split-calc`、`data-prep-and-exploration/distributed-skew-reason`、`feature-store-and-skew/guess`、`feature-store-and-skew/skew-root-cause-choice`、`feature-store-and-skew/feature-store-dual-engines`、`feature-store-and-skew/fti-pipelines-choice`、`reproducible-code-and-quality/guess`、`reproducible-code-and-quality/cli-config-repro`、`reproducible-code-and-quality/ml-unit-test-overfit`、`reproducible-code-and-quality/precommit-gate-role`、`training-tracking-and-pipelines/guess`、`training-tracking-and-pipelines/experiment-tracking-role`、`training-tracking-and-pipelines/random-vs-grid-search`、`data-model-checks-and-cicd/guess`、`data-model-checks-and-cicd/cicd-vs-ml-diff-choice`、`data-model-checks-and-cicd/mft-vs-drift-why`、`serving-patterns-and-rollouts/guess`、`serving-patterns-and-rollouts/shadow-vs-canary-diff`、`serving-patterns-and-rollouts/canary-rollback-choice`、`fastapi-inference-service/guess`、`fastapi-inference-service/pydantic-422-why-choice`、`monitoring-drift-and-psi/guess`、`monitoring-drift-and-psi/delayed-feedback-choice`、`monitoring-drift-and-psi/data-vs-concept-drift-choice`、`结业/b-systems-skew`、`结业/b-version-registry`、`结业/b-serving-and-rollout`、`结业/b-drift-distinction`、`结业/b-fastapi-best-practice`

### 2. 从前置技能继承的查词（40 个，逐个确认在这里意思对得上）

- **采样**（首次 `ml-systems-and-versioning/卡「数据版本、模型元数据与模型注」`）：每隔一段固定的时间记一个数，把连续的信号变成数组；每秒记几个叫采样率
- **参数**（首次 `ml-systems-and-versioning/卡「数据版本、模型元数据与模型注」`）：刻画一族概率分布具体形状和位置的固定常数，如二项分布的 (n, p) 或指数分布的 λ
- **依赖**（首次 `ml-systems-and-versioning/卡「数据版本、模型元数据与模型注」`）：程序运行要用到的库；那些库自己用到的库是间接依赖，pip 会一起装上
- **锁文件**（首次 `ml-systems-and-versioning/卡「数据版本、模型元数据与模型注」`）：记下环境里每个库确切版本的文件（如 pip freeze 的输出、uv.lock），用来重现一模一样的环境
- **切片**（首次 `ml-systems-and-versioning/卡「数据版本、模型元数据与模型注」`）：用 [开始:结束] 取出一段，不包括结束那个下标，如 "Python"[0:2] 得 "Py"
- **训练集**（首次 `ml-systems-and-versioning/versioning-why-choice`）：专门拿来给模型反复拟合参数的那部分带标注数据
- **不可变**（首次 `ml-systems-and-versioning/versioning-why-choice`）：不能被原地改动的值，如整数、浮点数、字符串；“改”其实是算出一个新值
- **方差**（首次 `data-prep-and-exploration/卡「数据准备（切分与探索）及无泄」`）：一组数离它们的平均值有多散：各数减平均值后平方、加起来，再除以（个数 − 1）
- **测试集**（首次 `data-prep-and-exploration/卡「数据准备（切分与探索）及无泄」`）：直到所有调参和模型选择全部敲定之后才动用一次、专门用来汇报最终泛化误差的数据
- **内存**（首次 `data-prep-and-exploration/卡「分布式特征计算：从单机受限到」`）：程序运行时存放数据的地方，电脑的“工作台”；NumPy 数组把数一个挨一个排在一整块内存里
- **笔记本**（首次 `feature-store-and-skew/guess`）：Jupyter 笔记本：一格一格的代码，Shift + Enter 运行一格，输出显示在格子下面
- **函数**（首次 `feature-store-and-skew/guess`）：一条规则：每个输入恰好对应一个输出，写作 f(x)
- **报错**（首次 `feature-store-and-skew/guess`）：Python 遇到看不懂或做不到的写法时停下来，显示一段错误说明
- **事件**（首次 `feature-store-and-skew/卡「特征存储与离线/在线 FTI」`）：样本空间的子集，也就是你关心的一组基本结果；某次试验落在这个子集里就说事件发生
- **特征值**（首次 `feature-store-and-skew/卡「特征存储与离线/在线 FTI」`）：Ax = λx 里的数 λ，是特征向量被拉伸的倍数
- **模块**（首次 `feature-store-and-skew/fti-pipelines-choice`）：装着现成函数的 Python 文件，用 import 导入后使用，如 math
- **脚本**（首次 `feature-store-and-skew/fti-pipelines-choice`）：一个 .py 文件，里面是一串命令，每次运行都从头执行到尾
- **迭代**（首次 `feature-store-and-skew/fti-pipelines-choice`）：一遍遍重复同样的计算，每次都用上一次的结果，一步步逼近答案
- **变量**（首次 `reproducible-code-and-quality/guess`）：在算式或过程里可以取不同数值的符号量（如积分哑变量 t 或上限 x）
- **语法**（首次 `reproducible-code-and-quality/卡「模块化脚本、命令行入参与文档」`）：代码的书写规矩，如 if 后面要有冒号、括号要配对
- **命令行参数**（首次 `reproducible-code-and-quality/cli-config-repro`）：运行程序时写在程序名后面的词；Python 用 sys.argv 拿到，都是字符串
- **梯度**（首次 `reproducible-code-and-quality/卡「ML 代码不像普通软件：专测」`）：偏导数构成的向量 ∇f = (f_x, f_y, …)，指向函数增加最快的方向，长度是最大变化率
- **异常**（首次 `reproducible-code-and-quality/卡「ML 代码不像普通软件：专测」`）：运行到一半才发现的错误，如 ZeroDivisionError；可以用 try / except 接住
- **断言**（首次 `reproducible-code-and-quality/卡「ML 代码不像普通软件：专测」`）：assert 条件：条件为 True 什么都不发生，为 False 立刻报 AssertionError
- **矩阵**（首次 `reproducible-code-and-quality/卡「ML 代码不像普通软件：专测」`）：排成 m 行 n 列的一张数表，叫 m×n 矩阵
- **循环**（首次 `reproducible-code-and-quality/卡「例子：抓出默默不崩溃却学不出」`）：把同一段代码重复执行，for 和 while 都是循环
- **交叉熵**（首次 `reproducible-code-and-quality/卡「例子：抓出默默不崩溃却学不出」`）：用真实标签与预测概率对数的加权负值衡量分类预测误差的凸损失函数
- **学习率**（首次 `reproducible-code-and-quality/ml-unit-test-overfit`）：梯度下降每一步 x − η∇f 里的正数 η，决定一步迈多大
- **向量**（首次 `reproducible-code-and-quality/ml-step-assertion-calc`）：一列有顺序的数，如 (1, 2)；也可以画成从原点出发的箭头
- **互斥**（首次 `reproducible-code-and-quality/ml-step-assertion-calc`）：两个事件不可能在同一次试验中同时发生，即交集为空集 A ∩ B = ∅
- **元素**（首次 `reproducible-code-and-quality/ml-step-assertion-calc`）：列表（或其他容器）里装的每一个值
- **验证集**（首次 `training-tracking-and-pipelines/guess`）：在训练阶段从可用数据中留出、专门用于挑选超参数与比较不同候选模型的独立子集
- **交叉验证**（首次 `training-tracking-and-pipelines/卡「实验追踪与超参数搜索的规范闭」`）：把训练数据分成多折轮流做训练与验证、汇总平均验证误差以更稳健地选模型与调超参数的方法
- **类型**（首次 `data-model-checks-and-cicd/卡「数据验证门禁与三类模型行为测」`）：值的种类（int、float、str、bool……），决定它能做哪些运算
- **单调**（首次 `data-model-checks-and-cicd/卡「数据验证门禁与三类模型行为测」`）：一直不减（单调递增）或一直不增（单调递减）
- **过拟合**（首次 `data-model-checks-and-cicd/卡「例子：抓出“升高信用收入后通」`）：模型容量过高，把训练集里的偶然噪声也背了下来，导致训练误差极低而新样本误差飙升的现象
- **进程**（首次 `serving-patterns-and-rollouts/batch-vs-qps-throughput`）：一个正在运行的程序，有操作系统分给它的一份内存；从 Python 启动的别的程序是子进程
- **正交**（首次 `serving-patterns-and-rollouts/shadow-vs-canary-diff`）：两个向量的点积为 0，在图上互相垂直
- **调用**（首次 `fastapi-inference-service/guess`）：写 函数名(值) 让函数用这些值执行一遍
- **期望**（首次 `结业/b-psi-calc-boss`）：以概率为权重的加权平均值，反映大量独立重复试验结果的长期中心位置，记作 E[X]

### 3. 本包没有加粗讲解、也不在 terms 里的英文词（26 个，候选“没讲就用”）

MLOps（`ml-systems-and-versioning/guess`）、ML（`ml-systems-and-versioning/卡「从产品需求立项到完整 ML 」`）、AUC（`ml-systems-and-versioning/卡「从产品需求立项到完整 ML 」`）、GB（`ml-systems-and-versioning/versioning-why-choice`）、EDA（`data-prep-and-exploration/eda-before-model`）、Group Split（`data-prep-and-exploration/group-split-calc`）、ID（`data-prep-and-exploration/group-split-calc`）、OOM（`data-prep-and-exploration/distributed-skew-reason`）、SQL（`feature-store-and-skew/guess`）、OK（`feature-store-and-skew/guess`）、FTI（`feature-store-and-skew/卡「特征存储与离线/在线 FTI」`）、Time Join（`feature-store-and-skew/卡「例子：抓出历史训练拼接时没对」`）、AI（`feature-store-and-skew/fti-pipelines-choice`）、Jupyter Notebook（`reproducible-code-and-quality/guess`）、CLI（`reproducible-code-and-quality/卡「模块化脚本、命令行入参与文档」`）、YAML（`reproducible-code-and-quality/cli-config-repro`）、DAG（`training-tracking-and-pipelines/guess`）、PR（`training-tracking-and-pipelines/卡「切片评估、概率校准与持续训练」`）、VIP（`training-tracking-and-pipelines/卡「例子：对照“总体 94% 却」`）、QPS（`serving-patterns-and-rollouts/batch-vs-qps-throughput`）、CPU（`serving-patterns-and-rollouts/shadow-vs-canary-diff`）、Python Web（`fastapi-inference-service/guess`）、MB（`fastapi-inference-service/guess`）、JSON（`fastapi-inference-service/卡「最小 FastAPI + P」`）、AB（`fastapi-inference-service/return-model-version-choice`）、Concept Drift（`monitoring-drift-and-psi/data-vs-concept-drift-choice`）

### 4. 夸张词（59 处）

- 「彻底」14 处：`ml-systems-and-versioning/guess`、`ml-systems-and-versioning/versioning-why-choice`、`data-prep-and-exploration/eda-before-model`、`data-prep-and-exploration/group-split-calc`、`data-prep-and-exploration/distributed-skew-reason`、`feature-store-and-skew/skew-root-cause-choice` 等
- 「飙」3 处：`ml-systems-and-versioning/卡「例子：一次完整的线上故障追溯」`、`data-prep-and-exploration/group-split-calc`、`serving-patterns-and-rollouts/canary-rollback-choice`
- 「极其」6 处：`ml-systems-and-versioning/ml-system-glue-choice`、`reproducible-code-and-quality/guess`、`reproducible-code-and-quality/cli-config-repro`、`training-tracking-and-pipelines/random-vs-grid-search`、`data-model-checks-and-cicd/behavioral-tests-match`
- 「暴跌」3 处：`data-prep-and-exploration/guess`、`training-tracking-and-pipelines/卡「例子：对照“总体 94% 却」`、`fastapi-inference-service/guess`
- 「绝对」8 处：`data-prep-and-exploration/卡「例子：抓出隐藏的“未来泄漏列」`、`data-prep-and-exploration/group-split-calc`、`feature-store-and-skew/guess`、`reproducible-code-and-quality/precommit-gate-role`、`training-tracking-and-pipelines/guess`、`serving-patterns-and-rollouts/shadow-vs-canary-diff` 等
- 「赫然」1 处：`data-prep-and-exploration/卡「例子：抓出隐藏的“未来泄漏列」`
- 「吐出」1 处：`data-prep-and-exploration/卡「例子：抓出隐藏的“未来泄漏列」`
- 「狂」1 处：`data-prep-and-exploration/卡「例子：抓出隐藏的“未来泄漏列」`
- 「轻松」3 处：`data-prep-and-exploration/卡「例子：抓出隐藏的“未来泄漏列」`、`data-prep-and-exploration/distributed-skew-reason`、`feature-store-and-skew/卡「例子：抓出历史训练拼接时没对」`
- 「当场」1 处：`data-prep-and-exploration/卡「例子：抓出隐藏的“未来泄漏列」`
- 「罪魁祸首」2 处：`data-prep-and-exploration/卡「例子：抓出隐藏的“未来泄漏列」`、`结业/b-systems-skew`
- 「毁掉」1 处：`data-prep-and-exploration/卡「例子：抓出隐藏的“未来泄漏列」`
- 「一毫秒」5 处：`data-prep-and-exploration/卡「例子：抓出隐藏的“未来泄漏列」`、`data-prep-and-exploration/leakage-time-or-target`、`feature-store-and-skew/卡「例子：抓出历史训练拼接时没对」`、`reproducible-code-and-quality/precommit-gate-role`、`serving-patterns-and-rollouts/卡「例子：用延迟要求与风险属性敲」`
- 「铁律」1 处：`data-prep-and-exploration/leakage-time-or-target`
- 「真真实实」1 处：`data-prep-and-exploration/leakage-time-or-target`
- 「天生」1 处：`data-prep-and-exploration/distributed-skew-reason`
- 「极度」3 处：`data-prep-and-exploration/distributed-skew-reason`、`data-model-checks-and-cicd/guess`、`data-model-checks-and-cicd/cicd-vs-ml-diff-choice`
- 「死死」1 处：`feature-store-and-skew/fti-pipelines-choice`
- 「竟然」1 处：`data-model-checks-and-cicd/guess`
- 「神奇」1 处：`fastapi-inference-service/guess`
- 「足足」1 处：`fastapi-inference-service/startup-load-latency-calc`
