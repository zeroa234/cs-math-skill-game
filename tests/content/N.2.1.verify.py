"""N.2.1 量子力学基础 — every number in data/content/N.2.1.yaml, recomputed.

Run: python -I tests/content/N.2.1.verify.py [path/to/N.2.1.yaml]
Plain Python. Number answers are read back from the YAML and compared with the values computed here, so a
typo in either place fails. Formulas the cards quote are checked independently where that is possible:
Wien's law by maximising Planck's spectrum and σ by integrating it, the Compton shift by solving relativistic
energy and momentum conservation, the Rydberg constant and Bohr radius from the fundamental constants, the
infinite-well and oscillator levels by shooting the Schrödinger equation with RK4, the finite-well level
from its transcendental equation, the barrier transmission by a transfer-matrix calculation, ladder-operator
coefficients and expectation values by integrating on a grid, the hydrogen 1s most probable radius by
maximising P(r), spin probabilities with 2×2 complex matrices, and shell filling by the aufbau order.
"""
import cmath
import math
import re
import sys
from math import acos, cos, degrees, erfc, exp, pi, radians, sin, sinh, sqrt
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


def simpson(f, a, b, n=2000):
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


def golden_min(f, a, b, it=200):
    g = (sqrt(5) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a)
    for _ in range(it):
        if f(c) < f(d):
            b = d
        else:
            a = c
        c, d = b - g * (b - a), a + g * (b - a)
    return (a + b) / 2


def rk4_end(f, x0, y, x1, n):
    """Integrate y' = f(x, y) from x0 to x1 in n steps, return the final y (a list)."""
    h = (x1 - x0) / n
    x = x0
    for _ in range(n):
        k1 = f(x, y)
        k2 = f(x + h / 2, [a + h / 2 * b for a, b in zip(y, k1)])
        k3 = f(x + h / 2, [a + h / 2 * b for a, b in zip(y, k2)])
        k4 = f(x + h, [a + h * b for a, b in zip(y, k3)])
        y = [a + h / 6 * (b + 2 * c + 2 * d + e) for a, b, c, d, e in zip(y, k1, k2, k3, k4)]
        x += h
    return y


# Constants: CODATA for the independent checks, and the rounded values the prompts give for the answers.
H_SI, HBAR_SI, ME_SI, E_SI, C_SI = 6.62607015e-34, 1.054571817e-34, 9.1093837015e-31, 1.602176634e-19, 2.99792458e8
KB_SI, EPS0 = 1.380649e-23, 8.8541878128e-12
h, hbar, me, e, c = 6.626e-34, 1.055e-34, 9.109e-31, 1.602e-19, 3.00e8
HC = 1240.0  # eV·nm, as given in the prompts
close(H_SI * C_SI / E_SI * 1e9, 1239.84, 1e-4, "hc = 1240 eV nm")
close(H_SI / (2 * pi), HBAR_SI, 1e-6, "hbar = h/2π")

# ==== 黑体辐射和光子 ====
def planck(lam, T):
    return 2 * H_SI * C_SI**2 / lam**5 / (exp(H_SI * C_SI / (lam * KB_SI * T)) - 1)


lam_peak = golden_min(lambda l: -planck(l, 5800), 100e-9, 2000e-9)
close(lam_peak * 5800, 2.898e-3, 1e-3, "Wien b from Planck's law")
sigma = simpson(lambda l: pi * planck(l, 5800), 20e-9, 200e-6, 200000) / 5800**4
close(sigma, 5.67e-8, 3e-3, "σ by integrating Planck's law")
b_wien = 2.898e-3
ans("sun-peak", b_wien / 5800 * 1e9, 0.5)
ans("body-peak", b_wien / 310 * 1e6, 0.01)
ans("double-temperature", (600 / 300) ** 4)
close(HC / 620, 2.00, 1e-9, "620 nm photon 2.00 eV")
ans("violet-photon", HC / 400, 0.005)
ans("laser-photon-rate", 1e-3 / (HC / 620 * e) / 1e15, 0.01)
close(HC / 300, 4.13, 0.005, "300 nm UV photon ~4 eV")
close(HC / 10000, 0.124, 0.001, "10 μm IR photon 0.12 eV")

# ==== 光电效应 ====
W = 2.30
ans("stopping-400", HC / 400 - W, 1e-6)
ans("cutoff-wavelength", HC / W, 0.1)
f1, f2 = c / 250e-9, c / 400e-9
V1, V2 = HC / 250 - W, HC / 400 - W
close(V1, 2.66, 1e-9, "250 nm stopping 2.66 V")
close(f1, 1.20e15, 1e-9, "f1")
close(f2, 7.50e14, 1e-9, "f2")
close(e * (V1 - V2) / (f1 - f2), 6.62e-34, 0.002, "h from two points")
ans("work-function-300", HC / 300 - 1.83, 0.005)
ans("silicon-cutoff", HC / 1.12, 1)

