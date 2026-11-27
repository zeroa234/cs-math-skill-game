"""N.2.2 固体与半导体物理 — every number in data/content/N.2.2.yaml, recomputed.

Run: python -I tests/content/N.2.2.verify.py [path/to/N.2.2.yaml]
Plain Python. Number answers are read back from the YAML and compared with the values computed here, so a
typo in either place fails. Formulas the cards quote are checked independently where that is possible:
reciprocal lattices by solving a_i·b_j = 2πδ_ij with a 3×3 inverse (simple cubic, FCC → BCC, BCC → FCC,
triangular), the lattice Fourier sum term by term, the Fermi sphere by counting k-points in a box, effective
masses by numerical second derivatives, the Kronig–Penney right-hand side, Nc by integrating g(E) times the
Boltzmann factor, F_1/2 by Simpson's rule, the compensated-doping quadratic by charge neutrality, the
built-in field by checking that drift and diffusion currents cancel, carrier decay by RK4, the diffusion
length by checking the ODE, the depletion width by integrating Poisson's equation, and the diode and
breakdown formulas from their definitions.
"""
import cmath
import math
import re
import sys
from math import asin, degrees, exp, log, pi, radians, sin, sqrt
from pathlib import Path

checks = 0
computed = {}


def close(a, b, tol=1e-9, what=""):
    global checks
    if abs(a - b) > tol * max(1.0, abs(b)) and abs(a - b) > tol:
        raise AssertionError(f"{what}: {a} != {b}")
    checks += 1


def ans(item_id, value, tol=1e-9):
    computed[item_id] = (value, tol)


def simpson(f, a, b, n=4000):
    if n % 2:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


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


def inv3(M):
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    co = [[e * i - f * h, -(d * i - f * g), d * h - e * g],
          [-(b * i - c * h), a * i - c * g, -(a * h - b * g)],
          [b * f - c * e, -(a * f - c * d), a * e - b * d]]
    return [[co[j][k] / det for j in range(3)] for k in range(3)]  # transpose of cofactors / det


def reciprocal(a1, a2, a3):
    # rows of B satisfy a_i · b_j = 2π δ_ij  ->  B = 2π (A^-1)^T
    A = [a1, a2, a3]
    Ai = inv3(A)
    B = [[2 * pi * Ai[r][j] for r in range(3)] for j in range(3)]
    for i in range(3):
        for j in range(3):
            close(sum(A[i][k] * B[j][k] for k in range(3)), 2 * pi if i == j else 0.0, 1e-9, "a·b")
    return B


norm = lambda v: sqrt(sum(x * x for x in v))

# constants used in the pack
q = 1.602e-19
h = 6.626e-34
hbar = 1.0546e-34
m0 = 9.109e-31
kB = 1.381e-23
kB_eV = 8.617e-5
VT = 0.02585  # kT/q at 300 K, as in the original exercise
eps = 11.7 * 8.854e-14  # F/cm
close(eps, 1.036e-12, 0.001, "ε_Si")
close(kB_eV * 300, VT, 0.0002, "kT at 300 K")
A_free = hbar**2 / (2 * m0) / q * 1e18  # eV nm²
close(A_free, 0.0381, 0.001, "ħ²/2m = 0.0381 eV nm²")
E_well = h**2 / (8 * m0 * 1e-18) / q  # eV, 1 nm well
close(E_well, 0.376, 0.001, "0.376 eV")
HC = 1240.0
ni = 1e10

# ==== 晶体结构 ====
ans("fcc-points", 8 / 8 + 6 / 2)
ans("bcc-points", 8 / 8 + 1)
a_si = 0.5431e-7
close(8 / a_si**3, 4.99e22, 0.001, "Si atom density")
close(a_si**3, 1.602e-22, 0.001, "a³")
ans("si-neighbor", norm([0.25 * 0.5431] * 3), 0.0005)
a_gaas = 0.5653e-7
close(a_gaas**3, 1.806e-22, 0.001, "GaAs a³")
ans("gaas-density", 4 / a_gaas**3 / 1e22, 0.005)
close(8 / a_gaas**3, 4.43e22, 0.001, "GaAs total")

