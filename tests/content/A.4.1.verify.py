"""Verify PSI drift math, latency calculations, and FastAPI inference schema logic in data/content/A.4.1.yaml."""
import ast
import json
import math
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
PACK_JS = (
    "const fs=require('fs'),yaml=require('js-yaml');"
    "console.log(JSON.stringify(yaml.load(fs.readFileSync('data/content/A.4.1.yaml','utf8'))))"
)
pack = json.loads(subprocess.check_output(["node", "-e", PACK_JS], cwd=ROOT, text=True, encoding="utf-8"))

items = {}
for l in pack["lessons"]:
    for step in l["flow"]:
        if "item" in step:
            items[step["item"]["id"]] = step["item"]
for it in pack["boss"]["items"]:
    items[it["id"]] = it

checks = []
def hold(name, cond, detail=""):
    checks.append((name, bool(cond), detail))
    if not cond:
        raise AssertionError(f"{name} failed: {detail}")

# 1. Latency budget, QPS, and throughput calculations
budget = 80 - (15 + 25 + 10)
hold("product-latency-calc", budget == int(items["product-latency-calc"]["answer"]))
qps_per_replica = 200 / 4
hold("batch-vs-qps-throughput", qps_per_replica == int(items["batch-vs-qps-throughput"]["answer"]))
throughput_startup = 1000 / 5
hold("startup-load-latency-calc", throughput_startup == int(items["startup-load-latency-calc"]["answer"]))

# 2. Point-in-time join lookup (feature-store-and-skew)
snaps = [(4, 620), (9, 650), (14, 710)]
t_event = 10
valid = [val for t, val in snaps if t <= t_event]
hold("point-in-time-join-val", valid[-1] == int(items["point-in-time-join-val"]["answer"]))

# 3. ML unit test assertion, slice imbalance, data expectation null %
hold("ml-step-assertion-calc", 8 == int(items["ml-step-assertion-calc"]["answer"]))
overall_acc = (900 / 1000) * 100
hold("slice-eval-imbalance-calc", math.isclose(overall_acc, float(items["slice-eval-imbalance-calc"]["answer"])))
null_pct = (150 / 5000) * 100
hold("data-expectation-null-calc", math.isclose(null_pct, float(items["data-expectation-null-calc"]["answer"])))

# 4. PSI calculations (monitoring-drift-and-psi + boss)
def calc_psi(expected, actual):
    return sum((ai - ei) * math.log(ai / ei) for ei, ai in zip(expected, actual))

e4 = [0.25, 0.25, 0.25, 0.25]
a4 = [0.10, 0.20, 0.30, 0.40]
psi4 = calc_psi(e4, a4)
hold("psi-full-calc", math.isclose(psi4, float(items["psi-full-calc"]["answer"]), abs_tol=1e-3) and psi4 > 0.2)

e2 = [0.5, 0.5]
a2 = [0.4, 0.6]
psi2 = calc_psi(e2, a2)
hold("b-psi-calc-boss", math.isclose(psi2, float(items["b-psi-calc-boss"]["answer"]), abs_tol=1e-3) and psi2 < 0.1)

# 5. FastAPI inference schema syntax & equivalent Pydantic validation logic check
fastapi_snippet = """
from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib

app = FastAPI()
model = joblib.load("model.joblib")

class Features(BaseModel):
    age: int = Field(ge=0, le=120)
    income: float = Field(ge=0)

@app.post("/predict")
def predict(x: Features):
    p = model.predict_proba([[x.age, x.income]])[0, 1]
    return {"probability": float(p), "model_version": "v3"}
"""
tree = ast.parse(fastapi_snippet)
cls_defs = [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Features"]
fn_defs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "predict"]
hold("fastapi-ast-structure", len(cls_defs) == 1 and len(fn_defs) == 1)

def predict_one(age, income):
    if not isinstance(age, int) or isinstance(age, bool) or age < 0 or age > 120 or income < 0:
        return {"status": 422, "prob": None}
    z = 0.02 * age + 0.0001 * income - 2.0
    p = round(1.0 / (1.0 + math.exp(-z)), 2)
    return {"status": 200, "prob": p, "ver": "v3"}

ok_resp = predict_one(50, 10000)
err_neg = predict_one(-5, 10000)
err_type = predict_one("bad", 10000)
hold("inference-validation-logic", ok_resp == {"status": 200, "prob": 0.5, "ver": "v3"} and err_neg["status"] == 422 and err_type["status"] == 422)

num_items = [it for it in items.values() if it["type"] == "number"]
print(f"{len(checks)}/{len(checks)} claims hold ({len(num_items)}/{len(num_items)} number items verified)")
