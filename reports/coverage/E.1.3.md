# E.1.3 射频与高频电路：覆盖表

**状态（2026-11-27）：已写完（第 12 轮），30 课，大纲 39 节全部有课。** 依据 `../cs-math-skill-tree/data/outlines/E.1.3.json`（主来源 Razavi *RF Microelectronics* 第 2 版的目录；小信号调谐（窄带）放大器取 MIT 6.976 第 6 讲；中文主课是北华大学《高频电子线路》）和原技能树综合练习。数值核对脚本是 `tests/content/E.1.3.verify.py`。

前置：必须前置是 H.1.4 模拟电子技术（BJT、MOSFET、共射和共源放大器、跨导、负反馈、振荡器、巴克豪森判据、考毕兹振荡器一张卡）和 H.1.3 信号与系统（频谱、傅里叶变换和频移性质、带宽、分贝、功率谱密度、频率响应、极点零点），这些直接用（`node temp/closure-terms.mjs E.1.3`）。E.2.3 通信原理、E.1.2 微波工程与天线只是推荐前置，不继承：调幅、调频、载波、边带、调制指数、鉴频这些在本包里从头讲；反射系数和史密斯圆图只讲到匹配网络需要的程度；热噪声和噪声系数也在本包里讲（H.2.6 不是前置）。

## 课的安排（30 课）