# ==== 晶面和布拉格 ====
d111 = 0.5431 / sqrt(3)
ans("si-d111", d111, 0.0001)
close(0.40 / sqrt(2), 0.2828, 0.0002, "d110")
close(0.154 / (2 * 0.40 / sqrt(2)), 0.2722, 0.0002, "sinθ")
close(degrees(asin(0.154 / (2 * 0.40 / sqrt(2)))), 15.8, 0.003, "15.8°")
ans("bragg-sc100", degrees(asin(0.154 / (2 * 0.5))), 0.01)
ans("bragg-second", degrees(asin(2 * 0.154 / (2 * 0.5))), 0.01)
ans("measure-a", sqrt(3) * 0.15406 / (2 * sin(radians(14.22))), 0.0005)
for lam, ok in ((0.15, True), (0.60, True), (0.70, False)):
    assert (lam / (2 * 0.31) <= 1) == ok
    checks += 1
close(degrees(asin(0.15 / 0.62)), 14.0, 0.005, "0.15 nm angle")
close(degrees(asin(0.60 / 0.62)), 75.4, 0.005, "0.60 nm angle")
# miller (320): reciprocals of 2, 3, ∞
from fractions import Fraction
r = [Fraction(1, 2), Fraction(1, 3), Fraction(0)]
lcm = 6
assert [int(x * lcm) for x in r] == [3, 2, 0]
checks += 1

# ==== 倒格子 ====
ans("g-shortest-1d", 2 * pi / 0.5, 0.005)
close(2 * pi / 0.3, 20.9, 0.003, "20.9")
close(2 * pi / 0.6, 10.5, 0.003, "10.5")


def S(k, N, a=1.0):
    return sum(cmath.exp(-1j * k * n * a) for n in range(N))


ans("sum-pi-over-a", S(pi, 5).real, 1e-9)
assert abs(S(pi, 5).imag) < 1e-9 and abs(S(2 * pi, 5) - 5) < 1e-9
checks += 1
ans("sum-at-g", abs(S(2 * pi, 1000)) ** 2 / 1e6, 1e-6)
ans("fold-back", 10 - 2 * pi / 0.5, 0.005)
# 3D
B = reciprocal([0.4, 0, 0], [0, 0.4, 0], [0, 0, 0.6])
ans("tetragonal-shortest", min(norm(b) for b in B), 0.005)
B = reciprocal([0.246, 0, 0], [0.123, 0.246 * sqrt(3) / 2, 0], [0, 0, 1.0])
ans("graphene-b", norm(B[0]), 0.02)
close(norm(B[1]), norm(B[0]), 1e-9, "|b2| = |b1|")
cosang = sum(B[0][i] * B[1][i] for i in range(3)) / (norm(B[0]) * norm(B[1]))
close(degrees(math.acos(cosang)), 120, 1e-9, "120° between b1, b2")
close(2 * pi / 0.246, 25.5, 0.002, "2π/a for graphene")
# FCC lattice with cubic constant a -> reciprocal primitive vectors are BCC with cubic constant 4π/a
a = 1.0
Bf = reciprocal([0, a / 2, a / 2], [a / 2, 0, a / 2], [a / 2, a / 2, 0])
for b in Bf:  # each is (2π/a)(±1, ±1, ±1) = half body diagonal of a cube of side 4π/a
    assert all(abs(abs(x) - 2 * pi / a) < 1e-9 for x in b)
checks += 1
# BCC (cubic a) -> FCC with cubic constant 4π/a: primitive b = (2π/a)(0,1,1) etc. = face centres of cube 4π/a
abcc = 0.30
Bb = reciprocal([-abcc / 2, abcc / 2, abcc / 2], [abcc / 2, -abcc / 2, abcc / 2], [abcc / 2, abcc / 2, -abcc / 2])
for b in Bb:
    nz = sorted(abs(x) for x in b)
    close(nz[0], 0, 1e-9, "bcc->fcc zero")
    close(nz[2], 2 * pi / abcc, 1e-9, "bcc->fcc face centre")
ans("bcc-reciprocal-size", 2 * (2 * pi / abcc), 0.02)  # cube side = twice the face-centre offset
ans("g111-si", 2 * pi / 0.3136, 0.01)
close(2 * pi * sqrt(3) / 0.5431, 2 * pi / d111, 1e-9, "|G| = 2π/d")
# G(1,1,0) ⟂ (110), lies in (1-10)
assert sum(x * y for x, y in zip((1, 1, 0), (1, -1, 0))) == 0
checks += 1

