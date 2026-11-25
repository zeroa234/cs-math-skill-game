# E.2.1 数字信号处理：覆盖表

**状态（2026-11-22）：已写完。** 依据 `vendor/cs-math-skill-tree/output/outlines.json` 与 `vendor/cs-math-skill-tree/output/skilltree.json`，主来源为 Alan V. Oppenheim & Ronald W. Schafer *Discrete-Time Signal Processing*（3rd Ed.，MIT OCW 开放教材，来源 A，第 2、3、4、5、7、8、9、10 章），并对照北京航空航天大学《数字信号处理》（`zh1`）补齐频率采样法 FIR 设计等中文课堂主线。

游戏内部章序：`1. 离散时间信号与系统`、`2. z变换`、`3. DTFT与DFT`、`4. 采样与重建`、`5. 快速傅里叶变换`、`6. FIR滤波器设计`、`7. IIR滤波器设计`、`8. 多速率信号处理`、`9. 谱分析与窗函数`。本技能的唯一必须前置是 `H.1.3`（信号与系统，前置链 `M.1.1` → `M.1.2` → `M.1.3` → `H.1.3`）；复变函数与科学计算编程仅为推荐前置，因此随机信号的均值/方差/自相关、部分分式展开、多相分解、Parks–McClellan 等波纹思想及功率谱估计均在本包从零讲清并配有分步例题。

