// Content-pack validation shared by scripts/build-data.mjs and scripts/check-pack.mjs.
// Checks: JSON schema; lesson chapters exist and every core chapter has a lesson; unique ids;
// choice items have a correct option; number/text answers present; every sim's params/goal pass the
// sim's own validator; graded sims ship a `solution` that passes the checker; trace sims get their
// steps recorded by running the code in Python.
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import * as yaml from "js-yaml";
import Ajv from "ajv";
import { SIMS } from "../../src/game/sims/logic/index.js";
import { checkItem } from "../../src/game/core/check.js";
import { normalizeLesson } from "../../src/game/core/lesson.js";
import { beginnerIssues } from "./beginner.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const ajv = new Ajv({ allErrors: true, strict: false });
const validateSchema = ajv.compile(JSON.parse(fs.readFileSync(path.join(ROOT, "data/content.schema.json"), "utf8")));

export function runPyTrace(code, stdin = "") {
  // -X utf8: -I ignores PYTHONIOENCODING, and traced code with Chinese text fails on Windows without UTF-8 mode
  const r = spawnSync("python", ["-I", "-X", "utf8", path.join(ROOT, "scripts/lib/pytrace.py")], { input: JSON.stringify({ code, stdin }), encoding: "utf8", env: { ...process.env, PYTHONIOENCODING: "utf-8" } });
  if (r.status !== 0) throw new Error(`pytrace failed: ${r.stderr}`);
  return JSON.parse(r.stdout);
}

