"""Verify every numerical claim, worked example, and number-item answer in data/content/M.6.1.yaml.

Uses only the Python standard library (fractions, math, itertools) plus Node's js-yaml
to read data/content/M.6.1.yaml so it runs cleanly under `python3 -I`.
"""
from __future__ import annotations

import itertools
import json
import math
import subprocess
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK_PATH = ROOT / "data" / "content" / "M.6.1.yaml"

# Load the YAML pack via Node's already-installed js-yaml to keep stdlib-only Python
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
    text=True,
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
    assert item_id in ANSWERS, f"missing number item {item_id!r} in M.6.1.yaml"
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


# ── Chapter 1: 概率空间 ──────────────────────────────────────────────
# Lesson 1: sample-space
coins = list(itertools.product(["H", "T"], repeat=2))
check_item("two-coins-at-least-one-head", Fraction(sum("H" in c for c in coins), len(coins)))
check_item("inclusion-exclusion-num", Fraction(45, 100) + Fraction(35, 100) - Fraction(15, 100))
check_item("complement-neither-num", 1 - Fraction(82, 100))

# Lesson 2: counting-prob
dice2 = list(itertools.product(range(1, 7), repeat=2))
check_close("example:dice-sum-7", Fraction(sum(a + b == 7 for a, b in dice2), len(dice2)), Fraction(1, 6))
check_item("two-dice-sum-8", Fraction(sum(a + b == 8 for a, b in dice2), len(dice2)))
check_item("draw-two-red-balls", Fraction(math.comb(3, 2), math.comb(5, 2)))

# Birthday problem worked example (n = 23)
p_diff_23 = Fraction(1, 1)
for k in range(23):
    p_diff_23 *= Fraction(365 - k, 365)
check_close("example:birthday-23", 1 - float(p_diff_23), 0.507297, tol=1e-5)

# Birthday season item (3 people, 4 seasons)
p_all_diff_seasons = Fraction(4 * 3 * 2, 4 ** 3)
check_item("birthday-season-comp", 1 - p_all_diff_seasons)

# Geometric probability
check_item("geom-prob-interval", Fraction(55 - 20, 100))
check_close("example:meeting-prob", 1 - Fraction(45 * 45, 60 * 60), Fraction(7, 16))
check_close("example:buffon-needle", 2.0 / math.pi, 0.63661977, tol=1e-5)

# Lesson 3: continuity-measure
# P(intersection B_n) = lim (5/6)^n = 0
check_item("forever-tails-prob", 0.0)
# Integral of spike f_n(x) = 2n on (0, 1/n) is 2 for every n
for n in (1, 10, 1000):
    check_close(f"spike-integral-n={n}", (2 * n) * (1 / n), 2.0)
check_item("spike-integral-value", 2.0)

# ── Chapter 2: 条件概率 ──────────────────────────────────────────────
# Lesson 4: cond-prob
first_6 = [pair for pair in dice2 if pair[0] == 6]
check_item("cond-dice-first-is-six", Fraction(sum(a + b == 7 for a, b in first_6), len(first_6)))
# Original exercise 1: at least one 6 -> sum == 7
at_least_one_6 = [pair for pair in dice2 if 6 in pair]
check_close("exercise1:two-dice-at-least-6", Fraction(sum(a + b == 7 for a, b in at_least_one_6), len(at_least_one_6)), Fraction(2, 11))
check_item("mult-rule-draw-without-replace", Fraction(4, 10) * Fraction(3, 9))
check_item("continuous-cond-uniform", Fraction(9 - 3, 12 - 3))

# Lesson 5: bayes-paradox
# Original exercise 2: prevalence 1%, sensitivity 95%, specificity 90%
p_pos_ex2 = Fraction(1, 100) * Fraction(95, 100) + Fraction(99, 100) * Fraction(10, 100)
p_dis_given_pos_ex2 = (Fraction(1, 100) * Fraction(95, 100)) / p_pos_ex2
check_close("exercise2:total-pos", p_pos_ex2, Fraction(1085, 10000))
check_close("exercise2:posterior", p_dis_given_pos_ex2, Fraction(95, 1085))
check_close("exercise2:posterior-pct", float(p_dis_given_pos_ex2), 0.0875576, tol=1e-5)

p_def = Fraction(60, 100) * Fraction(2, 100) + Fraction(40, 100) * Fraction(5, 100)
check_item("total-prob-factory", p_def)
check_item("bayes-factory-posterior", (Fraction(40, 100) * Fraction(5, 100)) / p_def)

