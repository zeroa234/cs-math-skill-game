"""E.2.4 无线与移动通信 — every number in data/content/E.2.4.yaml, recomputed.

Run: python3 -I tests/content/E.2.4.verify.py [path/to/E.2.4.yaml]
Plain Python (stdlib only). Reads back every `number` item answer from the YAML
and compares it against an independently computed value, plus checks card/example
constants and physical laws (Friis FSPL from power density & aperture, two-ray
crossover & d^4 decay, log-normal outage via erfc, thermal noise & link budget,
RMS delay spread from PDP, coherence bandwidth/time & Doppler shift, Rayleigh/
Rician statistics & Jakes U-spectrum normalization, Rayleigh BPSK BER via both
Simpson numerical integration and closed form, 2-branch MRC BER via numerical
integration over Gamma(2) and closed form, waterfilling optimality check,
Rayleigh slow-fading outage capacity, DFT orthogonality, CP linear-to-circular
convolution equivalence, OFDM PAPR waveform check, MIMO SVD capacity & pure-LOS
rank-1 Frobenius identity, ZF vs MMSE SINR, Zheng-Tse DMT curve, CDMA processing
gain & near-far SIR, MAC sum capacity vs TDMA, cellular reuse D/R & SIR,
Erlang-B blocking & trunking efficiency, LTE RB & 5G NR numerology).
"""
import cmath
import math
import re
import sys
from math import comb, erfc, exp, factorial, log2, log10, pi, sqrt
from pathlib import Path

checks = 0
computed = {}
FAILS = []


def close(a, b, tol=1e-9, what=""):
    global checks
    if abs(a - b) > tol * max(1.0, abs(b)) and abs(a - b) > tol:
        FAILS.append(f"{what}: {a} != {b}")
    checks += 1


def ok(cond, what=""):
    global checks
    if not cond:
        FAILS.append(f"FAILED: {what}")
    checks += 1


def ans(item_id, value, tol=1e-9):
    computed[item_id] = (value, tol)


def Q(x):
    return 0.5 * erfc(x / sqrt(2.0))


def simpson(f, a, b, n=2000):
    if n % 2 == 1:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 == 1 else 2) * f(a + i * h)
    return s * h / 3.0


def dft(x):
    N = len(x)
    return [
        sum(x[n] * cmath.exp(-2j * pi * k * n / N) for n in range(N))
        for k in range(N)
    ]


def idft(X):
    N = len(X)
    return [
        sum(X[k] * cmath.exp(2j * pi * k * n / N) for k in range(N)) / N
        for n in range(N)
    ]


def erlang_b(C, A):
    num = (A ** C) / factorial(C)
    den = sum((A ** k) / factorial(k) for k in range(C + 1))
    return num / den


c = 3e8
kB = 1.380649e-23
T0 = 290.0

# ==== L01: wireless-intro ====
close(c / 2.4e9 * 100, 12.5, 1e-6, "L01 2.4 GHz wavelength cm")
close(c / 3e9 * 100, 10.0, 1e-6, "L01 3 GHz wavelength cm")
close(20 - (-90), 110.0, 1e-9, "L01 card attenuation dB")
ans("q-wavelength", c / 5e9 * 100, 0.05)
ans("q-loss-db", 30 - (-85), 0.1)

# ==== L02: free-space ====
# First-principles check: Pr = (Pt * Gt / (4*pi*d^2)) * (Gr * lam^2 / (4*pi))
def friis_ratio(d, f):
    lam = c / f
    power_density = 1.0 / (4 * pi * d * d)
    ae = lam * lam / (4 * pi)
    return power_density * ae

# Frequency doubling -> +6.02 dB FSPL
close(-10 * log10(friis_ratio(1000, 2e9) / friis_ratio(1000, 1e9)), 6.0206, 1e-3, "L02 freq double +6dB")
# Example: 1 GHz, 500 m
fspl_ex = -10 * log10(friis_ratio(500, 1e9))
close(fspl_ex, 20 * log10(4 * pi * 500 / 0.3), 1e-9, "L02 Friis identity")
close(fspl_ex, 86.42, 0.05, "L02 example FSPL")
close(30 + 10 + 2 - fspl_ex, -44.42, 0.05, "L02 example Pr")
# Practice
ans("q-fspl-900", round(-10 * log10(friis_ratio(1000, 900e6)), 1), 0.1)
ans("q-friis-pr", 23 + 6 + 3 - 92, 0.1)

