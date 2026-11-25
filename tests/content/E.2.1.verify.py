"""
Verification script for E.2.1 数字信号处理 (Digital Signal Processing).
Independently checks every numerical example, transform, filter design calculation,
multirate speedup, spectral analysis value, and boss challenge answer in data/content/E.2.1.yaml.
Run with: python3 -I tests/content/E.2.1.verify.py
"""
import cmath
import math
import random


def close(a, b, tol=1e-6):
    assert abs(a - b) <= tol, f"Expected {b}, got {a} (diff={abs(a - b)})"


def convolve(x, h):
    out = [0.0] * (len(x) + len(h) - 1)
    for i, xv in enumerate(x):
        for j, hv in enumerate(h):
            out[i + j] += xv * hv
    return out


def dft(x):
    N = len(x)
    return [
        sum(x[n] * cmath.exp(-2j * math.pi * k * n / N) for n in range(N))
        for k in range(N)
    ]


def idft(X):
    N = len(X)
    return [
        sum(X[k] * cmath.exp(2j * math.pi * k * n / N) for k in range(N)) / N
        for n in range(N)
    ]


def circ_conv(x1, x2):
    N = len(x1)
    assert len(x2) == N
    return [sum(x1[m] * x2[(n - m) % N] for m in range(N)) for n in range(N)]


def dct2(x):
    N = len(x)
    return [
        2.0 * sum(x[n] * math.cos(math.pi * k * (2 * n + 1) / (2 * N)) for n in range(N))
        for k in range(N)
    ]


# 1. Lesson 1: dt-signals-lti-systems
# Periodicity of cos(3*pi*n/8): 3/16 -> N=16
N_per = 16
for n in range(20):
    close(math.cos(3 * math.pi * (n + N_per) / 8), math.cos(3 * math.pi * n / 8))
# Convolution of [1, 2, 1] and [1, -1, 2]
y_conv = convolve([1, 2, 1], [1, -1, 2])
assert [round(v) for v in y_conv] == [1, 1, 1, 3, 2], y_conv
# Geometric sum of |h[n]| for h[n] = 0.6^n u[n]
s_bibo = sum(0.6 ** n for n in range(200))
close(s_bibo, 2.5, 1e-9)
# Accumulator * first difference = delta[n]
u_trunc = [1] * 10
d_diff = [1, -1]
inv_check = convolve(u_trunc, d_diff)[:9]
assert inv_check == [1, 0, 0, 0, 0, 0, 0, 0, 0], inv_check

# 2. Lesson 2: difference-equations-systems
# y[n] = x[n] + 0.5*y[n-1], initial rest -> h[n] = 0.5^n u[n]
h_rec = []
prev = 0.0
for n in range(10):
    xn = 1.0 if n == 0 else 0.0
    yn = xn + 0.5 * prev
    h_rec.append(yn)
    prev = yn
for n, v in enumerate(h_rec):
    close(v, 0.5 ** n)
close(sum(0.5 ** n for n in range(200)), 2.0, 1e-9)
# Step response of y[n] = x[n] + 0.5*y[n-1]
s_rec = []
prev = 0.0
for n in range(4):
    yn = 1.0 + 0.5 * prev
    s_rec.append(yn)
    prev = yn
assert s_rec == [1.0, 1.5, 1.75, 1.875], s_rec

# 3. Lesson 3: dt-random-signals-corr
# White noise var=4 through h = [0.5, 0.5]
sigma2 = 4.0
h_ma = [0.5, 0.5]
phi_yy_0 = sigma2 * sum(v * v for v in h_ma)
phi_yy_1 = sigma2 * (h_ma[0] * h_ma[1])
close(phi_yy_0, 2.0)
close(phi_yy_1, 1.0)
# Mean output for m_x = 6
m_y = 6.0 * sum(h_ma)
close(m_y, 6.0)
# PSD at w=0 and w=pi
H0 = sum(h_ma)
Hpi = h_ma[0] - h_ma[1]
close(abs(H0) ** 2 * sigma2, 4.0)
close(abs(Hpi) ** 2 * sigma2, 0.0)

