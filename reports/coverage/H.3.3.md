# H.3.3 传感器与接口：覆盖表

**状态（2026-11-18）：已写完（48/48 节全覆盖，v2 零基础 + 4x 过采样蒙特卡洛 / WSL `ngspice` 惠斯通电桥仿真验证）。** 依据 `../cs-math-skill-tree/data/outlines/H.3.3.json`、`../cs-math-skill-tree/output/outlines.json`、`../cs-math-skill-tree/data/curation/learning-paths/H.3.3.json`，主来源为 Valvano *Embedded Systems: Real-Time Interfacing to ARM Cortex-M Microcontrollers (Vol.2, 4e)* 与 MIT OCW *6.071J Introduction to Electronics, Signals, and Measurement*（Lec 1/4/16/29 及 Lab 7），对齐 `H.3.3` 综合练习 5 问，本地核对脚本 `tests/content/H.3.3.verify.py`（Python `Fraction`/精确两点标定线性回归、UART/I²C/SPI 时序算术、`log2(sqrt(N))` 过采样白噪声抖动仿真、PWM 均值与 WSL `ngspice` 电桥实测验算）。

## 大纲逐节（C1：48/48 节，节号采用 `output/outlines.json` 连续 `number` 字段）

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Introduction | `capture-edge` |
| 1.2 | Timing | `capture-edge` |
| 1.3 | Edge-triggered Interfacing | `capture-edge` |
| 1.4 | Configuring Digital Output Pins | `capture-edge` |
| 1.5 | Blind-cycle Interfacing | `capture-edge` |
| 1.6 | Busy-Wait Synchronization | `capture-edge` |
| 1.7 | UART Interface | `uart-frame` |
| 1.8 | Keyboard Interface | `capture-edge` |
| 2.1 | Multithreading | `capture-edge` |
| 2.2 | Interthread Communication and Synchronization | `capture-edge` |
| 2.3 | Critical Sections | `capture-edge` |
| 2.4 | NVIC on the ARM Cortex-M Processor | `capture-edge` |
| 2.5 | Edge-triggered Interrupts | `capture-edge` |
| 2.6 | Interrupt-Driven UART | `uart-frame` |
| 2.7 | Periodic Interrupts using SysTick | `capture-edge` |
| 2.8 | Low-Power Design | `system-check` |
| 3.1 | Input Capture or Input Edge Time Mode | `capture-edge` |
| 3.2 | Output Compare or Periodic Timer | `capture-edge` |
| 3.3 | Pulse Width Modulation | `motor` |
| 3.4 | Frequency Measurement | `capture-edge` |
| 3.5 | Binary Actuators | `motor` |
| 3.6 | Integral Control of a DC Motor | `motor` |
| 4.1 | Introduction to Serial Communication | `uart-frame`、`choose-bus` |
| 4.2 | RS232 Interfacing | `uart-frame` |
| 4.3 | RS422/USB/RS423/RS485 Balanced Differential Lines | `physical-links` |
| 4.4 | Logic Level Conversion | `physical-links` |
| 4.5 | Synchronous Transmission and Receiving using the SSI | `spi` |
| 4.6 | Inter-Integrated Circuit (I2C) Interface | `i2c` |
| 4.7 | Introduction to Universal Serial Bus (USB) | `physical-links` |
| 5.1 | Resistors and Capacitors | `signal-chain` |
| 5.2 | Op Amps | `signal-chain` |
| 5.3 | Analog Filters | `signal-chain` |
| 5.4 | Digital to Analog Converters | `motor` |
| 5.5 | Analog to Digital Converters | `oversample` |
| 6.1 | Power | `system-check` |
| 6.2 | Tolerance | `uncertainty` |
| 6.3 | Design for Testability | `system-check` |
| 7.1 | Introduction | `acquisition` |
| 7.2 | Transducers | `measurement` |
| 7.3 | Discrete Calculus | `acquisition` |
| 7.4 | Data Acquisition System Design | `acquisition` |
| 7.5 | Analysis of Noise | `uncertainty` |
| 7.6 | Data Acquisition Case Studies | `oversample` |
| 8 | Introduction; Transducers (B lec 1) | `measurement` |
| 9 | Sampling and Aliasing; Numbering System (B lec 4) | `acquisition` |
| 10 | Frequency Response; Filters (B lec 16) | `system-check` |
| 11 | Op Amp (cont.); Fundamental Amplifier Circuits; Input/Output Impedance (B lec 29) | `signal-chain` |
| 12 | Measuring the Temperature Coefficient of Resistors (B Lab 7) | `calibration` |

