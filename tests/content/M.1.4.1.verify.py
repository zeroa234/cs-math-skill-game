"""Check partials, linearization, Jacobians, and second-order examples."""
from fractions import Fraction as F
from math import hypot
import sympy as s

x, y, z, u, v = s.symbols("x y z u v", real=True)
f = x*x*y + s.exp(x*y)
assert s.simplify(s.diff(f, x, y) - (2*x + (1+x*y)*s.exp(x*y))) == 0
assert s.diff(x*x*y, x).subs({x: 2, y: 3}) == 12
assert s.diff(x*x*y, x).subs({x: 3, y: 2}) == 12
assert 5 + 2*F(".02") - 4*F(".03") == F("4.92")
assert F("1.02")**2 + F("1.97")**2 == F("4.9213")
assert 5 + 2*F(".1") == F("5.2")
assert 3*F(".1") - 2*F(".1") == F(".1")
assert hypot(3, 4) == 5 and hypot(6, 8) == 10
assert 2*F(".6") + 4*F(".8") == F("4.4")
assert 3*1 + 4*0 == 3
assert [-F(a, 1) for a in (1, 1)] == [-1, -1]
assert -F(1, 2) == F("-.5")

g = s.Matrix([u+v, u*v])
dg = g.jacobian([u, v])
assert dg[1, 0].subs(v, 3) == 3
assert dg[1, 1].subs(u, 4) == 4
assert s.Matrix([2*u, 3*v]).jacobian([u, v]).det() == 6
assert s.simplify(s.Matrix([u*s.cos(v), u*s.sin(v)]).jacobian([u, v]).det()) == u
composed = (u+v)**2 + (u*v)**2
assert [s.diff(composed, a).subs({u: 1, v: 2}) for a in (u, v)] == [14, 10]
assert s.diff((2*u)**2, u).subs(u, 3) == 24

f = x*x*y + y*z**3
grad = s.Matrix([f]).jacobian([x, y, z]).subs({x: 1, y: 2, z: 1})
assert list(grad) == [4, 2, 6] and grad.dot(grad) == 56
f = x**3 - 3*x + y*y - 2*y
for a, value, determinant in [(1, -3, 12), (-1, 1, -12)]:
    point = {x: a, y: 1}
    assert list(s.Matrix([f]).jacobian([x, y]).subs(point)) == [0, 0]
    assert f.subs(point) == value and s.hessian(f, [x, y]).det().subs(point) == determinant
assert (x*x + 2*y*y).subs({x: 1, y: 2}) == 9
assert 1 - F(".05") * s.diff(x*x + 10*y*y, y).subs(y, 1) == 0
print("M.1.4.1: multivariable derivatives, geometry and optimization verified")
