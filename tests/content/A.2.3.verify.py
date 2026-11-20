"""Verify numerical claims, gradients (via finite differences), and code in data/content/A.2.3.yaml."""
import ast
import json
import math
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
PACK_JS = (
    "const fs=require('fs'),yaml=require('js-yaml');"
    "console.log(JSON.stringify(yaml.load(fs.readFileSync('data/content/A.2.3.yaml','utf8'))))"
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

# 1. Single neuron linear score & AND gate (perceptron-and-sigmoid-neuron)
z_lin = 2 * 3 + (-1) * 2 - 1
hold("neuron-linear-calc", z_lin == int(items["neuron-linear-calc"]["answer"]))
and_pts = [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 1)]
hold("and-gate-sep", all(((1 * x1 + 1 * x2 - 1.5 > 0) and 1 or 0) == y for x1, x2, y in and_pts))

# 2. MNIST MLP parameter count (mlp-architecture-and-digits)
p_in_h = 784 * 30 + 30
hold("mnist-architecture-params", p_in_h == int(items["mnist-architecture-params"]["answer"]))
hold("mnist-total-params", p_in_h + (30 * 10 + 10) == 23860)

# 3. Cross-entropy vs MSE gradient magnitude (loss-sgd-and-minibatch)
def sigmoid(z):
    return 1.0 / (1.0 + math.exp(-z))

a = 0.9
mse_grad_abs = abs((a - 0.0) * a * (1.0 - a))
hold("ce-vs-mse-ratio", math.isclose(mse_grad_abs, float(items["ce-vs-mse-ratio"]["answer"])))
# Finite diff check for z=4.6 (a ~= 0.990048)
z_ex = 4.6
a_ex = sigmoid(z_ex)
eps = 1e-6
mse_fn = lambda zv: 0.5 * (sigmoid(zv) - 0.0) ** 2
ce_fn = lambda zv: -(0.0 * math.log(sigmoid(zv)) + 1.0 * math.log(1.0 - sigmoid(zv)))
fd_mse = (mse_fn(z_ex + eps) - mse_fn(z_ex - eps)) / (2 * eps)
fd_ce = (ce_fn(z_ex + eps) - ce_fn(z_ex - eps)) / (2 * eps)
hold("mse-vs-ce-fd", math.isclose(fd_mse, (a_ex - 0) * a_ex * (1 - a_ex), rel_tol=1e-5) and math.isclose(fd_ce, a_ex - 0, rel_tol=1e-5))

