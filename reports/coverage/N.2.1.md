# N.2.1 量子力学基础：覆盖表

**状态（2026-11-26）：已写完（26 课，20/20 节有课；check-pack、check-coverage、verify.py 243 项通过；两个 pi 子代理通读后按报告修改）。** 依据 `../cs-math-skill-tree/data/outlines/N.2.1.json`（主来源 OpenStax *University Physics* 第三卷第 6–8 章“光子与物质波、量子力学、原子结构”，算符与测量由 MIT 8.04（2016）讲义第 8、9 讲补齐）、学习资源（北京理工大学《大学物理—近代物理》、清华大学庄鹏飞《现代量子力学》、MIT 8.04、MIT 8.05）和原技能树综合练习 7 小题。数值核对脚本 `tests/content/N.2.1.verify.py`。

前置：必须前置 N.1.3 振动、波动与光学（经 N.1.2、N.1.1 带来动量、角动量、电子伏特、磁矩、电磁波；N.1.3 自己讲了复数、欧拉公式、驻波、波包、群速度、单缝衍射、光栅），M.2.1 常微分方程（二阶常系数方程、特征方程、叠加原理），M.3.1 线性代数（矩阵、特征值、特征向量、对称矩阵、谱定理、正交）。推荐前置 M.6.1 概率论不在必须前置链上：概率密度、期望值、标准差在用到时现讲；M.2.2 偏微分方程没有包，薛定谔方程按“自由粒子的平面波满足什么方程”现讲。

常数和写法：$h = 6.626\times10^{-34}\ \text{J·s}$，$\hbar = h/2\pi$，$m_e = 9.109\times10^{-31}$ kg，$e = 1.602\times10^{-19}$ C，$c = 3.00\times10^8$ m/s，题目里需要时给出 $hc \approx 1240\ \text{eV·nm}$。波函数一般写 $\Psi(x, t)$，定态的空间部分写 $\psi(x)$；“本征值”注明就是线性代数里的“特征值”。

## 课的安排（26 课）

