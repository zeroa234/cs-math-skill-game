"""E.3.3 电力系统分析 — every number in data/content/E.3.3.yaml, recomputed.

Run: python -I tests/content/E.3.3.verify.py
Plain Python with complex numbers. Per-unit conversions; line inductance and capacitance from the
geometric formulas; the long-line solution from cosh/sinh of the telegrapher's equations; the bus
admittance matrix built as A y A^T; Gauss-Seidel and Newton iterations run to convergence; fault
currents in the sequence domain and transformed back to phase currents; the critical clearing angle
checked against a numerical simulation of the swing equation; dispatch from the equal-incremental
equations. Number answers are read back from the YAML and compared with the values computed here.
"""
import cmath
import math
import re
from math import acos, asin, cos, degrees, log, pi, radians, sin, sqrt
from pathlib import Path

checks = 0
computed = {}
EPS0 = 8.854e-12
W = 2 * pi * 50
a = cmath.exp(2j * pi / 3)


def close(x, y, tol=1e-9, what=""):
    """x equals y within tol, or (for a value the pack states rounded) x rounds to y at y's precision."""
    global checks
    if abs(x - y) > tol * max(1.0, abs(y)) and abs(x - y) > tol:
        s = repr(float(y)) if isinstance(y, (int, float)) else ""
        dec = len(s.split(".")[1]) if "." in s and "e" not in s else None
        if dec is None or round(x, dec) != round(float(y), dec) or (isinstance(y, int) and round(x) != y):
            raise AssertionError(f"{what}: {x} != {y}")
    checks += 1


def ok(cond, what):
    global checks
    if not cond:
        raise AssertionError(what)
    checks += 1


def ans(item_id, value, tol=1e-9):
    computed[item_id] = (value, tol)


# ==== 电网是怎样连起来的 ====
I220 = 100e6 / (sqrt(3) * 220e3)
close(I220, 262.4, 0.0005, "262.4 A")
ans("loss-vs-voltage", 3 * I220 ** 2 * 10 / 1e6, 0.005)
I110 = 100e6 / (sqrt(3) * 110e3)
close(3 * I110 ** 2 * 10 / 1e6, 8.26, 0.001, "8.26 MW at 110 kV")
close((3 * I110 ** 2 * 10) / (3 * I220 ** 2 * 10), 4, 1e-12, "loss ratio 4")
# ungrounded system, phase a grounded: b-to-ground = V_b - V_a
Vph = 10e3 / sqrt(3)
Va, Vb = Vph, Vph * a ** 2
ans("ungrounded-voltage", abs(Vb - Va) / 1e3)
close(Vph / 1e3, 5.77, 0.001, "5.77 kV phase voltage")

# ==== 标幺值 ====
close(12.7 * (10.5 / 110) ** 2, 0.116, 0.003, "guess 0.116 ohm")
close(12.7 / (12.7 * (10.5 / 110) ** 2), 110, 0.01, "about 110 times")
ans("rated-current", 120e6 / (sqrt(3) * 110e3), 0.5)
ZB110 = 110 ** 2 / 100
close(ZB110, 121, 1e-12, "Z_B 121")
ans("line-per-unit", 0.4 * 50 / ZB110, 0.0005)
ans("base-current", I110, 0.5)
close(10.5 ** 2 / 50, 2.205, 1e-12, "2.205 ohm")
close(0.2 * 2.205, 0.441, 1e-12, "0.441 ohm")
close(0.441 / (10.5 ** 2 / 100), 0.4, 1e-12, "0.4 pu")
close(0.2 * 100 / 50 * (10.5 / 10.5) ** 2, 0.4, 1e-12, "change-of-base formula")
ans("change-base", 0.105 * 100 / 120, 0.00005)
zl = 12.7 * (10.5 / 110) ** 2
close(zl, 0.1157, 0.0005, "0.1157 ohm")
close(12.7 / ZB110, zl / (10.5 ** 2 / 100), 1e-12, "same pu on both sides")
ans("two-sides-pu", 0.1157 / (10.5 ** 2 / 100), 0.0005)

