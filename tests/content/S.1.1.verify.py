"""Independent verification of every number, formula, hash demo, and Python snippet in data/content/S.1.1.yaml."""
import hashlib
import math

# 1. security-design-principles: defense in depth joint failure probability
p1, p2 = 0.10, 0.20
joint_fail_2 = p1 * p2
assert math.isclose(joint_fail_2, 0.02, rel_tol=1e-12)
assert math.isclose(1 - joint_fail_2, 0.98, rel_tol=1e-12)

# Three independent layers: 0.1, 0.2, 0.5 -> 0.01 (1%)
joint_fail_3 = 0.1 * 0.2 * 0.5
assert math.isclose(joint_fail_3, 0.01, rel_tol=1e-12)
assert math.isclose(joint_fail_3 * 100, 1.0, rel_tol=1e-12)

# 2. password-psychology-and-systems: search space & entropy
pin4 = 10 ** 4
pin6 = 10 ** 6
lower8 = 26 ** 8
words4_2048 = 2048 ** 4
assert pin4 == 10_000
assert pin6 == 1_000_000
assert lower8 == 208_827_064_576
assert words4_2048 == 2 ** 44 == 17_592_186_044_416
assert round(math.log2(pin4), 2) == 13.29
assert round(math.log2(pin6), 2) == 19.93
assert round(math.log2(lower8), 2) == 37.60
assert math.log2(words4_2048) == 44.0
assert words4_2048 // lower8 == 84

# Practice: 4 random words from 1024-word list -> 40 bits
assert math.log2(1024 ** 4) == 40.0

# Practice: online rate limit 5 tries/min on 4-digit PIN -> worst case 2000 min
assert pin4 // 5 == 2000
assert pin4 % 5 == 0

# Boss entropy item: 5 random words from 256-word list -> 5 * 8 = 40 bits;
# or 6 random chars from 64-char alphabet -> 6 * 6 = 36 bits
assert math.log2(64 ** 6) == 36.0

# 3. password-protection: SHA-256 salt uniqueness & offline crack timing
h_plain_a = hashlib.sha256(b"sunset42").hexdigest()
h_plain_b = hashlib.sha256(b"sunset42").hexdigest()
assert h_plain_a == h_plain_b

h_salt_a = hashlib.sha256(b"a9f3c1:sunset42").hexdigest()
h_salt_b = hashlib.sha256(b"7b2e84:sunset42").hexdigest()
assert h_salt_a != h_salt_b

# Reveal example: space 10^10; fast hash 10^9/s -> 10 s; slow KDF 10^4/s -> 10^6 s (~11.57 days)
space_demo = 10 ** 10
fast_sec = space_demo / (10 ** 9)
slow_sec = space_demo / (10 ** 4)
assert fast_sec == 10.0
assert slow_sec == 1_000_000.0
assert round(slow_sec / 86400, 2) == 11.57

# Practice: space 6,000,000; fast 1,000,000/s -> 6 s; slow 500/s -> 12,000 s
space_q = 6_000_000
assert space_q // 1_000_000 == 6
assert space_q // 500 == 12_000
assert space_q % 500 == 0

# 4. mediation-defaults-and-tcb: Python fail-safe default logic
def can_read_demo(role, rules):
    allowed = False
    if role in rules:
        allowed = rules[role]
    return allowed

rules_demo = {"admin": True, "auditor": True, "guest": False}
assert can_read_demo("admin", rules_demo) is True
assert can_read_demo("intern", rules_demo) is False

def check_access(role, active, allow_roles):
    allowed = False
    if active and role in allow_roles:
        allowed = True
    return allowed

assert check_access("editor", True, ["admin", "editor"]) is True
assert check_access("editor", False, ["admin", "editor"]) is False
assert check_access("intern", True, ["admin", "editor"]) is False

# 5. tocttou-vulnerabilities: race condition double-withdrawal
balance = 100
req_a = 80
req_b = 80
# Both pass check before write-back
assert balance >= req_a and balance >= req_b
dispensed = req_a + req_b
assert dispensed == 160
assert balance - req_a == 20

# Practice: balance 500, three parallel withdrawals of 300 -> 900 dispensed
assert 3 * 300 == 900
assert 900 - 500 == 400

# 6. risk-economics-and-quantification: SLE / ALE / net benefit
# Reveal example
av_demo, ef_demo, aro_demo = 40, 0.25, 0.6
sle_demo = av_demo * ef_demo
ale_before_demo = sle_demo * aro_demo
aro_after_demo, cost_demo = 0.2, 1.5
ale_after_demo = sle_demo * aro_after_demo
reduction_demo = ale_before_demo - ale_after_demo
net_demo = reduction_demo - cost_demo
assert math.isclose(sle_demo, 10.0)
assert math.isclose(ale_before_demo, 6.0)
assert math.isclose(ale_after_demo, 2.0)
assert math.isclose(reduction_demo, 4.0)
assert math.isclose(net_demo, 2.5)

# Practice 1: AV = 60, EF = 30%, ARO = 0.5 -> SLE = 18, ALE = 9
av_q1, ef_q1, aro_q1 = 60, 0.30, 0.5
sle_q1 = av_q1 * ef_q1
ale_q1 = sle_q1 * aro_q1
assert math.isclose(sle_q1, 18.0)
assert math.isclose(ale_q1, 9.0)

# Practice 2: AV = 80, EF = 25% -> SLE = 20; ARO 0.4 -> 0.1; cost = 2 -> net = 4
av_q2, ef_q2 = 80, 0.25
sle_q2 = av_q2 * ef_q2
ale_before_q2 = sle_q2 * 0.4
ale_after_q2 = sle_q2 * 0.1
net_q2 = (ale_before_q2 - ale_after_q2) - 2.0
assert math.isclose(sle_q2, 20.0)
assert math.isclose(ale_before_q2, 8.0)
assert math.isclose(ale_after_q2, 2.0)
assert math.isclose(net_q2, 4.0)

# Boss SLE/ALE item: AV = 100, EF = 20% -> SLE = 20; ARO 0.5 -> 0.1; cost = 3 -> net = 5
av_boss, ef_boss = 100, 0.20
sle_boss = av_boss * ef_boss
ale_before_boss = sle_boss * 0.5
ale_after_boss = sle_boss * 0.1
net_boss = (ale_before_boss - ale_after_boss) - 3.0
assert math.isclose(sle_boss, 20.0)
assert math.isclose(ale_before_boss, 10.0)
assert math.isclose(ale_after_boss, 2.0)
assert math.isclose(net_boss, 5.0)

# 7. detect-respond-and-governance: false positive rate & alert precision
# Reveal example: 10,000 normal logins (1% FP = 100), 10 real attacks (100% caught = 10)
fp_demo = int(10_000 * 0.01)
tp_demo = 10
total_alerts_demo = fp_demo + tp_demo
precision_demo = tp_demo / total_alerts_demo
assert fp_demo == 100
assert total_alerts_demo == 110
assert round(precision_demo * 100, 1) == 9.1

# Practice: 4,000 normal logins (2% FP = 80), 20 real attacks (100% caught = 20)
fp_q = int(4_000 * 0.02)
tp_q = 20
total_alerts_q = fp_q + tp_q
assert fp_q == 80
assert total_alerts_q == 100
assert tp_q / total_alerts_q == 0.20
assert fp_q / total_alerts_q == 0.80

print("S.1.1 verify OK")