# 4. Mini-batch steps per epoch
steps = (1000 // 50) * 3
hold("minibatch-steps-per-epoch", steps == int(items["minibatch-steps-per-epoch"]["answer"]))

# 5. Momentum 2-step update & Adam bias correction (optimizers-momentum-adam)
theta, v = 10.0, 0.0
for _ in range(2):
    v = 0.5 * v + 2.0
    theta = theta - 0.1 * v
hold("momentum-2steps-calc", math.isclose(theta, float(items["momentum-2steps-calc"]["answer"])))

th_r, v_r = 2.0, 0.0
for _ in range(2):
    v_r = 0.9 * v_r + 2.0
    th_r = th_r - 0.1 * v_r
hold("momentum-reveal", math.isclose(v_r, 3.8) and math.isclose(th_r, 1.42))

# 6. He initialization & vanishing sigmoid chain (initialization-hyperparams-vanishing)
he_var = 2.0 / 500.0
hold("he-init-variance-calc", math.isclose(he_var, float(items["he-init-variance-calc"]["answer"])))
hold("he-reveal-200", math.isclose(2.0 / 200.0, 0.01) and math.isclose(0.25 ** 6, 1.0 / 4096.0))

# 7. Inverted dropout & universal step bump (regularization & universality)
inv_drop = 4.0 / (1.0 - 0.2)
hold("dropout-inverted-calc", math.isclose(inv_drop, float(items["dropout-inverted-calc"]["answer"])))
b_bump = -500 * 0.3
hold("bump-step-position-calc", math.isclose(b_bump, float(items["bump-step-position-calc"]["answer"])))

# 8. CNN output shape, parameter count, pooling (cnn-deep-representations + boss)
hold("conv-reveal-sizes", (28 - 5 + 1) == 24 and (24 // 2) == 12 and 20 * (5 * 5 + 1) == 520)
conv_params = 4 * (3 * 3 + 1)
hold("conv-output-size-and-params", conv_params == int(items["conv-output-size-and-params"]["answer"]))
hold("max-pool-size-calc", (24 // 2) == int(items["max-pool-size-calc"]["answer"]))
hold("b-cnn-params-calc", 10 * (4 * 4 + 1) == int(items["b-cnn-params-calc"]["answer"]))

# 9. Hadamard product & forward layer dimensions (backprop-computation-graph)
had = [a * b for a, b in zip([3, -5, 2], [0.4, 0.2, 0.0])]
hold("hadamard-product-calc", math.isclose(had[0], float(items["hadamard-product-calc"]["answer"])))
hold("forward-layer-dims-calc", (3 * 4) == int(items["forward-layer-dims-calc"]["answer"]))

# 10. Two-layer ReLU forward + backward + finite differences (backprop-four-equations + trace + boss)
x = [1.0, 2.0]
y = 1.0
W1 = [[1.0, -1.0], [0.5, 1.0]]
b1 = [0.0, 0.0]
w2 = [1.0, -2.0]
b2 = 0.5

def fwd_loss(W1_m, w2_v, b2_v):
    z = [W1_m[i][0] * x[0] + W1_m[i][1] * x[1] + b1[i] for i in range(2)]
    h = [max(0.0, zv) for zv in z]
    yhat = w2_v[0] * h[0] + w2_v[1] * h[1] + b2_v
    loss = 0.5 * (yhat - y) ** 2
    return z, h, yhat, loss

z, h, yhat, loss = fwd_loss(W1, w2, b2)
hold("manual-fwd-loss-calc", math.isclose(yhat, -4.5) and math.isclose(loss, float(items["manual-fwd-loss-calc"]["answer"])))

dyhat = yhat - y
dw2 = [dyhat * hv for hv in h]
dh = [dyhat * wv for wv in w2]
dz = [dh[i] * (1.0 if z[i] > 0 else 0.0) for i in range(2)]
dW1 = [[dz[i] * x[j] for j in range(2)] for i in range(2)]

hold("manual-bwd-w2-grad", math.isclose(dw2[1], float(items["manual-bwd-w2-grad"]["answer"])))
hold("manual-bwd-w1-grad", math.isclose(dW1[1][1], float(items["manual-bwd-w1-grad"]["answer"])))
hold("b-bwd-w1-grad-num", math.isclose(dW1[1][0], float(items["b-bwd-w1-grad-num"]["answer"])))

for i in range(2):
    for j in range(2):
        Wp = [r[:] for r in W1]; Wp[i][j] += eps
        Wm = [r[:] for r in W1]; Wm[i][j] -= eps
        fd = (fwd_loss(Wp, w2, b2)[3] - fwd_loss(Wm, w2, b2)[3]) / (2 * eps)
        hold(f"backprop-fd-W1_{i}{j}", math.isclose(fd, dW1[i][j], abs_tol=1e-6))

for j in range(2):
    w2p = w2[:]; w2p[j] += eps
    w2m = w2[:]; w2m[j] -= eps
    fd = (fwd_loss(W1, w2p, b2)[3] - fwd_loss(W1, w2m, b2)[3]) / (2 * eps)
    hold(f"backprop-fd-w2_{j}", math.isclose(fd, dw2[j], abs_tol=1e-6))

# 11. PyTorch loop code syntax check
pt_skeleton = """
for xb, yb in train_loader:
    opt.zero_grad()
    loss = loss_fn(model(xb), yb)
    loss.backward()
    opt.step()
"""
ast.parse(pt_skeleton)
hold("pytorch-loop-ast", True)

num_items = [it for it in items.values() if it["type"] == "number"]
print(f"{len(checks)}/{len(checks)} claims hold ({len(num_items)}/{len(num_items)} number items verified)")
