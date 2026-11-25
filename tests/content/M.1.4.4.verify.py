"""M.1.4.4 多元积分与向量分析 — every number in data/content/M.1.4.4.yaml, recomputed.

Run: python -I tests/content/M.1.4.4.verify.py
Plain Python, no third-party libraries. Double and triple integrals are evaluated with nested composite
Simpson rules (variable limits for type I/II regions), line integrals and fluxes by integrating the
parametrised integrand over t (or u, v), divergence and curl by central differences. Where the pack
uses a theorem (Green, divergence, Stokes) both sides are computed independently. The closed forms
quoted in the pack are checked against these numbers, and every number answer is read back from the
YAML and compared.
"""
import math
import re
from math import cos, e, exp, log, pi, sin, sqrt
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


def simpson(f, a, b, n=400):
    if n % 2:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


def dbl(f, a, b, g1, g2, n=200):
    """∫_a^b ∫_{g1(x)}^{g2(x)} f(x, y) dy dx."""
    return simpson(lambda x: simpson(lambda y: f(x, y), g1(x), g2(x), n), a, b, n)


def tpl(f, a, b, g1, g2, u1, u2, n=40):
    """∫_a^b ∫_{g1(x)}^{g2(x)} ∫_{u1(x,y)}^{u2(x,y)} f dz dy dx."""
    return simpson(lambda x: simpson(lambda y: simpson(lambda z: f(x, y, z), u1(x, y), u2(x, y), n), g1(x), g2(x), n), a, b, n)


def line(F, r, dr, a, b, n=2000):
    """∫ F(r(t))·r'(t) dt."""
    return simpson(lambda t: sum(p * q for p, q in zip(F(*r(t)), dr(t))), a, b, n)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def div(F, p, h=1e-5):
    s = 0.0
    for k in range(3):
        q1 = list(p); q2 = list(p); q1[k] += h; q2[k] -= h
        s += (F(*q1)[k] - F(*q2)[k]) / (2 * h)
    return s


def curl(F, p, h=1e-5):
    def d(i, k):  # ∂F_i/∂x_k
        q1 = list(p); q2 = list(p); q1[k] += h; q2[k] -= h
        return (F(*q1)[i] - F(*q2)[i]) / (2 * h)
    return (d(2, 1) - d(1, 2), d(0, 2) - d(2, 0), d(1, 0) - d(0, 1))


c0 = lambda *_: 0.0

# ---- double-volume ----
f = lambda x, y: x * x + y
mids = [(0.5, 0.5), (1.5, 0.5), (0.5, 1.5), (1.5, 1.5)]
vals = [f(*p) for p in mids]
for v, w in zip(vals, [0.75, 2.75, 1.75, 3.75]):
    close(v, w, 1e-12, "midpoint values x^2 + y")
close(sum(vals), 9, 1e-12, "midpoint sum x^2 + y")
exact = dbl(f, 0, 2, lambda x: 0, lambda x: 2)
close(exact, 28 / 3, 1e-9, "exact x^2 + y")
close(28 / 3, 9.33, 0.005, "28/3 ~ 9.33")
g = lambda x, y: x * y
corners = [(1, 1), (2, 1), (1, 2), (2, 2)]
ok([g(*p) for p in corners] == [1, 2, 2, 4], "corner values")
ans("riemann-corner", sum(g(*p) for p in corners))
ok([g(*p) for p in mids] == [0.25, 0.75, 0.75, 2.25], "midpoint values xy")
ans("riemann-mid", sum(g(*p) for p in mids))
close(dbl(g, 0, 2, lambda x: 0, lambda x: 2), 4, 1e-9, "exact xy")
ok((1 * 6, 4 * 6) == (6, 24), "bounds 6..24")
ok(2 * 3 != 2 + 3, "area 6 not 5")
ans("average", 18 / 6)
ans("linearity", 3 * 5 - 4 * (-2))

# ---- iterated ----
close(simpson(lambda y: 0.7 + 2 * y, 0, 1), 0.7 + 1, 1e-12, "inner x + 1 at x = 0.7")
close(dbl(lambda x, y: x + 2 * y, 0, 2, lambda x: 0, lambda x: 1), 4, 1e-9, "example 4")
close(simpson(lambda x: x + 2 * 0.3, 0, 2), 2 + 4 * 0.3, 1e-12, "inner 2 + 4y")
close(dbl(lambda y, x: x + 2 * y, 0, 1, lambda y: 0, lambda y: 2), 4, 1e-9, "other order 4")
ans("iter-1", dbl(lambda x, y: x * x * y, 1, 2, lambda x: 0, lambda x: 3), 0.0001)
close(21 / 2, 10.5, 1e-12, "21/2")
v = dbl(lambda x, y: sin(x) * exp(y), 0, pi / 2, lambda x: 0, lambda x: 1)
close(v, e - 1, 1e-9, "separable e - 1")
ans("iter-separable", v, 0.0005)
ans("iter-volume", dbl(lambda x, y: 4 - x - y, 0, 1, lambda x: 0, lambda x: 2))
ok(4 - 1 - 2 >= 1, "4 - x - y >= 1 on the rectangle")
close(simpson(lambda y: 0.6 * y * y, 0, 2), 8 * 0.6 / 3, 1e-12, "inner 8x/3")
close(dbl(lambda x, y: x * y * y, 0, 1, lambda x: 0, lambda x: 2), 4 / 3, 1e-9, "outer 4/3")

