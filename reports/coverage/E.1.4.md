# E.1.4 光电子与光纤通信：覆盖表

**状态（2026-11-27）：已写完（18 课，大纲 17 节全部有课）。** 依据 `vendor/cs-math-skill-tree/output/outlines.json`（主来源 MIT 6.013 开放教材第 12 章 *Optical Communications* 与 MIT 6.974 *Fundamentals of Photonics: Quantum Electronics* 讲义；英文补充 Cornell ECE 5330 *Semiconductor Optoelectronics*；中文主课南京理工大学《通信系统》第二章光纤通信系统，中文补充西安交通大学《光电子学（二）》光调制与光电探测部分）和原技能树综合练习。数值核对脚本为 `tests/content/E.1.4.verify.py`。

前置：必须前置只有 E.1.1 电磁场与电磁波（其闭包已讲折射率、全反射背景、电磁波、波动方程、坡印廷矢量、波数、截止频率、品质因数、布儒斯特角、欧姆定律与电功率等）。N.1.3 振动、波动与光学、N.2.2 固体与半导体物理、E.2.3 通信原理只是推荐前置，不继承：光程与干涉、双折射与波片、光子与能级、半导体带隙与电子–空穴对、自发与受激辐射、粒子数反转、耗尽区与雪崩击穿、dBm 与误码率等概念均在本包里从头讲清。

## 课的安排（18 课）

| 章 | 课 | 内容 |
|---|---|---|
| 光波导与光纤模式 | `fiber-intro` | 光纤通信与应用概貌，光在介质界面的折射与全反射，阶跃折射率光纤的结构、数值孔径与最大入射角（综合练习 1） |
|  | `slab-waveguide` | 介质平板波导的相位自洽条件、导模与横向驻波、模数估算、TE 模与 TM 模及截止条件 |
|  | `fiber-modes` | 圆柱光纤的导模与归一化频率 $V$，单模条件 $V < 2.405$ 与截止波长，单模、多模与渐变折射率光纤（综合练习 2） |
| 色散与损耗 | `fiber-loss` | 光功率的 dBm 与光纤衰减系数（dB/km），瑞利散射（$\lambda^{-4}$）、本征吸收与氢氧根吸收峰，850/1310/1550 nm 通信窗口与弯曲损耗（综合练习 3 前半） |
|  | `fiber-dispersion` | 群速度与群折射率，模式色散、材料色散与波导色散（1310 nm 零色散抵消），色散系数 $D$、脉冲展宽与色散受限速率，色散补偿光纤（综合练习 3 后半） |
| 半导体激光器与LED | `light-matter` | 光子能量 $E = hc/\lambda$，半导体价带、导带、带隙与直接/间接带隙，受激吸收、自发辐射、受激辐射与粒子数反转，速率方程直觉（综合练习 4 前半） |
|  | `led-and-ld` | 发光二极管（LED）原理、宽谱与调制速率受限；法布里–珀罗谐振腔、纵模间隔、阈值增益、阈值电流 $I_{th}$ 与 $P$-$I$ 特性曲线（综合练习 4 后半） |
|  | `laser-structures` | 双异质结与量子阱、分布式反馈（DFB）单纵模激光器、垂直腔面发射激光器（VCSEL）、光发射机结构与直接调制中的频率啁啾 |
| 光电探测器 | `photodetector-basics` | 外光电效应（光电管与光电倍增管）与内光电效应，截止波长，量子效率 $\eta$ 与响应度 $R = \eta q\lambda/(hc)$（综合练习 5 前半） |
|  | `pin-and-apd` | PIN 光电二极管（耗尽区宽度与渡越时间权衡），雪崩光电二极管（APD）的碰撞电离、倍增增益 $M$、高偏压、过剩噪声与温度敏感性（综合练习 5 后半） |
|  | `optical-receiver` | 光接收机前端与跨阻放大器，散粒噪声与热噪声，光接收信噪比、误码率与接收机灵敏度、量子极限概念 |
| 光调制器 | `crystal-optics` | 直接调制与外调制的取舍，各向异性晶体中的双折射（寻常光与非常光），偏振态与半波片、四分之一波片 |
|  | `electro-optic` | 线性电光效应（泡克耳斯效应）与半波电压 $V_\pi$，相位调制与马赫–曾德尔（MZI）强度调制器、消光比与低啁啾优势，电吸收调制器（综合练习 6） |
|  | `acousto-optic-switches` | 声光调制（布拉格衍射与多普勒频移），磁光法拉第效应与光隔离器，光学干涉仪（马赫–曾德尔与法布里–珀罗）与光开关（MEMS、热光、电光） |
| 光放大器 | `edfa` | 长距离传输为什么需要纯光放大器而非光–电–光中继，掺铒光纤放大器（EDFA）的三能级机制与 980/1480 nm 泵浦，C 波段增益与增益饱和（综合练习 7 后半） |
|  | `soa-ase-noise` | 自发辐射放大（ASE）噪声、光放大器噪声系数（3 dB 量子极限）与光信噪比（OSNR），半导体光放大器（SOA）与分布式拉曼放大器的对比 |
| 光纤通信系统与波分复用 | `optical-link-budget` | 光纤链路功率预算（发射功率、光纤损耗、接头与熔接损耗、灵敏度与系统余量），损耗受限距离与色散受限距离的比较及工程系统实例（综合练习 7 前半） |
|  | `wdm-systems` | 波分复用（WDM/CWDM/DWDM）原理，频率间隔与波长间隔换算 $\Delta\lambda = \lambda^2\Delta f/c$，C 波段信道数，阵列波导光栅、光纤布拉格光栅滤波器与光分插复用器（综合练习 8） |

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1.1 | Introduction to optical communications and photonics | `fiber-intro` |
| 1.1.2 | Applications of photonics | `fiber-intro` |
| 1.1.3 | Link equations | `optical-receiver`、`optical-link-budget` |
| 1.1.4 | Examples of optical communications systems | `optical-link-budget`、`wdm-systems` |
| 1.2.1 | Dielectric slab waveguides | `slab-waveguide` |
| 1.2.2 | Optical fibers | `fiber-intro`、`fiber-modes` |
| 1.3.1 | Physical principles of stimulated emission and laser amplification | `light-matter`、`edfa` |
| 1.3.2 | Laser oscillators | `led-and-ld`、`laser-structures` |
| 1.4.1 | Phototubes | `photodetector-basics` |
| 1.4.2 | Photodiodes | `photodetector-basics`、`pin-and-apd`、`optical-receiver` |
| 1.4.3 | Frequency-multiplexing devices and filters | `wdm-systems` |
| 1.4.4 | Interferometers | `electro-optic`、`acousto-optic-switches` |
| 1.4.5 | Optical switches | `acousto-optic-switches` |
| 2 | Optical Fibers | `fiber-modes`、`fiber-loss`、`fiber-dispersion` |
| 3 | Rate Equations, Dispersion, Absorption and Gain | `fiber-loss`、`fiber-dispersion`、`light-matter` |
| 4 | Optical Amplifiers and Lasers | `led-and-ld`、`laser-structures`、`edfa`、`soa-ase-noise` |
| 5 | Electro- and Acousto-Optic Modulation | `crystal-optics`、`electro-optic`、`acousto-optic-switches` |

