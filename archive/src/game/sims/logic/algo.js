// Pure logic for the algorithms-route sim `graph`: you play BFS, DFS, Dijkstra, a topological sort,
// or Ford–Fulkerson on a small drawn graph. Same { name, validate, initial, check } shape as os.js.
//
// params { mode: bfs|dfs|dijkstra|topo|flow, nodes: [{id, x, y}], edges: [[from, to, weight?]],
//          directed?, start? (bfs/dfs/dijkstra/flow source), sink? (flow) }
// Order modes answer with the node ids in the order the algorithm handles them (BFS/DFS: discovery
// order; Dijkstra: the order nodes are settled; topo: the sorted order). Any order the algorithm
// could produce is accepted: ties are the player's choice. flow answers { paths: [[s, …, t], …] },
// augmenting paths in the residual graph, and is correct once the flow is maximum.

const ok = (correct, detail = {}) => ({ correct, detail });
export const byId = (a, b) => String(a).localeCompare(String(b), "en", { numeric: true });

export function adjacency(p) {
  const out = Object.fromEntries(p.nodes.map((n) => [n.id, []]));
  const inn = Object.fromEntries(p.nodes.map((n) => [n.id, []]));
  for (const [u, v, w = 1] of p.edges) {
    out[u].push({ to: v, w });
    inn[v].push({ to: u, w });
    if (!p.directed) { out[v].push({ to: u, w }); inn[u].push({ to: v, w }); }
  }
  for (const k in out) { out[k].sort((a, b) => byId(a.to, b.to)); inn[k].sort((a, b) => byId(a.to, b.to)); }
  return { out, inn };
}

// ---------- order modes: the state after a (valid) prefix, and which nodes may come next ----------
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

export function dijkstraState(adj, start, seq) {
  const dist = { [start]: 0 }, pred = {};
  const done = new Set();
  for (const v of seq) {
    done.add(v);
    for (const e of adj.out[v]) {
      if (done.has(e.to)) continue;
      const d = dist[v] + e.w;
      if (dist[e.to] === undefined || d < dist[e.to]) { dist[e.to] = d; pred[e.to] = v; }
    }
  }
  const open = Object.keys(dist).filter((v) => !done.has(v));
  const min = Math.min(...open.map((v) => dist[v]));
  return { next: open.filter((v) => dist[v] === min).sort(byId), dist, parent: pred };
}

function topoState(adj, nodes, seq) {
  const done = new Set(seq);
  return { next: nodes.filter((v) => !done.has(v) && adj.inn[v].every((e) => done.has(e.to))) };
}

