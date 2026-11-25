"""N.1.2 大学物理：电磁学 — every number in data/content/N.1.2.yaml, recomputed.

Run: python -I tests/content/N.1.2.verify.py
Plain Python. Number answers are read back from the YAML and compared with the values computed here,
so a typo in either place fails; integrals the cards quote (line charge, ring, solenoid inductance, RC/RL
curves, LC oscillation) are checked numerically.
"""
import math
import re
from math import cos, exp, log, pi, radians, sin, sqrt
from pathlib import Path

k = 8.99e9
eps0 = 8.854e-12
mu0 = 4 * pi * 1e-7
e = 1.602e-19
me = 9.11e-31
checks = 0
computed = {}


def close(a, b, tol=1e-9, what=""):
    global checks
    if abs(a - b) > tol * max(1.0, abs(b)) and abs(a - b) > tol:
        raise AssertionError(f"{what}: {a} != {b}")
    checks += 1


def ans(item_id, value, tol=1e-9):
    computed[item_id] = (value, tol)


# ---- 库仑定律与电场 ----
ans("electron-count", 3.204e-9 / e / 1e10)
F = k * 2e-6 * 1e-6 / 0.3**2
ans("coulomb-force", F, 0.005)
close(F, 0.1998, 1e-3, "coulomb 0.20")
close(1 / (4 * pi * eps0), k, 1e-3, "k = 1/(4 pi eps0)")
ans("three-charges", k * 4e-12 / 0.2**2 - k * 4e-12 / 0.4**2, 0.005)
close(k * 4e-12 / 0.04, 0.899, 1e-3, "left push")
close(k * 4e-12 / 0.16, 0.225, 1e-3, "right push")
E1 = k * 2e-6 / 0.15**2
ans("point-field", E1 / 1e5, 0.005)
E2 = k * 1e-6 / 0.15**2
close(E2, 4.00e5, 1e-2, "E2 4.00e5")
close(E1 + E2, 1.20e6, 1e-2, "midpoint 1.20e6")
ans("midpoint-field", (k * 3e-6 / 0.01 - k * 1e-6 / 0.01) / 1e5, 0.005)
ans("dipole-torque", 6e-30 * 5e5 / 1e-24)
ans("line-charge-field", 2 * k * 2e-8 / 0.1, 1)
# line charge field by numerical integration (long but finite line)
lam, r = 2e-8, 0.1
N, Lh = 200000, 200.0
dz = 2 * Lh / N
Ey = sum(k * lam * dz * r / ((r * r + (-Lh + (i + 0.5) * dz) ** 2) ** 1.5) for i in range(N))
close(Ey, 2 * k * lam / r, 1e-3, "line charge integral")

# ---- 高斯定律 ----
ans("flux-angle", 500 * 0.2 * cos(radians(60)))
ans("gauss-flux", 2e-9 / eps0, 1)
close(2e-9 / eps0, 226, 1 / 226, "226")
close(k * 1e-9 * 0.05 / 0.1**3, 449, 1 / 449, "sphere inside 449")
close(k * 1e-9 / 0.2**2, 225, 1 / 225, "sphere outside 225")
ans("sphere-inside", k * 8e-9 * 0.1 / 0.2**3, 1)
close(8 * (0.1 / 0.2) ** 3, 1, what="enclosed 1 nC")
ans("parallel-plates-field", 8.854e-9 / eps0)
# flux of a point charge through a sphere is q/eps0 for any radius
for rr in (0.1, 1.0, 7.0):
    close(k * 1e-9 / rr**2 * 4 * pi * rr**2, 1e-9 / eps0, 1e-3, "sphere flux")

