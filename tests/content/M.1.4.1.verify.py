# Checks every number data/content/M.1.4.1.yaml states. Partial derivatives, Jacobians, Hessians,
# implicit derivatives, critical points and Lagrange systems are recomputed with sympy from the functions
# the lessons use; values, approximations and error bounds with floats; the two sims (gradient descent,
# matrix2d) at their solutions. Every graded number item's `answer` is read from the pack and compared with
# the value computed here (ANSWERS); the run fails if a number item has no computed value or they disagree.
# Card and option claims are checked inline with add()/same().
# usage: .venv/Scripts/python.exe -I tests/content/M.1.4.1.verify.py   (needs sympy and pyyaml; prints
# "N/N claims hold", exit code 1 on any mismatch). The .venv is made as described in tests/content/M.1.1.verify.py.
import inspect, math, os, sys
import sympy as sp
import yaml

x, y, z, t, u, v, r, th, rho, ph, h, k = sp.symbols("x y z t u v r theta rho phi h k", real=True)
checks = []
def add(got, want, tol=1e-9):
    line = inspect.stack()[1].lineno
    try:
        ok = abs(float(got) - float(want)) <= tol
    except (TypeError, ValueError):
        ok = got == want or sp.simplify(sp.sympify(got) - sp.sympify(want)) == 0
    checks.append((bool(ok), got, want, line))
def same(e1, e2):
    line = inspect.stack()[1].lineno
    checks.append((sp.simplify(sp.expand(e1 - e2)) == 0, e1, e2, line))
D = sp.diff
def at(e, **kw):
    return e.subs({sp.Symbol(n, real=True): val for n, val in kw.items()})
def grad(f, vs): return sp.Matrix([D(f, s) for s in vs])
def hess(f, vs): return sp.hessian(f, vs)
def jac(F, vs): return sp.Matrix(F).jacobian(vs)
ANSWERS = {}

# ================= Chapter 1: partial derivatives
f = x**2 + 3*x*y
add(at(f, x=1, y=2), 7)
ANSWERS["two-var-functions/eval-two-var"] = at(f, x=2, y=-1)
same(D(f.subs(y, 2), x), 2*x + 6); add(at(D(f.subs(y, 2), x), x=1), 8)
same(D(f, x), 2*x + 3*y)                                   # fx-rule
ANSWERS["two-var-functions/fy-value"] = at(D(f, y), x=1, y=2)
add((at(f, x=1.1, y=2) - at(f, x=1, y=2)) / 0.1, 8.1, 1e-9); add(at(f, x=1.1, y=2), 7.81, 1e-12)
ANSWERS["two-var-functions/diff-quotient"] = (at(f, x=1.01, y=2) - at(f, x=1, y=2)) / 0.01
add(at(f, x=1.01, y=2), 7.0801, 1e-12)
add(at(D(4 - x**2 - y**2, x), x=1, y=1), -2); add(at(D(4 - x**2 - y**2, y), x=1, y=1), -2)
w_, hh = sp.symbols("w hh", positive=True)
ANSWERS["two-var-functions/area-rate"] = D(w_*hh, w_).subs({w_: 5, hh: 3})
# partial-rules
same(D(sp.sin(x*y), x), y*sp.cos(x*y))
same(D(sp.exp(x*y), x), y*sp.exp(x*y)); same(D(sp.exp(x*y), y), x*sp.exp(x*y)); same(D(x/y, y), -x/y**2)
ANSWERS["partial-rules/exp-chain"] = float(at(D(sp.exp(x**2*y), x), x=1, y=1))
same(D(x/(x + y), y), -x/(x + y)**2)
f = x**2*y + y*z**3
same(D(f, x), 2*x*y); same(D(f, y), x**2 + z**3); same(D(f, z), 3*y*z**2)
add(tuple(at(grad(f, [x, y, z]), x=1, y=2, z=1)), (4, 2, 6))
g = sp.log(x**2 + y*z)
add(tuple(at(grad(g, [x, y, z]), x=1, y=2, z=3)), (sp.Rational(2, 7), sp.Rational(3, 7), sp.Rational(2, 7)))
ANSWERS["partial-rules/three-var-half"] = at(D(x*y*z + z**2, z), x=1, y=2, z=3)
for fun, dy in [(x**3*y**2, 2*x**3*y), (x*sp.sin(y), x*sp.cos(y)), (sp.exp(x + 2*y), 2*sp.exp(x + 2*y))]:
    same(D(fun, y), dy)
