"""H.4.1 控制理论与状态估计 — every number in data/content/H.4.1.yaml, recomputed.

Run: python -I tests/content/H.4.1.verify.py
Plain Python (no numpy here). Characteristic polynomials come from the Faddeev–LeVerrier recursion and
their roots from Durand–Kerner iteration; step responses, Lyapunov derivatives and LQR closed loops are
checked by RK4 simulation; frequency-domain numbers are evaluated with complex arithmetic and the
crossover frequencies are found by bisection. Number answers are read back from the YAML and compared.
"""
import cmath
import math
import re
from math import atan, degrees, exp, log10, pi, sqrt
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


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def charpoly(A):
    """Coefficients [1, c1, ..., cn] of det(sI - A) by Faddeev–LeVerrier."""
    n = len(A)
    M = [[0.0] * n for _ in range(n)]
    c = [1.0]
    I = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for k in range(1, n + 1):
        M = [[sum(A[i][m] * M[m][j] for m in range(n)) + c[-1] * I[i][j] for j in range(n)] for i in range(n)]
        AM = matmul(A, M)
        c.append(-sum(AM[i][i] for i in range(n)) / k)
    return c


def roots(coeffs):
    """All roots of a monic polynomial (Durand–Kerner)."""
    n = len(coeffs) - 1
    p = lambda z: sum(c * z ** (n - i) for i, c in enumerate(coeffs))
    zs = [(0.4 + 0.9j) ** k for k in range(n)]
    for _ in range(2000):
        new = []
        for i, z in enumerate(zs):
            den = 1
            for j, w in enumerate(zs):
                if i != j:
                    den *= z - w
            new.append(z - p(z) / den)
        zs = new
    return zs


def eig(A):
    return roots(charpoly(A))


def rk4(f, t0, y0, t1, n=20000):
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


def bisect(f, lo, hi, it=200):
    flo = f(lo)
    for _ in range(it):
        mid = (lo + hi) / 2
        if (f(mid) > 0) == (flo > 0):
            lo, flo = mid, f(mid)
        else:
            hi = mid
    return (lo + hi) / 2


def det2(M):
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]


Mp = lambda z: exp(-pi * z / sqrt(1 - z * z)) * 100

# ==== 闭环和灵敏度 ====
ans("closed-loop-gain", 9 / (1 + 9))
ans("disturbance", 1 / (1 + 49))
T1, T2 = 100 / 101, 80 / 81
close(T1, 0.99010, 0.000005, "T before")
close(T2, 0.98765, 0.000005, "T after")
close((T1 - T2) / T1 * 100, 0.25, 0.005, "0.25 %")
close(1 / 101 * 20, 0.2, 0.005, "S * 20 %")
ans("robustness", (120 / 121 - 100 / 101) / (100 / 101) * 100, 0.005)
ans("tracking-error", 1 / (1 + 19))
# dT/T = S dP/P checked by a small perturbation
P0, C0, dP = 10.0, 10.0, 1e-6
T = lambda P: P * C0 / (1 + P * C0)
close((T(P0 + dP) - T(P0)) / T(P0) / (dP / P0), 1 / (1 + P0 * C0), 1e-5, "dT/T = S dP/P")

# ==== 时域响应 ====
close(1 - exp(-1), 0.632, 0.0005, "63.2 %")
close(1 - exp(-4), 0.982, 0.0005, "98.2 %")
ans("first-order", 3 * (1 - exp(-2)), 0.0005)
close(rk4(lambda t, y: [(3 - y[0]) / 0.5], 0, [0], 1)[0], 3 * (1 - exp(-2)), 1e-9, "first-order RK4")
close(Mp(0.5), 16.3, 0.05, "zeta 0.5")
close(Mp(1 / sqrt(2)), 4.3, 0.05, "zeta 0.707")
ans("overshoot", Mp(0.6), 0.05)
# example: 4/(s^2+2s+4): simulate the step response, measure overshoot
y = [0.0, 0.0]
h, peak = 1e-4, 0.0
for _ in range(100000):
    y = rk4(lambda t, v: [v[1], 4 * (1 - v[0]) - 2 * v[1]], 0, y, h, 1)
    peak = max(peak, y[0])