# ==== 线路参数 ====
L1 = 2e-7 * log(5 / (0.7788 * 0.01))
close(log(5 / 0.007788), 6.465, 0.0005, "ln 6.465")
close(L1 * 1e6, 1.293, 0.0005, "1.293 mH/km")
close(W * L1 * 1e3, 0.406, 0.001, "0.406 ohm/km")
C1 = 2 * pi * EPS0 / log(5 / 0.01)
close(log(500), 6.215, 0.0005, "ln 500")
close(C1 * 1e12, 8.95, 0.001, "8.95 nF/km")
close(W * C1 * 1e3 * 1e6, 2.81, 0.002, "2.81 uS/km")
L2 = 2e-7 * log(8 / (0.7788 * 0.012))
close(0.7788 * 12, 9.35, 0.001, "r' 9.35 mm")
close(log(8 / 0.0093456), 6.752, 0.0005, "ln 6.752")
ans("line-reactance", W * L2 * 1e3, 0.0005)
ok((log(10 / 0.007788) / log(5 / 0.007788) - 1) < 0.12, "doubling D raises L by about 11 %")
ans("charging-power", (500e3) ** 2 * 2.8e-6 * 300 / 1e6)

# ==== 线路的等值电路 ====
ans("pi-admittance", 2.8e-6 * 200 / 2 * 1e6)
x, b = 0.4, 2.8e-6
Zc = sqrt(x / b)
ans("surge-impedance", Zc, 0.5)
close(1 / sqrt((x / W) * (b / W)), 3e5, 0.02, "wave speed near light speed (km/s)")
ans("natural-power", 220 ** 2 / 380, 0.5)
close(500 ** 2 / 260, 960, 0.002, "500 kV SIL about 960 MW")
beta = sqrt(x * b)
close(degrees(beta), 0.06, 0.02, "0.06 deg/km")
# long-line solution with cosh: lossless gamma = j beta
for l in (300, 400):
    g = 1j * beta * l
    Vs_over_Vr = cmath.cosh(g)  # open end: Vs = Vr cosh(gamma l)
    close(abs(1 / Vs_over_Vr), 1 / cos(beta * l), 1e-12, f"open-end rise {l} km")
close(beta * 400, 0.423, 0.001, "0.423 rad")
close(degrees(beta * 400), 24.3, 0.002, "24.3 deg")
ans("ferranti", 1 / cos(beta * 400), 0.0005)
close(1 / cos(beta * 400) - 1, 0.10, 0.03, "about 10 % at 400 km")
# rise from the charging current: Vs = Vr (1 - X B) for a lumped pi approx (sanity)
ok(1 / (1 - 0.4 * 400 * 2.8e-6 * 400 / 2) > 1, "charging current raises the far-end voltage")

# ==== 线路上的功率 ====
Sx = 1 * (0.5 * cmath.exp(-1j * radians(30))).conjugate()
close(Sx.real, 0.433, 0.001, "P 0.433")
ans("complex-power", Sx.imag)
ans("two-bus-angle", degrees(asin(0.2)), 0.05)
dV_ex = (40 * 10 + 30 * 20) / 110
dv_ex = (40 * 20 - 30 * 10) / 110
close(dV_ex, 9.09, 0.001, "9.09 kV")
close(dv_ex, 4.55, 0.001, "4.55 kV")
close(sqrt((110 + dV_ex) ** 2 + dv_ex ** 2), 119.2, 0.0005, "119.2 kV")
# exact check of the drop formula: V1 = V2 + Z * conj(S/V2)
V1 = 110 + (10 + 20j) * ((40 + 30j) / 110).conjugate()
close(V1.real - 110, dV_ex, 1e-12, "longitudinal component exact")
close(V1.imag, dv_ex, 1e-12, "transverse component exact")
ans("voltage-drop", (50 * 8 + 25 * 16) / 110, 0.005)
ans("line-loss", (50 ** 2 + 25 ** 2) / 110 ** 2 * 10, 0.005)
# Q2 formula
for d_ in (0.1, 0.3):
    V1p, V2p, X = 1.05 * cmath.exp(1j * d_), 1.0, 0.2
    I = (V1p - V2p) / (1j * X)
    S2 = V2p * I.conjugate()
    close(S2.real, 1.05 * 1.0 / X * sin(d_), 1e-12, "P formula")
    close(S2.imag, (1.05 * cos(d_) - 1.0) / X, 1e-12, "Q2 formula")

