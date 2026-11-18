# H.1.1 电路与模拟电子基础：覆盖表

**状态（2026-11-18）：已写完（41/41 节全覆盖，v2 零基础 + WSL ngspice OP/TRAN/AC 实测验证）。** 依据 `../cs-math-skill-tree/data/outlines/H.1.1.json`、`output/outlines.json`、`../cs-math-skill-tree/data/curation/learning-paths/H.1.1.json`，主来源为 MIT OCW 6.002 *Circuits and Electronics*（第 1–3、12 讲）与 Sedra & Smith *Microelectronic Circuits* 5e（第 1、2、7、9、12 章精选），对齐 `H.1.1` 综合练习 5 问，本地核对脚本 `tests/content/H.1.1.verify.py`（Python 数值核对 + WSL `ngspice` 45.2 DC/TRAN/AC 实际电路仿真）。

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Signals | `gain` |
| 1.2 | Frequency Spectrum of Signals | `lowpass`、`noise` |
| 1.3 | Amplifiers | `gain` |
| 1.4 | Circuit Models for Amplifiers | `gain` |
| 1.5.1 | Measuring the Amplifier Frequency Response | `lowpass` |
| 1.5.2 | Amplifier Bandwidth | `lowpass` |
| 1.5.3 | Single-Time-Constant Networks | `transient`、`lowpass` |
| 1.5.4 | Classification of Amplifiers Based on Frequency Response | `lowpass` |
| 1.6 | Circuit Simulation Using SPICE | `ohm`、`transient` |
| 2.1 | The Ideal Op Amp | `feedback` |
| 2.2 | The Inverting Configuration | `feedback` |
| 2.3 | The Noninverting Configuration | `feedback` |
| 2.4 | Difference Amplifiers | `feedback` |
| 2.5 | Effect of Finite Open-Loop Gain and Bandwidth on Circuit Performance | `real-op-amp` |
| 2.6 | Large-Signal Operation of Op Amps | `real-op-amp` |
| 2.7 | DC Imperfections | `real-op-amp` |
| 2.8 | Integrators and Differentiators | `feedback` |
| 3.1 | The MOS Differential Pair | `transistor-amp` |
| 3.2 | Small-Signal Operation of the MOS Differential Pair | `transistor-amp` |
| 3.3 | The BJT Differential Pair | `transistor-amp` |
| 3.4 | The Differential Amplifier with Active Load | `transistor-amp` |
| 3.5 | Frequency Response of the Differential Amplifier | `real-op-amp` |
| 3.6 | Multistage Amplifiers | `transistor-amp` |
| 4.1 | The Two-Stage CMOS Op Amp | `real-op-amp` |
| 4.2 | The Folded-Cascode CMOS Op Amp | `real-op-amp` |
| 4.3 | Data Converters--an Introduction | `quantize` |
| 4.4 | D/A Converter Circuits | `quantize` |
| 4.5 | A/D Converter Circuits | `quantize`、`alias` |
| 5.1 | Filter Transmission, Types, and Specification | `lowpass`、`filter-design` |
| 5.2 | The Filter Transfer Function | `filter-design` |
| 5.3 | Butterworth and Chebyshev Filters | `filter-design` |
| 5.4 | First-Order and Second-Order Filter Functions | `filter-design` |
| 5.5 | The Second-Order LCR Resonator | `filter-design` |
| 5.6 | Second-Order Active Filters Based on Inductor Replacement | `filter-design` |
| 5.7 | Second-Order Active Filters Based on the Two-Integrator-Loop Topology | `filter-design` |
| 5.8 | Sensitivity | `filter-design` |
| 5.9 | Switched-Capacitor Filters | `filter-design` |
| 6 | Introduction and Lumped Abstraction | `ohm` |
| 7 | Basic Circuit Analysis Method | `nodes`、`loops` |
| 8 | Superposition, Thévenin and Norton | `equivalent` |
| 9 | Capacitors and First-Order Systems | `transient` |

## CS2023 核心主题（C2）

`../cs-math-skill-tree/data/curation/scope.json` 对 `H.1.1` 注明：`CS2023 没有电路与模拟电子（只在物理计算单元的学习成果里让学生接一个简单电路）。` 本包按照大纲全部 `41/41` 个叶子小节与 6 个章主题（`电路定律`、`RC/RL`、`放大器`、`运放`、`滤波`、`噪声与ADC/DAC接口`）完整落课覆盖。

## 学习路径外部资源映射（C3）

依据 `../cs-math-skill-tree/data/curation/learning-paths/H.1.1.json`，各推荐开源资料的对应覆盖与取舍如下：