close((peak - 1) * 100, Mp(0.5), 0.01, "simulated overshoot 16.3 %")
close(4 / (0.5 * 2), 4, what="example t_s")
ans("settling-time", 4 / 3, 0.005)
ans("step-error", 1 / (1 + 10 / 2), 0.0005)
ans("ramp-error", 1 / (20 / 4))

# ==== PID ====
ans("p-error", 1 / (1 + 4.5 * 2))
Ku, Tu = 10, 2
close(0.6 * Ku, 6, what="ZN Kp")
close(0.5 * Tu, 1, what="ZN Ti")
ans("ziegler-nichols", 0.125 * Tu)

# ==== 根轨迹 ====
close(roots([1, 2, 1])[0].real, -1, 1e-6, "K=1 double root at -1")
ans("breakaway", 16 / 4)
close(roots([1, 4, 4])[0].real, -2, 1e-6, "breakaway at -2")
ans("centroid", (0 - 1 - 5) / 3)
# real-axis rule for poles 0, -1, -3: test points
for x, on in ((-0.5, True), (-2, False), (-4, True), (0.5, False)):
    count = sum(1 for p in (0, -1, -3) if p > x)
    ok((count % 2 == 1) == on, f"real axis at {x}")

# ==== 劳斯判据 ====
close(6 * 5, 30, what="example K < 30")
r30 = roots([1, 6, 5, 30])
ok(any(abs(r - 1j * sqrt(5)) < 1e-6 for r in r30) and any(abs(r + 6) < 1e-6 for r in r30), "(s+6)(s^2+5)")
ans("k-max", 5 * 4)
for K, stable in ((19.9, True), (20.1, False)):
    ok((max(r.real for r in roots([1, 5, 4, K])) < 0) == stable, f"K = {K}")
rr = roots([1, 1, 2, 8])
ans("routh-count", sum(1 for r in rr if r.real > 0))
close((1 * 2 - 1 * 8) / 1, -6, what="Routh first column")
ok(sum(1 for r in roots([1, 0, 4 + 0j]) if abs(r.real) < 1e-9) == 2, "+-2i on the axis")

# ==== 李雅普诺夫 ====
f = lambda x1, x2: (-x1 + x2, -x1 - x2**3)
for x1, x2 in ((0.7, -0.3), (-1.2, 0.5)):
    d1, d2 = f(x1, x2)
    close(2 * x1 * d1 + 2 * x2 * d2, -2 * x1**2 - 2 * x2**4, 1e-12, "example Vdot")