# ---- 电势与电容 ----
ans("pe-pair", k * 1e-12 / 0.09, 0.0005)
ans("work-from-v", 2e-6 * (12 - 2) / 1e-5)
v100 = sqrt(2 * e * 100 / me)
close(v100, 5.93e6, 0.01e6 / 5.93e6, "100 V electron 5.93e6")
v400 = sqrt(2 * e * 400 / me)
ans("electron-speed", v400 / 1e7, 0.005)
close(v400 / v100, 2, 1e-12, "400 V is twice the speed")
ans("uniform-v", 300 / 0.02)
ans("v-superposition", k * (4e-9 / 0.2 - 2e-9 / 0.2), 1)
close(-100 * 0.3, -30, what="card E from 50x^2")
ans("e-from-v", 15 * 2**2)
ans("equipotential-work", 0)
C = eps0 * 0.01 / 0.001
ans("plate-capacitance", C / 1e-12, 0.05)
close(C * 10, 8.85e-10, 0.01e-10 / 8.85e-10, "Q 8.85e-10")
close(0.5 * C * 100, 4.43e-9, 0.01e-9 / 4.43e-9, "W 4.43e-9")
close(0.5 * eps0 * (1e4) ** 2 * 1e-5, 0.5 * C * 100, 1e-12, "energy density check")
close(0.5 * eps0 * (1e4) ** 2, 4.43e-4, 0.01e-4 / 4.43e-4, "u 4.43e-4")
ans("series-parallel-c", 1 / (1 / 3 + 1 / 6) + 4)
ans("flash-energy", 0.5 * 200e-6 * 300**2)
close(9 / 1e-3, 9000, what="flash power")
ans("dielectric-c", 3.7 * 50)
ans("isolated-insert", 120 / 4)
ans("field-in-dielectric", 6000 / 2.5)

# ---- 电流与电阻 ----
ans("charge-through", 1.5 * 7200)
close(20 / e, 1.25e20, 0.01e20 / 1.25e20, "20 C electrons")
n_cu = 8.5e28
close(1 / (n_cu * e * 1e-6), 7.3e-5, 0.1e-5 / 7.3e-5, "drift 1 A")
ans("drift-speed", 3 / (n_cu * e * 2e-6) / 1e-4, 0.005)
ans("wire-resistance", 1.7e-8 * 10 / 1e-6)
ans("wire-heat", 2**2 * 0.17)
I1, I2 = 100e3 / 10e3, 100e3 / 100e3
close(I1**2 * 5, 500, what="loss at 10 kV")
close(I2**2 * 5, 5, what="loss at 100 kV")
ans("transmission-loss", (I1**2 * 5) / (I2**2 * 5))
ans("terminal-voltage", 1.5 - (1.5 / 3) * 0.5)
ans("series-parallel-r", 12 / (6 * 3 / 9 + 4))
# example: two sources; V_A from (V-12)/2 + (V-6)/2 + V/4 = 0
VA = 36 / 5
close(VA, 7.2, what="example VA")
close(VA / 4, 1.8, what="example I3")
close((VA - 12) / 2 + (VA - 6) / 2 + VA / 4, 0, 1e-12, "example KCL")
ans("kirchhoff-node", 3 + 1.5 - 2)
VB = 28 / 5
close((VB - 10) / 2 + (VB - 4) / 2 + VB / 4, 0, 1e-12, "two-source KCL")
ans("kirchhoff-two-source", VB)
close(10 / 0.001 - 100, 9900, what="card voltmeter")
ans("voltmeter-series", 5 / 0.002 - 50)
ans("rc-tau", 1e4 * 1e-4)
ans("rc-discharge", 10 * exp(-4 / 2), 0.005)
ans("rc-63", 12 * (1 - exp(-1)), 0.05)
close(1 - exp(-1), 0.632, 1e-3, "63.2%")
close(1 - exp(-5), 0.993, 1e-3, "5 tau > 99%")
close(exp(-1), 0.368, 1e-3, "36.8%")
ans("fuse-current", (1500 + 700) / 220)
close(220 / 1000, 0.22, what="body current")
# RC charging curve satisfies eps = IR + q/C (numerical derivative)
Rr, Cc, emf = 1e4, 1e-4, 12.0
for t in (0.1, 0.7, 2.3):
    q = Cc * emf * (1 - exp(-t / (Rr * Cc)))
    h = 1e-6
    dq = (Cc * emf * (1 - exp(-(t + h) / (Rr * Cc))) - Cc * emf * (1 - exp(-(t - h) / (Rr * Cc)))) / (2 * h)
    close(dq * Rr + q / Cc, emf, 1e-6, "RC loop law")

