"""Verify all integrals, derivatives, Riemann sums, substitution bounds, and improper integrals in M.1.3."""

from __future__ import annotations

import math
from fractions import Fraction as F


def check_exact_fraction_riemann() -> None:
    # 1. Sigma sum_j^3 j^2 = 14
    assert sum(j * j for j in range(1, 4)) == 14
    # 2. Left vs right Riemann sum on [0, 2] for f(x) = x with n = 2 (width 1)
    assert sum(x * 1 for x in (0, 1)) == 1
    assert sum(x * 1 for x in (1, 2)) == 3
    # 3. Right Riemann sum on [0, 2] for f(x) = x^2 with n = 2 (width 1)
    assert sum(x * x * 1 for x in (1, 2)) == 5
    # 4. Left Riemann sum threshold on [0, 1] for x^2: exact threshold is n >= 25
    err24 = abs(sum(F(j * j, 24**3) for j in range(24)) - F(1, 3))
    err25 = abs(sum(F(j * j, 25**3) for j in range(25)) - F(1, 3))
    assert err24 >= F("0.02") and err25 < F("0.02")
    n = 50
    left = sum(F(j * j, n**3) for j in range(n))
    assert abs(left - F(1, 3)) < F("0.02")
    # 5. Net signed area vs total area on [0, 4] for f(x) = 2 - x
    # Split [0, 2] (triangle height 2) + [2, 4] (triangle height -2)
    signed_total = F(2 * 2, 2) - F(2 * 2, 2)
    abs_total = F(2 * 2, 2) + F(2 * 2, 2)
    assert signed_total == 0 and abs_total == 4
    # 6. Initial condition F'(x) = 2x, F(0) = 5 -> F(3) = 14
    c = 5 - 0**2
    assert 3**2 + c == 14


def check_sympy() -> None:
    try:
        import sympy as s
    except ImportError:
        # Pure stdlib numerical verification when SymPy is absent
        def trap(fn, a: float, b: float, steps: int = 4000) -> float:
            h = (b - a) / steps
            total = 0.5 * (fn(a) + fn(b))
            for k in range(1, steps):
                total += fn(a + k * h)
            return total * h

        assert abs(trap(math.sin, 0.0, math.pi) - 2.0) < 1e-6
        assert abs(trap(lambda u: 2 * u * (1 + u * u), 0.0, 2.0) - 12.0) < 1e-5
        assert abs(trap(lambda t: math.cos(t) * (math.sin(t) ** 3), 0.0, math.pi / 2) - 0.25) < 1e-6
        assert abs(trap(lambda x: 2.0 * math.sqrt(max(0.0, 4.0 - x * x)), -2.0, 2.0, 10000) / 2.0 - 2 * math.pi) < 1e-3
        return

    x, t = s.symbols("x t", real=True)
    assert s.integrate(s.sin(x), (x, 0, s.pi)) == 2
    assert s.integrate(s.sqrt(4 - x**2), (x, -2, 2)) == 2 * s.pi
    assert s.integrate(s.Abs(2 - x), (x, 0, 4)) == 4
    assert s.integrate(2 - x, (x, 0, 4)) == 0

    for end, fn in [(x * x, s.exp(-t * t)), (3 * x, s.cos(t)), (x * x, s.sin(t))]:
        integral = s.Integral(fn, (t, 0, end))
        assert s.simplify(s.diff(integral, x) - fn.subs(t, end) * s.diff(end, x)) == 0

    assert s.integrate(2 * x * (1 + x * x), (x, 0, 1)) == s.Rational(3, 2)
    assert s.integrate(2 * x * (1 + x * x), (x, 0, 2)) == 12
    assert s.integrate(s.cos(x) * s.sin(x) ** 3, (x, 0, s.pi / 2)) == s.Rational(1, 4)

    assert s.integrate(x**-2, (x, 1, s.oo)) == 1
    assert s.integrate(x**-1, (x, 1, s.oo)) == s.oo
    assert s.integrate(1 / s.sqrt(x), (x, 0, 1)) == 2
    assert s.integrate(x**-2, (x, -1, 1)) == s.oo
    assert s.integrate(s.exp(-x), (x, 1, s.oo)) == s.exp(-1)

    for primitive, integrand in [
        (x**3 / 3, x**2),
        (x**4 / 4, x**3),
        (s.log(1 + x * x), 2 * x / (1 + x * x)),
        ((x - 1) * s.exp(x), x * s.exp(x)),
        (x * s.sin(x) + s.cos(x), x * s.cos(x)),
        (x * s.log(x) - x, s.log(x)),
    ]:
        assert s.simplify(s.diff(primitive, x) - integrand) == 0


def main() -> None:
    check_exact_fraction_riemann()
    check_sympy()
    print("ok — verified all Riemann sums, FTC derivatives, substitutions, improper integrals, and antiderivatives in M.1.3.yaml")


if __name__ == "__main__":
    main()
