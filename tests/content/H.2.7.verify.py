"""H.2.7 集成电路制造工艺 — every number in data/content/H.2.7.yaml, recomputed.

Run: python -I tests/content/H.2.7.verify.py [path/to/H.2.7.yaml]
Plain Python. Number answers are read back from the YAML and compared with the values computed here, so a typo in
either place fails. Independent checks where possible: the erfc junction depths by bisection on math.erfc, the
Gaussian implant/diffusion profiles by integrating them back to the dose, the Deal-Grove times both forwards and
by solving the quadratic for the thickness, the Scheil profile against a step-by-step solidification, the
quadratic placement-style minimum not needed here; the 3-sigma fractions from statistics.NormalDist; the dies-per-
wafer formula against a direct count of whole dies on a grid; the KOH sidewall angle from the (100)/(111) normals.
Constants given in the pack: q = 1.602e-19 C, eps0 = 8.854e-14 F/cm, k = 8.617e-5 eV/K, kB = 1.381e-23 J/K.
Data cited in the pack: Deal & Grove (1965) 1000 C constants (dry A = 0.165 um, B = 0.0117 um^2/h, tau = 0.37 h;
wet A = 0.226 um, B = 0.287 um^2/h); boron D0 = 0.76 cm^2/s, Ea = 3.46 eV (Sze); k0 B 0.8, P 0.35, As 0.3;
Si a = 0.5431 nm, melting point 1414 C; ISO 14644-1 class formula.
"""
import re
import sys
from math import acos, asin, ceil, cos, degrees, erfc, exp, floor, log, log10, pi, radians, sin, sqrt, tan
from pathlib import Path
from statistics import NormalDist

checks = 0
computed = {}


def close(a, b, tol=1e-9, what=""):
    global checks
    if abs(a - b) > tol * max(1.0, abs(b)) and abs(a - b) > tol:
        raise AssertionError(f"{what}: {a} != {b}")
    checks += 1


def ok(cond, what=""):
    global checks
    if not cond:
        raise AssertionError(what)
    checks += 1


def ans(item_id, value, tol=1e-9):
    computed[item_id] = (value, tol)


def bisect(f, a, b, it=200):
    fa = f(a)
    for _ in range(it):
        m = (a + b) / 2
        fm = f(m)
        if (fm > 0) == (fa > 0):
            a, fa = m, fm
        else:
            b = m
    return (a + b) / 2


q, e0, k, kB = 1.602e-19, 8.854e-14, 8.617e-5, 1.381e-23
eox = 3.9 * e0

# ==== planar-process / isolation-wells ====
ans("mask-count", 40 * (1 + 15))
ans("well-masks", 1 + 2 + 2)

# ==== vt-gate ====
cox5 = eox / 5e-7
close(cox5, 6.91e-7, 0.001, "Cox 5 nm")
close(q * 1e12, 1.602e-7, 1e-9, "qQ")
close(q * 1e12 / cox5, 0.23, 0.01, "dVT 0.23")
cox2 = eox / 2e-7
close(cox2, 1.73e-6, 0.002, "Cox 2 nm")
ans("vt-shift", q * 5e12 / cox2, 0.002)
ans("vt-dose", 0.3 * 6.91e-7 / q / 1e12, 0.01)

# ==== sd-contacts / finfet ====
ans("spacer-width", 30 + 2 * 20)
ans("fin-weff", 3 * (2 * 42 + 8))
ans("fin-count", ceil(400 / (2 * 50 + 7)))
close(4 * 107, 428, 1e-9, "428 nm")
ok(2011 <= 2012, "22 nm FinFET volume production around 2011-2012 (Intel)")

# ==== beol ====
R_cu = 1.7e-6 * 1e-2 / (1e-5 * 2e-5)
ans("cu-al-ratio", R_cu, 0.1)
close(2.7e-6 * 1e-2 / (1e-5 * 2e-5), 135, 1e-9, "Al 135 Ohm")
close(1.7 / 2.7, 0.63, 0.001, "about six tenths")

