# H.1.4 模拟电子技术：覆盖表

**状态（2026-11-23）：已写完（21 课，81/81 节，check-pack、check-coverage、verify.py 127 项、FULL e2e 通过）。** 依据 `../cs-math-skill-tree/data/outlines/H.1.4.json`（主来源 Sedra & Smith *Microelectronic Circuits* 第 6 版第 4–11、17 章；稳压电源一章取北京工业大学《模拟电子技术》教学大纲第九章）、`data/curation/learning-paths/H.1.4.json`（清华华成英《模拟电子技术基础》、MIT 6.012、Benha ECE121）和原技能树综合练习 8 小题。数值核对脚本 `tests/content/H.1.4.verify.py`。

前置：必须前置 H.1.1（电压、电流、欧姆定律、基尔霍夫定律、戴维南等效、时间常数、增益、小信号模型、运算放大器、低通滤波器可直接用）。推荐前置 N.1.2、H.1.3 的内容（电容、电感、频率响应的分贝和波特图）在用到时简短重述。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | The Ideal Diode | `diode-models` |
| 1.2 | Terminal Characteristics of Junction Diodes | `diode-models` |
| 1.3 | Modeling the Diode Forward Characteristic | `diode-models` |
| 1.4 | Operation in the Reverse Breakdown Region-Zener Diodes | `diode-models` |
| 1.5 | Rectifier Circuits | `rectifier-limiter` |
| 1.6 | Limiting and Clamping Circuits | `rectifier-limiter` |
| 2.1 | Device Structure and Physical Operation | `mosfet-dc` |
| 2.2 | Current-Voltage Characteristics | `mosfet-dc` |
| 2.3 | MOSFET Circuits at DC | `mosfet-dc` |
| 2.4 | Applying the MOSFET in Amplifier Design | `mosfet-amp` |
| 2.5 | Small-Signal Operation and Models | `mosfet-amp` |
| 2.6 | Basic MOSFET Amplifier Configurations | `mosfet-amp` |
| 2.7 | Biasing in MOS Amplifier Circuits | `mosfet-amp` |
| 2.8 | Discrete-Circuit MOS Amplifiers | `mosfet-amp` |
| 2.9 | The Body Effect and Other Topics | `mosfet-amp` |
| 3.1 | Device Structure and Physical Operation | `bjt-dc` |
| 3.2 | Current-Voltage Characteristics | `bjt-dc` |
| 3.3 | BJT Circuits at DC | `bjt-dc` |
| 3.4 | Applying the BJT in Amplifier Design | `bjt-amp` |
| 3.5 | Small-Signal Operation and Models | `bjt-amp` |
| 3.6 | Basic BJT Amplifier Configurations | `bjt-amp` |
| 3.7 | Biasing in BJT Amplifier Circuits | `bjt-amp` |
| 3.8 | Discrete-Circuit BJT Amplifier | `bjt-amp` |
| 3.9 | Transistor Breakdown and Temperature Effects | `bjt-amp` |
| 4.1 | IC Design Philosophy | `gain-cell-cascode` |
| 4.2 | The Basic Gain Cell | `gain-cell-cascode` |
| 4.3 | The Cascode Amplifier | `gain-cell-cascode` |
| 4.4 | IC Biasing-Current Sources, Current Mirrors, and Current-Steering Circuits | `current-mirrors` |
| 4.5 | Current-Mirror Circuits with Improved Performance | `current-mirrors` |
| 4.6 | Some Useful Transistor Pairings | `current-mirrors` |
| 5.1 | The MOS Differential Pair | `diff-pair` |
| 5.2 | Small-Signal Operation of the MOS Differential Pair | `diff-pair` |
| 5.3 | The BJT Differential Pair | `diff-pair` |
| 5.4 | Other Nonideal Characteristics of the Differential Amplifier | `diff-nonideal-multistage` |
| 5.5 | The Differential Amplifier with Active Load | `current-mirrors` |
| 5.6 | Multistage Amplifiers | `diff-nonideal-multistage` |
| 6.1 | Low-Frequency Response of the CS and CE Amplifiers | `freq-low-hf-model` |
| 6.2 | Internal Capacitive Effects and the High-Frequency Model of the MOSFET and the BJT | `freq-low-hf-model` |
| 6.3 | High-Frequency Response of the CS and CE Amplifiers | `miller-octc` |
| 6.4 | Useful Tools for the Analysis of the High-Frequency Response of Amplifiers | `miller-octc` |
| 6.5 | A Closer Look at the High-Frequency Response of the CS and CE Amplifiers | `miller-octc` |
| 6.6 | High-Frequency Response of the CG and Cascode Amplifiers | `freq-other-stages` |
| 6.7 | High-Frequency Response of the Source and Emitter Followers | `freq-other-stages` |
| 6.8 | High-Frequency Response of Differential Amplifiers | `freq-other-stages` |
| 6.9 | Other Wideband Amplifier Configurations | `freq-other-stages` |
| 6.10 | High-Frequency Response of Multistage Amplifiers | `freq-other-stages` |
| 7.1 | The General Feedback Structure | `feedback-basics` |
| 7.2 | Some Properties of Negative Feedback | `feedback-basics` |
| 7.3 | The Four Basic Feedback Topologies | `feedback-basics` |
| 7.4 | The Feedback Voltage-Amplifier (Series-Shunt) | `feedback-amplifiers` |
| 7.5 | The Feedback Transconductance-Amplifier (Series-Series) | `feedback-amplifiers` |
| 7.6 | The Feedback Transresistance-Amplifier (Shunt-Shunt) | `feedback-amplifiers` |
| 7.7 | The Feedback Current-Amplifier (Shunt-Series) | `feedback-amplifiers` |
| 7.8 | Summary of the Feedback Analysis Method | `feedback-amplifiers` |
| 7.9 | Determining the Loop Gain | `stability-compensation` |
| 7.10 | The Stability Problem | `stability-compensation` |
| 7.11 | Effect of Feedback on the Amplifier Poles | `stability-compensation` |
| 7.12 | Stability Study Using Bode Plots | `stability-compensation` |
| 7.13 | Frequency Compensation | `stability-compensation` |
| 8.1 | Classification of Output Stages | `class-a-b` |
| 8.2 | Class A Output Stage | `class-a-b` |
| 8.3 | Class B Output Stage | `class-a-b` |
| 8.4 | Class AB Output Stage | `class-ab-power` |
| 8.5 | Biasing the Class AB Circuit | `class-ab-power` |
| 8.6 | CMOS Class AB Output Stages | `class-ab-power` |
| 8.7 | Power BJTs | `class-ab-power` |
| 8.8 | Variations on the Class AB Configuration | `class-ab-power` |
| 8.9 | IC Power Amplifiers | `class-ab-power` |
| 8.10 | MOS Power Transistors | `class-ab-power` |
| 9.1 | Basic Principles of Sinusoidal Oscillators | `sine-oscillators` |
| 9.2 | Op-Amp-RC Oscillator Circuits | `sine-oscillators` |
| 9.3 | LC and Crystal Oscillators | `sine-oscillators` |
| 9.4 | Bistable Multivibrators | `multivibrators` |
| 9.5 | Generation of Square and Triangular Waveforms Using Astable Multivibrators | `multivibrators` |
| 9.6 | Generation of a Standardized Pulse-The Monostable Multivibrator | `multivibrators` |
| 9.7 | Integrated-Circuit Timers | `multivibrators` |
| 10.1 | 整流电路 | `power-supply` |
| 10.2 | 滤波电路 | `power-supply` |
| 10.3 | 并联稳压电路 | `power-supply` |
| 10.4 | 串联稳压电路 | `power-supply` |
| 10.5 | 开关稳压电路 | `power-supply` |

