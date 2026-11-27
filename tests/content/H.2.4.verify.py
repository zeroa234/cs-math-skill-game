"""H.2.4 VLSI与芯片设计 — every number in data/content/H.2.4.yaml, recomputed.

Run: python -I tests/content/H.2.4.verify.py [path/to/H.2.4.yaml]
Plain Python. Number answers (and the three text answers) are read back from the YAML and compared with the
values computed here, so a typo in either place fails. Independent checks where possible: the unified MOS model
against the square law and for continuity between regions; the equivalent resistances against Rabaey's averaging
formula R_eq = 3/4 V_DD/I_DSAT (1 - 7/9 lambda V_DD); the pass-transistor level and the pseudo-NMOS V_OL by
bisection on the device equations; activity factors and the Euler-path orders by enumeration; the covering example
by dynamic programming over the subject tree; the distributed-line Elmore constant by slicing the line; the
buffer-chain optimum by solving f(ln f - 1) = p; the glitch by an event-driven simulation; the Lee examples by
breadth-first search; test vectors by fault simulation over all inputs; the LFSR period by stepping a 10-bit LFSR.
Device constants are Rabaey, Chandrakasan & Nikolic, Digital Integrated Circuits (2nd ed.), 0.25 um process:
NMOS k' = 115 uA/V^2, V_T0 = 0.43 V, V_DSAT = 0.63 V, lambda = 0.06 /V, gamma = 0.4 V^0.5, -2phi = 0.6 V;
PMOS k' = 30 uA/V^2, |V_T0| = 0.4 V, |V_DSAT| = 1.0 V, |lambda| = 0.1 /V.
"""
import re
import sys
from collections import deque
from itertools import permutations, product
from math import ceil, comb, e, exp, factorial, log, log10, sqrt
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


def bisect(f, a, b, it=200):
    fa = f(a)
    for _ in range(it):
        m = (a + b) / 2
        fm = f(m)
        if (fm > 0) == (fa > 0):
            a, fa = m, fm
        else:
            b = m
    return (a + b) / 2


kn, vtn, vdsatn, lamn = 115e-6, 0.43, 0.63, 0.06
kp, vtp, vdsatp, lamp = 30e-6, 0.4, 1.0, 0.1


def unified(k, wl, vgs, vds, vt, vdsat, lam):
    vgt = vgs - vt
    if vgt <= 0:
        return 0.0
    vmin = min(vgt, vds, vdsat)
    return k * wl * (vgt * vmin - vmin**2 / 2) * (1 + lam * vds)


def In(wl, vgs, vds):
    return unified(kn, wl, vgs, vds, vtn, vdsatn, lamn)


# ==== inverter-dc ====
close(In(1.5, 2.5, 2.5) * 1e3, 0.219, 0.002, "example 0.219 mA")
close(115e-6 * 1.5 * (2.07 * 0.63 - 0.63**2 / 2), 115e-6 * 1.5 * 1.106, 0.001, "bracket 1.106")
close(0.5 * 115e-6 * 1.5 * 2.07**2 * 1.15 * 1e3, 0.425, 0.002, "square law 0.425 mA (with 1+lambda V_DS)")
ok(1.9 < 0.425 / 0.219 < 2.0, "square law about twice")
ans("unified-low-vgs", In(1.5, 1.2, 2.5) * 1e6, 0.2)
close(In(1.5, 1.2, 2.5) * 1e6, 56.9, 0.003, "56.9")
ans("unified-triode", In(1.5, 2.5, 0.3) * 1e6, 0.5)
# continuity of the unified model where V_DS crosses V_DSAT
close(In(1, 2.5, 0.63 - 1e-9), In(1, 2.5, 0.63 + 1e-9), 1e-6, "continuous at V_DSAT")
# 0.25 um: 2.5 V on 0.25 um is 1e5 V/cm
close(2.5 / 0.25e-4, 1e5, 1e-9, "1e5 V/cm")
# V_M = V_DD/2 needs Wp/Wn about 3.4 (no channel-length modulation)
r = (kn * (0.82 * 0.63 - 0.63**2 / 2)) / (kp * (0.85 * 0.85 - 0.85**2 / 2))
close(r, 3.376, 0.002, "Wp/Wn for V_M = 1.25 V (unified model, PMOS not velocity saturated)")
r_rabaey = (kn * vdsatn * (1.25 - vtn - vdsatn / 2)) / (kp * vdsatp * (2.5 - 1.25 - vtp - vdsatp / 2))
close(r_rabaey, 3.48, 0.002, "Rabaey eq. 5.4 with both devices velocity saturated")
ok(3 < r < 3.6 and 3 < r_rabaey < 3.6, "'3 倍多'")