# ==== 自由电子 ====
ans("k-count", round((2 * pi / 1) / (2 * pi / 1000)))
close(2 * pi / 1.0, 6.28, 0.001, "2π/L in cm⁻¹")
# Fermi sphere: count k points to confirm N = 2·(4/3 π kF³)/(2π/L)³ with L = 1 (units 2π)
R = 25
cnt = sum(1 for x in range(-R, R + 1) for y in range(-R, R + 1) for z in range(-R, R + 1) if x * x + y * y + z * z <= R * R)
close(cnt, 4 / 3 * pi * R**3, 0.01, "lattice points in sphere")


def fermi(n_m3):
    kF = (3 * pi**2 * n_m3) ** (1 / 3)
    return kF, (hbar * kF) ** 2 / (2 * m0) / q, hbar * kF / m0


kF, EF, vF = fermi(8.47e28)
close(kF, 1.36e10, 0.002, "Cu kF")
close(hbar * kF, 1.433e-24, 0.001, "ħkF")
close(EF * q, 1.13e-18, 0.003, "Cu EF J")
close(EF, 7.03, 0.001, "Cu EF")
close(vF, 1.57e6, 0.002, "Cu vF")
kFn, EFn, _ = fermi(2.65e28)
close(kFn, 9.22e9, 0.001, "Na kF")
close(EFn * q, 5.19e-19, 0.002, "Na EF J")
ans("sodium-ef", EFn, 0.005)
ans("ef-scaling", 8 ** (2 / 3), 1e-9)
close(0.026 / 7, 0.0037, 0.02, "kT/EF < 1%")

# ==== 周期势 ====
ans("bloch-phase", cmath.exp(1j * pi * 3).real, 1e-9)
close(E_well / 0.5**2, 1.504, 0.001, "boundary 0.5 nm")
close(E_well / 0.5**2 - 0.2, 1.304, 0.001, "lower")
close(E_well / 0.5**2 + 0.2, 1.704, 0.001, "upper")
close(E_well / 0.4**2, 2.35, 0.001, "boundary 0.4 nm")
ans("upper-band-bottom", E_well / 0.4**2 + 0.3, 0.005)
close(E_well / 0.4**2 - 0.3, 2.05, 0.001, "lower 0.4")
# boundary energy equals ħ²(π/a)²/2m
close((hbar * pi / 0.5e-9) ** 2 / (2 * m0) / q, 1.504, 0.001, "ħ²(π/a)²/2m")
P = 3 * pi / 2
rhs = lambda aa: math.cos(aa) + P * sin(aa) / aa
close(rhs(pi / 2), 3, 1e-9, "KP rhs π/2")
close(rhs(pi), -1, 1e-9, "KP rhs π")
ans("states-per-band", 2 * 1e22 / 1e22)

# ==== 能带填充 ====
ans("si-bands-filled", 2 * 4 / 2)
close(exp(-1.12 / (2 * VT)), 3.9e-10, 0.02, "Si e^-Eg/2kT")
assert 1e-47 < exp(-5.5 / (2 * VT)) < 1e-45
checks += 1
ans("photon-momentum", (h / 1e-6) / (hbar * pi / 0.543e-9) / 1e-3, 0.005)
ans("gaas-cutoff", HC / 1.42, 0.5)
close(HC / 1.12, 1107, 0.001, "Si cutoff")

# ==== 电子和空穴 ====
ans("excess-energy", 1.5 - 1.12, 1e-9)
ans("pair-count", 1)

# ==== 有效质量 ====
ans("gaas-mass", A_free / 0.569, 0.0005)
ans("accel-ratio", 1 / 0.067, 0.05)


def d2(f, x, hh=1e-4):
    return (f(x + hh) - 2 * f(x) + f(x - hh)) / hh**2


for t, a_, key, tol in ((1.0, 0.3, None, 0), (0.5, 0.4, "tb-mass", 0.002), (0.8, 0.25, "b-tb-mass", 0.002)):
    E = lambda k: -2 * t * math.cos(k * a_)
    curv = d2(E, 0.0)  # eV nm²
    mratio = A_free / (curv / 2)  # E ≈ ħ²k²/2m* -> curv = 2·ħ²/2m*
    close(mratio, A_free / (t * a_**2), 1e-5, "tight binding m*")
    close(d2(E, pi / a_), -curv, 1e-5, "negative at top")
    if key:
        ans(key, mratio, tol)
    else:
        close(mratio, 0.423, 0.001, "tb example 0.423")
