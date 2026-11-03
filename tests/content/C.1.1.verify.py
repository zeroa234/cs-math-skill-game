# Checks every number, bit pattern and table that data/content/C.1.1.yaml states, by computing it in Python
# (two's complement, IEEE 754 via struct, Huffman with heapq, gates by exhaustive truth tables, caches and the
# 6.004 priority rules as small simulations). Quoted 6.004 facts were checked against the course's Annotated
# Slides (reports/coverage/C.1.1.md).
# usage: python -I tests/content/C.1.1.verify.py   (prints "N/N claims hold"; exit code 1 on any mismatch)
import math, struct, heapq, itertools
from fractions import Fraction as F

checks = []
add = lambda got, want: checks.append((got, want))

# ---------------- information
add([math.log2(n) for n in (2, 8, 16, 32, 1024)], [1, 3, 4, 5, 10])
bits_for = lambda n: next(k for k in range(64) if 2 ** k >= n)
add([bits_for(n) for n in (10, 26, 1000, 128)], [4, 5, 10, 7])

# ---------------- binary-hex
add((0b1011, int("1011", 2), 8 + 2 + 1), (11, 11, 11)); add(0b110101, 53); add(bin(37), "0b100101"); add(32 + 4 + 1, 37)
add((2 ** 8 - 1, 2 ** 16 - 1, 2 ** 32 - 1), (255, 65535, 4294967295))
add((0x9C, hex(156), 9 * 16 + 12, 0b10011100), (156, "0x9c", 156, 156)); add(hex(0b11010110), "0xd6"); add(0xFF, 255)

# ---------------- twos-complement
tc = lambda s: int(s, 2) - (1 << len(s)) * (s[0] == "1")
add([tc(s) for s in ("01111111", "10000000", "11111111", "11111110")], [127, -128, -1, -2])
add(format(37, "08b"), "00100101"); add(format(~37 & 0xFF, "08b"), "11011010"); add(format((~37 + 1) & 0xFF, "08b"), "11011011")
add(((-37) % 256, hex((-37) % 256), bin(219), tc("11011011")), (219, "0xdb", "0b11011011", -37))
add(-128 + 64 + 16 + 8 + 2 + 1, -37); add(tc(format(0x9C, "08b")), -100); add(156 - 256, -100)
add((2 ** 15 - 1, -2 ** 15), (32767, -32768)); add(bin((-1) % 256), "0b11111111"); add(tc(format(0xF6, "08b")), -10)
add(-128 + 64 + 32 + 16 + 8 + 4 + 2, -2)

# ---------------- huffman
def huffman(probs):
    tick = itertools.count()
    heap = [(p, next(tick), {s: ""}) for s, p in probs.items()]
    heapq.heapify(heap)
    first = None
    while len(heap) > 1:
        p1, _, c1 = heapq.heappop(heap); p2, _, c2 = heapq.heappop(heap)
        if first is None: first = sorted([p1, p2])
        heapq.heappush(heap, (p1 + p2, next(tick), {**{s: "0" + c for s, c in c1.items()}, **{s: "1" + c for s, c in c2.items()}}))
    return heap[0][2], first
code, _ = huffman({"A": F(1, 3), "B": F(1, 2), "C": F(1, 12), "D": F(1, 12)})
add({s: len(c) for s, c in code.items()}, {"A": 2, "B": 1, "C": 3, "D": 3})
lesson_code = {"B": "0", "A": "11", "C": "100", "D": "101"}
avg = lambda probs, lens: sum(probs[s] * lens[s] for s in probs)
add(avg({"A": F(1, 3), "B": F(1, 2), "C": F(1, 12), "D": F(1, 12)}, {s: len(c) for s, c in lesson_code.items()}), F(5, 3))
add((round(float(F(5, 3)), 2), round(1000 * 5 / 3)), (1.67, 1667))
def prefix_free(codes): return not any(a != b and b.startswith(a) for a in codes for b in codes)
add([prefix_free(c) for c in (["0", "10", "110", "111"], ["0", "1", "01"], ["1", "10", "100"])] + [prefix_free(list(lesson_code.values()))], [True, False, False, True])
def decode(bits, code):
    rev, out, cur = {c: s for s, c in code.items()}, "", ""
    for b in bits:
        cur += b
        if cur in rev: out += rev[cur]; cur = ""
    return out