export function orderState(p, seq, adj = adjacency(p)) {
  if (p.mode === "bfs") return bfsState(adj, p.start, seq);
  if (p.mode === "dfs") return dfsState(adj, p.start, seq);
  if (p.mode === "dijkstra") return dijkstraState(adj, p.start, seq);
  if (p.mode === "topo") return topoState(adj, p.nodes.map((n) => n.id).sort(byId), seq);
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

// True shortest distances (Bellman–Ford), to compare with Dijkstra when an edge is negative.
export function bellmanFord(p) {
  const adj = adjacency(p);
  const dist = { [p.start]: 0 };
  const ids = p.nodes.map((n) => n.id);
  for (let r = 0; r < ids.length; r++) {
    let changed = false;
    for (const u of ids) if (dist[u] !== undefined) for (const e of adj.out[u]) if (dist[e.to] === undefined || dist[u] + e.w < dist[e.to]) { dist[e.to] = dist[u] + e.w; changed = true; }
    if (!changed) return dist;
  }
  return null; // a negative cycle is reachable
}

// ---------- flow: augmenting paths in the residual graph ----------
const edgeKey = (u, v) => `${u}>${v}`;
export function residual(p, flow, u, v) {
  const fwd = p.edges.find((e) => e[0] === u && e[1] === v);
  if (fwd) return fwd[2] - (flow[edgeKey(u, v)] || 0);
  return p.edges.some((e) => e[0] === v && e[1] === u) ? flow[edgeKey(v, u)] || 0 : 0;
}

// Pushes the bottleneck along `path`; returns { flow, pushed } or { error }.
export function augment(p, flow0, path) {
  if (path[0] !== p.start || path[path.length - 1] !== p.sink) return { error: "路径要从源点走到汇点" };
  if (new Set(path).size !== path.length) return { error: "路径不能重复经过同一个点" };
  const caps = [];
  for (let i = 0; i + 1 < path.length; i++) {
    const r = residual(p, flow0, path[i], path[i + 1]);
    if (!(r > 0)) return { error: `${path[i]} → ${path[i + 1]} 没有剩余容量` };
    caps.push(r);
  }
  const pushed = Math.min(...caps);
  const flow = { ...flow0 };
  for (let i = 0; i + 1 < path.length; i++) {
    const [u, v] = [path[i], path[i + 1]];
    if (p.edges.some((e) => e[0] === u && e[1] === v)) flow[edgeKey(u, v)] = (flow[edgeKey(u, v)] || 0) + pushed;
    else flow[edgeKey(v, u)] -= pushed; // walking an edge backwards takes back flow already sent on it
  }
  return { flow, pushed };
}

export const flowValue = (p, flow) => p.edges.reduce((a, [u, v]) => a + (u === p.start ? flow[edgeKey(u, v)] || 0 : 0) - (v === p.start ? flow[edgeKey(u, v)] || 0 : 0), 0);

// Nodes reachable from the source in the residual graph (after a maximum flow: the source side of a minimum cut).
export function residualReach(p, flow) {
  const ids = p.nodes.map((n) => n.id);
  const seen = new Set([p.start]);
  const q = [p.start];
  while (q.length) { const u = q.shift(); for (const v of ids) if (!seen.has(v) && residual(p, flow, u, v) > 0) { seen.add(v); q.push(v); } }
  return seen;
}

// Edmonds–Karp: shortest augmenting paths until none is left.
export function maxFlow(p) {
  let flow = {};
  const paths = [];
  for (;;) {
    const ids = p.nodes.map((n) => n.id).sort(byId);
    const prev = { [p.start]: null };
    const q = [p.start];
    while (q.length && !(p.sink in prev)) { const u = q.shift(); for (const v of ids) if (!(v in prev) && residual(p, flow, u, v) > 0) { prev[v] = u; q.push(v); } }
    if (!(p.sink in prev)) break;
    const path = [];
    for (let v = p.sink; v !== null; v = prev[v]) path.unshift(v);
    flow = augment(p, flow, path).flow;
    paths.push(path);
  }
  const side = residualReach(p, flow);
  return { value: flowValue(p, flow), flow, paths, cut: p.edges.filter(([u, v]) => side.has(u) && !side.has(v)) };
}

export function replayFlow(p, paths) {
  let flow = {};
  for (const path of paths) {
    const r = augment(p, flow, path);
    if (r.error) return { flow, error: r.error };
    flow = r.flow;
  }
  return { flow };
}

// ---------- the sim ----------
const MODES = ["bfs", "dfs", "dijkstra", "topo", "flow"];
export const graph = {
  name: "graph",
  validate(p) {
    if (!MODES.includes(p.mode)) throw new Error(`graph: mode must be ${MODES.join("|")}`);
    const ids = p.nodes.map((n) => n.id);
    if (new Set(ids).size !== ids.length) throw new Error("graph: duplicate node id");
    for (const n of p.nodes) if (!(Number.isFinite(n.x) && Number.isFinite(n.y))) throw new Error(`graph: node ${n.id} needs x and y`);
    for (const e of p.edges) {
      if (!ids.includes(e[0]) || !ids.includes(e[1])) throw new Error(`graph: edge ${e.join(" ")} names an unknown node`);
      if (e.length > 2 && !Number.isFinite(e[2])) throw new Error(`graph: edge ${e.join(" ")} weight is not a number`);
    }
    if (p.mode !== "topo" && !ids.includes(p.start)) throw new Error("graph: start must be a node");
    if (p.mode === "topo") {
      if (!p.directed) throw new Error("graph: topo needs a directed graph");
      if (sampleOrder(p).length !== ids.length) throw new Error("graph: topo graph has a cycle");
    }
    if (p.mode === "flow") {
      if (!p.directed) throw new Error("graph: flow needs a directed graph");
      if (!ids.includes(p.sink) || p.sink === p.start) throw new Error("graph: flow needs a sink other than the start");
      for (const [u, v, c] of p.edges) {
        if (!(Number.isInteger(c) && c > 0)) throw new Error(`graph: capacity of ${u}→${v} must be a positive integer`);
        if (p.edges.some((e) => e[0] === v && e[1] === u)) throw new Error(`graph: ${u}→${v} and ${v}→${u} both exist; flow mode keeps the residual graph unambiguous`);
      }
    }
  },
  initial: (p) => (p.mode === "flow" ? { paths: [], cur: [p.start] } : []),
  check(p, g, r) {
    if (p.mode === "flow") {
      const best = maxFlow(p).value;
      const res = replayFlow(p, Array.isArray(r?.paths) ? r.paths : []);
      if (res.error) return ok(false, { error: res.error, best });
      const value = flowValue(p, res.flow);
      return ok(value === best, { value, best });
    }
    const seq = Array.isArray(r) ? r : [];
    const j = judgeOrder(p, seq);
    return ok(j.firstWrong === -1 && j.complete, { ...j, sample: sampleOrder(p) });
  },
};

export default [graph];
