# Checks every number, array state, traversal order and output that data/content/F.1.1.yaml states, by
# running the structures exactly as the lessons write them (after Morin, Open Data Structures).
# usage: python -I tests/content/F.1.1.verify.py   (prints "N/N claims hold"; exit code 1 on any mismatch)
import io, contextlib, math, sys, json, os, subprocess, heapq
from collections import deque

def out(code, env=None):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(code, dict(env or {}))
    return buf.getvalue()

checks = []
add = lambda got, want: checks.append((got, want))

# ---------------- array-basics
add(2000 + 5 * 8, 2040); add(1000 + 3 * 8, 1024); add(10 - 3, 7); add(5 + 6 + 7, 18); add(4 + 5 + 6, 15)
sizes = []
xs = []
for k in range(20):
    sizes.append(sys.getsizeof(xs)); xs.append(k)
add(len(set(sizes)) < len(sizes), True)          # the list does not grow its storage on every append

# ---------------- array-stack (the lesson's code, with a move counter)
class ArrayStack:
    def __init__(self):
        self.a = [None]
        self.n = 0
        self.moves = 0
        self.copies = 0
    def get(self, i):
        return self.a[i]
    def set(self, i, x):
        y = self.a[i]
        self.a[i] = x
        return y
    def add(self, i, x):
        if self.n == len(self.a):
            self.resize()
        for k in range(self.n, i, -1):
            self.a[k] = self.a[k - 1]
            self.moves += 1
        self.a[i] = x
        self.n += 1
    def resize(self):
        b = [None] * max(1, 2 * self.n)
        for k in range(self.n):
            b[k] = self.a[k]
            self.copies += 1
        self.a = b
    def remove(self, i):
        x = self.a[i]
        for k in range(i, self.n - 1):
            self.a[k] = self.a[k + 1]
            self.moves += 1
        self.n -= 1
        if len(self.a) >= 3 * self.n:
            self.resize()
        return x

s = ArrayStack(); add((s.n, len(s.a)), (0, 1))
s = ArrayStack()
for k in range(6): s.add(s.n, k)
s.moves = 0; s.add(2, "x"); add(s.moves, 4)
s = ArrayStack()
for k in range(5): s.add(s.n, k)
add(len(s.a), 8)
for _ in range(3): s.remove(s.n - 1)
add((s.n, len(s.a)), (2, 4))
s = ArrayStack()
for k in range(5): s.add(s.n, k)
s.moves = 0; s.add(s.n, 9); s.remove(s.n - 1); add(s.moves, 0)
fast = [1, 2, 3, None]; fast[2:4] = fast[1:3]; fast[1] = "x"; add(fast, [1, "x", 2, 3])   # slice-assignment shift

# ---------------- amortized
def copies_after(m):
    s = ArrayStack()
    for k in range(m): s.add(s.n, k)
    return s.copies
add(copies_after(9), 15); add(copies_after(9) < 2 * 9, True); add(copies_after(17), 31); add(1 + 2 + 4 + 8 + 16, 31)
add(all(copies_after(m) < 2 * m for m in range(1, 200)), True)
# naive rule: double when full, halve when half empty -> every op copies 8 at the boundary
a_len, n, naive = 8, 8, []
for op in ["add", "remove"] * 3:
    if op == "add":
        if n == a_len: naive.append(n); a_len *= 2
        n += 1
    else:
        n -= 1
        if n <= a_len // 2: naive.append(n); a_len //= 2
add(naive, [8] * 6)
s = ArrayStack(); s.a = [None] * 60; s.n = 30
removed = 0
while len(s.a) == 60:
    s.remove(s.n - 1); removed += 1
add(removed, 10)
s = ArrayStack(); s.a = [None] * 60; s.n = 30
added = 0
while s.n < len(s.a):
    s.add(s.n, 0); added += 1
add((added, len(s.a)), (30, 60))

