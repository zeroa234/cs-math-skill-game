# M.1.2 一元微分学：覆盖表

规则见 `docs/content-authoring.md` 的“知识覆盖面标准”。依据：skill-tree 大纲 `../cs-math-skill-tree/data/outlines/M.1.2.json`：MIT OCW 18.01SC Single Variable Calculus（Fall 2010）的 25 个 Session（Unit 1 Part A、B，Unit 2 Part A、C，Unit 5 Part B）。“节”是技能内部编号，“原文”是 18.01SC 的 Session 标题。技能的章另列了 OpenStax《Calculus Volume 1》第 3 章、4.2、4.4 节和《Volume 2》6.3 节，例题有一部分取自那里。

必须前置是极限与连续 M.1.1：极限、左右极限、连续、无穷小的阶（$o(\cdot)$ 记号）、$\frac{\sin x}{x} \to 1$、最值定理和临界点都在那里讲过，这里直接用。

`node scripts/check-coverage.mjs M.1.2` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Session 1 Introduction to Derivatives | `secant-tangent` |
| 1.2 | Session 2 Examples of Derivatives | `derivative-function`, `differentiable` |
| 1.3 | Session 3 Derivative as Rate of Change | `rate-of-change` |
| 1.4 | Session 6 Calculating Derivatives | `sum-rule` |
| 1.5 | Session 7 Derivatives of Sine and Cosine | `sin-cos` |
| 1.6 | Session 9 Product Rule | `product-rule` |
| 1.7 | Session 10 Quotient Rule | `quotient-rule` |
| 1.8 | Session 11 Chain Rule | `chain-rule` |
| 1.9 | Session 12 Higher Derivatives | `higher-derivatives` |
| 2.1 | Session 13 Implicit Differentiation | `implicit` |
| 2.2 | Session 14 Examples of Implicit Differentiation | `implicit-practice` |
| 2.3 | Session 15 Implicit Differentiation and Inverse Functions | `inverse-functions`, `inverse-trig` |
| 2.4 | Session 17 The Exponential Function, its Derivative, and its Inverse | `exp-log` |
| 2.5 | Session 18 Derivatives of other Exponential Functions | `log-diff` |
| 3.1 | Session 23 Linear Approximation | `linear-approx` |
| 3.2 | Session 24 Examples of Linear Approximation | `approx-uses` |
| 3.3 | Session 25 Introduction to Quadratic Approximation | `quadratic-approx` |
| 3.4 | Session 26 Using Quadratic Approximations | `quadratic-approx`, `taylor-poly` |
| 4.1 | Session 34 Introduction to the Mean Value Theorem | `mvt`, `mvt-consequences` |
| 4.2 | Session 35 Using the Mean Value Theorem | `mvt-consequences` |
| 4.3 | Session 36 Differentials | `differentials` |
| 5.1 | Session 97 Power Series | `power-series` |
| 5.2 | Session 98 Taylor's Series | `taylor-poly`, `remainder`, `taylor-series` |
| 5.3 | Session 99 Taylor's Series, Continued | `taylor-series` |
| 5.4 | Session 100 Operations on Power Series | `series-ops` |

另有几课不对应单独的一节：

- `fermat-rolle`（费马定理、用导数找临界点、罗尔定理）：OpenStax 4.4 先讲罗尔定理再推中值定理，18.01SC 的 Session 34 直接证中值定理，没有单独讲罗尔。M.1.1 的 `extreme-value` 把“用导数找临界点”留给了这一站。
- `monotone-extrema`（单调区间、一阶导数判别法、二阶导数判别法）：18.01SC 的函数作图（Session 27、28）大纲没收，但原技能树的综合练习 (2) 要求单调区间和极值，技能简介也写了“用导数判断单调性与极值”。判别法的说法按 OpenStax《Calculus Volume 1》4.5 节。二阶导数判别法是后继 M.1.4.1（Hessian 判别极值）的一元版本。
- `lhopital`（柯西中值定理、洛必达法则）和 `taylor-limits`（佩亚诺余项、用泰勒展开求极限）：技能第 4 章的说明写明于品《数学分析》§16 讲“Taylor 展开（含 L'Hôpital 与局部近似）”，18.01SC 的这几个 Session 没讲。柯西中值定理按于品命题 15.5，洛必达法则的条件按于品命题 16.1（明确要求 $g'(x) \ne 0$；OpenStax 4.8 的定理框没写这一条），误用的反例取自 OpenStax 4.8 例 4.40 和于品 §16 的例子，$0 \cdot \infty$ 型和乘方型的处理按 OpenStax 4.8。佩亚诺余项的条件按于品定理 16.6。于品 §15–16 没有“用泰勒展开求极限”的例题，`taylor-limits` 的例题是自写的，数值由 sympy 核对。