| 章 | 课 | 内容 |
|---|---|---|
| 谐振回路与阻抗变换 | `rf-intro` | 射频电路做什么、频段划分、无线收发机的组成框图；射频里的单位（dBm、50 Ω）和为什么要谈非线性与时变 |
|  | `resonance` | 串联和并联谐振回路：谐振频率、品质因数、带宽和选择性，串并联等效变换（综合练习 1 前半） |
|  | `loaded-q-tapping` | 负载和信号源内阻对 Q 的影响，部分接入（抽头、电容分压）和接入系数（综合练习 1 后半） |
|  | `impedance-matching` | 最大功率传输和共轭匹配，L 型匹配网络，反射系数和史密斯圆图入门，匹配网络的损耗 |
| 小信号调谐放大器 | `tuned-amplifier` | 单调谐回路谐振放大器的增益、带宽、矩形系数，多级同步调谐（综合练习 2），稳定性和中和；宽带放大器的并联峰化 |
|  | `rf-noise` | 热噪声 kTB、噪声系数和噪声温度、级联的 Friis 公式，灵敏度（-174 dBm/Hz + NF + 10lgB + 所需信噪比） |
|  | `nonlinearity` | 谐波、增益压缩和 1 dB 压缩点、互调和三阶截点 IP3、级联 IIP3，动态范围 |
|  | `lna` | 低噪声放大器：为什么要 50 Ω 输入匹配，共源加源极电感、共栅、电阻反馈几种结构的输入阻抗和噪声 |
| 高频功率放大器 | `pa-classes` | 功放的指标（输出功率、效率、线性度），甲、乙、丙类和导通角，最大输出功率 V²/(2R)（综合练习 3） |
|  | `class-c` | 丙类功放：余弦电流脉冲分解系数、功率和效率随导通角的变化，欠压、临界、过压和负载特性，大信号下的负载选择 |
|  | `pa-efficiency-linearization` | 开关类功放（D、E、F 类），峰均比和回退，线性化：反馈、前馈、预失真、包络消除与恢复 |
| 正弦波振荡器 | `oscillator-principles` | 反馈振荡的条件（复习巴克豪森判据）、起振和稳幅、负阻观点，振荡器的指标，互感耦合振荡器 |
|  | `three-point` | 三点式振荡器的组成法则，电容三点式（考毕兹）和电感三点式（哈特莱）的频率和起振（综合练习 4），克拉泼、西勒和晶体振荡器 |
|  | `cross-coupled-vco` | 交叉耦合振荡器的负阻、变容管和压控振荡器的增益 K_VCO、调谐范围，正交振荡器 |
|  | `phase-noise` | 相位噪声的定义（dBc/Hz）、对接收的影响（倒易混频），Leeson 模型的直观结论 |
| 混频器 | `mixer-basics` | 混频就是乘法：频谱搬移、中频、变频增益、噪声系数、端口隔离，镜像频率（综合练习 5） |
|  | `mixer-circuits` | 无源开关混频器、有源单平衡和双平衡（吉尔伯特单元）混频器，改进的结构 |
|  | `mixer-spurs` | 变频的失真与干扰：组合频率干扰、中频和镜像等副波道干扰、交调和互调 |
| 调幅与检波 | `am-theory` | 调幅波的表达式、调幅度、频谱和功率分配（综合练习 6），双边带和单边带 |
|  | `am-circuits` | 低电平调幅（乘法器）和高电平调幅（集电极调幅），单边带信号的产生（滤波法、相移法） |
|  | `am-detection` | 包络检波器和 RC 的选择（综合练习 6），惰性失真和负峰切割失真，同步检波 |
| 调频与鉴频 | `angle-modulation` | 调频和调相的表达式、频偏和调制指数、频谱和贝塞尔函数、卡森带宽（综合练习 7） |
|  | `fm-circuits` | 直接调频（变容管）和间接调频（由调相得到），调相电路，倍频扩展频偏 |
|  | `fm-demod` | 限幅和鉴频：斜率鉴频、相位鉴频、比例鉴频和正交鉴频（综合练习 7） |
| 锁相环与频率合成 | `pll-basics` | 自动增益控制和自动频率控制，锁相环的组成（鉴相器、环路滤波器、压控振荡器），I 型锁相环的锁定和相位误差 |
|  | `pll-dynamics` | 电荷泵和鉴频鉴相器，II 型锁相环，环路带宽和阻尼，锁相环里的相位噪声 |
|  | `integer-n` | 整数分频频率合成器：输出频率和步进（综合练习 8）、参考杂散、分频器和双模预分频（吞脉冲计数器） |
|  | `fractional-n-dds` | 小数分频：用平均分频比得到细步进，随机化和噪声整形；直接数字频率合成（DDS） |
| 射频收发机结构 | `receivers` | 超外差接收机和镜像抑制（综合练习 5），零中频和低中频接收机的问题（直流失调、闪烁噪声、镜像），镜像抑制接收机 |
|  | `transmitters` | 直接变频和两步变频发射机，极坐标发射机，发射机的指标（输出功率、频谱模板、邻道泄漏） |

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | General Considerations | `rf-intro` |
| 1.2 | Effects of Nonlinearity | `nonlinearity` |
| 1.3 | Noise | `rf-noise` |
| 1.4 | Sensitivity and Dynamic Range | `rf-noise`、`nonlinearity` |
| 1.5 | Passive Impedance Transformation | `resonance`、`loaded-q-tapping`、`impedance-matching` |
| 2.1.1 | Amplitude Modulation | `am-theory`、`am-circuits`、`am-detection` |
| 2.1.2 | Phase and Frequency Modulation | `angle-modulation`、`fm-circuits`、`fm-demod` |
| 3.1 | General Considerations | `rf-intro`、`receivers` |
| 3.2 | Receiver Architectures | `am-detection`、`fm-demod`、`receivers` |
| 3.3 | Transmitter Architectures | `transmitters` |
| 4.1 | General Considerations | `lna` |
| 4.2 | Problem of Input Matching | `lna` |
| 4.3 | LNA Topologies | `lna` |
| 5.1 | General Considerations | `mixer-basics`、`mixer-spurs` |
| 5.2 | Passive Downconversion Mixers | `mixer-circuits` |
| 5.3 | Active Downconversion Mixers | `mixer-circuits` |
| 5.4 | Improved Mixer Topologies | `mixer-circuits` |
| 6.1 | Performance Parameters | `oscillator-principles` |
| 6.2 | Basic Principles | `oscillator-principles` |
| 6.3 | Cross-Coupled Oscillator | `cross-coupled-vco` |
| 6.4 | Three-Point Oscillators | `three-point` |
| 6.5 | Voltage-Controlled Oscillators | `cross-coupled-vco` |
| 6.6 | Phase Noise | `phase-noise` |
| 6.7 | Quadrature Oscillators | `cross-coupled-vco` |
| 7.1 | Basic Concepts | `pll-basics` |
| 7.2 | Type-I PLLs | `pll-basics` |
| 7.3 | Type-II PLLs | `pll-dynamics` |
| 7.4 | Phase Noise in PLLs | `pll-dynamics` |
| 8.1 | General Considerations | `integer-n` |
| 8.2 | Basic Integer-N Synthesizer | `integer-n` |
| 8.3 | Divider Design | `integer-n` |
| 9.1 | Basic Concepts | `fractional-n-dds` |
| 9.2 | Randomization and Noise Shaping | `fractional-n-dds` |
| 10.1 | General Considerations | `pa-classes` |
| 10.2 | Classification of Power Amplifiers | `pa-classes`、`class-c` |
| 10.3 | High-Efficiency Power Amplifiers | `pa-efficiency-linearization` |
| 10.4 | Large-Signal Impedance Matching | `class-c`、`pa-efficiency-linearization` |
| 10.5 | Basic Linearization Techniques | `pa-efficiency-linearization` |
| 11 | Enhancement of Broadband Amplifiers, Narrowband Amplifiers | `tuned-amplifier` |

## CS2023 核心主题（C2）

`scope.json` 没有给 E.1.3 匹配 CS2023 主题，也没有附注。它属于电子信息类的专业课（国标通信工程专业示例二的“高频电子线路”），不在 CS2023 的范围里。

## 学习资源的章节（C3）

已逐条核对：

