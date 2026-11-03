// Unit tests of the archived sims, moved out of tests/unit/sims.test.mjs on 2026-11-04. They import
// the archived copies, so they still run: node --test archive/tests/unit/*.test.mjs
import test from "node:test";
import assert from "node:assert/strict";
import { trainMlp, dataset, riemann, integrate, taylor, descend, kmeansRun, neuronAccuracy, LOGIC } from "../../src/game/sims/logic/math.js";
import { compile, fx } from "../../src/game/sims/expr.js";
import { graph, judgeOrder, sampleOrder, dijkstraState, adjacency, bellmanFord, maxFlow } from "../../src/game/sims/logic/algo.js";

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

// graph sim, the archived modes. Positions do not matter to the logic; every node sits at the origin.
const at = (ids) => ids.map((id) => ({ id, x: 0, y: 0 }));
// the boss exercise of F.1.2 (answers verified there): settle order s b a c t, distances 0 1 3 4 7
const BOSS = { mode: "dijkstra", directed: true, start: "s", nodes: at(["s", "a", "b", "c", "t"]), edges: [["s", "a", 4], ["s", "b", 1], ["b", "a", 2], ["a", "c", 1], ["b", "c", 5], ["c", "t", 3], ["a", "t", 6]] };
test("graph dijkstra: settle order and distances of the F.1.2 boss graph", () => {
  assert.equal(sampleOrder(BOSS).join(""), "sbact");
  assert.deepEqual(dijkstraState(adjacency(BOSS), "s", [..."sbact"]).dist, { s: 0, a: 3, b: 1, c: 4, t: 7 });
  assert.equal(judgeOrder(BOSS, [..."sabct"]).firstWrong, 1);
});
test("graph dijkstra with a negative edge settles a too early; Bellman–Ford finds the shorter path", () => {
  const p = { mode: "dijkstra", directed: true, start: "s", nodes: at(["s", "a", "b"]), edges: [["s", "a", 2], ["s", "b", 5], ["b", "a", -4]] };
  assert.deepEqual(dijkstraState(adjacency(p), "s", [..."sab"]).dist, { s: 0, a: 2, b: 5 });
  assert.deepEqual(bellmanFord(p), { s: 0, a: 1, b: 5 });
});
test("graph topo: linear extensions of divisibility on {1,2,3,4,6,12}", () => {
  const p = { mode: "topo", directed: true, nodes: at(["1", "2", "3", "4", "6", "12"]), edges: [["1", "2"], ["1", "3"], ["2", "4"], ["2", "6"], ["3", "6"], ["4", "12"], ["6", "12"]] };
  assert.equal(judgeOrder(p, ["1", "3", "2", "6", "4", "12"]).firstWrong, -1);
  assert.equal(judgeOrder(p, ["1", "2", "6"]).firstWrong, 2); // 6 needs 3 first
  assert.equal(sampleOrder(p).join(","), "1,2,3,4,6,12");
  assert.throws(() => graph.validate({ mode: "topo", directed: true, nodes: at(["a", "b"]), edges: [["a", "b"], ["b", "a"]] }, {}), /cycle/);
});
test("graph flow: the greedy path s-a-b-t blocks at 1 until the reverse residual edge b→a is used", () => {
  const p = { mode: "flow", directed: true, start: "s", sink: "t", nodes: at(["s", "a", "b", "t"]), edges: [["s", "a", 1], ["s", "b", 1], ["a", "b", 1], ["a", "t", 1], ["b", "t", 1]] };
  assert.equal(maxFlow(p).value, 2);
  assert.equal(graph.check(p, {}, { paths: [[..."sabt"]] }).correct, false);
  assert.equal(graph.check(p, {}, { paths: [[..."sabt"], [..."sbat"]] }).correct, true);
  assert.ok(graph.check(p, {}, { paths: [[..."sabt"], [..."sat"]] }).detail.error); // s→a is full
});
test("graph flow: CLRS-style network, max flow 23 (networkx agrees) and the cut has the same capacity", () => {
  const p = { mode: "flow", directed: true, start: "s", sink: "t", nodes: at(["s", "v1", "v2", "v3", "v4", "t"]),
    edges: [["s", "v1", 16], ["s", "v2", 13], ["v2", "v1", 4], ["v1", "v3", 12], ["v3", "v2", 9], ["v2", "v4", 14], ["v4", "v3", 7], ["v3", "t", 20], ["v4", "t", 4]] };
  const r = maxFlow(p);
  assert.equal(r.value, 23);
  assert.equal(r.cut.reduce((a, e) => a + e[2], 0), 23);
});
