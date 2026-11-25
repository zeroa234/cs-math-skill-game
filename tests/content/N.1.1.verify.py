"""N.1.1 大学物理：力学与热学 — every number in data/content/N.1.1.yaml, recomputed.

Run: python -I tests/content/N.1.1.verify.py
Symbolic steps (derivatives, antiderivatives) use SymPy when it is installed; the rest is plain Python.
The pack's answers are also read back from the YAML (via a tiny parser for `id:` / `answer:` pairs) and
compared with the values computed here, so a typo in either place fails.
"""
import math
import re
import sys
from math import comb, cos, log, pi, radians, sin, sqrt
from pathlib import Path

g = 9.8
R = 8.314
k = 1.38e-23
checks = 0


def close(a, b, tol=1e-9, what=""):
    global checks
    if abs(a - b) > tol * max(1.0, abs(b)) and abs(a - b) > tol:
        raise AssertionError(f"{what}: {a} != {b}")
    checks += 1


computed = {}


def ans(item_id, value, tol=1e-9):
    computed[item_id] = (value, tol)


# ---- 质点运动学 ----
# position-velocity
close(200 / 300, 0.6667, 1e-3, "avg velocity walk")  # card: 200 m / 300 s
ans("avg-velocity", (-6 - 10) / (6 - 2))
try:
    import sympy as sp

    t = sp.symbols("t")
    x = 2 * t**3 - 4 * t
    ans("inst-velocity", float(sp.diff(x, t).subs(t, 1)))
    ans("accel-from-x", float(sp.diff(x, t, 2).subs(t, 1)))
    assert sp.diff(3 * t**2, t).subs(t, 2) == 12  # card example
    v = sp.integrate(6 * t, (t, 0, t)) + 2
    xx = sp.integrate(v, (t, 0, t))
    assert sp.simplify(v - (3 * t**2 + 2)) == 0
    ans("varying-accel", float(xx.subs(t, 2)))
except ImportError:  # same values by hand
    ans("inst-velocity", 6 * 1**2 - 4)
    ans("accel-from-x", 12 * 1)
    ans("varying-accel", 2**3 + 2 * 2)
ans("speed-vs-velocity", None)
close(400 / 80, 5, what="track average speed")

# constant-acceleration: braking example 20 m/s, 5 m/s^2
close(20 / 5, 4, what="brake time")
close(20**2 / (2 * 5), 40, what="brake distance")
close(20 * 4 - 0.5 * 5 * 16, 40, what="brake distance check")
ans("braking-half", 30**2 / (2 * 6))
ans("drop-time", sqrt(2 * 19.6 / g))
ans("area-vt", (4 + 16) / 2 * 6)
close(4 * 6 + 0.5 * 2 * 36, 60, what="area-vt formula")

# vectors-projectile
ans("components", 10 * sin(radians(30)))
close(10 * cos(radians(30)), 8.66, 1e-3, "horizontal component")
v0, th = 20, radians(30)
T = 2 * v0 * sin(th) / g
ans("projectile-time-half", round(T, 2), 0.01)
close(T, 2.0408, 1e-4, "flight time")
close(v0 * cos(th), 17.32, 1e-3, "vx")
Rng = v0 * cos(th) * T
close(Rng, 35.3, 0.05 / 35.3, "range")
close(v0**2 * sin(2 * th) / g, Rng, what="range formula")
close((v0 * sin(th)) ** 2 / (2 * g), 5.10, 0.005 / 5.1, "max height")
ans("projectile-height", (15 * 0.8) ** 2 / (2 * g), 0.05)
close((15 * 0.8) ** 2 / (2 * g), 7.3, 0.05 / 7.3, "football height 7.3")
assert max(range(1, 90), key=lambda d: sin(radians(2 * d))) == 45
close(sin(radians(120)), sin(radians(60)), what="60 and 30 same range")

# circular-relative
ans("centripetal-a", 20**2 / 50)
close(16 / 2, 8, what="card ac")
close(sqrt(8**2 + 6**2), 10, what="card total a")
ans("total-accel", sqrt((3**2 / 1) ** 2 + 12**2))
ans("train-walk", -2 + 20)
close(120 / 4, 30, what="boat time")
close(3 * 30, 90, what="boat drift")
close(sqrt(3**2 + 4**2), 5, what="boat speed")
ans("boat-drift", 2 * (60 / 5))