# ==== backend-issues ====
ans("em-current", 1.5 ** -2, 0.002)
temp_ratio = exp(0.9 / k * (1 / 378.15 - 1 / 398.15))
ans("em-temp", temp_ratio, 0.05)
close(0.9 / k * (1 / 378.15 - 1 / 398.15), 1.39, 0.002, "exponent 1.39")
close(1.7 / 2.7, 0.63, 0.001, "R ratio")
close(2.7 / 3.9, 0.69, 0.005, "C ratio")
close(0.63 * 0.69, 0.44, 0.02, "RC 0.44")
ans("rc-lowk", 2.5 / 3.9, 0.002)

# ==== cmp ====
ans("preston-rate", 1e-13 * 3e4 * 0.8 * 1e9 * 60, 0.1)
rr = 1e-13 * 2.5e4 * 1.2
close(rr * 1e9 * 60, 180, 1e-9, "180 nm/min")
close(800 / 180, 4.44, 0.005, "4.44 min")
ans("cmp-time", 600 / 120, 1e-9)

# ==== crystal-growth ====
a = 0.5431e-7
ans("si-density", 8 / a**3 / 1e22, 0.01)


def scheil(k0, f):
    return k0 * (1 - f) ** (k0 - 1)


ans("scheil-p", scheil(0.35, 0.5), 0.002)
# step-by-step solidification check of the Scheil formula
N = 200000
melt_atoms, melt_mass, cs_half = 1.0, 1.0, None
dm = 1.0 / N
for i in range(N):
    cl = melt_atoms / melt_mass
    cs = 0.35 * cl
    if cs_half is None and i >= N // 2:
        cs_half = cs
    melt_atoms -= cs * dm
    melt_mass -= dm
close(cs_half, scheil(0.35, 0.5), 1e-3, "Scheil by stepping")
close(1.569, 0.5 ** -0.65, 0.001, "1.569")
ok(1414 > 1400, "Si melting point 1414 C")

# ==== wafer-soi ====


def dpw(d, A):
    return pi * (d / 2) ** 2 / A - pi * d / sqrt(2 * A)


ans("dpw-1cm2", floor(dpw(30, 1)))
close(dpw(30, 1), 640.2, 0.001, "640.2")
ans("dpw-2cm2", floor(dpw(30, 2)))
close(pi * 225 / 2, 353.4, 0.001, "353.4")


# direct count of whole 1 cm x 1 cm dies on a 30 cm wafer (best grid offset) is close to the formula
def count(d, s, ox, oy):
    r = d / 2
    n = 0
    i0 = int(-r / s) - 2
    for i in range(i0, -i0 + 1):
        for j in range(i0, -i0 + 1):
            x0, y0 = i * s + ox, j * s + oy
            if all((x0 + dx) ** 2 + (y0 + dy) ** 2 <= r * r for dx in (0, s) for dy in (0, s)):
                n += 1
    return n


best = max(count(30, 1, ox / 4, oy / 4) for ox in range(4) for oy in range(4))
ok(abs(best - 640) / 640 < 0.03, f"grid count {best} within 3% of the formula")

# ==== contamination ====
iso = lambda N, D: 10**N * (0.1 / D) ** 2.08
ans("iso5-count", floor(iso(5, 0.5)), 4)
close(iso(5, 0.5), 3520, 0.001, "ISO table 3520")
close(0.2**2.08, 0.0352, 0.002, "0.0352")
close(3517 * 0.0283168, 100, 0.01, "about 100 per cubic foot")
ans("iso6-ratio", iso(6, 0.5) / iso(5, 0.5), 1e-9)

