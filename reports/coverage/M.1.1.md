# M.1.1 极限与连续：覆盖表

规则见 `docs/content-authoring.md` 的“知识覆盖面标准”。依据：skill-tree 大纲 `../cs-math-skill-tree/data/outlines/M.1.1.json`：OpenStax《Calculus Volume 1》第 2.2–2.5、4.3、4.6 节和《Calculus Volume 2》第 5.1 节（免费全文）。“节”是技能内部编号，“原文”是教材自己的节号和标题。

这一站是 AI 路线的第一站，没有必须前置。课从“函数是什么”讲起（教材第 1 章是复习，大纲没收，`functions` 一课补上读懂后面要用的最少内容），三角函数只复习弧度和 sin、cos 的几个值（`one-sided`）。

`node scripts/check-coverage.mjs M.1.1` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | 2.2 Intuitive Definition of a Limit | `limit-intuition` |
| 1.2 | 2.2 The Existence of a Limit | `one-sided` |
| 1.3 | 2.2 One-Sided Limits | `one-sided` |
| 1.4 | 2.2 Infinite Limits | `infinite-limits` |
| 2.1 | 2.3 Evaluating Limits with the Limit Laws | `limit-laws` |
| 2.2 | 2.3 Limits of Polynomial and Rational Functions | `limit-laws` |
| 2.3 | 2.3 Additional Limit Evaluation Techniques | `limit-techniques` |
| 2.4 | 2.3 The Squeeze Theorem | `squeeze` |
| 3.1 | 2.4 Continuity at a Point | `continuity` |
| 3.2 | 2.4 Types of Discontinuities | `discontinuities` |
| 3.3 | 2.4 Continuity over an Interval | `continuity-interval` |
| 3.4 | 2.4 The Intermediate Value Theorem | `ivt` |
| 4.1 | 2.5 Quantifying Closeness | `epsilon-delta` |
| 4.2 | 2.5 Proving Limit Laws | `epsilon-proofs` |
| 4.3 | 2.5 Showing That a Limit Does Not Exist | `no-limit` |
| 4.4 | 2.5 One-Sided and Infinite Limits | `no-limit` |
| 5.1 | 4.3 Absolute Extrema | `extreme-value` |
| 5.2 | 4.3 Local Extrema and Critical Points | `extreme-value` |
| 6.1 | 4.6 Limits at Infinity and Horizontal Asymptotes | `limits-at-infinity` |
| 6.2 | 4.6 Infinite Limits at Infinity | `limits-at-infinity` |
| 7.1 | Vol.2 5.1 Terminology of Sequences | `sequences` |
| 7.2 | Vol.2 5.1 Limit of a Sequence | `seq-limit` |
| 7.3 | Vol.2 5.1 Limits Involving Continuous Functions Defined on Convergent Sequences | `continuity-interval` |
| 7.4 | Vol.2 5.1 Bounded Sequences | `bounded-seq` |

另有三课不对应单独的一节：`functions`（函数、定义域、图像、分段函数：教材第 1 章，大纲判为复习没收，但零基础读后面每一课都要用）、`infinitesimal-order`（无穷小的阶和等价替换：技能第 2 章“无穷小”，中文教材的讲法，英文教材只在 2.5 用 ε 语言说“距离任意小”，见大纲 `coverage` 的说明）、`uniform`（一致连续：技能第 4 章的说明把“紧致区间上的基本性质”定为介值定理、最值定理和一致连续三项，一致连续来自于品《数学分析》§11，英文主教材没有这一节）。

教到什么深度（入门层）：
- ε-δ 定义讲到能对一次函数、$x^2$ 选出 $\delta$，会用三角不等式证明和的法则；积和商的法则只讲结论。
- 无穷小的比较讲高阶、同阶、等价和三个常用等价（$\sin x$、$1-\cos x$、$\sqrt{1+x}-1$）；$e^x - 1$、$\ln(1+x)$ 这些要指数和对数的极限，属于一元微分学 M.1.2。
- 最值定理只讲内容和反例（证明属于实分析，教材也这样说明）。临界点讲成“曲线平坦或有尖角的点”，按定义用导数找临界点属于 M.1.2。
- 一致连续讲定义、$\frac1x$ 的反例和“闭区间上连续就一致连续”的结论，不讲证明（紧性、开覆盖属于数学分析）。
- 数列讲术语、ε-N 定义、四则运算、等比数列、单调收敛定理；级数（第 9 章）不属于这个技能。

## 和原文的核对

