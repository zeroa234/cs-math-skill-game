# H.2.8 电子设计自动化（EDA）算法：覆盖表

**状态（2026-11-26）：已写完（第 10 轮写第 1–10 课，第 11 轮写第 11–26 课和结业挑战），26 课，大纲 62 节全部有课。** 依据 `../cs-math-skill-tree/data/outlines/H.2.8.json`（主来源 Kahng, Lienig, Markov, Hu *VLSI Physical Design: From Graph Partitioning to Timing Closure*；逻辑综合和仿真取 Wang, Chang, Cheng *Electronic Design Automation* 第 6、8 章；物理验证取 KLayout 手册）和原技能树综合练习。数值核对脚本将是 `tests/content/H.2.8.verify.py`。

前置：必须前置只有 F.1.2 算法分析与设计（图、BFS、Dijkstra、动态规划、最小生成树、NP 完全、贪心、复杂度都能直接用）。H.1.2、H.2.4 只是推荐前置，不继承：布尔代数、卡诺图、标准单元、布局布线、静态时序分析这些要在本包里先讲到够用。写课前先 `node temp/closure-terms.mjs H.2.8` 看 F.1.2 链上讲过的术语。

## 课的安排（26 课）

| 章 | 课 | 内容 |
|---|---|---|
| 逻辑综合与布尔优化 | `eda-intro` | 电子设计自动化是什么、设计流程、设计风格（全定制、标准单元、门阵列、FPGA），物理设计要优化的目标 |
|  | `complexity-graphs` | 算法复杂度和 NP 难问题、为什么用启发式；图和超图的术语；网表、线网、引脚、单元等 EDA 常用词 |
|  | `two-level` | 两级逻辑最小化：蕴涵项、质蕴涵项、Quine–McCluskey 和覆盖问题（综合练习 1） |
|  | `bdd-sat` | 计算布尔代数：二元决策图（BDD）的构造和变量顺序，可满足性（SAT）和等价性检查 |
|  | `multilevel` | 多级逻辑优化：因式分解、提取公共子式（核）、无关项 |
| 技术映射 | `tech-mapping` | 主题图、单元库模式、树覆盖的动态规划，把 DAG 拆成树（综合练习 2） |
| 电路划分 | `partition-goals` | 为什么要划分、割边数和平衡约束，超图的割 |
|  | `kl-fm` | Kernighan–Lin 算法（交换增益、锁定、取最好前缀，综合练习 3）和 Fiduccia–Mattheyses 算法 |
|  | `multilevel-partition` | 多级划分框架：粗化、初始划分、细化 |
| 布局 | `floorplan` | 布图规划的目标和术语，切分和非切分布图，波兰表达式、序列对 |
|  | `floorplan-algos` | 布图规划算法（尺寸优化、聚类生长、模拟退火），引脚分配，电源和地线网络 |
|  | `placement-objectives` | 布局的目标：线长估计（HPWL、Steiner 树）、密度、时序 |
|  | `global-placement` | 全局布局：最小割布局、二次布局解线性方程组（综合练习 4）、力导向、模拟退火 |
|  | `legalization` | 合法化和详细布局 |
| 布线 | `global-routing-basics` | 全局布线的术语、目标、布线区域的表示（网格图、通道）和流程 |
|  | `single-net` | 单线网布线：迷宫布线（Lee，综合练习 5）、A* 搜索、直角 Steiner 树 |
|  | `full-netlist` | 全网表布线：拆线重布、协商拥塞、整数线性规划，现代全局布线器 |
|  | `channel-routing` | 详细布线术语，水平和垂直约束图，左边算法和狗腿布线 |
|  | `switchbox-otc` | 开关盒布线、单元上方和 gcell 布线、现代详细布线的难点 |
|  | `special-routing` | 区域布线、非曼哈顿布线、时钟布线（均值中值法、零偏斜的 DME）和现代时钟树综合 |
| 静态时序分析 | `sta-algorithms` | 时序收敛的问题，按拓扑序算到达时间、要求时间和松弛量（综合练习 6），延迟模型 |
|  | `timing-driven` | 时序驱动布局和布线、物理综合（门尺寸、插缓冲器）、性能驱动的设计流程 |
| 电路仿真算法 | `logic-sim` | 逻辑仿真：编译式和事件驱动仿真 |
|  | `circuit-sim` | 电路仿真：改进节点分析、牛顿–拉夫逊迭代（综合练习 7）、数值积分 |
| 物理验证 | `drc` | 版图层和设计规则，DRC 的宽度、间距、包围、交叠检查，图层布尔运算，规则文件（综合练习 8） |
|  | `lvs` | LVS：器件提取、连接关系、网表比较、器件类别、网表微调（综合练习 8） |

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Electronic Design Automation | `eda-intro` |
| 1.2 | VLSI Design Flow | `eda-intro` |
| 1.3 | VLSI Design Style | `eda-intro` |
| 1.4 | Layout Layers and Design Rules | `drc` |
| 1.5 | Physical Design Optimization | `eda-intro` |
| 1.6 | Algorithms and Complexity | `complexity-graphs` |
| 1.7 | Graph Theory Terminology | `complexity-graphs` |
| 1.8 | Common EDA Terminology | `complexity-graphs` |
| 2.1 | Introduction | `partition-goals` |
| 2.2 | Terminology | `partition-goals` |
| 2.3 | Optimization Goals | `partition-goals` |
| 2.4 | Partitioning Algorithms | `kl-fm` |
| 2.5 | A Framework for Multilevel Partitioning | `multilevel-partition` |
| 3.1 | Introduction to Floorplanning | `floorplan` |
| 3.2 | Optimization Goals in Floorplanning | `floorplan` |
| 3.3 | Terminology | `floorplan` |
| 3.4 | Floorplan Representations | `floorplan` |
| 3.5 | Floorplanning Algorithms | `floorplan-algos` |
| 3.6 | Pin Assignment | `floorplan-algos` |
| 3.7 | Power and Ground Routing | `floorplan-algos` |
| 4.1 | Introduction | `placement-objectives` |
| 4.2 | Optimization Objectives | `placement-objectives` |
| 4.3 | Global Placement | `global-placement` |
| 4.4 | Legalization and Detailed Placement | `legalization` |
| 5.1 | Introduction | `global-routing-basics` |
| 5.2 | Terminology and Definitions | `global-routing-basics` |
| 5.3 | Optimization Goals | `global-routing-basics` |
| 5.4 | Representations of Routing Regions | `global-routing-basics` |
| 5.5 | The Global Routing Flow | `global-routing-basics` |
| 5.6 | Single-Net Routing | `single-net` |
| 5.7 | Full-Netlist Routing | `full-netlist` |
| 5.8 | Modern Global Routing | `full-netlist` |
| 6.1 | Terminology | `channel-routing` |
| 6.2 | Horizontal and Vertical Constraint Graphs | `channel-routing` |
| 6.3 | Channel Routing Algorithms | `channel-routing` |
| 6.4 | Switchbox Routing | `switchbox-otc` |
| 6.5 | Over-the-Cell and Gcell Routing Algorithms | `switchbox-otc` |
| 6.6 | Modern Challenges in Detailed Routing | `switchbox-otc` |
| 7.1 | Area Routing | `special-routing` |
| 7.2 | Non-Manhattan Routing | `special-routing` |
| 7.3 | Clock Routing | `special-routing` |
| 7.4 | Modern Clock Tree Synthesis | `special-routing` |
| 8.1 | Introduction | `sta-algorithms` |
| 8.2 | Timing Analysis and Performance Constraints | `sta-algorithms` |
| 8.3 | Timing-Driven Placement | `timing-driven` |
| 8.4 | Timing-Driven Routing | `timing-driven` |
| 8.5 | Physical Synthesis | `timing-driven` |
| 8.6 | Performance-Driven Design Flow | `timing-driven` |
| 8.7 | Conclusions | `timing-driven` |
| 9 | Logic Synthesis in a Nutshell | `two-level`、`bdd-sat`、`multilevel`、`tech-mapping` |
| 10 | Logic and Circuit Simulation | `logic-sim`、`circuit-sim` |
| 11.1 | Design Rule Checks (DRC) Basics | `drc` |
| 11.2 | DRC Runsets | `drc` |
| 12.1 | Layout vs. Schematic (LVS) Overview | `lvs` |
| 12.2 | LVS Introduction | `lvs` |
| 12.3 | LVS Devices | `lvs` |
| 12.4 | LVS Device Classes | `lvs` |
| 12.5 | LVS Device Extractors | `lvs` |
| 12.6 | LVS Input/Output | `lvs` |
| 12.7 | LVS Connectivity | `lvs` |
| 12.8 | LVS Compare | `lvs` |
| 12.9 | LVS Netlist Tweaks | `lvs` |

