"""Verify P.4.1 sprint planning velocity, release math, and communication channel upper bounds."""

from fractions import Fraction
from itertools import combinations
from math import ceil
from statistics import mean


def main():
    speeds = [21, 18, 24]
    avg_speed = mean(speeds)
    assert avg_speed == 21

    backlog = 130
    ratio = Fraction(backlog, avg_speed)
    assert round(float(ratio), 2) == 6.19
    needed_sprints = ceil(ratio)
    assert needed_sprints == 7
    assert needed_sprints * 2 == 14

    fixed_weeks = 10
    fixed_sprints = fixed_weeks // 2
    assert fixed_sprints == 5
    capacity_10w = fixed_sprints * avg_speed
    assert capacity_10w == 105
    assert backlog - capacity_10w == 25

    assert ceil(Fraction(81, 20)) == 5

    for members, expected in [(4, 6), (5, 10), (8, 28)]:
        assert len(list(combinations(range(members), 2))) == expected
        assert members * (members - 1) // 2 == expected

    print("P.4.1 verify: velocity mean, release rounding, scope gap, and n*(n-1)/2 channel checks passed.")


if __name__ == "__main__":
    main()
