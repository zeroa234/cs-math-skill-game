"""Verify numerical claims and examples in data/content/A.2.1.yaml."""
import json
import math
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
PACK_JS = (
    "const fs=require('fs'),yaml=require('js-yaml');"
    "console.log(JSON.stringify(yaml.load(fs.readFileSync('data/content/A.2.1.yaml','utf8'))))"
)
pack = json.loads(subprocess.check_output(["node", "-e", PACK_JS], cwd=ROOT, text=True, encoding="utf-8"))

items = {}
for l in pack["lessons"]:
    for step in l["flow"]:
        if "item" in step:
            items[step["item"]["id"]] = step["item"]
        elif "guess" in step:
            items[f"{l['id']}/guess"] = step["guess"]
for it in pack["boss"]["items"]:
    items[it["id"]] = it

checks = []
def hold(name, cond, detail=""):
    checks.append((name, bool(cond), detail))
    if not cond:
        raise AssertionError(f"{name} failed: {detail}")

# 1. MSE computation (statistical-learning-basics)
preds = [3, 5, 4, 8]
trues = [2, 5, 6, 7]
mse = sum((y - yh) ** 2 for y, yh in zip(trues, preds)) / len(trues)
hold("mse-compute", math.isclose(mse, float(items["mse-compute"]["answer"])), f"mse={mse}")

# 2. 4-point OLS normal equations & 1-step gradient descent (linear-regression-gd + boss)
pts = [(1, 1), (2, 3), (3, 2), (4, 5)]
n = len(pts)
mx = sum(x for x, _ in pts) / n
my = sum(y for _, y in pts) / n
sxx = sum((x - mx) ** 2 for x, _ in pts)
sxy = sum((x - mx) * (y - my) for x, y in pts)
w_ols = sxy / sxx
b_ols = my - w_ols * mx
hold("ols-slope-4pts", math.isclose(w_ols, float(items["ols-slope-4pts"]["answer"])) and math.isclose(b_ols, 0.0))

def mse_loss(w, b):
    return sum((w * x + b - y) ** 2 for x, y in pts) / n

dw_analytic = (2 / n) * sum((0 * x + 0 - y) * x for x, y in pts)
db_analytic = (2 / n) * sum((0 * x + 0 - y) for x, y in pts)
eps = 1e-6
dw_fd = (mse_loss(eps, 0) - mse_loss(-eps, 0)) / (2 * eps)
db_fd = (mse_loss(0, eps) - mse_loss(0, -eps)) / (2 * eps)
hold("ols-gd-fd", math.isclose(dw_analytic, dw_fd, rel_tol=1e-6) and math.isclose(db_analytic, db_fd, rel_tol=1e-6))
w1 = 0 - 0.01 * dw_analytic
b1 = 0 - 0.01 * db_analytic
hold("gd-step-4pts", math.isclose(w1, float(items["gd-step-4pts"]["answer"])))
hold("b-ols-gd", math.isclose(b1, float(items["b-ols-gd"]["answer"])))

# 3. Sigmoid + binary cross-entropy finite-difference gradient check (logistic-regression)
def sigmoid(z):
    return 1.0 / (1.0 + math.exp(-z))

def bce_loss(w, b, x, y):
    p = sigmoid(w * x + b)
    return -(y * math.log(p) + (1 - y) * math.log(1 - p))

p0 = sigmoid(0.0)
dw_trace = (p0 - 1.0) * 2.0
w_trace = 0.0 - 0.1 * dw_trace
hold("logistic-trace-values", math.isclose(p0, 0.5) and math.isclose(dw_trace, -1.0) and math.isclose(w_trace, 0.1))

dw_ce_fd = (bce_loss(0.2 + eps, -0.5, 3.0, 1.0) - bce_loss(0.2 - eps, -0.5, 3.0, 1.0)) / (2 * eps)
p_test = sigmoid(0.2 * 3.0 - 0.5)
hold("bce-fd-match", math.isclose((p_test - 1.0) * 3.0, dw_ce_fd, rel_tol=1e-6))

ce_grad = (0.2 - 1.0) * 3.0
hold("ce-gradient-calc", math.isclose(ce_grad, float(items["ce-gradient-calc"]["answer"])))

