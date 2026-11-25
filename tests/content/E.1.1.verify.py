"""E.1.1 电磁场与电磁波 — every number in data/content/E.1.1.yaml, recomputed.

Run: python -I tests/content/E.1.1.verify.py
Plain Python (no numpy). Where it is cheap, a formula taught in the pack is checked against an
independent calculation: the line-charge field by integrating Coulomb's law along the line, coax C and
L by integrating the field across the gap, curl and divergence by central differences, charge
relaxation by integrating dρ/dt step by step, the wave equation by finite differences, reflection and
transmission by solving the boundary conditions as linear equations, the Brewster angle from the
Fresnel TM coefficient, the short-dipole radiation resistance and directivity and the half-wave dipole
73 Ω by integrating the far-field power over a sphere. Every number answer is read back from the YAML
and compared.
"""
import cmath
import math
import re
from math import asin, atan, cos, degrees, exp, log, pi, radians, sin, sqrt
from pathlib import Path

checks = 0
computed = {}

E0 = 8.854e-12
MU0 = 4 * pi * 1e-7
C = 1 / sqrt(MU0 * E0)
ETA0 = sqrt(MU0 / E0)
C_ROUND = 2.998e8  # the value the prompts give


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


def simpson(f, a, b, n=2000):
    if n % 2:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


def gamma(zl, z0):
    return (zl - z0) / (zl + z0)


# ---- em-review ----
close(C, 2.998e8, 0.0005e8, "c from mu0 eps0")
close(MU0 * E0, 1.1127e-17, 0.0001e-17, "mu0 eps0")
close(sqrt(MU0 * E0), 3.336e-9, 0.001e-9, "sqrt")
ans("electron-force", 1.602e-19 * 1000 / 1e-16, 0.0005)
ans("light-speed", C / 1e8, 0.0005)
ans("wire-force", 2 * 0.5 * 0.1)
ans("earth-h", 50e-6 / MU0, 0.05)

# ---- gauss-electrostatics ----
def line_field(rho_l, r, half=2000.0):
    # Coulomb's law integrated along a long line (substitution z = r tan u keeps the integrand smooth)
    um = math.atan(half / r)
    return simpson(lambda u: rho_l / (4 * pi * E0) * cos(u) / r, -um, um, 4000)


e_line = line_field(1e-9, 0.1)
close(e_line, 1e-9 / (2 * pi * E0 * 0.1), 1e-4, "line charge: Coulomb integral = Gauss")
close(e_line, 180, 0.5, "≈ 180 V/m")
ans("point-charge", 1e-9 / (4 * pi * E0 * 0.09), 0.05)
h = 1e-5
D = lambda x, y, z: (2 * x, 3 * y, 0.0)
div = ((D(1 + h, 2, 3)[0] - D(1 - h, 2, 3)[0]) + (D(1, 2 + h, 3)[1] - D(1, 2 - h, 3)[1])) / (2 * h)
close(div, 5, 1e-6, "div D")
ans("div-d", 5)


def coax_c(eps_r, a, b):
    rho = 1e-9
    v = simpson(lambda r: rho / (2 * pi * eps_r * E0 * r), a, b)
    return rho / v


close(coax_c(2.25, 1e-3, 3.5e-3), 2 * pi * 2.25 * E0 / log(3.5), 1e-6, "coax C: integral = formula")
ans("coax-c", coax_c(2.25, 1e-3, 3.5e-3) * 1e12, 0.05)
ans("coax-air", coax_c(1, 1e-3, 2.3e-3) * 1e12, 0.05)

# ---- images-laplace ----
q, hh = 1e-9, 0.1
for x in (0.0, 0.05, 0.3):  # image pair gives zero potential on the plane
    r = sqrt(x * x + hh * hh)
    close(q / (4 * pi * E0 * r) - q / (4 * pi * E0 * r), 0, 1e-12, "potential zero on plane")
ans("image-force", q * q / (4 * pi * E0 * (2 * hh) ** 2) / 1e-7, 0.005)
close(8.988e9 * 1e-18 / 0.04 / 1e-7, 2.25, 0.005, "explain 8.988e9")
ans("plates", 10 / 0.002)

