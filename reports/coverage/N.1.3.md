# N.1.3 振动、波动与光学：覆盖表

**状态（2026-11-25）：已写完（21 课，30/31 节有课、1 节写明不教，check-pack、check-coverage、verify.py 184 项通过；FULL e2e 21 课通过）。** 依据 `../cs-math-skill-tree/data/outlines/N.1.3.json`（主来源 MIT 8.03SC *Physics III: Vibrations and Waves*，几何光学成像由 OpenStax *University Physics* 第三卷第 2 章补齐）、学习资源（中科大叶邦角《力学》振动部分、西安交大《大学物理——机械振动、波和波动光学》、北大钟锡华《光学》）和原技能树综合练习 6 小题。数值核对脚本 `tests/content/N.1.3.verify.py`。

前置：必须前置 N.1.2 大学物理：电磁学（经 N.1.1 带来力学：胡克定律、牛顿第二定律、动能、势能、周期；以及电磁波、LC 振荡）和 M.1.4.1 多元微分学（偏导数、波动方程这个名字）。推荐前置 M.2.1 常微分方程、M.3.1 线性代数不在必须前置链上：二阶线性方程的解法在简谐振动和阻尼振动两课里现讲（只讲用到的“猜 $e^{st}$ 代入”），复数指数在旋转矢量一课现讲；矩阵、特征值、特征向量照 M.1.4.1 写进 `assumes`，耦合振动一课先用对称性猜出两个模式，再说明它们就是矩阵的特征向量。

符号约定：阻尼和受迫振动按 MIT 8.03 写成 $\ddot x + \gamma\dot x + \omega_0^2 x = F_0\cos\omega t/m$，$\gamma = b/m$，品质因数 $Q = \omega_0/\gamma$；面镜和透镜按 OpenStax 的“实正虚负”（$1/d_o + 1/d_i = 1/f$，$m = -d_i/d_o$），并说明有的中文教材用笛卡儿符号法则，正负号写法不同、结论相同。

## 课的安排（21 课）