# ==== inverter-delay ====


def req(k, vdd, vt, vdsat, lam):
    idsat = unified(k, 1, vdd, vdd, vt, vdsat, lam) / (1 + lam * vdd)
    return 0.75 * vdd / idsat * (1 - 7 / 9 * lam * vdd)


close(req(kn, 2.5, vtn, vdsatn, lamn) / 1e3, 13, 0.01, "R_eq,n 13 kOhm by the averaging formula")
close(req(kp, 2.5, vtp, vdsatp, lamp) / 1e3, 31, 0.02, "R_eq,p 31 kOhm by the averaging formula")
close(req(kn, 1.5, vtn, vdsatn, lamn) / 1e3, 19, 0.02, "R_eq,n 19 kOhm at 1.5 V")
ok(abs(req(kn, 1.0, vtn, vdsatn, lamn) / 1e3 - 35) / 35 < 0.1, "35 kOhm at 1.0 V (Rabaey's simulated table) within 10% of the formula")
close(13 / 1.5, 8.67, 0.001, "8.67")
close(31 / 4.5, 6.89, 0.001, "6.89")
tphl = 0.69 * 13e3 / 1.5 * 6e-15 * 1e12
tplh = 0.69 * 31e3 / 4.5 * 6e-15 * 1e12
close(tphl, 35.9, 0.002, "35.9 ps")
close(tplh, 28.5, 0.002, "28.5 ps")
close((tphl + tplh) / 2, 32.2, 0.002, "32.2 ps")
ans("tphl-small", 0.69 * 6.5e3 * 10e-15 * 1e12, 0.2)
ans("miller-overlap", 2 * 0.3, 1e-9)

# ==== voltage-scaling ====
close((1.0 / 2.5) ** 2, 0.16, 1e-9, "energy 0.16")
ans("delay-1v", 35 / 13, 0.01)
ans("edp-ratio", 0.16 * 2.69, 0.002)
ans("vt-leakage", 10 ** (100 / 90), 0.05)
close(0.16 * 35 / 13, 0.43, 0.01, "EDP about 0.43")

# ==== static-cmos ====
ans("oai-count", 2 * 4)
ans("nand4-nmos", 4)
# AOI21 sizing: worst pull-down two in series (2 each), C alone 1; pull-up worst two PMOS in series (4 each)
cap_a, cap_c = 2 + 4, 1 + 4
close(cap_a, 6, 1e-9, "input A cap 6")
close(cap_c, 5, 1e-9, "input C cap 5")
# AB+C truth: pulldown conducts exactly when AB+C = 1
for a, b, c in product([0, 1], repeat=3):
    ok(bool((a and b) or c) == bool(a * b + c), "AOI21 pull-down")

# ==== ratioed-logic ====
ans("pseudo-count", 6 + 1)


def vol(ratio, vdd=2.5, vt=0.4):
    vgt = vdd - vt
    f = lambda v: ratio * (vgt * v - v * v / 2) - 0.5 * vgt**2
    return bisect(f, 0.0, vgt)


close(vol(4), 0.281, 0.003, "V_OL ratio 4")
close((8.4 - sqrt(70.56 - 17.64)) / 4, vol(4), 1e-6, "closed form ratio 4")
ans("pseudo-vol-ratio2", vol(2), 0.002)
close((4.2 - sqrt(17.64 - 8.82)) / 2, vol(2), 1e-6, "closed form ratio 2")
ans("pseudo-power", 0.5 * 100e-6 * 2.1**2 * 2.5 * 1e3, 0.002)
close(0.5 * 100 * 2.1**2, 220.5, 1e-9, "220.5 uA")
close(1e4 * 0.551e-3, 5.5, 0.01, "ten thousand gates 5.5 W")


# ==== pass-transistor ====
def vth_body(vsb, vt0=0.43, g=0.4, p=0.6):
    return vt0 + g * (sqrt(p + vsb) - sqrt(p))


