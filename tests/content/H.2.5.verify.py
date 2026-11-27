"""H.2.5 半导体器件与微电子基础 — every number in data/content/H.2.5.yaml, recomputed.

Run: python -I tests/content/H.2.5.verify.py [path/to/H.2.5.yaml]
Plain Python. Number answers are read back from the YAML and compared with the values computed here, so a
typo in either place fails. Independent checks where possible: the square law is checked against the triode
formula at pinch-off and by integrating the channel charge along the channel; g_m by a numerical derivative of
the square law; the resistor-load inverter V_OL by bisection on current balance; the CMOS switching point by
bisection on equal currents; the diode small-signal resistance and BJT g_m by numerical derivatives; the
built-in potential from the 60 mV rule and from V_T ln; depletion width by integrating Poisson's equation;
threshold voltage term by term; Dennard ratios from the scaled quantities.
"""
import re
import sys
from math import exp, log, log10, pi, sqrt
from pathlib import Path

checks = 0
computed = {}


def close(a, b, tol=1e-9, what=""):
    global checks
    if abs(a - b) > tol * max(1.0, abs(b)) and abs(a - b) > tol:
        raise AssertionError(f"{what}: {a} != {b}")
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


def simpson(f, a, b, n=2000):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


VT = 0.0259
q = 1.602e-19
e0 = 8.854e-14
eSi = 11.7 * e0
eox = 3.9 * e0
ni = 1e10
kB = 8.617e-5
close(eSi, 1.036e-12, 0.001, "εSi")
close(eox, 3.45e-13, 0.001, "εox")
close(kB * 300, VT, 0.002, "kT/q")

tri = lambda k, vov, vds: k * (vov * vds - vds**2 / 2)
sat = lambda k, vov: 0.5 * k * vov**2

# ==== MOSFET 端特性 ====
close(tri(2, 1.0, 0.2), 0.36, 1e-9, "triode 0.36")
ans("triode-current", tri(2, 1.0, 0.5), 1e-6)
ans("on-resistance", 1 / (2e-3 * 1.0), 1e-6)
# square law equals triode formula at V_DS = V_ov
for k, vov in ((4, 0.5), (1, 0.8)):
    close(tri(k, vov, vov), sat(k, vov), 1e-12, "continuity at pinch-off")
ans("square-law", sat(4, 0.5), 1e-6)
close(sat(1, 0.8), 0.32, 1e-9, "example 0.32")
close(tri(1, 0.8, 1.0), 0.30, 1e-9, "wrong triode 0.30")
ans("clm-current", sat(1, 0.8) * (1 + 0.1 * 2), 1e-6)
ans("backgate-vth", 0.5 + 0.4 * (sqrt(0.7 + 1) - sqrt(0.7)), 0.0005)
close(sqrt(1.7) - sqrt(0.7), 0.467, 0.002, "sqrt difference")
ans("pmos-current", sat(1, 0.8), 1e-6)

# ==== 小信号 ====
gm_num = lambda k, vov: (sat(k, vov + 1e-6) - sat(k, vov - 1e-6)) / 2e-6
I = 1e-3
vov1 = sqrt(2 * I / 2e-3)
close(gm_num(2e-3, vov1), sqrt(2 * 2e-3 * I), 1e-6, "gm numeric")
ans("gm-sqrt", sqrt(2 * 2e-3 * I) * 1e3, 1e-6)
ans("gm-vov", 2 * 0.5e-3 / 0.2 * 1e3, 1e-6)
ans("ro-value", 1 / (0.1 * 0.5e-3) / 1e3, 1e-6)
Iex = sat(4e-3, 0.3)
close(Iex * 1e3, 0.18, 1e-9, "example I")
close(4e-3 * 0.3 * 1e3, 1.2, 1e-9, "example gm")
close(1 / (0.05 * Iex) / 1e3, 111, 0.002, "example ro")
close(4e-3 * 0.3 / (0.05 * Iex), 133, 0.003, "example gmro")
I2 = sat(2e-3, 0.25)
ans("intrinsic-gain", 2e-3 * 0.25 / (0.04 * I2), 1e-6)
close(2 / (0.04 * 0.25), 200, 1e-9, "2/(λVov)")
Cgs = 2 / 3 * 1 * 0.1 * 10e-15
close(Cgs * 1e15, 0.667, 0.001, "Cgs")
ans("ft-value", 1e-3 / (2 * pi * Cgs) / 1e9, 0.5)

