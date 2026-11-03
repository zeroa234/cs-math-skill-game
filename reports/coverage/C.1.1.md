# C.1.1 计算机组成原理：覆盖表

规则见 `docs/content-authoring.md` 的“知识覆盖面标准”。依据：skill-tree 大纲 `../cs-math-skill-tree/data/outlines/C.1.1.json`：MIT 6.004 Computation Structures（2017 春季，OCW）第 1、2、4、5、6、13、14、18 单元的 Topic Videos 分段。“节”是技能内部编号，“原文”是 6.004 自己的编号和标题。

这一站的必须前置只有 P.1.1，所以课里需要算的地方用 Python 写（`bin`、`hex`、位运算）。6.004 用自己设计的 Beta 指令集；原技能树的综合练习用 RISC-V 和 Patterson & Hennessy 的控制信号名，所以数据通路和控制器两章用 RISC-V 讲，并在讲到时注明 Beta 的不同（Beta 的指令和数据在同一个内存里；异常时把 PC + 4 存进 R30，也叫 XP）。

`node scripts/check-coverage.mjs C.1.1` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | 1.2.1 What is Information? | `information` |
| 1.2 | 1.2.2 Quantifying Information | `information` |
| 1.3 | 1.2.4 Encoding | `information`, `binary-hex` |
| 1.4 | 1.2.5 Fixed-length Encodings | `binary-hex` |
| 1.5 | 1.2.6 Signed Integers: 2’s complement | `twos-complement` |
| 1.6 | 1.2.7 Variable-length Encoding | `huffman` |
| 1.7 | 1.2.9 Huffman Code | `huffman` |
| 1.8 | 1.2.10 Error Detection and Correction | `error-codes` |
| 2.1 | 2.2.1 Concrete Encoding of Information | `digital-abstraction` |
| 2.2 | 2.2.4 Combinational Devices | `digital-abstraction` |
| 2.3 | 2.2.5 Dealing with Noise | `digital-abstraction` |
| 2.4 | 2.2.6 Voltage Transfer Characteristic | `digital-abstraction` |
| 3.1 | 4.2.1 Sum of Products | `logic-gates` |
| 3.2 | 4.2.2 Useful Logic Gates | `logic-gates` |
| 3.3 | 4.2.3 Inverting Logic | `logic-gates` |
| 3.4 | 4.2.4 Logic Simplification | `simplify-mux-rom` |
| 3.5 | 4.2.5 Karnaugh Maps | `simplify-mux-rom` |
| 3.6 | 4.2.6 Multiplexers | `simplify-mux-rom` |
| 3.7 | 4.2.7 Read-only Memories | `simplify-mux-rom`, `fsm` |
| 4.1 | 5.2.1 Digital State | `registers-clock` |
| 4.2 | 5.2.2 D Latch | `registers-clock` |
| 4.3 | 5.2.3 D Register | `registers-clock` |
| 4.4 | 5.2.4 D Register Timing | `registers-clock` |
| 4.5 | 5.2.5 Sequential Circuit Timing | `registers-clock` |
| 5.1 | 6.2.1 Finite State Machines | `fsm` |
| 5.2 | 6.2.2 State Transition Diagrams | `fsm` |
| 5.3 | 6.2.3 FSM States | `fsm` |
| 5.4 | 6.2.4 Roboant Example | `fsm` |
| 5.5 | 6.2.5 Equivalent States; Implementation | `fsm` |
| 5.6 | 6.2.6 Synchronization and Metastability | `fsm` |
| 6.1 | 13.2.1 Building Blocks | `datapath-alu` |
| 6.2 | 13.2.2 ALU Instructions | `alu-bitwise`, `datapath-alu`, `control-unit` |
| 6.3 | 13.2.3 Load and Store | `load-store` |
| 6.4 | 13.2.4 Jumps and Branches | `branches-exceptions` |
| 6.5 | 13.2.5 Exceptions | `branches-exceptions` |
| 6.6 | 13.2.6 Summary | `branches-exceptions`, `control-unit` |
| 7.1 | 14.2.1 Memory Technologies | `memory-tech` |
| 7.2 | 14.2.2 SRAM | `memory-tech` |
| 7.3 | 14.2.3 DRAM | `memory-tech` |
| 7.4 | 14.2.4 Non-volatile Storage; Using the Hierarchy | `memory-tech` |
| 7.5 | 14.2.5 The Locality Principle | `memory-tech` |
| 7.6 | 14.2.6 Caches | `cache-direct` |
| 7.7 | 14.2.7 Direct-mapped Caches | `cache-direct` |
| 7.8 | 14.2.8 Block Size; Cache Conflicts | `cache-assoc` |
| 7.9 | 14.2.9 Associative Caches | `cache-assoc` |
| 7.10 | 14.2.10 Write Strategies | `cache-assoc` |
| 8.1 | 18.2.1 OS Device Handlers | `io-interrupts` |
| 8.2 | 18.2.2 SVCs for Input/Output | `io-interrupts` |
| 8.3 | 18.2.3 Example: Match Handler with OS | `io-interrupts` |
| 8.4 | 18.2.4 Real Time | `real-time` |
| 8.5 | 18.2.5 Weak Priorities | `real-time` |
| 8.6 | 18.2.6 Strong Priorities | `real-time` |
| 8.7 | 18.2.7 Example: Priorities in Action! | `real-time` |

