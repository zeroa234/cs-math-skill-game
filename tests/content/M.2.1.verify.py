"""M.2.1 常微分方程 — every number in data/content/M.2.1.yaml, recomputed.

Run: python -I tests/content/M.2.1.verify.py
Plain Python (no sympy on this machine). Closed-form solutions used in the pack are checked twice: the
formula is evaluated, and the initial value problem is integrated independently with a small-step RK4.
Fourier coefficients and Laplace transforms are recomputed by Simpson's rule, eigenvalues from the 2x2
characteristic polynomial and checked by multiplying back, matrix exponentials against the power series.
Number answers are read back from the YAML and compared with the values computed here.
"""
import cmath
import math
import re
from math import atan, cos, degrees, e, exp, log, pi, sin, sqrt, tan
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


def rk4(f, t0, y0, t1, n=20000):
    """Integrate y' = f(t, y) (y a list) from t0 to t1 with n RK4 steps."""
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


def simpson(g, a, b, n=20000):
    h = (b - a) / n
    s = g(a) + g(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * g(a + i * h)
    return s * h / 3


def eig2(a, b, c, d):
    T, D = a + d, a * d - b * c
    disc = cmath.sqrt(T * T - 4 * D)
    return (T + disc) / 2, (T - disc) / 2


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def expm_series(A, t, terms=60):
    R = [[1.0, 0.0], [0.0, 1.0]]
    P = [[1.0, 0.0], [0.0, 1.0]]
    for n in range(1, terms):
        P = matmul(P, [[A[i][j] * t / n for j in range(2)] for i in range(2)])
        R = [[R[i][j] + P[i][j] for j in range(2)] for i in range(2)]
    return R


# ==== 微分方程和分离变量 ====
# check-solution: sin 3t solves y'' + 9y = 0; the distractors do not
for t in (0.3, 1.1):
    close(-9 * sin(3 * t) + 9 * sin(3 * t), 0, what="sin 3t")
    ok(abs(-81 * sin(9 * t) + 9 * sin(9 * t)) > 1e-6, "sin 9t not a solution")
    ok(abs(9 * exp(3 * t) + 9 * exp(3 * t)) > 1e-6, "e^{3t} not a solution")
ans("ivp-constant", 8 * exp(-1), 0.0005)
close(rk4(lambda t, y: [-0.5 * y[0]], 0, [8], 2)[0], 8 * exp(-1), 1e-9, "ivp RK4")
k = log(2) / 10
close(k, 0.0693, 0.00005, "cooling k")
close(20 + 70 * exp(-20 * k), 37.5, what="cooling T(20)")
close(rk4(lambda t, y: [-k * (y[0] - 20)], 0, [90], 20)[0], 37.5, 1e-8, "cooling RK4")
ans("cooling-30", 20 + 60 * 0.5**3)
ans("separable-ivp", 1 / (1 - 0.25), 0.0005)
close(rk4(lambda x, y: [2 * x * y[0] ** 2], 0, [1], 0.5)[0], 4 / 3, 1e-9, "separable RK4")

# ==== 一阶线性方程和积分因子 ====
ex = lambda x: exp(-x) + exp(-2 * x)  # comprehensive exercise (1)
close(rk4(lambda x, y: [exp(-x) - 2 * y[0]], 0, [2], 1)[0], ex(1), 1e-9, "IF example RK4")
for x in (0.5, 2.0):  # (x^3 y)' = x^4 means x^3 y' + 3x^2 y = x^4, i.e. y' + 3y/x = x
    close(3 * x**2, x**3 * 3 / x, what="x^3 integrating factor")
ans("linear-ivp", 2 * (1 - exp(-1)), 0.0005)
close(rk4(lambda x, y: [2 - y[0]], 0, [0], 1)[0], 2 * (1 - exp(-1)), 1e-9, "linear RK4")
ans("rc-charge", 10 * (1 - exp(-1)), 0.005)

# ==== 复指数、正弦函数和指数输入 ====
ans("complex-modulus", abs(1 / (1 + 1j)), 0.0005)
close(degrees(cmath.phase(1 / (1 + 1j))), -45, what="arg 1/(1+i)")
ans("amplitude-combine", sqrt(3**2 + 4**2))
close(degrees(atan(4 / 3)), 53.1, 0.05, "phi 53.1")
for t in (0.2, 1.7):
    A, ph = 5, atan(4 / 3)
    close(3 * cos(2 * t) + 4 * sin(2 * t), A * cos(2 * t - ph), 1e-12, "a cos + b sin")
g = abs(2 / (2 + 2j))
ans("first-order-gain", g, 0.0005)
close(g, 1 / sqrt(1 + (2 / 2) ** 2), what="gain formula")
ans("phase-lag", degrees(atan(sqrt(3) / 1)), 1e-9)
# check the steady state directly: y_p = g cos(wt - phi) solves y' + ky = k cos wt
kk, w = 2.0, 2.0
G, P = 1 / sqrt(1 + (w / kk) ** 2), atan(w / kk)
for t in (0.4, 2.2):
    yp = G * cos(w * t - P)
    dyp = -G * w * sin(w * t - P)
    close(dyp + kk * yp, kk * cos(w * t), 1e-12, "first-order steady state")
ans("exp-input", 1 / (2 + 3))

# ==== 二阶常系数方程 ====
r = eig2(0, 1, -6, -5)  # r^2 + 5r + 6
ok(sorted([round(r[0].real, 9), round(r[1].real, 9)]) == [-3, -2], "y''+5y'+6y roots")
close((-4 + cmath.sqrt(16 - 52)) / 2, complex(-2, 3), what="r^2+4r+13")
ok(4**2 - 4 * 4 == 0, "critical damping discriminant")
ans("damped-freq", ((-2 + cmath.sqrt(4 - 104)) / 2).imag)
for t in (0.3, 1.2):  # Wronskian of e^{-2t}, t e^{-2t}
    y1, y1p = exp(-2 * t), -2 * exp(-2 * t)
    y2, y2p = t * exp(-2 * t), exp(-2 * t) - 2 * t * exp(-2 * t)
    close(y1 * y2p - y1p * y2, exp(-4 * t), 1e-12, "Wronskian")
for root in (0, 1, -1):
    close(root**3 - root, 0, what="r^3 - r roots")

# ==== 受迫响应 ====
p = lambda r: r * r + 3 * r + 2
close(p(-3), 2, what="ERF example p(-3)")
ans("erf-coefficient", 3 / (1 + 2 + 5))
p2 = lambda r: r * r + r + 4
close(p2(2j), 2j, what="p(2i)")
for t in (0.3, 1.9):  # y_p = 0.5 sin 2t
    close(-2 * sin(2 * t) + cos(2 * t) + 4 * 0.5 * sin(2 * t), cos(2 * t), 1e-12, "example check")
pi1 = (1j) ** 2 + 2j + 5
ans("gain-second-order", 1 / abs(pi1), 0.0005)
ans("phase-second-order", degrees(cmath.phase(pi1)), 0.05)
close(abs(pi1), 4.472, 0.0005, "|p(i)|")
for t in (0.5, 3.0):  # t^2 - 2 solves y'' + y = t^2
    close(2 + t * t - 2, t * t, what="undetermined example")
a_ = 4 / 2
b_ = -3 * a_ / 2
ans("undetermined", b_)
for t in (0.0, 1.3):
    close(0 + 3 * a_ + 2 * (a_ * t + b_), 4 * t, 1e-12, "2t - 3 check")
ans("superposition", 8 / 4 + 5 / (1 + 4))

# ==== 共振和 LRC 电路 ====
# pure resonance: x_p = t sin(3t)/6 solves x'' + 9x = cos 3t
for t in (0.7, 2.4):
    h = 1e-4
    xp = lambda s: s * sin(3 * s) / 6
    d2 = (xp(t + h) - 2 * xp(t) + xp(t - h)) / h**2
    close(d2 + 9 * xp(t), cos(3 * t), 1e-5, "pure resonance check")
ans("pure-resonance", 12 / 6)
ans("near-resonance", 1 / (4 - 1.9**2), 0.0005)
close(1 / (4 - 1), 1 / 3, what="omega = 1")
gain = lambda k_, b, w_: 1 / sqrt((k_ - w_ * w_) ** 2 + (b * w_) ** 2)
wr = sqrt(4 - 0.5)
close(wr, 1.871, 0.0005, "example wr")
close((4 - wr**2) ** 2 + wr**2, 3.75, 1e-12, "example 3.75")
close(gain(4, 1, wr), 0.516, 0.0005, "example peak gain")
ok(gain(4, 1, wr) > 2 * gain(4, 1, 0), "peak more than twice g(0)")
ws = [i / 10000 for i in range(1, 40000)]
close(max(ws, key=lambda w_: gain(4, 1, w_)), wr, 1e-4, "numeric peak location")
ans("practical-resonance", sqrt(10 - 2), 0.0005)
close(sqrt(10), 3.162, 0.0005, "sqrt 10")
# no-peak: b^2 >= 2k for x''+3x'+4x only; gain decreasing there
ok(9 >= 8 and 4 < 8 and 0.25 < 8, "no-peak condition")
ok(all(gain(4, 3, w_) > gain(4, 3, w_ + 0.01) for w_ in [i / 100 for i in range(0, 500)]), "monotone gain")
close(1 / sqrt(0.1 * 10e-6), 1000, 1e-9, "LRC example w0")
close(1000 / (2 * pi), 159, 0.5, "LRC example f0")
close(4 * 0.1 / 10e-6, 40000, 1e-9, "4L/C")
ans("lrc-freq", 1 / sqrt(0.2 * 50e-6) / (2 * pi), 0.05)
close(1 / sqrt(0.2 * 50e-6), 316.2, 0.05, "w0 316.2")
ans("lrc-critical", sqrt(4 * 0.2 / 50e-6), 0.05)

# ==== 傅里叶级数 ====
sq = lambda t: 1.0 if (t % (2 * pi)) < pi else -1.0
bn = lambda f, n: simpson(lambda t: f(t) * sin(n * t), -pi, pi, 40000) / pi
an = lambda f, n: simpson(lambda t: f(t) * cos(n * t), -pi, pi, 40000) / pi
ans("fourier-average", an(abs, 0) / 2, 0.0005)
close(an(abs, 0) / 2, pi / 2, 1e-6, "average |t|")
for n in range(1, 8):
    close(bn(sq, n), 4 / (n * pi) if n % 2 else 0.0, 1e-3, f"square b_{n}")
    close(an(sq, n), 0.0, 1e-3, f"square a_{n}")
ans("square-b5", 4 / (5 * pi), 0.0005)
for n in range(1, 4):  # t^2 is even: b_n = 0
    close(bn(lambda t: t * t, n), 0.0, 1e-6, "t^2 b_n")
close(an(lambda t: t * t, 0) / 2, pi**2 / 3, 1e-6, "t^2 average")
ans("jump-value", (1 + 3) / 2)
close(sum(1 / n**2 for n in range(1, 2000001, 2)), pi**2 / 8, 1e-6, "sum over odd n of 1/n^2")
# triangle wave from integrating the square wave
for t in (0.4, 2.0, -1.3):
    s = pi / 2 - 4 / pi * sum(cos(n * t) / n**2 for n in range(1, 4001, 2))
    close(s, abs(t), 1e-3, "triangle series")
ans("shift-scale", 0.5 * 4 / pi, 0.0005)
close(bn(lambda t: (1 + sq(t)) / 2, 1), 2 / pi, 1e-3, "0/1 square wave b1")
ans("periodic-response", (4 / (3 * pi)) / (10 - 9), 0.0005)
close((4 / pi) / 9, 0.141, 0.0005, "sin t term")
ok(abs(3**2 - 9) == 0, "w0 = 3 resonates")

# ==== 阶跃、冲激和卷积 ====
step = lambda t: 1.0 if t > 0 else 0.0
ans("window", simpson(lambda t: 3 * (step(t - 1) - step(t - 4)), 0, 10, 100000), 0.01)
ans("sifting", 2**3)
# a narrow box of area 1 around t = 2 reproduces the sifting value
hbox = 1e-4
close(simpson(lambda t: t**3 / hbox, 2 - hbox / 2, 2 + hbox / 2, 200), 8, 1e-6, "box approximation")
# impulse response of x'' + 4x: x(0)=0, x'(0)=1 gives sin(2t)/2
close(rk4(lambda t, y: [y[1], -4 * y[0]], 0, [0, 1], 1.0)[0], sin(2) / 2, 1e-9, "w for x''+4x")
ans("impulse-first", exp(-0.5 * 2), 0.0005)
# a narrow box input of area 1 on [0, h] gives x(h) close to 1 for x' + 0.5x (the jump), then e^{-0.5t}
hb = 1e-4
xh = rk4(lambda t, y: [1 / hb - 0.5 * y[0]], 0, [0], hb, 1000)[0]
close(xh, 1, 1e-3, "first-order impulse jump")
close(rk4(lambda t, y: [-0.5 * y[0]], hb, [xh], 2, 20000)[0], exp(-1), 1e-3, "impulse-first via box")
w2 = rk4(lambda t, y: [y[1], -9 * y[0]], 0, [0, 1], pi / 6)[0]
ans("impulse-second", w2, 0.0005)
close(w2, 1 / 3, 1e-9, "w = sin(3t)/3")
ans("step-first", 0.5 * (1 - exp(-2)), 0.0005)
close(rk4(lambda t, y: [1 - 2 * y[0]], 0, [0], 1)[0], 0.5 * (1 - exp(-2)), 1e-9, "step RK4")
conv = simpson(lambda tau: 1 * exp(-2 * (1.3 - tau)), 0, 1.3, 2000)
close(conv, 0.5 * (1 - exp(-2.6)), 1e-9, "convolution example at t=1.3")
cv = simpson(lambda tau: tau * exp(-(2 - tau)), 0, 2, 2000)
ans("convolution", cv, 0.0005)
close(cv, 1 + exp(-2), 1e-9, "convolution closed form")
close(rk4(lambda t, y: [t - y[0]], 0, [0], 2)[0], 1 + exp(-2), 1e-9, "convolution RK4")


# ==== 拉普拉斯变换 ====
def lap(f, s, T=60.0, n=60000):
    return simpson(lambda t: exp(-s * t) * f(t), 0, T, n)


ans("laplace-exp", lap(lambda t: exp(-3 * t), 1), 1e-6)
close(lap(lambda t: exp(-3 * t), 1), 0.25, 1e-6, "L{e^-3t}(1)")
for s in (1.5, 3.0):
    close(lap(lambda t: sin(3 * t), s), 3 / (s * s + 9), 1e-6, "L sin 3t")
    close(lap(lambda t: cos(3 * t), s), s / (s * s + 9), 1e-6, "L cos 3t")
    close(lap(lambda t: t * t, s), 2 / s**3, 1e-6, "L t^2")
    close(lap(lambda t: exp(2 * t), s + 2), 1 / s, 1e-6, "L e^2t")
lshift = lap(lambda t: exp(-t) * cos(2 * t), 0)
ans("laplace-shift", lshift, 1e-6)
close(lshift, 0.2, 1e-6, "shift rule")
# derivative rule on f = sin t: L{f'} = s F - f(0)
s = 2.0
close(lap(lambda t: cos(t), s), s * lap(lambda t: sin(t), s) - 0, 1e-6, "L{f'}")
# cover-up examples
close((1 + 5) / (1 + 2), 2, what="cover-up A")
close((-2 + 5) / (-2 - 1), -1, what="cover-up B")
for x in (0.3, 4.0):
    close((x + 5) / ((x - 1) * (x + 2)), 2 / (x - 1) - 1 / (x + 2), 1e-12, "partial fraction identity")
B = (3 * -2 + 1) / (-2 - 1)
ans("partial-fraction", B, 0.0005)
close((3 * 1 + 1) / (1 + 2), 4 / 3, what="A = 4/3")
for x in (0.5, 3.0):
    close((3 * x + 1) / ((x - 1) * (x + 2)), (4 / 3) / (x - 1) + B / (x + 2), 1e-12, "pf 3s+1")
yex = lambda t: 2 * exp(-t) - exp(-2 * t)
close(rk4(lambda t, y: [y[1], -3 * y[1] - 2 * y[0]], 0, [1, 0], 1)[0], yex(1), 1e-9, "Laplace IVP example")
ans("laplace-ivp", exp(-1) - exp(-2), 0.0005)
close(rk4(lambda t, y: [exp(-t) - 2 * y[0]], 0, [0], 1)[0], exp(-1) - exp(-2), 1e-9, "laplace-ivp RK4")

# ==== 传递函数和极点 ====
close(1 / (-2 + 4), 0.5, what="cover-up 1/2")
we = rk4(lambda t, y: [y[1], -6 * y[1] - 8 * y[0]], 0, [0, 1], 0.5)[0]
close(we, 0.5 * (exp(-1) - exp(-2)), 1e-9, "transfer example w(0.5)")
close(we, 0.116, 0.0005, "transfer example 0.116")
ans("transfer-impulse", 0.5 * (exp(-1) - exp(-3)), 0.0005)
close(rk4(lambda t, y: [y[1], -4 * y[1] - 3 * y[0]], 0, [0, 1], 1)[0], 0.5 * (exp(-1) - exp(-3)), 1e-9, "w RK4")
s = 1.7  # L{1 * e^{-2t}} = 1/(s(s+2))
close(lap(lambda t: (1 - exp(-2 * t)) / 2, s), 1 / (s * (s + 2)), 1e-6, "convolution theorem")
for den, stable in (((1, 2, 5), True), ((1, -2, 5), False), ((1, 0, 4), False), ((1, 1, -2), False)):
    roots = eig2(0, 1, -den[2], -den[1])
    ok((max(r_.real for r_ in roots) < 0) == stable, f"pole stability {den}")
ans("pole-from-ode", abs(((-4 + cmath.sqrt(16 - 80)) / 2).imag))
ans("amplitude-response", abs(1 / ((1j) ** 2 + 0.2j + 1)))
close(eig2(0, 1, -1, -0.2)[0].imag, 0.995, 0.0005, "poles -0.1 +- 0.995i")

# ==== 一阶线性方程组和特征值法 ====
lam = eig2(-2, 1, 1, -2)
ok(sorted([round(l.real, 9) for l in lam]) == [-3, -1], "tank eigenvalues")
for (v, l) in (((1, 1), -1), ((1, -1), -3)):
    close(-2 * v[0] + 1 * v[1], l * v[0], what="tank eigvec row1")
    close(1 * v[0] - 2 * v[1], l * v[1], what="tank eigvec row2")
sol = rk4(lambda t, y: [-2 * y[0] + y[1], y[0] - 2 * y[1]], 0, [2, 0], 1)
close(sol[0], exp(-1) + exp(-3), 1e-9, "tank example x(1)")
close(sol[1], exp(-1) - exp(-3), 1e-9, "tank example y(1)")
ans("eigenvalue", max(l.real for l in eig2(4, 1, 2, 3)))
close(4 * 1 + 1 * -2, 2 * 1, what="eigvec (1,-2) row1")
close(2 * 1 + 3 * -2, 2 * -2, what="eigvec (1,-2) row2")
sol = rk4(lambda t, y: [-2 * y[0] + y[1], y[0] - 2 * y[1]], 0, [0, 2], 1)
ans("system-ivp", sol[0], 0.0005)
close(sol[0], exp(-1) - exp(-3), 1e-9, "system-ivp closed form")
# complex example A = [[0,1],[-1,0]]: (cos t, -sin t) solves it
for t in (0.4, 2.0):
    close(-sin(t), -sin(t), what="x' = y")
    close(-cos(t), -cos(t), what="y' = -x")
ans("complex-eigen", abs(eig2(-1, -2, 2, -1)[0].imag))

# ==== 相图和矩阵指数 ====
lam = eig2(-1, -4, 1, -1)
close(lam[0], complex(-1, 2), what="spiral example eigenvalues")
ok(-1 * 1 + -4 * 0 == -1 and 1 * 1 + -1 * 0 == 1, "velocity at (1,0) is (-1, 1)")
ok(1 * 1 - 3 * 3 < 0, "saddle det")
ok(sorted([round(l.real, 9) for l in eig2(1, 3, 3, 1)]) == [-2, 4], "saddle eigenvalues 4, -2")
ok(eig2(0, 2, -2, 0)[0] == 2j or abs(eig2(0, 2, -2, 0)[0] - 2j) < 1e-12, "center +-2i")
E = expm_series([[0, 1], [0, 0]], 3)
ans("matexp-nilpotent", E[0][0] * 1 + E[0][1] * 2)
E = expm_series([[-1, 0], [0, 2]], 1)
ans("matexp-diag", E[0][0] * 3 + E[0][1] * 1, 0.0005)
E = expm_series([[1, 1], [0, 2]], 1)
ans("fundamental", E[0][1], 0.0005)
close(E[0][1], e**2 - e, 1e-9, "Phi Phi(0)^-1 entry")

# ==== 存在唯一性 ====
for x in (0.5, 1.3):  # y = x^3 solves y' = 3 y^(2/3)
    close(3 * x * x, 3 * (x**3) ** (2 / 3), 1e-12, "x^3 second solution")
    close(x / 2, sqrt(x * x / 4), 1e-12, "x^2/4 solves y' = sqrt y")
ans("lipschitz-rect", max(abs(2 * y) for y in [i / 1000 for i in range(-2000, 2001)]))
ans("lipschitz-sin", max(abs(3 * cos(3 * y)) for y in [i / 1000 for i in range(-3000, 3001)]))
# Picard iterates of y' = x + y and y' = 1 + y^2 by repeated numerical integration
def picard(f, n, xs):
    ys = [0.0] * len(xs)
    for _ in range(n):
        new = [0.0]
        for i in range(1, len(xs)):
            h = xs[i] - xs[i - 1]
            new.append(new[-1] + h / 2 * (f(xs[i - 1], ys[i - 1]) + f(xs[i], ys[i])))
        ys = new
    return ys


xs = [i / 20000 for i in range(20001)]
y2 = picard(lambda x, y: x + y, 2, xs)
close(y2[-1], 0.5 + 1 / 6, 1e-6, "Picard y2 for x + y")
y2 = picard(lambda x, y: 1 + y * y, 2, xs)
ans("picard-iterate", y2[-1], 0.0005)
close(y2[-1], 1 + 1 / 3, 1e-6, "Picard y2 closed form")
close(tan(1), 1.557, 0.0005, "tan 1")

# ==== 解能走多远 ====
ans("blowup", 1 / 4)
close(rk4(lambda x, y: [y[0] ** 2], 0, [4], 0.2)[0], 1 / (0.25 - 0.2), 1e-6, "blowup RK4 near 0.25")
close(rk4(lambda x, y: [y[0] ** 2], 0, [2], 0.4)[0], 2 / (1 - 0.8), 1e-6, "y(0)=2 example")
ans("blowup-tan", pi / 4, 0.0005)
close(rk4(lambda x, y: [1 + y[0] ** 2], 0, [1], 0.7)[0], tan(0.7 + pi / 4), 1e-6, "tan(x + pi/4)")
ans("negative-initial", -1 / (1 + 1))
close(rk4(lambda x, y: [y[0] ** 2], 0, [-1], 1)[0], -0.5, 1e-9, "negative initial RK4")

# ==== 方向场、自治方程 ====
ans("isocline", sqrt(4))
for x in (-2.0, 0.5, 3.0):
    close((x + 1) - x, 1, what="y = x + 1 is a solution of y' = y - x")
# logistic example: equilibria and max growth at 50
f = lambda y: 0.5 * y * (1 - y / 100)
close(max([i / 10 for i in range(0, 1001)], key=f), 50, what="logistic max growth")
ok(f(50) > 0 and f(150) < 0 and f(-5) < 0, "logistic phase line")
ok(2 * 2 > 0 and 2 * -2 < 0, "y^2 - 4 stability")
ans("logistic-limit", 50)
close(rk4(lambda t, y: [0.3 * y[0] * (1 - y[0] / 50)], 0, [80], 100)[0], 50, 1e-6, "logistic RK4")
roots = sorted([(4 - sqrt(16 - 12)) / 2, (4 + sqrt(16 - 12)) / 2])
close(roots[0], 1, what="harvest root 1")
ok(4 - 2 * roots[1] < 0 < 4 - 2 * roots[0], "harvest stability")
ans("harvest", roots[1])
close(rk4(lambda t, y: [y[0] * (4 - y[0]) - 3], 0, [2], 50)[0], 3, 1e-6, "harvest RK4")


# ==== 数值解 ====
def euler(f, x0, y0, h, n):
    x, y = x0, y0
    for _ in range(n):
        y += h * f(x, y)
        x += h
    return y


def heun(f, x0, y0, h, n):
    x, y = x0, y0
    for _ in range(n):
        k1 = f(x, y)
        k2 = f(x + h, y + h * k1)
        y += h / 2 * (k1 + k2)
        x += h
    return y


close(euler(lambda x, y: y, 0, 1, 0.5, 2), 2.25, what="Euler example")
close(e - 2.25, 0.468, 0.0005, "Euler error 0.468")
close(euler(lambda x, y: y, 0, 1, 0.25, 4), 2.441, 0.0005, "Euler h=0.25")
close(e - 1.25**4, 0.277, 0.0005, "error 0.277")
close((e - 2.25) / (e - 1.25**4), 1.7, 0.05, "ratio 1.7")
r1 = (e - 1.25**4) / (e - 1.125**8)
r2 = (e - 1.125**8) / (e - (1 + 1 / 16) ** 16)
ok(1.7 < r1 < r2 < 2, "ratio tends to 2")
ans("euler-two-steps", euler(lambda x, y: x + y, 0, 1, 0.1, 2), 0.0005)
close(2 * exp(0.2) - 1.2, 1.243, 0.0005, "exact y(0.2)")
close(heun(lambda x, y: x + y, 0, 1, 0.1, 1), 1.11, 1e-12, "Heun example")
close(2 * exp(0.1) - 1.1, 1.1103, 0.00005, "exact y(0.1)")
hv = heun(lambda x, y: y, 0, 1, 0.5, 2)
ans("heun-two-steps", hv, 0.0005)
close(hv, 1.625**2, 1e-12, "Heun factor")
close(e - hv, 0.078, 0.0005, "Heun error")
# empirical orders: Euler ~1, Heun ~2, RK4 ~4 on y' = y
err = lambda m, h: abs(e - m(h))
eu = lambda h: euler(lambda x, y: y, 0, 1, h, round(1 / h))
he = lambda h: heun(lambda x, y: y, 0, 1, h, round(1 / h))
rkk = lambda h: rk4(lambda t, y: [y[0]], 0, [1], 1, round(1 / h))[0]
k1 = 1.0
k2 = 1 + 0.25 * k1
k3 = 1 + 0.25 * k2
k4 = 1 + 0.5 * k3
ok((k2, k3, k4) == (1.25, 1.3125, 1.65625), "RK4 example slopes")
y_rk = 1 + 0.5 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
ans("rk4-step", y_rk, 0.0005)
close(y_rk, rk4(lambda t, y: [y[0]], 0, [1], 0.5, 1)[0], 1e-12, "RK4 one step matches rk4()")
close(exp(0.5), 1.6487, 0.00005, "e^0.5")
close(err(eu, 0.001) / err(eu, 0.0005), 2, 0.01, "Euler order 1")
close(err(he, 0.01) / err(he, 0.005), 4, 0.05, "Heun order 2")
close(err(rkk, 0.1) / err(rkk, 0.05), 16, 1.0, "RK4 order 4")
close(0.04 / 2, 0.02, what="error-scaling")
close(3.2e-6 / 16, 2e-7, 1e-15, "rk4-scaling")
close(1 - 10 * 0.05, 0.5, what="stable factor")
close(1 - 10 * 0.25, -1.5, what="unstable factor")
ok(abs(euler(lambda x, y: -10 * y, 0, 1, 0.25, 20)) > 1e3, "Euler blows up at h = 0.25")
ans("euler-unstable", 2 / 20)

# ==== 非线性方程组 ====
eq = [x for x in (-1.0, 0.0, 1.0) if abs(x - x**3) < 1e-12]
ans("count-equilibria", len(eq))
# pendulum Jacobians
T, D = -0.5, 0 * -0.5 - 1 * (-cos(0))
ok(D > 0 and T * T < 4 * D and T < 0, "pendulum (0,0) stable spiral")
ok(0 * -0.5 - 1 * (-cos(pi)) < 0, "pendulum (pi,0) saddle")
J = [[0, 1], [1 - 3 * 1**2, -1]]
T, D = J[0][0] + J[1][1], J[0][0] * J[1][1] - J[0][1] * J[1][0]
ok(T == -1 and D == 2 and T * T < 4 * D, "(1,0) stable spiral")
x0, y0 = 1, 2
ok(x0 * (3 - x0 - y0) == 0 and y0 * (x0 - 1) == 0, "(1,2) is an equilibrium")
J = [[3 - 2 * x0 - y0, -x0], [y0, x0 - 1]]
ans("jacobian-det", J[0][0] * J[1][1] - J[0][1] * J[1][0])
ok(J[0][0] + J[1][1] == -1, "(1,2) trace -1")


# van der Pol mu = 1: both starts approach the same amplitude, about 2
def vdp_amp(x0):
    y = rk4(lambda t, y: [y[1], (1 - y[0] ** 2) * y[1] - y[0]], 0, [x0, 0], 60, 30000)
    amp, h = 0.0, 0.002
    t = 0.0
    for _ in range(10000):  # 20 more time units, record max |x|
        y = rk4(lambda t, y: [y[1], (1 - y[0] ** 2) * y[1] - y[0]], 0, y, h, 1)
        amp = max(amp, abs(y[0]))
    return amp


a1, a2 = vdp_amp(0.1), vdp_amp(5.0)
close(a1, a2, 0.01, "vdP same amplitude")
close(a1, 2.0, 0.02, "vdP amplitude ~2")


# Lorenz: two starts 1e-8 apart separate to order 1 or more by t = 40
def lorenz(t, v):
    x, y, z = v
    return [10 * (y - x), x * (28 - z) - y, x * y - 8 / 3 * z]


u1 = rk4(lorenz, 0, [1, 1, 1], 40, 40000)
u2 = rk4(lorenz, 0, [1 + 1e-8, 1, 1], 40, 40000)
ok(math.dist(u1, u2) > 1, "Lorenz sensitive dependence")

# ==== 结业挑战 ====
ans("b-linear-ode", 2 * (1 - exp(-1.5)), 0.0005)
close(rk4(lambda x, y: [6 - 3 * y[0]], 0, [0], 0.5)[0], 2 * (1 - exp(-1.5)), 1e-9, "b-linear RK4")
yb = rk4(lambda t, y: [y[1], -6 * y[1] - 25 * y[0]], 0, [0, 4], pi / 8)[0]
ans("b-damped", yb, 0.0005)
close(yb, exp(-3 * pi / 8), 1e-9, "b-damped closed form")
ans("b-gain", 1 / abs((1j) ** 2 + 1j + 4), 0.0005)
ans("b-resonance", sqrt(9 - 2), 0.0005)
ans("b-fourier", 4 / (7 * pi), 0.0005)
close(bn(sq, 7), 4 / (7 * pi), 1e-3, "b7 Simpson")
xb = rk4(lambda t, y: [8 * step(t - 1) - 4 * y[0]], 0, [0], 1.5, 300000)[0]
ans("b-step-response", 2 * (1 - exp(-2)), 0.0005)
close(xb, 2 * (1 - exp(-2)), 1e-4, "b-step RK4")
ans("b-laplace-ivp", 2 * (exp(-2) - exp(-3)), 0.0005)
close(rk4(lambda t, y: [y[1], -5 * y[1] - 6 * y[0]], 0, [0, 2], 1)[0], 2 * (exp(-2) - exp(-3)), 1e-9, "b-laplace RK4")
roots = eig2(0, 1, -2, 1)  # s^2 - s + 2
ok(all(r_.real > 0 and r_.imag != 0 for r_ in roots), "b-poles right half plane, complex")
close(abs(roots[0].imag), sqrt(7) / 2, 1e-12, "b-poles imag sqrt7/2")
ok(sorted([round(l.real, 9) for l in eig2(0, 1, -2, -3)]) == [-2, -1], "b-node eigenvalues")
ok(9 - 8 > 0, "b-node real eigenvalues")
lam = eig2(1, 4, 1, 1)
ok(sorted([round(l.real, 9) for l in lam]) == [-1, 3], "b-eigen eigenvalues")
close(1 * 2 + 4 * 1, 3 * 2, what="(2,1) eigvec row1")
close(1 * 2 + 1 * 1, 3 * 1, what="(2,1) eigvec row2")
xe = rk4(lambda t, y: [y[0] + 4 * y[1], y[0] + y[1]], 0, [2, 1], 1)[0]
ans("b-eigen-ivp", xe, 0.005)
close(xe, 2 * exp(3), 1e-8, "b-eigen closed form")
for x in (0.5, 2.0):  # (2x/3)^(3/2) solves y' = y^(1/3)
    y_ = (2 * x / 3) ** 1.5
    close(sqrt(2 * x / 3), y_ ** (1 / 3), 1e-12, "b-picard second solution")
ans("b-blowup", pi / 2, 0.0005)
yb = euler(lambda x, y: exp(-x) - 2 * y, 0, 2, 0.1, 2)
ans("b-euler", yb, 0.001)
close(1.7 + 0.1 * (0.905 - 3.4), 1.4505, 1e-12, "b-euler with e^-0.1 rounded to 0.905")
ok(abs(1.4505 - 1.450) < 0.001 and abs(1.451 - 1.450) <= 0.001 + 1e-12, "b-euler tolerance covers rounding")
close(yb, 1.4505, 0.00005, "b-euler 1.4505")
close(exp(-0.2) + exp(-0.4), 1.489, 0.0005, "b-euler exact")
close(exp(-0.2) + exp(-0.4) - yb, 0.039, 0.0005, "b-euler error")
fa = lambda y: y * (3 - y) * (y - 1)
ok(fa(2) > 0, "b-autonomous direction")
close((fa(3 + 1e-6) - fa(3 - 1e-6)) / 2e-6, -6, 1e-5, "f'(3)")
ans("b-autonomous", rk4(lambda t, y: [fa(y[0])], 0, [2], 30)[0], 1e-6)
J = [[2 - 2 * 1 - 1, -1], [1, 1 - 1]]
T, D = J[0][0] + J[1][1], J[0][0] * J[1][1] - J[0][1] * J[1][0]
ok(T == -1 and D == 1 and T * T < 4 * D, "b-linearize stable spiral")

# ---- automation review 2026-11-23: worked examples added to solution-interval and numerical-methods ----
C0 = -1 / 2                      # y' = y^2, y(0) = 2: -1/y = x + C
close(-1 / 2.0, C0, 1e-12, "blow-up example C")
close(1 / (0.5 - 0), 2.0, 1e-12, "blow-up example y(0) = 2")
x_blow = 0.5
ok(abs(0.5 - x_blow) < 1e-12, "blow-up example: denominator 1/2 - x vanishes at 0.5")
f_rk = lambda y: -y              # RK4 example y' = -y, y(0) = 1, h = 1
h = 1.0
k1 = f_rk(1.0); k2 = f_rk(1.0 + h / 2 * k1); k3 = f_rk(1.0 + h / 2 * k2); k4 = f_rk(1.0 + h * k3)
close(k1, -1.0, 1e-12, "rk4 example k1"); close(1.0 + h / 2 * k1, 0.5, 1e-12, "rk4 example half step 1")
close(k2, -0.5, 1e-12, "rk4 example k2"); close(1.0 + h / 2 * k2, 0.75, 1e-12, "rk4 example half step 2")
close(k3, -0.75, 1e-12, "rk4 example k3"); close(1.0 + h * k3, 0.25, 1e-12, "rk4 example full step")
close(k4, -0.25, 1e-12, "rk4 example k4")
y1 = 1.0 + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
close(y1, 0.375, 1e-12, "rk4 example y1")
close(math.exp(-1), 0.368, 0.0005, "rk4 example exact e^-1")
close(y1 - math.exp(-1), 0.007, 0.0005, "rk4 example one-step error")
# check-solution: y = sin 3t + 3 leaves 9*3 = 27 in y'' + 9y
close(9 * 3, 27, 1e-12, "check-solution distractor constant")

# ---- compare with the pack ----
pack = Path(__file__).resolve().parents[2] / "data" / "content" / "M.2.1.yaml"
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

print(f"M.2.1 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
