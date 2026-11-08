"""Recompute instruction traces, pipeline and memory examples with exact arithmetic."""

from fractions import Fraction as F


def branch_correct(results):
    state = 3
    correct = 0
    for taken in results:
        correct += (state >= 2) == taken
        state = max(0, min(3, state + (1 if taken else -1)))
    return correct


def amat(hit, miss_rate, extra):
    return hit + miss_rate * extra


def elapsed(instructions, cpi, hz):
    return instructions * cpi / hz


assert 8 + 5 == 13 and 100 + 8 == 108 and 100 + 12 == 112
assert 6 * 3 == 18 and 5 + 4 - 1 == 8 and (5 + 6 - 1) * 3 == 30
# Phase numbers are relative to IF at 0. Consumers use EX at 2.
fetch = 0
load_available = fetch + 3 + 1
add_fetch = max(fetch + 1, load_available - 2)
add_available = add_fetch + 2 + 1
sub_fetch = max(add_fetch + 1, add_available - 2)
assert (add_fetch - fetch - 1, sub_fetch - add_fetch - 1) == (1, 0)
assert 4 * 2 == 8
assert divmod(52, 16) == (3, 4) and divmod(84 // 16, 4) == (1, 1)
assert 4 * 2 * 16 == 128 and 1024 + 12 == 1036
assert amat(1, F(1, 10), amat(8, F(1, 4), 80)) == F(19, 5)
assert amat(1, F(5, 100), 100) == 6
assert amat(1, F(5, 100), amat(10, F(1, 5), 100)) == F(5, 2)
pattern = [True, True, True, False]
assert branch_correct(pattern * 2) == 6 and F(branch_correct(pattern * 3), 12) == F(3, 4)
old = elapsed(10**9, F(3, 2), 2 * 10**9)
new = elapsed(10**9, F(6, 5), 18 * 10**8)
assert elapsed(2 * 10**8, F(3, 2), 2 * 10**9) == F(3, 20)
assert old == F(3, 4) and old / new == F(9, 8)
assert F(4 * 5, 100) == F(1, 5)
assert 1 / (F(1, 5) + F(4, 5) / 16) == 4
assert 1 / F(1, 5) == 5 and 1 / F(1, 4) == 4
print("C.1.2 architecture examples passed")
