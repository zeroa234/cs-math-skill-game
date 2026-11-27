# N.2.2 固体与半导体物理：覆盖表

**状态（2026-11-26）：已写完 25 课（第 9 轮），C1 36/36 节有课，两个 pi 子代理通读后按报告改完，等用户验收。** 依据 `../cs-math-skill-tree/data/outlines/N.2.2.json`（主来源 Van Zeghbroeck *Principles of Semiconductor Devices* 第 2、4 章；倒空间由 McCulloch *Solid-state physics* 4.2 补齐）、学习资源（电子科技大学《固体与半导体物理基础》、北京交通大学《固体物理学》、Simon *Oxford Solid State Physics*）和原技能树综合练习 7 小题。数值核对脚本是 `tests/content/N.2.2.verify.py`。

前置：必须前置只有 N.2.1 量子力学基础（经它带来 N.1.3、M.2.1、M.3.1 和整条物理链）：平面波和 $E = \hbar^2k^2/2m$、波包的群速度、势阱和势垒、费米子和泡利不相容、费米能、半导体和价电子、简并（N.2.1 的定义是“能量相同的几个状态”，本包的“简并半导体”意思不同，要在本包重新讲）。推荐前置 H.1.1 不在必须前置链上：电流、电阻、电容的电路含义按 N.1.2 的定义用。

常数和写法：300 K 时 $kT/q = 0.02585$ V，硅 $n_i = 1\times10^{10}\ \text{cm}^{-3}$、$N_c = 2.8\times10^{19}\ \text{cm}^{-3}$、$E_g = 1.12$ eV、$\varepsilon_{Si} = 11.7\varepsilon_0$（照综合练习的取值）；浓度用 $\text{cm}^{-3}$，迁移率用 $\text{cm}^2/(\text{V·s})$，和半导体教材一致。玻尔兹曼常数写 $k$，和 N.2.1 一样提醒它不是库仑常数。

## 课的安排（25 课）

