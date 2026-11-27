# E.1.5 射频集成电路设计：覆盖表

**状态（2026-11-27）：已写完（23 课，大纲 64 节中 54 节有课，10 节高阶或设计实例注理由不教）。** 依据 `vendor/cs-math-skill-tree/output/outlines.json`（主来源 Behzad Razavi *RF Microelectronics*, 2nd ed. 第 2、4、5、6、7、8、9、10、12 章；英文主课 MIT 6.976 *High Speed Communication Circuits and Systems*；中文来源杭州电子科技大学《射频放大器设计——理论与实践》、北华大学《高频电子线路》、四川信息职业技术学院《高频电子技术》）和原技能树综合练习。数值核对脚本为 `tests/content/E.1.5.verify.py`。

前置：必须前置只有 H.2.6 模拟集成电路设计（其闭包含 H.1.4 模拟电子技术、H.1.1 电路分析与基础电子学、M.3.1 线性代数、M.1.1–M.1.3 微积分，已讲 MOSFET 小信号模型、跨导、本征增益、共源/共栅/共源共栅、差分对、吉尔伯特单元、密勒效应、热噪声、闪烁噪声、负反馈、相位裕度、巴克豪森判据、甲/乙/甲乙类输出级等）。E.1.3 微波工程与天线、E.1.2 高频电路、H.1.3 信号与系统不在必须前置中，不继承：dBm、噪声系数与弗里斯公式、灵敏度与动态范围、超外差/零中频/低中频、电感源极退化 LNA、无源与有源混频器、相位噪声与利森公式、II 型电荷泵锁相环、整数 N/小数 N 综合器、大信号负载线与高效率功放、L 形阻抗匹配与 S 参数、片上螺旋电感 Q 值、P1dB 与 IIP3/OIP3 均在本包内从头讲清。

## 课的安排（23 课）

