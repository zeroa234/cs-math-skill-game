# E.3.1 电力电子技术：覆盖表

**状态（2026-11-23）：已写完，25 课，等用户验收。** 依据 `../cs-math-skill-tree/data/outlines/E.3.1.json`（主来源 Kassakian, Perreault, Verghese, Schlecht《Principles of Power Electronics》第 2 版，MIT 6.622 指定教材，大纲 18 章 70 节）、`data/curation/learning-paths/E.3.1.json`（西南交通大学《电力电子技术》MOOC 第二至八章；NPTEL IISc《Switched Mode Power Conversion》；NPTEL IIT Delhi《Power Electronics》）和原技能树综合练习 8 小题。数值核对脚本 `tests/content/E.3.1.verify.py`。

前置：必须前置只有 H.1.4 模拟电子技术（二极管、恒压降模型、整流、纹波、MOSFET 和它的三极管区、BJT、热阻、负反馈、环路增益、相位裕度、开关稳压电路可直接用），往下是 H.1.1（电压、电流、欧姆定律、基尔霍夫定律、电感、时间常数、方均根、低通滤波器）和微积分、线性代数。大学物理电磁学（N.1.2）不在必须前置里，所以磁通、磁感应强度、法拉第电磁感应定律在 `magnetics-basics` 里从头讲一遍；三相电压和线电压在 `three-phase-rectifier` 现讲；微分方程、状态变量的写法在 `averaged-models` 现讲；传递函数和极点在 `linearization` 现讲（H.4.1 只是推荐前置）。

## 课的安排