# ---- general-regions ----
close(simpson(lambda y: 0.8 + y, 0, 0.8), 1.5 * 0.8 ** 2, 1e-12, "inner 3x^2/2")
close(dbl(lambda x, y: x + y, 0, 1, lambda x: 0, lambda x: x), 0.5, 1e-9, "triangle example 1/2")
ans("region-volume", dbl(lambda x, y: x * y, 0, 2, lambda x: 0, lambda x: x))
ok(all(abs(2 * x - x * x) < 1e-12 for x in (0, 2)), "2x = x^2 at 0, 2")
ans("region-area", dbl(lambda x, y: 1, 0, 2, lambda x: x * x, lambda x: 2 * x), 0.0005)
close(4 - 8 / 3, 4 / 3, 1e-12, "4 - 8/3")
v = dbl(lambda x, y: x, 0, 1, lambda x: x * x, lambda x: x)
close(v, 1 / 12, 1e-9, "1/12")
ans("region-x", v, 0.00005)

# ---- triple-box ----
close(simpson(lambda z: 0.4 + 1.2 * z, 0, 3), 3 * 0.4 + 9 * 1.2 / 2, 1e-12, "inner 3x + 9y/2")
close(simpson(lambda y: 3 * 0.4 + 4.5 * y, 0, 2), 6 * 0.4 + 9, 1e-12, "middle 6x + 9")
close(tpl(lambda x, y, z: x + y * z, 0, 1, lambda x: 0, lambda x: 2, lambda x, y: 0, lambda x, y: 3), 12, 1e-9, "example 12")
ans("box-xyz", tpl(lambda x, y, z: x * y * z, 0, 1, lambda x: 0, lambda x: 1, lambda x, y: 0, lambda x, y: 2), 0.0001)
close(simpson(lambda z: 1 + z, 0, 1), 1.5, 1e-12, "1.5")
ans("box-mass", tpl(lambda x, y, z: 1 + z, 0, 2, lambda x: 0, lambda x: 3, c0, lambda x, y: 1), 0.0001)
ok(math.factorial(3) == 6, "six orders")
I = tpl(lambda x, y, z: x * x, 0, 3, lambda x: 0, lambda x: 3, c0, lambda x, y: 3)
close(I, 81, 1e-9, "81")
ans("box-average", I / 27)

# ---- triple-general ----
tet = lambda F, s=1: tpl(F, 0, s, lambda x: 0, lambda x: s - x, c0, lambda x, y: s - x - y)
close(tet(lambda x, y, z: 1), 1 / 6, 1e-9, "tetra volume 1/6")
v = tet(lambda x, y, z: x)
close(v, 1 / 24, 1e-9, "tetra x 1/24")
close(0.5 * (0.5 - 2 / 3 + 0.25), 1 / 24, 1e-12, "(1/2)(1/2 - 2/3 + 1/4)")
ans("tetra-x", v, 0.00005)
v = tpl(lambda x, y, z: z, 0, 1, lambda x: 0, lambda x: 1, c0, lambda x, y: x + y)
close(v, 7 / 12, 1e-9, "7/12")
close(0.5 * (1 / 3 + 1 / 2 + 1 / 3), 7 / 12, 1e-12, "(1/2)(1/3 + 1/2 + 1/3)")
ans("z-over-wedge", v, 0.0005)
ok(sqrt(9) == 3, "shadow radius 3")
v = dbl(lambda x, y: 4 - x * x - y * y, 0, 1, lambda x: 0, lambda x: 1)
close(v, 10 / 3, 1e-9, "10/3")
ans("under-paraboloid", v, 0.0005)

# ---- decompose ----
a1 = dbl(lambda x, y: x + y, 0, 2, lambda x: 0, lambda x: 1)
a2 = dbl(lambda x, y: x + y, 0, 1, lambda x: 1, lambda x: 2)
close(a1, 3, 1e-9, "L part 1"); close(a2, 2, 1e-9, "L part 2")
close(simpson(lambda x: x, 0, 1), 0.5, 1e-12, "0.5"); close(simpson(lambda y: y, 1, 2), 1.5, 1e-12, "1.5")
ans("l-shape", a1 + a2)
t1 = dbl(lambda x, y: y, 0, 1, lambda x: 0, lambda x: x)
t2 = dbl(lambda x, y: y, 1, 2, lambda x: 0, lambda x: 2 - x)
close(t1, 1 / 6, 1e-9, "triangle part 1"); close(t2, 1 / 6, 1e-9, "triangle part 2")
close(dbl(lambda y, x: y, 0, 1, lambda y: y, lambda y: 2 - y), 1 / 3, 1e-9, "type II 1/3")
close(1 - 2 / 3, 1 / 3, 1e-12, "1 - 2/3")
ok(abs(2 - (4 - 2)) < 1e-12, "y = x meets y = 4 - x at x = 2 -> 2 pieces")
big = dbl(lambda x, y: x * x, -2, 2, lambda x: -2, lambda x: 2)
small = dbl(lambda x, y: x * x, -1, 1, lambda x: -1, lambda x: 1)
close(big, 64 / 3, 1e-9, "64/3"); close(small, 4 / 3, 1e-9, "4/3")
ans("frame", big - small)
ans("frame-area", 16 - 4)

