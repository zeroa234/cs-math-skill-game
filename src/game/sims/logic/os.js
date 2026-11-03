// Pure logic for the systems-route sims: bits, stackqueue, hash, scheduler, paging, threads.
// Each sim: { name, validate(params, goal), initial(params), check(params, goal, response) }.
// validate throws on authoring mistakes; check never throws on player input.

const eq = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const ok = (correct, detail = {}) => ({ correct, detail });

// ---------- bits: an n-bit register the player toggles ----------
export const bitsValue = (bits, signed) => {
  const n = bits.length;
  const u = bits.reduce((acc, b) => acc * 2 + (b ? 1 : 0), 0);
  return signed && bits[0] ? u - 2 ** n : u;
};
export const bits = {
  name: "bits",
  validate(p, g) {
    const n = p.bits;
    if (!Number.isInteger(n) || n < 1 || n > 16) throw new Error("bits: params.bits must be 1..16");
    const lo = p.signed ? -(2 ** (n - 1)) : 0, hi = p.signed ? 2 ** (n - 1) - 1 : 2 ** n - 1;
    if (!(g.value >= lo && g.value <= hi)) throw new Error(`bits: goal.value ${g.value} outside ${lo}..${hi}`);
  },
  initial: (p) => Array.from({ length: p.bits }, (_, i) => ((p.start ?? 0) >> (p.bits - 1 - i)) & 1),
  check: (p, g, r) => (Array.isArray(r) && r.length === p.bits ? ok(bitsValue(r, p.signed) === g.value, { value: bitsValue(r, p.signed) }) : ok(false)),
};

// ---------- stackqueue: push / pop on a stack or a queue ----------
export function replayContainer(kind, start, ops) {
  const s = [...start];
  const out = [];
  for (const o of ops) {
    if (o.op === "push") s.push(o.v);
    else if (o.op === "pop") { if (!s.length) return { error: "从空容器里取元素" }; out.push(kind === "stack" ? s.pop() : s.shift()); }
  }
  return { state: s, outputs: out };
}
export const stackqueue = {
  name: "stackqueue",
  validate(p, g) {
    if (!["stack", "queue"].includes(p.kind)) throw new Error("stackqueue: kind must be stack|queue");
    if (!g.state && !g.outputs) throw new Error("stackqueue: goal needs state and/or outputs");
  },
  initial: () => ({ ops: [] }),
  check(p, g, r) {
    const res = replayContainer(p.kind, p.start || [], r?.ops || []);
    if (res.error) return ok(false, res);
    return ok((!g.state || eq(res.state, g.state)) && (!g.outputs || eq(res.outputs, g.outputs)), res);
  },
};

// ---------- hash: place keys into an open-addressing table ----------
export function hashPlacement(p) {
  const slots = Array(p.size).fill(null);
  return p.keys.map((k) => {
    const h = ((k % p.size) + p.size) % p.size;
    if (p.probe === "chain") return h;
    for (let i = 0; i < p.size; i++) {
      const s = (h + i) % p.size;
      if (slots[s] === null) { slots[s] = k; return s; }
    }
    return null;
  });
}
export const hash = {
  name: "hash",
  validate(p) {
    if (!Number.isInteger(p.size) || p.size < 2) throw new Error("hash: size");
    if (!["linear", "chain"].includes(p.probe)) throw new Error("hash: probe must be linear|chain");
    if (p.probe === "linear" && p.keys.length > p.size) throw new Error("hash: more keys than slots");
  },
  initial: () => [],
  check: (p, g, r) => { const want = hashPlacement(p); return ok(eq(want, r), { want }); },
};