## CS2023 核心主题（C2）

`scope.json` 没有给 H.2.8 匹配 CS2023 主题，只注明 CE2016 要求会用综合与设计工具（CE-DIG-2、CE-DIG-10）、不讲工具内部的算法。本站用到的算法基础（图搜索、动态规划、NP 难与启发式）来自必须前置 F.1.2。

## 学习资源的章节（C3）

已逐条核对：

| 资源的小节 | 去处 |
|---|---|
| 三江学院《数字集成电路设计》第 2 章：设计规则检查、电路规则检查、版图寄生参数提取 | `drc`（DRC，电路规则检查 ERC 一句话讲到查什么）、`sta-algorithms`（寄生参数提取和 SPEF、SDF 文件） |
| 第 3 章：布图规划和布局、电源规划、布局、扫描链重组 | `floorplan`、`floorplan-algos`（电源环、电源网格、IR 压降）、`global-placement`、`legalization`（扫描链重组） |
| 第 5 章：全局布线、详细布线、特殊布线、布线算法 | `global-routing-basics` 到 `special-routing` 六课 |
| 第 6 章：延迟计算、寄生参数和延迟格式、静态时序分析、时序优化 | `sta-algorithms`、`timing-driven` |
| 第 10 章：物理验证与芯片组装 | `drc`、`lvs`；芯片组装（封装、焊盘环）只在 `floorplan-algos` 的引脚分配里提到输入输出焊盘，不展开，属于 H.2.4 的后端流程 |
| 第 3.6、3.7、5.5、5.6、6.7 节的 DC、Innovus、ICC、PT 实训 | 不教：具体商业工具的操作，不是算法内容 |
| ShanghaiTech Week 3（BDD、SAT） | `bdd-sat` |
| Week 7（技术映射） | `tech-mapping` |
| Week 8（布局） | `placement-objectives`、`global-placement`、`legalization` |
| Week 13（布线） | `global-routing-basics`、`single-net`、`full-netlist`、`channel-routing` |
| Week 15（静态时序分析） | `sta-algorithms` |
| KLayout 手册 DRC Basics、LVS Introduction | `drc`（图层读入、宽度检查、布尔运算、报告和豁免）、`lvs`（器件提取、connect、schematic、netlist.simplify、compare） |

## 综合练习（C4）

| 小题 | 负责的课 |
|---|---|
| (1) 两级最小化，最简式是否唯一 | `two-level` |
| (2) 技术映射的树覆盖动态规划 | `tech-mapping` |
| (3) 割边数和 KL 交换增益 | `partition-goals`、`kl-fm` |
| (4) HPWL，二次布局 | `placement-objectives`、`global-placement` |
| (5) Lee 迷宫布线 | `single-net` |
| (6) 到达时间、松弛量、关键路径 | `sta-algorithms` |
| (7) 二极管电路的牛顿–拉夫逊迭代 | `circuit-sim` |
| (8) DRC 和 LVS | `drc`、`lvs` |

## 后继技能用到的（C5）

H.2.8 没有直接解锁的技能，是集成电路设计远征的一站（远征终点 H.2.4 把它列为 also）。
