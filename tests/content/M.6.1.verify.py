"""Enumerate the discrete cases and independently compute continuous values."""
from fractions import Fraction as F
from itertools import product
from math import comb, exp, isclose
from statistics import NormalDist, pvariance

coins = list(product((0, 1), repeat=2))
assert F(sum(sum(t) == 1 for t in coins), len(coins)) == F(1, 2)
assert F(sum(sum(t) <= 1 for t in coins), len(coins)) == F(3, 4)
assert comb(4, 2) == 6
assert F(1, 2)**3 == F(1, 8)
dice = list(product(range(1, 7), repeat=2))
assert F(sum(sum(t) == 7 for t in dice), len(dice)) == F(1, 6)
filtered = [t for t in dice if 6 in t]
assert F(sum(sum(t) == 7 for t in filtered), len(filtered)) == F(2, 11)
assert round(10000*F(95, 95+990)) == 876
assert F(2, 3) == F(2 - 0, 3 - 0)
assert isclose(exp(-6)/exp(-4), exp(-2))
assert round(exp(-2), 6) == 0.135335
assert 1/2 == 0.5 and 1/(2*2) == 0.25
assert pvariance([0, 4]) == 4 and pvariance([0, 6]) == 9
assert 2+3 == 5 and F(4, 100) == F(".04")
n = 100
mean, sd = n/2, (n/4)**0.5
assert (54.5 - mean)/sd == 0.9
assert round(1 - NormalDist().cdf((59.5 - mean)/sd), 4) == 0.0287
print("M.6.1: coins, dice, Bayes, exponential tail, variance and normal approximation verified")
