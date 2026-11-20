"""Verify every numerical claim, worked example, and number-item answer in data/content/M.6.2.2.yaml.

Uses only the Python standard library (fractions, math, statistics) plus Node's js-yaml
to read data/content/M.6.2.2.yaml so it runs cleanly under `python -I`.
"""
from __future__ import annotations

import json
import math
import statistics
import subprocess
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK_PATH = ROOT / "data" / "content" / "M.6.2.2.yaml"

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
    assert item_id in ANSWERS, f"missing number item {item_id!r} in M.6.2.2.yaml"
    CHECKED_ITEMS.add(item_id)
    check_close(f"item:{item_id}", ANSWERS[item_id], expected, tol=tol)


# ── Chapter 1: 线性/广义线性模型 ───────────────────────────────────────
# Lesson 1: simple-linear-regression (C4 exercise 1 & 4)
xs = [1, 2, 3, 4, 5]
ys = [2, 3, 5, 4, 6]
mx, my = Fraction(sum(xs), len(xs)), Fraction(sum(ys), len(ys))
sxx = sum((x - mx) ** 2 for x in xs)
sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
sst = sum((y - my) ** 2 for y in ys)
b1 = sxy / sxx
b0 = my - b1 * mx
resids = [y - (b0 + b1 * x) for x, y in zip(xs, ys)]
sse = sum(r ** 2 for r in resids)
check_close("ex1:mx", mx, 3)
check_close("ex1:my", my, 4)
check_close("ex1:sxx", sxx, 10)
check_close("ex1:sxy", sxy, 9)
check_close("ex1:sst", sst, 10)
check_close("ex1:b1", b1, Fraction(9, 10))
check_close("ex1:b0", b0, Fraction(13, 10))
check_close("ex1:sse", sse, Fraction(19, 10))
check_close("ex1:r2", 1 - sse / sst, Fraction(81, 100))
check_item("slr-predict-calc", b0 + b1 * 6)
check_item("slr-r2-calc", 1 - Fraction(12, 50))
check_item("slr-error-var", Fraction(45, 12 - 2))

# Lesson 2: multiple-regression-matrix (C4 exercise 2)
xtx = [[len(xs), sum(xs)], [sum(xs), sum(x * x for x in xs)]]
xty = [sum(ys), sum(x * y for x, y in zip(xs, ys))]
check_close("ex2:xtx00", xtx[0][0], 5)
check_close("ex2:xtx01", xtx[0][1], 15)
check_close("ex2:xtx11", xtx[1][1], 55)
check_close("ex2:xty0", xty[0], 20)
check_close("ex2:xty1", xty[1], 69)
# 5*b0 + 15*b1 = 20, 15*b0 + 55*b1 = 69
check_close("ex2:eq1", 5 * b0 + 15 * b1, 20)
check_close("ex2:eq2", 15 * b0 + 55 * b1, 69)
check_item("design-matrix-shape", 3 + 1)
check_item("normal-eq-solve", Fraction(35, 10))

# Lesson 3: categorical-and-interactions
check_item("dummy-count-rule", 4 - 1)
check_item("interaction-slope-calc", 4 + 3)

# Lesson 4: transforms-and-nonlinear
check_item("semilog-multiplier", math.exp(0.1), tol=1e-5)
check_item("loglog-power-ratio", 2.0 ** (-0.8), tol=1e-5)

# Lesson 5: logistic-poisson-glm
check_close("example:logistic-x4", 1.0 / (1.0 + math.exp(-(-2.0 + 0.5 * 4.0))), 0.5)
check_item("logistic-prob-calc", 1.0 / (1.0 + math.exp(-(-1.0 + 0.5 * 4.0))), tol=1e-5)
check_item("logistic-odds-ratio", math.exp(0.5 * 2.0), tol=1e-5)
check_item("poisson-expected-count", math.exp(1.0 + 0.2 * 5.0), tol=1e-5)

# ── Chapter 2: 残差诊断与不确定性 ─────────────────────────────────────
# Lesson 6: regression-inference-anova
check_item("coef-t-stat", Fraction(24, 10) / Fraction(8, 10))
check_item("anova-f-calc", Fraction(80, 1) / Fraction(160, 22 - 2))
check_close("example:gen-lin-f", ((140 - 105) / (23 - 21)) / (105 / 21), 3.5)
check_close("example:partial-r2", Fraction(140 - 105, 140), Fraction(1, 4))
check_item("partial-r2-calc", Fraction(200 - 150, 200))

# Lesson 7: residual-diagnostics
r_given = [Fraction(4, 10), Fraction(-7, 10), Fraction(5, 10), Fraction(-6, 10)]
check_item("residual-sum-zero", -sum(r_given))

# Lesson 8: confidence-and-prediction
check_close("example:slr-ci-center", 2.306 * 2.0 * math.sqrt(1.0 / 10.0), 1.458, tol=1e-3)
check_close("example:slr-pi-center", 2.306 * 2.0 * math.sqrt(1.0 + 1.0 / 10.0), 4.837, tol=1e-3)
check_close("example:slr-ci-far", 2.306 * 2.0 * math.sqrt(1.0 / 10.0 + ((9.0 - 5.0) ** 2) / 40.0), 3.261, tol=1e-3)
check_item("slr-ci-at-mean", 2.069 * 5.0 * math.sqrt(1.0 / 25.0))
check_item("slr-pi-at-mean", 2.069 * 5.0 * math.sqrt(1.0 + 1.0 / 25.0), tol=1e-5)

# Lesson 9: influential-and-pitfalls
check_item("hat-trace-sum", 3 + 1)
check_item("vif-calc", 1 / (1 - Fraction(8, 10)))

# ── Chapter 3: 正则化 ────────────────────────────────────────────────
# Lesson 10: subset-and-model-selection
check_item("adj-r2-calc", 1 - (Fraction(32, 21 - 4 - 1) / Fraction(100, 21 - 1)))
check_close("aic-vs-bic:ln200", math.log(200), 5.2983, tol=1e-3)

# Lesson 11: ridge-and-lasso
check_close("example:ridge-1d", Fraction(18, 6 + 3), 2)
check_item("ridge-1d-calc", Fraction(20, 8 + 2))

# ── Boss challenge ───────────────────────────────────────────────────
b_xs = [1, 2, 3, 4]
b_ys = [1, 4, 4, 7]
b_mx = Fraction(sum(b_xs), len(b_xs))
b_my = Fraction(sum(b_ys), len(b_ys))
b_sxx = sum((x - b_mx) ** 2 for x in b_xs)
b_sxy = sum((x - b_mx) * (y - b_my) for x, y in zip(b_xs, b_ys))
check_item("b-ols-slope", b_sxy / b_sxx)
check_item("b-logistic-prob", 1.0 / (1.0 + math.exp(-(-1.0 + 1.5 * 2.0))), tol=1e-5)
check_item("b-partial-r2", Fraction(100 - 60, 100))
check_item("b-vif-calc", 1 / (1 - Fraction(75, 100)))
check_item("b-ridge-1d", Fraction(15, 5 + 5))

missing = sorted(set(ANSWERS.keys()) - CHECKED_ITEMS)
assert not missing, f"Unverified number items in M.6.2.2.yaml: {missing}"

print(f"{CLAIMS}/{CLAIMS} claims hold ({len(CHECKED_ITEMS)}/{len(ANSWERS)} number items verified)")