ans("si-conductivity-mass", 3 / (1 / 0.98 + 2 / 0.19), 0.002)
close(1 / 0.98 + 2 / 0.19, 11.55, 0.001, "11.55")

# ==== 本征 ====
ans("fraction-ionized", 5e22 / ni / 1e12)
x = 1.12 / (2 * kB_eV)
close(x, 6499, 0.0005, "Eg/2k")
ans("ni-400k", exp(x * (1 / 300 - 1 / 400)), 1)
close((4 / 3) ** 1.5, 1.54, 0.002, "(4/3)^1.5")
close(exp(x * (1 / 300 - 1 / 400)) * (4 / 3) ** 1.5, 350, 0.02, "≈ 350")
close(exp((1.12 - 0.66) / (2 * VT)), 7.3e3, 0.01, "Ge/Si exponential")
ans("mass-action-p", ni**2 / 1e15 / 1e5)
close(ni**2 / 1e16, 1e4, 1e-9, "p = 1e4")

# ==== 掺杂 ====
close(5e22 / 1e6, 5e16, 1e-9, "1 ppm")
close(5e16 / ni, 5e6, 1e-9, "5 million times")
ans("donor-hydrogen", 13.6 * 0.26 / 11.7**2, 0.0001)
close(0.0529 * 11.7 / 0.26, 2.4, 0.01, "donor radius")
atoms_in_orbit = 4 / 3 * pi * (0.0529 * 11.7 / 0.26) ** 3 * 8 / 0.5431**3
assert 2000 < atoms_in_orbit < 4000  # "几千个硅原子"
checks += 1
ans("p-type-minority", ni**2 / 2e17, 0.5)


def n_of(Nd, Na, ni_=ni):
    half = (Nd - Na) / 2
    n = half + sqrt(half**2 + ni_**2)
    p = ni_**2 / n
    close(n + Na, p + Nd, 1e-9, "charge neutrality")  # all ionized
    return n, p


n_c, p_c = n_of(3e16, 1e16)
ans("compensated", p_c, 1)
close(ni**2 / 3e16, 3.3e3, 0.02, "wrong 3.3e3")
n_l, _ = n_of(1e10, 0)
ans("light-doping", n_l / 1e10, 0.001)
n_h, _ = n_of(1e14, 0, ni_=1.43e15)
assert 1.4e15 < n_h < 1.6e15
checks += 1
ni600 = 1e10 * 2 ** 1.5 * exp(x * (1 / 300 - 1 / 600))
assert ni600 > 1e15  # with a constant gap; the shrinking gap only raises it
checks += 1

# ==== 态密度 ====
ms = 1.08 * m0
Nbelow = (2 * ms * 0.1 * q / hbar**2) ** 1.5 / (3 * pi**2)
close(2 * ms * 0.1 * q / hbar**2, 2.83e18, 0.002, "2m*E/ħ²")
close((2 * ms * 0.1 * q / hbar**2) ** 1.5, 4.77e27, 0.002, "^1.5")
ans("states-below", Nbelow * 1e-6 / 1e20, 0.005)
g = lambda E: (2 * ms / hbar**2) ** 1.5 * sqrt(max(E, 0)) / (2 * pi**2)  # per J per m³
close(simpson(g, 0, 0.1 * q, 20000), Nbelow, 0.001, "∫g = N(E)")
ans("dos-ratio", sqrt(0.04 / 0.01))
close((0.067 / 1.08) ** 1.5, 0.01545, 0.001, "GaAs/Si DOS")
kT = kB * 300
Nc_formula = 2 * (2 * pi * ms * kT / h**2) ** 1.5
Nc_integral = simpson(lambda E: g(E) * exp(-E / kT), 0, 40 * kT, 20000)
close(Nc_integral, Nc_formula, 0.002, "Nc = ∫ g e^(-E/kT)")
close(Nc_formula * 1e-6, 2.82e19, 0.002, "Nc Si")
close(2 * (2 * pi * 0.81 * m0 * kT / h**2) ** 1.5 * 1e-6, 1.83e19, 0.003, "Nv Si")
ans("nc-400", 2.8 * (400 / 300) ** 1.5, 0.005)
ans("nc-gaas", 2.82e19 * (0.067 / 1.08) ** 1.5 / 1e17, 0.01)
close(2 * (2 * pi * 0.067 * m0 * kT / h**2) ** 1.5 * 1e-6 / 1e17, 4.35, 0.002, "GaAs Nc direct")
# worked example: GaAs states within 0.1 eV
xg = 2 * 0.067 * m0 * 0.1 * q / hbar**2
close(xg, 1.76e17, 0.002, "GaAs 2m*E/ħ²")
close(xg**1.5, 7.37e25, 0.002, "GaAs ^1.5")
close(3 * pi**2, 29.6, 0.001, "3π²")
close(xg**1.5 / (3 * pi**2), 2.49e24, 0.002, "GaAs N(E) m⁻³")
# N_v with the smaller hole mass some books use (0.56 m) is about 1.0e19
close(2 * (2 * pi * 0.56 * m0 * kT / h**2) ** 1.5 * 1e-6, 1.0e19, 0.06, "Nv with 0.56 m")

