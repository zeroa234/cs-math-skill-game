"""Verify alert expectations and the synthetic stateful firewall examples."""
from fractions import Fraction as F

events, attacks = 1_000_000, 10
true_alerts = attacks * F(99, 100)
false_alerts = (events - attacks) * F(1, 1000)
assert true_alerts == F("9.9")
assert false_alerts == F("999.99")
assert F(round(10000 * true_alerts / (true_alerts + false_alerts)), 100) == F("0.98")
assert 100 * F(10, 10 + 90) == 10
assert 100 * F(20, 20 + 180) == 10

def permits(source, target, protocol, port, reply_to_allowed=False):
    """Teaching policy: allow replies only when matched to an allowed connection."""
    if reply_to_allowed:
        return True
    if protocol != "TCP":
        return False
    return (
        (source == "inside" and target == "outside" and port in (80, 443))
        or (source == "outside" and target == "dmz-web" and port == 443)
    )

assert permits("inside", "outside", "TCP", 80)
assert permits("inside", "outside", "TCP", 443)
assert permits("outside", "dmz-web", "TCP", 443)
assert permits("outside", "inside", "TCP", 50000, reply_to_allowed=True)
assert not permits("outside", "inside", "TCP", 50000)
assert not permits("outside", "dmz-web", "TCP", 80)
assert not permits("outside", "dmz-other", "TCP", 443)
assert not permits("outside", "dmz-web", "UDP", 443)

print("S.2.2: detection base rates and firewall allow/deny cases verified")