xp, yp = sp.symbols("xp yp", positive=True); same(D(sp.log(xp*yp), yp), 1/yp)
T, V = sp.symbols("T V", positive=True); P = sp.Rational(821, 10000)*T/V
ANSWERS["partial-rules/gas-dv"] = float(D(P, V).subs({T: 300, V: 10}))
ANSWERS["partial-rules/gas-dt"] = float(D(P, T).subs({T: 300, V: 10}))
# mixed-partials
f = x**3*y**2
same(D(f, x, y), 6*x**2*y); same(D(f, y, x), 6*x**2*y)
f = x**3*y**2 - 2*x*y
same(D(f, x), 3*x**2*y**2 - 2*y); same(D(f, y), 2*x**3*y - 2*x)
same(D(f, x, x), 6*x*y**2); same(D(f, x, y), 6*x**2*y - 2); same(D(f, y, x), 6*x**2*y - 2); same(D(f, y, y), 2*x**3)
ANSWERS["mixed-partials/fxx-value"] = at(D(f, x, x), x=1, y=2)
ANSWERS["mixed-partials/clairaut-use"] = at(6*x**2*y - 2, x=1, y=1)
# the counterexample xy(x^2 - y^2)/(x^2 + y^2): f_xy(0,0) = -1, f_yx(0,0) = 1 from the definitions
fc = x*y*(x**2 - y**2)/(x**2 + y**2)
fx_on_yaxis = sp.limit((fc.subs(x, h) - 0)/h, h, 0)          # f_x(0, y) for y != 0 (f(0, y) = 0)
fy_on_xaxis = sp.limit((fc.subs(y, h) - 0)/h, h, 0)          # f_y(x, 0)
add(sp.limit(fx_on_yaxis/y, y, 0), -1)   # f_xy(0,0) = d/dy f_x(0, y) at 0, f_x(0,0) = 0
add(sp.limit(fy_on_xaxis/x, x, 0), 1)    # f_yx(0,0)
f = x**2*y + sp.exp(x*y)
same(D(f, x, y), 2*x + sp.exp(x*y) + x*y*sp.exp(x*y))
add(at(D(f, x, y), x=1, y=0), 3)
ANSWERS["mixed-partials/fxy-exp"] = float(at(D(f, x, y), x=1, y=1))
ANSWERS["mixed-partials/third-order"] = at(D(x**4*y**3, x, x, y), x=1, y=1)
same(D(x**4*y**3, x, x, y), D(x**4*y**3, y, x, x))
# pde-check
add(D(sp.exp(2*x), x) - 2*sp.exp(2*x), 0)
ANSWERS["pde-check/ode-k"] = sp.solve(sp.Eq(k, 5), k)[0]
uu = sp.exp(-t)*sp.sin(x); same(D(uu, t), D(uu, x, 2))
uu = sp.exp(-18*t)*sp.sin(3*x); ANSWERS["pde-check/heat-alpha"] = sp.simplify(D(uu, t)/D(uu, x, 2))
lap = lambda e: sp.simplify(D(e, x, 2) + D(e, y, 2))
add(lap(x**2 - y**2), 0); add(lap(x**2 + y**2), 4); add(lap(sp.exp(x)*sp.sin(y)), 0)
for good in [x*y, x**3 - 3*x*y**2, sp.exp(x)*sp.cos(y)]: add(lap(good), 0)
add(lap(x**3), 6*x)
uu = sp.sin(x - 2*t); same(D(uu, t, 2), 4*D(uu, x, 2))
uu = sp.cos(2*x + 6*t); ANSWERS["pde-check/wave-c2"] = sp.simplify(D(uu, t, 2)/D(uu, x, 2))
uu = sp.log(x**2 + y**2)
same(D(uu, x, 2), 2*(y**2 - x**2)/(x**2 + y**2)**2); add(lap(uu), 0)
ANSWERS["pde-check/uxx-ln"] = at(D(uu, x, 2), x=1, y=0)
add(at(D(uu, y, 2), x=1, y=0), 2)
uu = 5*sp.sin(3*sp.pi*x)*sp.sin(4*sp.pi*y)*sp.cos(10*sp.pi*t); same(D(uu, t, 2), 4*(D(uu, x, 2) + D(uu, y, 2)))

# ================= Chapter 2: tangent planes, differentiability, differentials
def plane(f, a, b):
    return at(f, x=a, y=b) + at(D(f, x), x=a, y=b)*(x - a) + at(D(f, y), x=a, y=b)*(y - b)
same(plane(x**2 + y**2, 1, 2), 2*x + 4*y - 5)
ANSWERS["tangent-plane/plane-const"] = sp.expand(plane(x**2 + y**2, 2, 1)).subs({x: 0, y: 0})
same(plane(x**2 + y**2, 2, 1), 4*x + 2*y - 5)
f = x**2*y - y**3
add(at(f, x=2, y=1), 3); add(at(D(f, x), x=2, y=1), 4); add(at(D(f, y), x=2, y=1), 1); same(plane(f, 2, 1), 4*x + y - 6)
same(plane(sp.exp(x)*sp.cos(y), 0, 0), 1 + x)
ANSWERS["tangent-plane/plane-read"] = -1   # read off the given plane z = 3 + 2(x − 1) − (y − 4)
# linear-approx
f = x**2 + y**2; L = plane(f, 1, 2)
add(at(L, x=1.1, y=2.1), 5.6, 1e-12)                       # guess
add(5 + 0.2, 5.2, 1e-12); add(5 + 2 + 4, 11)                # the two distractors' recipes
f = x**2*y; ANSWERS["linear-approx/approx-x2y"] = float(at(plane(f, 2, 3), x=2.01, y=2.98))
add(at(f, x=2.01, y=2.98), 12.039498, 1e-9)
f = x**2 + y**2
add(at(plane(f, 1, 2), x=1.02, y=1.97), 4.92, 1e-12); add(at(f, x=1.02, y=1.97), 4.9213, 1e-12)
add(at(f, x=1.02, y=1.97) - at(plane(f, 1, 2), x=1.02, y=1.97), 0.0013, 1e-12)
f = sp.sqrt(x**2 + y**2)
add(at(D(f, x), x=3, y=4), sp.Rational(3, 5)); add(at(D(f, y), x=3, y=4), sp.Rational(4, 5)); same(D(f, x), x/f)
ANSWERS["linear-approx/approx-sqrt"] = float(at(plane(f, 3, 4), x=3.06, y=3.92))
add(at(f, x=3.06, y=3.92), 4.97293, 1e-5)
f = sp.sqrt(41 - 4*x**2 - y**2)
add(at(f, x=2, y=3), 4); add(at(D(f, x), x=2, y=3), -2); add(at(D(f, y), x=2, y=3), sp.Rational(-3, 4))
ANSWERS["linear-approx/approx-ostax"] = float(at(plane(f, 2, 3), x=2.1, y=2.9))
add(at(f, x=2.1, y=2.9), math.sqrt(14.95), 1e-12); add(math.sqrt(14.95), 3.8665, 1e-4)
add(abs(3.875 - math.sqrt(14.95))/math.sqrt(14.95)*100, 0.2, 0.05)
Vc = sp.pi*r**2*h
Lc = at(Vc, r=2, h=5) + at(D(Vc, r), r=2, h=5)*(r - 2) + at(D(Vc, h), r=2, h=5)*(h - 5)
ANSWERS["linear-approx/approx-cylinder"] = float(at(Lc, r=2.05, h=4.9))
add(at(Lc, r=2.05, h=4.9), sp.Rational(206, 10)*sp.pi); add(at(Vc, r=2.05, h=4.9), 64.69, 0.01)
f = x**2 + y**2
for pt, err in [((1.01, 2.01), 0.0002), ((1.5, 2.5), 0.5), ((3, 4), 8)]:
    add(at(f, x=pt[0], y=pt[1]) - at(plane(f, 1, 2), x=pt[0], y=pt[1]), err, 1e-12)