另外两课不对应单独的一节，是原技能树综合练习和中文主资源（华中科技大学《计算机组成原理》授课目标）要求的：`floating-point`（IEEE 754 单精度，练习第 1 题）、`adder`（半加器、全加器、行波进位加法器、补码减法和溢出判断，练习第 2 题；6.004 把加法器放在第 4 单元的组合逻辑里讲）。

教到什么深度（入门层）：
- 信息量只讲 log₂(1/p) 和等可能时的 log₂ N；熵（1.2.3，大纲没收）只顺带提一句。
- 数字抽象讲四个电压门限、噪声容限和“组合器件”的四条要求；电压传输特性只讲“中间那段要有放大作用”，不讲 CMOS 电路（6.004 第 3 单元，大纲没收）。
- 卡诺图只讲 2、3 个变量。
- 时序电路讲 D 锁存器、D 寄存器、建立时间和保持时间、t_CLK ≥ t_PD,reg + t_PD,logic + t_SETUP；亚稳态只讲“异步输入要先过两个串联的寄存器”。
- 实时只讲 6.004 的延迟、截止时间、弱优先级和强优先级的最坏延迟算法，用一个小例子算。
- 流水线、多周期数据通路（中文主资源的授课目标里有）不在这一站：6.004 把流水线放在第 15–16 单元，大纲判归 C.1.2 计算机体系结构。微程序控制只讲它和硬布线控制的区别。

## 和原文的核对

2026-11-03 用 web-fetch 子代理逐条读了 6.004 第 1、2、5、6、13、14、18 单元的 Annotated Slides 原文，核对课里引用的说法：信息量公式、补码的负权重和取反加一、Huffman 例题（A = 1/3、B = 1/2、C = D = 1/12，平均 1⅔ 位）、检错 E + 1 与纠错 2E + 1、门限的顺序和例子（0.5 / 1 / 3 / 3.5 V）、锁存器和寄存器、时序约束、roboant、等价状态、两个寄存器的同步器、Beta 的寄存器堆和异常（XP = R30，处理程序在 0x4 或 0x8，JMP(XP) 返回）、存储器的数量级（寄存器约 20 ps、SRAM 几纳秒、例题里主存 40 ns、NAND 闪存读约 10 µs、磁盘约 10 ms）、SRAM 6 个晶体管、DRAM 1 个晶体管加电容并约每 10 ms 刷新一次、写直达和写回、弱优先级和强优先级。数值由 `tests/content/C.1.1.verify.py` 用 Python 算过。

## CS2023（`data/curation/scope.json`）

| 知识点 | CS2023 主题（scope.json 匹配原文） | 课 |
|---|---|---|
| 数据表示 | AR-Representation，CS Core：Numeric data representation and number bases | `binary-hex`, `twos-complement`, `floating-point` |
| 数据通路 | AR-Organization，KA Core：Implementation of simple datapaths | `datapath-alu`, `load-store`, `branches-exceptions` |
| 控制器 | AR-Assembly，CS Core：Control unit: instruction fetch, decode, and execution | `datapath-alu`, `control-unit` |
| 存储和I/O组织 | AR-Memory，CS Core：Main memory organization and operations；AR-IO，CS Core：I/O fundamentals | `memory-tech`, `cache-direct`, `cache-assoc`, `io-interrupts` |

## 综合练习（原技能树，约 45 分钟）

| 小题 | 要用到 | 课 |
|---|---|---|
| (1) −37 的 8 位补码；0x9C 的无符号和有符号值；−6.25 的 IEEE 754 单精度 | 补码、十六进制、浮点数格式 | `twos-complement`, `binary-hex`, `floating-point` |
| (2) 8 位补码 100 + 50 是否溢出，溢出标志怎样由进位判断 | 加法器、溢出 | `adder` |
| (3) 单周期 RISC-V 执行 lw x5, 8(x6) 经过的部件和五个控制信号 | 数据通路、控制信号 | `load-store`, `control-unit` |
| (4) 直接映射 cache 的 tag / index / offset 位数和例子 | cache 地址划分 | `cache-direct` |
| (5) 轮询、中断、DMA 各适合什么 | I/O 方式 | `io-interrupts` |

## 后继技能用到的写法（C5）

这条路线上以 C.1.1 为必须前置的是 C.2.1 操作系统。

| C.2.1 用到的 | 课 |
|---|---|
| 二进制、十六进制、位运算（拆虚拟地址、页表项的标志位） | `binary-hex`, `alu-bitwise` |
| 寄存器、程序计数器（上下文切换） | `datapath-alu` |
| 中断、异常、陷入处理程序再返回（受限直接执行、系统调用） | `io-interrupts`, `branches-exceptions` |
| 存储层次、局部性、cache 和替换（TLB 是页表的 cache） | `memory-tech`, `cache-direct`, `cache-assoc` |
| 轮询、中断、DMA、设备寄存器 | `io-interrupts` |