# ==== L03: propagation ====
# Two-ray far-field interference check: |1 - exp(-j*2*pi*delta_d/lam)|^2 with delta_d = 2*ht*hr/d
ht, hr, d_far, lam = 30.0, 1.5, 50000.0, 0.3
delta_d = sqrt(d_far**2 + (ht + hr)**2) - sqrt(d_far**2 + (ht - hr)**2)
interf_sq = abs(1 - cmath.exp(-2j * pi * delta_d / lam))**2
pr_exact = (lam / (4 * pi * d_far))**2 * interf_sq
pr_asymp = (ht * hr / d_far**2)**2
close(pr_exact / pr_asymp, 1.0, 1e-3, "L03 two-ray d^4 asymptotic")
close(4 * 30 * 1.5 / 0.3, 600.0, 1e-9, "L03 example dc")
# Example: log-distance & shadowing
close(80 + 10 * 3.2 * log10(1000 / 100), 112.0, 1e-9, "L03 example PL")
close(Q(12 / 8) * 100, 6.68, 0.02, "L03 example shadow outage %")
# Practice
ans("q-tworay-dc", 4 * 25 * 2 / 0.25, 1.0)
ans("q-logdist-inc", 10 * 3.8 * log10(500 / 50), 0.1)
ans("q-shadow-prob", round(Q(6 / 6) * 100, 1), 0.2)

# ==== L04: link-budget ====
n0_dbm_hz = 10 * log10(kB * T0 * 1000)
close(n0_dbm_hz, -173.98, 0.05, "L04 thermal noise dBm/Hz at 290K")
# Example
pmin_ex = -174 + 10 * log10(10e6) + 6 + 4
close(pmin_ex, -94.0, 1e-9, "L04 example sensitivity")
mapl_ex = 43 + 15 + 0 - 2 - 10 - pmin_ex
close(mapl_ex, 140.0, 1e-9, "L04 example MAPL")
close(10 ** ((mapl_ex - 128) / 35), 2.202, 0.01, "L04 example radius km")
# Practice
ans("q-sens", -174 + 10 * log10(1e6) + 7 + 9, 0.1)
ans("q-mapl", 40 + 14 + 0 - 4 - 12 - (-102), 0.1)
ans("q-radius", round(10 ** ((148 - 130) / 36), 2), 0.05)

# ==== L05: multipath-model ====
def rms_delay(weights, taus):
    tot = sum(weights)
    mean = sum(w * t for w, t in zip(weights, taus)) / tot
    mean2 = sum(w * t * t for w, t in zip(weights, taus)) / tot
    return mean, sqrt(mean2 - mean * mean)

m_ex, s_ex = rms_delay([0.5, 0.5], [0.0, 2.0])
close(m_ex, 1.0, 1e-9, "L05 example mean tau")
close(s_ex, 1.0, 1e-9, "L05 example rms tau")
# Practice
ans("q-taps", 1 + int(round(10e6 * 1.5e-6)), 0.1)
_, s_p = rms_delay([0.75, 0.25], [0.0, 4.0])
ans("q-rms-delay", round(s_p, 2), 0.03)

# ==== L06: coherence ====
# Example
close(1 / (5 * 0.5e-6) / 1e3, 400.0, 1e-6, "L06 example Bc kHz")
v_ex = 72 / 3.6
fd_ex = v_ex * 1.8e9 / c
close(fd_ex, 120.0, 1e-6, "L06 example fD Hz")
close(0.423 / fd_ex * 1e3, 3.525, 1e-3, "L06 example Tc ms")
# Practice
ans("q-bc-calc", 1 / (5 * 0.25e-6) / 1e3, 1.0)
ans("q-doppler-hsr", (360 / 3.6) * 2.1e9 / c, 1.0)
ans("q-tc-calc", round(0.423 / 150 * 1e3, 2), 0.02)

# ==== L07: rayleigh-rician ====
close((1 - exp(-0.1)) * 100, 9.52, 0.02, "L07 Rayleigh -10dB %")
close((1 - exp(-0.01)) * 100, 0.995, 0.01, "L07 Rayleigh -20dB %")
# Jakes U-spectrum normalization via substitution f = fD * cos(theta): integral_0^pi (1/pi) dtheta = 1
jakes_norm = simpson(lambda th: 1.0 / pi, 0.0, pi, 100)
close(jakes_norm, 1.0, 1e-9, "L07 Jakes spectrum norm")
# Practice
ans("q-rayleigh-out", round((1 - exp(-0.05)) * 100, 2), 0.1)
ans("q-rician-k", round(10 * log10(8 / 2), 2), 0.05)

