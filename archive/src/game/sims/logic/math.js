// Pure logic for the math / ML sims: plot (secant, riemann, taylor, limit), matrix2d, sampler,
// descent, neuron, mlp, kmeans. Same interface as logic/os.js.
import { fx, compile, derivative } from "../expr.js";

const ok = (correct, detail = {}) => ({ correct, detail });

// Seeded RNG (mulberry32) so sims and their checkers reproduce the same data and training runs.
export function rng(seed = 1) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const gauss = (r) => Math.sqrt(-2 * Math.log(1 - r())) * Math.cos(2 * Math.PI * r());

// ---------- plot ----------
// Composite Simpson with 2000 panels: the "exact" integral the Riemann mode compares against.
export function integrate(f, a, b, n = 2000) {
  const h = (b - a) / n;
  let s = f(a) + f(b);
  for (let i = 1; i < n; i++) s += f(a + i * h) * (i % 2 ? 4 : 2);
  return (s * h) / 3;
}
export function riemann(f, a, b, n, rule = "left") {
  const h = (b - a) / n;
  let s = 0;
  for (let i = 0; i < n; i++) s += f(a + (i + (rule === "left" ? 0 : rule === "right" ? 1 : 0.5)) * h);
  return s * h;
}
// Maclaurin series with known coefficients (numeric high-order derivatives are too noisy).
const SERIES = {
  exp: { f: Math.exp, c: (k) => 1 / fact(k) },
  sin: { f: Math.sin, c: (k) => (k % 2 ? ((k - 1) / 2) % 2 ? -1 / fact(k) : 1 / fact(k) : 0) },
  cos: { f: Math.cos, c: (k) => (k % 2 ? 0 : (k / 2) % 2 ? -1 / fact(k) : 1 / fact(k)) },
  ln1p: { f: (x) => Math.log(1 + x), c: (k) => (k === 0 ? 0 : (k % 2 ? 1 : -1) / k) },
};
function fact(k) { let r = 1; for (let i = 2; i <= k; i++) r *= i; return r; }
export const taylor = (name, order, x) => { let s = 0; for (let k = 0; k <= order; k++) s += SERIES[name].c(k) * x ** k; return s; };
export const seriesNames = Object.keys(SERIES);
export const seriesFn = (name) => SERIES[name].f;

export const plot = {
  name: "plot",
  validate(p, g) {
    if (!["secant", "riemann", "taylor", "limit"].includes(p.mode)) throw new Error("plot: mode");
    if (p.mode === "taylor") { if (!SERIES[p.series]) throw new Error(`plot: series must be one of ${seriesNames}`); }
    else fx(p.f)(p.a ?? 0.5);
    if (p.mode === "secant" && !g.slope) throw new Error("plot: secant goal needs slope {target, tol}");
    if (p.mode === "riemann" && !(g.errorBelow > 0)) throw new Error("plot: riemann goal needs errorBelow");
    if (p.mode === "taylor" && !(g.errorBelow > 0 && "at" in g)) throw new Error("plot: taylor goal needs errorBelow and at");
    if (p.mode === "limit" && !("value" in g)) throw new Error("plot: limit goal needs value");
  },
  initial: (p) => (p.mode === "secant" ? { h: p.hMax ?? 1 } : p.mode === "riemann" ? { n: 2 } : p.mode === "taylor" ? { order: 0 } : { guess: "" }),
  check(p, g, r) {
    if (p.mode === "secant") {
      const f = fx(p.f), h = Number(r?.h);
      if (!(Math.abs(h) > 0)) return ok(false);
      const slope = (f(p.a + h) - f(p.a)) / h;
      return ok(Math.abs(slope - g.slope.target) <= g.slope.tol, { slope });
    }
    if (p.mode === "riemann") {
      const f = fx(p.f), n = Math.round(Number(r?.n));
      if (!(n >= 1)) return ok(false);
      const approx = riemann(f, p.a, p.b, n, p.rule), exact = integrate(f, p.a, p.b);
      return ok(Math.abs(approx - exact) <= g.errorBelow, { approx, exact, n });
    }
    if (p.mode === "taylor") {
      const order = Math.round(Number(r?.order));
      const err = Math.abs(taylor(p.series, order, g.at) - SERIES[p.series].f(g.at));
      return ok(err <= g.errorBelow, { err, order });
    }
    const guess = Number(r?.guess);
    return ok(Math.abs(guess - g.value) <= (g.tol ?? 1e-6), { guess });
  },
};

