// Shared by tests/e2e.mjs and tests/phone-fit.mjs: answer the item on screen and walk a lesson
// (or any StepPlayer flow) to its end.
import { Marked } from "marked";
import markedKatex from "marked-katex-extension";

const md = new Marked(markedKatex({ throwOnError: false, nonStandard: true }));

// Text the page shows for a Markdown snippet (same renderer and options as src/game/ui/md.jsx).
export const shown = (p, text) => p.evaluate((html) => { const d = document.createElement("div"); d.innerHTML = html; return d.textContent.trim(); }, md.parseInline(String(text)));

export async function answerCorrectly(p, item) {
  const q = ".lcard";
  if (item.type === "choice") {
    const texts = await p.$$eval(`${q} .option .otext`, (els) => els.map((e) => e.textContent.trim()));
    for (const o of item.options) if (o.correct) {
      const k = texts.indexOf(await shown(p, o.text));
      if (k < 0) return false;
      await p.locator(`${q} .option`).nth(k).click();
    }
    return true;
  }
  if (item.type === "number") { await p.fill(`${q} .answer-line input`, String(item.answer)); return true; }
  if (item.type === "text") { await p.fill(`${q} .answer-line input`, item.answers[0]); return true; }
  if (item.type === "order") {
    // Whole-text match, like match pairs below: a step can be part of another ("log n" in "n log n").
    for (const step of item.steps) {
      const want = await shown(p, step);
      const chips = p.locator(`${q} .order-pool .chip`);
      const n = await chips.count();
      let hit = false;
      for (let i = 0; i < n && !hit; i++) if ((await chips.nth(i).textContent()).trim() === want) { await chips.nth(i).click(); hit = true; }
      if (!hit) return false;
    }
    return true;
  }
  if (item.type === "match") {
    for (const pair of item.pairs) {
      const want = await shown(p, pair[1]);
      const chips = p.locator(`${q} .match-right .chip:not(.used)`);
      const n = await chips.count();
      for (let i = 0; i < n; i++) if ((await chips.nth(i).textContent()).trim() === want) { await chips.nth(i).click(); break; }
    }
    return true;
  }
  if (item.type === "sim" && item.sim === "plot" && item.params.mode === "riemann") {
    await p.locator(q + ' .sim-plot input[type="range"]').fill(String(item.solution.n));
    return true;
  }
  if (item.type === "sim" && item.sim === "threads") {
    for (const i of item.solution) await p.locator(q + " .sim-threads .thread button").nth(i).click();
    return true;
  }
  if (item.type === "sim" && item.sim === "graph" && Array.isArray(item.solution)) {
    const buttons = p.locator(q + " .sim-graph .btns");
    for (const id of item.solution) await buttons.getByRole("button", { name: id, exact: true }).click();
    return true;
  }
  return false;
}

// Marks every lesson of every pack finished (keeps what is already there) and reloads: the 实验室 then
// lists every experiment.
export async function finishAllLessons(p, packs) {
  await p.evaluate((keys) => {
    const key = "cs-math-skill-game/progress", s = JSON.parse(localStorage.getItem(key)), at = new Date().toISOString();
    for (const k of keys) s.lessons[k] ||= { done: at, stars: 3, best: 1, attempts: 1 };
    localStorage.setItem(key, JSON.stringify(s));
  }, Object.entries(packs).flatMap(([skill, pack]) => pack.lessons.map((l) => `${skill}/${l.id}`)));
  await p.reload();
}

// Any input at all for sims (and as a fallback): enough to reach the next step.
export async function answerAnything(p) {
  const q = ".lcard";
  if (await p.$(`${q} .option`)) await p.click(`${q} .option`);
  else if (await p.$(`${q} .order-pool .chip`)) { while (await p.$(`${q} .order-pool .chip`)) await p.click(`${q} .order-pool .chip`); }
  else if (await p.$(`${q} .match-right .chip`)) { const n = (await p.$$(`${q} .match-left li`)).length; for (let i = 0; i < n; i++) await p.click(`${q} .match-right .chip:not(.used)`); }
  else if (await p.$(`${q} .gcell`)) { const cols = await p.$$eval(`${q} .grow:nth-of-type(2) .gcell`, (c) => c.length); for (let t = 0; t < cols; t++) await p.locator(`${q} .grow`).nth(1).locator(".gcell").nth(t).click(); }
  else if (await p.$(`${q} input[type=text], ${q} textarea`)) { for (const el of await p.$$(`${q} input[type=text], ${q} textarea`)) await el.fill("1"); }
  else if (await p.$(`${q} .bit`)) await p.click(`${q} .bit`);
  else if (await p.$(`${q} .sim .btn.small:not([disabled])`)) await p.click(`${q} .sim .btn.small:not([disabled])`);
}