| 章 | 课 | 内容 |
|---|---|---|
| 波粒二象性 | `blackbody-photons` | 热辐射和黑体，维恩位移定律、斯特藩–玻尔兹曼定律，紫外灾难，普朗克的能量子 $E = hf$，光子，$hc \approx 1240$ eV·nm |
| | `photoelectric` | 光电效应的四个实验事实，爱因斯坦方程 $hf = W + K_{\max}$，逸出功、截止频率、遏止电压，由两组数据求 $h$ 和 $W$ |
| | `compton` | 光子的动量 $p = h/\lambda$，康普顿散射公式 $\Delta\lambda = \frac{h}{m_ec}(1 - \cos\theta)$，反冲电子的能量，为什么可见光看不出来 |
| | `hydrogen-spectrum` | 氢的线状光谱、里德伯公式和赖曼、巴耳末、帕邢三个线系，经典模型的困难（电子绕核会辐射、落进核里） |
| | `bohr-model` | 玻尔的三条假设，$r_n = n^2a_0$、$E_n = -13.6\text{ eV}/n^2$，跃迁波长，电离能，模型的局限 |
| | `matter-waves` | 德布罗意波长 $\lambda = h/p$，加速电子的波长，戴维孙–革末实验，电子一个一个通过双缝，波粒二象性和互补，电子显微镜和中子衍射 |
| 薛定谔方程 | `wavefunction` | 波函数和复共轭，玻恩的概率解释、概率密度，归一化，算一段区间里的概率，波函数要满足的条件 |
| | `uncertainty` | 单缝衍射推出 $\Delta x\Delta p \sim h$，方差和标准差，不确定关系 $\Delta x\Delta p \ge \hbar/2$，和波包的关系，原子大小的估算，能量–时间关系和能级宽度 |
| | `schrodinger-equation` | 自由粒子的平面波推出薛定谔方程，波包以群速度 $\hbar k/m$ 运动，算符（动量、哈密顿量），定态和定态薛定谔方程，两个定态叠加时概率分布的振荡 |
| 一维势阱与隧穿 | `infinite-well` | 无限深势阱的边界条件，$\psi_n = \sqrt{2/L}\sin(n\pi x/L)$，$E_n = n^2h^2/8mL^2$，量子数、基态、零点能，节点数，概率分布，量子点 |
| | `finite-well-step` | 有限深势阱：阱外指数衰减、穿透深度、能级比无限深阱低、束缚态有限；势阶的反射和透射，$E < V_0$ 时全反射但有渗入 |
| | `tunneling` | 方势垒，$T \approx e^{-2\kappa a}$ 和精确公式的前置因子，宽度和质量的影响，扫描隧道显微镜，MOS 管栅氧化层的隧穿漏电 |
| 谐振子 | `quantum-oscillator` | $V = \tfrac12m\omega^2x^2$，$E_n = (n + \tfrac12)\hbar\omega$，等间距能级，零点能和不确定关系的估算，基态的高斯波函数，经典转折点外的渗入，分子振动光谱 |
| | `ladder-operators` | 对易子 $[\hat x, \hat p] = i\hbar$，升降算符 $\hat a_\pm$，$\hat H = \hbar\omega(\hat a_+\hat a_- + \tfrac12)$，升一级能量加 $\hbar\omega$，$\hat a_-\psi_0 = 0$ 给出基态，系数 $\sqrt{n}$ 和 $\sqrt{n+1}$ |
| 算符与测量 | `expectation-values` | 期望值和标准差，$\langle x\rangle$、$\langle p\rangle$、$\langle p^2\rangle$，势阱基态 $\Delta x\Delta p$，动量空间（傅里叶变换），期望值随时间的变化（埃伦费斯特定理） |
| | `hermitian-operators` | 本征值方程，内积，厄米算符和厄米矩阵，本征值是实数、本征函数正交，完备性和展开系数 |
| | `measurement` | 测量公设：结果是本征值、概率 $|c_n|^2$、坍缩；能量的期望值和不确定度；对易与同时测量，一般的不确定关系 |
| 角动量与氢原子 | `angular-momentum` | 角动量算符的对易关系，$L^2 = l(l+1)\hbar^2$、$L_z = m\hbar$，矢量模型，升降算符让 $m$ 加减 1，转动能级和分子转动光谱 |
| | `hydrogen-atom` | 三维薛定谔方程和三个量子数，$E_n = -13.6\text{ eV}/n^2$，$l$ 和 $m$ 的取值，简并度 $n^2$，s、p、d、f，1s 的径向概率分布，径向节点数 |
| | `orbital-magnetic-moment` | 轨道磁矩 $\mu = \frac{e}{2m}L$，玻尔磁子，磁场中的能量 $m\mu_BB$，正常塞曼效应的分裂和谱线移动 |
| 自旋 | `stern-gerlach` | 施特恩–格拉赫实验，自旋 $s = 1/2$、$S_z = \pm\hbar/2$，自旋磁矩和 $g \approx 2$，电子自旋共振，自旋–轨道耦合和钠双线 |
| | `spin-matrices` | 自旋态的二分量写法，泡利矩阵，沿 $x$ 测量的概率，连续几个施特恩–格拉赫装置，自旋进动和核磁共振 |
| 全同粒子与泡利不相容 | `identical-particles` | 全同粒子不可区分，交换对称和反对称，玻色子和费米子，泡利不相容原理，势阱里放几个电子，最高被占据的能级 |
| | `periodic-table` | 四个量子数，壳层和支壳层的容量 $2n^2$、$2(2l+1)$，电子组态和填充顺序，元素周期表的周期和族，硅的四个价电子 |
| | `xrays` | 跃迁的选择定则 $\Delta l = \pm1$，X 射线管的连续谱和最短波长，特征谱线 $K_\alpha$ 和莫塞莱定律，内层空位和不相容原理 |
| | `lasers` | 吸收、自发辐射、受激辐射，玻尔兹曼分布下为什么没有粒子数反转，亚稳态和三能级、四能级，谐振腔的纵模间隔，半导体激光器 |

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Blackbody Radiation | `blackbody-photons` |
| 1.2 | Photoelectric Effect | `photoelectric` |
| 1.3 | The Compton Effect | `compton` |
| 1.4 | Bohr's Model of the Hydrogen Atom | `hydrogen-spectrum`、`bohr-model` |
| 1.5 | De Broglie's Matter Waves | `matter-waves` |
| 1.6 | Wave-Particle Duality | `matter-waves`、`compton`（光子在碰撞里像粒子、在干涉里像波） |
| 2.1 | Wave Functions | `wavefunction` |
| 2.2 | The Heisenberg Uncertainty Principle | `uncertainty`、`measurement`（一般的不确定关系） |
| 2.3 | The Schrödinger Equation | `schrodinger-equation` |
| 2.4 | The Quantum Particle in a Box | `infinite-well`、`finite-well-step` |
| 2.5 | The Quantum Harmonic Oscillator | `quantum-oscillator`、`ladder-operators` |
| 2.6 | The Quantum Tunneling of Particles through Potential Barriers | `tunneling`、`finite-well-step`（势阶） |
| 3.1 | The Hydrogen Atom | `hydrogen-atom`、`angular-momentum` |
| 3.2 | Orbital Magnetic Dipole Moment of the Electron | `orbital-magnetic-moment` |
| 3.3 | Electron Spin | `stern-gerlach`、`spin-matrices` |
| 3.4 | The Exclusion Principle and the Periodic Table | `identical-particles`、`periodic-table` |
| 3.5 | Atomic Spectra and X-rays | `xrays`、`hydrogen-spectrum`（线状光谱） |
| 3.6 | Lasers | `lasers` |
| 4.1 | Uncovering Momentum Space, Expectation Values of Operators, Time Dependence of Expectation Values | `expectation-values` |
| 4.2 | Observables and Hermitian Operators, Uncertainty | `hermitian-operators`、`measurement` |