# ---------------- rootish
i2b = lambda i: math.ceil((-3 + math.sqrt(9 + 8 * i)) / 2)
def block_pos(i):
    b = 0
    while (b + 1) * (b + 2) // 2 <= i: b += 1
    return b, i - b * (b + 1) // 2
add(sum(range(1, 6)), 15); add(5 * 6 // 2, 15)
add(block_pos(7), (3, 1)); add(i2b(7), 3); add(round(math.sqrt(65), 2), 8.06); add(round((-3 + math.sqrt(65)) / 2, 2), 2.53)
add(all(i2b(i) == block_pos(i)[0] for i in range(10000)), True)
add(block_pos(12), (4, 2)); add(1 + 2 + 3 + 4, 10)
r = 1
while r * (r + 1) // 2 < 100: r += 1
add((r, r * (r + 1) // 2, 13 * 14 // 2), (14, 105, 91))
add(block_pos(20), (5, 5)); add(1 + 2 + 3 + 4 + 5, 15)
s = ArrayStack()
for k in range(100): s.add(s.n, k)
add(len(s.a), 128)
add(max(2 * m for m in range(1, 1000) if 2 * m < 3 * 100), 298)   # a length 2m left after removals to n = 100

# ---------------- sllist
class Node:
    def __init__(self, x):
        self.x = x
        self.next = None
add(out("a = Node(1)\nb = Node(2)\nc = Node(3)\na.next = b\nb.next = c\nprint(a.next.next.x)", {"Node": Node}), "3\n")
class SLList:
    def __init__(self):
        self.head = self.tail = None
        self.n = 0
    def push(self, x):
        u = Node(x)
        u.next = self.head
        self.head = u
        if self.n == 0:
            self.tail = u
        self.n += 1
    def pop(self):
        x = self.head.x
        self.head = self.head.next
        self.n -= 1
        if self.n == 0:
            self.tail = None
        return x
    def add(self, x):
        u = Node(x)
        if self.n == 0:
            self.head = u
        else:
            self.tail.next = u
        self.tail = u
        self.n += 1
    def items(self):
        p, r = self.head, []
        while p: r.append(p.x); p = p.next
        return r
L = SLList(); L.push(1); L.push(2); add(L.items(), [2, 1]); L.add(3); add(L.items(), [2, 1, 3]); add(L.pop(), 2); add(L.items(), [1, 3])
L = SLList()
for k in range(5): L.add(k)
p, steps = L.head, 0
for _ in range(3): p = p.next; steps += 1
add((steps, p.x), (3, 3))

# ---------------- dllist
class DNode:
    def __init__(self, x=None):
        self.x = x
        self.prev = self.next = None
class DLList:
    def __init__(self):
        self.dummy = DNode()
        self.dummy.next = self.dummy.prev = self.dummy
        self.n = 0
    def add_before(self, w, x):
        u = DNode(x)
        u.prev = w.prev
        u.next = w
        u.next.prev = u
        u.prev.next = u
        self.n += 1
        return u
    def remove(self, w):
        w.prev.next = w.next
        w.next.prev = w.prev
        self.n -= 1
    def get_node(self, i):
        steps = 0
        if i < self.n / 2:
            p = self.dummy.next
            for _ in range(i): p = p.next; steps += 1
        else:
            p = self.dummy
            for _ in range(self.n - i): p = p.prev; steps += 1
        return p, steps
    def items(self):
        p, r = self.dummy.next, []
        while p is not self.dummy: r.append(p.x); p = p.next
        return r
D = DLList(); add((D.dummy.next is D.dummy, D.dummy.prev is D.dummy), (True, True))
D = DLList()
for k in range(10): D.add_before(D.dummy, k)
node, st = D.get_node(8); add((node.x, st), (8, 2))
D = DLList()
for k in range(20): D.add_before(D.dummy, k)
node, st = D.get_node(17); add((node.x, st), (17, 3))
# wrong order: w.prev = u first
D = DLList(); w = D.add_before(D.dummy, "w")
u = DNode("u"); w.prev = u; u.prev = w.prev
add(u.prev is u, True)
D = DLList()
nodes = [D.add_before(D.dummy, k) for k in [1, 2, 3]]
D.remove(nodes[1]); add((D.items(), D.dummy.next.next.x), ([1, 3], 3))
add([p.x for p in [D.dummy.prev, D.dummy.prev.prev]], [3, 1])
D = DLList(); D.add_before(D.dummy.next, "first"); D.add_before(D.dummy, "last"); D.add_before(D.dummy.next, "new-first")
add(D.items(), ["new-first", "first", "last"])

# ---------------- selist
add(100 // (4 + 1), 20); add(round(95 / 10), 10)

# ---------------- stack-queue-adt
add(out('s = []\nfor c in "abc":\n    s.append(c)\nprint(s.pop() + s.pop())'), "cb\n")
def brackets(text):
    pair = {")": "(", "]": "[", "}": "{"}
    st = []
    for i, c in enumerate(text):
        if c in "([{": st.append(c)
        elif c in pair:
            if not st or st[-1] != pair[c]: return ("bad", i, st[-1] if st else None)
            st.pop()
    return ("ok",) if not st else ("open",)
add(brackets("([]{})"), ("ok",)); add(brackets("([)]"), ("bad", 2, "["))
q = deque([1, 2]); q.append(3); add(q.popleft(), 1)

# ---------------- array-queue (the lesson's code)
class ArrayQueue:
    def __init__(self, a, j, n):
        self.a, self.j, self.n = a, j, n
    def add(self, x):
        if self.n + 1 > len(self.a):
            self.resize()
        self.a[(self.j + self.n) % len(self.a)] = x
        self.n += 1
    def remove(self):
        x = self.a[self.j]
        self.j = (self.j + 1) % len(self.a)
        self.n -= 1
        if len(self.a) >= 3 * self.n:
            self.resize()
        return x
    def resize(self):
        b = [None] * max(1, 2 * self.n)
        for k in range(self.n):
            b[k] = self.a[(self.j + k) % len(self.a)]
        self.a = b
        self.j = 0
Q = ArrayQueue(["y", None, None, None, "a", "b"], 4, 3); Q.a[0] = "c"; Q.add("x"); add(Q.a[1], "x"); add((4 + 3) % 6, 1)
Q = ArrayQueue([None, None, None, None, None, "a"], 5, 2); Q.a[0] = "b"; Q.remove(); add(Q.j, 0)
Q = ArrayQueue(["c", "d", "a", "b"], 2, 4); Q.add("e"); add((Q.a, Q.j), (["a", "b", "c", "d", "e", None, None, None], 0))
add(min(8, 10 - 8), 2); add(min(1, 10 - 1), 1)

# ---------------- two-stacks
add(out('inn, out = [], []\nfor x in [1, 2, 3]:\n    inn.append(x)\nif not out:\n    while inn:\n        out.append(inn.pop())\nprint(out.pop())'), "1\n")
add(out('inn, out = [], []\nfor x in [1, 2, 3, 4, 5]:\n    inn.append(x)\nif not out:\n    while inn:\n        out.append(inn.pop())\nfirst = out.pop()\nprint(first, len(out))'), "1 4\n")
class TwoStackQueue:
    def __init__(self): self.inn, self.out, self.ops = [], [], 0
    def enqueue(self, x): self.inn.append(x); self.ops += 1
    def dequeue(self):
        if not self.out:
            while self.inn: self.out.append(self.inn.pop()); self.ops += 2
        self.ops += 1
        return self.out.pop()
T = TwoStackQueue()
for k in [1, 2, 3, 4]: T.enqueue(k)
first = T.dequeue(); T.enqueue(5); add((first, T.dequeue()), (1, 2))
T = TwoStackQueue(); got = []
for k in range(1000):
    T.enqueue(k)
    if k % 3 == 2: got.append(T.dequeue())
while T.inn or T.out: got.append(T.dequeue())
add((got == list(range(1000)), T.ops <= 4 * 1000), (True, True))
add(3 * 2 < 7, True); add((9 // 2, 9 - 9 // 2), (4, 5))

# ---------------- hash-chaining
add(2026 % 10, 6); add(47 % 10, 7); add(17 % 10 == 47 % 10, True); add([k % 7 for k in [3, 10, 17, 5]], [3, 3, 3, 5])
add([k % 5 for k in [12, 7, 22, 9]], [2, 2, 2, 4]); add(6 / 8, 0.75)
mh = lambda x, z=157, w=8, d=3: ((z * x) % 2 ** w) // 2 ** (w - d)
add((157 * 5, 785 % 256, mh(5)), (785, 17, 0)); add((157 * 3, 471 % 256, mh(3)), (471, 215, 6))

# ---------------- linear-probing
DEL = object()
class LinearTable:
    def __init__(self, m): self.t = [None] * m
    def add(self, x):
        i = x % len(self.t)
        while self.t[i] is not None and self.t[i] is not DEL: i = (i + 1) % len(self.t)
        self.t[i] = x; return i
    def find(self, x):
        i, seen = x % len(self.t), 0
        while self.t[i] is not None:
            seen += 1
            if self.t[i] == x: return True, seen
            i = (i + 1) % len(self.t)
        return False, seen + 1
H = LinearTable(7)
add([H.add(k) for k in [10, 22, 31, 4, 15]], [3, 1, 4, 5, 2]); add(list(H.t), [None, 22, 15, 10, 31, 4, None])
add(H.add(28), 0); add(list(H.t), [28, 22, 15, 10, 31, 4, None])
add(H.find(4), (True, 2)); add(H.find(11), (False, 3)); add(H.find(22), (True, 1))
cleared = LinearTable(7); cleared.t = [28, 22, 15, 10, None, 4, None]; add(cleared.find(4)[0], False)
marked = LinearTable(7); marked.t = [28, 22, 15, 10, DEL, 4, None]; add(marked.find(4)[0], True)
probes = lambda a: (1 + 1 / (1 - a) ** 2) / 2
add((probes(0.5), round(probes(0.9), 6), round(probes(0.8), 6)), (2.5, 50.5, 13.0))
H = LinearTable(7); add([H.add(k) for k in [7, 14, 3, 21]], [0, 1, 3, 2])

# ---------------- hash-codes
add(hash(5), 5); add(ord("a"), 97)
def poly(s):
    h = 0
    for c in s:
        h = h * 31 + ord(c)
    return h
add((poly("ab"), poly("ba")), (3105, 3135)); add(97 * 31 + 98, 3105)
try:
    hash([1, 2]); msg = None
except TypeError as e:
    msg = str(e)
add(msg, "unhashable type: 'list'")
add(hash((1, 2)) == hash((1, 2)), True); add({(1, 2): "A", (2, 1): "B"}[(2, 1)], "B")
runs = {subprocess.run([sys.executable, "-I", "-c", 'print(hash("abc"))'], capture_output=True, text=True).stdout for _ in range(3)}
add(len(runs) > 1, True)
add(len({hash("abc") for _ in range(3)}), 1)

# ---------------- binary-trees
size = lambda t: 0 if t is None else 1 + size(t[0]) + size(t[2])
height = lambda t: -1 if t is None else 1 + max(height(t[0]), height(t[2]))
add(size(((None, "B", None), "A", (None, "C", None))), 3)
d = (None, "D", None); tree = (((d, "B", None)), "A", (None, "C", None))
add((height(tree), height(d), height(None)), (2, 0, -1))
add(out('def size(t):\n    if t is None:\n        return 0\n    return 1 + size(t[0]) + size(t[2])\n\ntree = ((None, "B", None), "A", (None, "C", None))\nprint(size(tree))'), "3\n")
add(out('def height(t):\n    if t is None:\n        return -1\n    return 1 + max(height(t[0]), height(t[2]))\n\nd = (None, "D", None)\ntree = (((d, "B", None)), "A", (None, "C", None))\nprint(height(tree))'), "2\n")
T4 = (((None, 4, None), 2, None), 1, (None, 3, None))
pre = lambda t: [] if t is None else [t[1]] + pre(t[0]) + pre(t[2])
ino = lambda t: [] if t is None else ino(t[0]) + [t[1]] + ino(t[2])
post = lambda t: [] if t is None else post(t[0]) + post(t[2]) + [t[1]]
def level(t):
    q, r = deque([t]), []
    while q:
        u = q.popleft()
        if u is not None: r.append(u[1]); q.append(u[0]); q.append(u[2])
    return r
add((pre(T4), ino(T4), level(T4)), ([1, 2, 4, 3], [4, 2, 1, 3], [1, 2, 3, 4]))
add(out('from collections import deque\ntree = (((None, 4, None), 2, None), 1, (None, 3, None))\nq = deque([tree])\nwhile q:\n    t = q.popleft()\n    if t is not None:\n        print(t[1])\n        q.append(t[0])\n        q.append(t[2])'), "1\n2\n3\n4\n")

# ---------------- bst (insert as a leaf; remove a two-child node with the smallest in the right subtree)
class BNode:
    def __init__(self, x): self.x, self.left, self.right = x, None, None
def insert(r, x):
    if r is None: return BNode(x)
    if x < r.x: r.left = insert(r.left, x)
    elif x > r.x: r.right = insert(r.right, x)
    return r
def build(xs):
    r = None
    for x in xs: r = insert(r, x)
    return r
def bh(r): return -1 if r is None else 1 + max(bh(r.left), bh(r.right))
def bin_(r): return [] if r is None else bin_(r.left) + [r.x] + bin_(r.right)
def compares(r, x):
    k = 0
    while r is not None:
        k += 1
        if x == r.x: return k
        r = r.left if x < r.x else r.right
    return k
def remove(r, x):
    if r is None: return None
    if x < r.x: r.left = remove(r.left, x)
    elif x > r.x: r.right = remove(r.right, x)
    elif r.left is None: return r.right
    elif r.right is None: return r.left
    else:
        w = r.right
        while w.left: w = w.left
        r.x = w.x; r.right = remove(r.right, w.x)
    return r
B = build([5, 3, 8, 1, 4, 7, 9])
add((B.x, B.left.x, B.right.x, B.left.left.x, B.left.right.x, B.right.left.x, B.right.right.x), (5, 3, 8, 1, 4, 7, 9))
add((bin_(B), bh(B), compares(B, 4)), ([1, 3, 4, 5, 7, 8, 9], 2, 3))
B2 = build([6, 2, 9, 4, 8]); add((bin_(B2), bh(B2)), ([2, 4, 6, 8, 9], 2))
B = remove(B, 5); add((B.x, bin_(B)), (7, [1, 3, 4, 7, 8, 9]))
add(bh(build([1, 2, 3, 4, 5])), 4); add(bh(build([8, 3, 10, 1, 6, 14, 4])), 3)

# ---------------- two-four
add(2 ** 3, 8); add(max(h for h in range(40) if 2 ** h <= 1000), 9); add((2 ** 9, 2 ** 10), (512, 1024)); add(5 - 2, 3); add(1 + 2, 3)

# ---------------- red-black: trees as (left, key, colour, right), colour "R" / "B"; None counts as black
def rb_ok(t):
    """(no red edge, black height or None if unequal)"""
    if t is None: return True, 1
    l, k, c, r = t
    okl, hl = rb_ok(l); okr, hr = rb_ok(r)
    red_edge = c == "R" and any(ch is not None and ch[2] == "R" for ch in (l, r))
    ok = okl and okr and not red_edge
    return ok, (hl + (c == "B") if hl == hr and hl is not None else None)
bad = (((None, 3, "R", None), 5, "R", None), 10, "B", (None, 15, "R", None))
add(rb_ok(bad)[0], False)
good = ((((None, 5, "R", None)), 10, "B", None), 20, "B", (None, 30, "B", None))
add(rb_ok(good), (True, 3))                       # 3 counting the black None below each path: 2 black nodes + nil
def black_on_path(t, key):
    k = 0
    while t is not None:
        k += t[2] == "B"
        if key == t[1]: return k
        t = t[0] if key < t[1] else t[3]
    return k
add(black_on_path(good, 5), 2); add(black_on_path(good, 30), 2)
add(round(2 * math.log2(10 ** 6), 2), 39.86)
def left_leaning_ok(t):
    if t is None: return True
    l, _, _, r = t
    colour = lambda u: "B" if u is None else u[2]
    return (not (colour(l) == "B" and colour(r) == "R")) and left_leaning_ok(l) and left_leaning_ok(r)
add(left_leaning_ok((None, 1, "B", (None, 2, "R", None))), False); add(left_leaning_ok(((None, 1, "R", None), 2, "B", None)), True)
add(left_leaning_ok(((None, 1, "B", None), 2, "B", (None, 3, "B", None))), True)

# ---------------- graph-storage
E = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
M = [[False] * 5 for _ in range(5)]
for i, j in E: M[i][j] = M[j][i] = True
add(sum(map(sum, M)), 10); add([j for j in range(5) if M[3][j]], [1, 2, 4]); add(5 * 5, 25)
adj = [[] for _ in range(5)]
for i, j in E: adj[i].append(j); adj[j].append(i)
add(adj, [[1, 2], [0, 3], [0, 3], [1, 2, 4], [3]]); add(sum(map(len, adj)), 10); add(5 + 10, 15); add(7 * 2, 14)
add(10000 * 10000, 100000000)

# ---------------- graph-traversal (neighbours in the order the edges are listed)
def adj_of(nodes, edges):
    a = {v: [] for v in nodes}
    for u, v in edges: a[u].append(v); a[v].append(u)
    return a
def bfs(a, r):
    seen, q, order = {r}, deque([r]), [r]
    while q:
        i = q.popleft()
        for j in a[i]:
            if j not in seen: seen.add(j); q.append(j); order.append(j)
    return order
def dfs(a, i, seen=None, order=None):
    seen = set() if seen is None else seen; order = [] if order is None else order
    seen.add(i); order.append(i)
    for j in a[i]:
        if j not in seen: dfs(a, j, seen, order)
    return order
G1 = adj_of("abcde", [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d"), ("d", "e")])
G2 = adj_of("spqrtu", [("s", "p"), ("s", "q"), ("p", "r"), ("q", "t"), ("r", "u"), ("t", "u")])
add(bfs(G2, "s"), list("spqrtu")); add(dfs(G2, "s"), list("sprutq"))
def bfs_dist(a, r):
    dist, q = {r: 0}, deque([r])
    while q:
        i = q.popleft()
        for j in a[i]:
            if j not in dist: dist[j] = dist[i] + 1; q.append(j)
    return dist
add(bfs_dist(G2, "s")["u"], 3); add(bfs(G1, "a"), list("abcde"))

# ---------------- invariants
CHECK = 'def check_bst(t, lo=None, hi=None):\n    if t is None:\n        return True\n    left, x, right = t\n    if lo is not None and x <= lo:\n        return False\n    if hi is not None and x >= hi:\n        return False\n    return check_bst(left, lo, x) and check_bst(right, x, hi)\n\n'
add(out(CHECK + 'bad = ((None, 3, (None, 6, None)), 5, None)\nprint(check_bst(bad))'), "False\n")
add(out(CHECK + 'tree = ((None, 2, None), 4, ((None, 5, None), 7, None))\nprint(check_bst(tree))'), "True\n")
add(out(CHECK + 'print(check_bst(((None, 5, (None, 12, None)), 10, None)), check_bst(((None, 5, (None, 9, None)), 10, None)))'), "False True\n")
def parent_child_only(t):
    if t is None: return True
    l, x, r = t
    return (l is None or l[1] < x) and (r is None or r[1] > x) and parent_child_only(l) and parent_child_only(r)
add(parent_child_only(((None, 3, (None, 6, None)), 5, None)), True)
add(((7 + 1) % 7, 7 + 1 >= 7), (1, True))

# ---------------- binary-heap
left, right, parent = (lambda i: 2 * i + 1), (lambda i: 2 * i + 2), (lambda i: (i - 1) // 2)
add((parent(6), left(4)), (2, 9))
def h_add(a, x, trace=None):
    a.append(x); i = len(a) - 1
    while i > 0 and a[i] < a[parent(i)]:
        a[i], a[parent(i)] = a[parent(i)], a[i]; i = parent(i)
    if trace is not None: trace.append(list(a))
def h_remove(a):
    x = a[0]; a[0] = a[-1]; a.pop(); i = 0
    while True:
        l, r, j = left(i), right(i), i
        if l < len(a) and a[l] < a[j]: j = l
        if r < len(a) and a[r] < a[j]: j = r
        if j == i: return x
        a[i], a[j] = a[j], a[i]; i = j
states, h = [], []
for x in [5, 3, 8, 1, 4, 7, 9]: h_add(h, x, states)
add(states, [[5], [3, 5], [3, 5, 8], [1, 3, 8, 5], [1, 3, 8, 5, 4], [1, 3, 7, 5, 4, 8], [1, 3, 7, 5, 4, 8, 9]])
h2 = []
for x in [4, 2, 6, 1]: h_add(h2, x)
add(h2, [1, 2, 6, 4])
h = [1, 3, 7, 5, 4, 8, 9]
r1 = h_remove(h); s1 = list(h); r2 = h_remove(h); s2 = list(h)
add((r1, s1), (1, [3, 4, 7, 5, 9, 8])); add((r2, s2), (3, [4, 5, 7, 8, 9]))
add(math.floor(math.log2(1000)), 9)
add(out('import heapq\nh = []\nfor x in [5, 1, 4, 2]:\n    heapq.heappush(h, x)\nprint(heapq.heappop(h), heapq.heappop(h))'), "1 2\n")
add(heapq.nsmallest(3, [5, 1, 4, 2, 9]), [1, 2, 4])

# ---------------- meldable-heap (coin flips fixed in the order the lesson gives)
class MNode:
    def __init__(self, x, left=None, right=None): self.x, self.left, self.right = x, left, right
def merge(h1, h2, flips):
    if h1 is None: return h2
    if h2 is None: return h1
    if h2.x < h1.x: h1, h2 = h2, h1
    if flips.pop(0) == "L": h1.left = merge(h1.left, h2, flips)
    else: h1.right = merge(h1.right, h2, flips)
    return h1
mpre = lambda u: [] if u is None else [u.x] + mpre(u.left) + mpre(u.right)
def heap_ordered(u): return u is None or all(c is None or c.x >= u.x for c in (u.left, u.right)) and heap_ordered(u.left) and heap_ordered(u.right)
h1 = MNode(2, MNode(5), MNode(7)); h2 = MNode(3, MNode(4))
m = merge(h1, h2, ["L", "R"])
add((m.x, m.left.x, m.left.left.x, m.left.right.x, m.right.x, mpre(m), heap_ordered(m)), (2, 3, 4, 5, 7, [2, 3, 4, 5, 7], True))
add(merge(MNode(9), MNode(1), ["L"]).x, 1)

bad = [(i, got, want) for i, (got, want) in enumerate(checks) if got != want]
for i, got, want in bad:
    print(f"#{i}: got {got!r}, want {want!r}")
print(f"{len(checks) - len(bad)}/{len(checks)} claims hold")
raise SystemExit(1 if bad else 0)
