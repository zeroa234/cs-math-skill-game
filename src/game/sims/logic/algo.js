// Pure logic for the sim `graph`: you play BFS or DFS on a small drawn graph. Same { name, validate,
// initial, check } shape as os.js. Dijkstra, topological sort and max flow were archived with the
// lessons that used them (archive/src/game/sims/logic/algo.js).
//
// params { mode: bfs|dfs, nodes: [{id, x, y}], edges: [[from, to]], directed?, start }
// The answer is the node ids in the order the algorithm first reaches them. Any order the algorithm
// could produce is accepted: ties are the player's choice.

const ok = (correct, detail = {}) => ({ correct, detail });
export const byId = (a, b) => String(a).localeCompare(String(b), "en", { numeric: true });

export function adjacency(p) {
  const out = Object.fromEntries(p.nodes.map((n) => [n.id, []]));
  for (const [u, v] of p.edges) {
    out[u].push({ to: v });
    if (!p.directed) out[v].push({ to: u });
  }
  for (const k in out) out[k].sort((a, b) => byId(a.to, b.to));
  return { out };
}

// ---------- the state after a (valid) prefix, and which nodes may come next ----------
// parent[v] is the node whose expansion discovered v: the edges of the BFS/DFS tree.
function bfsState(adj, start, seq) {
  if (!seq.length) return { next: [start], queue: [], head: null, parent: {} };
  const disc = new Set([seq[0]]);
  const parent = {};
  let k = 1;
  for (let i = 0; i < seq.length; i++) {
    const need = new Set(adj.out[seq[i]].map((e) => e.to).filter((v) => !disc.has(v)));
    while (need.size && k < seq.length) { need.delete(seq[k]); disc.add(seq[k]); parent[seq[k]] = seq[i]; k++; }
    // the node being expanded is seq[i]; the queue holds discovered nodes not yet expanded
    if (need.size) return { next: [...need].sort(byId), head: seq[i], queue: seq.slice(i + 1), parent };
  }
  return { next: [], head: null, queue: [], parent };
}

function dfsState(adj, start, seq) {
  if (!seq.length) return { next: [start], stack: [], parent: {} };
  const disc = new Set();
  const stack = [];
  const parent = {};
  const open = (v) => adj.out[v].some((e) => !disc.has(e.to));
  for (const v of seq) {
    while (stack.length && !open(stack[stack.length - 1])) stack.pop();
    if (stack.length) parent[v] = stack[stack.length - 1];
    disc.add(v);
    stack.push(v);
  }
  while (stack.length && !open(stack[stack.length - 1])) stack.pop();
  const top = stack[stack.length - 1];
  return { next: top === undefined ? [] : adj.out[top].map((e) => e.to).filter((v) => !disc.has(v)), stack, parent };
}

export function orderState(p, seq, adj = adjacency(p)) {
  if (p.mode === "bfs") return bfsState(adj, p.start, seq);
  if (p.mode === "dfs") return dfsState(adj, p.start, seq);
  throw new Error(`graph: unknown mode ${p.mode}`);
}

// Index of the first entry that the algorithm could not have produced (-1: every entry is fine),
// and whether the order is complete.
export function judgeOrder(p, seq) {
  const adj = adjacency(p);
  const seen = new Set();
  for (let i = 0; i < seq.length; i++) {
    if (seen.has(seq[i]) || !orderState(p, seq.slice(0, i), adj).next.includes(seq[i])) return { firstWrong: i, complete: false };
    seen.add(seq[i]);
  }
  return { firstWrong: -1, complete: orderState(p, seq, adj).next.length === 0 };
}

// One valid order, breaking ties by id (what a textbook with sorted adjacency lists would print).
export function sampleOrder(p) {
  const adj = adjacency(p);
  const seq = [];
  for (let s = orderState(p, seq, adj); s.next.length; s = orderState(p, seq, adj)) seq.push(s.next[0]);
  return seq;
}

// ---------- the sim ----------
const MODES = ["bfs", "dfs"];
export const graph = {
  name: "graph",
  validate(p) {
    if (!MODES.includes(p.mode)) throw new Error(`graph: mode must be ${MODES.join("|")}`);
    const ids = p.nodes.map((n) => n.id);
    if (new Set(ids).size !== ids.length) throw new Error("graph: duplicate node id");
    for (const n of p.nodes) if (!(Number.isFinite(n.x) && Number.isFinite(n.y))) throw new Error(`graph: node ${n.id} needs x and y`);
    for (const e of p.edges) if (e.length !== 2 || !ids.includes(e[0]) || !ids.includes(e[1])) throw new Error(`graph: edge ${e.join(" ")} must name two known nodes`);
    if (!ids.includes(p.start)) throw new Error("graph: start must be a node");
  },
  initial: () => [],
  check(p, g, r) {
    const seq = Array.isArray(r) ? r : [];
    const j = judgeOrder(p, seq);
    return ok(j.firstWrong === -1 && j.complete, { ...j, sample: sampleOrder(p) });
  },
};

export default [graph];