vx = bisect(lambda v: 2.5 - v - vth_body(v), 0, 2.5)
close(vx, 1.76, 0.003, "pass level 1.76 V")
close(vth_body(vx), 0.74, 0.01, "V_th 0.74 V")
close(vth_body(2.07), 0.77, 0.01, "V_th at 2.07 V")
close(2.5 - vx, 0.74, 0.01, "loss 0.74")
ans("pass-drop-noeffect", 1.8 - 0.4, 1e-9)
ok(2.5 - 1.76 > 0.4, "PMOS still on")
ans("tg-mux-count", 2 * 2 + 2)

# ==== dynamic-logic ====
ans("dyn-count", 4 + 2)
close(2.5 * 50 / 65, 1.92, 0.003, "charge sharing 1.92 V")
close(2.5 - 2.5 * 50 / 65, 0.58, 0.01, "drop 0.58 V")
ca = bisect(lambda c: 2.5 * c / (c + 30) - 0.43, 0, 30)
ans("charge-share-max", ca, 0.02)
close(0.43 * 30 / 2.07, ca, 1e-6, "closed form 6.23")
# below V_tn the middle transistor cuts off at V_x = V_DD - V_tn: drop = C_a (V_DD - V_tn)/C_L; same C_a at the boundary
close(ca * (2.5 - 0.43) / 30, 0.43, 1e-6, "cut-off case gives the same C_a at 0.43 V")
ok(5 * 2.07 / 30 < 2.5 * 5 / 35, "cut-off case drop is smaller below the boundary")
ok(15 / 50 > 0.43 / 2.07 and 10 / 40 > 0.43 / 2.07, "the 50/15 and 40/10 examples are in the full-sharing case")
ok(2.5 - 1.92 > 0.4 and 0.5 > 0.4, "drops exceed |V_tp| = 0.4 V")
ans("dyn-leak-time", 20e-15 * 0.5 / 1e-9 * 1e6, 1e-6)

# ==== adders ====
ans("ripple-16", 15 * 40 + 60, 1e-9)
G0, P1, G1, C0 = 1 & 1, 1 ^ 0, 1 & 0, 0
close(G1 | (P1 & G0) | (P1 & 0 & C0), 1, 1e-9, "C2 = 1")
# full adder check against integer addition
for a, b, c in product([0, 1], repeat=3):
    s = a ^ b ^ c
    co = (a & b) | (c & (a ^ b))
    ok(2 * co + s == a + b + c, "full adder")
ans("pp-count", 16 * 16)
ans("log-shifter-stages", int(log(64, 2) + 0.5))
ok(all(any(sum(bits[i] * 2**i for i in range(6)) == n for bits in product([0, 1], repeat=6)) for n in range(64)), "0..63 from 1,2,4,...,32")

# ==== datapath-design ====
close(32 * 12, 384, 1e-9, "384")
close(200 + 150 + 100, 450, 1e-9, "450")
close(384 * 450, 172800, 1e-9, "172800")
ans("datapath-area", 64 * 9 * 600 / 1e6, 0.0005)

# ==== latches-registers ====
ans("fmax-regs", 1 / (100 + 1200 + 60) * 1e6, 0.5)
ans("hold-slack-basic", 60 + 20 - 50, 1e-9)
ans("ms-count", 2 * (2 * 2 + 2 * 2))

# ==== dynamic-registers ====
ans("overlap-max", 30 + 40 + 30, 1e-9)
ans("dyn-reg-hold", 5e-15 * 0.3 / 10e-12 * 1e6, 1e-6)
ans("two-phase-high", (2 - 2 * 0.1) / 2, 1e-9)

# ==== pulse-registers ====
ans("pulse-hold", 3 * 30, 1e-9)
ans("borrow-amount", 650 - 500, 1e-9)
ok(650 + 300 <= 1000 and 500 - 150 >= 300, "borrowing fits")
num = exp(800 / 20)
close(num, 2.35e17, 0.005, "e^40")
den = 20e-12 * 1e9 * 1e8
close(den, 2e6, 1e-9, "denominator")
mtbf = num / den
close(mtbf, 1.18e11, 0.005, "MTBF s")
ok(3650 < mtbf / (365.25 * 86400) < 3750, "about 3700 years")
ans("mtbf-ratio", exp(250 / 25), 5)

# ==== cell-layout ====
pd = {"A": ("Y", "n1"), "B": ("n1", "G"), "C": ("Y", "G")}
pu = {"A": ("V", "n2"), "B": ("V", "n2"), "C": ("n2", "Y")}


