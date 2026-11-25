# H.1.3 信号与系统：覆盖表

**状态（2026-11-22）：已写完。** 依据 `vendor/cs-math-skill-tree/output/outlines.json` 与 `vendor/cs-math-skill-tree/output/skilltree.json`，主来源为 Phillips, Parr & Riskin *Signals, Systems, and Transforms*（来源 A，第 2、3、5、6、9、10、11、12 章）与 Mitra *Digital Signal Processing*（来源 B，第 5–9 章可选延伸），并对照东南大学《信号与系统》（`zh1`）、北京交通大学《数字信号处理》（`zh2`）和 MIT 6.003 *Signals and Systems*（`en1`）补齐完整主线。

游戏内部章序：`1. 连续与离散信号`、`2. LTI`、`3. 采样`、`4. 卷积`、`5. 频域`、`6. 数字滤波基本模型`。本技能的唯一必须前置是 `M.1.3`（一元积分学，前置链 `M.1.1` → `M.1.2` → `M.1.3`）；常微分方程、电路与模拟电子、傅里叶分析与线性代数仅为推荐前置，因此欧拉公式、复指数、微分/差分方程、卷积、傅里叶变换、z 变换与零极点均在本包从零定义并配有分步例题。

`node scripts/check-coverage.mjs H.1.3` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | 2.1 Transformations of Continuous-Time Signals | `ct-signals-transforms` |
| 1.2 | 2.2 Signal Characteristics | `ct-signal-types-singularity` |
| 1.3 | 2.3 Common Signals in Engineering | `ct-signal-types-singularity` |
| 1.4 | 2.4 Singularity Functions | `ct-signal-types-singularity` |
| 1.5 | 2.5 Mathematical Functions for Signals | `ct-signals-transforms` |
| 1.6 | 2.6 Continuous-Time Systems | `systems-and-interconnections` |
| 1.7 | 2.7 Properties of Continuous-Time Systems | `system-properties-lti` |
| 2.1 | 3.1 Impulse Representation of Continuous-Time Signals | `ct-convolution` |
| 2.2 | 3.2 Convolution for Continuous-Time LTI Systems | `ct-convolution` |
| 2.3 | 3.3 Properties of Convolution | `convolution-properties-and-lti` |
| 2.4 | 3.4 Properties of Continuous-Time LTI Systems | `convolution-properties-and-lti` |
| 2.5 | 3.5 Differential-Equation Models | `differential-and-difference-eqs` |
| 2.6 | 3.7 System Response for Complex-Exponential Inputs | `eigenfunctions-complex-exp` |
| 2.7 | 3.8 Block Diagrams | `differential-and-difference-eqs` |
| 3.1 | 5.1 Definition of the Fourier Transform | `ctft-definition-and-pairs` |
| 3.2 | 5.2 Properties of the Fourier Transform | `ctft-properties-energy-power` |
| 3.3 | 5.3 Fourier Transforms of Time Functions | `ctft-definition-and-pairs` |
| 3.4 | 5.4 Sampling Continuous-Time Signals | `sampling-and-aliasing`, `ctft-properties-energy-power` |
| 3.5 | 5.5 Application of the Fourier Transform | `ctft-properties-energy-power` |
| 3.6 | 5.6 Energy and Power Density Spectra | `ctft-properties-energy-power` |
| 4.1 | 6.1 Ideal Filters | `ideal-real-filters-bandwidth` |
| 4.2 | 6.2 Real Filters | `ideal-real-filters-bandwidth` |
| 4.3 | 6.3 Bandwidth Relationships | `ideal-real-filters-bandwidth` |
| 4.4 | 6.4 Reconstruction of Signals from Sample Data | `signal-reconstruction-ideal-zoh` |
| 5.1 | 9.1 Discrete-Time Signals and Systems | `dt-signals-sequences` |
| 5.2 | 9.2 Transformations of Discrete-Time Signals | `dt-signals-sequences` |
| 5.3 | 9.3 Characteristics of Discrete-Time Signals | `dt-signals-sequences` |
| 5.4 | 9.4 Common Discrete-Time Signals | `dt-signals-sequences` |
| 5.5 | 9.5 Discrete-Time Systems | `systems-and-interconnections` |
| 5.6 | 9.6 Properties of Discrete-Time Systems | `system-properties-lti` |
| 6.1 | 10.1 Impulse Representation of Discrete-Time Signals | `impulse-response-and-dt-conv` |
| 6.2 | 10.2 Convolution for Discrete-Time Systems | `impulse-response-and-dt-conv` |
| 6.3 | 10.3 Properties of Discrete-Time LTI Systems | `convolution-properties-and-lti` |
| 6.4 | 10.4 Difference-Equation Models | `differential-and-difference-eqs` |
| 6.5 | 10.6 Block Diagrams | `differential-and-difference-eqs` |
| 6.6 | 10.7 System Response for Complex-Exponential Inputs | `eigenfunctions-complex-exp` |
| 7.1 | 11.1 Definitions of z-Transforms | `z-transform-and-roc` |
| 7.2 | 11.3 z-Transforms of Functions | `z-transform-and-roc` |
| 7.3 | 11.4 z-Transform Properties | `z-transform-and-roc` |
| 7.4 | 11.5 Additional Properties | `z-transform-and-roc` |
| 7.5 | 11.6 LTI System Applications | `poles-zeros-and-fir-iir` |
| 8.1 | 12.1 Discrete-Time Fourier Transform | `dtft-and-periodic-sequences` |
| 8.2 | 12.2 Properties of the Discrete-Time Fourier Transform | `dtft-and-periodic-sequences` |
| 8.3 | 12.3 Discrete-Time Fourier Transform of Periodic Sequences | `dtft-and-periodic-sequences` |
| 8.4 | 12.4 Discrete Fourier Transform | `dft-and-fft` |
| 8.5 | 12.5 Fast Fourier Transform | `dft-and-fft` |
| 9.1 | 5.2 Sampling of Continuous-Time Signals | `sampling-and-aliasing` |
| 9.2 | 5.6 Anti-Aliasing Filter Design | `adc-dac-anti-aliasing-chain` |
| 9.3 | 5.7 Sample-and-Hold Circuit | `signal-reconstruction-ideal-zoh` |
| 9.4 | 5.8 Analog-to-Digital Converter | `adc-dac-anti-aliasing-chain` |
| 9.5 | 5.9 Digital-to-Analog Converter | `adc-dac-anti-aliasing-chain` |
| 9.6 | 5.10 Reconstruction Filter Design | `signal-reconstruction-ideal-zoh` |
| 10.1 | 6.3 Basic FIR Digital Filter Structures | `filter-structures-and-design-basics` |
| 10.2 | 6.4 Basic IIR Digital Filter Structures | `filter-structures-and-design-basics` |
| 10.3 | 6.6 Allpass Filters | 不教：属 E.2.1 数字信号处理中的进阶全通滤波器结构，超出信号与系统入门层 |
| 10.4 | 6.10 Parallel Allpass Realization of IIR Transfer Functions | 不教：属 E.2.1 数字信号处理中的进阶 IIR 并联全通实现，超出信号与系统入门层 |
| 10.5 | 6.12 Computational Complexity of Digital Filter Structures | `filter-structures-and-design-basics` |
| 11.1 | 7.2 Bilinear Transformation Method of IIR Filter Design | `filter-structures-and-design-basics` |
| 11.2 | 7.3 Design of Lowpass IIR Digital Filters | 不教：属 E.2.1 数字信号处理中的完整模拟原型查表设计流程，超出信号与系统入门层 |
| 11.3 | 7.6 FIR Filter Design Based on Windowed Fourier Series | `filter-structures-and-design-basics` |
| 11.4 | 7.8 Design of FIR Digital Filters with Least-Mean-Square Error | 不教：属 E.2.1 数字信号处理中的优化型 FIR 滤波器设计，超出信号与系统入门层 |
| 12.1 | 8.1 Basic Issues | `fixed-point-quantization-and-effects` |
| 12.2 | 8.4 Number Representation | `fixed-point-quantization-and-effects` |
| 12.3 | 8.5 Arithmetic Operations | 不教：属 E.2.1 与硬件电路中的定点乘加器实现细节，超出信号与系统入门层 |
| 12.4 | 8.6 Handling of Overflow | `fixed-point-quantization-and-effects` |
| 13.1 | 9.1 The Quantization Process and Errors | `fixed-point-quantization-and-effects` |
| 13.2 | 9.5 A/D Conversion Noise Analysis | 不教：依赖随机过程与功率谱统计推导，属 E.2.1 与 E.2.2 进阶内容 |
| 13.3 | 9.11 Limit Cycles in IIR Digital Filters | `fixed-point-quantization-and-effects` |