// ---------- matrix2d ----------
const mul = (A, v) => [A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1]];
export const det = (A) => A[0][0] * A[1][1] - A[0][1] * A[1][0];
const close = (a, b, tol = 1e-6) => Math.abs(a - b) <= tol;
export const matrix2d = {
  name: "matrix2d",
  validate(p, g) {
    if (!g.matrix && !("det" in g) && !g.maps && !g.eigvec) throw new Error("matrix2d: goal needs matrix | det | maps | eigvec");
  },
  initial: (p) => p.start || [[1, 0], [0, 1]],
  check(p, g, A) {
    if (!Array.isArray(A) || A.length !== 2) return ok(false);
    const tol = g.tol ?? 1e-6;
    let good = true;
    if (g.matrix) good &&= A.every((row, i) => row.every((x, j) => close(x, g.matrix[i][j], tol)));
    if ("det" in g) good &&= close(det(A), g.det, tol);
    if (g.maps) good &&= g.maps.every(([from, to]) => mul(A, from).every((x, i) => close(x, to[i], tol)));
    if (g.eigvec) { const w = mul(A, g.eigvec); good &&= close(w[0] * g.eigvec[1] - w[1] * g.eigvec[0], 0, tol) && Math.hypot(...w) > tol; }
    return ok(good, { det: det(A) });
  },
};

// ---------- sampler: watch frequencies settle (law of large numbers) ----------
export function sample(dist, n, seed = 7) {
  const r = rng(seed);
  const draw = dist === "coin" ? () => (r() < 0.5 ? 1 : 0) : dist === "die" ? () => 1 + Math.floor(r() * 6) : () => 2 + Math.floor(r() * 6) + Math.floor(r() * 6);
  return Array.from({ length: n }, draw);
}
export const sampler = {
  name: "sampler",
  validate(p) { if (!["coin", "die", "twoDice"].includes(p.dist)) throw new Error("sampler: dist"); },
  initial: () => ({ n: 0 }),
  check: (p, g, r) => ok((r?.n || 0) >= (g.samples || 1)),
};

// ---------- descent: gradient descent with a chosen learning rate ----------
export function descend(p, lr, steps) {
  const vars = p.vars || ["x"];
  const f = compile(p.f);
  let x = [...(Array.isArray(p.x0) ? p.x0 : [p.x0])];
  const path = [x];
  const val = (pt) => f(Object.fromEntries(vars.map((v, i) => [v, pt[i]])));
  for (let k = 0; k < steps; k++) {
    const grad = vars.map((_, i) => derivative((t) => val(x.map((xj, j) => (j === i ? t : xj))))(x[i]));
    x = x.map((xi, i) => xi - lr * grad[i]);
    path.push(x);
    if (!x.every(Number.isFinite) || Math.max(...x.map(Math.abs)) > 1e6) return { path, diverged: true, x };
  }
  return { path, diverged: false, x, value: val(x) };
}
export const descent = {
  name: "descent",
  validate(p, g) { compile(p.f); if (!("target" in g) || !(g.tol > 0)) throw new Error("descent: goal needs target and tol"); },
  initial: (p) => ({ lr: p.lr ?? 0.1, steps: 0 }),
  check(p, g, r) {
    const steps = Math.round(Number(r?.steps)), lr = Number(r?.lr);
    if (!(steps >= 0 && lr > 0)) return ok(false);
    if (g.maxSteps && steps > g.maxSteps) return ok(false, { tooMany: true });
    const res = descend(p, lr, steps);
    const target = Array.isArray(g.target) ? g.target : [g.target];
    const dist = Math.hypot(...res.x.map((xi, i) => xi - target[i]));
    return ok(!res.diverged && dist <= g.tol, { ...res, dist });
  },
};

