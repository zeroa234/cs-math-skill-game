# Checks every number data/content/M.1.1.yaml states: limits with sympy, values and tables with floats.
# usage: .venv/Scripts/python.exe -I tests/content/M.1.1.verify.py   (needs sympy; prints "N/N claims hold",
# exit code 1 on any mismatch). The project's .venv is made with: python -m venv .venv && .venv/Scripts/pip
# install numpy pandas scikit-learn scipy sympy statsmodels
import math, sys
from fractions import Fraction as F
import sympy as sp

x, n = sp.symbols("x n", real=True)
checks = []
import inspect
def add(got, want, tol=1e-9):
    line = inspect.stack()[1].lineno
    if isinstance(want, float) or isinstance(got, float):
        ok = abs(float(got) - float(want)) <= tol
    else:
        ok = got == want
    checks.append((ok, got, want, line))
def lim(e, at, d="+-"):
    if at in (sp.oo, -sp.oo):
        return sp.limit(e, x, at)
    return sp.limit(e, x, at, dir=d)
def slim(e):
    return sp.limit(e, n, sp.oo)

# ---------------- functions
add(10 + 2 * (5 - 3), 14)
f = lambda t: 2 * t + 1; add(f(3), 7)
add(4**2 - 3 * 4, 4)
add(F(1, 0 - 2), F(-1, 2)); add(F(1, -2 - 2), F(-1, 4))
add([t * t for t in (0, 1, 2, -2)], [0, 1, 4, 4])
add(3**2 - 1, 8)
p = lambda km: 10 if km <= 3 else 10 + 2 * (km - 3); add(p(7), 18); add(p(5), 14)
add(1.01 + 1, 2.01, 1e-12); add((1.01**2 - 1) / (1.01 - 1), 2.01, 1e-9)
add(lim((x**2 - 1) / (x - 1), 1), 2)
add((0.999**2 - 1) / (0.999 - 1), 1.999, 1e-9); add((1.001**2 - 1) / (1.001 - 1), 2.001, 1e-9)

# ---------------- sequences
add(3 * 5 - 1, 14)
a = 2; seq = [a]
for _ in range(3): a = 2 * a + 1; seq.append(a)
add(seq, [2, 5, 11, 23])
add(3 * 2**5, 96); add(2 + 9 * 3, 29)
add(3**2, 9); add((-1)**1, -1); add(F(2, 3), F(2, 2 + 1))
add([F(2 * k, 2 * k - 1) for k in (1, 2, 3, 4)], [F(2), F(4, 3), F(6, 5), F(8, 7)])
add(F(2, 3), F(2 * 1, 2 * 1 + 1)); add(F(2 + 1, 2), F(3, 2))
add([1 / 2**(k - 1) for k in (1, 2, 3, 4)], [1, 0.5, 0.25, 0.125])

# ---------------- seq-limit
add([F(k + 1, k) for k in (1, 2, 3, 4)], [F(2), F(3, 2), F(4, 3), F(5, 4)])
add(abs(1.25 - 1), 0.25); add(abs(0.9 - 1), 0.1, 1e-12)
add(min(k for k in range(1, 5000) if 1 / k < 0.01), 101)
add(min(k for k in range(1, 5000) if 1 / k < 0.001), 1001)
add(slim((3 * n**2 - n) / (2 * n**2 + 5)), sp.Rational(3, 2))
add(slim((5 * n + 2) / (2 * n - 1)), sp.Rational(5, 2))
add(slim((n + 3) / (n**2 + 1)), 0)
add(slim(sp.Rational(9, 10)**n), 0)
add([0.5**k for k in (1, 2, 3)], [0.5, 0.25, 0.125])
add(all(abs(1 + 1 / k - 0.5) > 0.5 for k in range(1, 10000)), True)