`node scripts/check-coverage.mjs E.2.1` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | 2.1 Discrete-Time Signals | `dt-signals-lti-systems` |
| 1.2 | 2.2 Discrete-Time Systems | `dt-signals-lti-systems` |
| 1.3 | 2.3 LTI Systems | `dt-signals-lti-systems` |
| 1.4 | 2.4 Properties of Linear Time-Invariant Systems | `dt-signals-lti-systems` |
| 1.5 | 2.5 Linear Constant-Coefficient Difference Equations | `difference-equations-systems` |
| 1.6 | 2.6 Frequency-Domain Representation of Discrete-Time Signals and Systems | `dtft-properties-symmetry` |
| 1.7 | 2.7 Representation of Sequences by Fourier Transforms | `dtft-properties-symmetry` |
| 1.8 | 2.8 Symmetry Properties of the Fourier Transform | `dtft-properties-symmetry` |
| 1.9 | 2.9 Fourier Transform Theorems | `dtft-properties-symmetry` |
| 1.10 | 2.10 Discrete-Time Random Signals | `dt-random-signals-corr` |
| 2.1 | 3.1 z-Transform | `z-transform-roc` |
| 2.2 | 3.2 Properties of the ROC for the z-Transform | `z-transform-roc` |
| 2.3 | 3.3 The Inverse z-Transform | `inverse-z-and-properties` |
| 2.4 | 3.4 z-Transform Properties | `inverse-z-and-properties` |
| 2.5 | 3.5 z-Transforms and LTI Systems | `system-function-freq-response` |
| 2.6 | 3.6 The Unilateral z-Transform | `inverse-z-and-properties` |
| 3.1 | 4.1 Periodic Sampling | `sampling-aliasing-reconstruction` |
| 3.2 | 4.2 Frequency-Domain Representation of Sampling | `sampling-aliasing-reconstruction` |
| 3.3 | 4.3 Reconstruction of a Bandlimited Signal from Its Samples | `sampling-aliasing-reconstruction` |
| 3.4 | 4.4 Discrete-Time Processing of Continuous-Time Signals | `discrete-processing-analog-oversampling` |
| 3.5 | 4.5 Continuous-Time Processing of Discrete-Time Signals | `discrete-processing-analog-oversampling` |
| 3.6 | 4.6 Changing the Sampling Rate Using Discrete-Time Processing | `decimation-interpolation-rational` |
| 3.7 | 4.7 Multirate Signal Processing | `multirate-noble-polyphase` |
| 3.8 | 4.8 Digital Processing of Analog Signals | `discrete-processing-analog-oversampling` |
| 3.9 | 4.9 Oversampling and Noise Shaping in A/D and D/A Conversion | `discrete-processing-analog-oversampling` |
| 4.1 | 5.1 The Frequency Response of LTI Systems | `system-function-freq-response` |
| 4.2 | 5.2 System Functions—Linear Constant-Coefficient Difference Equations | `system-function-freq-response` |
| 4.3 | 5.3 Frequency Response for Rational System Functions | `system-function-freq-response` |
| 4.4 | 5.4 Relationship between Magnitude and Phase | `allpass-minimum-phase` |
| 4.5 | 5.5 All-Pass Systems | `allpass-minimum-phase` |
| 4.6 | 5.6 Minimum-Phase Systems | `allpass-minimum-phase` |
| 4.7 | 5.7 Linear Systems with Generalized Linear Phase | `generalized-linear-phase-fir` |
| 5.1 | 7.1 Filter Specifications | `generalized-linear-phase-fir` |
| 5.2 | 7.2 Design of Discrete-Time IIR Filters from Continuous-Time Filters | `iir-impulse-invariance-bilinear` |
| 5.3 | 7.3 Discrete-Time Butterworth, Chebyshev and Elliptic Filters | `iir-prototypes-and-freq-transforms` |
| 5.4 | 7.4 Frequency Transformations of Lowpass IIR Filters | `iir-prototypes-and-freq-transforms` |
| 5.5 | 7.5 Design of FIR Filters by Windowing | `fir-window-and-kaiser` |
| 5.6 | 7.6 Examples of FIR Filter Design by the Kaiser Window Method | `fir-window-and-kaiser` |
| 5.7 | 7.7 Optimum Approximations of FIR Filters | `fir-equiripple-and-comparison` |
| 5.8 | 7.8 Examples of FIR Equiripple Approximation | `fir-equiripple-and-comparison` |
| 5.9 | 7.9 Comments on IIR and FIR Discrete-Time Filters | `fir-equiripple-and-comparison` |
| 5.10 | 7.10 Design of an Upsampling Filter | `decimation-interpolation-rational` |
| 6.1 | 8.1 Representation of Periodic Sequences: The Discrete Fourier Series | `dfs-and-freq-sampling` |
| 6.2 | 8.2 Properties of the DFS | `dfs-and-freq-sampling` |
| 6.3 | 8.3 The Fourier Transform of Periodic Signals | `dfs-and-freq-sampling` |
| 6.4 | 8.4 Sampling the Fourier Transform | `dfs-and-freq-sampling` |
| 6.5 | 8.5 Fourier Representation of Finite-Duration Sequences | `dft-definition-properties` |
| 6.6 | 8.6 Properties of the DFT | `dft-definition-properties` |
| 6.7 | 8.7 Linear Convolution Using the DFT | `dft-linear-conv-and-dct` |
| 6.8 | 8.8 The Discrete Cosine Transform (DCT) | `dft-linear-conv-and-dct` |
| 7.1 | 9.1 Direct Computation of the Discrete Fourier Transform | `fft-dit-dif` |
| 7.2 | 9.2 Decimation-in-Time FFT Algorithms | `fft-dit-dif` |
| 7.3 | 9.3 Decimation-in-Frequency FFT Algorithms | `fft-dit-dif` |
| 7.4 | 9.4 Practical Considerations | `fft-implementation-and-general` |
| 7.5 | 9.5 More General FFT Algorithms | `fft-implementation-and-general` |
| 7.6 | 9.6 Implementation of the DFT Using Convolution | `fft-implementation-and-general` |
| 7.7 | 9.7 Effects of Finite Register Length | `fft-implementation-and-general` |
| 8.1 | 10.1 Fourier Analysis of Signals Using the DFT | `dft-sinusoidal-and-stft` |
| 8.2 | 10.2 DFT Analysis of Sinusoidal Signals | `dft-sinusoidal-and-stft` |
| 8.3 | 10.3 The Time-Dependent Fourier Transform | `dft-sinusoidal-and-stft` |
| 8.4 | 10.4 Examples of Fourier Analysis of Nonstationary Signals | `dft-sinusoidal-and-stft` |
| 8.5 | 10.5 Fourier Analysis of Stationary Random Signals: the Periodogram | `periodogram-welch-random-psd` |
| 8.6 | 10.6 Spectrum Analysis of Random Signals | `periodogram-welch-random-psd` |

## 核心主题（C2）

对照 ACM/IEEE CE2016 信号处理（SGP）核心知识领域及原技能树 9 个必学知识点：

