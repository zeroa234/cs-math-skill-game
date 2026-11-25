"""H.1.5 电子测量与仪器 — every number in data/content/H.1.5.yaml, recomputed.

Run: python -I tests/content/H.1.5.verify.py
Plain Python. Statistics are recomputed from the listed readings (Grubbs critical values from the
t distribution, integrated numerically), rounding uses decimal ROUND_HALF_EVEN, the dual-slope and
successive-approximation converters are simulated, AC meter readings come from numerically integrated
waveforms, the probe divider is evaluated as a complex network, and the DDS phase accumulator is run.
Number answers are read back from the YAML and compared with the values computed here.
"""
import cmath
import math
import re
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal
from math import erf, log10, pi, sin, sqrt
from pathlib import Path

checks = 0
computed = {}


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


def mean(xs):
    return sum(xs) / len(xs)


def sdev(xs):
    m = mean(xs)
    return sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def simpson(g, a, b, n=20000):
    h = (b - a) / n
    s = g(a) + g(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * g(a + i * h)
    return s * h / 3


def t_upper(p, nu):
    """t value with upper-tail probability p for nu degrees of freedom (bisection on a Simpson CDF)."""
    c = math.gamma((nu + 1) / 2) / (sqrt(nu * pi) * math.gamma(nu / 2))
    pdf = lambda x: c * (1 + x * x / nu) ** (-(nu + 1) / 2)
    lo, hi = 0.0, 50.0
    for _ in range(80):
        mid = (lo + hi) / 2
        tail = 0.5 - simpson(pdf, 0, mid, 4000)
        lo, hi = (mid, hi) if tail > p else (lo, mid)
    return (lo + hi) / 2


def grubbs(n, alpha):
    t = t_upper(alpha / n, n - 2)
    return (n - 1) / sqrt(n) * sqrt(t * t / (n - 2 + t * t))


par = lambda a, b: a * b / (a + b)
KF_SINE = pi / (2 * sqrt(2))

# ==== 测量、计量和误差的表示 ====
ans("correction", -(10.05 - 10.00))
ans("relative-error", 3 / 200 * 100)
close(0.5 / 100 * 50, 0.25, what="0.5 级 50 V")
close(1.0 / 100 * 10, 0.1, what="1.0 级 10 V")
close(0.25 / 8 * 100, 3.1, 0.05, "3.1 %")
close(0.1 / 8 * 100, 1.25, what="1.25 %")
ans("accuracy-class", 0.5 / 100 * 300 / 100 * 100)
opts = {"1.5/20": 1.5 * 20 / 100 / 15, "0.5/100": 0.5 * 100 / 100 / 15, "1.0/50": 1.0 * 50 / 100 / 15, "2.5/15": 2.5 * 15 / 100 / 15}
ok(min(opts, key=opts.get) == "1.5/20", "choose-meter best")
close(opts["0.5/100"] * 100, 3.3, 0.05, "3.3 %")
close(opts["2.5/15"] * 100, 2.5, what="2.5 %")
close(1.5 * 20 / 100, 0.3, what="0.3 V")

# ==== 随机误差、粗大误差和系统误差 ====
ex = [2.03, 2.01, 1.99, 2.02, 2.00]
close(mean(ex), 2.010, 1e-12, "example mean")
close(sum((x - mean(ex)) ** 2 for x in ex), 0.0010, 1e-12, "example sum of squares")
close(sdev(ex), 0.0158, 0.00005, "example s")
d6 = [4.98, 5.02, 5.01, 4.99, 5.03, 4.97]
close(mean(d6), 5.000, 1e-12, "6 readings mean")
close(sum((x - mean(d6)) ** 2 for x in d6), 0.0028, 1e-12, "6 readings sum sq")
ans("std-dev", sdev(d6), 0.00005)
for k, p in ((1, 68.3), (2, 95.4), (3, 99.7)):
    close(erf(k / sqrt(2)) * 100, p, 0.05, f"normal within {k} sigma")
ans("mean-std", 0.04 / sqrt(16))
close((10 - 1) / sqrt(10), 2.85, 0.005, "max normalised residual n=10")
# the bound (n-1)/sqrt(n) is reached when one reading is off and the rest are equal
xs = [0.0] * 9 + [1.0]
close(max(abs(x - mean(xs)) for x in xs) / sdev(xs), 9 / sqrt(10), 1e-12, "bound attained")
G8, G10 = grubbs(8, 0.05), grubbs(10, 0.05)
close(G8, 2.03, 0.005, "G(8, 0.05)")
close(G10, 2.18, 0.005, "G(10, 0.05)")
g = [1.01, 1.02, 0.99, 1.00, 1.01, 0.98, 1.02, 1.00, 1.15, 0.99]
close(mean(g), 1.017, 1e-12, "Grubbs example mean")
close(sum((x - mean(g)) ** 2 for x in g), 0.02121, 1e-9, "Grubbs example sum sq")
close(sdev(g), 0.0485, 0.00005, "Grubbs example s")
close(abs(1.15 - mean(g)), 0.133, 1e-9, "residual 0.133")
r = abs(1.15 - mean(g)) / sdev(g)
close(r, 2.74, 0.005, "ratio 2.74")
ok(G10 < r < 3, "Grubbs rejects, 3-sigma does not")
close(mean([x for x in g if x != 1.15]), 1.002, 0.0005, "mean after rejection")
d8 = [5.12, 5.10, 5.11, 5.13, 5.10, 5.11, 5.25, 5.12]
close(mean(d8), 5.13, 1e-12, "8 readings mean")
close(sum((x - mean(d8)) ** 2 for x in d8), 0.0172, 1e-12, "8 readings sum sq")
close(sdev(d8), 0.0496, 0.00005, "8 readings s")
gr = max(abs(x - mean(d8)) for x in d8) / sdev(d8)
ans("grubbs-ratio", gr, 0.005)
ok(gr > G8, "5.25 rejected")

# ==== 测量不确定度 ====
ans("type-b", 0.03 / sqrt(3), 0.00005)
uA = 0.0237 / sqrt(6)
uB = 0.01 / sqrt(3)
close(uA, 0.00968, 0.000005, "example uA")
close(uB, 0.00577, 0.000005, "example uB")
uc = sqrt(uA**2 + uB**2)
close(uc, 0.0113, 0.00005, "example uc")
close(2 * uc, 0.023, 0.0005, "example U")
ans("combined", 2 * sqrt(0.004**2 + 0.003**2))
ans("propagation", sqrt((2 * 1.0) ** 2 + 0.5**2), 0.005)
ans("worst-case", 1 + 2)
close(sqrt(1 + 4), 2.2, 0.05, "RSS 2.2")

# ==== 有效数字、修约、拟合 ====
ans("sig-figs", len("2030"))
q = lambda s, e: Decimal(s).quantize(Decimal(e), rounding=ROUND_HALF_EVEN)
ok(str(q("2.345", "0.01")) == "2.34", "2.345 -> 2.34")
ok(str(Decimal("2.345").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)) == "2.35", "half-up gives 2.35")
ans("round-even", float(q("6.3750", "0.01")))
ans("round-down", float(q("0.0465", "0.001")))


