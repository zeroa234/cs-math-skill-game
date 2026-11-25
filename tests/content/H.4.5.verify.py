"""H.4.5 PLC与工业自动化 — every number in data/content/H.4.5.yaml, recomputed.

Run: python -I tests/content/H.4.5.verify.py
Plain Python. IEC 61131-3 TON / TOF / TP and a retentive on-delay timer simulated on a 1 ms grid;
edge detection, CTU/CTUD and the seal-in rung run scan by scan; truth tables enumerated; the chance
of sampling a short pulse found by sweeping its phase; Modbus RTU frames built byte by byte with the
CRC-16 (polynomial 0xA001) and checked against the published example; analog scaling and the rest
from the formulas taught. Number answers are read back from the YAML and compared here.
"""
import math
import re
from itertools import product
from pathlib import Path

checks = 0
computed = {}


def close(x, y, tol=1e-9, what=""):
    global checks
    if abs(x - y) > tol * max(1.0, abs(y)) and abs(x - y) > tol:
        raise AssertionError(f"{what}: {x} != {y}")
    checks += 1


def ok(cond, what):
    global checks
    if not cond:
        raise AssertionError(what)
    checks += 1


def ans(item_id, value, tol=1e-9):
    computed[item_id] = (value, tol)


DT = 0.001  # 1 ms grid


def wave(segments, t_end):
    """segments: list of (t_on, t_off) where the input is 1; returns samples on the grid."""
    n = int(round(t_end / DT))
    return [1 if any(a <= k * DT < b for a, b in segments) else 0 for k in range(n)]


def ton(inp, pt):
    et, q, out = 0.0, 0, []
    for x in inp:
        if x:
            et = min(et + DT, pt)
        else:
            et = 0.0
        q = 1 if (x and et >= pt - 1e-9) else 0
        out.append(q)
    return out


def tof(inp, pt):
    et, q, out = 0.0, 0, []
    for x in inp:
        if x:
            et, q = 0.0, 1
        elif q:
            et += DT
            if et >= pt - 1e-9:
                q = 0
        out.append(q)
    return out


def tp(inp, pt):
    prev, et, q, out = 0, 0.0, 0, []
    for x in inp:
        if x and not prev and not q:
            q, et = 1, 0.0
        if q:
            et += DT
            if et > pt + 1e-9:
                q = 0
        out.append(q)
        prev = x
    return out


def tonr(inp, pt):
    acc, out = 0.0, []
    for x in inp:
        if x:
            acc = min(acc + DT, pt)
        out.append(1 if acc >= pt - 1e-9 else 0)
    return out


def first_on(out):
    return next(k for k, v in enumerate(out) if v) * DT


def last_off(out):
    k = max(i for i, v in enumerate(out) if v)
    return (k + 1) * DT


# ==== 从继电器柜到 PLC ====
ans("plc-sizing", math.ceil(18 * 1.2))
close(math.ceil(9 * 1.2), 11, what="11 outputs")

# ==== 硬件和存储区 ====
ans("bits-in-byte", sum(1 << b for b in (0, 1, 3)))
ans("siemens-address", 1 * 8 + 3)
ans("fx-address", int("12", 8))
close(-(2 ** 15), -32768, what="INT minimum")

# ==== 循环扫描 ====
ans("response-time", 3 + 2 * 10 + 1)


def capture_probability(pulse, scan, steps=10000):
    hit = 0
    for k in range(steps):
        start = k * scan / steps  # pulse start relative to a sample at t = 0, scan, 2 scan, ...
        end = start + pulse
        # a sample at multiples of scan falls inside [start, end)
        if math.floor((end - 1e-12) / scan) >= math.ceil(start / scan) or start == 0:
            hit += 1
    return hit / steps


close(capture_probability(5, 10), 0.5, 0.001, "5 ms in 10 ms caught half the time")
ans("missed-pulse", capture_probability(8, 20), 0.001)
close(capture_probability(25, 20), 1.0, 1e-12, "longer than the scan: always caught")
close(5000 * 0.010, 50, 1e-12, "50 pulses per 10 ms scan")

# ==== 输入设备 ====
ans("encoder-angle", 2750 * 360 / 1000)
ans("pt100", (119.25 - 100) / 0.385)
cvd = 100 * (1 + 3.9083e-3 * 50 - 5.775e-7 * 50 ** 2)  # IEC 60751 Callendar-Van Dusen
ok(abs(cvd - 119.25) < 0.2, "linear 0.385 ohm/degC close to IEC 60751 at 50 degC")

# ==== 输出设备 ====
ans("relay-life", 1e6 / (86400 / 2), 0.5)

# ==== 直流输入 ====
ans("input-current", (24 - 1.2) / 4700 * 1e3, 0.05)

# ==== 模拟量 ====
ans("ma-to-value", (15.2 - 4) / 16 * 10)
close(19354 / 27648, 0.700, 0.001, "0.700 of range")
close(5 * 19354 / 27648, 3.50, 0.001, "3.50 m")
close(4 + 0.7 * 16, 15.2, 1e-12, "15.2 mA")
ans("raw-to-value", -50 + 20736 / 27648 * 200)
ans("adc-resolution", 10 / 4096 * 1e3, 0.005)

# ==== 梯形图 ====
Q = lambda A, B, C: (A or B) and not C
close(int(Q(0, 1, 0)), 1, what="rung example")
ans("rung-truth", sum(1 for A, B, C in product((0, 1), repeat=3) if Q(A, B, C)))
for A, B in product((0, 1), repeat=2):
    ok(((A and not B) or (not A and B)) == (A ^ B), "XOR as two series branches in parallel")

