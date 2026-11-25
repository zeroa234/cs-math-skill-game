# E.1.1 电磁场与电磁波：覆盖表

**状态（2026-11-23 第 5 轮）：已写完。** 18 课，32/32 节，内容包 `data/content/E.1.1.yaml`，数值核对 `tests/content/E.1.1.verify.py`。依据 `../cs-math-skill-tree/output/outlines.json` 的 E.1.1（主来源 MIT 6.013 Staelin《Electromagnetics and Applications》第 1–2 章、第 4 章（静态和准静态场）、第 7 章（TEM 传输线）、第 9 章（波）、第 10 章（天线），大纲里的编号是重排后的 1–6 章）、`data/curation/learning-paths/E.1.1.json`（南京邮电大学《电磁场与电磁波理论》，西安电子科技大学《微波技术与天线》谐振器部分）和原技能树综合练习 8 小题。

前置：必须前置 N.1.2 大学物理：电磁学（库仑定律、高斯定律、安培环路定理、法拉第定律、位移电流、麦克斯韦方程组的积分形式、电磁波、坡印廷矢量）、M.1.4.4 多元积分与向量分析（通量、散度、旋度、∇ 记号、散度定理、斯托克斯定理、环流、球坐标和柱坐标）、H.1.1 电路（电压、电流、阻抗的入门）。复数相量在 E.3.2、H.1.5 讲过，但它们不在必须前置链上，本包在频域一课现讲 $e^{j\omega t}$ 和相量。

## 课的安排（18 课）

| 课 | 章 | 内容 |
|---|---|---|
| `em-review` | 静电场 | 复习：电荷、电场、磁场、洛伦兹力，场是怎样测量的，SI 单位和常数 $\varepsilon_0$、$\mu_0$、$c$ |
| `gauss-electrostatics` | 静电场 | 高斯定律的积分和微分形式 $\nabla\cdot\mathbf D = \rho$，电位和 $\mathbf E = -\nabla\Phi$，线电荷、同轴线电容（综合练习 1） |
| `images-laplace` | 静电场 | 镜像法，拉普拉斯方程和分离变量，通量管和场图 |
| `ampere-magnetostatics` | 恒定电流与静磁场 | 安培定律的积分和微分形式，同轴线电感（综合练习 2 前一半），非均匀材料中的静态场 |
| `relaxation-skin` | 恒定电流与静磁场 | 电荷弛豫时间，趋肤深度（综合练习 4 后一半） |
| `maxwell-differential` | 时变电磁场与麦克斯韦方程组 | 麦克斯韦方程组的微分形式，积分形式和微分形式的转换（散度定理、斯托克斯定理），位移电流（综合练习 3） |
| `media-boundaries` | 时变电磁场与麦克斯韦方程组 | 介质中的场（$\mathbf D = \varepsilon\mathbf E$、$\mathbf B = \mu\mathbf H$、$\mathbf J = \sigma\mathbf E$），边界条件，唯一性定理 |
| `poynting` | 时变电磁场与麦克斯韦方程组 | 时域和频域的功率与能量，坡印廷定理 |
| `waves-time` | 均匀平面波 | 从麦克斯韦方程组推出波动方程，均匀平面波，波速和波阻抗 |
| `waves-frequency` | 均匀平面波 | 相量和频域的麦克斯韦方程组，波数、波长、极化（线、圆、椭圆）（综合练习 4 前一半） |
| `tem-lines` | 传输线 | TEM 波和传输线方程，特性阻抗、波速（综合练习 2 后一半） |
| `line-junctions` | 传输线 | 负载处的反射系数、驻波比、输入阻抗，接头（综合练习 6） |
| `matching-resonance` | 传输线 | 四分之一波长变换、短截线匹配、史密斯圆图入门，TEM 谐振 |
| `normal-incidence` | 反射与折射 | 垂直入射：反射系数、透射系数、功率（综合练习 5 前一半），复杂媒质（有损、等离子体）入门 |
| `oblique-incidence` | 反射与折射 | 斜入射：斯涅尔定律、全反射、布儒斯特角（综合练习 5 后一半） |
| `waveguides` | 波导与谐振腔 | 平行板和矩形波导，TE、TM 模，截止频率（综合练习 7） |
| `cavities` | 波导与谐振腔 | 矩形谐振腔的谐振频率和品质因数 |
| `radiation` | 电磁辐射基础 | 电荷和电流的辐射，电流元（短偶极子）的场、辐射电阻（综合练习 8），天线增益、有效面积、阵列入门 |