# ---- change-order ----
v = dbl(lambda y, x: exp(y * y), 0, 1, lambda y: 0, lambda y: y)
close(v, (e - 1) / 2, 1e-9, "(e - 1)/2"); close(v, 0.859, 0.0005, "0.859")
close(dbl(lambda y, x: x, 0, 1, lambda y: y, lambda y: sqrt(y), 400), 1 / 12, 1e-6, "x-first 1/12")
close(0.5 * (0.5 - 1 / 3), 1 / 12, 1e-12, "(1/2)(1/2 - 1/3)")
ok(abs(sqrt(4) - 2) < 1e-12, "x = sqrt(y) reaches 2 at y = 4")
v = dbl(lambda x, y: sin(x * x), 0, 1, lambda x: 0, lambda x: x)
close(v, (1 - cos(1)) / 2, 1e-9, "(1 - cos 1)/2")
ans("swap-sin", v, 0.0005)
ok(all(abs(y / 2 - y / 2) < 1e-12 for y in (0, 1, 2)), "x >= y/2")
v = dbl(lambda y, x: exp(-y * y), 0, 1, lambda y: 0, lambda y: y)
close(v, (1 - exp(-1)) / 2, 1e-9, "(1 - 1/e)/2")
ans("swap-exp", v, 0.0005)

# ---- polar ----
pol = lambda F, a, b, h1, h2, n=200: dbl(lambda t, r: F(r * cos(t), r * sin(t)) * r, a, b, h1, h2, n)
inner = simpson(lambda r: exp(-r * r) * r, 0, 2)
close(inner, (1 - exp(-4)) / 2, 1e-9, "inner (1 - e^-4)/2")
v = pol(lambda x, y: exp(-(x * x + y * y)), 0, 2 * pi, lambda t: 0, lambda t: 2)
close(v, pi * (1 - exp(-4)), 1e-9, "pi(1 - e^-4)"); close(v, 3.084, 0.0005, "3.084")
close(dbl(lambda x, y: exp(-(x * x + y * y)), -2, 2, lambda x: -sqrt(4 - x * x), lambda x: sqrt(4 - x * x), 600), v, 1e-4, "same in x, y")
v = pol(lambda x, y: x * x + y * y, 0, 2 * pi, lambda t: 0, lambda t: 1)
close(v, pi / 2, 1e-9, "pi/2"); ans("polar-r2", v, 0.0005)
v = pol(lambda x, y: 1 / (x * x + y * y), 0, 2 * pi, lambda t: 1, lambda t: 2)
close(v, 2 * pi * log(2), 1e-9, "2 pi ln 2"); ans("polar-ring", v, 0.0005)
close(pol(lambda x, y: 1, -pi / 2, pi / 2, lambda t: 0, lambda t: 2 * cos(t)), pi, 1e-9, "r = 2cos area pi")
close(pol(lambda x, y: 4 - x * x - y * y, 0, 2 * pi, lambda t: 0, lambda t: 2), 8 * pi, 1e-9, "8 pi")
v = pol(lambda x, y: 1, 0, 2 * pi, lambda t: 0, lambda t: 1 + cos(t))
close(v, 1.5 * pi, 1e-9, "cardioid"); ans("cardioid", v, 0.0005)
v = pol(lambda x, y: 9 - x * x - y * y, 0, 2 * pi, lambda t: 0, lambda t: 3)
close(v, 81 * pi / 2, 1e-9, "81 pi/2"); ans("paraboloid-volume", v, 0.0005)

# ---- cyl-sph ----
close(tpl(lambda t, r, z: r, 0, 2 * pi, lambda t: 0, lambda t: 1, c0, lambda t, r: r * r), pi / 2, 1e-9, "cylinder example pi/2")
v = tpl(lambda t, r, z: r * r, 0, 2 * pi, lambda t: 0, lambda t: 1, c0, lambda t, r: 2)
close(v, 4 * pi / 3, 1e-9, "4 pi/3"); ans("cyl-mass", v, 0.0005)
sph = lambda F, rho_max, phi_max: tpl(lambda t, ph, rh: F(rh) * rh * rh * sin(ph), 0, 2 * pi, lambda t: 0, lambda t: phi_max, c0, lambda t, ph: rho_max)
close(sph(lambda r: 1, 2, pi), 4 * pi * 8 / 3, 1e-6, "ball volume R = 2")
v = sph(lambda r: r * r, 1, pi)
close(v, 4 * pi / 5, 1e-6, "4 pi/5"); ans("sph-r2", v, 0.0005)
v = sph(lambda r: 1, 1, pi / 4)
close(v, (1 / 3) * (1 - sqrt(2) / 2) * 2 * pi, 1e-6, "cone volume"); ans("cone-volume", v, 0.0005)

