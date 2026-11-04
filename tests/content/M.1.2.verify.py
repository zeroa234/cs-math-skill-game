# Checks every number data/content/M.1.2.yaml states: derivatives, limits and series with sympy, values,
# approximations and error bounds with floats, and the plot sims (secant slopes, Taylor errors) at their
# solutions. Every graded number item's `answer` is read from the pack and compared with the value computed
# here (ANSWERS below); the run fails if a number item has no computed value or the two disagree.
# usage: .venv/Scripts/python.exe -I tests/content/M.1.2.verify.py   (needs sympy; prints "N/N claims hold",
# exit code 1 on any mismatch). The .venv is made as described in tests/content/M.1.1.verify.py.
import inspect, math, os, re, sys
from fractions import Fraction as F
import sympy as sp

x, h, t, u, y, w, n, th = sp.symbols("x h t u y w n theta", real=True)
checks = []
def add(got, want, tol=1e-9):
    line = inspect.stack()[1].lineno
    if isinstance(want, (float, int)) and not isinstance(want, bool) and (isinstance(got, float) or isinstance(want, float)):
        ok = abs(float(got) - float(want)) <= tol
    else:
        ok = got == want
        if not ok and (isinstance(got, sp.Expr) or isinstance(want, sp.Expr)):
            ok = sp.simplify(got - want) == 0
    checks.append((bool(ok), got, want, line))
def same(e1, e2):  # symbolic identity
    line = inspect.stack()[1].lineno
    ok = sp.simplify(sp.expand(e1 - e2)) == 0
    checks.append((ok, e1, e2, line))
D = lambda e, v=x, k=1: sp.diff(e, v, k)
at = lambda e, v, val: e.subs(v, val)
lim = lambda e, a, d="+-": sp.limit(e, x, a, dir=d) if a not in (sp.oo, -sp.oo) else sp.limit(e, x, a)
coef = lambda e, k, order=12: sp.series(e, x, 0, order).removeO().coeff(x, k)
def idiff(eq, k=1):  # dy/dx (and d2y/dx2) of an implicit curve eq(x, y) = 0
    return sp.idiff(eq, y, x, k)
ANSWERS = {}  # "lesson/item" -> value the graded answer must equal

# ---------------- secant-tangent
add(F(9 - 1, 3 - 1), 4)
ANSWERS["secant-tangent/line-slope"] = (4 - 1) / (2 - 1)
f = x**2
add(at(f, x, 1.5), 2.25); ANSWERS["secant-tangent/secant-half"] = float((at(f, x, 1.5) - 1) / 0.5)
same((at(f, x, 1 + h) - at(f, x, 1)) / h, 2 + h)
add(abs(((1.005)**2 - 1) / 0.005 - 2) < 0.01, True)            # sim solution h = 0.005
same(at(f, x, 1 + h) - at(f, x, 1), 2 * h + h**2); add(lim((2 + x), 0), 2)
same(at(f, x, 3 + h) - at(f, x, 3), 6 * h + h**2); ANSWERS["secant-tangent/def-at-3"] = 6
g = 3 * x**2 - 4 * x + 1
add(at(g, x, 2), 5); same(at(g, x, 2 + h), 5 + 8 * h + 3 * h**2)
ANSWERS["secant-tangent/def-poly"] = sp.limit((at(g, x, 2 + h) - 5) / h, h, 0)

# ---------------- derivative-function
ANSWERS["derivative-function/guess"] = 2 * 5
same(((x + h)**2 - x**2) / h, 2 * x + h)
ANSWERS["derivative-function/slope-neg"] = at(D(x**2), x, -1)
same(1 / (x + h) - 1 / x, -h / (x * (x + h))); same(sp.limit(-1 / (x * (x + h)), h, 0), -1 / x**2)
ANSWERS["derivative-function/recip-at-3"] = float(at(D(1 / x), x, 3)); add(at(D(1 / x), x, 3), sp.Rational(-1, 9))
same(sp.expand((x + h)**3), x**3 + 3 * x**2 * h + 3 * x * h**2 + h**3)
same(sp.expand(((x + h)**3 - x**3) / h), 3 * x**2 + 3 * x * h + h**2)
ANSWERS["derivative-function/power5"] = at(D(x**5), x, 2)
tl = lambda fn, a: at(fn, x, a) + at(D(fn), x, a) * (x - a)      # tangent line at a
same(tl(1 / x, 1), -x + 2)
same(tl(1 / x, 2), -x / 4 + 1); ANSWERS["derivative-function/tangent-recip"] = at(tl(1 / x, 2), x, 0)
L4 = tl(1 / x, 4); xi = sp.solve(L4, x)[0]; yi = at(L4, x, 0)
add(xi, 8); add(yi, sp.Rational(1, 2)); ANSWERS["derivative-function/triangle-area"] = xi * yi / 2
a_ = sp.symbols("a", positive=True); La = tl(1 / x, a_)
add(sp.solve(La, x)[0], 2 * a_); add(at(La, x, 0), 2 / a_); add(sp.simplify(2 * a_ * (2 / a_) / 2), 2)
same(D(x**100), 100 * x**99)

# ---------------- sum-rule
ANSWERS["sum-rule/poly-at-1"] = at(D(x**3 + 5 * x**10), x, 1)
ANSWERS["sum-rule/poly-at-neg1"] = at(D(4 * x**3 - 2 * x + 7), x, -1)
p = x**3 - x
add(at(p, x, 2), 6); add(at(D(p), x, 2), 11); same(tl(p, 2), 11 * x - 16)
q = x**2 - 4 * x
add(at(q, x, 3), -3); add(at(D(q), x, 3), 2); same(tl(q, 3), 2 * x - 9); ANSWERS["sum-rule/tangent-quad"] = at(tl(q, 3), x, 0)
same(D(3 * x**2), 6 * x); ANSWERS["sum-rule/stretch"] = at(D(5 * x**4), x, 1)

