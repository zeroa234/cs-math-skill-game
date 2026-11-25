"""E.3.1 电力电子技术 — every number in data/content/E.3.1.yaml, recomputed.

Run: python -I tests/content/E.3.1.verify.py
Plain Python. Rectifier averages, harmonics and power factors by numerical integration of the waveforms;
the commutation overlap by integrating the source voltage over the inductance; the DCM buck ratio by a
cycle-by-cycle simulation of the ideal circuit until steady state; the quasi-square, six-step and sine-
triangle PWM spectra by numerical Fourier integrals; SVPWM by min-max injection and the dwell-time
vector sum; the rest (converters, resonant tank, models, magnetics) from the formulas taught.
Number answers are read back from the YAML and compared with the values computed here.
"""
import cmath
import math
import re
from math import acos, asin, cos, degrees, log10, pi, radians, sin, sqrt
from pathlib import Path

checks = 0
computed = {}
MU0 = 4 * pi * 1e-7
W50 = 2 * pi * 50


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


def avg(f, a=0.0, b=2 * pi, n=200000):
    h = (b - a) / n
    return sum(f(a + (k + 0.5) * h) for k in range(n)) * h / (b - a)


def fourier(f, n, N=200000):
    """Amplitude of the n-th harmonic of a 2*pi-periodic f (sine and cosine parts)."""
    h = 2 * pi / N
    a = b = 0.0
    for k in range(N):
        t = (k + 0.5) * h
        v = f(t)
        a += v * cos(n * t)
        b += v * sin(n * t)
    return math.hypot(a, b) * h / pi


def rms(f, N=200000):
    return sqrt(avg(lambda t: f(t) ** 2, n=N))


# ==== 为什么用开关 ====
close((12 - 5) * 2, 14, what="linear regulator 14 W")
close(5 / 12, 0.4167, 0.001, "42 % efficiency")
ans("linear-loss", (48 - 12) * 5)
close(100 / 0.95, 105.3, 0.0005, "P_in 105.3 W")
close(100 / 0.95 - 100, 5.26, 0.002, "loss about 5.3 W")
ans("efficiency-loss", 240 / 0.96 - 240)
ans("transformer-frequency", 50 / 50e3)

# ==== 二极管和 MOSFET ====
ans("diode-loss", 0.8 * 10 * 0.4)
ans("qrr-loss", 100e-9 * 400 * 100e3)
close(10 * sqrt(0.5), 7.07, 0.001, "I_rms 7.07")
close(100 * 0.5 * 0.02, 1.0, what="example 1 W")
close(5 ** 2 * 0.02, 0.5, what="mean-current mistake 0.5 W")
ans("mosfet-conduction", 20 ** 2 * 0.3 * 0.01)
close(2 ** 2.5, 5.7, 0.01, "2^2.5 = 5.7")
ans("voltage-scaling", 4 ** 2.5)

# ==== IGBT、晶闸管和宽禁带 ====
ans("igbt-vs-mosfet", 2 / 0.05)
close(0.05 * 10 ** 2, 5, what="MOSFET 5 W at 10 A")
close(2 * 10, 20, what="IGBT 20 W at 10 A")


def sw_energy(V, I, t_on, t_off, n=100000):
    """Clamped inductive switching: current ramps at full voltage, then voltage ramps at full current."""
    e = 0.0
    for t_tr in (t_on, t_off):
        h = t_tr / n
        for k in range(n):
            x = (k + 0.5) / n  # fraction of the whole transition
            if x < 0.5:  # first half: one quantity ramps while the other is full
                e += V * I * (2 * x) * h
            else:
                e += V * I * (2 - 2 * x) * h
    return e


E = sw_energy(400, 10, 50e-9, 50e-9)
close(E, 0.5 * 400 * 10 * 100e-9, 1e-6, "triangle area 1/2 VIt")
close(E, 0.2e-3, 1e-6, "0.2 mJ")
close(E * 50e3, 10, 1e-6, "10 W")
ans("switching-loss", 0.5 * 600 * 20 * 200e-9 * 20e3)