# ---- jacobian ----
jac = lambda xu, xv, yu, yv: xu * yv - xv * yu
ok(2 * 3 == 6, "guess area 6")
close(jac(1, 1, 1, -1), -2, 1e-12, "J = -2")
P = [(0, 0), (1, 1), (2, 0), (1, -1)]
close(math.dist(P[0], P[1]), sqrt(2), 1e-12, "side sqrt 2"); close(math.dist(P[0], P[1]) ** 2, 2, 1e-12, "area 2")
ans("jac-linear", jac(3, 1, 1, 2))
u, vv = 2, 3
ans("jac-point", jac(vv, u, 0, 1))
ans("jac-image-area", abs(jac(1, -1, 2, 1)) * 2)
for r, t in [(0.7, 0.3), (2.0, 1.9)]:
    close(jac(cos(t), -r * sin(t), sin(t), r * cos(t)), r, 1e-12, "polar J = r")

# ---- change-vars ----
close(abs(jac(0.5, 0.5, 0.5, -0.5)), 0.5, 1e-12, "|J| = 1/2")
close(abs(jac(1, 1, 1, -1)), 2, 1e-12, "d(u,v)/d(x,y) = 2, its inverse 1/2")
close(dbl(lambda u, v: u * 0.5, 0, 2, lambda u: 0, lambda u: 2), 2, 1e-9, "parallelogram example 2")
# direct in x, y: the parallelogram 0 <= x + y <= 2, 0 <= x - y <= 2 has vertices (0,0), (1,1), (2,0), (1,-1)
def in_par(F):
    left = dbl(F, 0, 1, lambda x: -x, lambda x: x, 400)
    right = dbl(F, 1, 2, lambda x: x - 2, lambda x: 2 - x, 400)
    return left + right
close(in_par(lambda x, y: x + y), 2, 1e-6, "x + y directly")
v = dbl(lambda u, w: w * w * 0.5, 0, 2, lambda u: 0, lambda u: 2)
close(v, 8 / 3, 1e-9, "8/3"); close(in_par(lambda x, y: (x - y) ** 2), 8 / 3, 1e-6, "(x - y)^2 directly")
ans("parallelogram-square", v, 0.0005)
def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
for rh, ph, th in [(1.3, 0.7, 2.1), (0.5, 2.0, 4.0)]:
    m = [[sin(ph) * cos(th), rh * cos(ph) * cos(th), -rh * sin(ph) * sin(th)],
         [sin(ph) * sin(th), rh * cos(ph) * sin(th), rh * sin(ph) * cos(th)],
         [cos(ph), -rh * sin(ph), 0]]
    close(det3(m), rh * rh * sin(ph), 1e-12, "spherical Jacobian")
close(det3([[1, 0, 0], [0, 2, 0], [0, 0, 3]]), 6, 1e-12, "abc")
v = pol(lambda x, y: 1, 0, 2 * pi, lambda t: 0, lambda t: 1) * 3 * 2
close(v, 6 * pi, 1e-9, "6 pi"); ans("ellipse-area", v, 0.0005)
close(dbl(lambda x, y: 1, -3, 3, lambda x: -2 * sqrt(max(0, 1 - x * x / 9)), lambda x: 2 * sqrt(max(0, 1 - x * x / 9)), 2000), 6 * pi, 1e-3, "ellipse directly")
ans("ellipsoid-volume", 6 * 4 * pi / 3, 0.0005)
close(6 * 4 * pi / 3, 8 * pi, 1e-12, "8 pi")

# ---- line-integrals ----
v = line(lambda x, y: (y, x), lambda t: (t, t * t), lambda t: (1, 2 * t), 0, 1)
close(v, 1, 1e-9, "example 1"); close(0.3 ** 2 + 0.3 * 2 * 0.3, 3 * 0.3 ** 2, 1e-12, "3t^2")
ans("segment-work", line(lambda x, y: (x, y), lambda t: (2 * t, t), lambda t: (2, 1), 0, 1), 0.0001)
v = line(lambda x, y: (y, x * x), lambda t: (t, t ** 3), lambda t: (1, 3 * t * t), 0, 1)
close(v, 0.25 + 0.6, 1e-9, "1/4 + 3/5"); ans("cubic-path", v, 0.0001)
close(line(lambda x, y: (-y, x), lambda t: (cos(t), sin(t)), lambda t: (-sin(t), cos(t)), 0, 2 * pi), 2 * pi, 1e-9, "circle 2 pi")
v = line(lambda x, y: (-y, x), lambda t: (cos(t), sin(t)), lambda t: (-sin(t), cos(t)), 0, pi)
close(v, pi, 1e-9, "half circle"); ans("half-circle", v, 0.0005)
close(line(lambda x, y: (y, x), lambda t: (1 - t, (1 - t) ** 2), lambda t: (-1, -2 * (1 - t)), 0, 1), -1, 1e-9, "reversed -1")