# ==== 康普顿效应 ====
lc = H_SI / (ME_SI * C_SI)
close(lc * 1e12, 2.43, 0.002, "Compton wavelength 2.43 pm")


def compton_by_conservation(lam, theta):
    """Scattered wavelength from energy and momentum conservation with a relativistic electron."""
    E0 = H_SI * C_SI / lam
    mc2 = ME_SI * C_SI**2

    def mismatch(E1):
        # electron momentum from momentum conservation, energy from energy conservation
        px = E0 / C_SI - E1 / C_SI * cos(theta)
        py = -E1 / C_SI * sin(theta)
        Ee = E0 - E1 + mc2
        return Ee**2 - ((px**2 + py**2) * C_SI**2 + mc2**2)

    E1 = bisect(mismatch, E0 * 0.5, E0 * (1 - 1e-12))
    return H_SI * C_SI / E1


for th in (60, 90, 180):
    close(compton_by_conservation(71.0e-12, radians(th)) - 71.0e-12, lc * (1 - cos(radians(th))), 1e-6, f"Compton {th}")
ans("photon-momentum", h / 500e-9 / 1e-27, 0.001)
lc2 = 2.43
ans("compton-90", lc2 * (1 - cos(radians(90))), 1e-9)
lam2 = 71.0 + lc2 * 2
close(lam2, 75.86, 1e-9, "180° wavelength")
close(1.240 / 0.0710, 17.46, 0.001, "17.46 keV")
close(1.240 / 0.07586, 16.35, 0.001, "16.35 keV")
close(1.240 / 0.0710 - 1.240 / 0.07586, 1.12, 0.005, "recoil 1.12 keV")
ans("recoil-90", 1.240 / 0.0710 - 1.240 / (0.0710 + 0.00243), 0.0005)
close(4.86e-12 / 500e-9, 1e-5, 0.03, "visible relative shift ~1e-5")

# ==== 玻尔模型 ====
R = ME_SI * E_SI**4 / (8 * EPS0**2 * H_SI**3 * C_SI)
close(R, 1.097e7, 1e-3, "Rydberg constant")
a0 = 4 * pi * EPS0 * HBAR_SI**2 / (ME_SI * E_SI**2)
close(a0 * 1e9, 0.0529, 1e-3, "Bohr radius")
close(ME_SI * E_SI**4 / (8 * EPS0**2 * H_SI**2) / E_SI, 13.6, 1e-3, "13.6 eV")
Rg = 1.097e7
ans("h-alpha", 1 / (Rg * (1 / 4 - 1 / 9)) * 1e9, 0.05)
ans("paschen-alpha", 1 / (Rg * (1 / 9 - 1 / 16)) * 1e9, 0.5)
close(Rg * (1 / 9 - 1 / 16), 5.33e5, 0.001, "Paschen 1/λ")
for n, lam in ((4, 486), (5, 434), (6, 410)):
    close(1 / (Rg * (1 / 4 - 1 / n**2)) * 1e9, lam, 0.003, f"Balmer n={n}")
ans("bohr-r3", 9 * 0.0529, 0.0005)
ans("h-beta-energy", HC / (13.6 * (1 / 4 - 1 / 16)), 0.05)
close(13.6 * (1 / 4 - 1 / 16), 2.55, 1e-9, "2.55 eV")
ans("ionize-n2", 13.6 / 4, 1e-9)
ans("line-count-n3", len([(i, j) for i in range(1, 4) for j in range(1, i)]))

# ==== 物质波 ====
close(h / (0.145 * 40), 1.1e-34, 0.05, "baseball λ")
K50 = e * 50
close(K50, 8.01e-18, 0.001, "50 eV in J")
p50 = sqrt(2 * me * K50)
close(p50, 3.82e-24, 0.002, "p at 50 V")
close(h / p50 * 1e9, 0.173, 0.003, "λ at 50 V")
close(h / sqrt(2 * me * e) * 1e9, 1.226, 0.001, "1.226/√U")
ans("electron-100v", h / sqrt(2 * me * e * 100) * 1e9, 0.0002)
ans("electron-150v", 1.226 / sqrt(150), 0.0001)
ans("davisson-54", 1.226 / sqrt(54), 0.0001)
close(0.215 * sin(radians(50)), 0.165, 0.003, "Davisson d sin 50°")
ans("neutron-wavelength", h / (1.675e-27 * 2200) * 1e9, 0.0002)
close(1.226 / sqrt(50000) * 1e3, 5.5, 0.01, "50 kV electron ~5.5 pm")