# ==== 二极管整流 ====
V = 220
half = avg(lambda t: max(0.0, sqrt(2) * V * sin(t)))
full = avg(lambda t: abs(sqrt(2) * V * sin(t)))
close(half, sqrt(2) * V / pi, 1e-6, "half-wave average")
close(full, 2 * sqrt(2) * V / pi, 1e-6, "full-wave average")
close(sqrt(2) / pi, 0.45, 0.001, "0.45")
close(2 * sqrt(2) / pi, 0.9, 0.001, "0.9")
close(full, 198, 0.0005, "198 V")
ans("half-wave", sqrt(2) * 220 / pi, 0.05)
ans("full-wave", 2 * sqrt(2) * 380 / pi, 0.5)
close(rms(lambda t: abs(sqrt(2) * V * sin(t))), 220, 1e-6, "rectified rms = 220")
ans("rectified-power", 220 ** 2 / 100)
close(198 ** 2 / 100, 392, 0.001, "wrong 392 W")
ans("diode-piv", sqrt(2) * 220, 0.5)

# ==== 功率因数和谐波 ====
ans("sine-power", 220 * 10 * cos(radians(30)), 0.5)
sq = lambda t: 1.0 if (t % (2 * pi)) < pi else -1.0
for n, expect in ((1, 4 / pi), (3, 4 / (3 * pi)), (5, 4 / (5 * pi)), (2, 0.0)):
    close(fourier(sq, n), expect, 1e-4, f"square wave harmonic {n}")
ans("fifth-harmonic", (4 / (5 * pi)) / (4 / pi))
I1 = 4 / (sqrt(2) * pi)
close(I1, 0.900, 0.0005, "I1 = 0.900 Id")
close(rms(sq), 1, 1e-9, "square rms")
thd_sq = sqrt(1 - I1 ** 2) / I1
close(thd_sq, 0.483, 0.0005, "THD 48.3 %")
ans("pf-product", 0.95 * 0.8)
ans("thd-from-df", sqrt((pi / 3) ** 2 - 1), 0.005)
# three-phase bridge current: +Id for 120 deg, 0, -Id for 120 deg, 0
q120 = lambda t: 1.0 if radians(30) <= (t % (2 * pi)) < radians(150) else (-1.0 if radians(210) <= (t % (2 * pi)) < radians(330) else 0.0)
df3 = fourier(q120, 1) / sqrt(2) / rms(q120)
close(df3, 3 / pi, 1e-4, "six-pulse distortion factor 3/pi")
close(sqrt(1 / df3 ** 2 - 1), 0.31, 0.005, "THD about 31 %")
for n in (3, 9, 2, 4):
    close(fourier(q120, n), 0, 1e-4, f"no {n}th harmonic in the 120-deg wave")
ok(fourier(q120, 5) > 0.1 and fourier(q120, 7) > 0.1, "5th and 7th present")
# neutral: third harmonics add, fifth cancel
s3 = sum(cmath.exp(1j * 3 * k * 2 * pi / 3) for k in range(3))
s5 = sum(cmath.exp(-1j * 5 * k * 2 * pi / 3) for k in range(3))
close(abs(s3), 3, 1e-12, "3rd harmonics add in neutral")
close(abs(s5), 0, 1e-12, "5th harmonics cancel in neutral")