| 资源的小节 | 去处 |
|---|---|
| 北华《高频电子线路》1.3 无线通信的基本要求、系统组成、电波传播与频段 | `rf-intro`（载波、调制、频段和波长、收发机框图）；电波传播只讲到“天线尺寸和波长相当”，传播模型不教：属于 E.1.2 微波工程与天线和 E.2.4 无线与移动通信 |
| 2.1 串并联谐振回路、2.2 阻抗变换电路 | `resonance`、`loaded-q-tapping`（部分接入、接入系数）、`impedance-matching` |
| 3.1 单调谐回路谐振放大器、3.2 放大电路的噪声 | `tuned-amplifier`（增益、带宽、矩形系数、多级同步调谐、稳定性和中和）、`rf-noise`（热噪声、噪声系数、Friis、灵敏度） |
| 4.1–4.5 丙类功放的工作原理、余弦脉冲分解、功率和效率、动态特性、负载特性 | `pa-classes`、`class-c`（分解系数、$\eta = \tfrac12\xi g_1$、欠压临界过压和负载特性）；动态特性曲线只讲到三种状态的物理意义 |
| 5.1–5.5 反馈型 LC 振荡器、互感耦合、三点式、电容三点式计算、高稳定度电容三点式 | `oscillator-principles`、`three-point`（组成法则、考毕兹、哈特莱、克拉泼、西勒、晶体） |
| 6.1–6.7 调幅、低电平和高电平调幅、单边带、包络检波、同步检波 | `am-theory`、`am-circuits`、`am-detection`（惰性失真、负峰切割失真的条件） |
| 7.1–7.5 调角波、调频和调相电路、调角信号的解调、鉴频器 | `angle-modulation`、`fm-circuits`、`fm-demod` |
| 8.1–8.3 变频概述、混频电路、失真与干扰 | `mixer-basics`、`mixer-circuits`、`mixer-spurs`（干扰哨声、中频和镜像干扰、交调、互调） |
| 9.1–9.4 自动增益控制、自动频率控制、锁相环及其应用 | `pll-basics`（AGC、AFC、锁相环组成）、`pll-dynamics`、`integer-n`、`fractional-n-dds`；锁相环用于同步检波在 `am-detection` 提到 |
| 四川信息职院 项目一 发射机和接收机组成 | `rf-intro`、`receivers`、`transmitters` |
| 项目五 锁相环原理和特性、频率合成器指标和方案、DDS | `pll-basics`、`pll-dynamics`、`integer-n`、`fractional-n-dds` |
| MIT 6.976 L4 反射系数、史密斯圆图、无源元件 | `impedance-matching`；传输线理论只讲到特性阻抗和反射系数的定义，不教：属于 E.1.1 电磁场与电磁波、E.1.2 |
| L6 宽带放大器的增强、窄带放大器 | `tuned-amplifier`（并联峰化、调谐放大器） |
| L7、L9 放大器的噪声建模、低噪声放大器 | `rf-noise`、`lna`；器件噪声模型的推导不教（H.2.6 模拟集成电路设计讲 MOS 管的噪声） |
| L10 混频器，L11–L12 压控振荡器和它的噪声 | `mixer-basics`、`mixer-circuits`、`cross-coupled-vco`、`phase-noise` |
| L15–L18 整数分频、噪声、高级频率合成器、设计与仿真 | `integer-n`、`pll-dynamics`、`fractional-n-dds`；仿真工具的使用不教 |
| L19–L20 无线通信基础和性能指标 | `rf-noise`（灵敏度）、`nonlinearity`（动态范围）、`transmitters`（ACPR、EVM） |
| Madhow 3.2 调幅和包络检波、3.3 调角、限幅鉴频、FM 频谱、3.4 超外差 | `am-theory`、`am-detection`、`angle-modulation`、`fm-demod`、`receivers` |

## 综合练习（C4）

| 小题 | 负责的课 |
|---|---|
| (1) 并联谐振回路的谐振频率、Q、带宽，接负载和部分接入 | `resonance`、`loaded-q-tapping` |
| (2) 调谐放大器的增益带宽矛盾，多级同步调谐的总带宽 | `tuned-amplifier` |
| (3) 丙类功放的效率和输出功率，最大输出功率 | `pa-classes`、`class-c` |
| (4) 考毕兹振荡器的频率和起振条件 | `three-point` |
| (5) 超外差接收机的中频、镜像频率和镜像抑制 | `mixer-basics`、`receivers` |
| (6) 调幅波的频谱、边带功率比例，包络检波器的 RC | `am-theory`、`am-detection` |
| (7) 调频的调制指数、卡森带宽，鉴频器的作用 | `angle-modulation`、`fm-demod` |
| (8) 锁相环频率合成器的输出范围和步进 | `integer-n` |

## 后继技能用到的（C5）

E.1.3 没有直接解锁的技能，是通信工程远征的一站（国标通信工程专业示例二的“高频电子线路”）。它是 E.1.5 射频集成电路设计的推荐前置，但 E.1.5 只以 H.2.6 为必须前置，所以 E.1.5 不能假定读者学过本包。
