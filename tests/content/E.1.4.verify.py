"""E.1.4 光电子与光纤通信 — every number in data/content/E.1.4.yaml, recomputed.

Run: python3 -I tests/content/E.1.4.verify.py [path/to/E.1.4.yaml]
Plain Python (stdlib only). Reads back every `number` item answer from the YAML
and compares it against an independently computed value, plus checks card/example
constants and physical laws (Snell/TIR, symmetric slab waveguide eigenvalue
equation by bisection, cylindrical fiber V-number and cutoff, Rayleigh lambda^-4
scaling, modal and chromatic dispersion, photon energy, Fabry-Perot mode spacing,
PIN responsivity/photocurrent, PIN transit time, APD gain, shot vs thermal noise,
half-wave/quarter-wave plate thickness, MZI cos^2 transfer function, acousto-optic
Bragg condition, EDFA gain/ASE/NF, link power budget, and DWDM channel spacing).
"""
import math
import re
import sys
from math import asin, cos, degrees, floor, log10, pi, sqrt, tan
from pathlib import Path

checks = 0
computed = {}
FAILS = []


def close(a, b, tol=1e-9, what=""):
    global checks
    if abs(a - b) > tol * max(1.0, abs(b)) and abs(a - b) > tol:
        FAILS.append(f"{what}: {a} != {b}")
    checks += 1


def ok(cond, what=""):
    global checks
    if not cond:
        FAILS.append(f"FAILED: {what}")
    checks += 1


def ans(item_id, value, tol=1e-9):
    computed[item_id] = (value, tol)


