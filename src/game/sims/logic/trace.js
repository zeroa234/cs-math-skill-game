// Code-stepping sim: the player steps through a real Python run (steps recorded at build time by
// scripts/lib/pytrace.py) and predicts values at marked moments.
//
// Authoring: params { code, stdin? }, goal { ask: [{ line, var, hit? }] } — "the value of `var` right
// after line `line` runs for the `hit`-th time (default 1)". The build adds params.steps and
// goal.answers, so checking needs no Python.

// Index of the step right after the hit-th execution of `line`, in the same frame.
export function afterLine(steps, line, hit = 1) {
  let seen = 0;
  for (let i = 0; i < steps.length; i++) {
    if (steps[i].line !== line) continue;
    if (++seen < hit) continue;
    const frame = steps[i].frame;
    for (let j = i + 1; j < steps.length; j++) if (steps[j].frame === frame) return j;
    return -1;
  }
  return -1;
}

export function answersFor(steps, ask) {
  return ask.map((a) => {
    const j = afterLine(steps, a.line, a.hit || 1);
    if (j < 0) throw new Error(`trace: line ${a.line} (hit ${a.hit || 1}) never runs`);
    const v = a.var === "@out" ? steps[j].out : steps[j].vars[a.var];
    if (v === undefined) throw new Error(`trace: ${a.var} is not defined after line ${a.line}`);
    return v;
  });
}

const norm = (s) => String(s ?? "").trim().replace(/^["'](.*)["']$/s, "$1").replace(/\s+/g, " ");
export const trace = {
  name: "trace",
  validate(p, g) {
    if (!p.steps) throw new Error("trace: params.steps missing (run the build, it records them)");
    if (!g.ask?.length) throw new Error("trace: goal.ask needs at least one question");
    g.answers = answersFor(p.steps, g.ask);
  },
  initial: (p, g) => ({ answers: g.ask.map(() => "") }),
  check(p, g, r) {
    const want = g.answers || answersFor(p.steps, g.ask);
    const each = want.map((w, i) => norm(r?.answers?.[i]) === norm(w));
    return { correct: each.every(Boolean), detail: { each, want } };
  },
};

export default [trace];
