"""Verify all numerical, probabilistic, and firewall-rule claims in data/content/S.2.2.yaml."""
from fractions import Fraction as F
import math


def check_base_rate():
    # Skill-tree exercise (4): N=1,000,000, attacks=10, TPR=99%, FPR=0.1%
    n = 1_000_000
    pos = 10
    neg = n - pos
    tp = F(pos) * F(99, 100)
    fp = F(neg) * F(1, 1000)
    assert tp == F(99, 10)  # 9.9
    assert fp == F(99999, 100)  # 999.99
    ppv = tp / (tp + fp)
    assert math.isclose(float(ppv), 0.009803047856697264, rel_tol=1e-9)
    assert float(ppv) < 0.01  # ~0.98%

    # Worked example / practice: N=100,000, attacks=20, TPR=95%, FPR=0.5%
    tp2 = F(20) * F(95, 100)
    fp2 = F(99_980) * F(5, 1000)
    assert tp2 == F(19)
    assert fp2 == F(4999, 10)  # 499.9
    ppv2 = tp2 / (tp2 + fp2)
    assert math.isclose(float(ppv2), 19 / 518.9, rel_tol=1e-9)  # ~3.66%

    # Boss base-rate: N=500,000, attacks=50, TPR=90%, FPR=0.2%
    tp3 = F(50) * F(90, 100)
    fp3 = F(499_950) * F(2, 1000)
    assert tp3 == F(45)
    assert fp3 == F(9999, 10)  # 999.9
    ppv3 = tp3 / (tp3 + fp3)
    assert math.isclose(float(ppv3), 45 / 1044.9, rel_tol=1e-9)  # ~4.31%


def check_protocol_math():
    # TCP 32-bit seq space and 65536 window
    assert 2**32 == 4_294_967_296
    assert F(2**16, 2**32) == F(1, 65536)

    # SYN flood: backlog=1024, timeout=60s -> 1024/60 = 17.067 -> 18 SYN/s saturates queue
    assert math.ceil(1024 / 60) == 18

    # UDP reflection amplification: 60B query -> 3000B response = 50x; 100 Mbps -> 5 Gbps
    assert 3000 // 60 == 50
    assert 100 * 50 == 5000  # 5000 Mbps = 5 Gbps

    # DNS 16-bit TXID vs TXID + 64000 ephemeral ports + 0x20 (10 letters)
    txid_space = 2**16
    assert txid_space == 65_536
    txid_port_space = txid_space * 64_000
    assert txid_port_space == 4_194_304_000  # ~4.19e9
    assert 2**10 == 1024  # example.com has 10 ASCII letters

    # WEP 24-bit IV birthday collision ~50% threshold: sqrt(2 * ln(2) * 2^24)
    wep_ivs = 2**24
    assert wep_ivs == 16_777_216
    collision_50 = math.sqrt(2 * math.log(2) * wep_ivs)
    assert 4800 < collision_50 < 4850  # ~4823 packets


def check_firewall_rules():
    # First-match stateful firewall evaluator for 3 zones: internal, dmz, external
    # Rule tuples: (src_zone, dst_zone, proto, dst_port, action)
    rules = [
        ("internal", "external", "TCP", 80, "ALLOW"),
        ("internal", "external", "TCP", 443, "ALLOW"),
        ("external", "dmz", "TCP", 443, "ALLOW"),
        ("dmz", "internal", "TCP", 5432, "ALLOW"),
        ("*", "*", "*", "*", "DENY"),
    ]

    def eval_fw(src, dst, proto, port, established=False):
        if established:
            return "ALLOW"
        for s, d, pr, pt, act in rules:
            if (s in ("*", src)) and (d in ("*", dst)) and (pr in ("*", proto)) and (pt in ("*", port)):
                return act
        return "DENY"

    assert eval_fw("internal", "external", "TCP", 443) == "ALLOW"
    assert eval_fw("external", "internal", "TCP", 443, established=True) == "ALLOW"  # return traffic
    assert eval_fw("external", "internal", "TCP", 443, established=False) == "DENY"  # unsolicited inbound
    assert eval_fw("external", "dmz", "TCP", 443) == "ALLOW"
    assert eval_fw("external", "dmz", "TCP", 22) == "DENY"
    assert eval_fw("external", "dmz", "TCP", 5432) == "DENY"
    assert eval_fw("dmz", "internal", "TCP", 5432) == "ALLOW"
    assert eval_fw("dmz", "internal", "TCP", 22) == "DENY"

    # Rule order bug: putting DENY ALL before ALLOW external -> dmz:443 blocks HTTPS
    broken = [("external", "*", "*", "*", "DENY")] + rules
    def eval_broken(src, dst, proto, port):
        for s, d, pr, pt, act in broken:
            if (s in ("*", src)) and (d in ("*", dst)) and (pr in ("*", proto)) and (pt in ("*", port)):
                return act
    assert eval_broken("external", "dmz", "TCP", 443) == "DENY"


def main():
    check_base_rate()
    check_protocol_math()
    check_firewall_rules()
    print("S.2.2 verify: all numerical, probabilistic, and firewall checks passed.")


if __name__ == "__main__":
    main()