// One-line flow mappings like `- { text: a, why: b }` silently split on ASCII commas inside a value;
// report those lines with a readable message before the schema complains about "additional properties".
export function lintFlowValues(text) {
  const out = [];
  text.split("\n").forEach((line, i) => {
    const m = line.match(/^\s*- \{ (.*) \}\s*$/);
    if (!m) return;
    for (const part of m[1].split(/,\s*(?=(?:text|why|correct):)/)) {
      const kv = part.match(/^(text|why|correct):\s*(.*)$/);
      if (kv && !/^(["']).*\1$/.test(kv[2]) && /[[\]{},]|: |#/.test(kv[2])) out.push(`line ${i + 1}: unquoted ${kv[1]} contains , [ ] { } or ": " — wrap it in double quotes`);
    }
  });
  return out;
}

export const loadPack = (file) => {
  const text = fs.readFileSync(file, "utf8");
  const lint = lintFlowValues(text);
  if (lint.length) throw new Error(lint.join("; "));
  return yaml.load(text);
};

// What a skill's required prerequisites' packs define: { term: definition }. A pack may use these terms
// without defining them again, and they get look-up buttons in it too.
export function inheritedGlossary(skillId, byId, packsBySkill) {
  const seen = new Set(), terms = {};
  const walk = (id) => {
    for (const r of byId[id]?.required || []) {
      if (seen.has(r.id)) continue;
      seen.add(r.id);
      for (const t of packsBySkill[r.id]?.terms || []) terms[t.term] ??= t.def;
      walk(r.id);
    }
  };
  walk(skillId);
  return terms;
}
export const inheritedTerms = (skillId, byId, packsBySkill) => new Set(Object.keys(inheritedGlossary(skillId, byId, packsBySkill)));

// Lessons in the order the game plays them: by chapter, then as written.
export const playOrder = (pack, skill) => {
  const no = new Map(skill.chapters.map((c) => [c.title, c.no]));
  return pack.lessons.map(normalizeLesson).sort((a, b) => no.get(a.chapter) - no.get(b.chapter));
};

// Returns a list of error strings; mutates trace items to carry recorded steps and answers.
// ctx: { byId, packsBySkill } enables the beginner standard's cross-pack term check.
export function validatePack(pack, skill, label = pack?.skill, ctx = {}) {
  const errs = [];
  const e = (m) => errs.push(`${label}: ${m}`);
  if (!validateSchema(pack)) { e(ajv.errorsText(validateSchema.errors, { separator: "\n  " })); return errs; }
  if (!skill) { e(`unknown skill ${pack.skill}`); return errs; }
  // YAML double quotes turn LaTeX "\frac" into a form feed + "rac", "\to" into a tab + "o", etc.
  const walk = (v, where) => {
    if (typeof v === "string") {
      const bad = v.match(/[\x00-\x08\x0b\x0c\x0e-\x1f]|\t(?=[a-z])/);
      if (bad && !/\.code$|\.params\.code$/.test(where)) e(`${where}: control character U+${bad[0].charCodeAt(0).toString(16).padStart(4, "0")} near "${v.slice(Math.max(0, bad.index - 12), bad.index + 12).replace(/[\x00-\x1f]/g, "¤")}" — a LaTeX backslash inside "double quotes"? use single quotes or a | block`);
    } else if (Array.isArray(v)) v.forEach((x, i) => walk(x, `${where}[${i}]`));
    else if (v && typeof v === "object") for (const [k, x] of Object.entries(v)) if (k !== "steps") walk(x, `${where}.${k}`);
  };
  walk(pack, "pack");
  const titles = skill.chapters.map((c) => c.title);
  for (const l of pack.lessons) if (!titles.includes(l.chapter)) e(`lesson "${l.id}" names chapter "${l.chapter}" — must be one of: ${titles.join(" / ")}`);
  const missing = skill.chapters.filter((c) => c.stage === "core" && !pack.lessons.some((l) => l.chapter === c.title)).map((c) => c.title);
  if (missing.length) e(`no lesson for core chapter(s): ${missing.join(" / ")}`);
  const lessonIds = new Set();
  const items = [];
  const lessons = pack.lessons.map(normalizeLesson);
  for (const l of lessons) {
    if (lessonIds.has(l.id)) e(`duplicate lesson id ${l.id}`);
    lessonIds.add(l.id);
    if (l.items.length < 2) e(`${l.id}: needs at least 2 graded items`);
    const ids = new Set();
    for (const it of l.flow.filter((s) => s.item).map((s) => s.item)) {
      if (ids.has(it.id)) e(`duplicate item id ${l.id}/${it.id}`);
      ids.add(it.id);
      items.push([`${l.id}/${it.id}`, it]);
    }
    for (const c of l.flow.filter((s) => s.card).map((s) => s.card)) {
      if (!c.sim) continue;
      if (!SIMS[c.sim.name]) { e(`${l.id}: card uses unknown sim ${c.sim.name}`); continue; }
      if (c.sim.name === "trace") {
        try {
          const run = runPyTrace(c.sim.params.code, c.sim.params.stdin);
          if (run.error && !c.sim.params.expectError) e(`${l.id}: card trace raised ${run.error}`);
          c.sim.params.steps = run.steps;
        } catch (err) { e(`${l.id}: card trace: ${err.message}`); }
      }
    }
  }
  // Review cards show one item on its own, weeks later: a prompt that leans on the previous item or
  // a card ("接上题", "上面那个") must either be rewritten to stand alone or opt out of review.
  for (const l of lessons) for (const it of l.items) {
    if (it.review === false || (it.type === "sim" && it.review !== true)) continue;
    if (/接上题|上一题|上题|同一题|上面那|上面的|上例|前一题|刚才/.test(it.prompt)) e(`${l.id}/${it.id}: prompt depends on earlier context ("${it.prompt.slice(0, 30)}…") — make it self-contained or set review: false`);
  }
  for (const it of pack.boss?.items || []) items.push([`boss/${it.id}`, it]);
  for (const m of beginnerIssues(pack, playOrder(pack, skill), { inherited: ctx.byId ? inheritedTerms(skill.id, ctx.byId, ctx.packsBySkill || {}) : new Set(), coreChapters: skill.chapters.filter((c) => c.stage === "core").length })) e(m);
  for (const [key, it] of items) {
    try {
      if (it.type === "choice") {
        const n = it.options.filter((o) => o.correct).length;
        if (!n) e(`${key}: no correct option`);
        if (!it.multi && n > 1) e(`${key}: ${n} correct options but multi is not set`);
      }
      if (it.type === "match" && new Set(it.pairs.map((p) => p[1])).size !== it.pairs.length) e(`${key}: right-hand texts must be distinct`);
      if (it.type === "order" && new Set(it.steps).size !== it.steps.length) e(`${key}: steps must be distinct`);
      if (it.type === "sim") {
        const sim = SIMS[it.sim];
        if (!sim) { e(`${key}: unknown sim ${it.sim}`); continue; }
        if (it.sim === "trace" && it.params?.code) {
          const run = runPyTrace(it.params.code, it.params.stdin);
          if (run.error && !it.params.expectError) e(`${key}: traced code raised ${run.error}`);
          it.params.steps = run.steps;
        }
        sim.validate(it.params || {}, it.goal || {});
        if (it.sim !== "trace") {
          if (it.solution === undefined) e(`${key}: graded sim needs a solution`);
          else if (!checkItem(it, it.solution).correct) e(`${key}: the solution does not pass the checker (${JSON.stringify(checkItem(it, it.solution).detail).slice(0, 200)})`);
        }
      }
      if (it.type === "number" && !Number.isFinite(it.answer)) e(`${key}: answer must be a finite number`);
    } catch (err) {
      e(`${key}: ${err.message}`);
    }
  }
  return errs;
}