add(at(plane(f, 1, 2), x=3, y=4), 17)
# differentiability
f = 2*x**2 - 4*y; P0 = plane(f, 2, -3)
same(P0, 20 + 8*(x - 2) - 4*(y + 3)); same(f - P0, 2*(x - 2)**2)
ANSWERS["differentiability/error-term"] = float(at(f - P0, x=2.1, y=-3))
add(at(f, x=2.1, y=-3), 20.82, 1e-12)
fo = x*y/sp.sqrt(x**2 + y**2)
xs = sp.symbols("xs", positive=True)
same(fo.subs({x: xs, y: xs}), xs/sp.sqrt(2))
dist = sp.sqrt(2)*xs; same(fo.subs({x: xs, y: xs})/dist, sp.Rational(1, 2))
ANSWERS["differentiability/diag-ratio"] = float(at(fo, x=0.01, y=0.01)/math.sqrt(2*0.01**2))
add(sp.limit(fo.subs(y, 0)/x, x, 0), 0)                    # f_x(0,0) = 0 (diag-partial)
add(sp.limit(fo.subs({x: h/sp.sqrt(2), y: h/sp.sqrt(2)})/h, h, 0, "+"), sp.Rational(1, 2))  # gradient card: ∇f(0,0)=0 yet D_u f = 1/2
add(-math.sqrt(52)*4, -28.84, 0.005)                        # abs-circle: min of 4x − 6y on radius 4
add(sp.limit(fo.subs({y: x}), x, 0), 0)                    # continuous along the diagonal at the origin
f = x*y*z
L3 = 6 + 6*(x - 1) + 3*(y - 2) + 2*(z - 3)
add(tuple(at(grad(f, [x, y, z]), x=1, y=2, z=3)), (6, 3, 2))
ANSWERS["differentiability/three-var-approx"] = float(at(L3, x=1.1, y=2, z=2.9)); add(at(f, x=1.1, y=2, z=2.9), 6.38, 1e-12)
same(D(x**3 - 2*x*y + y**4, x), 3*x**2 - 2*y); same(D(x**3 - 2*x*y + y**4, y), -2*x + 4*y**3)
# total-differential
add(5*0.1 + 10*0.1, 1.5, 1e-12); add(0.1*0.1, 0.01, 1e-12)
ANSWERS["total-differential/dz-basic"] = 2*1*0.02 + 2*2*(-0.03)
f = x**2*y
dz = at(D(f, x), x=2, y=3)*0.1 + at(D(f, y), x=2, y=3)*(-0.1); add(dz, 0.8, 1e-12)
add(at(f, x=2.1, y=2.9), 12.789, 1e-12); add(at(f, x=2.1, y=2.9) - 12, 0.789, 1e-12); add(0.8 - 0.789, 0.011, 1e-12)
f = 3*x**2 - 2*x*y + y**2
add(at(f, x=2, y=-3), 33); add(at(D(f, x), x=2, y=-3), 18); add(at(D(f, y), x=2, y=-3), -10)
ANSWERS["total-differential/delta-vs-d"] = float(at(D(f, x), x=2, y=-3)*0.1 + at(D(f, y), x=2, y=-3)*(-0.05))
add(at(f, x=2.1, y=-3.05) - at(f, x=2, y=-3), 2.3425, 1e-12)
ANSWERS["total-differential/cylinder-error"] = float(at(abs(D(Vc, r)), r=2, h=5)*0.05 + at(abs(D(Vc, h)), r=2, h=5)*0.1)
add(ANSWERS["total-differential/cylinder-error"], 1.4*math.pi, 1e-12)
ANSWERS["total-differential/relative-error"] = 100*(0.01 + 0.01)
same(D(x*y*z, x), y*z); same(D(x*y*z, y), x*z); same(D(x*y*z, z), x*y)

# ================= Chapter 3: directional derivatives
add(3/math.sqrt(2) + 4/math.sqrt(2), 4.95, 0.005); add(3*0.707 + 4*0.707, 4.949, 1e-9)
ANSWERS["directional/dir-angle"] = 3*math.cos(math.pi/3) + 4*math.sin(math.pi/3)
f = x**2 + x*y
add(at(D(f, x), x=1, y=2), 4); add(at(D(f, y), x=1, y=2), 1); add(4*0.6 + 1*0.8, 3.2, 1e-12); add(4*3 + 1*4, 16); add(16/5, 3.2, 1e-12)
f = x**2 + y**2
ANSWERS["directional/dir-zero"] = float((at(D(f, x), x=1, y=1) - at(D(f, y), x=1, y=1))/math.sqrt(2))
f = 100 - x**2 - 2*y**2
ANSWERS["directional/dir-temp"] = float(at(D(f, x), x=3, y=1)*(-1) + at(D(f, y), x=3, y=1)*0)
f = x**2 - x*y + 3*y**2
ANSWERS["directional/dir-limit"] = float(at(D(f, x), x=-1, y=2)*0.6 + at(D(f, y), x=-1, y=2)*0.8)
# the definition gives the same as the formula
add(sp.limit((at(f, x=-1 + h*sp.Rational(3, 5), y=2 + h*sp.Rational(4, 5)) - at(f, x=-1, y=2))/h, h, 0), 8)
# directional-3d
ANSWERS["directional-3d/dir3-unit"] = 1/3
f = x**2*y + y*z**3; gf = at(grad(f, [x, y, z]), x=1, y=2, z=1)
add(gf.dot(sp.Matrix([1, 2, 2]))/3, sp.Rational(20, 3))
ANSWERS["directional-3d/dir3-half"] = gf.dot(sp.Matrix([2, -1, 2]))/3
f = 5*x**2 - 2*x*y + y**2 - 4*y*z + z**2 + 3*x*z; gf = at(grad(f, [x, y, z]), x=1, y=-2, z=3)
add(tuple(gf), (23, -18, 17))
ANSWERS["directional-3d/dir3-ostax"] = float(gf.dot(sp.Matrix([-1, 2, 2]))/3)
ANSWERS["directional-3d/dir3-reverse"] = -20/3
add(math.sqrt(3), 1.7320508, 1e-6)                         # dir3-flat: D along (1,1,1)/√3 is √3