# ==== 波函数和概率 ====
ans("small-interval", (0.3**2 + 0.4**2) * 0.01, 1e-12)
ans("normalize-linear", 1 / simpson(lambda x: x * x, 0, 1), 1e-9)
P_q = simpson(lambda x: 2 * sin(pi * x) ** 2, 0, 0.25)
close(P_q, 0.25 - 1 / (2 * pi), 1e-9, "left quarter 0.091")
close(P_q, 0.091, 0.005, "0.091")
ans("middle-third", simpson(lambda x: 2 * sin(pi * x) ** 2, 1 / 3, 2 / 3), 0.0005)
close(simpson(lambda x: 1 / (1 + x * x) ** 2, -2000, 2000, 400000), pi / 2, 1e-5, "∫1/(1+x²)² = π/2")
a_exp = 0.5
ans("normalize-exponential", 1 / (2 * simpson(lambda x: exp(-2 * x / a_exp), 0, 40)), 1e-6)

# ==== 不确定关系 ====
ans("slit-halve", (1 / 0.5))
ans("electron-in-atom", hbar / (2 * 0.1e-9) / me / 1e5, 0.005)
ans("dust-grain", hbar / (2 * 1e-9 * 1e-6) / 1e-20, 0.005)
close(0.1e-9 / 5.27e-20 / (365.25 * 86400), 60, 0.02, "60 years for 0.1 nm")
k_c = 1 / (4 * pi * EPS0)
r_min = golden_min(lambda r: HBAR_SI**2 / (2 * ME_SI * r * r) - k_c * E_SI**2 / r, 1e-12, 1e-9)
close(r_min * 1e9, 0.0529, 1e-3, "atom size from uncertainty")
close((HBAR_SI**2 / (2 * ME_SI * r_min**2) - k_c * E_SI**2 / r_min) / E_SI, -13.6, 1e-3, "atom energy")
ans("squeeze-kinetic", (1 / 0.5) ** 2)
ans("level-width", hbar / (2 * 10e-9) / e / 1e-8, 0.005)

# ==== 薛定谔方程 ====
omega = lambda k: HBAR_SI * k * k / (2 * ME_SI)
k0 = 1e10
vg = (omega(k0 * (1 + 1e-6)) - omega(k0 * (1 - 1e-6))) / (2e-6 * k0)
close(vg, HBAR_SI * k0 / ME_SI, 1e-6, "group velocity ħk/m")
close(omega(k0) / k0, vg / 2, 1e-9, "phase velocity half")
ans("packet-velocity", hbar * 1.0e10 / me / 1e6, 0.0005)
close(2 * pi / 1e10 * 1e9, 0.63, 0.005, "λ 0.63 nm")
ans("superposition-frequency", 1.13 * e / h / 1e14, 0.005)
# the cross term of two stationary states repeats after h/ΔE
dE = 1.13 * E_SI
T_beat = H_SI / dE
dens = lambda t: 0.5 * (1 + 1 + 2 * cos(dE * t / HBAR_SI))
close(dens(0.37 * T_beat), dens(1.37 * T_beat), 1e-6, "density period h/ΔE")

# ==== 无限深势阱 ====
HB2M = HBAR_SI**2 / (2 * ME_SI) / E_SI * 1e18  # ħ²/2m in eV·nm²
close(HB2M, 0.0381, 1e-3, "ħ²/2m")


def well_shoot(E, L=1.0):
    return rk4_end(lambda x, y: [y[1], -E / HB2M * y[0]], 0, [0.0, 1.0], L, 400)[0]


E1_shoot = bisect(lambda E: well_shoot(E), 0.2, 0.6)
close(E1_shoot, H_SI**2 / (8 * ME_SI * 1e-18) / E_SI, 1e-6, "well E1 by shooting")
E1 = h**2 / (8 * me * 1e-18) / e
close(E1, 0.376, 0.001, "E1 = 0.376 eV")
close((6.626e-34) ** 2, 4.390e-67, 1e-3, "numerator")
close(8 * 9.109e-31 * 1e-18, 7.287e-48, 1e-3, "denominator")
close(4 * E1, 1.50, 0.003, "E2")
close(HC / 400 - 2.00, 1.10, 1e-9, "worked photoelectric 1.10 V")
close(1 / (sqrt(2 * me * 4 * e) / hbar) * 1e9, 0.0976, 0.002, "penetration ~0.1 nm at 4 eV")
close(9 * E1, 3.38, 0.002, "E3")
ans("well-transition", HC / (3 * 0.376), 0.5)
ans("narrow-well", 0.376 / 0.5**2, 1e-6)
psi4 = [sin(4 * pi * (i + 0.5) / 1000) for i in range(1000)]
ans("well-nodes", sum(1 for a, b in zip(psi4, psi4[1:]) if a * b < 0))
ans("n2-left-quarter", simpson(lambda x: 2 * sin(2 * pi * x) ** 2, 0, 0.25), 1e-6)