写课时（2026-11-04）主代理按 OpenStax 的内容写，但没有逐条打开原文。写完后由 pi 子代理逐条对照原文（7 节网页全文，报告 `temp/research/M.1.1-openstax-check.md`，不入库）：59 条里 45 条一致，7 条是这几节原文没有的内容（无穷小的阶、一致连续、二分法等，来源见上面“另有三课”），7 条有出入，同日按原文改了课：

- `limit-laws` 的开方法则：原文是偶次方根要 $L \ge 0$ 且 $f(x) \ge 0$，课里原来写成 $L > 0$；
- `continuity-interval` 的复合函数定理：原文只要求 $\lim_{x\to a} g(x) = L$ 且 $f$ 在 $L$ 处连续，课里原来多要求“$g$ 在 $a$ 处连续”（那是特例，现在两种都写）；
- `ivt` 的介值定理：原文是存在 $c \in [a, b]$，课里原来写成 $a < c < b$（$N$ 等于端点值时不成立），现在补上“$N$ 严格在两端之间时 $c$ 在内部”；
- `extreme-value` 的临界点：原文定义是“定义域的内点且 $f'(c) = 0$ 或 $f'(c)$ 不存在”。这一站还没有导数，课里改成“区间内部、切线水平或没有确定切线（尖角、竖直切线）的点”，导数的说法在 M.1.2；
- `squeeze` 里 $\frac{\sin x}{x} \to 1$ 的证法：原文文字比较的是三段长度 $\sin x < x < \tan x$，课里原来说成“比较两个三角形和一个扇形的面积”；
- 本表原来引的两个定理编号（“2.2 Theorem 2.1”“2.3 Theorem 2.8”）对不上原文，已改成写定理的内容。

对照一致的说法：极限的直观定义和“极限不看 $f(a)$”（2.2）、极限存在当且仅当左右极限存在且相等（2.2 Relating One-Sided and Two-Sided Limits）、极限运算法则（2.3）、$\lim \frac{\sin\theta}{\theta} = 1$ 和 $\lim\frac{1-\cos\theta}{\theta} = 0$（2.3，用夹逼定理）、点处连续的三个条件和三种间断点（2.4）、介值定理要求闭区间上连续（2.4）、ε-δ 定义和单侧、无穷极限的精确定义（2.5）、最值定理及“证明属于实分析”（4.3）、水平渐近线与无穷远处的无穷极限（4.6）、数列的通项和递推、等差和等比数列、收敛的定义、有界和单调收敛定理（Vol.2 5.1）。每个数值由 `tests/content/M.1.1.verify.py` 用 sympy 求极限、用浮点数重算核对。

## CS2023（`data/curation/scope.json`）

| 知识点 | CS2023 主题（scope.json 匹配原文） | 课 |
|---|---|---|
| 数列与函数极限 | MSF-Calculus，KA Core：Sequences, series, limits | `sequences`, `seq-limit`, `bounded-seq`, `limit-intuition`, `one-sided`, `limit-laws`, `limit-techniques`, `squeeze`, `limits-at-infinity` |

scope.json 说明 CS2023 只写到数列、级数和极限，连续性和闭区间性质没有对应主题。

## 原技能树的综合练习

| 小题 | 课 |
|---|---|
| (1a) $\lim \frac{3n^2-n}{2n^2+5}$ | `seq-limit`（分步例题就是这一题）、`limits-at-infinity` |
| (1b) $\lim \frac{\sin 3x}{x}$ | `squeeze`（分步例题） |
| (1c) $\lim \frac{\sqrt{1+x}-1}{x}$ | `limit-techniques`（分步例题：有理化） |
| (2) $1 - \cos x$ 与 $x^2$ 的阶 | `infinitesimal-order`（分步例题） |
| (3) 让 $\frac{x^2-4}{x-2}$ 在 2 处连续的 $a$ | `continuity`（分步例题） |
| (4) 介值定理找根、$\frac1x$ 在 $(0,1]$ 上没有最大值 | `ivt`、`extreme-value` |

## 后继技能要用的

必须后继只有一元微分学 M.1.2（还没有内容包）。它的导数定义是一个 $\frac00$ 型极限，要用到：约分、有理化（`limit-techniques`）、$\frac{\sin x}{x} \to 1$ 和 $\frac{1-\cos x}{x} \to 0$（`squeeze`，求 $\sin$ 的导数）、连续的定义（`continuity`）、等价无穷小（`infinitesimal-order`，微分就是增量的线性主部）、闭区间上的最值定理（`extreme-value`，罗尔定理和中值定理的前提）。