| 章 | 课 | 内容 |
|---|---|---|
| 射频收发机架构 | `rf-foundations` | 射频设计基本权衡、dBm、热噪声基底、噪声系数、弗里斯公式、接收机灵敏度与动态范围（综合练习 2） |
|  | `rx-architectures` | 本振、中频与镜像频率；超外差、零中频（直流失调、本振泄漏自混频、闪烁噪声）与低中频接收机架构（综合练习 1） |
|  | `tx-architectures` | 直接上变频与两步上变频发射机、本振牵引与载波馈通抑制、频率规划 |
| 低噪声放大器 | `lna-matching` | LNA 在接收链路最前端的作用、输入 50 Ω 阻抗匹配挑战与有损电阻匹配的 3 dB 噪声底限 |
|  | `lna-topologies` | 共栅 LNA、电感源极退化共源共栅 LNA（$\text{Re}(Z_{\text{in}})=\omega_T L_s$ 与谐振电感 $L_g$）及并联反馈宽带 LNA（综合练习 3） |
|  | `lna-switching-ip2` | 强信号防饱和增益切换、多频段切换、偶次非线性与高 IIP2 差分 LNA |
| 混频器 | `mixer-basics-passive` | 频谱搬移与变频增益、端口隔离度、SSB 与 DSB 噪声系数差异、无源 MOS 开关混频器（电压变频损耗 $2/\pi$） |
|  | `active-mixers` | 单平衡有源混频器与双平衡射频吉尔伯特混频器的变频增益、端口馈通抑制与电压裕度 |
|  | `mixer-improved-upconv` | 电流泄放与折迭式改进混频器、正交上变频混频器与单边带镜像抵消 |
| 压控振荡器与相位噪声 | `oscillator-lc-topologies` | 射频振荡器性能指标、LC 谐振腔并联损耗电阻 $R_p$、交叉耦合负阻起振条件与科尔皮兹/哈特莱三点式振荡器（综合练习 4 前半） |
|  | `vco-tuning-quadrature` | 压控振荡器与压控增益 $K_{\text{VCO}}$、开关电容阵列宽调谐、本振缓冲接口与正交本振产生 |
|  | `vco-phase-noise` | 相位噪声定义（dBc/Hz）、倒易混频危害、利森公式三大频区斜率与降噪方向（综合练习 4 后半） |
| 锁相环频率综合器 | `pll-type1-type2` | 锁相环闭环相位跟踪、I 型锁相环的静态相偏局限、II 型鉴频鉴相器/电荷泵锁相环的零点稳定与阻尼比 |
|  | `pll-noise-bandwidth` | PFD 死区与电荷泵失配产生的参考杂散、带内/带外相位噪声传递特性与最优环路带宽权衡 |
|  | `integer-n-synthesizer` | 整数 N 频率综合器步进与建立时间约束、杂散抑制、高速预分频器与小数 N 分频动机（综合练习 5） |
| 射频功率放大器 | `pa-loadline-classes` | 漏极效率与 PAE、低压电源下最大输出功率与最佳负载电阻变换、导通角与甲/乙/甲乙/丙类功放（综合练习 6） |
|  | `pa-high-efficiency` | 开关型丁/戊/己类高效率功放原理、共源共栅耐压输出级与大信号负载线阻抗匹配 |
|  | `pa-linearization-doherty` | 高峰均比信号与功率回退效率损耗、数字预失真等线性化技术及 Doherty 有源负载调制架构 |
| 阻抗匹配与片上无源器件 | `impedance-matching` | 共轭匹配、串并联等效与品质因数 $Q$、L 形匹配网络设计与 $\pi$/T 匹配带宽调控 |
|  | `s-parameters-tlines` | 传输线特征阻抗与四分之一波长变换器、反射系数与回波损耗、二端口散射参数（$S_{11},S_{21},S_{12},S_{22}$） |
|  | `onchip-passives` | 片上螺旋电感 $Q$ 值受金属趋肤损耗与衬底涡流/电容限制、自谐振频率、片上变压器、变容管与 MIM/MOM 电容（综合练习 7） |
| 非线性与线性度指标 | `nonlinearity-p1db-ip3` | 弱非线性幂级数、增益压缩与 $P_{1\text{dB}}$、双音测试三阶交调 IM3 与 IIP3/OIP3 快捷换算及 9.6 dB 经验差（综合练习 8） |
|  | `cascaded-linearity-sfdr` | 多级接收链路级联 IIP3 公式、前级增益对后级线性度的放大效应、LNA 非线性计算与无杂散动态范围（SFDR） |

## 1. 教材目录逐节覆盖（C1）

