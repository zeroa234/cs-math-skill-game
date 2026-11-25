# E.2.3 通信原理：覆盖表

**状态（2026-11-23 第 5 轮）：已写完。** 28 课，56 节里 51 节有课、5 节写明不教，内容包 `data/content/E.2.3.yaml`，数值核对 `tests/content/E.2.3.verify.py`。 依据 `../cs-math-skill-tree/output/outlines.json` 的 E.2.3（主来源 Couch《Digital and Analog Communication Systems》第 8 版第 1–7 章，只核目录）、`data/curation/learning-paths/E.2.3.json`（南京邮电大学《通信原理》第 1–5、7、8 章，北京邮电大学《通信原理》匹配滤波和最佳接收部分，MIT 6.02 开放教材 *Bits, Signals, and Packets* 第 4–14 章）和原技能树综合练习 8 小题。

前置：必须前置 H.1.3 信号与系统（傅里叶变换、频谱、卷积、线性时不变系统、频率响应、采样定理、量化、功率谱密度、分贝、带宽、二进制）、M.6.1 概率论（随机变量、概率密度、正态分布、期望、方差、独立）。这些术语直接用。推荐前置 M.6.3 随机过程、M.6.5 信息论还没有内容包，随机过程（平稳、自相关）和信息量、熵在用到时现讲。

## 课的安排（28 课）

| 课 | 章 | 内容 |
|---|---|---|
| `system-model` | 通信系统模型 | 模拟和数字信源，通信系统框图，频段划分，电磁波的传播方式，有效性和可靠性指标（码元速率、信息速率、误码率） |
| `information-capacity` | 通信系统模型 | 信息量、熵，香农信道容量，理想通信系统（综合练习 1） |
| `signals-power` | 信道与噪声 | 信号的功率和能量、有效值、dB 和 dBm，带宽的几种定义 |
| `random-processes` | 信道与噪声 | 随机过程、平稳、自相关函数，功率谱密度和维纳–辛钦定理 |
| `noise-linear` | 信道与噪声 | 随机过程通过线性系统，高斯过程，白噪声、热噪声 kTB（综合练习 3），带通噪声的同相和正交分量 |
| `channel-models` | 信道与噪声 | 加性和乘性干扰，恒参和随参信道，多径和衰落，接收信号加噪声 |
| `bandpass-envelope` | 模拟调制 | 带通信号的复包络，调制信号的表示，带通信号的频谱，带通采样定理 |
| `am-dsb` | 模拟调制 | AM、调制指数和效率、包络检波，DSB-SC 和相干解调（综合练习 2） |
| `ssb-vsb-fdm` | 模拟调制 | SSB、VSB，频分复用、调频立体声，超外差接收机 |
| `fm-pm` | 模拟调制 | 调相和调频，频偏、调频指数，卡森带宽，鉴频 |
| `analog-noise` | 模拟调制 | 模拟系统的输出信噪比：AM、DSB、SSB、FM，门限效应 |
| `pam-pcm` | 基带传输与码间干扰 | 采样复习，PAM，量化和 PCM，量化信噪比 6.02n + 1.76 dB，A 律压扩，PCM 的输出信噪比 |
| `dpcm-dm-tdm` | 基带传输与码间干扰 | DPCM、增量调制，时分复用和帧（E1），分组传输，PWM、PPM |
| `line-codes` | 基带传输与码间干扰 | 数字信令，线路码（单极性、双极性、归零、AMI、HDB3、曼彻斯特）及其频谱 |
| `isi-eye` | 基带传输与码间干扰 | 码间干扰的成因，眼图（综合练习 4） |
| `nyquist` | 奈奎斯特准则 | 奈奎斯特第一准则，2B 波特，升余弦滚降（综合练习 4），频带利用率 |
| `partial-response-eq` | 奈奎斯特准则 | 部分响应（双二进制）和预编码，迫零均衡 |
| `matched-filter` | 最佳接收与匹配滤波 | 匹配滤波器、最大输出信噪比 2E/N₀，相关接收（综合练习 6） |
| `binary-error` | 最佳接收与匹配滤波 | 二进制判决的误码率、Q 函数、最佳门限，单极性和双极性基带系统的误码率 |
| `binary-keying` | 数字调制 | 2ASK（OOK）、2FSK、2PSK、2DPSK，波形和带宽 |
| `mary-qam` | 数字调制 | QPSK、8PSK、16-QAM，星座图，比特率和码元速率（综合练习 5），MSK 和 GMSK |
| `bandpass-ber` | 误码率分析 | 相干检测的 OOK、BPSK、FSK，非相干检测的 OOK、FSK 和 DPSK（综合练习 5） |
| `compare-systems` | 误码率分析 | QPSK 和 MSK 的误码率，各种调制的比较，频带利用率和 E_b/N₀ |
| `error-control` | 信道编码初步 | 差错控制方式（ARQ、FEC），奇偶校验，码距和检错纠错能力 |
| `linear-block` | 信道编码初步 | 线性分组码，(7,4) 汉明码的生成和校验，伴随式译码（综合练习 8），循环码和 CRC |
| `convolutional` | 信道编码初步 | 卷积码的编码器和网格图，维特比译码 |
| `carrier-sync` | 同步 | 锁相环，平方环、科斯塔斯环（综合练习 7），频率合成器 |
| `symbol-frame-sync` | 同步 | 码元同步（早迟门），群同步（巴克码），时分复用的帧同步 |