# ==== L08: fading-ber ====
def rayleigh_bpsk_exact(g):
    return 0.5 * (1.0 - sqrt(g / (1.0 + g)))

def rayleigh_bpsk_num(g):
    # Substitute u = t^2 (du = 2t dt) to remove the sqrt(u) derivative singularity at 0
    return simpson(lambda t: Q(sqrt(2.0 * g) * t) * exp(-t * t) * 2.0 * t, 0.0, 6.0, 2000)

close(rayleigh_bpsk_exact(10.0), rayleigh_bpsk_num(10.0), 1e-7, "L08 numerical vs exact 10dB")
close(rayleigh_bpsk_exact(10.0), 0.0233, 0.0005, "L08 10dB exact BER")
close(Q(sqrt(20.0)), 3.87e-6, 5e-8, "L08 10dB AWGN BER")
close(10 * log10(250.0), 23.98, 0.05, "L08 1e-3 Rayleigh SNR dB")
# Practice
ans("q-ber-approx", 1 / (4 * 50) * 100, 0.02)
ans("q-ber-slope", 10 * log10(1e-2 / 1e-4), 0.1)

# ==== L09: time-diversity ====
close(0.05 ** 3, 1.25e-4, 1e-12, "L09 3-branch outage")
ans("q-div-prob", 0.1 ** 4, 1e-6)
ans("q-div-slope", 10 ** 3, 1.0)
ans("q-interleave-delay", 2 * 2 * 25, 0.5)

# ==== L10: antenna-diversity ====
def mrc_bpsk_exact(g, L):
    mu = sqrt(g / (1.0 + g))
    p = 0.5 * (1.0 - mu)
    return (p ** L) * sum(comb(L - 1 + k, k) * ((1.0 - p) ** k) for k in range(L))

def mrc_2_num(g):
    # Gamma(2, g): pdf(u) = u * exp(-u) for u = gamma / g
    return simpson(lambda u: Q(sqrt(2.0 * g * u)) * u * exp(-u), 0.0, 35.0, 4000)

close(mrc_bpsk_exact(10.0, 2), mrc_2_num(10.0), 1e-5, "L10 2-MRC numerical vs exact 10dB")
close(mrc_bpsk_exact(10.0, 2), 1.60e-3, 1e-5, "L10 2-MRC 10dB exact")
close(3 / (16 * 10**2), 1.875e-3, 1e-9, "L10 2-MRC 10dB approx")
close(c / 3e9 / 2 * 100, 5.0, 1e-6, "L10 3 GHz half-wave cm")
# Practice
ans("q-mrc-snr", 2 + 5 + 8 + 5, 0.05)
ans("q-half-wave", c / 2.5e9 / 2 * 100, 0.05)
ans("q-mrc-ber-25", 3 / (16 * 25**2) * 1e4, 0.05)

# ==== L11: frequency-diversity ====
close(1 + int(4e6 * 1.25e-6), 6, 1e-9, "L11 example taps")
close(c / 4e6, 75.0, 1e-6, "L11 example RAKE dist")
ans("q-freq-taps", 1 + int(round(5e6 * 0.8e-6)), 0.1)
ans("q-rake-dist", c * 0.2e-6, 0.5)

# ==== L12: fading-capacity ====
# Waterfilling optimality check vs equal power split
c_wf = log2(1 + 6 / 1) + log2(1 + 4 / 3)
c_eq = log2(1 + 5 / 1) + log2(1 + 5 / 3)
ok(c_wf > c_eq, "L12 waterfilling strictly beats equal power")
# Outage example
close((1 - exp(-(2**2 - 1) / 20)) * 100, 13.93, 0.05, "L12 example outage %")
close(log2(1 - 20 * math.log(1 - 0.01)), 0.264, 0.005, "L12 example 1% outage rate")
close(log2(21), 4.392, 0.005, "L12 AWGN 20 rate")
# Practice
ans("q-waterfill", (10 + 1 + 3) / 2 - 1, 0.05)
ans("q-outage-calc", round((1 - exp(-(2**3 - 1) / 50)) * 100, 1), 0.15)
ans("q-pilot-overhead", 18 / 20 * 100, 0.1)