# ---- 牛顿定律 ----
ans("f-ma", (3000 - 600) / 1200)
close(60 * 9.8, 588, what="60 kg weight")
ans("moon-weight", 72 * 1.6)
ans("spring-k", 2 * g / 0.05)
ans("static-threshold", 0.5 * 20 * g)
a_inc = g * (sin(radians(30)) - 0.2 * cos(radians(30)))
close(a_inc, 3.20, 0.005 / 3.2, "incline example 3.20")
close(0.2 * 0.866, 0.2 * cos(radians(30)), 1e-3, "cos30 = 0.866")
ans("incline-half", g * (0.6 - 0.25 * 0.8), 0.01)
ans("car-curve-friction", 1000 * 10**2 / 25)
vmax = sqrt(0.8 * g * 50)
close(vmax, 19.8, 0.05 / 19.8, "vmax 19.8")
close(vmax * 3.6, 71, 0.5 / 71, "vmax km/h")
ans("max-curve-speed", sqrt(0.5 * g * 20), 0.05)
close(sqrt(0.5 * g * 20), 9.9, 0.05 / 9.9, "9.9")
vT = sqrt(2 * 80 * g / (1 * 1.2 * 0.8))
ans("terminal-speed", vT, 0.05)
close(vT, 40.4, 0.05 / 40.4, "40.4")

# ---- 动量与角动量守恒 ----
ans("momentum-value", 0.15 * 40)
ans("egg-force", 0.06 * 5 / 0.1)
close(0.06 * 5 / 0.002, 150, what="egg on concrete")
ans("bounce-impulse", abs(0.5 * (-4) - 0.5 * 6))
ans("skater-push", -(60 * 2) / 40)
ans("ke-value", 0.5 * 2 * 3**2)
v = 2 * 3 / 3
close(v, 2, what="example common v")
close(0.5 * 2 * 9 - 0.5 * 3 * v**2, 3, what="example KE loss")
vc = 3 * 4 / 4
ans("inelastic-loss", 0.5 * 3 * 16 - 0.5 * 4 * vc**2)
# elastic, equal masses: m1=m2 -> v1'=0, v2'=v1
m1 = m2 = 1.0
v1 = 2.0
close((m1 - m2) / (m1 + m2) * v1, 0, what="elastic v1'")
close(2 * m1 / (m1 + m2) * v1, 2, what="elastic v2'")
close(sqrt(2**2 + 1.5**2), 2.5, what="2D card example")
vx, vy = 1500 * 20 / 4000, 2500 * 12 / 4000
ans("two-d-collision", sqrt(vx**2 + vy**2), 0.05)
close(sqrt(vx**2 + vy**2), 10.6, 0.05 / 10.6, "10.6")
ans("cm-position", (2 * 0 + 1 * 3) / 3)
d = 60 * 3 / (60 + 120)
ans("boat-walk", d)
ans("rocket-eq", 3000 * log(math.e**2))
close(math.e**2, 7.39, 0.005 / 7.39, "e^2")
ans("torque-value", 0.25 * 40 * sin(radians(30)))
ans("l-circular", 0.2 * 4 * 0.5)
ans("planet-speed", 1000 * 6e12 / 1.5e11)

# ---- 功与能量 ----
ans("work-angle", 50 * 10 * cos(radians(60)))
ans("spring-work", 0.5 * 200 * 0.1**2)
ans("wet-theorem", (0.5 * 2 * 9) / 4)
ans("power-car", 800 * 25 / 1000)
close(1000 * 3600, 3.6e6, what="kWh")
ans("slide-speed", sqrt(2 * g * 5), 0.05)
close(2 * g * 3, 58.8, what="example E1")
close(0.5 * 2 * 36 - 58.8, -22.8, what="example friction work")
ans("spring-launch", sqrt(2 * (0.5 * 800 * 0.1**2) / 0.5))
try:
    import sympy as sp

    xs = sp.symbols("x")
    ans("force-from-u", float(sp.solve(sp.diff(3 * xs**2 - 12 * xs, xs), xs)[0]))