## 核心主题（C2）

对照 ACM/IEEE CE2016 信号处理（SGP）及原技能树 6 个必学知识点：

| 知识点 | 对应主题 | 课 |
|---|---|---|
| 连续与离散信号 | 时移/反转/尺度变换、周期/能量/功率信号、奇偶分解、欧拉公式与复指数、奇异函数（阶跃/冲激/斜坡）、离散基本序列与数字角频率、系统级联/并联/反馈 | `ct-signals-transforms`、`ct-signal-types-singularity`、`dt-signals-sequences`、`systems-and-interconnections` |
| LTI | 线性、时不变、因果、BIBO 稳定、无记忆、常系数微分与差分方程、方框图、复指数特征函数与频率响应 | `system-properties-lti`、`differential-and-difference-eqs`、`eigenfunctions-complex-exp` |
| 采样 | 采样率、奈奎斯特采样定理与混叠折返、理想 sinc 插值与零阶保持、抗混叠滤波、采样保持、ADC 量化编码与 DAC 重建链路 | `sampling-and-aliasing`、`signal-reconstruction-ideal-zoh`、`adc-dac-anti-aliasing-chain` |
| 卷积 | 离散/连续信号冲激分解、离散卷积和与连续卷积积分、卷积交换/结合/分配律、由冲激响应判定因果性与 BIBO 稳定性 | `impulse-response-and-dt-conv`、`ct-convolution`、`convolution-properties-and-lti` |
| 频域 | CTFT 定义与常见变换对、频移/微分/卷积定理、能量谱与功率谱、理想与实际滤波器及带宽关系、DTFT 周期性与周期序列频谱、DFT 频率分辨率与基 2 FFT | `ctft-definition-and-pairs`、`ctft-properties-energy-power`、`ideal-real-filters-bandwidth`、`dtft-and-periodic-sequences`、`dft-and-fft` |
| 数字滤波基本模型 | z 变换与收敛域、单位圆联系、零极点图与稳定性/频率响应估计、FIR 与 IIR 对比、直接 I/II 型与级联结构及计算量、窗函数法与双线性变换入门、定点表示、饱和溢出、量化误差与 IIR 极限环 | `z-transform-and-roc`、`poles-zeros-and-fir-iir`、`filter-structures-and-design-basics`、`fixed-point-quantization-and-effects` |

