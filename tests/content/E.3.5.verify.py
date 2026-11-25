"""E.3.5 电力系统继电保护 — every number in data/content/E.3.5.yaml, recomputed.

Run: python -I tests/content/E.3.5.verify.py
Plain Python. Settings and sensitivity coefficients follow the formulas taught in the pack; transformer
and CT/VT conversions are recomputed; differential currents are complex phasor sums; the mho
characteristic is checked geometrically (|Z - Zset/2| <= |Zset|/2) as well as with the reach formula
Zset·cos(φsen − φ); the full-cycle Fourier algorithm is run on actual sample sequences. Every number
answer is read back from the YAML and compared.
"""
import cmath
import math
import re
from math import cos, pi, radians, sin, sqrt
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


def P(mag, deg):
    return cmath.rect(mag, radians(deg))


def in_mho(zset, zm):
    geo = abs(zm - zset / 2) <= abs(zset) / 2 + 1e-12
    reach = abs(zm) <= abs(zset) * cos(cmath.phase(zset) - cmath.phase(zm)) + 1e-12
    ok(geo == reach, "mho geometry and reach formula agree")
    return geo


# ---- protection-basics / four-requirements ----
ans("clearing-time", 30 + 50)
ans("ksen", 1500 / 1000, 0.0001)

# ---- instrument-transformers ----
close(1000 / 5, 200, 1e-12, "CT 1000/5"); close(3000 / 200, 15, 1e-12, "3000 A -> 15 A")
ans("ct-secondary", 6000 / (600 / 5))
close(110000 / 100, 1100, 1e-12, "VT ratio 1100")
ans("vt-secondary", 99000 / 1100)

# ---- current-three-zones ----
ans("instant-setting", 1.25 * 2000)
t = [0.5]
for _ in range(2):
    t.append(t[-1] + 0.5)
ans("stair-time", t[-1], 0.0001)

# ---- current-settings ----
iset = 1.2 * 1.5 * 300 / 0.85
close(iset, 635, 0.5, "635 A"); close(iset / 120, 5.29, 0.005, "5.29 A"); close(1200 / iset, 1.89, 0.005, "Ksen 1.89")
ok(1200 / iset >= 1.5, "near-backup sensitivity >= 1.5")
ans("oc-primary", 1.2 * 400)
ans("oc-secondary", 480 / (600 / 5))
ans("second-zone", 1.1 * 1200)
k = 1800 / 1320
close(k, 1.36, 0.005, "1.36"); ok(k > 1.3, "Ksen > 1.3")
ans("second-zone-ksen", k, 0.005)

# ---- directional-current: 90-degree connection ----
a = P(1, 120)
Ua, Ub, Uc = 1, a ** 2 * 1, a * 1          # Ub = 1∠-120°, Uc = 1∠120°
Ubc = Ub - Uc
Ia = 1 + 0j                                # unity power factor
close(math.degrees(cmath.phase(Ia) - cmath.phase(Ubc)) % 360, 90, 1e-9, "Ia leads Ubc by 90°")

# ---- zero-sequence ----
Ia, Ib, Ic = P(900, 0), 0, 0
ans("three-i0", abs(Ia + Ib + Ic) / 3)
close(abs(1 + a ** 2 + a), 0, 1e-12, "balanced currents sum to zero")
Uph = 10000 / sqrt(3)
w = 2 * pi * 50
close(Uph, 5774, 0.5, "5774 V"); close(w, 314.2, 0.05, "314.2")
ic = 3 * w * 2e-6 * Uph
close(ic, 10.9, 0.05, "10.9 A")
ans("cap-current", ic, 0.05)
U35 = 35000 / sqrt(3)
close(U35, 20207, 0.5, "35 kV phase voltage 20207 V")
close(3 * w * 1e-6 * U35, 19.0, 0.05, "35 kV, 1 uF -> 19.0 A")
close(3 * 314.2 * 1e-6 * 20207, 19.0, 0.05, "19.0 A from the rounded numbers")
# B and C to ground after a solid A-phase earth fault: U_B - U_A, U_C - U_A
close(abs(a ** 2 - 1), sqrt(3), 1e-12, "B to ground = sqrt3 x phase"); close(abs(a - 1), sqrt(3), 1e-12, "C to ground")
ans("overcomp", 20 * 1.10, 1e-9)

# ---- distance-principle ----
ans("measured-z", 0.4 * 50)
ans("secondary-z", 57.7 / 5, 0.005)
close(10 * cos(radians(30)), 8.66, 0.005, "reach along 50°"); ok(8 < 10 * cos(radians(30)), "8∠50° inside")
ok(in_mho(P(10, 80), P(8, 50)), "example inside")
zset = P(10, 75)
ok(in_mho(zset, P(7, 60)), "7∠60 inside")
close(10 * cos(radians(15)), 9.66, 0.005, "9.66"); close(10 * cos(radians(45)), 7.07, 0.005, "7.07")
ok(not in_mho(zset, P(9, 30)), "9∠30 outside")
ok(not in_mho(zset, P(11, 75)), "11∠75 outside")
ok(not in_mho(zset, P(5, -105)), "5∠-105 outside")