# ---------------- bounded-seq
add(round(0.99 - 0.9, 12), 0.09); add(round(0.999 - 0.99, 12), 0.009)
add([F(k, k + 1) for k in (1, 2, 3)], [F(1, 2), F(2, 3), F(3, 4)])
a = 0.0; s6 = [a]
for _ in range(60): a = (a + 6) / 2; s6.append(a)
add(s6[:4], [0, 3, 4.5, 5.25]); add(all(s6[i] < s6[i + 1] < 6 for i in range(40)), True); add(s6[-1], 6.0, 1e-9)
L = sp.symbols("L")
add(sp.solve(sp.Eq(L, (L + 6) / 2), L), [6])
a = 1.0; s2 = [a]
for _ in range(60): a = math.sqrt(2 + a); s2.append(a)
add([round(v, 3) for v in s2[:4]], [1.0, 1.732, 1.932, 1.983]); add(s2[-1], 2.0, 1e-9)
add(sorted(sp.solve(sp.Eq(L**2, L + 2), L)), [-1, 2])
a = 0.0; sh = [a]
for _ in range(60): a = a / 2 + 1; sh.append(a)
add(sh[:4], [0, 1, 1.5, 1.75]); add(sh[-1], 2.0, 1e-9)
add(round((1 + 1 / 10)**10, 4), 2.5937); add(round((1 + 1 / 1000)**1000, 4), 2.7169); add(round(math.e, 5), 2.71828)
es = [(1 + 1 / k)**k for k in range(1, 100000, 97)]
add(all(es[i] < es[i + 1] < 3 for i in range(len(es) - 1)), True)

# ---------------- limit-intuition
add(lim((x**2 + x - 6) / (x - 2), 2), 5)
add([round((t**2 - 1) / (t - 1), 6) for t in (0.9, 0.99, 0.999, 1.001, 1.01, 1.1)], [1.9, 1.99, 1.999, 2.001, 2.01, 2.1])
add(lim((x**2 - 9) / (x - 3), 3), 6)
add(round((2.999**2 - 9) / (2.999 - 3), 6), 5.999); add(round((3.001**2 - 9) / (3.001 - 3), 6), 6.001)
g = lambda t: (math.sqrt(t * t + 9) - 3) / (t * t)
add(round(g(0.1), 5), 0.16662); add(round(g(0.001), 5), 0.16667); add(g(1e-8), 0.0)
add(9 + 1e-16 == 9.0, True)
add(lim((sp.sqrt(x**2 + 9) - 3) / x**2, 0), sp.Rational(1, 6))
add(sp.simplify((sp.sqrt(x**2 + 9) - 3) / x**2 - 1 / (sp.sqrt(x**2 + 9) + 3)), 0)
add(lim((x**2 - 1) / (x + 1), -1), -2)

# ---------------- one-sided
add(lim(sp.Abs(x) / x, 0, "-"), -1); add(lim(sp.Abs(x) / x, 0, "+"), 1)
add((lim(x + 1, 2, "-"), lim(x**2 - 1, 2, "+")), (3, 3))
add((lim(x + 1, 2, "-"), lim(2 * x, 2, "+")), (3, 4))
k = sp.symbols("k"); add(sp.solve(sp.Eq(3 * 1 - 1, 1 + k), k), [1])
add(sp.sin(5 * sp.pi / 2), 1)
add([abs(round(math.sin(math.pi / t), 9)) for t in (0.1, 0.01)], [0.0, 0.0]); add(sp.sin(sp.pi / sp.Rational(2, 101)), 1)
add(round(2 / 101, 4), 0.0198)

# ---------------- infinite-limits
add([round(1 / t**2) for t in (0.1, 0.01, 0.001)], [100, 10000, 1000000])
add([round(1 / t) for t in (0.1, 0.01, 0.001)], [10, 100, 1000])
add(lim(1 / x, 0, "+"), sp.oo); add(lim(1 / x, 0, "-"), -sp.oo); add(lim(1 / x**2, 0), sp.oo)
add([round(1 / (t - 3)) for t in (2.9, 2.99)], [-10, -100]); add(lim(1 / (x - 3), 3, "-"), -sp.oo)
add(lim((x + 1) / ((x - 2) * (x + 1)), -1), sp.Rational(-1, 3))
add(lim((x - 1) / (x**2 - 1), 1), sp.Rational(1, 2)); add(lim((x - 1) / (x**2 - 1), -1, "+"), sp.oo)

# ---------------- limit-laws
add(lim(x**2 + 3 * x, 2), 10)
add(4 * (-2) + 3 * 4, 4)
add(lim(2 * x**2 - 3 * x + 1, 2), 3); add(2 * 2**2 - 3 * 2 + 1, 3)
add(lim(x**3 + 2 * x, -1), -3)
add(lim((x**2 - 1) / (x + 1), 3), 2); add(lim((x**2 + 1) / (x - 1), 3), 5); add(lim(4 * x**5 - x, 1), 3)
add(lim(sp.sqrt(x) * (x + 1), 4), 10)