# ==== 节点导纳矩阵 ====
branches = [(0, 1, 0.1), (1, 2, 0.25), (0, 2, 0.2)]
A = [[0] * 3 for _ in range(3)]
for k, (i, j, _) in enumerate(branches):
    A[i][k], A[j][k] = 1, -1
Y = [[sum(A[i][k] * (1 / (1j * branches[k][2])) * A[j][k] for k in range(3)) for j in range(3)] for i in range(3)]
close(Y[0][0].imag, -15, 1e-12, "Y11")
close(Y[1][1].imag, -14, 1e-12, "Y22")
close(Y[2][2].imag, -9, 1e-12, "Y33")
close(Y[0][1].imag, 10, 1e-12, "Y12")
close(Y[1][2].imag, 4, 1e-12, "Y23")
close(Y[0][2].imag, 5, 1e-12, "Y13")
for i in range(3):
    close(abs(sum(Y[i])), 0, 1e-12, "row sums zero")
ans("ybus-diagonal", Y[1][1].imag)
ans("ybus-offdiag", Y[1][2].imag)
ans("sparsity", 1000 + 2 * 1500)
close(4000 / 1e6, 0.004, 1e-12, "0.4 %")

# ==== 潮流方程 ====
Y2 = [[-5j, 5j], [5j, -5j]]
S2inj = -0.5 - 0.2j
V2 = 1 + 0j
V2_1 = (1 / Y2[1][1]) * (S2inj.conjugate() / V2.conjugate() - Y2[1][0] * 1)
close(V2_1.real, 0.96, 1e-12, "GS step real")
close(V2_1.imag, -0.1, 1e-12, "GS step imag")
ans("gauss-seidel", abs(V2_1), 0.0005)
V = V2_1
for _ in range(200):
    V = (1 / Y2[1][1]) * (S2inj.conjugate() / V.conjugate() - Y2[1][0] * 1)
close(abs(V), 0.952, 0.0005, "GS converges to 0.952")
close(degrees(cmath.phase(V)), -6.0, 0.005, "angle -6.0 deg")
Scheck = V * (Y2[1][0] * 1 + Y2[1][1] * V).conjugate()
close(abs(Scheck - S2inj), 0, 1e-9, "converged GS satisfies the power equation")

# ==== 牛顿法 ====
d = 0.0
d1 = d + (1 - 5 * sin(d)) / (5 * cos(d))
d2 = d1 + (1 - 5 * sin(d1)) / (5 * cos(d1))
close(d1, 0.2, 1e-12, "guess 0.2 rad")
ans("nr-first-step", degrees(d1), 0.005)
close(degrees(d2), 11.537, 0.0001, "second iterate 11.537")
close(degrees(asin(0.2)), 11.537, 0.0001, "exact 11.537")
close(asin(0.2), 0.2014, 0.001, "0.2014")
ans("nr-second-case", degrees(2 / 5), 0.005)
close(degrees(asin(0.4)), 23.58, 0.0005, "23.58")
# DC flow: two parallel paths, reactances 0.1 and 0.3
ans("dc-flow", 1.0 * 0.3 / (0.1 + 0.3))

# ==== 三相短路 ====
ans("fault-current", 10 * I110 / 1e3, 0.005)
ans("short-circuit-capacity", 10 * 100)
Xs = 0.15 + 0.0875 + 0.165
close(Xs, 0.4025, 1e-12, "0.4025 pu")
close(1 / Xs, 2.48, 0.002, "2.48 pu")
ans("series-fault", 1 / Xs * I110 / 1e3, 0.005)
ans("subtransient-current", 1 / 0.15, 0.005)
ans("steady-fault-current", 1 / 1.8, 0.0005)
ans("peak-current", sqrt(2) * 1.8 * 20, 0.05)
close(sqrt(2) * 1.8, 2.55, 0.001, "2.55")
Ks2 = 2.0 * cos(radians(30))
close(Ks2, 1.732, 0.0005, "example Ks 1.732")
close(sqrt(W * Ks2 / 8), 8.25, 0.001, "example 8.25 rad/s")
close(sqrt(W * Ks2 / 8) / (2 * pi), 1.31, 0.003, "example 1.31 Hz")
close(6000 / 4, 1500, 1e-12, "quarter wavelength 1500 km at 50 Hz (c = 3e5 km/s)")

