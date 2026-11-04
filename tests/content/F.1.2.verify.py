# Checks every number, example and claim data/content/F.1.2.yaml states, by computing it independently:
# running the programs the lessons show, brute force over small cases (every comparison order, every subset,
# every tour), networkx for the graph examples (shortest paths, MSTs, components, max flow, matchings) and
# sympy for the algebra. Every graded number item's `answer` and every text item's `answers` is read from the
# pack and compared with the value computed here (NUM / TEXT below); choice and order items whose right
# answer is a computed fact are checked the same way (CHOICE). The run fails if a number or text item has no
# computed value, or anything disagrees.
# usage: .venv/Scripts/python.exe -I tests/content/F.1.2.verify.py   (prints "N/N claims hold", exit 1 on a mismatch)
# The .venv needs sympy, networkx and pyyaml.
import heapq, inspect, itertools, math, os, re, sys
from fractions import Fraction as F
import networkx as nx
import sympy as sp
import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

checks = []
def add(got, want, tol=1e-9):
    line = inspect.stack()[1].lineno
    if isinstance(want, float) or isinstance(got, float):
        try: ok = abs(float(got) - float(want)) <= tol
        except (TypeError, ValueError): ok = False
    else:
        ok = got == want
    checks.append((bool(ok), got, want, line))

NUM, TEXT, CHOICE = {}, {}, {}   # "lesson/item" -> computed value / string / text of the right option(s)
print("Python", sys.version.split()[0], "sympy", sp.__version__, "networkx", nx.__version__)

# ================= 渐近分析
# ---------------- count-steps
def guess_count(n):
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            count = count + 1
    return count
add(guess_count(10), 45); add(9 * 10, 90)
def count2_compares(n):
    c = 0
    for i in range(n):
        for j in range(i + 1, n): c += 1
    return c