| 课 | 章 | 内容 |
|---|---|---|
| `why-switching` | 功率半导体器件 | 线性调整和开关调整的效率对比、理想开关、电力电子电路的四类变换（AC/DC、DC/DC、DC/AC、AC/AC）、变压器在电路里的作用 |
| `diode-mosfet-switch` | 功率半导体器件 | 二极管作开关的简单分析、功率二极管的反向恢复；MOSFET 作开关：导通电阻和导通损耗、体二极管、单极器件的耐压和导通电阻的矛盾 |
| `igbt-thyristor-wbg` | 功率半导体器件 | 超结 MOSFET、IGBT（电导调制、拖尾电流）、SiC 和 GaN、晶闸管（擎住、维持、只能控开通）和 GTO；开关损耗的线性估算（综合练习 1） |
| `diode-rectifiers` | 整流电路 | 单相半波、桥式全波二极管整流的平均电压（0.45、0.9 倍），电感负载下的方波电流 |
| `power-distortion` | 整流电路 | 有功功率、视在功率、功率因数；非正弦电流的谐波、总谐波畸变率、畸变因数和位移因数 |
| `phase-control` | 整流电路 | 晶闸管相控整流：触发角、电阻负载和大电感负载的平均电压、触发角大于 90° 时的有源逆变、半控桥、反并联晶闸管交流调压（AC/AC）（综合练习 2） |
| `commutation` | 整流电路 | 交流侧电感让换流不能瞬间完成：重叠角、换流压降 $2\omega L_s I_d/\pi$、相控时的换流、逆变的边界（最大触发角） |
| `three-phase-rectifier` | 整流电路 | 三相电源、相电压和线电压、三相桥式整流 $1.35V_{LL}\cos\alpha$、六脉波和 $6k \pm 1$ 次谐波（综合练习 2） |
| `buck-converter` | DC-DC变换器 | DC/DC 变换器的基本结构、标准开关单元、Buck（直接变换器）：伏秒平衡、占空比、电感电流纹波和输出电压纹波（综合练习 3） |
| `boost-buckboost` | DC-DC变换器 | Boost、Buck-Boost（间接变换器）、Cuk 和 SEPIC（综合练习 3） |
| `dcm` | DC-DC变换器 | 断续导通：临界条件、断续时的电压比 |
| `isolated-dcdc` | DC-DC变换器 | 正激变换器（磁复位、占空比上限）、反激变换器、推挽 |
| `square-wave-inverter` | 逆变器 | 全桥方波逆变器、基波 $4V_{dc}/\pi$ 和奇次谐波、移相（准方波）消 3 次谐波、单相功率在 2 倍频脉动和直流电容 |
| `three-phase-inverter` | 逆变器 | 三相电压型逆变器（六拍）、线电压、电流型逆变器、多电平（二极管钳位、级联 H 桥） |
| `spwm` | PWM控制 | 正弦脉宽调制：载波和调制波、调制比、线性区和过调制、谐波移到载波附近、单极性和双极性（综合练习 4） |
| `pwm-details` | PWM控制 | 三相 SPWM 的线电压、死区（桥臂互锁时间）、选择性谐波消除 |
| `svpwm-current` | PWM控制 | 空间矢量 PWM（8 个开关状态、15.5%）（综合练习 5）、逆变器电流控制（滞环、PI）、PWM 整流 |
| `snubbers` | 软开关 | 硬开关损耗、关断缓冲（RCD）、开通缓冲、复合缓冲 |
| `resonant-soft-switching` | 软开关 | 串联谐振槽路分析、谐振变换器的软开关（高于谐振频率时 ZVS）、谐振 DC/DC（串联谐振、LLC）、ZVS 和 ZCS、移相全桥（综合练习 6） |
| `averaged-models` | 变换器建模与控制 | 变换器的动态行为、动态模型、平均电路模型（开关换成受控源）、连续时间状态空间平均（综合练习 7 前半） |
| `linearization` | 变换器建模与控制 | 在工作点附近线性化、小信号传递函数、LC 双极点和 Q、Boost 的右半平面零点、采样数据模型 |
| `converter-control` | 变换器建模与控制 | 反馈控制、穿越频率和相位裕度的选法、补偿器、电流内环和电压外环（多环控制）、峰值电流控制的斜坡补偿、数字控制的延迟（综合练习 7 后半） |
| `magnetics-basics` | 磁性元件设计 | 磁通和磁感应强度、法拉第电磁感应定律、磁路和磁阻、电感 $L = N^2/\mathcal R = N^2A_L$、饱和、磁滞和剩磁、磁性材料（硅钢、铁氧体、铁粉芯） |
| `transformers-losses` | 磁性元件设计 | 变压器：励磁电感和漏感；磁性元件的损耗：绕组损耗和趋肤效应、铁芯损耗（Steinmetz 公式） |
| `magnetics-design` | 磁性元件设计 | 滤波电感设计和面积积、温升限制、电感储能和气隙（综合练习 8）、交流磁性元件（变压器）的面积积 |

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Power Electronic Circuits | `why-switching` |
| 1.2 | Power Semiconductor Switches | `why-switching` |
| 1.3 | Transformers | `why-switching`、`transformers-losses` |
| 2.1 | Functions of a Power Circuit | `why-switching` |
| 2.2 | AC/DC Converters | `why-switching`、`diode-rectifiers` |
| 2.3 | DC/DC Converters | `why-switching`、`buck-converter` |
| 2.4 | AC/AC Converters | `why-switching`、`phase-control` |
| 3.1 | Power in Electrical Networks | `power-distortion` |
| 3.2 | AC-Side Reactance and Current Commutation | `commutation` |
| 3.3 | Measures and Effects of Distortion | `power-distortion` |
| 4.1 | Phase Control with AC-Side Reactance | `phase-control`、`commutation` |
| 4.2 | Inversion Limits | `commutation` |
| 5.1 | The DC/DC Converter Topology | `buck-converter` |
| 5.2 | The Canonical Switching Cell | `buck-converter` |
| 5.3 | Direct Converter | `buck-converter` |
| 5.4 | Indirect Converter | `boost-buckboost` |
| 5.5 | Other PWM DC/DC Converters | `boost-buckboost` |
| 5.6 | Converter Operation with Discontinuous Conduction | `dcm` |
| 6.1 | Single-Ended Isolated Forward Converter | `isolated-dcdc` |
| 6.2 | Flyback Converter | `isolated-dcdc` |
| 7.1 | Basic Variable-Frequency Bridge Converter | `square-wave-inverter` |
| 7.2 | Harmonic Reduction | `square-wave-inverter`、`pwm-details` |
| 7.3 | Pulse-Width-Modulated DC/AC Converters | `spwm` |
| 7.4 | Current Control of Inverters | `svpwm-current` |
| 7.5 | Multi-level Converters | `three-phase-inverter` |
| 7.6 | Power Balance in Single-Phase DC/AC Converters | `square-wave-inverter` |
| 8.1 | Polyphase Sources | `three-phase-rectifier` |
| 8.2 | Phase-Controlled Three-Phase Converters | `three-phase-rectifier` |
| 8.3 | Three-Phase Inverters | `three-phase-inverter`、`pwm-details` |
| 8.4 | Space-Vector Representation and Modulation for Three-Phase Systems | `svpwm-current` |
| 8.5 | Multi-Level Inverters | `three-phase-inverter` |
| 9.1 | Resonant Converter Analysis | `resonant-soft-switching` |
| 9.2 | Soft Switching of Resonant Converters | `resonant-soft-switching` |
| 9.3 | Resonant DC/DC Converters | `resonant-soft-switching` |
| 10.1 | Dynamic Behavior of Power Converters | `averaged-models` |
| 10.2 | Dynamic Models | `averaged-models` |
| 10.3 | Averaged-Circuit Models | `averaged-models` |
| 10.4 | Linearized Models | `linearization` |
| 10.5 | Feedback Control | `converter-control` |
| 11.1 | Averaged-Circuit Models | `averaged-models` |
| 11.2 | Continuous-Time State-Space Models | `averaged-models` |
| 11.3 | Discrete-Time or Sampled-Data Models | `linearization` |
| 12.1 | Linearization | `linearization` |
| 12.2 | Analysis of Continuous-Time LTI Models | `linearization` |
| 12.3 | Feedback Control Design | `converter-control` |
| 12.4 | Multi-Loop Control | `converter-control` |
| 12.5 | Digital Control | `converter-control` |
| 13.1 | Simple Analysis of a Diode | `diode-mosfet-switch` |
| 13.2 | MOSFET | `diode-mosfet-switch` |
| 14.1 | Bipolar Diode | `diode-mosfet-switch` |
| 14.2 | Power MOSFET | `diode-mosfet-switch` |
| 14.3 | Superjunction MOSFET | `igbt-thyristor-wbg` |
| 14.4 | IGBT | `igbt-thyristor-wbg` |
| 14.5 | Silicon Carbide and Gallium Nitride Devices | `igbt-thyristor-wbg` |
| 14.6 | Thyristor | `igbt-thyristor-wbg` |
| 15.1 | Inductor | `magnetics-basics` |
| 15.2 | Saturation, Hysteresis, and Residual Flux | `magnetics-basics` |
| 15.3 | Losses In Magnetic Components | `transformers-losses` |
| 15.4 | Transformers | `transformers-losses` |
| 15.5 | Magnetic Material Properties | `magnetics-basics` |
| 16.1 | Filter Inductor Design and Core Factor | `magnetics-design` |
| 16.2 | Thermal Constraints in Magnetics Design | `magnetics-design` |
| 16.3 | Inductor Energy Storage Limits | `magnetics-design` |
| 16.4 | AC Magnetics Sizing and Core Area Product | `magnetics-design` |
| 17.1 | Winding Loss Calculation | `transformers-losses` |
| 17.2 | Core Loss | `transformers-losses` |
| 18.1 | Turn-Off Snubber | `snubbers` |
| 18.2 | Turn-On Snubber | `snubbers` |
| 18.3 | Combined Turn-On/Turn-Off Snubber | `snubbers` |
| 18.4 | Soft Switching | `resonant-soft-switching` |

