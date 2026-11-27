"""H.2.8 电子设计自动化（EDA）算法 — every number in data/content/H.2.8.yaml, recomputed.

Run: python -I tests/content/H.2.8.verify.py [path/to/H.2.8.yaml]
Plain Python. Number answers are read back from the YAML and compared with the values computed here, so a typo in
either place fails. The algorithms are implemented here rather than trusted: prime implicants and minimum covers by
brute force over all cubes, ROBDD sizes by Shannon expansion with a unique table, satisfying assignments by
enumeration, technology mapping by dynamic programming over all pattern matches (NAND2 inputs commutative), cuts and
Kernighan-Lin gains against the cut actually recomputed after the swap, floorplan shapes by enumerating every shape
combination, the rectilinear Steiner tree by trying every Hanan-grid point set, quadratic placement by Gaussian
elimination (and a check that the gradient is zero), Tetris legalization step by step, Lee routing by breadth-first
search, the constrained left-edge algorithm with a vertical constraint graph, static timing by a topological pass
forwards and backwards, glitches by a small event-driven simulator, Newton-Raphson by iterating to convergence.
"""
import re
import sys
from collections import deque
from fractions import Fraction
from itertools import combinations, permutations, product
from math import comb, exp, factorial, log2, sqrt
from pathlib import Path

checks = 0
computed = {}


def close(a, b, tol=1e-9, what=""):
    global checks
    if abs(a - b) > tol * max(1.0, abs(b)) and abs(a - b) > tol:
        raise AssertionError(f"{what}: {a} != {b}")
    checks += 1


def ok(cond, what=""):
    global checks
    if not cond:
        raise AssertionError(what)
    checks += 1


def ans(item_id, value, tol=1e-9):
    computed[item_id] = (value, tol)


# ==== eda-intro / complexity-graphs ====
hours = 1e7**2 / 1e9 / 3600
ans("n2-hours", hours, 0.05)
close(1e7 * log2(1e7), 2.3e8, 0.02, "n log n operations")
close(1e7 * log2(1e7) / 1e9, 0.23, 0.02, "0.23 s")
ans("clique-edges", comb(5, 2))
ans("star-vs-clique", comb(12, 2) - 12)
close(comb(12, 2), 66, 0, "66 clique edges")
close(comb(20, 2), 190, 0, "k = 20 clique")


# ==== two-level ====
def cube_covers(c, m, n):
    bits = [(m >> (n - 1 - i)) & 1 for i in range(n)]
    return all(ci is None or ci == b for ci, b in zip(c, bits))


def qm(ms, n=3):
    on = set(ms)
    cubes = [c for c in product((0, 1, None), repeat=n)]
    imp = [c for c in cubes if all(m in on for m in range(2**n) if cube_covers(c, m, n))]

    def inside(a, b):
        return all(bi is None or ai == bi for ai, bi in zip(a, b))

    pis = [c for c in imp if not any(d != c and inside(c, d) for d in imp)]
    for k in range(1, len(pis) + 1):
        sols = [s for s in combinations(pis, k) if all(any(cube_covers(c, m, n) for c in s) for m in on)]
        if sols:
            return pis, k, sols
    raise AssertionError("no cover")


ans("minterm-number", 0b101)
pis, k, sols = qm((0, 1, 2, 5, 6, 7))
ans("pi-count", len(pis))
ans("min-terms", k)
ok(len(sols) == 2, "two minimum covers (not unique)")
pis, k, sols = qm((0, 2, 3, 7))
ok(len(pis) == 3 and k == 2 and len(sols) == 1, "worked example: 3 PIs, F = a'c' + bc")
ok(set(sols[0]) == {(0, None, 0), (None, 1, 1)}, "worked example cover")
# guess: a'b'c' + a'bc' = a'c'
ok(all(((not a and not b and not c) or (not a and b and not c)) == (not a and not c) for a, b, c in product((0, 1), repeat=3)), "a'c'")