// ---------- scheduler: build the Gantt chart of a CPU scheduling policy ----------
// Conventions (shown to the player): time is in whole units; ties go to the earlier arrival, then
// the earlier row in the table. SJF is non-preemptive, SRTF preemptive (a running process keeps the
// CPU on a tie). RR: a process arriving at time t joins the ready queue before the process whose
// quantum expires at t.
export function schedule(p) {
  const procs = p.procs.map((q, i) => ({ ...q, i, left: q.burst }));
  const timeline = [];
  let t = 0, running = null, slice = 0;
  const queue = [];
  const arrivedAt = (time) => procs.filter((q) => q.arrive === time);
  const done = () => procs.every((q) => q.left === 0);
  const byArrival = (a, b) => a.arrive - b.arrive || a.i - b.i;
  if (p.algo === "RR") for (const q of arrivedAt(0).sort(byArrival)) queue.push(q);
  while (!done()) {
    if (t > 1000) throw new Error("scheduler: runaway");
    const ready = procs.filter((q) => q.arrive <= t && q.left > 0);
    let pick = null;
    if (p.algo === "FCFS") pick = running && running.left > 0 ? running : ready.sort(byArrival)[0];
    else if (p.algo === "SJF") pick = running && running.left > 0 ? running : ready.sort((a, b) => a.burst - b.burst || byArrival(a, b))[0];
    else if (p.algo === "SRTF") {
      const best = ready.sort((a, b) => a.left - b.left || byArrival(a, b))[0];
      pick = running && running.left > 0 && best && running.left <= best.left ? running : best;
    } else if (p.algo === "RR") {
      if (running && running.left > 0 && slice < p.quantum) pick = running;
      else pick = queue.shift() || null;
      if (pick !== running) slice = 0;
    } else throw new Error(`scheduler: unknown algo ${p.algo}`);
    timeline.push(pick ? pick.name : null);
    if (pick) { pick.left--; slice++; if (pick.left === 0) pick.end = t + 1; }
    running = pick;
    t++;
    if (p.algo === "RR") {
      for (const q of arrivedAt(t).sort(byArrival)) queue.push(q);
      if (running && running.left > 0 && slice >= p.quantum) { queue.push(running); running = null; }
      else if (running && running.left === 0) running = null;
    }
  }
  const stats = procs.map((q) => ({ name: q.name, end: q.end, turnaround: q.end - q.arrive, wait: q.end - q.arrive - q.burst }));
  return { timeline, stats, avgWait: stats.reduce((a, s) => a + s.wait, 0) / stats.length, avgTurnaround: stats.reduce((a, s) => a + s.turnaround, 0) / stats.length };
}
export const scheduler = {
  name: "scheduler",
  validate(p) {
    if (!["FCFS", "SJF", "SRTF", "RR"].includes(p.algo)) throw new Error("scheduler: algo");
    if (p.algo === "RR" && !(p.quantum >= 1)) throw new Error("scheduler: RR needs quantum");
    schedule(p);
  },
  initial: (p) => Array(p.procs.reduce((a, q) => a + q.burst, 0) + Math.max(0, ...p.procs.map((q) => q.arrive))).fill(undefined),
  check(p, g, r) {
    const want = schedule(p).timeline;
    const got = (r || []).slice(0, want.length).map((x) => (x === undefined ? undefined : x));
    const firstWrong = want.findIndex((w, i) => got[i] !== w);
    return ok(firstWrong === -1, { want, firstWrong });
  },
};

// ---------- paging: translate a virtual address with a one-level page table ----------
export function translate(p) {
  const vpn = Math.floor(p.vaddr / p.pageSize), offset = p.vaddr % p.pageSize;
  const frame = p.table[vpn];
  if (frame === null || frame === undefined) return { vpn, offset, fault: true };
  return { vpn, offset, fault: false, pfn: frame, paddr: frame * p.pageSize + offset };
}
export const paging = {
  name: "paging",
  validate(p) {
    if (!(p.pageSize > 0 && (p.pageSize & (p.pageSize - 1)) === 0)) throw new Error("paging: pageSize must be a power of two");
    if (Math.floor(p.vaddr / p.pageSize) >= p.table.length) throw new Error("paging: vaddr beyond the table");
  },
  initial: () => ({ vpn: "", offset: "", paddr: "", fault: false }),
  check(p, g, r) {
    const want = translate(p);
    const vpnOk = Number(r?.vpn) === want.vpn, offOk = Number(r?.offset) === want.offset;
    const tail = want.fault ? r?.fault === true : r?.fault !== true && Number(r?.paddr) === want.paddr;
    return ok(vpnOk && offOk && tail, { want, vpnOk, offOk, tailOk: tail });
  },
};