## 中文主课的章节（C3）

西南交大 MOOC 第二至八章的概念，除下面三项外都在上表的课里：

- 4.x 单相、三相半控桥：只在 `phase-control` 里说明它不能有源逆变，不单独推导（Kassakian 不收半控桥，属于全控桥的特例）。
- 6.4 负载并联谐振型逆变电路：`three-phase-inverter` 讲电流型逆变器时一句带过（用于感应加热），不推导。
- 8.3 谐振直流环、8.5 零电压转换（ZVT）电路：`resonant-soft-switching` 只说明“辅助谐振让主开关在零电压下动作”这一共同思路，不画具体电路。

## CS2023 核心主题（C2）

`scope.json` 对 E.3.1 没有 CS2023 主题；8 个章由上表的课负责。

## 原技能树综合练习（C4）

| 小题 | 内容 | 由哪一课教到 |
|---|---|---|
| (1) | 各种器件的可控性和适用场合；开关损耗 $\frac12VI(t_r + t_f)f$ | `diode-mosfet-switch`、`igbt-thyristor-wbg` |
| (2) | 单相桥整流 $0.9V$、三相桥 $1.35V_{LL}$、全控桥 $0.9V\cos\alpha$ | `diode-rectifiers`、`phase-control`、`three-phase-rectifier` |
| (3) | Buck 的占空比和电感电流纹波，Boost 的占空比 | `buck-converter`、`boost-buckboost` |
| (4) | SPWM 的基波峰值和有效值、过调制产生低次谐波 | `spwm` |
| (5) | SVPWM 比 SPWM 多输出 15.5% 的线电压 | `svpwm-current` |
| (6) | 硬开关和软开关、ZVS 怎样减小损耗 | `snubbers`、`resonant-soft-switching` |
| (7) | Buck 的状态空间平均模型、LC 双极点频率、穿越频率的选法 | `averaged-models`、`linearization`、`converter-control` |
| (8) | 由 $A_L$ 算匝数、电感储能、为什么开气隙 | `magnetics-basics`、`magnetics-design` |

## 后继技能用到的写法（C5）

必须后继 E.3.6 新能源发电与储能还没有内容包；按它的章（光伏、最大功率点跟踪、并网变流器、储能和电池管理），Boost 和 Buck-Boost 的电压比由 `boost-buckboost` 负责，并网逆变器的 PWM、电流控制和单相功率脉动由 `spwm`、`svpwm-current`、`square-wave-inverter` 负责，PWM 整流（双向变流）由 `svpwm-current` 负责。
