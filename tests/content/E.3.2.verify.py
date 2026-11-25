"""E.3.2 电机与电力拖动 — every number in data/content/E.3.2.yaml, recomputed.

Run: python -I tests/content/E.3.2.verify.py
Plain Python. Magnetic circuits from l/(mu A), the rotating field by summing three phase MMF vectors,
the swing equation and DC drive by RK4 simulation, the induction-machine torque from the equivalent
circuit compared with the Kloss approximation, and the Clarke/Park transforms evaluated directly.
Number answers are read back from the YAML and compared with the values computed here.
"""
import cmath
import math
import re
from math import cos, pi, radians, sin, sqrt
from pathlib import Path

checks = 0
computed = {}
MU0 = 4 * pi * 1e-7


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


def rk4(f, t0, y0, t1, n=20000):
    h = (t1 - t0) / n
    t, y = t0, list(y0)
    for _ in range(n):
        k1 = f(t, y)
        k2 = f(t + h / 2, [a + h / 2 * b for a, b in zip(y, k1)])
        k3 = f(t + h / 2, [a + h / 2 * b for a, b in zip(y, k2)])
        k4 = f(t + h, [a + h * b for a, b in zip(y, k3)])
        y = [a + h / 6 * (p + 2 * q + 2 * r + s) for a, p, q, r, s in zip(y, k1, k2, k3, k4)]
        t += h
    return y


rpm = lambda n: n * 2 * pi / 60

# ==== 磁路 ====
R_core = 0.5 / (2000 * MU0 * 4e-4)
close(R_core, 4.97e5, 0.001, "core reluctance 4.97e5")
ans("core-flux-density", 200 * 1 / R_core / 4e-4, 0.005)
R_gap = 1e-3 / (MU0 * 4e-4)
close(R_gap, 1.99e6, 0.0005, "gap reluctance")
close(R_gap / 4.97e5, 4, 0.01, "gap about 4 times the core")
ans("air-gap", 200 / (4.97e5 + R_gap) / 4e-4, 0.0005)
close(200 / (4.97e5 + R_gap), 8.04e-5, 0.001, "gap flux")
ans("inductance", 200**2 / 4.97e5 * 1e3, 0.05)

# ==== 变压器 ====
ans("core-flux", 220 / (4.44 * 50 * 500) * 1e3, 0.005)
close(2 * pi / sqrt(2), 4.44, 0.005, "4.44 = 2 pi / sqrt 2")
ans("reflected-impedance", 5**2 * 4)
close(10000 / 2200, 4.55, 0.005, "10 kVA I1")
close(10000 / 220, 45.5, 0.05, "10 kVA I2")
ans("rated-current", 25000 / 240, 0.05)
close(25000 / 2400, 10.4, 0.05, "25 kVA I1")
ok(10e3 / 400 == 25 and 250 / 25 == 10, "step-down 10 A")
ans("referred-resistance", 10**2 * 0.02)
close(120 / 10, 12, what="SC |Z|")
close(400 / 10**2, 4, what="SC R")
close(sqrt(12**2 - 4**2), 11.3, 0.05, "SC X")
ans("open-circuit", 240**2 / 160)
ans("efficiency", 8000 / (8000 + 100 + 200) * 100, 0.05)
ans("max-efficiency", sqrt(100 / 400) * 100)
ans("per-unit", 11.52 / (2400**2 / 25000))
close(sqrt(3) * 220, 380, 1, "Y line voltage ~ 380")

# ==== 机电能量转换 ====
ans("magnetic-force", 0.5 * 3**2 * (0.08 - 0.05) / 0.002)
th = radians(30)
dM = -0.05 * sin(th)
ans("mutual-torque", abs(10 * 2 * dM))
# check f = 1/2 i^2 dL/dx by energy balance at constant current: dW_mech = d(1/2 L i^2) at constant i
L1, L2, i = 0.05, 0.08, 3.0
W_elec = i * i * (L2 - L1)          # energy from the source at constant current: i dlambda
dW_field = 0.5 * i * i * (L2 - L1)
close(W_elec - dW_field, 0.5 * i * i * (L2 - L1), 1e-12, "mechanical work = half the source energy")

