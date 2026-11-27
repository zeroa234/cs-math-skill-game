# E.2.4 无线与移动通信：覆盖表

**状态（2026-11-27）：计划（第 12 轮写的覆盖表，课还没写）。** 依据 `../cs-math-skill-tree/data/outlines/E.2.4.json`（主来源 Tse & Viswanath *Fundamentals of Wireless Communication*；4G/5G 物理层取 Zaidi 等 *5G Physical Layer* 的章目录；中文主课是北京交通大学《无线通信基础》，蜂窝和频率规划取杭州电子科技大学《移动通信》）和原技能树综合练习。数值核对脚本将是 `tests/content/E.2.4.verify.py`。

前置：必须前置是 E.2.3 通信原理（调制、载波、基带、码元、误码率、信噪比、信道容量、dBm、加性高斯白噪声、码间干扰、Q 函数、星座图、匹配滤波器；E.2.3 写明 OFDM、扩频留给本站）和 M.3.1 线性代数（矩阵、特征值、奇异值分解，MIMO 用），H.1.3、M.6.1 在闭包里（傅里叶变换、卷积、快速傅里叶变换、概率密度、正态分布、指数分布）。E.2.1、M.6.5 只是推荐前置，不继承。

## 课的安排（26 课，计划）

| 章 | 课 | 内容 |
|---|---|---|
| 无线信道与路径损耗 | `wireless-intro` | 无线系统的组成和特点（频谱有限、信道随位置和时间变），这一站要解决的三个问题：衰落、干扰、多用户 |
|  | `free-space` | 自由空间路径损耗（Friis 公式、FSPL 的分贝式，综合练习 1 前半），天线增益、链路预算 |
|  | `propagation` | 反射、绕射、散射，两径模型和 d⁴ 规律，对数距离路径损耗模型和路径损耗指数（综合练习 1 后半），阴影衰落和对数正态分布 |
|  | `link-budget` | 链路预算：发射功率、天线增益、路径损耗、衰落余量、接收机灵敏度，求最大覆盖距离 |
| 多径衰落与多普勒 | `multipath-model` | 多径的输入输出模型：各径的时延和衰减，抽头延迟线，时延扩展 |
|  | `coherence` | 相干带宽和时延扩展、相干时间和多普勒扩展（综合练习 2），平坦/频率选择性、慢/快衰落 |
|  | `rayleigh-rician` | 瑞利衰落和莱斯衰落（K 因子），包络和功率的分布，衰落深度的概率，多普勒谱 |
|  | `fading-ber` | 瑞利衰落下 BPSK 的误码率和高信噪比近似 1/(4γ)，和 AWGN 的差距（综合练习 3 前半） |
| 分集技术 | `time-diversity` | 分集的基本思想和分集阶数，时间分集：重复编码、交织、信道编码 |
|  | `antenna-diversity` | 空间（天线）分集：选择合并、等增益合并、最大比合并（综合练习 3 后半），Alamouti 发射分集，宏分集 |
|  | `frequency-diversity` | 频率分集：均衡、RAKE 接收（扩频）、OFDM 加编码，分集增益 |
|  | `fading-capacity` | AWGN 信道容量回顾，衰落信道的中断容量和遍历容量，信道估计的误差（导频） |
| OFDM | `ofdm-principle` | 把宽带信道分成许多窄带子载波，子载波正交、用 IFFT 产生（综合练习 4 前半） |
|  | `cyclic-prefix` | 循环前缀把线性卷积变成循环卷积，单抽头均衡，循环前缀长度和开销（综合练习 4 后半） |
|  | `ofdm-design` | OFDM 的参数设计（子载波间隔、符号长度、多普勒），峰均比和频偏敏感，OFDMA 资源分配，NR 波形 |
| MIMO | `mimo-capacity` | 多天线的复用能力：确定 MIMO 信道的奇异值分解和容量，高信噪比时容量随 min(Nt, Nr) 增长（综合练习 5） |
|  | `mimo-channel` | MIMO 信道的物理建模：视距和散射、角度分辨率、信道的秩，衰落 MIMO 信道 |
|  | `mimo-receivers` | V-BLAST 和接收机结构：迫零、MMSE、串行干扰消除，快衰落 MIMO 信道，D-BLAST |
|  | `dmt-beamforming` | 分集–复用折中，空间复用和空间分集的区别，波束赋形，大规模 MIMO 和 NR 多天线 |
| 多址接入 | `fdma-tdma` | 按频率和按时隙划分用户：窄带蜂窝系统里的 FDMA、TDMA（综合练习 6） |
|  | `cdma` | 直接序列扩频、扩频增益、码分多址、远近效应和功率控制、跳频 |
|  | `multiuser` | 上行和下行的多用户容量，叠加编码和串行干扰消除，多用户分集和比例公平调度，多天线上行与下行（SDMA） |
| 蜂窝系统与频率复用 | `cellular-reuse` | 蜂窝的思路，六边形小区、簇大小 N 和复用距离 D/R = √(3N)，同频干扰和信干比（综合练习 7） |
|  | `cellular-capacity` | 扇区化、小区分裂、切换，话务量和爱尔兰 B 公式的结论，多天线在蜂窝网络里的作用 |
| 4G/5G物理层概述 | `lte-phy` | LTE 物理层：下行 OFDMA、上行 SC-FDMA、15 kHz 子载波、资源块、MIMO（综合练习 8 前半） |
|  | `nr-phy` | 5G NR：参数集 15×2^μ kHz、毫米波、大规模 MIMO 和波束管理、灵活的帧结构（综合练习 8 后半） |

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Book objective | 不教：全书的写作目标，不是知识内容 |
| 1.2 | Wireless systems | `wireless-intro` |
| 1.3 | Book outline | 不教：全书各章导读，不是知识内容 |
| 2.1 | Physical modeling for wireless channels | `free-space`、`propagation`、`link-budget` |
| 2.2 | Input /output model of the wireless channel | `multipath-model` |
| 2.3 | Time and frequency coherence | `coherence` |
| 2.4 | Statistical channel models | `rayleigh-rician` |
| 3.1 | Detection in a Rayleigh fading channel | `fading-ber` |
| 3.2 | Time diversity | `time-diversity` |
| 3.3 | Antenna diversity | `antenna-diversity` |
| 3.4 | Frequency diversity | `frequency-diversity` |
| 3.5 | Impact of channel uncertainty | `fading-capacity` |
| 4.1 | Introduction | `cellular-reuse` |
| 4.2 | Narrowband cellular systems | `fdma-tdma` |
| 4.3 | Wideband systems: CDMA | `cdma` |
| 4.4 | Wideband systems: OFDM | `ofdm-principle`、`cyclic-prefix`、`ofdm-design` |
| 5.1 | AWGN channel capacity | `fading-capacity` |
| 5.2 | Linear time-invariant Gaussian channels | `fading-capacity` |
| 5.3 | Capacity of fading channels | `fading-capacity` |
| 6.1 | Uplink AWGN channel | `multiuser` |
| 6.2 | Downlink AWGN channel | `multiuser` |
| 6.3 | Multiuser diversity | `multiuser` |
| 6.4 | Multiuser diversity: system aspects | `multiuser` |
| 7.1 | Multiplexing capability of deterministic MIMO channels | `mimo-capacity` |
| 7.2 | Physical modeling of MIMO channels | `mimo-channel` |
| 7.3 | Modeling of MIMO fading channels | `mimo-channel` |
| 8.1 | The V-BLAST architecture | `mimo-receivers` |
| 8.2 | Fast fading MIMO channel | `mimo-receivers` |
| 8.3 | Receiver architectures | `mimo-receivers` |
| 8.4 | D-BLAST: an outage-optimal architecture | `mimo-receivers` |
| 9.1 | Diversity–multiplexing tradeoff | `dmt-beamforming` |
| 9.2 | Universal code design for optimal diversity–multiplexing tradeoff | 不教：达到分集–复用折中的通用空时码构造，超出入门层（课里只讲折中曲线本身和 Alamouti 码） |
| 10.1 | Uplink with multiple receive antennas | `multiuser` |
| 10.2 | Downlink with multiple transmit antennas | `multiuser` |
| 10.3 | Multiple antennas in cellular networks: a system view | `cellular-capacity` |
| 11 | 5G Radio Access | `nr-phy` |
| 12 | NR Physical Layer: Overview | `lte-phy`、`nr-phy` |
| 13 | NR Waveform | `ofdm-design`、`nr-phy` |
| 14 | Multi-antenna Techniques | `dmt-beamforming`、`nr-phy` |