# ---------------- differentiable
fa = sp.Abs(x - 2)
ANSWERS["differentiable/abs-left"] = sp.limit((at(fa, x, 2 + h) - 0) / h, h, 0, dir="-")
add(sp.limit((at(fa, x, 2 + h)) / h, h, 0, dir="+"), 1)
add(sp.limit(sp.Abs(h) / h, h, 0, dir="+"), 1); add(sp.limit(sp.Abs(h) / h, h, 0, dir="-"), -1)
hp = sp.symbols("hp", positive=True)
add(sp.limit(sp.cbrt(hp) / hp, hp, 0), sp.oo)
right = 2 * x**5 + 3 * x**4 + 4 * x**2 + 5 * x + 6
a, b = sp.symbols("a b")
left = a * x**2 + b * x + 6
add(at(right, x, 1), 20); add(at(D(right), x, 1), 35)
sol = sp.solve([at(left, x, 1) - 20, at(D(left), x, 1) - 35], [a, b]); add(sol[a], 21); add(sol[b], -7)
add(at(right, x, 0), 6); add(at(left, x, 0), 6)
ANSWERS["differentiable/smooth-at-0"] = sp.solve(at(D(left), x, 0) - at(D(right), x, 0), b)[0]

# ---------------- rate-of-change
hh = 80 - 5 * t**2
add(at(hh, t, 4), 0); ANSWERS["rate-of-change/guess"] = (at(hh, t, 4) - at(hh, t, 0)) / 4
add(at(hh, t, 1), 75); add(at(hh, t, 3), 35); ANSWERS["rate-of-change/avg-1-3"] = (35 - 75) / (3 - 1)
same(D(hh, t), -10 * t); add(at(D(hh, t), t, 4), -40); add(40 * 3.6, 144.0)
ANSWERS["rate-of-change/speed-at-2"] = at(D(hh, t), t, 2)
acc = -5 * t**2 + 60 * t + 120
same(D(acc, t), -10 * t + 60); add(at(D(acc, t), t, 1), 50)
add([at(acc, t, k) for k in (1, 2, 3)], [175, 220, 255]); add(at(acc, t, 2) - at(acc, t, 1), 45)
ANSWERS["rate-of-change/balance-10"] = at(D(acc, t), t, 10)
tm = sp.solve(D(acc, t), t)[0]; add(tm, 6); ANSWERS["rate-of-change/balance-max"] = at(acc, t, tm)
add([at(acc, t, 5), at(acc, t, 7)], [295, 295])
add(at(acc, t, 11) - at(acc, t, 10), -45)

# ---------------- sin-cos
add(lim(sp.sin(x) / x, 0), 1); add(lim((sp.cos(x) - 1) / x, 0), 0)
add(abs((math.cos(0.01) - 1) / 0.01 - 0) < 0.01, True)          # sim solution h = 0.01
same(sp.expand_trig(sp.sin(x + h)), sp.sin(x) * sp.cos(h) + sp.cos(x) * sp.sin(h))
same(sp.expand_trig(sp.cos(x + h)), sp.cos(x) * sp.cos(h) - sp.sin(x) * sp.sin(h))
same(D(sp.sin(x)), sp.cos(x)); same(D(sp.cos(x)), -sp.sin(x))
ANSWERS["sin-cos/sin-at"] = at(D(sp.sin(x)), x, sp.pi / 3)
add(lim(sp.sin(sp.pi * x / 180) / x, 0), sp.pi / 180); add(round(math.pi / 180, 5), 0.01745)
hx = sp.sin(x) + sp.sqrt(3) * sp.cos(x)
for k in range(-2, 3): add(sp.simplify(at(D(hx), x, sp.pi / 6 + k * sp.pi)), 0)
add(sp.tan(sp.pi / 6), 1 / sp.sqrt(3)); same(sp.expand_trig(2 * sp.sin(x + sp.pi / 3)), hx)
gx = sp.sin(x) + sp.cos(x); roots = [r for r in sp.solveset(D(gx), x, sp.Interval.open(0, sp.pi))]
add(roots, [sp.pi / 4]); ANSWERS["sin-cos/flat-sin-cos"] = float(sp.pi / 4)
ANSWERS["sin-cos/lin-comb"] = at(D(5 * sp.sin(x) - 2 * sp.cos(x)), x, 0)

# ---------------- product-rule
same(D(x * x), 2 * x)
ANSWERS["product-rule/x3x4"] = at(D(x**3) * x**4 + x**3 * D(x**4), x, 1); add(at(D(x**7), x, 1), 7)
U, V = sp.Function("U"), sp.Function("V")
same(U(x + h) * V(x + h) - U(x) * V(x), (U(x + h) - U(x)) * V(x + h) + U(x) * (V(x + h) - V(x)))
yp = D(x**3 * sp.sin(x)); same(yp, 3 * x**2 * sp.sin(x) + x**3 * sp.cos(x))
add(at(yp, x, sp.pi / 2), 3 * sp.pi**2 / 4); add(round(float(3 * sp.pi**2 / 4), 3), 7.402)
ANSWERS["product-rule/x2cos"] = float(at(D(x**2 * sp.cos(x)), x, sp.pi)); add(at(D(x**2 * sp.cos(x)), x, sp.pi), -2 * sp.pi)
tri = x * (x + 1) * (x + 2); ANSWERS["product-rule/three"] = at(D(tri), x, 1)
add([1 * 2 * 3, 1 * 1 * 3, 1 * 2 * 1], [6, 3, 2]); same(sp.expand(tri), x**3 + 3 * x**2 + 2 * x)
same(D(x**2 * sp.sin(x)), 2 * x * sp.sin(x) + x**2 * sp.cos(x))

# ---------------- quotient-rule
same(D(x**2 / x), 1)
uu, vv = U(x), V(x)
same(D(uu / vv), (D(uu) * vv - uu * D(vv)) / vv**2)
fq = x**2 / (x + 1); same(D(fq), (x**2 + 2 * x) / (x + 1)**2); ANSWERS["quotient-rule/frac-at-1"] = float(at(D(fq), x, 1))
nn = sp.symbols("nn", positive=True, integer=True); same(D(x**(-nn)), -nn * x**(-nn - 1))
same(D(1 / x), -x**-2); ANSWERS["quotient-rule/neg-power"] = float(at(D(1 / x**2), x, 2))
same(D(sp.tan(x)), 1 / sp.cos(x)**2); ANSWERS["quotient-rule/tan-at"] = sp.simplify(at(D(sp.tan(x)), x, sp.pi / 4))
fs = (x**4 + 1) / x**2; same(D(fs), (2 * x**4 - 2) / x**3); ANSWERS["quotient-rule/simplify-first"] = float(at(D(fs), x, 2))
add(F(30, 8), F(15, 4)); same(D(x / 1), 1)

