"""N.1.3 振动、波动与光学 — every number in data/content/N.1.3.yaml, recomputed.

Run: python -I tests/content/N.1.3.verify.py [path/to/N.1.3.yaml]
Plain Python. Number answers are read back from the YAML and compared with the values computed here, so a
typo in either place fails. Formulas the cards quote are checked independently: oscillators by RK4 time
stepping (damped decay, ω_d, driven steady-state amplitude, beats between coupled pendulums), normal modes
by the characteristic polynomial, the bead-chain frequencies by the tridiagonal determinant, string power by
averaging the energy flux, Fourier coefficients and single-slit / grating patterns by summing phasors,
Brewster's angle from the Fresnel coefficient, the lens and mirror equations by tracing paraxial rays.
"""
import math
import re
import sys
from math import asin, atan, cos, degrees, exp, log, log10, pi, radians, sin, sqrt, tan
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


def rk4(f, y, t, dt, n):
    """Integrate y' = f(t, y) for n steps; returns the list of (t, y)."""
    out = [(t, y)]
    for _ in range(n):
        k1 = f(t, y)
        k2 = f(t + dt / 2, [a + dt / 2 * b for a, b in zip(y, k1)])
        k3 = f(t + dt / 2, [a + dt / 2 * b for a, b in zip(y, k2)])
        k4 = f(t + dt, [a + dt * b for a, b in zip(y, k3)])
        y = [a + dt / 6 * (b + 2 * c + 2 * d + e) for a, b, c, d, e in zip(y, k1, k2, k3, k4)]
        t += dt
        out.append((t, y))
    return out


def peaks(series):
    """Times and values of local maxima of x in [(t, [x, v]), ...]."""
    res = []
    for (t0, a), (t1, b), (t2, c) in zip(series, series[1:], series[2:]):
        if b[0] > a[0] and b[0] >= c[0]:
            res.append((t1, b[0]))
    return res


# ==== 简谐振动 ====
ans("read-omega", sqrt(16))
w0 = sqrt(200 / 0.5)
close(w0, 20, what="omega0 = 20")
ans("spring-frequency", w0 / (2 * pi), 0.005)
close(2 * pi / w0, 0.314, 1e-3, "T 0.314")
ans("initial-amplitude", sqrt(6**2 + (40 / 5) ** 2))
# worked example: m 0.2, k 20, x0 0.04, v0 0.3
A = sqrt(0.04**2 + (0.3 / 10) ** 2)
close(A, 0.05, what="example amplitude")
phi = math.atan2(-0.3 / 10, 0.04)
close(cos(phi), 0.8, 1e-12, "cos phi")
close(phi, -0.64, 0.005, "phi -0.64")
# the solution really starts at x0 with v0
close(A * cos(phi), 0.04, 1e-12, "x(0)")
close(-A * 10 * sin(phi), 0.3, 1e-12, "v(0)")
ans("pendulum-period", 2 * pi * sqrt(1 / 9.8), 0.005)
close(sin(radians(10)) / radians(10), 1 - 0.005, 0.0005, "sin x ~ x 0.5 % at 10 deg")
ans("max-speed", 0.05 * w0)
close(0.5 * 200 * 0.05**2, 0.5 * 0.5 * 1**2, 1e-12, "energy route to vmax")
ans("energy-half-amplitude", 1 - 0.25)
ans("add-perpendicular-phasors", sqrt(9 + 16 + 2 * 12 * cos(pi / 2)))
close(sqrt(9 + 16 + 24 * cos(0)), 7, 1e-12, "in phase 7")
close(sqrt(9 + 16 + 24 * cos(pi)), 1, 1e-12, "anti-phase 1")
# beats: string 437 or 443, tighten -> higher; only 443 gives a larger beat
cands = [440 - 3, 440 + 3]
grow = [f for f in cands if abs(f + 2 - 440) > 3]
ans("beat-frequency", grow[0])
ans("beat-period", 1 / (104 - 100))
# product formula for beats
for t in (0.013, 0.2, 0.77):
    lhs = cos(2 * pi * 440 * t) + cos(2 * pi * 442 * t)
    rhs = 2 * cos(pi * (440 - 442) * t) * cos(pi * (440 + 442) * t)
    close(lhs, rhs, 1e-9, "sum to product")