# ==== 旋转磁场 ====
ans("phase-voltage", 380 / sqrt(3), 0.05)
mags = []
for k in range(12):
    t = k / 12
    F = sum(cos(2 * pi * t - 2 * pi * m / 3) * cmath.exp(1j * 2 * pi * m / 3) for m in range(3))
    mags.append(abs(F))
ok(max(mags) - min(mags) < 1e-12, "rotating field has constant magnitude")
close(mags[0], 1.5, 1e-12, "magnitude 1.5 times one phase")
ans("sync-speed", 60 * 50 / 4)
for p_, n_ in ((1, 3000), (2, 1500), (3, 1000)):
    close(60 * 50 / p_, n_, what=f"{2*p_}-pole speed")

# ==== 同步电机 ====
ans("power-angle", 3 * 230 * 260 * sin(radians(20)) / 5 / 1e3, 0.005)
ans("pull-out", 3 * 230 * 260 / 5 / 1e3, 0.005)
# phasor check: E = V + j Xs I gives P = 3 V E sin(delta)/Xs
V, E, Xs, d = 230.0, 260.0, 5.0, radians(20)
I = (E * cmath.exp(1j * d) - V) / (1j * Xs)
close(3 * (V * I.conjugate()).real, 3 * V * E * sin(d) / Xs, 1e-9, "phasor power")
ans("equilibrium-angle", math.degrees(math.asin(1.0 / 2.0)))
ans("sync-coefficient", 2.0 * cos(radians(30)), 0.0005)
# swing equation: start at delta0 = 30 deg with a small kick; oscillates around 30 deg
M = 0.05
sol = rk4(lambda t, y: [y[1], (1.0 - 2.0 * sin(y[0])) / M - 0.0 * y[1]], 0, [radians(30) + 0.05, 0], 2.0, 20000)
ok(abs(math.degrees(sol[0]) - 30) < 5, "small swing stays near 30 deg")
ok(2.0 * cos(radians(150)) < 0, "150 deg has negative synchronising coefficient")

# ==== 直流电机 ====
E1 = 240 - 25 * 0.4
w1 = rpm(1200)
close(E1, 230, what="DC example E")
close(w1, 125.7, 0.05, "DC example omega")
close(E1 / w1, 1.83, 0.005, "DC example kPhi")
close(E1 / w1 * 25, 45.8, 0.05, "DC example T")
close(E1 * 25, 5750, 1e-9, "DC example power")
E2 = 120 - 50 * 0.2
ans("dc-torque", E2 / rpm(1000) * 50, 0.05)
close(120 / 0.2, 600, what="start current 600 A")
ans("start-resistor", 120 / 100 - 0.2)

# ==== 步进和永磁 ====
ans("vr-step", 360 / (3 * 8))
ans("stepper-speed", 1000 * 1.8 / 360 * 60)
ok(360 / 1.8 == 200, "1.8 deg -> 200 steps")
ans("commutation-steps", 6 * 4)
ans("electrical-frequency", 3000 / 60 * 4)

# ==== 感应电机 ====
s1 = (1000 - 975) / 1000
ans("rotor-frequency", s1 * 50)
ans("rotor-speed", 60 * 60 / 2 * (1 - 0.03))
ans("load-resistance", 0.2 * (1 - 0.04) / 0.04)
close(0.2 * (1 - 0.04) / 0.04 + 0.2, 0.2 / 0.04, 1e-12, "R2/s split")
close(0.04 * 10, 0.4, what="example rotor copper")
close(10 - 0.4, 9.6, what="example P_mech")
close(10000 / rpm(1500), 63.7, 0.05, "example torque")
ans("rotor-copper", 0.05 * 20)
kl = lambda s, sm: 2 / (s / sm + sm / s)
ans("kloss", kl(0.04, 0.2), 0.0005)
ans("starting-torque", kl(1, 0.25), 0.0005)
# compare Kloss with the exact equivalent-circuit torque when R1 = 0: T ~ (R2/s)/((R2/s)^2 + X^2)
R2, X = 0.2, 1.0
Tex = lambda s: (R2 / s) / ((R2 / s) ** 2 + X**2)
sm = R2 / X
close(Tex(0.04) / Tex(sm), kl(0.04, sm), 1e-12, "Kloss exact when R1 = 0")
ok(max([i / 1000 for i in range(1, 1000)], key=Tex) == sm, "max torque at s_m = R2/X")

