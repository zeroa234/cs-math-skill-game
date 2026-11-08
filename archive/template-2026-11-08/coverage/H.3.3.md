# H.3.3 课程覆盖表

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
| 8 | Introduction; Transducers | `measurement` |
| 9 | Sampling and Aliasing; Numbering System | `acquisition` |
| 10 | Frequency Response; Filters | `system-check` |
| 11 | Op Amp (cont.); Fundamental Amplifier Circuits; Input/Output Impedance | `signal-chain` |
| 12 | Measuring the Temperature Coefficient of Resistors | `calibration` |

## CS2023、原综合练习与后续技能

- CS2023 的 AR-IO 总线、GIT-Physical 采集与 SPD-Embedded 传感器/执行器由 uart-frame、i2c、spi 和 physical-links 各课、acquisition/oversample、measurement/motor 负责。参考 [Valvano 嵌入式接口教材](https://users.ece.utexas.edu/~valvano/Volume1/) · [NXP UM10204](https://www.nxp.com/docs/en/user-guide/UM10204.pdf) · [MIT 2.671 测量与仪器](https://ocw.mit.edu/courses/2-671-measurement-and-instrumentation-spring-2006/)
- 原练习 (1) 见 calibration、uncertainty，(2) 见 uart-frame、i2c、spi，(3) 见 signal-chain，(4) 见 acquisition、oversample，(5) 见 motor。H.1.1 的放大与滤波用来设计前端。GPIO、计时和中断等内容在需要的地方说明，H.3.1 和 H.3.2 可作为实作补充。
