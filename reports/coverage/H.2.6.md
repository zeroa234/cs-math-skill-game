# H.2.6 模拟集成电路设计：覆盖表

**状态（2026-11-27）：已写完（第 11 轮写覆盖表和 22 课草稿，第 12 轮写结业挑战、术语和 verify.py），22 课，大纲 16 节全部有课。** 依据 `../cs-math-skill-tree/data/outlines/H.2.6.json`（主来源 Razavi《Design of Analog CMOS Integrated Circuits》第 2 版；采样和数据转换器取 CppSim 公开讲座的 Sampling、D/A、A/D 三讲）和原技能树综合练习。数值核对脚本是 `tests/content/H.2.6.verify.py`。

前置：必须前置只有 H.1.4 模拟电子技术，它已经讲过 MOSFET、阈值电压、过驱动电压、三极管区、饱和区、跨导、沟道长度调制、体效应、共源放大器、源极跟随器、差分放大器、共模抑制比、失调电压、本征增益、共源共栅、电流镜、有源负载、密勒效应、开路时间常数法、主极点、负反馈、环路增益、相位裕度、频率补偿（`node temp/closure-terms.mjs H.2.6`），这些词直接用，本包往深处讲（输出电阻、小信号推导、五管差分对、两级运放、补偿、噪声）。H.2.5 只是推荐前置，不继承：短沟道效应、亚阈值导通要在本包里讲。

## 课的安排（22 课）

| 章 | 课 | 内容 |
|---|---|---|
| MOS器件模型与小信号分析 | `analog-intro` | 为什么还要模拟电路、模拟设计的折中（增益、速度、功耗、噪声、线性度、电源电压），从 H.1.4 的平方律接上 |
| | `mos-large-signal` | 平方律复习、饱和条件、沟道长度调制、体效应、器件电容（$C_{GS}$、$C_{GD}$、$C_{DB}$）的来源 |
| | `mos-small-signal` | 小信号模型 $g_m$、$r_o$、$g_{mb}$ 的三种写法，本征增益（综合练习 1） |
| | `short-channel-gmid` | 速度饱和、迁移率退化、亚阈值导通、$g_m/I_D$ 设计法 |
| 单级与差分放大器 | `cs-stage` | 共源级：电阻负载、二极管接法负载、电流源负载、源极负反馈（综合练习 2 前半） |
| | `sf-cg` | 源极跟随器的增益和输出电阻、共栅级的输入电阻 |
| | `cascode` | 共源共栅级的输出电阻和增益、折叠共源共栅 |
| | `diff-pair` | 差分对的大信号特性、小信号增益、共模响应和失配 |
| | `five-transistor-ota` | 电流镜负载的差分对（五管单元）的增益，吉尔伯特单元一句话（综合练习 2 后半） |
| 电流镜与偏置 | `current-mirrors` | 基本电流镜、比例、沟道长度调制带来的误差（综合练习 3） |
| | `cascode-mirrors` | 共源共栅电流镜、低压共源共栅、偏置电路 |
| 频率响应与稳定性 | `freq-miller` | 密勒定理、极点和节点的对应、共源级的频率响应（综合练习 4） |
| | `freq-stages` | 源极跟随器、共栅级、共源共栅级的频率响应，差分对的频率响应 |
| | `feedback` | 反馈的作用（增益降敏、带宽、输入输出阻抗），四种拓扑，环路增益的算法 |
| | `stability` | 波特图、相位裕度和闭环响应、主极点补偿 |
| 噪声分析 | `noise-basics` | 噪声的统计描述、功率谱密度、热噪声、闪烁噪声、MOS 管的噪声（综合练习 6 前半） |
| | `noise-circuits` | 等效输入噪声、共源级和差分对的噪声、kT/C 噪声（综合练习 6 后半） |
| 运算放大器设计与补偿 | `opamp-specs` | 运放的指标、单级运放（套筒式、折叠式）、两级运放、增益提升、输出摆幅 |
| | `miller-compensation` | 两级运放的密勒补偿、极点分裂、右半平面零点和调零电阻、压摆率（综合练习 5） |
| 带隙基准 | `bandgap` | 与电源无关的偏置、CTAT 的 $V_{BE}$、PTAT 的 $\Delta V_{BE}$、带隙基准电路（综合练习 7） |
| 开关电容与数据转换器概述 | `switched-cap` | MOS 开关、采样保持、开关电容等效电阻、开关电容放大器和积分器（综合练习 8 前半） |
| | `dac-adc` | 数模转换器（电阻串、电流舵、电容阵列），模数转换器（Flash、SAR、流水线），量化噪声（综合练习 8 后半） |

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1 | Introduction to Analog Design | `analog-intro` |
| 2 | Basic MOS Device Physics | `mos-large-signal`、`mos-small-signal` |
| 3 | Single-Stage Amplifiers | `cs-stage`、`sf-cg`、`cascode` |
| 4 | Differential Amplifiers | `diff-pair`、`five-transistor-ota` |
| 5 | Current Mirrors and Biasing Techniques | `current-mirrors`、`cascode-mirrors` |
| 6 | Frequency Response of Amplifiers | `freq-miller`、`freq-stages` |
| 7 | Noise | `noise-basics`、`noise-circuits` |
| 8 | Feedback | `feedback` |
| 9 | Operational Amplifiers | `opamp-specs` |
| 10 | Stability and Frequency Compensation | `stability`、`miller-compensation` |
| 11 | Bandgap References | `bandgap` |
| 12 | Introduction to Switched-Capacitor Circuits | `switched-cap` |
| 13 | Short-Channel Effects and Device Models | `short-channel-gmid` |
| 14 | Sampling | `switched-cap` |
| 15 | Digital to Analog Conversion | `dac-adc` |
| 16 | Analog to Digital Conversion | `dac-adc` |