except ImportError:
    ans("force-from-u", 12 / 6)

# ---- 刚体转动 ----
ans("rpm-to-rad", 1200 / 60 * 2 * pi, 0.05)
close(1200 / 60 * 2 * pi, 125.7, 0.05 / 125.7, "125.7")
close(4 * 5, 20, what="grinder omega")
close(0.5 * 4 * 25, 50, what="grinder angle")
close(50 / (2 * pi), 8, 0.05, "about 8 turns")
ans("wheel-stop", 30**2 / (2 * 3))
close(150 / (2 * pi), 24, 0.0 + 0.05, "about 24 turns")
ans("rim-speed", 0.06 * 50)
ans("centripetal-rim", 40**2 * 0.25)
close(400 / g, 41, 0.01, "41 g")
ans("point-masses-inertia", 3 * 1**2 + 3 * 1**2)
close(1 / 12 + (1 / 2) ** 2, 1 / 3, what="rod parallel axis")
Icm = 0.5 * 2 * 0.3**2
ans("parallel-axis", Icm + 2 * 0.3**2)
# disk + block (exercise (4))
I = 0.5 * 2 * 0.1**2
a = 1 * g / (1 + I / 0.1**2)
close(I, 0.01, what="disk I")
close(a, 4.9, what="disk a")
close(a / 0.1, 49, what="disk alpha")
close(1 * (g - a), 4.9, what="disk T")
I4 = 0.5 * 4 * 0.2**2
ans("disk-block-tension", 2 * g / (2 + I4 / 0.2**2))
ans("rot-power", 30 * 100)
ans("rolling-ke-fraction", round((1 / 4) / (3 / 4), 3), 0.001)
vdisk = sqrt(4 * g * 1.5 / 3)
close(vdisk, 4.43, 0.005 / 4.43, "rolling disk 4.43")
close(sqrt(2 * g * 1.5), 5.42, 0.005 / 5.42, "sliding block 5.42")
ans("rolling-hoop", sqrt(g * 2.5), 0.01)
close(sqrt(g * 2.5), 4.95, 0.005 / 4.95, "4.95")
ans("skater-spin", 4 * 2 / 1.6)
close((0.5 * 1.6 * (5 * 2 * pi) ** 2) / (0.5 * 4 * (2 * 2 * pi) ** 2), 2.5, what="KE ratio 2.5")
ans("precession-rate", 0.5 * g * 0.04 / (5e-4 * 200), 0.005)

# ---- 热力学定律 ----
ans("ideal-gas-volume", 1 * R * 273.15 / 101325 * 1000, 0.05)
close(1 * R * 273.15 / 101325 * 1000, 22.4, 0.05 / 22.4, "22.4 L")
ans("isobaric-work", 2e5 * (0.03 - 0.01))
ans("first-law-calc", 500 - 200)
close(-100 - (-300), 200, what="compress sign")
Wiso = 1 * R * 300 * log(2)
close(Wiso, 1729, 1 / 1729, "isothermal card 1729")
ans("isothermal-work", 2 * R * 400 * log(3), 1)
close(2 * R * 400 * log(3), 7307, 1 / 7307, "7307")
Qp = 2 * 2.5 * R * 10
ans("isobaric-heat", Qp, 0.05)
close(2 * 1.5 * R * 10, 249.4, 0.05 / 249.4, "dU part")
close(2 * R * 10, 166.3, 0.05 / 166.3, "work part")
ans("adiabatic-temp", 300 * 8 ** (2 / 3))
close(8 ** (2 / 3), 4, 1e-12, "8^(2/3)")
ans("engine-eff", (2000 - 1400) / 2000 * 100)
ans("fridge-cop", 300 + 100)
ans("heatpump-cop", 3 + 1)
ans("carnot-eff", (1 - 300 / 600) * 100)
ans("carnot-celsius", (1 - 300 / 800) * 100, 0.05)
close((1 - 27 / 527) * 100, 94.9, 0.05 / 94.9, "wrong celsius 94.9")
ans("entropy-flow", -1200 / 400 + 1200 / 300)
close(comb(4, 2), 6, what="4 molecules split 2-2")
ans("microstates", comb(6, 3))

