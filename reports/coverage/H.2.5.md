# H.2.5 半导体器件与微电子基础：覆盖表

**状态（2026-11-26）：已写完 23 课（第 9 轮），C1 32/32 节有课，两个 pi 子代理通读后按报告改完，等用户验收。电场、掺杂（n 型、p 型）放进第一课讲，晶体管模型一章不依赖后面的物理课。** 依据 `../cs-math-skill-tree/data/outlines/H.2.5.json`（主来源 MIT 6.012 *Microelectronic Devices and Circuits*，逐讲大纲 15 节；B 是 6.374 数字集成电路，大纲里没有单独的节）、学习资源（复旦《半导体物理与器件原理》、交大《半导体元件物理》、哈工大《微电子工艺》、“一生一芯”E8、MIT 6.152J）和原技能树综合练习 5 小题。数值核对脚本是 `tests/content/H.2.5.verify.py`。

前置：必须前置只有 H.1.1 电路与模拟电子基础（经它带来 M.1.1–M.1.3 微积分、M.3.1 线性代数）。**物理链（N.1.2 电磁学、N.2.1 量子、N.2.2 半导体物理）都不在必须前置里**，N.2.2 只是推荐前置，它的术语不会继承过来，所以电子、空穴、能带、掺杂、漂移、扩散、PN 结、电场、电势这些都要在本包里从头讲到够用的程度（照 6.012 的讲法：键模型、载流子浓度、漂移–扩散，不讲倒格子和费米–狄拉克积分）。说法和数值要和 N.2.2、H.1.4 一致：热电压 300 K 取 $kT/q = 0.0259$ V（6.012 写 25.9 mV），硅 $n_i = 10^{10}\ \text{cm}^{-3}$，$\varepsilon_{Si} = 11.7\varepsilon_0$，$\varepsilon_{ox} = 3.9\varepsilon_0$；MOSFET 的三个区按 H.1.4 叫截止区、三极管区（也叫线性区）、饱和区，平方律写成 $I_D = \tfrac12\mu_nC_{ox}\tfrac WL(V_{GS} - V_{th})^2$，$k = \mu_nC_{ox}W/L$（综合练习的写法）。

章的顺序由技能树定（晶体管模型 → 器件物理 → 工艺与电路实现约束）：先从端口的电流–电压关系讲模型和电路，再讲这些关系的物理来历，最后讲怎样做出来、工艺怎样约束电路。

## 课的安排（23 课）

