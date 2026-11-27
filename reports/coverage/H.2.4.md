# H.2.4 VLSI与芯片设计：覆盖表

**状态（2026-11-26）：32 课已写完并按两份通读报告修改（第 10 轮），check-coverage 63/63 节，verify.py 277 项，FULL e2e 32 课通过。** 依据 `../cs-math-skill-tree/data/outlines/H.2.4.json`（主来源 MIT 6.374 *Analysis and Design of Digital Integrated Circuits* 逐讲大纲，物理设计和时序分析由 UMBC CMPE 691 补齐）、学习资源（东南大学《VLSI 设计基础》、东北大学《集成电路测试与验证》、一生一芯 E8/D6、Rutenbar VLSI CAD Part I/II、OpenLane PDK 文档）和原技能树综合练习。数值核对脚本将是 `tests/content/H.2.4.verify.py`。

前置：必须前置 H.1.2 数字电路与数字逻辑、H.2.5 半导体器件与微电子基础（已有包，MOSFET 的三个区和平方律、阈值电压、CMOS 反相器和静态 CMOS 门、传播延迟 $t_p \approx C_LV_{DD}/(2I)$、动态功耗 $C_LV_{DD}^2f$、噪声容限、上拉/下拉网络、速度饱和、按比例缩小、设计规则、DRC/LVS/静态时序分析都能直接用，说法和数值要和 H.2.5 一致）。写课前先 `node temp/closure-terms.mjs H.2.4` 看 H.1.2 讲过的锁存器、触发器、建立和保持时间等术语。

## 课的安排（32 课）