# ==== 费米–狄拉克 ====
f = lambda dE: 1 / (1 + exp(dE))
ans("f-2kt", f(2), 0.0005)
ans("f-01ev", f(0.1 / VT), 0.0001)
close(exp(0.1 / VT), 47.9, 0.001, "47.9")
ans("empty-3kt", 1 - f(-3), 0.0005)
close(f(3), 0.0474, 0.001, "3kT exact")
close(exp(-3), 0.0498, 0.001, "3kT Boltzmann")
ans("boltzmann-02", exp(-0.2 / VT) / 1e-4, 0.005)
close(log(99), 4.595, 0.0001, "ln 99")
close(log(99) * VT, 0.119, 0.002, "1 % level")
ans("f-0001", bisect(lambda xx: f(xx / VT) - 0.001, 0, 1), 0.0005)
close(log(999), 6.907, 0.0001, "ln 999")

# ==== 载流子浓度 ====
ans("ef-1e16", VT * log(2.8e19 / 1e16), 0.0005)
close(log(2800), 7.937, 0.0002, "ln 2800")
ni_calc = sqrt(2.8e19 * 1.8e19) * exp(-1.12 / (2 * VT))
close(sqrt(2.8e19 * 1.8e19), 2.245e19, 0.001, "√NcNv")
close(exp(-1.12 / (2 * VT)), 3.91e-10, 0.002, "e^-21.66")
ans("ni-from-nc", ni_calc / 1e9, 0.02)
close(1e10 / ni_calc - 1, 0.14, 0.03, "12 % low")  # 8.77e9 is 12 % below 1e10 (1e10 is 14 % above)
close(VT / 2 * log(1.8 / 2.8), -0.0057, 0.01, "Si Ei shift")
ans("ei-gaas", VT / 2 * 1.5 * log(0.48 / 0.067) * 1e3, 0.05)
close(VT * log(280), 0.146, 0.002, "Ec-EF 1e17")
close(VT * log(1e7), 0.417, 0.001, "EF-Ei 1e17")
close(VT * log(280) + VT * log(1e7), 0.56, 0.01, "half gap")
ans("ef-p-type", VT * log(1.8e19 / 1e15), 0.0005)


def F12(eta):
    return 2 / sqrt(pi) * simpson(lambda xx: sqrt(xx) / (1 + exp(xx - eta)), 0, 60, 60000)


close(F12(0), 0.765, 0.001, "F1/2(0)")
close(F12(-3), 0.0489, 0.002, "F1/2(-3)")
close(1 / F12(0) - 1, 0.31, 0.02, "31 %")
ans("degenerate-onset", 2.8e19 * exp(-3) / 1e18, 0.005)

# ==== 准费米能级 ====
n_ = 1e16 + 1e14
p_ = 1e14 + 1e4
ans("np-ratio", n_ * p_ / ni**2 / 1e10, 0.001)
close(VT * log(n_ / ni), 0.3574, 0.0003, "EFn - Ei")
close(VT * log(1e16 / ni), 0.3571, 0.0003, "EF - Ei before")
close((VT * log(n_ / ni) - VT * log(1e16 / ni)) * 1e3, 0.26, 0.02, "0.26 meV")
close(VT * log(p_ / ni), 0.238, 0.001, "Ei - EFp")
close(VT * log(n_ * p_ / ni**2), 0.595, 0.001, "split")
ans("qf-split", exp(0.6 / VT) / 1e10, 0.005)
ans("qf-equilibrium", VT * log(1.0))