# ==== 对称分量 ====
def seq(xa, xb, xc):
    return ((xa + xb + xc) / 3, (xa + a * xb + a * a * xc) / 3, (xa + a * a * xb + a * xc) / 3)


def phase(x0, x1, x2):
    return (x0 + x1 + x2, x0 + a * a * x1 + a * x2, x0 + a * x1 + a * a * x2)


close(abs(1 + a + a * a), 0, 1e-12, "1 + a + a^2 = 0")
s = seq(3, 0, 0)
for v in s:
    close(v, 1, 1e-12, "single-phase current splits into three equal thirds")
for xa, xb, xc in [(1, 2j, -0.5), (0.3 - 1j, 0, 2)]:
    back = phase(*seq(xa, xb, xc))
    close(abs(back[0] - xa) + abs(back[1] - xb) + abs(back[2] - xc), 0, 1e-12, "transform round trip")
p1 = phase(0, 1, 0)
close(cmath.phase(p1[1]), radians(-120), 1e-12, "positive sequence b lags 120")
p2 = phase(0, 0, 1)
close(cmath.phase(p2[2]), radians(-120), 1e-12, "negative sequence c lags 120")
Ia, Ib = 10, 10 * cmath.exp(-1j * radians(120))
i0, i1, i2 = seq(Ia, Ib, 0)
close(abs(Ia + Ib), 10, 1e-12, "10 + 10 at -120 has magnitude 10")
ans("zero-sequence", abs(i0), 0.005)
ans("positive-sequence", abs(i1), 0.005)
ans("neutral-impedance", 3 * 0.05)

# ==== 不对称短路 ====
Z1, Z2, Z0 = 0.1j, 0.1j, 0.2j
E = 1
i1 = E / (Z1 + Z2 + Z0)
ia, ib, ic = phase(i1, i1, i1)
close(abs(ib) + abs(ic), 0, 1e-12, "SLG: b and c currents zero")
ans("slg-current", abs(ia))
ans("slg-ka", abs(ia) * I110 / 1e3, 0.005)
# LL: I1 = -I2 = E/(Z1+Z2), I0 = 0
i1 = E / (Z1 + Z2)
ia, ib, ic = phase(0, i1, -i1)
close(abs(ia), 0, 1e-12, "LL: a current zero")
close(abs(ib + ic), 0, 1e-12, "LL: b = -c")
ans("ll-current", abs(ib), 0.005)
close(abs(ib) / 10, sqrt(3) / 2, 1e-12, "0.87 of the three-phase current")
par = Z2 * Z0 / (Z2 + Z0)
close(abs(par), 0.0667, 0.001, "Z2 // Z0")
i1 = E / (Z1 + par)
i2 = -i1 * Z0 / (Z2 + Z0)
i0 = -i1 * Z2 / (Z2 + Z0)
ia, ib, ic = phase(i0, i1, i2)
close(abs(ia), 0, 1e-12, "LLG: a current zero")
ans("llg-positive", abs(i1))
m = sqrt(3) * sqrt(1 - (0.1 * 0.2) / (0.1 + 0.2) ** 2)
close(abs(ib), m * abs(i1), 1e-9, "LLG multiplier formula")
for z0 in (0.05, 0.08):
    ok(3 / (0.2 + z0) > 10, f"SLG exceeds 3-phase when Z0 = {z0} < Z1")
ok(3 / (0.2 + 0.15) < 10, "SLG below 3-phase when Z0 > Z1")