## 大纲逐节（C1）

| 节 | 原文 | 课 |
|---|---|---|
| 1.1.1 | Introduction | `em-review` |
| 1.1.2 | Review of basic physical concepts and definitions | `em-review` |
| 1.2 | Forces and the measurement and nature of electromagnetic fields | `em-review` |
| 1.3 | Gauss’s Law and electrostatic fields and potentials | `gauss-electrostatics` |
| 1.4 | Ampere’s Law and magnetostatic fields | `ampere-magnetostatics` |
| 2.1 | Maxwell’s differential equations in the time domain | `maxwell-differential` |
| 2.2 | Electromagnetic waves in the time domain | `waves-time` |
| 2.3 | Maxwell’s equations, waves, and polarization in the frequency domain | `waves-frequency` |
| 2.4 | Relation between integral and differential forms of Maxwell’s equations | `maxwell-differential` |
| 2.5 | Electric and magnetic fields in media | `media-boundaries` |
| 2.6 | Boundary conditions for electromagnetic fields | `media-boundaries` |
| 2.7 | Power and energy in the time and frequency domains, Poynting theorem | `poynting` |
| 2.8 | Uniqueness theorem | `media-boundaries` |
| 3.1 | Introduction | `images-laplace` |
| 3.2 | Mirror image charges and currents | `images-laplace` |
| 3.3 | Relaxation of fields, skin depth | `relaxation-skin` |
| 3.4 | Static fields in inhomogeneous materials | `ampere-magnetostatics` |
| 3.5 | Laplace’s equation and separation of variables | `images-laplace` |
| 3.6 | Flux tubes and field mapping | `images-laplace` |
| 4.1 | TEM waves on structures | `tem-lines` |
| 4.2 | TEM lines with junctions | `line-junctions` |
| 4.3 | Methods for matching transmission lines | `matching-resonance` |
| 4.4 | TEM resonances | `matching-resonance` |
| 5.1 | Waves at planar boundaries at normal incidence | `normal-incidence` |
| 5.2 | Waves incident on planar boundaries at angles | `oblique-incidence` |
| 5.3 | Waves guided within Cartesian boundaries | `waveguides` |
| 5.4 | Cavity resonators | `cavities` |
| 5.5 | Waves in complex media | `normal-incidence` |
| 6.1 | Radiation from charges and currents | `radiation` |
| 6.2 | Short dipole antennas | `radiation` |
| 6.3 | Antenna gain, effective area, and circuit properties | `radiation` |
| 6.4 | Antenna arrays | `radiation` |

`omitted`：Staelin 第 3、5、6、8、11、12、13 章（器件、电磁力、机电、瞬态、常用天线、光通信、声学）和附录，本包同样不教。

## CS2023 核心主题（C2）

电子信息类专业课，`scope.json` 没有 CS2023 主题。

## 原技能树综合练习（C4）

| 小题 | 内容 | 由哪一课教到 |
|---|---|---|
| (1) | 线电荷的电场，同轴线单位长度电容 | `gauss-electrostatics` |
| (2) | 同轴线单位长度电感、特性阻抗、波速 | `ampere-magnetostatics`、`tem-lines` |
| (3) | 麦克斯韦方程组微分形式，铜里传导电流和位移电流之比 | `maxwell-differential` |
| (4) | 介质中平面波的相速、波长、波阻抗、磁场、功率密度；铜的趋肤深度 | `waves-frequency`、`poynting`、`relaxation-skin` |
| (5) | 垂直入射反射系数和功率，布儒斯特角 | `normal-incidence`、`oblique-incidence` |
| (6) | 反射系数、驻波比、四分之一波长变换器 | `line-junctions`、`matching-resonance` |
| (7) | WR-90 波导 TE₁₀ 截止频率 | `waveguides` |
| (8) | 电流元辐射电阻，半波振子 | `radiation` |

## 后继技能用到的写法（C5）

必须后继 E.1.2 微波工程与天线、E.1.4 光电子与光纤通信、E.1.6 电磁兼容与信号完整性、E.1.7 雷达原理（都还没有内容包）：用到传输线的反射系数、驻波比、特性阻抗、史密斯圆图，波导模式和截止频率，平面波、极化、天线增益和有效面积。这些写进本包 `terms`。