# ==== 晶闸管相控整流 ====
ha = lambda a: avg(lambda t: sqrt(2) * V * sin(t) if radians(a) <= t <= pi else 0.0)
close(ha(90), 0.45 * 220 * 0.5, 0.002, "half-wave alpha formula")
close(ha(90), sqrt(2) * 220 / pi * 0.5, 1e-5, "half-wave alpha exact")
ans("half-wave-alpha", sqrt(2) * 220 / pi * (1 + cos(radians(90))) / 2, 0.5)
br = lambda a: avg(lambda t: abs(sqrt(2) * V * sin(t)) if radians(a) <= (t % pi) else 0.0)
close(br(45), 2 * sqrt(2) * 220 / pi * (1 + cos(radians(45))) / 2, 1e-5, "bridge R-load formula")
ans("bridge-r-load", 2 * sqrt(2) * 220 / pi * (1 + cos(radians(45))) / 2, 0.5)
close(0.9 * 220 * (1 + cos(radians(45))) / 2, 169, 0.0005, "0.9-coefficient also 169")
bl = lambda a: avg(lambda t: sqrt(2) * V * sin(t), radians(a), radians(a) + pi)
close(bl(60), 2 * sqrt(2) * 220 / pi * cos(radians(60)), 1e-6, "bridge L-load 0.9 V cos a")
ans("bridge-l-load", 2 * sqrt(2) * 220 / pi * cos(radians(60)), 0.5)
close(round(2 * sqrt(2) * 220 / pi * 0.75), 149, what="R-load at 60 deg about 149")
ans("inversion-voltage", 2 * sqrt(2) * 220 / pi * cos(radians(120)), 0.5)
acv = lambda a: sqrt(avg(lambda t: (sqrt(2) * V * sin(t)) ** 2 if radians(a) <= (t % pi) else 0.0))
for a_ in (30, 90, 135):
    close(acv(a_), V * sqrt(1 - radians(a_) / pi + sin(2 * radians(a_)) / (2 * pi)), 1e-5, f"AC controller rms at {a_}")
ans("ac-controller", 220 * sqrt(1 - 0.5 + 0), 0.5)

# ==== 换流重叠 ====
Ls, Id = 1e-3, 20
k = 2 * W50 * Ls * Id / (sqrt(2) * V)
close(2 * W50 * Ls * Id, 12.57, 0.0005, "2 w Ls Id = 12.57")
close(k, 0.0404, 0.001, "k = 0.0404")
mu0 = degrees(acos(1 - k))
close(mu0, 16.3, 0.003, "overlap 16.3 deg")
# integrate: current change over the overlap = 2 Id
h = radians(mu0) / 100000
dI = sum(sqrt(2) * V * sin((j + 0.5) * h) for j in range(100000)) * h / (W50 * Ls)
close(dI, 2 * Id, 1e-6, "overlap integral moves 2 Id")
dV = 2 * W50 * Ls * Id / pi
close(dV, 4.0, 1e-9, "commutation drop 4.0 V")
# average of the output with zero during overlap
outw = lambda t: 0.0 if (t % pi) < radians(mu0) else abs(sqrt(2) * V * sin(t))
close(full - avg(outw), dV, 1e-4, "drop by waveform")
close(full - dV, 194, 0.0005, "about 194 V")
ans("commutation-drop", 2 * W50 * 2e-3 * 15 / pi, 0.05)
mus = {a: degrees(acos(cos(radians(a)) - k)) - a for a in (0, 30, 60, 90, 120, 150)}
ok(min(mus, key=mus.get) == 90, "overlap smallest near 90 deg")
ans("overlap-at-150", mus[150], 0.05)
close(150 + mus[150], 155.0, 0.0005, "alpha + mu = 155.0")
ans("max-firing-angle", 180 - 15 - 18)