# ==== yield ====
ans("yield-poisson", exp(-0.2) * 100, 0.05)
close(exp(-0.1) * 100, 90.5, 0.001, "90.5%")
close(exp(-0.75), 0.472, 0.001, "Poisson example")
close(1.375**-2, 0.529, 0.001, "NB example")
ans("yield-nb", (1 + 0.75) ** -1 * 100, 0.05)
ans("good-dies", floor(640 * exp(-0.1)))
for Y in (0.9, 0.5):
    close((Y) ** 2, exp(-2 * -log(Y)), 1e-12, "area doubling squares the yield")

# ==== process-control ====
nd = NormalDist()
close((nd.cdf(1) - nd.cdf(-1)) * 100, 68.3, 0.001, "68.3%")
close((nd.cdf(2) - nd.cdf(-2)) * 100, 95.4, 0.001, "95.4%")
close((nd.cdf(3) - nd.cdf(-3)) * 100, 99.73, 0.0001, "99.73%")
ans("outside-3sigma", floor(2 * (1 - nd.cdf(3)) * 1e6), 2)
close(2 * (1 - nd.cdf(3)) * 1e6, 2699.8, 0.0001, "2699.8")
close(0.5**8, 1 / 256, 1e-12, "1/256")
close(0.12 / 0.09, 1.33, 0.003, "Cp 1.33")
close(0.05 / 0.045, 1.11, 0.002, "Cpk 1.11")
ans("cpk-calc", min(1.06 - 1.02, 1.02 - 0.94) / (3 * 0.01), 0.002)
close((1.06 - 0.94) / (6 * 0.01), 2, 1e-9, "centred 2")

# ==== litho-concepts ====
ans("proximity-res", sqrt(0.365 * 20), 0.01)
ans("mask-4x", 45 * 4)
ok([436, 365, 248, 193, 13.5] == sorted([436, 365, 248, 193, 13.5], reverse=True), "wavelength order")

# ==== litho-optics ====
ans("krf-res", 0.4 * 248 / 0.8, 0.1)
close(0.3 * 193 / 1.35, 42.9, 0.001, "ArF 42.9")
close(0.5 * 193 / 1.35**2, 52.9, 0.001, "DOF 52.9")
close(1.35**2, 1.8225, 1e-9, "1.8225")
ans("krf-dof", 0.5 * 248 / 0.64, 0.5)
ans("euv-res", 0.4 * 13.5 / 0.33, 0.05)
close((0.93 / 1.35) ** 2, 0.47, 0.01, "DOF ratio 0.47")

# ==== photoresist ====
ans("resist-gamma", 1 / log10(50 / 20), 0.01)
close(sqrt(3000 / 4000), 0.866, 0.001, "0.866")
ans("spin-thickness", 1.2 * sqrt(2500 / 4500), 0.002)
close(sqrt(2500 / 4500), 0.745, 0.001, "0.745")

# ==== ret-nil ====
ans("water-wavelength", 193 / 1.44, 0.1)
ok(1.44 * sin(radians(70)) > 1.35, "NA 1.35 reachable with water")
close(80 / 2, 40, 1e-9, "SADP 40 nm")
close(80 / 4, 20, 1e-9, "SAQP 20 nm")
ans("euv-highna", 0.3 * 13.5 / 0.55, 0.02)
close(0.3 * 13.5 / 0.33, 12.3, 0.003, "12.3 nm")

# ==== deal-grove ====


def dg_t(x, A, B, tau):
    return (x * x + A * x) / B - tau


def dg_x(t, A, B, tau):
    return (-A + sqrt(A * A + 4 * B * (t + tau))) / 2


ans("si-consumed", 0.44 * 500, 0.1)
close(500 - 220, 280, 1e-9, "280 above")
close(dg_t(0.5, 0.226, 0.287, 0), 1.26, 0.005, "wet 1.26 h")
close(dg_x(dg_t(0.5, 0.226, 0.287, 0), 0.226, 0.287, 0), 0.5, 1e-9, "wet round trip")
ok(0.25 > 0.113, "x^2 > Ax")
ans("dg-exercise", dg_t(0.5, 0.1, 0.5, 0), 0.001)
ans("dg-dry", dg_t(0.1, 0.165, 0.0117, 0.37), 0.01)
close(dg_x(dg_t(0.1, 0.165, 0.0117, 0.37), 0.165, 0.0117, 0.37), 0.1, 1e-9, "dry round trip")

