// Unit tests of the math / machine-learning sims (src/game/sims/logic/math.js, src/game/sims/expr.js).
// Moved back from archive/tests/unit/sims-archived.test.mjs on 2026-11-04 with the sims.
import test from "node:test";
import assert from "node:assert/strict";
import { sample, trainMlp, dataset, riemann, integrate, taylor, descend, kmeansRun, neuronAccuracy, LOGIC } from "../../src/game/sims/logic/math.js";
import { compile, fx } from "../../src/game/sims/expr.js";

test("expr: precedence, implicit multiplication, functions", () => {
  assert.equal(fx("2x^2 + 3")(2), 11);
  assert.equal(fx("-x^2")(3), -9);
  assert.ok(Math.abs(fx("sin(pi/2)")(0) - 1) < 1e-12);
  assert.equal(compile("(x-3)^2")({ x: 5 }), 4);
  assert.throws(() => compile("x +"));
  assert.throws(() => compile("alert(1)")({ x: 0 }));
});

test("riemann sums converge to the integral of x^2 on [0,1] = 1/3", () => {
  const f = fx("x^2");
  assert.ok(Math.abs(integrate(f, 0, 1) - 1 / 3) < 1e-12);
  assert.ok(Math.abs(riemann(f, 0, 1, 4, "left") - 0.21875) < 1e-12);
  assert.ok(Math.abs(riemann(f, 0, 1, 1000, "mid") - 1 / 3) < 1e-6);
});
test("taylor: sin series at 1 with order 5 is within 2e-4", () => {
  assert.ok(Math.abs(taylor("sin", 5, 1) - Math.sin(1)) < 2e-4);
  assert.ok(Math.abs(taylor("cos", 4, 0.5) - Math.cos(0.5)) < 1e-4);
  assert.ok(Math.abs(taylor("exp", 10, 1) - Math.E) < 1e-6);
});
test("gradient descent on (x-3)^2: lr 0.1 converges, lr 1.1 diverges", () => {
  assert.ok(Math.abs(descend({ f: "(x-3)^2", x0: 0 }, 0.1, 60).x[0] - 3) < 1e-4);
  assert.ok(descend({ f: "(x-3)^2", x0: 0 }, 1.1, 200).diverged);
  const two = descend({ f: "x^2 + 10y^2", vars: ["x", "y"], x0: [2, 1] }, 0.05, 200);
  assert.ok(Math.hypot(...two.x) < 1e-3);
});

test("sampler: extending a seeded run preserves prior dice draws", () => {
  const draws = sample("twoDice", 100, 7);
  assert.deepEqual(draws.slice(0, 20), sample("twoDice", 20, 7));
  assert.equal(draws.length, 100);
  assert.ok(draws.every((value) => Number.isInteger(value) && value >= 2 && value <= 12));
  assert.ok(new Set(draws).size > 1);
});

test("a single neuron solves AND but cannot solve XOR", () => {
  assert.equal(neuronAccuracy(LOGIC.and, { w1: 1, w2: 1, b: -1.5 }), 1);
  let best = 0;
  for (let w1 = -3; w1 <= 3; w1 += 0.5) for (let w2 = -3; w2 <= 3; w2 += 0.5) for (let b = -3; b <= 3; b += 0.5) best = Math.max(best, neuronAccuracy(LOGIC.xor, { w1, w2, b }));
  assert.equal(best, 0.75);
});
test("mlp: no hidden layer fails the circle, 6 tanh units learn it", () => {
  const pts = dataset("circle");
  assert.ok(trainMlp(pts, { hidden: 0, lr: 1, epochs: 300 }).accuracy < 0.75);
  assert.ok(trainMlp(pts, { hidden: 6, activation: "tanh", lr: 1, epochs: 600 }).accuracy >= 0.9);
});
test("kmeans converges on three blobs", () => {
  const r = kmeansRun(dataset("blobs3"), 3);
  assert.ok(r.iterations < 50);
});