add(decode("011100", lesson_code), "BAC")
add(0.5 * 1 + 0.25 * 2 + 0.125 * 3 + 0.125 * 3, 1.75)
c4, _ = huffman({"a": F(1, 2), "b": F(1, 4), "c": F(1, 8), "d": F(1, 8)}); add(sorted(len(v) for v in c4.values()), [1, 2, 3, 3])
_, first = huffman({"a": 0.4, "b": 0.2, "c": 0.2, "d": 0.1, "e": 0.1}); add(first, [0.1, 0.1])
cb, _ = huffman({"a": F(4, 10), "b": F(3, 10), "c": F(2, 10), "d": F(1, 10)})
add(({s: len(c) for s, c in cb.items()}, avg({"a": F(4, 10), "b": F(3, 10), "c": F(2, 10), "d": F(1, 10)}, {s: len(c) for s, c in cb.items()})), ({"a": 1, "b": 2, "c": 3, "d": 3}, F(19, 10)))

# ---------------- error-codes
ham = lambda a, b: sum(x != y for x, y in zip(a, b))
add((ham("0110", "0011"), ham("10110", "11100")), (2, 2))
add("1011001" + str("1011001".count("1") % 2), "10110010")
add((ham("110", "111"), ham("110", "000"), ham("001", "000"), ham("000", "111")), (1, 2, 1, 3))
add((2 * 2 + 1, 3 + 1), (5, 4))
words = [format(v, "03b") + str(bin(v).count("1") % 2) for v in range(8)]
add(min(ham(a, b) for a in words for b in words if a != b), 2)

# ---------------- floating-point
fhex = lambda x: struct.pack(">f", x).hex()
add((fhex(-6.25), fhex(1.0)), ("c0c80000", "3f800000")); add(6.25, 4 + 2 + 0.25); add((2 + 127, format(129, "08b"), 3 + 127), (129, "10000001", 130))
add(format(int(fhex(-6.25), 16), "032b"), "1" + "10000001" + "1001" + "0" * 19)
add((0.1 + 0.2 == 0.3, repr(0.1 + 0.2), math.isclose(0.1 + 0.2, 0.3)), (False, "0.30000000000000004", True))
import sys
add(sys.float_info.mant_dig - 1, 52); add(1 + 11 + 52, 64)

# ---------------- digital-abstraction
VOL, VIL, VIH, VOH = 0.5, 1, 3, 3.5
add((VOL < VIL < VIH < VOH, VIL - VOL, VOH - VIH), (True, 0.5, 0.5)); add(0.4 + 0.5 <= VIL, True); add(3 * 2, 6)

# ---------------- logic-gates / simplify (exhaustive truth tables)
B2, B3 = list(itertools.product([0, 1], repeat=2)), list(itertools.product([0, 1], repeat=3))
n = lambda x: 1 - x
add([(a & b, a | b, a ^ b) for a, b in B2], [(0, 0, 0), (0, 1, 1), (0, 1, 1), (1, 1, 0)])
add(all((a ^ b) == ((n(a) & b) | (a & n(b))) for a, b in B2), True)
maj = lambda a, b, c: int(a + b + c >= 2)
add([r for r in B3 if maj(*r)], [(0, 1, 1), (1, 0, 1), (1, 1, 0), (1, 1, 1)])
add(all(maj(a, b, c) == ((n(a) & b & c) | (a & n(b) & c) | (a & b & n(c)) | (a & b & c)) for a, b, c in B3), True)
nand = lambda a, b: n(a & b)
add((nand(1, 1), nand(0, 1)), (0, 1)); add(all(nand(a, a) == n(a) for a in (0, 1)), True)
add(all(nand(nand(a, b), nand(a, b)) == (a & b) for a, b in B2), True); add(all(nand(a, 0) == 1 for a in (0, 1)), True)
add(all(((a & b) | (a & n(b))) == a for a, b in B2), True); add(all((a | (a & b)) == a for a, b in B2), True)
add(all(n(a & b) == (n(a) | n(b)) and n(a | b) == (n(a) & n(b)) for a, b in B2), True)
add(all(((n(a) & b) | (a & b)) == b for a, b in B2), True)
f = lambda a, b, c: int(format(a * 4 + b * 2 + c, "03b") in ("010", "011", "110", "111"))
add(all(f(a, b, c) == b for a, b, c in B3), True)
add(all(((a & n(b) & c) | (a & b & c)) == (a & c) for a, b, c in B3), True)
mux = lambda s, a, b: (n(s) & a) | (s & b)
add(all(mux(s, a, b) == (b if s else a) for s, a, b in B3), True); add((2 ** 3, 2 ** 4), (8, 16))

