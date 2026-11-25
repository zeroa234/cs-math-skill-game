# M.1.4.4 多元积分与向量分析：覆盖表

**状态（2026-11-23）：已写完，20 课，等用户验收。** 依据 `../cs-math-skill-tree/output/outlines.json` 的 M.1.4.4（主来源 OpenStax《Calculus Volume 3》5.1–5.5、5.7 和 MIT 18.02SC Unit 3 Part B–C、Unit 4 Part B–C）、`data/curation/learning-paths/M.1.4.4.json`（台大朱桦《微积分》第 14–16 章、于品《数学分析》§43–§49）和原技能树综合练习 6 小题。数值核对脚本 `tests/content/M.1.4.4.verify.py`（纯 Python：重积分用嵌套的辛普森求和，线积分和通量用参数化后的数值积分，散度、旋度用中心差分，和课里的精确值对照）。

前置：必须前置 M.1.3（定积分、原函数、换元、分部积分、微积分基本定理）和 M.1.4.1（偏导数、梯度、雅可比矩阵、平面变换、雅可比行列式、标量场），往下还有 M.1.2、M.1.1。推荐前置 M.3.1 不在必须前置链上，照 M.1.4.1 的做法把向量、点积、行列式写进 `assumes`；叉积在通量一课现讲（用 3×3 行列式的展开写法，只讲怎么算和它的方向、长度）。

章序按游戏（技能树原顺序）：二重 → 三重积分 → 区域分割 → 换元与雅可比行列式 → 曲线与曲面积分 → 梯度/散度/旋度 → Green/Gauss/Stokes定理。一般区域（I 型、II 型）放在“二重”里先讲，“区域分割”一章专讲把区域拆块和交换积分次序（二重和三重一起）。

## 课的安排

| 课 | 章 | 内容 |
|---|---|---|
| `double-volume` | 二重 | 用小长方体逼近体积，二重积分的定义（黎曼和）和性质 |
| `iterated` | 二重 | 累次积分和富比尼定理，矩形区域上的计算 |
| `general-regions` | 二重 | I 型、II 型区域，非矩形区域上的二重积分，面积（综合练习 1 的前一半） |
| `triple-box` | 三重积分 | 三元函数的积分、长方体上的三重累次积分、体积和平均值 |
| `triple-general` | 三重积分 | 一般有界区域上的三重积分：先定 z 的上下界，再在投影区域上做二重积分（综合练习 3） |
| `decompose` | 区域分割 | 把区域拆成几个 I 型、II 型区域分别积分，积分对区域的可加性 |
| `change-order` | 区域分割 | 交换二重积分次序（综合练习 1），三重积分的六种次序 |
| `polar` | 换元与雅可比行列式 | 极坐标矩形、一般极坐标区域、$dA = r\,dr\,d\theta$、面积和体积（综合练习 2） |
| `cyl-sph` | 换元与雅可比行列式 | 柱坐标、球坐标和它们的体积元 |
| `jacobian` | 换元与雅可比行列式 | 平面变换、一对一、雅可比行列式是面积放大倍数 |
| `change-vars` | 换元与雅可比行列式 | 二重积分和三重积分的一般换元公式 |
| `line-integrals` | 曲线与曲面积分 | 向量场、做功的线积分、参数化计算、几何意义、例题（综合练习 4 的前一半） |
| `line-space` | 曲线与曲面积分 | 空间里的向量场和线积分 |
| `flux` | 曲线与曲面积分 | 通过曲面的通量、$\mathbf n\,dS$ 的几种求法（球面、柱面、$z = f(x, y)$、参数曲面），叉积 |
| `conservative` | 梯度/散度/旋度 | 线积分基本定理、保守场和路径无关、恰当微分、梯度场、求势函数（平面和空间）（综合练习 4 的后一半） |
| `curl-div` | 梯度/散度/旋度 | 平面旋度、三维旋度和散度、$\nabla$ 记号、通量的物理意义（综合练习 5） |
| `green` | Green/Gauss/Stokes定理 | 格林定理（做功形式）、旋度为零推出保守、证明思路、用格林定理求面积（求积仪） |
| `green-normal` | Green/Gauss/Stokes定理 | 平面通量、格林定理的法向形式、多段边界、单连通区域 |
| `divergence-thm` | Green/Gauss/Stokes定理 | 散度定理、证明思路（综合练习 6） |
| `stokes` | Green/Gauss/Stokes定理 | 斯托克斯定理、证明思路、例题、单连通和拓扑、曲面无关性 |