# 4. Lesson 4: z-transform-roc
# Finite sequence [2, -1, 3] evaluated at z=2 -> 2 - 0.5 + 0.75 = 2.25
close(2 - 2 ** -1 + 3 * 2 ** -2, 2.25)
# Annulus ROC: 0.5^n u[n] - 2^n u[-n-1] converges at z=1 (unit circle)
# Sum_{n>=0} 0.5^n + Sum_{n<=-1} (-2^n) = 2 - (1/2 + 1/4 + ...) = 2 - 1 = 1
X_at_1 = 1 / (1 - 0.5) + 1 / (1 - 2.0)
close(X_at_1, 1.0)

# 5. Lesson 5: inverse-z-and-properties (includes Exercise 2)
# X(z) = 1 / ((1 - 0.5 z^-1)(1 - 0.25 z^-1)), |z| > 0.5
# Partial fractions: A / (1 - 0.5 z^-1) + B / (1 - 0.25 z^-1)
A_pf = 1.0 / (1.0 - 0.25 / 0.5)
B_pf = 1.0 / (1.0 - 0.5 / 0.25)
close(A_pf, 2.0)
close(B_pf, -1.0)
x_inv = [A_pf * (0.5 ** n) + B_pf * (0.25 ** n) for n in range(6)]
# Independently verify by convolving 0.5^n u[n] and 0.25^n u[n]
h1 = [0.5 ** n for n in range(6)]
h2 = [0.25 ** n for n in range(6)]
x_conv = convolve(h1, h2)[:6]
for a, b in zip(x_inv, x_conv):
    close(a, b)
close(x_inv[0], 1.0)
close(x_inv[1], 0.75)
close(x_inv[2], 0.4375)
close(x_inv[3], 0.234375)
# ROC 0.25 < |z| < 0.5: x[n] = -2*0.5^n u[-n-1] - 0.25^n u[n]
close(-0.25 ** 0, -1.0)
close(-2.0 * (0.5 ** -1), -4.0)
# Unilateral z-transform: y[n] - 0.5 y[n-1] = delta[n], y[-1] = 4 -> y[n] = 3 * 0.5^n u[n]
y_uni = []
prev = 4.0
for n in range(5):
    xn = 1.0 if n == 0 else 0.0
    yn = xn + 0.5 * prev
    y_uni.append(yn)
    prev = yn
for n, v in enumerate(y_uni):
    close(v, 3.0 * (0.5 ** n))
close(y_uni[0], 3.0)
close(y_uni[1], 1.5)

# 6. Lesson 6: system-function-freq-response
# H(z) = (1 - z^-1) / (1 - 0.8 z^-1)
def H_hp(w):
    ejw = cmath.exp(1j * w)
    return (1 - ejw ** -1) / (1 - 0.8 * ejw ** -1)


close(abs(H_hp(0)), 0.0)
close(abs(H_hp(math.pi)), 10.0 / 9.0)
# Poles of 1 - 1.3 z^-1 + 0.4 z^-2 = (1 - 0.8 z^-1)(1 - 0.5 z^-1)
close(0.8 + 0.5, 1.3)
close(0.8 * 0.5, 0.4)

# 7. Lesson 7: allpass-minimum-phase
# H_ap(z) = (z^-1 - 0.5) / (1 - 0.5 z^-1)
def H_ap(z):
    return (z ** -1 - 0.5) / (1 - 0.5 * z ** -1)


for k in range(36):
    w = 2 * math.pi * k / 36
    close(abs(H_ap(cmath.exp(1j * w))), 1.0)
# Group delay of H_ap(z) with a=0.5: (1 - a^2) / (1 + a^2 - 2 a cos w)
a = 0.5
tau_0 = (1 - a ** 2) / (1 + a ** 2 - 2 * a * 1)
tau_pi = (1 - a ** 2) / (1 + a ** 2 - 2 * a * (-1))
close(tau_0, 3.0)
close(tau_pi, 1.0 / 3.0)
# Minimum-phase factorization: H(z) = (1 - 2 z^-1) / (1 - 0.4 z^-1)
# = [-2 (1 - 0.5 z^-1) / (1 - 0.4 z^-1)] * [(z^-1 - 0.5) / (1 - 0.5 z^-1)]
for k in range(16):
    z = cmath.exp(1j * 2 * math.pi * k / 16)
    H_orig = (1 - 2 / z) / (1 - 0.4 / z)
    H_min = (-2 * (1 - 0.5 / z)) / (1 - 0.4 / z)
    close(H_orig, H_min * H_ap(z))
    close(abs(H_orig), abs(H_min))