# ================= Chapter 4: implicit and inverse function theorems
add(at(sp.idiff(x**2 + y**2 - 25, y, x), x=3, y=4), sp.Rational(-3, 4))   # guess (choice): about −0.75; −4/3 is x, y swapped
same(sp.idiff(x**2 + 3*y**2 + 4*y - 4, y, x), -x/(3*y + 2))
F_ = x**3 + y**3 - 6*x*y; add(at(D(F_, x), x=3, y=3), 9); add(at(D(F_, y), x=3, y=3), 9); add(at(sp.idiff(F_, y, x), x=3, y=3), -1)
F_ = x**2 + x*y + y**2 - 7; add(at(F_, x=1, y=2), 0)
ANSWERS["implicit-diff/implicit-ellipse"] = float(at(-D(F_, x)/D(F_, y), x=1, y=2))
F_ = x**2 + y**2 + z**2 - 3; add(at(-D(F_, x)/D(F_, z), x=1, y=1, z=1), -1); add(at(-D(F_, y)/D(F_, z), x=1, y=1, z=1), -1)
F_ = x**2 + 2*y**2 + 3*z**2 - 6; add(at(F_, x=1, y=1, z=1), 0)
ANSWERS["implicit-diff/implicit-3d"] = float(at(-D(F_, y)/D(F_, z), x=1, y=1, z=1))
F_ = x*y*z + z**2 - 3; add(at(F_, x=1, y=2, z=1), 0)
ANSWERS["implicit-diff/implicit-3d-x"] = float(at(-D(F_, x)/D(F_, z), x=1, y=2, z=1))
add(at(D(x**2 + y**2 - 25, y), x=5, y=0), 0)
# implicit-theorem: F_y = 2y vanishes only at (±1, 0) on the unit circle; the option points lie on it
for pt in [(0, 1), (0.6, -0.8), (-0.6, 0.8), (1, 0), (-1, 0)]: add(pt[0]**2 + pt[1]**2, 1, 1e-12)
add(sp.real_root(x, 3)**3, x)
Fs, Gs = x**2 + y**2 + z**2 - 3, z - 1
ANSWERS["implicit-theorem/ift-two-eq"] = at(jac([Fs, Gs], [y, z]).det(), x=1, y=1, z=1)
add(at(Fs.subs(z, 1), x=1, y=1), 0)
Gp = x + y + z - 3; add(at(jac([Fs, Gp], [y, z]).det(), x=1, y=1, z=1), 0)
# sphere x²+y²+z²=3 and plane x+y+z=3 meet only at (1,1,1): distance from origin to plane = √3 = radius
add(3/math.sqrt(3), math.sqrt(3), 1e-12)
# inverse-theorem
Fm = [x**2 - y**2, 2*x*y]; same(jac(Fm, [x, y]).det(), 4*x**2 + 4*y**2)
ANSWERS["inverse-theorem/inv-det"] = at(jac(Fm, [x, y]).det(), x=1, y=1)
same(jac([r*sp.cos(th), r*sp.sin(th)], [r, th]).det(), r)
ANSWERS["inverse-theorem/inv-polar-det"] = sp.simplify(jac([r*sp.cos(th), r*sp.sin(th)], [r, th]).det()).subs({r: 2, th: sp.pi/6})
J = jac([x + y, x*y], [x, y])
add(at(J, x=2, y=1).det(), 1); add(at(J, x=2, y=1).inv(), sp.Matrix([[2, -1], [-1, 1]]))
Ue, Ve = sp.symbols("Ue Ve", positive=True)
xbig = (Ue + sp.sqrt(Ue**2 - 4*Ve))/2; ysmall = (Ue - sp.sqrt(Ue**2 - 4*Ve))/2
add(D(xbig, Ue).subs({Ue: 3, Ve: 2}), 2); add(D(xbig, Ve).subs({Ue: 3, Ve: 2}), -1)
inv31 = at(J, x=3, y=1).inv(); add(inv31, sp.Matrix([[sp.Rational(3, 2), -sp.Rational(1, 2)], [-sp.Rational(1, 2), sp.Rational(1, 2)]]))
ANSWERS["inverse-theorem/inv-yu"] = inv31[1, 1]
add(D(ysmall, Ve).subs({Ue: 4, Ve: 3}), sp.Rational(1, 2))