教到什么深度（入门层）：
- 导数从割线讲起，用定义算 $x^2$、$\frac1x$、$x^n$（$n = 2, 3$ 展开，一般的 $n$ 说明展开式的前两项），求导法则讲用法和证明的思路（乘积法则写出插项的一步，商法则由乘积法则和链式法则推出）。
- 链式法则用中间变量 $\frac{dy}{dt} = \frac{dy}{dx}\cdot\frac{dx}{dt}$ 讲，不讲严格证明（18.01SC 也只给差商相乘再取极限的直观推导）。
- 指数函数按 18.01SC 的讲法：$a^x$ 的导数是 $M(a)\,a^x$，$e$ 是让 $M(e) = 1$ 的底；$e = \lim (1 + \frac1n)^n$ 在 Session 19，大纲没收，这里只提一句，用 `taylor-series` 里的 $e = \sum \frac{1}{n!}$ 算 $e$。
- 中值定理讲内容、几何意义、两个条件为什么不能少，证明用“把割线平移到相切”的图（18.01SC 的讲法）和由罗尔定理构造辅助函数（OpenStax 的讲法）。
- 泰勒公式讲多项式系数 $a_n = \frac{f^{(n)}(0)}{n!}$ 怎么来、拉格朗日余项的用法（18.01SC 和 OpenStax 都不证明）、佩亚诺余项和局部近似。
- 幂级数讲几何级数、收敛半径的意思、用比值求三个简单级数的半径；收敛判别法的理论、端点、一致收敛属于无穷级数 M.1.5。
- 幂级数的运算讲加、乘 $x$、代换、逐项求导，以及“找一个导数等于已知级数的级数”（得到 $\ln(1+x)$ 和 $\arctan x$ 的级数）。18.01SC 写成逐项积分 $\int$ 和误差函数 erf，积分记号属于一元积分学 M.1.3，这里不用。

## 和原文的核对

写课前，pi 子代理逐条读了 18.01SC 的 25 个 Session（页面概要、讲课逐字稿、例题和习题课的解答，笔记 `temp/research/M.1.2-mit1801-notes.md`，不入库），课里的定义、结论和例题按这份笔记写。写课时（2026-11-04）pi 又读了 OpenStax《Calculus Volume 1》4.5、4.8 节和于品《数学分析》§15、§16 的全文（笔记 `temp/research/M.1.2-extra-notes.md`，不入库），用于 `monotone-extrema`、`lhopital`、`taylor-limits` 和余项的条件。

和原文说法不同、或原文有误的地方：
- 18.01SC 的讲稿把 $f'$ 叫“Newton's notation”，撇号记法一般认为出自拉格朗日，课里只写“f 撇”，不署名。
- pi 读到的 18.01SC 例题 ex23 文本里，$\sin 0.1$ 的真值是 .099883341…，和正确值 0.0998334… 不符（可能是原文笔误，也可能是 PDF 转文字出的错）；课里没有用这个数。
- 链式法则只给 $\frac{\Delta y}{\Delta x} = \frac{\Delta y}{\Delta u}\cdot\frac{\Delta u}{\Delta x}$ 的直观推导（18.01SC 也是这样），课里注明 $\Delta u = 0$ 时严格证明要另外处理；商法则由乘积法则推出时注明先承认 $u/v$ 可导。

每个数值由 `tests/content/M.1.2.verify.py` 核对：导数、极限和级数用 sympy 算，近似值、误差和误差上界用浮点数重算，交互题（割线、泰勒）在给出的解答处重算是否达标；124 道数字题的答案逐题从课包里读出来，和独立算出的值比较。写完第一次运行时它查出一处错：`approx-uses` 里 $y + y^3 = 2.2$ 的真实解写成了 1.0466，实际是 1.0482，已改。

## CS2023（`data/curation/scope.json`）

| 知识点 | CS2023 主题（scope.json 匹配原文） | 课 |
|---|---|---|
| 导数 | MSF-Calculus，KA Core：Single-variable derivatives | `secant-tangent` 到 `log-diff` 共 16 课 |
| 微分 | MSF-Calculus，KA Core：computation rules (chain rule etc.) | `sum-rule`, `product-rule`, `quotient-rule`, `chain-rule`, `differentials` |
| 泰勒公式与局部近似 | MSF-Calculus，KA Core：Taylor series | `quadratic-approx`, `taylor-poly`, `remainder`, `taylor-limits`, `power-series`, `taylor-series`, `series-ops` |

## 原技能树的综合练习

| 小题 | 课 |
|---|---|
| (1a) $y = x^3 e^{2x}$ | `exp-log`（乘积法则加链式法则的分步例题） |
| (1b) $y = \ln(1 + x^2)$ | `exp-log`（$(\ln u)' = \frac{u'}{u}$） |
| (1c) $y = \sin(x^2)$ | `chain-rule`（分步例题） |
| (2) $x^3 - 3x$ 的单调区间和极值 | `monotone-extrema`（分步例题就是这一题） |
| (3) $x^2$ 在 $[1, 3]$ 上的中值定理，求 $\xi$ | `mvt`（练习题） |
| (4) $e^x$ 的 3 阶泰勒多项式估算 $e^{0.1}$，拉格朗日余项给误差上界 | `remainder`（分步例题就是这一题） |

## 后继技能要用的

必须后继是一元积分学 M.1.3、多元微分学 M.1.4.1、无穷级数 M.1.5（都还没有内容包），按它们的综合练习核对：

- M.1.3 的 $\int x e^x dx$（分部积分）要乘积法则（`product-rule`），$\int \frac{2x}{1+x^2}dx$（换元）要链式法则和 $(\ln u)' = \frac{u'}{u}$（`chain-rule`、`exp-log`），$F(x) = \int_0^{x^2} e^{-t^2}dt$ 求导要链式法则；微积分基本定理的证明要中值定理和“导数为 0 就是常数”（`mvt`、`mvt-consequences`）。
- M.1.4.1 的偏导数沿用一元的全部求导法则；全微分和线性近似的一元版本在 `differentials`、`linear-approx`；隐函数求导在 `implicit`；Hessian 判别极值的一元版本是二阶导数判别法（`monotone-extrema`）。
- M.1.5 从 $\frac{1}{1+x}$ 的级数逐项积分得到 $\ln(1 + x)$ 的级数并估算 $\ln 1.1$：`power-series` 讲几何级数和收敛半径，`series-ops` 讲由已知级数得到 $\ln(1 + x)$ 的级数，并用前 3 项算 $\ln 1.1$。