| 节 | 大纲原文（Razavi *RF Microelectronics* 2nd ed.） | 覆盖课或理由 |
|---|---|---|
| 1.1 | 2.1 General Considerations | `rf-foundations` |
| 1.2 | 2.2 Effects of Nonlinearity | `nonlinearity-p1db-ip3` |
| 1.3 | 2.3 Noise | `rf-foundations` |
| 1.4 | 2.4 Sensitivity and Dynamic Range | `rf-foundations`, `cascaded-linearity-sfdr` |
| 1.5 | 2.5 Passive Impedance Transformation | `impedance-matching` |
| 1.6 | 2.6 Scattering Parameters | `s-parameters-tlines` |
| 1.7 | 2.7 Analysis of Nonlinear Dynamic Systems | 不教：超出入门层（动态记忆型非线性系统涉及高阶微分方程分析，入门层聚焦无记忆弱非线性幂级数） |
| 1.8 | 2.8 Volterra Series | 不教：超出入门层（沃尔泰拉级数属研究生高阶射频专题，入门层用三阶幂级数已足够覆盖 P1dB 与 IIP3） |
| 2.1 | 4.1 General Considerations | `rf-foundations` |
| 2.2 | 4.2 Receiver Architectures | `rx-architectures` |
| 2.3 | 4.3 Transmitter Architectures | `tx-architectures` |
| 2.4 | 4.4 OOK Transceivers | 不教：属超低功耗窄带特例（开关键控收发机在通用无线通信中占比较小，架构部分聚焦超外差、零中频与低中频主线） |
| 3.1 | 5.1 General Considerations | `lna-matching` |
| 3.2 | 5.2 Problem of Input Matching | `lna-matching` |
| 3.3 | 5.3 LNA Topologies | `lna-topologies` |
| 3.4 | 5.4 Gain Switching | `lna-switching-ip2` |
| 3.5 | 5.5 Band Switching | `lna-switching-ip2` |
| 3.6 | 5.6 High-IP2 LNAs | `lna-switching-ip2` |
| 3.7 | 5.7 Nonlinearity Calculations | `cascaded-linearity-sfdr` |
| 4.1 | 6.1 General Considerations | `mixer-basics-passive` |
| 4.2 | 6.2 Passive Downconversion Mixers | `mixer-basics-passive` |
| 4.3 | 6.3 Active Downconversion Mixers | `active-mixers` |
| 4.4 | 6.4 Improved Mixer Topologies | `mixer-improved-upconv` |
| 4.5 | 6.5 Upconversion Mixers | `mixer-improved-upconv` |
| 5.1 | 7.1 General Considerations | `onchip-passives` |
| 5.2 | 7.2 Inductors | `onchip-passives` |
| 5.3 | 7.3 Transformers | `onchip-passives` |
| 5.4 | 7.4 Transmission Lines | `s-parameters-tlines` |
| 5.5 | 7.5 Varactors | `onchip-passives` |
| 5.6 | 7.6 Constant Capacitors | `onchip-passives` |
| 6.1 | 8.1 Performance Parameters | `oscillator-lc-topologies` |
| 6.2 | 8.2 Basic Principles | `oscillator-lc-topologies` |
| 6.3 | 8.3 Cross-Coupled Oscillator | `oscillator-lc-topologies` |
| 6.4 | 8.4 Three-Point Oscillators | `oscillator-lc-topologies` |
| 6.5 | 8.5 Voltage-Controlled Oscillators | `vco-tuning-quadrature` |
| 6.6 | 8.6 LC VCOs with Wide Tuning Range | `vco-tuning-quadrature` |
| 6.7 | 8.7 Phase Noise | `vco-phase-noise` |
| 6.8 | 8.8 Design Procedure | 不教：属具体工艺版图迭代流程（核心振荡频率、起振负阻、调谐范围与相噪约束已在各振荡器课中覆盖） |
| 6.9 | 8.9 LO Interface | `vco-tuning-quadrature` |
| 6.10 | 8.10 Mathematical Model of VCOs | 不教：超出入门层（线性时变相位冲激灵敏度函数等严格数学模型属研究生专题，入门层掌握压控模型与利森公式即可） |
| 6.11 | 8.11 Quadrature Oscillators | `vco-tuning-quadrature` |
| 7.1 | 9.1 Basic Concepts | `pll-type1-type2` |
| 7.2 | 9.2 Type-I PLLs | `pll-type1-type2` |
| 7.3 | 9.3 Type-II PLLs | `pll-type1-type2` |
| 7.4 | 9.4 PFD/CP Nonidealities | `pll-noise-bandwidth` |
| 7.5 | 9.5 Phase Noise in PLLs | `pll-noise-bandwidth` |
| 7.6 | 9.6 Loop Bandwidth | `pll-noise-bandwidth` |
| 7.7 | 9.7 Design Procedure | 不教：属具体工艺迭代设计手册（II 型锁相环自然频率、阻尼比与环路带宽权衡已在前面三课中讲清） |
| 8.1 | 10.1 General Considerations | `integer-n-synthesizer` |
| 8.2 | 10.2 Basic Integer-N Synthesizer | `integer-n-synthesizer` |
| 8.3 | 10.3 Settling Behavior | `integer-n-synthesizer` |
| 8.4 | 10.4 Spur Reduction Techniques | `integer-n-synthesizer` |
| 8.5 | 10.5 PLL-Based Modulation | 不教：属专门调制发射机技巧（锁相环两点调制与预加重属进阶专题，发射机主线已在发射机架构课覆盖） |
| 8.6 | 10.6 Divider Design | `integer-n-synthesizer` |
| 9.1 | 12.1 General Considerations | `pa-loadline-classes` |
| 9.2 | 12.2 Classification of Power Amplifiers | `pa-loadline-classes` |
| 9.3 | 12.3 High-Efficiency Power Amplifiers | `pa-high-efficiency` |
| 9.4 | 12.4 Cascode Output Stages | `pa-high-efficiency` |
| 9.5 | 12.5 Large-Signal Impedance Matching | `pa-high-efficiency` |
| 9.6 | 12.6 Basic Linearization Techniques | `pa-linearization-doherty` |
| 9.7 | 12.7 Polar Modulation | 不教：属高阶发射机线性化变体（极坐标调制需严控幅相路径延时校准，入门层聚焦数字预失真与 Doherty 架构） |
| 9.8 | 12.8 Outphasing | 不教：属专门大信号功率合成拓扑（异相合成依赖复杂合路器与相位校准，超出入门层范围） |
| 9.9 | 12.9 Doherty Power Amplifier | `pa-linearization-doherty` |
| 9.10 | 12.10 Design Examples | 不教：属特定工艺完整芯片实例（无新增原理概念，入门层已用独立例题与练习覆盖负载线、匹配与效率计算） |