# Energy concentration: [1, -0.5] vs [-0.5, 1]
close(1.0 / (1.0 + 0.25), 0.8)
close(0.25 / (1.0 + 0.25), 0.2)

# 8. Lesson 8: dtft-properties-symmetry
# 4-point pulse [1, 1, 1, 1] DTFT
def X_rect4(w):
    return sum(cmath.exp(-1j * w * n) for n in range(4))


close(abs(X_rect4(0)), 4.0)
close(abs(X_rect4(math.pi / 2)), 0.0)
# Parseval for x[n] = 0.5^n u[n]
energy_time = sum((0.5 ** n) ** 2 for n in range(200))
close(energy_time, 4.0 / 3.0, 1e-9)
M_int = 2000
energy_freq = sum(
    abs(1.0 / (1.0 - 0.5 * cmath.exp(-1j * (-math.pi + 2 * math.pi * k / M_int)))) ** 2
    for k in range(M_int)
) / M_int
close(energy_freq, 4.0 / 3.0, 1e-6)
# Conjugate symmetry: |3 - 4j| = 5
close(abs(3 - 4j), 5.0)

# 9. Lesson 9: dfs-and-freq-sampling
# Periodic [1, 0, -1, 0] -> DFS [0, 2, 0, 2]
X_dfs = dft([1, 0, -1, 0])
for got, exp in zip(X_dfs, [0, 2, 0, 2]):
    close(got, exp)
# Sampling 6-point sequence [1, 2, 3, 4, 5, 6] DTFT at N=4 gives time-aliased [6, 8, 3, 4]
x6 = [1, 2, 3, 4, 5, 6]
X4_samples = [
    sum(x6[n] * cmath.exp(-1j * (2 * math.pi * k / 4) * n) for n in range(6))
    for k in range(4)
]
x_alias = [v.real for v in idft(X4_samples)]
for got, exp in zip(x_alias, [6, 8, 3, 4]):
    close(got, exp)

# 10. Lesson 10: dft-definition-properties (includes Exercise 3)
# 4-point DFT of [1, 1, 1, 1] -> [4, 0, 0, 0]
X_ones4 = dft([1, 1, 1, 1])
for got, exp in zip(X_ones4, [4, 0, 0, 0]):
    close(got, exp)
# Zero-padded to 8 points
X_ones8 = dft([1, 1, 1, 1, 0, 0, 0, 0])
for k in range(4):
    close(X_ones8[2 * k], X_ones4[k])
close(abs(X_ones8[1]), math.sqrt(4 + 2 * math.sqrt(2)))
close(abs(X_ones8[1]), 2.613125929752753, 1e-6)
close(abs(X_ones8[3]), math.sqrt(4 - 2 * math.sqrt(2)))
close(abs(X_ones8[3]), 1.082392200292394, 1e-6)
# 4-point circular convolution of [1, 2, 0, 1] and [2, 1, 1, 0]
c4 = circ_conv([1, 2, 0, 1], [2, 1, 1, 0])
assert c4 == [3, 6, 3, 4], c4
lin7 = convolve([1, 2, 0, 1], [2, 1, 1, 0])
assert [round(v) for v in lin7] == [2, 5, 3, 4, 1, 1, 0], lin7
# Verify wrap-around: [2+1, 5+1, 3+0, 4] = [3, 6, 3, 4]
assert [round(lin7[0] + lin7[4]), round(lin7[1] + lin7[5]), round(lin7[2] + lin7[6]), round(lin7[3])] == c4
# Verify DFT product equals IDFT of circular convolution
X1 = dft([1, 2, 0, 1])
X2 = dft([2, 1, 1, 0])
c4_via_dft = [v.real for v in idft([a * b for a, b in zip(X1, X2)])]
for a, b in zip(c4_via_dft, c4):
    close(a, b)