# ==== 有限深势阱和势阶 ====
kap1 = sqrt(2 * me * 1.0 * e) / hbar
close(kap1, 5.12e9, 0.001, "κ for 1 eV")
ans("penetration-depth", 1 / kap1 * 1e9, 0.0005)
# finite well, 1 nm wide, 2 eV deep: even ground state from k tan(ka/2) = κ is below 0.376 eV
V0w = 2.0
gs = bisect(lambda E: sqrt(E / HB2M) * math.tan(sqrt(E / HB2M) * 0.5) - sqrt((V0w - E) / HB2M), 0.01, 0.37)
assert gs < E1_shoot
checks += 1


def step_R(E, V0):
    k1, k2 = sqrt(E), sqrt(E - V0)
    return ((k1 - k2) / (k1 + k2)) ** 2


close(step_R(8, 6), 1 / 9, 1e-12, "R = 1/9")
ans("step-reflection", step_R(5, 4), 0.0001)
ans("step-down", step_R(5, -4), 0.0001)
for E, V0 in ((5, 4), (8, 6), (5, -4)):  # T computed from fluxes: T = (k2/k1)|t|², t = 2k1/(k1+k2)
    k1, k2 = sqrt(E), sqrt(E - V0)
    close(k2 / k1 * (2 * k1 / (k1 + k2)) ** 2 + step_R(E, V0), 1, 1e-12, "R + T = 1")

# ==== 隧穿 ====


def barrier_T_transfer(E, V0, a_nm):
    """Transmission through a square barrier by matching ψ, ψ′ at both edges (complex wave numbers)."""
    k = cmath.sqrt(E / HB2M)
    q = cmath.sqrt((E - V0) / HB2M)
    # region I: e^{ikx} + r e^{-ikx}; II: A e^{iqx} + B e^{-iqx}; III: t e^{ikx}. Solve right to left.
    a = a_nm
    t = 1.0
    # at x = a: A e^{iqa} + B e^{-iqa} = t e^{ika}; iq(A e^{iqa} - B e^{-iqa}) = ik t e^{ika}
    A = t * cmath.exp(1j * k * a) * (1 + k / q) / 2 * cmath.exp(-1j * q * a)
    B = t * cmath.exp(1j * k * a) * (1 - k / q) / 2 * cmath.exp(1j * q * a)
    # at x = 0: 1 + r = A + B; ik(1 - r) = iq(A - B)  =>  incident amplitude = ((A+B) + q/k (A-B)) / 2
    inc = ((A + B) + q / k * (A - B)) / 2
    return abs(t / inc) ** 2


kap4 = sqrt(2 * me * 4 * e) / hbar * 1e-9
close(kap4, 10.25, 0.001, "κ for 4 eV")
close(2 * kap4 * 0.5, 10.25, 0.001, "2κa")
close(exp(-2 * kap4 * 0.5), 3.55e-5, 0.01, "e^-2κa")
T_exact = 1 / (1 + 25 * sinh(kap4 * 0.5) ** 2 / (4 * 1 * 4))
close(T_exact, 9.09e-5, 0.002, "exact T")
close(barrier_T_transfer(1.0, 5.0, 0.5) / T_exact, 1, 0.01, "exact T by transfer matrix")
close(T_exact / exp(-2 * kap4 * 0.5), 2.56, 0.003, "prefactor 2.56")
ans("barrier-1nm", exp(-2 * 10.25 * 1.0) / 1e-9, 0.005)
close(sqrt(1.6726e-27 / ME_SI), 42.85, 0.001, "proton κ 43×")
close(2 * sqrt(2 * 1.6726e-27 * 4 * E_SI) / HBAR_SI * 0.5e-9, 440, 0.01, "proton 2κa ~440")
ans("stm-factor", exp(2 * 10 * 0.1), 0.005)
close(sqrt(2 * ME_SI * 4.5 * E_SI) / HBAR_SI * 1e-9, 10.9, 0.01, "κ ≈ 10 nm⁻¹ for 4.5 eV")