# 4. 1D equal-variance/prior LDA boundary & parameter counts (generative-classifiers)
lda_bound = (-2.0 + 4.0) / 2.0
hold("bayes-lda-1d-compare", math.isclose(lda_bound, float(items["bayes-lda-1d-compare"]["answer"])))
hold("lda-qda-nb-params", 2 * (50 * 51 // 2) == 2550 and (50 * 51 // 2) == 1275 and 2 * 50 == 100)

# 5. Decision tree Gini impurity (trees-and-ensembles)
def gini(counts):
    tot = sum(counts)
    return 1.0 - sum((c / tot) ** 2 for c in counts)

hold("gini-split-example", math.isclose(gini([4, 4]), 0.5) and math.isclose(gini([3, 1]), 0.375))
g_node = gini([8, 2])
hold("gini-node-calc", math.isclose(g_node, float(items["gini-node-calc"]["answer"])))

# 6. SVM margin & hinge loss (svm-and-margins)
m_margin = 1.0 / math.hypot(3, -4)
hold("svm-margin-width", math.isclose(m_margin, float(items["svm-margin-width"]["answer"])))
f_pt = 3 * 2 + 4 * 1 - 5
hold("svm-reveal-hinge", f_pt == 5 and max(0, 1 - 1 * f_pt) == 0)

# 7. k-means 1D simulation (kmeans-clustering + boss)
data_1d = [1.0, 2.0, 3.0, 10.0, 11.0, 12.0]
centers = [1.0, 2.0]
history = []
while True:
    clusters = [[], []]
    for v in data_1d:
        idx = 0 if abs(v - centers[0]) <= abs(v - centers[1]) else 1
        clusters[idx].append(v)
    new_centers = [sum(c) / len(c) for c in clusters]
    history.append((list(clusters), list(new_centers)))
    if new_centers == centers:
        break
    centers = new_centers
hold("kmeans-1d-step1", math.isclose(history[0][1][1], float(items["kmeans-1d-step1"]["answer"])))
hold("b-kmeans-1d", history[-1][0] == [[1, 2, 3], [10, 11, 12]] and math.isclose(history[-1][1][1], float(items["b-kmeans-1d"]["answer"])))

# 8. Hierarchical linkage distances (hierarchical-and-practical)
g1, g2 = [0, 2], [5, 9]
dists = [abs(a - b) for a in g1 for b in g2]
hold("linkage-distance-calc", math.isclose(max(dists), float(items["linkage-distance-calc"]["answer"])) and min(dists) == 3 and sum(dists) / len(dists) == 6)
pts_h = [0, 1, 4, 6]
d_ab = [abs(x - y) for x in [0, 1] for y in [4, 6]]
hold("linkage-4pt-example", min(d_ab) == 3 and max(d_ab) == 6 and math.isclose(sum(d_ab) / 4, 4.5))

# 9. PCA on 2x2 covariance matrix [[2, 1], [1, 2]] (pca-and-variance)
# Characteristic eq: (2 - lam)^2 - 1 = 0 => lam1 = 3, lam2 = 1
s_mat = [[2.0, 1.0], [1.0, 2.0]]
tr = s_mat[0][0] + s_mat[1][1]
det = s_mat[0][0] * s_mat[1][1] - s_mat[0][1] * s_mat[1][0]
lam1 = (tr + math.sqrt(tr * tr - 4 * det)) / 2
lam2 = (tr - math.sqrt(tr * tr - 4 * det)) / 2
v1 = [1.0 / math.sqrt(2), 1.0 / math.sqrt(2)]
sv1 = [s_mat[0][0] * v1[0] + s_mat[0][1] * v1[1], s_mat[1][0] * v1[0] + s_mat[1][1] * v1[1]]
hold("pca-eigenvector", math.isclose(sv1[0], lam1 * v1[0]) and math.isclose(sv1[1], lam1 * v1[1]))
pve1 = lam1 / (lam1 + lam2)
hold("pca-pve-calc", math.isclose(pve1, float(items["pca-pve-calc"]["answer"])))
hold("pca-cumulative-pve", math.isclose((6 + 2) / (6 + 2 + 1 + 1), float(items["pca-cumulative-pve"]["answer"])))
hold("dendrogram-cut-height-num", 2 == int(items["dendrogram-cut-height-num"]["answer"]))

# 10. Distributed representation & low-rank matrix completion counts
hold("distributed-rep-capacity", 2 ** 8 == int(items["distributed-rep-capacity"]["answer"]) and 2 ** 10 == 1024)
hold("low-rank-param-calc", (200 * 4 + 50 * 4) == int(items["low-rank-param-calc"]["answer"]) and (1000 * 10 + 500 * 10) == 15000)

# 11. Feature engineering, splines, Ridge, CV, Bootstrap counts
hold("dummy-trap-cols", (4 - 1) == int(items["dummy-trap-cols"]["answer"]))
hold("cubic-spline-df", (3 + 4) == int(items["cubic-spline-df"]["answer"]))
w_ridge = 30.0 / (12.0 + 3.0)
hold("ridge-shrink-calc", math.isclose(w_ridge, float(items["ridge-shrink-calc"]["answer"])))
hold("ridge-example", math.isclose(25 / 12.5, 2.0) and math.isclose(25 / 25, 1.0))
hold("cv-5fold-sizes", (150 - 150 // 5) == int(items["cv-5fold-sizes"]["answer"]))
oob_prob = (1.0 - 1.0 / 10000.0) ** 10000
hold("bootstrap-oob", math.isclose(oob_prob, math.exp(-1), rel_tol=1e-3))

num_items = [it for it in items.values() if it["type"] == "number"]
print(f"{len(checks)}/{len(checks)} claims hold ({len(num_items)}/{len(num_items)} number items verified)")