# 11. Lesson 11: dft-linear-conv-and-dct
# Linear conv lengths L=5, P=4 -> N >= 8
assert 5 + 4 - 1 == 8
# Overlap-add: L=6, M=3 -> block conv len 8, overlap M-1=2
assert 6 + 3 - 1 == 8 and 3 - 1 == 2
# Overlap-save: N=8, M=3 -> valid outputs N-M+1 = 6, discard 2
assert 8 - 3 + 1 == 6
# 4-point DCT-II of [2, 2, 2, 2]: all energy in k=0 (value 16)
C_const = dct2([2, 2, 2, 2])
close(C_const[0], 16.0)
for k in range(1, 4):
    close(C_const[k], 0.0)
# 4-point DCT-II of ramp [1, 2, 3, 4]: energy compaction in first 2 coeffs
C_ramp = dct2([1, 2, 3, 4])
# Orthogonal normalized weights: k=0 has factor 1/(2N), k>0 has 1/N in unscaled DCT-II (with 2x sum)
# Specifically Parseval for C[k] = 2 sum x[n] cos(...): sum x[n]^2 = (C[0]^2 / (4N)) + sum_{k>=1} (C[k]^2 / (2N))
E_ramp = sum(v * v for v in [1, 2, 3, 4])
E_dct_total = C_ramp[0] ** 2 / 16.0 + sum(C_ramp[k] ** 2 / 8.0 for k in range(1, 4))
close(E_ramp, E_dct_total)
E_first2 = C_ramp[0] ** 2 / 16.0 + C_ramp[1] ** 2 / 8.0
assert E_first2 / E_ramp > 0.99  # 99.6%+ energy in first two DCT coefficients!

# 12. Lesson 12: sampling-aliasing-reconstruction (includes Exercise 5)
# 1 kHz & 3 kHz sampled at 4 kHz
fs = 4000.0
fN = fs / 2
close(fN, 2000.0)
f_alias_3k = abs(3000.0 - fs)
close(f_alias_3k, 1000.0)
# Verify discrete samples cos(2*pi*3000*n/4000) == cos(2*pi*1000*n/4000)
for n in range(12):
    close(math.cos(2 * math.pi * 3000 * n / 4000), math.cos(2 * math.pi * 1000 * n / 4000))
# 700 Hz and 2300 Hz sampled at 1000 Hz both alias to 300 Hz
for n in range(10):
    close(math.cos(2 * math.pi * 700 * n / 1000), math.cos(2 * math.pi * 300 * n / 1000))
    close(math.cos(2 * math.pi * 2300 * n / 1000), math.cos(2 * math.pi * 300 * n / 1000))

# 13. Lesson 13: discrete-processing-analog-oversampling
# Digital cutoff pi/4 at fs=16 kHz -> analog cutoff 2 kHz
close((math.pi / 4) / (2 * math.pi) * 16000, 2000.0)
# SQNR = 6.02 B + 1.76 dB
close(6.02 * 16 + 1.76, 98.08)
close(6.02 * 12 + 1.76, 74.00)
# Oversampling by M=4 -> +6.02 dB (+1 bit)
close(10 * math.log10(4), 6.020599913279624, 1e-6)
close(10 * math.log10(16), 12.041199826559248, 1e-6)