# ==== 阻尼振动 ====
m, k, b = 0.5, 200.0, 1.0
g = b / m
wd = sqrt(w0**2 - g**2 / 4)
close(wd, 19.97, 0.0005, "omega_d 19.97")
close(1 - wd / w0, 0.001, 0.0005, "about 0.1 %")
ser = rk4(lambda t, y: [y[1], -k / m * y[0] - b / m * y[1]], [1.0, 0.0], 0.0, 1e-4, 40000)
pk = peaks(ser)
period = (pk[5][0] - pk[0][0]) / 5
close(2 * pi / period, wd, 1e-4, "RK4 omega_d")
ratio = pk[1][1] / pk[0][1]
close(ratio, exp(-g / 2 * period), 1e-4, "RK4 decay per period")
ans("half-amplitude-time", 2 * log(2) / 2, 0.005)
ans("q-factor", sqrt(80 / 0.2) / (0.8 / 0.2))
close(w0 / g, 10, what="example Q 10")
ans("q-cycles", 50)
close(exp(-pi), 0.043, 0.001, "e^-pi about 4 %")
# after Q cycles (Q = 50) the amplitude is e^{-pi} for small damping
Qx = 50
gx = 1.0 / Qx  # omega0 = 1
cyc = Qx * 2 * pi / sqrt(1 - gx**2 / 4)
close(exp(-gx / 2 * cyc), exp(-pi), 1e-3, "Q cycles to e^-pi")
# classification boundary 2 omega0 = 20 for omega0 = 10
for gam, kind in ((4, "under"), (20, "critical"), (30, "over")):
    disc = gam**2 / 4 - 100
    got = "under" if disc < 0 else ("critical" if disc == 0 else "over")
    assert got == kind, (gam, got)
    checks += 1

# ==== 受迫振动 ====
F0 = 2.0


def amp(w, w0=20.0, g=2.0, F0m=4.0):
    return F0m / sqrt((w0**2 - w**2) ** 2 + g**2 * w**2)


close(amp(1e-9), F0 / k, 1e-9, "static 0.01")
close(amp(20), 0.1, 1e-12, "resonance 0.1")
close(amp(40), 0.0033, 0.00005, "fast 0.0033")
# steady state by RK4 at w = w0: run long, measure the amplitude
ser = rk4(lambda t, y: [y[1], -400 * y[0] - 2 * y[1] + 4 * cos(20 * t)], [0.0, 0.0], 0.0, 2e-4, 60000)
tail = [y[0] for t, y in ser[-4000:]]
close(max(tail), 0.1, 2e-3, "RK4 steady amplitude at resonance")
ans("resonance-amplitude", 20 * 1 / 500 * 100)
close(1 / 500 * 20, 0.04, 1e-12, "Q F0/k")
ans("displacement-resonance", sqrt(400 - 4 / 2), 0.005)
# the displacement peak really is there (scan), the velocity peak at omega0
ws = [19.9 + i * 1e-4 for i in range(1001)]
wpk = max(ws, key=lambda w: amp(w))
close(wpk, sqrt(398), 2e-4, "scan displacement peak")
wv = max(ws + [20 + i * 1e-4 for i in range(1, 1001)], key=lambda w: w * amp(w))
close(wv, 20, 2e-4, "velocity peak at omega0")
# half-power width = gamma exactly: (w0^2 - w^2) = +/- g w
wl = (-2 + sqrt(4 + 4 * 400)) / 2
wh = (2 + sqrt(4 + 4 * 400)) / 2
close(wh - wl, 2, 1e-12, "half-power width")
ans("bandwidth", 1000 / 100)
# phase lag pi/2 at resonance
close(math.atan2(2 * 20, 400 - 400), pi / 2, 1e-12, "delta = pi/2")

