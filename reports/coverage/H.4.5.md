# H.4.5 PLC与工业自动化：覆盖表

**状态（2026-11-23）：已写完，19 课，等用户验收。** 依据 `../cs-math-skill-tree/data/outlines/H.4.5.json`（主来源 W. Bolton《Programmable Logic Controllers》第 6 版第 1、2、4–7、9、10、13 章，大纲 10 章 45 节；补充 Petruzella 第 14 章）、`data/curation/learning-paths/H.4.5.json`（江苏开放大学《可编程控制器应用技术》、常州工程职业技术学院《可编程控制器技术应用》（三菱 FX3U）、北京信息职业技术学院《工业控制网络与现场总线》；control.com《Lessons In Industrial Automation》第 4 章和数字数据采集与网络一章）和原技能树综合练习 8 小题。数值核对脚本 `tests/content/H.4.5.verify.py`。

前置：必须前置 H.1.1（电压、电流、欧姆定律、基尔霍夫定律、ADC）和 H.1.2（二进制、布尔代数、组合逻辑、锁存器、触发器、寄存器、有限状态机），往下是微积分和线性代数。程序设计不是前置：`data/jargon.yaml` 里的指令、地址、内存、中断、字节、循环、分支等词在第一次用到时现讲（指令和内存在 `plc-hardware`，地址在 `plc-hardware`，循环扫描在 `scan-cycle`，中断在 `scan-cycle`，字节在 `plc-hardware`，分支在 `sfc`）。继电器和常开、常闭触点在 `what-is-plc` 讲，接触器在 `what-is-plc` 先用一句话说明、在 `output-devices` 细讲，高速计数器在 `scan-cycle`，上升沿在 `timers`，变量和函数在 `iec-languages`；变频器只讲它在接线上是什么（电机调速见 E.3.2，它只是推荐前置）。

## 课的安排

| 课 | 章 | 内容 |
|---|---|---|
| `what-is-plc` | PLC硬件结构与扫描周期 | 继电器控制和 PLC 的区别、PLC 的由来、整体式和模块式、PLC 系统的规模 |
| `plc-hardware` | PLC硬件结构与扫描周期 | 电源、CPU、存储器、输入输出模块、通信口；内部结构和存储区（输入映像、输出映像、内部位、定时器计数器、数据区）；位、字节、字；输入输出地址 |
| `scan-cycle` | PLC硬件结构与扫描周期 | 循环扫描的三个阶段、过程映像、扫描时间和响应时间、短脉冲会被漏掉、中断输入和高速计数器（综合练习 1） |
| `input-devices` | 传感器与执行器接线 | 按钮、限位开关、接近开关（电感式、电容式、光电式）、编码器、温度传感器、变送器；应用举例 |
| `output-devices` | 传感器与执行器接线 | 继电器、接触器、电磁阀、电动机、变频器；继电器、晶体管、晶闸管三种输出 |
| `io-wiring` | 传感器与执行器接线 | 24 V 直流输入回路、光耦隔离和输入滤波、NPN 和 PNP 传感器、漏型和源型接法（综合练习 6） |
| `analog-signals` | 传感器与执行器接线 | 4–20 mA 电流信号、活零点和断线检测、模拟量的量程换算、分辨率 |
| `ladder-basics` | 梯形图与IEC 61131-3语言 | 梯形图的母线、触点、线圈和梯级；与、或、非、异或；程序的编写和下载 |
| `latching` | 梯形图与IEC 61131-3语言 | 启保停（自锁）、停止按钮接常闭、多个输出、内部继电器、置位和复位、编程举例（综合练习 2） |
| `iec-languages` | 梯形图与IEC 61131-3语言 | IEC 61131-3 的五种语言、变量和数据类型、功能块、指令表、结构化文本 |
| `timers` | 定时器与计数器 | 定时器的种类、接通延时（TON）、断开延时（TOF）、时基和预设值（综合练习 3） |
| `timers-advanced` | 定时器与计数器 | 脉冲定时器（TP）、保持型定时器（TONR）、闪烁电路、星三角起动的时序 |
| `counters` | 定时器与计数器 | 加计数器、减计数器、加减计数器、上升沿和单次脉冲、定时器和计数器组合（综合练习 4） |
| `sfc` | 顺序控制 | 顺序功能图的步、转移、动作、初始步；单序列、选择分支、并行分支（综合练习 5） |
| `sequence-to-ladder` | 顺序控制 | 用置位复位把顺序功能图写成梯形图、步进指令、顺序器指令、程序开发的步骤 |
| `fieldbus` | 工业现场总线 | 远程 I/O、RS-485、Modbus RTU 的帧和功能码、PROFIBUS、PROFINET 和 EtherCAT、HART（综合练习 7） |
| `hmi-scada` | HMI与SCADA | HMI 的画面、变量和报警；SCADA 的组成（RTU、通信、主站、历史数据库）；数据采集；SCADA 和 DCS（综合练习 8 前半） |
| `safety` | 安全联锁 | 故障安全原则、急停必须硬接线、安全继电器、正反转互锁、主控继电器、功能安全标准（综合练习 8 后半） |
| `commissioning` | 安全联锁 | 调试、故障查找、系统文档 |

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Controllers | `what-is-plc` |
| 1.2 | Hardware | `plc-hardware` |
| 1.3 | PLC Architecture | `plc-hardware` |
| 1.4 | PLC Systems | `what-is-plc` |
| 1.5 | Programs | `scan-cycle`、`ladder-basics` |
| 2.1 | Input Devices | `input-devices` |
| 2.2 | Output Devices | `output-devices` |
| 2.3 | Examples of Applications | `input-devices` |
| 3.1 | Input/Output Units | `output-devices`、`io-wiring` |
| 3.2 | Signal Conditioning | `io-wiring`、`analog-signals` |
| 3.3 | Remote Connections | `fieldbus` |
| 3.4 | Networks | `fieldbus` |
| 3.5 | Processing Inputs | `scan-cycle` |
| 3.6 | I/O Addresses | `plc-hardware` |
| 4.1 | Ladder Diagrams | `ladder-basics` |
| 4.2 | Logic Functions | `ladder-basics` |
| 4.3 | Latching | `latching` |
| 4.4 | Multiple Outputs | `latching` |
| 4.5 | Entering Programs | `ladder-basics` |
| 4.6 | Function Blocks | `iec-languages` |
| 4.7 | Program Examples | `latching` |
| 5.1 | Instruction Lists | `iec-languages` |
| 5.2 | Sequential Function Charts | `sfc` |
| 5.3 | Structured Text | `iec-languages` |
| 6.1 | Internal Relays | `latching` |
| 6.2 | One-Shot Operation | `counters` |
| 6.3 | Set and Reset | `latching`、`sequence-to-ladder` |
| 6.4 | Master Control Relay | `safety` |
| 7.1 | Types of Timers | `timers` |
| 7.2 | On-Delay Timers | `timers` |
| 7.3 | Off-Delay Timers | `timers` |
| 7.4 | Pulse Timers | `timers-advanced` |
| 7.5 | Retentive Timers | `timers-advanced` |
| 7.6 | Programming Examples | `timers-advanced` |
| 8.1 | Forms of Counter | `counters` |
| 8.2 | Programming | `counters` |
| 8.3 | Up- and Down-Counting | `counters` |
| 8.4 | Timers with Counters | `counters` |
| 8.5 | Sequencer | `sequence-to-ladder` |
| 9.1 | Program Development | `sequence-to-ladder` |
| 9.2 | Safe Systems | `safety` |
| 9.3 | Commissioning | `commissioning` |
| 9.4 | Fault Finding | `commissioning` |
| 9.5 | System Documentation | `commissioning` |
| 10 | Process Control and Data Acquisition Systems | `hmi-scada` |