# ==== 漂移 ====
ans("tau-from-mu", 0.135 * 0.26 * m0 / q * 1e12, 0.001)
ans("hole-drift-v", 480 * 500 / 1e5)
sig_p = q * 1e16 * 480
close(sig_p, 0.769, 0.001, "σ p-type")
close(1 / sig_p, 1.30, 0.002, "ρ p-type")
close(1 / (q * 1e16 * 1350), 0.46, 0.01, "ρ n-type 1e16")
close(q * 1e15 * 1350, 0.216, 0.002, "σ 1e15")
ans("rho-n-1e15", 1 / (q * 1e15 * 1350), 0.005)
close(q * ni * 1830, 2.93e-6, 0.001, "σ intrinsic")
ans("rho-intrinsic", 1 / (q * ni * 1830) / 1e5, 0.005)
assert 7e4 < (1 / (q * ni * 1830)) / 4.62 < 8e4
checks += 1
ans("matthiessen", 1 / (1 / 1500 + 1 / 3000), 0.01)
# copper vs silicon drift (about 30 times): μ_Cu from σ = 5.96e7 S/m, n = 8.47e28
mu_cu = 5.96e7 / (8.47e28 * q) * 1e4
close(1350 / mu_cu, 30, 0.05, "Si/Cu mobility")

# ==== 速度饱和、霍尔 ====
vs = lambda E, mu=1350, vsat=1e7: mu * E / (1 + mu * E / vsat)
ans("sat-field", 1e7 / 1350 / 1e3, 0.005)
close(vs(1e7 / 1350), 0.5e7, 1e-9, "v = vsat/2")
ans("sat-1e4", vs(1e4) / 1e6, 0.005)
close(vs(1e5), 9.31e6, 0.001, "v at 1e5")
ans("transit-time", 1e-5 / vs(1e5) * 1e12, 0.005)
close(1 / (2 * pi * 1e-5 / vs(1e5)) / 1e9, 150, 0.02, "1/(2πτ) ≈ 150 GHz")
n_hall = 2e-3 * 0.4 / (q * 2e-4 * 2.0e-3)  # m⁻³
ans("hall-n", n_hall * 1e-6 / 1e16, 0.005)
ans("hall-mobility", 1 / (q * 1.25e16 * 0.5), 1)
close(1e-3 * 0.5 / (q * 1e22 * 5e-4), 0.624e-3, 0.001, "VH example")

# ==== 扩散 ====
ans("diffusion-linear", q * 35 * (1e16 / 1e-3), 0.1)
ans("dp-einstein", 480 * VT, 0.01)
close(1350 * VT, 34.9, 0.001, "Dn")
ans("einstein-350", 1000 * kB_eV * 350, 0.02)
close(1000 * VT, 25.85, 1e-9, "wrong 25.85")
L = 10e-4
pfun = lambda xx: 1e14 * exp(-xx / L)
dpdx = lambda xx: (pfun(xx + 1e-9) - pfun(xx - 1e-9)) / 2e-9
J0 = -q * 12.4 * dpdx(0)
close(J0, 0.199, 0.002, "J at 0")
ans("diffusion-at-l", -q * 12.4 * dpdx(L), 0.0002)

# ==== 漂移–扩散 ====
lam = 1e-4
Ebi = VT / lam
close(Ebi, 258.5, 1e-9, "built-in field")
nfun = lambda xx: 1e16 * exp(-xx / lam)
dndx = (nfun(1e-9) - nfun(-1e-9)) / 2e-9
Jdrift = q * nfun(0) * 1350 * Ebi
Jdiff = q * (1350 * VT) * dndx
close(Jdrift + Jdiff, 0, 1e-6, "drift + diffusion = 0")
ans("dd-drift-balance", Jdrift, 0.5)
ans("built-in-voltage", VT * log(1e17 / 1e15), 0.0005)

# ==== 复合 ====


def rk4_decay(tau, t_end, n=2000):
    y, dt = 1.0, t_end / n
    for _ in range(n):
        k1 = -y / tau
        k2 = -(y + dt / 2 * k1) / tau
        k3 = -(y + dt / 2 * k2) / tau
        k4 = -(y + dt * k3) / tau
        y += dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return y


ans("decay-3tau", rk4_decay(1e-6, 3e-6), 0.0001)
ans("decay-1percent", bisect(lambda t: rk4_decay(1.0, t, 400) - 0.01, 0.1, 10), 0.005)
ans("srh-tau", 1 / (1e-15 * 1e7 * 1e14) * 1e6, 1e-6)


