# H.1.2 数字电路与数字逻辑：覆盖表

**状态（2026-11-18）：已写完（46/46 节全覆盖，v2 零基础 + Icarus Verilog / Python 实测验证）。** 依据 `../cs-math-skill-tree/data/outlines/H.1.2.json`、`output/outlines.json`、`../cs-math-skill-tree/data/curation/learning-paths/H.1.2.json`，主来源为 MIT 6.004 Computation Structures（模块 2–7），辅以中文数字逻辑教材与野火 FPGA 时序分析文档，对齐 `H.1.2` 综合练习 5 问，本地核对脚本 `tests/content/H.1.2.verify.py`（Python 布尔真值表穷举 + Mealy 重叠序列穷举 + `fractions.Fraction` 精确时序 + WSL Icarus Verilog 12.0 真仿真实测）。

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Concrete Encoding of Information | `signals` |
| 1.2 | Analog Signaling | `signals` |
| 1.3 | Using Voltages Digitally | `signals` |
| 1.4 | Combinational Devices | `signals` |
| 1.5 | Dealing with Noise | `vtc` |
| 1.6 | Voltage Transfer Characteristic | `vtc` |
| 1.7 | VTC Example | `vtc` |
| 1.8 | Worked Examples | `vtc` |
| 2.1 | MOSFET: Physical View | `mos` |
| 2.2 | MOSFET: Electrical View | `mos` |
| 2.3 | CMOS Recipe | `mos` |
| 2.4 | Beyond Inverters | `cmos` |
| 2.5 | CMOS Gates | `cmos` |
| 2.6 | CMOS Timing | `gate-delay` |
| 2.7 | Lenient Gates | `gate-delay` |
| 2.8 | Worked Examples | `cmos` |
| 3.1 | Sum of Products | `truth` |
| 3.2 | Useful Logic Gates | `truth` |
| 3.3 | Inverting Logic | `kmap` |
| 3.4 | Logic Simplification | `kmap` |
| 3.5 | Karnaugh Maps | `kmap` |
| 3.6 | Multiplexers | `mux-rom` |
| 3.7 | Read-only Memories | `mux-rom` |
| 3.8 | Worked Examples | `adder` |
| 4.1 | Digital State | `registers` |
| 4.2 | D Latch | `registers` |
| 4.3 | D Register | `registers` |
| 4.4 | D Register Timing | `timing` |
| 4.5 | Sequential Circuit Timing | `timing` |
| 4.6 | Timing Example | `timing` |
| 4.7 | WE5.1 | `timing` |
| 4.8 | WE5.2 | `timing` |
| 5.1 | Finite State Machines | `fsm` |
| 5.2 | State Transition Diagrams | `fsm` |
| 5.3 | FSM States | `fsm` |
| 5.4 | Roboant Example | `fsm-design` |
| 5.5 | Equivalent States; Implementation | `fsm-design` |
| 5.6 | Synchronization and Metastability | `sync` |
| 5.7 | Worked Examples | `fsm` |
| 6.1 | Latency and Throughput | `pipeline` |
| 6.2 | Pipelined Circuits | `pipeline` |
| 6.3 | Pipelining Methodology | `pipeline` |
| 6.4 | Circuit Interleaving | `self-time` |
| 6.5 | Self-timed Circuits | `self-time` |
| 6.6 | Control Structures | `self-time` |
| 6.7 | Worked Examples | `pipeline` |

## CS2023 核心主题（C2）

`../cs-math-skill-tree/data/curation/scope.json` 为 `H.1.2` 匹配的 **5 项** CS2023 核心主题全部落课（对应 `布尔代数`、`组合/时序逻辑`、`状态机`、`时钟`、`时序与逻辑实现` 5 章，共覆盖大纲 `46/46` 节）：

| 知识点 | KA / 要求 | 课 |
|---|---|---|
| 布尔代数 | SF-Foundations / CS Core：Boolean logic simplification | `signals`、`vtc`、`truth`、`kmap` |
| 组合/时序逻辑 | SF-Foundations / CS Core：Combinational Logic, Sequential Logic | `mos`、`cmos`、`mux-rom`、`adder`、`registers` |
| 状态机 | SF-Foundations / CS Core：Finite state machines | `fsm`、`fsm-design` |
| 时钟 | SF-Foundations / CS Core：Clocks, State, Sequencing | `sync`、`timing` |
| 时序与逻辑实现 | AR-Logic / KA Core：Gate delays | `gate-delay`、`pipeline`、`self-time` |

## 综合练习与前置/后继映射（C3 / C4 / C5）

- **综合练习 5 问映射（C4）**：
  - 第 (1) 问卡诺图化简 $F(A, B, C) = \sum m(1, 3, 5, 6, 7) = C + AB$ → `kmap`。
  - 第 (2) 问仅用 3 只与非门（NAND）实现 $C + AB$（并经 Icarus Verilog 全 8 种输入仿真验真） → `kmap`。
  - 第 (3) 问全加器逻辑式 $S = A \oplus B \oplus C_{in}$、$C_{out} = AB + C_{in}(A \oplus B)$、4 位行波最长进位路径与超前进位（$G_i, P_i$）提速 → `adder`。
  - 第 (4) 问 D 锁存器（电平透明）与 D 触发器（边沿采样）区别，及允许重叠检测序列 `101` 的 Mealy 状态机转移表（`S0 / S1 / S2`） → `registers`、`fsm`。
  - 第 (5) 问建立时间（$t_{setup}$）与保持时间（$t_{hold}$）定义，及简化无偏斜模型下 $T_{min} = 1 + 5 + 0.5 = 6.5\text{ ns}$、$f_{max} \approx 154\text{ MHz}$（约 `153.85 MHz`）计算 → `timing`。
- **前后继状态（C3 / C5）**：
  - `H.1.2` 无必须前置（推荐前置仅为 `P.1.1`，本包零基础定义所有数字电路、VTC/CMOS/时序符号并在演示代码块旁附最小门级读法说明，不假设先修过任何前置）。
  - 下游必须后继（`unlocks`）为 `C.1.2 计算机体系结构`、`H.2.1 数字集成电路与 FPGA 设计` 与 `H.2.4 数字芯片物理与后端`（并被 `C.1.1`、`H.3.1` 列为推荐前置；互相关联 `H.1.1`）。本包在组合/时序延迟模型、同步寄存器与流水线节拍概念上为 `C.1.2` 和 `H.2.1` 提供了直接衔接（C5 无缺口）。