# ==== L13: ofdm-principle ====
# Verify DFT subcarrier orthogonality for N=16
N_chk = 16
for k in range(N_chk):
    for m in range(N_chk):
        ip = sum(cmath.exp(2j * pi * (k - m) * n / N_chk) for n in range(N_chk))
        close(abs(ip), N_chk if k == m else 0.0, 1e-9, f"L13 DFT ortho {k},{m}")
# Example
close(10e6 / 256 / 1e3, 39.0625, 1e-6, "L13 example df")
close(256 / 10e6 * 1e6, 25.6, 1e-6, "L13 example Tu")
close(256 * 4, 1024, 1e-9, "L13 example bits")
# Practice
ans("q-ofdm-df", 16e6 / 128 / 1e3, 0.1)
ans("q-ofdm-tu", 1 / 125e3 * 1e6, 0.05)
ans("q-ofdm-bits", 200 * 6, 0.1)

# ==== L14: cyclic-prefix ====
# Verify CP turns linear convolution into exact frequency-domain multiplication!
N_cp = 8
L_cp = 3
X_freq = [1+1j, -1+1j, 1-1j, -1-1j, 1+0j, 0-1j, -1+0j, 0+1j]
x_time = idft(X_freq)
x_with_cp = x_time[-L_cp:] + x_time
h_chan = [0.8+0.1j, -0.3+0.4j, 0.15-0.2j]  # length 3 <= L_cp + 1
# Linear convolution
y_lin = [
    sum(h_chan[l] * x_with_cp[n - l] for l in range(len(h_chan)) if 0 <= n - l < len(x_with_cp))
    for n in range(len(x_with_cp))
]
y_stripped = y_lin[L_cp:L_cp + N_cp]
Y_freq = dft(y_stripped)
H_freq = dft(h_chan + [0] * (N_cp - len(h_chan)))
for k in range(N_cp):
    close(abs(Y_freq[k] - H_freq[k] * X_freq[k]), 0.0, 1e-9, f"L14 CP one-tap eq k={k}")
# Example
close(8 / (32 + 8) * 100, 20.0, 1e-9, "L14 example CP overhead")
close(1 / 40e-6, 25000.0, 1e-6, "L14 example sym/s")
# Practice
ans("q-cp-overhead", 16 / (64 + 16) * 100, 0.1)
ans("q-cp-samples", 2.4 / 0.1, 0.1)
ans("q-cp-rate", 100 * 2 / 50e-6 / 1e6, 0.05)

# ==== L15: ofdm-design ====
# Construct N=128 equal-amplitude all-in-phase OFDM waveform to verify peak/avg power = N
N_papr = 128
x_papr = [sum(cmath.exp(2j * pi * k * n / N_papr) for k in range(N_papr)) / sqrt(N_papr) for n in range(N_papr)]
p_inst = [abs(v)**2 for v in x_papr]
papr_lin = max(p_inst) / (sum(p_inst) / len(p_inst))
close(papr_lin, N_papr, 1e-6, "L15 PAPR waveform peak/avg == N")
ans("q-df-doppler", 20 * (30 * 3e9 / c) / 1e3, 0.1)
ans("q-papr-calc", round(10 * log10(papr_lin), 1), 0.1)

# ==== L16: mimo-capacity ====
# Example: sigma = [2, 1], total SNR = 10
c_eq_mimo = log2(1 + 5 * 4) + log2(1 + 5 * 1)
mu_mimo = (10 + 0.25 + 1.0) / 2
c_wf_mimo = log2(1 + (mu_mimo - 0.25) * 4) + log2(1 + (mu_mimo - 1.0) * 1)
close(c_eq_mimo, 6.977, 0.01, "L16 example equal MIMO cap")
close(c_wf_mimo, 6.981, 0.01, "L16 example WF MIMO cap")
ok(c_wf_mimo >= c_eq_mimo, "L16 WF >= equal")
# Practice
ans("q-mimo-dof", min(4, 2), 0.1)
ans("q-mimo-cap-exact", log2(1 + 7 * 9) + log2(1 + 7 * 1), 0.05)
ans("q-mimo-highsnr", min(3, 3) * log2(256), 0.1)

