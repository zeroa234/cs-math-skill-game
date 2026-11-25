"""E.2.3 通信原理 — every number in data/content/E.2.3.yaml, recomputed.

Run: python -I tests/content/E.2.3.verify.py
Plain Python (no numpy). Formulas taught in the pack are checked against independent calculations where
it is cheap: Q(x) against a numerical Gaussian tail integral, the random-phase autocorrelation by
averaging over the phase, the RC noise bandwidth by integrating |H|², AM power and coherent detection by
time averages, the J0 zero by its power series and bisection, the PCM quantisation SNR by quantising a
sine wave, the PCM bit-error formula by summing the error power of each bit, raised-cosine zero crossings
in the time domain, the zero-forcing taps by solving the linear equations, the matched-filter SNR by
discrete convolution, Hamming encoding and syndrome decoding over all 16 codewords, CRC by polynomial
division, the convolutional code by brute-force maximum-likelihood decoding (what Viterbi finds) and its
free distance, and the Barker autocorrelation. Every number and text answer is read back and compared.
"""
import cmath
import itertools
import math
import re
from math import atan, cos, erfc, exp, log, log2, log10, pi, sin, sqrt
from pathlib import Path

checks = 0
computed = {}
texts = {}

K_B = 1.38e-23


def close(a, b, tol=1e-9, what=""):
    global checks
    if abs(a - b) > tol * max(1.0, abs(b)) and abs(a - b) > tol:
        raise AssertionError(f"{what}: {a} != {b}")
    checks += 1


def ok(cond, what):
    global checks
    if not cond:
        raise AssertionError(what)
    checks += 1


def ans(item_id, value, tol=1e-9):
    computed[item_id] = (value, tol)


def simpson(f, a, b, n=4000):
    if n % 2:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


def Q(x):
    return 0.5 * erfc(x / sqrt(2))


def db(x):
    return 10 * log10(x)


def undb(x):
    return 10 ** (x / 10)


# Q from erfc agrees with a direct tail integral
for x in (1, 2, 3, 4):
    tail = simpson(lambda u: exp(-u * u / 2) / sqrt(2 * pi), x, x + 12, 8000)
    close(Q(x), tail, 1e-9, f"Q({x}) tail integral")
close(Q(1), 0.159, 0.0005, "Q1"); close(Q(2), 0.0228, 0.00005, "Q2")
close(Q(3), 1.35e-3, 0.005e-3, "Q3"); close(Q(4), 3.2e-5, 0.05e-5, "Q4")

# ---- system-model ----
close(sqrt(2 * (4 / 3) * 6371e3 * 1) / 1e3, 4.12, 0.005, "4.12 sqrt(h) from the 4/3 earth radius")
ans("los-100", 4.12 * sqrt(100), 0.5)
ans("rate-4ary", 2400 * log2(4))
ans("ser", 12 / 1e6 / 1e-5, 0.001)

# ---- information-capacity ----
ans("info-16", log2(16))
H = lambda ps: sum(p * log2(1 / p) for p in ps)
close(H([1 / 2, 1 / 4, 1 / 8, 1 / 8]), 1.75, 1e-12, "1.75"); close(H([1 / 4] * 4), 2, 1e-12, "2 bits")
ans("entropy-3", H([1 / 2, 1 / 4, 1 / 4]))
ans("rate-8ary", 1000 * log2(8))
close(log2(1001), 9.97, 0.005, "log2 1001"); close(3000 * log2(1001) / 1e3, 29.9, 0.05, "29.9 kb/s")
ans("capacity-1m", 1e6 * log2(1 + undb(20)) / 1e6, 0.005)
close(1e6 * log2(21) / 1e6, 4.39, 0.005, "dB mistake 4.39")
ans("snr-2b", db(2 ** 2 - 1), 0.005)
c1, c2 = 1e3 * log2(1 + 1e3 / 1e3), 2e3 * log2(1 + 1e3 / 2e3)  # S/N0 = 1000, B = 1 kHz then 2 kHz
ok(c1 < c2 < 2 * c1, "doubling B raises C by less than 2x")
close(1e3 / log(2) / 1e3, 1.44, 0.005, "C_inf = 1.44 S/N0")
close(db(log(2)), -1.6, 0.01, "Shannon limit -1.6 dB")