# ---------------- chain-rule
same(D(sp.sin(3 * x)), 3 * sp.cos(3 * x))
ANSWERS["chain-rule/sin10t"] = at(D(sp.sin(10 * t), t), t, 0)
same(D(sp.sin(x**2)), 2 * x * sp.cos(x**2))
ANSWERS["chain-rule/power-chain"] = at(D((x**2 + 1)**5), x, 1)
s10 = D(sp.sin(t)**10, t); same(s10, 10 * sp.sin(t)**9 * sp.cos(t))
ANSWERS["chain-rule/sin-pow"] = float(at(s10, t, sp.pi / 4)); add(at(s10, t, sp.pi / 4), sp.Rational(5, 16))
same(D(sp.cos(th**4)**2, th), -8 * th**3 * sp.cos(th**4) * sp.sin(th**4))
same(D(sp.sin(3 * x)**2), 6 * sp.sin(3 * x) * sp.cos(3 * x))
pc = 3 * x**2 * (x + 1)**-1 + x**3 * (-1) * (x + 1)**-2
same(pc, D(x**3 / (x + 1))); same(D(x**3 / (x + 1)), (2 * x**3 + 3 * x**2) / (x + 1)**2)
ANSWERS["chain-rule/quot-by-chain"] = float(at(pc, x, 1))

# ---------------- higher-derivatives
ANSWERS["higher-derivatives/guess"] = at(D(t**3, t, 2), t, 2)
ANSWERS["higher-derivatives/x4-third"] = at(D(x**4, x, 3), x, 1)
add([D(sp.sin(x), x, k) for k in range(1, 5)], [sp.cos(x), -sp.sin(x), -sp.cos(x), sp.sin(x)])
same(D(sp.sin(x), x, 10), -sp.sin(x)); same(D(sp.sin(x), x, 5), sp.cos(x)); same(D(sp.sin(x), x, 9), sp.cos(x))
add(sp.factorial(4), 24); ANSWERS["higher-derivatives/d5x5"] = D(x**5, x, 5); add(D(x**5, x, 6), 0)
fpp = 3 * sp.sin(x) - sp.cos(x); same(D(fpp, x, 2), -fpp); same(D(sp.exp(x), x, 2), sp.exp(x)); same(D(x**2, x, 2), 2)

# ---------------- implicit
add(F(4, 3) * F(-3, 4), -1)
circ = x**2 + y**2 - 25
same(idiff(circ), -x / y)
ANSWERS["implicit/circle-34"] = float(idiff(circ).subs({x: 3, y: 4}))
ANSWERS["implicit/circle-3m4"] = float(idiff(circ).subs({x: 3, y: -4}))
c2 = y**4 + x * y**2 - 2
add(c2.subs({x: 1, y: 1}), 0); same(idiff(c2), -y**2 / (4 * y**3 + 2 * x * y)); add(idiff(c2).subs({x: 1, y: 1}), sp.Rational(-1, 6))
c3 = x**2 + x * y + y**2 - 3
add(c3.subs({x: 1, y: 1}), 0); same(idiff(c3), -(2 * x + y) / (x + 2 * y)); ANSWERS["implicit/xy-curve"] = idiff(c3).subs({x: 1, y: 1})
ANSWERS["implicit/x23"] = float(at(D(x**sp.Rational(2, 3)), x, 8)); add(at(D(x**sp.Rational(2, 3)), x, 8), sp.Rational(1, 3))
ANSWERS["implicit/sqrt4"] = float(at(D(sp.sqrt(x)), x, 4))

# ---------------- implicit-practice
fol = y**3 + x**3 - 3 * x * y; P = {x: sp.Rational(4, 3), y: sp.Rational(2, 3)}
add(sp.Rational(8, 27) + sp.Rational(64, 27), sp.Rational(8, 3)); add(3 * P[x] * P[y], sp.Rational(8, 3)); add(fol.subs(P), 0)
same(idiff(fol), (y - x**2) / (y**2 - x))
add((P[y] - P[x]**2), sp.Rational(-10, 9)); add((P[y]**2 - P[x]), sp.Rational(-8, 9)); add(idiff(fol).subs(P), sp.Rational(5, 4))
hyp = y**2 - x**2 - 1; same(idiff(hyp), x / y)
ANSWERS["implicit-practice/hyperbola"] = float(idiff(hyp).subs({x: 1, y: sp.sqrt(2)}))
cs = x**3 + y**3 - 9; add(cs.subs({x: 1, y: 2}), 0); ANSWERS["implicit-practice/cubic-sum"] = float(idiff(cs).subs({x: 1, y: 2}))
el = x**2 + 4 * y**2 - 1; same(idiff(el), -x / (4 * y)); add(idiff(el).subs({x: 0, y: sp.Rational(1, 2)}), 0)
ypp = idiff(el, 2)
add(sp.simplify(ypp - (-(x**2 + 4 * y**2) / (16 * y**3))), 0)
ANSWERS["implicit-practice/ellipse-ypp"] = float((-1 / (16 * y**3)).subs(y, sp.Rational(1, 2)))

# ---------------- inverse-functions
add(2 * 3 + 1, 7); add(F(7 - 1, 2), 3); add(2 * 7 - 1, 13)
ANSWERS["inverse-functions/cube-inv"] = sp.solve(x**3 - 8, x)[0]
fi = x**3 + x; add(at(fi, x, 1), 2); ANSWERS["inverse-functions/inv-slope"] = float(1 / at(D(fi), x, 1))
same(D(sp.sqrt(x)), 1 / (2 * sp.sqrt(x)))
ANSWERS["inverse-functions/cbrt-inv"] = float(1 / (3 * 2**2)); add(at(D(sp.cbrt(x)), x, 8), sp.Rational(1, 12))

# ---------------- inverse-trig
add(sp.tan(5 * sp.pi / 4), 1); add(round(math.tan(1), 3), 1.557)
add(sp.asin(sp.Rational(1, 2)), sp.pi / 6); add(sp.sin(5 * sp.pi / 6), sp.Rational(1, 2)); add(sp.sin(sp.pi / 3), sp.sqrt(3) / 2)
same(D(sp.atan(x)), 1 / (1 + x**2)); same(sp.cos(sp.atan(x)), 1 / sp.sqrt(1 + x**2))
ANSWERS["inverse-trig/atan1"] = float(at(D(sp.atan(x)), x, 1))
same(D(sp.asin(x)), 1 / sp.sqrt(1 - x**2)); same(D(sp.acos(x)), -1 / sp.sqrt(1 - x**2))
ANSWERS["inverse-trig/asin06"] = float(at(D(sp.asin(x)), x, sp.Rational(3, 5)))
ANSWERS["inverse-trig/atan2x"] = at(D(sp.atan(2 * x)), x, 0)
add(sp.acos(-1), sp.pi); add(sp.acos(1), 0)