| 章 | 课 | 内容 |
|---|---|---|
| 晶体结构与倒格子 | `crystal-lattices` | 晶体和非晶体，晶格、基元、原胞与晶胞，简单立方、体心立方、面心立方，金刚石和闪锌矿结构，晶格常数和原子密度（硅 $5\times10^{22}\ \text{cm}^{-3}$） |
| | `miller-planes` | 晶向和密勒指数，晶面间距 $d = a/\sqrt{h^2 + k^2 + l^2}$，布拉格条件 $2d\sin\theta = n\lambda$，X 射线衍射测晶格常数 |
| | `reciprocal-1d` | 为什么要倒格子：周期函数的傅里叶级数只含 $G = 2\pi n/a$，倒格子是晶格的傅里叶变换，倒格子的周期性（$k$ 和 $k + G$ 等价） |
| | `reciprocal-3d` | 推广到二维、三维：$\vec a_i\cdot\vec b_j = 2\pi\delta_{ij}$，三角格子的例子，简单立方的倒格子还是简单立方，面心和体心互为倒格子，第一布里渊区，倒格矢和晶面的关系 |
| 能带理论 | `free-electron` | 自由电子模型：周期性边界条件下 $k$ 的取值，$E = \hbar^2k^2/2m$，按不相容原理填到费米能，金属里电子的费米能和费米速度 |
| | `periodic-potential` | 周期势和布洛赫定理，在布里渊区边界 $k = \pm\pi/a$ 处行波被布拉格反射成两种驻波，能量分开出现带隙（近自由电子），克勒尼希–彭尼模型的结论 |
| | `bands-metals-insulators` | 半导体的能带：价带、导带、带隙（硅 1.12 eV、锗 0.66 eV、砷化镓 1.42 eV），直接带隙和间接带隙，满带不导电，金属、半导体、绝缘体的区别 |
| 有效质量 | `electrons-holes` | 导带里的电子和价带里的空穴，空穴带正电，本征激发产生电子–空穴对，能带图上的画法 |
| | `effective-mass` | $1/m^* = \frac{1}{\hbar^2}\frac{d^2E}{dk^2}$，能带曲率和有效质量，价带顶的负曲率和空穴的正有效质量，硅、砷化镓的有效质量 |
| 本征与掺杂半导体 | `intrinsic` | 本征半导体 $n = p = n_i$，$n_i \propto e^{-E_g/2kT}$ 随温度和带隙变化，质量作用定律 $np = n_i^2$（本征费米能级要用到费米能级，挪到 `carrier-densities`） |
| | `doping` | 施主（磷）和受主（硼），电离能（几十 meV），n 型和 p 型，多子和少子，电荷中性条件，杂质补偿，$n \approx N_d$、$p = n_i^2/N_d$ |
| 载流子统计 | `density-of-states` | 态密度：在 $k$ 空间数状态，三维 $g(E) \propto \sqrt{E - E_c}$，导带和价带的有效态密度 $N_c$、$N_v$ |
| | `fermi-dirac` | 费米–狄拉克分布 $f(E) = 1/(1 + e^{(E - E_F)/kT})$，费米能级的意义，$E - E_F \gg kT$ 时的玻尔兹曼近似，空穴占据概率 $1 - f$ |
| | `carrier-densities` | 态密度乘占据概率积分，$n = N_ce^{-(E_c - E_F)/kT}$、$p = N_ve^{-(E_F - E_v)/kT}$，乘积推出质量作用定律和 $n_i$，本征费米能级，费米积分，非简并和简并半导体，由浓度求费米能级位置 |
| | `quasi-fermi` | 光照或注入时的非平衡载流子，$np > n_i^2$，电子和空穴各用一个准费米能级描述 |
| 漂移与扩散 | `drift-mobility` | 漂移速度 $v = \mu E$，平均自由时间和散射（晶格振动、电离杂质），迁移率随掺杂和温度变化，电导率 $\sigma = q(n\mu_n + p\mu_p)$，电阻率 |
| | `velocity-saturation-hall` | 强电场下的速度饱和（硅约 $10^7$ cm/s），霍尔效应测载流子类型和浓度 |
| | `diffusion` | 浓度梯度引起的扩散电流 $J = qD\,dn/dx$，扩散系数，爱因斯坦关系 $D = \mu kT/q$ |
| | `drift-diffusion` | 漂移–扩散模型：总电流是两者之和，热平衡时电流为零，非均匀掺杂产生内建电场，平衡时费米能级处处相同 |
| 产生与复合 | `recombination` | 产生和复合，直接（带间）复合和通过杂质能级的间接复合（SRH），俄歇复合，少子寿命，过剩载流子按 $e^{-t/\tau}$ 衰减，SRH 净复合率的一般式和耗尽区里的净产生 |
| | `continuity` | 连续性方程，稳态时的扩散方程，扩散长度 $L = \sqrt{D\tau}$，光照一端时的指数分布 |
| PN结物理 | `pn-structure` | p-n 结的结构，扩散形成耗尽区和内建电场，能带图，内建电势 $V_{bi} = \frac{kT}{q}\ln\frac{N_aN_d}{n_i^2}$ |
| | `depletion` | 耗尽近似，泊松方程，电场和电势的分布，$N_ax_p = N_dx_n$，耗尽区宽度和偏压的关系，结电容 |
| | `diode-current` | 正偏时少子注入，结两边少子浓度 $n_{p0}e^{V/V_T}$，扩散电流，理想二极管方程 $I = I_s(e^{V/V_T} - 1)$，反偏饱和电流 |
| | `breakdown` | 反向击穿：雪崩击穿（碰撞电离）和齐纳击穿（隧穿），击穿电压和掺杂的关系，稳压管 |

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Introduction | `crystal-lattices` |
| 1.2 | Crystals and crystal structures | `crystal-lattices`、`miller-planes` |
| 1.3.1 | Free electron model | `free-electron` |
| 1.3.2 | Periodic potentials | `periodic-potential` |
| 1.3.3 | Energy bands of semiconductors | `bands-metals-insulators` |
| 1.3.4 | Metals, insulators and semiconductors | `bands-metals-insulators` |
| 1.3.5 | Electrons and holes in semiconductors | `electrons-holes` |
| 1.3.6 | The effective mass concept | `effective-mass` |
| 1.4 | Density of states | `density-of-states` |
| 1.5 | Carrier distribution functions | `fermi-dirac` |
| 1.6.1 | General discussion | `carrier-densities` |
| 1.6.2 | Calculation of the Fermi integral | `carrier-densities` |
| 1.6.3 | Intrinsic semiconductors | `intrinsic`、`carrier-densities`（本征费米能级） |
| 1.6.4 | Doped semiconductors | `doping` |
| 1.6.5 | Non-equilibrium carrier densities | `quasi-fermi` |
| 1.7.1 | Carrier drift | `drift-mobility` |
| 1.7.2 | Mobility and Conductivity | `drift-mobility` |
| 1.7.3 | Velocity saturation | `velocity-saturation-hall` |
| 1.7.4 | Carrier diffusion | `diffusion` |
| 1.7.5 | The Hall Effect | `velocity-saturation-hall` |
| 1.8 | Carrier recombination and generation | `recombination` |
| 1.9 | Continuity equation | `continuity` |
| 1.10 | The drift-diffusion model | `drift-diffusion` |
| 2.1 | Introduction | `pn-structure` |
| 2.2 | Structure and principle of operation | `pn-structure` |
| 2.3 | Electrostatic analysis of a p-n diode | `depletion` |
| 2.4 | The p-n diode current | `diode-current` |
| 2.5 | Reverse bias breakdown | `breakdown` |
| 3.1 | Introduction | `reciprocal-1d` |
| 3.2 | Reciprocal lattice motivation | `reciprocal-1d` |
| 3.3 | Extending to higher dimensions | `reciprocal-3d` |
| 3.4 | 2D example: triangular lattice | `reciprocal-3d` |
| 3.5 | 3D lattice example | `reciprocal-3d` |
| 3.6 | The reciprocal lattice as a Fourier transform | `reciprocal-1d` |
| 3.7 | Periodicity of the reciprocal lattice | `reciprocal-1d` |
| 3.8 | Miller planes | `miller-planes`、`reciprocal-3d`（倒格矢垂直于晶面） |