# ---- signals-power ----
ans("sine-50", (10 / sqrt(2)) ** 2 / 50)
close(10 / sqrt(2), 7.07, 0.005, "7.07 V")
ans("dbm-2w", db(2000), 0.05)
ans("db-chain", -50 + 30 - 6)
ans("null-bw", 1 / 1e-6 / 1e6)
# rectangular pulse of width T: |P(f)| = T|sinc(fT)| has its first zero at 1/T
T = 1e-3
P = lambda f: abs(simpson(lambda t: cos(2 * pi * f * t), -T / 2, T / 2, 400))
ok(P(1 / T) < 1e-12 and P(0.5 / T) > 0.1 * T, "first null at 1/T (1 kHz for 1 ms)")

# ---- random-processes ----
A, w0, tau = 4.0, 2 * pi * 50, 0.003
R = simpson(lambda th: A * cos(w0 * 0.01 + th) * A * cos(w0 * (0.01 + tau) + th), 0, 2 * pi) / (2 * pi)
close(R, A * A / 2 * cos(w0 * tau), 1e-9, "random-phase autocorrelation")
mean = simpson(lambda th: A * cos(w0 * 0.01 + th), 0, 2 * pi) / (2 * pi)
close(mean, 0, 1e-9, "zero mean")
ans("r0-power", A * A / 2)
ans("white-lpf", simpson(lambda f: 1e-9, -1e6, 1e6, 10) * 1e3)
close(1e-9 * 1e6 * 1e3, 1, 1e-9, "one-sided mistake 1 mW")

# ---- noise-linear ----
# RC low-pass |H|² = 1/(1 + (f/fc)²): B_N = ∫0^∞ |H|² df, with f = fc tan(u)
fc = 10e3
bn = simpson(lambda u: 1 / (1 + math.tan(u) ** 2) * fc / cos(u) ** 2, 0, pi / 2 - 1e-9)
close(bn, pi / 2 * fc, 1e-3, "RC noise bandwidth")
ans("rc-noise-bw", bn / 1e3, 0.05)
ans("gauss-2sigma", 2 * Q(2) * 100, 0.005)
close(2 * Q(3) * 100, 0.27, 0.005, "3 sigma 0.27%")
kT = K_B * 290
close(kT, 4.00e-21, 0.005e-21, "kT"); close(db(kT * 1e3), -174, 0.5, "-174 dBm/Hz")
close(db(kT * 1e6 * 1e3), -114, 0.5, "-114 dBm in 1 MHz")
ans("ktb-10k", db(kT * 1e4 * 1e3), 0.5)
v2 = 4 * K_B * 290 * 1e3 * 1e6
close(v2, 1.6e-11, 0.005e-11, "1.6e-11 V2")
ans("noise-voltage", sqrt(v2) * 1e6, 0.05)
# bandpass noise: E[n²] = ½E[nc²] + ½E[ns²]
sig2 = 3.0
close(0.5 * sig2 + 0.5 * sig2, sig2, 1e-12, "nc, ns variance = n variance")

# ---- channel-models ----
close(300 / 3e8 * 1e6, 1, 1e-12, "300 m -> 1 us")
ans("delay-spread", 600 / 3e8 * 1e6)
ans("coherence-bw", 1 / 2e-6 / 1e3)
close(-90 - (-114), 24, 1e-12, "24 dB")
ans("rx-snr", -100 - (-114))
close(undb(14), 25, 0.2, "about 25 times")

