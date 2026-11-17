"""Verify P.4.5 triangle equivalence/boundary cases, mutation score, property tests, short-circuit MC/DC, and MTBF math."""

from fractions import Fraction


def classify_triangle(a, b, c):
    if a <= 0 or b <= 0 or c <= 0:
        return "非法"
    x, y, z = sorted((a, b, c))
    if x + y <= z:
        return "非法"
    if x == z:
        return "等边"
    if x == y or y == z:
        return "等腰"
    return "不等边"


def classify_triangle_mutant(a, b, c):
    # Buggy mutant: <= changed to < (misses degenerate boundary x + y == z)
    if a <= 0 or b <= 0 or c <= 0:
        return "非法"
    x, y, z = sorted((a, b, c))
    if x + y < z:
        return "非法"
    if x == z:
        return "等边"
    if x == y or y == z:
        return "等腰"
    return "不等边"


def check_triangle_and_mutation():
    cases = [
        ((3, 3, 3), "等边"),
        ((2, 2, 3), "等腰"),
        ((5, 5, 6), "等腰"),
        ((2, 3, 4), "不等边"),
        ((1, 2, 3), "非法"),   # Degenerate boundary a + b == c
        ((2, 3, 5), "非法"),
        ((2, 3, 6), "非法"),
        ((0, 3, 4), "非法"),
        ((-1, 3, 4), "非法"),
    ]
    for args, expected in cases:
        assert classify_triangle(*args) == expected

    # Mutant test suite check
    sub_cases = [((1, 2, 3), "非法"), ((2, 2, 3), "等腰"), ((3, 3, 3), "等边"), ((2, 3, 4), "不等边")]
    results = [classify_triangle_mutant(*args) == exp for args, exp in sub_cases]
    assert results == [False, True, True, True]  # 1 failed (killed!), 3 passed


def check_property_sorting():
    def bad_sort(xs):
        return sorted(set(xs))

    assert bad_sort([1, 1]) == [1]  # Fails length invariant!
    assert len(bad_sort([1, 1])) != len([1, 1])
    assert sorted([3, 1, 1, 2]) == [1, 1, 2, 3]


def check_short_circuit_mcdc():
    def eval_and(a, b):
        log = []

        def check_b():
            val = b > 0
            log.append(val)
            return val

        res = (a > 0) and check_b()
        return res, log

    assert eval_and(1, 1) == (True, [True])
    assert eval_and(1, -1) == (False, [False])
    assert eval_and(-1, 1) == (False, [])
    assert eval_and(-1, 2) == (False, [])

    # Condition coverage pair {(1, -1), (-1, 1)} covers T/F of (a>0) and triggers False for overall expression only
    cc_outputs = [eval_and(a, b)[0] for a, b in ((1, -1), (-1, 1))]
    assert cc_outputs == [False, False]  # Branch True NEVER executed!

    # MC/DC minimal 3-case set: {(1, 1), (1, -1), (-1, 1)}
    mcdc = [(1, 1), (1, -1), (-1, 1)]
    assert len(mcdc) == 3
    assert [eval_and(a, b)[0] for a, b in mcdc] == [True, False, False]


def check_coverage_and_availability():
    assert Fraction(4, 5) == Fraction("0.8")
    assert Fraction(6, 8) == Fraction("0.75")
    assert Fraction(8, 10) == Fraction("0.8")
    assert Fraction(9, 12) == Fraction("0.75")

    mtbf, mttr = 500, 2
    avail_pct = round(mtbf / (mtbf + mttr) * 100, 2)
    assert avail_pct == 99.60

    hours_per_year = 365 * 24
    assert hours_per_year == 8760
    downtime_h = hours_per_year * 0.0001
    downtime_m = downtime_h * 60
    assert abs(downtime_h - 0.876) < 1e-9
    assert abs(downtime_m - 52.56) < 1e-9


if __name__ == "__main__":
    check_triangle_and_mutation()
    check_property_sorting()
    check_short_circuit_mcdc()
    check_coverage_and_availability()
    print("P.4.5 verify: all triangle BVA, mutation, property-sort, short-circuit MC/DC, and MTBF checks passed.")
