# H.3.1 课程覆盖表

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

## CS2023、原综合练习与后续技能

- CS2023 的 timers、interrupt handlers、I/O devices、embedded programming、platform constraints 分别在 timer/pwm-capture、interrupts/shared、serial/converters、bare-metal、observe/sleep。参考 [UT Austin 教材](https://users.ece.utexas.edu/~valvano/Volume1/E-Book/) · [TM4C123 数据手册](https://www.ti.com/lit/ds/symlink/tm4c123gh6pm.pdf) · [野火 STM32 启动、调试与 Flash](https://doc.embedfire.com/mcu/stm32/f103zhinanzhe/std/zh/latest/index.html)
- 原练习 (1) 见 gpio、shared，(2) 见 timer，(3) 见 interrupts、shared、sleep，(4) 见 buttons，(5) 见 serial、sleep。H.3.2 用到的复位入口、中断上下文和交接规则在本包先教。gpio 中的地址和读改写模型为教学设定，实际芯片寄存器并不通用。