## CS2023 核心主题（C2）

`scope.json` 没有给 N.2.2 匹配 CS2023 主题，只有说明：CE2016 的 CE-CAE-5 只要求掺杂、漂移与扩散这类材料性质（归到 H.2.5），本包的 `doping`、`drift-mobility`、`diffusion` 都讲到了；国标把固体物理、半导体物理列在电子科学与技术、微电子专业的专业基础知识里。

## 学习资源的章节（C3）

| 资源小节 | 去处 |
|---|---|
| 电子科大 [1.1.1] 晶体结构的基本概念、[1.1.2] 原胞与晶胞 | `crystal-lattices` |
| 电子科大 [1.7.1]、北交大 [2.1.1]、[2.1.4] 倒格子与布里渊区，Simon 12.1.2 | `reciprocal-1d`、`reciprocal-3d` |
| Simon 11.1、11.2 格子和晶胞，12.1.5 密勒指数 | `crystal-lattices`、`miller-planes` |
| 电子科大 [3.1.1] 几种电子模型，北交大 [9.1.1] 能带理论的基本近似 | `free-electron`（忽略电子间排斥，即单电子近似；绝热近似不单讲，超出入门层） |
| 北交大 [9.1.2] 布洛赫定理，Simon 14.1 近自由电子模型，Van Zeghbroeck 2.3.2 克勒尼希–彭尼模型 | `periodic-potential` |
| 电子科大 [3.7.1] 导体、半导体和绝缘体的能带结构，[3.7.2] 近满带和空穴 | `bands-metals-insulators`、`electrons-holes` |
| 北交大 [11.4/11.5] 紧束缚色散关系与有效质量，[12.2] 布洛赫电子的加速度和有效质量 | `effective-mass`（一维紧束缚能带的例题，晶体动量和加速度的推导） |
| 北交大 [16.1.2] 带边有效质量与 k·p 微扰法 | 不教：k·p 微扰超出入门层，本包只用硅的椭球谷质量和电导有效质量的结论 |
| 电子科大 [4.2.1] 本征半导体和杂质半导体，[4.2.2] 杂质补偿，[4.3.4] 载流子浓度乘积，[4.3.5] 本征载流子浓度 | `intrinsic`、`doping`、`carrier-densities` |
| 电子科大 [4.3.6] 杂质能级上的载流子占据几率 | 不教：只讲室温下杂质几乎全部电离（电离能和 $kT$ 比较）和高温回到本征；含简并因子 1/2 的占据公式超出入门层 |
| 电子科大 [3.2.2] 分布函数及费米能级，[4.3.2]、[4.3.3] 载流子的统计分布和浓度，[4.3.11] 费米能级的变化 | `fermi-dirac`、`carrier-densities`（随掺杂），`doping` 的 `hot-intrinsic`（随温度） |
| 电子科大 [5.2.1] 漂移运动和迁移率，[5.2.2] 电导率，[6.3] 扩散运动与漂移运动 | `drift-mobility`、`diffusion`、`drift-diffusion` |
| 电子科大 [6.1.1]–[6.1.3] 注入、寿命、准费米能级，[6.2.1]、[6.2.2]、[6.2.4] 直接复合、间接复合、复合率 | `quasi-fermi`、`recombination`、`continuity` |
| 电子科大 [7.1] 平衡 PN 结、正向注入，Van Zeghbroeck 第 4 章 | `pn-structure`、`depletion`、`diode-current`、`breakdown` |

## 综合练习（C4）

| 小题 | 负责的课 |
|---|---|
| (1) 简单立方的倒格子、最短倒格矢，(100) 面的布拉格角 | `reciprocal-3d`、`miller-planes` |
| (2) 自由电子和近自由电子近似下能带、带隙的来历，金属、半导体、绝缘体 | `free-electron`、`periodic-potential`、`bands-metals-insulators` |
| (3) 有效质量和能带曲率，空穴为什么带正电、有正有效质量 | `effective-mass`、`electrons-holes` |
| (4) 掺磷 $10^{16}$ 的电子、空穴浓度和费米能级位置 | `doping`、`carrier-densities` |
| (5) 漂移速度、电导率、电阻率，爱因斯坦关系 | `drift-mobility`、`diffusion` |
| (6) 过剩载流子的衰减和扩散长度 | `recombination`、`continuity` |
| (7) 突变结的内建电势和耗尽区宽度、偏向哪一侧 | `pn-structure`、`depletion` |

## 后继技能用到的（C5）

N.2.2 没有直接解锁的技能；集成电路设计远征里以它为前置的器件技能（H.2.x）写课时会用到能带图、费米能级、迁移率、扩散、少子寿命、p-n 结的耗尽区和二极管方程，本包都要讲到。