# ==== L17: mimo-channel ====
# Verify pure LOS 4x4 outer product matrix Frobenius norm squared == Nt * Nr
er = [cmath.exp(1j * 0.7 * i) for i in range(4)]
et = [cmath.exp(1j * 1.1 * j) for j in range(4)]
H_los = [[er[i] * et[j].conjugate() for j in range(4)] for i in range(4)]
frob_sq = sum(abs(H_los[i][j])**2 for i in range(4) for j in range(4))
close(frob_sq, 16.0, 1e-9, "L17 LOS Frobenius^2 == 16")
close(1 / (8 * 0.5), 0.25, 1e-9, "L17 example angular res")
# Practice
ans("q-los-rank", 1, 0.05)
ans("q-los-sigma", frob_sq, 0.1)
ans("q-ang-res", 1 / 5.0, 0.01)

# ==== L18: mimo-receivers ====
# Example: diag(1, 0.5), P2=4, N0=1 -> ZF SNR2 = 4 / 4 = 1
close(4 / (1 / 0.5**2), 1.0, 1e-9, "L18 example ZF SNR")
# Verify MMSE SINR >= ZF SNR on a correlated 2x2 channel [[1, 0.9], [0, 0.4]]
h1, h2 = (1.0, 0.0), (0.9, 0.4)
# ZF for stream 1 projects orthogonal to h2: u = (0.4, -0.9)
u_zf = (0.4, -0.9)
num_zf = (u_zf[0]*h1[0] + u_zf[1]*h1[1])**2
den_zf = u_zf[0]**2 + u_zf[1]**2
snr_zf = num_zf / den_zf
# MMSE: R = h2 h2^T + I -> invert 2x2
r00, r01, r11 = h2[0]**2 + 1, h2[0]*h2[1], h2[1]**2 + 1
det = r00 * r11 - r01**2
sinr_mmse = (r11 * h1[0]**2 - 2*r01*h1[0]*h1[1] + r00*h1[1]**2) / det
ok(sinr_mmse > snr_zf, "L18 MMSE SINR strictly beats ZF on correlated channel")
# Practice
ans("q-zf-div", 5 - 2 + 1, 0.05)
ans("q-zf-noise", 32 / (1 / 0.25**2), 0.05)

# ==== L19: dmt-beamforming ====
close((4 - 1) * (4 - 1), 9, 1e-9, "L19 4x4 DMT r=1")
ans("q-dmt-max", 3 * 3, 0.05)
ans("q-dmt-r1", (3 - 1) * (3 - 1), 0.05)
ans("q-bf-gain", round(10 * log10(16), 1), 0.1)

# ==== L20: fdma-tdma ====
close(10e6 / 200e3 * 8, 400, 1e-9, "L20 GSM 10MHz slots")
ans("q-fdma-users", 6000 / 30, 0.1)
ans("q-tdma-slot", round(4.8 / 8 - 0.05, 2), 0.01)

# ==== L21: cdma ====
close(1.2288e6 / 9.6e3, 128.0, 1e-9, "L21 example Gp")
close(1 + 128 / 4, 33.0, 1e-9, "L21 example max users")
close(10 * log10((1000 / 50)**4), 52.04, 0.05, "L21 near-far 52dB")
ans("q-gp-calc", 3.84e6 / 15e3, 0.1)
ans("q-cdma-sir", 64 / (17 - 1), 0.05)
ans("q-near-far", 64 / 100.0, 0.01)

# ==== L22: multiuser ====
c_mac_ex = log2(1 + 7 + 8)
c_tdma_ex = 0.5 * log2(1 + 7) + 0.5 * log2(1 + 8)
ok(c_mac_ex > c_tdma_ex, "L22 MAC sum rate > equal-time TDMA without peak boost")
ans("q-mac-sum", log2(1 + 15 + 16), 0.05)
ans("q-pf-metric", 18 / 6, 0.05)

# ==== L23: cellular-reuse ====
close(sqrt(3 * 3)**4 / 6, 13.5, 1e-9, "L23 example N=3 SIR")
close(10 * log10(13.5), 11.30, 0.05, "L23 example N=3 SIR dB")
ans("q-reuse-dr", sqrt(3 * 12), 0.05)
ans("q-cell-cap", 300 / 4 * 20, 0.5)
ans("q-sir-n4", (3 * 4)**2 / 6, 0.1)