# ---------------- exp-log
M = lambda base: math.log(base)
add(round(M(2), 4), 0.6931); add(round(M(3), 4), 1.0986)
add(abs((2**0.005 - 1) / 0.005 - 0.6931) < 0.002, True)        # sim solution h = 0.005
add((2**1 - 2**0) / 1, 1.0)
add(round(math.e, 5), 2.71828); add(abs(2**(1 / M(2)) - math.e) < 1e-12, True)
ANSWERS["exp-log/e3x"] = at(D(sp.exp(3 * x)), x, 0)
same(D(sp.log(x)), 1 / x); ANSWERS["exp-log/ln4"] = float(at(D(sp.log(x)), x, 4))
same(D(sp.log(1 + x**2)), 2 * x / (1 + x**2))
d1a = D(x**3 * sp.exp(2 * x)); same(d1a, x**2 * (2 * x + 3) * sp.exp(2 * x))
ANSWERS["exp-log/x3e2x"] = float(at(d1a, x, 1)); add(at(d1a, x, 1), 5 * sp.E**2)
same(D(sp.log(sp.cos(x))), -sp.tan(x)); ANSWERS["exp-log/ln-cos"] = sp.simplify(at(D(sp.log(sp.cos(x))), x, sp.pi / 4))
same(sp.expand_log(sp.log(sp.exp(x**2)), force=True), x**2)

# ---------------- log-diff
add((sp.log(sp.E))**3, 1); add(3 * sp.log(sp.E), 3)
same(D(2**x), sp.log(2) * 2**x); same(D(10**x), sp.log(10) * 10**x)
ANSWERS["log-diff/two-x"] = float(at(D(2**x), x, 3))
xx = D(x**x); same(xx, x**x * (1 + sp.log(x))); ANSWERS["log-diff/xx2"] = float(at(xx, x, 2))
r_ = sp.symbols("r", real=True); xp = sp.symbols("xp", positive=True); same(sp.diff(xp**r_, xp), r_ * xp**(r_ - 1))
pm = x**sp.pi + sp.pi**x; ANSWERS["log-diff/pi-mix"] = float(at(D(pm), x, 1))
add(round(float(sp.pi * sp.log(sp.pi)), 4), 3.5963)
yl = (x + 1)**2 * (x + 2)**3
add(at(yl, x, 0), 8); add(at(2 / (x + 1) + 3 / (x + 2), x, 0), sp.Rational(7, 2)); ANSWERS["log-diff/log-product"] = at(D(yl), x, 0)
add(2 * 8 + 3 * 4, 28)

# ---------------- linear-approx
add(2 + 0.25 * 0.1, 2.025, 1e-12); add(2.05**2, 4.2025, 1e-12); add(2.1**2, 4.41, 1e-12); add(round(math.sqrt(4.1), 5), 2.02485)
lin = lambda fn, a0, xv: float(at(fn, x, a0) + at(D(fn), x, a0) * (xv - a0))
ANSWERS["linear-approx/recip-21"] = lin(1 / x, 2, 2.1); add(round(1 / 2.1, 5), 0.47619)
for fn, (v0, d0), approx in [(sp.sin(x), (0, 1), x), (sp.cos(x), (1, 0), 1), (sp.exp(x), (1, 1), 1 + x), (sp.log(1 + x), (0, 1), x), ((1 + x)**r_, (1, r_), 1 + r_ * x)]:
    add(at(fn, x, 0), v0); add(sp.simplify(at(D(fn), x, 0) - d0), 0); same(at(fn, x, 0) + at(D(fn), x, 0) * x, approx)
ANSWERS["linear-approx/cube-101"] = 1 + 3 * 0.01; add(1.01**3, 1.030301, 1e-12); add(round(1.01**3 - 1.03, 4), 0.0003)
ANSWERS["linear-approx/e002"] = 1 + 0.02; add(round(math.exp(0.02), 6), 1.020201)
add(round(math.sin(0.01), 7), 0.0099998); add(round(math.sin(1), 3), 0.841); add(1 - math.sin(1) > 0.15, True)
add(round(math.pi - 3.1, 4), 0.0416); add(round(math.sin(3.1), 4), 0.0416)
add(lin(sp.log(x), 1, 0.98), -0.02, 1e-12); add(round(math.log(0.98), 4), -0.0202)
add(at(D(sp.cbrt(x)), x, 8), sp.Rational(1, 12)); ANSWERS["linear-approx/cbrt83"] = 2 + 0.3 / 12; add(round(8.3**(1 / 3), 4), 2.0247)

# ---------------- differentials
add(10.1**2 - 100, 2.01, 1e-9); add(2 * 10 * 0.1, 2.0, 1e-12); add(10 * 0.1, 1.0, 1e-12)
ANSWERS["differentials/dy-gap"] = (10.1**2 - 100) - 2 * 10 * 0.1
dyc = F(1, 3) * F(1, 16) * F(1, 10); add(dyc, F(1, 480)); add(round(1 / 480, 5), 0.00208); add(round(4 + 1 / 480, 5), 4.00208)
add(at(D(x**sp.Rational(1, 3)), x, 64), sp.Rational(1, 48)); add(abs(64.1**(1 / 3) - (4 + 1 / 480)) < 1e-5, True)
ANSWERS["differentials/sqrt1005"] = 10 + 0.5 / 20; add(round(math.sqrt(100.5), 5), 10.02497)
same(D(sp.sin(th) * sp.cos(th), th), sp.cos(th)**2 - sp.sin(th)**2)
dpoly = D(7 * u**9 + 34 - 5 * u**-3, u); same(dpoly, 63 * u**8 + 15 * u**-4); ANSWERS["differentials/d-poly"] = at(dpoly, u, 1)
ANSWERS["differentials/cube-err"] = 3 * 5**2 * 0.1; add(5.1**3 - 125, 7.651, 1e-9); add(125 - 4.9**3, 7.351, 1e-9)