ans("v-dot", 2 * 1 * (-2 * 1) + 2 * 1 * (-1 * 1))
ans("lyap-scalar", -6 / (2 * -3))
ans("lyap-diag", -1 / (2 * -1))
close(-1 / (2 * -2), 0.25, what="p22")
A = [[-1, 0], [0, -2]]
P = [[0.5, 0], [0, 0.25]]
At = [[A[j][i] for j in range(2)] for i in range(2)]
L = [[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(matmul(At, P), matmul(P, A))]
ok(L == [[-1.0, 0.0], [0.0, -1.0]], "A'P + PA = -I")

# ==== 波特图 ====
ans("block-series", 2 / 1 * 5 / 10)
G = lambda w: 100 / ((1 + 1j * w) * (1 + 1j * w / 10))
close(abs(G(10)), 7.04, 0.005, "|G(10i)|")
close(20 * log10(abs(G(10))), 16.9, 0.05, "16.9 dB")
ans("bode-asymptote", 20 - 20 * log10(100 / 2), 0.05)
close(20 * log10(10 / sqrt(1 + (100 / 2) ** 2)), -14.0, 0.05, "actual -14 dB")
ans("corner-phase", degrees(cmath.phase(1 / (1 + 1j * 5 / 5))))

# ==== 奈奎斯特和裕度 ====
ans("nyquist-count", -1 + 1)


def pm(L):
    wgc = bisect(lambda w: abs(L(w)) - 1, 1e-4, 100)
    return wgc, 180 + degrees(cmath.phase(L(wgc)))


wgc, m = pm(lambda w: 2 / (1j * w * (1j * w + 1)))
close(wgc, 1.250, 0.0005, "example wgc")
close(wgc**2, (-1 + sqrt(17)) / 2, 1e-9, "wgc^2")
close(m, 38.7, 0.05, "example PM")
wgc, m = pm(lambda w: 4 / (1j * w * (1j * w + 2)))
close(wgc, 1.572, 0.0005, "item wgc")
ans("phase-margin", m, 0.05)
Lg = lambda w: 4 / (1j * w + 1) ** 3
close(abs(cmath.phase(Lg(sqrt(3)))), pi, 1e-9, "phase crossover at sqrt 3")
ans("gain-margin", 1 / abs(Lg(sqrt(3))))
ok(max(r.real for r in roots([1, 3, 3, 1 + 7.99])) < 0 < max(r.real for r in roots([1, 3, 3, 1 + 8.01])), "K = 8 is critical")
ans("delay-margin", degrees(2 * 0.1), 0.05)
ok(abs(abs(1 - 2j) - abs(1 + 2j)) < 1e-12, "1 - s and 1 + s same gain")

# ==== 状态空间 ====
ans("msd-matrix", -8 / 2)
close(-4 / 2, -2, what="A22 = -2")
ans("companion", -2)
ans("steady-state", 3 * (1 / 2))
close(rk4(lambda t, y: [-2 * y[0] + 1], 0, [0], 20)[0] * 3, 1.5, 1e-9, "steady state RK4")
close(sorted(r.real for r in eig([[0, 1], [-2, -3]]))[0], -2, 1e-6, "example poles -2")
ans("tf-dc-gain", 1 / 6, 0.0005)
ok(sorted(round(r.real, 6) for r in eig([[0, 1], [-6, -5]])) == [-3, -2], "tf poles")
ok(sorted(round(r.real, 6) for r in eig([[-1, 2], [0, -4]])) == [-4, -1], "triangular eigenvalues")

# ==== 状态反馈 ====
Kd = [8, 4]
c = charpoly([[0, 1], [-Kd[0], -Kd[1]]])
ok(c == [1.0, 4.0, 8.0], "double integrator s^2 + 4s + 8")
ok(all(abs(r.real + 2) < 1e-6 and abs(abs(r.imag) - 2) < 1e-6 for r in roots(c)), "poles -2 +- 2i")
k1, k2 = 20 - 2, 9 - 3
ans("place-k1", k1)
ok(sorted(round(r.real, 6) for r in eig([[0, 1], [-2 - k1, -3 - k2]])) == [-5, -4], "placed at -4, -5")
ans("kr", 8)
x = rk4(lambda t, v: [v[1], -8 * v[0] - 4 * v[1] + 8 * 1.0], 0, [0, 0], 20)
close(x[0], 1.0, 1e-6, "kr gives y -> r")

# ==== 能控性 ====
W = [[1, 1], [0, 0]]
ok(det2(W) == 0, "uncontrollable example")
A = [[0, 1], [-4, -5]]
B = [0, 2]
AB = [A[0][0] * B[0] + A[0][1] * B[1], A[1][0] * B[0] + A[1][1] * B[1]]
ans("wr-det", det2([[B[0], AB[0]], [B[1], AB[1]]]))
ok(det2([[1, -1], [0, 0]]) == 0, "diagonal example uncontrollable")

# ==== 能观性和观测器 ====
ok(det2([[1, 1], [-1, -3]]) == -2, "W_o example")
ok(charpoly([[-10, 1], [-25, 0]]) == [1.0, 10.0, 25.0], "observer example")
l1, l2 = 12 - 3, 36 - 27 - 2
ans("observer-l2", l2)
cp = charpoly([[-l1, 1], [-2 - l2, -3]])
close(cp[1], 12, 1e-9, "observer s coefficient")
close(cp[2], 36, 1e-9, "observer constant")
# separation: double integrator, K = (8, 4), L = (16, 64) -> poles -2 +- 2i, -8, -8
K = [8, 4]
Lo = [16, 64]
Acl = [
    [0, 1, 0, 0],
    [-K[0], -K[1], K[0], K[1]],
    [0, 0, -Lo[0], 1],
    [0, 0, -Lo[1], 0],
]  # states (x, e), e = x - xhat
rs = eig(Acl)
target = [complex(-2, 2), complex(-2, -2), -8, -8]
ok(all(min(abs(r - t) for r in rs) < 1e-4 for t in target), "separation principle poles")

# ==== LQR ====
def lqr1(a, b, q, r):
    p = r * (a + sqrt(a * a + b * b * q / r)) / (b * b)
    return p, b * p / r


p, Kq = lqr1(1, 1, 3, 1)
close(p, 3, 1e-12, "example p")
close(1 - Kq, -2, 1e-12, "example pole")
p, Kq = lqr1(0, 1, 4, 1)
ans("lqr-gain", Kq)
ans("bryson", 1 / 0.5**2)
p, Kq = lqr1(2, 1, 5, 1)
ans("lqr-pole", 2 - 1 * Kq)
close(-sqrt(4 + 5), 2 - Kq, 1e-12, "closed form pole")
# optimality check: cost with K slightly off is larger (a=2,b=1,q=5,r=1, x0=1)
cost = lambda k: (5 + k * k) / (2 * (k - 2))  # integral of (q + r k^2) x^2 with x = e^{(2-k)t}
ok(cost(Kq) < cost(Kq * 1.05) and cost(Kq) < cost(Kq * 0.95), "LQR gain minimises the cost")
close(cost(Kq), p, 1e-9, "optimal cost = p x0^2")

# ==== 卡尔曼滤波 ====
Kk = 9 / 12
close(50 + Kk * 6, 54.5, 1e-12, "KF example estimate")
close((1 - Kk) * 9, 2.25, 1e-12, "KF example variance")
close(4 / 5, 0.8, what="guess weight")
close(20 + 0.8 * 2, 21.6, 1e-12, "guess 21.6")
ans("kf-update", 100 + 0.25 * 4)
close((1 - 0.25) * 1, 0.75, what="posterior variance 0.75")
ans("kf-predict", 1 * 2 + 0.5)
ans("kf-gain-two-steps", (0.8 + 0.2) / (0.8 + 0.2 + 1))
# minimum-variance check: weight w on measurement, variance (1-w)^2 P + w^2 R is smallest at K
Pm, R = 9.0, 3.0
var = lambda w: (1 - w) ** 2 * Pm + w * w * R
ok(var(Kk) < var(Kk + 0.01) and var(Kk) < var(Kk - 0.01), "Kalman gain minimises variance")
close(var(Kk), 2.25, 1e-12, "minimum variance 2.25")

# ==== MPC ====
close(-4 / 2, -2, what="MPC example unconstrained")
costf = lambda x0, u: (x0 + u) ** 2 + u * u
ok(min([i / 1000 for i in range(-1000, 1001)], key=lambda u: costf(4, u)) == -1, "MPC example constrained")
ans("mpc-one-step", -6 / 2)
ok(min([i / 100 for i in range(-1000, 1001)], key=lambda u: (6 + u) ** 2 + u * u) == -3, "mpc-one-step grid")
Pi1 = 1 + 1 - 1 / (1 + 1)
close(Pi1, 1.5, what="Pi_{N-1}")
ans("dp-riccati", 1 + Pi1 - Pi1**2 / (1 + Pi1))
# example with a = 2: Pi_{N-1} = 3, K_{N-1} = 1; brute force one step from x = 1
close(1 + 4 - 4 * 1 / (1 + 1), 3, 1e-12, "DP example Pi")
close(1 * 1 * 2 / (1 + 1), 1, 1e-12, "DP example K")
bu = min([i / 1000 for i in range(-3000, 1)], key=lambda u: 1 + u * u + (2 + u) ** 2)
close(bu, -1, 1e-9, "DP example u = -x")
close(1 + bu * bu + (2 + bu) ** 2, 3, 1e-9, "DP example cost 3")
close(1 / (1 + 1), 0.5, what="K_{N-1}")
# brute force two-step LQ: min over u0, u1 of x0^2 + u0^2 + x1^2 + u1^2 + x2^2 with x0 = 1
best = min(((1 + u0 + u1) ** 2 + (1 + u0) ** 2 + 1 + u0 * u0 + u1 * u1, u0, u1)
           for u0 in [i / 200 for i in range(-400, 1)] for u1 in [j / 200 for j in range(-400, 1)])
close(best[0], 1.6, 0.0005, "two-step optimal cost = Pi_{N-2} x0^2")
ans("mpc-target", 4 - 0.5 * 4)
ans("terminal-constraint", -2 * 1.5)

# ==== 结业挑战 ====
close(5 * (1 - exp(-1)), 3.16, 0.005, "b-first-order 3.16")
ans("b-first-order", 4, 0.05)
ans("b-second-order", Mp(3 / (2 * 3)), 0.05)
ans("b-steady-error", 1 / (1 + 18), 0.0005)
ans("b-routh", 5 * 6)
wgc, m = pm(lambda w: 6 / (1j * w * (1j * w + 3)))
close(wgc**2, 3, 1e-9, "b wgc^2 = 3")
ans("b-phase-margin", m, 0.05)
A = [[0, 1], [-3, -4]]
B = [1, 1]
AB = [A[0][0] * B[0] + A[0][1] * B[1], A[1][0] * B[0] + A[1][1] * B[1]]
ok(AB == [1, -7], "b AB")
ans("b-controllable", det2([[B[0], AB[0]], [B[1], AB[1]]]))
ok(sorted(round(r.real, 6) for r in eig(A)) == [-3, -1], "b eigenvalues")
ans("b-place", 4 + 16)
ok(charpoly([[0, 1], [-20, -4]]) == [1.0, 4.0, 20.0], "b-place poles -2 +- 4i")
for x1, x2 in ((0.4, -1.1), (2.0, 0.3)):
    close(2 * x1 * (-x1 + x2) + 2 * x2 * (-x1 - x2), -2 * (x1**2 + x2**2), 1e-12, "b-lyapunov Vdot")
ok(all(abs(r.real + 1) < 1e-6 for r in eig([[-1, 1], [-1, -1]])), "b-lyapunov eigenvalues -1 +- i")
ans("b-observer", 16)
p, Kq = lqr1(3, 2, 4, 1)
close(p, 2, 1e-12, "b-lqr p")
close(Kq, 4, 1e-12, "b-lqr K")
ans("b-lqr", 3 - 2 * Kq)
close(30 + 0.25 * 3, 30.75, 1e-12, "b-kalman estimate")
ans("b-kalman", (1 - 2 / 8) * 2)
ok(min([i / 1000 for i in range(-2000, 2001)], key=lambda u: costf(6, u)) == -2, "b-mpc constrained")
ans("b-mpc", -2)

# ---- automation review 2026-11-23: Routh worked example s^3 + 2s^2 + 3s + 4 ----
a3, a2, a1, a0 = 1, 2, 3, 4
row3 = (a2 * a1 - a3 * a0) / a2
close(row3, 1, 1e-12, "routh example third row")
first_col = [a3, a2, row3, a0]
ok(all(v > 0 for v in first_col), "routh example: first column all positive, 0 sign changes")
# ---- compare with the pack ----
pack = Path(__file__).resolve().parents[2] / "data" / "content" / "H.4.1.yaml"
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

print(f"H.4.1 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