# ---- 气体动理论 ----
ans("avg-ke-molecule", 1.5 * k * 300 / 1e-21, 0.005)
close(1.5 * k * 300, 6.21e-21, 0.005e-21 / 6.21e-21, "6.21e-21")
close(sqrt(3 * R * 300 / 0.028), 517, 1 / 517, "N2 vrms 517")
ans("vrms-oxygen", sqrt(3 * R * 300 / 0.032), 1)
close(3 * R * 300 / 0.032, 233831, 1 / 233831, "233831")
ans("vrms-ratio", sqrt(0.032 / 0.002))
close(sqrt(2), 1.41, 0.005, "sqrt2")
ans("cv-diatomic", 2.5 * R * 12, 0.05)
close(1.5 * R * 12, 149.7, 0.05 / 149.7, "He 149.7")
ans("gamma-diatomic", (7 / 2) / (5 / 2))
close(sqrt(8 / pi), 1.60, 0.005, "sqrt(8/pi)")
close(sqrt(3), 1.73, 0.005, "sqrt3")
lam = k * 300 / (sqrt(2) * pi * (3.7e-10) ** 2 * 101325)
ans("mean-free-path", lam / 1e-9, 1)
close(lam / 1e-9, 67, 1 / 67, "67 nm")
close(lam / 3.7e-10, 180, 5 / 180, "about 180 diameters")
close(k * 300 / (sqrt(2) * pi * (3.7e-10) ** 2 * 101325e-6) / lam, 1e6, 1e-9, "lambda ~ 1/p")
# Maxwell distribution: numerically check the three speeds and the normalization for N2 at 300 K
M = 0.028


def f(v, T=300.0):
    a = M / (2 * R * T)
    return 4 * pi * (a / pi) ** 1.5 * v * v * math.exp(-a * v * v)


dv = 0.5
vs = [i * dv for i in range(1, 8000)]
norm = sum(f(v) for v in vs) * dv
mean = sum(v * f(v) for v in vs) * dv
rms = sqrt(sum(v * v * f(v) for v in vs) * dv)
vp = max(vs, key=f)
close(norm, 1, 1e-6, "normalization")
close(mean, sqrt(8 * R * 300 / (pi * M)), 1e-4, "mean speed")
close(rms, sqrt(3 * R * 300 / M), 1e-4, "rms speed")
close(vp, sqrt(2 * R * 300 / M), 0.5 / vp, "most probable speed")

# ---- 结业挑战 ----
ans("b-projectile", Rng, 0.05)
ans("b-incline", g * (0.5 - 0.3 * cos(radians(30))), 0.01)
close(g * (0.5 - 0.3 * cos(radians(30))), 2.35, 0.005 / 2.35, "2.35")
vb = 4 * 5 / 10
ans("b-collision", 0.5 * 4 * 25 - 0.5 * 10 * vb**2)
ans("b-disk", 1 * (g - a))
ans("b-angular", 2 * 3 / (2 + 0.5 * 1**2))
ans("b-isothermal", Wiso, 1)
ans("b-carnot", (1 - 300 / 500) * 1000)
ans("b-vrms", sqrt(3 * R * 300 / 0.028), 1)

# ---- compare with the pack ----
pack = Path(__file__).resolve().parents[2] / "data" / "content" / "N.1.1.yaml"
text = pack.read_text(encoding="utf-8")
pairs = re.findall(r"^\s*-?\s*id: ([a-z0-9-]+)\n(?:(?!^\s*-?\s*id: ).*\n)*?\s*answer: ([-0-9.e]+)", text, re.M)
answers = {i: float(a) for i, a in pairs}
missing = [i for i, (v, _) in computed.items() if v is not None and i not in answers]
assert not missing, f"computed but not in the pack: {missing}"
unchecked = [i for i in answers if i not in computed]
assert not unchecked, f"number answers in the pack without a check here: {unchecked}"
for i, (v, tol) in computed.items():
    if v is None:
        continue
    pa = answers[i]
    if abs(pa - v) > max(tol, 1e-9 * max(1, abs(v))):
        raise AssertionError(f"{i}: pack answer {pa} but computed {v}")
    checks += 1

print(f"N.1.1 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