def srh(n, p, tn=1e-6, tp=1e-6):
    return (n * p - ni**2) / (tp * (n + ni) + tn * (p + ni))


ans("srh-rate", srh(1e12 + 1e4, 1e16 + 1e12) / 1e18, 0.002)
close(srh(1e12 + 1e4, 1e16 + 1e12), 1e12 / 1e-6, 0.001, "low injection -> Δn/τ")
close(srh(1e10, 1e10), 0, 1e-9, "equilibrium U = 0")
close(srh(1e5, 1e5), -ni / (2 * 1e-6), 1e-4, "depletion generation -ni/2τ")
close(-ni / 2e-6, -5e15, 1e-9, "-5e15")

# ==== 连续性方程 ====
for D, tau in ((12.4, 10e-6), (30.0, 3.333e-6)):
    Lx = sqrt(D * tau)
    dn = lambda xx: exp(-xx / Lx)
    xx, hh = 0.7 * Lx, Lx * 1e-3
    lhs = D * (dn(xx + hh) - 2 * dn(xx) + dn(xx - hh)) / hh**2 - dn(xx) / tau
    close(lhs * tau, 0, 1e-5, "D n'' - n/τ = 0")
ans("hole-diff-length", sqrt(12.4 * 10e-6) * 1e4, 0.3)
ans("at-2l", exp(-2), 0.0005)
ans("tau-from-l", (100e-4) ** 2 / 30 * 1e6, 0.005)
close(1 - exp(-5 / 100), 0.05, 0.03, "5 % over 5 μm")
close(sqrt(1350 * VT * 1e-6) * 1e4, 59, 0.003, "exercise L ≈ 59 μm")

# ==== PN 结 ====
vbi = lambda Na, Nd, ni_=ni: VT * log(Na * Nd / ni_**2)
close(VT * log(2e16 / ni), 0.375, 0.001, "n side")
close(VT * log(5e17 / ni), 0.458, 0.001, "p side")
close(vbi(5e17, 2e16), 0.833, 0.001, "0.833")
ans("vbi-1e17-1e15", vbi(1e17, 1e15), 0.0005)
close(VT * log(10), 0.06, 0.01, "0.06 V per decade")
ans("vbi-ge", vbi(1e17, 1e15, 2e13), 0.0005)


def width(Na, Nd, V):
    return sqrt(2 * eps * V / q * (1 / Na + 1 / Nd))


def poisson_drop(Na, Nd, W, n=20000):
    # integrate dE/dx = ρ/ε twice across the depletion layer and return the potential drop
    xn = W * Na / (Na + Nd)
    xp = W - xn
    dx = W / n
    E, V, Emax = 0.0, 0.0, 0.0
    for i in range(n):
        xx = -xp + (i + 0.5) * dx
        rho = -q * Na if xx < 0 else q * Nd
        E_new = E + rho / eps * dx
        V += -(E + E_new) / 2 * dx  # V = -∫E dx, so the n side ends up higher
        E = E_new
        Emax = max(Emax, abs(E))
    close(E / Emax, 0, 2e-3, "field returns to zero")  # up to one grid cell of charge at x = 0
    close(Emax, q * Nd * xn / eps, 2e-3, "Emax = qNd xn/ε")
    return V


Vb = vbi(1e17, 1e15)
W0 = width(1e17, 1e15, Vb)
close(poisson_drop(1e17, 1e15, W0), Vb, 1e-3, "Poisson drop = Vbi")
close(W0 * 1e4, 0.966, 0.001, "W 0.966")
close(W0 * 1e17 / (1e17 + 1e15) * 1e4, 0.956, 0.001, "xn 0.956")
close(2 * Vb / W0, 1.48e4, 0.002, "Emax")
close(q * 1e15 * (W0 * 1e17 / 1.01e17) / eps, 2 * Vb / W0, 1e-6, "Emax two ways")
Vb2 = vbi(1e17, 1e16)
close(Vb2, 0.774, 0.001, "exercise Vbi")
W2 = width(1e17, 1e16, Vb2)
close(W2 * 1e4, 0.332, 0.002, "exercise W")
ans("xn-share", 0.332 * 1e17 / 1.1e17, 0.0005)
ans("width-reverse", width(1e17, 1e16, 0.774 + 5) * 1e4, 0.001)
close(poisson_drop(1e17, 1e16, width(1e17, 1e16, 5.774)), 5.774, 1e-3, "Poisson reverse")
ans("cj-value", eps / 0.966e-4 * 1e9, 0.03)
close(eps / 0.966e-4 * 1e-4 * 1e12, 1.07, 0.01, "1 pF for 100×100 μm²")
ans("cj-ratio", 1 / sqrt(4 / 1))
close(sqrt(0.2 / 0.7), 0.53, 0.01, "forward W ratio")