# ==== 反相器 ====
ans("nm-low", 0.7 - 0.1, 1e-9)
ans("nm-high", 1.8 - 1.1, 1e-9)
close(2.5 - 1.6, 0.9, 1e-9, "NMH 0.9")
VDD, R, kk, Vt = 2.5, 10e3, 1e-3, 0.5
VOL = bisect(lambda V: (VDD - V) / R - tri(kk, VDD - Vt, V), 0, VDD - Vt)
close(VOL, 0.123, 0.003, "VOL bisection")
close((21 - sqrt(441 - 50)) / 10, VOL, 1e-9, "VOL quadratic")
close((21 + sqrt(441 - 50)) / 10, 4.08, 0.001, "other root")
ans("static-current", VDD * (VDD - 0.123) / R * 1e3, 0.001)
close((VDD - 0.123) / R * 1e3, 0.238, 0.001, "I 0.238")
ans("tplh-rc", log(2) * 10e3 * 10e-15 * 1e12, 0.3)
close(0.69 * 10e3 * 10e-15 * 1e12, 69, 1e-9, "0.69RC")
ans("tphl-sat", 10e-15 * 1.25 / 2e-3 * 1e12, 1e-6)

# ==== CMOS ====
kn = 1.0
kp = 0.5
VM = bisect(lambda v: sat(kn, v - 0.5) - sat(kp, 1.8 - v - 0.5), 0.5, 1.3)
r = sqrt(kp / kn)
close(VM, (0.5 + r * 1.3) / (1 + r), 1e-9, "VM formula vs bisection")
ans("vm-value", VM, 0.001)
close(10e-15 * 1.8 / (2 * 0.5e-3) * 1e12, 18, 1e-9, "tp 18 ps")
close(10e-15 * 1.8**2 * 1e9 * 1e6, 32.4, 1e-9, "P 32.4 uW")
ans("power-scaling", 20 * (0.9 / 1.2) ** 2, 1e-6)
ans("delay-current", 4e-15 * 1.0 / (2 * 0.2e-3) * 1e12, 1e-6)

# ==== CMOS 门 ====
ans("nand3-count", 2 * 3)
ans("nor2-width", 2 * 2, 1e-9)
ans("nand3-width", 3 * 1, 1e-9)
close(2 + 2, 4, 1e-9, "NAND2 input width")
close(1 + 4, 5, 1e-9, "NOR2 input width")

# ==== 二极管 ====
close(exp(0.060 / VT), 10.1, 0.01, "60 mV → ×10")
ans("decade-voltage", VT * log(10) * 1e3, 0.05)
idiode = lambda v: 1e-14 * (exp(v / VT) - 1)
vd = bisect(lambda v: idiode(v) - 1e-3, 0.3, 0.9)
ans("vd-at-current", vd, 0.0005)
close(log(1e11), 25.33, 0.0002, "ln 1e11")
v_hi = bisect(lambda v: idiode(v) - (0.5e-3 + 0.5e-6), 0.3, 0.9)
v_lo = bisect(lambda v: idiode(v) - (0.5e-3 - 0.5e-6), 0.3, 0.9)
rd_num = (v_hi - v_lo) / 1e-6  # dV/dI at 0.5 mA
close(rd_num, VT / 0.5e-3, 1e-3, "rd numeric")
ans("rd-value", VT / 0.5e-3, 0.05)
close(VT / 1e-3, 25.9, 1e-9, "rd 1 mA")
ans("cd-value", 1e-9 * 1e-3 / VT * 1e12, 0.05)
assert (0.7 - 0.0) > 0 and VT * log(100) < 0.13  # 0.1 → 10 mA spans ≈ 0.12 V
checks += 1