# ---------------- approx-uses
add(round(1.02**3, 3), 1.061)
rr, dr = sp.symbols("rr dr", positive=True); Vb = sp.Rational(4, 3) * sp.pi * rr**3
same(D(Vb, rr) * dr / Vb, 3 * dr / rr); add(3 * 80 / 4000, 0.06, 1e-12); add(80 / 4000, 0.02, 1e-12)
Ac = sp.pi * rr**2; same(D(Ac, rr) * dr / Ac, 2 * dr / rr); ANSWERS["approx-uses/circle-rel"] = 2 * 1
same(sp.expand((1 - 3 * x) * (1 - x / 2)), 1 - sp.Rational(7, 2) * x + sp.Rational(3, 2) * x**2)
add(coef(sp.exp(-3 * x) / sp.sqrt(1 + x), 1), sp.Rational(-7, 2))
ANSWERS["approx-uses/prod-lin"] = float(coef(sp.sqrt(1 + x) * sp.exp(x), 1)); same(sp.expand((1 + x / 2) * (1 + x)), 1 + sp.Rational(3, 2) * x + x**2 / 2)
same(sp.series((1 + u)**sp.Rational(-1, 2), u, 0, 2).removeO(), 1 - u / 2)
vc2 = (4 / 3e5)**2; add(round(vc2 * 1e10, 1), 1.8); add(round(vc2 / 2 * 1e11, 1), 8.9)
ANSWERS["approx-uses/gps-day"] = round(86400 * 8.9e-11 * 1e6, 1); add(abs(86400 * vc2 / 2 * 1e6 - 7.7) < 0.05, True)
weq = (w + 1) * sp.exp(w) - x
add(weq.subs({w: 0, x: 1}), 0); same(sp.simplify(sp.idiff(weq, w, x) - 1 / ((w + 2) * sp.exp(w))), 0)
add(sp.idiff(weq, w, x).subs({w: 0, x: 1}), sp.Rational(1, 2)); add(0 + 0.5 * (1.5 - 1), 0.25, 1e-12)
add(round(float(sp.nsolve((w + 1) * sp.exp(w) - 1.5, w, 0.2)), 3), 0.213)
yeq = y + y**3 - x; add(yeq.subs({y: 1, x: 2}), 0); add(sp.idiff(yeq, y, x).subs({y: 1, x: 2}), sp.Rational(1, 4))
ANSWERS["approx-uses/y-plus-y3"] = 1 + 0.25 * 0.2; add(round(float(sp.nsolve(y + y**3 - 2.2, y, 1)), 4), 1.0482)

# ---------------- fermat-rolle
add(sorted(sp.solve(D(x**3 - 12 * x), x)), [-2, 2]); ANSWERS["fermat-rolle/crit-pos"] = 2
add(D(x**3).subs(x, 0), 0); add((-0.1)**3 < 0 < 0.1**3, True)
fr = x**2 + 2 * x; add([at(fr, x, -2), at(fr, x, 0)], [0, 0]); add(sp.solve(D(fr), x), [-1])
fr2 = 2 * x**2 - 8 * x + 6; add([at(fr2, x, 1), at(fr2, x, 3)], [0, 0]); ANSWERS["fermat-rolle/rolle-quad"] = sp.solve(D(fr2), x)[0]
fr3 = x**3 - 4 * x; add([at(fr3, x, -2), at(fr3, x, 2)], [0, 0])
cs3 = sorted(sp.solve(D(fr3), x)); add(cs3, [-2 / sp.sqrt(3), 2 / sp.sqrt(3)]); ANSWERS["fermat-rolle/rolle-cubic"] = float(cs3[1])
add([abs(-1) - 1, abs(1) - 1], [0, 0])

# ---------------- mvt
add(3000 / 6, 500.0)
st = -16 * t**2 + 100; add(at(st, t, sp.Rational(5, 2)), 0); add((at(st, t, sp.Rational(5, 2)) - at(st, t, 0)) / sp.Rational(5, 2), -40)
ANSWERS["mvt/fall"] = float(sp.solve(D(st, t) + 40, t)[0])
ANSWERS["mvt/x2-13"] = sp.solve(D(x**2) - (9 - 1) / 2, x)[0]
add((sp.sqrt(9) - 0) / 9, sp.Rational(1, 3)); add(sp.solve(D(sp.sqrt(x)) - sp.Rational(1, 3), x), [sp.Rational(9, 4)])
add((27 - 0) / 3, 9.0); ANSWERS["mvt/x3-03"] = float([r for r in sp.solve(3 * x**2 - 9, x) if r > 0][0])
add(F(abs(2) - abs(-1), 3), F(1, 3)); add((1 / 1 - 1 / -1) / (1 - -1), 1.0)

# ---------------- mvt-consequences
ANSWERS["mvt-consequences/same-deriv"] = at(x**2 + 3, x, 2)
add(all(1 - 1 / (1 + v) > 0 for v in (0.001, 0.5, 3, 100)), True); add(all(math.log(1 + v) < v for v in (0.001, 0.5, 3, 100)), True)
add(all(math.exp(v) > 1 + v + v * v / 2 for v in (0.001, 0.5, 3)), True)
add(abs(math.sin(0.31) - math.sin(0.30)) <= 0.01, True)
add(1 / (2 * math.sqrt(100)), 0.05, 1e-12); ANSWERS["mvt-consequences/sqrt101"] = 10 + 0.05; add(round(math.sqrt(101), 4), 10.0499)
add(all(math.tan(v) > v for v in (0.01, 0.5, 1.5)), True)

# ---------------- monotone-extrema
m = x**3 - 3 * x
add([at(D(m), x, v) for v in (-2, 0, 2)], [9, -3, 9]); add(sorted(sp.solve(D(m), x)), [-1, 1])
add(at(m, x, -1), 2); add(at(m, x, 1), -2); add(sp.solve_univariate_inequality(D(m) < 0, x, relational=False), sp.Interval.open(-1, 1))
m2 = x**3 - 12 * x; add(sp.solve_univariate_inequality(D(m2) < 0, x, relational=False), sp.Interval.open(-2, 2))
ANSWERS["monotone-extrema/dec-end"] = 2; ANSWERS["monotone-extrema/max-val"] = at(m2, x, -2)
m3 = x**3 - 3 * x**2 - 9 * x - 1; same(D(m3), 3 * (x - 3) * (x + 1)); add(at(m3, x, -1), 4); ANSWERS["monotone-extrema/cubic-test"] = at(m3, x, 3)
add(at(D(m, x, 2), x, 1), 6)
m4 = x**4 - 2 * x**2; add(sorted(sp.solve(D(m4), x)), [-1, 0, 1]); add([at(D(m4, x, 2), x, v) for v in (-1, 0, 1)], [8, -4, 8])
ANSWERS["monotone-extrema/quartic-min"] = at(m4, x, 1); add(at(m4, x, 0), 0)
m5 = x**5 - 5 * x**3; same(D(m5), 5 * x**2 * (x**2 - 3)); add([at(D(m5), x, -1) < 0, at(D(m5), x, 1) < 0], [True, True]); add(at(D(m5, x, 2), x, 0), 0)
for g4 in (x**4, -x**4, x**3): add([at(D(g4), x, 0), at(D(g4, x, 2), x, 0)], [0, 0])

