# E.3.3 电力系统分析：覆盖表

**状态（2026-11-23）：已写完，17 课，等用户验收。** 依据 `../cs-math-skill-tree/data/outlines/E.3.3.json`（主来源 P. S. R. Murty《Electrical Power Systems》第 1、2、6、12–14、17–21 章；MIT 6.061 Introduction to Electric Power Systems 2011 讲座表的相关讲次）、`data/curation/learning-paths/E.3.3.json`（吉林大学《电力系统分析》MOOC 第一至九章；常州工学院《风力发电技术》的并网与储能章节）和原技能树综合练习 8 小题。数值核对脚本 `tests/content/E.3.3.verify.py`。

前置：必须前置 H.1.1（电压、电流、欧姆定律、基尔霍夫定律、方均根）、M.3.1（矩阵、逆矩阵、线性方程组、稀疏矩阵的思想）和 E.3.2（相量、功率因数、无功功率、功角、同步电机的等效电路和功角特性、摇摆方程、变压器等效电路和标幺值的初步、线电压和相电压）。E.3.2 只讲了以额定值为基准的标幺值，本包在 `per-unit` 讲系统统一基准和换算；E.3.2 的摇摆方程用 $M$ 写，本包在 `steady-state-stability` 引入惯性时间常数 $H$ 并说明 $M$ 和 $H$ 的关系。牛顿迭代法在 `newton-raphson` 现讲。

## 课的安排

| 课 | 章 | 内容 |
|---|---|---|
| `system-overview` | 电力系统组成与标幺值 | 发电、输电、配电、用电；我国的电压等级；为什么高压输电；中性点接地方式；主接线的概念 |
| `per-unit` | 电力系统组成与标幺值 | 三相功率、基准容量和基准电压、基准阻抗和基准电流、标幺值在变压器两侧不变、换基准（综合练习 1） |
| `line-parameters` | 输电线路参数与模型 | 线路的电阻、电感、电容和电导；电感和电容的公式、分裂导线、换位；典型值 0.4 Ω/km、2.8 μS/km |
| `line-models` | 输电线路参数与模型 | 短线路、π 型等值电路、长线路的分布参数（电报方程、波阻抗、传播常数）、自然功率、空载长线末端电压升高（综合练习 2） |
| `line-power-flow` | 输电线路参数与模型 | 复功率、线路上有功和无功怎样流动 $P = \frac{V_1V_2}{X}\sin\delta$、电压降落 $\frac{PR + QX}{V}$、线损和电压等级 |
| `network-matrices` | 潮流计算 | 网络的图、关联矩阵、节点导纳矩阵的形成和稀疏性 |
| `load-flow-equations` | 潮流计算 | 节点功率方程、PQ 节点、PV 节点、平衡节点、高斯–赛德尔迭代（综合练习 3 后半） |
| `newton-raphson` | 潮流计算 | 牛顿–拉夫逊法和雅可比矩阵、PQ 分解法、直流潮流（综合练习 3） |
| `three-phase-fault` | 对称与不对称故障分析 | 三相短路电流、短路容量、同步发电机的次暂态和暂态电抗、冲击电流（综合练习 4 前半） |
| `symmetrical-components` | 对称与不对称故障分析 | 算子 $a$、正序负序零序、对称分量变换、各元件的序阻抗、变压器接线对零序的影响 |
| `unbalanced-faults` | 对称与不对称故障分析 | 单相接地、两相短路、两相接地短路的序网连接，正序等效定则（综合练习 4 后半） |
| `steady-state-stability` | 电力系统稳定性 | 稳定的分类、惯性时间常数 $H$、功角特性和静态稳定极限、小干扰下的振荡频率、提高静态稳定的措施（综合练习 5 前半） |
| `transient-stability` | 电力系统稳定性 | 等面积定则、极限切除角和切除时间、摇摆方程的逐步计算、提高暂态稳定的措施（综合练习 5 后半） |
| `frequency-control` | 频率与电压控制 | 有功平衡和频率、负荷的频率调节效应、调差系数和一次调频、二次调频（综合练习 6） |
| `voltage-control` | 频率与电压控制 | 无功平衡和电压、调压手段（发电机励磁、变压器分接头、并联电容器和电抗器、静止无功补偿、串联补偿）、分接头选择（综合练习 6） |
| `economic-dispatch` | 经济调度 | 耗量特性、微增率、等微增率准则、拉格朗日乘子和系统边际成本、出力上下限、网损修正（综合练习 7） |
| `renewables-integration` | 新能源并网概述 | 风电机组的类型（定速异步、双馈、永磁直驱）、光伏和变流器并网、系统惯量下降和频率变化率、虚拟惯量和构网型变流器、储能（综合练习 8） |

