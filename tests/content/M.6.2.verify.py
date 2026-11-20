"""Verify every numerical claim, worked example, and number-item answer in data/content/M.6.2.yaml.

Uses only the Python standard library (fractions, math, statistics) plus Node's js-yaml
to read data/content/M.6.2.yaml so it runs cleanly under `python -I`.
"""
from __future__ import annotations

import json
import math
import statistics
import subprocess
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK_PATH = ROOT / "data" / "content" / "M.6.2.yaml"

_raw = subprocess.check_output(
    [
        "node",
        "-e",
        (
            "const fs=require('fs'), y=require('js-yaml');"
            "console.log(JSON.stringify(y.load(fs.readFileSync(process.argv[1],'utf8'))));"
        ),
        str(PACK_PATH),
    ],
    encoding="utf-8",
)
PACK = json.loads(_raw)

ANSWERS: dict[str, float] = {}
for lesson in PACK["lessons"]:
    for step in lesson["flow"]:
        it = step.get("item") or step.get("guess")
        if it and it.get("type") == "number":
            ANSWERS[it["id"]] = float(it["answer"])
for it in PACK["boss"]["items"]:
    if it.get("type") == "number":
        ANSWERS[it["id"]] = float(it["answer"])

CHECKED_ITEMS: set[str] = set()
CLAIMS = 0


def check_close(label: str, actual: float | Fraction, expected: float | Fraction, tol: float = 1e-9) -> None:
    global CLAIMS
    CLAIMS += 1
    a, e = float(actual), float(expected)
    assert abs(a - e) <= tol, f"{label}: got {a!r}, expected {e!r} (diff={abs(a - e)})"


def check_item(item_id: str, expected: float | Fraction, tol: float = 1e-6) -> None:
    assert item_id in ANSWERS, f"missing number item {item_id!r} in M.6.2.yaml"
    CHECKED_ITEMS.add(item_id)
    check_close(f"item:{item_id}", ANSWERS[item_id], expected, tol=tol)


def phi(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def simpson(f, a: float, b: float, n: int = 2000) -> float:
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4.0 if i % 2 == 1 else 2.0) * f(a + i * h)
    return s * h / 3.0


def t_pdf(x: float, df: int) -> float:
    c = math.exp(math.lgamma((df + 1) / 2.0) - math.lgamma(df / 2.0)) / math.sqrt(df * math.pi)
    return c * (1.0 + (x * x) / df) ** (-(df + 1) / 2.0)


def t_two_sided_p(t_val: float, df: int) -> float:
    # P(|T| >= |t_val|) = 1 - P(-|t| <= T <= |t|)
    a = abs(t_val)
    return 1.0 - 2.0 * simpson(lambda x: t_pdf(x, df), 0.0, a, n=4000)


# ── Chapter 1: 抽样分布 ──────────────────────────────────────────────
# Lesson 1: sampling-order
check_item("max-order-stat-prob", Fraction(6, 10) ** 3)
check_item("min-order-stat-exp", math.exp(-4.0 * 0.5), tol=1e-5)
arr_ord = sorted([24, 11, 18, 30, 15])
check_item("order-stat-median-range", arr_ord[2] + (arr_ord[-1] - arr_ord[0]))

# Lesson 2: sampling-dists
check_close("example:guess-se", 15.0 / math.sqrt(25), 3.0)
check_item("order-pdf-expectation", simpson(lambda x: x * 2.0 * x, 0.0, 1.0), tol=1e-6)
check_close("example:order-min-expectation", simpson(lambda x: x * 2.0 * (1.0 - x), 0.0, 1.0), 1.0 / 3.0, tol=1e-6)
check_item("sample-mean-se", Fraction(12, 4))

# ── Chapter 2: 估计 ──────────────────────────────────────────────────
# Lesson 3: point-estimators
data_var = [10, 12, 14, 16]
check_item("sample-variance-unbiased", Fraction(sum((x - 13) ** 2 for x in data_var), len(data_var) - 1), tol=1e-6)
check_close("example:mse-A", 10 + 0 ** 2, 10)
check_close("example:mse-B", 3 + (6 - 5) ** 2, 4)
check_item("mse-calc-item", 5 + (12 - 10) ** 2)