# ==== 三相整流 ====
close(380 / 220, sqrt(3), 0.005, "380/220 = sqrt3 (rounded voltages)")
ans("line-voltage", 230 * sqrt(3), 0.5)
VLL = 380
envelope = lambda t: max(sqrt(2) * VLL * sin(t + p) for p in (0, 2 * pi / 3, 4 * pi / 3, pi, pi + 2 * pi / 3, pi + 4 * pi / 3))
close(avg(envelope), 3 * sqrt(2) / pi * VLL, 1e-5, "six-pulse average")
close(3 * sqrt(2) / pi, 1.35, 0.001, "1.35")
ans("three-phase-bridge", 3 * sqrt(2) / pi * 380, 0.5)
ans("six-pulse-ripple", 6 * 50)
ans("three-phase-alpha", 3 * sqrt(2) / pi * 380 * cos(radians(30)), 0.5)
ans("three-phase-commutation", 3 * W50 * 0.5e-3 * 100 / pi, 0.5)
# balanced three-phase power is constant
pt = [sum(sqrt(2) * 220 * sin(t - p) * sqrt(2) * 10 * sin(t - p - 0.5) for p in (0, 2 * pi / 3, 4 * pi / 3)) for t in (0.1, 1.0, 2.3, 4.0)]
ok(max(pt) - min(pt) < 1e-9, "three-phase instantaneous power constant")

# ==== Buck ====
ans("buck-duty", 5 / 24, 0.0005)
D = 5 / 12
T = 1 / 200e3
close(D * T * 1e6, 2.08, 0.002, "on time 2.08 us")
dI_ex = (12 - 5) * D * T / 22e-6
close(dI_ex, 0.66, 0.005, "ripple 0.66 A")
close(5 * (1 - D) * T / 22e-6, dI_ex, 1e-12, "same from off interval")
ans("buck-ripple", (24 - 12) * 0.5 * 10e-6 / 30e-6)
ans("buck-voltage-ripple", 0.66 / (8 * 200e3 * 100e-6) * 1e3, 0.05)
ans("buck-peak-current", 3 + 0.66 / 2, 0.005)
# 1/(8fC) from the triangle charge
close((0.5 * (T / 2) * (dI_ex / 2)) / 100e-6, dI_ex / (8 * 200e3 * 100e-6), 1e-12, "triangle charge")

# ==== Boost、Buck-Boost ====
ans("boost-duty", 1 - 5 / 12, 0.0005)
ans("boost-inductor-current", 60 / 12)
close(60 / 48, 5 * (1 - 0.75), 1e-12, "output current 1.25 A")
ans("buckboost-output", -0.6 / 0.4 * 12)

# ==== 断续导通 ====
ans("dcm-boundary", dI_ex / 2, 0.0005)
M = lambda D, K: 2 / (1 + sqrt(1 + 4 * K / D ** 2))
close(M(0.3, 0.1), 0.6, 1e-12, "M = 0.6")
ans("dcm-ratio", M(0.3, 0.1))
K2 = 2 * 22e-6 * 200e3 / 44
close(K2, 0.2, 1e-12, "K = 0.2")
ans("dcm-output", 12 * M(0.4, K2), 0.005)


def sim_buck_dcm(Vin, L, C, R, D, f, cycles=4000, steps=400):
    """Ideal buck with a diode, explicit simulation of i_L and v_C; returns the mean output in the last cycles."""
    T = 1 / f
    h = T / steps
    i = v = 0.0
    acc = 0.0
    nacc = 0
    for c in range(cycles):
        for s in range(steps):
            on = s < D * steps
            vl = (Vin - v) if on else -v
            if not on and i <= 0 and vl < 0:
                vl, i = 0.0, 0.0
            i = max(0.0, i + vl / L * h) if not on else i + vl / L * h
            v += (i - v / R) / C * h
            if c >= cycles - 50:
                acc += v
                nacc += 1
    return acc / nacc


vsim = sim_buck_dcm(12, 22e-6, 100e-6, 44, 0.4, 200e3)
close(vsim, 12 * M(0.4, K2), 0.01, "DCM simulation matches M")
ok(abs(vsim - 4.8) > 1.5, "DCM output far above D*Vin")

# ==== 隔离型 ====
ans("forward-output", 48 / 4 * 0.4)
ans("forward-stress", 2 * 75)
ans("flyback-turns", 0.4 / 0.6 * 360 / 12)
close(5 / 311, 0.016, 0.01, "duty 1.6 % without a transformer")

