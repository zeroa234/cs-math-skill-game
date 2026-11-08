"""Recompute the measurement, sampling and actuator examples."""

from fractions import Fraction as F
from math import log2, sqrt
from statistics import mean


def calibrated(voltage):
    slope = (F("1.52") - F(".52")) / 100
    return (F(voltage) - F(".52")) / slope


assert 4 * 10 == 40
assert calibrated(".97") == 45 and calibrated("1.02") == 50
assert F(108 - 100, 100 * 20) * 100 == F(".4")
assert mean([22, 22, 22]) - 20 == 2
assert 9600 // (1 + 8 + 1) == 960
assert F(1000, 2000) == F(".5") and 2000 * 2 == 4000
assert log2(sqrt(4)) == 1 and log2(sqrt(16)) == 2
assert F(1_000_000, 2000) == 500
assert 12 * F(".25") == 3
print("H.3.3 calibration, acquisition, communication and PWM examples passed")