# ==== 启保停 ====
M = 0
for S, P in [(1, 1), (0, 1), (0, 0), (0, 1)]:
    M = int((S or M) and P)
ans("latch-sequence", M)

# ==== IEC 语言 ====
ans("int-range", 2 ** 15 - 1)
for A, B, C in product((0, 1), repeat=3):
    acc = A
    acc = acc and B
    acc = acc or C
    ok(acc == ((A and B) or C), "IL LD/AND/OR/ST order")

# ==== 定时器 ====
out = ton(wave([(0, 3), (4, 20)], 20), 5)
ans("ton-interrupted", first_on(out), 0.002)
ans("timer-preset", round(2.5 / 0.01))
close(5 / 0.1, 50, 1e-9, "100 ms base, 5 s -> 50")
out = tof(wave([(0, 10), (11, 12)], 30), 3)
ans("tof-off-time", last_off(out), 0.002)
out = tp(wave([(0, 0.5), (1, 5)], 10), 2)
ans("tp-length", sum(out) * DT, 0.002)
out = tonr(wave([(0, 3), (5, 20)], 20), 6)
ans("retentive-sum", first_on(out), 0.002)
close(first_on(ton(wave([(0, 3), (5, 20)], 20), 6)), 11, 0.002, "plain TON would need 11 s")
ans("flasher-frequency", 1 / (0.3 + 0.7))
# star-delta: line current ratio
Z = 1.0
I_delta_line = math.sqrt(3) * (1.0 / Z)
I_star_line = (1.0 / math.sqrt(3)) / Z
close(I_star_line / I_delta_line, 1 / 3, 1e-12, "star line current is one third")
ans("star-delta-current", 300 * I_star_line / I_delta_line)

# ==== 计数器 ====
seq = [0, 1, 1, 0, 1, 0, 0, 1, 1, 1]
edges = sum(1 for prev, cur in zip([0] + seq, seq) if cur and not prev)
ans("edge-count", edges)
close(0.3 / 0.010, 30, 1e-9, "level counting adds about 30")
ans("parking-ctud", 100 - (37 - 12))
ans("long-delay", 2 * 3600)
ans("speed-count", 50 / 2 * 60)
# CTU with reset after each 12
cv, boxes = 0, 0
for _ in range(1000):
    cv += 1
    if cv >= 12:
        boxes += 1
        cv = 0
close(cv, 4, what="4 bottles left")

# ==== 顺序控制 ====
ans("active-steps", 3)
ans("traffic-cycle", 30 + 3 + 33)

# ==== 现场总线 ====
def crc16(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return bytes([crc & 0xFF, crc >> 8])


req = bytes([0x11, 0x03, 0x00, 0x00, 0x00, 0x0A])
frame = req + crc16(req)
close(len(frame), 8, what="request is 8 bytes")
# Modbus spec example: slave 0x01 read 0x0002 registers from 0x0000 -> CRC C4 0B
close(int.from_bytes(crc16(bytes([0x01, 0x03, 0x00, 0x00, 0x00, 0x02])), "big"), 0xC40B, what="CRC-16 matches the spec example")
resp_len = lambda n: 1 + 1 + 1 + 2 * n + 2
close(resp_len(10), 25, what="10 registers -> 25 bytes")
close(25 * 11 / 9600 * 1e3, 28.6, 0.002, "28.6 ms at 9600")
ans("modbus-response", resp_len(4))
ans("modbus-time", 25 * 11 / 19200 * 1e3, 0.05)
close(3.5 * 11 / 9600 * 1e3, 4.0, 0.01, "3.5 characters about 4 ms at 9600")

# ==== HMI 和 SCADA ====
ans("polling-cycle", 50 * 0.2)
day = 1000 * 86400 * 8
ans("historian-size", day / 1e6, 0.05)
close(round(day * 365 / 1e9), 252, what="about 252 GB a year")

# ==== 调试 ====
ans("half-split", math.ceil(math.log2(64)))  # 64 segments: each test halves the suspect range
close(64 - 1, 63, what="segment by segment: 63 tests at worst")

# ==== 结业挑战 ====
ans("b-response", 5 + 2 * 15 + 10)
ans("b-siemens-address", 2 * 8 + 5)
ans("b-analog", (9.6 - 4) / 16 * 6)
Qb = lambda A, B, C: (A and not B) or C
ans("b-logic", sum(1 for A, B, C in product((0, 1), repeat=3) if Qb(A, B, C)))
ans("b-timer", round(3 / 0.01))
out = tonr(wave([(0, 4), (6, 9), (12, 30)], 30), 10)
ans("b-retentive", first_on(out), 0.002)
ans("b-counter", boxes)
ans("b-modbus", resp_len(6))

# ---- compare with the pack ----
pack = Path(__file__).resolve().parents[2] / "data" / "content" / "H.4.5.yaml"
text = pack.read_text(encoding="utf-8")
pairs = re.findall(r"^\s*-?\s*id: ([a-z0-9-]+)\n(?:(?!^\s*-?\s*id: ).*\n)*?\s*answer: ([-0-9.e]+)", text, re.M)
answers = {i: float(v) for i, v in pairs}
missing = [i for i in computed if i not in answers]
assert not missing, f"computed but not in the pack: {missing}"
unchecked = [i for i in answers if i not in computed]
assert not unchecked, f"number answers in the pack without a check here: {unchecked}"
for i, (val, tol) in computed.items():
    pa = answers[i]
    if abs(pa - val) > max(tol, 1e-9 * max(1, abs(val))):
        raise AssertionError(f"{i}: pack answer {pa} but computed {val}")
    checks += 1

print(f"H.4.5 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