# ---------------- limit-techniques
add(lim((x**2 - 9) / (x - 3), 3), 6); add(lim((x**2 - 4) / (x - 2), 2), 4)
add(lim((x**2 + x - 2) / (x - 1), 1), 3); add(sp.factor(x**2 + x - 2), (x - 1) * (x + 2))
add(lim((sp.sqrt(1 + x) - 1) / x, 0), sp.Rational(1, 2))
add(lim((sp.sqrt(x) - 2) / (x - 4), 4), sp.Rational(1, 4))
add(lim((1 / x - sp.Rational(1, 2)) / (x - 2), 2), sp.Rational(-1, 4))
add(sp.simplify((1 / x - sp.Rational(1, 2)) / (x - 2) + 1 / (2 * x)), 0)
add(lim((1 / x - sp.Rational(1, 3)) / (x - 3), 3), sp.Rational(-1, 9))
add(abs(-1 / 9 - (-0.1111111)) <= 0.001, True)
add(lim((x**2 + 5 * x + 6) / (x + 2), -2), 1)

# ---------------- squeeze
add(lim(x**2 * sp.sin(1 / x), 0), 0); add(lim(x * sp.cos(1 / x), 0), 0)
add(lim(sp.sin(x) / x, 0), 1); add(lim(sp.sin(2 * x) / x, 0), 2); add(lim(sp.sin(3 * x) / x, 0), 3)
add(lim(sp.sin(5 * x) / (2 * x), 0), sp.Rational(5, 2)); add(lim((1 - sp.cos(x)) / x, 0), 0)
add(all(math.cos(t) <= math.sin(t) / t <= 1 for t in [k / 1000 for k in range(1, 1500)]), True)

# ---------------- limits-at-infinity
add(lim((2 * x**2 + 1) / (5 * x**2 - x), sp.oo), sp.Rational(2, 5))
add(lim((6 * x - 1) / (3 * x + 2), sp.oo), 2); add(lim((3 * x + 1) / (x**2 + 2), sp.oo), 0)
add(lim(x**3 / (x + 1), sp.oo), sp.oo)
add(lim(x**3 - 100 * x**2, sp.oo), sp.oo); add(lim(x**3 - 100 * x**2, -sp.oo), -sp.oo)
add(lim(-2 * x**4 + x, -sp.oo), -sp.oo)
add(2**10, 1024); add(F(1, 2**10), F(1, 1024)); add(lim(3 + 2**x, -sp.oo), 3); t_ = sp.symbols('t_', positive=True); add(sp.limit(2**(-t_), t_, sp.oo), 0)  # sympy 1.14 returns oo for limit(2**x, x, -oo) with real x; substitute x = -t

# ---------------- epsilon-delta
add(round(0.1 / 2, 12), 0.05)
add(round(0.03 / 3, 12), 0.01)
add(all(abs(3 * t - 2 - 4) < 0.03 for t in [2 + 0.01 * (j / 1000 - 1) * 0.999 for j in range(2000)] if t != 2), True)
add(sp.simplify(sp.Abs(5 * x - 3 - 2) - 5 * sp.Abs(x - 1)), 0)
add(round(3 * 2.001 + 1 - 7, 12), 0.003)

# ---------------- epsilon-proofs
add(round(0.1 * 4.1, 12), 0.41)
add(all(abs(t * t - 4) < 0.5 for t in [1.9 + 0.2 * j / 10000 for j in range(1, 10000)]), True)
dl = lambda e: min(1, e / 5)
add(dl(0.5), 0.1); add(dl(10), 1)
for e in (0.5, 10, 0.01):
    d = dl(e)
    add(all(abs(t * t - 4) < e for t in [2 - d + 2 * d * j / 10000 for j in range(1, 10000)]), True)
add(min(0.02, 0.005), 0.005)

# ---------------- no-limit
add(abs(0 - 0.5), 0.5); add(abs(1 - 0.5), 0.5)
add(abs(1 - (-1)), 2)
add(0.1**2, 0.01, 1e-15)
add(all(math.sqrt(t) < 0.1 for t in [0.01 * j / 1000 for j in range(1, 1000)]), True)
add(1 / math.sqrt(10000), 0.01)
add(all(1 / t**2 > 10000 for t in [0.01 * j / 1000 for j in range(1, 1000)]), True)

