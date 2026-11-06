"""Verify the cloud lesson models with exact arithmetic and the stated rates."""
from decimal import Decimal as D
from fractions import Fraction as F
from math import ceil

assert 200 * F(70, 100) == 140
assert ceil(F(5000, 140)) == 36
assert 100 * F(80, 100) == 80
assert ceil(F(950, 80)) == 12

assert ceil(3 * F(90, 60)) == 5
assert ceil(4 * F(75, 50)) == 6

hours = 30 * 24
base = 10 * hours * D("0.06")
peak = 20 * 4 * 30 * D("0.10")
full = 10 * hours * D("0.10") + peak
assert hours == 720
assert (base, peak, base + peak, full) == (432, 240, 672, 960)
assert full - (base + peak) == 288
assert (full - (base + peak)) / full == D("0.30")
assert 2 * hours * D("0.05") + 30 * 2 * D("0.10") == 78

print("C.4.2: capacity, autoscaling, baseline, peak and savings verified")
