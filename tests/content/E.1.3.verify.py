"""E.1.3 射频与高频电路 — every number in data/content/E.1.3.yaml, recomputed.

Run: python -I tests/content/E.1.3.verify.py [path/to/E.1.3.yaml]
Plain Python. Number answers are read back from the YAML and compared with the values computed here, so a typo in
either place fails. Closed-form results are also derived another way where that is cheap: resonance and 3 dB
bandwidth by searching |Z(f)|, the capacitive tap by the real part of the actual network's admittance, L-match and
LNA input impedance by complex arithmetic, multistage and shunt-peaking bandwidths by bisection on |H|, the 1 dB
point by solving the cubic's gain exactly, IM3 and AM sidebands by numerical Fourier integrals, class-C decomposition
coefficients by integrating the cosine pulse, Bessel functions both by their series and by integrating
cos(beta sin x), the charge-pump loop's natural frequency and damping from its characteristic polynomial, the pulse
swallow counter, a first-order fractional-N accumulator and a DDS phase accumulator by simulation.
"""
import math
import re
import sys
from math import atan, cos, degrees, exp, log10, pi, radians, sin, sqrt
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
        raise AssertionError(what)
    checks += 1


def ans(item_id, value, tol=1e-9):
    computed[item_id] = (value, tol)