# ==== 耦合振动 ====
ans("antisymmetric-frequency", sqrt(3 * 400), 0.005)
# eigenvalues of [[2,-1],[-1,2]]: (2-l)^2 - 1 = 0
for lam in (1, 3):
    close((2 - lam) ** 2 - 1, 0, 1e-12, "char poly")
# transfer time: pi / (w2 - w1)
ans("energy-transfer-time", pi / (3.23 - 3.13), 0.05)
# check by RK4 that x1 first vanishes near pi/(w2-w1) for two weakly coupled oscillators
w1s, w2s = 3.13, 3.23
kc = (w2s**2 - w1s**2) / 2  # spring term per unit mass so that the out-of-phase mode is w2
ser = rk4(lambda t, y: [y[2], y[3], -w1s**2 * y[0] - kc * (y[0] - y[1]), -w1s**2 * y[1] - kc * (y[1] - y[0])],
          [1.0, 0.0, 0.0, 0.0], 0.0, 0.002, 20000)
env = [(t, abs(y[0]) + abs(y[2]) / w1s) for t, y in ser]
first_min = min((e for e in env if 20 < e[0] < 40), key=lambda e: e[1])
close(first_min[0], pi / (w2s - w1s), 0.03, "RK4 transfer time")
ans("unequal-coupling", sqrt((100 + 2 * 50) / 1), 0.005)


def chain_freqs(N, w0):
    return [2 * w0 * sin(n * pi / (2 * (N + 1))) for n in range(1, N + 1)]


def tridiag_det(N, lam):
    """det(K - lam I) for K = tridiag(-1, 2, -1) (in units of k/m)."""
    a, b_ = 1.0, 2 - lam
    for _ in range(N - 1):
        a, b_ = b_, (2 - lam) * b_ - a
    return b_


for N in (2, 3, 5):
    for w in chain_freqs(N, 1.0):
        close(tridiag_det(N, w * w), 0, 1e-9, f"chain N={N}")
close(chain_freqs(2, 10)[1], sqrt(3) * 10, 1e-9, "N=2 gives sqrt3 w0")
ans("three-mass-middle-mode", chain_freqs(3, 10)[1], 0.005)
ans("chain-wave-speed", sqrt(100 / 0.01) * 0.01)
ans("b-mode-count", len(chain_freqs(5, 1.0)))

# ==== 波 ====
ans("string-speed", sqrt(100 / 0.01))
ans("pulse-time", 12 / sqrt(72 / 0.08))
close(10 / sqrt(50 / 0.02), 0.2, 1e-12, "example pulse")
ans("sound-wavelength", 343 / 440, 0.005)
ans("phase-difference-points", degrees(2 * pi / 2 * 0.5))
mu, f, Aw, v = 0.01, 100.0, 0.005, 100.0
w = 2 * pi * f
P = 0.5 * mu * w**2 * Aw**2 * v
ans("string-wave-power", P, 0.005)
# average power = time average of -T y_x y_t at x = 0, with T = mu v^2
T = mu * v**2
kk = w / v
n = 2000
avg = sum(-T * (-Aw * kk * sin(-w * (i / n) / f)) * (Aw * w * sin(-w * (i / n) / f)) for i in range(n)) / n
close(avg, P, 1e-6, "power from energy flux")
ans("inverse-square", (6 / 2) ** 2)
ans("wave-vector-length", 2 * pi / 5, 0.0005)
ans("node-spacing", 0.8 / 2)
ans("string-fundamental", sqrt(100 / 0.01) / (2 * 0.5))
# triangle plucked at the middle: even Fourier coefficients vanish
L = 1.0
tri = lambda x: x if x < 0.5 else 1 - x
M = 20000
for nn in (1, 2, 3, 4):
    bn = 2 / L * sum(tri((i + 0.5) / M) * sin(nn * pi * (i + 0.5) / M) for i in range(M)) / M
    if nn % 2 == 0:
        close(bn, 0, 1e-9, f"even harmonic {nn}")
    else:
        close(bn, 4 / (nn * pi) ** 2 * sin(nn * pi / 2), 1e-6, f"odd harmonic {nn}")
