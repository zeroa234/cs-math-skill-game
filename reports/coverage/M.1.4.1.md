# M.1.4.1 多元微分学：覆盖表

**状态（2026-11-19）：已写完（v2 重写，按零基础与知识覆盖面标准）。** 依据 `../cs-math-skill-tree/output/outlines.json` 的 M.1.4.1 大纲（OpenStax《Calculus Volume 3》4.3–4.8、5.7；于品《数学分析》第 30、31、33、34 讲；Deisenroth 等《Mathematics for Machine Learning》5.7、5.8；Boyd & Vandenberghe《Convex Optimization》3.1、9.1、9.5）。定义和定理的前提条件对照原文核对过，笔记在 `temp/m141-research/`（openstax.md、theory.md，pi 子代理抓取整理，主代理逐条用于核对）。数值核对：`tests/content/M.1.4.1.verify.py`（SymPy 1.14，357 条，104 道数字题逐一和包里的答案比对）。

游戏的章序是自动生成的（`reports/chapter-order.md`，依据 original）：方向导数排在梯度之前，隐函数与反函数定理排在链式法则之前。为此方向导数公式和隐函数求导公式都从全微分推出（不借用链式法则），反函数定理用全微分线性化成二元一次方程组来讲，雅可比矩阵的名字留到第 6 章。

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | 4.3 Derivatives of a Function of Two Variables | `two-var-functions`、`partial-rules` |
| 1.2 | 4.3 Functions of More Than Two Variables | `partial-rules` |
| 1.3 | 4.3 Higher-Order Partial Derivatives | `mixed-partials`、`hessian` |
| 1.4 | 4.3 Equality of Mixed Partial Derivatives (Clairaut's Theorem) | `mixed-partials` |
| 1.5 | 4.3 Partial Differential Equations | `pde-check` |
| 2.1 | 4.4 Tangent Planes | `tangent-plane` |
| 2.2 | 4.4 Linear Approximations | `linear-approx` |
| 2.3 | 4.4 Differentiability | `differentiability` |
| 2.4 | 4.4 Differentials | `total-differential` |
| 2.5 | 4.4 Differentiability of a Function of Three Variables | `differentiability`、`total-differential` |
| 3.1 | 4.5 Chain Rules for One or Two Independent Variables | `chain-one`、`chain-two` |
| 3.2 | 4.5 The Generalized Chain Rule | `chain-two`、`chain-matrix` |
| 3.3 | 4.5 Implicit Differentiation | `implicit-diff` |
| 4.1 | 4.6 Directional Derivatives | `directional` |
| 4.2 | 4.6 Gradient | `gradient` |
| 4.3 | 4.6 Gradients and Level Curves | `gradient-level` |
| 4.4 | 4.6 Three-Dimensional Gradients and Directional Derivatives | `directional-3d`、`gradient`、`gradient-level` |
| 5 | 于品 第 33 讲 反函数定理 | `inverse-theorem` |
| 6 | 于品 第 34 讲 隐函数定理 | `implicit-theorem` |
| 7.1 | 5.7 Planar Transformations | `planar-transform` |
| 7.2 | 5.7 讲到面积放大倍数（雅可比行列式的绝对值）和 dA 要乘上这个倍数的原因acobians | `jacobian-det` |
| 7.3 | 5.7 Change of Variables for Double Integrals | 不教：二重积分属于 M.1.4.4 多元积分与向量分析（本技能不讲重积分）；`jacobian-det` 讲到面积放大倍数（雅可比行列式的绝对值）和积分换元时 dA 要乘上这个倍数的原因，积分本身留给 M.1.4.4 |
| 7.4 | 5.7 Change of Variables for Triple Integrals | 不教：三重积分属于 M.1.4.4；`jacobian-det` 给出柱坐标 r、球坐标 ρ² sin φ 的雅可比行列式（体积放大倍数） |
| 8 | 于品 第 30 讲 高维函数的微分 | `differential-linear-map` |
| 9 | 于品 第 31 讲 映射的微分 | `vector-maps`、`chain-matrix` |
| 10.1 | 4.7 Critical Points | `critical-points` |
| 10.2 | 4.7 Second Derivative Test | `critical-points` |
| 10.3 | 4.7 Absolute Maxima and Minima | `absolute-extrema` |
| 11 | 4.8 Lagrange Multipliers | `lagrange` |
| 12 | MML 5.7 Higher-Order Derivatives（海森矩阵） | `hessian` |
| 13 | MML 5.8 Linearization and Multivariate Taylor Series | `taylor-2d` |
| 14 | Boyd 3.1 二阶条件 | `hessian-definite` |
| 15 | Boyd 9.1 Unconstrained minimization problems | `newton` |
| 16 | Boyd 9.5 Newton's method | `newton` |

## 写法上的取舍（对照原文）

- 混合偏导数：OpenStax 用 $\partial^2 f/\partial x\partial y = f_{yx}$，同济等中文教材的分式写法顺序相反。课里只用下标写法（$f_{xy}$ 先 x 后 y），并说明分式写法各书约定不同（`mixed-partials`）。
- Clairaut 定理按 OpenStax 定理 4.5 的条件（包含该点的开圆盘上 $f_{xy}$、$f_{yx}$ 连续）；不连续时的反例 $xy(x^2-y^2)/(x^2+y^2)$ 由 verify.py 从定义算出 $f_{xy}(0,0) = -1$、$f_{yx}(0,0) = 1$。
- 可微的定义用 OpenStax 式 4.26（误差除以距离趋于 0）；“偏导数存在但不可微”用 OpenStax 本节的 $xy/\sqrt{x^2+y^2}$（原点连续、不可微）；定理 4.7 的条件按原文写成“f、f_x、f_y 在附近存在且 f_x、f_y 在该点连续”。
- 临界点按 OpenStax 定义包含偏导数不存在的点；二阶导数判别法的条件（一、二阶偏导数在附近连续）照原文。
- 拉格朗日乘数法的条件（连续偏导数、∇g ≠ 0）照 OpenStax 定理 4.20，并单列一题说明为什么要另查 ∇g = 0 的点。
- 隐函数定理、反函数定理按于品第 33、34 讲（C¹、相应的偏导数矩阵可逆，结论是局部的，反变换的导数是逆矩阵），只讲二元和“三个变量两个方程”的情形，证明不讲（超出入门层）。
- 凸函数的二阶条件按 Boyd 3.1.4（凸开定义域上：凸 ⇔ 海森矩阵处处半正定；处处正定 ⇒ 严格凸，反之不成立，例 $x^4$）。牛顿法按 Boyd 9.5（牛顿步是二阶模型的最小点，二次函数一步到位，牛顿减量 λ²/2 估计剩余下降量，配合回溯步长）；“海森矩阵不定时牛顿步会被吸到鞍点”用 $x^2 - y^2$ 的计算说明，不是 Boyd 原文的陈述。
- 2×2 对称矩阵的正定判别（左上角 > 0 且行列式 > 0）只讲 2×2；n×n 的顺序主子式判别只提一句不展开。

## 核心主题（C2）

`../cs-math-skill-tree/data/curation/scope.json` 给 M.1.4.1 匹配的 CS2023 主题（都在 MSF-Calculus，KA Core）：

| 知识点 | CS2023 原文 | 课 |
|---|---|---|
| 偏导数 | Multivariate calculus: partial derivatives | `two-var-functions`、`partial-rules`、`mixed-partials` |
| 标量场梯度 | partial derivatives, gradient | `gradient`、`gradient-level` |
| 向量映射导数（雅可比矩阵） | vector valued functions | `vector-maps` |
| 链式法则与坐标变换 | gradient, chain-rule | `chain-one`、`chain-two`、`chain-matrix` |
| 二阶近似与极值判别 | global vs local minima | `critical-points`、`absolute-extrema`、`hessian-definite`（凸函数的局部最小就是全局最小） |

另有元主题“连接二阶优化”：`newton`。

## 学习资源的章节（C3）

按 `node scripts/skill-brief.mjs M.1.4.1` 列出的各章资源核对。于品讲义按 `temp/m141-research/theory.md` 的原文笔记核对；台大和 MIT 的录像只按章节标题和 OCW 的单元目录核对，没有逐讲看录像。

- 台大朱桦《微积分》第 11–13 章：偏导数、全微分、方向导数、隐函数求导、偏导数的应用（极值），都在第 1–5、9 章里。第 11 章向量值函数的曲线部分（切向量、弧长）不属于这个技能的大纲，不收。
- 于品第 45–46 讲（换元积分）在 skill-brief 里挂在“链式法则与坐标变换”下，按大纲 7.3、7.4 的处理，积分部分留给 M.1.4.4，本包只讲雅可比行列式。
- 于品第 30、31、33、34、37 讲：微分是线性映射、映射的微分和链式法则、反函数定理、隐函数定理、Hesse 矩阵与极值，分别在 `differential-linear-map`、`vector-maps`、`chain-matrix`、`inverse-theorem`、`implicit-theorem`、`hessian`、`critical-points`。子流形的判定（第 34 讲后半）属于微分几何（M.4.2），不收。
- MIT 18.02SC Unit 2：Part A（偏导数、切平面近似、极值）、Part B（链式法则、梯度、方向导数）、Part C（拉格朗日乘数、约束微分）都覆盖；Part C 的“非独立变量的偏导数”记号 $(\partial w/\partial x)_y$ 没有单列，相应的计算用 `implicit-diff` 的三元隐函数公式完成。
- Lebl §8.3、§8.5、§8.6：导数是线性映射、反函数和隐函数定理、高阶导数，同上。

## 综合练习（C4）

| 小题 | 内容 | 课 |
|---|---|---|
| (1) | $f = x^2y + e^{xy}$ 的 $f_x$、$f_y$、$f_{xy}$ | `mixed-partials`（例题就是这个函数）、`partial-rules` |
| (2) | 全微分近似 $1.02^2 + 1.97^2$ | `linear-approx`（例题原题）、`total-differential` |
| (3) | $\nabla f(1, 2, 1)$、最速方向、最大变化率 $\sqrt{56}$ | `gradient-level`（`steepest-rate` 原题） |
| (4) | 球面隐函数 $\partial z/\partial x$、$\partial z/\partial y$ | `implicit-diff`（卡片原例） |
| (5) | 矩阵形式链式法则 $D(h \circ g) = Dh \cdot Dg$ 并代入验证 | `chain-matrix`（例题原题） |
| (6) | $x^3 - 3x + y^2 - 2y$ 的临界点 | `critical-points`（`crit-find`） |
| (7) | 海森矩阵判别，求函数值 | `hessian`、`critical-points`（`crit-classify`、`crit-minval`） |

用课里教过的方法逐题做过一遍，答案和原技能树给的参考答案一致（数值都在 verify.py 里）。

## 后继技能（C5）

必须后继里已有或将有内容包的：A.2.1（监督/无监督学习）、A.2.3（深度学习）。它们要用的：梯度和负梯度方向（`gradient-level`）、梯度下降和学习率（`differential-linear-map`，带 2D 演示和操作题）、向量映射的雅可比矩阵和链式法则的矩阵形式（`vector-maps`、`chain-matrix`，最后一张卡讲反向传播就是一串雅可比矩阵从左往右乘）、海森矩阵和凸性（`hessian-definite`）、二阶近似和牛顿法（`taylor-2d`、`newton`）。M.7.2 凸优化、M.7.3 非凸优化、M.8.5 自动微分还没有内容包；它们的大纲要用的海森矩阵正定性、鞍点、牛顿步、链式法则的矩阵形式都已在本包讲到。积分换元（M.1.4.4）要的雅可比行列式和“面积放大倍数”在 `jacobian-det`。