# ==== 二极管 ====
e06 = exp(0.6 / VT)
close(e06, 1.20e10, 0.003, "e^(0.6/VT)")
ans("injected-np", ni**2 / 1e17 * e06 / 1e13, 0.005)
term_p = 10 * 1e4 / 30e-4
term_n = 25 * 1e3 / 50e-4
close(term_p, 3.33e7, 0.002, "hole term")
close(term_n, 5e6, 1e-9, "electron term")
Js = q * (term_p + term_n)
close(Js, 6.14e-12, 0.001, "Js")
close(Js * e06, 0.074, 0.005, "J at 0.6 V")
ans("ratio-01v", exp(0.1 / VT), 0.05)
ans("mv-per-decade", VT * log(10) * 1e3, 0.05)
ans("v-at-1ma", VT * log(1e-3 / 1e-14 + 1), 0.0005)
close(VT * log(1e11), 0.655, 0.001, "0.655")

# ==== 击穿 ====
Ecrit = 3e5
vbr = lambda N: eps * Ecrit**2 / (2 * q * N)
# check against the depletion picture: one-sided junction whose Emax reaches Ecrit
for N in (1e15, 1e16):
    W_ = width(1e30, N, vbr(N))
    close(q * N * W_ / eps, Ecrit, 1e-6, "Emax = Ecrit at V_BR")
ans("vbr-1e15", vbr(1e15), 0.5)
ans("vbr-1e16", vbr(1e16), 0.05)
close(60 * (1e15 / 1e16) ** -0.75, 337, 0.01, "empirical 340 V")
close(60 * (1e16 / 1e16) ** -0.75, 60, 1e-9, "empirical 60 V")
vbi_deg = vbi(1e19, 1e19)
close(vbi_deg, 1.07, 0.002, "Vbi heavy")
Wt = width(1e19, 1e19, 1.07 + 2)
ans("tunnel-width", Wt * 1e7, 0.1)
close(3.07 / Wt, 1.1e6, 0.02, "average field")
I_R = (12 - 5.1) / 470
close(I_R * 1e3, 14.68, 0.001, "resistor current")
ans("zener-current", (I_R - 5e-3) * 1e3, 0.005)

# ==== 结业挑战 ====
ans("b-bragg", degrees(asin(0.154 / (2 * 0.36 / sqrt(3)))), 0.01)
close(0.36 / sqrt(3), 0.2078, 0.0003, "b d111")
close(0.154 / (2 * 0.36 / sqrt(3)), 0.3705, 0.0003, "b sinθ")
ans("b-bcc-reciprocal", 4 * pi / 0.35, 0.02)
close(E_well / 0.3**2, 4.18, 0.001, "b boundary")
ans("b-band-top", E_well / 0.3**2 - 0.25, 0.005)
ans("b-compensation", n_of(1e16, 5e16)[0], 1)
ans("b-fermi-level", VT * log(1.8e19 / 1e17), 0.0005)
close(q * 2e15 * 1350, 0.433, 0.001, "b σ")
ans("b-resistivity", 1 / (q * 2e15 * 1350), 0.005)
Db = 1160 * VT
close(Db, 30.0, 0.001, "b D")
ans("b-diff-length", sqrt(Db * 2e-6) * 1e4, 0.05)
ans("b-decay", bisect(lambda t: rk4_decay(2.0, t, 400) - 0.1, 0.1, 20), 0.005)
close(2 * log(10), 4.61, 0.002, "τ ln 10")
vbb = vbi(1e18, 1e16)
close(vbb, 0.833, 0.001, "b Vbi")
Wb = width(1e18, 1e16, vbb)
close(poisson_drop(1e18, 1e16, Wb), vbb, 1e-3, "b Poisson")
ans("b-depletion", Wb * 1e4, 0.001)
ans("b-diode-voltage", VT * log(2e-3 / 2e-15 + 1), 0.0005)

# ---- compare with the pack ----
pack = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "data" / "content" / "N.2.2.yaml"
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

print(f"N.2.2 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
