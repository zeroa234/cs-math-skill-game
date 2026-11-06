"""Check OLS, normal equations, and regression diagnostics examples."""
from fractions import Fraction as F
from statistics import mean
from math import exp

x, y = list(range(1, 6)), [2, 3, 5, 4, 6]
mx, my = mean(x), mean(y)
assert (mx, my) == (3, 4)
sxx = sum((i-mx)**2 for i in x)
sxy = sum((i-mx)*(j-my) for i, j in zip(x, y))
assert (sxx, sxy) == (10, 9)
w = F(sxy, sxx)
b = my - w*mx
assert (w, b) == (F(".9"), F("1.3"))
assert [len(x), sum(x), sum(i*i for i in x)] == [5, 15, 55]
assert [sum(y), sum(i*j for i, j in zip(x, y))] == [20, 69]
assert 5*b + 15*w == 20 and 15*b + 55*w == 69
sse = sum((j-b-w*i)**2 for i, j in zip(x, y))
sst = sum((j-my)**2 for j in y)
assert (sse, sst) == (F("1.9"), 10) and 1 - sse/sst == F(".81")
assert [b+w*i for i in (2, 5)] == [F("3.1"), F("5.8")]
assert sum(i*i for i in [1, 2, 3]) == 14
assert 1/(1+exp(0)) == 0.5 and 3+2*1 == 5
assert 1/(1-F(".8")) == 5 and 2**2+3**2 == 13
assert F(".5")*(2**2 + (-3)**2) == F("6.5")
print("M.6.2.2: exact OLS, R^2, link, interaction, variance and ridge examples verified")
