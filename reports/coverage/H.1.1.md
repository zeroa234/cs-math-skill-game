# H.1.1 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Signals | `gain` |
| 1.2 | Frequency Spectrum of Signals | `gain` |
| 1.3 | Amplifiers | `gain` |
| 1.4 | Circuit Models for Amplifiers | `gain` |
| 1.5.1 | Measuring the Amplifier Frequency Response | `gain` |
| 1.5.2 | Amplifier Bandwidth | `gain` |
| 1.5.3 | Single-Time-Constant Networks | `transient` |
| 1.5.4 | Classification of Amplifiers Based on Frequency Response | `gain` |
| 1.6 | Circuit Simulation Using SPICE | `noise` |
| 2.1 | The Ideal Op Amp | `feedback` |
| 2.2 | The Inverting Configuration | `feedback` |
| 2.3 | The Noninverting Configuration | `feedback` |
| 2.4 | Difference Amplifiers | `feedback` |
| 2.5 | Effect of Finite Open-Loop Gain and Bandwidth on Circuit Performance | `real-op-amp` |
| 2.6 | Large-Signal Operation of Op Amps | `real-op-amp` |
| 2.7 | DC Imperfections | `real-op-amp` |
| 2.8 | Integrators and Differentiators | `real-op-amp` |
| 3.1 | The MOS Differential Pair | `transistor-amp` |
| 3.2 | Small-Signal Operation of the MOS Differential Pair | `transistor-amp` |
| 3.3 | The BJT Differential Pair | `transistor-amp` |
| 3.4 | The Differential Amplifier with Active Load | `transistor-amp` |
| 3.5 | Frequency Response of the Differential Amplifier | `transistor-amp` |
| 3.6 | Multistage Amplifiers | `transistor-amp` |
| 4.1 | The Two-Stage CMOS Op Amp | `real-op-amp` |
| 4.2 | The Folded-Cascode CMOS Op Amp | `real-op-amp` |
| 4.3 | Data Converters--an Introduction | `quantize` |
| 4.4 | D/A Converter Circuits | `quantize` |
| 4.5 | A/D Converter Circuits | `quantize`、`alias` |
| 5.1 | Filter Transmission, Types, and Specification | `lowpass` |
| 5.2 | The Filter Transfer Function | `lowpass` |
| 5.3 | Butterworth and Chebyshev Filters | `filter-design` |
| 5.4 | First-Order and Second-Order Filter Functions | `lowpass` |
| 5.5 | The Second-Order LCR Resonator | `filter-design` |
| 5.6 | Second-Order Active Filters Based on Inductor Replacement | `filter-design` |
| 5.7 | Second-Order Active Filters Based on the Two-Integrator-Loop Topology | `filter-design` |
| 5.8 | Sensitivity | `filter-design` |
| 5.9 | Switched-Capacitor Filters | `filter-design` |
| 6 | Introduction and Lumped Abstraction | `ohm` |
| 7 | Basic Circuit Analysis Method | `nodes`、`loops` |
| 8 | Superposition, Thévenin and Norton | `equivalent` |
| 9 | Capacitors and First-Order Systems | `transient` |

## CS2023、原综合练习与后续技能

- 上游 scope 说明 CS2023 未设模拟电子单元。知识边界以大纲和原练习为准。实际晶体管级设计、二阶极点综合深入学习可回到教材，互动课先练工作点、级联、反馈、频带和接口决策。参考 [MIT 6.002](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) · [MIT 6.012 放大器讲义](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-spring-2009/pages/lecture-notes/) · [TI 运放与噪声实验](https://www.ti.com/video/series/precision-labs/ti-precision-labs-op-amps.html)
- 原练习 (1) 见 nodes/loops，(2) 见 transient/lowpass，(3) 见 feedback，(4) 见 quantize，(5) 见 alias。H.3.3 继续使用放大、抗混叠、转换范围和噪声的概念。
