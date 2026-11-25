"""H.1.4 模拟电子技术 — every number in data/content/H.1.4.yaml, recomputed.

Run: python -I tests/content/H.1.4.verify.py
Plain Python. Number answers are read back from the YAML and compared with the values computed here.
The diode exponential model is solved by iteration, the ripple formula is checked against a simulated
peak rectifier, the Wien-bridge network is evaluated at f0 as a complex divider, and the stability example's
crossover and phase are recomputed from the three-pole loop gain.
"""
import cmath
import math
import re
from math import atan, degrees, exp, log, pi, sqrt
from pathlib import Path

VT = 0.025
checks = 0
computed = {}


def close(a, b, tol=1e-9, what=""):
    global checks
    if abs(a - b) > tol * max(1.0, abs(b)) and abs(a - b) > tol:
        raise AssertionError(f"{what}: {a} != {b}")
    checks += 1


def ans(item_id, value, tol=1e-9):
    computed[item_id] = (value, tol)


par = lambda a, b: a * b / (a + b)

# ---- 二极管电路 ----
close((5 - 0.7) / 1e3, 4.3e-3, what="CVD 4.3 mA")
# exponential model: I_S chosen so that 0.7 V gives 1 mA; solve 5 V, 1 kOhm by iteration
Is = 1e-3 / exp(0.7 / VT)
v = 0.7
for _ in range(50):
    i = (5 - v) / 1e3
    v = VT * log(i / Is + 1)
close(v, 0.736, 0.0005, "iterated diode voltage ~0.736")
close((5 - v) / 1e3 * 1e3, 4.26, 0.005, "iterated current ~4.26 mA")
close(VT * log(10) * 1e3, 57.6, 0.05, "57.6 mV per decade")
ans("decade-voltage", VT * log(100) * 1e3, 0.05)
ans("small-signal-rd", VT / 2e-3)
close(VT / 1e-3, 25, what="rd at 1 mA")
ans("zener-current", ((9 - 5) / 200 - 5 / 1000) * 1e3)
ans("halfwave-peak", 10 - 0.7)
ans("bridge-peak", 12 - 2 * 0.7)
ans("ripple-halfwave", 10 / (50 * 1000 * 1e-3))
# simulate an ideal-diode half-wave peak rectifier with RC load and measure the ripple
f, R, C, Vp = 50.0, 1e3, 1e-3, 10.0
dt = 1e-6
vc, vmin, vmax = 0.0, 1e9, -1e9
for n in range(int(0.2 / dt)):
    t = n * dt
    vs = Vp * math.sin(2 * pi * f * t)
    if vs > vc:
        vc = vs
    else:
        vc -= vc / (R * C) * dt
    if t > 0.1:
        vmin, vmax = min(vmin, vc), max(vmax, vc)
close(vmax - vmin, 0.2, 0.02, "simulated ripple ~0.2 V (approximation)")
ans("limiter-level", 3 + 0.7)