# ---- 磁场与安培定律 ----
ans("lorentz-force", e * 2e6 * 0.5 / 1e-13, 0.0005)
rad = me * 1e7 / (e * 1e-3)
ans("cyclotron-radius", rad * 100, 0.05)
close(rad, 0.0569, 1e-3, "0.0569 m")
ans("wire-force", 4 * 0.5 * 0.2)
ans("loop-torque", 50 * 2 * 0.02 * 0.3)
ans("hall-voltage", 5e-4 * 2 * 0.01 / 1e-6)
ans("velocity-selector", 3e4 / 0.1)
close(mu0 * 10 / (2 * pi * 0.05), 4e-5, 1e-12, "card 10 A at 5 cm")
ans("wire-field", mu0 * 20 / (2 * pi * 0.04) / 1e-5)
ans("parallel-wires", mu0 * 5 * 5 / (2 * pi * 0.1) / 1e-5)
ans("loop-center", mu0 * 2 / (2 * 0.1) / 1e-6, 0.005)
# ring field at the centre by Biot-Savart: each element is perpendicular to the radius
Rg, Ig, M = 0.1, 2.0, 100000
Bc = sum(mu0 / (4 * pi) * Ig * (2 * pi * Rg / M) / Rg**2 for _ in range(M))
close(Bc, mu0 * Ig / (2 * Rg), 1e-9, "ring by Biot-Savart")
# straight wire by Biot-Savart (long finite wire)
Iw, rw, Nw, Lw = 20.0, 0.04, 200000, 200.0
dzw = 2 * Lw / Nw
Bw = sum(mu0 / (4 * pi) * Iw * dzw * rw / ((rw * rw + (-Lw + (i + 0.5) * dzw) ** 2) ** 1.5) for i in range(Nw))
close(Bw, mu0 * Iw / (2 * pi * rw), 1e-3, "wire by Biot-Savart")
ans("ampere-enclosed", 3 + 3 - 5)
ans("solenoid-field", mu0 * 1000 * 2 / 1e-3, 0.005)

# ---- 电磁感应 ----
ans("faraday-avg", 100 * 0.5 * 0.01 / 0.1)
ans("motional-emf", 0.3 * 0.4 * 5)
Irod = 0.6 / 0.2
ans("rod-force", Irod * 0.4 * 0.3)
close(0.36 * 5, 0.6 * Irod, 1e-12, "rod power balance")
ans("induced-field", 0.1 / 2 * 0.2 / 1e-2)
w = 2 * pi * 50
ans("generator-peak", 200 * 0.1 * 0.05 * w, 0.05)
ans("back-emf", (120 - 100) / 2)
close(120 / 2, 60, what="start current")
ans("transformer", 1100 * 12 / 220)
ans("mutual-emf", 0.05 * 4 / 0.02)
L = mu0 * 1000**2 * 4e-4 / 0.5
ans("solenoid-l", L / 1e-3, 0.0005)
ans("inductor-energy", 0.5 * 0.2 * 3**2)
ans("rl-tau", 0.5 / 25 * 1000)
ans("rl-current", 2 * (1 - exp(-0.05 / 0.05)), 0.005)
f_lc = 1 / (2 * pi * sqrt(1e-3 * 10e-9))
ans("lc-frequency", f_lc / 1e3, 0.05)
close(f_lc, 50329, 1 / 50329, "50329 Hz")
ans("lc-energy", 10 * sqrt(2e-6 / 5e-3))
# LC oscillation: integrate q'' = -q/(LC) and compare with Q0 cos(wt); energy conserved
Lx, Cx, Q0 = 5e-3, 2e-6, 2e-6 * 10
wx = 1 / sqrt(Lx * Cx)
dt = 1e-8
q, i_ = Q0, 0.0
steps = int(round((2 * pi / wx) / 4 / dt))
for _ in range(steps):  # velocity Verlet over a quarter period
    a = -q / (Lx * Cx)
    q += i_ * dt + 0.5 * a * dt * dt
    a2 = -q / (Lx * Cx)
    i_ += 0.5 * (a + a2) * dt