def fit(x, y):
    mx, my = mean(x), mean(y)
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sum((a - mx) ** 2 for a in x)
    return my - b * mx, b


a0, b0 = fit([0, 1, 2, 3, 4], [0.1, 1.1, 1.9, 3.1, 3.9])
close(b0, 0.96, 1e-12, "fit example slope")
close(a0, 0.10, 1e-12, "fit example intercept")
a1, b1 = fit([1, 2, 3, 4], [2.1, 3.9, 6.2, 7.8])
ans("fit-slope", b1, 0.005)
close(a1, 0.15, 1e-9, "fit intercept 0.15")

# ==== 数字万用表和负载效应 ====
ans("digits", 1999 / 1000)
close(0.005 * 12.00 + 2 * 0.01, 0.08, 1e-12, "spec example")
ans("dmm-spec", 0.0005 * 15.000 + 3 * 0.001, 0.00005)
Rl = par(2e6, 10e6)
close(Rl / 1e6, 1.667, 0.0005, "2M || 10M")
close(10 * Rl / (2e6 + Rl), 4.545, 0.0005, "loading example")
close(1 - 10 * Rl / (2e6 + Rl) / 5, 0.09, 0.005, "about 9 % low")
Rl = par(500e3, 10e6)
ans("loading", 12 * Rl / (500e3 + Rl), 0.0005)
close(Rl / 1e3, 476.2, 0.05, "476.2 kOhm")
ans("ammeter", 5 / 1005 * 1e3, 0.0005)
ans("two-wire", 0.2 / 0.5 * 100)