def walk(g, order):
    nodes = {x for ed in g.values() for x in ed}
    for st in nodes:
        cur, good = st, True
        for edge in order:
            a, b = g[edge]
            if cur == a:
                cur = b
            elif cur == b:
                cur = a
            else:
                good = False
                break
        if good:
            return True
    return False


ok(walk(pd, "ABC") and walk(pu, "ABC"), "A,B,C works for both")
ok(walk(pd, "ACB") and not walk(pu, "ACB"), "A,C,B breaks the pull-up only")
ok(any(walk(pd, o) and walk(pu, o) for o in permutations("ABC")), "some order works")
close(6 * 0.46, 2.76, 1e-9, "2.76")
close(2.76 * 2.72, 7.51, 0.001, "7.51")
close(10000 * 6 * 0.46 * 2.72, 75072, 1e-6, "75072")
close(75072 / 0.7, 107246, 1e-5, "107246")
ans("row-sites", int(500 / 0.46))
close(500 / 0.46, 1086.96, 1e-5, "1086.96")
ans("core-area", 20000 * 5 * 0.46 * 2.72 / 0.8 / 1e6, 0.0002)
close(20000 * 5 * 0.46 * 2.72, 125120, 1e-6, "125120")

# ==== cell-library ====
T = {(0.1, 10): 50, (0.1, 20): 80, (0.2, 10): 60, (0.2, 20): 92}


def bil(sl, c):
    u, v = (sl - 0.1) / 0.1, (c - 10) / 10
    return (1 - u) * (1 - v) * T[(0.1, 10)] + (1 - u) * v * T[(0.1, 20)] + u * (1 - v) * T[(0.2, 10)] + u * v * T[(0.2, 20)]


close((50 + 80) / 2, 65, 1e-9, "65")
close((60 + 92) / 2, 76, 1e-9, "76")
close(bil(0.15, 15), 70.5, 1e-9, "70.5")
# the order of interpolation does not matter
close(((50 + 60) / 2 + (80 + 92) / 2) / 2, 70.5, 1e-9, "other order")
ans("nldm-interp", bil(0.2, 14), 0.05)
ans("spice-energy", 1.8 * 50e-6 * 10e-9 * 1e12, 0.001)

# ==== power-components ====
ans("pdyn-exercise", 0.1 * 1e-9 * 1.0**2 * 1e9, 1e-4)
ans("pdyn-08v", (1 - 0.8**2) * 100, 0.01)
close(0.1 * 0.8**2, 0.064, 1e-9, "0.064 W")


def alpha(f, n):
    p1 = sum(f(*x) for x in product([0, 1], repeat=n)) / 2**n
    return (1 - p1) * p1


close(alpha(lambda a, b: int(not (a or b)), 2), 3 / 16, 1e-12, "NOR2 3/16")
ok(abs(3 / 16 - 0.19) < 0.005 and abs(1 / (3 / 16) - 5.3) < 0.05, "about one fifth")
ans("nand3-alpha", alpha(lambda a, b, c: int(not (a and b and c)), 3), 0.001)
close(alpha(lambda a, b, c: int(not (a and b and c)), 3), 7 / 64, 1e-12, "7/64")
ans("leak-power", 1.0 * 50, 1e-9)


# ==== dynamic-power-reduction ====
def flips(seq):
    return sum(bin(seq[i] ^ seq[(i + 1) % len(seq)]).count("1") for i in range(len(seq)))


b3 = list(range(8))
g3 = [x ^ (x >> 1) for x in b3]
close(flips(b3), 14, 1e-9, "binary 3-bit 14")
close(flips(g3), 8, 1e-9, "gray 3-bit 8")
ok(g3 == [0b000, 0b001, 0b011, 0b010, 0b110, 0b111, 0b101, 0b100], "gray sequence")
close(8 / 14 * 100, 57, 0.01, "57%")
ans("binary-flips-4", flips(list(range(16))))
close(flips([x ^ (x >> 1) for x in range(16)]), 16, 1e-9, "gray 4-bit 16")
ans("clock-gating-save", 1 * 2e-12 * 1.0**2 * 500e6 * 1e3 * 0.8, 0.001)

# ==== leakage-power ====
ans("vt-raise-leak", 10 ** (100 / 85), 0.05)
close(10 ** (100 / 60), 46, 0.01, "46x at 60 mV/dec")
ans("power-gating-avg", 0.1 * 10 + 0.9 * 10 * 0.05, 0.001)