# Lesson 4: sufficiency-mom
check_close("example:mom-uniform", 2.0 * statistics.mean([1.2, 2.8, 3.5, 4.5]), 6.0)
check_item("mom-exp-item", Fraction(10, 25))
# (b-a)^2/12 = 3 -> b-a = 6, (a+b)/2 = 5 -> b = 8, a = 2
check_close("mom-uniform-ab-width", math.sqrt(12 * 3), 6.0)
check_item("mom-uniform-ab-item", (10 + 6) // 2)

# ── Chapter 3: 渐近理论与决策 ────────────────────────────────────────
# Lesson 5: consistency-delta
check_item("se-sample-size-scale", 25 * (Fraction(60, 15) ** 2))
check_close("example:delta-square", abs(2 * 3) * 0.2, 1.2)
check_item("delta-reciprocal-se", abs(-1.0 / (2.0 ** 2)) * 0.2)

# Lesson 6: errors-and-power
check_item("power-from-beta", Fraction(100 - 15, 100))
n_ex = ((1.96 + 0.84) * 10.0 / 5.0) ** 2
check_close("example:sample-size-raw", n_ex, 31.36)
check_close("example:sample-size-ceil", math.ceil(n_ex), 32)
check_item("sample-size-calc", ((3.0 * 8.0) / 4.0) ** 2)

# Lesson 7: bayesian-decision
check_item("bayes-loss-discrete", Fraction(3, 10) * Fraction(2, 10) + Fraction(7, 10) * Fraction(8, 10))
check_close("example:beta-binom-mean", Fraction(2 + 7, 2 + 2 + 10), 9 / 14)
check_item("beta-binomial-update", Fraction(1 + 3, 1 + 1 + 4), tol=1e-6)

# ── Chapter 4: 似然 ──────────────────────────────────────────────────
# Lesson 8: likelihood-mle
check_item("mle-bernoulli-calc", Fraction(12, 20))
check_item("mle-exp-calc", Fraction(3, 1) / (Fraction(15, 10) + Fraction(20, 10) + Fraction(25, 10)))

# Lesson 9: mle-support-multi
check_close("example:uniform-mle", max([1.4, 3.2, 2.8]), 3.2)
check_close("example:uniform-mom-vs-mle", 2.0 * statistics.mean([1.4, 3.2, 2.8]), 14.8 / 3.0, tol=1e-4)
check_item("mle-uniform-boundary", max([2.1, 4.8, 3.5, 1.9]))
norm_s = [2, 4, 6]
m_s = sum(norm_s) / len(norm_s)
check_item("normal-mle-variance", Fraction(sum((x - int(m_s)) ** 2 for x in norm_s), len(norm_s)), tol=1e-6)
check_item("mle-invariance-exp", Fraction(10, 4))

# Lesson 10: numeric-mle
# Example: l'(t) = 4/t - 2, l''(t) = -4/t^2 at t0=1 -> 1 - 2/(-4) = 1.5
check_close("example:newton-step", 1.0 - (4.0 / 1.0 - 2.0) / (-4.0 / 1.0), 1.5)
# Item: l'(t) = 6/t - 2, l''(t) = -6/t^2 at t0=2 -> 2 - 1/(-1.5) = 8/3
check_item("newton-step-calc", 2.0 - (6.0 / 2.0 - 2.0) / (-6.0 / 4.0), tol=1e-6)

# Lesson 11: fisher-asymptotic
check_item("fisher-bernoulli-calc", Fraction(25, 1) / (Fraction(1, 2) * Fraction(1, 2)))
check_item("fisher-exp-se", 1.0 / math.sqrt(25.0 / (2.0 ** 2)))
check_item("observed-fisher-se", 1.0 / math.sqrt(100.0))

# ── Chapter 5: 置信区间 ──────────────────────────────────────────────
# Lesson 12: ci-normal-exact (including C4 exercise 1 & 4)
parts = [4.8, 5.1, 5.3, 4.9, 5.4, 5.0, 5.2, 4.7, 5.1, 5.5]
p_mean = statistics.mean(parts)
p_s = statistics.stdev(parts)
p_se = p_s / math.sqrt(len(parts))
t_crit_9 = 2.262  # verified against t_two_sided_p(2.262, 9) ~ 0.05
check_close("exercise1:t-crit-9", t_two_sided_p(t_crit_9, 9), 0.05, tol=2e-4)
check_close("exercise1:mean", p_mean, 5.10)
check_close("exercise1:ss", sum((x - p_mean) ** 2 for x in parts), 0.60)
check_close("exercise1:s2", statistics.variance(parts), 0.60 / 9.0)
check_close("exercise1:s", p_s, 0.2582, tol=1e-4)
check_close("exercise1:se", p_se, 0.08165, tol=1e-4)
check_close("exercise1:ci-low", p_mean - t_crit_9 * p_se, 4.915, tol=1e-3)
check_close("exercise1:ci-high", p_mean + t_crit_9 * p_se, 5.285, tol=1e-3)
pi_margin = t_crit_9 * p_s * math.sqrt(1.0 + 1.0 / len(parts))
check_close("exercise4:pi-margin", pi_margin, 0.613, tol=1e-3)
check_close("exercise4:pi-low", p_mean - pi_margin, 4.487, tol=1e-3)
check_close("exercise4:pi-high", p_mean + pi_margin, 5.713, tol=1e-3)

check_item("z-ci-upper", 50.0 + 1.96 * (4.0 / math.sqrt(16)))
check_item("t-ci-margin", 2.064 * (10.0 / math.sqrt(25)))
check_item("pred-interval-margin", 2.064 * 10.0 * math.sqrt(1.0 + 1.0 / 25.0), tol=1e-5)

# Lesson 13: ci-large-mle
check_item("wald-prop-halfwidth", 1.96 * math.sqrt(0.5 * 0.5 / 100.0))
check_item("mle-asymp-ci-lower", 4.0 - 1.96 / math.sqrt(25.0))

# Lesson 14: ci-bootstrap
check_item("transform-ci-upper", math.exp(2.0), tol=1e-5)

# ── Chapter 6: 检验 ──────────────────────────────────────────────────
# Lesson 15: hypothesis-logic
p_coin_20_14 = 2.0 * sum(math.comb(20, k) for k in range(14, 21)) / (2 ** 20)
check_close("example:coin-20-14-twosided-p", p_coin_20_14, 0.1153, tol=5e-4)
check_item("two-sided-pvalue-calc", 2.0 * 0.025)

# Lesson 16: tests-normal-duality (including C4 exercise 2)
t_parts = (p_mean - 5.3) / p_se
check_close("exercise2:t-stat", t_parts, -2.4495, tol=1e-3)
check_close("exercise2:p-val", t_two_sided_p(t_parts, 9), 0.0368, tol=5e-4)
check_item("prop-z-test-calc", (0.62 - 0.5) / math.sqrt(0.5 * 0.5 / 100.0))
check_item("normal-z-known-sigma", (98.0 - 100.0) / (6.0 / math.sqrt(36)))

# Lesson 17: wald-and-multi
se_ab = math.sqrt(0.60 * 0.40 / 100.0 + 0.45 * 0.55 / 100.0)
w_ab = (0.60 - 0.45) / se_ab
check_close("example:ab-se", se_ab, 0.06982, tol=1e-4)
check_close("example:ab-wald", w_ab, 2.148, tol=1e-3)
check_close("example:ab-wald-sq", w_ab ** 2, 4.615, tol=2e-3)
check_item("wald-stat-num", (2.6 - 2.0) / 0.2)
check_item("wald-chisq-num", 3.0 ** 2)
check_item("wald-two-group-diff", 0.24 / math.hypot(0.06, 0.08))

# ── Boss challenge ───────────────────────────────────────────────────
check_item("b-order-stat", 1.0 - 0.5 ** 3)
check_item("b-mse-decomp", 16 + (-3) ** 2)
check_item("b-delta-se", abs(2 * 5) * 0.1)
check_item("b-bayes-beta", Fraction(6, 6 + 4))
check_item("b-mle-poisson", Fraction(2 + 5 + 3 + 6, 4))
check_item("b-fisher-ci-upper", 10.0 + 1.96 / math.sqrt(64.0))
check_close("boss:b-pvalue-wald-twosided", 2.0 * (1.0 - phi(2.5)), 0.0124, tol=2e-4)
check_item("b-wald-stat", (0.30 - 0.20) / math.sqrt(0.20 * 0.80 / 100.0))

missing = sorted(set(ANSWERS.keys()) - CHECKED_ITEMS)
assert not missing, f"Unverified number items in M.6.2.yaml: {missing}"

print(f"{CLAIMS}/{CLAIMS} claims hold ({len(CHECKED_ITEMS)}/{len(ANSWERS)} number items verified)")