## 中文主课的章节（C3）

三门中文课列出的概念都在上表的课里，按机型讲的部分改成通用写法：

- 三菱 FX3U 的面板、步进顺控指令（STL）、西门子 S7-300 的定时器指令格式：`plc-hardware`、`sequence-to-ladder`、`timers` 用 IEC 61131-3 的写法讲，提到三菱和西门子各自的地址写法和步进指令的思路，不讲具体型号的操作。
- PROFIBUS DP、PROFINET 的组态实训，WinCC Flexible 的组态操作：`fieldbus`、`hmi-scada` 讲网络和画面要完成什么、帧和变量是什么，不讲软件操作步骤。
- PLC 和变频器的模拟量调速：`analog-signals` 讲 4–20 mA 和 0–10 V 信号的换算，`output-devices` 讲变频器怎样接到 PLC 上。

## CS2023 核心主题（C2）

`scope.json` 对 H.4.5 没有 CS2023 主题；8 个章由上表的课负责。

## 原技能树综合练习（C4）

| 小题 | 内容 | 由哪一课教到 |
|---|---|---|
| (1) | 扫描周期的三个阶段、短脉冲被漏掉、解决办法 | `scan-cycle` |
| (2) | 启保停梯形图和逻辑式、停止按钮接常闭 | `latching` |
| (3) | TON 的预设值、中途断开的结果、保持型定时器 | `timers`、`timers-advanced` |
| (4) | 加计数器装箱、复位的时机 | `counters` |
| (5) | 水箱灌装的顺序功能图 | `sfc` |
| (6) | NPN 传感器接哪种输入、电流的路径 | `io-wiring` |
| (7) | Modbus RTU 功能码 03 和帧结构、工业以太网的特点 | `fieldbus` |
| (8) | HMI 和 SCADA 的分工、急停不能只靠 PLC 程序 | `hmi-scada`、`safety` |

## 后继技能用到的写法（C5）

H.4.5 没有必须后继技能（直接解锁：无）。