## CS2023 核心主题（C2）

`../cs-math-skill-tree/data/curation/scope.json` 为 `H.3.3` 匹配的 **3 项** CS2023 核心主题全部覆盖落课（3/3，连同测量、校准、误差共覆盖全部 6 章主题）：

| 知识点 | KA / 要求 | 课 |
|---|---|---|
| 总线 | AR-IO / CS Core：Buses fundamentals | `uart-frame`、`i2c`、`spi`、`physical-links`、`choose-bus` |
| 采集 | GIT-Physical / KA Core：Acquisition of data from sensors | `acquisition`、`oversample` |
| 执行器和软硬件接口 | SPD-Embedded / KA Core：Sensors and actuators | `measurement`、`signal-chain`、`capture-edge`、`motor`、`system-check` |

## 学习路径资源与综合练习/后续映射（C3 / C4 / C5）

- **参考资料映射（C3）**：`zh1`（《传感器与检测技术》中国大学 MOOC 12 单元，中文主源）覆盖传感器转导、惠斯通电桥调理、精密度/准确度误差与标定；`en1`（MIT 6.071J OCW，英文主源）覆盖测量误差、采样与混叠、运算放大器调理、滤波及 Lab 7 温度系数校准实验；`zh2`（江协科技《STM32 入门教程》2023 版，补充）与 `en2`（Valvano *Embedded Systems*，补充）及 `r7-en1`（Auburn MECH 4240/50 讲义，补充）对照微控制器实战里的 UART/I²C/SPI 串行总线、输入捕获/PWM 控制直流电机以及低功耗系统集成。
- **综合练习 5 问映射（C4）**：
  - 第 (1) 问精密度 vs 准确度辨析，以及两点线性标定（0 °C→0.52 V，100 °C→1.52 V）求 `0.97 V` 对应温度 `45 °C` → `calibration`、`uncertainty`、`boss`。
  - 第 (2) 问 I²C（2 线开漏上拉/7 位寻址/半双工/100k–1MHz）、SPI（4 线/独立 CS 片选/全双工/数十 MHz）、UART（2 线异步/波特率约定/全双工）对比与 I²C 地址冲突解法（改引脚/分总线/I²C 多路器） → `uart-frame`、`i2c`、`spi`、`choose-bus`、`boss`。
  - 第 (3) 问完整传感器调理链路（阻抗匹配缓冲、满量程放大、电平移位、低通抗混叠滤波、隔离保护/线性化）与惠斯通电桥微电阻测量及抑温漂/共模干扰优势 → `signal-chain`、`boss`。
  - 第 (4) 问采样率防混叠与带宽匹配依据、12 位 ADC 每 **4 倍过采样**平均多获得约 **`1` 位**有效分辨率及核心前提（须含充分白噪声/人工抖动打破台阶死锁） → `acquisition`、`oversample`、`boss`。
  - 第 (5) 问 PWM 驱动 `12 V` × `25%` 平均电压 `3 V`、H 桥四开关控制双向正反转/制动原理与感性负载续流二极管保护开关管击穿 → `motor`、`boss`。
- **前后继状态（C5）**：必须前置为 `H.1.1`（电阻等效、运放放大、低通抗混叠与基础量化）与 `C.1.1`（计算机组成与总线中断基础），`H.3.1` 为推荐前置（`H.1.3` 在研究节点 `research/nodes/H.3.3.json` 中亦列为额外先修要求，而练习与技能树图边里作推荐先修，本包自带采样率与抗混叠推导不强制依赖 `H.1.3`）。虽无强解后继，本包将模拟前端调理、总线互联与执行驱动收束打通至真实物理系统（C5 无缺口）。