# 14. Lesson 14: fft-dit-dif (includes Exercise 4)
N_fft = 1024
direct_muls = N_fft ** 2
fft_muls = (N_fft // 2) * int(math.log2(N_fft))
assert direct_muls == 1048576
assert fft_muls == 5120
close(direct_muls / fft_muls, 204.8)
# 4-point DIT-FFT on [1, 2, 3, 4]
x4 = [1, 2, 3, 4]
G = dft([1, 3])
H = dft([2, 4])
W4 = [1, -1j]
X4_dit = [G[0] + W4[0] * H[0], G[1] + W4[1] * H[1], G[0] - W4[0] * H[0], G[1] - W4[1] * H[1]]
X4_ref = dft(x4)
for a, b in zip(X4_dit, X4_ref):
    close(a, b)
for a, b in zip(X4_dit, [10, -2 + 2j, -2, -2 - 2j]):
    close(a, b)
# IFFT via FFT: (1/N) * conj(FFT(conj(X)))
x4_via_fft = [v.conjugate() / 4 for v in dft([v.conjugate() for v in X4_ref])]
for a, b in zip(x4_via_fft, x4):
    close(a, b)

# 15. Lesson 15: fft-implementation-and-general
# 8-point bit-reversal
bitrev8 = [int(f"{i:03b}"[::-1], 2) for i in range(8)]
assert bitrev8 == [0, 4, 2, 6, 1, 5, 3, 7], bitrev8
# N=64 stages & butterflies/stage
assert int(math.log2(64)) == 6 and 64 // 2 == 32

# 16. Lesson 16: generalized-linear-phase-fir
# Type II symmetric odd M=3: h = [1, 2, 2, 1] -> H(e^{j*pi}) = 0
h_t2 = [1, 2, 2, 1]
close(sum(h_t2[n] * ((-1) ** n) for n in range(4)), 0.0)
# Type III antisymmetric even M=4: h = [1, 2, 0, -2, -1] -> H(e^{j*0})=0 and H(e^{j*pi})=0
h_t3 = [1, 2, 0, -2, -1]
close(sum(h_t3), 0.0)
close(sum(h_t3[n] * ((-1) ** n) for n in range(5)), 0.0)
# Group delay of L=21 (M=20) -> 10 samples; L=20 (M=19) -> 9.5 samples
close((21 - 1) / 2, 10.0)
close((20 - 1) / 2, 9.5)

# 17. Lesson 17: fir-window-and-kaiser (includes Exercise 6)
# Hamming window: M approx 3.3 / Delta_f; for Delta_f = 0.05 -> M = 66, L = 67
close(3.3 / 0.05, 66.0)
# Kaiser window: A = 50 dB, Delta_w = 0.2*pi
A_k = 50.0
dw_k = 0.2 * math.pi
M_k = (A_k - 8.0) / (2.285 * dw_k)
close(M_k, 29.253862625206143, 1e-6)
assert math.ceil(M_k) == 30  # even order M=30 for Type I
beta_50 = 0.5842 * ((A_k - 21.0) ** 0.4) + 0.07886 * (A_k - 21.0)
close(beta_50, 4.53351396, 1e-4)
beta_60 = 0.1102 * (60.0 - 8.7)
close(beta_60, 5.65326, 1e-5)

# 18. Lesson 18: fir-equiripple-and-comparison
# Type I order M=10 -> L_cos = M/2 = 5 -> at least L_cos + 2 = 7 alternations
assert (10 // 2) + 2 == 7
# Kaiser equiripple order estimate: delta1=0.01, delta2=0.001, Delta_f=0.05
M_eq = (-10 * math.log10(0.01 * 0.001) - 13) / (14.6 * 0.05)
close(M_eq, 50.6849315, 1e-4)
assert math.ceil(M_eq) == 51

# 19. Lesson 19: iir-impulse-invariance-bilinear (includes Exercise 7)
# Bilinear prewarping: fs = 8000 Hz, fc = 1000 Hz
fs_bi = 8000.0
fc_bi = 1000.0
wc_bi = 2 * math.pi * fc_bi / fs_bi
close(wc_bi, math.pi / 4)
Omega_pre = 2 * fs_bi * math.tan(wc_bi / 2)
close(Omega_pre, 6627.416997969522, 1e-4)
Omega_naive = 2 * math.pi * fc_bi
close(Omega_naive, 6283.185307179586, 1e-4)
# Without prewarping, actual digital cutoff:
wc_actual = 2 * math.atan(Omega_naive / (2 * fs_bi))
fc_actual = wc_actual * fs_bi / (2 * math.pi)
close(fc_actual, 952.8840223, 1e-4)
# Impulse invariance pole mapping: s_p = -2, T_d = 0.5 -> z_p = e^-1
close(math.exp(-2 * 0.5), 0.36787944, 1e-6)
# Bilinear pole mapping: s_p = -2, T_d = 1 -> z_p = (1 + (-2)*0.5)/(1 - (-2)*0.5) = 0
close((1 + (-2) * 0.5) / (1 - (-2) * 0.5), 0.0)

# 20. Lesson 20: iir-prototypes-and-freq-transforms
# Butterworth order: -3 dB at Omega_p = 1, >= 20 dB at Omega_s = 2
att_n3 = 10 * math.log10(1 + 2 ** (2 * 3))
att_n4 = 10 * math.log10(1 + 2 ** (2 * 4))
close(att_n3, 18.129133566, 1e-5)
close(att_n4, 24.099331233, 1e-5)
assert att_n3 < 20.0 <= att_n4
# Lowpass -> highpass z^-1 -> -z^-1 maps pi/3 -> 2*pi/3
close(math.pi - math.pi / 3, 2 * math.pi / 3)

# 21. Lesson 21: decimation-interpolation-rational (includes Exercise 8 part 1)
# 48 kHz -> 12 kHz: M = 4, cutoff = pi/4 (6 kHz)
assert 48 // 12 == 4
close(48 / (2 * 4), 6.0)
# 16 kHz -> 24 kHz: L=3, M=2 -> min(pi/3, pi/2) = pi/3, gain = 3
assert 16 * 3 // 2 == 24
close(min(math.pi / 3, math.pi / 2), math.pi / 3)

# 22. Lesson 22: multirate-noble-polyphase (includes Exercise 8 part 2)
# Length-32 FIR decimation filter, M=4, fs=48 kHz
direct_rate = 32 * 48000
poly_rate = 4 * (32 // 4) * (48000 // 4)
assert direct_rate == 1536000
assert poly_rate == 384000
assert direct_rate // poly_rate == 4
# Verify polyphase identity H(z) = E0(z^2) + z^-1 E1(z^2) for [1,2,3,4,5,6]
h_poly = [1, 2, 3, 4, 5, 6]
E0 = [1, 3, 5]
E1 = [2, 4, 6]
for k in range(10):
    z = cmath.exp(1j * 2 * math.pi * k / 10)
    Hz = sum(h_poly[n] * (z ** -n) for n in range(6))
    Ez = sum(E0[m] * ((z ** 2) ** -m) for m in range(3)) + (z ** -1) * sum(
        E1[m] * ((z ** 2) ** -m) for m in range(3)
    )
    close(Hz, Ez)

# 23. Lesson 23: dft-sinusoidal-and-stft (includes Exercise 9)
# fs = 8000 Hz, N = 1024 -> Delta_f = 7.8125 Hz
close(8000 / 1024, 7.8125)
# L = 256 at fs = 8000 -> fs/L = 31.25 Hz
close(8000 / 256, 31.25)
# STFT at fs = 16000 Hz: L=512 -> 32 ms, 31.25 Hz; L=64 -> 4 ms, 250 Hz
close(512 / 16000 * 1000, 32.0)
close(16000 / 512, 31.25)
close(64 / 16000 * 1000, 4.0)
close(16000 / 64, 250.0)

# 24. Lesson 24: periodogram-welch-random-psd
# Q = 4096, L = 512
Q_len, L_seg = 4096, 512
K_bartlett = Q_len // L_seg
assert K_bartlett == 8
R_hop = L_seg // 2
K_welch = (Q_len - L_seg) // R_hop + 1
assert K_welch == 15
# Verify periodogram non-diminishing variance empirically on unit-variance Gaussian white noise
rng = random.Random(42)
def emp_pgram_var(L_val, trials=300):
    vals = []
    w_test = math.pi / 2  # interior frequency away from 0 and pi
    for _ in range(trials):
        x = [rng.gauss(0, 1) for _ in range(L_val)]
        X = sum(x[n] * cmath.exp(-1j * w_test * n) for n in range(L_val))
        vals.append((abs(X) ** 2) / L_val)
    mean_v = sum(vals) / trials
    var_v = sum((v - mean_v) ** 2 for v in vals) / (trials - 1)
    return mean_v, var_v

m64, v64 = emp_pgram_var(64)
m256, v256 = emp_pgram_var(256)
# Both means ~ 1.0 and both variances ~ 1.0 (does NOT shrink with L!)
assert 0.8 < m64 < 1.25 and 0.8 < m256 < 1.25, (m64, m256)
assert 0.65 < v64 < 1.45 and 0.65 < v256 < 1.45, (v64, v256)

# Boss challenge extra calculations
# Boss Q4: 512-point radix-2 FFT complex multiplications = 256 * 9 = 2304
assert (512 // 2) * int(math.log2(512)) == 2304
# Boss Q5: 5 kHz sinusoid sampled at 6 kHz -> aliases to |6 - 5| = 1 kHz
close(abs(6000 - 5000), 1000.0)
# Boss Q7: Bilinear prewarping at fs=4000 Hz, fc=1000 Hz -> wc = pi/2, tan(pi/4) = 1 -> Omega_c = 8000 rad/s!
wc_boss = 2 * math.pi * 1000 / 4000
close(wc_boss, math.pi / 2)
close(2 * 4000 * math.tan(wc_boss / 2), 8000.0)
# Boss Q8: 20 kHz -> 5 kHz decimation M=4, length-20 FIR: direct 20*20000=400000 vs polyphase 4*5*5000=100000 (1/4)
assert 20 * 20000 == 400000 and 4 * 5 * 5000 == 100000

# 2026-11-23 review: new numbers so practice questions and the final challenge do not repeat worked examples
assert convolve([2, 1, 3], [1, -1, 2]) == [2, -1, 6, -1, 6]  # dt-signals-lti-systems q2: y[3] = -1


def recur(a, x):
    out, prev = [], 0.0
    for v in x:
        prev = v + a * prev
        out.append(prev)
    return out


h08 = recur(0.8, [1] + [0] * 400)
close(h08[1], 0.8)
close(h08[2], 0.64)
close(sum(abs(v) for v in h08), 5.0, 1e-9)  # difference-equations-systems q2
s04 = recur(0.4, [1] * 3)
close(s04[2], 1.56)  # difference-equations-systems q3
# dt-random-signals-corr q2: white noise var 4 through h = [1, 0.5] -> phi_yy[1] = h0*h1*4 = 2
hh = [1.0, 0.5]
close(4 * sum(hh[k] * hh[k + 1] for k in range(len(hh) - 1)), 2.0)
# inverse-z q1: x[n] = (2*0.5^n - 0.25^n) u[n] -> x[3] = 0.234375; cross-check by convolving the two geometric sequences
g1 = [0.5 ** n for n in range(6)]
g2 = [0.25 ** n for n in range(6)]
close(2 * 0.5 ** 3 - 0.25 ** 3, 0.234375)
close(convolve(g1, g2)[3], 0.234375)
# dfs-and-freq-sampling q2: [1..6] with N = 5 -> xt[0] = x[0] + x[5] = 7
xs6 = [1, 2, 3, 4, 5, 6]
xt5 = [sum(xs6[n + 5 * r] for r in range(2) if n + 5 * r < 6) for n in range(5)]
assert xt5 == [7, 2, 3, 4, 5]
X5 = [sum(xs6[n] * cmath.exp(-2j * math.pi * k * n / 5) for n in range(6)) for k in range(5)]
close(idft(X5)[0].real, 7.0, 1e-9)
# Boss b1: y[n] = x[n] + 0.25 y[n-1] -> h = 0.25^n u[n], sum = 4/3
close(sum(recur(0.25, [1] + [0] * 200)), 4 / 3, 1e-9)
# Boss b2: X(z) = 1/((1-0.8z^-1)(1-0.4z^-1)), |z| > 0.8 -> A = 2, B = -1, x[2] = 1.12
A = 1 / (1 - 0.4 / 0.8)
B = 1 / (1 - 0.8 / 0.4)
close(A, 2.0)
close(B, -1.0)
close(A * 0.8 ** 2 + B * 0.4 ** 2, 1.12)
close(convolve([0.8 ** n for n in range(4)], [0.4 ** n for n in range(4)])[2], 1.12)
# Boss b4: eight ones -> 8-point DFT [8, 0, ..., 0]; zero-padded to 16, |X16[1]| = 1/sin(pi/16) ~ 5.126
X8 = dft([1] * 8)
close(abs(X8[0]), 8.0)
assert all(abs(v) < 1e-9 for v in X8[1:])
X16 = dft([1] * 8 + [0] * 8)
close(abs(X16[1]), 5.126, 1e-3)
close(abs(X16[1]), 1 / math.sin(math.pi / 16), 1e-9)
# Boss b7: Blackman M ~ 5.5 / 0.05 = 110
close(5.5 / 0.05, 110.0)

print("ALL E.2.1 VERIFICATIONS PASSED!")