| 章 | 课 | 内容 |
|---|---|---|
| 晶体管模型 | `mosfet-terminals` | 硅集成电路和 MOSFET 的地位，MOSFET 的结构（源、漏、栅、衬底、栅氧化层）和电路符号，栅压吸引电子形成沟道的直观图像，阈值电压，端特性：截止、三极管区（$I_D = k[(V_{GS} - V_{th})V_{DS} - V_{DS}^2/2]$）、饱和区，输出特性曲线 |
| | `mosfet-saturation` | 夹断和饱和，平方律 $I_D = \tfrac12k(V_{GS} - V_{th})^2$，区域判断，沟道长度调制 $\lambda$，背栅（体）效应 $V_{th}$ 随 $V_{SB}$ 增大，PMOS 的符号约定 |
| | `mosfet-small-signal` | 工作点和小信号，跨导 $g_m = k(V_{GS} - V_{th}) = \sqrt{2kI_D} = 2I_D/V_{ov}$，输出电阻 $r_o = 1/(\lambda I_D)$，背栅跨导 $g_{mb}$，小信号等效电路，栅电容 |
| | `inverter-basics` | 数字逻辑的电压表示，反相器的电压传输特性，$V_{OH}$、$V_{OL}$、$V_{IL}$、$V_{IH}$，噪声容限 |
| | `inverter-loads` | 电阻负载和 NMOS 负载的反相器，$V_{OL}$ 的计算，静态功耗，瞬态：负载电容的充放电和传播延迟的定义 |
| | `cmos-inverter` | CMOS 反相器：两管互补，电压传输特性的五段，$V_M$，静态电流为零，传播延迟模型 $t_p \approx CV_{DD}/(2I)$，动态功耗 $CV_{DD}^2f$ |
| | `cmos-gates` | 静态 CMOS 与非门、或非门：上拉网络和下拉网络互为对偶，串联管加宽，扇入对延迟的影响 |
| | `diode-model` | PN 二极管的端特性，大信号静态模型（理想方程、恒压降），小信号电阻 $r_d = V_T/I_D$，耗尽电容和扩散电容 |
| | `bjt-basics` | BJT 的结构和符号，正向有源偏置，$I_C = I_Se^{V_{BE}/V_T}$，电流增益 $\beta$，$I_B$、$I_E$，小信号 $g_m = I_C/V_T$、$r_\pi = \beta/g_m$ |
| | `single-stage-amps` | 放大器的二端口小信号模型（输入电阻、输出电阻、增益），电阻负载和电流源负载的共源放大器，$A_v = -g_m(R_D\parallel r_o)$，本征增益 $g_mr_o$ |
| 器件物理 | `electrons-holes` | 硅的键模型，电子和空穴，能带图（导带、价带、带隙 1.12 eV），本征载流子 |
| | `generation-equilibrium` | 产生和复合，热平衡，$n_0p_0 = n_i^2$，$n_i$ 随温度变化 |
| | `doping` | 施主和受主，n 型和 p 型，多子和少子，$n_0 \approx N_d$、$p_0 = n_i^2/N_d$，补偿 |
| | `drift` | 漂移速度 $v = \mu E$，迁移率随掺杂变化，漂移电流密度，电导率、电阻率，方块电阻 |
| | `diffusion` | 扩散电流密度 $J = qD\,dn/dx$，爱因斯坦关系 $D = \mu V_T$ |
| | `pn-equilibrium` | 热平衡下载流子浓度和电势的关系 $\phi = V_T\ln(n_0/n_i)$，“60 mV 规则”（浓度每差 10 倍电势差 60 mV），内建电势 |
| | `pn-depletion` | 耗尽近似，电荷、电场、电势分布，耗尽区宽度，偏压下的变化，正偏注入和二极管方程的来历 |
| | `mos-equilibrium` | MOS 电容的结构，热平衡下的能带和电势，功函数差，平带电压 |
| | `mos-bias` | 外加偏压：积累、耗尽、反型，阈值电压 $V_{th} = V_{FB} - 2\phi_p + \sqrt{2\varepsilon_{Si}qN_a(-2\phi_p)}/C_{ox}$，反型层电荷 $Q_n = -C_{ox}(V_{GB} - V_{th})$，C–V 曲线 |
| | `mosfet-from-charge` | 由反型层电荷推出三极管区的电流，夹断与饱和，背栅效应的来历 |
| 工艺与电路实现约束 | `cmos-process` | CMOS 工艺流程：衬底和阱、热氧化、光刻、刻蚀、离子注入和退火、多晶硅栅、源漏、薄膜沉积、金属互连和化学机械抛光 |
| | `process-constraints` | 工艺参数怎样决定 $V_{th}$、$g_m$ 和寄生电容，版图和设计规则，DRC、LVS、STA 签核 |
| | `scaling` | 按比例缩小（Dennard 缩放）的规则和结果，为什么 2000 年代中期失效，短沟道效应（阈值电压滚降、DIBL、亚阈值漏电、速度饱和），FinFET、GAA |

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | silicon integrated circuit technology | `mosfet-terminals` |
| 2.1 | electrons and holes | `electrons-holes` |
| 2.2 | bond model | `electrons-holes` |
| 2.3 | generation recombination and thermal equilibrium | `generation-equilibrium` |
| 2.4 | doping, donors, acceptors, compensation | `doping` |
| 3.1 | drift velocity | `drift` |
| 3.2 | drift current density | `drift` |
| 3.3 | diffusion current density | `diffusion` |
| 4.1 | carrier concentration and potential in thermal equilibrium | `pn-equilibrium`、`pn-depletion` |
| 4.2 | 60mV rule | `pn-equilibrium` |
| 5.1 | MOS capacitor in thermal equilibrium | `mos-equilibrium` |
| 6.1 | accumulation, depletion, and inversion regions | `mos-bias` |
| 7.1 | circuit symbol and terminal characteristics | `mosfet-terminals` |
| 7.2 | MOS transistor characteristics | `mosfet-terminals`、`mosfet-from-charge` |
| 8.1 | backgate effect | `mosfet-saturation`、`mosfet-from-charge` |
| 8.2 | MOSFET in saturation | `mosfet-saturation` |
| 9 | MOSFET small-signal model | `mosfet-small-signal` |
| 10.1 | inverter characteristics | `inverter-basics` |
| 10.2 | logic levels and noise margins | `inverter-basics` |
| 10.3 | transient characteristics | `inverter-loads` |
| 10.4 | inverter circuits, NMOS/resistor loads | `inverter-loads` |
| 11.1 | propagation delay model | `cmos-inverter` |
| 11.2 | static CMOS gates | `cmos-gates` |
| 12.1 | large signal static model | `diode-model` |
| 12.2 | small signal model | `diode-model` |
| 12.3 | diffusion capacitance | `diode-model` |
| 13.1 | terminal characteristics | `bjt-basics` |
| 13.2 | forward active bias | `bjt-basics` |
| 13.3 | current gain | `bjt-basics` |
| 14.1 | two port small signal model | `single-stage-amps` |
| 14.2 | common source amplifier with resistor and current source supply | `single-stage-amps` |
| 15 | Integrated CMOS Processing | `cmos-process`、`process-constraints` |