# ==== bdd-sat ====
def robdd_size(f, n, order):
    """f: function of a tuple of n bits (indexed by variable); order: list of variable indices."""
    unique = {}

    def build(level, fixed):
        if level == n:
            return ("T", f(tuple(fixed[i] for i in range(n))))
        v = order[level]
        lo = build(level + 1, {**fixed, v: 0})
        hi = build(level + 1, {**fixed, v: 1})
        if lo == hi:
            return lo
        key = (v, lo, hi)
        if key not in unique:
            unique[key] = ("N", len(unique))
        return unique[key]

    build(0, {})
    return len(unique)


ans("bdd-small", robdd_size(lambda x: (x[0] and x[1]) or x[2], 3, [0, 1, 2]))
f2 = lambda x: (x[0] and x[1]) or (x[2] and x[3])  # a1 b1 a2 b2
ans("bdd-order", robdd_size(f2, 4, [0, 2, 1, 3]))
close(robdd_size(f2, 4, [0, 1, 2, 3]), 4, 0, "interleaved order, 2 pairs")
f3 = lambda x: (x[0] and x[1]) or (x[2] and x[3]) or (x[4] and x[5])
close(robdd_size(f3, 6, [0, 1, 2, 3, 4, 5]), 6, 0, "interleaved 6 nodes")
close(robdd_size(f3, 6, [0, 2, 4, 1, 3, 5]), 14, 0, "separated 14 nodes")
sat = [(a, b, c) for a, b, c in product((0, 1), repeat=3) if (a or b) and ((not a) or c) and ((not b) or (not c))]
ok(sat == [(0, 1, 0), (1, 0, 1)], "SAT example: two assignments")

# ==== multilevel ====
ans("factor-literals", (3 + 3 + 1) - (2 + 2 + 1))
ok(all(((a and b and c) or (a and b and d) or e) == ((a and b and (c or d)) or e) for a, b, c, d, e in product((0, 1), repeat=5)), "ab(c+d)+e")
close(4 + 4, 8, 0, "card example before")
close(2 + 2 + 2, 6, 0, "card example after")
ans("extract-literals", 2 + 2 + 2 + 2)
close(4 * 3, 12, 0, "before extraction 12 literals")
ok(all((((a or b) and c) == ((a and c) or (b and c))) for a, b, c in product((0, 1), repeat=3)), "xc = ac + bc")


# ==== tech-mapping ====
def matches(pat, node, leaves):
    if pat == "*":
        leaves.append(node)
        return True
    if isinstance(node, str):
        return False
    if pat[0] != node[0] or len(pat) != len(node):
        return False
    if pat[0] == "NAND2":
        for order in ((1, 2), (2, 1)):
            trial = []
            if matches(pat[1], node[order[0]], trial) and matches(pat[2], node[order[1]], trial):
                leaves.extend(trial)
                return True
        return False
    return matches(pat[1], node[1], leaves)


def best_cost(node, lib, memo=None):
    memo = {} if memo is None else memo
    if isinstance(node, str):
        return 0
    if node in memo:
        return memo[node]
    best = None
    for name, (cost, pat) in lib.items():
        leaves = []
        if matches(pat, node, leaves):
            c = cost + sum(best_cost(l, lib, memo) for l in leaves)
            best = c if best is None or c < best else best
    memo[node] = best
    return best


INV, NAND = "INV", "NAND2"
lib = {
    "INV": (2, (INV, "*")),
    "NAND2": (3, (NAND, "*", "*")),
    "AND2": (4, (INV, (NAND, "*", "*"))),
    "NAND3": (4, (NAND, (INV, (NAND, "*", "*")), "*")),
}
subject = (NAND, (INV, (NAND, "a", "b")), (INV, (NAND, "c", "d")))
ans("map-no-nand4", best_cost(subject, lib))
lib4 = dict(lib, NAND4=(6, (NAND, (INV, (NAND, "*", "*")), (INV, (NAND, "*", "*")))))
close(best_cost(subject, lib4), 6, 0, "worked example with NAND4")
close(best_cost((INV, (NAND, "a", "b")), lib), 4, 0, "AND2 subtree 4")