## CS2023 核心主题（C2）

写课时查 `scope.json` 补上。

## 学习资源的章节（C3）

写课时逐条核对：北交大《无线通信基础》第 2 章（电波传播机制、反射与透射、绕射与散射、链路预算）、第 3 章（大尺度衰落、两径模型、小尺度衰落、莱斯、多普勒谱）、第 4 章（时延扩展、多普勒扩展）、第 8 章（分集原理、微分集、宏分集、合并、分集增益）、第 9 章（跳频、直接序列扩频与 CDMA）、第 10 章（OFDM 系统模型、数字实现、抗多径、参数设计、OFDMA）、第 11 章（多天线容量、波束赋形、空时编码、大规模天线）；杭电《移动通信》1.5 多址方式、1.10 5G 概述、2.1–2.5 移动通信网（体制、干扰、频率规划、多信道共用）、4.7 OFDM、7.10–7.11 LTE。

## 综合练习（C4）

| 小题 | 负责的课 |
|---|---|
| (1) 自由空间路径损耗，对数距离模型，阴影衰落的分布 | `free-space`、`propagation` |
| (2) 相干带宽、多普勒频移、相干时间，频率选择性和快衰落 | `coherence` |
| (3) 瑞利衰落下 BPSK 的误码率和近似，二分集最大比合并 | `fading-ber`、`antenna-diversity` |
| (4) OFDM 的子载波间隔、符号长度，循环前缀 | `ofdm-principle`、`cyclic-prefix` |
| (5) MIMO 容量随天线数的增长，空间复用和空间分集 | `mimo-capacity`、`dmt-beamforming` |
| (6) FDMA、TDMA、CDMA、OFDMA 怎样划分用户 | `fdma-tdma`、`cdma`、`ofdm-design` |
| (7) 簇大小 7 时的信干比，簇大小的影响 | `cellular-reuse` |
| (8) LTE 和 NR 物理层的波形、子载波间隔、多天线 | `lte-phy`、`nr-phy` |

## 后继技能用到的（C5）

E.2.4 没有直接解锁的技能，是通信工程远征的终点之一（国标通信工程专业示例二的“移动通信”）。