p_pos_2 = Fraction(2, 100) * Fraction(90, 100) + Fraction(98, 100) * Fraction(5, 100)
check_item("bayes-medical-second", (Fraction(2, 100) * Fraction(90, 100)) / p_pos_2)

# Lesson 6: cond-expectation
check_item("cond-exp-dice-coins", Fraction(4, 2))
check_close("example:dice-then-coins-EY", sum(Fraction(1, 6) * Fraction(k, 2) for k in range(1, 7)), Fraction(7, 4))
check_item("tower-two-box-avg", Fraction(1, 2) * 12 + Fraction(1, 2) * 28)
check_item("tower-weighted-stages", Fraction(30, 100) * 40 + Fraction(70, 100) * 100)

# ── Chapter 3: 随机变量 ──────────────────────────────────────────────
# Lesson 7: rv-discrete-cdf
check_item("pmf-normalize-c", Fraction(1, 1 + 2 + 3))
check_item("pmf-interval-sum", Fraction(3, 10) + Fraction(4, 10))
check_item("cdf-from-pmf-val", Fraction(20, 100) + Fraction(35, 100))
check_item("cdf-interval-diff", Fraction(85, 100) - Fraction(35, 100))

# Lesson 8: rv-continuous-transform
check_close("example:tri-pdf-int", simpson(lambda x: 0.5 * x, 0.0, 2.0), 1.0, tol=1e-9)
check_close("example:tri-pdf-0-1", simpson(lambda x: 0.5 * x, 0.0, 1.0), 0.25, tol=1e-9)
check_item("pdf-normalize-quad", 1.0 / simpson(lambda x: x * x, 0.0, 1.0))
check_item("pdf-interval-prob", simpson(lambda x: 3.0 * x * x, 0.5, 1.0))
# F(x) = x^2 / 4 => f(1.6) = 1.6 / 2 = 0.8
check_item("pdf-from-cdf-deriv", 1.6 / 2.0)
# Y = X^2, X ~ U[0,1] => P(Y <= 0.25) = P(X <= 0.5) = 0.5
check_item("transform-square-prob", math.sqrt(0.25))
# Y = 4X + 2, X ~ U[0,1] => f_Y(y) = 1/4
check_item("transform-linear-density", Fraction(1, 4))

# ── Chapter 4: 分布 ──────────────────────────────────────────────────
# Lesson 9: discrete-dist
check_item("binom-free-throw", math.comb(3, 2) * (Fraction(1, 2) ** 3))
check_item("geom-third-try", Fraction(5, 6) * Fraction(1, 6))
check_item("poisson-zero-prob", math.exp(-3.0))
# Worked example: Binomial(100, 0.02) vs Poisson(2) at k = 0, 1, 2
for k in (0, 1, 2):
    b_val = math.comb(100, k) * (0.02 ** k) * (0.98 ** (100 - k))
    p_val = math.exp(-2.0) * (2.0 ** k) / math.factorial(k)
    check_close(f"example:binom-pois-k={k}", b_val, p_val, tol=0.005)

# Lesson 10: continuous-dist (includes Original exercise 3: X ~ Exp(2))
check_item("exp-survival-prob", math.exp(-2.0 * 1.0))
check_item("exp-interval-cdf", 1.0 - math.exp(-0.5 * 2.0))
# Memoryless: P(X > 3 | X > 2) = P(X > 3) / P(X > 2) = e^-6 / e^-4 = e^-2
check_item("exp-memoryless-cond", math.exp(-6.0) / math.exp(-4.0))

# Lesson 11: normal-joint
check_close("example:normal-1sigma", phi(1.0) - phi(-1.0), 0.682689, tol=1e-4)
check_close("example:normal-2sigma", phi(2.0) - phi(-2.0), 0.954499, tol=1e-4)
check_close("example:normal-3sigma", phi(3.0) - phi(-3.0), 0.997300, tol=1e-4)
check_item("normal-z-score", Fraction(130 - 100, 15))
check_item("normal-symmetry-tail", 1.0 - phi(1.9), tol=1e-4)
check_item("marginal-from-joint-table", Fraction(1, 10) + Fraction(3, 10))
check_item("sum-two-indep-normals", math.hypot(3.0, 4.0))

# Lesson 12: mgf-transforms
check_item("mgf-at-zero", 1.0)
# M(t) = exp(3t + 2t^2) => M'(0) = 3
check_item("mgf-deriv-first-moment", 3.0)
check_item("mgf-sum-poisson-param", 2 + 5)
# X ~ Exp(2): M(t) = 2 / (2 - t), M''(t) = 4 / (2 - t)^3 => M''(0) = 4 / 8 = 0.5
check_item("mgf-second-moment-exp", Fraction(4, 8))