| 章 | 课 | 内容 |
|---|---|---|
| CMOS 数字设计 | `inverter-dc` | 亚微米 MOS 模型（速度饱和、统一模型 $I_D = k'\frac WL(V_{ov}V_{min} - V_{min}^2/2)(1 + \lambda V_{DS})$），反相器电压传输特性参数 $V_M$、噪声容限 |
|  | `inverter-delay` | 传播延迟 $t_p = 0.69R_{eq}C_L$，等效电阻，寄生电容估算（栅、扩散、连线、密勒） |
|  | `voltage-scaling` | 电源电压和阈值电压对延迟和能量的影响，能量–延迟积 |
|  | `static-cmos` | 静态 CMOS 复合门（AOI、OAI）、上拉下拉对偶、管子尺寸、扇入扇出对延迟的影响 |
|  | `ratioed-logic` | 有比逻辑：伪 NMOS，$V_{OL}$ 与静态功耗 |
|  | `pass-transistor` | 传输管和传输门逻辑（阈值损失、电平恢复），差分级联电压开关逻辑 DCVSL |
|  | `dynamic-logic` | 动态逻辑：预充–求值、多米诺、电荷分享、漏电和噪声 |
|  | `adders` | 加法器（行波进位、超前进位、进位选择）、乘法器、移位器 |
|  | `datapath-design` | 数据通路的设计方法学和位片版图映射 |
|  | `latches-registers` | 时序元件的分类和参数（建立时间、保持时间、时钟到输出延迟），静态锁存器和寄存器（主从结构） |
|  | `dynamic-registers` | 竞争冒险（时钟重叠），动态锁存器和寄存器（C²MOS），两相与单相时钟 |
|  | `pulse-registers` | 脉冲型寄存器，锁存器系统与寄存器系统（借时间），亚稳态和同步器的平均无故障时间 |
| 标准单元 | `cell-layout` | 反相器和逻辑门的版图、棍图、欧拉路径，标准单元的固定高度和电源轨 |
|  | `cell-library` | 单元库的视图（LEF、GDS、Liberty 时序表）和用 SPICE 表征单元（延迟随输入转换时间和负载变化） |
| 时序/功耗/面积 | `power-components` | 能量和功耗的组成：开关功耗 $\alpha CV^2f$、短路功耗、漏电功耗 |
|  | `dynamic-power-reduction` | 翻转活动因子、毛刺、门控时钟、逻辑和结构层面降低翻转 |
|  | `leakage-power` | 漏电功耗：亚阈值、栅极漏电，多阈值单元、电源门控 |
|  | `logical-effort` | 逻辑努力：$d = gh + p$，路径努力，最优级数和每级努力约 4 |
|  | `interconnect` | 互连电容估算（平板加边缘），连线电阻和 Elmore 延迟 |
|  | `buffer-chains` | 驱动大负载的缓冲器链、最优锥形比，低摆幅驱动 |
|  | `power-distribution` | 电源网络：IR 压降、$L\,di/dt$、去耦电容 |
|  | `clock-skew-jitter` | 时钟偏斜和抖动对建立、保持的影响，来源 |
|  | `clock-distribution` | H 树、时钟网格、锁相环和延迟锁相环，自定时电路 |
| 逻辑综合与布局布线 | `design-flow` | 电子设计工具和从 RTL 到 GDS 的自动化物理设计流程，FPGA 厂商在 EDA 中的角色 |
|  | `synthesis-mapping` | 逻辑综合、工艺映射（覆盖）、打包 |
|  | `place-route` | 布局（划分、模拟退火、解析布局）和布线（迷宫布线） |
|  | `timing-verification` | 时序验证与逻辑验证，布局布线后仿真，动态时序分析（事件驱动仿真）与静态时序分析的比较 |
|  | `sta-setup` | 静态时序分析、时钟周期约束、建立时间和保持时间、关键路径的建立裕量 |
|  | `skew-hold` | 时钟偏斜对建立和保持的影响，保持时间分析和裕量 |
|  | `timing-exceptions` | 未约束路径、跨时钟域信号和同步，多周期路径，伪路径 |
| 芯片测试 | `fault-models` | 缺陷和故障模型（固定型故障），路径敏化，测试向量生成 |
|  | `scan-bist` | 扫描链、内建自测试、IDDQ 测试 |

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | MOS Device Model with Sub-micron Effects | `inverter-dc` |
| 1.2 | VTC Parameters - DC Characteristics | `inverter-dc` |
| 2.1 | CMOS Propagation Delay | `inverter-delay` |
| 2.2 | Parasitic Capacitance Estimation | `inverter-delay` |
| 2.3 | Layout of an Inverter | `cell-layout` |
| 2.4 | Supply and Threshold Voltage Scaling | `voltage-scaling` |
| 2.5 | SPICE Simulation Techniques | `cell-library` |
| 3.1 | Components of Energy and Power | `power-components` |
| 3.2 | Switching, Short-Circuit and Leakage Components | `power-components` |
| 3.3 | SPICE Simulation Techniques | `cell-library` |
| 4.1 | Static CMOS Construction | `static-cmos` |
| 4.2 | Ratioed Logic | `ratioed-logic` |
| 5.1 | Pass Transistor / Transmission Gate Logic | `pass-transistor` |
| 5.2 | DCVSL | `pass-transistor` |
| 5.3 | Introduction to Dynamic Logic | `dynamic-logic` |
| 6.1 | Dynamic Logic Design Considerations | `dynamic-logic` |
| 6.2 | Power Dissipation in CMOS | `power-components` |
| 7.1 | Power Consumption in CMOS Logic (cont.) | `dynamic-power-reduction` |
| 7.2 | Leakage Power Dissipation | `leakage-power` |
| 7.3 | Logical Effort Sizing - Performance Optimization of Digital Circuits | `logical-effort` |
| 8.1 | Adders, Multipliers, Shifters | `adders` |
| 8.2 | Design Methodology | `datapath-design` |
| 8.3 | Layout Techniques and Mapping | `datapath-design` |
| 9.1 | Classification / Parameters | `latches-registers` |
| 9.2 | Static Latches and Register | `latches-registers` |
| 10.1 | Race Condition | `dynamic-registers` |
| 10.2 | Dynamic Latches and Registers | `dynamic-registers` |
| 10.3 | Two Phase vs. Single Phase | `dynamic-registers` |
| 11.1 | Pulse Based Registers | `pulse-registers` |
| 11.2 | Latch vs. Register Systems | `pulse-registers` |
| 11.3 | Metastability | `pulse-registers` |
| 12.1 | Capacitance Estimation | `interconnect` |
| 12.2 | Buffer Chains | `buffer-chains` |
| 12.3 | Low Swing Drivers | `buffer-chains` |
| 12.4 | Power Distribution | `power-distribution` |
| 13.1 | Issues in Timing - Impact of Clock Skew and Jitter | `clock-skew-jitter` |
| 14.1 | Origins of Clock Skew / Jitter and Impact on Performance | `clock-skew-jitter` |
| 14.2 | Clock Distribution Techniques | `clock-distribution` |
| 14.3 | Self-timed Circuits | `clock-distribution` |
| 15.1 | Power Reduction Through Switching Activity Reduction | `dynamic-power-reduction` |
| 15.2 | Defects, Fault Models, Path Sensitization | `fault-models` |
| 15.3 | Scan, Built-in-self Test, IDDQ | `scan-bist` |
| 16.1 | Electronic Design Tools | `design-flow` |
| 16.2 | Automated Physical Design | `design-flow` |
| 16.3 | Synthesis and Mapping | `synthesis-mapping` |
| 16.4 | Packing | `synthesis-mapping` |
| 16.5 | Place and Route | `place-route` |
| 16.6 | Timing Verification vs Logical Verification | `timing-verification` |
| 16.7 | Timing Analysis and Post-Place-and-Route simulation | `timing-verification` |
| 16.8 | Static Timing Analysis | `sta-setup` |
| 16.9 | Clock Period Constraint | `sta-setup` |
| 16.10 | Setup and Hold Times | `sta-setup` |
| 16.11 | Clock Skew | `skew-hold` |
| 16.12 | Setup Timing Slack in Critical Path | `sta-setup` |
| 16.13 | Hold Time Analysis and Slack | `skew-hold` |
| 16.14 | Unconstrained Paths and CDC Clock Domain Crossing | `timing-exceptions` |
| 16.15 | Clock Domain Crossing (CDC) Signals | `timing-exceptions` |
| 16.16 | Multicycle Paths | `timing-exceptions` |
| 16.17 | False Paths | `timing-exceptions` |
| 16.18 | Dynamic Timing Analysis | `timing-verification` |
| 16.19 | Dynamic Timing Analysis using Event-Driven Simulation | `timing-verification` |
| 16.20 | Dynamic vs Static Timing Analysis; Functional vs Timing Verification | `timing-verification` |
| 16.21 | FPGA vendors role in EDA | `design-flow` |