// ---------- datasets for neuron / mlp / kmeans ----------
export const LOGIC = {
  and: [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]],
  or: [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]],
  nand: [[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 0]],
  xor: [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]],
};
export function dataset(name, n = 160, seed = 3) {
  const r = rng(seed);
  const pts = [];
  for (let i = 0; i < n; i++) {
    if (name === "circle") { const rad = i % 2 ? 0.25 + 0.2 * r() : 0.65 + 0.25 * r(); const a = 2 * Math.PI * r(); pts.push([rad * Math.cos(a), rad * Math.sin(a), i % 2 ? 1 : 0]); }
    else if (name === "xor") { const x = r() * 2 - 1, y = r() * 2 - 1; pts.push([x, y, x * y > 0 ? 1 : 0]); }
    else if (name === "linear") { const x = r() * 2 - 1, y = r() * 2 - 1; pts.push([x, y, x + 0.5 * y > 0.1 ? 1 : 0]); }
    else if (name === "blobs3") { const c = [[-0.5, -0.4], [0.5, -0.3], [0, 0.55]][i % 3]; pts.push([c[0] + 0.15 * gauss(r), c[1] + 0.15 * gauss(r), i % 3]); }
    else throw new Error(`unknown dataset ${name}`);
  }
  return pts;
}

// ---------- neuron: one perceptron, weights set by hand ----------
export const neuronAccuracy = (pts, { w1, w2, b }) => pts.filter(([x1, x2, y]) => (w1 * x1 + w2 * x2 + b > 0 ? 1 : 0) === y).length / pts.length;
export const neuron = {
  name: "neuron",
  validate(p, g) { if (!LOGIC[p.gate] && !p.dataset) throw new Error("neuron: gate or dataset"); if (!(g.accuracy > 0)) throw new Error("neuron: goal.accuracy"); },
  initial: () => ({ w1: 0, w2: 0, b: 0 }),
  check(p, g, r) {
    const pts = p.gate ? LOGIC[p.gate] : dataset(p.dataset, p.n, p.seed);
    const acc = neuronAccuracy(pts, { w1: Number(r?.w1), w2: Number(r?.w2), b: Number(r?.b) });
    return ok(acc >= g.accuracy, { accuracy: acc });
  },
};