## CS2023 核心主题（C2）

E.1.4 属于电子信息类专业课（国标通信工程专业示例二的“光纤通信”/光电子方向），不在 CS2023 核心主题覆盖范围内。

## 学习资源的章节（C3）

已对照中英文课程目录安排去处：

| 资源的小节 | 去处 |
|---|---|
| 南京理工《通信系统》2.1.1 光纤通信系统概述 | `fiber-intro`、`optical-link-budget` |
| 2.2.1–2.2.2、2.2.5 几何光学导光、波动方程导光、单模光纤 | `fiber-intro`、`slab-waveguide`、`fiber-modes` |
| 2.2.3–2.2.4 光纤损耗、光纤色散 | `fiber-loss`、`fiber-dispersion` |
| 2.3.1–2.3.4 激光物理基础、LD、LED、光发射机 | `light-matter`、`led-and-ld`、`laser-structures` |
| 2.4.1–2.4.2 光检测器、光接收机 | `photodetector-basics`、`pin-and-apd`、`optical-receiver` |
| 2.5.1 光放大器 | `edfa`、`soa-ase-noise` |
| 2.5.3–2.5.4 波分复用系统与单元部件、2.6.1 光纤通信系统设计 | `optical-link-budget`、`wdm-systems` |
| 西交大《光电子学（二）》第 1–3 周 光调制、晶体光学、电光/声光/磁光调制 | `crystal-optics`、`electro-optic`、`acousto-optic-switches` |
| 西交大《光电子学（二）》第 4–5 周 光电探测性能参数、外/内光电效应、光电探测器 | `photodetector-basics`、`pin-and-apd`、`optical-receiver` |
| Cornell ECE 5330 Ch.3/5/7/8/9/11/12（吸收、探测器、LED、平板波导、SOA、激光器与 VCSEL） | `slab-waveguide`、`light-matter`、`led-and-ld`、`laser-structures`、`photodetector-basics`、`pin-and-apd`、`soa-ase-noise` |
| MIT 6.013 Ch.12 与 MIT 6.974 讲义 | 见大纲逐节表（1.1.1–5 全覆盖） |

## 综合练习（C4）

| 小题 | 负责的课 |
|---|---|
| (1) 阶跃光纤的数值孔径、最大入射角与导光原理 | `fiber-intro` |
| (2) 单模光纤的归一化频率 $V$、单模判据与截止波长 | `fiber-modes` |
| (3) 1550 nm 损耗、色散脉冲展宽与 10 Gb/s 影响，损耗与零色散窗口原因 | `fiber-loss`、`fiber-dispersion` |
| (4) 1550 nm 与 850 nm 光子能量，LD 与 LED 差异，阈值电流 | `light-matter`、`led-and-ld` |
| (5) PIN 响应度与光电流，APD 灵敏度优势与代价 | `photodetector-basics`、`pin-and-apd` |
| (6) 直接调制与外调制区别，马赫–曾德尔调制器半波电压 | `crystal-optics`、`electro-optic` |
| (7) 光纤链路功率预算与系统余量，长距离光放大器（EDFA） | `optical-link-budget`、`edfa` |
| (8) DWDM 100 GHz 对应波长间隔与 C 波段信道数 | `wdm-systems` |

## 后继技能用到的（C5）

E.1.4 没有直接解锁的后继技能，是通信工程远征的终点站之一（对应国标通信工程专业示例二的光纤通信课程）。