## 大纲逐节（C1）

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Volumes and Double Integrals | `double-volume` |
| 1.2 | Properties of Double Integrals | `double-volume` |
| 1.3 | Iterated Integrals | `iterated` |
| 2.1 | General Regions of Integration | `general-regions` |
| 2.2 | Double Integrals over Nonrectangular Regions | `general-regions` |
| 2.3 | Decomposing Regions | `decompose` |
| 2.4 | Changing the Order of Integration | `change-order` |
| 3.1 | Polar Rectangular Regions of Integration | `polar` |
| 3.2 | General Polar Regions of Integration | `polar` |
| 3.3 | Polar Areas and Volumes | `polar` |
| 4.1 | Integrable Functions of Three Variables | `triple-box` |
| 4.2 | Triple Integrals over a General Bounded Region | `triple-general` |
| 4.3 | Changing the Order of Integration | `change-order` |
| 5.1 | Integration in Cylindrical Coordinates | `cyl-sph` |
| 5.2 | Integration in Spherical Coordinates | `cyl-sph` |
| 6.1 | Planar Transformations | `jacobian` |
| 6.2 | Jacobians | `jacobian` |
| 6.3 | Change of Variables for Double Integrals | `change-vars` |
| 6.4 | Change of Variables for Triple Integrals | `change-vars` |
| 7.1 | Vector Fields | `line-integrals` |
| 7.2 | Work and Line Integrals | `line-integrals` |
| 7.3 | Geometric Approach | `line-integrals` |
| 7.4 | Example: Line Integrals for Work | `line-integrals` |
| 7.5 | Fundamental Theorem for Line Integrals | `conservative` |
| 7.6 | Conservative Fields, Path Independence, Exact Differentials | `conservative` |
| 7.7 | Gradient Fields | `conservative` |
| 7.8 | Potential Functions | `conservative` |
| 7.9 | Curl | `curl-div` |
| 8.1 | Green’s Theorem | `green` |
| 8.2 | Curl(F) = 0 Implies Conservative | `green` |
| 8.3 | Proof of Green's Theorem | `green` |
| 8.4 | Planimeter: Green's Theorem and Area | `green` |
| 8.5 | Flux in 2D | `green-normal` |
| 8.6 | Normal Form of Green's Theorem | `green-normal` |
| 8.7 | Extended Green's Theorem: Boundaries with Multiple Pieces | `green-normal` |
| 8.8 | Simply Connected Regions and Conservative | `green-normal` |
| 9.1 | Vector Fields in Space | `line-space` |
| 9.2 | Flux Through a Surface | `flux` |
| 9.3 | Calculating Flux; Finding ndS | `flux` |
| 9.4 | ndS for a Surface z = f(x, y) | `flux` |
| 9.5 | Other Ways to Find ndS | `flux` |
| 9.6 | Divergence Theorem | `divergence-thm` |
| 9.7 | Physical Meaning of Flux; Del Notation | `curl-div` |
| 9.8 | Proof of the Divergence Theorem | `divergence-thm` |
| 10.1 | Line Integrals in Space | `line-space` |
| 10.2 | Gradient Fields and Potential Functions | `conservative` |
| 10.3 | Curl in 3D | `curl-div` |
| 10.4 | Stokes’ Theorem | `stokes` |
| 10.5 | Proof of Stokes’ Theorem | `stokes` |
| 10.6 | Example | `stokes` |
| 10.7 | Simply Connected Regions; Topology | `stokes` |
| 10.8 | Stokes’ Theorem and Surface Independence | `stokes` |

`omitted`（大纲自己写明不收的）：OpenStax 5.6 质心与转动惯量、各节习题；18.02SC Session 87 扩散方程、Session 96 总复习。本包同样不教。

## CS2023 核心主题（C2）

`scope.json` 写明 CS2023 的微积分只到多元微分，没有重积分、曲线曲面积分和三大定理，本技能没有 CS2023 主题。

## 原技能树综合练习（C4）

| 小题 | 内容 | 由哪一课教到 |
|---|---|---|
| (1) | $y = x^2$ 与 $y = x$ 围成的区域，两种次序算 $\iint_D x\,dA$ | `general-regions`、`change-order` |
| (2) | 极坐标算 $\iint e^{-(x^2+y^2)}\,dA$，说明 $dA = r\,dr\,d\theta$ 的 $r$ | `polar`、`jacobian` |
| (3) | $\iiint_E z\,dV$，$0 \le z \le x + y$ | `triple-general` |
| (4) | $\mathbf F = (y, x)$ 沿 $(t, t^2)$ 的线积分，判断保守、求势函数 | `line-integrals`、`conservative` |
| (5) | $\mathbf F = (x^2y, xy^2, z)$ 的散度和旋度 | `curl-div` |
| (6) | 用散度定理求 $(x, y, z)$ 穿过单位球面的通量 | `divergence-thm` |

## 后继技能用到的写法（C5）

必须后继是 E.1.1 电磁场与电磁波：用到通量、散度、旋度、$\nabla$ 记号、高斯散度定理、斯托克斯定理（把麦克斯韦方程组在积分形式和微分形式之间转换），以及球坐标、柱坐标下的积分（点电荷、长直导线）。这些都写进本包 `terms`，另加了“环流”（安培环路定理要用）。恒等式 $\nabla \times (\nabla \times \mathbf F) = \nabla(\nabla \cdot \mathbf F) - \nabla^2\mathbf F$ 只在推导电磁波方程时用到，不在本技能的大纲里，不教，留给 E.1.1 在用到时讲；本包讲了 $\nabla \times (\nabla f) = \mathbf 0$ 和 $\nabla \cdot (\nabla \times \mathbf F) = 0$。