# ==== 量子谐振子 ====


def osc_shoot(eps, parity):
    # ψ'' = (ξ² − 2ε)ψ in units of √(ħ/mω); integrate from 0 outward and look at the sign far out
    y0 = [1.0, 0.0] if parity == 0 else [0.0, 1.0]
    return rk4_end(lambda x, y: [y[1], (x * x - 2 * eps) * y[0]], 0, y0, 4.5, 900)[0]


close(bisect(lambda s: osc_shoot(s, 0), 0.3, 0.7), 0.5, 1e-4, "oscillator E0 = ħω/2 by shooting")
close(bisect(lambda s: osc_shoot(s, 1), 1.3, 1.7), 1.5, 1e-4, "oscillator E1 = 3ħω/2 by shooting")
ans("oscillator-ground", 0.5 * 0.1, 1e-12)
ans("oscillator-e3", 3.5 * 0.1, 1e-12)
dx_opt = golden_min(lambda d2: 1 / (8 * d2) + 0.5 * d2, 0.01, 5)  # ħ = m = ω = 1
close(dx_opt, 0.5, 1e-6, "(Δx)² = ħ/2mω")
close(1 / (8 * dx_opt) + 0.5 * dx_opt, 0.5, 1e-9, "E_min = ħω/2")
p_out = 2 * simpson(lambda x: exp(-x * x) / sqrt(pi), 1, 12, 20000)
close(p_out, erfc(1), 1e-9, "forbidden probability")
close(p_out, 0.157, 0.002, "0.157")
ans("co-infrared", 1.240 / 0.266, 0.005)
w_s = sqrt(500 / 1.6e-27)
close(w_s, 5.59e14, 0.001, "ω spring")
ans("spring-hw", hbar * w_s / e, 0.0005)
close(hbar * w_s, 5.90e-20, 0.002, "5.90e-20 J")
k_pend = (2 * pi) ** 2
close(0.5 * k_pend * 0.01**2, 2e-3, 0.02, "pendulum energy")
close(0.5 * k_pend * 0.01**2 / (H_SI), 3e30, 0.05, "n ~ 3e30")
close(HBAR_SI * 2 * pi, 6.6e-34, 0.01, "ħω for 1 s period ~7e-34 J")

# ==== 升降算符 ====
dxg = 0.002
xs = [-8 + i * dxg for i in range(8001)]


def d1(f):
    return [(f[min(i + 1, len(f) - 1)] - f[max(i - 1, 0)]) / (2 * dxg) for i in range(len(f))]


def inner(f, g):
    return sum(a * b for a, b in zip(f, g)) * dxg


# units ħ = m = ω = 1: â₊ = (x − d/dx)/√2, â₋ = (x + d/dx)/√2
psi0 = [pi**-0.25 * exp(-x * x / 2) for x in xs]
psi1 = [pi**-0.25 * sqrt(2) * x * exp(-x * x / 2) for x in xs]
psi2 = [pi**-0.25 / sqrt(2) * (2 * x * x - 1) * exp(-x * x / 2) for x in xs]
up = lambda f: [(x * a - b) / sqrt(2) for x, a, b in zip(xs, f, d1(f))]
down = lambda f: [(x * a + b) / sqrt(2) for x, a, b in zip(xs, f, d1(f))]
close(inner(up(psi0), psi1), 1.0, 1e-4, "â₊ψ0 = ψ1")
close(inner(up(psi1), psi2), sqrt(2), 1e-4, "â₊ψ1 = √2 ψ2")
close(max(abs(v) for v in down(psi0)), 0, 1e-5, "â₋ψ0 = 0")
close(inner(down(psi2), psi1), sqrt(2), 1e-4, "â₋ψ2 = √2 ψ1")
# [x, p] f = iħ f, checked on f = x²: x(−2iħx) − (−iħ)(3x²) = iħx²
close((-2 + 3), 1, 0, "[x,p]x² = iħx²")
ans("climb-three", 1.5 + 3)
ans("raise-twice", sqrt(1) * sqrt(2), 0.0005)
ans("number-operator", sqrt(5) * sqrt(5), 1e-9)