# ==== BJT ====
ans("vbe-1ma", VT * log(1e-3 / 1e-15), 0.0005)
close(log(1e12), 27.63, 0.0002, "ln 1e12")
ans("base-current", 1 + 1 / 100, 1e-9)
close(100 / 101, 0.990, 0.001, "alpha")
icv = lambda v: 1e-15 * exp(v / VT)
v1 = VT * log(1e-3 / 1e-15)
close((icv(v1 + 1e-6) - icv(v1 - 1e-6)) / 2e-6, 1e-3 / VT, 1e-6, "BJT gm numeric")
close(1e-3 / VT * 1e3, 38.6, 0.001, "gm 38.6")
close(100 / (1e-3 / VT) / 1e3, 2.59, 1e-9, "rpi 2.59")
close(2 * 1e-3 / 0.2 * 1e3, 10, 1e-9, "MOSFET gm 10 mS")
ans("bjt-gm", 0.5e-3 / VT * 1e3, 0.05)
ans("bjt-rpi", 150 / (0.5e-3 / VT) / 1e3, 0.01)

# ==== 放大器 ====
par = lambda a, b: a * b / (a + b)
ans("loaded-gain", -20 * 5 / (5 + 5), 1e-9)
close(par(5, 50), 4.55, 0.001, "RD||ro")
close(-2 * par(5, 50), -9.09, 0.001, "example gain")
ans("cs-gain", -1 * par(10, 100), 0.005)
ans("active-load-gain", -2 * par(50, 100), 0.05)

# ==== 电子和空穴 ====
ans("photon-cutoff", 1240 / 1.12, 0.5)
ans("intrinsic-fraction", 5e22 / ni / 1e12, 1e-9)
close(5e22 * 4, 2e23, 1e-9, "bond electrons")
assert exp(-9 / (2 * VT)) / exp(-1.12 / (2 * VT)) < 1e-60
checks += 1

# ==== 产生和复合 ====
ans("p0-from-n0", ni**2 / 1e15 / 1e5, 1e-9)
x = 1.12 / (2 * kB)
close(x, 6499, 0.0005, "Eg/2k")
close((350 / 300) ** 1.5, 1.26, 0.002, "T factor 350")
close(exp(x * (1 / 300 - 1 / 350)), 22.1, 0.003, "exp factor 350")
close((350 / 300) ** 1.5 * exp(x * (1 / 300 - 1 / 350)), 27.8, 0.002, "350 K ratio")
r250 = (250 / 300) ** 1.5 * exp(x * (1 / 300 - 1 / 250))
close((250 / 300) ** 1.5, 0.761, 0.001, "T factor 250")
close(exp(x * (1 / 300 - 1 / 250)), 0.0131, 0.01, "exp factor 250")
ans("ni-250k", r250, 0.0002)

# ==== 掺杂 ====
close(5e22 / 1e6, 5e16, 1e-9, "1 ppm")
ans("n-type-p0", ni**2 / 1e16 / 1e4, 1e-9)
ans("p-type-n0", ni**2 / 2e17, 0.5)
close(ni**2 / 7e16, 1.43e3, 0.002, "example compensation")
n_c = 5e16 - 2e16
ans("compensated-n", ni**2 / n_c, 1)
close(ni**2 / 5e16, 2000, 1e-9, "wrong 2000")
nb = 2e17 - 5e16
close(nb + (ni**2 / nb), 2e17 - 5e16 + ni**2 / nb, 1e-9, "neutrality")
close(ni**2 / nb, 667, 0.001, "compensation 667 (old boss item, kept as a check)")

# ==== 漂移 ====
ans("drift-v", 1350 * 1000 / 1e6, 1e-9)
ans("drift-j", q * 1e16 * 1350 * 1000, 1)
close(q * 1e16 * 1350 * 1000 * 1e-8 * 1e6, 21.6, 0.002, "22 uA")
sig = q * 1e17 * 800
close(sig, 12.8, 0.002, "σ 12.8")
close(1 / sig, 0.078, 0.002, "ρ 0.078")
close(1 / sig / 0.5e-4, 1561, 0.001, "Rsq")
close(10 / sig / 0.5e-4 / 1e3, 15.6, 0.002, "R 15.6k")
ans("resistor-squares", 10000 / 200 * 2, 1e-9)
close((1e17 * 800) / (1e15 * 1350), 59, 0.01, "≈60× conductivity")