NUM["count-steps/two-sum-compares"] = count2_compares(1000)
add(NUM["count-steps/two-sum-compares"], 1000 * 999 // 2)
NUM["count-steps/three-sum-10"] = sum(1 for _ in itertools.combinations(range(10), 3))
add(math.comb(10, 3), 10 * 9 * 8 // 6)
add(3 * math.comb(1000, 3) / 1000**3, 0.4985, tol=1e-4)          # ~ n^3/2 array accesses

# ---------------- tilde
n_ = 1000
add(math.comb(n_, 3), 166167000)
NUM["tilde/exact-1000"] = 1000 * 999 * 998 // 6
add(F(n_**3, 6) - F(n_**2, 2) + F(n_, 3), F(166167000))
add(round(n_**3 / 6), 166666667)
add(abs(166167000 / (n_**3 / 6) - 1) < 0.01, True)                  # guess: under 1%
add(round((1 - 166167000 / (n_**3 / 6)) * 100, 1), 0.3)
CHOICE["tilde/tilde-pick"] = "∼ 3n²"
add([round((3 * m**2 + 100 * m + 7) / (3 * m**2), 4) for m in (10**2, 10**4, 10**6)], [1.3336, 1.0033, 1.0])
times = {1000: 0.1, 2000: 0.8, 4000: 6.4, 8000: 51.1}
add([round(times[2 * m] / times[m], 1) for m in (1000, 2000, 4000)], [8.0, 8.0, 8.0])
NUM["tilde/doubling-b"] = math.log2(4)
NUM["tilde/doubling-predict"] = 51.1 * 2**3
add(round(NUM["tilde/doubling-predict"], 1), 408.8)
nlogn_ratio = lambda m: (2 * m * math.log2(2 * m)) / (m * math.log2(m))
add(all(abs(nlogn_ratio(m) - (2 + 2 / math.log2(m))) < 1e-9 for m in (8, 1000, 10**6)), True)
add(round(nlogn_ratio(10**6), 2), 2.1)

# ---------------- big-o
add([(m * m < 2 * m + 20) for m in range(1, 8)], [True] * 5 + [False] * 2)   # n <= 5: n^2 smaller; n >= 6: 2n+20
add((5 * 5, 2 * 5 + 20, 6 * 6, 2 * 6 + 20), (25, 30, 36, 32))
ratios = [F(2 * m + 20, m + 1) for m in range(1, 10000)]
NUM["big-o/smallest-c"] = max(ratios)
add(all(ratios[i] > ratios[i + 1] for i in range(len(ratios) - 1)), True)
add(max(F(2 * m + 20, m * m) for m in range(1, 1000)), 22)            # DPV: (2n+20)/n^2 <= 22
add(max(F(2 * m + 20, m + 1) for m in range(1, 1000)) <= 20, True)   # DPV's looser c = 20
N_ = sp.Symbol("n", positive=True)
lim = lambda f, g: sp.limit(f / g, N_, sp.oo)
add(lim(sp.sqrt(N_), N_**sp.Rational(2, 3)), 0); CHOICE["big-o/sqrt-vs"] = "f = O(g)，但 f 不是 Ω(g)"
add(sp.simplify(10 * sp.log(N_) / sp.log(N_**2)), 5); CHOICE["big-o/log-square"] = "f = Θ(g)"
add(lim(N_ * 2**N_, 3**N_), 0); CHOICE["big-o/expo-poly"] = "f = O(g)"
order = [sp.log(N_), sp.sqrt(N_), N_ * sp.log(N_), N_**2, 2**N_, sp.factorial(N_)]
add(all(lim(order[i], order[i + 1]) == 0 for i in range(len(order) - 1)), True)
CHOICE["big-o/order-growth"] = ["log n", "√n", "n log n", "n²", "2ⁿ", "n!"]
add(next(m for m in range(1, 50) if math.factorial(m) > 2**m), 4)

# ---------------- growth-classes
def bsearch_compares(a, x):
    lo, hi, c = 0, len(a) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2; c += 1
        if a[mid] == x: return c
        if a[mid] < x: lo = mid + 1
        else: hi = mid - 1
    return c
worst = lambda m: max(max(bsearch_compares(list(range(m)), x) for x in range(m)), bsearch_compares(list(range(m)), m))
add(worst(1000), 1 + math.floor(math.log2(1000))); add(worst(1000), 10)
NUM["growth-classes/bs-million"] = 1 + math.floor(math.log2(10**6))
add(2**19 <= 10**6 < 2**20, True)
add(worst(2**12), 1 + 12)

# ---------------- memory
NUM["memory/guess"] = 1001
depth = [0, 0]
def f_rec(m):
    depth[0] += 1; depth[1] = max(depth[1], depth[0])
    if m > 0: f_rec(m - 1)
    depth[0] -= 1
f_rec(900); add(depth[1], 901)                                       # n + 1 calls deep (1000 would hit the limit)
NUM["memory/int-array"] = 24 + 4 * 1000
date = 16 + 3 * 4; add(date, 28); add(-(-date // 8) * 8, 32)
pt = 16 + 4 + 4 + 8; NUM["memory/point-object"] = -(-pt // 8) * 8
add((sys.getsizeof(1), sys.getsizeof([])), (28, 56))
add(sys.version_info[:2], (3, 14))

# ================= 递归
# ---------------- fibonacci
calls = {}
def fib1(m):
    calls[m] = calls.get(m, 0) + 1
    return m if m <= 1 else fib1(m - 1) + fib1(m - 2)
fib1(5); add(sum(calls.values()), 15); add((calls[3], calls[2]), (2, 3)); CHOICE["fibonacci/guess"] = "15"
calls.clear(); fib1(10)
NUM["fibonacci/calls-10"] = sum(calls.values())
C = [1, 1]
for m in range(2, 11): C.append(C[-1] + C[-2] + 1)
add(C, [1, 1, 3, 5, 9, 15, 25, 41, 67, 109, 177])
Fib = [0, 1]
for m in range(2, 300): Fib.append(Fib[-1] + Fib[-2])
add(C[10], 2 * Fib[11] - 1); add(Fib[11], 89)
NUM["fibonacci/repeat-2"] = calls[2]; add(calls[2], Fib[9])
add([calls[k] for k in range(10, 1, -1)], [Fib[i] for i in range(1, 10)])
add(Fib[:10], [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])
add(Fib[200] / 4e13 >= 2**92, True)                                 # DPV: fib1(200) takes at least 2^92 s at 40 trillion steps/s
add(round(math.log2(Fib[200]) / 200, 3), 0.688)                     # F_n ~ 2^(0.694 n): the ratio tends to 0.694
add(round(math.log2((1 + 5**0.5) / 2), 3), 0.694)
def fib2(m):
    if m == 0: return 0
    f = [0] * (m + 1); f[1] = 1; adds = 0
    for i in range(2, m + 1): f[i] = f[i - 1] + f[i - 2]; adds += 1
    return f[m], adds
NUM["fibonacci/fib2-adds"] = fib2(100)[1]; add(fib2(100)[0], Fib[100])
add(2 * Fib[101] - 1 > 10**21, True)
add(len(str(Fib[100])), 21); add(Fib[100].bit_length(), 69)
CHOICE["fibonacci/fib2-bits"] = "n²"

# ---------------- recursion-iteration
def s2(m): return 0 if m == 0 else m + s2(m - 1)
try: s2(5000); deep = "ok"
except RecursionError: deep = "RecursionError"
add(deep, "RecursionError"); add(sum(range(5001)), 12502500); add(sys.getrecursionlimit(), 1000)
CHOICE["recursion-iteration/guess"] = "报错，说递归太深"
dd = [0, 0]
def fd(m):
    dd[0] += 1; dd[1] = max(dd[1], dd[0])
    r = m if m <= 1 else fd(m - 1) + fd(m - 2)
    dd[0] -= 1; return r
fd(10); NUM["recursion-iteration/fib-depth"] = dd[1]
def s4(m, acc=0): return acc if m == 0 else s4(m - 1, acc + m)
add(s4(100), 5050)
def s3(m):
    stack = []
    for i in range(m, 0, -1): stack.append(i)
    t = 0
    while stack: t = t + stack.pop()
    return t
add(s3(4), 10); add(s3(3), 6)
st = []
for i in range(4, 0, -1): st.append(i)
add(st, [4, 3, 2, 1]); add(st[-1] + st[-2], 3)                    # trace: t after two pops

# ---------------- recursion-tree
T = lambda m: 1 if m == 1 else 2 * T(m // 2) + m
add((T(2), T(4), T(8)), (4, 12, 32)); CHOICE["recursion-tree/guess"] = "32"
NUM["recursion-tree/level-two"] = 3**2 * (64 // 2**2); add(NUM["recursion-tree/level-two"], 64 * 9 / 4)
NUM["recursion-tree/geo-sum"] = sum(2**i for i in range(11))
NUM["recursion-tree/leaves-3"] = 3**10; add(round(2**(10 * math.log2(3))), 59049)
T4 = lambda m: 1 if m == 1 else 4 * T4(m // 2) + m
add([T4(2**k) for k in range(6)], [2 * 4**k - 2**k for k in range(6)])   # Θ(n²): 2n² − n
add([4**k * 64 // 2**k for k in range(3)], [64 * 2**k for k in range(3)])

# ---------------- master-theorem
def master(a, b, d):
    e = math.log(a, b)
    if abs(d - e) < 1e-12: return "n^d log n"
    return "n^d" if d > e else "n^log_b a"
add(master(1, 2, 0), "n^d log n")
add([master(2, 2, 1), master(4, 2, 1), master(1, 2, 0), master(2, 2, 2)], ["n^d log n", "n^log_b a", "n^d log n", "n^d"])
add((master(5, 2, 1), master(9, 3, 2)), ("n^log_b a", "n^d log n"))
NUM["master-theorem/log2-5"] = math.log2(5)
B = lambda m: 1 if m == 0 else 2 * B(m - 1) + 1
add([B(m) for m in range(6)], [2**(m + 1) - 1 for m in range(6)])
D = lambda m: 1 if m == 1 else D(m - 1) + m
add(all(D(m) == m * (m + 1) // 2 for m in range(1, 200)), True)
add(lim(N_**2 * sp.log(N_), N_**sp.log(5, 2)), 0)                   # n^2 log n grows slower than n^2.32

# ================= 分治
# ---------------- karatsuba
def three_mult(x, y, half):
    a, b = divmod(x, 10**half); c, d = divmod(y, 10**half)
    ac, bd, s = a * c, b * d, (a + b) * (c + d)
    return ac, bd, s, s - ac - bd, ac * 10**(2 * half) + (s - ac - bd) * 10**half + bd
add(three_mult(1234, 5678, 2), (672, 2652, 6164, 2840, 7006652)); add(1234 * 5678, 7006652)
add((6720000 + 284000 + 2652), 7006652)
r = three_mult(47, 53, 1); NUM["karatsuba/mid-47-53"] = r[3]; add(r[4], 47 * 53); add((r[0], r[1], r[2]), (20, 21, 88))
NUM["karatsuba/log2-3"] = math.log2(3)
def karatsuba(x, y):
    if x < 10 or y < 10: return x * y
    half = max(len(str(x)), len(str(y))) // 2
    a, b = divmod(x, 10**half); c, d = divmod(y, 10**half)
    ac, bd = karatsuba(a, c), karatsuba(b, d)
    return ac * 10**(2 * half) + (karatsuba(a + b, c + d) - ac - bd) * 10**half + bd
import random
rnd = random.Random(1)
add(all(karatsuba(p, q) == p * q for p, q in ((rnd.randrange(10**40), rnd.randrange(10**40)) for _ in range(200))), True)

# ---------------- sorting-bound
def min_worst_comparisons(m):
    return math.ceil(math.log2(math.factorial(m)))
NUM["sorting-bound/lb-4"] = min_worst_comparisons(4); NUM["sorting-bound/lb-5"] = min_worst_comparisons(5)
add(min_worst_comparisons(3), 3); CHOICE["sorting-bound/guess"] = "3"
add((2**4 < 24 <= 2**5, 2**6 < 120 <= 2**7), (True, True))
def queue_mergesort(a):
    from collections import deque
    q = deque([x] for x in a); merges = 0
    while len(q) > 1:
        x, y = q.popleft(), q.popleft(); out = []
        while x and y: out.append(x.pop(0) if x[0] <= y[0] else y.pop(0))
        q.append(out + x + y); merges += 1
    return q[0], merges
srt, mg = queue_mergesort([10, 2, 3, 1, 13, 5, 7, 6]); add(srt, [1, 2, 3, 5, 6, 7, 10, 13])
NUM["sorting-bound/merges-8"] = mg
add(all(math.factorial(m) >= (m / 2)**(m / 2) for m in range(2, 60)), True)
# 3 items really can be sorted with 3 comparisons in the worst case (and 2 cannot): all 6 orders
def sort3_comparisons(a):
    c = 0; a = list(a)
    for i in range(1, 3):
        j = i
        while j > 0:
            c += 1
            if a[j - 1] > a[j]: a[j - 1], a[j] = a[j], a[j - 1]; j -= 1
            else: break
    return c
add(max(sort3_comparisons(p) for p in itertools.permutations([1, 2, 3])), 3)

# ---------------- quickselect
add(sorted([45, 1, 10, 30, 25])[2], 25); NUM["quickselect/guess"] = sorted([45, 1, 10, 30, 25])[2]
S = [2, 36, 5, 21, 8, 13, 11, 20, 5, 4, 1]; v = 5
SL, Sv, SR = [x for x in S if x < v], [x for x in S if x == v], [x for x in S if x > v]
add((SL, Sv, SR), ([2, 4, 1], [5, 5], [36, 21, 8, 13, 11, 20]))
NUM["quickselect/select-8"] = sorted(S)[7]; add(sorted(SR)[8 - len(SL) - len(Sv) - 1], sorted(S)[7])
NUM["quickselect/select-k"] = 15 - (6 + 2)
E = sp.Symbol("E"); add(sp.solve(sp.Eq(E, 1 + E / 2), E), [2])
add(sum(F(3, 4)**k for k in range(200)) < 4, True)
add(sum(range(50, 101)), 3825)                                       # n + (n−1) + … + n/2 for n = 100: quadratic
def qs_compares(a):
    if len(a) <= 1: return 0
    v_ = a[0]; rest = a[1:]
    return len(rest) + qs_compares([x for x in rest if x < v_]) + qs_compares([x for x in rest if x > v_])
NUM["quickselect/quicksort-worst"] = qs_compares(list(range(1, 11))); add(NUM["quickselect/quicksort-worst"], 10 * 9 // 2)
def quicksort(a):
    if len(a) <= 1: return a
    v_ = rnd.choice(a)
    return quicksort([x for x in a if x < v_]) + [x for x in a if x == v_] + quicksort([x for x in a if x > v_])
add(all(quicksort(l_) == sorted(l_) for l_ in ([rnd.randint(0, 9) for _ in range(rnd.randint(0, 15))] for _ in range(200))), True)
vals = [100 + i for i in range(-5, 6)]; bad = vals[:-1] + [10000]
add((sum(bad) / len(bad) > 100 * 1.5, sorted(bad)[5] == sorted(vals)[5]), (True, True))

# ---------------- strassen
X = sp.Matrix([[1, 2], [3, 4]]); Y = sp.Matrix([[5, 6], [7, 8]])
add((X * Y).tolist(), [[19, 22], [43, 50]]); NUM["strassen/entry-43"] = (X * Y)[1, 0]
CHOICE["strassen/guess"] = "8"
NUM["strassen/mnp"] = 2 * 3 * 4
A_, B_, C_, D_, E_, F_, G_, H_ = sp.symbols("A B C D E F G H", commutative=False)
P1 = A_ * (F_ - H_); P2 = (A_ + B_) * H_; P3 = (C_ + D_) * E_; P4 = D_ * (G_ - E_)
P5 = (A_ + D_) * (E_ + H_); P6 = (B_ - D_) * (G_ + H_); P7 = (A_ - C_) * (E_ + F_)
ex = lambda z: sp.expand(z)
add([ex(P5 + P4 - P2 + P6 - (A_ * E_ + B_ * G_)), ex(P1 + P2 - (A_ * F_ + B_ * H_)),
     ex(P3 + P4 - (C_ * E_ + D_ * G_)), ex(P1 + P5 - P3 - P7 - (C_ * F_ + D_ * H_))], [0, 0, 0, 0])
NUM["strassen/log2-7"] = math.log2(7)
add(round((8 / 7)**10, 2), 3.8); CHOICE["strassen/ratio-1024"] = "约 3.8 倍"
add((X * Y == Y * X), False)

# ---------------- fft
x_ = sp.Symbol("x")
prod = sp.Poly(sp.expand((1 + 2 * x_ + 3 * x_**2) * (2 + x_ + 4 * x_**2)), x_)
add(prod.all_coeffs()[::-1], [2, 5, 12, 11, 12])
NUM["fft/guess"] = prod.coeff_monomial(x_**2); NUM["fft/coef-x3"] = prod.coeff_monomial(x_**3)
NUM["fft/points-needed"] = 2 * 3 + 1
P6_ = 3 + 4 * x_ + 6 * x_**2 + 2 * x_**3 + x_**4 + 10 * x_**5
add(sp.expand((3 + 6 * x_**2 + x_**4) + x_ * (4 + 2 * x_**2 + 10 * x_**4) - P6_), 0)
yy = sp.Symbol("y"); Ae, Ao = 1 + 3 * yy, 2 + 4 * yy
add(sp.expand(Ae.subs(yy, x_**2) + x_ * Ao.subs(yy, x_**2) - (1 + 2 * x_ + 3 * x_**2 + 4 * x_**3)), 0)
CHOICE["fft/even-part"] = "1 + 3y"
roots8 = [sp.exp(2 * sp.pi * sp.I * k / 8) for k in range(8)]
sq = {sp.nsimplify(sp.simplify(r**2)) for r in roots8}; NUM["fft/squares-8"] = len(sq)
add({sp.simplify(z**2) for z in (1, -1, sp.I, -sp.I)}, {1, -1}); add(sp.I**2, -1)
# the FFT of the lesson's recursion multiplies polynomials correctly (plain complex arithmetic)
import cmath
def fft(a, inv=False):
    m = len(a)
    if m == 1: return a[:]
    w = cmath.exp((-2 if inv else 2) * cmath.pi * 1j / m)
    e, o = fft(a[0::2], inv), fft(a[1::2], inv)
    out = [0] * m
    for j in range(m // 2):
        out[j] = e[j] + w**j * o[j]; out[j + m // 2] = e[j] - w**j * o[j]
    return out
fa, fb = fft([1, 2, 3, 0, 0, 0, 0, 0]), fft([2, 1, 4, 0, 0, 0, 0, 0])
back = [round((z / 8).real) for z in fft([p * q for p, q in zip(fa, fb)], inv=True)]
add(back, [2, 5, 12, 11, 12, 0, 0, 0])

# ================= 贪心
# ---------------- activity-selection
def overlap(a, b): return a[0] < b[1] and b[0] < a[1]          # half-open [s, e)
def greedy_acts(acts, key):
    out = []
    for a in sorted(acts, key=key):
        if not any(overlap(a, b) for b in out): out.append(a)
    return out
def best_acts(acts):
    return max(r for r in range(len(acts) + 1) for c in itertools.combinations(acts, r) if not any(overlap(a, b) for a, b in itertools.combinations(c, 2)))
acts = [(1, 3), (2, 5), (4, 7), (1, 8), (5, 9), (8, 10), (9, 11), (11, 14), (13, 16)]
g = greedy_acts(acts, lambda a: a[1]); add(g, [(1, 3), (4, 7), (8, 10), (11, 14)])
NUM["activity-selection/synthesis-count"] = len(g); add(best_acts(acts), len(g))
sh = [(1, 5), (4, 7), (6, 10)]
NUM["activity-selection/shortest-fails"] = len(greedy_acts(sh, lambda a: a[1] - a[0])); add(best_acts(sh), 2)
es = [(0, 10), (1, 2), (3, 4)]; add((len(greedy_acts(es, lambda a: a[0])), best_acts(es)), (1, 2))
rnd = random.Random(7)                     # finish-time greedy is optimal on random instances too
for _ in range(300):
    inst = [(s, s + rnd.randint(1, 6)) for s in (rnd.randint(0, 15) for _ in range(rnd.randint(1, 8)))]
    if len(greedy_acts(inst, lambda a: a[1])) != best_acts(inst): add("finish-time greedy", "optimal"); break
def greedy_coins(cs, a):
    k = 0
    for c in sorted(cs, reverse=True): k += a // c; a %= c
    return k
def opt_coins(cs, a):
    d = [0] + [math.inf] * a
    for x in range(1, a + 1): d[x] = min([d[x - c] + 1 for c in cs if c <= x] + [math.inf])
    return d[a]
add((greedy_coins([1, 20, 50], 60), opt_coins([1, 20, 50], 60)), (11, 3))
NUM["activity-selection/coins-greedy"] = greedy_coins([1, 49, 50], 98); add(opt_coins([1, 49, 50], 98), 2)
def frac_knap(W, items):
    tot = F(0)
    for w, v in sorted(items, key=lambda it: F(it[1], it[0]), reverse=True):
        take = min(w, W); tot += F(v, w) * take; W -= take
    return tot
NUM["activity-selection/fractional"] = frac_knap(50, [(10, 60), (20, 100), (30, 120)])
add([F(v, w) for w, v in [(10, 60), (20, 100), (30, 120)]], [6, 5, 4]); add(F(120) * F(20, 30), 80)

# ---------------- mst-cut
K = nx.Graph(); K.add_weighted_edges_from([("A", "B", 1), ("B", "C", 2), ("A", "C", 3), ("C", "D", 4), ("B", "D", 5), ("D", "E", 6), ("C", "E", 7)])
def kruskal(G):
    par = {v: v for v in G}
    def fd(x):
        while par[x] != x: x = par[x]
        return x
    taken, skipped = [], []
    for u, v, w in sorted(G.edges(data="weight"), key=lambda e: e[2]):
        if len(taken) == len(G) - 1: break
        ru, rv = fd(u), fd(v)
        if ru == rv: skipped.append(f"{u}-{v}")
        else: par[ru] = rv; taken.append((u, v, w))
    return taken, skipped
tk, sk = kruskal(K)
add(sum(w for *_, w in tk), nx.minimum_spanning_tree(K).size(weight="weight")); add(sum(w for *_, w in tk), 13)
TEXT["mst-cut/kruskal-skipped"] = " ".join(sk)
K2 = nx.Graph(); K2.add_weighted_edges_from([("P", "Q", 4), ("P", "R", 1), ("Q", "R", 2), ("Q", "S", 5), ("R", "S", 8), ("P", "S", 6)])
NUM["mst-cut/kruskal-total"] = nx.minimum_spanning_tree(K2).size(weight="weight"); add(kruskal(K2)[1], ["P-Q"])
NUM["mst-cut/mst-edges"] = 50 - 1
CHOICE["mst-cut/guess"] = "7"
ewg = [(4, 5, .35), (4, 7, .37), (5, 7, .28), (0, 7, .16), (1, 5, .32), (0, 4, .38), (2, 3, .17), (1, 7, .19), (0, 2, .26), (1, 2, .36), (1, 3, .29), (2, 7, .34), (6, 2, .40), (3, 6, .52), (6, 0, .58), (6, 4, .93)]
EWG = nx.Graph(); EWG.add_weighted_edges_from(ewg)
add(round(nx.minimum_spanning_tree(EWG).size(weight="weight"), 2), 1.81)   # algs4's tinyEWG.txt

# ---------------- union-find
par, rank_ = {}, {}
def mk(x): par[x] = x; rank_[x] = 0
def find(x):
    while par[x] != x: x = par[x]
    return x
def union(x, y):                     # DPV's rule: on a tie the first argument's root goes under the second's
    rx, ry = find(x), find(y)
    if rx == ry: return
    if rank_[rx] > rank_[ry]: par[ry] = rx
    else:
        par[rx] = ry
        if rank_[rx] == rank_[ry]: rank_[ry] += 1
for c_ in "ABCDEFG": mk(c_)
union("A", "D"); union("B", "E"); union("C", "F")
add([par[c_] for c_ in "ABC"] + [rank_[c_] for c_ in "DEF"], ["D", "E", "F", 1, 1, 1])
union("C", "G"); add(par["G"], "F")
union("E", "A"); add((par["E"], rank_["D"]), ("D", 2))
union("B", "G"); add((par["F"], {find(c_) for c_ in "ABCDEFG"}), ("D", {"D"}))
pp = {"a": "a", "b": "a", "c": "b", "d": "d", "e": "d", "f": "c"}
def find_pp(x):
    while pp[x] != x: x = pp[x]
    return x
TEXT["union-find/find-root"] = find_pp("f"); add(find_pp("e"), "d")
NUM["union-find/max-rank"] = math.floor(math.log2(1000)); add(2**9 <= 1000 < 2**10, True)
for trial in range(50):              # a rank-k root has at least 2^k elements: random union-by-rank runs
    par, rank_ = {}, {}
    for i in range(64): mk(i)
    for _ in range(80): union(rnd.randrange(64), rnd.randrange(64))
    size = {}
    for i in range(64): size[find(i)] = size.get(find(i), 0) + 1
    if any(size[r_] < 2**rank_[r_] for r_ in size): add("rank property", "violated"); break
logstar = lambda m: 0 if m <= 1 else 1 + logstar(math.log2(m))
add(logstar(1000), 4); add(all(logstar(m) <= 5 for m in (10**6, 10**80, 2**65536)), True)

# ---------------- prim
def prim(G, s):
    order, seen, tot = [s], {s}, 0
    while len(seen) < len(G):
        w, u, v = min((d["weight"], u, v) for u in seen for v, d in G[u].items() if v not in seen)
        seen.add(v); order.append(v); tot += w
    return order, tot
add(prim(K, "A"), (["A", "B", "C", "D", "E"], 13))
o_, t_ = prim(K, "E"); TEXT["prim/prim-order"] = " ".join(o_); add(t_, 13)
CHOICE["prim/add-constant"] = "不会变"
K3 = nx.Graph(); K3.add_weighted_edges_from([(u, v, w + 10) for u, v, w in K.edges(data="weight")])
add(sorted(nx.minimum_spanning_tree(K3).edges()), sorted(nx.minimum_spanning_tree(K).edges()))

# ---------------- huffman
def huffman(freq):
    h = [(f, i, {s: ""}) for i, (s, f) in enumerate(freq.items())]; heapq.heapify(h); k = len(h)
    while len(h) > 1:
        f1, _, a = heapq.heappop(h); f2, _, b = heapq.heappop(h)
        m = {s: "0" + c for s, c in a.items()}; m.update({s: "1" + c for s, c in b.items()})
        heapq.heappush(h, (f1 + f2, k, m)); k += 1
    return h[0][2]
def cost(freq, code): return sum(freq[s] * len(code[s]) for s in freq)
dpv = {"A": 70, "B": 3, "C": 20, "D": 37}
add(cost(dpv, huffman(dpv)), 213); add(cost(dpv, {"A": "0", "D": "11", "B": "100", "C": "101"}), 213)
add((sum(dpv.values()) * 2, round((1 - 213 / 260) * 100, 1)), (260, 18.1))   # DPV calls it "a 17% improvement"
def prefix_free(ws): return not any(a != b and b.startswith(a) for a in ws for b in ws)
add([prefix_free(w) for w in (["0", "10", "110", "111"], ["0", "01", "11"], ["1", "10", "100", "1000"])], [True, False, False])
CHOICE["huffman/which-prefix"] = "0、10、110、111"
add(prefix_free(["0", "01", "11", "001"]), False)
NUM["huffman/cost-small"] = cost({"A": 5, "B": 1, "C": 2, "D": 2}, {"A": "0", "B": "110", "C": "111", "D": "10"})
dna = {"A": 31, "C": 20, "G": 9, "T": 40}; hc = huffman(dna)
add({s: len(c) for s, c in hc.items()}, {"T": 1, "A": 2, "C": 3, "G": 3})
NUM["huffman/avg-bits"] = cost(dna, hc) / 100
add(prefix_free(["0", "11", "100", "101"]), True)
q5 = {"a": F(1, 2), "b": F(1, 4), "c": F(1, 8), "d": F(1, 16), "e": F(1, 16)}
add(sorted(len(c) for c in huffman(q5).values()), [1, 2, 3, 4, 4])
NUM["huffman/file-bits"] = cost(q5, huffman(q5)) * 1_000_000

# ---------------- horn
def horn(imps, negs, vars_):
    val = {v: False for v in vars_}
    changed = True
    while changed:
        changed = False
        for lhs, rhs in imps:
            if all(val[x] for x in lhs) and not val[rhs]: val[rhs] = True; changed = True
    return val, all(any(not val[x] for x in neg) for neg in negs)
def sat_assignments(imps, negs, vars_):
    for bits in itertools.product([False, True], repeat=len(vars_)):
        val = dict(zip(vars_, bits))
        if all((not all(val[x] for x in l)) or val[r] for l, r in imps) and all(any(not val[x] for x in n) for n in negs): yield val
brute_sat = lambda *f: any(True for _ in sat_assignments(*f))
CHOICE["horn/guess"] = "不在场"
add({v["z"] for v in sat_assignments([((), "x"), (("x",), "y")], [("y", "z")], "xyz")}, {False})
f1 = ([((), "a"), (("a",), "b"), (("a", "c"), "d")], [("b", "d")], "abcd")
val, ok = horn(*f1); TEXT["horn/horn-true"] = " ".join(v for v in "abcd" if val[v]); add((ok, brute_sat(*f1)), (True, True))
dpvh = ([(("w", "y", "z"), "x"), (("x", "z"), "w"), (("x",), "y"), ((), "x"), (("x", "y"), "w")], [("w", "x", "y"), ("z",)], "wxyz")
val, ok = horn(*dpvh); add(({v for v in "wxyz" if val[v]}, ok, brute_sat(*dpvh)), ({"w", "x", "y"}, False, False))
f3 = ([((), "p"), (("p",), "q"), (("q", "p"), "r"), (("r", "s"), "t")], [("s", "p")], "pqrst")
val, ok = horn(*f3); NUM["horn/horn-count"] = sum(val.values()); add((ok, brute_sat(*f3)), (True, True))
for _ in range(300):                 # the stingy greedy agrees with brute force on random Horn formulas
    vs = "abcde"
    imps = [(tuple(rnd.sample(vs, rnd.randint(0, 2))), rnd.choice(vs)) for _ in range(rnd.randint(1, 6))]
    negs = [tuple(rnd.sample(vs, rnd.randint(1, 3))) for _ in range(rnd.randint(0, 2))]
    val, ok = horn(imps, negs, vs)
    if ok != brute_sat(imps, negs, vs) or any(any(val[x] and not s_[x] for x in vs) for s_ in sat_assignments(imps, negs, vs)):
        add("horn greedy", "matches brute force"); break

# ---------------- set-cover
def greedy_cover(Bset, sets):
    left, picked = set(Bset), []
    while left:
        best = max(sets, key=lambda s: len(left & sets[s])); picked.append(best); left -= sets[best]
    return picked
def opt_cover(Bset, sets):
    return min(r for r in range(1, len(sets) + 1) for c in itertools.combinations(sets, r) if set().union(*(sets[s] for s in c)) >= set(Bset))
sc = {"S1": {1, 2, 3}, "S2": {4, 5, 6}, "S3": {1, 2, 4, 5}}
gp = greedy_cover(range(1, 7), sc); add(gp[0], "S3"); NUM["set-cover/greedy-3"] = len(gp); add(opt_cover(range(1, 7), sc), 2)
NUM["set-cover/bound-1000"] = 5 * math.log(1000); add(round(math.log(1000), 3), 6.908); add(round(math.e, 3), 2.718)
add(all(1 - t < math.exp(-t) for t in (0.001, 0.2, 0.5, 1, 3)), True)
CHOICE["set-cover/guess"] = "不一定"

# ================= 动态规划与摊还分析
# ---------------- dag-dp
dag_e = [("S", "A", 1), ("S", "C", 2), ("C", "A", 4), ("A", "B", 6), ("C", "D", 3), ("B", "D", 1), ("B", "E", 2), ("D", "E", 1)]
DAG = nx.DiGraph(); DAG.add_weighted_edges_from(dag_e)
add(nx.is_directed_acyclic_graph(DAG), True)
topo = ["S", "C", "A", "B", "D", "E"]
add(all(topo.index(u) < topo.index(v) for u, v, _ in dag_e), True)
def dag_paths(pick):
    d = {"S": 0}
    for v in topo[1:]: d[v] = pick(d[u] + w for u, x, w in dag_e if x == v)
    return d
short, long_ = dag_paths(min), dag_paths(max)
add(short, nx.single_source_dijkstra_path_length(DAG, "S"))
CHOICE["dag-dp/guess"] = str(short["E"]); add((short["A"], short["B"]), (1, 7))
NUM["dag-dp/dist-d"] = short["D"]
NUM["dag-dp/longest-e"] = long_["E"]
add(long_["E"], max(sum(DAG[u][v]["weight"] for u, v in zip(p, p[1:])) for p in nx.all_simple_paths(DAG, "S", "E")))
add((long_["C"], long_["A"], long_["B"], long_["D"]), (2, 6, 12, 13))

# ---------------- lis
def lis(a):
    L, prev = [1] * len(a), [None] * len(a)
    for j in range(len(a)):
        for i in range(j):
            if a[i] < a[j] and L[i] + 1 > L[j]: L[j] = L[i] + 1; prev[j] = i
    return L, prev
def lis_brute(a):
    return max(r for r in range(len(a) + 1) for c in itertools.combinations(a, r) if all(x < y for x, y in zip(c, c[1:])))
a = [5, 2, 8, 6, 3, 6, 9, 7]; L, prev = lis(a)
add(L, [1, 1, 2, 2, 2, 3, 4, 4]); NUM["lis/guess"] = max(L); add(lis_brute(a), 4)
j = L.index(4); seq = []
while j is not None: seq.append(a[j]); j = prev[j]
add(seq[::-1], [2, 3, 6, 9])
b_ = [3, 1, 4, 1, 5, 9, 2, 6]; Lb, _ = lis(b_); add(Lb, [1, 1, 2, 1, 3, 4, 2, 4])
NUM["lis/lis-new"] = max(Lb); add(lis_brute(b_), 4)
add([all(x < y for x, y in zip(s_, s_[1:])) for s_ in ([3, 4, 5, 9], [1, 4, 5, 6])], [True, True])
memo = {}
def fibm(m):
    if m <= 1: return m
    if m not in memo: memo[m] = fibm(m - 1) + fibm(m - 2)
    return memo[m]
fibm(30); NUM["lis/memo-size"] = len(memo); add(memo[30], Fib[30])
CHOICE["lis/lis-time"] = "O(n²)"

# ---------------- edit-distance
def edit(x, y):
    m, n = len(x), len(y); E = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1): E[i][0] = i
    for j in range(n + 1): E[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            E[i][j] = min(E[i - 1][j] + 1, E[i][j - 1] + 1, E[i - 1][j - 1] + (x[i - 1] != y[j - 1]))
    return E
def edit_bfs(x, y):                  # independent check: shortest sequence of single edits, by breadth-first search
    alpha = sorted(set(x + y)); seen = {x}; frontier = [x]; d = 0
    while y not in seen:
        nxt = []
        for s in frontier:
            for i in range(len(s) + 1):
                cands = [s[:i] + c + s[i:] for c in alpha]
                if i < len(s): cands += [s[:i] + s[i + 1:]] + [s[:i] + c + s[i + 1:] for c in alpha]
                for t in cands:
                    if t not in seen and len(t) <= max(len(x), len(y)) + 1: seen.add(t); nxt.append(t)
        frontier = nxt; d += 1
    return d
NUM["edit-distance/guess"] = edit("SNOWY", "SUNNY")[-1][-1]; add(edit_bfs("SNOWY", "SUNNY"), 3)
align_l, align_r = "S-NOWY", "SUNN-Y"; add(sum(p != q for p, q in zip(align_l, align_r)), 3)
NUM["edit-distance/kitten"] = edit("kitten", "sitting")[-1][-1]; add(edit_bfs("kitten", "sitting"), 3)
add(edit("AB", "BA"), [[0, 1, 2], [1, 1, 1], [2, 1, 2]])
NUM["edit-distance/expo-poly"] = edit("EXPONENTIAL", "POLYNOMIAL")[-1][-1]
al1, al2 = "EXPONEN-TIAL", "--POLYNOMIAL"; add(sum(p != q for p, q in zip(al1, al2)), 6)
NUM["edit-distance/hello-algo"] = edit("hello", "algo")[-1][-1]; add(edit_bfs("hello", "algo"), 3)
add(["ello", "allo", "algo"], ["hello"[1:], "a" + "ello"[1:], "al" + "g" + "o"])

# ---------------- lcs
def lcs(x, y):
    m, n = len(x), len(y); L = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            L[i][j] = L[i - 1][j - 1] + 1 if x[i - 1] == y[j - 1] else max(L[i - 1][j], L[i][j - 1])
    return L[m][n]
def is_subseq(s, t): it = iter(t); return all(ch in it for ch in s)
def all_lcs(x, y):
    k = lcs(x, y)
    return {"".join(x[i] for i in c) for c in itertools.combinations(range(len(x)), k) if is_subseq("".join(x[i] for i in c), y)}
add(lcs("ABCBDAB", "BDCABA"), 4); CHOICE["lcs/guess"] = "4"
add(sorted(all_lcs("ABCBDAB", "BDCABA")), ["BCAB", "BCBA", "BDAB"])
NUM["lcs/lcs-new"] = lcs("AGGTAB", "GXTXAYB"); add(is_subseq("GTAB", "AGGTAB") and is_subseq("GTAB", "GXTXAYB"), True)
TEXT["lcs/lcs-text"] = "ABD"; add(all_lcs("ABCD", "ACBD"), {"ABD", "ACD"})
def insdel(x, y):                    # independent: BFS over insert/delete only
    alpha = sorted(set(x + y)); seen = {x}; frontier = [x]; d = 0
    while y not in seen:
        nxt = []
        for s in frontier:
            for i in range(len(s) + 1):
                for t in [s[:i] + c + s[i:] for c in alpha] + ([s[:i] + s[i + 1:]] if i < len(s) else []):
                    if t not in seen and len(t) <= 8: seen.add(t); nxt.append(t)
        frontier = nxt; d += 1
    return d
NUM["lcs/ins-del"] = 7 + 6 - 2 * lcs("ABCBDAB", "BDCABA"); add(insdel("ABCBDAB", "BDCABA"), NUM["lcs/ins-del"])

# ---------------- knapsack
goods = [(6, 30), (3, 14), (4, 16), (2, 9)]
Krep = [0] * 11
for w in range(1, 11): Krep[w] = max([Krep[w - wi] + vi for wi, vi in goods if wi <= w] + [0])
add(Krep, [0, 0, 9, 14, 18, 23, 30, 32, 39, 44, 48])
add([Krep[4] + 30, Krep[7] + 14, Krep[6] + 16, Krep[8] + 9], [48, 46, 46, 48])
NUM["knapsack/rep-8"] = Krep[8]; add([Krep[2] + 30, Krep[5] + 14, Krep[4] + 16, Krep[6] + 9], [39, 37, 34, 39])
def k01(W): return max(sum(v for _, v in c) for r in range(5) for c in itertools.combinations(goods, r) if sum(w for w, _ in c) <= W)
def k01_table(W):
    K = [[0] * (len(goods) + 1) for _ in range(W + 1)]
    for jj in range(1, len(goods) + 1):
        wj, vj = goods[jj - 1]
        for w in range(1, W + 1):
            K[w][jj] = K[w][jj - 1] if wj > w else max(K[w][jj - 1], K[w - wj][jj - 1] + vj)
    return K[W][len(goods)]
add((k01(10), k01_table(10)), (46, 46)); CHOICE["knapsack/guess"] = "46 元"
NUM["knapsack/once-9"] = k01_table(9); add(k01(9), 44)
add(sorted(sum(v for _, v in c) for c in ([(6, 30), (2, 9)], [(4, 16), (3, 14), (2, 9)])), [39, 39])

# ---------------- chain-matrix
def chain(m):
    n = len(m) - 1; C = {(i, i): 0 for i in range(1, n + 1)}
    for s in range(1, n):
        for i in range(1, n - s + 1):
            j = i + s; C[i, j] = min(C[i, k] + C[k + 1, j] + m[i - 1] * m[k] * m[j] for k in range(i, j))
    return C[1, n]
def all_orders(dims):                # every parenthesization: (cost, rows, cols)
    if len(dims) == 1: return [(0,) + dims[0]]
    out = []
    for k in range(1, len(dims)):
        for c1, r1, k1 in all_orders(dims[:k]):
            for c2, r2, k2 in all_orders(dims[k:]): out.append((c1 + c2 + r1 * k1 * k2, r1, k2))
    return out
ABCD = [(50, 20), (20, 1), (1, 10), (10, 100)]
add(sorted({c for c, *_ in all_orders(ABCD)}), [7000, 51500, 60200, 103000, 120200])   # all 5 orders
add(chain([50, 20, 1, 10, 100]), 7000)
add((20 * 1 * 10 + 20 * 10 * 100 + 50 * 20 * 100, 20 * 1 * 10 + 50 * 20 * 10 + 50 * 10 * 100, 50 * 20 * 1 + 1 * 10 * 100 + 50 * 1 * 100), (120200, 60200, 7000))
add(min([50 * 20 * 1, 20 * 1 * 10, 1 * 10 * 100]), 20 * 1 * 10)   # the cheapest first product is B × C: the greedy's choice
NUM["chain-matrix/left-to-right"] = 50 * 20 * 1 + 50 * 1 * 10 + 50 * 10 * 100
NUM["chain-matrix/three-chain"] = chain([10, 30, 5, 60]); add(sorted(c for c, *_ in all_orders([(10, 30), (30, 5), (5, 60)])), [4500, 27000])
add(round(120200 / 7000, 1), 17.2)   # "best and worst differ by more than 17 times"

# ---------------- hops-tsp
def hops(E_, s, t, k):
    d = {s: 0}; best = math.inf
    for _ in range(k):
        nd = {}
        for u, v, w in E_:
            if u in d: nd[v] = min(nd.get(v, math.inf), d[u] + w)
        d = nd; best = min(best, d.get(t, math.inf))
    return best
E2 = [("S", "A", 1), ("A", "B", 1), ("B", "C", 1), ("C", "T", 1), ("S", "D", 3), ("D", "T", 3)]
add((hops(E2, "S", "T", 2), hops(E2, "S", "T", 4)), (6, 4)); CHOICE["hops-tsp/guess"] = "6"
E3 = E2 + [("S", "B", 3)]
NUM["hops-tsp/hops-3"] = hops(E3, "S", "T", 3); add((hops(E3, "S", "T", 2), hops(E3, "S", "T", 10)), (6, 4))
dist4 = {(1, 2): 2, (1, 3): 9, (1, 4): 10, (2, 3): 6, (2, 4): 4, (3, 4): 8}
dd = lambda p, q: dist4[(min(p, q), max(p, q))]
tour = lambda t: sum(dd(t[i], t[(i + 1) % len(t)]) for i in range(len(t)))
add(sorted({tour((1,) + p) for p in itertools.permutations([2, 3, 4])}), [23, 26, 29])
def held_karp(n, d):
    C = {(frozenset([1]), 1): 0}
    for s in range(2, n + 1):
        for S_ in itertools.combinations(range(2, n + 1), s - 1):
            S_ = frozenset((1,) + S_)
            for j in S_ - {1}: C[S_, j] = min(C.get((S_ - {j}, i), math.inf) + d(i, j) for i in S_ if i != j)
    full = frozenset(range(1, n + 1))
    return min(C[full, j] + d(j, 1) for j in full - {1})
NUM["hops-tsp/tsp-4"] = held_karp(4, dd); add(NUM["hops-tsp/tsp-4"], min(tour((1,) + p) for p in itertools.permutations([2, 3, 4])))
add((math.factorial(19), 400 * 2**20), (121645100408832000, 419430400)); CHOICE["hops-tsp/tsp-growth"] = "约 4 × 10⁸"
add(round(math.factorial(19) / (400 * 2**20) / 1e8, 1), 2.9)

# ---------------- tree-independent-set
def mis(G):
    nodes = list(G)
    return max(r for r in range(len(nodes) + 1) for c in itertools.combinations(nodes, r) if not any(G.has_edge(u, v) for u, v in itertools.combinations(c, 2)))
def tree_I(G, root):
    parent_ = {root: None}
    for u, v in nx.bfs_edges(G, root): parent_[v] = u
    kids = {u: [v for v in G[u] if v != parent_[u]] for u in G}
    memo_ = {}
    def I(u):
        if u not in memo_:
            ch = kids.get(u, []); gc = [w for c in ch for w in kids.get(c, [])]
            memo_[u] = max(1 + sum(I(w) for w in gc), sum(I(c) for c in ch))
        return memo_[u]
    return I(root), memo_
TR = nx.Graph([("r", "a"), ("r", "b"), ("a", "c"), ("a", "d"), ("b", "e"), ("e", "f")])
val_, memo_ = tree_I(TR, "r")
add((val_, mis(TR)), (4, 4)); add({k: memo_[k] for k in "cdfeab"}, {"c": 1, "d": 1, "f": 1, "e": 1, "a": 2, "b": 2})
P7 = nx.path_graph(range(1, 8)); NUM["tree-independent-set/guess"] = mis(P7)
v7, m7 = tree_I(P7, 1); NUM["tree-independent-set/path-7"] = v7; add([m7[k] for k in range(7, 0, -1)], [1, 1, 2, 2, 3, 3, 4])
ST = nx.star_graph(5); NUM["tree-independent-set/star"] = tree_I(ST, 0)[0]; add(mis(ST), 5)
for _ in range(40):                  # the recurrence agrees with brute force on random trees
    RT = nx.random_labeled_tree(rnd.randint(1, 10), seed=rnd.randrange(10**6))
    if tree_I(RT, 0)[0] != mis(RT): add("tree recurrence", "matches brute force"); break

# ---------------- amortized-counter
def flips(n):
    x = tot = 0
    for _ in range(n): tot += bin(x ^ (x + 1)).count("1"); x += 1
    return tot
add(flips(16), 31); add(flips(16) < 32, True); CHOICE["amortized-counter/guess"] = "不到 32 位"
NUM["amortized-counter/flips-0111"] = bin(0b0111 ^ 0b1000).count("1")
NUM["amortized-counter/flips-16"] = flips(16); add(16 + 8 + 4 + 2 + 1, 31)
add([bin(k)[2:] for k in range(1, 6)], ["1", "10", "11", "100", "101"])
add(all(flips(m) < 2 * m for m in range(1, 2000)), True)
st, popped = [], 0
def multipop(k):
    global popped
    for _ in range(min(k, len(st))): st.pop(); popped += 1
for i in range(10): st.append(i)
multipop(4)
for i in range(3): st.append(i)
multipop(20); NUM["amortized-counter/multipop"] = popped; add(len(st), 0)

# ---------------- potential-method
ones = lambda x: bin(x).count("1")
actual = bin(0b1011 ^ 0b1100).count("1"); add(actual, 3)
NUM["potential-method/potential-one"] = actual + ones(0b1100) - ones(0b1011)
add(all(bin(x ^ (x + 1)).count("1") + ones(x + 1) - ones(x) == 2 for x in range(5000)), True)
CHOICE["potential-method/guess"] = "计数器里 1 的个数"
def append_costs(n0):
    n, c, out = 0, 1, []
    for _ in range(n0):
        real = 1
        if n == c: real += n; c *= 2
        phi_before = 2 * n - (c if real == 1 else c // 2)
        n += 1; out.append(real + (2 * n - c) - phi_before)
    return out
add(set(append_costs(200)[1:]), {3})                   # every append after the first has amortized cost 3
nn_ = sp.Symbol("n"); NUM["potential-method/append-amortized"] = sp.expand((nn_ + 1) + (2 * (nn_ + 1) - 2 * nn_) - (2 * nn_ - nn_))
add(sp.expand(1 + (2 * (nn_ + 1) - 2 * nn_)), 3)        # no resize: real cost 1, ΔΦ = 2
cap, n_el, total = 1, 0, 0
for _ in range(16):
    if n_el == cap: total += n_el; cap *= 2
    total += 1; n_el += 1
NUM["potential-method/append-16"] = total; add(total <= 3 * 16, True)

# ================= 图的遍历
# ---------------- components
tinyG = [(0, 5), (4, 3), (0, 1), (9, 12), (6, 4), (5, 4), (0, 2), (11, 12), (9, 10), (0, 6), (7, 8), (9, 11), (5, 3)]
TG = nx.Graph(); TG.add_nodes_from(range(13)); TG.add_edges_from(tinyG)
add(sorted(nx.node_connected_component(TG, 0)), [0, 1, 2, 3, 4, 5, 6]); CHOICE["components/guess"] = "图不连通，剩下 6 个顶点在别的块里"
def cc_ids(n, edges):                # the lesson's method: DFS from each unmarked vertex, one id per call
    adj = {v: [] for v in range(n)}
    for u, v in edges: adj[u].append(v); adj[v].append(u)
    comp, c = [None] * n, 0
    for s in range(n):
        if comp[s] is None:
            stack = [s]; comp[s] = c
            while stack:
                v = stack.pop()
                for w in adj[v]:
                    if comp[w] is None: comp[w] = c; stack.append(w)
            c += 1
    return comp, c
ids, ncc = cc_ids(13, tinyG); NUM["components/tiny-g"] = ncc; add(ncc, nx.number_connected_components(TG))
tinyCG = [(0, 5), (2, 4), (2, 3), (1, 2), (0, 1), (3, 4), (3, 5), (0, 2)]
CG = nx.Graph(tinyCG); dist_to = [nx.shortest_path_length(CG, 0, v) for v in range(6)]
add(dist_to, [0, 1, 1, 2, 2, 1]); NUM["components/dist-to"] = dist_to[4]
add([nx.is_bipartite(nx.cycle_graph(k)) for k in (4, 3, 5)], [True, False, False])
CHOICE["components/bipartite-which"] = "4 个点围成一圈（正方形的四条边）"
for _ in range(100):                 # bipartite iff no odd cycle, on random small graphs
    RG = nx.gnp_random_graph(7, 0.35, seed=rnd.randrange(10**6))
    odd = any(len(c) % 2 == 1 for c in nx.cycle_basis(RG)) or any(len(c) % 2 == 1 for c in nx.simple_cycles(RG.to_directed()) if len(c) > 2)
    if nx.is_bipartite(RG) == odd: add("bipartite", "iff no odd cycle"); break

# ---------------- topo-dfs
def dfs_post(adj, order):
    post, seen = [], set()
    def dfs(v):
        seen.add(v)
        for w in adj[v]:
            if w not in seen: dfs(w)
        post.append(v)
    for v in order:
        if v not in seen: dfs(v)
    return post
adj5 = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": [], "e": ["c"]}
p5 = dfs_post(adj5, "abcde"); add(p5, ["d", "b", "c", "a", "e"]); rp5 = p5[::-1]; add(rp5, ["e", "a", "c", "b", "d"])
add(all(rp5.index(u) < rp5.index(v) for u in adj5 for v in adj5[u]), True)
adjp = {"p": ["q", "r"], "q": ["s"], "r": ["s"], "s": [], "t": ["p"]}
pp_ = dfs_post(adjp, "pqrst"); TEXT["topo-dfs/rev-post"] = " ".join(pp_[::-1])
add(all(pp_[::-1].index(u) < pp_[::-1].index(v) for u in adjp for v in adjp[u]), True)
topo_e = [("p", "q"), ("p", "s"), ("r", "s"), ("q", "t"), ("s", "t"), ("t", "u"), ("q", "u")]
TD = nx.DiGraph(topo_e); add(nx.is_directed_acyclic_graph(TD), True)
sol = ["p", "r", "q", "s", "t", "u"]; add(all(sol.index(u) < sol.index(v) for u, v in topo_e), True)
alt = ["r", "p", "s", "q", "t", "u"]; add(all(alt.index(u) < alt.index(v) for u, v in topo_e), True)
add(all(p5.index(v) < p5.index(u) for u in adj5 for v in adj5[u]), True)   # postorder puts every edge's head first
for _ in range(100):                 # reverse postorder is a topological order on random DAGs
    nodes = list(range(8)); E_ = [(i, j) for i in nodes for j in nodes if i < j and rnd.random() < 0.3]
    perm = nodes[:]; rnd.shuffle(perm); E_ = [(perm[i], perm[j]) for i, j in E_]
    adj_ = {v: [w for u, w in E_ if u == v] for v in nodes}
    rp = dfs_post(adj_, nodes)[::-1]
    if not all(rp.index(u) < rp.index(v) for u, v in E_): add("reverse postorder", "topological"); break
# algs4's tinyDAG7 (its trace dfs(0) → dfs(1) → dfs(4) has the edge 1→4; Bag order = reverse insertion)
E7 = [(0, 5), (0, 2), (0, 1), (3, 6), (3, 5), (3, 4), (5, 2), (6, 4), (6, 0), (3, 2), (1, 4)]
adj7 = {v: [] for v in range(7)}
for u, v in E7: adj7[u].insert(0, v)
p7 = dfs_post(adj7, range(7)); add((p7, p7[::-1]), ([4, 1, 2, 5, 0, 6, 3], [3, 6, 0, 5, 2, 1, 4]))

# ---------------- scc
add(nx.has_path(nx.DiGraph([(1, 2), (2, 3), (3, 1), (3, 4)]), 4, 1), False); CHOICE["scc/guess"] = "不能"
OWN = nx.DiGraph([(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 6), (6, 4), (6, 7)])
NUM["scc/own-scc"] = nx.number_strongly_connected_components(OWN)
tinyDG = [(4, 2), (2, 3), (3, 2), (6, 0), (0, 1), (2, 0), (11, 12), (12, 9), (9, 10), (9, 11), (7, 9), (10, 12), (11, 4), (4, 3), (3, 5), (6, 8), (8, 6), (5, 4), (0, 5), (6, 4), (6, 9), (7, 6)]
add(len(tinyDG), 22)
DG = nx.DiGraph(tinyDG)
def kosaraju(G):
    rev = {v: [] for v in G}; fwd = {v: [] for v in G}
    for u, v in G.edges(): rev[v].append(u); fwd[u].append(v)
    order = dfs_post(rev, sorted(G))[::-1]
    comp, seen = [], set()
    for s in order:
        if s in seen: continue
        cur, stack = [], [s]; seen.add(s)
        while stack:
            v = stack.pop(); cur.append(v)
            for w in fwd[v]:
                if w not in seen: seen.add(w); stack.append(w)
        comp.append(sorted(cur))
    return sorted(comp)
add(kosaraju(DG), sorted(sorted(c) for c in nx.strongly_connected_components(DG)))
add(kosaraju(DG), [[0, 2, 3, 4, 5], [1], [6, 8], [7], [9, 10, 11, 12]])
NUM["scc/tiny-dg"] = len(kosaraju(DG)); add(kosaraju(OWN), [[1, 2, 3], [4, 5, 6], [7]])
add(nx.number_strongly_connected_components(nx.DiGraph([(i, j) for i in range(10) for j in range(10) if i < j])), 10)
CHOICE["scc/dag-scc"] = "10 个，每个顶点自己一个"
add(kosaraju(DG.reverse()), kosaraju(DG)); CHOICE["scc/scc-reverse"] = "不变"

# ================= 最短路
# ---------------- dijkstra
def dijkstra(E_, s):
    g = {}
    for u, v, w in E_: g.setdefault(u, []).append((v, w))
    dist, done, pq = {s: 0}, [], [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if u in done: continue
        done.append(u)
        for v, w in g.get(u, []):
            if v not in done and d + w < dist.get(v, math.inf): dist[v] = d + w; heapq.heappush(pq, (d + w, v))
    return dist, done
syn = [("s", "a", 4), ("s", "b", 1), ("b", "a", 2), ("a", "c", 1), ("b", "c", 5), ("c", "t", 3), ("a", "t", 6)]
dsyn, osyn = dijkstra(syn, "s"); add((dsyn, osyn), ({"s": 0, "b": 1, "a": 3, "c": 4, "t": 7}, ["s", "b", "a", "c", "t"]))
NUM["dijkstra/guess"] = dsyn["t"]; SYN = nx.DiGraph(); SYN.add_weighted_edges_from(syn)
add(nx.shortest_path(SYN, "s", "t", weight="weight"), ["s", "b", "a", "c", "t"])
it_e = [("s", "a", 2), ("s", "b", 5), ("a", "b", 1), ("a", "c", 6), ("b", "c", 2), ("b", "d", 7), ("c", "d", 1), ("c", "t", 5), ("d", "t", 2)]
dit, oit = dijkstra(it_e, "s"); add(oit, ["s", "a", "b", "c", "d", "t"]); add(dit, {"s": 0, "a": 2, "b": 3, "c": 5, "d": 6, "t": 8})
add(len(set(dit.values())), len(dit))                                # no ties: the order is unique
ewd = [(4, 5, .35), (5, 4, .35), (4, 7, .37), (5, 7, .28), (7, 5, .28), (5, 1, .32), (0, 4, .38), (0, 2, .26), (7, 3, .39), (1, 3, .29), (2, 7, .34), (6, 2, .40), (3, 6, .52), (6, 0, .58), (6, 4, .93)]
EWD = nx.DiGraph(); EWD.add_weighted_edges_from(ewd)
NUM["dijkstra/tiny-ewd"] = 0.26 + 0.34 + 0.39 + 0.52
add(round(nx.shortest_path_length(EWD, 0, 6, weight="weight"), 2), 1.51); add(nx.shortest_path(EWD, 0, 6, weight="weight"), [0, 2, 7, 3, 6])
add({v: round(d, 2) for v, d in nx.single_source_dijkstra_path_length(EWD, 0).items()}, {0: 0, 1: 1.05, 2: 0.26, 3: 0.99, 4: 0.38, 5: 0.73, 6: 1.51, 7: 0.6})
TRI = nx.Graph(); TRI.add_weighted_edges_from([("s", "b", 3), ("s", "a", 2), ("a", "b", 2)])
add(sorted(map(sorted, nx.minimum_spanning_tree(TRI).edges())), [["a", "b"], ["a", "s"]])
spt = nx.single_source_dijkstra_path(TRI, "s"); add((spt["a"], spt["b"]), (["s", "a"], ["s", "b"]))

# ---------------- negative-edges
neg = [("s", "a", 2), ("s", "b", 3), ("b", "a", -2)]
dn, on = dijkstra(neg, "s"); add((dn["a"], on), (2, ["s", "a", "b"]))
NEG = nx.DiGraph(); NEG.add_weighted_edges_from(neg)
add(nx.single_source_bellman_ford_path_length(NEG, "s")["a"], 1); CHOICE["negative-edges/guess"] = "1"
def bellman_ford_rounds(n, E_, s):
    d = {s: 0}; rounds = 0
    while True:
        changed = False
        for u, v, w in E_:
            if u in d and d[u] + w < d.get(v, math.inf): d[v] = d[u] + w; changed = True
        if not changed: return d, rounds
        rounds += 1
chain_e = [("c", "d", 1), ("b", "c", 1), ("a", "b", 1), ("s", "a", 1)]
dch, rch = bellman_ford_rounds(5, chain_e, "s"); add((dch["d"], rch), (4, 4))
NUM["negative-edges/bf-rounds"] = 6 - 1
SQ = nx.DiGraph(); SQ.add_weighted_edges_from([("s", "a", 1), ("a", "t", 1), ("s", "t", 3)])
SQ2 = nx.DiGraph(); SQ2.add_weighted_edges_from([(u, v, w + 2) for u, v, w in SQ.edges(data="weight")])
add((nx.shortest_path(SQ, "s", "t", weight="weight"), nx.shortest_path(SQ2, "s", "t", weight="weight")), (["s", "a", "t"], ["s", "t"]))
CHOICE["negative-edges/add-constant-sp"] = "可能变：边数多的路被多加了好几次"
NUM["negative-edges/arbitrage"] = 1000 * 0.741 * 1.366 * 0.995
add((round(1000 * 0.741, 3), round(741 * 1.366, 3)), (741.0, 1012.206))
add(sum(-math.log(r) for r in (0.741, 1.366, 0.995)) < 0, True)
DAGN = nx.DiGraph(); DAGN.add_weighted_edges_from([("s", "a", 3), ("s", "b", 1), ("a", "b", -4), ("b", "c", 2)])
add(nx.single_source_bellman_ford_path_length(DAGN, "s")["c"], 1)                # topological-order relaxation on a DAG with a negative edge
dd_ = {"s": 0}
for v in ["a", "b", "c"]: dd_[v] = min(dd_[u] + w for u, x, w in DAGN.edges(data="weight") if x == v and u in dd_)
add(dd_["c"], 1)

# ---------------- floyd-warshall
fw_e = [(1, 2, 4), (1, 3, 1), (3, 2, 2), (2, 4, 1), (3, 4, 5)]
def floyd(n, E_):
    d = [[0 if i == j else math.inf for j in range(n + 1)] for i in range(n + 1)]
    for u, v, w in E_: d[u][v] = min(d[u][v], w)
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if d[i][k] + d[k][j] < d[i][j]: d[i][j] = d[i][k] + d[k][j]
    return d
fw = floyd(4, fw_e); NUM["floyd-warshall/fw-14"] = fw[1][4]
FWG = nx.DiGraph(); FWG.add_weighted_edges_from(fw_e); add(nx.shortest_path_length(FWG, 1, 4, weight="weight"), fw[1][4])
add((1 + 5, 1 + 2 + 1), (6, 4))
# k in the inner loop gives a wrong answer on some graph (why it must be outermost)
def floyd_k_inner(n, E_):
    d = [[0 if i == j else math.inf for j in range(n + 1)] for i in range(n + 1)]
    for u, v, w in E_: d[u][v] = min(d[u][v], w)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            for k in range(1, n + 1):
                if d[i][k] + d[k][j] < d[i][j]: d[i][j] = d[i][k] + d[k][j]
    return d
bad_e = next(E_ for E_ in ([(u, v, rnd.randint(1, 5)) for u in range(1, 6) for v in range(1, 6) if u != v and rnd.random() < 0.3] for _ in range(2000))
             if floyd(5, E_) != floyd_k_inner(5, E_))
add(floyd(5, bad_e) != floyd_k_inner(5, bad_e), True)
G_ = nx.DiGraph(); G_.add_nodes_from(range(1, 6)); G_.add_weighted_edges_from(bad_e)
nxd = dict(nx.all_pairs_dijkstra_path_length(G_))
add(all(floyd(5, bad_e)[i_][j_] == nxd[i_].get(j_, math.inf) for i_ in range(1, 6) for j_ in range(1, 6)), True)
cyc = floyd(3, [(1, 2, 1), (2, 3, -3), (3, 1, 1)]); add(min(cyc[i][i] for i in (1, 2, 3)) < 0, True)
CHOICE["floyd-warshall/neg-cycle-diag"] = "某个 d[i][i] 变成了负数"

TC = nx.transitive_closure(nx.DiGraph([(1, 2), (2, 3), (3, 4)]), reflexive=False)
NUM["floyd-warshall/closure-count"] = TC.number_of_edges()
def closure_fw(n, E_):
    r = [[False] * (n + 1) for _ in range(n + 1)]
    for u, v in E_: r[u][v] = True
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1): r[i][j] = r[i][j] or (r[i][k] and r[k][j])
    return {(i, j) for i in range(1, n + 1) for j in range(1, n + 1) if r[i][j] and i != j}
add(closure_fw(4, [(1, 2), (2, 3), (3, 4)]), set(TC.edges()))

# ================= 网络流与匹配
def maxflow(edges, s="s", t="t"):
    G_ = nx.DiGraph()
    for u, v, c in edges: G_.add_edge(u, v, capacity=c)
    return nx.maximum_flow_value(G_, s, t)
def ff_paths(edges, paths):          # push each augmenting path's bottleneck in the residual network, as the sim does
    cap = {(u, v): c for u, v, c in edges}; flow = {k: 0 for k in cap}; total = 0
    def resid(u, v): return cap[(u, v)] - flow[(u, v)] if (u, v) in cap else flow.get((v, u), 0)
    for p in paths:
        b = min(resid(u, v) for u, v in zip(p, p[1:])); assert b > 0
        for u, v in zip(p, p[1:]):
            if (u, v) in cap: flow[(u, v)] += b
            else: flow[(v, u)] -= b
        total += b
    return total, flow
lab = [("s", "a", 1), ("s", "b", 1), ("a", "b", 1), ("a", "t", 1), ("b", "t", 1)]
add(maxflow(lab), 2); CHOICE["max-flow/guess"] = "2 升"
tot, fl = ff_paths(lab, [["s", "a", "b", "t"], ["s", "b", "a", "t"]]); add((tot, fl[("a", "b")]), (2, 0))
CHOICE["max-flow/undo-why"] = "把 a→b 上的那 1 升退回去，让它改走 a→t"
NUM["max-flow/conservation"] = (2 + 3 + 1) - 4
fn = [("s", "a", 2), ("s", "b", 3), ("a", "c", 3), ("a", "d", 1), ("b", "c", 1), ("b", "d", 1), ("c", "t", 2), ("d", "t", 3)]
add(maxflow(fn), 4)
tot, fl = ff_paths(fn, [["s", "a", "c", "t"], ["s", "b", "d", "t"], ["s", "b", "c", "a", "d", "t"]]); add((tot, fl[("a", "c")]), (4, 1))

# ---------------- min-cut
def cut_cap(edges, A): return sum(c for u, v, c in edges if u in A and v not in A)
NUM["min-cut/cut-cap"] = cut_cap(fn, {"s", "b"}); add(NUM["min-cut/cut-cap"], maxflow(fn))
add(cut_cap(fn, {"s", "a", "b", "c"}), 4)
add(min(cut_cap(fn, {"s"} | set(A_)) for r in range(5) for A_ in itertools.combinations("abcd", r)), maxflow(fn))
CHOICE["min-cut/guess"] = "不可能"
tot, fl = ff_paths(lab, [["s", "a", "t"], ["s", "b", "t"]])
res_reach = {"s"} | {v for (u, v), c in {(u, v): c for u, v, c in lab}.items() if u == "s" and c - fl[(u, v)] > 0}
add((res_reach, cut_cap(lab, res_reach)), ({"s"}, 2)); CHOICE["min-cut/find-cut"] = "只有 s 自己；割 {s} 的容量是 2"
bad = [("s", "a", 1000), ("s", "b", 1000), ("a", "t", 1000), ("b", "t", 1000), ("a", "b", 1)]
add(maxflow(bad), 2000); NUM["min-cut/bad-paths"] = maxflow(bad)
alt_paths = [["s", "a", "b", "t"] if i % 2 == 0 else ["s", "b", "a", "t"] for i in range(2000)]
add(ff_paths(bad, alt_paths)[0], 2000)
add(maxflow([("s", "a", 100), ("s", "b", 100), ("a", "t", 100), ("b", "t", 100), ("a", "b", 1)]), 200)
CHOICE["min-cut/integer-flow"] = "一定存在每条边流量都是整数的最大流"

# ---------------- bipartite-matching
def max_matching(left, edges):
    B_ = nx.Graph(edges); B_.add_nodes_from(left)
    return len(nx.bipartite.maximum_matching(B_, top_nodes=left)) // 2, B_
mm, B4 = max_matching(["A", "B", "C", "D"], [("A", "w"), ("A", "x"), ("B", "w"), ("C", "x"), ("C", "y"), ("D", "y")])
NUM["bipartite-matching/guess"] = mm
def min_cover(G_):
    nodes = list(G_)
    return min(r for r in range(len(nodes) + 1) for c in itertools.combinations(nodes, r) if all(u in c or v in c for u, v in G_.edges()))
NUM["bipartite-matching/cover-size"] = min_cover(B4); add(min_cover(B4), mm)
add(all(u in {"w", "x", "y"} or v in {"w", "x", "y"} for u, v in B4.edges()), True)
mf_edges = [("s", l_, 1) for l_ in "123"] + [(u, v, 1) for u, v in [("1", "x"), ("1", "y"), ("2", "x"), ("3", "x")]] + [(r_, "t", 1) for r_ in "xyz"]
NUM["bipartite-matching/match-flow"] = maxflow(mf_edges); add(max_matching(["1", "2", "3"], [("1", "x"), ("1", "y"), ("2", "x"), ("3", "x")])[0], 2)
before = {("A", "x")}; path = [("B", "x"), ("x", "A"), ("A", "y")]
after = {frozenset(e) for e in before} ^ {frozenset(e) for e in path}
add(after, {frozenset(("B", "x")), frozenset(("A", "y"))}); CHOICE["bipartite-matching/alternating"] = "{B-x, A-y}"
for _ in range(60):                  # König: in bipartite graphs max matching = min vertex cover
    Lr, Rr = ["L%d" % i for i in range(4)], ["R%d" % i for i in range(4)]
    E_ = [(l_, r_) for l_ in Lr for r_ in Rr if rnd.random() < 0.35]
    if not E_: continue
    m_, G_ = max_matching(Lr, E_)
    if m_ != min_cover(nx.Graph(E_)): add("König", "holds"); break

# ================= 字符串匹配与索引
# ---------------- substring-search
def brute(txt, pat):
    c = 0
    for i in range(len(txt) - len(pat) + 1):
        j = 0
        while j < len(pat):
            c += 1
            if txt[i + j] != pat[j]: break
            j += 1
        if j == len(pat): return i, c
    return None, c
add(brute("A" * 20 + "B", "AAAAAB"), (15, 96)); CHOICE["substring-search/guess"] = "约 100 次"
add(15 * 6 + 6, 96)
pos, cnt = brute("ABABDABABCABABCABAB", "ABABCABAB"); add(pos, 5); NUM["substring-search/brute-count"] = cnt
txt = "3141592653589793"
add([int(txt[i:i + 5]) % 997 for i in range(7)], [508, 201, 715, 971, 442, 929, 613]); add(int("26535") % 997, 613)
add(txt.find("26535"), 6)
hh = 0; seqh = []
for ch in "26535": hh = (hh * 10 + int(ch)) % 997; seqh.append(hh)
add(seqh, [2, 26, 265, 659, 613])
add(((508 + 3 * (997 - 30)) * 10 + 9) % 997, 201); add(10000 % 997, 30)
NUM["substring-search/window-hash"] = 41592 % 997; add(997 * 41, 40877)
CHOICE["substring-search/rk-collision"] = "结果一定对，只是运气极差时会变慢"
def bm(txt_, pat):
    right = {}
    for j, c_ in enumerate(pat): right[c_] = j
    i, trace = 0, []
    while i <= len(txt_) - len(pat):
        skip = 0
        for j in range(len(pat) - 1, -1, -1):
            if pat[j] != txt_[i + j]: trace.append((i, j)); skip = max(1, j - right.get(txt_[i + j], -1)); break
        if skip == 0: return i, trace, right
        i += skip
    return None, trace, right
pos, trace, right = bm("FINDINAHAYSTACKNEEDLEINA", "NEEDLE")
add((pos, trace), (15, [(0, 5), (5, 5), (11, 4)])); add(right, {"N": 0, "E": 5, "D": 3, "L": 4})
NUM["substring-search/right-e"] = right["E"]

# ---------------- prefix-function
def prefix(s):
    pi = [0] * len(s)
    for i in range(1, len(s)):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]: j = pi[j - 1]
        if s[i] == s[j]: j = j + 1
        pi[i] = j
    return pi
def prefix_brute(s): return [max(k for k in range(i + 1) if s[:k] == s[i + 1 - k:i + 1] and k <= i) for i in range(len(s))]
add(prefix("ABABAB")[-1], 4); CHOICE["prefix-function/guess"] = "4（ABAB）"
add(prefix("ABABCABAB"), [0, 0, 1, 2, 0, 1, 2, 3, 4]); add(prefix_brute("ABABCABAB"), [0, 0, 1, 2, 0, 1, 2, 3, 4])
TEXT["prefix-function/pi-aabaab"] = " ".join(map(str, prefix("AABAAB"))); add(prefix_brute("AABAAB"), prefix("AABAAB"))
NUM["prefix-function/pi-last"] = prefix("ABACABAB")[-1]; add(prefix("ABACABA")[-1], 3)
add(all(prefix(s_) == prefix_brute(s_) for s_ in ("".join(p) for k in range(1, 9) for p in itertools.product("ab", repeat=k))), True)

# ---------------- kmp-search
def kmp(t, p):
    pp_, j, out = prefix(p), 0, []
    for i, ch in enumerate(t):
        while j > 0 and ch != p[j]: j = pp_[j - 1]
        if ch == p[j]: j += 1
        if j == len(p): out.append(i - len(p) + 1); j = pp_[j - 1]
    return out
naive = lambda t, p: [i for i in range(len(t) - len(p) + 1) if t[i:i + len(p)] == p]
add(kmp("ABABDABABCABABCABAB", "ABABCABAB"), [5, 10]); add(naive("ABABDABABCABABCABAB", "ABABCABAB"), [5, 10])
TEXT["kmp-search/overlap"] = " ".join(map(str, kmp("ABABABA", "ABA"))); add(naive("ABABABA", "ABA"), [0, 2, 4])
add(prefix("ABABC")[3], 2); CHOICE["kmp-search/guess"] = "从第 3 个字母（A）接着比，前面的 AB 已知是对上的"
def dfa(pat, R="ABC"):
    M = len(pat); d = {c_: [0] * M for c_ in R}; d[pat[0]][0] = 1; X_ = 0
    for j in range(1, M):
        for c_ in R: d[c_][j] = d[c_][X_]
        d[pat[j]][j] = j + 1; X_ = d[pat[j]][X_]
    return d
Dd = dfa("ABABAC")
add({c_: Dd[c_] for c_ in "ABC"}, {"A": [1, 1, 3, 1, 5, 1], "B": [0, 2, 0, 4, 0, 4], "C": [0, 0, 0, 0, 0, 6]})
st_ = 0
for ch in "BCBAABA": st_ = Dd[ch][st_]
NUM["kmp-search/dfa-state"] = st_
st_, found = 0, None
for i, ch in enumerate("AABACAABABACAA"):
    st_ = Dd[ch][st_]
    if st_ == 6: found = i - 5; break
add(found, naive("AABACAABABACAA", "ABABAC")[0])
for _ in range(300):                 # KMP agrees with the naive search on random texts
    t_ = "".join(rnd.choice("ab") for _ in range(rnd.randint(0, 20))); p_ = "".join(rnd.choice("ab") for _ in range(rnd.randint(1, 4)))
    if kmp(t_, p_) != naive(t_, p_): add("kmp", "matches naive"); break

# ---------------- tries
keys = ["by", "sea", "sells", "she", "shells", "shore", "the"]
prefixes = {""} | {k[:i] for k in keys for i in range(1, len(k) + 1)}
NUM["tries/trie-nodes"] = len(prefixes); add(len(prefixes) - 1, 19)
add(sorted(k for k in keys if k.startswith("sh")), ["she", "shells", "shore"])
TEXT["tries/prefix-se"] = " ".join(sorted(k for k in keys if k.startswith("se")))
TEXT["tries/longest-prefix"] = max((k for k in keys if "shoreline".startswith(k)), key=len)
add(max((k for k in keys if "shellsort".startswith(k)), key=len), "shells")
add(sorted({k[:i] for k in keys for i in range(1, len(k) + 1)}), sorted("b by s se sea sel sell sells sh she shel shell shells sho shor shore t th the".split()))

# ---------------- regex
CHOICE["regex/guess"] = "babb"; add([bool(re.fullmatch("(a|b)*abb", s_)) for s_ in ("babb", "abba", "ab")], [True, False, False])
NUM["regex/regex-count"] = sum(1 for t_ in itertools.product("ab", repeat=3) if re.fullmatch("(a|b)*b", "".join(t_)))
add(sorted("".join(t_) for t_ in itertools.product("ab", repeat=3) if re.fullmatch("(a|b)*b", "".join(t_))), ["aab", "abb", "bab", "bbb"])
tm = [1.6, 3.7, 9.7, 23.2, 62.2, 161.6]; add([round(b / a, 1) for a, b in zip(tm, tm[1:])], [2.3, 2.6, 2.4, 2.7, 2.6])
CHOICE["regex/regex-match"] = "abcbd"; add([bool(re.fullmatch("a(b|c)*d", s_)) for s_ in ("abcbd", "abcb", "bcd", "ad")], [True, False, False, True])
nfa = {0: {"a": {0, 1}, "b": {0}}, 1: {"b": {2}}, 2: {"b": {3}}, 3: {}}   # (a|b)*abb as an NFA, simulated as a set of states
def run_nfa(s_):
    cur = {0}
    for ch in s_: cur = set().union(*(nfa[q].get(ch, set()) for q in cur)) if cur else set()
    return 3 in cur
add(all(run_nfa("".join(t_)) == bool(re.fullmatch("(a|b)*abb", "".join(t_))) for k in range(8) for t_ in itertools.product("ab", repeat=k)), True)

# ---------------- suffix-array
sa = lambda s_: sorted(range(len(s_)), key=lambda i: s_[i:])
def lcp(a_, b_):
    k = 0
    while k < min(len(a_), len(b_)) and a_[k] == b_[k]: k += 1
    return k
CHOICE["suffix-array/guess"] = "a"; add(min("banana"[i:] for i in range(6)), "a")
ab = "ABRACADABRA!"; add(sa(ab), [11, 10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2])
add([ab[i:] for i in sa(ab)][:4], ["!", "A!", "ABRA!", "ABRACADABRA!"])
add([lcp(ab[sa(ab)[i - 1]:], ab[sa(ab)[i]:]) for i in range(1, 12)], [0, 1, 4, 1, 1, 0, 3, 0, 0, 0, 2])
TEXT["suffix-array/sa-banana"] = " ".join(map(str, sa("banana")))
def lrs(s_):
    S_ = sa(s_); best = ""
    for i in range(1, len(S_)):
        k = lcp(s_[S_[i - 1]:], s_[S_[i]:])
        if k > len(best): best = s_[S_[i]:S_[i] + k]
    return best
def lrs_brute(s_):
    return max((s_[i:j] for i in range(len(s_)) for j in range(i + 1, len(s_) + 1) if s_.find(s_[i:j], i + 1) != -1), key=len)
TEXT["suffix-array/lrs-banana"] = lrs("banana"); add(lrs_brute("banana"), "ana")
add(lrs(ab), "ABRA"); NUM["suffix-array/lcp-abra"] = lcp("ABRA!", "ABRACADABRA!")
TEXT["suffix-array/mississippi"] = lrs("mississippi"); add(lrs_brute("mississippi"), "issi")
add((sa("mississippi").index(1) - sa("mississippi").index(4)), 1)
add(len({"cgcgggcgcg"[i:i + 3] for i in range(8)}), 5)          # algs4 exercise: 5 distinct length-3 substrings

# ================= boss
n_s = sp.Symbol("n", positive=True)
add(sp.limit((100 * n_s + sp.log(n_s)) / (n_s + sp.log(n_s)**2), n_s, sp.oo), 100); CHOICE["boss/b-theta"] = "f = Θ(g)"
add(master(8, 2, 3), "n^d log n"); CHOICE["boss/b-master"] = "Θ(n³ log n)"
NUM["boss/b-sort6"] = min_worst_comparisons(6)
fr = {"a": 45, "b": 13, "c": 12, "d": 16, "e": 9, "f": 5}; NUM["boss/b-huffman"] = cost(fr, huffman(fr))
add({s_: len(c_) for s_, c_ in huffman(fr).items()}, {"a": 1, "b": 3, "c": 3, "d": 3, "e": 4, "f": 4})
MB = nx.Graph(); MB.add_weighted_edges_from([("A", "B", 4), ("A", "C", 2), ("B", "C", 5), ("B", "D", 10), ("C", "E", 3), ("D", "E", 4), ("D", "F", 11), ("E", "F", 8)])
NUM["boss/b-mst"] = nx.minimum_spanning_tree(MB).size(weight="weight"); add(sum(w for *_, w in kruskal(MB)[0]), 21)
NUM["boss/b-lis"] = max(lis([10, 9, 2, 5, 3, 7, 101, 18])[0]); add(lis_brute([10, 9, 2, 5, 3, 7, 101, 18]), 4)
gb = [(1, 1), (3, 4), (4, 5), (5, 7)]
NUM["boss/b-knap"] = max(sum(v for _, v in c_) for r in range(5) for c_ in itertools.combinations(gb, r) if sum(w for w, _ in c_) <= 7)
cap, n_el, copies = 1, 0, 0
for _ in range(1000):
    if n_el == cap: copies += n_el; cap *= 2
    n_el += 1
NUM["boss/b-doubling"] = copies; add(copies < 2 * 1000, True); add(copies + 1000 < 3 * 1000, True)
NUM["boss/b-scc"] = nx.number_strongly_connected_components(nx.DiGraph([("a", "b"), ("b", "c"), ("c", "a"), ("b", "d"), ("d", "e"), ("e", "d")]))
TEXT["boss/b-dijkstra"] = " ".join(dijkstra(syn, "s")[1])
NUM["boss/b-maxflow"] = maxflow([("s", "a", 10), ("s", "b", 5), ("a", "b", 15), ("a", "t", 5), ("b", "t", 10)])
TEXT["boss/b-pi"] = " ".join(map(str, prefix("ABAABA"))); add(prefix_brute("ABAABA"), prefix("ABAABA"))

# ================= compare with the pack
pack = yaml.safe_load(open(os.path.join(ROOT, "data", "content", "F.1.2.yaml"), encoding="utf8"))
items = {}
for les in pack["lessons"]:
    for step in les["flow"]:
        it = step.get("item") or step.get("guess")
        if it: items[f"{les['id']}/{it['id']}"] = it
for it in (pack.get("boss") or {}).get("items", []): items[f"boss/{it['id']}"] = it
here = inspect.stack()[0].lineno
for key, it in items.items():
    if it["type"] == "number":
        if key not in NUM: checks.append((False, key, "a computed value in NUM", here)); continue
        ans = float(it["answer"]); tol = float(it.get("tolerance", max(1e-9, abs(ans) * 1e-6)))
        checks.append((abs(ans - float(NUM[key])) <= tol, f"{key} = {it['answer']}", float(NUM[key]), here))
    elif it["type"] == "text":
        if key not in TEXT: checks.append((False, key, "a computed value in TEXT", here)); continue
        sp_ = lambda s: " ".join(str(s).split())
        checks.append((sp_(TEXT[key]) in [sp_(a) for a in it["answers"]], f"{key} answers {it['answers']}", TEXT[key], here))
    elif it["type"] == "choice" and key in CHOICE:
        right = [o["text"] for o in it["options"] if o.get("correct")]
        want = CHOICE[key] if isinstance(CHOICE[key], list) else [CHOICE[key]]
        checks.append((right == want, f"{key} right option {right}", want, here))
    elif it["type"] == "order" and key in CHOICE:
        checks.append((it["steps"] == CHOICE[key], f"{key} steps {it['steps']}", CHOICE[key], here))
for d, kinds in [(NUM, ("number",)), (TEXT, ("text",)), (CHOICE, ("choice", "order"))]:
    for key in d:
        if key not in items or items[key]["type"] not in kinds: checks.append((False, key, f"a {'/'.join(kinds)} item in the pack", here))

bad = [(ln, g, w) for (ok, g, w, ln) in checks if not ok]
for ln, g, w in bad:
    print(f"line {ln}: got {g!r}, want {w!r}")
n_items = sum(1 for it in items.values() if it["type"] in ("number", "text"))
print(f"{len(checks) - len(bad)}/{len(checks)} claims hold ({n_items} number and text items, {len(CHOICE)} choice and order items compared with the pack)")
sys.exit(1 if bad else 0)