# ---- line-space ----
helix = line(lambda x, y, z: (y, z, x), lambda t: (cos(t), sin(t), t), lambda t: (-sin(t), cos(t), 1), 0, 2 * pi)
close(helix, -pi, 1e-9, "helix -pi")
close(simpson(lambda t: -sin(t) ** 2, 0, 2 * pi), -pi, 1e-9, "-sin^2 part")
close(simpson(lambda t: t * cos(t), 0, 2 * pi), 0, 1e-9, "t cos t part")
close(simpson(cos, 0, 2 * pi), 0, 1e-9, "cos part")
ans("space-segment", line(lambda x, y, z: (x, y, z), lambda t: (t, 2 * t, 2 * t), lambda t: (1, 2, 2), 0, 1), 0.0001)
v = line(lambda x, y, z: (z, x, y), lambda t: (t, t * t, t ** 3), lambda t: (1, 2 * t, 3 * t * t), 0, 1)
close(v, 91 / 60, 1e-9, "91/60"); close(0.25 + 2 / 3 + 0.6, 91 / 60, 1e-12, "1/4 + 2/3 + 3/5")
ans("twisted-cubic", v, 0.0005)
m, gg = 2, 9.8
v = line(lambda x, y, z: (0, 0, -m * gg), lambda t: (t, sin(3 * t), 5 - 3 * t), lambda t: (1, 3 * cos(3 * t), -3), 0, 1)
close(v, 3 * m * gg, 1e-9, "gravity work on a wiggly path"); ans("gravity-work", v, 0.0001)

# ---- flux ----
ok(3 * 2 == 6, "net 6 m^3/s")
ans("disk-flux", 3 * pi * 4, 0.0005)
close(3 * pi * 4, 37.699, 0.0005, "12 pi")
ok(cross((1, 0, 0), (0, 1, 0)) == (0, 0, 1), "i x j = k")
cx = cross((1, 2, 3), (4, 5, 6))
ok(cx == (-3, 6, -3), "(1,2,3) x (4,5,6)")
ok(sum(p * q for p, q in zip(cx, (1, 2, 3))) == 0 and sum(p * q for p, q in zip(cx, (4, 5, 6))) == 0, "cross is perpendicular")
ans("cross-third", cx[2])
fx, fy = 0.3, -0.8
ok(cross((1, 0, fx), (0, 1, fy)) == (-fx, -fy, 1), "graph normal (-f_x, -f_y, 1)")
close(dbl(lambda x, y: x + y + (1 - x - y), 0, 1, lambda x: 0, lambda x: 1 - x), 0.5, 1e-9, "plane piece flux 1/2")
def sphere_flux(F, a, n=200):
    def integrand(ph, th):
        p = (a * sin(ph) * cos(th), a * sin(ph) * sin(th), a * cos(ph))
        nn = (p[0] / a, p[1] / a, p[2] / a)
        return sum(u * w for u, w in zip(F(*p), nn)) * a * a * sin(ph)
    return dbl(integrand, 0, pi, lambda ph: 0, lambda ph: 2 * pi, n)
v = sphere_flux(lambda x, y, z: (x, y, z), 2)
close(v, 32 * pi, 1e-8, "32 pi"); ans("sphere-flux", v, 0.0005)
v = dbl(lambda x, y: sum(u * w for u, w in zip((0, 0, x * x + y * y), (-2 * x, -2 * y, 1))), 0, 1, lambda x: 0, lambda x: 1)
close(v, 2 / 3, 1e-9, "2/3"); ans("graph-flux", v, 0.0005)

# ---- conservative ----
close(line(lambda x, y: (2 * x * y + 3, x * x + 4 * y), lambda t: (t, 2 * t * t), lambda t: (1, 4 * t), 0, 1), 13, 1e-9, "potential example 13 along a curve")
fpot = lambda x, y: x * x * y + 3 * x + 2 * y * y
close(fpot(1, 2) - fpot(0, 0), 13, 1e-12, "f(1,2) = 13")
ok((fpot(2, 3), fpot(1, 1)) == (36, 6), "36 and 6")
v = line(lambda x, y: (2 * x * y + 3, x * x + 4 * y), lambda t: (1 + t, 1 + 2 * t + sin(pi * t)), lambda t: (1, 2 + pi * cos(pi * t)), 0, 1)
close(v, 30, 1e-9, "path independence 30"); ans("potential-work", fpot(2, 3) - fpot(1, 1))
h = 1e-6
for (x, y) in [(0.4, -1.2), (2.0, 0.5)]:
    close((fpot(x + h, y) - fpot(x - h, y)) / (2 * h), 2 * x * y + 3, 1e-6, "f_x")
    fq = lambda x, y: x * x + x * y + y * y
    close((fq(x + h, y) - fq(x - h, y)) / (2 * h), 2 * x + y, 1e-6, "x^2 + xy + y^2 f_x")
    close((fq(x, y + h) - fq(x, y - h)) / (2 * h), x + 2 * y, 1e-6, "x^2 + xy + y^2 f_y")
fs = lambda x, y, z: x * y * z + z * z
v = line(lambda x, y, z: (y * z, x * z, x * y + 2 * z), lambda t: (t, 2 * t * t, 3 * t ** 3), lambda t: (1, 4 * t, 9 * t * t), 0, 1)
close(v, 15, 1e-9, "space potential along a curve"); ans("space-potential", fs(1, 2, 3) - fs(0, 0, 0))

