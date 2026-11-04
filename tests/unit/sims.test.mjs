// Unit tests for sim logic. Expected values are worked by hand in the comments. The graph sim's
// Dijkstra, topological sort and max flow modes are in sims-graph.test.mjs, the math sims in sims-math.test.mjs.
import test from "node:test";
import assert from "node:assert/strict";
import { SIMS } from "../../src/game/sims/logic/index.js";
import { schedule, translate, hashPlacement, goalReachable, replayThreads, bitsValue, replaceRun } from "../../src/game/sims/logic/os.js";
import { runPyTrace } from "../../scripts/lib/packs.mjs";
import { answersFor } from "../../src/game/sims/logic/trace.js";
import { judgeOrder, sampleOrder } from "../../src/game/sims/logic/algo.js";

const procs = [{ name: "A", arrive: 0, burst: 5 }, { name: "B", arrive: 1, burst: 3 }, { name: "C", arrive: 2, burst: 1 }];

test("FCFS: A0-5, B5-8, C8-9; waits 0,4,6", () => {
  const r = schedule({ procs, algo: "FCFS" });
  assert.equal(r.timeline.join(""), "AAAAABBBC");
  assert.deepEqual(r.stats.map((s) => s.wait), [0, 4, 6]);
});
test("SJF non-preemptive: A runs to 5, then C (1) before B (3)", () => {
  assert.equal(schedule({ procs, algo: "SJF" }).timeline.join(""), "AAAAACBBB");
});
test("SRTF: B preempts A at 1 (3 < 4), C preempts? no: at 2 B has 2 left, C 1 → C runs", () => {
  // t0 A(5→4); t1 B arrives 3 < A's 4 → B(3→2); t2 C arrives 1 < B's 2 → C done at 3; then B 2, then A 4
  assert.equal(schedule({ procs, algo: "SRTF" }).timeline.join(""), "ABCBBAAAA");
});
test("RR q=2: new arrivals queue before the preempted process", () => {
  assert.equal(schedule({ procs, algo: "RR", quantum: 2 }).timeline.join(""), "AABBCAABA");
});
test("scheduler idles when nothing has arrived", () => {
  assert.deepEqual(schedule({ procs: [{ name: "A", arrive: 2, burst: 1 }], algo: "FCFS" }).timeline, [null, null, "A"]);
});

test("paging: 4 KiB pages, vaddr 0x2345 → vpn 2, offset 0x345", () => {
  const t = translate({ pageSize: 4096, vaddr: 0x2345, table: [5, null, 7] });
  assert.deepEqual([t.vpn, t.offset, t.pfn, t.paddr], [2, 0x345, 7, 7 * 4096 + 0x345]);
  assert.equal(translate({ pageSize: 4096, vaddr: 0x1000, table: [5, null, 7] }).fault, true);
  assert.ok(SIMS.paging.check({ pageSize: 4096, vaddr: 0x2345, table: [5, null, 7] }, {}, { vpn: 2, offset: 837, paddr: 29509 }).correct);
});

test("hash linear probing: size 7, keys 10 17 3 24 → 3 4 5 6", () => {
  assert.deepEqual(hashPlacement({ size: 7, keys: [10, 17, 3, 24], probe: "linear" }), [3, 4, 5, 6]);
});

test("bits: two's complement", () => {
  assert.equal(bitsValue([1, 1, 1, 1, 1, 1, 1, 1], true), -1);
  assert.equal(bitsValue([1, 0, 0, 0, 0, 0, 0, 0], true), -128);
  assert.equal(bitsValue([0, 0, 0, 0, 0, 1, 0, 1], false), 5);
});

const race = { shared: { x: 0 }, threads: [{ name: "T1", locals: { t: 0 }, steps: ["t = x", "t = t + 1", "x = t"] }, { name: "T2", locals: { t: 0 }, steps: ["t = x", "t = t + 1", "x = t"] }] };
test("threads: the lost update x == 1 is reachable, x == 3 is not", () => {
  assert.ok(goalReachable(race, { final: { x: 1 } }));
  assert.ok(goalReachable(race, { final: { x: 2 } }));
  assert.ok(!goalReachable(race, { final: { x: 3 } }));
  assert.ok(SIMS.threads.check(race, { final: { x: 1 } }, [0, 1, 0, 0, 1, 1]).correct);
  assert.ok(!SIMS.threads.check(race, { final: { x: 1 } }, [0, 0, 0, 1, 1, 1]).correct);
});
test("threads: locks prevent the race; opposite lock order can deadlock", () => {
  const locked = { shared: { x: 0 }, locks: ["m"], threads: [0, 1].map((i) => ({ name: "T" + i, locals: { t: 0 }, steps: ["lock m", "t = x", "t = t + 1", "x = t", "unlock m"] })) };
  assert.ok(!goalReachable(locked, { final: { x: 1 } }));
  const dl = { locks: ["a", "b"], threads: [{ name: "T1", steps: ["lock a", "lock b", "unlock b", "unlock a"] }, { name: "T2", steps: ["lock b", "lock a", "unlock a", "unlock b"] }] };
  assert.ok(goalReachable(dl, { deadlock: true }));
  assert.equal(replayThreads(dl, [0, 1]).error, undefined); // T1 holds a, T2 holds b
  assert.ok(replayThreads(dl, [0, 1, 0]).error);
});

