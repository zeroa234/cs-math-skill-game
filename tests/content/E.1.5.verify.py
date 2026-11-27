#!/usr/bin/env python3
"""Independent numerical verification for E.1.5 (RF Integrated Circuit Design).

Uses Python standard library only. Recomputes every worked example, card number,
lesson item, and boss item from first principles, and cross-checks every `number`
item answer in data/content/E.1.5.yaml.
"""
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
PACK_PATH = ROOT / "data" / "content" / "E.1.5.yaml"

checks = 0


def check_close(name: str, got: float, expected: float, tol: float = 1e-6) -> None:
    global checks
    checks += 1
    if not math.isfinite(got) or abs(got - expected) > tol:
        raise AssertionError(f"{name}: got {got}, expected {expected} (tol {tol})")


def db10(x: float) -> float:
    return 10.0 * math.log10(x)


def db20(x: float) -> float:
    return 20.0 * math.log10(x)


def undb10(x: float) -> float:
    return 10.0 ** (x / 10.0)


def parse_yaml_number_answers(text: str) -> dict[str, float]:
    """Extract {item_id: float(answer)} for every type: number item."""
    answers: dict[str, float] = {}
    cur_id = None
    cur_type = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        m_id = re.match(r"^(?:-\s+)?id:\s*([A-Za-z0-9_-]+)\s*$", line)
        if m_id:
            cur_id = m_id.group(1)
            cur_type = None
            continue
        m_type = re.match(r"^type:\s*([A-Za-z0-9_-]+)\s*$", line)
        if m_type:
            cur_type = m_type.group(1)
            continue
        m_ans = re.match(r"^answer:\s*([-+]?[0-9]+(?:\.[0-9]+)?)\s*$", line)
        if m_ans and cur_id and cur_type == "number":
            answers[cur_id] = float(m_ans.group(1))
    return answers