# ---- BJT与MOSFET放大电路 ----
k = 2e-3
ans("mosfet-id", 0.5 * k * (1 - 0.5) ** 2 * 1e3)
VD = 5 - 0.25e-3 * 10e3
close(VD, 2.5, what="example VD")
assert VD >= 0.5
assert 0.5 < 1.4 - 0.6  # region item: vDS 0.5 < Vov 0.8 -> triode
ans("mosfet-ro", 1 / (0.05 * 0.5e-3) / 1e3)
ans("mosfet-gm", 2 * 0.25e-3 / 0.5 * 1e3)
close(2 * 0.5e-3 / 0.2, 5e-3, what="card gm 5 mS")
close(k * 0.5, 2 * 0.25e-3 / 0.5, what="gm both forms")
ans("cs-gain-ro", -5e-3 * par(10e3, 40e3))
ans("follower-gain", 1000 / (1000 + 1 / 5e-3), 0.0005)
ans("degenerated-cs", -5e-3 * 10e3 / (1 + 5e-3 * 200))
ans("body-effect", 0.5 + 0.4 * (sqrt(2.6) - sqrt(0.6)), 0.0005)
ans("bjt-currents", (1 + 1 / 100))
close(1 / 1.01, 0.990, 0.001, "alpha")
VB = 12 * 20 / 100
close(VB, 2.4, what="example VB")
IE = (VB - 0.7) / 1.7e3
close(IE, 1e-3, what="example IE")
close(12 - 1e-3 * 4e3 - 1.7, 6.3, 1e-12, "example VCE")
ans("divider-bias", (10 * 30 / 100 - 0.7) / 2.3e3 * 1e3)
assert 100 * 0.1e-3 * 1e3 > 5  # region item: needs 10 V across 1 kOhm, saturates
close((5 - 0.2) / 1e3, 4.8e-3, what="saturation current")
ans("bjt-rpi", 100 / (1e-3 / VT) / 1e3)
close(-(1e-3 / VT) * 4e3, -160, what="CE -160")
close(-(1e-3 / VT) * par(4e3, 4e3), -80, what="CE -80")
ans("ce-gain-load", -(0.5e-3 / VT) * par(10e3, 10e3))
ans("ce-re-gain", -4000 / (25 + 225))
ans("follower-rin", (99 + 1) * (25 + 975) / 1e3)
ans("vbe-temp", 0.70 - 50 * 0.002)
close(2 * 1e-3 / 0.2, 10e-3, what="MOS gm at 1 mA, 0.2 V")

# ---- 差分放大器 ----
ans("dm-cm", (2.005 - 1.995) * 1e3)
gm = 2 * 0.2e-3 / 0.2
ans("mos-diff-gain", gm * 20e3)
gmb = 0.5e-3 / VT
close(gmb * 10e3, 200, what="double-ended 200")
Acm = 10e3 / (2 * 50e3)
close(Acm, 0.1, what="Acm 0.1")
close(20 * math.log10(100 / Acm), 60, what="CMRR 60 dB")
ans("cmrr-db", 20 * math.log10(50 / 0.05))
ans("offset-bjt", VT * 0.02 * 1e3)
ans("offset-mos", 0.2 / 2 * 0.02 * 1e3)
ans("bias-current", 100 / (99 + 1))
ans("multistage-gain", 100 * -200 * 0.9)
close(20 * math.log10(18000), 85.1, 0.1, "85 dB")

# ---- 电流源与有源负载 ----
ans("intrinsic-gain", 2 * 10 / 0.2)
close(100 / VT, 4000, what="BJT intrinsic 4000")
ans("cascode-ro", (2e-3 * 50e3) * 50e3 / 1e6)
ans("cascode-gain", 40**2)
ans("mirror-ratio", 50 * 40 / 10)
ans("bjt-mirror", 1 / (1 + 2 / 100), 0.0005)
ro = 100 / 1e-3
close(ro, 100e3, what="ro 100k")
close(-(1e-3 / VT) * par(ro, ro), -2000, what="active load -2000")
ans("active-load-gain", -2e-3 * par(60e3, 60e3))
ans("darlington", 100 * 100)
close(100 * 100 + 100 + 100, 10200, what="exact darlington")

