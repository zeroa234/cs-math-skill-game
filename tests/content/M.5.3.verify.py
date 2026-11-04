# Checks every number, example and claim data/content/M.5.3.yaml states, by computing it independently:
# brute force over small cases (truth tables, every coloring of the 6-person graph, every way to unstack
# blocks, an actual L-tromino tiling of each 2^n x 2^n courtyard, every Nim position, the stable-matching
# ritual run step by step), sympy for algebra and recurrences, and plain integer arithmetic for the rest.
# Every graded number item's `answer` and every text item's `answers` is read from the pack and compared with
# the value computed here (NUM / TEXT below); choice items whose right option is a computed fact are checked
# the same way (CHOICE). The run fails if a number or text item has no computed value, or anything disagrees.
# usage: .venv/Scripts/python.exe -I tests/content/M.5.3.verify.py   (prints "N/N claims hold", exit 1 on a mismatch)
# The .venv needs sympy and pyyaml.
import inspect, itertools, math, os, sys
from fractions import Fraction as F
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

NUM, TEXT, CHOICE = {}, {}, {}   # "lesson/item" -> computed value / string / text of the right option
isprime = sp.isprime
n, k, x, c = sp.symbols("n k x c", integer=True)
X = sp.Symbol("X", real=True)
same = lambda a, b: sp.simplify(sp.expand(a - b)) == 0
imp = lambda p, q: (not p) or q
TF = [True, False]
print("Python", sys.version.split()[0], "sympy", sp.__version__)

# ================= 归纳
# ---------------- propositions
p = lambda m: m * m + m + 41
add(all(isprime(p(m)) for m in range(40)), True)                     # p(0..39) are all prime
add([p(m) for m in range(4)] + [p(39)], [41, 43, 47, 53, 1601])
add((p(40), p(40) == 41 * 41, isprime(p(40))), (1681, True, False))
add(95800**4 + 217519**4 + 414560**4 == 422481**4, True)             # Elkies' counterexample to Euler
NUM["propositions/first-counter"] = next(m for m in range(100) if not isprime(2**m + 1))
add([2**m + 1 for m in range(4)], [2, 3, 5, 9])
add((3 * 3 + 1, 3 % 2 == 0, (3 * 3 + 1) % 2 == 0), (10, False, True))   # pred-or-num: p(3), P(3), E(3)

# ---------------- axioms-implications
NUM["axioms-implications/break-implication"] = next(m for m in range(1, 100) if m % 6 == 0 and m % 4 != 0)
add(imp(7 % 4 == 0, 7 % 2 == 0), True)                                # vacuous: n = 7
sound = lambda prem, concl: all(imp(all(f(P, Q, R) for f in prem), concl(P, Q, R)) for P in TF for Q in TF for R in TF)
add(sound([lambda P, Q, R: imp(P, Q), lambda P, Q, R: imp(Q, R)], lambda P, Q, R: imp(P, R)), True)
add(sound([lambda P, Q, R: imp(P, Q), lambda P, Q, R: Q], lambda P, Q, R: P), False)
add(sound([lambda P, Q, R: imp(not P, not Q)], lambda P, Q, R: imp(P, Q)), False)
add(sound([lambda P, Q, R: imp(not P, not Q)], lambda P, Q, R: imp(Q, P)), True)   # the contrapositive rule is sound
f151 = -X**3 + 4 * X + 1
add([f151.subs(X, v) for v in (0, 1, 2)], [1, 4, 1])
add(same(X * (2 - X) * (2 + X), -X**3 + 4 * X), True)
add(min(float(f151.subs(X, i / 1000 * 2)) for i in range(1001)) > 0, True)
add((same(X * (3 - X) * (3 + X), -X**3 + 9 * X), same(X * (X - 3) * (X + 3), X**3 - 9 * X), same(-X * (X**2 + 9), -X**3 - 9 * X)), (True, True, True))
add(min(float((-X**3 + 9 * X).subs(X, i / 1000 * 3)) for i in range(1001)) >= 0, True)
add(same((2 * k)**2, 2 * (2 * k**2)), True)