# ==== logical-effort ====
cin_inv = 1 + 2
g_nand2 = (2 + 2) / cin_inv
g_nor2 = (1 + 4) / cin_inv
close(g_nand2, 4 / 3, 1e-12, "g NAND2")
close(g_nor2, 5 / 3, 1e-12, "g NOR2")
for n in range(1, 6):
    close((n + 2) / 3, (n + 2) / cin_inv, 1e-12, "NAND n")  # NMOS n wide each, PMOS 2 each
    close((2 * n + 1) / 3, (1 + 2 * n) / cin_inv, 1e-12, "NOR n")  # NMOS 1, PMOS 2n each
ans("nand2-delay", g_nand2 * 3 + 2, 1e-9)
ans("nor3-g", (1 + 2 * 3) / cin_inv, 0.002)
G = g_nand2 * g_nor2
F = G * 12
f = F ** (1 / 3)
close(F, 26.7, 0.002, "F 26.7")
close(f, 2.99, 0.002, "f 2.99")
close(3 * f + 5, 14.0, 0.003, "D 14.0")
c3 = 12 / f
c2 = g_nor2 * c3 / f
c1 = g_nand2 * c2 / f
close(c3, 4.02, 0.002, "4.02")
close(c2, 2.24, 0.003, "2.24")
close(c1, 1.0, 1e-9, "back to 1")
ans("inv-chain-64", 3 * 64 ** (1 / 3) + 3, 1e-9)
close(4 * 64 ** 0.25 + 4, 15.3, 0.002, "4 stages 15.3")
close(64 ** 0.25, 2.83, 0.002, "2.83")
close(65, 64 + 1, 1e-9, "one stage 65")

# ==== interconnect ====
ans("wire-cap", (30 * 1 * 500 + 2 * 40 * 500) / 1000, 1e-9)
ans("elmore-two", (100 * 30e-15 + 200 * 20e-15) * 1e12, 1e-9)
R = 0.08 * 1000 / 0.2
C = 0.2 * 1000e-15
close(R, 400, 1e-9, "400 Ohm")
close(0.38 * R * C * 1e12, 30.4, 1e-6, "30.4 ps")
close(0.69 * R * C * 1e12, 55.2, 1e-6, "55.2 ps")
close(0.38 * (5 * R) * (5 * C) * 1e12, 760, 1e-6, "760 ps")
N = 4000
elm = sum((R / N) * (C / N) * (N - i) for i in range(N))  # each slice resistor times downstream capacitance
close(elm / (R * C), 0.5, 0.001, "distributed Elmore -> RC/2")
ans("tg-chain", 10e3 * 5e-15 * sum(range(1, 5)) * 1e12, 0.1)

# ==== buffer-chains ====
ans("buffer-stages", round(log(4096, 4)))
close(6 * 4 + 6, 30, 1e-9, "D 30")
fb = 1000 ** (1 / 5)
close(fb, 3.98, 0.002, "3.98")
caps = [2 * fb**i for i in range(5)]
close(caps[1], 7.96, 0.002, "8 fF")
close(caps[2], 31.7, 0.003, "32 fF")
close(caps[3], 126, 0.003, "126 fF")
close(caps[4], 502, 0.002, "502 fF")
ans("buffer-delay", 5 * fb + 5, 0.05)
close(1001 / (5 * fb + 5), 40, 0.01, "40 times slower")
fopt = bisect(lambda x: x * (log(x) - 1) - 1, 2.8, 6)  # minimise N(F^(1/N) + p) with p = 1
close(fopt, 3.59, 0.002, "optimum with p = 1 about 3.6")
close(bisect(lambda x: x * (log(x) - 1), 2, 4), e, 1e-6, "optimum without p is e")
ans("low-swing-energy", 1e-12 * 1.2 * 0.3 * 1e12, 0.001)
close(1e-12 * 1.2**2 * 1e12, 1.44, 1e-9, "full swing 1.44 pJ")

# ==== power-distribution ====
close(10 / 1.0, 10, 1e-9, "10 A")
ans("ir-drop", 2 * 20e-3 * 1e3, 1e-9)
ok(40 / 900 > 0.04, "over 4% of 0.9 V")
ans("ldidt", 0.5e-9 * 1 / 1e-9, 1e-9)
close(1 * 1e-9 / 0.05 * 1e9, 20, 1e-9, "20 nF")
ans("decap-size", 0.5 * 2e-9 / 0.03 * 1e9, 0.05)

