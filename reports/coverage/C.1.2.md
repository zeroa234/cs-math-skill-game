# C.1.2 计算机体系结构：覆盖表

**状态（2026-11-18）：已写完（47/47 节全覆盖，v2 零基础 + WSL SPIM 8.0 / Python 精确验算）。** 依据 `../cs-math-skill-tree/data/outlines/C.1.2.json`、`../cs-math-skill-tree/output/outlines.json`、`../cs-math-skill-tree/data/curation/learning-paths/C.1.2.json`，主来源为 ETH Zürich *Digital Design and Computer Architecture*（SAFARI, Spring 2024）与胡伟武《计算机体系结构基础》第 3 版，辅以 UC Berkeley CS 152/252A 与 MIT 6.823 分支/一致性/性能专题；对齐 `C.1.2` 综合练习 6 问（注：课程指令集以 MIPS 教基础结构与寻址，综合练习第 1 问按原题题干采用等价 RISC-V 五级流水线示例并清楚标明，不混淆编码）；本地核对脚本 `tests/content/C.1.2.verify.py`（Python `Fraction` 精确流水线/AMAT/分支预测/性能加速比验证 + WSL `spim` 8.0 真实执行 MIPS 汇编）。

## 大纲逐节（C1：47/47 节）

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Assembly Language | `isa` |
| 1.2 | Architecture Design Principles | `isa` |
| 1.3 | Where to store data (memory/register) | `isa` |
| 1.4 | Main types of MIPS instructions | `isa` |
| 2 | MIPS Assembly II | `isa` |
| 3.1 | Overview of the MIPS Microprocessor | `datapath` |
| 3.2 | RTL Design Revisited | `datapath` |
| 3.3 | Single-Cycle Processor | `datapath` |
| 3.4 | Performance Analysis | `datapath`、`cpu-time` |
| 4 | Single-Cycle Microarchitecture II | `datapath` |
| 5.1 | Pipelining | `overlap` |
| 5.2 | Single Cycle vs. Pipelined | `overlap` |
| 5.3 | Pipelined MIPS architecture | `overlap` |
| 5.4 | Hazards and how to solve them | `data-hazard` |
| 5.5 | Data hazards | `data-hazard` |
| 5.6 | Control hazards | `control` |
| 5.7 | Performance of the Pipelined architecture | `overlap`、`cpu-time` |
| 6 | Pipelined Processor Architecture II | `data-hazard`、`control` |
| 7.1 | Control & Data Dependence Handling | `out-of-order` |
| 7.2 | Precise Exceptions: State Maintenance & Recovery | `out-of-order` |
| 7.3 | Out-of-Order Execution | `out-of-order` |
| 7.4 | Issues in OoO Execution: Load-Store Handling | `out-of-order` |
| 8.1 | The Memory Hierarchy | `cache` |
| 8.2 | Cache Basics and Operation | `cache` |
| 8.3.1 | Cache Parameters vs. Miss/Hit Rate | `cache` |
| 8.3.2 | Classification of Cache Misses | `miss` |
| 8.3.3 | How to Improve Cache Performance | `miss` |
| 8.4.1 | Private vs. Shared Caches | `amat` |
| 8.4.2 | Resource Sharing vs. Partitioning | `amat` |
| 8.5.1 | The Cache Coherence Problem | `coherence` |
| 8.5.2 | Hardware Cache Coherence | `coherence` |
| 8.5.3 | Directory Based Coherence | `coherence` |
| 8.5.4 | Coherence: Update vs. Invalidate | `coherence` |
| 9.1 | Part 1: Multi-core issues in Caching | `amat` |
| 9.2 | Cache sharing/partitioning | `amat` |
| 9.3 | Brief intro to cache coherence | `coherence` |
| 10.1 | Virtual Memory | `virtual-memory` |
| 10.2.1 | Address Translation: Page Hit | `virtual-memory` |
| 10.2.2 | Address Translation: Page Fault | `virtual-memory` |
| 10.3 | Memory Protection | `virtual-memory` |
| 10.4 | Some Issues in Virtual Memory | `virtual-memory` |
| 10.5 | A Modern Example Virtual Memory System | `virtual-memory` |
| 10.6 | Virtual Memory Summary | `virtual-memory` |
| 11 | Branch Prediction 1 | `predict` |
| 12 | Branch Prediction 2 | `predict` |
| 13 | Memory Consistency | `ordering` |
| 14 | OoO Performance Engineering | `out-of-order`、`cpu-time`、`amdahl` |