// ---------- threads: you are the scheduler of a few threads sharing memory ----------
// Step language (one atomic step per line): "a = <expr>" with + - and integers over shared or local
// names; "lock m" / "unlock m"; "wait s" / "signal s" (counting semaphores).
const STEP = /^(?:(\w+)\s*=\s*(.+)|(lock|unlock|wait|signal)\s+(\w+))$/;
function evalSimple(expr, env) {
  const toks = expr.replace(/\s+/g, "").match(/[+-]?[^+-]+/g) || [];
  return toks.reduce((acc, t) => {
    const sign = t[0] === "-" ? -1 : 1;
    const body = t.replace(/^[+-]/, "");
    const v = /^\d+$/.test(body) ? Number(body) : env(body);
    return acc + sign * v;
  }, 0);
}
export function threadsInit(p) {
  return {
    shared: { ...(p.shared || {}) },
    locks: Object.fromEntries((p.locks || []).map((m) => [m, null])),
    sems: { ...(p.sems || {}) },
    pc: p.threads.map(() => 0),
    locals: p.threads.map((t) => ({ ...(t.locals || {}) })),
  };
}
const cloneState = (s) => JSON.parse(JSON.stringify(s));
export function canStep(p, s, ti) {
  const th = p.threads[ti];
  if (s.pc[ti] >= th.steps.length) return false;
  const m = th.steps[s.pc[ti]].trim().match(STEP);
  if (m[3] === "lock") return s.locks[m[4]] === null;
  if (m[3] === "wait") return s.sems[m[4]] > 0;
  if (m[3] === "unlock") return s.locks[m[4]] === ti;
  return true;
}
export function stepThread(p, s0, ti) {
  const s = cloneState(s0);
  const line = p.threads[ti].steps[s.pc[ti]].trim();
  const m = line.match(STEP);
  const lookup = (name) => (name in s.locals[ti] ? s.locals[ti][name] : name in s.shared ? s.shared[name] : (() => { throw new Error(`threads: unknown name ${name}`); })());
  if (m[1]) {
    const v = evalSimple(m[2], lookup);
    if (m[1] in s.locals[ti]) s.locals[ti][m[1]] = v; else s.shared[m[1]] = v;
  } else if (m[3] === "lock") s.locks[m[4]] = ti;
  else if (m[3] === "unlock") s.locks[m[4]] = null;
  else if (m[3] === "wait") s.sems[m[4]]--;
  else if (m[3] === "signal") s.sems[m[4]]++;
  s.pc[ti]++;
  return s;
}
const finished = (p, s) => s.pc.every((pc, i) => pc >= p.threads[i].steps.length);
const deadlocked = (p, s) => !finished(p, s) && p.threads.every((_, i) => !canStep(p, s, i));
function goalMet(p, g, s) {
  if (g.deadlock) return deadlocked(p, s);
  if (!finished(p, s)) return false;
  return Object.entries(g.final || {}).every(([k, v]) => s.shared[k] === v);
}
export function replayThreads(p, choices) {
  let s = threadsInit(p);
  for (const ti of choices) {
    if (!canStep(p, s, ti)) return { state: s, error: `第 ${ti + 1} 个线程此刻不能执行` };
    s = stepThread(p, s, ti);
  }
  return { state: s };
}
// Exhaustive search over interleavings (authoring check: is the goal reachable at all?)
export function goalReachable(p, g, limit = 200000) {
  const seen = new Set();
  const stack = [threadsInit(p)];
  while (stack.length) {
    const s = stack.pop();
    const key = JSON.stringify(s);
    if (seen.has(key)) continue;
    seen.add(key);
    if (seen.size > limit) throw new Error("threads: state space too large");
    if (goalMet(p, g, s)) return true;
    for (let i = 0; i < p.threads.length; i++) if (canStep(p, s, i)) stack.push(stepThread(p, s, i));
  }
  return false;
}
export const threads = {
  name: "threads",
  validate(p, g) {
    for (const t of p.threads) for (const line of t.steps) if (!STEP.test(line.trim())) throw new Error(`threads: cannot read step "${line}"`);
    if (!g.final && !g.deadlock) throw new Error("threads: goal needs final or deadlock");
    if (!goalReachable(p, g)) throw new Error("threads: goal is not reachable by any interleaving");
  },
  initial: () => [],
  check(p, g, r) {
    const res = replayThreads(p, r || []);
    if (res.error) return ok(false, res);
    return ok(goalMet(p, g, res.state), { state: res.state, finished: finished(p, res.state), deadlocked: deadlocked(p, res.state) });
  },
};