test("trace: real Python run, values after a line", () => {
  const code = "total = 0\nfor i in range(3):\n    total = total + i\nprint(total)\n";
  const run = runPyTrace(code);
  assert.equal(run.error, null);
  assert.equal(run.out, "3\n");
  assert.deepEqual(answersFor(run.steps, [{ line: 3, var: "total", hit: 2 }, { line: 4, var: "@out" }]), ["1", "3\n"]);
});

// graph sim. Positions do not matter to the logic; every node sits at the origin.
const at = (ids) => ids.map((id) => ({ id, x: 0, y: 0 }));
const G1 = { nodes: at(["a", "b", "c", "d", "e", "f"]), edges: [["a", "b"], ["a", "c"], ["b", "d"], ["c", "d"], ["c", "e"], ["d", "f"], ["e", "f"]], start: "a" };
test("graph bfs: any queue order of a node's new neighbours is accepted, a skipped level is not", () => {
  const p = { ...G1, mode: "bfs" };
  // expand a → {b, c}; if c came first, c is expanded first → {d, e}; then b (nothing new), d → f
  for (const seq of ["abcdef", "acbdef", "acbedf"]) assert.deepEqual(judgeOrder(p, [...seq]), { firstWrong: -1, complete: true }, seq);
  // after a b c, b is expanded first and its only new neighbour is d, so e cannot be next
  assert.equal(judgeOrder(p, [..."abced"]).firstWrong, 3);
  assert.equal(sampleOrder(p).join(""), "abcdef");
});
test("graph dfs: go deep from the newest node, back up only when it has no new neighbour", () => {
  const p = { ...G1, mode: "dfs" };
  for (const seq of ["abdcef", "abdfec", "acdbfe"]) assert.equal(judgeOrder(p, [...seq]).firstWrong, -1, seq);
  // from b the only new neighbour is d
  assert.equal(judgeOrder(p, [..."abc"]).firstWrong, 2);
  assert.equal(sampleOrder(p).join(""), "abdcef");
});
// replace: OSTEP ch. 22's stream 0,1,2,0,1,3,0,3,1,2,1 with 3 frames — optimal 6 hits / 5 misses, FIFO 4 hits
// (36.4%), LRU matches optimal here; the skill tree's exercise 7 0 1 2 0 3 0 4 2 3 0 3 2: FIFO 10, LRU 9 faults.
const auto = (p) => replaceRun(p, [], (allowed) => allowed[0]);
test("replace: OSTEP's example stream under OPT, FIFO, LRU", () => {
  const refs = [0, 1, 2, 0, 1, 3, 0, 3, 1, 2, 1];
  assert.equal(auto({ frames: 3, refs, policy: "OPT" }).misses, 5);
  assert.equal(auto({ frames: 3, refs, policy: "FIFO" }).hits, 4);
  assert.equal(auto({ frames: 3, refs, policy: "LRU" }).hits, 6);
});
test("replace: the skill tree's exercise, FIFO 10 faults and LRU 9", () => {
  const refs = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2];
  assert.equal(auto({ frames: 3, refs, policy: "FIFO" }).misses, 10);
  assert.equal(auto({ frames: 3, refs, policy: "LRU" }).misses, 9);
});
test("replace: Belady's anomaly, FIFO misses more with 4 frames (10) than with 3 (9)", () => {
  const refs = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5];
  assert.equal(auto({ frames: 3, refs, policy: "FIFO" }).misses, 9);
  assert.equal(auto({ frames: 4, refs, policy: "FIFO" }).misses, 10);
});
test("replace: the checker takes the player's evictions; OPT accepts any tie among never-used-again pages", () => {
  const p = { frames: 2, refs: [1, 2, 3, 1], policy: "FIFO" };
  assert.ok(SIMS.replace.check(p, {}, [1, 2]).correct); // 3 evicts 1 (oldest), then 1 evicts 2
  const bad = SIMS.replace.check(p, {}, [2]);
  assert.ok(!bad.correct && /FIFO/.test(bad.detail.error));
  assert.equal(SIMS.replace.check(p, {}, [1]).detail.pending, 3); // still waiting for the second choice
  const opt = { frames: 2, refs: [1, 2, 3], policy: "OPT" }; // neither 1 nor 2 is used again
  assert.ok(SIMS.replace.check(opt, {}, [1]).correct && SIMS.replace.check(opt, {}, [2]).correct);
  assert.ok(!SIMS.replace.check(opt, { misses: 2 }, [1]).correct); // 3 misses, goal says 2
});
