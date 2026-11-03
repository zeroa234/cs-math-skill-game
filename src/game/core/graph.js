// Skill graph queries. Pure functions over the built tree (src/gen/tree.json); no UI, no storage.

export function indexTree(tree) {
  const byId = new Map(tree.skills.map((s) => [s.id, s]));
  const lanes = new Map(tree.lanes.map((l) => [l.id, l]));
  const laneOrder = new Map(tree.lanes.map((l, i) => [l.id, i]));
  return { tree, byId, lanes, laneOrder };
}

// Every skill that must be lit before `goal` (its required-prerequisite closure), goal included.
export function requiredClosure(g, goal) {
  const out = new Set();
  const walk = (id) => {
    if (out.has(id) || !g.byId.has(id)) return;
    out.add(id);
    for (const r of g.byId.get(id).required) walk(r.id);
  };
  walk(goal);
  return out;
}

// Orders a set of skills so every required prerequisite comes first (Kahn's algorithm).
// Ties: lower step first, then the lane order of the tree, then the id, so the order is stable.
export function topoOrder(g, ids) {
  const set = new Set(ids);
  const indeg = new Map([...set].map((id) => [id, 0]));
  for (const id of set) for (const r of g.byId.get(id).required) if (set.has(r.id)) indeg.set(id, indeg.get(id) + 1);
  const rank = (id) => {
    const s = g.byId.get(id);
    return [s.step, g.laneOrder.get(s.lane) ?? 99, id];
  };
  const cmp = (a, b) => {
    const ra = rank(a), rb = rank(b);
    return ra[0] - rb[0] || ra[1] - rb[1] || (ra[2] < rb[2] ? -1 : ra[2] > rb[2] ? 1 : 0);
  };
  const ready = [...set].filter((id) => indeg.get(id) === 0).sort(cmp);
  const out = [];
  while (ready.length) {
    const id = ready.shift();
    out.push(id);
    for (const s of g.tree.skills) {
      if (!set.has(s.id) || !s.required.some((r) => r.id === id)) continue;
      indeg.set(s.id, indeg.get(s.id) - 1);
      if (indeg.get(s.id) === 0) { ready.push(s.id); ready.sort(cmp); }
    }
  }
  if (out.length !== set.size) throw new Error("cycle in required prerequisites");
  return out;
}

// The goals a route must reach: its headline goal and any `also` goals (a career route such as web
// development needs several skills that do not require one another).
export const routeGoals = (route) => [...(route.also || []), route.goal];

// A campaign route: the goals' required closure in a valid learning order, plus the recommended
// prerequisites of those stops as optional side quests (not on the path, never blocking).
export function planRoute(g, route) {
  const closure = new Set(routeGoals(route).flatMap((id) => [...requiredClosure(g, id)]));
  const stops = topoOrder(g, closure);
  const side = new Map();
  for (const id of stops) {
    for (const r of g.byId.get(id).recommended) {
      if (closure.has(r.id) || !g.byId.has(r.id)) continue;
      if (!side.has(r.id)) side.set(r.id, { id: r.id, for: [] });
      side.get(r.id).for.push({ id, why: r.why });
    }
  }
  return { ...route, stops, sideQuests: [...side.values()] };
}

// Skills that become unblocked when `id` is lit (direct dependents).
export const dependents = (g, id) => g.tree.skills.filter((s) => s.required.some((r) => r.id === id)).map((s) => s.id);