| 知识点 | 对应主题 | 课 |
|---|---|---|
| 离散时间信号与系统 | 基本序列与周期条件、系统性质判定、卷积和与 LTI 性质、常系数差分方程与初始静止递推、离散宽平稳随机信号与自相关/互相关及 LTI 功率谱变换 | `dt-signals-lti-systems`、`difference-equations-systems`、`dt-random-signals-corr` |
| z变换 | 双边 z 变换与收敛域八大性质、逆 z 变换（观察法/幂级数/部分分式展开）、z 变换性质、单边 z 变换求解非零初始状态、有理系统函数与零极点频率响应、群延迟、全通与最小相位分解 | `z-transform-roc`、`inverse-z-and-properties`、`system-function-freq-response`、`allpass-minimum-phase` |
| DTFT与DFT | DTFT 定义/收敛/对称性与定理、DFS 及其性质、周期序列频谱与频域采样导致的时域周期延拓、有限长序列 DFT/补零插值/圆周移位与圆周卷积、重叠相加/重叠保留法计算线性卷积、离散余弦变换 DCT | `dtft-properties-symmetry`、`dfs-and-freq-sampling`、`dft-definition-properties`、`dft-linear-conv-and-dct` |
| 采样与重建 | 周期采样与频谱搬移、奈奎斯特采样定理与混叠折返、理想 sinc 重建、模拟信号的离散处理与分数延迟、实用 ADC/DAC 量化信噪比与过采样噪声整形 | `sampling-aliasing-reconstruction`、`discrete-processing-analog-oversampling` |
| 快速傅里叶变换 | 直接 DFT 复杂度、旋转因子对称性与周期性、基 2 DIT-FFT 与 DIF-FFT 蝶形、利用 FFT 算 IFFT、原位运算与位倒序、混合基/Goertzel/Chirp-z、定点 FFT 缩放与舍入噪声 | `fft-dit-dif`、`fft-implementation-and-general` |
| FIR滤波器设计 | 滤波器通阻带与波纹指标、广义线性相位与四类对称 FIR、窗函数法与吉布斯现象、经典窗权衡与 Kaiser 窗参数公式、等波纹最优逼近（交错定理与 Parks–McClellan）、频率采样法、FIR 与 IIR 综合比较 | `generalized-linear-phase-fir`、`fir-window-and-kaiser`、`fir-equiripple-and-comparison` |
| IIR滤波器设计 | 模拟低通原型到数字 IIR、冲激响应不变法与混叠限制、双线性变换与频率预畸变、巴特沃斯/切比雪夫 I 型与 II 型/椭圆原型比较与阶数估算、数字低通到高通/带通/带阻的频率变换 | `iir-impulse-invariance-bilinear`、`iir-prototypes-and-freq-transforms` |
| 多速率信号处理 | 降采样与抽取抗混叠、升采样镜像与内插抗镜像、上采样滤波器指标、有理数倍 $L/M$ 速率转换与合并低通、贵族恒等式、多相分解节省计算量与多级抽取 | `decimation-interpolation-rational`、`multirate-noble-polyphase` |
| 谱分析与窗函数 | DFT 频点间隔与真实双音分辨率、频谱泄漏与栅栏效应、强弱双正弦分析的窗选择、短时傅里叶变换 STFT 与语谱图及时间–频率分辨率权衡、周期图偏差与非一致方差、Bartlett 与 Welch 分段平均谱估计 | `dft-sinusoidal-and-stft`、`periodogram-welch-random-psd` |

## 学习资源的章节（C3）

| 来源 | 章节与概念 | 课 / 说明 |
|---|---|---|
| `A` Oppenheim & Schafer *DTSP* 3e | Ch. 2, 3, 4, 5, 7, 8, 9, 10 全部 63 个小节 | 全 63 个小节均由本包 24 课逐一覆盖，无遗漏 |
| `zh1` 北航《数字信号处理》 | CH3（DTFT/DFS/z 变换）、CH5（采样重建）、CH6（DFT 与线性卷积）、CH7（DIT/DIF FFT 与 IFFT）、CH8（IIR 模拟原型/冲激不变/双线性；FIR 窗函数法与频率采样法）、CH10（加窗截短、DFT 谱分析、采样率转换） | 全部主线已融入 9 章 24 课，其中 CH8-6 频率采样法在 `fir-equiripple-and-comparison` 中专门讲授 |

## 综合练习（C4）