# ==== 扩散 ====
ans("dn-einstein", 1350 * VT, 0.05)
close(480 * VT, 12.4, 0.003, "Dp")
close(q * 1350 * VT * 1e20, 560, 0.002, "example 560")
ans("diff-current", q * 12.4 * (1e14 / 2e-4), 0.01)

# ==== 电势和内建电势 ====
ans("phi-n", VT * log(1e17 / ni), 0.0005)
close(VT * log(10) * 1e3, 59.6, 0.001, "60 mV")
ans("rule-p", -60 * log10(1e15 / ni), 1e-9)
close(-VT * log(1e15 / ni) * 1e3, -298, 0.002, "exact -298")
close(60 * 7 - (-60 * 6), 780, 1e-9, "rule 780")
close(VT * log(1e33 / 1e20), 0.775, 0.001, "exact 0.775")
ans("phib-value", VT * log(1e32 / 1e20), 0.0005)
ans("b-built-in", VT * log(1e34 / 1e20), 0.0005)
close(VT * log(1e34 / 1e20), 0.835, 0.001, "b 0.835")

# ==== 耗尽区 ====


def width(Na, Nd, V):
    return sqrt(2 * eSi * V / q * (1 / Na + 1 / Nd))


def poisson_drop(Na, Nd, W, n=20000):
    xn = W * Na / (Na + Nd)
    xp = W - xn
    dx = W / n
    E = V = Emax = 0.0
    for i in range(n):
        xx = -xp + (i + 0.5) * dx
        rho = -q * Na if xx < 0 else q * Nd
        E2 = E + rho / eSi * dx
        V += -(E + E2) / 2 * dx
        E = E2
        Emax = max(Emax, abs(E))
    close(E / Emax, 0, 2e-3, "field back to zero")
    return V


ans("charge-balance", 0.02 * 1e17 / 1e16, 1e-9)
W0 = width(1e17, 1e15, 0.716)
close(poisson_drop(1e17, 1e15, W0), 0.716, 1e-3, "Poisson")
close(W0 * 1e4, 0.967, 0.001, "W 0.967")
close(W0 * 1e17 / 1.01e17 * 1e4, 0.957, 0.001, "xn")
close((W0 - W0 * 1e17 / 1.01e17) * 1e4, 0.0096, 0.01, "xp")
ans("w-reverse", width(1e17, 1e15, 3.716) * 1e4, 0.002)
close(VT * log(1e33 / 1e20), 0.775, 0.001, "b φB 0.775")
Wb = width(1e18, 1e15, 0.775 + 5)
close(poisson_drop(1e18, 1e15, Wb, n=1001 * 400), 5.775, 1e-3, "b Poisson")  # n = 1001k puts x = 0 on a cell edge (x_p = W/1001)
ans("b-depletion-width", Wb * 1e4, 0.005)
close(sqrt(3.716 / 0.716), 2.28, 0.001, "ratio 2.28")
close(sqrt(0.2 / 0.7), 0.53, 0.01, "forward ratio")
ans("injected", 1e20 / 1e17 * exp(0.6 / VT) / 1e13, 0.005)

# ==== MOS ====
ans("cox-2nm", eox / 2e-7 * 1e-8 * 1e15, 0.03)
close(eox / 10e-7, 3.45e-7, 0.001, "Cox 10 nm")
ans("phip-1e17", -60 * log10(1e17 / ni), 1e-9)
close(-VT * log(1e17 / ni) * 1e3, -417, 0.002, "exact -417")
close(-(0.55 - (-0.36)), -0.91, 1e-9, "VFB n+ 1e16")
close(-(-0.55 - (-0.36)), 0.19, 1e-9, "VFB p+ 1e16")
ans("vfb-1e17", -(0.55 - (-0.42)), 1e-9)
Cox10 = 3.45e-7
Qd = sqrt(2 * 1.036e-12 * q * 1e17 * 0.84)
close(Qd, 1.67e-7, 0.002, "Qd")
close(Qd / Cox10, 0.484, 0.002, "Qd/Cox")
close(-0.97 + 0.84 + Qd / Cox10, 0.354, 0.003, "Vth 10 nm")
ans("inversion-charge", Cox10 * 1.0 / q / 1e12, 0.005)
ans("xd-max", sqrt(2 * 1.036e-12 * 0.84 / (q * 1e17)) * 1e7, 0.3)
close(3.45e-13 / 3.45e-7 * 1e7, 10, 1e-9, "tox from C-V")
Cox5 = 3.45e-13 / 5e-7
close(Cox5, 6.9e-7, 1e-9, "Cox 5 nm")
close(1.67e-7 / Cox5, 0.242, 0.002, "b Qd/Cox")
ans("b-threshold", -0.97 + 0.84 + 1.67e-7 / Cox5, 0.001)