## CS2023 核心主题（C2）

`scope.json` 对 N.2.1 的说明是 CS2023、CE2016 都没有量子力学，国标通识类只要求“近代物理”的基本内容。近代物理的基本内容（光子、物质波、不确定关系、势阱、氢原子、泡利不相容原理）由第 1–3 章和第 6–8 章的课负责。

## 学习资源的章节（C3）

- zh1（北京理工大学《大学物理—近代物理》）：光的波粒二象性、康普顿效应、氢原子光谱与玻尔假设在第 1 章五课；自由粒子和一般情况下的薛定谔方程、定态薛定谔方程在 `schrodinger-equation`；无限深势阱、势垒贯穿在第 3 章；简谐振子在 `quantum-oscillator`；海森伯不确定关系在 `uncertainty`；氢原子的量子数和电子概率分布在 `hydrogen-atom`；电子自旋在 `stern-gerlach`；四个量子数与泡利不相容原理在 `periodic-table`、`identical-particles`。
- zh2（清华大学《现代量子力学》）：基矢正交归一完备性、算符的矩阵形式、厄米算符在 `hermitian-operators`（狄拉克符号只用到 $\langle f|g\rangle$ 表示内积，不展开右矢、左矢的形式体系）；单个力学量的测量、塌缩、共同本征态在 `measurement`；一维谐振子的代数解法和升降算符在 `ladder-operators`；角动量的本征值、升降算符在 `angular-momentum`；Stern–Gerlach 实验、自旋矩阵、泡利矩阵、自旋进动在第 7 章两课；两全同粒子的态和全同性原理的观察效应在 `identical-particles`。
- en1（MIT 8.04）：光电效应、康普顿散射、物质波（第 3、4 讲）在第 1 章；波函数方程和波包（第 5、7 讲）在第 2 章；第 8、9 讲就是大纲第 4 部分；无限深、有限深势阱、势阶在第 3 章，δ 势不教（大纲 2.4 只收 OpenStax 7.4，后继技能不用）；节点定理（第 $n$ 个束缚态有 $n - 1$ 个节点）在 `infinite-well`、`quantum-oscillator`；谐振子的代数解法（第 14、15 讲）在 `ladder-operators`；角动量和中心势（Part 3）在第 6 章。
- en2（MIT 8.05）：两态系统、角动量和自旋在第 7 章；全同粒子在 `identical-particles`。8.05 的其余内容（希尔伯特空间的一般理论、微扰论、角动量相加）超出入门层，不教。

## 综合练习（C4）

| 小题 | 负责的课 |
|---|---|
| (1) 100 V 电子的德布罗意波长，为什么能用晶体衍射验证 | `matter-waves` |
| (2) 1 nm 无限深势阱的定态方程、能级、基态能量、2→1 跃迁波长 | `infinite-well` |
| (3) 1 eV 电子对 5 eV、0.5 nm 势垒的透射系数 | `tunneling` |
| (4) 谐振子能级、零点能和它不为零的原因 | `quantum-oscillator` |
| (5) 叠加态测能量的可能值、概率、期望值、测后的波函数 | `measurement` |
| (6) 氢原子 3→2 跃迁波长，$n = 3$ 的 $l$ 和状态数（计不计自旋） | `bohr-model`、`hydrogen-atom`、`stern-gerlach` |
| (7) 3 个电子放进势阱的基态总能量，换成无自旋玻色子 | `identical-particles` |

## 后继技能用到的（C5）

必须后继 N.2.2 固体与半导体物理还没有内容包。按它的章节（自由电子模型、克勒尼希–彭尼模型、布洛赫定理、有效质量、费米–狄拉克分布、载流子统计），这一站要教到：自由粒子的平面波和 $E = \hbar^2k^2/2m$、波包的群速度 $\frac{1}{\hbar}\frac{dE}{dk}$（`schrodinger-equation`），势阱的能级和波函数、有限深阱和势垒（第 3 章），费米子、泡利不相容和“从低到高填能级、最高被占据能级”（`identical-particles`），硅的价电子（`periodic-table`），简并（`hydrogen-atom`）。
