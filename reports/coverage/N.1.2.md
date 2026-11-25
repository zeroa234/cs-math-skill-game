# N.1.2 大学物理：电磁学：覆盖表

**状态（2026-11-23）：已写完（22 课，66/66 节，check-pack、check-coverage、verify.py 130 项、FULL e2e 通过）。** 依据 `../cs-math-skill-tree/data/outlines/N.1.2.json`（主来源 OpenStax *University Physics* 第二卷第 5–14、16 章）、`data/curation/learning-paths/N.1.2.json`（中科大叶邦角《电磁学》、清华大学物理录像、MIT 8.02）和原技能树综合练习 7 小题。数值核对脚本 `tests/content/N.1.2.verify.py`。

前置：必须前置 N.1.1（矢量、力、功、势能、动能、圆周运动、力矩可直接用）和 M.1.3（定积分、原函数可直接用）。推荐前置 M.1.4.4 多元积分与向量分析还没有内容包，所以通量（面积分）和环路积分只按“分成小块再相加”讲，并且只用在对称的情形，算的时候都化成简单的乘法。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Electric Charge | `charge-coulomb` |
| 1.2 | Conductors, Insulators, and Charging by Induction | `charge-coulomb` |
| 1.3 | Coulomb's Law | `charge-coulomb` |
| 1.4 | Electric Field | `electric-field` |
| 1.5 | Calculating Electric Fields of Charge Distributions | `electric-field` |
| 1.6 | Electric Field Lines | `electric-field` |
| 1.7 | Electric Dipoles | `electric-field` |
| 2.1 | Electric Flux | `gauss-law` |
| 2.2 | Explaining Gauss's Law | `gauss-law` |
| 2.3 | Applying Gauss's Law | `gauss-applications` |
| 2.4 | Conductors in Electrostatic Equilibrium | `gauss-applications` |
| 3.1 | Electric Potential Energy | `potential` |
| 3.2 | Electric Potential and Potential Difference | `potential` |
| 3.3 | Calculations of Electric Potential | `potential-calc` |
| 3.4 | Determining Field from Potential | `potential-calc` |
| 3.5 | Equipotential Surfaces and Conductors | `potential-calc` |
| 3.6 | Applications of Electrostatics | `potential-calc` |
| 4.1 | Capacitors and Capacitance | `capacitance` |
| 4.2 | Capacitors in Series and in Parallel | `capacitance` |
| 4.3 | Energy Stored in a Capacitor | `capacitance` |
| 4.4 | Capacitor with a Dielectric | `dielectrics` |
| 4.5 | Molecular Model of a Dielectric | `dielectrics` |
| 5.1 | Electrical Current | `current-resistance` |
| 5.2 | Model of Conduction in Metals | `current-resistance` |
| 5.3 | Resistivity and Resistance | `current-resistance` |
| 5.4 | Ohm's Law | `current-resistance` |
| 5.5 | Electrical Energy and Power | `power-emf` |
| 5.6 | Superconductors | `power-emf` |
| 6.1 | Electromotive Force | `power-emf` |
| 6.2 | Resistors in Series and Parallel | `dc-circuits` |
| 6.3 | Kirchhoff's Rules | `dc-circuits` |
| 6.4 | Electrical Measuring Instruments | `dc-circuits` |
| 6.5 | RC Circuits | `rc-safety` |
| 6.6 | Household Wiring and Electrical Safety | `rc-safety` |
| 7.1 | Magnetism and Its Historical Discoveries | `magnetic-force-charge` |
| 7.2 | Magnetic Fields and Lines | `magnetic-force-charge` |
| 7.3 | Motion of a Charged Particle in a Magnetic Field | `magnetic-force-charge` |
| 7.4 | Magnetic Force on a Current-Carrying Conductor | `magnetic-force-current` |
| 7.5 | Force and Torque on a Current Loop | `magnetic-force-current` |
| 7.6 | The Hall Effect | `magnetic-force-current` |
| 7.7 | Applications of Magnetic Forces and Fields | `magnetic-force-current` |
| 8.1 | The Biot-Savart Law | `biot-savart` |
| 8.2 | Magnetic Field Due to a Thin Straight Wire | `biot-savart` |
| 8.3 | Magnetic Force between Two Parallel Currents | `biot-savart` |
| 8.4 | Magnetic Field of a Current Loop | `biot-savart` |
| 8.5 | Ampère's Law | `ampere-law` |
| 8.6 | Solenoids and Toroids | `ampere-law` |
| 8.7 | Magnetism in Matter | `ampere-law` |
| 9.1 | Faraday's Law | `faraday-lenz` |
| 9.2 | Lenz's Law | `faraday-lenz` |
| 9.3 | Motional Emf | `faraday-lenz` |
| 9.4 | Induced Electric Fields | `induction-applications` |
| 9.5 | Eddy Currents | `induction-applications` |
| 9.6 | Electric Generators and Back Emf | `induction-applications` |
| 9.7 | Applications of Electromagnetic Induction | `induction-applications` |
| 10.1 | Mutual Inductance | `inductance` |
| 10.2 | Self-Inductance and Inductors | `inductance` |
| 10.3 | Energy in a Magnetic Field | `inductance` |
| 10.4 | RL Circuits | `rl-lc-rlc` |
| 10.5 | Oscillations in an LC Circuit | `rl-lc-rlc` |
| 10.6 | RLC Series Circuits | `rl-lc-rlc` |
| 11.1 | Maxwell's Equations and Electromagnetic Waves | `maxwell` |
| 11.2 | Plane Electromagnetic Waves | `em-waves` |
| 11.3 | Energy Carried by Electromagnetic Waves | `em-waves` |
| 11.4 | Momentum and Radiation Pressure | `em-waves` |
| 11.5 | The Electromagnetic Spectrum | `em-waves` |