# ==== 模-数转换 ====
def sar(vin, lsb, bits):
    code = 0
    for b in reversed(range(bits)):
        trial = code | (1 << b)
        if trial * lsb <= vin:
            code = trial
    return code


ok(sar(11.3, 1.0, 4) == 0b1011, "SAR example 1011")
ans("sar-code", sar(1.234, 0.01, 8))


def dual_slope(vin, vref, n1, f=1.0):
    # integrate vin for n1 clocks, then -vref until zero; RC and f drop out
    rc, dt = 0.37, 1 / f
    v = vin * n1 * dt / rc
    step = vref * dt / rc
    n2 = 0
    while v > step / 2:  # the comparator flips within the last clock; count to the nearest clock
        v -= step
        n2 += 1
    return n2


ok(dual_slope(1.236, 2.0, 1000) == 618, "dual-slope example 618 counts")
close(2 * 618 / 1000, 1.236, 1e-12, "dual-slope example")
ans("dual-slope", 1 * 1350 / 2000)
ok(dual_slope(0.675, 1.0, 2000) == 1350, "dual-slope 1350 counts")
for T, zero in ((0.040, True), (0.025, False), (0.010, False), (1 / 60, False)):
    vals = [simpson(lambda t: sin(2 * pi * 50 * t + ph), 0, T, 4000) for ph in (0.3, 1.1)]
    ok(all(abs(v) < 1e-9 for v in vals) == zero, f"50 Hz rejection over {T}")

# ==== 交流电压 ====
avg = lambda f, T: simpson(lambda t: abs(f(t)), 0, T, 20000) / T
rms = lambda f, T: sqrt(simpson(lambda t: f(t) ** 2, 0, T, 20000) / T)
sine = lambda t: sin(2 * pi * t)
tri = lambda t: 4 * abs((t % 1) - 0.5) - 1  # peak 1
square = lambda t: 1.0 if (t % 1) < 0.5 else -1.0
close(avg(sine, 1), 2 / pi, 1e-6, "sine avg")
close(rms(sine, 1), 1 / sqrt(2), 1e-6, "sine rms")
close(KF_SINE, 1.11, 0.005, "K_F sine")
close(sqrt(2), 1.414, 0.0005, "K_P sine")
close(avg(tri, 1), 0.5, 1e-6, "triangle avg")
close(rms(tri, 1), 1 / sqrt(3), 1e-6, "triangle rms")
ans("triangle-factors", 3 / (3 / sqrt(3)), 0.0005)
close((3 / sqrt(3)) / 1.5, 1.155, 0.0005, "triangle K_F")
close(1.11 * 0.5, 0.555, 1e-12, "triangle reading")
close((KF_SINE * 0.5 - 1 / sqrt(3)) / (1 / sqrt(3)) * 100, -3.8, 0.05, "triangle error -3.8 %")
close((KF_SINE * avg(square, 1) - rms(square, 1)) / rms(square, 1) * 100, 11, 0.1, "square +11 %")
ans("square-true-rms", 2.22 / 1.11, 0.005)
ans("triangle-reading", KF_SINE * 3, 0.005)
close(6 / sqrt(3), 3.46, 0.005, "triangle true rms 3.46")
close(sqrt(1e-3 * 600), 0.775, 0.0005, "0 dBm on 600 Ohm")
ans("dbm-600", 10 * log10(1 / 600 / 1e-3), 0.005)
ans("dbv", 20 * log10(0.1))