// ---------- replace: you are the page-replacement policy ----------
// params: { frames: 3, refs: [7, 0, 1, …], policy: FIFO | LRU | OPT }. A hit, or a miss while a frame is
// still free, needs no decision; at a miss with every frame full the player picks the page to evict.
// Response: the evicted pages in order. FIFO evicts the page that came in earliest, LRU the one used
// longest ago; OPT accepts any page whose next use is furthest away (never used again = furthest).
export function replaceVictims(p, frames, t, loaded, used) {
  const pages = frames.filter((x) => x !== null);
  if (p.policy === "FIFO") return [pages.reduce((a, b) => (loaded[b] < loaded[a] ? b : a))];
  if (p.policy === "LRU") return [pages.reduce((a, b) => (used[b] < used[a] ? b : a))];
  const next = (pg) => { const k = p.refs.indexOf(pg, t + 1); return k === -1 ? Infinity : k; };
  const far = Math.max(...pages.map(next));
  return pages.filter((pg) => next(pg) === far);
}
// Replays references with the given evictions. Returns the per-reference rows the view draws, how many
// references are done, and either `pending` (the index waiting for a decision) or `error`.
export function replaceRun(p, evictions = [], choose = null) {
  const frames = Array(p.frames).fill(null), loaded = {}, used = {}, rows = [];
  let k = 0, misses = 0;
  for (let t = 0; t < p.refs.length; t++) {
    const pg = p.refs[t];
    let evicted = null, hit = frames.includes(pg);
    if (!hit) {
      misses++;
      let slot = frames.indexOf(null);
      if (slot === -1) {
        const allowed = replaceVictims(p, frames, t, loaded, used);
        const pick = choose ? choose(allowed) : evictions[k];
        if (pick === undefined) return { rows, done: t, misses: misses - 1, pending: t, allowed, frames: [...frames] };
        k++;
        if (!frames.includes(pick)) return { rows, done: t, misses, error: `${pick} 不在内存里`, frames: [...frames] };
        if (!allowed.includes(pick)) return { rows, done: t, misses, error: `${p.policy} 这一步不会换出 ${pick}`, allowed, frames: [...frames] };
        slot = frames.indexOf(pick);
        evicted = pick;
      }
      frames[slot] = pg;
      loaded[pg] = t;
    }
    used[pg] = t;
    rows.push({ ref: pg, hit, evicted, frames: [...frames] });
  }
  return { rows, done: p.refs.length, misses, hits: p.refs.length - misses, frames: [...frames] };
}
export const replace = {
  name: "replace",
  validate(p) {
    if (!["FIFO", "LRU", "OPT"].includes(p.policy)) throw new Error("replace: policy must be FIFO|LRU|OPT");
    if (!(Number.isInteger(p.frames) && p.frames >= 1 && p.frames <= 6)) throw new Error("replace: frames must be 1..6");
    if (!Array.isArray(p.refs) || !p.refs.length || p.refs.length > 24) throw new Error("replace: refs must be 1..24 pages");
  },
  initial: () => [],
  check(p, g, r) {
    const res = replaceRun(p, Array.isArray(r) ? r : []);
    const done = res.done === p.refs.length && !res.error;
    const okMisses = g.misses === undefined || res.misses === g.misses;
    return ok(done && okMisses, res);
  },
};

export default [bits, stackqueue, hash, scheduler, paging, threads, replace];
