# H.2.7 集成电路制造工艺：覆盖表

**状态（2026-11-26）：27 课已写完并按两份通读报告修改（第 10 轮），check-coverage 54/54 节，verify.py 162 项，FULL e2e 27 课通过。** 依据 `../cs-math-skill-tree/data/outlines/H.2.7.json`（主来源 Plummer & Griffin *Integrated Circuit Fabrication: Science and Technology*，2024）、学习资源（北京信息职业技术学院《微电子制造工艺》、西电《现代集成电路制造技术》）和原技能树综合练习。数值核对脚本将是 `tests/content/H.2.7.verify.py`。

前置：必须前置只有 N.1.2 大学物理：电磁学（电场、电势、电容、电流、电阻率、电介质能直接用）。N.2.2、H.2.5 只是推荐前置，不继承：晶格、晶向、掺杂、n 型和 p 型、MOSFET、CMOS、阈值电压、PN 结这些都要在本包里先讲（jargon 里的晶格、密勒指数、施主、受主、n型半导体、扩散系数、衍射、瑞利判据等 B1 会查）。

## 课的安排（27 课）

| 章 | 课 | 内容 |
|---|---|---|
| CMOS工艺集成 | `planar-process` | 平面工艺的思路：一层层“长膜/氧化 → 光刻 → 刻蚀 → 掺杂”；晶圆、n 型和 p 型掺杂、MOSFET 和 CMOS 的结构 |
|  | `isolation-wells` | 衬底准备和浅槽隔离（STI），阱的形成（倒掺杂阱） |
|  | `vt-gate` | 阈值调整注入 $\Delta V_T = qQ/C_{ox}$，栅氧化层和多晶硅假栅（后栅工艺的金属栅替换） |
|  | `sd-contacts` | 轻掺杂漏（LDD）、侧墙、晕环注入、源漏掺杂，自对准硅化物和接触孔 |
|  | `finfet` | FinFET 的结构、有效沟道宽度 $2H_{fin} + W_{fin}$、为什么要从平面管转到鳍式 |
| 金属化与化学机械抛光 | `beol` | 后道工艺（BEOL）：多层互连、铝到铜、大马士革和双大马士革工艺 |
|  | `backend-issues` | 后道的关键问题：电迁移（Black 方程）、阻挡层、低 k 介质和 RC 延迟、未来结构，化合物半导体的后道 |
|  | `cmp` | 化学机械抛光：Preston 方程、碟形凹陷和侵蚀、STI 和铜 CMP |
| 晶圆与洁净室 | `crystal-growth` | 硅的金刚石结构和晶向（密勒指数），直拉法和区熔法，杂质分凝 |
|  | `wafer-soi` | 晶圆加工（切片、研磨、抛光、定位缺口），每片晶圆的芯片数，SOI 和键合晶圆（智能剥离） |
|  | `contamination` | 三级污染控制：洁净室（ISO 等级）、晶圆清洗（RCA 清洗）、吸杂 |
| 良率与工艺监控 | `yield` | 缺陷和良率模型：泊松模型 $Y = e^{-DA}$、负二项模型，面积对良率的影响 |
|  | `process-control` | 参数良率和工艺控制：正态分布、控制图、过程能力指数 $C_p$、$C_{pk}$ |
| 光刻 | `litho-concepts` | 光刻的流程和发展：掩模、接触/接近/投影曝光、步进扫描、光源波长从 g 线到 EUV |
|  | `litho-optics` | 衍射和成像：数值孔径、瑞利分辨率 $R = k_1\lambda/NA$、焦深 $k_2\lambda/NA^2$ |
|  | `photoresist` | 光刻胶：正胶和负胶、对比度、化学放大胶，涂胶到坚膜的工序 |
|  | `ret-nil` | 分辨率增强：离轴照明、浸没式、光学邻近效应修正、相移掩模、多重图形、EUV；纳米压印 |
| 氧化 | `deal-grove` | 热氧化和 Deal–Grove 模型 $x^2 + Ax = B(t + \tau)$，线性和抛物线两个区，干氧和湿氧 |
|  | `oxide-2d-highk` | 薄氧化层的初始快速生长，体积膨胀、应力和二维生长（LOCOS 鸟嘴），高 k 介质和等效氧化层厚度 |
| 扩散与离子注入 | `fick-diffusion` | 杂质在硅里怎样扩散，菲克定律，恒定表面浓度（erfc）和有限源（高斯）两种解，结深 |
|  | `diffused-layers` | 扩散系数的阿伦尼乌斯关系，方块电阻和四探针，掺杂方法 |
|  | `implant-basics` | 离子注入：剂量 $Q = It/(qA)$、投影射程和高斯分布、峰值浓度、多层注入和掩蔽厚度 |
|  | `stopping-annealing` | 核阻止和电子阻止、沟道效应，注入损伤和退火（快速热退火、瞬态增强扩散），等离子体浸没注入 |
| 刻蚀 | `wet-etch` | 湿法刻蚀：各向同性和横向钻蚀、选择比、过刻、KOH 的各向异性 |
|  | `plasma-etch` | 等离子体刻蚀：等离子体的产生，化学、物理、离子增强三种机理，反应离子刻蚀的各向异性，原子层刻蚀 |
| 薄膜沉积 | `cvd` | 化学气相沉积：台阶覆盖，表面反应控制和质量输运控制（Grove 模型），LPCVD、PECVD、原子层沉积 |
|  | `pvd` | 物理气相沉积：溅射和蒸发、平均自由程、方向性和阴影效应，沉积的模型和仿真（黏附系数） |

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Basic CMOS Technology and Device Structures | `planar-process` |
| 1.2 | Preparing the Substrate for Transistors | `isolation-wells` |
| 1.3 | Well Formation | `isolation-wells` |
| 1.4 | Threshold-Adjust Implants | `vt-gate` |
| 1.5 | Gate Oxide and Polysilicon“Dummy”Gate | `vt-gate` |
| 1.6 | Lightly Doped Drain Formation, Halo Implants and Source/Drain Doping | `sd-contacts` |
| 1.7 | Contact Formation | `sd-contacts` |
| 1.8 | The Back-End-of-Line (BEOL) Process | `beol` |
| 1.9 | The Introduction of the FinFET | `finfet` |
| 2.1 | Silicon Crystal Growth Methods: Czochralski and Float Zone | `crystal-growth` |
| 2.2 | Wafer Preparation | `wafer-soi` |
| 2.3 | Other Wafer Approaches: Silicon-on-Insulator and Bonded Wafers | `wafer-soi` |
| 3.1 | Level 1 Contamination Reduction: Clean Factories | `contamination` |
| 3.2 | Level 2 Contamination Reduction: Wafer Cleaning | `contamination` |
| 3.3 | Level 3 Contamination Reduction: Gettering in Silicon | `contamination` |
| 3.4 | Modeling Yield in Chip Manufacturing | `yield` |
| 3.5 | Parametric Yield: Manufacturing Process Control | `process-control` |
| 4.1 | Historical Development and General Concepts | `litho-concepts` |
| 4.2 | Optical System Basics: Ray Tracing and Diffraction | `litho-optics` |
| 4.3 | Photoresist Basics: Properties and Processing | `photoresist` |
| 4.4 | Resolution Enhancement Methods | `ret-nil` |
| 4.5 | Nanoimprint Lithography | `ret-nil` |
| 5.1 | Introduction | `deal-grove` |
| 5.2 | Basic Model for Oxide Growth | `deal-grove` |
| 5.3 | Thin Oxide Growth Kinetics in Dry O2 Ambients | `oxide-2d-highk` |
| 5.4 | Oxide Flow, Stress and Two-Dimensional Growth | `oxide-2d-highk` |
| 5.5 | High-K Dielectrics | `oxide-2d-highk` |
| 6.1 | Introduction and Basic Concepts | `fick-diffusion` |
| 6.2 | Diffusion from a Macroscopic Viewpoint | `fick-diffusion` |
| 6.3 | Analytic Solutions of the Diffusion Equation | `fick-diffusion` |
| 6.4 | Intrinsic Diffusion Coefficients of Dopants in Silicon | `diffused-layers` |
| 6.5 | Design and Evaluation of Diffused Layers | `diffused-layers` |
| 6.6 | Doping Methods | `diffused-layers` |
| 7.1 | Introduction | `implant-basics` |
| 7.2 | Historical Development and Basic Concepts | `implant-basics` |
| 7.3 | Multilayer Implants | `implant-basics` |
| 7.4 | Nuclear and Electronic Stopping | `stopping-annealing` |
| 7.5 | Damage Production and Damage Annealing | `stopping-annealing` |
| 7.6 | Plasma Immersion Ion Implantation | `stopping-annealing` |
| 8.1 | Wet Etching | `wet-etch` |
| 8.2 | Basics of Dry or Plasma Etching | `plasma-etch` |
| 8.3 | Plasma Etching Mechanisms | `plasma-etch` |
| 8.4 | Atomic Layer Etching (ALE) | `plasma-etch` |
| 8.5 | Planarization Methods: Chemical–Mechanical Polishing (CMP) | `cmp` |
| 9.1 | Introduction | `cvd` |
| 9.2 | Chemical Vapor Deposition (CVD) | `cvd` |
| 9.3 | Physical Deposition Systems: Sputtering Systems | `pvd` |
| 9.4 | Evaporation | `pvd` |
| 9.5 | Deposition Models and Simulations | `pvd` |
| 10.1 | Historical Development and Basic Concepts | `beol` |
| 10.2 | Key Process Technologies and Back-End Issues | `backend-issues` |
| 10.3 | Future Evolution of Back-End Structures | `backend-issues` |
| 10.4 | Si CMOS Back-End Technology Revisited | `beol` |
| 10.5 | Back-End Technologies for Compound Semiconductors | `backend-issues` |