# ==== clock-skew-jitter ====
ans("skew-setup", 80 + 700 + 40 - 40, 1e-9)
close(80 + 700 + 40, 820, 1e-9, "820 without skew")
ans("skew-hold", (50 + 40) - (30 + 70), 1e-9)
close((50 + 40) - 30, 60, 1e-9, "+60 without skew")
close(80 + 700 + 40 - 50 + 2 * 20, 810, 1e-9, "810 with jitter")

# ==== clock-distribution ====
ans("htree-levels", round(log(1024, 4)))
ans("pll-n", 2e9 / 25e6, 1e-9)
ans("dual-rail-wires", 16 * 2)

# ==== design-flow ====
ans("die-area", (2 + 2 * 0.25) * (1.5 + 2 * 0.25), 1e-9)

# ==== synthesis-mapping ====
ok(any((a & b | a & c) != (a & b & c) for a, b, c in product([0, 1], repeat=3)), "AB+AC != ABC")
ok(all((a & b | a & c) == (a & (b | c)) for a, b, c in product([0, 1], repeat=3)), "AB+AC = A(B+C)")
ans("literal-count", 4)
ok(len("ABACAD") == 6, "6 literals before factoring")


# tree covering by dynamic programming: nodes are ('INV', x), ('NAND2', x, y) or leaf strings
def best(node, lib):
    if isinstance(node, str):
        return 0
    costs = []
    for name, pat, cost in lib:
        leaves = match(pat, node)
        if leaves is not None:
            costs.append(cost + sum(best(l, lib) for l in leaves))
    return min(costs)


def match(pat, node):
    if pat == "*":
        return [node]
    if isinstance(node, str) or pat[0] != node[0] or len(pat) != len(node):
        return None
    out = []
    for p, n in zip(pat[1:], node[1:]):
        m = match(p, n)
        if m is None:
            return None
        out += m
    return out


INV = ("INV", "*")
NAND2 = ("NAND2", "*", "*")
AND2 = ("INV", ("NAND2", "*", "*"))
AOI21 = ("INV", ("NAND2", ("NAND2", "*", "*"), ("INV", "*")))
NAND3 = ("NAND2", ("INV", ("NAND2", "*", "*")), "*")
lib1 = [("INV", INV, 2), ("NAND2", NAND2, 3), ("AND2", AND2, 4), ("AOI21", AOI21, 6)]
tree1 = ("INV", ("NAND2", ("NAND2", "a", "b"), ("INV", "c")))
close(best(tree1, lib1), 6, 1e-9, "AOI21 cover 6")
close(2 + 3 + 3 + 2, 10, 1e-9, "naive 10")
close(4 + 3 + 2, 9, 1e-9, "AND2 cover 9")
lib2 = [("INV", INV, 2), ("NAND2", NAND2, 3), ("AND2", AND2, 4), ("NAND3", NAND3, 4)]
tree2 = ("NAND2", ("INV", ("NAND2", "a", "b")), "c")
ans("cover-nand3", best(tree2, lib2))
for a, b, c in product([0, 1], repeat=3):
    ok(int(not ((not (not (a and b))) and c)) == int(not (a and b and c)), "tree2 is NAND3")
ans("lut6-bits", 2**6)

# ==== place-route ====
close(log10(factorial(100)), 157.97, 1e-4, "100! about 9.3e157")
close(factorial(100) / 10**157, 9.33, 0.001, "9.33")
pins = [(1, 2), (4, 6), (3, 1)]
ans("hpwl", (max(p[0] for p in pins) - min(p[0] for p in pins)) + (max(p[1] for p in pins) - min(p[1] for p in pins)))
ans("anneal-prob", exp(-5 / 10), 0.001)
close(exp(-5), 0.0067, 0.01, "e^-5")
xs = [i / 1000 for i in range(0, 10001)]
xbest = min(xs, key=lambda x: 1 * x**2 + 3 * (x - 10) ** 2)
ans("quad-place", (1 * 0 + 3 * 10) / 4, 0.001)
close(xbest, 7.5, 1e-9, "grid minimum 7.5")
close(min(xs, key=lambda x: 2 * x**2 + (x - 6) ** 2), 2, 1e-9, "worked example x = 2")
close((2 * 0 + 1 * 6) / 3, 2, 1e-12, "weighted average 2")