# ================= Chapter 5: gradient
f = x**2*y + y**3; gf = at(grad(f, [x, y]), x=1, y=2); add(tuple(gf), (4, 13))
ANSWERS["gradient/grad-dot"] = float(gf.dot(sp.Matrix([0.6, -0.8])))
f = sp.exp(-2*z)*sp.sin(2*x)*sp.cos(2*y)
same(D(f, x), 2*sp.exp(-2*z)*sp.cos(2*x)*sp.cos(2*y)); same(D(f, y), -2*sp.exp(-2*z)*sp.sin(2*x)*sp.sin(2*y))
same(D(f, z), -2*sp.exp(-2*z)*sp.sin(2*x)*sp.cos(2*y)); add(tuple(at(grad(f, [x, y, z]), x=0, y=0, z=0)), (2, 0, 0))
f = 5*x**2 - 2*x*y + y**2 - 4*y*z + z**2 + 3*x*z
ANSWERS["gradient/grad-3d-half"] = at(D(f, z), x=1, y=1, z=1)
f = x**2 + x*y + y**2 - 3*x; sol = sp.solve([D(f, x), D(f, y)], [x, y]); add((sol[x], sol[y]), (2, -1))
ANSWERS["gradient/grad-zero"] = sol[x]
f = x**2*y + y*z**3; gf = at(grad(f, [x, y, z]), x=1, y=2, z=1)
ANSWERS["gradient-level/steepest-rate"] = float(gf.norm()); add(gf.norm(), 2*sp.sqrt(14))
f = 3*x**2 - 4*x*y + 2*y**2; gf = at(grad(f, [x, y]), x=-2, y=3); add(tuple(gf), (-24, 20))
add(gf.norm(), 4*sp.sqrt(61)); add(float(gf.norm()), 31.24, 0.005); add(gf.dot(sp.Matrix([20, 24])), 0)
f = 2*x**2 - 3*x*y + 8*y**2 + 2*x - 4*y + 4; gf = at(grad(f, [x, y]), x=-2, y=1)
add(tuple(gf), (-9, 18)); add(at(f, x=-2, y=1), 18); add(gf.dot(sp.Matrix([18, 9])), 0); add(gf.dot(sp.Matrix([9, 18])), 243)
Fs = x**2 + y**2 + z**2; add(tuple(at(grad(Fs, [x, y, z]), x=1, y=1, z=1)), (2, 2, 2))
Fs = x**2 + 2*y**2 + 3*z**2; gF = at(grad(Fs, [x, y, z]), x=1, y=1, z=1); add(tuple(gF), (2, 4, 6))
ANSWERS["gradient-level/level-plane"] = (gF.dot(sp.Matrix([1, 1, 1])))/2
add(tuple(at(grad(x**2 + y**2, [x, y]), x=3, y=4)), (6, 8))
ANSWERS["differential-linear-map/linear-map"] = 2*0.1 + (-1)*0.2 + 3*(-0.1)
ANSWERS["differential-linear-map/linear-scale"] = 2*ANSWERS["differential-linear-map/linear-map"]
ANSWERS["differential-linear-map/gd-step"] = 1.5 - 0.05*20*1.5
ANSWERS["differential-linear-map/gd-diverge"] = float(sp.solve(sp.Eq(1 - 20*h, -1), h)[0])
def gd(lr, steps, p=(2.5, 1.5)):
    X, Y = p
    for _ in range(steps): X, Y = X - lr*2*X, Y - lr*20*Y
    return X, Y
X40, Y40 = gd(0.09, 40); add(math.hypot(X40, Y40) <= 0.01, True); add(abs(X40) < 0.001 and abs(Y40) < 0.001, True)  # gd-sim solution
add(math.hypot(*gd(0.05, 40)) > 0.01, True); add(2.5*0.9**40, 0.037, 5e-4)                 # default η = 0.05 is not enough in 40 steps
add(abs(gd(0.099, 40)[1]), 0.67, 0.005)                                                    # η just under 0.1: y barely decays
add(abs(gd(0.1, 40)[1]), 1.5, 1e-9); add(abs(gd(0.11, 60)[1]) > 1.5, True)                 # η = 0.1 jumps ±1.5, η > 0.1 diverges
add(1 - 2*0.05, 0.9, 1e-12)

# ================= Chapter 6: Jacobians
Fm = [x**2*y, 5*x + sp.sin(y)]; add(jac(Fm, [x, y]), sp.Matrix([[2*x*y, x**2], [5, sp.cos(y)]]))
J10 = at(jac(Fm, [x, y]), x=1, y=0); add(tuple(at(sp.Matrix(Fm), x=1, y=0)), (0, 5))
ANSWERS["vector-maps/jac-approx"] = float((sp.Matrix([0, 5]) + J10*sp.Matrix([0.1, 0.2]))[0])
add(at(x**2*y, x=1.1, y=0.2), 0.242, 1e-12)
ANSWERS["vector-maps/guess"] = 2*3
add(at(jac([x + y**2, 2*x - y], [x, y]), x=1, y=1), sp.Matrix([[1, 2], [2, -1]]))
add(at(jac([x*y, x - y**2], [x, y]), x=2, y=1), sp.Matrix([[1, 2], [1, -2]]))   # jac-sim goal
ANSWERS["vector-maps/jac-3x2"] = at(jac([x*y*z, x + 2*z], [x, y, z])[0, 2], x=1, y=2, z=3)
ANSWERS["planar-transform/polar-point"] = float(2*sp.sin(sp.pi/3))
ANSWERS["planar-transform/inverse-transform"] = sp.solve([u + v - 5, u - v - 1], [u, v])[u]
add(jac([2*u, v], [u, v]).det(), 2)
J = jac([u**2 - v**2, 2*u*v], [u, v]); same(J.det(), 4*u**2 + 4*v**2)
ANSWERS["jacobian-det/jdet-poly"] = at(J.det(), u=1, v=2)
add(jac([u + v, u - v], [u, v]).det(), -2)
ANSWERS["jacobian-det/jdet-linear"] = 4*abs(jac([3*u + v, u + 2*v], [u, v]).det())
add(sp.simplify(jac([r*sp.cos(th), r*sp.sin(th), z], [r, th, z]).det()), r)
Jsph = sp.simplify(jac([rho*sp.sin(ph)*sp.cos(th), rho*sp.sin(ph)*sp.sin(th), rho*sp.cos(ph)], [rho, ph, th]).det())
same(Jsph, rho**2*sp.sin(ph))
ANSWERS["jacobian-det/jdet-sphere"] = Jsph.subs({rho: 2, ph: sp.pi/2})