| 小题 | 要用到的 | 课 |
|---|---|---|
| (1) $y[n]=x[n]+0.5y[n-1]$（初始静止）线性/时不变/因果/稳定判定与 $h[n]$ | 常系数差分方程性质检验、递推求 $h[n]=0.5^n u[n]$、绝对可和 $\sum|h[n]|=2$ | `dt-signals-lti-systems`、`difference-equations-systems` |
| (2) 求 $H(z)$ 与收敛域；部分分式求 $X(z)=\frac{1}{(1-0.5z^{-1})(1-0.25z^{-1})}$（$|z|>0.5$）反变换并验证前两项 | 差分方程转 $H(z)$、右侧收敛域、部分分式展开与序列卷积前两项验证 | `z-transform-roc`、`inverse-z-and-properties` |
| (3) $x[n]=[1,1,1,1]$ 的 4 点 DFT、补零到 8 点的含义、DTFT 与 DFT 关系 | $N$ 点 DFT 计算、补零对 DTFT 插值不提高真实分辨率、DFT 是 DTFT 的等间隔频域采样 | `dfs-and-freq-sampling`、`dft-definition-properties` |
| (4) 1024 点 DFT 直接计算与基 2 FFT 的复数乘法量对比 | 直接 DFT $N^2=1{,}048{,}576$ 与基 2 FFT $\frac{N}{2}\log_2 N=5120$ | `fft-dit-dif` |
| (5) 1 kHz 与 3 kHz 正弦以 4 kHz 采样后的视在频率与理想重建滤波器 | 奈奎斯特频率 $f_s/2=2\text{ kHz}$、混叠折返 $4-3=1\text{ kHz}$、截止在 $f_s/2$ 的理想低通（sinc 插值） | `sampling-aliasing-reconstruction` |
| (6) 汉明窗设计 $\Delta f=0.05$ 线性相位 FIR 的阶数与线性相位冲激响应条件 | 汉明窗近似 $M\approx 3.3/\Delta f=66$、对称/反对称条件 $h[n]=\pm h[M-n]$ | `generalized-linear-phase-fir`、`fir-window-and-kaiser` |
| (7) 双线性变换（$f_s=8\text{ kHz}, f_c=1\text{ kHz}$）预畸变模拟截止频率及 FIR/IIR 优缺点 | 预畸变 $\Omega_c=(2/T)\tan(\omega_c/2)\approx 6627\text{ rad/s}$ 与未预畸变 $6283\text{ rad/s}$ 对比、FIR 与 IIR 权衡 | `iir-impulse-invariance-bilinear`、`fir-equiripple-and-comparison` |
| (8) 48 kHz 降到 12 kHz 的抽取前处理与多相结构省计算原理 | 截止 $\pi/4$（6 kHz）抗混叠低通、多相拆成 4 路子滤波器仅算保留输出使计算量降为 $1/4$ | `decimation-interpolation-rational`、`multirate-noble-polyphase` |
| (9) 8 kHz 采样 1024 点 FFT 频点间隔、加窗减泄漏的原理与代价 | 频点间隔 $8000/1024=7.8125\text{ Hz}$、矩形截断 sinc 卷积旁瓣高、平滑窗降旁瓣但展宽主瓣 | `dft-sinusoidal-and-stft` |

## 后继技能（C5）

本技能有 2 个必须后继技能（尚无互动课，对照其章节核对衔接）：

| 后继技能 | 直接用到的概念与方法 | 本包对应课 |
|---|---|---|
| `E.1.7` 雷达原理 | 离散互相关与匹配滤波思想、脉冲压缩中的快速卷积（重叠相加/保留）、多普勒频移的 DFT/FFT 与 STFT 谱分析、加窗抑制强杂波旁瓣、采样与欠采样混叠 | `dt-random-signals-corr`、`dft-linear-conv-and-dct`、`fft-dit-dif`、`dft-sinusoidal-and-stft`、`sampling-aliasing-reconstruction` |
| `E.2.5` 自适应信号处理 | 宽平稳随机信号均值/方差与自相关/互相关序列、有限长 FIR 滤波器与频率响应、多速率与子带滤波基础、随机信号功率谱与周期图/Welch 评估收敛后的残差谱 | `dt-random-signals-corr`、`generalized-linear-phase-fir`、`multirate-noble-polyphase`、`periodogram-welch-random-psd` |