def bisect(f, lo, hi, n=200):
    flo = f(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        if (f(mid) > 0) == (flo > 0):
            lo, flo = mid, f(mid)
        else:
            hi = mid
    return (lo + hi) / 2


def par(*rs):
    return 1 / sum(1 / r for r in rs)


def db(x):
    return 10 * log10(x)


def f_res(L, C):
    return 1 / (2 * pi * sqrt(L * C))


def bw3_parallel(L, C, R):
    """3 dB bandwidth of a parallel RLC found from |Z(f)| (two bisections around f0)."""
    f0 = f_res(L, C)
    Z = lambda f: abs(1 / (1 / R + 1j * 2 * pi * f * C + 1 / (1j * 2 * pi * f * L)))
    g = lambda f: Z(f) - R / sqrt(2)
    hi = bisect(g, f0, 10 * f0)
    lo = bisect(g, f0 / 10, f0)
    return hi - lo


c = 3e8
# ==== rf-intro ====
ans("wavelength", c / 100e6)
close(c / 100e6 / 4, 0.75, 1e-12, "quarter wave 0.75 m")
close(2.998e8 / 2.4e9 * 100, 12.5, 0.002, "2.4 GHz wavelength 12.5 cm")
ans("dbm-to-watt", 10 ** (-60 / 10) * 1e-3 / 1e-9)
ans("gain-dbm", -30 + 20)
close(10 ** (-30 / 10), 1e-3, 1e-12, "-30 dBm = 1 uW")
close(10 ** (-10 / 10), 0.1, 1e-12, "-10 dBm = 0.1 mW")
close(sqrt(1e-3 * 50), 0.224, 0.002, "0 dBm in 50 Ohm: 0.224 V rms")
close(sqrt(1e-3 * 50) * sqrt(2), 0.316, 0.002, "peak 0.316 V")

# ==== resonance ====
ans("inductive-reactance", round(2 * pi * 1e7 * 1e-6, 1), 0.05)
close(2 * pi * 1e8 * 1e-6, 628, 0.001, "628 Ohm at 100 MHz")
ans("series-f0", round(f_res(25e-6, 100e-12) / 1e6, 2), 0.005)
L, C, R = 10e-6, 1e-9, 5
f0 = f_res(L, C)
close(f0 / 1e6, 1.59, 0.002, "example f0")
close(sqrt(L / C), 100, 1e-9, "example w0L = sqrt(L/C)")
Q = sqrt(L / C) / R
close(Q, 20, 1e-9, "example Q")
# series current |I| = 1/|Z|; 3 dB points by bisection
Iz = lambda f: 1 / abs(R + 1j * (2 * pi * f * L - 1 / (2 * pi * f * C)))
g = lambda f: Iz(f) - (1 / R) / sqrt(2)
bw = bisect(g, f0, 10 * f0) - bisect(g, f0 / 10, f0)
close(bw / 1e3, 79.6, 0.001, "example series bandwidth 79.6 kHz")
L, C, R = 4e-6, 100e-12, 25e3
close(sqrt(L / C), 200, 1e-9, "parallel w0L 200")
ans("parallel-q", R / sqrt(L / C))
close(f_res(L, C) / 1e6, 7.96, 0.001, "7.96 MHz")
ans("parallel-bw", round(7.96e6 / 125 / 1e3, 1), 0.05)
close(bw3_parallel(L, C, R) / 1e3, 63.7, 0.002, "parallel bandwidth from |Z|")
Qc = 2 * pi * 1e7 * 2e-6 / 2
ans("series-to-parallel", round(2 * (1 + Qc**2) / 1e3, 1), 0.05)
close(Qc, 62.8, 0.001, "coil Q 62.8")
# exact series-to-parallel: admittance of r + jwL, real part
Y = 1 / (2 + 1j * 2 * pi * 1e7 * 2e-6)
close(1 / Y.real, 2 * (1 + Qc**2), 1e-9, "Rp = r(1+Q^2) exactly from the admittance")

# ==== loaded-q-tapping ====
close(par(25e3, 1e3) / 200, 4.8, 0.002, "guess: Q under 5")
ans("loaded-q", round(par(25e3, 5e3) / 200, 1), 0.05)
close(par(25e3, 1e3 / 0.2**2) / 200, 62.5, 1e-9, "example tapped Q 62.5")
ans("cap-divider", 2 / (100 / 500) ** 2)
# check the capacitive tap with the real network at resonance: C1 in series with (C2 || RL)
C1, C2, RL = 100e-12, 400e-12, 2e3
Cs = C1 * C2 / (C1 + C2)
w = 1 / sqrt(4e-6 * Cs)
Zb = 1 / (1j * w * C2 + 1 / RL)
Yin = 1 / (1 / (1j * w * C1) + Zb)
close(1 / Yin.real / 1e3, 50, 0.03, "capacitive tap: equivalent parallel resistance about 50 k")
Rl_min = 1 / (1 / 10e3 - 1 / 25e3)
pmax = sqrt(1e3 / Rl_min)
ans("max-tap", 0.24, 0.005)
ok(0.24 <= pmax < 0.245 + 1e-9 and par(25e3, 1e3 / 0.24**2) / 200 >= 50, "p = 0.24 keeps Q >= 50")

# ==== impedance-matching ====
for RL_ in (50, 200, 12.5):
    pass
P = lambda RL_: (1 / (50 + RL_)) ** 2 * RL_
ans("mismatch-power", P(200) * 1e3)
close(P(50) * 1e3, 5, 1e-9, "matched 5 mW")
close(1 - P(200) / P(50), 0.36, 1e-9, "36 % lost")
Qm = sqrt(200 / 50 - 1)
Xs, Xp = Qm * 50, 200 / Qm
close(Xs, 86.6, 0.001, "example Xs")
close(Xp, 115.5, 0.001, "example Xp")
w = 2 * pi * 100e6
Lm, Cm = Xs / w, 1 / (w * Xp)
close(Cm * 1e12, 13.8, 0.002, "example C 13.8 pF")
close(Lm * 1e9, 138, 0.002, "example L 138 nH")
Zin = 1j * w * Lm + 1 / (1 / 200 + 1j * w * Cm)
close(abs(Zin - 50), 0, 1e-9, "example L-match gives 50 Ohm")
ans("l-match-q", round(sqrt(450 / 50 - 1), 2), 0.005)
close(sqrt(8) * 50, 141, 0.005, "series 141")
close(450 / sqrt(8), 159, 0.002, "shunt 159")
G = lambda z: (z - 50) / (z + 50)
ans("reflected-power", round(abs(G(100)) ** 2 * 100, 1), 0.05)
close(abs(G(25)) ** 2, abs(G(100)) ** 2, 1e-12, "25 Ohm same reflection")

# ==== tuned-amplifier ====
ans("tuned-gain", 20e-3 * 4e3)
gbw = 20e-3 / (2 * pi * 200e-12)
ans("tuned-gbw", round(gbw / 40 / 1e3), 0.5)
close(gbw / 1e6, 15.9, 0.002, "GBW 15.9 MHz")
close(gbw / 80 / 1e3, 199, 0.003, "gain 80: 199 kHz")
# rectangle coefficient: |H| = 1/sqrt(1+x^2), x = 2Q df/f0
x01 = bisect(lambda x: 1 / sqrt(1 + x * x) - 0.1, 0, 100)
close(x01, sqrt(99), 1e-9, "K0.1 = sqrt(99)")
close(sqrt(99), 9.95, 0.001, "9.95")
close(1 / sqrt(1 + 2**2), 0.45, 0.01, "at 400 kHz width gain about 0.45")
shrink = lambda n: bisect(lambda x: (1 / sqrt(1 + x * x)) ** n - 1 / sqrt(2), 0, 1)
for n in (2, 3):
    close(shrink(n), sqrt(2 ** (1 / n) - 1), 1e-9, f"{n}-stage shrink factor")
close(200 * shrink(3), 102, 0.001, "example 3 stages 102 kHz")
close(200 / shrink(3), 392, 0.001, "example per-stage 392 kHz")
ans("two-stage-bw", round(300 * sqrt(sqrt(2) - 1)), 0.5)
k2 = bisect(lambda x: (1 / sqrt(1 + x * x)) ** 2 - 0.1, 0, 10) / shrink(2)
close(k2, 4.7, 0.01, "two-stage K0.1 about 4.7")


def bw_peaking(R, C, L):
    H = lambda f: abs((R + 1j * 2 * pi * f * L) / (1 + 1j * 2 * pi * f * R * C - (2 * pi * f) ** 2 * L * C))
    f = 1e6
    while H(f) >= R / sqrt(2):
        f *= 1.01
    return bisect(lambda x: H(x) - R / sqrt(2), f / 1.01, f)


b0 = 1 / (2 * pi * 1e3 * 0.5e-12)
bp = bw_peaking(1e3, 0.5e-12, 1e6 * 0.5e-12 / 2.41)
close(bp / b0, 1.72, 0.003, "maximally flat shunt peaking 1.72x")
ans("shunt-peaking", round(bp / 1e6), 3)
close(1e6 * 0.5e-12 / 2.41 * 1e9, 207, 0.005, "207 nH")
close(b0 / 1e6, 318, 0.002, "318 MHz")

# ==== rf-noise ====
k = 1.380649e-23
close(db(k * 290 / 1e-3), -174, 0.0002, "kT = -174 dBm/Hz")
ans("noise-floor", -174 + 60)
ans("snr-out", 30 - 4)
close((2 - 1) * 290, 290, 0, "F = 2 is 290 K")
F1, G1, F2 = 10 ** 0.2, 10 ** 1.5, 10
F = F1 + (F2 - 1) / G1
close(F, 1.870, 0.0005, "example F 1.870")
close(db(F), 2.72, 0.002, "example 2.72 dB")
# same cascade with noise temperatures
T = (F1 - 1) * 290 + (F2 - 1) * 290 / G1
close(1 + T / 290, F, 1e-12, "noise temperature cascade agrees")
ans("friis", round(db(2 + 10 / 100), 2), 0.005)
close(db(2 + 10 / 10), 4.8, 0.01, "gain 10: 4.8 dB")
Lc = 10 ** 0.2
Fc = Lc + (10 ** 0.2 - 1) * Lc
close(db(Fc), 4.0, 1e-9, "2 dB cable before a 2 dB LNA: 4 dB")
ans("sensitivity", round(-174 + 6 + 10 * log10(2e5) + 10, 1), 0.05)
close(10 * log10(2e5), 53.0, 0.0005, "53.0 dB-Hz")

# ==== nonlinearity ====
a1, a3 = 10, -1
A1db = bisect(lambda A: (a1 + 0.75 * a3 * A * A) - a1 * 10 ** (-1 / 20), 0, 3)
close(A1db, sqrt(0.145 * abs(a1 / a3)), 0.0005, "1 dB point exact vs 0.145 rule")
ans("p1db", round(sqrt(0.145 * 10), 2), 0.005)
close(10 - 0.75 * 1.2**2, 8.92, 1e-9, "gain 8.92 at 1.2 V")
close(20 * log10(8.92 / 10), -1, 0.01, "about 1 dB lower")
# IM3 amplitude by numerical Fourier integral of a3 x^3 with two tones (w1 = 2, w2 = 3 in units of a base frequency)
A = 0.1
N = 20000
s = 0.0
for i in range(N):
    t = 2 * pi * i / N
    x = A * (cos(2 * t) + cos(3 * t))
    y = a1 * x + a3 * x**3
    s += y * cos(1 * t)          # 2*w1 - w2 = 1
im3 = abs(2 * s / N)
close(im3, 0.75 * abs(a3) * A**3, 1e-6, "IM3 amplitude 3/4 a3 A^3")
Aip3 = sqrt(4 / 3 * abs(a1 / a3))
close(20 * log10(Aip3 / A1db), 9.6, 0.005, "IIP3 about 9.6 dB above P1dB")
ans("im3-freq", 2 * 100.0 - 100.2, 1e-9)
close(2 * 100.2 - 100.0, 100.4, 1e-9, "other IM3 100.4")
close(-30 + (-10 - (-70)) / 2, 0, 0, "example IIP3 0 dBm")
ans("iip3-measure", -35 + (-20 - (-70)) / 2)
inv = 1 / 1 + 10 ** 1.5 / 10 ** 0.5
ans("cascade-iip3", round(db(1 / inv), 1), 0.05)
close(inv, 11, 1e-9, "1/IIP3 = 11")
Pn = -174 + 6 + 10 * log10(2e5)
ans("sfdr", round(2 / 3 * (-10 - Pn) - 10), 0.5)
close(Pn, -115.0, 0.0001, "noise power -115.0 dBm")

# ==== lna ====
ans("resistor-match-nf", round(db(2), 1), 0.05)
wT = 2 * pi * 20e9
Ls = 50 / wT
close(Ls * 1e9, 0.40, 0.01, "example Ls 0.40 nH")
w0 = 2 * pi * 2.4e9
Lt = 1 / (w0**2 * 200e-15)
close(Lt * 1e9, 22.0, 0.001, "example Lg + Ls 22.0 nH")
close((Lt - Ls) * 1e9, 21.6, 0.001, "example Lg 21.6 nH")
gm = wT * 200e-15
Zin = 1j * w0 * Lt + 1 / (1j * w0 * 200e-15) + gm * Ls / 200e-15
close(abs(Zin - 50), 0, 1e-9, "degenerated CS input is 50 Ohm")
ans("degeneration-real", round(2 * pi * 30e9 * 0.5e-9, 1), 0.05)
close(50 / (2 * pi * 30e9) * 1e9, 0.27, 0.02, "0.27 nH for 50 Ohm")
ans("degeneration-res", round(1 / ((2 * pi * 5e9) ** 2 * 150e-15) * 1e9, 2), 0.005)
ans("cg-match", 1 / 50 * 1e3)
close(db(1 + 2 / 3), 2.2, 0.01, "CG LNA NF about 2.2 dB")

# ==== pa-classes ====
ans("pae", (1 - 0.1) / 2.5 * 100)
close(1 / 2.5 * 100, 40, 1e-9, "drain efficiency 40 %")
close(1 / 0.25, 4, 0, "guess 4 W")
close(1 / 0.6, 1.67, 0.002, "guess 1.67 W")
ans("pmax", 5**2 / (2 * 50) * 1e3)
close(25 / (2 * 1), 12.5, 1e-12, "1 W from 5 V needs 12.5 Ohm")
ans("ropt", 3.6**2 / (2 * 2))
close(50 / 3.24, 15, 0.03, "impedance ratio about 15")


def alphas(th_deg):
    th = radians(th_deg)
    a0 = (sin(th) - th * cos(th)) / (pi * (1 - cos(th)))
    a1_ = (th - sin(th) * cos(th)) / (pi * (1 - cos(th)))
    return a0, a1_


def alphas_num(th_deg, n=20000):
    th = radians(th_deg)
    s0 = s1 = 0.0
    for i in range(n):
        x = -th + 2 * th * (i + 0.5) / n
        ic = (cos(x) - cos(th)) / (1 - cos(th))
        s0 += ic
        s1 += ic * cos(x)
    return s0 * 2 * th / n / (2 * pi), s1 * 2 * th / n / pi


for th in (60, 70, 90):
    a0, a1_ = alphas(th)
    n0, n1 = alphas_num(th)
    close(a0, n0, 1e-6, f"alpha0({th}) by integration")
    close(a1_, n1, 1e-6, f"alpha1({th}) by integration")
close(alphas(90)[0], 1 / pi, 1e-12, "alpha0(90) = 1/pi")
close(alphas(90)[1], 0.5, 1e-12, "alpha1(90) = 0.5")
close(alphas(60)[1], 0.391, 0.001, "alpha1(60) 0.391")
close(alphas(60)[0], 0.218, 0.001, "alpha0(60) 0.218")
close(alphas(70)[0], 0.252, 0.002, "alpha0(70) 0.252")
close(alphas(70)[1], 0.436, 0.001, "alpha1(70) 0.436")
ans("alpha1-ratio", round(0.391 / 0.5, 2), 0.005)
close(0.782**2, 0.61, 0.003, "power about 0.61")
close(0.5 * 0.9 * 0.436 / 0.252, 0.779, 0.001, "example eta 0.779")
close(0.5 * 0.9 * pi / 2, 0.707, 0.001, "class B at xi 0.9: 70.7 %")
ans("class-c-eta", round(0.5 * alphas(60)[1] / alphas(60)[0] * 100, 1), 0.15)
close(0.5 * 0.391 / 0.218 * 100, 89.7, 0.001, "rounded coefficients also 89.7")

# ==== pa-efficiency-linearization ====
# class B: DC current of a half-sine pulse train is I/pi, fundamental I/2; eta = (1/2 xi I/2 V)/(V I/pi) = pi/4 xi
ans("backoff-eta", round(pi / 4 * 0.5 * 100, 1), 0.05)
n = 100000
env_peak = 0.0
pw = 0.0
for i in range(n):
    t = i / n
    v = cos(2 * pi * 100 * t) + cos(2 * pi * 101 * t)
    pw += v * v
pw /= n
ans("two-tone-papr", round(db((2**2 / 2) / pw), 1), 0.05)
close(pw, 1.0, 1e-6, "two unit tones: average power 1")

# ==== oscillator-principles ====
ans("min-feedback", 1 / 5)
ans("negative-r", 2)
ans("stability-drift", 1e7 * 2e-6)

# ==== three-point ====
Cx = 300e-12 * 600e-12 / 900e-12
close(Cx * 1e12, 200, 1e-9, "example series C 200 pF")
close(f_res(2e-6, Cx) / 1e6, 7.96, 0.001, "example 7.96 MHz")
Cc = 470e-12 * 1000e-12 / 1470e-12
close(Cc * 1e12, 320, 0.001, "item series C 320 pF")
ans("colpitts-f", round(f_res(3e-6, Cc) / 1e6, 2), 0.005)
ans("hartley-f", round(f_res(5e-6, 100e-12) / 1e6, 2), 0.005)
Ccl = par(1000e-12, 1000e-12, 50e-12)
close(Ccl * 1e12, 45.5, 0.002, "Clapp total 45.5 pF")
ans("clapp-f", round(f_res(10e-6, Ccl) / 1e6, 2), 0.005)
close(f_res(10e-6, 50e-12) / 1e6, 7.12, 0.001, "C3 only 7.12 MHz")

# ==== cross-coupled-vco ====
ans("cc-gm", 1 / 500 * 1e3)
ans("kvco", 100 * 0.3)
ans("tuning-range", 6 / sqrt(1.44))
close(1 / ((6 + 5) / 2), 0.18, 0.02, "1 GHz range about 18 % of centre")

# ==== phase-noise ====
ans("pn-dbc", -112 - 0)
close(-112 - 5, -117, 0, "+5 dBm carrier: -117 dBc/Hz")
Lex = -100 - (-40) - 10 * log10(2e5)
close(Lex, -113, 0.0002, "example -113 dBc/Hz")
ans("reciprocal", (-80 - 15) - (-30) - 60)
ans("pn-offset", -100 - 20)
ans("pn-divide", round(20 * log10(2), 1), 0.05)

# ==== mixer-basics ====
close(900 - 855, 45, 0, "guess difference 45")
close(900 + 855, 1755, 0, "guess sum 1755")
ans("if-freq", abs(2140 - 2440))
close(2140 + 2440, 4580, 0, "sum 4580")
close(2 * 855 - 900, 810, 0, "example image 810")
ans("image-high", 2 * 2440 - 2140)
ok(abs(2740 - 2440) == 300, "image also 300 MHz from LO")
ans("image-low-if", 2 * 1571 - 1575)
close(2 * 10.7, 21.4, 1e-12, "image distance 21.4 MHz")
close(200e3 / 70e6 * 100, 0.29, 0.02, "200 kHz is 0.3 % of 70 MHz")

# ==== mixer-circuits ====
n = 200000
s = 0.0
for i in range(n):
    t = (i + 0.5) / n
    sq = 1 if cos(2 * pi * t) >= 0 else -1
    s += sq * cos(2 * pi * t)
fund = 2 * s / n
close(fund, 4 / pi, 1e-6, "square wave fundamental 4/pi")
ans("passive-gain-db", round(20 * log10(0.5 * fund), 1), 0.05)
close(20 * log10(1 / pi), -9.9, 0.005, "single switch -9.9 dB")
ans("active-gain", round(2 / pi * 10e-3 * 500, 2), 0.005)
close(20 * log10(2 / pi * 5), 10.1, 0.01, "10.1 dB")

# ==== mixer-spurs ====
flo = 931 + 465
close(flo, 1396, 0, "LO 1396 kHz")
ans("whistle-check", 2 * 931 - flo)
ans("if-interference", 465)
ans("lo-harmonic-spur", 2 * (600 + 465) - 465)
ans("intermod-hit", 2 * 1000 - 1010)
close(2 * 1010 - 1000, 1020, 0, "other 1020 kHz")

# ==== am-theory ====
ans("mod-index", round((1.6 - 0.4) / (1.6 + 0.4), 1), 0.001)
ans("am-bandwidth", 2 * 4.5)


def am_sideband(m, Uc=1.0, n=40000):
    # numerical Fourier: carrier at 10 cycles, modulation at 1 cycle per window
    s = 0.0
    for i in range(n):
        t = i / n
        u = Uc * (1 + m * cos(2 * pi * t)) * cos(2 * pi * 10 * t)
        s += u * cos(2 * pi * 11 * t)
    return 2 * s / n


close(am_sideband(0.6), 0.3, 1e-6, "sideband amplitude m Uc / 2")
ans("sideband-power", 0.36 / 2 * 10)
close(0.5 * 100, 50, 0, "example sidebands 50 W")
close(50 / 150, 1 / 3, 1e-12, "example 1/3")
ans("sideband-fraction", round(0.09 / 2.09 * 100, 1), 0.05)

# ==== am-circuits ====
ans("collector-power", 1 + 1**2 / 2)
ans("ssb-gap", 2 * 300)
close(600 / 10e6 * 100, 0.006, 1e-9, "0.006 % of 10 MHz")

# ==== am-detection ====
ans("rc-max", round(sqrt(1 - 0.8**2) / (0.8 * 2 * pi * 5000) * 1e6, 1), 0.05)
close(1 / 465e3 * 1e6, 2.15, 0.002, "carrier period 2.15 us")
ans("negative-peak", round(par(5.1, 10) / 5.1, 2), 0.005)
close(par(5.1, 10), 3.38, 0.001, "AC load 3.38 k")
ans("sync-phase", cos(radians(60)), 1e-9)

# ==== angle-modulation ====


def J(n_, x, terms=40):
    return sum((-1) ** k / (math.factorial(k) * math.factorial(k + n_)) * (x / 2) ** (2 * k + n_) for k in range(terms))


def J_int(n_, x, N=4000):
    return sum(cos(n_ * th - x * sin(th)) for th in (pi * (i + 0.5) / N for i in range(N))) / N


for b in (1, 3):
    close(J(0, b), J_int(0, b), 1e-9, f"J0({b}) series vs integral")
ans("fm-beta", 45 / 15)
close(J(0, 1), 0.765, 0.0005, "J0(1) 0.765")
ans("fm-carrier-power", round(0.765**2 * 100, 1), 0.15)
close(J(0, 1) ** 2 * 100, 58.55, 0.001, "exact J0^2 58.6 %")
z = bisect(lambda x: J(0, x), 2, 3)
close(z, 2.405, 0.0005, "first zero of J0 at 2.405")
close(J(0, 3) ** 2 + 2 * sum(J(m_, 3) ** 2 for m_ in range(1, 30)), 1, 1e-9, "power conserved")
close(J(0, 3) ** 2 + 2 * sum(J(m_, 3) ** 2 for m_ in range(1, 5)), 0.996, 0.001, "|n| <= 4 holds 99.6 %")
close(2 * (45 + 15), 120, 0, "example Carson 120 kHz")
ans("carson-narrow", 2 * (5 + 3))

# ==== fm-circuits ====
ans("varactor-df", 100 * 0.5 * 0.02, 0.02)
close(100 / sqrt(0.98) - 100, 1.015, 0.001, "exact 1.015 MHz")
close(75000 / 25, 3000, 0, "example N 3000")
close(100e3 * 3000 / 1e6, 300, 1e-9, "example 300 MHz")
ans("multiply-n", 75000 / 50)

# ==== fm-demod ====
ans("disc-out", 5 * 40)
ans("disc-range", 2 * 50)

# ==== pll-basics ====
ans("agc-range", 60 - 6)
ans("afc-residual", round(100 / (1 + 50), 2), 0.005)
close(1 / 10 / 0.5, 0.2, 1e-12, "example 0.2 rad")
ans("static-phase", (3 / 20) / 1)

# ==== pll-dynamics ====
Ip, K, C = 100e-6, 2 * pi * 100e6, 100e-12
# loop gain with R + 1/(sC) filter: open loop Ip/(2pi) (R + 1/(sC)) K/s; characteristic s^2 + (Ip K R/2pi) s + Ip K/(2pi C)
c1 = Ip * K * 1.4e3 / (2 * pi)
c0 = Ip * K / (2 * pi * C)
wn = sqrt(c0)
zeta = c1 / (2 * wn)
close(wn, 1e7, 1e-9, "wn 1e7 rad/s")
ans("pll-fn", round(wn / (2 * pi) / 1e6, 2), 0.005)
ans("pll-zeta", round(zeta, 1), 0.001)
close(zeta, (1.4e3 / 2) * sqrt(Ip * C * K / (2 * pi)), 1e-12, "zeta formula agrees")
close(Ip * K * 2e3 / (2 * pi) / (2 * wn), 1.0, 1e-12, "2 kOhm gives zeta 1")
close(10 * wn / (2 * pi) / 1e6, 16, 0.006, "reference at least about 16 MHz")
ans("in-band-noise", -150 + 20 * log10(1000))

# ==== integer-n ====
ans("synth-n", round(902.4e6 / 200e3))
close(902.6e6 / 200e3, 4513, 1e-9, "next channel 4513")


def swallow(P, B, A):
    count = 0
    for _ in range(A):
        count += P + 1
    for _ in range(B - A):
        count += P
    return count


close(swallow(8, 12, 4), 100, 0, "example N = 100")
ans("pulse-swallow", swallow(16, 60, 7))
close(16 * 60 + 7, 967, 0, "PB + A")

# ==== fractional-n-dds ====
acc, n92, n93 = 0.0, 0, 0
for _ in range(1000):
    acc += 0.4
    if acc >= 1 - 1e-12:
        acc -= 1
        n93 += 1
    else:
        n92 += 1
avg = (92 * n92 + 93 * n93) / 1000
close(avg, 92.4, 1e-9, "first-order accumulator averages 92.4")
ans("frac-out", round(avg * 26, 1), 0.05)
phase, M, Nb, fclk = 0, 2**28, 32, 100e6
wraps = 0
for _ in range(16 * 50):
    phase += M
    if phase >= 2**Nb:
        phase -= 2**Nb
        wraps += 1
ans("dds-out", wraps / (16 * 50) * fclk / 1e6)
close(fclk / 2**32, 0.023, 0.02, "resolution 0.023 Hz")
close(abs(80 - 100), 20, 0, "80 MHz aliases to 20 MHz")

# ==== receivers ====
ans("fm-image", round(95.0 + 2 * 10.7, 1), 0.05)
eps, th = 0.01, radians(1)
irr_exact = (1 + 2 * (1 + eps) * cos(th) + (1 + eps) ** 2) / (1 - 2 * (1 + eps) * cos(th) + (1 + eps) ** 2)
ans("irr", round(db(4 / (eps**2 + th**2))), 0.5)
close(db(irr_exact), 40, 0.002, "exact IRR also about 40 dB")
close(th**2, 3.05e-4, 0.002, "theta^2")

# ==== transmitters ====
ans("two-step-lo", 2400 - 400)
close(2000 - 400, 1600, 0, "difference 1600 MHz")
ans("acpr", 20 - (-25))
ans("evm", round(20 * log10(0.05), 1), 0.05)

# ==== boss ====
L, C, R = 1e-6, 100e-12, 10e3
ans("b-q", R / sqrt(L / C))
close(f_res(L, C) / 1e6, 15.9, 0.001, "boss f0 15.9 MHz")
ans("b-bw", round(f_res(L, C) / 100 / 1e3), 0.5)
close(bw3_parallel(L, C, R) / 1e3, 159, 0.002, "boss bandwidth from |Z|")
ans("b-loaded-q", round(par(R, 1e3) / sqrt(L / C), 1), 0.05)
close(f_res(L, C) / (par(R, 1e3) / 100) / 1e6, 1.75, 0.001, "boss loaded bandwidth 1.75 MHz")
ans("b-stages", round(250 * shrink(3)), 0.5)
ans("b-pmax", 12**2 / (2 * 50))
ans("b-colpitts", round(f_res(1e-6, 200e-12) / 1e6, 1), 0.05)
close(400e-12 * 400e-12 / 800e-12, 200e-12, 1e-24, "boss series C 200 pF")
ok(abs(f_res(1e-6, 200e-12) / 1e6 - 15.9) > 1, "boss Colpitts answer differs from the tank in b-q")
ans("b-image", round(110.7 + (110.7 - 100), 1), 0.05)
ans("b-sb-frac", round(0.25 / 2.25 * 100, 1), 0.05)
close(am_sideband(0.5), 0.25, 1e-6, "boss sideband amplitude 0.25 V")
ans("b-beta", 75 / 15)
ans("b-carson", 2 * (75 + 15))
ans("b-synth", 1100 * 100e3 / 1e6)
ans("b-mixer-gain", round(0.5 * fund * 0.02 * 400, 2), 0.005)
close(20 * log10(2 / pi * 8), 14.1, 0.005, "boss mixer 14.1 dB")
ans("b-prescaler", swallow(32, 100, 5))
close(33 * 5 + 32 * 95, 3205, 0, "boss 33 x 5 + 32 x 95")
phase, wraps = 0, 0
for _ in range(8 * 40):
    phase += 2**29
    if phase >= 2**32:
        phase -= 2**32
        wraps += 1
ans("b-dds", wraps / (8 * 40) * 80)

assert not FAILS, "\n".join(FAILS)

# ---- compare with the pack ----
pack = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "data" / "content" / "E.1.3.yaml"
text = pack.read_text(encoding="utf-8")
pairs = re.findall(r"^\s*-?\s*id: ([a-z0-9-]+)\n(?:(?!^\s*-?\s*id: ).*\n)*?\s*answer: ([-0-9.e]+)", text, re.M)
answers = {i: float(a) for i, a in pairs}
assert len(answers) == len(pairs), "duplicate ids with number answers"
missing = [i for i in computed if i not in answers]
assert not missing, f"computed but not in the pack: {missing}"
unchecked = [i for i in answers if i not in computed]
assert not unchecked, f"number answers in the pack without a check here: {unchecked}"
bad = []
for i, (v, tol) in computed.items():
    pa = answers[i]
    if abs(pa - v) > max(tol, 1e-9 * max(1, abs(v))):
        bad.append(f"{i}: pack answer {pa} but computed {v} (allowed ±{tol})")
    checks += 1
assert not bad, "\n".join(bad)

print(f"E.1.3 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