# ================= Chapter 7: chain rule
same(D((x**2 + y**2).subs({x: sp.cos(t), y: sp.sin(t)}), t), 0)
zt = (x*y).subs({x: t**2, y: t**3}); same(D(zt, t), 5*t**4)
ANSWERS["chain-one/chain-power"] = D(zt, t).subs(t, 1)
zz = sp.sqrt(x**2 - y**2); sub = {x: sp.exp(2*t), y: sp.exp(-t)}
chain = (D(zz, x)*D(sp.exp(2*t), t) + D(zz, y)*D(sp.exp(-t), t)).subs(sub)
same(chain, D(zz.subs(sub), t))
ANSWERS["chain-one/chain-sqrt"] = float(chain.subs(t, 1))
add(math.exp(2), 7.389, 5e-4); add(math.exp(-1), 0.368, 5e-4); add(2*math.e**4 + math.e**-2, 109.33, 0.005); add(math.sqrt(math.e**4 - math.e**-2), 7.380, 5e-4)
zt = (4*x**2 + 3*y**2).subs({x: sp.sin(t), y: sp.cos(t)}); same(D(zt, t), 2*sp.sin(t)*sp.cos(t)); same(zt, 3 + sp.sin(t)**2)
Tt = (x**2*y).subs({x: 1 + t, y: 2 - t}); ANSWERS["chain-one/chain-temp"] = D(Tt, t).subs(t, 0)
ANSWERS["chain-two/guess"] = 2
zz = (3*x**2 - 2*x*y + y**2).subs({x: 3*u + 2*v, y: 4*u - v})
same(D(zz, u), 38*u + 18*v); same(D(zz, v), 18*u + 34*v)
fp = (x**2 + 3*y).subs({x: r*sp.cos(th), y: r*sp.sin(th)})
ANSWERS["chain-two/polar-ftheta"] = D(fp, th).subs({r: 2, th: 0})
ww = (3*x**2 - 2*x*y + 4*z**2).subs({x: sp.exp(u)*sp.sin(v), y: sp.exp(u)*sp.cos(v), z: sp.exp(u)})
ANSWERS["chain-two/chain-general"] = D(ww, u).subs({u: 0, v: 0})
same(D(ww, u), 2*sp.exp(2*u)*(3*sp.sin(v)**2 - 2*sp.sin(v)*sp.cos(v) + 4))
same(D(ww, v), 2*sp.exp(2*u)*(sp.sin(v)**2 + 3*sp.sin(v)*sp.cos(v) - sp.cos(v)**2))
ANSWERS["chain-two/chain-count"] = 3
hg = (x**2 + y**2).subs({x: u + v, y: u*v})
Dh = sp.Matrix([[2*x, 2*y]]); Dg = jac([u + v, u*v], [u, v])
prod = (Dh*Dg).subs({x: u + v, y: u*v})
same(prod[0], D(hg, u)); same(prod[1], D(hg, v)); same(D(hg, u), 2*(u + v) + 2*u*v**2); same(D(hg, v), 2*(u + v) + 2*u**2*v)
ANSWERS["chain-matrix/chain-matrix-num"] = D(hg, u).subs({u: 1, v: 2})
ANSWERS["chain-matrix/chain-matrix-v"] = D(hg, v).subs({u: 1, v: 2})
add(tuple(sp.Matrix([[1, -1]])*sp.Matrix([[2, 0, 1], [1, 3, 0]])), (1, -3, 1))

# ================= Chapter 8: Hessian
add(hess(x**3 - 3*x + y**2 - 2*y, [x, y]), sp.Matrix([[6*x, 0], [0, 2]]))
f = x**2 + 2*x*y + y**3; add(at(hess(f, [x, y]), x=1, y=2), sp.Matrix([[2, 2], [2, 12]]))
add(tuple(at(grad(f, [x, y]), x=1, y=2)), (6, 14)); add(at(f, x=1, y=2), 13)
ANSWERS["hessian/guess"] = 3*3
ANSWERS["hessian/hess-entry"] = at(D(x**2*y + sp.exp(x*y), x, y), x=0, y=1)
ANSWERS["hessian/hess-grad-change"] = float(14 + (at(hess(f, [x, y]), x=1, y=2)*sp.Matrix([0.1, 0]))[1])
add(at(D(f, y), x=1.1, y=2), 14.2, 1e-12)
ANSWERS["hessian/hess-3var"] = at(D(x*y*z + x**2, y, z), x=1, y=2, z=3)
H = sp.Matrix([[2, 1], [1, 2]]); hv = sp.Matrix([1, -1])
ANSWERS["hessian-definite/qform"] = (hv.T*H*hv)[0]
Hq = sp.Matrix([[2, 3], [3, 4]]); add(Hq.det(), -1); add((sp.Matrix([1, -1]).T*Hq*sp.Matrix([1, -1]))[0], 0)
add(float((sp.Matrix([1, -0.7]).T*Hq*sp.Matrix([1, -0.7]))[0]), -0.24, 1e-9)
ev = sorted(Hq.eigenvals()); add(ev[0] < 0 < ev[1], True)
ANSWERS["hessian-definite/definite-det"] = hess(x**2 + x*y + y**2, [x, y]).det()
for fun, convex in [(x**2 + x*y + y**2, True), (x**2 + y**2 + 3*x - 5*y, True), (x**2 - y**2, False), (x*y, False)]:
    Hf = hess(fun, [x, y]); add(all(e >= 0 for e in Hf.eigenvals()), convex)
add(hess(x**4 + y**4, [x, y]), sp.Matrix([[12*x**2, 0], [0, 12*y**2]])); add(D(x**4, x, 2).subs(x, 0), 0)