# ==== partition-goals / kl-fm / multilevel-partition ====


def cut(edges, A):
    return sum((u in A) != (v in A) for u, v in edges)


def net_cut(nets, A):
    return sum(any(v in A for v in n) and any(v not in A for v in n) for n in nets)


ans("cut-small", cut([(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)], {1, 3}))
close(net_cut([{1, 2, 3}, {3, 4}, {4, 5, 6}, {1, 6}], {1, 2, 3}), 2, 0, "card net cut")
ans("net-cut", net_cut([{1, 2}, {2, 3, 4}, {4, 5}, {5, 6}, {1, 6}], {1, 2, 3}))

KL = [(1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6), (2, 5)]


def kl_gain(edges, A, a, b):
    def D(v, own):
        ext = sum(1 for e in edges if v in e and ((e[0] if e[1] == v else e[1]) in own) != (v in own))
        inn = sum(1 for e in edges if v in e and ((e[0] if e[1] == v else e[1]) in own) == (v in own))
        return ext - inn

    w = sum(1 for e in edges if set(e) == {a, b})
    g = D(a, A) + D(b, A) - 2 * w
    A2 = (A - {a}) | {b}
    ok(cut(edges, A) - cut(edges, A2) == g, "KL gain equals the actual cut change")
    return g


close(cut(KL, {1, 2, 4}), 6, 0, "KL initial cut 6")
close(kl_gain(KL, {1, 2, 4}, 4, 3), 4, 0, "swap 3 and 4 gain 4")
close(cut(KL, {1, 2, 3}), 2, 0, "after swap 2")
ans("kl-gain", kl_gain(KL, {1, 2, 4}, 1, 5))
gains = [3, -1, 2, -4]
pref = [sum(gains[: i + 1]) for i in range(len(gains))]
ans("kl-prefix", pref.index(max(pref)) + 1)
lv = next(k for k in range(60) if 1e6 / 2**k < 100)
ans("coarsen-levels", lv)
ok(1e6 / 2**13 > 100, "13 levels not enough")

# ==== floorplan ====


def polish(expr, mods):
    st = []
    for ch in expr:
        if ch in "VH":
            b, a = st.pop(), st.pop()
            st.append((a[0] + b[0], max(a[1], b[1])) if ch == "V" else (max(a[0], b[0]), a[1] + b[1]))
        else:
            st.append(mods[ch])
    return st[0]


mods = {"a": (2, 3), "b": (3, 2), "c": (4, 1)}
ok(polish("abVcH", mods) == (5, 4), "abVcH 5 x 4")
close(5 * 4 - (6 + 6 + 4), 4, 0, "worked example dead space 4")
ans("dead-space", 4 * 4 - (3 + 5 + 6))
close(2 / 16, 0.125, 1e-12, "12.5%")
w, h = polish("abcHV", mods)
ans("polish-area", w * h)
close(w * h - 16, 2, 0, "abcHV dead space 2")

# ==== floorplan-algos ====
A_opts, B_opts = [(1, 4), (2, 2), (4, 1)], [(1, 3), (3, 1)]
areas = [(a[0] + b[0]) * max(a[1], b[1]) for a in A_opts for b in B_opts]
ok(areas == [8, 16, 9, 10, 15, 7], "six V combinations listed in order")
ans("sizing-v", min(areas))
ans("sa-accept", round(exp(-2 / 4), 2), 0.005)
close(exp(-0.5), 0.61, 0.01, "e^-0.5")
close(exp(-2), 0.14, 0.01, "e^-2")
ok(min(2 + 7, 5 + 3) == 8 and 2 + 7 == 9, "pin assignment matching")
ans("ir-drop", 0.5 * 0.02 * 1000, 1e-9)
close(0.5 * 0.02 / 1.0 * 100, 1, 1e-9, "1% of 1.0 V")


# ==== placement-objectives ====
def hpwl(pts):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return max(xs) - min(xs) + max(ys) - min(ys)