ans("echo-distance", 343 * 2 / 2)
close(sqrt(1.4 * 101325 / 1.204), 343, 0.5 / 343, "air sound speed")
close(sqrt(2.2e9 / 1000), 1480, 5 / 1480, "water about 1480")
ans("closed-pipe", 343 / (4 * 0.25))
ans("decibel-level", 10 * log10(1e-6 / 1e-12))
ans("two-sources-db", 60 + 10 * log10(2), 0.05)
ans("deep-water-phase", sqrt(9.8 / (2 * pi / 10)), 0.005)
ans("group-from-table", (101 - 100) / (10.2 - 10.0), 1e-9)
kq = 0.7
h = 1e-6
vg = (sqrt(9.8 * (kq + h)) - sqrt(9.8 * (kq - h))) / (2 * h)
ans("deep-water-ratio", vg / (sqrt(9.8 * kq) / kq), 1e-6)
ans("pulse-bandwidth", 1 / 1e-6 / 1e6)

# ==== 干涉与衍射 ====
close(0.1715 / (343 / 1000), 0.5, 1e-12, "speakers half wavelength")
ans("fringe-spacing", 500e-9 * 1 / 0.2e-3 * 1e3)
close(1.8e-3 * 0.5e-3 / 1.5, 600e-9, 1e-15, "example 600 nm")
ans("wavelength-from-fringes", 27 / 6 * 1e-3 * 0.25e-3 / 2 * 1e9, 0.05)
ans("quarter-path-intensity", cos(pi / 4) ** 2)
# two-slit intensity from phasors averages to 2 I1
avg2 = sum(abs(1 + complex(cos(2 * pi * i / 1000), sin(2 * pi * i / 1000))) ** 2 for i in range(1000)) / 1000
close(avg2, 2, 1e-9, "average 2 I1")
ans("optical-path", (1.5 - 1) * 1e-3 * 1e6)
close(550 / (4 * 1.38), 99.6, 0.05 / 99.6, "AR coating 99.6")
ans("soap-film-thickness", 600 / (4 * 1.33), 0.05)
# check soap film: phase from path 2nt plus one flip gives constructive
t_ = 600 / (4 * 1.33)
close((2 * 1.33 * t_ + 600 / 2) / 600, 1, 1e-12, "soap constructive")
ans("wedge-spacing", 589e-9 / (2 * 1e-4) * 1e3, 0.0005)
ans("newton-ring", sqrt(4 * 600e-9 * 1) * 1e3, 0.005)
# Newton ring: air gap at radius r is r^2/(2R); dark when 2t = m lambda
r4 = sqrt(4 * 600e-9 * 1)
close(2 * (r4**2 / 2), 4 * 600e-9, 1e-18, "ring gap")
ans("michelson-shift", 200 * 632.8e-9 / 2 * 1e6, 0.005)
ans("single-slit-angle", asin(500e-9 / 1e-4) * 1e3, 1e-3)
# single slit: summing Huygens wavelets across the slit gives zero at a sin = lambda
a, lam = 1e-4, 500e-9
th = asin(lam / a)
S = sum(complex(cos(2 * pi * (i + 0.5) / 1000 * a * sin(th) / lam), sin(2 * pi * (i + 0.5) / 1000 * a * sin(th) / lam)) for i in range(1000))
close(abs(S) / 1000, 0, 1e-9, "single slit first dark")
ans("central-width", 2 * 2 * lam / a * 1e3, 0.01)
close(1.22 * 550e-9 / 3e-3, 2.24e-4, 0.005e-4 / 2.24e-4, "eye angle")
close(1.22 * 550e-9 / 3e-3 * 1000, 0.22, 0.005 / 0.22, "eye 0.22 m")
ans("telescope-resolution", 1.22 * 550e-9 / 2.4 / 1e-7, 0.005)
close((1.22 * 550e-9 / 3e-3) / (1.22 * 550e-9 / 2.4), 800, 1e-9, "800 times")
d = 1e-3 / 600
ans("grating-angle", degrees(asin(500e-9 / d)), 0.05)
ans("grating-max-order", math.floor(d / 500e-9))
close(3 * 500e-9 / d, 0.9, 1e-12, "third order sin 0.9")
# N-slit phasor sum: N^2 at the principal maximum, zero N-1 times in between
Nsl = 6
I = lambda ph: abs(sum(complex(cos(j * ph), sin(j * ph)) for j in range(Nsl))) ** 2
close(I(2 * pi), Nsl**2, 1e-9, "principal max N^2")
zeros = sum(1 for q in range(1, Nsl) if I(2 * pi * q / Nsl) < 1e-18)
close(zeros, Nsl - 1, 0, "N-1 minima")
close(589 / 0.6, 982, 0.5 / 982, "sodium 982")
ans("grating-resolve", 600 / 0.3 / 2, 1)
ans("phased-array-angle", degrees(asin((pi / 2) * 1 / (2 * pi * 0.5))))