# ---- ampere-magnetostatics ----
close(MU0 * 5 / (2 * pi * 0.02), 50e-6, 1e-12, "50 uT")
ans("wire-b", MU0 * 20 / (2 * pi * 0.1) * 1e6, 0.001)
H = lambda x, y, z: (0.0, 3 * x, 0.0)
jz = (H(1 + h, 0, 0)[1] - H(1 - h, 0, 0)[1]) / (2 * h) - (H(1, h, 0)[0] - H(1, -h, 0)[0]) / (2 * h)
close(jz, 3, 1e-6, "curl H z")
ans("curl-j", 3)


def coax_l(a, b):
    i = 1.0
    flux = simpson(lambda r: MU0 * i / (2 * pi * r), a, b)
    return flux / i


close(coax_l(1e-3, 3.5e-3), MU0 / (2 * pi) * log(3.5), 1e-6, "coax L integral")
close(coax_l(1e-3, 3.5e-3) * 1e6, 0.251, 0.0005, "0.251 uH/m")
ans("coax-l-air", coax_l(1e-3, 2.3e-3) * 1e9, 0.5)
# two layers: same D, voltages add
e1 = 30 / (1e-3 + 1e-3 * 2 / 4)
close(e1, 20e3, 1e-9, "card 20 kV/m"); close(e1 * 2 / 4, 10e3, 1e-9, "card 10 kV/m")
e1 = 45 / (1e-3 + 1e-3 * 3 / 6)
ans("two-layer", e1 / 1e3)
close(e1 * 3 / 6 / 1e3, 15, 1e-9, "15 kV/m")

# ---- relaxation-skin ----
tau_cu = E0 / 5.8e7
close(tau_cu, 1.5e-19, 0.05e-19, "copper tau")
# step dρ/dt = -(σ/ε)ρ through one τ and compare with 1/e (seawater)
sig, eps = 4.0, 81 * E0
tau = eps / sig
rho, n = 1.0, 20000
dt = tau / n
for _ in range(n):  # RK4
    k1 = -sig / eps * rho
    k2 = -sig / eps * (rho + dt / 2 * k1)
    k3 = -sig / eps * (rho + dt / 2 * k2)
    k4 = -sig / eps * (rho + dt * k3)
    rho += dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
close(rho, exp(-1), 1e-9, "relaxation: 1/e after tau")
ans("relax-sea", tau / 1e-10, 0.005)
ans("relax-glass", 5 * E0 / 1e-12, 0.5)


def skin(f, sigma, mu=MU0):
    return 1 / sqrt(pi * f * mu * sigma)


d1 = skin(1e6, 5.8e7)
close(d1, sqrt(2 / (2 * pi * 1e6 * MU0 * 5.8e7)), 1e-12, "two forms of delta")
close(pi * 1e6 * MU0 * 5.8e7, 2.29e8, 0.005e8, "product 2.29e8"); close(sqrt(pi * 1e6 * MU0 * 5.8e7), 1.51e4, 0.005e4, "1.51e4")
close(d1 * 1e6, 66.1, 0.05, "66 um"); close(exp(-1), 0.37, 0.005, "1/e 37%")
close(skin(1e8, 5.8e7) * 1e6, 6.6, 0.05, "100 MHz 6.6 um")
ans("skin-50", skin(50, 5.8e7) * 1e3, 0.005)
ans("skin-2delta", exp(-2) * 100, 0.05)
close(skin(1e6, 5.8e7) / skin(1e8, 5.8e7), 10, 1e-9, "x100 f -> /10")

# ---- maxwell-differential ----
close(2 * pi * 1e9 * E0, 0.0556, 0.00005, "omega eps0")
ans("cu-ratio", 5.8e7 / (2 * pi * 1e9 * E0) / 1e9, 0.005)
ans("sea-ratio", 4 / (2 * pi * 1e6 * 81 * E0), 0.5)
close(4 / (2 * pi * 1e3 * 81 * E0), 9e5, 0.15e5, "seawater 1 kHz about 9e5")

# ---- media-boundaries ----
ans("water-d", 80 * E0 * 100 * 1e9, 0.05)
close(2 * 4 / 4, 2, 1e-12, "example E2y")
ans("boundary-en", 3 * 6 / 9)

