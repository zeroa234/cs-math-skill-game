# E.3.5 电力系统继电保护：覆盖表

**状态（2026-11-23）：已写完，16 课，等用户验收。** 依据 `../cs-math-skill-tree/output/outlines.json` 的 E.3.5（主来源山东科技大学《电力系统继电保护原理》课程教学大纲，章节与张保会、尹项根《电力系统继电保护》一致；补充 Blackburn & Domin《Protective Relaying: Principles and Applications》第 4 版的 Relay Input Sources、Generator Protection、Microprocessor Applications 三章）、`data/curation/learning-paths/E.3.5.json`（三峡大学、南京工程学院的国家级课程，Kalahandi 工程学院讲义）和原技能树综合练习 8 小题。数值核对脚本 `tests/content/E.3.5.verify.py`（纯 Python：整定值、灵敏系数、阻抗换算按公式重算，差动电流用复数相量相加，傅里叶算法用采样序列实际计算）。

前置：必须前置 E.3.3 电力系统分析（标幺值、三相短路电流、对称分量、正序负序零序网络、断路器、短路电流计算、继电保护的目的在那里只提了一句）和 E.3.2 电机与电力拖动（变压器、同步发电机、相量、功率因数），往下有 H.1.1、N.1.2、M.2.1 等。三相短路电流、序分量、零序电流 $3I_0$ 的来历在 E.3.3 讲过，本包直接用；继电器、互感器、整定、灵敏系数都在本包从头讲。

## 课的安排

| 课 | 章 | 内容 |
|---|---|---|
| `protection-basics` | 继电保护的基本要求 | 正常、不正常和故障状态，继电保护的任务、基本原理（测量、逻辑、执行）和组成 |
| `four-requirements` | 继电保护的基本要求 | 选择性、速动性、灵敏性、可靠性和它们的矛盾，主保护和后备保护，保护范围（综合练习 1） |
| `instrument-transformers` | 互感器与保护装置 | 电流互感器、电压互感器的变比和极性，二次侧严禁开路和短路，电流互感器饱和，保护装置的输入回路（综合练习 2） |
| `current-three-zones` | 电流保护 | 单侧电源网络的电流速断、限时电流速断、定时限过电流，三段式的保护范围和配合 |
| `current-settings` | 电流保护 | 三段式整定计算：可靠系数、返回系数、自启动系数、灵敏系数、阶梯时限（综合练习 3） |
| `directional-current` | 电流保护 | 双侧电源网络的方向性电流保护，功率方向元件和 90° 接线，电压死区 |
| `zero-sequence` | 电流保护 | 中性点直接接地系统的零序电流和零序方向保护，中性点非直接接地系统单相接地的电容电流、绝缘监视和消弧线圈 |
| `distance-principle` | 距离保护 | 测量阻抗、距离保护的原理和三段、阻抗平面、方向圆和全阻抗圆特性 |
| `distance-settings` | 距离保护 | 整定计算和一次值换二次值（综合练习 4），过渡电阻的影响，系统振荡和振荡闭锁，对距离保护的评价 |
| `pilot-protection` | 输电线路纵联保护 | 纵联保护的原理，通道（导引线、载波、微波、光纤），方向比较式和电流差动式（综合练习 5） |
| `transformer-differential` | 变压器保护 | 变压器的故障和不正常状态，瓦斯保护，纵差动保护和不平衡电流，额定电流计算（综合练习 6 前一半） |
| `inrush-backup` | 变压器保护 | 励磁涌流和二次谐波制动、间断角，相间短路和接地短路的后备保护（综合练习 6 后一半） |
| `generator-protection` | 发电机与母线保护 | 发电机的故障和不正常状态，纵差动、定子接地、转子接地、失磁、负序、逆功率保护，分布式电源并网保护（综合练习 7 前一半） |
| `bus-protection` | 发电机与母线保护 | 母线故障和装设原则，母线差动保护，断路器失灵保护（综合练习 7 后一半） |
| `reclosing` | 自动重合闸 | 重合闸的作用和要求，三相一次重合闸、前加速和后加速，单相重合闸和潜供电流（综合练习 8 前一半） |
| `numerical-relays` | 微机保护原理 | 微机保护装置的构成，采样和抗混叠，全周傅里叶算法求幅值和相角，变电站自动化（综合练习 8 后一半） |