close(abs(i_), 0.2, 1e-3, "LC quarter period current")
close(0.5 * Lx * i_**2 + q**2 / (2 * Cx), 0.5 * Cx * 100, 1e-4, "LC energy")

# ---- 麦克斯韦方程组 / 电磁波 ----
ans("displacement-current", eps0 * 2e11, 0.005)
c = 1 / sqrt(mu0 * eps0)
ans("speed-of-light", c / 1e8, 0.005)
close(mu0 * eps0, 1.1127e-17, 1e-3, "mu0 eps0")
close(c, 2.998e8, 1e-3, "c")
ans("wavelength", 3e8 / 100e6)
ans("e-to-b", 600 / 3e8 / 1e-6)
Iint = 600**2 / (2 * mu0 * 3e8)
ans("intensity", Iint, 1)
close(1360 / 3e8, 4.5e-6, 0.05e-6 / 4.5e-6, "sun pressure absorbed")
ans("radiation-pressure", 2 * 1360 / 3e8 / 1e-6, 0.005)
# the two halves of the energy density are equal when B = E/c
E0 = 600.0
close(0.5 * eps0 * E0**2, (E0 / c) ** 2 / (2 * mu0), 1e-9, "u_E = u_B")

# ---- 结业挑战 ----
ans("b-coulomb", k * 6e-12 / 0.04, 0.005)
ans("b-gauss", k * 2e-9 / 0.09, 1)
Cb = eps0 * 0.02 / 0.002
ans("b-capacitor", 0.5 * Cb * 50**2 / 1e-7, 0.005)
Ib = 9 / (2 + 1)
ans("b-circuit", Ib**2 * 2)
close(Ib**2 * 1, 9, what="internal loss")
ans("b-magnetic", mu0 * 15 / (2 * pi * 0.03) / 1e-5)
ans("b-faraday", 50 * (0.5 - 0.1) * 0.04 / 0.2)
fb = 1 / (2 * pi * sqrt(2e-3 * 8e-9))
ans("b-lc", fb / 1e3, 0.05)
close(sqrt(2e-3 * 8e-9), 4e-6, 1e-12, "sqrt LC")
ans("b-wave", 3e8 / 0.5 / 1e6)

# ---- compare with the pack ----
pack = Path(__file__).resolve().parents[2] / "data" / "content" / "N.1.2.yaml"
text = pack.read_text(encoding="utf-8")
pairs = re.findall(r"^\s*-?\s*id: ([a-z0-9-]+)\n(?:(?!^\s*-?\s*id: ).*\n)*?\s*answer: ([-0-9.e]+)", text, re.M)
answers = {i: float(a) for i, a in pairs}
missing = [i for i in computed if i not in answers]
assert not missing, f"computed but not in the pack: {missing}"
unchecked = [i for i in answers if i not in computed]
assert not unchecked, f"number answers in the pack without a check here: {unchecked}"
for i, (v, tol) in computed.items():
    pa = answers[i]
    if abs(pa - v) > max(tol, 1e-9 * max(1, abs(v))):
        raise AssertionError(f"{i}: pack answer {pa} but computed {v}")
    checks += 1

print(f"N.1.2 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