# ==== L24: cellular-capacity ====
close(10 * log10(3), 4.77, 0.02, "L24 3-sector gain dB")
close(120 * 3 / 60, 6.0, 1e-9, "L24 example Erlang")
close(erlang_b(2, 1) * 100, 20.0, 1e-9, "L24 example Erlang-B(2,1) %")
# Verify trunking efficiency: 1 pool of 60 channels beats 3 pools of 20 at same load/channel
ok(erlang_b(60, 45) < erlang_b(20, 15), "L24 trunking efficiency")
ans("q-split-cap", (1.0 / 0.5)**2, 0.05)
ans("q-erlang-a", 240 * 2.5 / 60, 0.1)
ans("q-erlang-b", erlang_b(2, 2) * 100, 0.2)

# ==== L25: lte-phy ====
close(100 * 180e3 / 1e6, 18.0, 1e-9, "L25 20MHz effective BW")
ans("q-lte-rb-bw", 12 * 15, 0.1)
ans("q-lte-10m", 50 * 0.18, 0.05)

# ==== L26: nr-phy ====
close(20 * log10(28 / 2.8), 20.0, 1e-9, "L26 28GHz vs 2.8GHz FSPL")
close(10 * log10(100), 20.0, 1e-9, "L26 100x planar array gain")
ans("q-nr-df", 15 * (2 ** 2), 0.1)
ans("q-nr-slot", 1 / (2 ** 3), 0.002)
ans("q-mmwave-loss", 20 * log10(30 / 3), 0.1)

# ==== BOSS (original skill-tree comprehensive exercise) ====
ans("b-fspl", round(-10 * log10(friis_ratio(1000, 2e9)), 1), 0.2)
ans("b-logdist", 10 * 3.5 * log10(1000 / 100), 0.1)
ans("b-bc", 1 / (5 * 2e-6) / 1e3, 0.5)
ans("b-doppler", (108 / 3.6) * 2e9 / c, 0.5)
ans("b-tc", round(0.423 / 200 * 1e3, 2), 0.05)
# Boss 3: 20 dB Rayleigh BER exact & approx, plus 2-branch MRC check
close(rayleigh_bpsk_exact(100.0), 2.48e-3, 2e-5, "Boss 20dB Rayleigh exact")
close(mrc_bpsk_exact(100.0, 2), 1.84e-5, 2e-7, "Boss 20dB 2-MRC exact")
close(3 / (16 * 100**2), 1.875e-5, 1e-9, "Boss 20dB 2-MRC approx")
ans("b-rayleigh-ber", round(1 / (4 * 100) * 100, 2), 0.01)
ans("b-ofdm-df", 20e6 / 64 / 1e3, 0.2)
ans("b-ofdm-tu", 1 / (20e6 / 64) * 1e6, 0.05)
ans("b-mimo-cap", round(4 * log2(100), 1), 0.2)
close(log2(101), 6.658, 0.01, "Boss SISO 20dB cap")
ans("b-cellular-sir", round(10 * log10(((3 * 7) ** 2) / 6), 1), 0.15)


# ==== Read back EVERY number item from YAML and verify ====
yaml_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/content/E.2.4.yaml")
text = yaml_path.read_text(encoding="utf-8")
items_found = {}
cur_id = None
cur_type = None
for line in text.splitlines():
    m_id = re.match(r"^\s*(?:-\s*)?id:\s*([a-z0-9-]+)\s*$", line)
    if m_id:
        cur_id = m_id.group(1)
        cur_type = None
        continue
    m_ty = re.match(r"^\s*type:\s*(\w+)\s*$", line)
    if m_ty:
        cur_type = m_ty.group(1)
        continue
    m_ans = re.match(r"^\s*answer:\s*([-+0-9.eE]+)\s*$", line)
    if m_ans and cur_type == "number" and cur_id:
        items_found[cur_id] = float(m_ans.group(1))

for item_id, yaml_val in items_found.items():
    if item_id not in computed:
        FAILS.append(f"YAML number item '{item_id}' ({yaml_val}) is NOT verified in verify.py!")
    else:
        exp_val, tol = computed[item_id]
        close(yaml_val, exp_val, tol, f"YAML item {item_id}")

for item_id in computed:
    if item_id not in items_found:
        FAILS.append(f"verify.py computed '{item_id}' but it was NOT found as a number item in YAML!")

if FAILS:
    print(f"FAIL ({len(FAILS)} failures out of {checks} checks):")
    for f in FAILS:
        print("  -", f)
    sys.exit(1)
else:
    print(f"OK: E.2.4.verify.py passed {checks} checks ({len(items_found)} YAML number items verified).")