# ==== 单相逆变器 ====
close(4 / pi / sqrt(2), 0.9, 0.001, "square fundamental rms 0.9 Vdc")
ans("square-fundamental", 4 * 300 / pi / sqrt(2), 0.5)


def quasi(alpha_deg):
    a = radians(alpha_deg)
    return lambda t: 1.0 if a <= (t % (2 * pi)) < pi - a else (-1.0 if pi + a <= (t % (2 * pi)) < 2 * pi - a else 0.0)


for n in (1, 3, 5, 7):
    close(fourier(quasi(30), n), 4 / (n * pi) * abs(cos(n * radians(30))), 1e-4, f"quasi-square harmonic {n}")
close(fourier(quasi(30), 3), 0, 1e-4, "3rd eliminated at 30 deg")
close(fourier(quasi(18), 5), 0, 1e-4, "5th eliminated at 18 deg")
ans("quasi-square", 4 * 400 / pi * cos(radians(30)), 0.5)
ans("eliminate-fifth", 90 / 5)
# single-phase power pulsation identity
for t in (0.2, 1.3, 2.9):
    vv, ii, phi = sqrt(2) * 230 * sin(t), sqrt(2) * 10 * sin(t - 0.4), 0.4
    close(vv * ii, 230 * 10 * cos(phi) - 230 * 10 * cos(2 * t - phi), 1e-9, "p(t) identity")
# capacitor energy swing P/w and C
C_ex = 3000 / (W50 * 400 * 20)
close(round(C_ex * 1e3, 2), 1.19, what="1.19 mF")
emax = max(-3000 / (2 * W50) * sin(2 * W50 * t) for t in [j * 1e-5 for j in range(2000)])
emin = min(-3000 / (2 * W50) * sin(2 * W50 * t) for t in [j * 1e-5 for j in range(2000)])
close(emax - emin, 3000 / W50, 1e-6, "energy swing P/w")
ans("dc-link-capacitor", 2400 / (W50 * 400 * 12) * 1e6, 1)

# ==== 三相逆变器 ====
leg = lambda t, p: 1.0 if ((t - p) % (2 * pi)) < pi else 0.0
line = lambda t: leg(t, 0) - leg(t, 2 * pi / 3)
close(fourier(line, 1), 4 / pi * cos(radians(30)), 1e-4, "six-step line = quasi-square 30")
close(fourier(line, 1) / sqrt(2), sqrt(6) / pi, 1e-4, "0.78 Vdc")
close(fourier(line, 3), 0, 1e-4, "no 3rd in six-step line")
ok(fourier(line, 5) > 0.1, "5th present in six-step line")
ans("six-step", sqrt(6) / pi * 540, 0.5)
ans("cascaded-levels", 2 * 5 + 1)
ans("npc-stress", 3000 / 2)
states = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
close(len(states), 8, what="8 states")

# ==== SPWM ====
ans("spwm-full-bridge", 0.8 * 400 / sqrt(2), 0.5)
ans("spwm-half-bridge", 0.9 * 600 / 2)
ans("unipolar-harmonics", 2 * 10)


def spwm_half(m, mf=21, N=200000):
    """Naturally sampled half-bridge sine-triangle PWM, output +-1 (units of Vdc/2)."""
    def f(t):
        x = (t * mf / (2 * pi)) % 1.0
        tri = 4 * x - 1 if x < 0.5 else 3 - 4 * x
        return 1.0 if m * sin(t) > tri else -1.0
    return f


close(fourier(spwm_half(0.8), 1, 400000), 0.8, 0.01, "SPWM fundamental = m (half-bridge, Vdc/2 units)")
ok(fourier(spwm_half(1.6), 1, 400000) < 1.6 and fourier(spwm_half(1.6), 1, 400000) <= 4 / pi + 0.01, "overmodulation: fundamental below m, at most 4/pi")
ok(fourier(spwm_half(1.6), 3, 400000) > 5 * fourier(spwm_half(0.8), 3, 400000), "overmodulation brings a 3rd harmonic")
close(sqrt(3) / 2 / sqrt(2), 0.612, 0.001, "0.612")
ans("three-phase-spwm", sqrt(3) / 2 * 600 / sqrt(2), 0.5)
ans("dead-time-error", 1e-6 * 10e3 * 600)
ans("she-angles", 5 - 1)