# ---- 功率放大器 ----
ans("class-a-eff", (10**2 / (2 * 100)) / (2 * 10 * 0.1) * 100)
# class A worked example (automation review 2026-11-23): +-12 V, 0.15 A, 100 ohm, 12 V peak
close(12**2 / (2 * 100), 0.72, 1e-9, "class A example P_L 0.72 W")
close(2 * 12 * 0.15, 3.6, 1e-9, "class A example P_S 3.6 W")
close(0.72 / 3.6, 0.20, 1e-9, "class A example 20 %")
Vcc, RL = 12.0, 100.0
close((Vcc**2 / (2 * RL)) / (2 * Vcc * (Vcc / RL)), 0.25, 1e-12, "class A max efficiency 1/4")
ans("class-b-power", 12**2 / (2 * 8))
close(2 * 12 * 12 / (pi * 8), 11.46, 0.01, "class B supply power")
ans("class-b-eff-half", pi * 6 / (4 * 12) * 100, 0.05)
ans("vbe-multiplier", 0.6 * (1 + 1.2 / 1))
ans("junction-temp", 25 + 20 * (1.5 + 0.5 + 3))
ans("btl-power", 4 * 0.5)
# class B: dissipation is maximal at Vo = 2Vcc/pi
Vcc, RL = 12.0, 8.0
diss = lambda Vo: 2 * Vcc * Vo / (pi * RL) - Vo**2 / (2 * RL)
vbest = max((i / 1000 * Vcc for i in range(1001)), key=diss)
close(vbest, 2 * Vcc / pi, 0.02, "max dissipation point")
close(diss(2 * Vcc / pi), 2 * Vcc**2 / (pi**2 * RL), 1e-9, "max dissipation value")

# ---- 频率响应 ----
ans("coupling-pole", 1 / (2 * pi * 1e4 * 1e-6), 0.05)
ans("transition-freq", 0.04 / (2 * pi * 12e-12) / 1e6, 1)
ans("miller-cap", 1 * (1 + 50))
Cin = 10e-12 + 2e-12 * 101
close(Cin, 212e-12, 1e-15, "212 pF")
close(1 / (2 * pi * 1e3 * Cin) / 1e3, 751, 1, "751 kHz")
ans("miller-fh", 1 / (2 * pi * 1e4 * (2e-12 + 0.5e-12 * 41)) / 1e6, 0.005)
ans("octc-sum", 1 / (2 * pi * (20e3 * 5e-12 + 10e3 * 2e-12)) / 1e6, 0.005)
ans("cascode-miller", 1 * (1 + 1))
ans("follower-bootstrap", 2 * (1 - 0.9))
ans("cascade-bandwidth", 1e3 * sqrt(2 ** 0.5 - 1), 1)
close(sqrt(2 ** (1 / 3) - 1), 0.510, 0.001, "three stages 0.510")
# check the n-stage formula against |H|^n = 1/sqrt(2)
for n_st in (2, 3):
    x = sqrt(2 ** (1 / n_st) - 1)
    close((1 / sqrt(1 + x * x)) ** n_st, 1 / sqrt(2), 1e-12, "n-stage -3 dB")

# ---- 负反馈 ----
A, B = 1e4, 0.01
close(A / (1 + A * B), 99.0, 0.01, "Af 99.0")
close(5000 / 51, 98.04, 0.01, "Af 98.04")
close((A / 101 - 5000 / 51) / (A / 101), 0.0098, 0.0001, "0.98 %")
ans("closed-loop-gain", 2000 / (1 + 2000 * 0.05), 0.005)
ans("bandwidth-extend", 1 * (1 + 1e4 * 0.01))
close(1e5 * 0.1, 1e4, what="opamp 1+AB ~1e4")
ans("series-shunt-ro", 2000 / (1 + 1000 * 0.1), 0.05)
ans("transresistance", 2e-6 * 1e5)
ans("noninv-gain", 1 + 90 / 10)
ans("phase-margin", 180 - 135)
ans("dominant-pole", 1e5 * 10 / 1e6)
# stability example: poles 1, 10, 100 MHz, A0*beta = 100
L = lambda fr: 100 / ((1 + 1j * fr / 1e6) * (1 + 1j * fr / 1e7) * (1 + 1j * fr / 1e8))
fc = 1e7 * 10 ** 0.5
close(fc / 1e6, 31.6, 0.05, "asymptotic crossover 31.6 MHz")
ph = -(degrees(atan(fc / 1e6)) + degrees(atan(fc / 1e7)) + degrees(atan(fc / 1e8)))
close(ph, -178.2, 0.1, "phase at 31.6 MHz")
close(degrees(cmath.phase(L(fc))) - 360 if degrees(cmath.phase(L(fc))) > 0 else degrees(cmath.phase(L(fc))), ph, 1e-6, "phase from complex")
# the exact |L| = 1 frequency is a bit lower than the asymptote; still a tiny phase margin
lo, hi = 1e6, 1e8
for _ in range(200):
    mid = sqrt(lo * hi)
    if abs(L(mid)) > 1:
        lo = mid
    else:
        hi = mid