| 章 | 课 | 内容 |
|---|---|---|
| 简谐振动与阻尼受迫振动 | `shm-basics` | 回复力、弹簧振子的方程、$x = A\cos(\omega t + \varphi)$、$\omega = \sqrt{k/m}$、周期和频率、单摆的小角度近似 |
| | `phasor-energy-beats` | 振幅、频率、相位三个特征量，旋转矢量，复数指数，能量 $\tfrac12 kA^2$，同频振动的合成，拍 |
| | `damped-oscillator` | 阻尼力 $-bv$，欠阻尼、临界阻尼、过阻尼，$\omega_d$，振幅按 $e^{-\gamma t/2}$ 衰减，品质因数 |
| | `driven-resonance` | 受迫振动的稳态振幅和相位、瞬态、位移共振和速度共振、共振峰的宽度和 $Q$、减震 |
| 耦合振动与简正模式 | `coupled-oscillators` | 两个耦合振子的运动方程、同相和反相两个简正模式、一般运动是模式的叠加、能量在两个振子间来回（拍） |
| | `mode-chain` | 用矩阵特征值求简正模式、对称性、N 个振子的链、平移对称给出正弦形状的模式、色散关系，振子无穷多时变成连续的弦 |
| 机械波与波动方程 | `string-wave-equation` | 弦上一小段的受力，推出波动方程，$v = \sqrt{T/\mu}$，通解 $f(x - vt) + g(x + vt)$ |
| | `harmonic-waves` | 平面简谐波 $y = A\cos(kx - \omega t)$，波长、波数、$v = f\lambda$，相位差，能量和强度，平面波和球面波，惠更斯原理，二维的波 |
| | `standing-waves` | 两列反向行波叠加成驻波，波节和波腹，两端固定的弦的简正频率，固定端反射的半波损失，傅里叶级数 |
| | `sound-waves` | 声波是纵波，声速，两端开口和一端封闭的管，声强和分贝 |
| | `dispersion-group-velocity` | 色散介质，相速度和群速度，两列波叠加成波包，波包越短包含的波数越宽 |
| 干涉与衍射 | `double-slit` | 相干，波程差，相长和相消，杨氏双缝的条纹间距和光强 |
| | `thin-film` | 光程，反射时的半波损失，薄膜（肥皂泡、增透膜）、劈尖、牛顿环，迈克尔逊干涉仪 |
| | `single-slit-resolution` | 单缝衍射的暗纹条件、中央亮纹宽度，圆孔衍射和瑞利判据 |
| | `grating-phased-array` | 多缝干涉和光栅方程、主极大变尖，相控阵雷达靠相位差转动波束，单个电子的双缝干涉 |
| 偏振 | `polarization-malus` | 电磁波是横波，线偏振光和自然光，起偏和检偏，马吕斯定律，散射和反射产生偏振，布儒斯特角 |
| | `birefringence-waveplates` | 双折射，四分之一波片和半波片，圆偏振光和椭圆偏振光，偏振光的干涉（液晶屏） |
| 几何光学成像 | `refraction-snell` | 折射率和介质中的光速，折射定律，费马原理，全反射和临界角，光纤 |
| | `mirrors` | 平面镜成像，球面镜的焦距 $f = R/2$，面镜公式、放大率、光路图 |
| | `thin-lens` | 单个球面折射成像，薄透镜公式、磨镜者公式、放大率、像的虚实和正倒 |
| | `optical-instruments` | 眼睛和眼镜（屈光度），相机，放大镜，显微镜和望远镜的放大率 |

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Periodic Oscillations, Harmonic Oscillators | `shm-basics`、`phasor-energy-beats` |
| 1.2 | Damped Free Oscillators | `damped-oscillator` |
| 1.3 | Driven Oscillators, Transient Phenomena, Resonance | `driven-resonance` |
| 1.4 | Coupled Oscillators, Normal Modes | `coupled-oscillators` |
| 1.5 | Beat Phenomena | `phasor-energy-beats`、`coupled-oscillators` |
| 1.6 | Driven Oscillators, Resonance | `driven-resonance` |
| 1.7 | Symmetry, Infinite Number of Coupled Oscillators | `mode-chain` |
| 1.8 | Translation Symmetry | `mode-chain` |
| 1.9 | Wave Equation, Standing Waves, Fourier Series | `string-wave-equation`、`standing-waves` |
| 1.10 | Traveling Waves | `harmonic-waves` |
| 1.11 | Sound Waves | `sound-waves` |
| 2.1 | Maxwell's Equation, Electromagnetic Waves | `polarization-malus`（回顾 N.1.2 讲过的电磁波：E 和 B 都垂直于传播方向，由此说明光能偏振） |
| 2.2 | Dispersive Medium, Phase Velocity, Group Velocity | `dispersion-group-velocity` |
| 2.3 | Fourier Transform, AM Radio | `dispersion-group-velocity`（只讲两列频率相近的波叠加成包络，即调幅信号的样子）；傅里叶变换本身属于 H.1.3，调幅广播的调制解调属于 E.2.3 |
| 2.4 | Uncertainty Principle, 2D Waves | `dispersion-group-velocity`（波包长度和波数范围此消彼长）、`harmonic-waves`（二维的波和波矢）；量子力学的不确定关系属于 N.2.1 |
| 2.5 | 2D and 3D Waves, Snell's Law | `harmonic-waves`、`refraction-snell` |
| 3.1 | Polarization, Polarizer | `polarization-malus` |
| 3.2 | Wave Plates, Radiation | `birefringence-waveplates`、`polarization-malus`（振荡电荷向侧面辐射，散射光是偏振的） |
| 3.3 | Waves in Medium | `refraction-snell`、`thin-film`（折射率、光程） |
| 3.4 | Interference, Soap Bubble | `double-slit`、`thin-film` |
| 3.5 | Phased Radar, Single Electron Interference | `grating-phased-array` |
| 3.6 | Diffraction, Resolution | `single-slit-resolution` |
| 3.7 | Quantum Waves and Gravitational Waves | 不教：物质波和量子力学的波函数属于 N.2.1；引力波超出入门层，本包只在相控阵一课用“单个电子也能干涉”引出物质波 |
| 4.1 | Images Formed by Plane Mirrors | `mirrors` |
| 4.2 | Spherical Mirrors | `mirrors` |
| 4.3 | Images Formed by Refraction | `thin-lens`、`refraction-snell` |
| 4.4 | Thin Lenses | `thin-lens` |
| 4.5 | The Eye | `optical-instruments` |
| 4.6 | The Camera | `optical-instruments` |
| 4.7 | The Simple Magnifier | `optical-instruments` |
| 4.8 | Microscopes and Telescopes | `optical-instruments` |