# ==== 电力拖动 ====
ans("fan-torque", 40 * (1200 / 1500) ** 2, 0.05)
close((1200 / 1500) ** 3, 0.512, 1e-12, "fan power 51 %")
w = (220 - (40 / 2) * 0.5) / 2
ans("dc-speed", w)
close(w * 60 / (2 * pi), 1003, 0.5, "1003 r/min")
ans("dc-half-voltage", (110 - 20 * 0.5) / 2)
# simulate the DC drive settling: J dw/dt = kPhi*Ia - TL, Ia = (V - kPhi w)/Ra
wss = rk4(lambda t, y: [(2 * (220 - 2 * y[0]) / 0.5 - 40) / 0.1], 0, [0], 2, 20000)[0]
close(wss, 105, 1e-6, "DC drive settles at 105 rad/s")

# ==== 变频和矢量控制 ====
ans("vf-speed", 60 * (30 - 1.5) / 2)
ans("vf-voltage", 400 * 30 / 50)
close(380 * 25 / 50, 190, what="example 190 V")
clarke = lambda a, b: (a, (a + 2 * b) / sqrt(3))
park = lambda al, be, th: (al * cos(th) + be * sin(th), -al * sin(th) + be * cos(th))
for th in (0.0, pi / 2, 1.1, 2.7):
    ia, ib = 10 * cos(th), 10 * cos(th - 2 * pi / 3)
    d, q = park(*clarke(ia, ib), th)
    close(d, 10, 1e-9, f"i_d constant at {th}")
    close(q, 0, 1e-9, f"i_q constant at {th}")
close(10 * cos(-pi / 6), 8.66, 0.005, "8.66")
ans("clarke", clarke(5, 5)[1], 0.005)
ans("iq-torque", 2 * 6 / 4)

# ==== 结业挑战 ====
ans("b-magnetic", 100 * 2 / 4e5 * 1e3)
ans("b-transformer", 50000 / 400)
ans("b-dc", (440 - 30 * 0.8) / rpm(1000) * 30, 0.05)
ans("b-sync", 3 * 240 * 300 * 0.5 / 8 / 1e3)
ans("b-stepper", 360 / (360 / (4 * 6)))
s2 = (1800 - 1740) / 1800
ans("b-slip", s2 * 60)
ans("b-induction-torque", 15000 / rpm(1000), 0.05)
ans("b-vf", 460 * 45 / 60)

# ---- automation review 2026-11-23: air-gap worked example ----
Rg_ex = 0.5e-3 / (4 * pi * 1e-7 * 3e-4)
close(Rg_ex, 1.33e6, 0.005e6, "air-gap example gap reluctance")
Rt_ex = 3.0e5 + Rg_ex
close(Rt_ex, 1.63e6, 0.005e6, "air-gap example total reluctance")
close(150 * 0.8, 120, 1e-12, "air-gap example mmf")
Phi_ex = 120 / Rt_ex
close(Phi_ex, 7.38e-5, 0.005e-5, "air-gap example flux")
close(Phi_ex / 3e-4, 0.246, 0.0005, "air-gap example B")
close(7.38e-5 / 3e-4, 0.246, 0.0005, "air-gap example B from rounded flux")

# ---- compare with the pack ----
pack = Path(__file__).resolve().parents[2] / "data" / "content" / "E.3.2.yaml"
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

print(f"E.3.2 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