def lee(start, goal, walls, n=5):
    q, dist = deque([start]), {start: 0}
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            v = (x + dx, y + dy)
            if 0 <= v[0] < n and 0 <= v[1] < n and v not in walls and v not in dist:
                dist[v] = dist[(x, y)] + 1
                q.append(v)
    return dist


d1 = lee((0, 0), (4, 0), {(2, 0), (2, 1), (2, 2), (2, 3)})
close(d1[(4, 0)], 12, 1e-9, "Lee example 12")
close(d1[(2, 4)], 6, 1e-9, "gap reached at step 6")
d2 = lee((0, 2), (4, 2), {(2, 1), (2, 2), (2, 3), (2, 4)})
ans("lee-steps", d2[(4, 2)])

# ==== timing-verification ====
close(2**64, 1.845e19, 0.001, "2^64")
ans("exhaustive-years", 2**64 / 1e9 / (365.25 * 86400), 1)


# event-driven simulation of Y = NAND(A, NOT A), inverter 1 ns, NAND 2 ns, A rises at t = 0
def simulate():
    val = {"A": 0, "NA": 1, "Y": 1}
    events = [(0, "A", 1)]
    trace = []
    while events:
        events.sort()
        t, sig, v = events.pop(0)
        if val[sig] == v:
            continue
        val[sig] = v
        trace.append((t, sig, v))
        if sig == "A":
            events.append((t + 1, "NA", 1 - v))
            events.append((t + 2, "Y", int(not (val["A"] and val["NA"]))))
        if sig == "NA":
            events.append((t + 2, "Y", int(not (val["A"] and val["NA"]))))
    return trace


tr = [x for x in simulate() if x[1] == "Y"]
ok(tr == [(2, "Y", 0), (3, "Y", 1)], f"glitch events {tr}")
ans("event-glitch", tr[1][0] - tr[0][0], 1e-9)

# ==== sta-setup ====
close(max(300, 450) + 100, 550, 1e-9, "guess 550")
at_g1, at_g2 = 100 + 150, 100 + 250
at_g3 = max(at_g1, at_g2) + 200
close(at_g3, 550, 1e-9, "AT 550")
close(600 - 50 - at_g3, 0, 1e-9, "slack 0")
close(550 - (100 + 150 + 200), 100, 1e-9, "G1 path slack 100")
ans("slack-sign", 460 - 480, 1e-9)
at = 80 + max(120, 200) + 90 + 60
ans("sta-slack", 500 - 40 - at, 1e-9)
ans("sta-fmax", 1 / (430 + 40) * 1e3, 0.002)

# ==== skew-hold ====
ans("hold-slack-skew", (60 + 30) - (40 + 80), 1e-9)
nb = ceil(30 / 12)
close(nb, 3, 1e-9, "3 buffers")
close(nb * 12 - 30, 6, 1e-9, "+6 ps")
close(200 - nb * 12, 164, 1e-9, "setup 164")
ans("hold-buffers", ceil(25 / 10))

# ==== timing-exceptions ====
gray = {}
gray["gray-6"] = format(6 ^ (6 >> 1), "03b")
ans("multicycle-slack", 2 * 1 - 0.05 - (0.1 + 1.6), 0.001)
close(1 - 0.05 - 1.7, -0.75, 1e-9, "single-cycle -0.75")
close(2 - 0.05 - (0.1 + 1.5), 0.35, 1e-9, "worked example 0.35")
close(1 - 0.05 - 1.6, -0.65, 1e-9, "worked example single-cycle -0.65")
# counter 0111 -> 1000 with per-bit sync can show 1111
ok((0b0111 & 0b0111) | (0b1000 & 0b1000) == 0b1111, "mixed sample 1111")

# ==== fault-models ====
ans("stuck-count", 12 * 2)


def detects(circ, fault, n=3):
    return [v for v in product([0, 1], repeat=n) if circ(v, None) != circ(v, fault)]


def y1(v, fault):
    a, b, c = v
    if fault == ("A", 0):
        a = 0
    if fault == ("B", 1):
        b = 1
    return (a & b) | c


ok(detects(y1, ("A", 0)) == [(1, 1, 0)], "A s-a-0 only 110")
tv = detects(y1, ("B", 1))
ok(tv == [(1, 0, 0)], f"B s-a-1 only 100: {tv}")
gray["test-b-sa1"] = " ".join(map(str, tv[0]))
ans("defect-level", (1 - 0.5**0.05) * 100, 0.01)
close(0.5**0.05, 0.9659, 1e-4, "0.9659")
close((1 - 0.5**0.001) * 1e6, 693, 0.002, "about 690 ppm at 99.9%")

