// Unit tests of the graph sim's Dijkstra, topological sort and max flow modes (BFS and DFS are in
// sims.test.mjs). Archived with those modes on 2026-11-04 and moved back with them for M.5.3 and F.1.2.
import test from "node:test";
import assert from "node:assert/strict";
import { graph, judgeOrder, sampleOrder, dijkstraState, adjacency, bellmanFord, maxFlow } from "../../src/game/sims/logic/algo.js";

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