# ==== SVPWM ====
vecs = []
for a, b, c in states:
    va, vb, vc = a * 1.0, b * 1.0, c * 1.0
    vecs.append(2 / 3 * (va + vb * cmath.exp(2j * pi / 3) + vc * cmath.exp(4j * pi / 3)))
mags = sorted(abs(x) for x in vecs)
close(mags[0], 0, 1e-12, "zero vector")
close(mags[1], 0, 1e-12, "second zero vector")
for x in mags[2:]:
    close(x, 2 / 3, 1e-12, "active vector length 2/3 Vdc")
close(2 / 3 * cos(radians(30)), 1 / sqrt(3), 1e-12, "inscribed radius Vdc/sqrt3")
# min-max injection: phase amplitude Vdc/sqrt3 keeps all legs inside [0, Vdc]
A = 1 / sqrt(3)
worst = 0.0
for j in range(3600):
    t = 2 * pi * j / 3600
    ph = [A * sin(t - p) for p in (0, 2 * pi / 3, 4 * pi / 3)]
    off = -(max(ph) + min(ph)) / 2
    worst = max(worst, max(abs(x + off) for x in ph))
close(worst, 0.5, 1e-6, "SVPWM legs stay within +-Vdc/2")
close(A * sqrt(3), 1, 1e-12, "line amplitude = Vdc")
close(2 / sqrt(3) - 1, 0.155, 0.001, "15.5 %")
ans("svpwm-gain", 2 / sqrt(3), 0.0005)
ans("svpwm-max-line", 700 / sqrt(2), 0.5)
# dwell times: T1 V1 + T2 V2 = Ts Vref
m_ex = sqrt(3) * 200 / 600
T1, T2 = 100 * m_ex * sin(radians(40)), 100 * m_ex * sin(radians(20))
close(m_ex, 0.577, 0.001, "m = 0.577")
close(T1, 37.1, 0.002, "T1 37.1")
close(T2, 19.7, 0.003, "T2 19.7")
close(100 - T1 - T2, 43.1, 0.002, "T0 43.1")
v1, v2 = 2 / 3 * 600, 2 / 3 * 600 * cmath.exp(1j * pi / 3)
close(abs(T1 * v1 + T2 * v2 - 100 * 200 * cmath.exp(1j * radians(20))), 0, 1e-9, "dwell vector sum")
m2 = sqrt(3) * 300 / 600
t12 = 100 * m2 * sin(radians(30))
close(abs(t12 * v1 + t12 * v2 - 100 * 300 * cmath.exp(1j * radians(30))), 0, 1e-9, "30 deg dwell vector sum")
ans("svpwm-zero-time", 100 - 2 * t12, 0.05)
ans("pwm-rectifier-vdc", 380 * sqrt(2), 0.5)
close(round(380 * sqrt(2) / (sqrt(3) / 2)), 621, what="SPWM needs 621 V")

# ==== 缓冲电路 ====
close(100e-9 * 20 / 50e-9, 40, 1e-12, "guess 40 V")
ans("stray-spike", 30e-9 * 30 / 20e-9)
Cs = 10 * 100e-9 / (2 * 400)
tf = 100e-9
vcap = sum(10 * ((j + 0.5) / 10000) for j in range(10000)) * (tf / 10000) / Cs
close(vcap, 400, 1e-6, "snubber cap reaches V at t_f")
ans("snubber-capacitor", Cs * 1e9, 0.005)
ans("snubber-loss", 0.5 * 1.25e-9 * 400 ** 2 * 50e3)
ans("turn-on-snubber-loss", 0.5 * 1e-6 * 20 ** 2 * 20e3)