# ---- poynting ----
close(0.5 * E0 * 1e12, 4.43, 0.005, "4.43 J/m3")
ans("energy-density", 0.5 * E0 * 9e12, 0.05)
a_, L_, V_, I_ = 1e-3, 1.0, 3.0, 2.0
Es, Hs = V_ / L_, I_ / (2 * pi * a_)
close(Hs, 318.3, 0.05, "318.3 A/m"); close(2 * pi * a_ * L_, 0.00628, 0.000005, "side area")
close(Es * Hs * 2 * pi * a_ * L_, V_ * I_, 1e-12, "Poynting = VI")
ans("wire-s", Es * Hs, 0.5)
avg = simpson(lambda t: 100 * cos(t) * 0.2 * cos(t), 0, 2 * pi) / (2 * pi)
ans("avg-s", avg, 1e-9)
for th in (0.3, pi / 2):  # out of phase by th: average is ½E0H0cos(th), zero at 90°
    av = simpson(lambda t: 100 * cos(t) * 0.2 * cos(t - th), 0, 2 * pi) / (2 * pi)
    close(av, 0.5 * 100 * 0.2 * cos(th), 1e-9, "phase-shifted average")

# ---- waves-time ----
v = 1 / sqrt(MU0 * E0)
f = lambda s: exp(-s * s)  # any shape: check f(z - vt) solves the 1-D wave equation by differences
z0, t0, dz = 0.3, 1e-9, 1e-3
dtt = dz / v
d2z = (f(z0 + dz - v * t0) - 2 * f(z0 - v * t0) + f(z0 - dz - v * t0)) / dz ** 2
d2t = (f(z0 - v * (t0 + dtt)) - 2 * f(z0 - v * t0) + f(z0 - v * (t0 - dtt))) / dtt ** 2
close(d2z, MU0 * E0 * d2t, 1e-6, "wave equation by differences")
ans("pulse-move", C_ROUND * 10e-9, 0.005)
ans("speed-er4", C_ROUND / sqrt(4) / 1e8, 0.005)
close(MU0 / E0, 1.419e5, 0.0005e5, "mu0/eps0")
ans("eta0", ETA0, 0.5)
ans("eta-er4", 376.7 / 2, 0.5)
close(377 / ETA0, 1.0, 0.001, "377 V/m gives about 1 A/m")

# ---- waves-frequency ----
ph = 5 * cmath.exp(-1j * pi / 2)
close(ph.real, 0, 1e-12, "phasor real"); close(ph.imag, -5, 1e-12, "phasor -5j")
close(C_ROUND / 1e9, 0.3, 0.001, "1 GHz wavelength 30 cm")
lam = C_ROUND / 2 / 1e9
close(2 * pi / lam, 41.9, 0.05, "k 41.9"); close(ETA0 / 2, 188.4, 0.05, "eta 188.4")
ans("lambda-er4", lam * 100, 0.05)
ans("h-er4", 10 / (376.7 / 2) * 1e3, 0.05)
ans("s-er4", 100 / (2 * 188.4), 0.0005)
close(100 / 188.4, 0.531, 0.0005, "forgot the 1/2")
for t in (0.1, 0.7, 2.0):  # circular: |E| constant
    close(cos(t) ** 2 + sin(t) ** 2, 1, 1e-12, "circular")
ans("pol-angle", degrees(atan(1 / 2)), 0.05)

# ---- tem-lines ----
close(C_ROUND / 50 / 1e3, 6000, 10, "50 Hz wavelength about 6000 km")
Lc, Cc = coax_l(1e-3, 3.5e-3), coax_c(2.25, 1e-3, 3.5e-3)
close(sqrt(Lc / Cc), 50.1, 0.05, "Z0 50.1"); close(1 / sqrt(Lc * Cc) / 1e8, 2.0, 0.005, "v 2.0e8")
close(Lc * Cc, MU0 * 2.25 * E0, 1e-6, "LC = mu eps")
close(0.1666e-6 / 66.79e-12, 2494, 1, "2494")
ans("z0-air", sqrt(0.1666e-6 / 66.79e-12), 0.05)
close(sqrt(coax_l(1e-3, 2.3e-3) / coax_c(1, 1e-3, 2.3e-3)), 49.9, 0.05, "air coax from geometry")
ans("v-coax", C_ROUND / 1.5 / 1e8, 0.005)
ans("elec-length", 1 / (2.0e8 / 1e8), 0.005)
close(1 / (C_ROUND / 1.5 / 1e8), 0.50, 0.005, "with exact v")
close(C_ROUND / 1.5 / 1e9, 0.2, 0.001, "1 GHz in cable about 20 cm")