# ================= Chapter 9: second-order approximation and extrema
f = sp.exp(x)*sp.cos(y)
add(at(f, x=0, y=0), 1); add(tuple(at(grad(f, [x, y]), x=0, y=0)), (1, 0)); add(at(hess(f, [x, y]), x=0, y=0), sp.Matrix([[1, 0], [0, -1]]))
q = 1 + x + (x**2 - y**2)/2
ANSWERS["taylor-2d/taylor-value"] = float(at(q, x=0.1, y=0.2)); add(math.exp(0.1)*math.cos(0.2), 1.083141, 1e-6)
f = x**2 + 2*x*y + y**3; h1, h2 = sp.symbols("h1 h2")
T2 = 13 + 6*h1 + 14*h2 + sp.Rational(1, 2)*(sp.Matrix([h1, h2]).T*at(hess(f, [x, y]), x=1, y=2)*sp.Matrix([h1, h2]))[0]
same(T2, 13 + 6*h1 + 14*h2 + h1**2 + 2*h1*h2 + 6*h2**2)
ANSWERS["taylor-2d/taylor-mml"] = float(T2.subs({h1: 0.1, h2: 0.1})); add(at(f, x=1.1, y=2.1), 15.091, 1e-12)
f = x**3 - 3*x + y**2 - 2*y; crit = sp.solve([D(f, x), D(f, y)], [x, y], dict=True)
add(sorted((c[x], c[y]) for c in crit), [(-1, 1), (1, 1)])
ANSWERS["critical-points/crit-find"] = crit[0][y]
for c, Dv in [((1, 1), 12), ((-1, 1), -12)]: add(at(hess(f, [x, y]), x=c[0], y=c[1]).det(), Dv)
ANSWERS["critical-points/crit-minval"] = at(f, x=1, y=1); add(at(f, x=-1, y=1), 1)
g = x**3/3 + y**2 + 2*x*y - 6*x - 3*y + 4; crit = sp.solve([D(g, x), D(g, y)], [x, y], dict=True)
add(sorted((c[x], c[y]) for c in crit), [(-1, sp.Rational(5, 2)), (3, sp.Rational(-3, 2))])
for c, Dv in [((-1, sp.Rational(5, 2)), -8), ((3, sp.Rational(-3, 2)), 8)]: add(at(hess(g, [x, y]), x=c[0], y=c[1]).det(), Dv)
f = x**2 + x*y + y**2 - 3*x; ANSWERS["critical-points/crit-half"] = at(f, x=2, y=-1)
add(hess(x**4 + y**4, [x, y]).subs({x: 0, y: 0}).det(), 0); add(hess(x**4 - y**4, [x, y]).subs({x: 0, y: 0}).det(), 0)
# absolute extrema on rectangles: compare interior critical points, edge critical points and corners
def rect_extrema(f, x0, x1, y0, y1):
    cand = [(x0, y0), (x0, y1), (x1, y0), (x1, y1)]
    for c in sp.solve([D(f, x), D(f, y)], [x, y], dict=True):
        if x0 <= c[x] <= x1 and y0 <= c[y] <= y1: cand.append((c[x], c[y]))
    for yy in (y0, y1):
        for s in sp.solve(D(f.subs(y, yy), x), x):
            if s.is_real and x0 <= s <= x1: cand.append((s, yy))
    for xx in (x0, x1):
        for s in sp.solve(D(f.subs(x, xx), y), y):
            if s.is_real and y0 <= s <= y1: cand.append((xx, s))
    vals = [f.subs({x: a, y: b}) for a, b in cand]
    return min(vals), max(vals)
f = x**2 + y**2 - 2*x - 4*y
add(rect_extrema(f, 0, 3, 0, 3), (-5, 3))
for edge, lo, hi in [(f.subs(y, 0), -1, 3), (f.subs(y, 3), -4, 0)]:
    vals = [edge.subs(x, s) for s in [0, 3] + sp.solve(D(edge, x), x)]; add((min(vals), max(vals)), (lo, hi))
for edge, lo, hi in [(f.subs(x, 0), -4, 0), (f.subs(x, 3), -1, 3)]:
    vals = [edge.subs(y, s) for s in [0, 3] + sp.solve(D(edge, y), y)]; add((min(vals), max(vals)), (lo, hi))