# ==== 静态稳定 ====
ws_m = 3000 * 2 * pi / 60
close(ws_m, 314.16, 0.0001, "314.16 rad/s")
KE = 0.5 * 30000 * ws_m ** 2
close(KE, 1.48e9, 0.001, "1.48e9 J")
ans("inertia-constant", KE / 300e6, 0.005)
d0 = asin(1 / 2.4)
ans("steady-angle", degrees(d0), 0.05)
ans("stability-reserve", (2.4 - 1) / 1)
Ks = 2.4 * cos(d0)
close(Ks, 2.18, 0.001, "Ks 2.18")
wn = sqrt(W * Ks / (2 * 5))
close(wn, 8.28, 0.001, "8.28 rad/s")
ans("oscillation-frequency", wn / (2 * pi), 0.005)
# simulate a small disturbance and measure the period
dd, om, t, h = d0 + 0.01, 0.0, 0.0, 1e-4
cross = []
prev = dd - d0
while t < 3:
    acc = W / (2 * 5) * (1 - 2.4 * sin(dd))
    om += acc * h
    dd += om * h
    t += h
    cur = dd - d0
    if prev > 0 >= cur:
        cross.append(t)
    prev = cur
close(1 / (cross[1] - cross[0]), wn / (2 * pi), 0.01, "simulated oscillation frequency")
ans("series-compensation", 1.2 / (0.5 - 0.1))
# M (SI) / S_N equals 2H/ws for a 2-pole machine (p = 1)
close(30000 * ws_m / 1 / 300e6, 2 * (KE / 300e6) / W, 1e-9, "M/S_N = 2H/ws")

# ==== 暂态稳定 ====
close(d0, 0.4298, 0.0005, "0.4298 rad")
close(pi - 2 * d0, 2.2820, 0.0005, "2.2820")
cdc = (pi - 2 * d0) * sin(d0) - cos(d0)
close(cdc, 0.042, 0.05, "cos dc 0.042")
dc = acos(cdc)
ans("critical-angle", degrees(dc), 0.05)
A1 = 1.0 * (dc - d0)
A2 = 2.4 * (cos(dc) - cos(pi - d0)) - 1.0 * (pi - d0 - dc)
close(A1, A2, 1e-9, "equal areas at the critical angle")
tc = sqrt(4 * 5 * (dc - d0) / (W * 1.0))
close(degrees(dc - d0), 63.0, 0.001, "63.0 deg")
close(dc - d0, 1.099, 0.001, "1.099 rad")
ans("critical-time", tc, 0.005)


def survives(t_clear, Pmax=2.4, Pm=1.0, H=5.0, h=1e-4):
    dd, om, t = asin(Pm / Pmax), 0.0, 0.0
    while t < 3:
        Pe = 0.0 if t < t_clear else Pmax * sin(dd)
        om += W / (2 * H) * (Pm - Pe) * h
        dd += om * h
        t += h
        if dd > pi:
            return False
    return True


ok(survives(tc - 0.005), "stable when cleared just before t_c")
ok(not survives(tc + 0.005), "unstable when cleared just after t_c")
acc0 = W * 1.0 / (2 * 5)
close(acc0, 31.4, 0.001, "31.4 rad/s^2")
close(0.5 * acc0 * 0.01, 0.157, 0.001, "0.157 rad")
ans("euler-step", degrees(0.5 * acc0 * 0.1 ** 2), 0.05)

# ==== 频率 ====
ans("droop-response", (0.1 / 50) / 0.05 * 1000)
KG = 1000 / (0.05 * 50)
close(KG, 400, 1e-12, "K_G 400 MW/Hz")
KL = 1.5 * 1000 / 50
close(KL, 30, 1e-12, "K_L 30")
df = 100 / (KG + KL)
close(df, 0.233, 0.001, "0.233 Hz")
close(KG * df, 93, 0.005, "93 MW")
close(KL * df, 7, 0.01, "7 MW")
ans("frequency-deviation", 150 / (800 + 60), 0.0005)

# ==== 电压 ====
ans("capacitor-voltage", 110 * 10 / 500)
close(1 - 0.9 ** 2, 0.19, 1e-12, "capacitor Q drops 19 % at 0.9 V")
close((112 - 6) * 11 / 10.5, 111.0, 0.0005, "tap example 111.0")
taps = [110 * (1 + k * 0.025) for k in (-2, -1, 0, 1, 2)]
for tv, ref in zip(taps, (104.5, 107.25, 110, 112.75, 115.5)):
    close(tv, ref, 1e-9, "tap list")
ok(min(taps, key=lambda v: abs(v - 111.05)) == 110, "nearest tap 110 kV")
ans("tap-voltage", (114 - 8) * 11 / 10.5, 0.05)
# Delta V / V = Delta Q / S_k: X_th = V^2/S_k
close((10 * (110 ** 2 / 500) / 110) / 110, 10 / 500, 1e-12, "dV/V = dQ/Sk")