pm_exact = 180 + (degrees(cmath.phase(L(lo))) - 360 if degrees(cmath.phase(L(lo))) > 0 else degrees(cmath.phase(L(lo))))
assert 0 < pm_exact < 20, pm_exact
checks += 1

# ---- 振荡器与稳压电源 ----
f0 = 1 / (2 * pi * 1e4 * 1e-8)
ans("wien-freq", f0 / 1e3, 0.005)
# Wien network: series RC over parallel RC at f0 -> ratio 1/3, zero phase
w0 = 2 * pi * f0
Zs = 1e4 + 1 / (1j * w0 * 1e-8)
Zp = 1 / (1 / 1e4 + 1j * w0 * 1e-8)
ratio = Zp / (Zs + Zp)
close(abs(ratio), 1 / 3, 1e-9, "Wien |beta| = 1/3")
close(cmath.phase(ratio), 0, 1e-9, "Wien phase 0")
ans("wien-gain", 2 * 10)
ans("colpitts", 1 / (2 * pi * sqrt(10e-6 * 1e-9)) / 1e6, 0.0005)
ans("schmitt-thresholds", 2 * 12 * 10 / 60)
ans("astable-period", 2 * 1e4 * 1e-7 * log((1 + 0.5) / (1 - 0.5)) * 1e3, 0.005)
T555 = 0.693 * (1e3 + 2 * 10e3) * 10e-9
ans("timer-555", 1 / T555 / 1e3, 0.01)
close(11 / 21, 0.524, 0.001, "555 duty")
ans("monostable", 1.1 * 1e5 * 1e-5)
close((12 - 5.1) / 15e-3, 460, 1e-9, "example 460 Ohm")
close(5.1 * 0.015, 0.0765, 1e-12, "zener power")
ans("zener-resistor", (15 - 9) / 25e-3)
ans("lm317", 1.25 * (1 + 720 / 240))
ans("linear-vs-buck", (12 - 5) * 1)
close(5 / 12, 0.417, 0.001, "linear efficiency")
close(5 / 0.9 - 5, 0.556, 0.001, "buck loss at 90 %")
ans("buck-duty", 6 / 24)

# ---- 结业挑战 ----
ans("b-diode", (9 - 0.7) / 2e3 * 1e3)
ans("b-cs-amp", -(2 * 0.4e-3 / 0.25) * 15e3)
g = 0.25e-3 / VT
ans("b-diff", 20 * math.log10((g * 20e3 / 2) / (20e3 / (2 * 100e3))))
ans("b-mirror", 2 / (1 + 2 / 50), 0.0005)
ans("b-class-b", pi / 4 * 100, 0.05)
close(15**2 / 16, 14.06, 0.01, "class B 14.1 W")
ans("b-miller", 1 / (2 * pi * 2000 * (9e-12 + 1e-12 * 81)) / 1e3, 1)
Af1, Af2 = 5e4 / (1 + 5e4 * 0.02), 4e4 / (1 + 4e4 * 0.02)
close(Af1, 49.9500, 0.0001, "Af before")
close(Af2, 49.9376, 0.0001, "Af after")
ans("b-feedback", (Af1 - Af2) / Af1 * 100, 0.0005)
ans("b-wien", 1 / (2 * pi * 5e3 * 20e-9) / 1e3, 0.005)
ans("b-supply", (18 - 12) / 30e-3)

# ---- compare with the pack ----
pack = Path(__file__).resolve().parents[2] / "data" / "content" / "H.1.4.yaml"
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

print(f"H.1.4 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