# ── Chapter 5: 期望与极限定理 ────────────────────────────────────────
# Lesson 13: expectation-variance
check_item("exp-discrete-calc", Fraction(2, 10) * 0 + Fraction(5, 10) * 2 + Fraction(3, 10) * 5)
# Original exercise 3: E[Exp(2)] = 1/2, Var(Exp(2)) = 1/4
ex_exp2 = simpson(lambda x: x * 2.0 * math.exp(-2.0 * x), 0.0, 20.0, n=4000)
ex2_exp2 = simpson(lambda x: x * x * 2.0 * math.exp(-2.0 * x), 0.0, 20.0, n=4000)
check_close("exercise3:exp2-mean-integral", ex_exp2, 0.5, tol=1e-6)
check_close("exercise3:exp2-var-integral", ex2_exp2 - ex_exp2 ** 2, 0.25, tol=1e-6)
check_item("exp-exponential-mean", Fraction(1, 2))
check_item("var-shortcut-discrete", Fraction((-1) ** 2 + 0 ** 2 + 1 ** 2, 3))
check_item("var-linear-scale", 3 ** 2 * 4)

# Lesson 14: inequalities-lln
check_item("markov-bound-num", Fraction(15, 60))
check_item("chebyshev-bound-num", Fraction(16, 12 ** 2))
check_item("sample-mean-var-scale", math.sqrt(100.0 / 25.0))

# Lesson 15: clt-normal-approx (includes Original exercise 4: 100 coins, P(S >= 60))
check_item("clt-standardize-mean-sd", math.sqrt(400 * 0.5 * 0.5))
z_cc = (60.0 - 0.5 - 50.0) / 5.0
check_item("clt-cont-corr-z", z_cc)
clt_cc_prob = 1.0 - phi(z_cc)
exact_binom_ge_60 = sum(math.comb(100, k) for k in range(60, 101)) / (2 ** 100)
clt_no_cc_prob = 1.0 - phi((60.0 - 50.0) / 5.0)
check_close("exercise4:clt-cc-prob", clt_cc_prob, 0.0287166, tol=1e-5)
check_close("exercise4:exact-binom-ge-60", exact_binom_ge_60, 0.02844397, tol=1e-5)
check_close("exercise4:clt-no-cc-prob", clt_no_cc_prob, 0.0227501, tol=1e-5)
assert abs(clt_cc_prob - exact_binom_ge_60) < abs(clt_no_cc_prob - exact_binom_ge_60) / 10.0

check_item("clt-continuous-sample-mean", (11.0 - 10.0) / (3.0 / math.sqrt(36.0)))

# ── Boss challenge (8 number items) ──────────────────────────────────
check_item("b-inclusion", 1 - (Fraction(6, 10) + Fraction(5, 10) - Fraction(2, 10)))
sum_8 = [pair for pair in dice2 if sum(pair) == 8]
check_item("b-two-dice-cond", Fraction(sum(6 in pair for pair in sum_8), len(sum_8)))
p_pos_b = Fraction(5, 1000) * Fraction(98, 100) + Fraction(995, 1000) * Fraction(5, 100)
check_close("boss:bayes-total-pos", p_pos_b, Fraction(5465, 100000))
check_item("b-bayes-screen", (Fraction(5, 1000) * Fraction(98, 100)) / p_pos_b)
check_item("b-tower-expectation", Fraction(1, 2) * 8 + Fraction(1, 2) * 20)
check_item("b-pdf-integral", simpson(lambda x: 0.5 * x, 1.0, 2.0))
check_item("b-exp-memoryless", Fraction(1, 2 ** 2))
check_item("b-var-transform", 2 ** 2 * 2 + (-1) ** 2 * 3)
z_b = (214.5 - 400 * 0.5) / math.sqrt(400 * 0.5 * 0.5)
check_close("boss:clt-z", z_b, 1.45)
check_close("boss:phi-1.45", phi(1.45), 0.9265, tol=1e-4)
check_item("b-clt-approx", 1.0 - phi(z_b), tol=1e-4)
check_close("boss:exact-binom-ge-215", sum(math.comb(400, k) for k in range(215, 401)) / 2 ** 400, 0.0735, tol=1e-4)

# Ensure EVERY number item in M.6.1.yaml was verified!
missing = sorted(set(ANSWERS.keys()) - CHECKED_ITEMS)
assert not missing, f"Unverified number items in M.6.1.yaml: {missing}"

print(f"{CLAIMS}/{CLAIMS} claims hold ({len(CHECKED_ITEMS)}/{len(ANSWERS)} number items verified)")