# ==== 谐振和软开关 ====
ans("coss-loss", 0.5 * 200e-12 * 400 ** 2 * 100e3)
L_, C_ = 100e-6, 25.3e-9
f0 = 1 / (2 * pi * sqrt(L_ * C_))
close(sqrt(L_ * C_), 1.591e-6, 0.001, "sqrt(LC)")
close(f0 / 1e3, 100.1, 0.001, "100.1 kHz")
ans("resonant-frequency", f0 / 1e3, 0.5)
Z0 = sqrt(L_ / C_)
close(Z0, 62.9, 0.001, "Z0 62.9")
ans("quality-factor", Z0 / 10, 0.005)
Zs = lambda f: 10 + 1j * (2 * pi * f * L_ - 1 / (2 * pi * f * C_))
ok(cmath.phase(Zs(1.2 * f0)) > 0 and cmath.phase(Zs(0.8 * f0)) < 0, "inductive above, capacitive below resonance")
close(abs(Zs(f0)), 10, 1e-6, "impedance R at resonance")

# ==== 平均模型 ====
ans("state-count", 2 + 2)
ans("averaged-steady-state", 0.4 * 12 / 2)
ans("averaged-input-current", 0.4 * 3)
close(12 * 1.2, 4.8 * 3, 1e-12, "power balance 14.4 W")
for Dx in (0.3, 0.5, 0.7):  # Boost averaged equation steady state
    close(12 / (1 - Dx) * (1 - Dx), 12, 1e-12, "boost averaged steady state")
    close(Dx * 12 + (1 - Dx) * (12 - 12 / (1 - Dx)), 0, 1e-12, "boost weighted average of the two states")

# ==== 线性化 ====
ans("boost-linearize", 12 / 0.25 * 0.01, 0.005)
close(12 / 0.49 - 24, 0.49, 0.001, "exact 0.49")
f_lc = 1 / (2 * pi * sqrt(22e-6 * 100e-6))
close(sqrt(22e-6 * 100e-6), 4.69e-5, 0.001, "sqrt(LC) 4.69e-5")
ans("lc-pole", f_lc / 1e3, 0.005)
Q = 5 * sqrt(100e-6 / 22e-6)
close(sqrt(100 / 22), 2.132, 0.0005, "sqrt(100/22)")
ans("lc-q", Q, 0.05)
close(20 * log10(Q), 20.6, 0.003, "20.6 dB")
G = lambda f: 1 / (1 - (2 * pi * f) ** 2 * 22e-6 * 100e-6 + 1j * 2 * pi * f * 22e-6 / 5)
close(abs(G(f_lc)), Q, 1e-9, "peak = Q at f0")
close(abs(G(10 * f_lc)) / abs(G(f_lc * 100)), 100, 0.02, "-40 dB/decade")
wz = 10 * 0.25 / 50e-6
close(wz, 50000, 1e-12, "wz 50000")
ans("rhp-zero", wz / (2 * pi) / 1e3, 0.005)

# ==== 闭环控制 ====
ans("modulator-gain", 20 * log10(12 / 2), 0.05)
ans("crossover-limit", 300 / 5)
ans("digital-delay", 360 * 10e3 * 1.5 * 10e-6)
ans("dpwm-resolution", 12 / (100e6 / 200e3) * 1e3)
close(100e6 / 200e3, 500, 1e-12, "500 counts")
ans("b-switching-loss", 0.5 * 300 * 15 * 80e-9 * 100e3)

# ==== 磁路和电感 ====
Rc = 0.05 / (2000 * MU0 * 50e-6)
close(Rc, 3.98e5, 0.001, "reluctance 3.98e5")
ans("core-inductance", 20 ** 2 / Rc * 1e3, 0.005)
close(sqrt(22e-6 / 100e-9), 14.8, 0.003, "14.8 turns")
ans("turns-from-al", round(sqrt(22e-6 / 100e-9)))
close(15 ** 2 * 100e-9, 22.5e-6, 1e-12, "22.5 uH")
ans("volt-second-flux", 48 * 4e-6 / (10 * 50e-6), 0.0005)