# ==== 示波器 ====
close(4 * 2, 8, what="example 8 Vpp")
close(1 / (5 * 1e-3), 200, what="example 200 Hz")
ans("read-scope", 1 / (4 * 20e-6) / 1e3)
# Lissajous: count tangencies numerically for fy/fx = 3/2
ts = [i / 200000 for i in range(200000)]
fx, fy = 2, 3
xs_ = [sin(2 * pi * fx * t) for t in ts]
ys_ = [sin(2 * pi * fy * t + 0.4) for t in ts]
top = sum(1 for i in range(1, len(ts) - 1) if ys_[i] > ys_[i - 1] and ys_[i] >= ys_[i + 1] and ys_[i] > 0.999)
side = sum(1 for i in range(1, len(ts) - 1) if xs_[i] > xs_[i - 1] and xs_[i] >= xs_[i + 1] and xs_[i] > 0.999)
ok(top == 3 and side == 2, f"Lissajous tangencies {top}:{side}")
ans("lissajous", 1 * 3 / 2)
close(math.degrees(math.asin(3 / 6)), 30, 1e-9, "ellipse 30 deg")

# ==== 数字示波器 ====
ans("memory-depth", 2e6 / (10 * 500e-6) / 1e6)
ok(100e6 / 80e6 < 2, "less than two samples per cycle")
close(100e6 / 80e6, 1.25, 1e-12, "1.25 samples per cycle")
# rise time constant 0.35 from a single-pole RC
RC = 1.0
close(RC * math.log(9) * (1 / (2 * pi * RC)), 0.35, 0.001, "t_r * BW = 0.35")
close(0.35 / 200e6 * 1e9, 1.75, 1e-9, "200 MHz rise time")
close(sqrt(3**2 + 1.75**2), 3.47, 0.005, "displayed 3.47 ns")
close(sqrt(3**2 + 1.75**2) / 3 - 1, 0.16, 0.005, "16 % larger")
ans("rise-time", sqrt(10**2 + (0.35 / 50e6 * 1e9) ** 2), 0.05)
R1, R2, C2 = 9e6, 1e6, 18e-12
C1 = R2 * C2 / R1
ans("probe-c1", C1 * 1e12, 1e-9)
for f in (10.0, 1e3, 1e6, 1e8):  # compensated divider is flat
    w = 2 * pi * f
    Z1 = 1 / (1 / R1 + 1j * w * C1)
    Z2 = 1 / (1 / R2 + 1j * w * C2)
    close(abs(Z2 / (Z1 + Z2)), 0.1, 1e-9, f"compensated ratio at {f} Hz")
Z1 = lambda w, c: 1 / (1 / R1 + 1j * w * c)
Z2 = lambda w: 1 / (1 / R2 + 1j * w * C2)
hf = lambda c: abs(Z2(2 * pi * 1e8) / (Z1(2 * pi * 1e8, c) + Z2(2 * pi * 1e8)))
ok(hf(3e-12) > 0.1 > hf(1e-12), "larger C1 boosts high frequencies (overshoot)")

# ==== 信号源 ====
close(4 * 100 / 150, 2.67, 0.005, "source example 2.67 Vpp")
ans("source-load", 2 * 25 / 75, 0.0005)
ans("dc-offset", 1 + 2 / 2)
ans("duty-cycle", 2 / 8 * 100)

# ==== 频率合成 ====
ans("pll-n", 101.4e6 / 25e3)
ok(101.4e6 % 25e3 == 0, "101.4 MHz on the 25 kHz grid")
M = round(1e6 * 2**32 / 50e6)
ok(M == 85899346, "DDS example M")
close(M * 50e6 / 2**32, 1000000.001, 0.0005, "DDS example actual")
close(50e6 / 2**32, 0.0116, 0.00005, "DDS example resolution")
ans("dds-resolution", 100e6 / 2**24, 0.005)
ans("dds-output", 80e6 * 2**28 / 2**32 / 1e6)
# run a 32-bit phase accumulator and count wraps over 1e-5 s (800 clocks)
acc, wraps = 0, 0
for _ in range(800):
    acc += 2**28
    if acc >= 2**32:
        acc -= 2**32
        wraps += 1