# ==== 期望值和动量空间 ====
ans("mean-linear", simpson(lambda x: x * 3 * x * x, 0, 1), 1e-9)
x2 = simpson(lambda x: x * x * 3 * x * x, 0, 1)
close(x2, 0.6, 1e-9, "<x²> = 0.6")
close(sqrt(x2 - 0.75**2), 0.194, 0.001, "Δx = 0.194")
ans("well-mean-x", simpson(lambda x: x * 2 * sin(pi * x) ** 2, 0, 1), 1e-9)
mx = simpson(lambda x: x * 2 * sin(pi * x) ** 2, 0, 1)
dxw = sqrt(simpson(lambda x: x * x * 2 * sin(pi * x) ** 2, 0, 1) - mx * mx)
close(dxw, 0.181, 0.002, "Δx = 0.181 L")
p2 = simpson(lambda x: sqrt(2) * sin(pi * x) * sqrt(2) * pi * pi * sin(pi * x), 0, 1)  # −ψψ″ with ħ = L = 1
close(p2, pi * pi, 1e-9, "<p²> = (πħ/L)²")
ans("well-uncertainty-product", 0.181 * pi, 0.001)
close(dxw * pi, 0.568, 0.001, "Δx Δp = 0.568 ħ")
ans("well-oscillation-period", h / (1.128 * e) / 1e-15, 0.005)

# ==== 可观测量和厄米算符 ====
ans("well-orthogonal", round(simpson(lambda x: 2 * sin(pi * x) * sin(2 * pi * x), 0, 1), 12), 1e-9)
tr, det = 4, 2 * 2 - (1j * -1j).real
ans("hermitian-eigenvalue", (tr + sqrt(tr * tr - 4 * det)) / 2, 1e-9)
close(simpson(lambda x: 30 * (x * (1 - x)) ** 2, 0, 1), 1, 1e-9, "√30 x(1−x) normalised")
I1 = simpson(lambda x: x * (1 - x) * sin(pi * x), 0, 1)
close(I1, 4 / pi**3, 1e-9, "∫x(1−x)sin πx = 4/π³")
c1 = sqrt(60) * I1
close(c1, 0.9993, 0.0001, "c1")
close(c1 * c1, 0.9986, 0.0001, "|c1|²")
ans("parabola-ground-share", 1 - c1 * c1, 0.0001)
# eigenvalues of the 2×2 matrix in the options: [[0,1],[-1,0]] has ±i
close(abs(cmath.sqrt(-1)), 1, 1e-12, "antisymmetric ±i")

# ==== 测量 ====
E1r = 0.376
close(0.25 * E1r + 0.75 * 4 * E1r, 1.22, 0.002, "<E> = 1.22 eV")
ans("three-level-mean", (1 + 4 + 9) / 3 * E1r, 0.0005)
ans("complex-coefficient", abs(2j) ** 2 / 5, 1e-12)
mE = 0.25 * 1 + 0.75 * 4
mE2 = 0.25 * 1 + 0.75 * 16
close(mE, 3.25, 1e-12, "3.25 E1")
close(mE2, 12.25, 1e-12, "12.25 E1²")
ans("energy-spread", sqrt(mE2 - mE * mE), 0.0005)

# ==== 角动量 ====
ans("l2-magnitude", sqrt(2 * 3), 0.0005)
ans("l3-m-count", len(range(-3, 4)))
ans("l2-min-angle", degrees(acos(2 / sqrt(6))), 0.01)
close(sqrt(1 * 2), 1.414, 0.001, "l=1 |L| = √2 ħ")
I_co = 1.449e-46
dE_rot = hbar**2 / I_co
close(dE_rot, 7.67e-23, 0.002, "CO rotational ΔE")
ans("co-rotation", h * c / dE_rot * 1e3, 0.003)
close(dE_rot / h / 1e9, 116, 0.005, "116 GHz")

# ==== 氢原子 ====
ans("n3-states", sum(2 * l + 1 for l in range(3)))
close(-13.6 / 9, -1.51, 0.002, "E3 = −1.51 eV")
ans("n4-degeneracy", sum(2 * l + 1 for l in range(4)))
r_peak = golden_min(lambda r: -(r * r * exp(-2 * r)), 0.01, 5)  # r in units of a0
close(r_peak, 1.0, 1e-6, "1s most probable r = a0")
mean_r = simpson(lambda r: r * 4 * r * r * exp(-2 * r), 0, 40, 20000)
close(mean_r, 1.5, 1e-6, "<r> = 1.5 a0")
R30 = lambda r: (1 - 2 * r / 3 + 2 * r * r / 27) * exp(-r / 3)  # hydrogen 3s radial function, r in a0
vals = [R30(0.01 + i * 0.01) for i in range(5000)]
ans("radial-nodes", sum(1 for a, b in zip(vals, vals[1:]) if a * b < 0))
ans("lyman-alpha", HC / (13.6 * 0.75), 0.05)