## CS2023 核心主题（C2）

`scope.json` 没有给 H.2.7 匹配 CS2023 主题（器件制造不在 CS2023 的范围里）。

## 学习资源的章节（C3）

写课时逐条核对：北信《微电子制造工艺》第二章洁净技术、第三章半导体材料（晶面晶向、单晶硅制备、晶圆加工）、第四章硅平面工艺（双极、MOS、CMOS、BiCMOS 流程）、第五章薄膜制备（氧化、CVD、外延、PVD）、第六章光刻（含 6.11 刻蚀）、第七章掺杂（扩散、离子注入）、第八章金属化与平坦化（欧姆接触、布线、平坦化、铜）；西电 MOOC 概述里的各单项工艺。

## 综合练习（C4）

| 小题 | 负责的课 |
|---|---|
| (1) 洁净室、(100) 晶向 | `contamination`、`crystal-growth` |
| (2) Deal–Grove 估算氧化时间，干氧和湿氧 | `deal-grove` |
| (3) 瑞利分辨率和焦深，提高 NA 的代价 | `litho-optics` |
| (4) 选择比、过刻、各向异性干法刻蚀 | `wet-etch`、`plasma-etch` |
| (5) erfc 扩散的结深，注入峰值浓度，退火 | `fick-diffusion`、`implant-basics`、`stopping-annealing` |
| (6) CVD 和溅射的台阶覆盖 | `cvd`、`pvd` |
| (7) 铜为什么用大马士革加 CMP | `beol`、`cmp` |
| (8) 简化 CMOS 流程的顺序，泊松良率 | `planar-process` 到 `sd-contacts`、`yield` |

## 后继技能用到的（C5）

H.2.7 没有直接解锁的技能。H.2.4 不以它为前置（只用到 H.2.5 讲的设计规则和工艺概念）。