# ==== scan-bist ====
cyc = 1000 * (10000 + 1) + 10000
close(cyc, 10011000, 1e-9, "cycles")
close(cyc / 1e8, 0.1, 0.002, "0.1 s")
close((1000 * (1000 + 1) + 1000) / 1e8 * 1e3, 10.02, 1e-6, "10 chains about 10 ms")
L = 20000 // 4
ans("scan-time", (2000 * (L + 1) + L) / 50e6 * 1e3, 0.05)
close(2000 * 5001 + 5000, 10007000, 1e-9, "10 007 000 cycles")


def lfsr_period(n, taps):
    st = start = 1
    k = 0
    while True:
        fb = 0
        for t in taps:
            fb ^= (st >> (t - 1)) & 1
        st = ((st << 1) | fb) & ((1 << n) - 1)
        k += 1
        if st == start:
            return k


ans("lfsr-period", lfsr_period(10, (10, 7)))
close(lfsr_period(10, (10, 7)), 2**10 - 1, 1e-9, "maximal 10-bit")

# ==== 结业挑战 ====
ans("b-unified", In(3, 1.5, 2.5) * 1e6, 0.3)
ans("b-charge-share", 2.5 * 40 / 50, 1e-9)
ans("b-fmax", 1 / (90 + 850 + 45) * 1e6, 1)
T2 = {(0.05, 8): 30, (0.05, 16): 48, (0.15, 8): 38, (0.15, 16): 58}
u, v = (0.08 - 0.05) / 0.1, (12 - 8) / 8
b_nldm = (1 - u) * (1 - v) * T2[(0.05, 8)] + (1 - u) * v * T2[(0.05, 16)] + u * (1 - v) * T2[(0.15, 8)] + u * v * T2[(0.15, 16)]
ans("b-nldm", b_nldm, 0.05)
close((30 + 48) / 2, 39, 1e-9, "39")
close((38 + 58) / 2, 48, 1e-9, "48")
close(39 + 0.3 * 9, b_nldm, 1e-9, "41.7")
ans("b-core-area", 50000 * 4 * 0.46 * 2.72 / 0.75 / 1e6, 0.0005)
close(50000 * 4 * 0.46 * 2.72, 250240, 1e-6, "250240")
ans("b-pdyn", 0.15 * 2e-9 * 0.81 * 8e8, 0.0005)
Fb = g_nand2 * g_nor2 * 18
close(Fb, 40, 1e-9, "F 40")
ans("b-logical-effort", 3 * Fb ** (1 / 3) + 5, 0.02)
ans("b-skew-jitter", 100 + 650 + 50 - 30 + 2 * 25, 1e-9)
ans("b-sta-slack", 520 - 30 - (70 + max(150 + 120, 180 + 120, 400)), 1e-9)
ans("b-hold-fix", ceil(52 / 15))
close(ceil(52 / 15) * 15 - 52, 8, 1e-9, "+8 ps")
ans("b-multicycle", 3 - 0.08 - (0.12 + 2.6), 0.001)


def y2(v, fault):
    a, b, c = v
    if fault == ("A", 0):
        a = 0
    return (a | b) & c


tv2 = detects(y2, ("A", 0))
ok(tv2 == [(1, 0, 1)], f"(A+B)C, A s-a-0 only 101: {tv2}")
gray["b-test-vector"] = " ".join(map(str, tv2[0]))
ans("b-defect-level", (1 - 0.7**0.02) * 100, 0.002)
ans("b-scan-time", (500 * (1000 + 1) + 1000) / 1e8 * 1e3, 0.005)

# ---- compare with the pack ----
pack = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "data" / "content" / "H.2.4.yaml"
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
texts = dict(re.findall(r"^\s*-?\s*id: ([a-z0-9-]+)\n(?:(?!^\s*-?\s*id: ).*\n)*?\s*answers: \['([^']+)'\]", text, re.M))
assert set(texts) == set(gray), f"text answers {sorted(texts)} vs checked {sorted(gray)}"
for i, v in gray.items():
    assert texts[i] == v, f"{i}: pack {texts[i]!r} but computed {v!r}"
    checks += 1

print(f"H.2.4 verify.py: all {checks} checks passed ({len(answers)} number answers, {len(texts)} text answers in the pack).")