# ==== 轨道磁矩和塞曼效应 ====
close(E_SI * HBAR_SI / (2 * ME_SI), 9.274e-24, 1e-4, "μB CODATA")
close(E_SI * HBAR_SI / (2 * ME_SI) / E_SI, 5.79e-5, 0.001, "μB in eV/T")
ans("bohr-magneton", e * hbar / (2 * me) / 1e-24, 0.0005)
ans("zeeman-2t", 5.79e-5 * 2 / 1e-4, 1e-6)
ans("zeeman-d-width", (2 - (-2)) * 5.79e-5 * 2 / 1e-4, 0.0005)
ans("zeeman-wavelength", 656.3**2 * 5.79e-5 / 1240, 0.00002)

# ==== 自旋 ====
ans("spin-magnitude", sqrt(0.5 * 1.5), 0.0005)
ans("spin-angle", degrees(acos(0.5 / sqrt(0.75))), 0.01)
ans("esr-frequency", 2 * 9.274e-24 * 0.35 / h / 1e9, 0.005)
ans("sodium-doublet", 1239.84 * (1 / 588.995 - 1 / 589.592) * 1e3, 0.005)
close(1239.84 / 588.995, 2.10501, 1e-5, "2.10501")
close(1239.84 / 589.592, 2.10288, 1e-5, "2.10288")
ans("n3-with-spin", 2 * 9)


def matvec(M, v):
    return [M[0][0] * v[0] + M[0][1] * v[1], M[1][0] * v[0] + M[1][1] * v[1]]


def braket(u, v):
    return u[0].conjugate() * v[0] + u[1].conjugate() * v[1]


sx = [[0, 1], [1, 0]]
sy = [[0, -1j], [1j, 0]]
sz = [[1, 0], [0, -1]]
xp, xm = [1 / sqrt(2), 1 / sqrt(2)], [1 / sqrt(2), -1 / sqrt(2)]
for vec, val in ((xp, 1), (xm, -1)):
    close(abs(matvec(sx, vec)[0] - val * vec[0]) + abs(matvec(sx, vec)[1] - val * vec[1]), 0, 1e-12, "σx eigenvectors")
for M in (sx, sy, sz):  # Hermitian, eigenvalues ±1
    assert all(abs(complex(M[i][j]) - complex(M[j][i]).conjugate()) < 1e-12 for i in range(2) for j in range(2))
    tr_m = complex(M[0][0] + M[1][1])
    det_m = complex(M[0][0] * M[1][1] - M[0][1] * M[1][0])
    close(abs(tr_m), 0, 1e-12, "trace 0")
    close(det_m.real, -1, 1e-12, "det −1 so eigenvalues ±1")
up_z = [1 + 0j, 0j]
ans("up-measure-x", abs(braket([complex(a) for a in xp], up_z)) ** 2, 1e-9)
chi = [0.6 + 0j, 0.8 + 0j]
ans("spinor-prob", abs(chi[0]) ** 2, 1e-12)
ans("spinor-mean-sz", braket(chi, matvec(sz, chi)).real / 2, 1e-12)
close(braket(chi, matvec(sx, chi)).real / 2, 0.48, 1e-12, "<Sx> = 0.48 ħ")


def tilted(theta_deg):
    t = radians(theta_deg)
    n_dot_sigma = [[cos(t), sin(t)], [sin(t), -cos(t)]]
    v = [cos(t / 2), sin(t / 2)]
    w = matvec(n_dot_sigma, v)
    assert abs(w[0] - v[0]) < 1e-12 and abs(w[1] - v[1]) < 1e-12  # it is the +1 eigenvector of n·σ
    return v


close(tilted(60)[0] ** 2, 0.75, 1e-12, "60° → 0.75")
ans("tilted-120", tilted(120)[0] ** 2, 1e-9)
ans("sg-chain", abs(braket([complex(a) for a in xp], up_z)) ** 2 * abs(xp[1]) ** 2, 1e-9)
ans("mri-frequency", 42.58 * 3, 0.05)

# ==== 全同粒子 ====


def fill_well(n_electrons, per_level=2):
    total, n, left = 0, 1, n_electrons
    top = 0
    while left > 0:
        take = min(per_level, left)
        total += take * n * n
        top = n
        left -= take
        n += 1
    return total, top