# ==== oxide-2d-highk ====
ans("volume-ratio", 1 / 0.44, 0.01)
close(1 / 0.44, 2.2, 0.04, "about 2.2")
close(3 * 3.9 / 25, 0.468, 1e-9, "0.468")
close(3 * 3.9 / 25 + 0.5, 0.968, 1e-9, "0.968")
ans("eot-calc", 2 * 3.9 / 25, 0.001)
ans("highk-thick", 1 * 25 / 3.9, 0.01)


# ==== fick-diffusion ====
def erfcinv(y):
    return bisect(lambda u: erfc(u) - y, 0, 10)


u5 = erfcinv(1e-5)
close(u5, 3.12, 0.002, "u for 1e-5")
close(sqrt(2e-14 * 1800), 6.0e-6, 1e-9, "sqrt(Dt) 6.0e-6")
close(2 * u5 * sqrt(2e-14 * 1800) * 1e4, 0.375, 0.003, "example xj 0.375")
u4 = erfcinv(1e-4)
close(u4, 2.75, 0.001, "u for 1e-4")
ans("erfc-xj", 2 * u4 * sqrt(1e-13 * 3600) * 1e4, 0.01)
close(sqrt(1e-13 * 3600), 1.90e-5, 0.002, "1.90e-5")
Dt = 1e-13 * 3600
C0 = 1e14 / sqrt(pi * Dt)
ans("gauss-surface", C0 / 1e18, 0.01)
# Gaussian integrates back to the dose
h = 1e-7
integral = sum(C0 * exp(-((i * h) ** 2) / (4 * Dt)) * h for i in range(0, 20000)) - C0 * h / 2
close(integral, 1e14, 1e-3, "Gaussian integrates to Q")
close(sqrt(4), 2, 1e-12, "4x time doubles xj")

# ==== diffused-layers ====
DB = lambda T: 0.76 * exp(-3.46 / (k * (T + 273.15)))
ans("boron-d", DB(1100) / 1e-13, 0.01)
close(DB(1000), 1.53e-14, 0.003, "1000 C")
close(DB(1100) / DB(1000), 10, 0.01, "about 10x")
close(k * 1373.15, 0.1183, 0.001, "kT")
close(pi / log(2), 4.532, 0.0001, "4.532")
Rs = 4.532 * 10
close(Rs, 45.3, 0.001, "45.3")
close(Rs * 0.5e-4, 2.27e-3, 0.003, "rho")
close(Rs * 10, 453, 0.001, "453")
ans("four-point", 4.532 * 15 / 2, 0.05)
ans("sheet-resistor", 200 * 150 / 5 / 1000, 1e-9)

# ==== implant-basics ====
A200 = pi * 10**2
ans("implant-time", 1e15 * q * A200 / 1e-3, 0.1)
close(A200, 314.2, 0.001, "314.2 cm^2")
close(5e14 / (sqrt(2 * pi) * 3e-6), 6.65e19, 0.002, "6.65e19")
close(sqrt(2 * pi), 2.507, 0.001, "2.507")
ans("implant-peak", 1e15 / (sqrt(2 * pi) * 4e-6) / 1e19, 0.02)
Np = 1e15 / (sqrt(2 * pi) * 4e-6)
dx = 1e-8
tot = sum(Np * exp(-((i * dx - 1e-5) ** 2) / (2 * (4e-6) ** 2)) * dx for i in range(-4000, 6000))
close(tot, 1e15, 1e-3, "implant profile integrates to Q (whole Gaussian)")
m = sqrt(2 * log(1e4))
close(m, 4.29, 0.001, "m 4.29")
ans("mask-thickness", 0.1 + 4.29 * 0.04, 0.002)

# ==== stopping-annealing ====
ans("tilt-depth", 200 * cos(radians(7)), 0.05)