# ---- line-junctions ----
def solve_reflection(zl, z0):
    # V+ + V- = ZL (V+ - V-)/Z0 with V+ = 1
    return (zl / z0 - 1) / (zl / z0 + 1)


ans("gamma-75", solve_reflection(75, 50))
g = gamma(100, 50)
close(g, 1 / 3, 1e-12, "1/3"); close((1 + g) / (1 - g), 2, 1e-12, "SWR 2"); close(g * g, 1 / 9, 1e-12, "1/9")
g = gamma(25, 50)
ans("swr-25", (1 + abs(g)) / (1 - abs(g)))
ans("refl-power", 0.2 ** 2 * 100)
tau_ = 1 + gamma(75, 50)
ans("tau-50-75", tau_)
close(tau_ ** 2 * 50 / 75 + 0.2 ** 2, 1, 1e-12, "power balance at the junction")


def zin(zl, z0, bl):
    t = math.tan(bl)
    return z0 * (zl + 1j * z0 * t) / (z0 + 1j * zl * t)


close(abs(zin(100, 50, pi / 2 - 1e-9) - 25), 0, 1e-6, "quarter-wave from the general formula")
ans("zin-quarter", 50 ** 2 / 100)
ok(abs(zin(1e-12, 50, pi / 2 - 1e-9)) > 1e6, "shorted quarter-wave looks open")
close(abs(zin(77, 50, pi - 1e-12) - 77), 0, 1e-6, "half-wave repeats the load")

# ---- matching-resonance ----
close(sqrt(50 * 100), 70.7, 0.05, "70.7")
ans("qw-200", sqrt(50 * 200))
close(zin(200, 100, pi / 2 - 1e-9).real, 50, 1e-6, "100-ohm quarter-wave gives 50")
close(125 ** 2 / 200, 78, 0.2, "arithmetic mean mistake 78")
close(C_ROUND / 2e9, 0.150, 0.0005, "2 GHz air wavelength"); close(C_ROUND / 2e9 / 4 * 100, 3.75, 0.005, "3.75 cm")
ans("qw-length", C_ROUND / 1.5 / 1e9 / 4 * 100, 0.05)
close(C_ROUND / 1e9 / 4 * 100, 7.5, 0.005, "vacuum quarter 7.5 cm")
q_ = (1 + 2j) / (3 + 2j)
close(q_.real, 7 / 13, 1e-12, "complex division card (real)"); close(q_.imag, 4 / 13, 1e-12, "complex division card (imag)")
close(((1 + 2j) * (3 - 2j)).real, 7, 1e-12, "numerator 7"); close(((3 + 2j) * (3 - 2j)).real, 13, 1e-12, "denominator 13")
zn = (100 + 50j) / 50
gm = (zn - 1) / (zn + 1)
close(gm.real, 0.4, 1e-12, "0.4"); close(gm.imag, 0.2, 1e-12, "0.2")
ans("smith-gamma", abs(gm), 0.0005)
ans("res-half", C_ROUND / (2 * 0.5) / 1e6, 0.5)
ans("q-bw", 300 / 0.3)

# ---- normal-incidence ----
g = gamma(ETA0 / 2, ETA0)
close(g, -1 / 3, 1e-12, "-1/3"); close(1 - g * g, 8 / 9, 1e-12, "89%")
# solve the boundary conditions directly: 1 + r = t (E tangential), (1 - r)/eta1 = t/eta2 (H tangential)
def normal(eta1, eta2):
    r = (eta2 - eta1) / (eta2 + eta1)
    t = 1 + r
    if eta2:
        close((1 - r) / eta1, t / eta2, 1e-12, "H continuity")
    else:
        close(t, 0, 1e-12, "no field inside a perfect conductor")
    return r