## 2. 权威课程标准（C2）

EE/ECE 领域无 CS2023 对应条文，按 MIT 6.976 / Razavi *RF Microelectronics*（2nd ed.）及中国大学 MOOC《射频放大器设计》《高频电子线路》的射频集成电路核心教学大纲对照：

| 主题领域 | 核心概念与技能 | 对应课 |
|---|---|---|
| 射频系统与架构 | dBm、噪声系数与弗里斯公式、灵敏度、动态范围；超外差、零中频与低中频收发机 | `rf-foundations`, `rx-architectures`, `tx-architectures` |
| 低噪声放大器 | 50 Ω 输入匹配、共栅与电感源极退化 LNA、增益/频段切换与高 IIP2 | `lna-matching`, `lna-topologies`, `lna-switching-ip2` |
| 混频器 | 变频增益、端口隔离、SSB/DSB NF、无源开关混频器、单/双平衡有源吉尔伯特混频器与上变频 | `mixer-basics-passive`, `active-mixers`, `mixer-improved-upconv` |
| 振荡器与相位噪声 | LC 谐振腔负阻起振、交叉耦合与三点式拓扑、变容管与开关电容阵宽调谐、相位噪声与利森公式 | `oscillator-lc-topologies`, `vco-tuning-quadrature`, `vco-phase-noise` |
| 锁相环与频率综合器 | I 型与 II 型电荷泵锁相环、PFD/CP 杂散、噪声传递与环路带宽、整数 N 与小数 N 分频 | `pll-type1-type2`, `pll-noise-bandwidth`, `integer-n-synthesizer` |
| 功率放大器 | 最佳负载电阻与电源电压约束、甲/乙/甲乙/丙/丁/戊/己类效率、共源共栅耐压、DPD 与 Doherty | `pa-loadline-classes`, `pa-high-efficiency`, `pa-linearization-doherty` |
| 匹配与片上无源器件 | 串并联等效与 L/π/T 匹配、传输线与 S 参数、片上螺旋电感损耗机理与 Q 值、变压器与电容 | `impedance-matching`, `s-parameters-tlines`, `onchip-passives` |
| 非线性与线性度 | $P_{1\text{dB}}$、双音测试 IM3 与 IIP3/OIP3、级联 IIP3 与 SFDR | `nonlinearity-p1db-ip3`, `cascaded-linearity-sfdr` |