ok(wraps == 50, "accumulator wraps 50 times in 10 us -> 5 MHz")
ans("awg", 250e6 / 1000 / 1e3)

# ==== 计数器 ====
ans("cesium-period", 1 / 9192631770 * 1e9, 0.0005)
close(1 / (1e3 * 1) * 100, 0.1, what="1 kHz, 1 s gate: 0.1 %")
ans("gate-error", 1 / (50 * 1) * 100)
close(sqrt(1e7 / 1), 3162, 0.5, "mid frequency example")
ok(1e7 / 50 == 200000, "period count 200000")
close(50 / 1e7, 5e-6, 1e-15, "period method error")
ans("mid-frequency", sqrt(1e8 / 0.1) / 1e3, 0.05)
ans("timebase-error", (1 / (20e6 * 1) + 5e-8) / 1e-8)

# ==== 逻辑分析仪 ====
ans("la-sample-rate", 25e6 * 4 / 1e6)
close(1 / 100e6 * 1e9, 10, 1e-9, "10 ns interval")
ans("pre-trigger", 2000 * 0.25)

# ==== 频谱分析仪 ====
ans("dbm-50", 10 * log10(0.5**2 / 50 / 1e-3), 0.005)
k_B = 1.380649e-23
close(10 * log10(k_B * 290 / 1e-3), -174, 0.05, "kT at 290 K in dBm/Hz")
close(-174 + 10 * log10(1e4), -134, 1e-9, "RBW 10 kHz")
close(-174 + 10 * log10(1e3), -144, 1e-9, "RBW 1 kHz")
ans("noise-floor", -174 + 10 * log10(100), 0.05)
ok(300 < 1000 < 3000, "300 Hz resolves 1 kHz spacing")

# ==== 频率特性 ====
ans("gain-db", 20 * log10(2 / 0.1), 0.005)
ans("phase-shift", 25e-6 * 5e3 * 360)
ans("minus-3db", 1 / sqrt(2), 0.0005)
close(10 ** (-3 / 20), 0.708, 0.0005, "10^(-3/20)")

# ==== 阻抗 ====
Xc = lambda f, C: 1 / (2 * pi * f * C)
ans("cap-reactance", Xc(1e3, 4.7e-6), 0.05)
ans("va-method", par(50, 10000), 0.005)
close(sqrt(1 * 10000), 100, what="criterion sqrt(RA RV)")
close(50 + 1, 51, what="internal connection 51")
ans("wheatstone", 10 * 472.5)
L = 1 / ((2 * pi * 1e6) ** 2 * 253.3e-12)
ans("resonance-l", L * 1e6, 0.05)
close((2 * pi * 1e6) ** 2 * 253.3e-12, 1e4, 0.001, "1e4")
ans("esr-d", 0.5 / Xc(1e3, 22e-6), 0.0005)
close(Xc(1e3, 22e-6), 7.23, 0.005, "22 uF at 1 kHz")

# ==== 自动测试 ====
# IEEE 488: at most 15 devices on one bus including the controller (the interface card)
ans("gpib-cards", math.ceil(18 / (15 - 1)))
# bridge: equal midpoint potentials give R1*Rx = R2*R3
R1b, R2b, R3b = 100.0, 1000.0, 472.5
Rx = R2b / R1b * R3b
close(R2b / (R1b + R2b), Rx / (R3b + Rx), 1e-12, "bridge midpoints equal")