## CS2023 核心主题（C2）

`scope.json`：CS2023 没有半导体器件。CE2016 两条：CE-CAE-6“等效电路模型和它们的局限”由 `mosfet-small-signal`、`diode-model`、`bjt-basics`、`single-stage-amps` 负责（每个模型都写明适用条件：小信号、饱和区、长沟道）；CE-CAE-5“漂移和扩散电流、迁移率和扩散系数”由 `drift`、`diffusion` 负责。

## 学习资源的章节（C3）

| 资源 | 讲到的内容 | 去处 |
|---|---|---|
| en1 MIT 6.012 | 器件建模、大信号和小信号模型、电流源和电流镜；半导体结和 MOS 器件的物理 | 第 1、2 章各课；电流镜不单讲（H.1.4 `current-mirrors` 讲过，本包的电流源负载一课讲到用 PMOS 当电流源） |
| zh1 复旦《半导体物理与器件原理》 | 能带论、载流子统计和输运、非平衡载流子、PN 结、MIS 结构；BJT 与 MOSFET 的直流、频率、开关特性 | `electrons-holes` 到 `mosfet-from-charge`，`diode-model`、`bjt-basics`；费米–狄拉克统计、准费米能级不讲（属于 N.2.2，6.012 也只用 $n_0p_0 = n_i^2$ 和 60 mV 规则） |
| r7-zh1 哈工大《微电子工艺》、r7-en1 MIT 6.152J | 外延、热氧化、扩散、离子注入、CVD/PVD、光刻、刻蚀、金属互连、工艺集成 | `cmos-process`；外延、PVD 只在薄膜沉积一条里点到，详细工艺属于 H.2.7 |
| r7-zh2 一生一芯 E8 | DRC、LVS、STA 签核和不达标时的调整 | `process-constraints` |

## 综合练习（C4）

| 小题 | 负责的课 |
|---|---|
| (1) 能带说明导体、半导体、绝缘体，本征载流子，n 型和 p 型掺杂 | `electrons-holes`、`doping` |
| (2) 耗尽区的形成、正偏和反偏，正偏多 60 mV 电流约 10 倍 | `pn-equilibrium`、`pn-depletion`、`diode-model` |
| (3) 阈值电压，三极管区和饱和区的条件，平方律算饱和电流 | `mosfet-terminals`、`mosfet-saturation` |
| (4) Dennard 缩放和它的失效，短沟道效应 | `scaling` |
| (5) CMOS 工艺的主要步骤 | `cmos-process` |

## 后继技能用到的（C5）

必须后继 H.2.4 VLSI 与芯片设计会用到：MOSFET 的平方律和区域、阈值电压、CMOS 反相器和静态 CMOS 门、传播延迟和动态功耗、按比例缩小和短沟道效应、工艺和设计规则、DRC/LVS/STA。本包都要讲到。