# ---- curl-div ----
pc = lambda F, x, y: curl(lambda a, b, c: (*F(a, b), 0.0), (x, y, 0.0))[2]
close(pc(lambda x, y: (-y, x), 0.3, 0.9), 2, 1e-6, "curl (-y, x) = 2")
close(pc(lambda x, y: (y, x), 0.3, 0.9), 0, 1e-6, "curl (y, x) = 0")
v = pc(lambda x, y: (x * x * y, 3 * x * y), 1, 2)
close(v, 5, 1e-6, "plane curl 5"); ans("plane-curl", round(v, 9))
v = div(lambda x, y, z: (x * y, y * z, z * x), (1, 2, 3))
close(v, 6, 1e-6, "div 6"); ans("div-point", round(v, 9))
c = curl(lambda x, y, z: (y * y, z * z, x * x), (1, 2, 3))
close(c[0], -6, 1e-6, "curl first"); close(c[1], -2, 1e-6, "curl second"); close(c[2], -4, 1e-6, "curl third")
ans("curl-first", round(c[0], 9))
Fe = lambda x, y, z: (x * x * y, x * y * y, z)
for p in [(0.5, -1.0, 2.0), (1.5, 0.7, -0.3)]:
    close(div(Fe, p), 4 * p[0] * p[1] + 1, 1e-6, "div 4xy + 1")
    ce = curl(Fe, p)
    close(ce[0], 0, 1e-6, "curl x 0"); close(ce[1], 0, 1e-6, "curl y 0"); close(ce[2], p[1] ** 2 - p[0] ** 2, 1e-6, "curl z y^2 - x^2")
fsc = lambda x, y, z: x * x * y + sin(y * z)
gradf = lambda x, y, z: ((fsc(x + h, y, z) - fsc(x - h, y, z)) / (2 * h), (fsc(x, y + h, z) - fsc(x, y - h, z)) / (2 * h), (fsc(x, y, z + h) - fsc(x, y, z - h)) / (2 * h))
cg = curl(gradf, (0.4, 0.8, -0.6), 1e-3)
ok(all(abs(t) < 1e-4 for t in cg), "curl grad = 0")

# ---- green ----
close(line(lambda x, y: (x * x - y, x + y * y), lambda t: (t, 0), lambda t: (1, 0), 0, 1)
      + line(lambda x, y: (x * x - y, x + y * y), lambda t: (1, t), lambda t: (0, 1), 0, 1)
      + line(lambda x, y: (x * x - y, x + y * y), lambda t: (1 - t, 1), lambda t: (-1, 0), 0, 1)
      + line(lambda x, y: (x * x - y, x + y * y), lambda t: (0, 1 - t), lambda t: (0, -1), 0, 1), 2, 1e-9, "square example both sides 2")
v = line(lambda x, y: (3 * y, 5 * x), lambda t: (2 * cos(t), 2 * sin(t)), lambda t: (-2 * sin(t), 2 * cos(t)), 0, 2 * pi)
close(v, 8 * pi, 1e-9, "green circle directly"); ans("green-circle", 2 * 4 * pi, 0.0005)
sq = lambda F: (line(F, lambda t: (t, 0), lambda t: (1, 0), 0, 1) + line(F, lambda t: (1, t), lambda t: (0, 1), 0, 1)
                + line(F, lambda t: (1 - t, 1), lambda t: (-1, 0), 0, 1) + line(F, lambda t: (0, 1 - t), lambda t: (0, -1), 0, 1))
v = sq(lambda x, y: (x * y, x * x))
close(v, 0.5, 1e-9, "green square directly"); ans("green-square", dbl(lambda x, y: x, 0, 1, lambda x: 0, lambda x: 1), 0.0001)
a_, b_ = 3, 2
close(0.5 * line(lambda x, y: (-y, x), lambda t: (a_ * cos(t), b_ * sin(t)), lambda t: (-a_ * sin(t), b_ * cos(t)), 0, 2 * pi), pi * a_ * b_, 1e-9, "ellipse pi a b")
v = 0.5 * line(lambda x, y: (-y, x), lambda t: (cos(t) ** 3, sin(t) ** 3), lambda t: (-3 * cos(t) ** 2 * sin(t), 3 * sin(t) ** 2 * cos(t)), 0, 2 * pi)
close(v, 3 * pi / 8, 1e-9, "astroid 3 pi/8"); close(simpson(lambda t: sin(t) ** 2 * cos(t) ** 2, 0, 2 * pi), pi / 4, 1e-9, "pi/4")
ans("astroid-area", v, 0.0005)
close(-line(lambda x, y: (3 * y, 5 * x), lambda t: (2 * cos(t), 2 * sin(t)), lambda t: (-2 * sin(t), 2 * cos(t)), 0, 2 * pi),
      line(lambda x, y: (3 * y, 5 * x), lambda t: (2 * cos(-t), 2 * sin(-t)), lambda t: (2 * sin(-t), -2 * cos(-t)), 0, 2 * pi), 1e-9, "clockwise flips sign")