# ==== 变压器和损耗 ====
ans("magnetizing-current", 48 * 4e-6 / 1e-3, 0.0005)
rho = 1.72e-8
skin = lambda f: sqrt(rho / (pi * f * MU0))
close(skin(1e5) * 1e3, 0.21, 0.01, "0.21 mm at 100 kHz")
close(skin(1e6) * 1e3, 0.066, 0.005, "0.066 mm at 1 MHz")
close(skin(1e5) / skin(1e6), sqrt(10), 1e-9, "factor sqrt10")
ans("skin-depth", skin(1e6) * 1e3, 0.0005)
ans("winding-dc-loss", 5 ** 2 * 0.02)
ans("steinmetz", 2 ** 1.5 * 0.5 ** 2.5)

# ==== 电感和变压器设计 ====
Ap_ex = 100e-6 * 10 * 9 / (0.3 * 4e6 * 0.4)
close(Ap_ex * 1e8, 1.88, 0.003, "1.88 cm^4")
close(100e-6 * 10 / (0.3 * 1.2e-4), 27.8, 0.001, "27.8 turns")
ans("area-product", 47e-6 * 6 * 5 / (0.25 * 5e6 * 0.4) * 1e8, 0.0005)
nt = 68e-6 * 5 / (0.3 * 0.8e-4)
close(nt, 14.2, 0.003, "14.2 turns")
ans("inductor-turns", math.ceil(nt))
ans("temperature-rise", 20 * (1.2 + 0.8))
ans("stored-energy", 0.5 * 22e-6 * 3 ** 2 * 1e6)
ans("gap-energy", 0.3 ** 2 / (2 * MU0) * 0.5e-3 * 50e-6 * 1e6, 0.5)
ans("transformer-turns", 400 / (4 * 100e3 * 0.1 * 1e-4))
# square wave: V for half a period swings B from -Bmax to +Bmax
close(400 * (1 / 100e3 / 2) / (100 * 1e-4), 2 * 0.1, 1e-12, "transformer swing 2 Bmax")

# ==== 结业挑战 ====
ans("b-conduction", 8 ** 2 * 0.5 * 0.025)
ans("b-phase-control", 3 * sqrt(2) / pi * 400 * cos(radians(45)), 0.5)
ans("b-power-factor", 0.9 * 0.95, 0.0005)
ans("b-buck", (48 - 12) * 0.25 * (1 / 500e3) / 10e-6, 0.05)
ans("b-boost", 1 - 12 / 48)
ans("b-dc-link", 2500 / (2 * pi * 60 * 400 * 15) * 1e6, 1)
ans("b-spwm", sqrt(3) / 2 * 0.9 * 650 / sqrt(2), 0.5)
close(sqrt(3) / 2 * 0.9 * 650, 506.6, 0.0005, "506.6 V")
ans("b-svpwm", 800 / sqrt(2), 0.5)
close(sqrt(3) / 2 / sqrt(2) * 800, 490, 0.0005, "SPWM 490 V")
ans("b-resonant", 1 / (2 * pi * sqrt(50e-6 * 50e-9)) / 1e3, 0.05)
ans("b-lc", 1 / (2 * pi * sqrt(47e-6 * 220e-6)), 0.5)
close(cmath.phase(1 - 1j) * -1, pi / 4, 1e-12, "RHP zero lags 45 deg at its frequency")
ans("b-turns", sqrt(100e-6 / 250e-9))
ans("b-skin", skin(1e5) * 1e3, 0.005)

# ---- compare with the pack ----
pack = Path(__file__).resolve().parents[2] / "data" / "content" / "E.3.1.yaml"
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

print(f"E.3.1 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
