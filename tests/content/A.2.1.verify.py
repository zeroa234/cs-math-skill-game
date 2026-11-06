"""Independently compute the gradient, fit, cluster centers and PCA examples."""
from fractions import Fraction as F
from statistics import mean
from math import exp

x, y = list(range(1, 5)), [1, 3, 2, 5]
# Use exact means and normal equations for the fitted line.
mx, my = F(sum(x), len(x)), F(sum(y), len(y))
w = sum((i-mx)*(j-my) for i, j in zip(x, y)) / sum((i-mx)**2 for i in x)
assert w == F("1.1") and my-w*mx == 0
errors = [-v for v in y]
dw = F(2, len(x))*sum(i*r for i, r in zip(x, errors))
db = F(2, len(x))*sum(errors)
assert (dw, db) == (F("-16.5"), F("-5.5"))
assert (-F(".01")*dw, -F(".01")*db) == (F(".165"), F(".055"))
assert 0 - F(".1")*(-4) == F(".4") and 0 - F(".1")*(-6) == F(".6")
assert 1/(1+exp(0)) == 0.5 and F(".2") - 1 == F("-.8")

points = [1, 2, 3, 10, 11, 12]
centers = [F(1), F(2)]
history = []
for _ in range(3):
    groups = [[p for p in points if min(range(2), key=lambda j: abs(p-centers[j])) == i]
              for i in range(2)]
    centers = [F(sum(g), len(g)) for g in groups]
    history.append(centers)
assert history == [[1, F("7.6")], [2, 11], [2, 11]]
assert (1+F("7.6"))/2 == F("4.3") and F(2+11, 2) == F("6.5")
assert mean([2, 4, 9]) == 5 and mean([3, 6, 9]) == 6

cov = [[2, 1], [1, 2]]
def product(v):
    return [sum(a*b for a, b in zip(row, v)) for row in cov]
assert product([1, 1]) == [3, 3] and product([1, -1]) == [1, -1]
assert F(3, 3+1) == F(".75") and F(8, 10) == F(".8") and F(9, 12) == F(".75")
assert 3**2 == 9
print("A.2.1: regression, classification, k-means and PCA examples verified")