## 大纲逐节

大纲是两份来源的章（讲）目录，没有小节。

| 节 | 原文 | 课 |
|---|---|---|
| 1 | Introduction | `system-overview` |
| 2 | Line Parameters | `line-parameters` |
| 3 | Performance of Transmission Lines | `line-models`、`line-power-flow` |
| 4 | Graph Theory and Network Matrices | `network-matrices` |
| 5 | Short Circuit Analysis | `three-phase-fault` |
| 6 | Unbalanced Fault Analysis | `unbalanced-faults` |
| 7 | Relaying and Protection | 不教：属于必须后继 E.3.5 电力系统继电保护；`three-phase-fault` 只说明为什么要算短路电流（选断路器、整定保护） |
| 8 | Power System Stability | `steady-state-stability`、`transient-stability` |
| 9 | Load Flow Analysis | `load-flow-equations`、`newton-raphson` |
| 10 | Economic Operation of Power Systems | `economic-dispatch` |
| 11 | Load Frequency Control | `frequency-control` |
| 12 | Voltage and Reactive Power Control | `voltage-control` |
| 13 | Introduction to power systems | `system-overview` |
| 14 | Sinusoidal steady state: complex impedance; flow through lines | `per-unit`、`line-power-flow` |
| 15 | Transmission lines: telegrapher’s equations | `line-models` |
| 16 | Transformers and per-unit systems | `per-unit` |
| 17 | Unbalanced circuits: symmetrical components | `symmetrical-components` |
| 18 | Symmetrical components, transformers, faults, protection | `symmetrical-components`、`unbalanced-faults` |
| 19 | Protection, load flow | `load-flow-equations` |

## 中文主课的章节（C3）

吉林大学 MOOC 第一至九章列出的概念都在上表的课里，下面几项只讲到入门深度：

- 6.x 同步发电机突然三相短路的完整暂态过程（派克方程求解）：`three-phase-fault` 只讲次暂态、暂态、稳态三段电抗和非周期分量，不推导。
- 6.10、3.x 的计算机解法：`network-matrices`、`newton-raphson` 讲矩阵形式和迭代步骤，不写程序。
- 9.4 最优潮流仿真实验、9.5 无功功率经济分配：`economic-dispatch` 用一段话说明最优潮流是在潮流方程和电压、线路约束下求成本最小，不做仿真。

## CS2023 核心主题（C2）

`scope.json` 对 E.3.3 没有 CS2023 主题；8 个章由上表的课负责。

## 原技能树综合练习（C4）

| 小题 | 内容 | 由哪一课教到 |
|---|---|---|
| (1) | 基准阻抗、线路电抗的标幺值、为什么用标幺值 | `per-unit` |
| (2) | π 型等值电路、空载长线末端电压升高 | `line-models` |
| (3) | 两母线的功角、节点功率方程、牛顿–拉夫逊迭代、节点类型 | `line-power-flow`、`load-flow-equations`、`newton-raphson` |
| (4) | 三相短路电流（标幺值和安）、单相接地短路电流、对称分量法 | `three-phase-fault`、`symmetrical-components`、`unbalanced-faults` |
| (5) | 功角特性的最大功率和稳态功角、等面积定则 | `steady-state-stability`、`transient-stability` |
| (6) | 调差系数和一次调频；频率对应有功平衡、电压对应无功平衡 | `frequency-control`、`voltage-control` |
| (7) | 等微增率、经济分配和系统边际成本 | `economic-dispatch` |
| (8) | 变流器并网对惯量和频率稳定的影响 | `renewables-integration` |

## 后继技能用到的写法（C5）

必须后继 E.3.5 电力系统继电保护还没有内容包；按它的简介（互感器、电流保护、距离保护、纵联保护、变压器和发电机保护、自动重合闸），三相短路电流和短路容量由 `three-phase-fault` 负责，对称分量、零序电流和不对称短路由 `symmetrical-components`、`unbalanced-faults` 负责，中性点接地方式由 `system-overview` 负责。