# ---- distance-settings ----
z1 = 0.85 * 25
close(z1, 21.25, 1e-12, "21.25"); close(400 / 5, 80, 1e-12, "nTA 80")
close(z1 * 80 / 1100, 1.55, 0.005, "1.55")
v = 0.8 * 20 * (600 / 5) / 1100
close(0.8 * 20, 16, 1e-12, "16 ohm"); close(v, 1.75, 0.005, "1.75")
ans("zone1-secondary", v, 0.005)
z2 = 0.8 * (20 + 25.5)
close(z2 / 20, 1.82, 1e-9, "Ksen 1.82"); ok(z2 / 20 >= 1.25, "zone 2 sensitivity")
ans("zone2-setting", z2, 0.0001)
zline = P(10, 75)
ok(abs(zline + 5) > abs(zline), "fault resistance makes |Zm| larger")
ok(in_mho(P(12, 75), zline) and not in_mho(P(12, 75), zline + 8), "a large Rg can push a fault out of the mho circle")

# ---- pilot-protection ----
close(abs(P(1000, 0) + P(1000, 180)), 0, 1e-9, "external fault Id = 0")
s_ = P(1000, 0) + P(800, -10)
close(s_.real, 1787.8, 0.05, "real 1787.8"); close(s_.imag, -138.9, 0.05, "imag -138.9"); close(abs(s_), 1793, 0.5, "Id 1793")
ans("diff-internal", abs(P(600, 0) + P(400, 0)))
ans("diff-external", abs(1000 + (-950)))
close(abs(1000 - (-950)), 1950, 1e-12, "restraint 1950")

# ---- transformer-differential ----
In = lambda S, U: S / (sqrt(3) * U)
i1, i2 = In(31.5e6, 110e3), In(31.5e6, 10.5e3)
close(i1, 165.3, 0.05, "165.3 A"); close(i2, 1732, 0.5, "1732 A"); close(i2 / i1, 110 / 10.5, 1e-12, "ratio = voltage ratio")
close(i2 / i1, 10.48, 0.005, "10.48")
v = In(40e6, 110e3)
close(v, 209.9, 0.05, "209.9"); ans("rated-hv", v, 0.05)
v = 165.3 / (200 / 5)
close(v, 4.13, 0.005, "4.13"); ans("ct-mismatch", v, 0.005)
close(1732 / (2000 / 5), 4.33, 0.005, "LV 4.33")

# ---- inrush-backup ----
ans("harmonic-ratio", 0.7 / 2.0 * 100)
ok(0.05 < 0.15, "5% below the 15-20% threshold")

# ---- generator-protection ----
ans("stator-coverage", (1 - 0.05) * 100)

# ---- bus-protection ----
ans("bus-sum", 1000 - 300 - 500 - 200)
ans("bus-internal", 4000 + 1500)

# ---- reclosing ----
ans("reclose-benefit", 20 * 0.75)

# ---- numerical-relays ----
ans("sample-rate", 50 * 20)
fs = 1000
h = max(n for n in range(1, 50) if 50 * n < fs / 2)
ok(50 * 10 == fs / 2, "10th harmonic sits at fs/2")
ans("highest-harmonic", h)


def fourier(x):
    N = len(x)
    a_ = 2 / N * sum(x[k] * cos(2 * pi * k / N) for k in range(N))
    b_ = 2 / N * sum(x[k] * sin(2 * pi * k / N) for k in range(N))
    return a_, b_


x = [10 * cos(radians(30 * k + 30)) for k in range(12)]
for got, want in zip(x[:4], [8.66, 5, 0, -5]):
    close(got, want, 0.005, "sample values")
a_, b_ = fourier(x)
close(a_, 8.66, 0.005, "a = 8.66"); close(b_, -5, 1e-9, "b = -5")
amp = math.hypot(a_, b_)
close(amp, 10, 1e-9, "amplitude 10"); close(amp / sqrt(2), 7.07, 0.005, "rms 7.07")
close(math.degrees(math.atan2(-b_, a_)), 30, 1e-9, "phase 30°")
# DC and integer harmonics vanish from a full-cycle window
xd = [x[k] + 3 + 2 * cos(3 * 2 * pi * k / 12 + 0.4) for k in range(12)]
a2, b2 = fourier(xd)
close(a2, a_, 1e-9, "DC and 3rd harmonic removed (a)"); close(b2, b_, 1e-9, "DC and 3rd harmonic removed (b)")
v = math.hypot(6, -8) / sqrt(2)
close(v, 7.07, 0.005, "7.07"); ans("fourier-amp", v, 0.005)

# ---- boss ----
ans("b-ct", 4000 / (800 / 5))
ans("b-instant", 1.3 * 1500)
v = 1.2 * 2 * 250 / 0.85
close(v, 705.9, 0.05, "705.9"); ans("b-overcurrent", v, 0.5)
v = 0.85 * 25 * (400 / 5) / 1100
close(v, 1.55, 0.005, "1.55"); ans("b-distance", v, 0.005)
zs = P(8, 70)
ok(in_mho(zs, P(6, 55)), "6∠55 inside"); close(8 * cos(radians(15)), 7.73, 0.005, "7.73")
ok(not in_mho(zs, P(7, 20)), "7∠20 outside"); close(8 * cos(radians(50)), 5.14, 0.005, "5.14")
ok(not in_mho(zs, P(9, 70)), "9∠70 outside"); ok(not in_mho(zs, P(4, -110)), "4∠-110 outside")
ans("b-pilot", abs(P(700, 0) + P(500, 0)))
v = In(63e6, 220e3)
close(v, 165.3, 0.05, "165.3"); ans("b-transformer", v, 0.05)
v = math.hypot(3, 4) / sqrt(2)
close(v, 3.54, 0.005, "3.54"); ans("b-fourier", v, 0.005)

# ---- compare with the pack ----
pack = Path(__file__).resolve().parents[2] / "data" / "content" / "E.3.5.yaml"
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

print(f"E.3.5 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