## 3. 中文与国际对照（C3）

- 中文课程（杭州电子科技大学《射频放大器设计——理论与实践》、北华大学《高频电子线路》、四川信息职业技术学院《高频电子技术》）强调传输线与 L/π/T 匹配网络、高频丙类功放、三点式 LC 振荡器（科尔皮兹/哈特莱）与锁相环工程实现，已全部融入 `impedance-matching`、`s-parameters-tlines`、`oscillator-lc-topologies`、`pa-loadline-classes` 与 `integer-n-synthesizer`。
- 英文课程（MIT 6.976 与 Razavi 教材）的 CMOS 片上集成核心——电感源极退化 LNA、无源电流模混频器、交叉耦合 LC VCO 与开关电容阵、利森相位噪声与倒易混频、II 型电荷泵锁相环噪声传递、低压功放负载变换与 Doherty 架构、片上螺旋电感衬底涡流损耗、级联 IIP3 与 SFDR——已完整覆盖。

## 4. 原技能树综合练习（C4）

课内例题和随堂练习全部使用独立参数，原 8 道综合练习题全部以可自动判分题目进入结业 `boss`：

| 题 | 原综合练习 | 对应课 | 结业 boss 题 |
|---|---|---|---|
| (1) | 比较超外差、零中频和低中频优缺点；零中频直流失调与本振泄漏原因 | `rx-architectures` | `b-rx-arch`, `b-zeroif-dc` |
| (2) | 接收链路 LNA(1.5/15 dB)、混频器(10/5 dB)、中频(12 dB) 弗里斯总噪声系数与 LNA 前置原因 | `rf-foundations`, `lna-matching` | `b-friis-nf`, `b-lna-first` |
| (3) | 电感源极退化 LNA：$\omega_T=2\pi\times 50\text{ GHz}$ 匹配 50 Ω 求 $L_s$；2.4 GHz、$C_{gs}=100\text{ fF}$ 求 $L_g$ | `lna-topologies` | `b-lna-ls`, `b-lna-lg` |
| (4) | LC VCO（2 nH, 2.2 pF）求振荡频率；$-120\text{ dBc/Hz @ 1 MHz}$ 含义与利森降噪方向 | `oscillator-lc-topologies`, `vco-phase-noise` | `b-vco-freq`, `b-leeson-pn` |
| (5) | 整数 N 锁相环频率分辨率决定因素与小数 N 分频原因 | `integer-n-synthesizer` | `b-intn-fracn` |
| (6) | 1.8 V 电源直驱 50 Ω 最大功率（dBm）、23 dBm 所需负载电阻及甲/乙类理论最大效率 | `pa-loadline-classes` | `b-pa-pmax`, `b-pa-ropt`, `b-pa-eff` |
| (7) | 片上螺旋电感 Q 值不高的原因及限制它的损耗机制 | `onchip-passives` | `b-inductor-q` |
| (8) | 双音测试每音 $-30\text{ dBm}$、基波 $-10\text{ dBm}$、IM3 $-70\text{ dBm}$ 求增益/OIP3/IIP3 及 $P_{1\text{dB}}$ 差值 | `nonlinearity-p1db-ip3` | `b-iip3-calc`, `b-p1db-gap` |

## 5. 后继节点的需要（C5）

E.1.5 位于通信工程远征的收官电路深度节点，后续若学习高级射频/毫米波前端、射频系统级联预算或无线移动通信硬件实现（E.2.4 无线与移动通信中的射频前端约束），需要牢固掌握：收发机架构取舍、弗里斯噪声级联、电感源极退化匹配、无源/有源混频器与 I/Q 镜像抑制、相位噪声与倒易混频、锁相环环路带宽与综合器步进、功放效率–线性度权衡、S 参数与 L 形匹配、以及 $P_{1\text{dB}}$/IIP3/SFDR 指标计算，本包 23 课与 18 题结业测验已全部覆盖。