def main() -> int:
    text = PACK_PATH.read_text(encoding="utf-8")
    yaml_ans = parse_yaml_number_answers(text)

    # 1. rf-foundations
    # Thermal noise floor at T0 = 290 K: k*T0 in dBm/Hz
    k_B = 1.380649e-23
    noise_floor_dbm_hz = db10(k_B * 290.0 * 1e3)
    check_close("thermal noise floor", noise_floor_dbm_hz, -173.98, tol=0.05)

    # Worked example: Friis 3-stage (2 dB/16 dB, 11 dB/6 dB, 14 dB)
    f1, g1 = undb10(2.0), undb10(16.0)
    f2, g2 = undb10(11.0), undb10(6.0)
    f3 = undb10(14.0)
    f_ex1 = f1 + (f2 - 1.0) / g1 + (f3 - 1.0) / (g1 * g2)
    check_close("ex1 Friis F", f_ex1, 2.028, tol=0.005)
    check_close("ex1 Friis NF", db10(f_ex1), 3.07, tol=0.01)
    # Worked example sensitivity: B=10 MHz, NF=5 dB, SNRmin=12 dB
    sens_ex1 = -174.0 + db10(10e6) + 5.0 + 12.0
    check_close("ex1 sensitivity", sens_ex1, -87.0, tol=1e-6)

    # q-friis-2stage: NF1=2.0 dB, G1=13 dB, NF2=12.0 dB
    f_q1 = undb10(2.0) + (undb10(12.0) - 1.0) / undb10(13.0)
    nf_q1 = round(db10(f_q1), 2)
    check_close("q-friis-2stage", nf_q1, 3.67, tol=0.01)

    # q-sens-calc: B=1 MHz, NF=6 dB, SNRmin=10 dB
    sens_q = -174.0 + db10(1e6) + 6.0 + 10.0
    check_close("q-sens-calc", sens_q, -98.0, tol=1e-6)

    # 2. rx-architectures
    # Ex: f_RF=900, f_IF=45, high-side LO=945 -> f_IM=990
    check_close("ex2 high-side image", 900.0 + 2 * 45.0, 990.0)
    # q-image-lowside: f_RF=2400, f_IF=100, low-side LO=2300 -> f_IM=2200
    f_im_q = 2400.0 - 2 * 100.0
    check_close("q-image-lowside", f_im_q, 2200.0)

    # 3. tx-architectures
    # Ex: 3.6 GHz + 1.8 GHz = 5.4 GHz
    check_close("ex3 offset LO", 3.6 + 3.6 / 2.0, 5.4)
    # q-tx-freq-plan: (3/2)*f_VCO = 2.4 -> 1.6 GHz
    f_vco_tx = 2.4 * 2.0 / 3.0
    check_close("q-tx-freq-plan", f_vco_tx, 1.6)

    # 4. lna-matching
    # Shunt 50 ohm match NF = 10 log10(2) = 3.01 dB
    check_close("shunt 50 ohm NF", db10(2.0), 3.01, tol=0.01)
    # Ex: Vs_rms = 2 mV, Rs = 50 -> Pav = 20 nW (-47.0 dBm)
    p_av_ex = (2e-3) ** 2 / (4.0 * 50.0)
    check_close("ex4 Pav nW", p_av_ex * 1e9, 20.0, tol=1e-6)
    check_close("ex4 Pav dBm", db10(p_av_ex * 1e3), -47.0, tol=0.02)
    # q-lna-pav: Vs_rms = 4 mV, Rs = 50 -> 80 nW
    p_av_q = ((4e-3) ** 2 / (4.0 * 50.0)) * 1e9
    check_close("q-lna-pav", p_av_q, 80.0, tol=1e-6)

    # 5. lna-topologies
    # Ex: 5 GHz, fT=80 GHz, Cgs=120 fF
    ls_ex5 = 50.0 / (2.0 * math.pi * 80e9)
    ltot_ex5 = 1.0 / ((2.0 * math.pi * 5e9) ** 2 * 120e-15)
    check_close("ex5 Ls nH", ls_ex5 * 1e9, 0.10, tol=0.005)
    check_close("ex5 Ltot nH", ltot_ex5 * 1e9, 8.44, tol=0.01)
    check_close("ex5 Lg nH", (ltot_ex5 - ls_ex5) * 1e9, 8.34, tol=0.01)
    # q-lna-ls: fT=40 GHz -> Ls = 0.20 nH
    ls_q = round((50.0 / (2.0 * math.pi * 40e9)) * 1e9, 2)
    check_close("q-lna-ls", ls_q, 0.20, tol=0.005)
    # q-lna-lg: f0=5.0 GHz, Cgs=100 fF, Ls=0.20 nH -> Lg = 9.93 nH
    ltot_q5 = 1.0 / ((2.0 * math.pi * 5e9) ** 2 * 100e-15)
    lg_q = round(ltot_q5 * 1e9 - 0.20, 2)
    check_close("q-lna-lg", lg_q, 9.93, tol=0.01)
    # q-cg-gm: 1/50 S = 20 mS
    check_close("q-cg-gm", (1.0 / 50.0) * 1e3, 20.0)

    # 6. lna-switching-ip2
    # Ex: -20 + 18 = -2, -20 + 6 = -14; 2412 - 2410 = 2 MHz
    check_close("ex6 IM2", 2412.0 - 2410.0, 2.0)
    # q-im2-freq: 1819 - 1815 = 4 MHz
    check_close("q-im2-freq", 1819.0 - 1815.0, 4.0)

    # 7. mixer-basics-passive
    gv_pass = 2.0 / math.pi
    gv_pass_db = round(db20(gv_pass), 2)
    check_close("ex7 passive gain lin", gv_pass, 0.637, tol=0.001)
    check_close("q-passive-gain-db", gv_pass_db, -3.92, tol=0.01)

    # 8. active-mixers
    # Ex: gm=20 mS, RD=250 -> 3.183 (10.1 dB)
    gv_act_ex = (2.0 / math.pi) * 0.020 * 250.0
    check_close("ex8 Gilbert Gv", gv_act_ex, 3.183, tol=0.005)
    check_close("ex8 Gilbert dB", db20(gv_act_ex), 10.06, tol=0.05)
    # q-gilbert-gv-lin: gm=15 mS, RD=400 -> 3.82
    gv_act_q = round((2.0 / math.pi) * 0.015 * 400.0, 2)
    check_close("q-gilbert-gv-lin", gv_act_q, 3.82, tol=0.01)

    # 9. mixer-improved-upconv
    # Ex: 0.6/2m = 300, 0.6/0.8m = 750
    check_close("ex9 no bleed", 0.60 / 2e-3, 300.0)
    check_close("ex9 bleed", 0.60 / 0.8e-3, 750.0)
    # q-bleeding-rd: 0.50 / (2.5m - 1.5m) = 500 ohm
    rd_bleed_q = 0.50 / ((2.5 - 1.5) * 1e-3)
    check_close("q-bleeding-rd", rd_bleed_q, 500.0)

    # 10. oscillator-lc-topologies
    # Ex: L=1.6 nH, C=1.0 pF, Q=10 -> f0=3.98 GHz, wL=40.0 ohm, Rp=400 ohm, gm_min=2.5 mS
    f0_ex10 = 1.0 / (2.0 * math.pi * math.sqrt(1.6e-9 * 1.0e-12))
    wL_ex10 = 2.0 * math.pi * f0_ex10 * 1.6e-9
    rp_ex10 = 10.0 * wL_ex10
    check_close("ex10 f0 GHz", f0_ex10 / 1e9, 3.98, tol=0.01)
    check_close("ex10 Rp", rp_ex10, 400.0, tol=0.5)
    check_close("ex10 gm_min mS", (1.0 / rp_ex10) * 1e3, 2.5, tol=0.02)
    # q-lc-freq: L=1.0 nH, C=1.0 pF -> 5.03 GHz
    f0_q10 = round(1.0 / (2.0 * math.pi * math.sqrt(1.0e-9 * 1.0e-12)) / 1e9, 2)
    check_close("q-lc-freq", f0_q10, 5.03, tol=0.01)
    # q-lc-gm-min: Rp=250, margin 2 -> 8 mS
    gm_q10 = (2.0 / 250.0) * 1e3
    check_close("q-lc-gm-min", gm_q10, 8.0)

    # 11. vco-tuning-quadrature
    # Ex: Cmax/Cmin = 1.44 -> 1.20 -> 2.40 GHz, KVCO = 400 MHz/V
    check_close("ex11 fmax", 2.0 * math.sqrt(1.44 / 1.0), 2.40)
    check_close("ex11 KVCO", (2400.0 - 2000.0) / (1.2 - 0.2), 400.0)
    # q-vco-fmax: 2.0 * sqrt(1.69) = 2.60 GHz
    fmax_q = round(2.0 * math.sqrt(1.69), 2)
    check_close("q-vco-fmax", fmax_q, 2.60)
    # q-vco-kvco: (2520 - 2400) / (1.0 - 0.4) = 200 MHz/V
    kvco_q = (2520.0 - 2400.0) / (1.0 - 0.4)
    check_close("q-vco-kvco", kvco_q, 200.0)

    # 12. vco-phase-noise
    # Ex: -112 - 20 = -132; -35 - 125 + 60 = -100
    check_close("ex12 PN@10MHz", -112.0 - 20.0, -132.0)
    check_close("ex12 recip", -35.0 - 125.0 + db10(1e6), -100.0)
    # q-pn-10x: -118 - 20 = -138
    check_close("q-pn-10x", -118.0 - 20.0, -138.0)
    # q-recip-noise: -30 - 122 + 60 = -92
    check_close("q-recip-noise", -30.0 - 122.0 + db10(1e6), -92.0)

    # 13. pll-type1-type2
    # Ex: Icp=200u, Kv=80M, C1=160p, R1=1k -> wn=10 Mrad/s, zeta=0.80
    wn_ex13 = math.sqrt(200e-6 * 80e6 / 160e-12)
    zeta_ex13 = 0.5 * wn_ex13 * 1000.0 * 160e-12
    check_close("ex13 wn Mrad/s", wn_ex13 / 1e6, 10.0)
    check_close("ex13 zeta", zeta_ex13, 0.80)
    # q-pll-wn & q-pll-zeta: Icp=100u, Kv=90M, C1=250p, R1=1k -> wn=6.0, zeta=0.75
    wn_q13 = math.sqrt(100e-6 * 90e6 / 250e-12)
    zeta_q13 = 0.5 * wn_q13 * 1000.0 * 250e-12
    check_close("q-pll-wn", wn_q13 / 1e6, 6.0)
    check_close("q-pll-zeta", zeta_q13, 0.75)

    # 14. pll-noise-bandwidth
    # Ex: N = 2000/20 = 100 -> +40 dB -> -105 dBc/Hz
    check_close("ex14 20lgN", db20(2000.0 / 20.0), 40.0)
    # q-pll-20logn: N = 2500/50 = 50 -> 34.0 dB
    n_lift_q = round(db20(2500.0 / 50.0), 1)
    check_close("q-pll-20logn", n_lift_q, 34.0)

    # 15. integer-n-synthesizer
    # Ex: N_int=1200, N_frac=60, 20lg(20)=26.02 dB
    check_close("ex15 improvement", db20(1200.0 / 60.0), 26.02, tol=0.05)
    # q-intn-nval: 900e6 / 200e3 = 4500
    check_close("q-intn-nval", 900e6 / 200e3, 4500.0)
    # q-intn-bw: 200 / 10 = 20 kHz
    check_close("q-intn-bw", 200.0 / 10.0, 20.0)

    # 16. pa-loadline-classes
    # Ex: VDD=3.3 V, RL=50 -> 108.9 mW (20.4 dBm); 27 dBm -> 10.9 ohm
    pmax_ex16 = 3.3 ** 2 / (2.0 * 50.0)
    ropt_ex16 = 3.3 ** 2 / (2.0 * undb10(27.0) * 1e-3)
    check_close("ex16 Pmax dBm", db10(pmax_ex16 * 1e3), 20.37, tol=0.05)
    check_close("ex16 Ropt", ropt_ex16, 10.86, tol=0.05)
    # q-pa-pmax-2v: VDD=2.0 V, RL=50 -> 40 mW -> 16.0 dBm
    pmax_q16 = round(db10((2.0 ** 2 / (2.0 * 50.0)) * 1e3), 1)
    check_close("q-pa-pmax-2v", pmax_q16, 16.0)
    # q-pa-ropt-2v: VDD=2.0 V, 100 mW -> 20 ohm
    ropt_q16 = 2.0 ** 2 / (2.0 * 0.100)
    check_close("q-pa-ropt-2v", ropt_q16, 20.0)

    # 17. pa-high-efficiency
    # Ex: Pout=200, G=10 -> Pin=20, PDC=400 -> eta=50%, PAE=45%
    check_close("ex17 PAE", (200.0 - 20.0) / 400.0 * 100.0, 45.0)
    # q-pae-calc: (500-50)/750 = 60%
    check_close("q-pae-calc", (500.0 - 50.0) / 750.0 * 100.0, 60.0)

    # 18. pa-linearization-doherty
    # Ex: Class B at 6 dB BO -> pi/8 = 39.3%
    check_close("ex18 Class B 6dB BO", (math.pi / 8.0) * 100.0, 39.27, tol=0.05)
    # q-classb-12db: pi/16 = 19.6%
    cb_12db = round((math.pi / 16.0) * 100.0, 1)
    check_close("q-classb-12db", cb_12db, 19.6)

    # 19. impedance-matching
    # Ex: 50 -> 10 ohm @ 2 GHz: Q=2, Xs=20 (L=1.59 nH), Xp=25 (C=3.18 pF)
    q_ex19 = math.sqrt(50.0 / 10.0 - 1.0)
    w_ex19 = 2.0 * math.pi * 2.0e9
    check_close("ex19 Q", q_ex19, 2.0)
    check_close("ex19 L nH", (20.0 / w_ex19) * 1e9, 1.59, tol=0.01)
    check_close("ex19 C pF", (1.0 / (w_ex19 * 25.0)) * 1e12, 3.18, tol=0.01)
    # q-lmatch-q: 50 -> 5 ohm -> Q = 3.0
    check_close("q-lmatch-q", math.sqrt(50.0 / 5.0 - 1.0), 3.0)
    # q-lmatch-rp: Rs=4, Xs=12 (Q=3) -> Rp = 40 ohm
    check_close("q-lmatch-rp", 4.0 * (1.0 + (12.0 / 4.0) ** 2), 40.0)

    # 20. s-parameters-tlines
    # Ex: ZL=100, Z0=50 -> Gamma=1/3, RL=9.54 dB; Zq = sqrt(50*200)=100
    g_ex20 = (100.0 - 50.0) / (100.0 + 50.0)
    check_close("ex20 RL", -db20(abs(g_ex20)), 9.54, tol=0.01)
    check_close("ex20 Zq", math.sqrt(50.0 * 200.0), 100.0)
    # q-gamma-rl: ZL=75, Z0=50 -> Gamma=0.20, RL=14.0 dB
    rl_q20 = round(-db20(abs((75.0 - 50.0) / (75.0 + 50.0))), 1)
    check_close("q-gamma-rl", rl_q20, 14.0)
    # q-qwave-z0: sqrt(50*12.5) = 25 ohm
    check_close("q-qwave-z0", math.sqrt(50.0 * 12.5), 25.0)

    # 21. onchip-passives
    # Ex: L=2 nH @ 5 GHz, Rs=6.28 -> Q=10.0, Cp=50 fF -> SRF=15.9 GHz
    wL_ex21 = 2.0 * math.pi * 5e9 * 2e-9
    check_close("ex21 Q", wL_ex21 / 6.28, 10.0, tol=0.05)
    check_close("ex21 SRF", 1.0 / (2.0 * math.pi * math.sqrt(2e-9 * 50e-15)) / 1e9, 15.92, tol=0.05)
    # q-ind-q-calc: L=5 nH @ 1 GHz, Rs=2.5 -> Q=12.6
    q_ind_q = round((2.0 * math.pi * 1e9 * 5e-9) / 2.5, 1)
    check_close("q-ind-q-calc", q_ind_q, 12.6)
    # q-ind-srf: L=2.5 nH, Cp=100 fF -> 10.1 GHz
    srf_q = round(1.0 / (2.0 * math.pi * math.sqrt(2.5e-9 * 100e-15)) / 1e9, 1)
    check_close("q-ind-srf", srf_q, 10.1)

    # 22. nonlinearity-p1db-ip3
    # Ex: Pin=-25, Pout=-10, PIM3=-64 -> G=15, OIP3=17, IIP3=2, P1dB=-7.6
    check_close("ex22 OIP3", -10.0 + (-10.0 - (-64.0)) / 2.0, 17.0)
    check_close("ex22 IIP3", 17.0 - 15.0, 2.0)
    # q-ip3-oip3 & q-ip3-iip3: Pin=-20, Pout=-8, PIM3=-56 -> OIP3=16, IIP3=4
    oip3_q = -8.0 + (-8.0 - (-56.0)) / 2.0
    iip3_q = oip3_q - (-8.0 - (-20.0))
    check_close("q-ip3-oip3", oip3_q, 16.0)
    check_close("q-ip3-iip3", iip3_q, 4.0)

    # 23. cascaded-linearity-sfdr
    # Ex: G1=10 dB, IIP3_1=+10 dBm, IIP3_2=+10 dBm -> -0.41 dBm; SFDR @ -105.4 -> 70.0 dB
    iip3_ex23 = db10(1.0 / (1.0 / undb10(10.0) + undb10(10.0) / undb10(10.0)))
    check_close("ex23 cascaded IIP3", iip3_ex23, -0.41, tol=0.01)
    check_close("ex23 SFDR", (2.0 / 3.0) * (iip3_ex23 - (-105.4)), 70.0, tol=0.05)
    # q-casc-iip3-calc: G1=15 dB, IIP3_1=+10 dBm, IIP3_2=+5 dBm -> -10.0 dBm
    iip3_casc_q = round(db10(1.0 / (1.0 / undb10(10.0) + undb10(15.0) / undb10(5.0))), 1)
    check_close("q-casc-iip3-calc", iip3_casc_q, -10.0)
    # q-sfdr-calc: IIP3=-5, Pnoise=-110 -> 70 dB
    sfdr_q = (2.0 / 3.0) * (-5.0 - (-110.0))
    check_close("q-sfdr-calc", sfdr_q, 70.0)

    # BOSS (all 8 original exercises)
    # (2) b-friis-nf: LNA 1.5/15, Mixer 10/5, IF 12 -> 2.7 dB
    f_b = undb10(1.5) + (undb10(10.0) - 1.0) / undb10(15.0) + (undb10(12.0) - 1.0) / (undb10(15.0) * undb10(5.0))
    nf_b = round(db10(f_b), 1)
    check_close("b-friis-nf", nf_b, 2.7)

    # (3) b-lna-ls & b-lna-lg: wT=2pi*50GHz -> Ls=0.16 nH; 2.4GHz, 100fF -> Lg=43.8 nH
    ls_b = 50.0 / (2.0 * math.pi * 50e9)
    ltot_b = 1.0 / ((2.0 * math.pi * 2.4e9) ** 2 * 100e-15)
    lg_b = ltot_b - ls_b
    check_close("b-lna-ls", round(ls_b * 1e9, 2), 0.16)
    check_close("b-lna-lg", round(lg_b * 1e9, 1), 43.8)

    # (4) b-vco-freq: L=2.0 nH, C=2.2 pF -> 2.40 GHz
    fvco_b = round(1.0 / (2.0 * math.pi * math.sqrt(2.0e-9 * 2.2e-12)) / 1e9, 2)
    check_close("b-vco-freq", fvco_b, 2.40)

    # (6) b-pa-pmax & b-pa-ropt: VDD=1.8V -> 15.1 dBm, 23 dBm -> 8.1 ohm
    pmax_b = round(db10((1.8 ** 2 / (2.0 * 50.0)) * 1e3), 1)
    ropt_b = round(1.8 ** 2 / (2.0 * undb10(23.0) * 1e-3), 1)
    check_close("b-pa-pmax", pmax_b, 15.1)
    check_close("b-pa-ropt", ropt_b, 8.1)

    # (8) b-iip3-calc & b-p1db-gap
    oip3_b = -10.0 + (-10.0 - (-70.0)) / 2.0
    iip3_b = oip3_b - (-10.0 - (-30.0))
    gap_b = round(-db20(math.sqrt(0.145 * 3.0 / 4.0)), 1)
    check_close("b-iip3-calc", iip3_b, 0.0)
    check_close("b-p1db-gap", gap_b, 9.6)

    # Cross-check EVERY `type: number` answer in YAML
    expected_yaml = {
        "q-friis-2stage": nf_q1,
        "q-sens-calc": sens_q,
        "q-image-lowside": f_im_q,
        "q-tx-freq-plan": f_vco_tx,
        "q-lna-pav": p_av_q,
        "q-lna-ls": ls_q,
        "q-lna-lg": lg_q,
        "q-cg-gm": 20.0,
        "q-im2-freq": 4.0,
        "q-passive-gain-db": gv_pass_db,
        "q-gilbert-gv-lin": gv_act_q,
        "q-bleeding-rd": rd_bleed_q,
        "q-lc-freq": f0_q10,
        "q-lc-gm-min": gm_q10,
        "q-vco-fmax": fmax_q,
        "q-vco-kvco": kvco_q,
        "q-pn-10x": -138.0,
        "q-recip-noise": -92.0,
        "q-pll-wn": 6.0,
        "q-pll-zeta": 0.75,
        "q-pll-20logn": n_lift_q,
        "q-intn-nval": 4500.0,
        "q-intn-bw": 20.0,
        "q-pa-pmax-2v": pmax_q16,
        "q-pa-ropt-2v": ropt_q16,
        "q-pae-calc": 60.0,
        "q-classb-12db": cb_12db,
        "q-lmatch-q": 3.0,
        "q-lmatch-rp": 40.0,
        "q-gamma-rl": rl_q20,
        "q-qwave-z0": 25.0,
        "q-ind-q-calc": q_ind_q,
        "q-ind-srf": srf_q,
        "q-ip3-oip3": oip3_q,
        "q-ip3-iip3": iip3_q,
        "q-casc-iip3-calc": iip3_casc_q,
        "q-sfdr-calc": sfdr_q,
        "b-friis-nf": nf_b,
        "b-lna-ls": 0.16,
        "b-lna-lg": 43.8,
        "b-vco-freq": fvco_b,
        "b-pa-pmax": pmax_b,
        "b-pa-ropt": ropt_b,
        "b-iip3-calc": iip3_b,
        "b-p1db-gap": gap_b,
    }

    missing = set(yaml_ans.keys()) - set(expected_yaml.keys())
    extra = set(expected_yaml.keys()) - set(yaml_ans.keys())
    if missing or extra:
        raise AssertionError(f"YAML number item mismatch: missing={missing}, extra={extra}")

    for item_id, exp in expected_yaml.items():
        check_close(f"YAML item {item_id}", yaml_ans[item_id], exp, tol=1e-6)

    print(f"E.1.5 verify.py OK: {checks} checks ({len(yaml_ans)} YAML number answers verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