// ---------- mlp: a tiny 2-H-1 network trained by full-batch gradient descent ----------
const ACT = {
  tanh: { f: Math.tanh, d: (y) => 1 - y * y },
  relu: { f: (z) => Math.max(0, z), d: (y) => (y > 0 ? 1 : 0) },
  sigmoid: { f: (z) => 1 / (1 + Math.exp(-z)), d: (y) => y * (1 - y) },
};
export function trainMlp(pts, { hidden = 4, activation = "tanh", lr = 0.5, epochs = 200, seed = 1 }, onEpoch) {
  const r = rng(seed);
  const H = Math.max(0, Math.round(hidden));
  const act = ACT[activation] || ACT.tanh;
  const sig = ACT.sigmoid.f;
  const W1 = Array.from({ length: H }, () => [gauss(r) * 0.8, gauss(r) * 0.8]);
  const b1 = Array(H).fill(0);
  const W2 = Array.from({ length: H || 2 }, () => gauss(r) * 0.5);
  let b2 = 0;
  const forward = (x) => {
    const h = H ? W1.map((w, j) => act.f(w[0] * x[0] + w[1] * x[1] + b1[j])) : [x[0], x[1]];
    return { h, y: sig(h.reduce((a, hj, j) => a + hj * W2[j], b2)) };
  };
  let loss = 0;
  for (let e = 0; e < epochs; e++) {
    const gW1 = W1.map(() => [0, 0]), gb1 = Array(H).fill(0), gW2 = W2.map(() => 0);
    let gb2 = 0;
    loss = 0;
    for (const [x0, x1, t] of pts) {
      const { h, y } = forward([x0, x1]);
      loss += -(t * Math.log(y + 1e-12) + (1 - t) * Math.log(1 - y + 1e-12));
      const dz = y - t; // d(cross-entropy)/d(logit) for a sigmoid output
      gb2 += dz;
      for (let j = 0; j < W2.length; j++) {
        gW2[j] += dz * h[j];
        if (H) { const dh = dz * W2[j] * act.d(h[j]); gW1[j][0] += dh * x0; gW1[j][1] += dh * x1; gb1[j] += dh; }
      }
    }
    const n = pts.length;
    for (let j = 0; j < W2.length; j++) W2[j] -= (lr * gW2[j]) / n;
    b2 -= (lr * gb2) / n;
    for (let j = 0; j < H; j++) { W1[j][0] -= (lr * gW1[j][0]) / n; W1[j][1] -= (lr * gW1[j][1]) / n; b1[j] -= (lr * gb1[j]) / n; }
    if (onEpoch && (e % 10 === 9 || e === epochs - 1)) onEpoch(e + 1, loss / n);
  }
  const predict = (x) => forward(x).y;
  const accuracy = pts.filter(([x0, x1, t]) => (predict([x0, x1]) > 0.5 ? 1 : 0) === t).length / pts.length;
  return { predict, accuracy, loss: loss / pts.length };
}
export const mlp = {
  name: "mlp",
  validate(p, g) { dataset(p.dataset); if (!(g.accuracy > 0)) throw new Error("mlp: goal.accuracy"); },
  initial: (p) => ({ hidden: p.hidden ?? 0, activation: p.activation || "tanh", lr: p.lr ?? 0.5, epochs: p.epochs ?? 200, seed: 1 }),
  check(p, g, r) {
    const res = trainMlp(dataset(p.dataset, p.n, p.seed), { ...r, epochs: Math.min(Number(r?.epochs) || 0, 2000) });
    return ok(res.accuracy >= g.accuracy, { accuracy: res.accuracy, loss: res.loss });
  },
};

// ---------- kmeans: step Lloyd's algorithm until nothing moves ----------
export function kmeansRun(pts, k, seed = 5, maxIter = 50) {
  const r = rng(seed);
  let cents = Array.from({ length: k }, () => { const q = pts[Math.floor(r() * pts.length)]; return [q[0], q[1]]; });
  const history = [cents];
  let assign = [];
  for (let it = 0; it < maxIter; it++) {
    assign = pts.map((q) => cents.reduce((best, c, j) => ((q[0] - c[0]) ** 2 + (q[1] - c[1]) ** 2 < (q[0] - cents[best][0]) ** 2 + (q[1] - cents[best][1]) ** 2 ? j : best), 0));
    const next = cents.map((c, j) => {
      const mine = pts.filter((_, i) => assign[i] === j);
      return mine.length ? [mine.reduce((a, q) => a + q[0], 0) / mine.length, mine.reduce((a, q) => a + q[1], 0) / mine.length] : c;
    });
    const moved = next.some((c, j) => Math.hypot(c[0] - cents[j][0], c[1] - cents[j][1]) > 1e-9);
    cents = next;
    history.push(cents);
    if (!moved) return { history, assign, iterations: it + 1 };
  }
  return { history, assign, iterations: maxIter };
}
export const kmeans = {
  name: "kmeans",
  validate(p) { dataset(p.dataset || "blobs3"); if (!(p.k >= 1)) throw new Error("kmeans: k"); },
  initial: () => ({ iterations: 0 }),
  check(p, g, r) {
    const res = kmeansRun(dataset(p.dataset || "blobs3", p.n, p.seed), p.k, p.kmSeed);
    return ok((r?.iterations || 0) >= res.iterations, { need: res.iterations });
  },
};

export default [plot, matrix2d, sampler, descent, neuron, mlp, kmeans];