## CS2023 核心主题（C2）

`scope.json` 对 N.1.3 只给了国标物理学类的一条（0806-1.1.1 光学），没有 CS2023 主题。光学由干涉与衍射、偏振、几何光学成像三章的课负责。

## 学习资源的章节（C3）

- en1（MIT 8.03SC）：就是上面大纲的第 1–3 部分，逐讲落课。
- en2（OpenStax 第三卷）：第 1 章的折射、全反射、偏振在 `refraction-snell`、`polarization-malus`；第 2 章就是大纲第 4 部分；第 3、4 章的干涉衍射和 8.03SC 重复，按中文教材的题型（劈尖、牛顿环、迈克尔逊干涉仪、光栅）补在干涉与衍射四课。
- zh1（叶邦角《力学》）：8.1–8.5 的简谐振动、阻尼、受迫振动、位移共振和速度共振、共振峰锐度、减震、耦合振动，分在第 1、2 章的六课；8.2 振动的合成在 `phasor-energy-beats`（同频、拍）。互相垂直的振动合成（李萨如图形）不教：不在 8.03SC 大纲里，后面的技能也不用。
- zh3（西安交大）：旋转矢量、简谐振动的能量、平面简谐波的波函数、波的能量和强度、惠更斯原理、驻波与半波损失、杨氏双缝、光程、等厚和等倾干涉、迈克尔逊干涉仪、单缝和光栅衍射、马吕斯定律、布儒斯特定律、双折射、偏振光的干涉、圆和椭圆偏振光，都在对应的课里。多普勒效应不教：不在本技能的大纲（8.03SC Lecture 11 讲声波的方程和声速）和综合练习里，必须后继也不用。
- zh4（钟锡华《光学》）：费马原理、几何光学三定律、傍轴折射球面成像公式在 `refraction-snell`、`thin-lens`；齐明点超出入门层，不教。

## 原技能树综合练习（C4）

| 小题 | 内容 | 由哪一课教到 |
|---|---|---|
| (1) | 弹簧振子的固有角频率、频率、周期，阻尼的 $Q$ 和 $\omega_d$，共振 | `shm-basics`、`damped-oscillator`、`driven-resonance` |
| (2) | 墙—m—m—墙三根弹簧的运动方程、两个简正模式 | `coupled-oscillators`、`mode-chain` |
| (3) | 弦的波速、基频，驻波由两列反向行波叠加 | `string-wave-equation`、`standing-waves` |
| (4) | 双缝条纹间距、单缝第一级暗纹 | `double-slit`、`single-slit-resolution` |
| (5) | 自然光经过两块夹角 60° 的偏振片 | `polarization-malus` |
| (6) | 薄凸透镜的像距、放大率、虚实正倒，全反射临界角 | `thin-lens`、`refraction-snell` |

## 后继技能用到的写法（C5）

必须后继：N.2.1 量子力学基础、E.1.9 激光原理与技术，都还没有内容包。按它们的大纲和综合练习，直接用到的有：波长、频率、波数、相位、驻波和简正模式（谐振腔里的纵模）、干涉和相干、单缝衍射、偏振、折射率和全反射。这些都在本包讲到并写进 `terms`。