# ---------------- induction
add(all(sum(range(1, m + 1)) == m * (m + 1) // 2 for m in range(300)), True)
NUM["induction/sum-100"] = sum(range(1, 101))
add(same(n * (n + 1) / 2 + (n + 1), (n + 1) * (n + 2) / 2), True)
add(same((n + 1) * (n + 2) / 2, (n + 1)**2 / 2), False)

# ---------------- induction-practice
odd_sums = [sum(2 * i - 1 for i in range(1, m + 1)) for m in range(1, 5)]
add(odd_sums, [1, 4, 9, 16])
add(all(sum(2 * i - 1 for i in range(1, m + 1)) == m * m for m in range(1, 300)), True)
add((3 * 4 // 2, 2 * 3 - 1), (6, 5))                                 # the wrong guesses at n = 3 (sum is 9)
add(same(2 * (n + 1) - 1, 2 * n + 1), True)
add(same(n**2 + 2 * n + 1, (n + 1)**2), True)
NUM["induction-practice/sum-odd-50"] = sum(range(1, 100, 2)); add(2 * 50 - 1, 99)
add([sum(2**i for i in range(m + 1)) for m in range(4)], [1, 3, 7, 15])
add(all(sum(2**i for i in range(m + 1)) == 2**(m + 1) - 1 for m in range(200)), True)
add(same(2**(n + 1) - 1 + 2**(n + 1), 2**(n + 2) - 1), True)
NUM["induction-practice/geo-10"] = sum(2**i for i in range(11))
add(same((n + 1)**3 - (n + 1), (n**3 - n) + 3 * n**2 + 3 * n), True)
add(same((n + 1)**3, n**3 + 1), False)
add(same(n**3 - n, n * (n - 1) * (n + 1)), True)
add(all((m**3 - m) % 3 == 0 for m in range(2000)), True)
holds = lambda m: 2**m > m * m
NUM["induction-practice/pick-base"] = min(b for b in range(0, 50) if all(holds(m) for m in range(b, 400)))
add([(2**m, m * m) for m in range(2, 6)], [(4, 4), (8, 9), (16, 16), (32, 25)])
add((holds(0), holds(1)), (True, True))
add(all(m * m - 2 * m - 1 > 0 for m in range(3, 1000)), True)

# ---------------- stronger-hypothesis: build the tiling the proof describes, for every statue position
def tile(size, statue):
    """L-tromino tiling of a size x size board (size a power of 2) leaving `statue` empty, by the proof's recursion."""
    board = [[0] * size for _ in range(size)]
    tid = [0]
    def go(top, left, s, hole):
        if s == 1: return
        h = s // 2
        tid[0] += 1; t = tid[0]
        quads = [(top, left), (top, left + h), (top + h, left), (top + h, left + h)]
        centre = [(top + h - 1, left + h - 1), (top + h - 1, left + h), (top + h, left + h - 1), (top + h, left + h)]
        for (qt, ql), cc in zip(quads, centre):
            if qt <= hole[0] < qt + h and ql <= hole[1] < ql + h:
                go(qt, ql, h, hole)
            else:
                board[cc[0]][cc[1]] = t                  # the temporary statue, covered by tile t
                go(qt, ql, h, cc)
    go(0, 0, size, statue)
    return board
ok = True
for e in range(0, 5):
    s = 2**e
    for r in range(s):
        for cl in range(s):
            b = tile(s, (r, cl))
            cells = {}
            for i in range(s):
                for j in range(s):
                    cells.setdefault(b[i][j], []).append((i, j))
            ok &= cells.get(0) == [(r, cl)]               # only the statue's square is uncovered
            ok &= all(len(v) == 3 and len({i for i, _ in v}) == 2 and len({j for _, j in v}) == 2 for t, v in cells.items() if t)
            ok &= len(cells) - 1 == (4**e - 1) // 3
add(ok, True)
add((4**2 - 1) // 3, 5)
NUM["stronger-hypothesis/tiles-8"] = (8 * 8 - 1) // 3

# ---------------- strong-induction
def payable(a):
    return any((a - 5 * f) >= 0 and (a - 5 * f) % 3 == 0 for f in range(a // 5 + 1))
add(all(payable(a) for a in range(8, 2000)), True)
add([a for a in range(1, 8) if not payable(a)], [1, 2, 4, 7])
NUM["strong-induction/largest-gap"] = max(a for a in range(1, 2000) if not payable(a))
add((3 + 5, 3 * 3, 5 * 2), (8, 9, 10))
NUM["strong-induction/coins-26"] = min(f + (26 - 5 * f) // 3 for f in range(6) if (26 - 5 * f) % 3 == 0)
add(sorted((f, (26 - 5 * f) // 3) for f in range(6) if (26 - 5 * f) % 3 == 0), [(1, 7), (4, 2)])
add([26 - 5 * f for f in (3, 2)], [11, 16])
from functools import lru_cache
@lru_cache(None)
def scores(m):
    """Every total score reachable when unstacking a stack of m blocks."""
    if m == 1: return frozenset([0])
    out = set()
    for a in range(1, m):
        for s1 in scores(a):
            for s2 in scores(m - a):
                out.add(a * (m - a) + s1 + s2)
    return frozenset(out)
add(all(scores(m) == {m * (m - 1) // 2} for m in range(1, 13)), True)
NUM["strong-induction/unstack-10"] = next(iter(scores(10)))
add(5 * 5, 25)                                                       # the book's first split 10 -> 5 + 5
NUM["strong-induction/unstack-one-by-one"] = sum(m * 1 for m in range(4, 0, -1))
a_, b_ = sp.symbols("a b", positive=True)
add(same(a_ * b_ + a_ * (a_ - 1) / 2 + b_ * (b_ - 1) / 2, (a_ + b_) * (a_ + b_ - 1) / 2), True)
add((12 == 3 * 4), True)

# ================= 反证
# ---------------- contrapositive
add(all(imp(P, Q) == imp(not Q, not P) for P in TF for Q in TF), True)
add(all(imp(P, Q) == imp(Q, P) for P in TF for Q in TF), False)
add((6 % 2 == 0, 6 % 4 == 0), (True, False))
add(same((2 * k + 1)**2, 2 * (2 * k**2 + 2 * k) + 1), True)
add(sorted({(r * r) % 3 for r in (1, 2)}), [1])                      # (3k+1)², (3k+2)² leave remainder 1
add((9 < 5 or 1 < 5, 9 + 1), (True, 10))                              # why "or" is the wrong negation
add((5 >= 5 or 0 >= 5, 5 + 0 >= 10), (True, False))                   # the converse is false
grid = [F(i, 4) for i in range(-40, 81)]
add(all(imp(a < 5 and b < 5, a + b < 10) for a in grid for b in grid), True)
add(all(imp(a + b >= 10, a >= 5 or b >= 5) for a in grid for b in grid), True)

# ---------------- contradiction
add(F(49, 25) == F(196, 100), True)
add(any(math.isqrt(2 * q * q)**2 == 2 * q * q for q in range(1, 200000)), False)   # no p/q squares to 2
add((F(2, 1).denominator % 2), 1)                                    # √4 = 2/1 in lowest terms: d = 1 is odd
add(sorted({(r * r) % 3 for r in range(3)}), [0, 1])                 # n² ≡ 0 (mod 3) only when n ≡ 0
add(4 * 0 == 2 * 0, True)

# ---------------- iff-and-cases
vals = [3, 5, 7]; mu = sum(vals) / 3
NUM["iff-and-cases/sd-value"] = math.sqrt(sum((v - mu)**2 for v in vals) / 3)
add(sum((v - mu)**2 for v in vals), 8.0)
add(all((m * m + m) % 2 == 0 for m in range(-500, 500)), True)
add(0 * 0 > 0, False)
def mono_triangle(people, met):
    """Is there a 3-person club or 3 strangers? met holds the pairs (a, b), a < b, who have met."""
    return any(((a, b) in met) == ((a, c) in met) == ((b, c) in met) for a, b, c in itertools.combinations(range(people), 3))
pairs6 = list(itertools.combinations(range(6), 2))
add(all(mono_triangle(6, {pr for pr, bit in zip(pairs6, bits) if bit}) for bits in itertools.product([0, 1], repeat=15)), True)
ring5 = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}
add(mono_triangle(5, ring5), False)
NUM["iff-and-cases/five-split"] = math.ceil(4 / 2)
add(math.ceil(5 / 2), 3)

# ================= well-ordering
add(min(m for m in range(101, 300) if m % 2 == 0), 102)
add([m for m in range(1, 100) if m % 101 == 0], [])
NUM["well-ordering/factor-360"] = sum(sp.factorint(360).values())
add(sp.factorint(360), {2: 3, 3: 2, 5: 1})

# ---------------- well-ordered-sets
add(max(m for m in range(1, 100) if m * m < 50), 7); CHOICE["well-ordered-sets/max-exists"] = "有，是 7"
seq, v = [1000], 1000
while v: v //= 2; seq.append(v)
add(seq, [1000, 500, 250, 125, 62, 31, 15, 7, 3, 1, 0])
NUM["well-ordered-sets/halving-steps"] = len(seq) - 1
add(2**9 <= 1000 < 2**10, True)

# ---------------- good-proofs
import cmath
add((cmath.sqrt((-1) * (-1)), cmath.sqrt(-1) * cmath.sqrt(-1)), (1, -1))
add(all(m * m >= m for m in range(1, 1000)), True)

# ================= 不变式
# ---------------- state-machines
def counter(presses):
    s = 0
    for _ in range(presses): s = s + 1 if isinstance(s, int) and s < 99 else "溢出"
    return s
add((counter(99), counter(100), counter(150)), (99, "溢出", "溢出"))
NUM["state-machines/counter-states"] = len(list(range(100)) + ["溢出"])
moves = [(dx, dy) for dx in (1, -1) for dy in (1, -1)]
def robot_after(steps):
    cur = {(0, 0)}
    for _ in range(steps): cur = {(m + dx, q + dy) for (m, q) in cur for dx, dy in moves}
    return cur
add(robot_after(1), {(1, 1), (1, -1), (-1, 1), (-1, -1)})
NUM["state-machines/robot-two-steps"] = len(robot_after(2)); add((0, 0) in robot_after(2), True)
NUM["state-machines/robot-three-steps"] = len(robot_after(3))
NUM["state-machines/robot-to-20"] = next(s for s in range(10) if (2, 0) in robot_after(s))

# ---------------- invariants
reach = set().union(*[robot_after(s) for s in range(12)])
add((1, 0) in reach, False)
pts = [(m, q) for m in range(-6, 7) for q in range(-6, 7)]
add(all(((m + q) % 2 == 0) <= (((m + dx) + (q + dy)) % 2 == 0) for m, q in pts for dx, dy in moves), True)   # m+n even is kept
add(any(m % 2 == 0 and (m + dx) % 2 == 0 for m, q in pts for dx, dy in moves), False)                    # m even never survives a step
add(any(m >= 0 and m + dx < 0 for m, q in pts for dx, dy in moves), True)
add([pt in reach for pt in [(3, 0), (2, 5), (4, -2), (5, 5)]], [False, False, True, True])
path = [(0, 0), (1, -1), (2, -2), (3, -1), (4, -2)]
add(all((b[0] - a[0], b[1] - a[1]) in moves for a, b in zip(path, path[1:])), True)
colour = lambda r, cl: (r + cl) % 2                                   # 0 = the corner colour
board = {(r, cl) for r in range(8) for cl in range(8)}
add(colour(0, 0) == colour(7, 7), True)
left = board - {(0, 0), (7, 7)}
add((sum(1 for s in left if colour(*s)), sum(1 for s in left if not colour(*s))), (32, 30))
NUM["invariants/domino-count"] = sum(1 for s in left if colour(*s)) - sum(1 for s in left if not colour(*s))
left2 = board - {(0, 0), (0, 1)}
add(colour(0, 0) != colour(0, 1), True)
row_tiling = [((r, cl), (r, cl + 1)) for r in range(8) for cl in range(0 if r else 2, 8, 2)]   # row 0 keeps 6 squares: 3 dominoes
add((len(row_tiling), {s for d in row_tiling for s in d} == left2), (31, True))
def can_tile(cells):
    cells = set(cells)
    if not cells: return True
    s = min(cells)
    return any(t in cells and can_tile(cells - {s, t}) for t in [(s[0], s[1] + 1), (s[0] + 1, s[1])])
add(can_tile({(r, cl) for r in range(4) for cl in range(4)} - {(0, 0), (3, 3)}), False)   # the 4x4 version, by brute force

# ---------------- die-hard: every state the jugs can reach, by breadth-first search
def jug_moves(state, big, small):
    b, l = state
    out = {(big, l), (b, small), (0, l), (b, 0)}
    t = min(l, big - b); out.add((b + t, l - t))     # pour small into big
    t = min(b, small - l); out.add((b - t, l + t))   # pour big into small
    return out
def jug_bfs(big, small):
    dist, frontier = {(0, 0): 0}, [(0, 0)]
    while frontier:
        nxt = []
        for s in frontier:
            for t in jug_moves(s, big, small):
                if t not in dist: dist[t] = dist[s] + 1; nxt.append(t)
        frontier = nxt
    return dist
d53 = jug_bfs(5, 3)
NUM["die-hard/min-steps-4"] = min(v for (b, l), v in d53.items() if b == 4)
seq6 = [(0, 0), (5, 0), (2, 3), (2, 0), (0, 2), (5, 2), (4, 3)]
add(all(t in jug_moves(s, 5, 3) for s, t in zip(seq6, seq6[1:])), True)
TEXT["die-hard/pour-result"] = "(1, 3)"; add((4 - min(4, 3 - 0), 0 + min(4, 3 - 0)), (1, 3))
add((1, 3) in jug_moves((4, 0), 5, 3), True)
d93 = jug_bfs(9, 3)
add(all(b % 3 == 0 and l % 3 == 0 for b, l in d93), True)
add([s in d93 for s in [(6, 3), (3, 0), (4, 3), (8, 1)]], [True, True, False, False])
add((0, 0) in jug_moves((1, 0), 9, 3), True)                         # (1,0) breaks the negation
d64 = jug_bfs(6, 4)
add(all(b % 2 == 0 and l % 2 == 0 for b, l in d64), True)
add(any(5 in s for s in d64), False)

# ---------------- termination: fast exponentiation as the state machine in the lesson
def fastpow(a, b):
    st, trace, mults = (a, 1, b), [(a, 1, b)], 0
    while st[2]:
        x_, y_, z_ = st
        if z_ % 2 == 0: st = (x_ * x_, y_, z_ // 2); mults += 1
        else: st = (x_ * x_, x_ * y_, (z_ - 1) // 2); mults += 2
        trace.append(st)
        add(st[1] * st[0]**st[2], a**b)                               # the invariant y·x^z = a^b holds at every step
    return trace, mults
tr13, m13 = fastpow(2, 13)
add(tr13, [(2, 1, 13), (4, 2, 6), (16, 2, 3), (256, 32, 1), (65536, 8192, 0)])
NUM["termination/fastpow-3-5"] = fastpow(3, 5)[0][-1][1]
add(fastpow(3, 5)[0], [(3, 1, 5), (9, 3, 2), (81, 3, 1), (6561, 243, 0)])
NUM["termination/invariant-at-step"] = 2 * 16**3
NUM["termination/fastpow-mults"] = m13
tr1000, m1000 = fastpow(2, 1000)
add((len(tr1000) - 1, m1000, m1000 < 20), (10, 16, True))

# ---------------- stable-matching
MEN = {"A": "XYZ", "B": "YXZ", "C": "XYZ"}
WOMEN = {"X": "BAC", "Y": "ABC", "Z": "ABC"}
def ritual(proposers, choosers):
    lists = {m: list(v) for m, v in proposers.items()}
    days = 0
    while True:
        days += 1
        suitors = {}
        for m, l in lists.items(): suitors.setdefault(l[0], []).append(m)
        if all(len(v) == 1 for v in suitors.values()):
            return days, {w: v[0] for w, v in suitors.items()}
        for w, v in suitors.items():
            keep = min(v, key=choosers[w].index)
            for m in v:
                if m != keep: lists[m].remove(w)
def rogues(match, men=MEN, women=WOMEN):    # match: man -> woman
    wife_of, husband_of = match, {w: m for m, w in match.items()}
    return {(m, w) for m in men for w in women if wife_of[m] != w
            and men[m].index(w) < men[m].index(wife_of[m]) and women[w].index(m) < women[w].index(husband_of[w])}
days, res = ritual(MEN, WOMEN)
NUM["stable-matching/ritual-days"] = days
add(res, {"X": "A", "Y": "B", "Z": "C"})
stable = [dict(zip("ABC", perm)) for perm in itertools.permutations("XYZ") if not rogues(dict(zip("ABC", perm)))]
add(sorted(tuple(sorted(s.items())) for s in stable), [(("A", "X"), ("B", "Y"), ("C", "Z")), (("A", "Y"), ("B", "X"), ("C", "Z"))])
r = rogues({"A": "Z", "B": "Y", "C": "X"})
add((("A", "X") in r, ("B", "X") in r, ("C", "Y") in r), (True, False, False))
wdays, wres = ritual(WOMEN, MEN)
add((wres, wdays), ({"B": "X", "A": "Y", "C": "Z"}, 3))
two_m, two_w = {"A": "XY", "B": "XY"}, {"X": "AB", "Y": "AB"}
add(rogues({"A": "Y", "B": "X"}, two_m, two_w), {("A", "X")})
add(rogues({"A": "X", "B": "Y"}, two_m, two_w), set())
NUM["stable-matching/ritual-bound"] = 5 * 5

# ================= 等价关系 / 偏序: relations as sets of pairs, properties by brute force
def rel(S, f): return {(a, b) for a in S for b in S if f(a, b)}
def reflexive(S, R): return all((a, a) in R for a in S)
def irreflexive(S, R): return all((a, a) not in R for a in S)
def symmetric(S, R): return all((b, a) in R for a, b in R)
def antisymmetric(S, R): return all(not ((b, a) in R) for a, b in R if a != b)
def asymmetric(S, R): return all((b, a) not in R for a, b in R)
def transitive(S, R): return all((a, d) in R for a, b in R for c, d in R if b == c)
def equivalence(S, R): return reflexive(S, R) and symmetric(S, R) and transitive(S, R)
def weak_po(S, R): return reflexive(S, R) and antisymmetric(S, R) and transitive(S, R)
def strict_po(S, R): return irreflexive(S, R) and transitive(S, R)
def linear(S, R): return all((a, b) in R or (b, a) in R for a in S for b in S if a != b)
divides = lambda a, b: b % a == 0
Z = range(-12, 13)
P12 = range(1, 13)

# ---------------- relations
add(len(rel([1, 2, 3], lambda a, b: a > b)), 3)
D5 = rel([1, 2, 3, 4, 6], divides)
NUM["relations/divides-arrows"] = len(D5); add(sum(1 for a, b in D5 if a == b), 5)
near = rel(Z, lambda a, b: abs(a - b) <= 1)
add((reflexive(Z, near), symmetric(Z, near), transitive(Z, near)), (True, True, False))
le = rel(Z, lambda a, b: a <= b)
add((antisymmetric(Z, le), transitive(Z, le), asymmetric(Z, le), symmetric(Z, le)), (True, True, False, False))
lt = rel(Z, lambda a, b: a < b)
add((transitive(Z, lt), reflexive(Z, lt), symmetric(Z, lt)), (True, False, False))
DP = rel(P12, divides)
add((reflexive(P12, DP), transitive(P12, DP), symmetric(P12, DP)), (True, True, False))
Rabc = {("a", "b"), ("b", "a"), ("a", "a"), ("b", "b"), ("c", "c")}
add((reflexive("abc", Rabc), symmetric("abc", Rabc), transitive("abc", Rabc)), (True, True, True))
classmates = rel(range(6), lambda a, b: a // 3 == b // 3)               # two classes of three
add((equivalence(range(6), classmates), antisymmetric(range(6), classmates)), (True, False))

# ---------------- equivalence
add(sorted({m % 3 for m in Z}), [0, 1, 2])
cong = lambda nn: (lambda a, b: (a - b) % nn == 0)
add((equivalence(Z, rel(Z, cong(5))), equivalence(Z, near), equivalence(Z, le)), (True, False, False))
add([cong(5)(6, 16), cong(5)(-1, 4), cong(5)(2, 9), cong(4)(3, 13)], [True, True, False, False])
add(cong(5)(17, 2), True)
sq = lambda a, b: a * a == b * b
add((sq(3, -3), sq(2, 4), sq(3, 9), equivalence(Z, rel(Z, sq))), (True, False, False, True))
cls = lambda a, nn=5: {b for b in range(-20, 30) if cong(nn)(a, b)}
add(min(b for b in cls(-3) if b >= 0), 2); NUM["equivalence/class-rep"] = min(b for b in cls(-3) if b >= 0)
add(sorted(b for b in cls(7) if -5 <= b <= 20), [-3, 2, 7, 12, 17])
NUM["equivalence/class-count"] = len({frozenset(cls(a)) for a in range(-20, 30)})
add((cls(12) == cls(7), cls(8) == cls(7), cls(5) == cls(7)), (True, False, False))

# ---------------- partitions
def is_partition(S, blocks):
    return all(blocks) and sum(len(b) for b in blocks) == len(set().union(*blocks)) and set().union(*blocks) == set(S)
S6 = range(1, 7)
add([is_partition(S6, b) for b in ([{1, 2}, {3, 4, 5}, {6}], [{1, 2, 3}, {3, 4, 5, 6}], [{1, 2}, {4, 5, 6}])], [True, False, False])
add((2 % 5, 9 % 5), (2, 4))
pairs3 = [(a, b) for a in range(3) for b in range(3)]
equivs3 = [R for bits in itertools.product([0, 1], repeat=9) if equivalence(range(3), R := {pr for pr, bt in zip(pairs3, bits) if bt})]
NUM["partitions/count-partitions"] = len(equivs3)
refines = lambda fine, coarse: all(cong(coarse)(a, b) for a in Z for b in Z if cong(fine)(a, b))
add((refines(4, 2), refines(6, 3), refines(6, 4), refines(12, 6), refines(6, 12)), (True, True, False, True, False))
add((cong(6)(2, 8), 2 % 4, 8 % 4), (True, 2, 0))
blocks = [{1, 4}, {2}, {3, 5, 6}]
same_block = lambda a, b: any(a in bl and b in bl for bl in blocks)
add((same_block(3, 6), same_block(3, 4), same_block(1, 2), same_block(1, 4)), (True, False, False, True))

# ---------------- partial-orders
cyc = {("a", "b"), ("b", "c"), ("c", "a")}
closure = set(cyc)
while True:
    more = {(a, d) for a, b in closure for c, d in closure if b == c} - closure
    if not more: break
    closure |= more
add(("a", "a") in closure, True)
add((divides(2, -2), divides(-2, 2), 2 != -2), (True, True, True))
add((weak_po(P12, rel(P12, lambda a, b: a <= b)), weak_po(P12, DP), weak_po(P12, rel(P12, lambda a, b: a < b)), weak_po(P12, rel(P12, lambda a, b: abs(a - b) <= 1))), (True, True, False, False))
add((strict_po(P12, rel(P12, lambda a, b: a < b)), antisymmetric(P12, rel(P12, lambda a, b: abs(a - b) <= 1))), (True, False))
D12 = [1, 2, 3, 4, 6, 12]
add(weak_po(D12, rel(D12, divides)), True)

# ---------------- hasse
def covers(S, R):
    return {(a, b) for a, b in R if a != b and not any(c not in (a, b) and (a, c) in R and (c, b) in R for c in S)}
add(len({(a, b) for a, b in rel(D12, divides) if a != b}), 12)
add(covers(D12, rel(D12, divides)), {(1, 2), (1, 3), (2, 4), (2, 6), (3, 6), (4, 12), (6, 12)})
D18 = [1, 2, 3, 6, 9, 18]
NUM["hasse/hasse-18"] = len(covers(D18, rel(D18, divides)))
add(covers(D18, rel(D18, divides)), {(1, 2), (1, 3), (2, 6), (3, 6), (3, 9), (6, 18), (9, 18)})
maximal = lambda S: {a for a in S if not any(b != a and divides(a, b) for b in S)}
minimal = lambda S: {a for a in S if not any(b != a and divides(b, a) for b in S)}
least = lambda S: [a for a in S if all(divides(a, b) for b in S)]
add(maximal([2, 3, 4, 5, 6, 12]), {5, 12}); add(5 in minimal([2, 3, 4, 5, 6, 12]), True)
add((least([2, 3, 4, 6]), minimal([2, 3, 4, 6])), ([], {2, 3}))
add((least(D12), [a for a in D12 if all(divides(b, a) for b in D12)]), ([1], [12]))
S136 = [1, 3, 4, 6, 8, 12]
down = lambda S, a: {b for b in S if divides(b, a)}
add({a: down(S136, a) for a in S136}, {1: {1}, 3: {1, 3}, 4: {1, 4}, 6: {1, 3, 6}, 8: {1, 4, 8}, 12: {1, 3, 4, 6, 12}})
add(all(divides(a, b) == (down(S136, a) <= down(S136, b)) for a in S136 for b in S136), True)
add(down(D18, 9), {1, 3, 9}); add(down(D18, 9) <= down(D18, 18), True)
def linear_extensions(S, R):
    return [o for o in itertools.permutations(S) if all(o.index(a) < o.index(b) for a, b in R if a != b)]
ext18 = linear_extensions(D18, rel(D18, divides))
NUM["hasse/topo-count"] = len(ext18)
add(((1, 2, 3, 6, 9, 18) in ext18, (1, 3, 9, 2, 6, 18) in ext18), (True, True))
add(len(linear_extensions(D12, rel(D12, divides))) > 1, True)

# ---------------- linear-product
add((linear(D12, rel(D12, divides)), divides(2, 3) or divides(3, 2), divides(4, 6) or divides(6, 4)), (False, False, False))
add([linear(S, rel(S, divides)) for S in ([1, 2, 4, 8, 16], [1, 2, 3, 6], [2, 4, 6, 12])], [True, False, False])
prod_le = lambda p_, q_: p_[0] <= q_[0] and p_[1] <= q_[1]
comparable = lambda p_, q_: prod_le(p_, q_) or prod_le(q_, p_)
add([comparable((3, 5), q_) for q_ in [(4, 6), (1, 5), (2, 7), (5, 4)]], [True, True, False, False])
add(comparable((240, 68), (228, 72)), False)
add(comparable((20, 170), (19, 180)), False)
grid3 = [(a, b) for a in range(3) for b in range(3)]
NUM["linear-product/product-below"] = sum(1 for q_ in grid3 if prod_le(q_, (1, 2)))
add(weak_po(grid3, rel(grid3, prod_le)), True)
eq = rel(range(5), lambda a, b: a == b)
add((symmetric(range(5), eq), antisymmetric(range(5), eq)), (True, True))

# ================= 递推与结构化证明
# ---------------- recursive-data: strings as nested pairs, exactly as defined
LAM = ()
def mk(word):                                   # "abc" -> <a, <b, <c, λ>>>
    s = LAM
    for ch in reversed(word): s = (ch, s)
    return s
def length(s): return 0 if s == LAM else 1 + length(s[1])
def concat(s, t): return t if s == LAM else (s[0], concat(s[1], t))
def depth_of_pairs(s): return 0 if s == LAM else 1 + depth_of_pairs(s[1])
NUM["recursive-data/build-1011"] = depth_of_pairs(mk("1011"))
add(mk("1011"), ("1", ("0", ("1", ("1", LAM)))))
words = ["".join(w) for m in range(5) for w in itertools.product("01", repeat=m)]
add(all(length(concat(mk(a), mk(b))) == length(mk(a)) + length(mk(b)) for a in words for b in words), True)
add(all(concat(mk(a), LAM) == mk(a) for a in words), True)
add(concat(mk("xy"), mk("z")), mk("xyz"))
add(("x", concat(mk("y"), mk("z"))) == concat(mk("xy"), mk("z")), True)   # the first step <x, <y,λ>·<z,λ>>

# ---------------- brackets
def recmatch(maxlen):
    """Every RecMatch string up to maxlen, built only by the definition: λ; [s]t."""
    S = {""}
    while True:
        new = {"[" + s + "]" + t for s in S for t in S if len(s) + len(t) + 2 <= maxlen} - S
        if not new: return S
        S |= new
RM = recmatch(8)
by_len = {}
for s in RM: by_len.setdefault(len(s), []).append(s)
NUM["brackets/catalan-6"] = len(by_len[6])
add(sorted(by_len[6]), sorted(["[][][]", "[][[]]", "[[]][]", "[[][]]", "[[[]]]"]))
add(("[[][]]" in RM, "[]][" in RM, "[[]" in RM, "][" in RM), (True, False, False, False))
add(all(s.count("[") == s.count("]") for s in RM), True)
add(("][".count("[") == "][".count("]")), True)
def split_rm(s):                                 # the unique [s]t decomposition of a nonempty RecMatch string
    depth_ = 0
    for i, ch in enumerate(s):
        depth_ += 1 if ch == "[" else -1
        if depth_ == 0: return s[1:i], s[i + 1:]
def nest(s): return 0 if s == "" else max(1 + nest(split_rm(s)[0]), nest(split_rm(s)[1]))
NUM["brackets/depth"] = nest("[[]][]"); add(split_rm("[[]][]"), ("[]", "[]"))
add((0, 1 + 0 + 0), (0, 1))                      # f(λ) = 0 but f(λλ) = 1 under the ambiguous definition

# ---------------- recursive-functions
fac = lambda m: 1 if m == 0 else m * fac(m - 1)
NUM["recursive-functions/fac-5"] = fac(5); add([fac(m) for m in range(5)], [1, 1, 2, 6, 24])
f1a = lambda m: 2 * m; f1b = lambda m: 2 * m + 1
add(all(f1a(m) == 2 + f1a(m - 1) and f1b(m) == 2 + f1b(m - 1) for m in range(1, 50)), True)   # f1 is not unique
add((10 % 2 == 0, 10 % 5 == 0, 6 % 2 == 0, 6 % 3 == 0), (True, True, True, True))
g3 = lambda m: 1 if m == 0 else 3 * g3(m - 1); add(all(g3(m) == 3**m for m in range(20)), True)
g2 = lambda m: 0 if m == 0 else g2(m - 1) + 2 * (m - 1) + 1; add(all(g2(m) == m * m for m in range(40)), True)
def collatz(m):
    chain = [m]
    while m > 1:
        m = m // 2 if m % 2 == 0 else 3 * m + 1
        chain.append(m)
    return chain
add(collatz(3), [3, 10, 5, 16, 8, 4, 2, 1])
NUM["recursive-functions/collatz-steps"] = len(collatz(6)) - 1
add(collatz(6), [6, 3, 10, 5, 16, 8, 4, 2, 1])
f2 = lambda m: 0 if m == 0 else 7
add(all(f2(m) == f2(m + 1) for m in range(1, 50)) and f2(0) == 0, True)
add((1 == 2), False)                             # f(n) = n fails f(1) = f(2)

# ---------------- expressions: Aexp as nested tuples, eval and subst by the definitions
def ev(e, nn):
    if e == "x": return nn
    if isinstance(e, int): return e
    op = e[0]
    if op == "+": return ev(e[1], nn) + ev(e[2], nn)
    if op == "*": return ev(e[1], nn) * ev(e[2], nn)
    if op == "-": return -ev(e[1], nn)
def subst(f, e):
    if e == "x": return f
    if isinstance(e, int): return e
    return (e[0],) + tuple(subst(f, part) for part in e[1:])
mults = lambda e: 0 if e == "x" or isinstance(e, int) else (e[0] == "*") + sum(mults(part) for part in e[1:])
poly = ("+", ("*", 3, ("*", "x", "x")), ("+", ("*", 2, "x"), 1))     # [[3*[x*x]] + [[2*x]+1]]
add(ev(poly, 3), 34); add((3 * 3)**2 + 2 * 3 + 1, 88)
NUM["expressions/eval-small"] = ev(("+", 3, ("*", "x", "x")), 2)
NUM["expressions/eval-big"] = ev(poly, 4)
three_x = ("*", 3, "x"); x_x1 = ("*", "x", ("+", "x", ("-", 1)))   # 3x and x(x - 1)
NUM["expressions/subst-eval"] = ev(subst(three_x, x_x1), 2)
add(ev(x_x1, ev(three_x, 2)), 30)
add((mults(subst(three_x, x_x1)), mults(three_x) + mults(x_x1)), (3, 2))   # substitution model does 3·2 twice
import random
rng = random.Random(53)
def rand_exp(d):
    if d == 0 or rng.random() < 0.3: return "x" if rng.random() < 0.5 else rng.randint(0, 5)
    op = rng.choice("+*-")
    return ("-", rand_exp(d - 1)) if op == "-" else (op, rand_exp(d - 1), rand_exp(d - 1))
add(all(ev(subst(f, e), nn) == ev(e, ev(f, nn)) for f, e in [(rand_exp(3), rand_exp(4)) for _ in range(300)] for nn in range(-3, 4)), True)

# ---------------- games: Nim positions as sorted tuples of pile sizes
def nim_moves(pos):
    out = []
    for i, p_ in enumerate(pos):
        for take in range(1, p_ + 1):
            rest = list(pos); rest[i] -= take
            out.append(tuple(sorted(x_ for x_ in rest if x_)))
    return out
@lru_cache(None)
def mover_wins(pos): return any(not mover_wins(q) for q in nim_moves(pos))
add(sorted(set(nim_moves((2, 3)))), sorted({(2, 2), (1, 2), (2,), (1, 3), (3,)}))
add(len(nim_moves((2, 3))), 5)
NUM["games/first-moves"] = len(nim_moves((3, 4)))
add((mover_wins((2, 3)), [q for q in nim_moves((2, 3)) if not mover_wins(q)]), (True, [(2, 2)]))
add(mover_wins((2, 2)), False)
add([q for q in nim_moves((1, 4)) if not mover_wins(q)], [(1, 1)])   # the only winning move from (4, 1)
NUM["games/winning-move"] = 4 - 1                # (4, 1) -> (1, 1): take 3 from the 4-pile

# ---------------- search-trees: binary trees as None (leaf) or (left, right)
def trees(d):
    """Every binary tree of depth at most d."""
    if d == 0: return [None]
    sub = trees(d - 1)
    return [None] + [(l_, r_) for l_ in sub for r_ in sub]
size = lambda t: 1 if t is None else 1 + size(t[0]) + size(t[1])
tdepth = lambda t: 0 if t is None else 1 + max(tdepth(t[0]), tdepth(t[1]))
add(all(size(t) <= 2**(tdepth(t) + 1) - 1 for t in trees(3)), True)
add(max(size(t) for t in trees(3)), 15)
NUM["search-trees/full-size"] = sum(2**i for i in range(5))
NUM["search-trees/min-depth-100"] = min(dd for dd in range(20) if 2**(dd + 1) - 1 >= 100)
add((2**6 - 1, 2**7 - 1), (63, 127))
BST = (50, (30, (20, None, None), (40, None, None)), (70, (60, None, None), (80, None, None)))
def compares(t, r_):
    k_ = 0
    while t:
        k_ += 1
        if r_ == t[0]: return k_
        t = t[1] if r_ < t[0] else t[2]
    return None
NUM["search-trees/search-compares"] = compares(BST, 60)
def keys(t): return [] if t is None else keys(t[1]) + [t[0]] + keys(t[2])
def is_search(t): return t is None or (is_search(t[1]) and is_search(t[2]) and all(v < t[0] for v in keys(t[1])) and all(v > t[0] for v in keys(t[2])))
bad_tree = (50, (30, None, (55, None, None)), (70, None, None))
add((is_search(BST), is_search(bad_tree), compares(bad_tree, 55)), (True, False, None))
add((3.7 < 6.8, 3.7 > math.pi, 3.7 < 4.9), (True, True, True))

# ---------------- hanoi
def T_h(m): return 1 if m == 1 else 2 * T_h(m - 1) + 1
add([T_h(m) for m in range(1, 7)], [1, 3, 7, 15, 31, 63])
NUM["hanoi/hanoi-4"] = T_h(4)
add(all(T_h(m) == 2**m - 1 for m in range(1, 60)), True)
def hanoi_moves(m, a="A", b="B", c="C"):
    return [] if m == 0 else hanoi_moves(m - 1, a, c, b) + [(a, c)] + hanoi_moves(m - 1, b, a, c)
def legal(m, moves_):
    pegs = {"A": list(range(m, 0, -1)), "B": [], "C": []}
    for s_, t_ in moves_:
        dsk = pegs[s_].pop()
        if pegs[t_] and pegs[t_][-1] < dsk: return False
        pegs[t_].append(dsk)
    return pegs["C"] == list(range(m, 0, -1))
add((len(hanoi_moves(3)), legal(3, hanoi_moves(3))), (7, True))
add(same(2 * 2**(n - 1) + 1, 2**n + 1), True)
NUM["hanoi/hanoi-64-digits"] = len(str(2**64 - 1)); add(2**64 - 1, 18446744073709551615); add(2**64 - 1 > 10**19, True)
add(all(T_h(10) == 2**kk * T_h(10 - kk) + 2**kk - 1 for kk in range(0, 10)), True)

# ---------------- merge-sort
def merge(a, b):
    out, cmp_ = [], 0
    a, b = list(a), list(b)
    while a and b:
        cmp_ += 1
        out.append(a.pop(0) if a[0] <= b[0] else b.pop(0))
    return out + a + b, cmp_
add(merge([5, 7, 10, 23], [2, 6, 8, 9]), ([2, 5, 6, 7, 8, 9, 10, 23], 6))
add(max(merge(sorted(c_), sorted(set(range(8)) - set(c_)))[1] for c_ in itertools.combinations(range(8), 4)), 7)
NUM["merge-sort/merge-count"] = merge([1, 4, 9], [2, 3, 10])[1]
def msort(xs):
    if len(xs) <= 1: return list(xs), 0
    h = len(xs) // 2
    a, ca = msort(xs[:h]); b, cb = msort(xs[h:])
    out, cm = merge(a, b)
    return out, ca + cb + cm
add(max(msort(p_)[1] for p_ in itertools.permutations(range(8))), 17)     # worst case over all 8! inputs
T_m = lambda m: 0 if m == 1 else 2 * T_m(m // 2) + m - 1
add([T_m(2**e) for e in range(1, 5)], [1, 5, 17, 49])
add(all(T_m(2**e) == 2**e * e - 2**e + 1 for e in range(0, 20)), True)
NUM["merge-sort/ms-32"] = T_m(32)
NUM["merge-sort/log-1024"] = int(math.log2(1024))
add(T_m(64), 321)

# ---------------- linear-recurrences
stairs = lambda m: 1 if m <= 1 else stairs(m - 1) + stairs(m - 2)
add(sum(1 for m in range(1, 5) for c_ in itertools.product([1, 2], repeat=m) if sum(c_) == 4), 5)
add([stairs(m) for m in range(7)], [1, 1, 2, 3, 5, 8, 13]); add(stairs(5), 8)
NUM["linear-recurrences/stairs-10"] = stairs(10)
a_rec = lambda m: m if m < 2 else a_rec(m - 1) + 2 * a_rec(m - 2)
add([a_rec(m) for m in range(6)], [0, 1, 1, 3, 5, 11])
add(all(a_rec(m) == F(2**m - (-1)**m, 3) for m in range(25)), True)
r_ = sp.Symbol("r"); add(sorted(sp.solve(r_**2 - r_ - 2, r_)), [-1, 2])
A_, B_ = sp.symbols("A B"); add(sp.solve([A_ + B_, 2 * A_ - B_ - 1], [A_, B_]), {A_: sp.Rational(1, 3), B_: sp.Rational(-1, 3)})
NUM["linear-recurrences/a10"] = a_rec(10)
add(sorted(sp.solve(r_**2 - 5 * r_ + 6, r_)), [2, 3])
c1, c2 = sp.symbols("c1 c2")
fd = lambda e: (c1 + c2 * e) * 3**e
add(sp.expand(fd(n) - (6 * fd(n - 1) - 9 * fd(n - 2))), 0)
add(sp.expand((c1 + c2 * n) * 2**n - (4 * (c1 + c2 * (n - 1)) * 2**(n - 1) - 4 * (c1 + c2 * (n - 2)) * 2**(n - 2))), 0)
phi = (1 + math.sqrt(5)) / 2
add((round(phi**20 / math.sqrt(5), 5), stairs(19)), (6765.00003, 6765))
add(round((1 - math.sqrt(5)) / 2, 3), -0.618)
hv = lambda m: 1 if m == 1 else 2 * hv(m - 1) + m
add([hv(m) for m in range(1, 6)], [1, 4, 11, 26, 57])
add(all(hv(m) == 2**(m + 1) - m - 2 for m in range(1, 40)), True)
add(sp.expand((-n - 2) - (2 * (-(n - 1) - 2) + n)), 0)                 # the particular solution an + b, a = -1, b = -2
a_, b_ = sp.symbols("a b")
add(sp.expand((a_ * n + b_) - (2 * (a_ * (n - 1) + b_) + n) + ((a_ + 1) * n + (b_ - 2 * a_))), 0)   # an+b = 2(a(n-1)+b)+n  ⇔  0 = (a+1)n + (b-2a)
add(sp.solve([a_ + 1, b_ - 2 * a_], [a_, b_]), {a_: -1, b_: -2})
NUM["linear-recurrences/hanoi-variant-5"] = hv(5)
add(sp.simplify(3**(n + 1) - (2 * 3**n + 3**n)), 0)                 # c·3ⁿ with c = 3 is a particular solution

# ---------------- divide-conquer: compute T(2^k) and watch T(n)/f(n) settle
def T_dc(a, g, k, t1=1):
    v = t1
    for e in range(1, k + 1): v = a * v + g(2**e)
    return v
ratio = lambda a, g, f, k: T_dc(a, g, k) / f(2**k)
settles = lambda a, g, f: abs(ratio(a, g, f, 40) / ratio(a, g, f, 30) - 1) < 0.05
add(settles(2, lambda m: m, lambda m: m * math.log2(m)), True)
add(settles(4, lambda m: m, lambda m: m * m), True)
add(settles(1, lambda m: 1, lambda m: math.log2(m)), True)
add(settles(3, lambda m: m, lambda m: m**math.log2(3)), True)
add(settles(8, lambda m: m * m, lambda m: m**3), True)
add(round(T_dc(4, lambda m: m, 31) / T_dc(4, lambda m: m, 30), 2), 4.0)          # doubling n quadruples the work
NUM["divide-conquer/master-3-2-1"] = math.log2(3)
add((math.log2(2), math.log2(4), math.log2(1), math.log2(8)), (1.0, 2.0, 0.0, 3.0))
add(2 * F(1, 2)**2 + F(8, 9) * F(3, 4)**2, 1)                        # Akra–Bazzi p = 2 for 2T(n/2) + (8/9)T(3n/4) + n²
add((15 // 2, -(-15 // 2)), (7, 8))
def feel(a, k):
    """T(2^k)/f(2^k) for T_1 = 0, T_n = a·T_{n/2} + n − 1, with f = n (a < 2), n log n (a = 2), n^{log2 a} (a > 2)."""
    u = 0.0                                      # u_k = T(2^k) / scale_k, updated without forming 2^k
    for e in range(1, k + 1):
        if a < 2: u = (a / 2) * u + 1 - 0.5**e                       # scale 2^k
        elif a == 2: u = u * (e - 1) / e + (1 - 0.5**e) / e if e > 1 else 0.5   # scale k·2^k
        else: u = u + (2 / a)**e - (1 / a)**e                        # scale a^k
    return u
add([abs(feel(a, 6000) / feel(a, 5000) - 1) < 1e-3 for a in (1.99, 2, 2.01)], [True, True, True])
add((round(feel(1.99, 6000)), round(feel(2, 6000), 2)), (200, 1.0))      # T ~ 200n and T ~ n log n
T3 = lambda m: 0 if m == 0 else 3 * T3(m - 1) + 1
add(all(T3(m) == (3**m - 1) // 2 for m in range(30)), True)

# ================= boss
add(sp.expand(n * (n + 1) * (2 * n + 1) / 6 + (n + 1)**2 - (n + 1) * (n + 2) * (2 * n + 3) / 6), 0)
add(sp.expand(6 * (n * (n + 1) * (2 * n + 1) / 6 + (n + 1)**2)), 2 * n**3 + 9 * n**2 + 13 * n + 6)
add(all(sum(i * i for i in range(1, m + 1)) * 6 == m * (m + 1) * (2 * m + 1) for m in range(100)), True)
stamp = lambda a: any((a - 7 * b) >= 0 and (a - 7 * b) % 4 == 0 for b in range(a // 7 + 1))
NUM["boss/b-stamps"] = max(a for a in range(1, 500) if not stamp(a))
add([stamp(a) for a in (18, 19, 20, 21)], [True, True, True, True])
add([17 - 4 * k_ for k_ in range(5)], [17, 13, 9, 5, 1])
add(all(2**p_ % 2 == 0 and 3**q_ % 2 == 1 for p_ in range(1, 30) for q_ in range(1, 30)), True)
add(all((m * m + 2 * m) % 2 == 0 for m in range(-100, 101, 2)), True)
def robot2_reach(steps):
    seen, frontier = {(0, 0)}, {(0, 0)}
    for _ in range(steps):
        frontier = {(x_ + 2, y_ - 1) for x_, y_ in frontier} | {(x_ - 1, y_ + 2) for x_, y_ in frontier}
        seen |= frontier
    return seen
R2 = robot2_reach(12)
add(all((x_ + 2 * y_) % 3 == 0 for x_, y_ in R2), True)
add([pt in R2 for pt in [(1, 0), (2, -1), (1, 1)]], [False, True, True])
def sub_gcd(x_, y_):
    while x_ != y_:
        before = x_ + y_
        x_, y_ = (x_ - y_, y_) if x_ > y_ else (x_, y_ - x_)
        if not (0 < x_ + y_ < before): return None
    return x_
add(all(sub_gcd(x_, y_) == math.gcd(x_, y_) for x_ in range(1, 40) for y_ in range(1, 40)), True)
pairs4 = [(a, b) for a in range(4) for b in range(4)]
NUM["boss/b-bell4"] = sum(1 for bits in itertools.product([0, 1], repeat=16) if equivalence(range(4), {pr for pr, bt in zip(pairs4, bits) if bt}))
D30 = [1, 2, 3, 5, 6, 10, 15, 30]
NUM["boss/b-hasse30"] = len(covers(D30, rel(D30, divides)))
def full_trees(internal):
    """Every tree in which each non-leaf has exactly two subtrees, with `internal` non-leaves."""
    if internal == 0: return [None]
    return [(l_, r_) for i in range(internal) for l_ in full_trees(i) for r_ in full_trees(internal - 1 - i)]
leaves = lambda t: 1 if t is None else leaves(t[0]) + leaves(t[1])
add(all(leaves(t) == k_ + 1 for k_ in range(7) for t in full_trees(k_)), True)
NUM["boss/b-leaves"] = leaves(full_trees(10)[0])
br = lambda m: m if m < 2 else 3 * br(m - 1) - 2 * br(m - 2)
add(all(br(m) == 2**m - 1 for m in range(25)), True); NUM["boss/b-recur"] = br(8)
add(sorted(sp.solve(r_**2 - 3 * r_ + 2, r_)), [1, 2])

# ================= compare with the pack
pack = yaml.safe_load(open(os.path.join(ROOT, "data", "content", "M.5.3.yaml"), encoding="utf8"))
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
for d, kind in [(NUM, "number"), (TEXT, "text"), (CHOICE, "choice")]:
    for key in d:
        if key not in items or items[key]["type"] != kind: checks.append((False, key, f"a {kind} item in the pack", here))

bad = [(ln, g, w) for (ok, g, w, ln) in checks if not ok]
for ln, g, w in bad:
    print(f"line {ln}: got {g!r}, want {w!r}")
n_items = sum(1 for it in items.values() if it["type"] in ("number", "text"))
print(f"{len(checks) - len(bad)}/{len(checks)} claims hold ({n_items} number and text items, {len(CHOICE)} choice items compared with the pack)")
sys.exit(1 if bad else 0)