ans("glass-r", normal(ETA0, ETA0 / 1.5) ** 2 * 100, 1e-9)
ans("er9-r", normal(ETA0, ETA0 / 3) ** 2 * 100, 1e-9)
close(normal(ETA0, 0.0), -1, 1e-12, "perfect conductor")
d = skin(1e6, 5.8e7)
close(abs((1 + 1j) / (5.8e7 * d)), 0.00037, 0.000005, "copper eta at 1 MHz")
ans("power-1pct", log(100) / 2, 0.005)
close(log(100), 4.61, 0.005, "amplitude 1% at 4.61 delta")
e_ch, m_e = 1.602176634e-19, 9.1093837015e-31
fp = sqrt(1e12 * e_ch ** 2 / (E0 * m_e)) / (2 * pi)
close(fp / sqrt(1e12), 8.98, 0.005, "fp = 8.98 sqrt(N)")
ans("plasma-fp", 8.98 * sqrt(1e12) / 1e6, 0.005)
close(1 - (9 / 100) ** 2, 0.9919, 1e-9, "plasma eps_r at 100 MHz"); ok(1 - (9 / 1) ** 2 < 0, "1 MHz eps_r < 0")

# ---- oblique-incidence ----
ans("snell-30", degrees(asin(sin(radians(30)) / 1.5)), 0.05)
close(degrees(asin(1 / 1.5)), 41.8, 0.05, "glass critical 41.8")
tc = degrees(asin(1 / 1.33))
ans("critical-water", tc, 0.5)
close(2 * tc, 98, 0.6, "cone about 98 degrees")


def r_tm(n1, n2, th1):
    th2 = asin(n1 * sin(th1) / n2)
    return (n2 * cos(th1) - n1 * cos(th2)) / (n2 * cos(th1) + n1 * cos(th2))


def r_te(n1, n2, th1):
    th2 = asin(n1 * sin(th1) / n2)
    return (n1 * cos(th1) - n2 * cos(th2)) / (n1 * cos(th1) + n2 * cos(th2))


tb = atan(2)
close(degrees(tb), 63.4, 0.05, "63.4"); close(r_tm(1, 2, tb), 0, 1e-12, "TM zero at Brewster (er 4)")
ok(abs(r_te(1, 2, tb)) > 0.1, "TE not zero at Brewster")
tb = atan(1.5)
close(r_tm(1, 1.5, tb), 0, 1e-12, "TM zero at Brewster (glass)")
ans("brewster-glass", degrees(tb), 0.05)
ok(all(abs(r_te(1, 1.5, radians(x))) > 1e-3 for x in range(1, 90)), "TE never zero (nonmagnetic)")

# ---- waveguides ----
ans("pp-cutoff", C_ROUND / (2 * 0.01) / 1e9, 0.05)
a, b = 22.86e-3, 10.16e-3
fc = lambda m, n: C_ROUND / 2 * sqrt((m / a) ** 2 + (n / b) ** 2)
close(fc(2, 0) / 1e9, 13.1, 0.05, "13.1"); close(fc(0, 1) / 1e9, 14.8, 0.05, "14.8")
ok(fc(1, 0) < fc(2, 0) < fc(0, 1) < fc(1, 1), "mode order")
ans("wr90-te10", fc(1, 0) / 1e9, 0.005)
ans("wr90-te20", fc(2, 0) / 1e9, 0.005)
lam = C_ROUND / 10e9
close(lam * 1e3, 29.98, 0.005, "29.98 mm"); close(6.557 / 10, 0.656, 0.0005, "fc/f")
close(sqrt(1 - 0.6557 ** 2), 0.755, 0.0005, "0.755")
ans("guide-lambda", lam / sqrt(1 - (6.557e9 / 10e9) ** 2) * 1e3, 0.05)

# ---- cavities ----
dcav = 30e-3
close(sqrt(1 / a ** 2 + 1 / dcav ** 2), 55.0, 0.05, "55.0")
ans("cavity-101", C_ROUND / 2 * sqrt(1 / a ** 2 + 1 / dcav ** 2) / 1e9, 0.005)
ans("cavity-cube", C_ROUND / 2 * sqrt(2) / 0.03 / 1e9, 0.005)
# card "为什么微波频段用腔体": 10 GHz wavelength 3 cm, a tenth of it is 3 mm, copper skin depth 0.66 um
close(C_ROUND / 10e9 * 100, 3.0, 0.005, "10 GHz wavelength 3 cm")
close(C_ROUND / 10e9 / 10 * 1e3, 3.0, 0.005, "lambda/10 = 3 mm")
close(skin(10e9, 5.8e7) * 1e6, 0.66, 0.005, "copper skin depth at 10 GHz 0.66 um")
ans("cavity-q", 10e9 / 1e6)
close(sqrt(1e-9 * 1e-12), 3.16e-11, 0.005e-11, "sqrt LC"); close(2 * pi * sqrt(1e-21), 1.99e-10, 0.005e-10, "2pi sqrt LC")
ans("rlc-f0", 1 / (2 * pi * sqrt(1e-9 * 1e-12)) / 1e9, 0.005)