# ---------------- infinitesimal-order
add([round(t**2, 10) for t in (0.1, 0.01, 0.001)], [0.01, 0.0001, 0.000001])
add(lim(3 * x / x, 0), 3); add(lim((x**2 + x) / x, 0), 1)
add(lim((1 - sp.cos(x)) / x**2, 0), sp.Rational(1, 2))
add(sp.simplify(1 - sp.cos(x) - 2 * sp.sin(x / 2)**2), 0)
add(lim(sp.sin(4 * x) / (3 * x), 0), sp.Rational(4, 3))
add(lim((sp.sin(x) - x) / x**3, 0), sp.Rational(-1, 6))
add(lim(x * sp.sin(2 * x) / (1 - sp.cos(x)), 0), 4)
add(lim(1 / x, sp.oo), 0)

# ---------------- continuity
add(lim((x**2 - 4) / (x - 2), 2), 4); add(lim((x**2 - 9) / (x - 3), 3), 6)
add(sp.solve(sp.Eq(k * 1 + 1, 1**2 + 2), k), [2])
add(lim(sp.cos(x) + x**2, 0), 1)

# ---------------- discontinuities
e = (x**2 - x) / (x**2 - 1)
add(lim(e, 1), sp.Rational(1, 2)); add(lim(e, -1, "+"), -sp.oo); add(lim(e, -1, "-"), sp.oo)
add([math.floor(v) for v in (2.7, 2, 1.99)], [2, 2, 1])
add((lim(sp.floor(x), 2, "-"), lim(sp.floor(x), 2, "+")), (1, 2))
e = (x + 2) / (x**2 - 4)
add(lim(e, 2, "+"), sp.oo); add(lim(e, 2, "-"), -sp.oo); add(lim(e, -2), sp.Rational(-1, 4))

# ---------------- continuity-interval
add(lim(sp.sqrt(x**2 + 3), 1), 2)
add(slim(sp.sqrt(4 + 1 / n)), 2)
add(slim(sp.sin(sp.pi / 2 * n / (n + 1))), 1)
add(slim(sp.cos(1 / n)), 1)
add(all(math.floor(1 - 1 / m) == 0 for m in range(1, 10000)), True); add(math.floor(1), 1)

# ---------------- ivt
gg = lambda t: t**3 + t - 1
add([gg(0), gg(1), gg(2), gg(-1)], [-1, 1, 9, -3])
add(gg(0.5), -0.375); add(0.75**3, 0.421875); add(gg(0.75), 0.171875)
add(0.625**3, 0.244140625); add(gg(0.625), -0.130859375); add(round(gg(0.625), 4), -0.1309)
add(round(gg(0.6875), 4), 0.0125)
add(round(1 / 512, 5), 0.00195); add(round(1 / 1024, 6), 0.000977)
add(min(m for m in range(1, 30) if 2**-m < 0.001), 10)
add(sp.nsolve(x**3 + x - 1, x, 0.68) > 0.625 and sp.nsolve(x**3 + x - 1, x, 0.68) < 0.6875, True)

# ---------------- extreme-value
fx = lambda t: t * t - 2 * t
add([fx(0), fx(1), fx(3)], [0, -1, 3]); add(sp.expand((x - 1)**2 - 1), x**2 - 2 * x)
add([abs(t - 1) for t in (0, 1, 3)], [1, 0, 2])
fy = lambda t: t * t - 4 * t + 1
add([fy(0), fy(2), fy(5)], [1, -3, 6]); add(sp.expand((x - 2)**2 - 3), x**2 - 4 * x + 1)
add(min(fy(j / 1000) for j in range(0, 5001)), -3)

# ---------------- uniform
add(1 / 0.01, 100.0); add(round(1 / 0.011, 1), 90.9)
add(round(1 / 0.001 - 1 / 0.0011, 1), 90.9); add(round(1 / 0.0011, 2), 909.09)
add(0.01 / 2, 0.005)
add(round(1000.001**2 - 1000**2, 1), 2.0)

# ---------------- boss
a = 1.0; sb = [a]
for _ in range(60): a = (a + 8) / 3; sb.append(a)
add([round(v, 3) for v in sb[:4]], [1.0, 3.0, 3.667, 3.889]); add(sb[-1], 4.0, 1e-9)
add(sp.solve(sp.Eq(L, (L + 8) / 3), L), [4])
add(round(0.02 / 4, 12), 0.005)

bad = [(ln, g, w) for (ok, g, w, ln) in checks if not ok]
for i, g, w in bad:
    print(f"line {i}: got {g!r}, want {w!r}")
print(f"{len(checks) - len(bad)}/{len(checks)} claims hold")
sys.exit(1 if bad else 0)