## 学习资源的章节（C3）

| 来源 | 章节与概念 | 课 / 说明 |
|---|---|---|
| `A` Phillips, Parr & Riskin | Ch. 2, 3, 5, 6, 9, 10, 11, 12 连续/离散信号、LTI、卷积、CTFT、滤波器与采样、z 变换、DTFT/DFT/FFT | 全 46 个小节均已由前 20 课覆盖 |
| `B` Mitra *Digital Signal Processing* | Ch. 5–9 采样链路、FIR/IIR 基本结构、窗函数与双线性变换、定点与量化/极限环 | 核心工程衔接概念分布于 `sampling-and-aliasing`、`signal-reconstruction-ideal-zoh`、`adc-dac-anti-aliasing-chain`、`filter-structures-and-design-basics`、`fixed-point-quantization-and-effects`；进阶设计推导划归 `E.2.1` |
| `zh1` 东南大学《信号与系统》 | 连续与离散时域分析、卷积、傅里叶变换、频率响应、z 变换与系统函数 | 对应全部 6 章核心课程 |
| `zh2` 北京交通大学《数字信号处理》 | 时域/频域抽样定理、DFT/FFT、FIR/IIR 差分方程与基本滤波器结构 | 对应第 3、5、6 章课程 |
| `en1` MIT 6.003 | 信号表示、LTI 微分/差分方程与方框图、卷积与冲激/阶跃响应、傅里叶变换与频率响应、采样与重建、零极点与滤波 | 对应全部 6 章核心课程 |