# ==== 偏振 ====
ans("two-polarizers", 0.5 * cos(radians(60)) ** 2)
ans("three-polarizers", 0.5 * cos(radians(45)) ** 2 * cos(radians(45)) ** 2)
ans("polarizer-angle", degrees(math.acos(sqrt(3 / 8 * 2))))
# natural light: average of cos^2 over all angles is 1/2
close(sum(cos(2 * pi * i / 3600) ** 2 for i in range(3600)) / 3600, 0.5, 1e-12, "mean cos^2")
thB = atan(1.5)
ans("brewster-glass", degrees(thB), 0.05)
# Fresnel r_p vanishes at Brewster, reflected and refracted rays perpendicular
th2 = asin(sin(thB) / 1.5)
rp = (1.5 * cos(thB) - 1 * cos(th2)) / (1.5 * cos(thB) + 1 * cos(th2))
close(rp, 0, 1e-12, "r_p = 0")
close(thB + th2, pi / 2, 1e-12, "perpendicular rays")
ans("quarter-wave-thickness", 589e-9 / (4 * 0.009) * 1e6, 0.05)
ans("half-wave-rotation", 2 * 20)
# half-wave plate: flip the slow component; angle goes from +20 to -20 about the fast axis
ex, ey = cos(radians(20)), sin(radians(20))
close(degrees(math.atan2(-ey, ex)), -20, 1e-9, "half-wave mirror")

# ==== 几何光学 ====
ans("air-to-water", degrees(asin(sin(radians(45)) / 1.33)), 0.05)
ans("speed-in-glass", 3.0e8 / 1.5 / 1e8)
# Fermat: the least-time path from A (0, 1) in air to B (1, -1) in water obeys Snell
ya, yb, xb, n1, n2 = 1.0, -1.0, 1.0, 1.0, 1.33
tt = lambda x: n1 * sqrt(x**2 + ya**2) + n2 * sqrt((xb - x) ** 2 + yb**2)
lo, hi = 0.0, 1.0
for _ in range(200):
    m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
    if tt(m1) < tt(m2):
        hi = m2
    else:
        lo = m1
xs = (lo + hi) / 2
s1 = xs / sqrt(xs**2 + ya**2)
s2 = (xb - xs) / sqrt((xb - xs) ** 2 + yb**2)
close(n1 * s1, n2 * s2, 1e-6, "Fermat gives Snell")
assert xs > 0.5  # more of the path in air than the straight line
checks += 1
ans("glass-critical", degrees(asin(1 / 1.5)), 0.05)
ans("fiber-critical", degrees(asin(1.46 / 1.48)), 0.05)
close(90 - degrees(asin(1.46 / 1.48)), 9.4, 0.05 / 9.4, "9.4 deg")
close(500 / 1.33, 376, 0.5 / 376, "376 nm")
ans("mirror-distance", 2 * (1.5 - 0.5))


def image(f, do):
    return 1 / (1 / f - 1 / do)