# ==== MOSFET 的电流（由电荷积分）====
mu, W, L, Vth, Vgs, Vds = 400, 2e-4, 0.5e-4, 0.35, 1.0, 0.4
Qn = lambda V: Cox10 * (Vgs - V - Vth)
I_int = W * mu * simpson(Qn, 0, Vds) / L  # ∫ W μ Qn dV / L
close(I_int, tri(mu * Cox10 * W / L, Vgs - Vth, Vds), 1e-9, "charge integral = triode formula")
ans("k-from-process", 400 * 3.45e-7 * 10 * 1e3, 0.005)
kex = 138 * 2 / 0.5
close(kex, 552, 1e-9, "k 552")
close(0.5 * kex * 0.65**2, 117, 0.004, "117 uA")
ans("gamma-value", sqrt(2 * 1.036e-12 * q * 1e17) / 3.45e-7, 0.001)
ans("sat-from-process", 0.5 * 138 * 8 * 0.5**2, 0.1)

# ==== 工艺 ====
ans("litho-resolution", 0.3 * 193 / 1.35, 0.05)
ans("oxide-consume", 20 * 0.44, 1e-9)
area200 = pi * 10**2
close(area200, 314, 0.001, "200 mm area")
close(1e15 * area200 * q, 0.0503, 0.001, "charge")
close(1e15 * area200 * q / 1e-3, 50, 0.01, "50 s")
area300 = pi * 15**2
close(area300, 707, 0.001, "300 mm area")
ans("implant-time", 1e15 * area300 * q / 2e-3, 0.1)
ans("cox-ratio", 4 / 2, 1e-9)
ans("slack-value", 0.95 - 1.02, 1e-9)

# ==== 按比例缩小 ====
kap = sqrt(2)
# scale: L, W, tox, V -> /κ ; C ∝ WL/tox -> /κ ; I ∝ (W/L) Cox V² -> /κ
C = 1 / kap
Ic = (1) * kap * (1 / kap) ** 2  # (W/L)=1, Cox ×κ, V² /κ²
close(Ic, 1 / kap, 1e-12, "I scales 1/κ")
ans("scaling-area", (1 / kap) ** 2, 1e-9)
ans("scaling-delay", C * (1 / kap) / Ic, 0.0005)
close((1 / kap) * Ic * kap**2, 1, 1e-12, "power density constant")
close(10 ** (0.1 / 0.06), 46, 0.01, "46×")
ans("leakage-increase", 10 ** (0.16 / 0.08), 1e-9)
ans("power-density", (1 / kap) * kap**2, 0.001)
close(0.08 / 0.95 * 1e3, 84, 0.01, "DIBL 84 mV/V")
ans("b-scaling", 1 / 1.4**2, 0.001)

# ==== 结业挑战（其余）====
ans("b-triode", tri(3, 0.6, 0.3), 1e-6)
ans("b-gm", 1.5 * 0.6, 1e-9)
close(sat(1.5, 0.6), 0.27, 1e-9, "b I 0.27")
close(2 * 0.27 / 0.6, 0.9, 1e-9, "b gm two ways")
ans("b-dynamic-power", 15e-15 * 0.81 * 2e9 * 1e6, 0.01)
ans("b-cs-gain", -4 * par(25, 10), 0.01)
ans("b-rpi", 120 / (2e-3 / VT) / 1e3, 0.005)

# ---- compare with the pack ----
pack = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "data" / "content" / "H.2.5.yaml"
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

print(f"H.2.5 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