## CS2023 核心主题（C2）

`scope.json` 只给“时序/功耗/面积”匹配了 AR-Logic（KA Core）的 Energy/power：`power-components`（开关、短路、漏电三部分，活动因子，DVFS）、`dynamic-power-reduction`（毛刺、门控时钟、编码）、`leakage-power`（亚阈值和栅极漏电、多阈值、电源门控）。

## 学习资源的章节（C3）

- 东南大学第二章 MOS 器件：`inverter-dc`（速度饱和的统一模型）；器件物理本身属于 H.2.5。
- 第三章反相器和组合逻辑：`inverter-dc`、`inverter-delay`、`voltage-scaling`、`static-cmos`、`ratioed-logic`、`pass-transistor`、`dynamic-logic`、`adders`。
- 第四章时序逻辑：`latches-registers`、`dynamic-registers`、`pulse-registers`。
- 第五章单元库设计技术：`cell-layout`、`cell-library`。IO 单元只讲到布图规划时四周留出输入输出单元的位置（`design-flow`），IO 电路本身（ESD 保护、输出驱动）大纲没有这一节，不教。
- 东北大学：故障建模、ATPG（`fault-models`），扫描、BIST（`scan-bist`）；故障仿真只讲到“测试向量能发现哪些故障、故障覆盖率”的层面（`fault-models` 的覆盖率和缺陷水平），并行故障仿真等算法不教。
- 一生一芯 E8/D6：`design-flow`（RTL 到 GDS 的流程、布图规划、时钟树综合、签核）、`place-route`、`sta-setup`、`skew-hold`。
- Rutenbar Part I：两级和多级逻辑优化（`synthesis-mapping`）；BDD 和布尔函数的表示算法属于推荐后继 H.2.8 EDA 算法，这里不教。Part II：工艺映射（`synthesis-mapping`）、布局（划分、模拟退火、解析布局，`place-route`）、迷宫布线（`place-route`）、时序评估（`sta-setup`）。
- OpenLane PDK 配置：单元库的 LEF、GDS、Liberty 和布线网格（`cell-library`）。

原计划写的核对范围：东南大学第二到第五章（MOS 器件、反相器和组合逻辑、时序逻辑、单元库设计技术，含 IO 单元）、东北大学的故障建模、故障仿真、ATPG、扫描、BIST，一生一芯 E8/D6 的 RTL 到可流片版图流程，Rutenbar Part I（布尔函数、BDD、两级和多级逻辑综合）和 Part II（工艺映射、布局、布线、时序评估），OpenLane 的标准单元库视图。存储器（ROM、SRAM、DRAM）和电压调节不在本技能的知识点里（大纲 omitted 已写明）。

## 综合练习（C4）

| 小题 | 负责的课 |
|---|---|
| (1) 反相器原理、二输入与非门的上拉和下拉、静态 CMOS 几乎没有静态功耗 | H.2.5 的反相器和静态 CMOS 门；`static-cmos`（复合门的上拉下拉对偶）；`power-components`（三部分功耗，静态时只有漏电） |
| (2) $P = \alpha CV^2f$ 算 0.1 W，降到 0.8 V 降低 36%，为什么降压还要降频 | `power-components`（`pdyn-exercise`、`pdyn-08v`、`dvfs-why`） |
| (3) 物理设计流程 | `design-flow`（`flow-order`） |
| (4) 建立和保持违例怎样修，偏斜对两者的影响 | `clock-skew-jitter`、`skew-hold`（`hold-buffers`、`skew-tradeoff`），结业 `b-hold-how` |
| (5) 可测性设计、扫描链和 ATPG 怎样检测固定型故障 | `fault-models`（路径敏化、`test-b-sa1`）、`scan-bist`（扫描链、`scan-why`） |

## 后继技能用到的（C5）

H.2.4 没有直接解锁的技能；它是集成电路设计远征的终点。H.2.8 EDA 算法把它列为推荐前置，会用到综合、布局、布线、静态时序分析的概念：第 4 章（`design-flow` 到 `timing-exceptions`）都讲到了，算法细节留给 H.2.8。