## CS2023 核心主题（C2）

`scope.json` 没有给 H.2.6 匹配 CS2023 主题，只注明 CE2016 讲到运放和混合信号电路概述（CE-CAE-9、CE-CAE-10）：运放在 `opamp-specs`、`miller-compensation`，混合信号的开关电容和数据转换器在 `switched-cap`、`dac-adc`。

## 学习资源的章节（C3）

已逐条核对：

| 资源的小节 | 去处 |
|---|---|
| 吴金第 03 讲 无源器件 | 只讲到用法上的结论：片上电阻绝对值偏差 10%–20%、电容比能做到 0.1% 以内（`current-mirrors`、`switched-cap` 的先猜和解析），电流镜和开关电容都靠比值。电阻、电容的版图结构不教：属于工艺和器件（H.2.7、H.2.5） |
| 吴金第 04、05 讲 二极管、双极结型晶体管 | 二极管和 BJT 的基本特性属于必须前置 H.1.4；本包只在 `bandgap` 用到 $V_{BE}$ 的温度特性和 $\Delta V_{BE} = V_T\ln n$，并说明 CMOS 工艺里用寄生 PNP |
| 吴金第 06–10 讲 场效应晶体管、张鸿第 2、3 讲 MOS 器件物理和小信号模型、CppSim 大信号和小信号模型 | `analog-intro`、`mos-large-signal`、`mos-small-signal` |
| CppSim Subthreshold Operation and gm/Id Design、Razavi 第 17 章 | `short-channel-gmid` |
| 吴金第 21–23 讲 共源极放大电路、张鸿第 4–7 讲 CS/SF/CG/Cascode、CppSim Single Stage Amplifiers、Cascode Techniques | `cs-stage`、`sf-cg`、`cascode` |
| 张鸿第 8–10 讲 差动放大器（大信号、小信号、吉尔伯特单元）、CppSim Differential Amplifiers | `diff-pair`、`five-transistor-ota` |
| 吴金第 11–15 讲 偏置电路和 Cascode、张鸿第 11–13 讲 电流镜、低压 Cascode 电流镜、五管单元、CMRR 和偏置、CppSim Current Mirrors | `current-mirrors`、`cascode-mirrors`（共源共栅、低压共源共栅、与电源无关的偏置和启动电路）、`diff-pair`（共模响应和共模抑制）、`five-transistor-ota` |
| 张鸿第 13–15 讲 频率响应和密勒定理、CppSim Open Circuit Time Constant Technique、Frequency Response、Two-Port Models | `freq-miller`、`freq-stages`；两端口模型只用到“从某个端口看进去的电阻”和节点时间常数的写法，没有单独讲 y、z 参数 |
| Razavi 第 8 章反馈 | `feedback`（增益降敏、带宽、四种拓扑和输入输出电阻） |
| 张鸿第 26–27 讲 稳定性与频率补偿、Razavi 第 10 章 | `stability`、`miller-compensation` |
| Razavi 第 7 章、CppSim Basics of Noise、Noise Spectral Analysis for Circuit Elements | `noise-basics`、`noise-circuits` |
| CppSim Basic Two Stage CMOS Opamp、Key Opamp Specifications、Advanced Opamp Topologies、Razavi 第 9 章 | `opamp-specs`（指标、套筒式、折叠式、增益提升、两级）、`miller-compensation` |
| 吴金第 16–20 讲 基准电路、Razavi 第 12 章 | `cascode-mirrors`（与电源无关的偏置、启动电路）、`bandgap` |
| Razavi 第 13 章、CppSim Sampling | `switched-cap`（MOS 开关、采样保持、电荷注入、时钟馈通、等效电阻、放大器和积分器）；kT/C 在 `noise-circuits` |
| CppSim Digital to Analog Conversion、Analog to Digital Conversion | `dac-adc`（电阻串、电流舵、电容阵列；Flash、SAR、流水线、Σ-Δ 一句话；量化噪声和 $6.02N + 1.76$ dB） |

## 综合练习（C4）

| 小题 | 负责的课 |
|---|---|
| (1) $I_D$、$g_m$、$r_o$、本征增益 | `mos-small-signal` |
| (2) 电流源负载共源级、五管差分对的增益 | `cs-stage`、`five-transistor-ota` |
| (3) 电流镜比例、$V_{DS}$ 失配、共源共栅镜 | `current-mirrors`、`cascode-mirrors` |
| (4) 主极点和增益带宽积 | `freq-miller` |
| (5) 两级运放密勒补偿的 GBW 和 $g_{m2}$ | `miller-compensation` |
| (6) 电阻热噪声、MOS 等效输入噪声、kT/C | `noise-basics`、`noise-circuits` |
| (7) 带隙基准的温度系数和输出电压 | `bandgap` |
| (8) 开关电容等效电阻、SAR 和 Flash 的比较次数 | `switched-cap`、`dac-adc` |

## 后继技能用到的（C5）

H.2.6 直接解锁 E.1.5 射频集成电路设计（通信工程远征的一站，主来源 Razavi《RF Microelectronics》）。它的低噪声放大器、混频器、振荡器各章直接用到本包的小信号模型和 $g_m$、$r_o$（`mos-small-signal`）、共源级和共栅级的输入电阻（`cs-stage`、`sf-cg`）、共源共栅（`cascode`）、差分对和吉尔伯特单元（`diff-pair`、`five-transistor-ota`）、电阻和 MOS 管的热噪声 $4kTR$、$4kT\gamma g_m$ 以及等效输入噪声（`noise-basics`、`noise-circuits`）、电流镜偏置（`current-mirrors`）。噪声系数、灵敏度、非线性（IP3）、S 参数在 E.1.5 自己的第 1 章讲，本包不提前讲。
