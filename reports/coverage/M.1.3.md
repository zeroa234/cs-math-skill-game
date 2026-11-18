# M.1.3 一元积分学：覆盖表

**状态（2026-11-18）：已写完（v2 重写，按零基础与知识覆盖面标准重写）。** 依据 `../cs-math-skill-tree/data/outlines/M.1.3.json`、`output/outlines.json`、`../cs-math-skill-tree/data/curation/learning-paths/M.1.3.json` 与 `reports/chapter-order.md`（章节顺序按 OpenStax Calculus Vol. 2 Ch.1 重排为：`定积分` → `微积分基本定理与反常积分` → `不定积分`），主来源为 OpenStax《Calculus Volume 2》（Ch.1 & 3.7）与《Calculus Volume 1》（4.10），辅以中国大学 MOOC《高等数学》与同济/MIT 单变量微积分体系，对齐 `M.1.3` 综合练习 4 问，本地核对脚本 `tests/content/M.1.3.verify.py`（`.venv` 中 SymPy 1.14.0 符号积分/求导 + `fractions.Fraction` 黎曼和实测；注：下表“节”列为技能大纲叶子条目顺序编号）。

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Sigma (Summation) Notation | `riemann` |
| 1.2 | Approximating Area | `riemann` |
| 1.3 | Forming Riemann Sums | `riemann` |
| 2.1 | Definition and Notation | `signed-area` |
| 2.2 | Evaluating Definite Integrals | `signed-area` |
| 2.3 | Area and the Definite Integral | `signed-area` |
| 2.4 | Net Signed Area | `signed-area` |
| 2.5 | Total Area | `signed-area` |
| 3.1 | The Mean Value Theorem for Integrals | `fundamental` |
| 3.2 | Fundamental Theorem of Calculus Part 1: Integrals and Antiderivatives | `fundamental` |
| 3.3 | The Fundamental Theorem of Calculus, Part 2 | `fundamental` |
| 4.1 | Substitution for Definite Integrals | `substitution` |
| 5.1 | Integrating over an Infinite Interval | `improper` |
| 5.2 | Integrating a Discontinuous Integrand | `improper` |
| 5.3 | A Comparison Theorem | `improper` |
| 6.1 | The Reverse of Differentiation | `antiderivative` |
| 6.2 | Finding Antiderivatives | `antiderivative`、`integration-by-parts` |
| 6.3 | Indefinite Integrals | `antiderivative` |
| 6.4 | Integration Formulas | `antiderivative`、`integration-by-parts` |

## 核心主题（C2）、综合练习（C4）与前后继（C3 / C5）

- **核心主题映射（C2）**：`定积分`（`riemann`、`signed-area`）、`微积分基本定理与反常积分`（`fundamental`、`substitution`、`improper`）与 `不定积分`（`antiderivative`、`integration-by-parts`）完整覆盖课程简介要求及换元与分部计算技巧（按 `reports/chapter-order.md` 先定积分建立极限面积直觉，再由基本定理搭桥到不定积分技巧）。
- **综合练习 4 问映射（C4）**：
  - 第 (1) 问求不定积分 $\int x e^x\,dx$（分部积分）与 $\int \frac{2x}{1+x^2}\,dx$（凑微分换元） → `integration-by-parts`、`substitution`。
  - 第 (2) 问牛顿–莱布尼茨公式计算 $\int_0^\pi \sin x\,dx = 2$ 及几何面积意义 → `fundamental`、`signed-area`。
  - 第 (3) 问变上限积分 $F(x)=\int_0^{x^2} e^{-t^2}\,dt$ 求 $F'(x)=2x e^{-x^4}$ → `fundamental`。
  - 第 (4) 问反常积分收敛判别与求值（$\int_1^\infty x^{-2}\,dx = 1$ 收敛、$\int_1^\infty x^{-1}\,dx$ 发散、瑕积分 $\int_0^1 x^{-1/2}\,dx = 2$ 收敛） → `improper`。
- **前后继状态（C3 / C5）**：
  - 必须前置链为 `M.1.2 一元微分学` → `M.1.1 极限与连续性`（沿必须前置链递归继承 `极限`、`收敛`、`发散`、`无穷大`、`导数`、`复合函数`、`链式法则`、`乘积法则`、`自然对数`、`微分`、`中值定理` 等术语；本包补定义 `黎曼和`、`定积分`、`微积分基本定理`、`换元积分`、`反常积分`、`原函数`、`分部积分`、`变量`）。
  - 必须后继含 `M.1.4.4`、`M.1.6`、`M.1.9`、`M.2.1`、`M.6.1`、`M.8.2`、`C.3.1`、`H.1.1`、`H.1.3`（9 个必选后继，加上推荐后继 `M.1.4.1`、`M.1.5`、`X.3.3`）。本包所授的定积分、极限尾部收敛（含正态型衰减比较）与原函数换元/分部方法为这些后续概率、微分方程与模拟电子电路节点提供了扎实的一元积分运算准备（C5 无缺口）。