def manh(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def mst(pts):
    n = len(pts)
    inT, d, tot = [False] * n, [float("inf")] * n, 0
    d[0] = 0
    for _ in range(n):
        u = min((i for i in range(n) if not inT[i]), key=lambda i: d[i])
        inT[u] = True
        tot += d[u]
        for v in range(n):
            if not inT[v]:
                d[v] = min(d[v], manh(pts[u], pts[v]))
    return tot


def rsmt(pts):
    xs, ys = sorted({p[0] for p in pts}), sorted({p[1] for p in pts})
    H = [(x, y) for x in xs for y in ys if (x, y) not in pts]
    best = mst(pts)
    for k in range(1, len(pts) - 1):
        for extra in combinations(H, k):
            best = min(best, mst(list(pts) + list(extra)))
    return best


ans("hpwl-four", hpwl([(2, 3), (6, 1), (5, 7), (3, 4)]))
P3 = [(0, 0), (4, 0), (2, 3)]
ok(hpwl(P3) == 7 and mst(P3) == 9 and rsmt(P3) == 7, "worked example 7 / 9 / 7")
P4 = [(0, 0), (4, 1), (1, 4), (5, 5)]
ok([manh(p, q) for p, q in combinations(P4, 2)] == [5, 5, 10, 6, 5, 5], "six distances")
ans("rmst-vs-rsmt", mst(P4))
ok(rsmt(P4) == 13 and hpwl(P4) == 10, "RSMT 13, HPWL 10")
ans("density-overflow", 85 - 0.7 * 100, 1e-9)


# ==== global-placement ====
def solve(Am, bv):
    n = len(bv)
    M = [[Fraction(x) for x in row] + [Fraction(bv[i])] for i, row in enumerate(Am)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def quad_place(nmov, conns):
    """conns: (i, j, w) with i, j movable indices or ('F', x) fixed pins. Returns the x minimizing sum w (xi - xj)^2."""
    Am = [[0] * nmov for _ in range(nmov)]
    bv = [0] * nmov
    for i, j, w in conns:
        for p, q in ((i, j), (j, i)):
            if isinstance(p, int):
                Am[p][p] += w
                if isinstance(q, int):
                    Am[p][q] -= w
                else:
                    bv[p] += w * q[1]
    x = solve(Am, bv)
    pos = lambda q: x[q] if isinstance(q, int) else q[1]
    for k in range(nmov):  # the gradient of sum w (xi - xj)^2 is zero at the solution
        g = sum(2 * w * (pos(p) - pos(q)) for i, j, w in conns for p, q in ((i, j), (j, i)) if p == k)
        ok(g == 0, "gradient zero")
    return x


ok(quad_place(1, [(0, ("F", 0), 1), (0, ("F", 2), 1), (0, ("F", 10), 1)]) == [4], "guess: mean 4")
ok(quad_place(2, [(0, ("F", 0), 1), (0, 1, 1), (1, ("F", 9), 1)]) == [3, 6], "worked example 3, 6")
x = quad_place(2, [(0, ("F", 0), 1), (0, 1, 1), (1, ("F", 12), 2)])
ans("quad-x2", float(x[1]))
close(float(x[0]), 4.8, 1e-12, "x1 = 4.8")
ans("mincut-levels", log2(1024 / 4))
ans("quad-mean", float(quad_place(1, [(0, ("F", v), 1) for v in (1, 3, 4, 12)])[0]))


# ==== legalization ====
def tetris(cells):
    free, disp, pos = 0, 0.0, {}
    for name, x, w in sorted(cells, key=lambda c: c[1]):
        p = max(free, round(x))
        pos[name] = p
        disp += abs(p - x)
        free = p + w
    return pos, disp


pos, disp = tetris([("A", 0.3, 2), ("B", 1.0, 2), ("C", 5.2, 1)])
ok(pos == {"A": 0, "B": 2, "C": 5}, "worked Tetris positions")
close(disp, 1.5, 1e-12, "worked Tetris displacement")
pos, disp = tetris([("D", 0.6, 3), ("E", 2.2, 1), ("F", 3.9, 2)])
ok(pos == {"D": 1, "E": 4, "F": 5}, "item Tetris positions")
ans("tetris-disp", disp, 1e-9)
ans("detail-window", factorial(4))
close(factorial(8), 40320, 0, "8!")
ans("rows-count", 27.2 / 2.72, 1e-9)

# ==== global-routing-basics ====
ans("gcell-tracks", 4 / 0.4, 1e-9)
ans("overflow-total", sum(max(0, d - 10) for d in (8, 12, 15)))
ans("grid-graph-size", 2 * 100 * 99)


# ==== single-net ====
def lee(rows):
    R, C = len(rows), len(rows[0])
    cells = {(r, c): ch for r, row in enumerate(rows) for c, ch in enumerate(row)}
    s = next(k for k, v in cells.items() if v == "S")
    t = next(k for k, v in cells.items() if v == "T")
    dist, q = {s: 0}, deque([s])
    while q:
        u = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            v = (u[0] + dr, u[1] + dc)
            if v in cells and cells[v] != "#" and v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist[t], manh(s, t)


d, m = lee(["S....", "####.", ".....", ".####", "....T"])
ok(d == 16 and m == 8, "worked maze 16 steps, Manhattan 8")
d, m = lee(["S..#.", ".#.#.", ".#...", ".###.", "...#T"])
ans("lee-length", d)
ok(d == m == 8, "item maze equals Manhattan distance")
# the BFS sim: solution order must be a BFS order of the drawn graph
nodes = "s a b c d e f g h t".split()
edges = [("s", "a"), ("a", "b"), ("b", "c"), ("s", "d"), ("c", "e"), ("d", "f"), ("e", "t"), ("f", "g"), ("g", "h"), ("h", "t")]
adj = {n: set() for n in nodes}
for u, v in edges:
    adj[u].add(v)
    adj[v].add(u)
lvl, q = {"s": 0}, deque(["s"])
while q:
    u = q.popleft()
    for v in sorted(adj[u]):
        if v not in lvl:
            lvl[v] = lvl[u] + 1
            q.append(v)
sol = "s a d b f c g e h t".split()
ok([lvl[v] for v in sol] == sorted(lvl[v] for v in sol) and lvl["t"] == 5, "BFS layers s | a d | b f | c g | e h | t")
ans("hanan-points", 4 * 4 - 4)

# ==== full-netlist ====
ans("pathfinder-cost", (1 + 2) * 1.5, 1e-9)
ans("ilp-vars", 100 * 3)
ans("monotone-paths", comb(5, 2))
ok(sum(1 for p in set(permutations("RRRUU"))) == 10, "monotone paths by enumeration")


# ==== channel-routing ====
def spans(top, bot):
    s = {}
    for col, pair in enumerate(zip(top, bot)):
        for n in pair:
            if n:
                lo, hi = s.get(n, (col, col))
                s[n] = (min(lo, col), max(hi, col))
    return s


def density(sp, ncol):
    return max(sum(1 for lo, hi in sp.values() if lo <= c <= hi) for c in range(ncol))


def left_edge(sp, vcg=()):
    placed, tracks = {}, []
    while len(placed) < len(sp):
        cur = []
        for n in sorted((n for n in sp if n not in placed), key=lambda n: sp[n][0]):
            preds = [a for a, b in vcg if b == n]
            if any(p not in placed for p in preds):
                continue
            if all(sp[n][0] > sp[m][1] or sp[n][1] < sp[m][0] for m in cur):
                cur.append(n)
        ok(cur, "left edge makes progress (no VCG cycle)")
        for n in cur:
            placed[n] = len(tracks)
        tracks.append(cur)
    return tracks


TOP, BOT = [1, 1, 3, 0, 2, 4, 0, 4], [2, 3, 0, 2, 0, 3, 4, 0]
sp = spans(TOP, BOT)
ok(sp == {1: (0, 1), 2: (0, 4), 3: (1, 5), 4: (5, 7)}, "net spans")
ans("channel-density", density(sp, len(TOP)))
vcg = {(a, b) for a, b in zip(TOP, BOT) if a and b and a != b}
ok(vcg == {(1, 2), (1, 3), (4, 3)}, "VCG edges")
ok(left_edge(sp, vcg) == [[1, 4], [2], [3]], "constrained left edge: tracks {1,4} {2} {3}")
items = {"a": (0, 2), "b": (3, 6), "c": (1, 4), "d": (5, 7)}
tr = left_edge(items)
ok(tr == [["a", "b"], ["c", "d"]], "left edge item tracks")
ans("left-edge-tracks", len(tr))
close(max(sum(1 for lo, hi in items.values() if lo <= c <= hi) for c in range(8)), 2, 0, "item density 2")

# ==== switchbox-otc ====
ans("otc-height", 8 * 0.5 - 5 * 0.5, 1e-9)

# ==== special-routing ====
close(1 + 3 * sqrt(2), 5.24, 0.001, "octilinear (3,4)")
ans("octilinear", round(3 + 2 * sqrt(2), 2), 0.005)
close(2 * sqrt(2), 2.83, 0.002, "2 sqrt 2")
close(sqrt(29), 5.39, 0.001, "sqrt 29")
ans("skew-value", max(1.20, 1.35, 1.28, 1.31) - min(1.20, 1.35, 1.28, 1.31), 1e-9)
tap = lambda t1, t2, L: (L + t2 - t1) / 2
close(tap(2, 4, 10), 6, 1e-12, "worked tap 6")
close(2 + 6, 4 + 4, 0, "both sides 8")
ans("zero-skew-tap", tap(3, 1, 8))
close(3 + tap(3, 1, 8), 1 + 8 - tap(3, 1, 8), 1e-12, "both sides 6")
ans("htree-levels", next(k for k in range(10) if 4**k >= 64))


# ==== sta-algorithms ====
def sta(arr, gates, T=None, setup=0.0, out="out"):
    at = dict(arr)
    for g, ins, d in gates:  # gates listed in topological order
        at[g] = max(at[i] for i in ins) + d
    rat = {}
    if T is not None:
        rat[out] = T - setup
        for g, ins, d in reversed(gates):
            for i in ins:
                rat[i] = min(rat.get(i, float("inf")), rat[g] - d)
    return at, rat


at, rat = sta({"a": 0, "b": 1}, [("g1", "ab", 2), ("g2", ["g1", "a"], 1), ("g3", "b", 2.5), ("out", ["g2", "g3"], 1)], T=6, setup=0.4)
ok((at["g1"], at["g2"], at["g3"], at["out"]) == (3, 4, 3.5, 5), "worked arrival times")
close(rat["out"] - at["out"], 0.6, 1e-12, "worked slack 0.6")
close(rat["g2"], 4.6, 1e-12, "RAT g2 4.6")
close(rat["g1"], 3.6, 1e-12, "RAT g1 3.6")
close(rat["g3"] - at["g3"], 1.1, 1e-12, "g3 slack 1.1")
close(rat["b"] - at["b"], 0.6, 1e-12, "b slack 0.6 (critical)")
close(rat["a"] - at["a"], 1.6, 1e-12, "a slack 1.6")
at, _ = sta({"a": 0.2, "b": 0}, [("g1", "ab", 1.5), ("g2", ["g1", "b"], 1), ("out", ["g2", "a"], 0.5)])
ans("sta-at", at["out"], 1e-9)
ans("sta-slack", (4 - 0.3) - 3.2, 1e-9)
close((3.4 - 0.3) - 3.2, -0.1, 1e-9, "3.4 ns period")
ans("elmore", (2e3 * (5e-15 + 10e-15) + 1e3 * 10e-15) * 1e12, 1e-9)

# ==== timing-driven ====
ans("criticality", 1 - 0.5 / 5, 1e-12)
close(1 - 4 / 5, 0.2, 1e-12, "slack 4 criticality")
close(2 * 400 / 4 + 30, 230, 1e-12, "worked buffer 230")
close(400 - 230, 170, 0, "saves 170")
ans("buffer-three", 3 * 450 / 9 + 2 * 30, 1e-9)


# ==== logic-sim ====
def event_sim(d_inv, d_and):
    """a: 0 -> 1 at t = 0; g1 = NOT a (d_inv), out = AND(a, g1) (d_and). Returns out's change times."""
    val = {"a": 0, "g1": 1, "out": 0}
    queue = [(0, "a", 1)]
    changes = []
    while queue:
        queue.sort()
        t, sig, v = queue.pop(0)
        if val[sig] == v:
            continue
        val[sig] = v
        if sig == "out":
            changes.append((t, v))
        if sig == "a":
            queue.append((t + d_inv, "g1", 1 - val["a"]))
        if sig in ("a", "g1"):
            queue.append((t + d_and, "out", val["a"] & val["g1"]))
    return changes


ok(event_sim(1, 1) == [(1, 1), (2, 0)], "worked glitch 1 -> 2")
ch = event_sim(2, 1)
ok(ch[0] == (1, 1), "out rises at 1")
ans("glitch-width", ch[1][0])
ans("event-saving", (1000 * 100) / (1000 * 0.02 * 100), 1e-9)

# ==== circuit-sim ====
ans("nodal-divider", 10 / 3, 0.0005)
ans("mna-unknowns", 6 + 2)
Is, VT = 1e-14, 0.025


def newton_diode(Vs, R, v0, n):
    vs, v = [], v0
    for _ in range(n):
        f = (Vs - v) / R - Is * (exp(v / VT) - 1)
        fp = -1 / R - Is / VT * exp(v / VT)
        v = v - f / fp
        vs.append(v)
    return vs


close(exp(28), 1.446e12, 0.001, "e^28")
f0 = (3 - 0.7) / 1000 - Is * (exp(28) - 1)
close(f0, -0.01216, 0.001, "f(v0)")
close(-1 / 1000 - Is / VT * exp(28), -0.5795, 0.001, "f'(v0)")
it = newton_diode(3, 1e3, 0.7, 40)
for got, want in zip(it, (0.6790, 0.6634, 0.6559, 0.6546)):
    close(got, want, 0.0001, f"iterate {want}")
close(it[-1], 0.6545, 0.0001, "converged 0.6545")
ans("newton-step", round(1.5 - (1.5**2 - 2) / 3, 4), 0.00005)
v1 = 1.5 - (1.5**2 - 2) / 3
close(v1 - (v1**2 - 2) / (2 * v1), 1.41422, 1e-5, "second iterate")
ans("diode-current", (3 - 0.6545) / 1000 * 1000, 1e-9)
close(Is * exp(0.6545 / VT) * 1000, 2.343, 0.001, "diode formula at 0.6545 V")
close(Is * exp(0.654523 / VT) * 1000, 2.3455, 0.0005, "diode formula at 0.654523 V")
ans("backward-euler", round(1 / 1.1, 3), 0.0005)
close(exp(-0.1), 0.905, 0.001, "exact")
close(1 - 0.1, 0.900, 1e-12, "forward Euler")
close(0.95 / 1.05, 0.905, 0.001, "trapezoidal")
ok(abs(1 - 3) > 1, "forward Euler with h = 3 tau grows")

# ==== drc / lvs ====
ans("lambda-rule", 9 * 0.09, 1e-9)
ans("spacing-check", 0.68 - 0.50, 1e-9)
ans("enclosure-check", (0.28 - 0.20) / 2, 1e-9)
close(0.20 + 2 * 0.05, 0.30, 1e-12, "0.30 um metal")
ans("extract-wl", 1.2 / 0.15, 1e-9)
ans("merge-parallel", 4 * 0.5, 1e-9)

# ==== 结业挑战 ====
pis, k, sols = qm((1, 3, 4, 5, 6))
ans("b-prime-implicants", len(pis))
ok(k == 3 and len(sols) == 2, "boss: 3 terms, two covers")
libB = dict(lib, NAND3=(5, lib["NAND3"][1]))
ans("b-tech-map", best_cost((INV, (NAND, (INV, (NAND, "a", "b")), "c")), libB))
KB = [(1, 2), (1, 4), (2, 4), (2, 3), (3, 5), (3, 6), (5, 6), (4, 5)]
close(cut(KB, {1, 2, 3}), 4, 0, "boss cut 4")
ans("b-kl-gain", kl_gain(KB, {1, 2, 3}, 3, 4))
close(cut(KB, {1, 2, 4}), 2, 0, "boss cut after 2")
ans("b-hpwl", hpwl([(1, 1), (4, 2), (2, 5)]))
close(rsmt([(1, 1), (4, 2), (2, 5)]), 7, 0, "three pins: RSMT = HPWL")
x = quad_place(2, [(0, ("F", 0), 1), (0, 1, 1), (1, ("F", 10), 1), (1, ("F", 4), 1)])
ans("b-quadratic", float(x[0]))
close(float(x[1]), 5.6, 1e-12, "boss x2 5.6")
d, m = lee(["S.#.T", "..#.#", "#.#..", "....."])
ans("b-lee", d)
close(m, 4, 0, "boss Manhattan 4")
ans("b-zero-skew", tap(1, 4, 11))
close(1 + 7, 4 + 4, 0, "boss both sides 8")
at, rat = sta({"a": 0, "b": 0.5}, [("g1", "ab", 1), ("g2", ["g1", "b"], 2), ("g3", "a", 1.5), ("out", ["g2", "g3"], 1)], T=5, setup=0.3)
ans("b-sta-slack", rat["out"] - at["out"], 1e-9)
ok((at["g1"], at["g2"], at["g3"], at["out"]) == (1.5, 3.5, 1.5, 4.5), "boss arrival times")
ok(rat["b"] - at["b"] < rat["a"] - at["a"] and abs((rat["a"] - at["a"]) - (rat["b"] - at["b"]) - 0.5) < 1e-12, "path from a has 0.5 ns more slack")
close(0.5 + 2, 2.5, 0, "b direct into g2 2.5")
nb = newton_diode(5, 1e3, 0.7, 40)
ans("b-newton", round(nb[0], 4), 0.0005)
close((5 - 0.7) / 1000 - Is * (exp(28) - 1), -0.01016, 0.001, "boss f(0.7)")
close(nb[-1], 0.670, 0.001, "boss converged 0.670")
close((5 - nb[-1]) / 1000 * 1000, 4.33, 0.001, "boss 4.33 mA")
ans("b-merge-fingers", 3 / 0.75, 1e-9)
close(3 * 0.75, 2.25, 1e-12, "three fingers 2.25")

# ---- compare with the pack ----
pack = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "data" / "content" / "H.2.8.yaml"
text = pack.read_text(encoding="utf-8")
pairs = re.findall(r"^\s*-?\s*id: ([a-z0-9-]+)\n(?:(?!^\s*-?\s*id: ).*\n)*?\s*answer: ([-0-9.e]+)", text, re.M)
answers = {i: float(a) for i, a in pairs}
assert len(answers) == len(pairs), "duplicate ids with number answers"
missing = [i for i in computed if i not in answers]
assert not missing, f"computed but not in the pack: {missing}"
unchecked = [i for i in answers if i not in computed]
assert not unchecked, f"number answers in the pack without a check here: {unchecked}"
bad = []
for i, (v, tol) in computed.items():
    pa = answers[i]
    if abs(pa - v) > max(tol, 1e-9 * max(1, abs(v))):
        bad.append(f"{i}: pack answer {pa} but computed {v} (allowed ±{tol})")
    checks += 1
assert not bad, "\n".join(bad)

print(f"H.2.8 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