# ---------------- quadratic-approx
quad = lambda fn: sp.series(fn, x, 0, 3).removeO()
same(quad(sp.cos(x)), 1 - x**2 / 2); same(quad(sp.exp(x)), 1 + x + x**2 / 2); same(quad(sp.sin(x)), x)
add([at(sp.log(1 + x), x, 0), at(D(sp.log(1 + x)), x, 0), at(D(sp.log(1 + x), x, 2), x, 0)], [0, 1, -1])
ANSWERS["quadratic-approx/ln11"] = 0.1 - 0.01 / 2; add(round(math.log(1.1), 5), 0.09531)
ANSWERS["quadratic-approx/sqrt-coef"] = float(coef(sp.sqrt(1 + x), 2)); add(at(D(sp.sqrt(1 + x), x, 2), x, 0), sp.Rational(-1, 4))
add(1 + 0.05 - 0.00125, 1.04875, 1e-12); add(round(math.sqrt(1.1), 6), 1.048809)
same(quad(sp.log(1 + x)), x - x**2 / 2); same(quad((1 + x)**r_), 1 + r_ * x + r_ * (r_ - 1) / 2 * x**2)
ANSWERS["quadratic-approx/e01"] = 1 + 0.1 + 0.005; add(round(math.exp(0.1), 7), 1.1051709)
same(quad(sp.exp(-3 * x)), 1 - 3 * x + sp.Rational(9, 2) * x**2); same(quad((1 + x)**sp.Rational(-1, 2)), 1 - x / 2 + sp.Rational(3, 8) * x**2)
add(sp.Rational(3, 8) + sp.Rational(3, 2) + sp.Rational(9, 2), sp.Rational(51, 8))
same(quad(sp.exp(-3 * x) * (1 + x)**sp.Rational(-1, 2)), 1 - sp.Rational(7, 2) * x + sp.Rational(51, 8) * x**2)
ANSWERS["quadratic-approx/excos"] = coef(sp.exp(x) * sp.cos(x), 2)
add(1 + 1 + 0.5, 2.5, 1e-12); add(round(math.exp(0.1) - 1.105, 5), 0.00017)