# ---- radiation ----
def short_dipole_rrad(dl_over_lam):
    # P = ∮ |E|²/(2η) dS with E = η k I Δl sinθ / (4πr), I = 1, r = 1
    k = 2 * pi
    p = simpson(lambda th: (ETA0 * k * dl_over_lam * sin(th) / (4 * pi)) ** 2 / (2 * ETA0) * 2 * pi * sin(th), 0, pi)
    return 2 * p


close(short_dipole_rrad(1 / 50), 80 * pi ** 2 / 2500, 0.001, "80 pi^2 rule vs integral")
ans("rrad-50", 80 * pi ** 2 * (1 / 50) ** 2, 0.005)
close(80 * pi ** 2 * (1 / 50) ** 2, 0.316, 0.0005, "0.316")
ans("eff-short", 0.316 / 1.316 * 100, 0.5)
# directivity of the short dipole: 4π max / ∮ sin²θ dΩ
dir_ = 4 * pi / simpson(lambda th: sin(th) ** 2 * 2 * pi * sin(th), 0, pi)
close(dir_, 1.5, 1e-9, "directivity 1.5")
# half-wave dipole about 73 ohm
hw = ETA0 / (2 * pi) * simpson(lambda th: cos(pi / 2 * cos(th)) ** 2 / sin(th) if sin(th) > 1e-12 else 0.0, 0, pi, 20000)
close(hw, 73, 0.5, "half-wave dipole 73 ohm")
# triangular current (short dipole fed at the centre): far field ∝ ∫I dz, half of the uniform case, power 1/4
tri = simpson(lambda zz: 1 - abs(zz), -1, 1) / 2
close(tri ** 2 * 80 * pi ** 2, 20 * pi ** 2, 1e-9, "20 pi^2 for the triangular distribution")
lam = C_ROUND / 3e8
close(lam, 0.999, 0.0005, "300 MHz wavelength"); close(1.5 * lam ** 2 / (4 * pi), 0.119, 0.0005, "0.119 m2")
close(1.5 * lam ** 2 / (4 * pi) * 1e4, 1190, 5, "about 1190 cm2")
lam = C_ROUND / 1e9
close(lam ** 2, 0.0899, 0.00005, "lambda^2")
ans("ae-dipole", 1.5 * lam ** 2 / (4 * pi) * 1e4, 0.5)
af = lambda psi: abs(1 + cmath.exp(1j * 2 * pi * 0.5 * cos(psi)))
close(af(0), 0, 1e-12, "array null along the axis"); close(af(pi / 2), 2, 1e-12, "array max broadside")

# ---- boss ----
ans("b-line", 2e-9 / (2 * pi * E0 * 0.2), 0.5)
ans("b-coax-l", coax_l(0.5e-3, 2e-3) * 1e9, 0.5)
ans("b-skin", skin(1e6, 3.5e7) * 1e6, 0.05)
ans("b-lambda", C_ROUND / 3 / 3e9 * 100, 0.005)
g = gamma(150, 50)
ans("b-swr", (1 + g) / (1 - g))
ans("b-qw", sqrt(50 * 72))
ans("b-normal", normal(ETA0, ETA0 / 4) ** 2 * 100, 1e-9)
close(r_tm(1, sqrt(3), atan(sqrt(3))), 0, 1e-12, "boss Brewster")
ans("b-brewster", degrees(atan(sqrt(3))), 0.05)
ans("b-te10", C_ROUND / (2 * 15.8e-3) / 1e9, 0.005)
ans("b-rrad", 80 * pi ** 2 / 400, 0.005)

# ---- compare with the pack ----
pack = Path(__file__).resolve().parents[2] / "data" / "content" / "E.1.1.yaml"
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

print(f"E.1.1 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
