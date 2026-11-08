# C.1.2 课程覆盖表

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
| 6 | Pipelined Processor Architecture II | `data-hazard` |
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
| 12 | Branch Prediction 2 (Apple Guest Lecture) | `predict` |
| 13 | Memory Consistency | `ordering` |
| 14 | OoO Performance Engineering | `out-of-order`、`cpu-time`、`amdahl` |

## CS2023、原综合练习与后续技能

- CS2023 的 AR-Assembly、AR-Organization、AR-Memory、AR-Performance-Energy 对应各章。MIPS 教基本操作与寻址，原练习按题设使用等效的 RISC-V 五级流水线，不混用两种编码。预测与恢复、乱序、目录和内存顺序用小模型讲解。依据 [《计算机体系结构基础》第 2、9、11、12 章](https://foxsen.github.io/archbase/) · [ETH DDCA](https://safari.ethz.ch/digitaltechnik/spring2024/doku.php?id=schedule) · [MIT 6.823 分支预测](https://ocw.mit.edu/courses/6-823-computer-system-architecture-fall-2005/resources/l13_brnchpred/)
- 原练习 (1) 见 data-hazard，(2) 见 cpu-time，(3) 见 amdahl，(4) 见 amat，(5) 见 coherence，(6) 见 predict。虚拟页、权限和 TLB 在 virtual-memory 补齐，模型不要求已学操作系统。