# ---------------- adder
def full(a, b, cin): return a ^ b ^ cin, (a & b) | (cin & (a ^ b))
add(all(full(a, b, c) == ((a + b + c) % 2, (a + b + c) // 2) for a, b, c in B3), True); add(full(1, 1, 1), (1, 1))
add(32 * 2, 64)
def add8(x, y, cin=0):
    """ripple-carry 8-bit: returns (sum, carry into bit 7, carry out of bit 7)"""
    c, s, c_in7 = cin, 0, None
    for i in range(8):
        if i == 7: c_in7 = c
        bit, c = full((x >> i) & 1, (y >> i) & 1, c)
        s |= bit << i
    return s, c_in7, c
add(add8(0b00000101, (~0b00000011) & 0xFF, 1)[0], 0b00000010); add((0b00000101 + 0b11111101) & 0xFF, 2)
add(format(add8(0b00001001, (~0b00000100) & 0xFF, 1)[0], "08b"), "00000101"); add(format((~4 + 1) & 0xFF, "08b"), "11111100")
s, ci, co = add8(100, 50); add((format(s, "08b"), tc(format(s, "08b")), ci, co, ci ^ co), ("10010110", -106, 1, 0, 1))
add((0b1100100 + 0b0110010) >> 7, 1)
s2, ci2, co2 = add8((-100) % 256, (-50) % 256); add((tc(format(s2, "08b")), ci2 ^ co2), (106, 1)); add(-150 + 256, 106)
s3, ci3, co3 = add8(60, 50); add((s3, ci3 ^ co3), (110, 0))

# ---------------- alu-bitwise
add((12 & 10, 12 | 10, 12 ^ 10, 9 & 12, 9 ^ 12), (8, 14, 6, 8, 5))
add((0x1234 & 0xFFF, 0x1234 >> 12, 1 * 2 ** 12 + 0x234, 0x1234), (0x234, 1, 4660, 4660))
add(((0x1234 >> 4) & 0x3F, 0x1234 >> 4, 291 - 4 * 64), (35, 0x123, 35)); add(1 | (1 << 3), 9); add((~5, (~5) & 0xFF, format(250, "08b")), (-6, 250, "11111010"))
add(all((x << k) == x * 2 ** k and (x >> k) == x // 2 ** k for x in range(200) for k in range(5)), True)

# ---------------- memory-tech
add(round(10e-3 / 40e-9), 250000); add((10 ** 6, 10 ** 3), (1000000, 1000))

# ---------------- caches
def split(addr, cache_bytes, block, ways=1, addr_bits=32):
    off = int(math.log2(block)); sets = cache_bytes // block // ways; idx = int(math.log2(sets))
    return {"off_bits": off, "idx_bits": idx, "tag_bits": addr_bits - off - idx, "offset": addr & (block - 1), "index": (addr >> off) & (sets - 1), "tag": addr >> (off + idx), "sets": sets}
r = split(0x1234, 1024, 16); add((r["off_bits"], r["idx_bits"], r["tag_bits"], r["offset"], r["index"], r["tag"]), (4, 6, 22, 4, 35, 4))
add(split(0, 4096, 64)["tag_bits"], 20); add(split(0x5678, 1024, 16)["index"], 39); add((0x567, 1383 & 63), (1383, 39))
add(split(0x0400, 1024, 16)["index"], split(0x0000, 1024, 16)["index"]); add(split(0x0400, 1024, 16)["index"], 0)
add(split(0, 1024, 16, ways=2)["sets"], 32); add(split(0, 1024, 16, ways=2)["idx_bits"], 5); add(split(0, 2048, 32)["tag_bits"], 21)
add((1 + 0.05 * 40, 2 + 0.1 * 50), (3.0, 7.0))
def lru_misses(seq, ways):
    s, misses = [], 0
    for x in seq:
        if x in s: s.remove(x)
        else:
            misses += 1
            if len(s) == ways: s.pop(0)
        s.append(x)
    return misses
add((lru_misses("ABACAB", 2), lru_misses("ABACAB", 1), lru_misses("ABCAB", 2)), (4, 6, 5))

# ---------------- io / real-time (6.004 Unit 18 example: disk 500 highest, printer 400, keyboard 800 lowest)
add(1048576 // 4, 262144)
S = {"disk": 500, "printer": 400, "keyboard": 800}; prio = ["disk", "printer", "keyboard"]
fcfs = {d: sum(S[o] for o in S if o != d) for d in S}
weak = {d: max(S[o] for o in S if o != d) + sum(S[o] for o in prio[:prio.index(d)]) for d in S}
strong = {d: sum(S[o] for o in prio[:prio.index(d)]) for d in S}
add((fcfs, weak["disk"], weak["printer"], strong["disk"], strong["printer"]), ({"disk": 1200, "printer": 1300, "keyboard": 900}, 800, 1300, 0, 500))
add((weak["disk"] + S["disk"] > 800, strong["disk"] + S["disk"] <= 800, strong["disk"] + S["disk"]), (True, True, 500))
S2 = {"X": 100, "Y": 200, "Z": 600}; p2 = ["X", "Y", "Z"]
add(max(S2[o] for o in S2 if o != "Y") + sum(S2[o] for o in p2[:1]), 700); add(300 + 200, 500)

# ---------------- registers-clock
add((1 + 6 + 1, round(1 / 8e-9 / 1e6), 1 + 10 + 1, 2 + 15 + 3, round(1 / 20e-9 / 1e6)), (8, 125, 12, 20, 50))

# ---------------- datapath / load-store / branches
add((10 + (-3), 256 + 4, hex(260)), (7, 260, "0x104"))
sext12 = lambda v: v - 4096 if v & 0x800 else v
add((4096 + 8, 0xFFC, sext12(0xFFC), hex(sext12(0xFFC) & 0xFFFFFFFF), 4096 + sext12(0xFFC)), (4104, 4092, -4, "0xfffffffc", 4092))
add((200 + 24, 200 + 4, 300 + 4, 300 + 80, 516 - 4, 100 + 12), (224, 204, 304, 380, 512, 112))

# ---------------- fsm
T = {"A": {"0": "A", "1": "B"}, "B": {"0": "A", "1": "C"}, "C": {"0": "A", "1": "C"}}; OUT = {"A": "0", "B": "0", "C": "1"}
st, outs = "A", ""
for bit in "011101":
    st = T[st][bit]; outs += OUT[st]
add(outs, "001100")
add((bits_for(5), bits_for(9), bits_for(4)), (3, 4, 2)); add((2 ** (3 + 2), 2 ** (2 + 2)), (32, 16))

# ---------------- control-unit (P&H single-cycle RISC-V): each row against what the datapath needs
needs = {
    "add": dict(writes_reg=True, imm_operand=False, reads_mem=False, writes_mem=False, value_from_mem=False, branch=False),
    "lw": dict(writes_reg=True, imm_operand=True, reads_mem=True, writes_mem=False, value_from_mem=True, branch=False),
    "sw": dict(writes_reg=False, imm_operand=True, reads_mem=False, writes_mem=True, value_from_mem=None, branch=False),
    "beq": dict(writes_reg=False, imm_operand=False, reads_mem=False, writes_mem=False, value_from_mem=None, branch=True),
}
table = {"add": (1, 0, 0, 0, 0, 0), "lw": (1, 1, 1, 0, 1, 0), "sw": (0, 1, 0, 1, None, 0), "beq": (0, 0, 0, 0, None, 1)}
derive = lambda d: (int(d["writes_reg"]), int(d["imm_operand"]), int(d["reads_mem"]), int(d["writes_mem"]), None if d["value_from_mem"] is None else int(d["value_from_mem"]), int(d["branch"]))
add({k: derive(v) for k, v in needs.items()}, table)

bad = [(i, got, want) for i, (got, want) in enumerate(checks) if got != want]
for i, got, want in bad:
    print(f"#{i}: got {got!r}, want {want!r}")
print(f"{len(checks) - len(bad)}/{len(checks)} claims hold")
raise SystemExit(1 if bad else 0)