# ==== 经济调度 ====
ans("incremental-cost", 0.02 * 200 + 10)
P1 = (20 - 10) / 0.06
P2 = 300 - P1
close(0.02 * P1 + 10, 0.04 * P2 + 8, 1e-12, "equal incremental")
close(P2, 133.3, 0.0005, "133.3 MW")
close(0.02 * P1 + 10, 13.33, 0.0005, "13.33")
ans("dispatch-p1", P1, 0.05)
# check optimality by brute force
best = min(((0.01 * p ** 2 + 10 * p) + (0.02 * (300 - p) ** 2 + 8 * (300 - p)), p) for p in [k / 10 for k in range(0, 3001)])
close(best[1], P1, 0.0005, "brute-force optimum")
P1b = 23 / 0.1
ans("dispatch-lambda", 0.04 * P1b + 6)
close(0.04 * P1b + 6, 0.06 * (400 - P1b) + 5, 1e-12, "lambda equal")
ans("dispatch-limit", 0.04 * 150 + 8)

# ==== 新能源并网 ====
ans("rocof", 500 * 50 / (2 * 5 * 10000))
close(500 * 50 / (2 * 2.5 * 10000), 0.5, 1e-12, "0.5 Hz/s when H halves")

# ==== 结业挑战 ====
ans("b-per-unit", 40 / (220 ** 2 / 100), 0.00005)
ans("b-ferranti", 1 / cos(beta * 300), 0.0005)
close(beta * 300, 0.317, 0.002, "0.317 rad")
ans("b-power-angle", degrees(asin(1.5 * 0.3 / 1.05)), 0.05)
ans("b-dc-flow", 1.2 * 0.2 / (0.2 + 0.2))
ans("b-three-phase", 25 * I220 / 1e3, 0.005)
ans("b-slg", 3 * 1 / (0.1 + 0.1 + 0.05))
ans("b-ll", sqrt(3) / 0.24, 0.005)
d0b = asin(1.1 / 2.2)
close(degrees(d0b), 30, 1e-9, "30 deg")
cb = (pi - 2 * d0b) * sin(d0b) - cos(d0b)
close(cb, 0.181, 0.002, "0.181")
ans("b-critical-angle", degrees(acos(cb)), 0.05)
ans("b-droop", (0.2 / 50) / 0.04 * 600)
P1c = 18 / 0.08
close(P1c, 225, 1e-12, "225 MW")
ans("b-dispatch", 0.03 * P1c + 9, 0.005)
ans("b-rocof", 1000 * 50 / (2 * 3 * 20000), 0.005)

# ---- automation review 2026-11-23: Ferranti worked example, 200 km ----
beta_ex = sqrt(0.4 * 2.8e-6)
close(beta_ex, 1.058e-3, 0.0005e-3, "ferranti example beta")
bl_ex = beta_ex * 200
close(bl_ex, 0.212, 0.0005, "ferranti example beta*l")
close(degrees(bl_ex), 12.1, 0.05, "ferranti example degrees")
close(1 / cos(bl_ex), 1.023, 0.0005, "ferranti example ratio")

# ---- compare with the pack ----
pack = Path(__file__).resolve().parents[2] / "data" / "content" / "E.3.3.yaml"
text = pack.read_text(encoding="utf-8")
pairs = re.findall(r"^\s*-?\s*id: ([a-z0-9-]+)\n(?:(?!^\s*-?\s*id: ).*\n)*?\s*answer: ([-0-9.e]+)", text, re.M)
answers = {i: float(v) for i, v in pairs}
missing = [i for i in computed if i not in answers]
assert not missing, f"computed but not in the pack: {missing}"
unchecked = [i for i in answers if i not in computed]
assert not unchecked, f"number answers in the pack without a check here: {unchecked}"
for i, (val, tol) in computed.items():
    pa = answers[i]
    if abs(pa - val) > max(tol, 1e-9 * max(1, abs(val))):
        raise AssertionError(f"{i}: pack answer {pa} but computed {val}")
    checks += 1

print(f"E.3.3 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