ANSWERS["absolute-extrema/abs-max"] = rect_extrema(f, 0, 3, 0, 4)[1]; add(f.subs({x: 3, y: 4}), 3)
f = x**2 - 2*x*y + 4*y**2 - 4*x - 2*y + 24
ANSWERS["absolute-extrema/abs-ostax"] = f.subs(sp.solve([D(f, x), D(f, y)], [x, y]))
add(rect_extrema(f, 0, 4, 0, 2), (17, 36)); add(f.subs({x: 0, y: 2}), 36)
g = x**2 + y**2 + 4*x - 6*y; c = sp.solve([D(g, x), D(g, y)], [x, y]); add((c[x], c[y]), (-2, 3))
ANSWERS["absolute-extrema/abs-circle"] = g.subs(c)
add(16 - 4*math.sqrt(52), -12.844, 5e-4)                   # boundary minimum 16 + min(4x − 6y) on radius 4
bmin = sp.minimum((g.subs({x: 4*sp.cos(t), y: 4*sp.sin(t)})), t, sp.Interval(0, 2*sp.pi)); add(float(bmin), -12.844, 5e-4)
# Lagrange
lam = sp.symbols("lam")
ANSWERS["lagrange/guess"] = sp.maximum(x*(10 - x), x, sp.Interval(0, 10))
sol = sp.solve([y - lam, x - lam, x + y - 10], [x, y, lam], dict=True)[0]; add(sol[x]*sol[y], 25)
sols = sp.solve([1 - 2*lam*x, 1 - 2*lam*y, x**2 + y**2 - 2], [x, y, lam], dict=True)
add(sorted(s[x] + s[y] for s in sols), [-2, 2])
f = x**2 + 4*y**2 - 2*x + 8*y
sol = sp.solve([2*x - 2 - lam, 8*y + 8 - 2*lam, x + 2*y - 7], [x, y, lam], dict=True)[0]; add((sol[x], sol[y]), (5, 1))
ANSWERS["lagrange/lag-ostax"] = f.subs(sol); add(f.subs({x: 7, y: 0}), 35)
sol = sp.solve([2*x - lam, 2*y - lam, 2*z - lam, x + y + z - 1], [x, y, z, lam], dict=True)[0]
ANSWERS["lagrange/lag-3d"] = float((x**2 + y**2 + z**2).subs(sol))
# Newton
fe = sp.exp(x) - 2*x; step = lambda e, a: a - D(e, x).subs(x, a)/D(e, x, 2).subs(x, a)
x1 = step(fe, 0); ANSWERS["newton/newton-1d"] = x1
x2 = step(fe, x1); same(x2, 2/sp.E); ANSWERS["newton/newton-1d-2"] = float(x2)
x3 = step(fe, x2); x4 = step(fe, x3); add(float(x3), 0.6940, 5e-5); add(float(x4), 0.6931, 5e-5); add(math.log(2), 0.6931, 5e-5)
f = x**2 + x*y + y**2 - 3*x; Hm = hess(f, [x, y]); add(Hm.inv(), sp.Matrix([[2, -1], [-1, 2]])/3)
add(tuple(-Hm.inv()*at(grad(f, [x, y]), x=0, y=0)), (2, -1))
f = x**2 + 4*y**2; gN = at(grad(f, [x, y]), x=2, y=1); HN = hess(f, [x, y]); stepN = HN.inv()*gN; add(tuple(stepN), (2, 1))
ANSWERS["newton/newton-2d"] = (sp.Matrix([2, 1]) - stepN)[1]
ANSWERS["newton/newton-vs-gd"] = 2 - 0.1*gN[0]; add(1 - 0.1*gN[1], 0.2, 1e-12)
ANSWERS["newton/newton-decrement"] = gN.dot(stepN)/2; add(f.subs({x: 2, y: 1}), 8)
f = x**2 - y**2; add(tuple(sp.Matrix([1, 1]) - hess(f, [x, y]).inv()*at(grad(f, [x, y]), x=1, y=1)), (0, 0))
add(at(f, x=1, y=1), 0)

# ================= boss
f = x**2*y + sp.exp(x*y); ANSWERS["boss/b-fxy"] = float(at(D(f, x, y), x=1, y=2))
f = x**2 + y**2; ANSWERS["boss/b-dz"] = float(5 + 2*0.03 + 4*(-0.04)); add(at(f, x=1.03, y=1.96), 4.9025, 1e-12)
f = x**2*y + y*z**3; gb = at(grad(f, [x, y, z]), x=1, y=1, z=2); add(tuple(gb), (2, 9, 12))
ANSWERS["boss/b-grad-max"] = float(gb.norm())
f = 3*x**2 + y**2; ANSWERS["boss/b-gd"] = float((sp.Matrix([1, 2]) - 0.1*at(grad(f, [x, y]), x=1, y=2))[0])
f = x**2 - x*y + 3*y**2; ANSWERS["boss/b-dir"] = float(at(grad(f, [x, y]), x=2, y=1).dot(sp.Matrix([0.8, -0.6])))
F_ = x**2 + y**2 + z**2 - 9; add(at(F_, x=1, y=2, z=2), 0); ANSWERS["boss/b-implicit"] = at(-D(F_, y)/D(F_, z), x=1, y=2, z=2)
ANSWERS["boss/b-inverse"] = at(jac([x + y, x*y], [x, y]), x=3, y=1).inv()[0, 1]
add(D(xbig, Ve).subs({Ue: 4, Ve: 3}), -sp.Rational(1, 2))
ANSWERS["boss/b-jac"] = at(jac([u**2 - v**2, 2*u*v], [u, v]).det(), u=2, v=1)
ANSWERS["boss/b-chain"] = D(hg, v).subs({u: 2, v: 1})
f = x**3 - 3*x + y**2 - 2*y; add(at(hess(f, [x, y]), x=-1, y=1).det(), -12)
ANSWERS["boss/b-minval"] = at(f, x=1, y=1)
sols = sp.solve([1 - 2*lam*x, 1 - 2*lam*y, x**2 + y**2 - 8], [x, y, lam], dict=True)
ANSWERS["boss/b-lagrange"] = max(s[x] + s[y] for s in sols)
f = 2*x**2 + y**2 - 4*x; gb = at(grad(f, [x, y]), x=0, y=3); nb = sp.Matrix([0, 3]) - hess(f, [x, y]).inv()*gb
add(tuple(nb), (1, 0)); ANSWERS["boss/b-newton"] = nb[0]

# ---------------- every graded number item in the pack has the value computed above
pack_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "content", "M.1.4.1.yaml")
pack = yaml.safe_load(open(pack_path, encoding="utf8"))
numbers = {}
for les in pack["lessons"]:
    for step in les["flow"]:
        for kind in ("item", "guess"):
            it = step.get(kind)
            if it and it["type"] == "number": numbers[f"{les['id']}/{it['id']}"] = it
for it in pack["boss"]["items"]:
    if it["type"] == "number": numbers[f"boss/{it['id']}"] = it
here = inspect.stack()[0].lineno
for key, it in numbers.items():
    if key not in ANSWERS:
        checks.append((False, key, "a computed value in ANSWERS", here)); continue
    ans = float(it["answer"]); tol = float(it.get("tolerance", max(1e-9, abs(ans)*1e-6)))
    checks.append((abs(ans - float(ANSWERS[key])) <= tol, f"{key} = {it['answer']}", float(ANSWERS[key]), here))
for key in ANSWERS:
    if key not in numbers: checks.append((False, key, "a number item in the pack", here))

bad = [(ln, g, wv) for (ok, g, wv, ln) in checks if not ok]
for i, g, wv in bad:
    print(f"line {i}: got {g!r}, want {wv!r}")
print(f"{len(checks) - len(bad)}/{len(checks)} claims hold ({len(numbers)} number items compared with the pack)")
sys.exit(1 if bad else 0)
