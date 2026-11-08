"""Check estimates, Student-t inference and the worked examples."""
from fractions import Fraction as F
from math import sqrt
from statistics import mean, stdev
from scipy import stats

assert F(1, 2)**2 == F(1, 4) and F(1, 2)**3 == F(1, 8)
assert 3 + (-2)**2 == 7 and 2 + 3**2 == 11
assert F(8, 2) == 4 and 3 * F(".1") == F(".3")
assert 1 - F(".2") == F(".8") and 1 - F(".15") == F(".85")
for observations, answer in [([0, 2, 4], 2), ([1, 3, 5], 3)]:
    score = sum(observations)/answer - len(observations)
    assert score == 0 and mean(observations) == answer
assert max({1: -7, 2: -3, 3: -5}.items(), key=lambda t: t[1])[0] == 2

samples = [4.8, 5.1, 5.3, 4.9, 5.4, 5.0, 5.2, 4.7, 5.1, 5.5]
avg, sd, count = mean(samples), stdev(samples), len(samples)
se = sd/sqrt(count)
assert avg == 5.1 and round(sd, 4) == 0.2582 and round(se, 5) == 0.08165
critical = stats.t.ppf(.975, count-1)
assert round(critical, 3) == 2.262
assert [round(avg + sign * 2.262 * se, 4) for sign in [-1, 1]] == [4.9153, 5.2847]
assert sd*sqrt(1+1/count) > se
test = stats.ttest_1samp(samples, 5.3)
assert round(test.statistic, 3) == -2.449 and round(test.pvalue, 4) == 0.0368
assert 10 + 2*F(".5") == 11 and (F(".8") - F(".5")) / F(".1") == 3
print("M.6.2: estimation, interval, Student-t test and decision quantities verified")