# ---- bandpass-envelope ----
def bp_rate(fl, fh):
    b = fh - fl
    n = int(fh // b)
    return 2 * fh / n


def no_alias(fl, fh, fs):
    # spectral copies of [fl, fh] and [-fh, -fl] shifted by k fs must not overlap [fl, fh]
    for k in range(-100, 101):
        for lo, hi in ((fl + k * fs, fh + k * fs), (-fh + k * fs, -fl + k * fs)):
            if (lo, hi) == (fl, fh):
                continue
            if lo < fh - 1e-9 and hi > fl + 1e-9:
                return False
    return True


close(bp_rate(20, 25), 10, 1e-12, "20-25 MHz -> 10 MHz"); ok(no_alias(20, 25, 10), "10 MHz does not alias")
ans("bp-sample", bp_rate(100, 104))
ok(no_alias(100, 104, 8), "8 MHz does not alias"); ok(not no_alias(100, 104, 7.9), "7.9 MHz aliases")
ans("bp-width", 2 * 5)

# ---- am-dsb ----
ans("am-bw", 2 * 4)
fcar, fm_ = 1000.0, 10.0
Pt = simpson(lambda t: (sqrt(200) * (1 + 0.5 * cos(2 * pi * fm_ * t)) * cos(2 * pi * fcar * t)) ** 2, 0, 1, 200000)
close(Pt, 112.5, 1e-3, "AM total power by time average (carrier 100 W, mu 0.5)")
close(12.5 / 112.5 * 100, 11.1, 0.05, "11.1%")
eff = lambda mu: mu * mu / (2 + mu * mu)
close(eff(1), 1 / 3, 1e-12, "1/3")
ans("am-eff", eff(0.8) * 100, 0.05)
ans("am-total", 1000 * (1 + 1 / 2))
# coherent detection with phase error: average of m cos(wt) * cos(wt + phi) = (m/2) cos(phi)
out = lambda phi: simpson(lambda t: cos(2 * pi * fcar * t) * cos(2 * pi * fcar * t + phi), 0, 1, 200000)
ans("phase-error", out(pi / 3) / out(0), 1e-6)
close(out(pi / 2), 0, 1e-9, "90 degrees -> zero")

# ---- ssb-vsb-fdm ----
ans("ssb-bw", 4)
ans("fdm-12", 12 * 4)
close(108 - 60, 48, 1e-12, "60-108 kHz")
ans("stereo-top", 38 + 15)
close(38 - 15, 23, 1e-12, "23 kHz")
lo = 1000 + 465
close(lo, 1465, 1e-12, "LO 1465")
ans("image-freq", lo + 465)

# ---- fm-pm ----
ans("fm-beta", 75 / 15)
close(2 * (75 + 15), 180, 1e-12, "180 kHz"); close(2 * (5 + 3), 16, 1e-12, "16 kHz")
close(180 / 30, 6, 1e-12, "6x AM")
ans("carson", 2 * (50 + 10))
close(2 * 50, 100, 1e-12, "2 delta-f mistake")


def J0(x):
    return sum((-1) ** k * (x / 2) ** (2 * k) / math.factorial(k) ** 2 for k in range(40))


a_, b_ = 2.0, 3.0
for _ in range(80):
    m_ = (a_ + b_) / 2
    if J0(a_) * J0(m_) <= 0:
        b_ = m_
    else:
        a_ = m_
close(a_, 2.405, 0.0005, "first zero of J0")
ans("carrier-null", 2.405 * 2, 0.005)

# ---- analog-noise ----
close(30 + db(1 / 3), 25.2, 0.05, "AM 25.2"); close(db(1.5 * 25), 15.7, 0.05, "FM +15.7"); close(30 + db(37.5), 45.7, 0.05, "45.7")
close(2 * (5 + 1), 12, 1e-12, "12W")
ans("fm-gain-db", db(1.5 * 9), 0.05)
ans("am-out", 40 + db(1 / 3), 0.05)
ans("fm-g", 3 * 25 * 6)
close(450 * 1 / (2 * (5 + 1)), 37.5, 1e-12, "G_FM over input = 1.5 beta^2 over baseband")
# DSB vs SSB: same received power, DSB input noise in 2W
g_ = 1.0
close(2 * (g_ / 2), 1 * g_, 1e-12, "DSB output = SSB output")

# ---- pam-pcm ----
ans("music-fs", 2 * 20)
n = 8
N = 20000
sq = 0.0
sp = 0.0
step = 2 / 2 ** n
for i in range(N):
    x = sin(2 * pi * i / N + 0.1)
    qv = (math.floor(x / step) + 0.5) * step
    qv = min(max(qv, -1 + step / 2), 1 - step / 2)
    sq += (x - qv) ** 2
    sp += x * x
close(db(sp / sq), 6.02 * 8 + 1.76, 0.2, "8-bit sine SQNR by simulation")
close(6.02 * 8 + 1.76, 49.9, 0.05, "49.9")
close(db(4), 6.02, 0.005, "6.02 dB per bit")
ans("sqnr-12", 6.02 * 12 + 1.76, 0.05)
ans("pcm-rate", 12 * 16)
close(8 * 8, 64, 1e-12, "64 kb/s")
M = 256
Pe = 1e-5
# error power summed bit by bit: flips of bit i move the value by 2^i steps
err = sum(Pe * (2 ** i) ** 2 for i in range(8))
snr = (M * M / 12) / (1 / 12 + err)
close(snr, M * M / (1 + 4 * (M * M - 1) * Pe), 1e-9, "PCM error formula from bit-by-bit sum")
close(4 * 65535 * 1e-5, 2.62, 0.005, "2.62"); close(65536 / 3.62, 18100, 50, "18100")
ans("pcm-pe", db(snr), 0.05)
close(db(M * M), 48.2, 0.05, "48.2 dB")

# ---- dpcm-dm-tdm ----
ans("dm-step", 2 * pi * 1000 * 1 / 64000, 0.0005)
ans("t1-rate", (24 * 8 + 1) * 8000 / 1e6, 0.0005)
close(32 * 8 * 8000, 2.048e6, 1e-6, "E1 2.048 Mb/s")
ans("e1-voice", 30 * 64)
close(2048 - 1920, 128, 1e-12, "128 kb/s")

# ---- line-codes ----
def ami(bits):
    out, s = [], 1
    for b in bits:
        if b:
            out.append(s)
            s = -s
        else:
            out.append(0)
    return out


ok(ami([1, 0, 1, 1, 0, 0, 0, 0, 1]) == [1, 0, -1, 1, 0, 0, 0, 0, -1], "AMI example")
ok(ami([1, 1, 0, 1]) == [1, -1, 0, 1], "AMI item")


def pulse_ft(shape, f, Tb=1.0):
    re_ = simpson(lambda t: shape(t) * cos(2 * pi * f * t), 0, Tb, 2000)
    im_ = simpson(lambda t: shape(t) * sin(2 * pi * f * t), 0, Tb, 2000)
    return abs(complex(re_, im_))


nrz = lambda t: 1.0
man = lambda t: 1.0 if t < 0.5 else -1.0
ok(pulse_ft(nrz, 1.0) < 1e-6, "NRZ null at Rb")
ok(pulse_ft(man, 1.0) > 0.1 and pulse_ft(man, 2.0) < 1e-3, "Manchester first null at 2Rb")
ans("manchester-bw", 2 * 10)
ans("nrz-bw", 2)

# ---- isi-eye ----
close(1 - 0.2 - 0.2, 0.6, 1e-12, "example 0.6")
ans("isi-worst", 1 - 0.3 - 0.1, 0.0001)

# ---- nyquist ----
ans("nyq-rate", 2 * 4000)
def rc_pulse(t, Ts, a):
    if abs(t) < 1e-15:
        return 1.0
    if a > 0 and abs(abs(t) - Ts / (2 * a)) < 1e-12:
        return pi / 4 * math.sin(pi / (2 * a)) / (pi / (2 * a))
    x = t / Ts
    return math.sin(pi * x) / (pi * x) * cos(pi * a * x) / (1 - (2 * a * x) ** 2)


for a in (0.25, 0.5, 1.0):
    ok(all(abs(rc_pulse(k * 1.0, 1.0, a)) < 1e-12 for k in range(1, 8)), f"raised cosine zero ISI (alpha {a})")
close((1 + 0.25) * 1e6 / 2 / 1e3, 625, 1e-9, "625 kHz"); close(2 / 1.25, 1.6, 1e-12, "1.6 Baud/Hz")
ans("rc-bw", (1 + 0.5) * 2 / 2)
ans("rc-max", 2 * 100 / 1.25)
ans("rc-bits", 2 * 100 / 1.25 * 2)

# ---- partial-response-eq ----
def precode(d, b0=0):
    b, out = b0, []
    for x in d:
        b = x ^ b
        out.append(b)
    return out


d = [1, 0, 1, 1, 0]
bb = precode(d)
ok(bb == [1, 1, 0, 1, 1], "precoded b")
aa = [-1] + [2 * x - 1 for x in bb]
cc = [aa[i] + aa[i - 1] for i in range(1, len(aa))]
ok(cc == [0, 2, 0, 0, 2], "duobinary c")
ok([1 if c == 0 else 0 for c in cc] == d, "decode back")
ok([1 if c == 0 else 0 for c in (2, 0, -2, 0)] == [0, 1, 0, 1], "item decode 0101")


def solve3(Mx, y):
    m = [row[:] + [v] for row, v in zip(Mx, y)]
    for i in range(3):
        piv = max(range(i, 3), key=lambda r: abs(m[r][i]))
        m[i], m[piv] = m[piv], m[i]
        for r in range(3):
            if r != i:
                f = m[r][i] / m[i][i]
                m[r] = [u - f * v for u, v in zip(m[r], m[i])]
    return [m[i][3] / m[i][i] for i in range(3)]


def zf(xm1, x0, x1):
    x = {-1: xm1, 0: x0, 1: x1}
    g = lambda k: x.get(k, 0.0)
    Mx = [[g(k - n) for n in (-1, 0, 1)] for k in (-1, 0, 1)]
    return solve3(Mx, [0, 1, 0]), g


(cm1, c0, cp1), g = zf(0.2, 1, -0.3)
close(c0, 0.893, 0.0005, "example c0"); close(cm1, -0.179, 0.0005, "c-1"); close(cp1, 0.268, 0.0005, "c1")
close(cp1 * g(1), -0.080, 0.0005, "y2"); close(cm1 * g(-1), -0.036, 0.0005, "y-2")
(cm1, c0, cp1), g = zf(0.1, 1, -0.2)
ans("zf-tap", c0, 0.0005)

# ---- matched-filter ----
Ns = 200
s = [1.0] * Ns  # amplitude 1 over T, sample spacing T/Ns
dt = 1e-6 / Ns
E = sum(v * v for v in s) * dt
h = s[::-1]
y = [sum(s[j] * h[k - j] for j in range(max(0, k - Ns + 1), min(k, Ns - 1) + 1)) * dt for k in range(2 * Ns - 1)]
close(max(y), E, 1e-12, "matched filter peak = E")
ok(y.index(max(y)) == Ns - 1, "peak at t = T")
N0 = 1e-7
noise_var = N0 / 2 * sum(v * v for v in h) * dt
ans("mf-snr", db(max(y) ** 2 / noise_var), 0.05)
close(max(y) ** 2 / noise_var, 2 * E / N0, 1e-9, "2E/N0")
close(db(2), 3.0, 0.02, "double width +3 dB")

# ---- binary-error ----
close(Q(2) * 100, 2.3, 0.05, "2.3%"); close(Q(1) * 100, 15.9, 0.05, "15.9%")
ans("q3", Q(3) / 1e-3, 0.005)
close(undb(9.6), 9.12, 0.005, "9.12"); close(sqrt(2 * 9.12), 4.27, 0.005, "4.27"); close(Q(sqrt(2 * undb(9.6))) / 1e-5, 1.0, 0.05, "1e-5")
close(undb(8), 6.31, 0.005, "6.31"); close(sqrt(2 * undb(8)), 3.55, 0.005, "3.55")
ans("polar-8db", Q(sqrt(2 * undb(8))) / 1e-4, 0.05)
ans("unipolar-db", db(2), 0.05)

# ---- binary-keying ----
ans("fsk-bw", 400 + 2 * 100)
ans("ask-bw", 2 * 1)
ok(precode([0, 1, 1, 0], 1) == [1, 0, 1, 1], "DPSK encode item")
bseq = precode([1, 0, 1, 1], 0)
ok(bseq == [1, 1, 0, 1], "DPSK example")
inv = [1 - x for x in bseq]
ref = 1
dec = []
for x in inv:
    dec.append(x ^ ref)
    ref = x
ok(dec == [1, 0, 1, 1], "inverted carrier decodes the same")

# ---- mary-qam ----
ans("psk8-rate", log2(8) * 1)
ans("qam16-rate", log2(16) * 1)
ans("qam64-rate", 10 / 1.25 * log2(64))
# 16-QAM vs 16PSK minimum distance at equal average energy 1
qam = [complex(i, q) for i in (-3, -1, 1, 3) for q in (-3, -1, 1, 3)]
es = sum(abs(z) ** 2 for z in qam) / 16
dq = 2 / sqrt(es)
dp = 2 * sin(pi / 16)
ok(dq > dp, "16-QAM points farther apart than 16PSK")
ans("msk-sep", 100 / 2)

# ---- bandpass-ber ----
ans("bpsk-10db", Q(sqrt(20)) / 1e-6, 0.05)
close(undb(12.6), 18.2, 0.05, "18.2")
ans("cfsk-126", Q(sqrt(undb(12.6))) / 1e-5, 0.05)
ans("dpsk-10db", 0.5 * exp(-10) / 1e-5, 0.005)
ans("ncfsk-10db", 0.5 * exp(-5) / 1e-3, 0.005)
ok(Q(sqrt(20)) < 0.5 * exp(-10) < 0.5 * exp(-5), "ranking at 10 dB")
close(0.5 * exp(-5) / Q(sqrt(20)), 870, 30, "almost a thousand times")

# ---- compare-systems ----
ans("qpsk-96", Q(sqrt(2 * undb(9.6))) / 1e-5, 0.05)
ans("qpsk-eff", 2 / 1.25)
need = lambda f: db(f)
x_d = log(1 / (2 * 1e-5))
close(x_d, 10.82, 0.005, "ln 5e4")
ans("dpsk-need", db(x_d), 0.05)
close(db(2 * x_d), 13.4, 0.05, "NC-FSK about 13.4 dB")
# BPSK needs 9.6 dB, coherent FSK 12.6 dB at 1e-5
lo_, hi_ = 0.1, 30.0
for _ in range(100):
    mid = (lo_ + hi_) / 2
    if Q(sqrt(2 * mid)) > 1e-5:
        lo_ = mid
    else:
        hi_ = mid
close(db(lo_), 9.6, 0.05, "BPSK 9.6 dB"); close(db(2 * lo_), 12.6, 0.05, "coherent FSK 12.6 dB")
close(db(x_d) - db(lo_), 0.7, 0.1, "DPSK about 0.7 dB worse")

# ---- error-control ----
ans("even-parity", sum([1, 0, 1, 1, 0, 0, 1]) % 2)
hd = lambda a, b: sum(x != y for x, y in zip(a, b))
ans("ham-dist", hd("1011101", "1001001"))
ans("dmin5", (5 - 1) // 2)
close(4 / 7, 0.571, 0.0005, "code rate 4/7")

# ---- linear-block ----
def ham_enc(d1, d2, d3, d4):
    return [d1, d2, d3, d4, d1 ^ d3 ^ d4, d1 ^ d2 ^ d3, d2 ^ d3 ^ d4]


words = [ham_enc(*bits) for bits in itertools.product([0, 1], repeat=4)]
ok(len({tuple(w) for w in words}) == 16, "16 codewords")
ok(min(hd(a, b) for a, b in itertools.combinations(words, 2)) == 3, "d_min = 3")
ok(ham_enc(1, 0, 1, 1) == [1, 0, 1, 1, 1, 0, 0], "example 1011100")
texts["hamming-enc"] = "".join(map(str, ham_enc(0, 1, 1, 0)))


def syndrome(r):
    p = ham_enc(*r[:4])[4:]
    return tuple(a ^ b for a, b in zip(p, r[4:]))


cols = {}
for pos in range(7):
    e = [0] * 7
    e[pos] = 1
    cols[syndrome(e)] = pos + 1
ok(len(cols) == 7 and (0, 0, 0) not in cols, "7 distinct non-zero syndromes")
ok(syndrome([1, 0, 1, 1, 1, 0, 0]) == (0, 0, 0), "codeword syndrome 0")
ok(syndrome([1, 0, 0, 1, 1, 0, 0]) == (1, 1, 1) and cols[(1, 1, 1)] == 3, "example: d3")
ok([k for k, v in cols.items() if v == 1] == [(1, 1, 0)], "d1 column 110")
r = [1, 1, 0, 0, 0, 1, 1]
ans("syndrome-pos", cols[syndrome(r)])
r[0] ^= 1
ok(r == [0, 1, 0, 0, 0, 1, 1] and syndrome(r) == (0, 0, 0), "corrected 0100011")


def crc(m, g):
    r = list(m) + [0] * (len(g) - 1)
    for i in range(len(m)):
        if r[i]:
            for j in range(len(g)):
                r[i + j] ^= g[j]
    return r[-(len(g) - 1):]


ok(crc([1, 1, 0, 1], [1, 0, 1, 1]) == [0, 0, 1], "example remainder 001")
full = [1, 1, 0, 1, 0, 0, 1]
rem = list(full)
for i in range(4):
    if rem[i]:
        for j, gb in enumerate([1, 0, 1, 1]):
            rem[i + j] ^= gb
ok(rem[-3:] == [0, 0, 0], "1101001 divides evenly")
texts["crc-rem"] = "".join(map(str, crc([1, 0, 0, 1], [1, 0, 1, 1])))

# ---- convolutional ----
def conv(u):
    s1 = s2 = 0
    out = []
    for x in u:
        out += [x ^ s1 ^ s2, x ^ s2]
        s1, s2 = x, s1
    return out


ok(conv([1, 0, 1, 1]) == [1, 1, 1, 0, 0, 0, 0, 1], "example 11 10 00 01")
texts["conv-enc"] = "".join(map(str, conv([1, 1])))
rx = [1, 1, 1, 1, 0, 0, 0, 1]
dist = {u: hd(conv(list(u)), rx) for u in itertools.product([0, 1], repeat=4)}
best = min(dist.values())
winners = [u for u, v in dist.items() if v == best]
ok(winners == [(1, 0, 1, 1)] and best == 1, "ML (Viterbi) decode 1011")
ok(dist[(1, 1, 1, 1)] == 4 and dist[(1, 0, 0, 1)] == 4, "why texts: distances 4 and 4")
ok(conv([1, 1, 1, 1]) == [1, 1, 0, 1, 1, 0, 1, 0] and conv([1, 0, 0, 1]) == [1, 1, 1, 0, 1, 1, 1, 1], "why texts: codewords")
free = min(sum(conv(list(u) + [0, 0])) for k in range(1, 8) for u in itertools.product([0, 1], repeat=k) if u[0] == 1)
ok(free == 5, "free distance 5")
ok(2 ** (3 - 1) == 4, "4 states")
ans("k7-states", 2 ** (7 - 1))

# ---- carrier-sync ----
for th in (0.3, 1.1):
    for sgn in (1, -1):
        close((sgn * cos(th)) ** 2, 0.5 * (1 + cos(2 * th)), 1e-12, "squaring removes the sign")
ans("mpsk-ambig", 360 / 4)
ans("synth-out", 3600 * 25e3 / 1e6)
ans("synth-n", round(935.2e6 / 200e3))
close(935.2e6 / 200e3, 4676, 1e-9, "exact N")

# ---- symbol-frame-sync ----
tri = lambda t: max(0.0, 1 - abs(t))  # matched-filter output for a rectangular pulse, peak at 0
est = 0.2  # estimate is late
ok(tri(est - 0.3) > tri(est + 0.3), "late estimate: early gate larger -> move earlier")
bk = [1, 1, 1, -1, -1, 1, -1]
acf = [sum(a * b for a, b in zip(bk[k:], bk)) for k in range(7)]
ok(all(abs(v) <= 1 for v in acf[1:]), "Barker sidelobes <= 1")
ans("barker-peak", acf[0])
ans("false-sync", 100 / 2 ** 7, 0.005)

# ---- boss ----
ans("b-capacity", 4000 * log2(101) / 1e3, 0.05)
ans("b-ktb", db(kT * 1e5 * 1e3), 0.5)
ans("b-carson", 2 * (25 + 5))
ans("b-am-power", 0.5 ** 2 / 2 * 400)
ans("b-pcm", 6.02 * 10 + 1.76, 0.05)
ans("b-nyquist", 2 * 3000 / 1.5)
ans("b-qam", log2(64) * 2)
close(undb(7), 5.01, 0.005, "5.01"); close(sqrt(2 * undb(7)), 3.17, 0.005, "3.17")
ans("b-bpsk", Q(sqrt(2 * undb(7))) / 1e-4, 0.05)
ans("b-hamming", (7 - 1) // 2)

# ---- compare with the pack ----
pack = Path(__file__).resolve().parents[2] / "data" / "content" / "E.2.3.yaml"
text = pack.read_text(encoding="utf-8")
pairs = re.findall(r"^\s*-?\s*id: ([a-z0-9-]+)\n(?:(?!^\s*-?\s*id: ).*\n)*?\s*answer: ([-0-9.e]+)", text, re.M)
answers = {i: float(a) for i, a in pairs}
missing = [i for i in computed if i not in answers]
assert not missing, f"computed but not in the pack: {missing}"
unchecked = [i for i in answers if i not in computed]
assert not unchecked, f"number answers in the pack without a check here: {unchecked}"
tols = dict(re.findall(r"^\s*-?\s*id: ([a-z0-9-]+)\n(?:(?!^\s*-?\s*id: ).*\n)*?\s*tolerance: ([0-9.e-]+)", text, re.M))
for i, (val, tol) in computed.items():
    pa = answers[i]
    if abs(pa - val) > max(tol, 1e-9 * max(1, abs(val))):
        raise AssertionError(f"{i}: pack answer {pa} but computed {val}")
    if i in tols:
        ok(abs(pa - val) <= float(tols[i]), f"{i}: computed value inside the pack tolerance")
    checks += 1
tpairs = dict(re.findall(r"^\s*-?\s*id: ([a-z0-9-]+)\n(?:(?!^\s*-?\s*id: ).*\n)*?\s*answers: \['([^']*)'\]", text, re.M))
assert set(tpairs) == set(texts), (sorted(tpairs), sorted(texts))
for i, v in texts.items():
    ok(tpairs[i] == v, f"{i}: text answer {tpairs[i]} vs {v}")

print(f"E.2.3 verify.py: all {checks} checks passed ({len(answers)} number answers, {len(texts)} text answers in the pack).")