## 大纲逐节（C1）

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | 电力系统的正常工作状态、不正常工作状态和故障状态 | `protection-basics` |
| 1.2 | 继电保护的基本原理及其组成 | `protection-basics` |
| 1.3 | 对继电保护的基本要求 | `four-requirements` |
| 2.1 | 单侧电源网络相间短路的电流保护 | `current-three-zones`、`current-settings` |
| 2.2 | 双侧电源网络相间短路的方向性电流保护 | `directional-current` |
| 2.3 | 中性点接地系统中接地短路的零序电流及方向保护 | `zero-sequence` |
| 2.4 | 中性点非直接接地系统中单相接地故障的保护 | `zero-sequence` |
| 3.1 | 距离保护的基本概念 | `distance-principle` |
| 3.2 | 距离保护的基本原理和基本电量 | `distance-principle` |
| 3.3 | 距离元件静态特性的阻抗平面分析法 | `distance-principle` |
| 3.4 | 常用的圆和直线特性的阻抗元件 | `distance-principle` |
| 3.5 | 距离保护的整定计算与对距离保护的评价 | `distance-settings` |
| 3.6 | 短路点过渡电阻对距离保护的影响 | `distance-settings` |
| 3.7 | 距离保护的振荡闭锁 | `distance-settings` |
| 4.1 | 输电线路纵联保护概述 | `pilot-protection` |
| 4.2 | 输电线路纵联保护两侧信息的交换 | `pilot-protection` |
| 4.3 | 方向比较式纵联保护 | `pilot-protection` |
| 4.4 | 纵联电流差动保护 | `pilot-protection` |
| 5.1 | 自动重合闸的作用 | `reclosing` |
| 5.2 | 输电线路的三相一次自动重合闸 | `reclosing` |
| 5.3 | 高压输电线路的单相自动重合闸 | `reclosing` |
| 6.1 | 变压器的故障类型和不正常工作状态 | `transformer-differential` |
| 6.2 | 变压器纵差动保护 | `transformer-differential` |
| 6.3 | 变压器励磁涌流及鉴别方法 | `inrush-backup` |
| 6.4 | 变压器相间短路的后备保护 | `inrush-backup` |
| 6.5 | 变压器接地短路的后备保护 | `inrush-backup` |
| 7.1 | 母线故障及装设母线保护基本原则 | `bus-protection` |
| 7.2 | 母线差动保护基本原理 | `bus-protection` |
| 7.3 | 断路器失灵保护 | `bus-protection` |
| 8 | Relay Input Sources | `instrument-transformers` |
| 9 | Generator Protection/Intertie Protection for Distributed Generation | `generator-protection` |
| 10 | Microprocessor Applications and Substation Automation | `numerical-relays` |

## CS2023 核心主题（C2）

E.3.5 是电气类专业课，`scope.json` 没有 CS2023 主题。

## 原技能树综合练习（C4）

| 小题 | 内容 | 由哪一课教到 |
|---|---|---|
| (1) | 四个基本要求和它们的矛盾 | `four-requirements` |
| (2) | 电流互感器二次电流，二次侧严禁开路、电压互感器严禁短路 | `instrument-transformers` |
| (3) | 过电流保护一次、二次动作电流，三段式各保护哪一部分 | `current-three-zones`、`current-settings` |
| (4) | 距离 I 段二次整定阻抗，I 段为什么不保护全长 | `distance-principle`、`distance-settings` |
| (5) | 纵联保护为什么能无延时切除全长故障，依赖什么通道 | `pilot-protection` |
| (6) | 变压器两侧额定电流，差动保护为什么要考虑励磁涌流 | `transformer-differential`、`inrush-backup` |
| (7) | 发电机和母线保护的主要类型 | `generator-protection`、`bus-protection` |
| (8) | 重合闸为什么能提高可靠性，微机保护怎样算幅值和相角 | `reclosing`、`numerical-relays` |

## 后继技能用到的写法（C5）

E.3.5 在技能树里没有必须后继。
