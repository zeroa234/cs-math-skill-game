"""H.2.6 模拟集成电路设计 — every number in data/content/H.2.6.yaml, recomputed.

Run: python -I tests/content/H.2.6.verify.py [path/to/H.2.6.yaml]
Plain Python. Number answers are read back from the YAML and compared with the values computed here, so a typo in
either place fails. Where a lesson uses a closed-form result, the result is also derived another way here instead of
being trusted: transconductance and output resistance by numerical derivatives of the square law, cascode and
five-transistor OTA small-signal behaviour by solving the nodal equations, the differential pair's full current
steering by solving the large-signal equations, poles and gain-bandwidth by searching |H(f)|, phase margins from the
actual loop phase at the actual unity-gain frequency, kT/C by integrating 4kTR over the RC noise bandwidth,
switched-capacitor resistance by the charge moved per cycle, SAR by running the binary search, and the ideal ADC's
SNR by quantizing a sine wave.
"""
import math
import re
import sys
from math import atan, degrees, exp, log, log10, pi, sqrt
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


def solve(A, b):
    """Gaussian elimination with partial pivoting (real or complex)."""
    n = len(A)
    M = [list(map(complex, row)) + [complex(bi)] for row, bi in zip(A, b)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def bisect(f, lo, hi, n=200):
    flo = f(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        if (f(mid) > 0) == (flo > 0):
            lo, flo = mid, f(mid)
        else:
            hi = mid
    return (lo + hi) / 2


def sq(kp, wl, vov, lam=0.0, vds=0.0):
    """Square-law saturation current (A); kp in A/V^2."""
    return 0.5 * kp * wl * vov**2 * (1 + lam * vds)


def par(a, b):
    return a * b / (a + b)


kT = 4.14e-21
k_B, q = 1.380649e-23, 1.602176634e-19
close(k_B * 300, kT, 0.001, "kT at 300 K is 4.14e-21 J")

# ==== analog-intro ====
I = sq(300e-6, 8, 0.25)
ans("square-law-id", I * 1e6, 1e-9)
h = 1e-7
gm_num = (sq(300e-6, 8, 0.25 + h) - sq(300e-6, 8, 0.25 - h)) / (2 * h)
ans("gm-from-id", 2 * 75e-6 / 0.25 * 1e3)
close(gm_num, 2 * I / 0.25, 1e-6, "gm = 2ID/Vov by derivative")
ans("gm-efficiency", 2 / 0.2)
close(2 / 0.1, 20, 0, "Vov 0.1 V gives 20 /V")

# ==== mos-large-signal ====
ans("min-vds", 0.9 - 0.45)
lam1 = 0.1 * 0.5 / 1
ans("ro-long-l", 1 / (lam1 * 50e-6) / 1e3)
close(1 / (0.1 * 50e-6) / 1e3, 200, 1e-12, "0.5 um gives 200 kOhm")
# ro by derivative of ID(VDS) with channel-length modulation (ID0 = 50 uA)
dI = (50e-6 * (1 + lam1 * (1 + h)) - 50e-6 * (1 + lam1 * (1 - h))) / (2 * h)
close(1 / dI / 1e3, 400, 1e-6, "ro = 1/(lambda ID) by derivative")


def vt_shift(gamma, phi2, vsb):
    return gamma * (sqrt(phi2 + vsb) - sqrt(phi2))


shift = vt_shift(0.4, 0.7, 0.5)
ans("body-shift", round(shift, 3), 0.0005)
close(sqrt(1.2), 1.095, 0.0005, "sqrt 1.2")
close(sqrt(0.7), 0.837, 0.0005, "sqrt 0.7")
close(sqrt(1.2) - sqrt(0.7), 0.259, 0.0005, "difference 0.259")
ans("cgs-value", 2 / 3 * 10 * 0.18 * 8.5)
close(10 * 0.18, 1.8, 1e-12, "WL 1.8 um^2")

# ==== mos-small-signal ====
I = sq(400e-6, 5, 0.3)
close(I * 1e6, 90, 1e-9, "example ID 90 uA")
gm = 2 * I / 0.3
close(gm * 1e6, 600, 1e-9, "example gm 600 uS")
ro = 1 / (0.08 * I)
close(ro / 1e3, 139, 0.003, "example ro 139 kOhm")
close(gm * ro, 83, 0.005, "example gm*ro 83")
close(400e-6 * 5 * 0.3, gm, 1e-12, "gm = k'(W/L)Vov")
close(sqrt(2 * 400e-6 * 5 * I), gm, 1e-12, "gm = sqrt(2k'(W/L)ID)")
ans("gm-sqrt", round(sqrt(2 * 200e-6 * 20 * 100e-6) * 1e3, 3), 0.0005)
# intrinsic gain from gm and ro at an arbitrary current: the current cancels
for Id in (10e-6, 100e-6):
    close((2 * Id / 0.25) * (1 / (0.05 * Id)), 160, 1e-9, "intrinsic gain independent of ID")
ans("intrinsic-gain", 2 / (0.05 * 0.25))
eta_num = (vt_shift(0.4, 0.7, 0.5 + h) - vt_shift(0.4, 0.7, 0.5 - h)) / (2 * h)
ans("gmb-ratio", round(0.4 / (2 * sqrt(1.2)), 2), 0.005)
close(eta_num, 0.4 / (2 * sqrt(1.2)), 1e-6, "eta = dVt/dVSB")

# ==== short-channel-gmid ====
ans("vsat-gm", 10e-6 * 8.5e-3 * 1e5 * 1e3)
close(8.5e-15 / 1e-12, 8.5e-3, 1e-12, "Cox 8.5 fF/um^2 = 8.5e-3 F/m^2")
sw = 1.5 * 25 * log(10)
ans("sub-swing", round(sw, 1), 0.05)
close(2 * sw / 1000, 0.17, 0.02, "two decades need about 0.17 V")
s300 = k_B * 300 / q * log(10) * 1000
ok(59 < s300 < 60, f"subthreshold swing limit at 300 K is about 60 mV ({s300:.1f})")
close(1.2e-3 / 12 * 1e6, 100, 1e-9, "gm/ID example current 100 uA")
close(100 / 5, 20, 0, "gm/ID example width 20 um")
ans("gmid-current", round(1e-3 / 15 * 1e6, 1), 0.05)
close(1e-3 / 10 * 1e6, 100, 1e-9, "gm/ID 10 needs 100 uA")
ok(1 / (1.5 * 0.025) > 2 / 0.2 and 1 / (1.2 * 0.025) < 40, "weak inversion gm/ID about 20-30 /V")

# ==== cs-stage ====
ans("cs-resistive", round(-1e-3 * par(10e3, 100e3), 2), 0.005)
ans("cs-diode", -sqrt(36 / 4))
close(sqrt(100), 10, 0, "gain 10 needs ratio 100")
gm1 = 2 * 100e-6 / 0.2
ro1, ro2 = 1 / (0.1 * 100e-6), 1 / (0.15 * 100e-6)
close(gm1, 1e-3, 1e-12, "example gm 1 mS")
close(ro2 / 1e3, 66.7, 0.001, "example ro2 66.7 k")
close(par(ro1, ro2) / 1e3, 40, 1e-9, "example parallel 40 k")
close(-gm1 * par(ro1, ro2), -40, 1e-9, "example gain -40")
ans("cs-current-load", -0.5e-3 * par(200e3, 300e3))
# degeneration: solve the small-signal loop vgs = vin - gm*vgs*Rs
vgs = 1 / (1 + 2e-3 * 1e3)
ans("cs-degen", -2e-3 * vgs * 6e3)
close(-2e-3 * 6e3, -12, 1e-12, "without Rs: -12")

# ==== sf-cg ====
ans("sf-gain-ideal", round(1 / 1.2, 3), 0.0005)
ans("sf-rout", round(1 / 1.2e-3), 0.5)
ans("cg-gain", 2.3e-3 * 5e3)
ans("cg-rin", round(1 / 2.3e-3), 0.5)
close(1 / 50, 20e-3, 1e-12, "50 Ohm match needs 20 mS")

# ==== cascode ====


def cascode_rout(ro1, ro2, gm2, gmb2=0.0):
    # test voltage v at the output; unknowns vX and i. M2 current (drain->source) = gm2*(0-vX) + gmb2*(0-vX) + (v-vX)/ro2
    v = 1.0
    # KCL at X: i = vX/ro1 and i = -(gm2+gmb2)vX + (v - vX)/ro2
    vX = (v / ro2) / (1 / ro1 + gm2 + gmb2 + 1 / ro2)
    return v / (vX / ro1)


R = cascode_rout(100e3, 100e3, 1e-3)
ans("cascode-rout", R / 1e6)
close(R, 100e3 + 100e3 + 1e-3 * 100e3 * 100e3, 1e-9, "nodal solve matches the formula")
close(R / 100e3, 102, 1e-9, "a hundred-odd times one transistor")
ans("cascode-gain", 0.5 * 50**2)
gmro, ro = 50, 100e3
gm = gmro / ro
close(gm * par(gm * ro * ro, gm * ro * ro), 1250, 1e-9, "gm x (gm ro^2 || gm ro^2)")
g_e, r_e = 1e-3, 100e3
close(g_e * r_e * r_e / 1e6, 10, 1e-12, "cascode example Rout 10 MOhm")
close(par(g_e * r_e**2, g_e * r_e**2) / 1e6, 5, 1e-12, "cascode example 5 MOhm")
close(g_e * par(g_e * r_e**2, g_e * r_e**2), 5000, 1e-9, "cascode example gain 5000")
close(0.5 * (g_e * r_e) ** 2, 5000, 1e-9, "half of (gm ro)^2")
ans("cascode-headroom", 2 * 0.2)

# ==== diff-pair ====


def steer(dv, Iss=1.0, k=1.0, vt=0.0):
    """Square-law pair: find the common source voltage so I1 + I2 = Iss; return (I1, I2)."""
    def tot(vs):
        i1 = 0.5 * k * max(dv / 2 - vs - vt, 0) ** 2
        i2 = 0.5 * k * max(-dv / 2 - vs - vt, 0) ** 2
        return i1 + i2 - Iss
    vs = bisect(tot, -10, 10)
    return 0.5 * k * max(dv / 2 - vs - vt, 0) ** 2, 0.5 * k * max(-dv / 2 - vs - vt, 0) ** 2


vov = 0.2
k = 1.0 / vov**2              # balanced: Iss/2 = (1/2) k vov^2 with Iss = 1
dv_full = bisect(lambda d: steer(d, 1.0, k)[1] - 1e-12, 0.0, 1.0)
ans("dp-steer", round(sqrt(2) * 0.2, 3), 0.0005)
close(dv_full, sqrt(2) * vov, 1e-5, "full steering at sqrt(2) Vov by solving the pair")
ans("dp-ad", 1e-3 * 8e3)
acm = -8e3 / (2 * 200e3)
ans("dp-acm", acm, 0.0005)
close(-8e3 / (1 / 1e-3 + 2 * 200e3), acm, 0.003, "1/gm term changes it by under 0.3 %")
close(4 / 0.02, 200, 1e-9, "single-ended differential gain 4 vs 0.02")
close(20 * log10(200), 46, 0.001, "46 dB")

# ==== five-transistor-ota ====


def ota_gain(gm1, gm3, ro1, ro2, ro3, ro4, rtail=1e15):
    """Nodal solve: unknowns vA (mirror node), vo, vP (tail). Gates +0.5, -0.5. Currents downward."""
    g1, g2 = 0.5, -0.5
    # I1 = gm1(g1-vP) + (vA-vP)/ro1 ; I2 = gm1(g2-vP) + (vo-vP)/ro2
    # I3 = -(gm3 + 1/ro3) vA ; I4 = -gm3 vA - vo/ro4 ; tail: I1 + I2 = vP/rtail
    A = [
        [-(gm3 + 1 / ro3) - 1 / ro1, 0, gm1 + 1 / ro1],          # I3 - I1 = 0
        [-gm3, -1 / ro4 - 1 / ro2, gm1 + 1 / ro2],              # I4 - I2 = 0
        [1 / ro1, 1 / ro2, -2 * gm1 - 1 / ro1 - 1 / ro2 - 1 / rtail],  # I1 + I2 - vP/rtail = 0
    ]
    b = [gm1 * g1, gm1 * g2, -gm1 * (g1 + g2)]
    vA, vo, vP = solve(A, b)
    return (vo / (g1 - g2)).real


ans("ota-gain", 0.6e-3 * par(150e3, 100e3))
close(par(150e3, 100e3), 60e3, 1e-9, "60 k")
g_ex = ota_gain(0.6e-3, 0.6e-3, 150e3, 150e3, 100e3, 100e3)
close(g_ex, 36, 0.02, "nodal solve of the 5T OTA close to gm1(ro2||ro4)")
Id = 20e-6
v = sqrt(2 * Id / 4e-3)
close(v, 0.1, 1e-12, "example Vov 0.1 V")
close(2 * Id / v, 0.4e-3, 1e-12, "example gm 0.4 mS")
close(1 / (0.1 * Id), 500e3, 1e-9, "example ro 500 k")
close(0.4e-3 * par(500e3, 500e3), 100, 1e-9, "example gain 100")
gm = 2 * 40e-6 / 0.25
r2, r4 = 1 / (0.1 * 40e-6), 1 / (0.2 * 40e-6)
ans("ota-half-current", round(gm * par(r2, r4), 1), 0.05)
close(gm * 1e6, 320, 1e-9, "320 uS")
close(par(r2, r4) / 1e3, 83.3, 0.001, "83.3 k")
close(gm * par(r2, r4), 2 / (0.25 * (0.1 + 0.2)), 1e-9, "gain 2/[Vov(ln+lp)]")

# ==== current-mirrors ====
ans("mirror-ratio", 50 * 15 / 5)
ex = (1 + 0.1 * 1.2) / (1 + 0.1 * 0.6)
close(ex, 1.057, 0.0005, "example ratio 1.057")
close(10 * ex, 10.57, 0.0005, "example 10.57 uA")
ans("mirror-error", round(((1 + 0.1 * 1.5) / (1 + 0.1 * 0.7) - 1) * 100, 1), 0.05)

# ==== cascode-mirrors ====
ans("cmirror-rout", 0.5e-3 * 200e3**2 / 1e6)
close(cascode_rout(200e3, 200e3, 0.5e-3) / 1e6, 20.4, 1e-9, "full expression 20.4 MOhm, approx 20")
close(0.5e-3 * 200e3, 100, 1e-9, "100 times the simple mirror")
ans("cmirror-vmin", (0.5 + 0.2) + 0.2)
close(2 * 0.2, 0.4, 0, "low-voltage cascode 0.4 V")
close(0.9 - 0.4, 0.5, 1e-12, "saves 0.5 V")

# ==== freq-miller ====
ans("miller-cap", 4 * (1 - (-50)))
close(5 * (1 + 40), 205, 0, "guess and the cascode note: 5 fF at -40 is 205 fF")
# Miller: charge drawn from the input for a 1 mV step when the output moves -40 mV
close(5e-15 * (1e-3 - (-40e-3)) / 1e-3 / 1e-15, 205, 1e-9, "charge view of the Miller capacitance")
cin = 40 + 4 * (1 + 25)
close(4 * 26, 104, 0, "example Miller part 104 fF")
close(cin, 144, 0, "example 144 fF")
close(1 / (2 * pi * 20e3 * 144e-15) / 1e6, 55.3, 0.001, "example input pole 55.3 MHz")


def pole_3db(A0, R, C):
    return bisect(lambda f: abs(A0 / (1 + 2j * pi * f * R * C)) - A0 / sqrt(2), 1, 1e13)


ans("input-pole", round(1 / (2 * pi * 1e4 * 255e-15) / 1e6, 1), 0.05)
close(pole_3db(1, 1e4, 255e-15) / 1e6, 62.4, 0.001, "input pole by |H| search")
fp = 1 / (2 * pi * 100e3 * 0.5e-12)
ans("dominant-pole", round(fp / 1e6, 2), 0.005)
close(pole_3db(40, 100e3, 0.5e-12), fp, 1e-6, "dominant pole by |H| search")
gbw = 0.4e-3 / (2 * pi * 0.5e-12)
ans("gbw-value", round(gbw / 1e6, 1), 0.05)
fu = bisect(lambda f: abs(40 / (1 + 1j * f / fp)) - 1, fp, 1e12)
close(fu, gbw, 0.001, "unity-gain frequency equals gm/(2 pi CL)")
close(40 * fp / 1e6, 127, 0.003, "40 x 3.18 MHz is 127 MHz")

# ==== freq-stages ====
ans("sf-pole", round(1.2e-3 / (2 * pi * 1e-12) / 1e6), 0.5)
close(1 / 1.2e-3, 833, 0.001, "833 Ohm")
ans("cg-pole", round(2e-3 / (2 * pi * 100e-15) / 1e9, 2), 0.005)
ans("cascode-miller", 5 * (1 + 1))
ans("octc-bw", round(1 / (2 * pi * 450e-12) / 1e6), 0.5)
close(300 / 450, 2 / 3, 1e-12, "300 ps is two thirds")

# ==== feedback ====
acl = 1000 / (1 + 100)
ans("fb-closed", round(acl, 3), 0.0005)
close((10 - acl) / 10, 0.0099, 0.01, "1 % from 1/beta")
acl2 = 800 / (1 + 80)
ans("fb-desens", round((acl - acl2) / acl * 100, 2), 0.005)
close((acl - acl2) / acl * 100, 20 / 81, 1e-9, "exactly 20 % / (1 + A_new beta)")
close(acl2, 9.877, 0.0001, "9.877")


def closed_bw(A0, fp, beta):
    A = lambda f: A0 / (1 + 1j * f / fp)
    H = lambda f: A(f) / (1 + A(f) * beta)
    H0 = abs(H(0))
    return bisect(lambda f: abs(H(f)) - H0 / sqrt(2), 1, 1e12)


bw = closed_bw(1000, 10e3, 0.1)
ans("fb-bandwidth", 10e3 * 101 / 1e6)
close(bw, 1.01e6, 1e-6, "closed-loop -3 dB by |H| search")
close(acl * bw / 1e6, 10, 0.001, "9.9 x 1.01 MHz about 10 MHz")
ans("fb-rin", 10e3 * 101 / 1e6)

# ==== stability ====
ok(180 - 150 == 30, "PM 30")


def pm_two_pole(A0, p1, p2):
    L = lambda f: A0 / ((1 + 1j * f / p1) * (1 + 1j * f / p2))
    fu = bisect(lambda f: abs(L(f)) - 1, p1, 1e14)
    ph = degrees(-atan(fu / p1) - atan(fu / p2))
    return 180 + ph, fu


ans("pm-two-pole", round(90 - degrees(atan(1 / 3)), 1), 0.05)
# check with a real loop: put p2 at 3x the actual unity-gain frequency
fu_target = 1e6
A0 = 1e6
p1 = bisect(lambda p: abs(A0 / ((1 + 1j * fu_target / p) * (1 + 1j / 3))) - 1, 1e-3, 1e6)
pm, fu_chk = pm_two_pole(A0, p1, 3 * fu_target)
close(fu_chk, fu_target, 1e-6, "loop built so that fu = 1 MHz")
close(pm, 71.6, 0.0005, "phase margin from the actual loop phase")
close(90 - degrees(atan(1)), 45, 1e-12, "p2 at fu: 45")
close(90 - degrees(atan(1 / 2)), 63, 0.01, "p2 at 2 fu: about 63")
close(90 - degrees(atan(1 / 3)), 72, 0.01, "p2 at 3 fu: about 72")
close(10e6 / 1000, 10e3, 1e-12, "example p1 10 kHz")
pm_ex, fu_ex = pm_two_pole(1000, 10e3, 10e6)
ok(pm_ex > 45 and fu_ex < 10e6, f"single-pole estimate: actual PM {pm_ex:.1f} slightly above 45, fu slightly below p2")
close(10e6 / sqrt(3) / 1e6, 5.8, 0.01, "60 deg: fu = p2/sqrt3 about 5.8 MHz")
close(10e6 / sqrt(3) / 1000 / 1e3, 5.8, 0.01, "p1 about 5.8 kHz")
close(90 - degrees(atan(1 / sqrt(3))), 60, 1e-9, "p2/sqrt3 gives 60")
ans("dominant-place", 20e6 / 2000 / 1e3)

# ==== noise-basics ====
ans("noise-sum", sqrt(3**2 + 4**2))
vn1k = sqrt(4 * kT * 1e3)
ans("thermal-1k", round(vn1k * 1e9, 2), 0.005)
close(vn1k * 1e9, 4, 0.02, "1 kOhm about 4 nV/rtHz")
ans("thermal-band", round(4.07e-9 * sqrt(1e6) * 1e6, 2), 0.005)
mos = sqrt(4 * kT * (2 / 3) / 1e-3)
ans("mos-noise", round(mos * 1e9, 2), 0.005)
close((2 / 3) / 1e-3, 670, 0.005, "equivalent to about 670 Ohm")

# ==== noise-circuits ====
r_eq = (2 / 3) / 2e-3 + 1 / ((2e-3) ** 2 * 5e3)
close(r_eq, 383.3, 0.001, "333 + 50 Ohm")
ans("cs-input-noise", round(sqrt(4 * kT * r_eq) * 1e9, 2), 0.005)
ans("dp-noise", round(sqrt(2 * 4 * kT * (2 / 3) / 1e-3) * 1e9, 2), 0.005)
close(sqrt(2) * 3.32, 4.70, 0.002, "sqrt2 times the single device")


def ktc_by_integration(R, C):
    # integrate 4kTR / (1 + (2 pi f R C)^2) df over 0..inf with f = f0 * tan(u), u in [0, pi/2)
    f0 = 1 / (2 * pi * R * C)
    n = 20000
    s = 0.0
    for i in range(n):
        u = (i + 0.5) * (pi / 2) / n
        f = f0 * math.tan(u)
        dfdu = f0 / math.cos(u) ** 2
        s += 4 * kT * R / (1 + (f / f0) ** 2) * dfdu
    return s * (pi / 2) / n


for R in (1e3, 2e3):
    close(ktc_by_integration(R, 1e-12), kT / 1e-12, 1e-6, f"kT/C independent of R ({R})")
close(kT / 0.5e-12, 8.28e-9, 1e-9, "example kT/C 8.28e-9 V^2")
close(sqrt(kT / 0.5e-12) * 1e6, 91, 0.002, "example 91 uV")
close(sqrt(kT / 2e-12) / sqrt(kT / 0.5e-12), 0.5, 1e-12, "4x capacitance halves the noise")
ans("ktc-4p", round(sqrt(kT / 4e-12) * 1e6, 1), 0.05)

# ==== opamp-specs ====
ok(1 / 1000 <= 0.001 and 1 / 10 > 0.001 and 1 / 1e6 < 0.001 / 100, "0.1 % needs A about 1000")
ans("telescopic-swing", 1.8 - 5 * 0.2)
close(1.2 - 5 * 0.2, 0.2, 1e-12, "1.2 V supply leaves 0.2 V")
ans("two-stage-gain", round(20 * log10(40 * 50), 1), 0.05)
close(round(20 * log10(40), 1) + round(20 * log10(50), 1), 66.0, 1e-9, "32.0 + 34.0 = 66.0")
ans("two-stage-swing", 1.8 - 2 * 0.2)

# ==== miller-compensation ====
ans("miller-gbw", round(0.5e-3 / (2 * pi * 1e-12) / 1e6, 1), 0.05)
close(0.5e-3 / (2 * pi * 2e-12) / 1e6, 39.8, 0.001, "example GBW 39.8 MHz")
close(2.2 * 0.5 * 3 / 2, 1.65, 1e-12, "example gm2 1.65 mS")
close(90 - degrees(atan(1 / 2.2)), 66, 0.01, "p2 = 2.2 GBW: about 66 deg")
close(degrees(atan(0.1)), 6, 0.05, "zero at 10 GBW takes about 6 deg")
close(90 - degrees(atan(1 / 2.2)) - degrees(atan(0.1)), 60, 0.005, "still about 60 deg")
ans("miller-pm", round(90 - degrees(atan(79.6 / 318))), 0.5)
close(79.6 / 318, 0.25, 0.002, "ratio 0.25")
ans("miller-gm2", round(2.2 * 0.3 * 4 / 1.5, 2), 0.005)
ans("rhp-zero", round(4e-3 / (2 * pi * 1e-12) / 1e6), 0.5)
close(1 / 4e-3, 250, 1e-12, "Rz = 250 Ohm")
ans("slew-rate", 30e-6 / 1.5e-12 / 1e6)
ok(1 / 0.1 == 10, "1 V in 0.1 us needs 10 V/us")

# ==== bandgap ====
kq = k_B / q * 1000           # mV/K
close(kq, 0.0862, 0.0005, "k/q = 0.0862 mV/K")
ans("delta-vbe", round(25 * log(4), 1), 0.05)
tc24 = 0.0862 * log(24)
ans("ptat-tc", round(tc24, 3), 0.0005)
close(1.9 / 0.274, 6.93, 0.001, "example K 6.93")
dv300 = 0.0862e-3 * 300 * log(24)
close(dv300 * 1000, 82.2, 0.001, "example dVBE 82.2 mV")
close(0.65 + 6.93 * 0.0822, 1.22, 0.003, "example VREF 1.22 V")
# zero temperature coefficient by construction: d/dT [VBE(T) + K dVBE(T)] = 0 with linear VBE
vbe = lambda T: 0.65 - 1.9e-3 * (T - 300)
K = 1.9e-3 / (0.0862e-3 * log(24))
vref = lambda T: vbe(T) + K * 0.0862e-3 * T * log(24)
close((vref(301) - vref(299)) / 2, 0, 1e-9, "zero TC at the chosen K")
ans("bandgap-k", round(1.5 / 0.274, 2), 0.01)
# silicon band gap: Varshni Eg(T) = 1.17 - 4.73e-4 T^2 / (T + 636); linear extrapolation from 300 K to 0 K about 1.2 eV
Eg = lambda T: 1.17 - 4.73e-4 * T**2 / (T + 636)
close(Eg(300), 1.12, 0.005, "Eg(300 K) about 1.12 eV")
slope = (Eg(301) - Eg(299)) / 2
close(Eg(300) - 300 * slope, 1.2, 0.005, "linear extrapolation to 0 K about 1.2 eV")

# ==== switched-cap ====
close(1 / (0.5e-12 * 10e6) / 1e3, 200, 1e-9, "example 200 k")
close(1 / (2e-12 * 10e6) / 1e3, 50, 1e-9, "example 50 k")


def sc_resistance(C, f, dV=1.0):
    q_per_cycle = C * dV
    return dV / (q_per_cycle * f)


ans("sc-req", sc_resistance(2e-12, 1e6) / 1e3)
ans("sc-gain", 4e-12 / 1e-12)

# ==== dac-adc ====


def sar(vin, n, fs=1.0):
    code, comps = 0, 0
    for b in range(n - 1, -1, -1):
        trial = code | (1 << b)
        comps += 1
        if vin >= trial * fs / 2**n:
            code = trial
    return code, comps


for v in (0.0, 0.3, 0.71, 0.999):
    c, n = sar(v, 8)
    ok(n == 8 and c == min(int(v * 256), 255), f"8-bit SAR takes 8 comparisons ({v})")
lsb = 1 / 2**10
ans("adc-lsb", round(lsb * 1000, 3), 0.0005)
close(lsb / sqrt(12) * 1e6, 282, 0.002, "quantization noise 282 uV")


def ideal_adc_snr(N, samples=1 << 16):
    full = 2**N
    sig = err = 0.0
    for i in range(samples):
        x = 0.5 + 0.5 * math.sin(2 * pi * 0.1234567 * i) * (1 - 1e-9)
        code = min(int(x * full), full - 1)
        xq = (code + 0.5) / full
        sig += (x - 0.5) ** 2
        err += (x - xq) ** 2
    return 10 * log10(sig / err)


ans("adc-snr", round(6.02 * 12 + 1.76, 1), 0.05)
close(ideal_adc_snr(12), 74.0, 0.002, "quantized sine wave SNR about 74 dB")
ans("dac-string", 2**6)
close(2**10, 1024, 0, "10-bit string 1024 resistors")
ans("flash-comps", len([k for k in range(1, 2**7)]))
close(2**8 - 1, 255, 0, "8-bit flash in the guess: 255 reference voltages")
close(2**12 - 1, 4095, 0, "12-bit flash 4095 comparators")

# ==== boss ====
Id = sq(200e-6, 10, 0.2)
close(Id * 1e6, 40, 1e-9, "boss ID 40 uA")
gm_b = 2 * Id / 0.2
ro_b = 1 / (0.1 * Id)
ans("b-ro", ro_b / 1e3)
close(gm_b * ro_b, 100, 1e-9, "boss intrinsic gain 100")
close(2 / (0.1 * 0.2), 100, 1e-9, "boss 2/(lambda Vov)")
ans("b-cs-gain", -gm_b * par(ro_b, ro_b))
ans("b-ota-gain", gm_b * par(ro_b, ro_b))
close(ota_gain(gm_b, gm_b, ro_b, ro_b, ro_b, ro_b), 50, 0.01, "boss 5T OTA by nodal solve about 50")
ans("b-mirror", 20 * 40 / 10)
fpb = 1 / (2 * pi * 125e3 * 1e-12)
ans("b-dominant-pole", round(fpb / 1e6, 2), 0.005)
close(pole_3db(50, 125e3, 1e-12), fpb, 1e-6, "boss pole by |H| search")
gbw_b = 0.4e-3 / (2 * pi * 1e-12)
ans("b-gbw", round(gbw_b / 1e6, 1), 0.05)
close(50 * fpb, gbw_b, 1e-9, "boss 50 x 1.27 MHz")
ans("b-pm", round(90 - degrees(atan(1 / 2.5))), 0.5)
close(degrees(atan(1 / 2.5)), 21.8, 0.002, "boss p2 phase 21.8 deg")
A0b = 1e6
p1b = bisect(lambda p: abs(A0b / ((1 + 1j * 1e6 / p) * (1 + 1j / 2.5))) - 1, 1e-3, 1e6)
close(pm_two_pole(A0b, p1b, 2.5e6)[0], 68, 0.003, "boss PM from the actual loop")
c1, c2 = 2000 / (1 + 40), 1600 / (1 + 32)
close(c1, 48.78, 0.0002, "boss 48.78")
close(c2, 48.48, 0.0002, "boss 48.48")
ans("b-fb-desens", round((c1 - c2) / c1 * 100, 2), 0.005)
close((c1 - c2) / c1 * 100, 20 / 33, 1e-9, "boss 20 % / 33")
ans("b-thermal", round(sqrt(4 * kT * 1e4) * 1e9, 1), 0.05)
close(4.07 * sqrt(10), 12.9, 0.003, "boss sqrt(10) times 1 kOhm")
ans("b-mos-noise", round(sqrt(4 * kT * (2 / 3) / 0.4e-3) * 1e9, 1), 0.05)
close(4 * kT * (2 / 3) / 0.4e-3, 2.76e-17, 1e-9, "boss 2.76e-17")
ans("b-ktc", round(sqrt(kT / 1e-12) * 1e6), 0.5)
ans("b-miller-gbw", round(0.4e-3 / (2 * pi * 2e-12) / 1e6, 1), 0.05)
ans("b-gm2", 2.2 * 0.4 * 5 / 2)
tc8 = 0.0862 * log(8)
close(tc8, 0.179, 0.002, "boss (k/q) ln 8 = 0.179 mV/K")
ans("b-bandgap-k", round(2 / tc8, 1), 0.05)
close(2 / 0.179, 11.2, 0.003, "rounded TC gives the same 11.2")
ptat = 11.2 * 0.0862e-3 * 300 * log(8)
close(ptat, 0.6, 0.01, "boss PTAT part about 0.6 V at 300 K")
ok(1.1 < 0.65 + ptat < 1.3, "boss output about 1.2 V")
ans("b-sc-req", sc_resistance(1e-12, 1e6) / 1e6)
c, n = sar(0.6180, 10)
ok(n == 10, "10-bit SAR: 10 comparisons")
close(2**10 - 1, 1023, 0, "10-bit flash: 1023 comparators")

# ---- compare with the pack ----
pack = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "data" / "content" / "H.2.6.yaml"
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

print(f"H.2.6 verify.py: all {checks} checks passed ({len(answers)} number answers in the pack).")
