"""Verify Riemann sums, FTC, substitution, antiderivatives and improper integrals."""
from fractions import Fraction as F
import sympy as s

x, t = s.symbols("x t", real=True)
b = s.symbols("b", positive=True)
assert sum([0, 1]) == 1 and sum([1, 2]) == 3
assert sum(j*j for j in (1, 2)) == 5
n = 50
left = sum(F(j*j, n**3) for j in range(n))
assert abs(left - F(1, 3)) < F("0.02")
assert 5 - 2 == 3 and 6 - 4 == 2 and 7 - 3 == 4
assert s.integrate(s.sin(x), (x, 0, s.pi)) == 2
for end, fn in [(x*x, s.exp(-t*t)), (3*x, s.cos(t)), (x*x, s.sin(t))]:
    integral = s.Integral(fn, (t, 0, end))
    assert s.simplify(s.diff(integral, x) - fn.subs(t, end)*s.diff(end, x)) == 0
for stop, expected in [(1, s.Rational(3, 2)), (2, 12)]:
    assert s.integrate(2*x*(1+x*x), (x, 0, stop)) == expected
assert s.integrate(x**-2, (x, 1, s.oo)) == 1
assert s.integrate(x**-1, (x, 1, s.oo)) == s.oo
assert s.integrate(1/s.sqrt(x), (x, 0, 1)) == 2
for primitive, integrand in [
    (x**3/3, x**2), (x**4/4, x**3), ((x-1)*s.exp(x), x*s.exp(x)),
    (s.log(1+x*x), 2*x/(1+x*x)), (s.sin(x), s.cos(x)),
]:
    assert s.simplify(s.diff(primitive, x) - integrand) == 0
print("M.1.3: sums and symbolic integrals verified")