def bisect(f, lo, hi, n=200):
    flo = f(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        if (f(mid) > 0) == (flo > 0):
            lo, flo = mid, f(mid)
        else:
            hi = mid
    return (lo + hi) / 2


c = 3e8
h = 6.626e-34
q = 1.602e-19
kB = 1.380649e-23
J0_FIRST_ZERO = 2.4048255576957727

# ==== L01: fiber-intro ====
# Example: n1=1.50, n2=1.45
na_ex = sqrt(1.50**2 - 1.45**2)
close(degrees(asin(1.45 / 1.50)), 75.16, 0.01, "L01 example critical angle")
close(na_ex, 0.3841, 0.0005, "L01 example NA")
close(degrees(asin(na_ex)), 22.59, 0.02, "L01 example acceptance angle")
# Practice: n1=1.48, n2=1.44
na_p1 = sqrt(1.48**2 - 1.44**2)
ans("q-na-calc", round(na_p1, 3), 0.001)
ans("q-angle-calc", round(degrees(asin(na_p1)), 1), 0.1)

# ==== L02: slab-waveguide ====
# Independent check: symmetric TE slab dispersion tan(u) = sqrt(V^2 - u^2)/u (even)
# and -cot(u) = sqrt(V^2 - u^2)/u (odd), where V = (pi * d * NA) / lam.
# Number of guided TE modes equals floor(2 * V / pi) + 1 = floor(2 * d * NA / lam) + 1.
def slab_te_modes(d_um, n1, n2, lam_um):
    na = sqrt(n1**2 - n2**2)
    V = pi * d_um * na / lam_um
    modes = []
    m = 0
    while m * pi / 2 < V:
        lo = m * pi / 2 + 1e-9
        hi = min((m + 1) * pi / 2 - 1e-9, V - 1e-9)
        if m % 2 == 0:
            f = lambda u: u * tan(u) - sqrt(V**2 - u**2)
        else:
            f = lambda u: -u / tan(u) - sqrt(V**2 - u**2)
        u_sol = bisect(f, lo, hi)
        modes.append(u_sol)
        m += 1
    return modes


modes_ex = slab_te_modes(2.0, 1.50, 1.46, 1.0)
ok(len(modes_ex) == 2, f"L02 example slab modes == 2 (got {len(modes_ex)})")
na_s_ex = sqrt(1.50**2 - 1.46**2)
close(na_s_ex, 0.3441, 0.0005, "L02 example NA")
close(2 * 2.0 * na_s_ex / 1.0, 1.376, 0.002, "L02 example 2dNA/lam")

modes_q = slab_te_modes(3.0, 1.50, 1.48, 1.5)
ok(len(modes_q) == 1, f"L02 practice slab modes == 1 (got {len(modes_q)})")
ans("q-slab-modes", len(modes_q), 0)
ans("q-slab-cutoff", 1.55 / (2 * 0.25), 0.01)

# ==== L03: fiber-modes ====
V_ex = 2 * pi * 4.5 * 0.12 / 1.55
lam_c_ex = 2 * pi * 4.5 * 0.12 / 2.405
close(V_ex, 2.189, 0.002, "L03 example V")
close(lam_c_ex, 1.411, 0.003, "L03 example lam_c")
ok(V_ex < J0_FIRST_ZERO, "L03 example single-mode")

V_q = 2 * pi * 5.0 * 0.11 / 1.55
lam_c_q = 2 * pi * 5.0 * 0.11 / 2.405
ans("q-v-calc", round(V_q, 2), 0.01)
ans("q-cutoff-calc", round(lam_c_q, 2), 0.01)
V_mm = 2 * pi * 25.0 * 0.20 / 0.85
ans("q-multimode-num", round(V_mm**2 / 2), 2)

# ==== L04: fiber-loss ====
close(10 * log10(2.0), 3.01, 0.02, "L04 2 mW in dBm")
close(10 ** (-4.0 / 10), 0.398, 0.002, "L04 -4 dBm in mW")
ans("q-loss-db", 2.0 - 0.25 * 40.0, 0.05)
ans("q-rayleigh-ratio", round((1550 / 850) ** 4, 1), 0.1)

# ==== L05: fiber-dispersion ====
close(16 * 0.2 * 50, 160.0, 1e-9, "L05 example chromatic broadening")
close(1 / 10e9 * 1e12, 100.0, 1e-9, "L05 10 Gb/s bit period")
dt_modal = 1.48 * (1.48 - 1.46) / (c * 1.46) * 1e3 * 1e9
ans("q-modal-disp", round(dt_modal, 1), 0.1)
ans("q-chrom-disp", 18 * 0.05 * 100, 0.1)

# ==== L06: light-matter ====
close(h * c / (1310e-9 * q), 0.9472, 0.001, "L06 1310 nm photon energy")
close(h * c / (1e-6 * q), 1.2408, 0.002, "L06 hc/q constant eV*um")
ans("q-photon-650", round(h * c / (650e-9 * q), 2), 0.01)

# ==== L07: led-and-ld ====
close(c / (2 * 3.5 * 300e-6) / 1e9, 142.86, 0.1, "L07 example FP df")
close((1550e-9) ** 2 / (2 * 3.5 * 300e-6) * 1e9, 1.144, 0.01, "L07 example FP dlam")
close(0.25 * (40 - 20), 5.0, 1e-9, "L07 example P-I output")
ans("q-fp-spacing", c / (2 * 4.0 * 250e-6) / 1e9, 0.5)
ans("q-pi-curve", 0.30 * (45 - 15), 0.05)

# ==== L08: laser-structures ====
ans("q-dfb-bragg", round(1550 / (2 * 3.20), 1), 0.2)

# ==== L09: photodetector-basics ====
R_ex = 0.75 * q * 1310e-9 / (h * c)
close(R_ex, 0.7918, 0.002, "L09 example responsivity")
close(R_ex * 100.0, 79.18, 0.2, "L09 example photocurrent uA")
ans("q-resp-850", round(0.70 * q * 850e-9 / (h * c), 2), 0.01)
ans("q-photocurrent", 0.85 * 50.0, 0.2)

# ==== L10: pin-and-apd ====
close(2.0e-6 / 1.0e5 * 1e12, 20.0, 1e-9, "L10 example transit time")
close(10 * 0.90 * 5.0, 45.0, 1e-9, "L10 example APD current")
ans("q-pin-transit", 1.5e-6 / 1.0e5 * 1e12, 0.1)
ans("q-apd-current", 15 * 0.80 * 4.0, 0.1)

# ==== L11: optical-receiver ====
i_shot_ex = sqrt(2 * q * 10e-6 * 1e9) * 1e6
i_th_ex = sqrt(4 * kB * 300 * 1e9 / 1000) * 1e6
close(i_shot_ex, 0.0566, 0.001, "L11 example shot noise uA")
close(i_th_ex, 0.1287, 0.001, "L11 example thermal noise uA")
ok(i_th_ex**2 / i_shot_ex**2 > 5.0, "L11 thermal variance > 5x shot variance")
ans("q-tia-vout", 12e-6 * 5000 * 1e3, 0.1)

# ==== L12: crystal-optics ====
close(0.630 / (2 * 0.009), 35.0, 1e-9, "L12 example HWP thickness")
close(0.630 / (4 * 0.009), 17.5, 1e-9, "L12 example QWP thickness")
ans("q-hwp-thick", 1.55 / (2 * 0.010), 0.1)

# ==== L13: electro-optic ====
close(cos(pi / 4) ** 2, 0.5, 1e-9, "L13 example MZI quadrature")
close(10 * log10(1.0 / 0.01), 20.0, 1e-9, "L13 example ER")
ans("q-mzi-trans", 4.0 * cos((pi * 2.0 / 6.0) / 2) ** 2, 0.02)

# ==== L14: acousto-optic-switches ====
Lam_ex = 4000 / 100e6
lam_m_ex = 632e-9 / 2.2
th_B_ex = asin(lam_m_ex / (2 * Lam_ex))
close(Lam_ex * 1e6, 40.0, 1e-9, "L14 example acoustic wavelength")
close(lam_m_ex * 1e9, 287.27, 0.1, "L14 example medium wavelength")
close(th_B_ex * 1e3, 3.59, 0.02, "L14 example Bragg angle mrad")
close(degrees(th_B_ex), 0.206, 0.005, "L14 example Bragg angle deg")
ans("q-ao-lambda", 3600 / 90e6 * 1e6, 0.1)

# ==== L15: edfa ====
close(-20 + 25, 5.0, 1e-9, "L15 example output dBm")
close(10 ** (5.0 / 10), 3.162, 0.01, "L15 example output mW")
ans("q-edfa-out", -18 + 22, 0.05)

# ==== L16: soa-ase-noise ====
nu_1550 = c / 1550e-9
P_ase_ex = 2 * 1.5 * (100 - 1) * h * nu_1550 * 12.5e9
close(P_ase_ex * 1e6, 0.476, 0.005, "L16 example ASE power uW")
close(10 * log10(P_ase_ex / 1e-3), -33.22, 0.05, "L16 example ASE dBm")
close(10 * log10(2.0), 3.01, 0.02, "L16 3 dB quantum limit")
ans("q-nf-calc", round(10 * log10(2 * 1.6), 1), 0.06)

# ==== L17: optical-link-budget ====
close(2 - 0.22 * 60 - 2.8 - (-24), 10.0, 1e-9, "L17 example margin")
close((0 - (-26) - 2.0 - 4.0) / 0.25, 80.0, 1e-9, "L17 example max distance")
ans("q-margin-calc", 3 - 50 * 0.20 - 3.0 - (-25), 0.05)
ans("q-max-dist", (0 - (-28) - 2.5 - 4.5) / 0.35, 0.1)

# ==== L18: wdm-systems ====
dlam_50 = (1550e-9) ** 2 * 50e9 / c * 1e9
close(dlam_50, 0.4004, 0.002, "L18 50 GHz dlam")
close(floor(35 / dlam_50), 87, 1e-9, "L18 50 GHz channels")
ans("q-dwdm-spacing", round((1550e-9) ** 2 * 200e9 / c * 1e9, 2), 0.01)
ans("q-dwdm-capacity", 40 * 100 / 1000, 1e-9)

# ==== BOSS (matching comprehensive exercise C4) ====
na_b1 = sqrt(1.48**2 - 1.46**2)
ans("b-na-angle", round(na_b1, 3), 0.001)
close(degrees(asin(na_b1)), 14.03, 0.05, "boss acceptance angle 14.0 deg")
ans("b-v-number", round(2 * pi * 4.1 * 0.14 / 1.55, 2), 0.01)
ans("b-cutoff", round(2 * pi * 4.1 * 0.14 / 2.405, 2), 0.01)
ans("b-loss-disp", 17 * 0.1 * 80, 0.1)
ans("b-photon-e", round(h * c / (850e-9 * q), 2), 0.01)
R_boss = 0.80 * q * 1550e-9 / (h * c)
ans("b-pin-resp", round(R_boss, 2), 0.01)
ans("b-pin-curr", 1.00 * (10 ** (-20 / 10) * 1e3), 0.1)
ans("b-link-margin", 0 - 16 - 2 - (-28), 0.05)
dlam_100 = (1550e-9) ** 2 * 100e9 / c * 1e9
ans("b-dwdm-dlam", round(dlam_100, 2), 0.01)
ans("b-dwdm-ch", floor(35 / 0.80), 0)

# ==== Read back all `number` answers from YAML and verify every single one ====
pack_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/content/E.1.4.yaml")
text = pack_path.read_text(encoding="utf-8")
yaml_nums = {}
cur_id = None
cur_type = None
for line in text.splitlines():
    m_id = re.match(r"^\s*(?:-\s*)?id:\s*([a-z0-9-]+)\s*$", line)
    if m_id:
        cur_id = m_id.group(1)
        cur_type = None
        continue
    m_t = re.match(r"^\s*type:\s*([a-z]+)\s*$", line)
    if m_t:
        cur_type = m_t.group(1)
        continue
    m_a = re.match(r"^\s*answer:\s*([-+0-9.eE]+)\s*$", line)
    if m_a and cur_id and cur_type == "number":
        yaml_nums[cur_id] = float(m_a.group(1))

for item_id, val in yaml_nums.items():
    if item_id not in computed:
        FAILS.append(f"YAML number item '{item_id}' = {val} is NOT verified in verify.py")
    else:
        exp_val, tol = computed[item_id]
        close(val, exp_val, tol, f"YAML item {item_id}")

for item_id in computed:
    if item_id not in yaml_nums:
        FAILS.append(f"verify.py checks '{item_id}' which is missing from YAML number items")

if FAILS:
    print("FAILURES:")
    for f in FAILS:
        print(" -", f)
    sys.exit(1)

print(f"E.1.4 verify.py OK: {checks} checks ({len(yaml_nums)} YAML number answers verified)")
