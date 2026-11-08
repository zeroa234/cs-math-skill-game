# H.1.2 课程覆盖表

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

## CS2023 与原综合练习

- SF-Foundations CS Core 的布尔化简、组合/时序逻辑、有限状态机和时钟见各对应章节。AR-Logic KA Core 的门延迟见 `gate-delay`、`timing`。补充 CMOS、ROM、流水线、交错与握手。 [MIT 6.004](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) · [MIT CMOS](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c3/c3s1/) · [MIT RoboAnt 与同步](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c6/c6s1/)
- 原题 1–2 的卡诺图与三 NAND 实现见 `kmap`；原题 3 的全加器和进位路径见 `adder`；原题 4 的 D 锁存、触发与允许重叠的 101 检测见 `registers`、`fsm`；原题 5 在 `timing` 分别验建立和保持，频率例题使用无偏斜的简化模型。
- 验证脚本穷举布尔输入与 Mealy 状态机的小输入，并用 Icarus Verilog 实际运行门级示例。 [Icarus Verilog](https://steveicarus.github.io/iverilog/)