## CS2023 核心主题（C2）

`../cs-math-skill-tree/data/curation/scope.json` 为 `C.1.2` 匹配的 **5 项** CS2023 核心主题全部覆盖落课（5/5）：

| 知识点 | KA / 要求 | 课 |
|---|---|---|
| 指令集 | AR-Assembly / KA Core：Instruction set architecture (ISA) | `isa`、`datapath` |
| 流水线 | AR-Organization / KA Core：Instruction pipelining | `overlap`、`data-hazard`、`control`、`out-of-order` |
| 缓存 | AR-Memory / CS Core：Cache memories | `cache`、`miss`、`amat`、`virtual-memory` |
| 多核一致性 | AR-Memory / CS Core：Multiprocessor cache coherence | `coherence`、`ordering` |
| 分支预测和性能模型 | AR-Performance-Energy / KA Core：Branch prediction | `predict`、`cpu-time`、`amdahl` |

## 学习路径参考资料与综合练习/后续衔接（C3 / C4 / C5）

- **参考资料映射（C3）**：`en1`（ETH DDCA L12–L26，主源）覆盖 MIPS ISA、单周期数据通路、五级流水线与冒险、乱序精确异常、Cache 层次/3C 缺失/写失效一致性与虚拟内存；`zh2`（胡伟武《计算机体系结构基础》第 3 版第 2/9/11/12 章，主源）补充中文处理器流水线与多核一致/性能剖析；`en2`（MIT 6.823 L13）覆盖动态分支预测；大纲补充源 B（UC Berkeley CS 152）覆盖分支预测（L12–L13）、内存一致性模型（L17）与乱序性能工程（L18）；`zh1`（华中科技大学《计算机系统结构》MOOC）作中文教学替代参考。
- **综合练习 6 问映射（C4）**：
  - 第 (1) 问 RISC-V 五级流水线 `lw x1, 0(x2); add x3, x1, x4; sub x5, x3, x6` 识别 `load-use` 数据冒险、旁路转发后仍停顿 `1` 个周期（`add→sub` 无停顿） → `data-hazard`、`boss`。
  - 第 (2) 问 $10^9$ 条指令在 `CPI=1.5 @ 2 GHz`（`0.75 s`）与 `CPI=1.2 @ 1.8 GHz`（约 `0.667 s`）下的执行时间与加速比 `1.125`（$9/8$） → `cpu-time`、`boss`。
  - 第 (3) 问 80% 可并行程序在 16 核下的 Amdahl 加速比 `4`（`amdahl-16core-c4`、`boss-amdahl-c4`）与核数趋无穷理论极限 `5`（`amdahl-inf-limit-c4` 单独计分验证） → `amdahl`、`boss`。
  - 第 (4) 问 L1（1 周期 / 5% / 100 周期）单级 `AMAT = 6` 周期（`amat-l1-only-c4` 单独计分验证），加入 L2（10 周期 / 局部缺失率 20% / 主存 100 周期）后降至 `AMAT = 2.5` 周期（`amat-with-l2-c4`、`boss-amat-l2-c4`） → `amat`、`boss`。
  - 第 (5) 问 MSI 协议下 `S/S` 双核由核 1 写入后的状态演化（`M/I`）及伪共享原因（同 cache 行不同字节反复失效搬运）与填充/对齐解法 → `coherence`、`boss`。
  - 第 (6) 问初始强跳转（`11`）的 2 位饱和计数器在 `T T T N` 循环分支上的稳态命中率 `75%`（每 4 次错 1 次） → `predict`、`boss`。
- **前后继状态（C5）**：必须前置为 `C.1.1`（数字基础/单周期数据通路基础）与 `H.1.2`（数字逻辑、寄存器、状态机与时序），推荐前置 `P.2.2`。虽无强制 `unlocks` 边，但作为 `F.1.5`、`C.1.3`、`C.1.4`、`C.2.1`、`C.5.1`、`C.5.2` 共同推荐前置，本包中的虚拟页/TLB 翻译为 `C.2.1`、Cache 行对齐与局部性为 `F.1.5`/`C.1.3`、多核一致与内存序为 `C.1.4`/`C.5.1` 提供直接铺垫（C5 无缺口）。