// Walks a lesson to its summary (`.celebrate`, or `done` for other flows). With `lesson`, supported
// items are answered correctly and must be graded correct on the first try (else pushed to `errors`).
// `onStep(label)` runs on every screen before its bottom button is pressed (label: 检查/继续/…).
export async function playLesson(p, tag, lesson, { errors = [], onStep, done = ".celebrate" } = {}) {
  const byId = lesson ? Object.fromEntries(lesson.flow.filter((s) => s.item).map((s) => [s.item.id, s.item])) : {};
  const seen = new Set();
  for (let guard = 0; guard < 80; guard++) {
    if (await p.$(done)) return true;
    const btn = await p.$(".answer-bar .inner > .btn");
    if (!btn) { await p.waitForTimeout(100); continue; }
    const label = (await btn.textContent()).trim();
    if (label === "检查") {
      const id = await p.$eval(".lcard", (el) => el.dataset.item || "");
      const item = byId[id];
      const firstTime = !seen.has(id);
      seen.add(id);
      let mode = "any";
      if (item && firstTime && (await answerCorrectly(p, item))) mode = "correct";
      if (await btn.isDisabled()) await answerAnything(p);
      if (await btn.isDisabled()) { errors.push(`[${tag}] could not answer item ${id}`); return false; }
      if (onStep) await onStep("answer " + id);
      await btn.click();
      if (mode === "correct" && !(await p.$(".lcard.is-good"))) errors.push(`[${tag}] item ${id} (${item.type}): the correct answer was graded wrong`);
      if (onStep) await onStep("verdict " + id);
      continue;
    }
    if (onStep) await onStep(label);
    await btn.click();
  }
  return !!(await p.$(done));
}

// Which lessons a run walks. Every lesson goes through the same input components, so a routine run
// takes the lessons that between them show every item type and every interactive component (with its
// mode), plus the 3 with the widest content (longest line of code, option or sortable step: what
// breaks phone layouts). FULL=1 walks all of them: before a release or after changing lesson content.
// → { [skill]: lessons[] } in pack order.
export function lessonsToWalk(packs, full = process.env.FULL === "1") {
  const out = Object.fromEntries(Object.keys(packs).map((k) => [k, []]));
  const all = Object.entries(packs).flatMap(([skill, p]) => p.lessons.map((l, i) => ({ skill, l, i })));
  if (full) { for (const x of all) out[x.skill].push(x.l); return out; }
  const keys = (l) => l.flow.filter((s) => s.item).map(({ item }) => item.type === "sim" ? `sim:${item.sim}:${item.params?.mode || item.params?.policy || ""}` : `type:${item.type}`);
  // prose wraps; code does not: measure code-block lines, inline code and sortable steps
  const widest = (l) => {
    let w = 0;
    const code = (s) => [...s.matchAll(/```[^\n]*\n([\s\S]*?)```/g)].flatMap((m) => m[1].split("\n")).concat([...s.matchAll(/`([^`\n]+)`/g)].map((m) => m[1]));
    JSON.stringify(l.flow, (k, v) => { if (typeof v === "string") for (const line of code(v)) w = Math.max(w, line.length); return v; });
    for (const s of l.flow) for (const step of s.item?.type === "order" ? s.item.steps : []) w = Math.max(w, ...String(step).split("\n").map((x) => x.length));
    return w;
  };
  const take = new Set(), seen = new Set();
  for (const x of all) if (keys(x.l).some((k) => !seen.has(k))) { take.add(x); keys(x.l).forEach((k) => seen.add(k)); }
  for (const x of [...all].sort((a, b) => widest(b.l) - widest(a.l)).slice(0, 3)) take.add(x);
  for (const x of all) if (take.has(x)) out[x.skill].push(x.l);
  return out;
}