## 综合练习（C4）

| 小题 | 要用到的 | 课 |
|---|---|---|
| (1) 判断 $y[n]=2x[n]+1$、$x[n]+x[n-1]$、$n x[n]$ 的线性与时不变性 | 叠加性、齐次性、零输入必为零输出检验、时移检验 | `system-properties-lti` |
| (2) 计算 $x[n]=[1,2,1]$ 与 $h[n]=[1,-1]$ 的离散卷积并说明作用 | 离散卷积和计算、输出长度、一阶差分突出变化（高通特性） | `impulse-response-and-dt-conv` |
| (3) 判断 $\cos(2\pi\cdot 300t)$ 在 1000 Hz 与 500 Hz 采样下是否混叠及视在频率 | 奈奎斯特频率 $f_s/2$、混叠折返频率 $|f - k f_s|$ | `sampling-and-aliasing` |
| (4) 8 kHz 采样做 8 点 DFT 的频率分辨率；$h=[1/2, 1/2]$ 的频率响应 $\cos(\omega/2)e^{-j\omega/2}$ 类型 | 频率分辨率 $\Delta f = f_s/N$、DTFT 在 $\omega=0$ 与 $\omega=\pi$ 处的幅值判断低通 | `dtft-and-periodic-sequences`、`dft-and-fft` |
| (5) FIR 与 IIR 区别；$y[n]=0.9y[n-1]+0.1x[n]$ 的极点、稳定性与滤波类型 | 差分方程转 $H(z)$、极点在单位圆内判稳、直流与奈奎斯特处增益计算 | `poles-zeros-and-fir-iir` |

## 后继技能（C5）

本技能有 5 个必须后继技能（尚无互动课，对照其章节与大纲核对衔接）：

| 后继技能 | 直接用到的概念与方法 | 本包对应课 |
|---|---|---|
| `E.2.1` 数字信号处理 | 离散信号与 LTI、z 变换与收敛域、DTFT/DFT/FFT、采样与重建、FIR/IIR 模型与结构、窗函数与双线性变换入门、定点与量化误差 | `dt-signals-sequences`、`impulse-response-and-dt-conv`、`dtft-and-periodic-sequences`、`dft-and-fft`、`z-transform-and-roc`、`poles-zeros-and-fir-iir`、`filter-structures-and-design-basics`、`fixed-point-quantization-and-effects` |
| `E.2.3` 通信原理 | 傅里叶变换与频移调制、能量/功率谱密度、滤波与带宽、奈奎斯特采样与 sinc 插值 | `ctft-definition-and-pairs`、`ctft-properties-energy-power`、`ideal-real-filters-bandwidth`、`sampling-and-aliasing`、`signal-reconstruction-ideal-zoh` |
| `E.1.3` 射频与高频电路 | 复指数稳态响应 $H(j\omega)$、$-3\text{ dB}$ 截止频率与带宽、分贝换算、频谱搬移 | `eigenfunctions-complex-exp`、`ctft-properties-energy-power`、`ideal-real-filters-bandwidth` |
| `E.2.2` 统计信号处理 | LTI 卷积与系统响应、能量谱与功率谱密度、帕塞瓦尔定理、频率响应幅值平方 | `ct-convolution`、`ctft-properties-energy-power`、`dtft-and-periodic-sequences` |
| `V.1.2` 多媒体技术 | 采样率与奈奎斯特频率、量化位数与信噪比、DFT/FFT 分帧频谱分析、数字滤波基本模型 | `sampling-and-aliasing`、`adc-dac-anti-aliasing-chain`、`dft-and-fft`、`fixed-point-quantization-and-effects` |