## 大纲逐节（C1）

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Digital and Analog Sources and Systems | `system-model` |
| 1.2 | Block Diagram of a Communication System | `system-model` |
| 1.3 | Frequency Allocations | `system-model` |
| 1.4 | Propagation of Electromagnetic Waves | `system-model` |
| 1.5 | Information Measure | `information-capacity` |
| 1.6 | Channel Capacity and Ideal Communication Systems | `information-capacity` |
| 1.7 | Coding | `error-control` |
| 2.1 | Properties of Signals and Noise | `signals-power` |
| 2.2 | Fourier Transform and Spectra | 不教：属于 H.1.3（傅里叶变换、频谱，必须前置已讲） |
| 2.3 | Power Spectral Density and Autocorrelation Function | `random-processes` |
| 2.4 | Fourier Series | 不教：属于 H.1.3（周期信号的频谱，必须前置已讲） |
| 2.5 | Review of Linear Systems | 不教：属于 H.1.3（线性时不变系统、频率响应、卷积，必须前置已讲） |
| 2.6 | Bandlimited Signals and Noise | `pam-pcm` |
| 2.7 | Bandwidth of Signals | `signals-power` |
| 3.1 | Pulse Amplitude Modulation | `pam-pcm` |
| 3.2 | Pulse Code Modulation | `pam-pcm` |
| 3.3 | Digital Signaling | `line-codes` |
| 3.4 | Line Codes and Spectra | `line-codes` |
| 3.5 | Intersymbol Interference | `isi-eye`、`nyquist` |
| 3.6 | Differential Pulse Code Modulation | `dpcm-dm-tdm` |
| 3.7 | Delta Modulation | `dpcm-dm-tdm` |
| 3.8 | Time-Division Multiplexing | `dpcm-dm-tdm`、`symbol-frame-sync` |
| 3.9 | Packet Transmission System | `dpcm-dm-tdm` |
| 3.10 | Pulse Time Modulation: Pulse Width Modulation and Pulse Position Modulation | `dpcm-dm-tdm` |
| 4.1 | Complex Envelope Representation of Bandpass Waveforms | `bandpass-envelope` |
| 4.2 | Representation of Modulated Signals | `bandpass-envelope` |
| 4.3 | Spectrum of Bandpass Signals | `bandpass-envelope` |
| 4.4 | Bandpass Sampling Theorem | `bandpass-envelope` |
| 4.5 | Received Signal Plus Noise | `channel-models` |
| 4.6 | Detector Circuits | `am-dsb`、`fm-pm` |
| 4.7 | Phase-Locked Loops and Frequency Synthesizers | `carrier-sync` |
| 4.8 | Transmitters and Receivers | `ssb-vsb-fdm` |
| 5.1 | Amplitude Modulation | `am-dsb` |
| 5.2 | Double-Sideband Suppressed Carrier | `am-dsb` |
| 5.3 | Asymmetric Sideband Signals | `ssb-vsb-fdm` |
| 5.4 | Phase Modulation and Frequency Modulation | `fm-pm` |
| 5.5 | Frequency-Division Multiplexing and FM Stereo | `ssb-vsb-fdm` |
| 5.6 | Binary Modulated Bandpass Signaling | `binary-keying` |
| 5.7 | Multilevel Modulated Bandpass Signaling | `mary-qam` |
| 5.8 | Minimum-Shift Keying and GMSK | `mary-qam` |
| 5.9 | Orthogonal Frequency Division Multiplexing (OFDM) | 不教：属于 E.2.4（必须后继《无线与移动通信》4.4 Wideband systems: OFDM） |
| 5.10 | Spread Spectrum Systems | 不教：属于 E.2.4（必须后继《无线与移动通信》4.3 Wideband systems: CDMA） |
| 6.1 | Some Basic Definitions | `random-processes` |
| 6.2 | Power Spectral Density | `random-processes` |
| 6.3 | Linear Systems | `noise-linear` |
| 6.4 | The Gaussian Random Process | `noise-linear` |
| 6.5 | Bandpass Processes | `noise-linear` |
| 6.6 | Matched Filters | `matched-filter` |
| 7.1 | Error Probabilities for Binary Signaling | `binary-error` |
| 7.2 | Performance of Baseband Binary Systems | `binary-error` |
| 7.3 | Coherent Detection of Bandpass Binary Signals | `bandpass-ber` |
| 7.4 | Noncoherent Detection of Bandpass Binary Signals | `bandpass-ber` |
| 7.5 | Quadrature Phase-Shift Keying and Minimum-Shift Keying | `compare-systems` |
| 7.6 | Comparison of Digital Signaling Systems | `compare-systems` |
| 7.7 | Output Signal-to-Noise Ratio for PCM Systems | `pam-pcm` |
| 7.8 | Output Signal-to-Noise Ratios for Analog Systems | `analog-noise` |