# ==== 结业挑战 ====
d = [1.002, 0.998, 1.001, 0.999, 1.003, 0.997, 1.000, 1.000]
close(mean(d), 1.000, 1e-12, "b mean")
close(sdev(d), 0.002, 1e-12, "b s")
uA, uB = sdev(d) / sqrt(8), 0.002 / sqrt(3)
close(uA, 0.000707, 0.0000005, "b uA")
close(uB, 0.001155, 0.0000005, "b uB")
close(sqrt(uA**2 + uB**2), 0.001354, 0.0000005, "b uc")
ans("b-uncertainty", 2 * sqrt(uA**2 + uB**2) * 1e3, 0.01)
ans("b-class", 0.5 / 100 * 150 / 60 * 100, 0.005)
Rl = par(1e6, 10e6)
ans("b-loading", 20 * Rl / (3e6 + Rl), 0.005)
ans("b-ac-meter", KF_SINE * 5, 0.005)
close(10 / sqrt(3), 5.77, 0.005, "b true rms")
ans("b-dual-slope", 2 * 2500 / 4000)
ans("b-rise-time", sqrt(2**2 + 3.5**2), 0.01)
ans("b-generator", 6 * 1e6 / (1e6 + 50), 0.01)
ans("b-counter", 1 / (5000 * 0.1) * 100)
ans("b-dds", 125e6 / 2**32, 0.00005)
ans("b-noise", -174 + 10 * log10(3000), 0.05)
ans("b-impedance", Xc(120, 47e-6), 0.05)
lim = 0.005 * 1.500 + 2 * 0.001
close(lim, 0.0095, 1e-12, "b-dmm limit")
uB = lim / sqrt(3)
close(uB, 0.00548, 0.000005, "b-dmm uB")
close(sqrt(0.0020**2 + uB**2), 0.00584, 0.000005, "b-dmm uc")
ans("b-dmm-uncertainty", 2 * sqrt(0.0020**2 + uB**2), 0.0001)
fm = sqrt(1e7 / 1)
ok(2000 < fm, "2 kHz below the crossover -> period method")
close(1 / 2000 * 100, 0.05, 1e-12, "frequency method 0.05 %")
ans("b-counter-method", 2000 / 1e7 * 100)
ans("b-snr", -60 - (-174 + 10 * log10(1000) + 20))

# ---- automation review 2026-11-23: worked examples and the -3 dB tolerance ----
T2k = 1 / 2000
close(T2k * 1000, 0.5, 1e-12, "phase example period 0.5 ms")
close(100e-6 / T2k, 0.2, 1e-12, "phase example 0.2 period")
close(0.2 * 360, 72, 1e-12, "phase example 72 degrees")
rel = sqrt((2 * 2) ** 2 + 1 ** 2)
close(2 * 2, 4, 1e-12, "propagation example I^2 -> 4 %")
close(rel, sqrt(17), 1e-12, "propagation example sqrt(17)")
close(rel, 4.12, 0.005, "propagation example 4.12 %")
close(25 * rel / 100, 1.03, 0.005, "propagation example 1.03 W")
close(4 + 1, 5, 1e-12, "propagation example worst case 5 %")
den = (2 * pi * 2e6) ** 2 * 63.3e-12
close(den, 9.996e3, 0.0005e3, "resonance example denominator")
close(1 / den * 1e6, 100.0, 0.05, "resonance example L = 100 uH")
close(10 ** (-3 / 20), 0.708, 0.0005, "-3 dB as 10^(-3/20)")
ok(abs(0.708 - 0.707) <= 0.0015 and abs(1 / sqrt(2) - 0.707) <= 0.0015, "minus-3db tolerance accepts 0.707 and 0.708")

# ---- compare with the pack ----
pack = Path(__file__).resolve().parents[2] / "data" / "content" / "H.1.5.yaml"
text = pack.read_text(encoding="utf-8")
pairs = re.findall(r"^\s*-?\s*id: ([a-z0-9-]+)\n(?:(?!^\s*-?\s*id: ).*\n)*?\s*answer: ([-0-9.e]+)", text, re.M)
answers = {i: float(a) for i, a in pairs}
missing = [i for i in computed if i not in answers]
assert not missing, f"computed but not in the pack: {missing}"
unchecked = [i for i in answers if i not in computed]
assert not unchecked, f"number answers in the pack without a check here: {unchecked}"
for i, (val, tol) in computed.items():
    pa = answers[i]
    if abs(pa - val) > max(tol, 1e-9 * max(1, abs(val))):
        raise AssertionError(f"{i}: pack answer {pa} but computed {val}")
    checks += 1

print(f"H.1.5 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
