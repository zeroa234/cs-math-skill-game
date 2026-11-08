"""Verify the planning and communication examples against their stated models."""

from fractions import Fraction
from itertools import combinations
from math import ceil
from statistics import mean


speed = mean([21, 18, 24])
assert speed == 21
assert round(Fraction(130, speed), 2) == Fraction(619, 100)
assert ceil(Fraction(130, speed)) == 7
assert 7 * 2 == 14
assert 10 // 2 == 5
assert 5 * speed == 105
assert 130 - 5 * speed == 25
assert ceil(Fraction(81, 20)) == 5

for members, expected in [(4, 6), (5, 10), (8, 28)]:
    assert len(list(combinations(range(members), 2))) == expected
    assert members * (members - 1) // 2 == expected

print("P.4.1 sprint forecasts and pair counts passed")