# ---- green-normal ----
def flux2(F, r, dr, a, b, n=2000):
    return simpson(lambda t: F(*r(t))[0] * dr(t)[1] - F(*r(t))[1] * dr(t)[0], a, b, n)
close(flux2(lambda x, y: (x, y), lambda t: (cos(t), sin(t)), lambda t: (-sin(t), cos(t)), 0, 2 * pi), 2 * pi, 1e-9, "unit circle outflow 2 pi")
v = flux2(lambda x, y: (x, y), lambda t: (3 * cos(t), 3 * sin(t)), lambda t: (-3 * sin(t), 3 * cos(t)), 0, 2 * pi)
close(v, 18 * pi, 1e-9, "18 pi directly"); ans("flux-circle", 2 * 9 * pi, 0.0005)
Fq = lambda x, y: (x * x, y * y)
v = (flux2(Fq, lambda t: (t, 0), lambda t: (1, 0), 0, 1) + flux2(Fq, lambda t: (1, t), lambda t: (0, 1), 0, 1)
     + flux2(Fq, lambda t: (1 - t, 1), lambda t: (-1, 0), 0, 1) + flux2(Fq, lambda t: (0, 1 - t), lambda t: (0, -1), 0, 1))
close(v, 2, 1e-9, "square outflow directly"); ans("flux-square", dbl(lambda x, y: 2 * x + 2 * y, 0, 1, lambda x: 0, lambda x: 1))
vortex = lambda x, y: (-y / (x * x + y * y), x / (x * x + y * y))
for a in (0.5, 3.0):
    close(line(vortex, lambda t: (a * cos(t), a * sin(t)), lambda t: (-a * sin(t), a * cos(t)), 0, 2 * pi), 2 * pi, 1e-9, "vortex circle 2 pi")
v = (line(vortex, lambda t: (2, -2 + 4 * t), lambda t: (0, 4), 0, 1, 4000) + line(vortex, lambda t: (2 - 4 * t, 2), lambda t: (-4, 0), 0, 1, 4000)
     + line(vortex, lambda t: (-2, 2 - 4 * t), lambda t: (0, -4), 0, 1, 4000) + line(vortex, lambda t: (-2 + 4 * t, -2), lambda t: (4, 0), 0, 1, 4000))
close(v, 2 * pi, 1e-9, "vortex square"); ans("vortex-square", v, 0.0005)
v = line(vortex, lambda t: (5 + cos(t), sin(t)), lambda t: (-sin(t), cos(t)), 0, 2 * pi)
close(v, 0, 1e-9, "vortex away"); ans("vortex-away", round(v, 9))
close(pc(vortex, 0.7, -1.3), 0, 1e-5, "vortex curl 0 away from origin")

# ---- divergence-thm ----
close(sphere_flux(lambda x, y, z: (x, y, z), 1), 4 * pi, 1e-8, "unit sphere 4 pi directly")
close(3 * 4 * pi / 3, 4 * pi, 1e-12, "3 x 4pi/3")
def cube_flux(F, n=60):
    tot = 0.0
    for k in range(3):
        for side, sgn in ((1.0, 1), (0.0, -1)):
            def g(u, w, k=k, side=side, sgn=sgn):
                p = [u, w]; p.insert(k, side)
                return sgn * F(*p)[k]
            tot += dbl(g, 0, 1, lambda u: 0, lambda u: 1, n)
    return tot
close(cube_flux(lambda x, y, z: (x, y, z)), 3, 1e-9, "cube flux directly"); ans("cube-flux", 3 * 1)
v = sph(lambda r: 3 * r * r, 1, pi)
close(v, 12 * pi / 5, 1e-6, "12 pi/5"); close(sphere_flux(lambda x, y, z: (x ** 3, y ** 3, z ** 3), 1), v, 1e-6, "cubic sphere directly")
ans("cubic-sphere", v, 0.0005)
close(div(lambda x, y, z: (y, z, x), (0.3, -0.2, 1.1)), 0, 1e-8, "div (y, z, x) = 0")
side = dbl(lambda th, z: (cos(th) * cos(th) + sin(th) * sin(th)) * 1, 0, 2 * pi, lambda th: 0, lambda th: 2)
close(side, 4 * pi, 1e-9, "cylinder side flux directly"); ans("cylinder-flux", 2 * pi * 2, 0.0005)

# ---- stokes ----
close(line(lambda x, y, z: (-y, x, 0), lambda t: (cos(t), sin(t), 0), lambda t: (-sin(t), cos(t), 0), 0, 2 * pi), 2 * pi, 1e-9, "stokes example line")
def hemi_curl_flux(Fc, n=200):  # upper unit hemisphere, outward
    def g(ph, th):
        p = (sin(ph) * cos(th), sin(ph) * sin(th), cos(ph))
        return sum(u * w for u, w in zip(Fc(*p), p)) * sin(ph)
    return dbl(g, 0, pi / 2, lambda ph: 0, lambda ph: 2 * pi, n)