`omitted`：Couch 第 8 章（有线和无线通信的应用：电话网、卫星、链路预算）和各章的小结、例题、习题、附录，本包同样不教。

中文主课另有、Couch 目录里没有单列的：部分响应系统（南邮 4.8，`partial-response-eq`）、时域均衡（`partial-response-eq`）、二进制差分相移键控 2DPSK（南邮 5.2，`binary-keying`、`bandpass-ber`）、恒参和随参信道（南邮 2.3–2.4，`channel-models`）、差错控制编码的线性分组码、循环码、卷积码（南邮第 7 章，`linear-block`、`convolutional`）、载波同步、码元同步、群同步（南邮第 8 章，`carrier-sync`、`symbol-frame-sync`），都按中文主课教到。

## CS2023 核心主题（C2）

电子信息类专业课，`scope.json` 没有 CS2023 主题。

## 原技能树综合练习（C4）

| 小题 | 内容 | 由哪一课教到 |
|---|---|---|
| (1) | 数字通信系统框图，3 kHz、30 dB 电话信道的香农容量 | `system-model`、`information-capacity` |
| (2) | AM、DSB-SC、SSB 的带宽，包络检波和相干解调 | `am-dsb`、`ssb-vsb-fdm` |
| (3) | 290 K、1 MHz 的热噪声功率（dBm），AWGN 模型的假设 | `signals-power`、`noise-linear` |
| (4) | 码间干扰，奈奎斯特速率 2B，滚降 0.25 时 1 MBaud 的带宽，眼图 | `isi-eye`、`nyquist` |
| (5) | 16-QAM 的比特率，BPSK 在 9.6 dB 的误比特率，QPSK 和 BPSK 比较 | `mary-qam`、`bandpass-ber`、`compare-systems` |
| (6) | 最佳接收机等于匹配滤波加采样判决，它最大化的是什么 | `matched-filter`、`binary-error` |
| (7) | 接收机要做的几种同步，科斯塔斯环 | `carrier-sync`、`symbol-frame-sync` |
| (8) | (7,4) 汉明码的码率、最小码距、检错纠错能力 | `error-control`、`linear-block` |

## 后继技能用到的写法（C5）

必须后继 E.2.4 无线与移动通信（还没有内容包）：用到 AWGN 信道和信道容量、E_b/N₀ 与误码率、BPSK 和 QPSK 的误码率式子、多径和衰落的基本概念、QAM 星座、匹配滤波和相干检测。这些写进本包 `terms`。OFDM 和 CDMA 由 E.2.4 自己教。