## CS2023 核心主题（C2）

`scope.json` 对 N.1.2 只给国标物理学类的电磁学，没有 CS2023 主题；全部 8 章由上表的课负责。

## 学习资源的章节（C3）

- en1（OpenStax 第二卷第 5–14、16 章）：就是上面的大纲，逐节落课。
- zh1、zh2 里比 OpenStax 多的电位移矢量 $D$：在 `dielectrics` 用一段说明 $D = \varepsilon_0 E + P$ 和“自由电荷”的高斯定律，不展开推导。
- MIT 8.02 的电磁波偏振：在 `em-waves` 用一句话说明电场振动方向就是偏振方向，不讲马吕斯定律（属于 N.1.3 光学）。
- 交流电路（OpenStax 第 15 章）：大纲不收，RLC 只讲串联时的阻尼振荡。

## 原技能树综合练习（C4）

| 小题 | 内容 | 由哪一课教到 |
|---|---|---|
| (1) | 两点电荷的库仑力、中点合场强 | `charge-coulomb`、`electric-field` |
| (2) | 均匀带电球体内外的场（高斯定律） | `gauss-applications` |
| (3) | 平行板电容器的电容、电荷、储能 | `capacitance` |
| (4) | 导线电阻和发热功率 | `current-resistance`、`power-emf` |
| (5) | 长直导线和螺线管的磁场，安培环路的路径 | `ampere-law` |
| (6) | 线圈的平均感应电动势和楞次定律 | `faraday-lenz` |
| (7) | 麦克斯韦方程组积分形式、位移电流、光速 | `maxwell` |

## 后继技能用到的写法（C5）

必须后继：N.1.3 振动、波动与光学，H.2.7 集成电路制造工艺，E.1.1 电磁场与电磁波，E.3.2 电机与电力拖动，E.3.4 高电压技术，H.2.10 MEMS 与微传感器（都还没有内容包）。它们直接用到：电场、电势、电容、电流、电阻、磁感应强度、安培力、洛伦兹力、法拉第定律、电感、麦克斯韦方程组积分形式、电磁波速度。这些都写进本包 `terms`。