close(hemi_curl_flux(lambda x, y, z: curl(lambda a, b, c: (-b, a, 0), (x, y, z))), 2 * pi, 1e-6, "hemisphere curl flux 2 pi")
v = line(lambda x, y, z: (z, x, y), lambda t: (2 * cos(t), 2 * sin(t), 0), lambda t: (-2 * sin(t), 2 * cos(t), 0), 0, 2 * pi)
close(v, 4 * pi, 1e-9, "stokes disk line"); ok(all(abs(c - 1) < 1e-6 for c in curl(lambda x, y, z: (z, x, y), (0.3, 0.4, 0.5))), "curl (1,1,1)")
ans("stokes-disk", 4 * pi, 0.0005)
v = line(lambda x, y, z: (-y ** 3, x ** 3, 0), lambda t: (cos(t), sin(t), 0), lambda t: (-sin(t), cos(t), 0), 0, 2 * pi)
close(v, 1.5 * pi, 1e-9, "3 pi/2 line"); close(pol(lambda x, y: 3 * x * x + 3 * y * y, 0, 2 * pi, lambda t: 0, lambda t: 1), 1.5 * pi, 1e-9, "3 pi/2 disk")
ans("stokes-cubic", v, 0.0005)
# paraboloid z = 9 - x^2 - y^2 upward: n dS = (2x, 2y, 1) dx dy over the disk r <= 3; curl F = (0, 0, 2)
v = pol(lambda x, y: sum(u * w for u, w in zip(curl(lambda a, b, c: (-b, a, c * c), (x, y, 9 - x * x - y * y)), (2 * x, 2 * y, 1))), 0, 2 * pi, lambda t: 0, lambda t: 3)
close(v, 18 * pi, 1e-5, "paraboloid curl flux directly")
close(line(lambda x, y, z: (-y, x, z * z), lambda t: (3 * cos(t), 3 * sin(t), 0), lambda t: (-3 * sin(t), 3 * cos(t), 0), 0, 2 * pi), 18 * pi, 1e-9, "boundary circle 18 pi")
ans("paraboloid-stokes", 18 * pi, 0.0005)

# ---- boss ----
ans("b-iterated", dbl(lambda x, y: x * x * y, 0, 1, lambda x: 0, lambda x: 2), 0.0005)
v = tet(lambda x, y, z: 1, 2)
close(v, 4 / 3, 1e-9, "tetra s = 2"); ans("b-tetra", v, 0.0005)
v = dbl(lambda y, x: exp(x * x), 0, 2, lambda y: y / 2, lambda y: 1, 400)
close(v, e - 1, 1e-8, "b-order directly"); close(dbl(lambda x, y: exp(x * x), 0, 1, lambda x: 0, lambda x: 2 * x), e - 1, 1e-9, "b-order swapped")
ans("b-order", v, 0.0005)
v = pol(lambda x, y: sqrt(x * x + y * y), 0, 2 * pi, lambda t: 1, lambda t: 2)
close(v, 14 * pi / 3, 1e-9, "14 pi/3"); ans("b-polar", v, 0.0005)
ok(abs(jac(1, 2, 3, -1)) == 7 and abs(1 * (-1) + 2 * 3) == 5 and 2 * 3 == 6, "b-jacobian 7 and the distractors 5, 6")
v = line(lambda x, y: (y, 2 * x), lambda t: (t, t * t), lambda t: (1, 2 * t), 0, 1)
close(v, 5 / 3, 1e-9, "5/3"); ans("b-line", v, 0.0005)
ans("b-plane-flux", 5 * 1 * 3)
v = div(lambda x, y, z: (x * x * y, y * z, x * z * z), (1, 1, 1))
close(v, 5, 1e-6, "b-div"); ans("b-div", round(v, 9))
fb = lambda x, y: y * sin(x) + y * y
v = line(lambda x, y: (y * cos(x), sin(x) + 2 * y), lambda t: (pi / 2 * t, t ** 2), lambda t: (pi / 2, 2 * t), 0, 1)
close(v, 2, 1e-9, "b-potential along a curve"); ans("b-potential", fb(pi / 2, 1) - fb(0, 0))
Fg = lambda x, y: (2 * y + x, 5 * x - y)
v = (line(Fg, lambda t: (2 * t, 0), lambda t: (2, 0), 0, 1) + line(Fg, lambda t: (2 - 2 * t, 2 * t), lambda t: (-2, 2), 0, 1)
     + line(Fg, lambda t: (0, 2 - 2 * t), lambda t: (0, -2), 0, 1))
close(v, 6, 1e-9, "b-green directly"); ans("b-green", 3 * 2)
v = 3 * pi * 3
side = dbl(lambda th, z: 1.0, 0, 2 * pi, lambda th: 0, lambda th: 3)   # F·n = x^2 + y^2 = 1 on the side
top = pi * 3                                                            # F·n = z = 3 on the top disk of area pi
close(side + top + 0.0, v, 1e-9, "b-gauss directly (bottom contributes 0)")
ans("b-gauss", v, 0.0005)

# ---- compare with the pack ----
pack = Path(__file__).resolve().parents[2] / "data" / "content" / "M.1.4.4.yaml"
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

print(f"M.1.4.4 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