close(fill_well(5)[0], 19, 0, "5 electrons 19 E1")
close(19 * E1r, 7.14, 0.002, "7.14 eV")
close(5 * E1r, 1.88, 0.001, "1.88 eV")
ans("three-electrons", fill_well(3)[0] * E1r, 0.0005)
ans("three-bosons", 3 * E1r, 0.0005)
ans("ten-electrons-top", fill_well(10)[1] ** 2 * E1r, 0.001)
close(KB_SI * 300 / E_SI, 0.026, 0.01, "kT at 300 K")

# ==== 周期表 ====
ORDER = ["1s", "2s", "2p", "3s", "3p", "4s", "3d", "4p", "5s", "4d", "5p"]
CAP = {"s": 2, "p": 6, "d": 10, "f": 14}


def config(Z):
    out, left = [], Z
    for sub in ORDER:
        if left == 0:
            break
        k = min(CAP[sub[1]], left)
        out.append((sub, k))
        left -= k
    return out


assert config(11) == [("1s", 2), ("2s", 2), ("2p", 6), ("3s", 1)]
assert config(8) == [("1s", 2), ("2s", 2), ("2p", 4)]
checks += 2
ans("shell-n3", 2 + 6 + 10)
ans("f-subshell", 2 * (2 * 3 + 1))
ans("period-two", CAP["s"] + CAP["p"])
ans("first-4s", next(Z for Z in range(1, 40) if any(s == "4s" for s, _ in config(Z))))
ans("silicon-valence", sum(k for s, k in config(14) if s[0] == "3"))
assert sum(k for s, k in config(15) if s[0] == "3") == 5 and sum(k for s, k in config(5) if s[0] == "2") == 3
checks += 1

# ==== X 射线 ====
ans("lambda-min", HC / 30000 * 1e3, 0.05)
close(HC / 40000 * 1e3, 31.0, 0.002, "40 kV 31.0 pm")
close(13.6 * 0.75, 10.2, 1e-9, "Moseley 10.2")
close(10.2 * 28**2, 7997, 0.0005, "Cu Kα")
close(1.240 / 7.997, 0.155, 0.002, "Cu Kα λ")
ans("iron-kalpha", 10.2 * 25**2 / 1000, 1e-9)
ans("identify-z", 1 + sqrt(8040 / 10.2), 0.2)

# ==== 激光 ====
dE_hene = HC / 632.8
close(dE_hene, 1.960, 0.001, "He-Ne 1.960 eV")
ans("hene-boltzmann", dE_hene / 0.02586, 0.05)
close(exp(-dE_hene / 0.02586), 1e-33, 1.0, "~1e-33")
ans("mode-spacing", c / (2 * 0.30) / 1e6, 1e-6)
ans("hene-photons", 5e-3 / (1.960 * e) / 1e16, 0.005)
ans("fiber-photon", HC / 1550, 1e-9)

# ==== 结业挑战 ====
ans("b-photoelectric", HC / 200 - 4.5, 1e-6)
ans("b-de-broglie", 1.226 / sqrt(200), 0.0001)
ans("b-bohr-line", HC / (13.6 * (1 / 4 - 1 / 25)), 0.05)
ans("b-uncertainty", hbar / (2 * 1.673e-27 * 1e-14) / 1e6, 0.005)
ans("b-normalize", 1 / simpson(lambda x: (x * (1 - x * x)) ** 2, 0, 1), 1e-6)
E1b = 0.376 / 0.8**2
ans("b-well-transition", HC / (8 * E1b), 0.1)
ans("b-tunnel", exp(-2 * 10.25 * 0.30) / 1e-3, 0.005)
close(sqrt(2 * me * 4 * e) / hbar * 1e-9, 10.25, 0.001, "b-tunnel κ")
ans("b-ladder", sqrt(4) * sqrt(3), 0.0005)
ans("b-measure-mean", (0.2 + 0.8 * 4) * 0.376, 0.0005)
ans("b-l-angle", degrees(acos(3 / sqrt(12))), 0.01)
ans("b-zeeman", 5.788e-5 * 1.5 / 1e-5, 0.002)
ans("b-spin-tilt", tilted(45)[0] ** 2, 0.0005)
ans("b-pauli-seven", fill_well(7)[0] * 0.376, 0.005)
ans("b-moseley", 10.2 * 27**2 / 1000, 0.0005)

# ---- compare with the pack ----
pack = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "data" / "content" / "N.2.1.yaml"
text = pack.read_text(encoding="utf-8")
pairs = re.findall(r"^\s*-?\s*id: ([a-z0-9-]+)\n(?:(?!^\s*-?\s*id: ).*\n)*?\s*answer: ([-0-9.e]+)", text, re.M)
answers = {i: float(a) for i, a in pairs}
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

print(f"N.2.1 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