- `en1`（MIT 6.002 OCW，主源）：集总抽象、KVL/KCL、受控源、运放、RC/RL 暂态、频率响应与 ADC/DAC 接口 → `ohm`、`nodes`、`loops`、`equivalent`、`transient`、`gain`、`feedback`、`lowpass`、`quantize`、`alias`。
- `r7-zh1`（清华《电路原理》于歆杰，学堂在线官方版；替代第三方转载 `zh1`）：线性电阻分析、节点/回路方程、动态 RC/RL 时域与频响 → `ohm`、`nodes`、`loops`、`equivalent`、`transient`、`lowpass`。
- `r7-zh2`（清华《模拟电子技术基础》华成英，学堂在线官方版；替代第三方转载 `zh2`）：放大基础、差分与多级放大、集成运放、反馈与有源滤波、ADC/DAC 转换 → `gain`、`transistor-amp`、`feedback`、`real-op-amp`、`filter-design`、`quantize`、`alias`（功率放大器与直流稳压电源详章按技能粒度属 `H.2.5`/`H.2.2` 不展深）。
- `r7-en1`（MIT 6.012 Lec 19–24 讲义）：单级与多级放大器小信号/频率响应 → `transistor-amp`、`real-op-amp`。
- `r7-zh3` / `r7-en2`（TI Precision Labs 噪声/滤波与 ADC 驱动）：RMS 噪声带宽权衡与前端抗混叠驱动 → `noise`、`quantize`、`alias`。

## 综合练习与前置/后继映射（C4 / C5）

- **综合练习 5 问映射（C4）**：
  - 第 (1) 问 12 V 串并联电阻网（2 kΩ 串联 3 kΩ ∥ 6 kΩ）全部子问均有独立计分题检查：总等效阻 `4 kΩ`（`series-total-res-c4`）、干路总电流 `3 mA`（`ohm-current-calc`、`boss-resistor-kcl-c4`）、并联电压 `6 V`（`parallel-node-volt-c4`）、$I_{R2} = 2\text{ mA}$（`kcl-branch-current-c4`）、$I_{R3} = 1\text{ mA}$ 及 KCL `2 + 1 = 3 mA` 检验（`kcl-ir3-c4`） → `ohm`、`nodes`、`loops`。
  - 第 (2) 问 RC 电路 $R = 10\text{ k}\Omega, C = 10\ \mu\text{F}$ 充向 5 V 全部子问均有独立计分题检查：时间常数 $\tau = 0.1\text{ s}$（`rc-tau-c4-sec`）、$t = 0.1\text{ s}$ 电压 $\approx 3.16\text{ V}$（`rc-charge-1tau-c4`）、$t = 0.3\text{ s}$ 电压 $\approx 4.75\text{ V}$（`rc-charge-3tau-c4`、`boss-rc-voltage-c4`）与低通截止频率 $f_c \approx 1.59\text{ Hz}$（`rc-cutoff-c4`、`boss-rc-fc-c4`） → `transient`、`lowpass`。
  - 第 (3) 问理想运放反相增益 $A = -R_f / R_{in} = -10$、同相增益 $A = 1 + R_f / R_{in} = 11$，以及负反馈下的“虚短”与“虚断”概念 → `feedback`、`boss`。
  - 第 (4) 问 10 位 3.3 V ADC 求最小步距 $\text{LSB} \approx 3.22\text{ mV}$ 与 1.2 V 对应输出数字码 `372` → `quantize`、`boss`。
  - 第 (5) 问理想 $N$ 位 ADC 量化信噪比 $6.02N + 1.76 \approx 62\text{ dB}$，以及采集前必须先用模拟低通抗混叠滤波器滤除高于奈奎斯特频率成分的原因 → `quantize`、`alias`、`boss`。
- **前后继状态（C5）**：
  - 必须前置为 `M.1.3`（微积分指数积分直觉）与 `M.3.1`（线性方程组解节点方程），推荐前置为 `M.2.1`；本包在 `assumes:` 下声明前置已教词汇并在首现处用白话带过，零基础解释基尔霍夫定律、集总抽象、时间常数、运放虚短虚断、滤波器与量化混叠。
  - 下游必须后继（`unlocks`）为 `H.2.5 半导体器件与微电子基础`（直接复用本包 MOSFET/BJT 静态偏置与小信号跨导放大模型）与 `H.3.3 传感器与接口`（直接复用戴维南加载效应、RC 低通滤波、运放信号调理与 ADC 量化/抗混叠接口）（并被 `H.1.3`、`H.2.3`、`H.3.1` 列为推荐前置；互相关联 `H.1.2`），C5 无缺口。