ans("concave-image", image(40 / 2, 60))
close(-image(20, 60) / 60, -0.5, 1e-12, "concave m")
ans("convex-image", image(-20, 20))
close(image(-15, 30), -10, 1e-12, "example convex")
close(-image(-15, 30) / 30, 1 / 3, 1e-12, "example m 1/3")
# paraxial ray check of the mirror equation for a concave mirror R = 40: a ray from the axis point at 60 cm
R = 40.0
y0 = 0.01
ang = y0 / 60  # small slope from the object point to the mirror
ang_out = 2 * y0 / R - ang  # reflection off a sphere of radius R (paraxial)
close(y0 / ang_out, 30, 1e-6, "ray trace mirror")
ans("apparent-depth", 1.33 / 1.33)
close(2.0 / 1.33, 1.5, 0.005, "pool 2 m looks 1.5 m")
ans("lensmaker", 1 / (0.5 * (1 / 20 - 1 / -20)))
close(image(10, 15), 30, 1e-9, "example lens 30")
ans("magnifier-virtual", image(10, 5))
ans("diverging-lens", -image(-20, 20) / 20)
# ray trace a thin lens: two refractions of a 1.5 glass biconvex lens, R = 20, thin
# single surface: n1/do + n2/di = (n2 - n1)/R
di1 = 1.5 / ((1.5 - 1) / 20 - 1 / 1e12)  # object at infinity, first surface
do2 = -di1  # virtual object for the second surface (thin lens)
di2 = 1 / ((1 - 1.5) / -20 - 1.5 / do2)
close(di2, 20, 1e-6, "two surfaces give f = 20")
for do, kind in ((30, "far"), (15, "mid"), (5, "near")):
    di = image(10, do)
    mm = -di / do
    if kind == "far":
        assert 10 < di < 20 and abs(mm) < 1
    elif kind == "mid":
        assert di > 20 and abs(mm) > 1
    else:
        assert di < 0 and mm > 1
    checks += 1
ans("myopia-lens", 1 / -0.5)
ans("hyperopia-lens", 1 / 0.25 - 1 / 1.0)
ans("camera-focus", image(50, 2000), 0.05)
close(image(50, 2000) - 50, 1.3, 0.05, "1.3 mm")
ans("magnifier-power", 25 / 5)
ans("microscope-power", 16 / 0.4 * 25 / 2.5)
ans("telescope-power", 100 / 2.5)

# ==== 结业挑战 ====
ans("b-quality", sqrt(100 / 0.25) / (0.25 / 0.25))
ans("b-resonance", 15 * 2 / 400 * 100)
close(5 * 5 - 36 < 0, True, 0, "b-damping-type over")
ans("b-normal-mode", sqrt(3 * 180 / 0.5), 0.005)
close(sqrt(360), 18.97, 0.005, "b in-phase")
ans("b-string-harmonic", 3 * sqrt(64 / 0.01) / (2 * 0.4))
ans("b-closed-pipe", 343 / (4 * 0.17), 0.05)
ans("b-double-slit", 600e-9 * 1.2 / 0.3e-3 * 1e3)
ans("b-coating", 520 / (4 * 1.38), 0.05)
ans("b-rayleigh", 1.22 * 500e-9 / 0.1 / 1e-6, 0.05)
ans("b-grating", degrees(asin(600e-9 / (1e-3 / 500))), 0.05)
ans("b-polarizers", 0.5 * cos(radians(30)) ** 2 * cos(radians(60)) ** 2, 0.0005)
close(0.5 * 0.75 * 0.25, 3 / 32, 1e-12, "3/32")
ans("b-brewster", degrees(atan(1.33)), 0.05)
ans("b-lens", image(12, 18))
ans("b-critical", degrees(asin(1 / 1.33)), 0.05)
for do in (1, 5, 20, 100):
    di = image(-15, do)
    assert di < 0 and 0 < -di / do < 1
    checks += 1

# ---- compare with the pack ----
pack = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "data" / "content" / "N.1.3.yaml"
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

print(f"N.1.3 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
