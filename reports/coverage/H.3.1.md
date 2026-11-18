# H.3.1 单片机与微控制器：覆盖表

**状态（2026-11-18）：已写完（44/44 节全覆盖，v2 零基础 + WSL `gcc -std=c11 -O2` 真实编译执行 C 片段验证）。** 依据 `../cs-math-skill-tree/data/outlines/H.3.1.json`、`../cs-math-skill-tree/output/outlines.json`、`../cs-math-skill-tree/data/curation/learning-paths/H.3.1.json` 及 `reports/chapter-order.md`（按先修与教学逻辑重排 6 章顺序：`裸机程序 → GPIO → 调试与资源限制 → 外设 → 定时器 → 中断`），主来源为 UT Austin *Embedded Systems - Shape The World*（Valvano & Yerraballi），对齐 `H.3.1` 综合练习 5 问（说明：GPIO 寄存器基址与位掩码示例为教学通用设定，具体地址以各芯片手册为准）；本地核对脚本 `tests/content/H.3.1.verify.py`（Python `Fraction` 精确定时/串口/ADC/PWM 验算 + WSL `gcc` 实测编译运行嵌入式 C 代码段）。

## 大纲逐节（C1：44/44 节）

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Binary number systems | `bare-metal` |
| 1.2 | Embedded Systems | `bare-metal` |
| 1.3 | Introduction to Computers | `bare-metal` |
| 1.4 | I/O Ports | `gpio` |
| 1.5 | CPU Registers | `bare-metal` |
| 1.6 | Address Space | `bare-metal` |
| 1.7 | Software Development Process | `observe` |
| 2.1 | Structure and Organization of C | `bare-metal` |
| 2.2 | Variables and Expressions | `bare-metal` |
| 2.3 | Functions | `bare-metal` |
| 2.4 | Conditional branching and loops | `bare-metal` |
| 3.1 | Stellaris LM4F120 and Tiva TM4C123 LaunchPad I/O pins | `gpio` |
| 3.2 | Basic Concepts of Input and Output Ports | `gpio` |
| 3.3 | I/O Programming and the Direction Register | `gpio` |
| 3.4 | Debugging monitor using an LED | `observe` |
| 3.5 | Hardware debugging tools | `observe` |
| 4.1 | Product Life Cycle | `observe` |
| 4.2 | Successive Refinement | `observe` |
| 4.3 | Quality Design | `observe` |
| 4.4 | Functional debugging | `observe` |
| 5.1 | Breadboard | `gpio` |
| 5.2 | Switch Interfaces | `buttons` |
| 5.3 | LED Interfaces | `gpio` |
| 6.1 | Debugging Theory | `observe` |
| 6.2 | SysTick Timer | `timer` |
| 6.3 | Functional debugging | `observe` |
| 7.1 | Accurate Time Delays using SysTick | `timer` |
| 7.2 | Finite State Machines with Indexed Structures | `state-machine` |
| 7.3 | Stepper motors | `state-machine` |
| 8.1 | I/O Synchronization | `serial` |
| 8.2 | Universal Asynchronous Receiver Transmitter (UART) | `serial` |
| 8.3 | Distributed Systems | `serial` |
| 8.4 | Interfacing the Nokia 5110 Using a Synchronous Serial Port | `serial` |
| 9.1 | Interrupt Concepts | `interrupts` |
| 9.2 | Interthread Communication and Synchronization | `shared` |
| 9.3 | NVIC on the ARM Cortex-M Processor | `interrupts` |
| 9.4 | Edge-triggered Interrupts | `interrupts` |
| 9.5 | SysTick Periodic Interrupts | `timer` |
| 9.6 | DC Motor Interface with PWM | `pwm-capture` |
| 10.1 | Approximating continuous signals in the digital domain | `converters` |
| 10.2 | Digital to Analog Conversion | `converters` |
| 11.1 | Data Acquisition and Control Systems | `converters` |
| 11.2 | The Analog to Digital Converter | `converters` |
| 11.3 | Details of the ADC on the TM4C123 | `converters` |

## CS2023 核心主题（C2）

`../cs-math-skill-tree/data/curation/scope.json` 为 `H.3.1` 匹配的 **5 项** CS2023 核心主题全部覆盖落课（5/5；注：CS2023 未单设 `GPIO` 主题，由大纲 3.x/5.x 补充完善）：

| 知识点 | KA / 要求 | 课 |
|---|---|---|
| 裸机程序 | SPD-Embedded / KA Core：Embedded programming | `bare-metal` |
| 调试与资源限制 | SPD-Common / CS Core：Programming under platform constraints | `observe`、`sleep` |
| 外设 | AR-IO / CS Core：I/O devices | `serial`、`converters`、`state-machine` |
| 定时器 | OS-Scheduling / KA Core：Timers | `timer`、`pwm-capture` |
| 中断 | SPD-Embedded / KA Core：Interrupt handlers | `interrupts`、`shared` |

## 学习路径资源与综合练习/后续映射（C3 / C4 / C5）

- **参考资料映射（C3）**：`en1`（Valvano *Embedded Systems - Shape The World*，主源）完整覆盖二进制/I/O 端口/C 组织结构、`GPIO`、调试与仪器、查表有限状态机、UART/同步串口、NVIC 与边沿/周期中断、PWM 及 DAC/ADC 数据采集；`zh1`（江协科技《STM32 入门教程》2023 版，中文主源）与 `zh2`（电子科技大学《嵌入式系统及应用》MOOC，补充）对照 STM32 外设寄存器操作、定时中断、串口与 ADC 实践；`r7-zh1`（野火《STM32 库开发实战指南》，补充）补足芯片资源约束、硬件调试观测及低功耗睡眠策略。
- **综合练习 5 问映射（C4）**：
  - 第 (1) 问 C 语言 `volatile uint32_t *` 读写第 5 脚方向/输出寄存器（`GPIO_DIR |= (1u << 5)`、`GPIO_OUT |= (1u << 5)`），读–改–写保护无关位及 `volatile` 防优化原因 → `gpio`、`shared`、`boss`。
  - 第 (2) 问 16 MHz 主频、64 分频（250 kHz）每 1 ms 比较中断的比较值 `249`（从 0 计满 250 次） → `timer`、`boss`。
  - 第 (3) 问中断服务程序精简原则（禁阻塞/`printf`）、共享状态加 `volatile` 与临界区关中断/原子保护，及轮询 vs 中断适用边界 → `interrupts`、`shared`、`boss`。
  - 第 (4) 问机械按键弹跳成因与 1 ms 周期连续采样去抖状态机 C 代码实现 → `buttons`、`boss`。
  - 第 (5) 问 UART `115200` 波特 8N1（每字节 10 位）最大速率 `11520 B/s` 及多种降功耗手段（睡眠中断唤醒、关外设时钟、降频、DMA/硬件定时替忙等） → `serial`、`sleep`、`boss`。
- **前后继状态（C5）**：必须前置为 `P.2.2`（C 语言位运算、指针与结构），推荐前置 `H.1.1`、`H.1.2`、`C.1.1`。下游必须解锁（`unlocks`）为 `H.3.2 嵌入式系统、驱动与 RTOS`（并作 `H.3.3`、`H.3.4`、`H.4.3` 推荐前置），本包在复位启动流程、MMIO `volatile` 寄存器编程、定时器节拍与中断上下半拆解思路上直接衔接 `H.3.2` 及传感器采集（C5 无缺口）。