## CS2023 核心主题（C2）

`scope.json` 对 H.1.4 只给国标电子信息类的模拟电子技术，没有 CS2023 主题；8 个章由上表的课负责。

## 学习资源的章节（C3）

- en1（Sedra & Smith 第 4–11、17 章）：就是上面的大纲，逐节落课。半导体物理（第 3 章）不收，PN 结只讲到伏安特性和单向导电，物理机理属于 N.2.2、H.2.5。
- zh2（华成英）的“零点漂移”和四种差分接法比较：在 `diff-pair` 讲零点漂移是差分电路的动机，四种接法用“双端输出增益是单端的 2 倍”一句话概括。
- en3（Benha）和 zh3（北工大第九章）的 78xx/LM317 三端稳压器和开关稳压：在 `power-supply` 讲到框图和效率，不讲开关电源的控制环路设计。

## 原技能树综合练习（C4）

| 小题 | 内容 | 由哪一课教到 |
|---|---|---|
| (1) | 二极管恒压降模型、半波整流峰值 | `diode-models`、`rectifier-limiter` |
| (2) | 共射、共源放大器的 g_m、r_π、增益 | `mosfet-amp`、`bjt-amp` |
| (3) | BJT 差分对的差模、共模增益和 CMRR | `diff-pair`、`diff-nonideal-multistage` |
| (4) | 电流镜有源负载的 r_o 和增益 | `current-mirrors` |
| (5) | 密勒电容和上限截止频率 | `miller-octc` |
| (6) | 负反馈闭环增益和增益灵敏度 | `feedback-basics` |
| (7) | 乙类效率、交越失真和甲乙类 | `class-a-b`、`class-ab-power` |
| (8) | 文氏桥振荡频率和起振增益、稳压管限流电阻 | `sine-oscillators`、`power-supply` |

## 后继技能用到的写法（C5）

必须后继：H.2.6 模拟集成电路设计、E.1.3 射频与高频电路、E.3.1 电力电子技术（都还没有内容包）。它们直接用到：二极管和稳压管模型、MOSFET 平方律和小信号模型（g_m、r_o）、共源/共栅/源极跟随器、电流镜、共源共栅、差分对、密勒效应、负反馈和相位裕度、功率放大器效率、整流滤波和线性/开关稳压。这些都写进本包 `terms`。
