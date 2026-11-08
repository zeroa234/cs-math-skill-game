"""Check timer, ADC and serial math and the GPIO/debounce models."""

from fractions import Fraction as F


def debounce(samples, stable, threshold):
    count = 0
    for index, sample in enumerate(samples, 1):
        count = count + 1 if sample != stable else 0
        if count == threshold:
            yield index, sample
            stable, count = sample, 0


assert 1 << 5 == 32
assert (2 | 1 << 5, 4 | 1 << 5, 8 | 1 << 5) == (34, 36, 40)
assert list(debounce([0, 0, 1, 0, 0, 0], 1, 3)) == [(6, 0)]
assert list(debounce([0, 1, 0, 0, 0], 1, 3)) == [(5, 0)]
assert 8 - 3 - 2 == 3
assert 115200 / (1 + 8 + 1) == 11520
step = F("2.56") / (1 << 8)
assert step == F(".01") and F(".91") // step == 91 and F("1.28") // step == 128
assert 16_000_000 // 64 == 250_000
assert 250_000 * F(1, 1000) - 1 == 249
assert 8_000_000 // 8 * F(500, 1_000_000) - 1 == 499
assert F(250, 250_000) * 1000 == 1
assert F(3, 10) * 100 == 30 and F(25, 100) * 100 == 25
assert (14 - 250) % 256 == 20
assert F(".1") * 11 + F(".9") == 2
assert F(".2") * 9 + F(".8") == F("2.6")
print("H.3.1 GPIO, debounce, conversion and timing models passed")