# ---------------- taylor-poly
X = sp.symbols("X")
P = lambda fn, k, a0=0: sum(at(D(fn, x, j), x, a0) / sp.factorial(j) * (X - a0)**j for j in range(k + 1))
ANSWERS["taylor-poly/p3-at-1"] = float(P(sp.exp(x), 3).subs(X, 1)); add(P(sp.exp(x), 3).subs(X, 1), sp.Rational(8, 3))
terr = lambda name, k, xv: abs(sum({"exp": 1 / math.factorial(j), "sin": (0 if j % 2 == 0 else (-1)**((j - 1) // 2) / math.factorial(j)), "cos": (0 if j % 2 else (-1)**(j // 2) / math.factorial(j))}[name] * xv**j for j in range(k + 1)) - {"exp": math.exp, "sin": math.sin, "cos": math.cos}[name](xv))
add(round(terr("exp", 5, 1), 4), 0.0016); add(round(terr("exp", 6, 1), 5), 0.00023); add(terr("exp", 6, 1) < 0.001 < terr("exp", 5, 1), True)
add([at(D(sp.sin(x), x, k), x, 0) for k in range(6)], [0, 1, 0, -1, 0, 1])
ANSWERS["taylor-poly/sin-x5"] = float(coef(sp.sin(x), 5)); add(coef(sp.sin(x), 5), sp.Rational(1, 120))
same(sp.series(sp.cos(x), x, 0, 6).removeO(), 1 - x**2 / 2 + x**4 / 24)
add(round(terr("sin", 7, 2), 4), 0.0014); add(round(terr("sin", 8, 2), 4), 0.0014); add(round(terr("sin", 9, 2), 5), 0.00005)
add(terr("sin", 9, 2) < 0.001 < terr("sin", 8, 2), True)
pp = 3 * x**3 + 4 * x**2 - 2 * x + 1
add([at(D(pp, x, k), x, 0) for k in range(5)], [1, -2, 8, 18, 0]); same(P(pp, 3).subs(X, x), pp)
q3 = x**3 + 2 * x + 1; add([at(D(q3, x, k), x, 1) for k in range(3)], [4, 5, 6]); same(P(q3, 2, 1), 4 + 5 * (X - 1) + 3 * (X - 1)**2)
same(P(sp.log(x), 2, 1), (X - 1) - (X - 1)**2 / 2); ANSWERS["taylor-poly/ln-at-1"] = 0.2 - 0.5 * 0.04; add(round(math.log(1.2), 5), 0.18232)

# ---------------- remainder
p3 = 1 + 0.1 + 0.01 / 2 + 0.001 / 6
add(round(p3, 7), 1.1051667); add(round(math.exp(0.1), 7), 1.1051709); add(round(math.exp(0.1) - p3, 7), 0.0000043)
add(at(q3, x, 3), 34); add(P(q3, 2, 1).subs(X, 3), 26); ANSWERS["remainder/cubic-rem"] = at(q3, x, 3) - P(q3, 2, 1).subs(X, 3)
add(sp.Rational(6, 6) * 2**3, 8)
add(round(1.2 * 0.1**4 / 24, 12), 5e-6); add(math.exp(0.1) < 1.2, True)
ANSWERS["remainder/p1-bound"] = 1.2 / 2 * 0.1**2; add(round(math.exp(0.1) - 1.1, 5), 0.00517)
ANSWERS["remainder/sin-bound"] = 0.5**5 / 120; add(round(0.5**5 / 120, 5), 0.00026); add(round(abs(math.sin(0.5) - (0.5 - 0.5**3 / 6)), 6), 0.000259)
add(round(0.5**4 / 24, 4), 0.0026)
seq = [10**(k + 1) / math.factorial(k + 1) for k in range(60)]; add(seq[-1] < 1e-20, True); add(seq[10] > seq[0], True)

# ---------------- lhopital
ANSWERS["lhopital/guess"] = lim((sp.exp(x) - 1) / x, 0)
ANSWERS["lhopital/sin3x"] = lim(sp.sin(3 * x) / x, 0)
add(lim((sp.exp(x) - x - 1) / x**2, 0), sp.Rational(1, 2)); add(lim((sp.exp(x) - 1) / (2 * x), 0), sp.Rational(1, 2))
ANSWERS["lhopital/x-sin"] = float(lim((x - sp.sin(x)) / x**3, 0))
ANSWERS["lhopital/cos-x2"] = float(lim((1 - sp.cos(x)) / x**2, 0))
add(at((x**2 + 5) / (3 * x + 4), x, 1), sp.Rational(6, 7)); add(at(2 * x / 3, x, 1), sp.Rational(2, 3))
add(lim(sp.sin(x) / sp.exp(x), 0), 0)
ANSWERS["lhopital/inf-inf"] = lim(x**2 / sp.exp(x), sp.oo)
add(sp.limit(x * sp.log(x), x, 0, dir="+"), 0)
ANSWERS["lhopital/x-root-x"] = lim(x**(1 / x), sp.oo); add(lim(sp.log(x) / x, sp.oo), 0)

# ---------------- taylor-limits
same(sp.series(sp.sin(x) - x, x, 0, 4).removeO(), -x**3 / 6)
same(sp.series(sp.exp(x), x, 0, 4).removeO(), 1 + x + x**2 / 2 + x**3 / 6)
same(sp.series(sp.sin(x), x, 0, 4).removeO(), x - x**3 / 6); same(sp.series(sp.cos(x), x, 0, 5).removeO(), 1 - x**2 / 2 + x**4 / 24)
same(sp.series(sp.log(1 + x), x, 0, 3).removeO(), x - x**2 / 2)
ANSWERS["taylor-limits/ln-lim"] = float(lim((sp.log(1 + x) - x) / x**2, 0))
same(sp.series(sp.exp(x) * sp.sin(x), x, 0, 4).removeO(), x + x**2 + x**3 / 3); add(lim((sp.exp(x) * sp.sin(x) - x - x**2) / x**3, 0), sp.Rational(1, 3))
ANSWERS["taylor-limits/cos4"] = float(lim((sp.cos(x) - 1 + x**2 / 2) / x**4, 0))
ANSWERS["taylor-limits/e3"] = float(lim((sp.exp(x) - 1 - x - x**2 / 2) / x**3, 0))
add(at(D(sp.tan(x), x, 3), x, 0), 2); same(sp.series(sp.tan(x), x, 0, 4).removeO(), x + x**3 / 3)
add(lim((sp.tan(x) - sp.sin(x)) / x**3, 0), sp.Rational(1, 2)); add(sp.Rational(1, 3) + sp.Rational(1, 6), sp.Rational(1, 2))
add(lim((sp.sin(x) - x) / x**3, 0), sp.Rational(-1, 6)); add(lim(sp.tan(x) / x, 0), 1)

# ---------------- power-series
ANSWERS["power-series/guess"] = sp.summation(sp.Rational(1, 2)**n, (n, 0, sp.oo))
ANSWERS["power-series/third"] = float(sp.summation(sp.Rational(1, 3)**n, (n, 0, sp.oo)))
k_ = sp.symbols("k", integer=True, nonnegative=True)
same(sp.summation(x**k_, (k_, 0, 5)), (1 - x**6) / (1 - x))
add([sum(2**j for j in range(m + 1)) for m in range(4)], [1, 3, 7, 15])
ratio = lambda an: sp.limit(sp.Abs(an.subs(n, n + 1) / an), n, sp.oo)   # |a_{n+1}/a_n| -> 1/R
add(ratio(1 / n), 1); add(ratio(sp.Rational(1, 2)**n), sp.Rational(1, 2)); add(ratio(1 / sp.factorial(n)), 0)
ANSWERS["power-series/r3"] = 1 / ratio(sp.Rational(1, 3)**n); ANSWERS["power-series/rn"] = 1 / ratio(n)

# ---------------- taylor-series
ANSWERS["taylor-series/guess"] = sum(1 / math.factorial(j) for j in range(6)); add(round(sum(1 / math.factorial(j) for j in range(6)), 5), 2.71667)
e8 = sum(1 / math.factorial(j) for j in range(8)); ANSWERS["taylor-series/e-sum"] = round(e8, 5)
add(round(e8, 6), 2.718254); add(round(1 / 720, 6), 0.001389); add(round(1 / 5040, 6), 0.000198); add(round(math.e - e8, 5), 0.00003)
add(round(terr("cos", 8, 3), 3), 0.015); add(round(terr("cos", 10, 3), 3), 0.001); add(terr("cos", 10, 3) < 0.01 < terr("cos", 8, 3), True)
same(sp.series(1 / (1 + x), x, 0, 6).removeO(), 1 - x + x**2 - x**3 + x**4 - x**5)
add([sum((-1)**j for j in range(m + 1)) for m in range(4)], [1, 0, 1, 0]); add(at(1 / (1 + x), x, 1), sp.Rational(1, 2))
xpos = sp.symbols("xpos", positive=True); bump = sp.exp(-1 / xpos**2)
add([sp.limit(sp.diff(bump, xpos, k), xpos, 0, dir="+") for k in range(4)], [0, 0, 0, 0])
same(D(sp.sec(x)), sp.sec(x) * sp.tan(x)); same(D(sp.sec(x), x, 2), sp.sec(x) * sp.tan(x)**2 + sp.sec(x)**3)
add(at(D(sp.sec(x), x, 2), x, 0), 1); ANSWERS["taylor-series/sec-coef"] = float(coef(sp.sec(x), 2))
add([coef(sp.sin(x), k) for k in (0, 2, 4)], [0, 0, 0]); add([coef(sp.cos(x), k) for k in (1, 3, 5)], [0, 0, 0])

# ---------------- series-ops
same(sp.series(x * sp.sin(x), x, 0, 6).removeO(), x**2 - x**4 / 6)
same(sp.series(sp.exp(-x**2), x, 0, 8).removeO(), 1 - x**2 + x**4 / 2 - x**6 / 6); ANSWERS["series-ops/ex2-coef"] = float(coef(sp.exp(-x**2), 4))
same(sp.series(1 / (1 + 25 * x**2), x, 0, 5).removeO(), 1 - 25 * x**2 + 625 * x**4)
xr = sp.symbols("xr", positive=True); add(sp.solve(25 * xr**2 - 1, xr), [sp.Rational(1, 5)])
ANSWERS["series-ops/r-sub"] = float(sp.solve(4 * xr**2 - 1, xr)[0]); same(sp.series(1 / (1 + 4 * x**2), x, 0, 5).removeO(), 1 - 4 * x**2 + 16 * x**4)
add([F(3, math.factorial(3)), F(5, math.factorial(5))], [F(1, math.factorial(2)), F(1, math.factorial(4))])
same(sp.diff(sp.series(sp.sin(x), x, 0, 10).removeO(), x), sp.series(sp.cos(x), x, 0, 9).removeO())
same(sp.series(1 / (1 - x)**2, x, 0, 5).removeO(), 1 + 2 * x + 3 * x**2 + 4 * x**3 + 5 * x**4)
ANSWERS["series-ops/sum-n"] = sp.summation((n + 1) * sp.Rational(1, 2)**n, (n, 0, sp.oo))
same(sp.series(sp.log(1 + x), x, 0, 5).removeO(), x - x**2 / 2 + x**3 / 3 - x**4 / 4)
same(sp.integrate(1 - t + t**2 - t**3, (t, 0, x)), x - x**2 / 2 + x**3 / 3 - x**4 / 4)   # "reverse" of term-by-term differentiation
ANSWERS["series-ops/ln11-3"] = round(0.1 - 0.01 / 2 + 0.001 / 3, 5); add(round(0.1 - 0.005 + 0.001 / 3, 6), 0.095333); add(round(math.log(1.1), 7), 0.0953102)
same(sp.series(1 / (1 + x**2), x, 0, 7).removeO(), 1 - x**2 + x**4 - x**6)
same(sp.series(sp.atan(x), x, 0, 8).removeO(), x - x**3 / 3 + x**5 / 5 - x**7 / 7); ANSWERS["series-ops/atan-x7"] = float(coef(sp.atan(x), 7))
ANSWERS["series-ops/atan5x"] = float(coef(sp.atan(5 * x), 3)); add(coef(sp.atan(5 * x), 3), sp.Rational(-125, 3))

# ---------------- boss
same(D(x**3 * sp.exp(2 * x)), x**2 * (2 * x + 3) * sp.exp(2 * x))
ANSWERS["boss/d-ln"] = at(D(sp.log(1 + x**2)), x, 1)
same(D(sp.sin(x**2)), 2 * x * sp.cos(x**2))
ANSWERS["boss/implicit-boss"] = float(idiff(circ).subs({x: 4, y: 3}))
ANSWERS["boss/max-boss"] = at(m, x, -1)
ANSWERS["boss/mvt-boss"] = ANSWERS["mvt/x2-13"]
ANSWERS["boss/dy-boss"] = 10 + 1 / (2 * 10)
ANSWERS["boss/p3-boss"] = round(p3, 6)
ANSWERS["boss/rem-boss"] = 1.2 * 0.1**4 / 24
ANSWERS["boss/lim-boss"] = float(lim((x - sp.sin(x)) / x**3, 0))

# ---------------- rounded values shown in cards and explanations (value, as written, decimals)
for val, shown, dp in [(0.001 / 6, 0.000167, 6), (0.001 / 3, 0.000333, 6), (0.5**5, 0.03125, 5), (0.6**2, 0.36, 2), (1 - 0.36, 0.64, 2),
                       (math.sqrt(0.64), 0.8, 1), (1 + math.log(2), 1.6931, 4), (math.pi, 3.1416, 4), (math.exp(0.1) - p3, 4.3e-6, 7),
                       (math.e, 2.718282, 6), (1 / 9, 0.111, 3), (1 / 12, 0.0833, 4), (1 / 120, 0.008333, 6), (1 / 24, 0.0417, 4),
                       (1 / math.sqrt(2), 0.707, 3), (math.pi / 4, 0.785, 3), (2 / math.sqrt(3), 1.155, 3), (math.sqrt(3), 1.732, 3),
                       (2 * math.pi, 6.283, 3), (5 * math.e**2, 36.95, 2), (8 * math.log(2), 5.545, 3), (4 * (1 + math.log(2)), 6.773, 3),
                       (math.pi + math.pi * math.log(math.pi), 6.738, 3), (125 / 3, 41.67, 2), (1 / 7, 0.143, 3), (sum(1 / math.factorial(j) for j in range(6)), 2.716667, 6),
                       (30 / 8, 3.75, 2)]:
    add(round(val, dp), shown, 1e-12)

# ---------------- every graded number item in the pack has the value computed above
pack = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "content", "M.1.2.yaml")
items, lesson, cur, in_boss, typ = {}, None, None, False, None
for line in open(pack, encoding="utf8"):
    if line.startswith("boss:"): in_boss, lesson = True, "boss"
    m_ = re.match(r"^  - id: (\S+)$", line)
    if m_ and not in_boss: lesson = m_.group(1)
    m_ = re.match(r"^(?: {10}| {4}- )id: (\S+)$", line)
    if m_: cur = f"{lesson}/{m_.group(1)}"; items[cur] = {}
    m_ = re.match(r"^\s+(type|answer|tolerance): (\S+)$", line)
    if m_ and cur: items[cur].setdefault(m_.group(1), m_.group(2))
numbers = {k: v for k, v in items.items() if v.get("type") == "number"}
for k, v in numbers.items():
    line = inspect.stack()[0].lineno
    if k not in ANSWERS:
        checks.append((False, k, "a computed value in ANSWERS", line)); continue
    ans, tol = float(v["answer"]), float(v.get("tolerance", max(1e-9, abs(float(v["answer"])) * 1e-6)))
    checks.append((abs(ans - float(ANSWERS[k])) <= tol, f"{k} = {v['answer']}", float(ANSWERS[k]), line))
for k in ANSWERS:
    if k not in numbers: checks.append((False, k, "a number item in the pack", inspect.stack()[0].lineno))

bad = [(ln, g, wv) for (ok, g, wv, ln) in checks if not ok]
for i, g, wv in bad:
    print(f"line {i}: got {g!r}, want {wv!r}")
print(f"{len(checks) - len(bad)}/{len(checks)} claims hold ({len(numbers)} number items compared with the pack)")
sys.exit(1 if bad else 0)