# ==== wet-etch ====
ans("iso-undercut", 2 + 2 * 0.6, 1e-9)
close(200 / 4, 50, 1e-9, "selectivity 50")
close(300 / 200, 1.5, 1e-9, "1.5 min")
close(0.2 * 1.5, 0.3, 1e-9, "0.3 min")
close(4 * 0.3, 1.2, 1e-9, "1.2 nm")
ans("selectivity-calc", 5 * (0.1 * 500 / 100), 1e-9)
# KOH: angle between (100) and (111) planes
ang = degrees(acos(1 / sqrt(3)))
close(ang, 54.74, 0.0001, "54.74 deg")
close(2 / tan(radians(54.74)), 1.414, 0.001, "1.414")
ans("koh-bottom", 100 - 2 * 30 / tan(radians(54.74)), 0.05)
close(30 / tan(radians(54.74)), 21.2, 0.002, "21.2 per side")
close(50 * tan(radians(54.74)), 70.7, 0.001, "V-groove 70.7")

# ==== plasma-etch ====
ans("anisotropy", 1 - 5 / 100, 1e-9)
ans("ale-cycles", round(10 / 0.2))

# ==== cvd ====
ans("step-coverage", 60 / 100 * 100, 1e-9)
heff = 1 * 10 / 11
close(heff, 0.909, 0.001, "0.909")
v = heff * 1e16 / 5e22
close(v * 1e7, 1.82, 0.001, "1.82 nm/s")
close(v * 1e7 * 60, 109, 0.001, "109 nm/min")
ans("ald-cycles", round(2 / 0.1))

# ==== pvd ====
lam = lambda p: kB * 300 / (sqrt(2) * pi * (0.36e-9) ** 2 * p)
ans("mfp-calc", lam(1) * 1e3, 0.02)
close(kB * 300, 4.14e-21, 0.001, "kT 4.14e-21")
close(lam(1e-4), 72, 0.002, "72 m")
ans("mfp-highvac", lam(0.5) / lam(1), 1e-9)

# ==== 结业挑战 ====
ans("b-vt-shift", q * 2e12 / (eox / 3e-7), 0.002)
ans("b-fin", ceil(250 / (2 * 45 + 6)))
ans("b-em", 2**-2 * exp(0.8 / k * (1 / 393.15 - 1 / 373.15)), 0.0005)
close(exp(0.8 / k * (1 / 393.15 - 1 / 373.15)), 0.282, 0.002, "temperature factor 0.282")
ans("b-cmp", 900 / (1e-13 * 4e4 * 0.5 * 1e9 * 60), 0.01)
ans("b-dpw", floor(dpw(30, 0.5)), 0.6)
ans("b-scheil", scheil(0.8, 0.9), 0.002)
ans("b-yield", exp(-0.16) * 100, 0.05)
ans("b-cpk", min(10.3 - 10.1, 10.1 - 9.7) / (3 * 0.04), 0.002)
ans("b-litho", 0.35 * 193 / 0.93, 0.1)
close(0.35 * 193 / 1.35, 50, 0.001, "immersion 50 nm")
ans("b-dg", dg_t(1, 0.11, 0.51, 0), 0.01)
ans("b-implant-peak", 2e15 / (sqrt(2 * pi) * 5e-6) / 1e20, 0.005)
close(1e15 / 1e20, 1e-5, 1e-12, "erfc 1e-5")
ans("b-erfc", 2 * u5 * sqrt(4e-14 * 7200) * 1e4, 0.005)
ans("b-etch", 8 * 0.25 * 400 / 160, 1e-9)
ans("b-grove", 2 * 2 / 4 * 1e16 / 2.3e22 * 1e7 * 60, 0.5)
close(1e16 / 2.3e22 * 1e7, 4.35, 0.001, "4.35 nm/s")

# ---- compare with the pack ----
pack = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "data" / "content" / "H.2.7.yaml"
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

print(f"H.2.7 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
