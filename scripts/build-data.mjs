// Builds the game's skill data from the cs-math-skill-tree prototype (read-only input).
// usage: node scripts/build-data.mjs [--tree <path-to-cs-math-skill-tree>] [--skip-invalid-packs]
//
// What it does (all rules are data-driven, no per-skill constants):
//  1. Drops the cross-domain lane X (交叉应用与前沿专题) and every edge touching it.
//  2. Adds game-side extension skills from data/extra-skills.yaml (each must carry course evidence).
//  3. Turns each skill's must-learn topics into chapters numbered 1..n, ordered by the teaching
//     order of the skill's primary source (see orderChapters), and renumbers the knowledge-map
//     outline 1..n while keeping the textbook's own section number as a "source ref" tag.
//  4. Merges content packs from data/content/*.yaml (validated against data/content.schema.json).
// Writes src/gen/tree.json, src/gen/content.json, src/web/outlines.js and reports/chapter-order.md.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import * as yaml from "js-yaml";
import { loadPack, validatePack, inheritedGlossary } from "./lib/packs.mjs";
import { leanLesson, normalizeLesson } from "../src/game/core/lesson.js";
import { resolveTerms } from "./lib/beginner.mjs";
import { coverageIssues, readCoverageTable } from "./lib/coverage.mjs";
import { sectionKey, cmpKey } from "./lib/sections.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const argTree = process.argv.indexOf("--tree");
const TREE = path.resolve(argTree > 0 ? process.argv[argTree + 1] : path.join(ROOT, "../cs-math-skill-tree"));
const EXCLUDED_DOMAINS = new Set(["X"]);
// --skip-invalid-packs: while content is being written, leave failing packs out instead of failing.
const SKIP_INVALID = process.argv.includes("--skip-invalid-packs");

const readJson = (p) => JSON.parse(fs.readFileSync(p, "utf8"));
const src = readJson(path.join(TREE, "output/skilltree.json"));
const outlines = readJson(path.join(TREE, "output/outlines.json"));
const errors = [];
const fail = (msg) => errors.push(msg);

// ---------- chapter ordering ----------
// Rule: order the must-learn topics by where the skill's primary teaching source first covers them.
// Only references marked extent "covered" count. A primary source (zh or en) qualifies only when it
// places EVERY core topic (each has a parsed section number) and the numbers tell the topics apart
// (distinct numbers >= half the topic count; a course that files 7 of 9 topics under one chapter
// says nothing about their order). Partial evidence never reshuffles the list: moving the topics we
// can place around the ones we cannot put e.g. shortest paths before greedy/DP. Ties between a zh and
// an en source go to zh (the game's language). Extension-stage topics go last. No qualifying source →
// the original order, which is the skill description's own order.
function orderChapters(skill) {
  const lp = skill.learningPath;
  const topics = lp.topics.map((t, i) => ({ ...t, orig: i }));
  const core = topics.filter((t) => t.stage !== "extension");
  const candidates = lp.sources.filter((s) => s.role === "primary").sort((a, b) => (a.lang === "zh" ? -1 : 1) - (b.lang === "zh" ? -1 : 1));
  let best = null;
  for (const s of candidates) {
    const keyOf = (t) => {
      const refs = (t[s.lang] || []).filter((r) => r.source === s.key && r.extent === "covered").map((r) => sectionKey(r.section)).filter(Boolean);
      return refs.length ? refs.sort(cmpKey)[0] : null;
    };
    const keys = core.map(keyOf);
    if (keys.some((k) => !k)) continue;
    const distinct = new Set(keys.map((k) => k.join("."))).size;
    if (distinct < Math.ceil(core.length / 2)) continue;
    best = { source: s, keyOf };
    break;
  }
  let basis = "original";
  let ordered;
  if (best) {
    basis = best.source.key;
    ordered = topics
      .map((t) => ({ t, key: t.stage === "extension" ? null : best.keyOf(t) }))
      .sort((a, b) => (a.t.stage === "extension") - (b.t.stage === "extension") || (a.key && b.key ? cmpKey(a.key, b.key) : 0) || a.t.orig - b.t.orig)
      .map((x) => ({ ...x.t, sourceKey: x.key }));
  } else {
    ordered = [...topics].sort((a, b) => (a.stage === "extension") - (b.stage === "extension") || a.orig - b.orig);
  }
  return { basis, basisTitle: basis === "original" ? null : best.source.title, ordered };
}

// ---------- outline renumbering ----------
function renumberOutline(o) {
  if (!o) return null;
  const sections = (items, prefix = "") => items.map((it, i) => {
    const no = it.number || (prefix ? `${prefix}.${i + 1}` : String(i + 1));
    return { no, ...(it.src ? { src: it.src } : {}), sourceRef: it.ref || null,
      title: it.title, zh: it.zh, items: sections(it.items || [], no) };
  });
  return {
    sources: o.sources.map((s) => ({ key: s.key, kind: s.kind, title: s.title, by: s.by, year: s.year, url: s.url, why: s.why })),
    branches: sections(o.outline),
    fills: o.fills || o.gaps || null,
  };
}

// ---------- extension skills ----------
function loadExtras() {
  const p = path.join(ROOT, "data/extra-skills.yaml");
  if (!fs.existsSync(p)) return [];
  const doc = yaml.load(fs.readFileSync(p, "utf8")) || {};
  for (const s of doc.skills || []) {
    if (!s.evidence?.length) fail(`extra skill ${s.id}: needs at least one course evidence entry`);
    for (const e of s.evidence || []) if (!e.url || !e.quote) fail(`extra skill ${s.id}: evidence needs url and verbatim quote`);
  }
  return doc.skills || [];
}

// ---------- assemble ----------
const keep = src.skills.filter((s) => !EXCLUDED_DOMAINS.has(s.domain));
const keepIds = new Set(keep.map((s) => s.id));
const orderReport = [];
const skills = keep.map((s) => {
  const { basis, basisTitle, ordered } = orderChapters(s);
  const srcById = Object.fromEntries(s.learningPath.sources.map((x) => [x.key, x]));
  const chapters = ordered.map((t, i) => ({
    no: i + 1,
    title: t.topic,
    stage: t.stage,
    note: t.note || "",
    zh: t.zh.map((r) => ({ source: r.source, section: r.section, extent: r.extent })),
    en: t.en.map((r) => ({ source: r.source, section: r.section, extent: r.extent })),
  }));
  const moved = ordered.some((t, i) => t.orig !== i);
  orderReport.push({ id: s.id, name: s.name, basis, basisTitle, moved, before: s.learningPath.topics.map((t) => t.topic), after: ordered.map((t) => t.topic), keys: ordered.map((t) => t.sourceKey?.join(".") ?? "—") });
  const dropEdge = (list) => list.filter((r) => keepIds.has(r.id));
  return {
    id: s.id, name: s.name, en: s.en, domain: s.domain, lane: s.lane, step: s.step, x: s.x, y: s.y,
    optional: s.optional, scope: s.scope, desc: s.desc, levels: s.levels,
    required: dropEdge(s.required).map((r) => ({ id: r.id, why: r.why })),
    recommended: dropEdge(s.recommended).map((r) => ({ id: r.id, why: r.why })),
    unlocks: s.unlocks.filter((id) => keepIds.has(id)),
    reach: s.reach,
    prereqSummary: s.prereqSummary,
    courses: (s.courses || []).map((c) => ({ school: c.school, course: c.course, url: c.url, prereq: c.prereq_text, kind: c.prereq_kind })),
    chapterOrder: { basis, source: basisTitle },
    chapters,
    sources: s.learningPath.sources.map((x) => ({ key: x.key, lang: x.lang, role: x.role, title: x.title, url: x.url, tier: x.tier, free: x.free, access: x.access, publisher: x.publisher })),
    readingSteps: { zh: s.learningPath.routes?.zh?.steps || [], en: s.learningPath.routes?.en?.steps || [] },
    routeStatus: { zh: s.learningPath.routes?.zh?.status, en: s.learningPath.routes?.en?.status },
    exercise: s.exercise ? { question: s.exercise.question, answer: s.exercise.answer, covers: s.exercise.covers, minutes: s.exercise.time_min, level: s.exercise.level } : null,
    hasOutline: !!outlines[s.id],
    origin: "cs-math-skill-tree",
    _srcCheck: Object.keys(srcById).length,
  };
});

for (const e of loadExtras()) {
  if (keepIds.has(e.id)) { fail(`extra skill ${e.id} collides with an existing id`); continue; }
  skills.push({
    id: e.id, name: e.name, en: e.en, domain: e.domain, lane: e.lane, step: e.step ?? null, x: null, y: null,
    optional: !!e.optional, scope: e.scope || "", desc: e.desc, levels: e.levels || [1, 3],
    required: e.required || [], recommended: e.recommended || [], unlocks: [], reach: 0,
    prereqSummary: e.prereqSummary || "", courses: e.evidence.map((c) => ({ school: c.school, course: c.course, url: c.url, prereq: c.quote, kind: c.kind || "required", content: c.content || "" })),
    chapterOrder: { basis: "extension", source: e.chapterSource || null },
    chapters: (e.chapters || []).map((c, i) => ({ no: i + 1, title: c.title, stage: c.stage || "core", note: c.note || "", zh: c.zh || [], en: c.en || [] })),
    sources: e.sources || [], readingSteps: { zh: [], en: [] },
    routeStatus: {
      zh: (e.chapters || []).every((c) => (c.zh || []).some((r) => r.extent === "covered")) ? "complete" : "incomplete",
      en: (e.chapters || []).every((c) => (c.en || []).some((r) => r.extent === "covered")) ? "complete" : "incomplete",
    },
    exercise: null, hasOutline: false,
    origin: "game-extension", extensionNote: e.note || "",
  });
  keepIds.add(e.id);
}

// Graph checks: ids exist, no cycles; recompute unlocks and steps (extensions may add nodes).
const byId = Object.fromEntries(skills.map((s) => [s.id, s]));
for (const s of skills) for (const r of [...s.required, ...s.recommended]) if (!byId[r.id]) fail(`${s.id}: unknown prerequisite ${r.id}`);
for (const s of skills) s.unlocks = skills.filter((t) => t.required.some((r) => r.id === s.id)).map((t) => t.id);
const stepMemo = {};
const visiting = new Set();
function stepOf(id) {
  if (stepMemo[id]) return stepMemo[id];
  if (visiting.has(id)) { fail(`cycle through ${id}`); return 1; }
  visiting.add(id);
  const req = byId[id].required.filter((r) => byId[r.id]);
  const st = req.length ? 1 + Math.max(...req.map((r) => stepOf(r.id))) : 1;
  visiting.delete(id);
  return (stepMemo[id] = st);
}
for (const s of skills) {
  const st = stepOf(s.id);
  if (s.origin === "cs-math-skill-tree" && st !== s.step) fail(`${s.id}: step changed ${s.step} → ${st} after dropping X edges`);
  s.step = st;
  delete s._srcCheck;
}

// Extension skills get a map slot the same way the tree's layout spaces cards: x is the step column,
// y the free row (rows every 72 px from 16) of their lane in that column closest to the mean row of
// their required prerequisites in the same lane (ties → upper row).
const ROW0 = 16, ROW = 72;
for (const s of skills.filter((x) => x.origin === "game-extension")) {
  s.x = (s.step - 1) * src.meta.card.colW;
  const column = skills.filter((t) => t !== s && t.lane === s.lane && t.step === s.step && t.y != null).map((t) => t.y);
  const lanePre = s.required.map((r) => byId[r.id]).filter((t) => t.lane === s.lane);
  const target = lanePre.length ? lanePre.reduce((a, t) => a + t.y, 0) / lanePre.length : ROW0;
  const laneMax = Math.max(...skills.filter((t) => t.lane === s.lane && t.y != null).map((t) => t.y));
  let best = null;
  for (let y = ROW0; y <= laneMax + ROW; y += ROW) {
    if (column.some((cy) => Math.abs(cy - y) < src.meta.card.h)) continue;
    if (best === null || Math.abs(y - target) < Math.abs(best - target)) best = y;
  }
  s.y = best;
}

// KTH course pages as a second check: every prerequisite course must map to a skill inside the
// required closure of the course's own skill (or the skill itself).
const kthDoc = yaml.load(fs.readFileSync(path.join(ROOT, "data/kth-evidence.yaml"), "utf8"));
const closureOf = (id, acc = new Set()) => { if (acc.has(id)) return acc; acc.add(id); for (const r of byId[id].required) closureOf(r.id, acc); return acc; };
const kthRows = [];
for (const c of kthDoc.courses) {
  if (!byId[c.skill]) { fail(`kth ${c.code}: unknown skill ${c.skill}`); continue; }
  const closure = closureOf(c.skill);
  const needs = (c.needs || []).map((n) => {
    if (!byId[n.skill]) fail(`kth ${c.code}: unknown skill ${n.skill}`);
    return { ...n, inClosure: closure.has(n.skill) };
  });
  for (const id of c.covers || [c.skill]) {
    (byId[id].kth ||= []).push({ code: c.code, name: c.name, credits: c.credits, url: `https://www.kth.se/student/kurser/kurs/${c.code}?l=en`, quote: c.quote, fit: c.fit, note: c.note || "", needs, fetched: kthDoc.fetched });
  }
  kthRows.push({ c, needs });
}

// ---------- content packs ----------
const content = {};
const contentDir = path.join(ROOT, "data/content");
// Loaded first, validated second: the beginner standard lets a pack use terms its prerequisites define.
const loaded = (fs.existsSync(contentDir) ? fs.readdirSync(contentDir).filter((f) => f.endsWith(".yaml")).sort() : []).map((f) => [f, loadPack(path.join(contentDir, f))]);
const packsBySkill = Object.fromEntries(loaded.map(([, p]) => [p?.skill, p]));
for (const [f, pack] of loaded) {
  const errs = validatePack(pack, byId[pack?.skill], f, { byId, packsBySkill });
  if (errs.length && SKIP_INVALID) { console.warn(`skipped unfinished pack ${f}:\n  - ${errs.join("\n  - ")}`); continue; }
  if (errs.length) { errors.push(...errs); continue; }
  if (content[pack.skill]) { fail(`${f}: a second pack for ${pack.skill}`); continue; }
  // Runtime shape (core/lesson.js): lessons as flows, [[term]] resolved to its definition.
  const { lessons, boss } = resolveTerms(pack, pack.lessons.map(normalizeLesson), inheritedGlossary(pack.skill, byId, packsBySkill));
  // Knowledge-coverage rule C1: a pack counts as written only when its coverage table passes.
  const cov = coverageIssues(pack.skill, outlines[pack.skill], pack, readCoverageTable(path.join(ROOT, "reports/coverage", pack.skill + ".md")));
  content[pack.skill] = { ...pack, lessons: lessons.map(leanLesson), boss, coverage: !cov.issues.length };
}

// Routes (campaigns) are declared in data/routes.yaml: the author's own goals, the recommended
// routes and whether 自己定目标 is open. They come out as one flat list; an own route's id is
// "goal:<skill>", the same id a goal picked in the game gets, so both share one code path.
const routesDoc = yaml.load(fs.readFileSync(path.join(ROOT, "data/routes.yaml"), "utf8"));
const STATUS = new Set(["open", "dev"]);
const routes = [
  ...(routesDoc.own || []).map((r) => ({ id: "goal:" + r.goal, kind: "own", status: "open", goal: r.goal, was: r.was || [] })),
  ...(routesDoc.recommended || []).map((r) => ({ ...r, kind: "recommended" })),
];
const seenRoute = new Set();
for (const r of routes) {
  if (seenRoute.has(r.id)) fail(`route ${r.id}: listed twice`);
  seenRoute.add(r.id);
  for (const id of [r.goal, ...(r.also || [])]) if (!byId[id]) fail(`route ${r.id}: unknown goal ${id}`);
  if (!STATUS.has(r.status)) fail(`route ${r.id}: status must be open or dev`);
  if (r.kind === "recommended" && !(r.name && r.tagline && r.story && r.evidence)) fail(`route ${r.id}: a recommended route needs name, tagline, story and evidence`);
}
if (!STATUS.has(routesDoc.customGoals)) fail("routes.yaml: customGoals must be open or dev");

if (errors.length) {
  console.error("build-data failed:\n- " + errors.join("\n- "));
  process.exit(1);
}

const lanes = src.lanes.filter((l) => !EXCLUDED_DOMAINS.has(l.domain)).map((l) => ({ id: l.id, domain: l.domain, name: l.name, short: l.short, en: l.en, color: l.color, count: skills.filter((s) => s.lane === l.id).length }));
const tree = {
  meta: {
    builtFrom: "cs-math-skill-tree " + src.meta.built,
    skills: skills.length,
    excludedDomains: [...EXCLUDED_DOMAINS],
    requiredEdges: skills.reduce((n, s) => n + s.required.length, 0),
    recommendedEdges: skills.reduce((n, s) => n + s.recommended.length, 0),
    card: src.meta.card,
  },
  levels: src.depths,
  lanes,
  routes,
  customGoals: routesDoc.customGoals,
  skills,
};
fs.mkdirSync(path.join(ROOT, "src/gen"), { recursive: true });
fs.writeFileSync(path.join(ROOT, "src/gen/tree.json"), JSON.stringify(tree));
fs.writeFileSync(path.join(ROOT, "src/gen/content.json"), JSON.stringify(content));

// Background music (data/music.yaml): the game gets the styles and the credits. Every track a style
// names must be listed and encoded (node scripts/music/encode-music.mjs).
const musicDoc = yaml.load(fs.readFileSync(path.join(ROOT, "data/music.yaml"), "utf8"));
const SCENES = ["title", "explore", "focus", "challenge"];
for (const s of musicDoc.styles) {
  for (const scene of SCENES) if (!s.scenes[scene]?.length) throw new Error(`data/music.yaml: style ${s.id} has no ${scene} tracks`);
  for (const [scene, ids] of Object.entries(s.scenes)) for (const id of ids) {
    if (!SCENES.includes(scene)) throw new Error(`data/music.yaml: style ${s.id} has an unknown scene ${scene}`);
    if (!musicDoc.tracks[id]) throw new Error(`data/music.yaml: style ${s.id} names an unlisted track ${id}`);
    if (!fs.existsSync(path.join(ROOT, "assets/music", `${id}.ogg`))) throw new Error(`assets/music/${id}.ogg is missing: run node scripts/music/encode-music.mjs`);
  }
}
const usedPacks = new Set(musicDoc.styles.flatMap((s) => Object.values(s.scenes).flat()).map((id) => musicDoc.tracks[id].pack));
const music = {
  styles: musicDoc.styles,
  packs: Object.entries(musicDoc.packs).filter(([id]) => usedPacks.has(id)).map(([id, p]) => ({ id, name: p.name, author: p.author, license: p.license, page: p.page })),
};
fs.writeFileSync(path.join(ROOT, "src/gen/music.json"), JSON.stringify(music));

const outl = {};
for (const s of skills) if (outlines[s.id]) outl[s.id] = renumberOutline(outlines[s.id]);
fs.mkdirSync(path.join(ROOT, "src/web"), { recursive: true });
fs.writeFileSync(path.join(ROOT, "src/web/outlines.js"), "window.__OUTLINES__=" + JSON.stringify(outl) + ";\n");

// Report: which skills changed chapter order and on what basis.
const moved = orderReport.filter((r) => r.moved);
const basisCount = orderReport.reduce((m, r) => ((m[r.basis === "original" ? "original" : r.basis.slice(0, 2)] = (m[r.basis === "original" ? "original" : r.basis.slice(0, 2)] || 0) + 1), m), {});
let md = `# 章节顺序（自动生成）\n\n由 \`scripts/build-data.mjs\` 生成，请勿手改。\n\n规则：每个技能的“必学知识项”就是游戏里的章，编号 1…n。顺序取该技能某个主来源（中文或英文主来源，都合格时取中文）里第一次讲到它的章节号（只算标为 covered 的对应章节；“20 页”这类页数、年份、“(1)–(3)”这类讲次分段不算章节号）。这个主来源必须给**每一个**必学知识项都找到章节号，而且章节号要能区分它们（不同章节号的个数不少于知识项数的一半），否则保留技能简介里的原顺序：只有部分知识项能定位时重排，会把能定位的项挪到不能定位的项前面（例如把最短路排到贪心和动态规划之前）。extension（选学）知识项放最后。教材自己的章节号（如 OpenStax 2.2）只作为“来源章节”标签显示，不再当作游戏章节号。\n\n- 技能数：${orderReport.length}\n- 依据：${Object.entries(basisCount).map(([k, v]) => `${k} ${v}`).join("，")}\n- 顺序有变化：${moved.length}\n\n| 技能 | 依据 | 原顺序 | 新顺序（来源章节号） |\n|---|---|---|---|\n`;
for (const r of moved) md += `| ${r.id} ${r.name} | ${r.basis}：${r.basisTitle || ""} | ${r.before.join(" / ")} | ${r.after.map((t, i) => `${i + 1}. ${t}（${r.keys[i]}）`).join(" / ")} |\n`;
fs.mkdirSync(path.join(ROOT, "reports"), { recursive: true });
fs.writeFileSync(path.join(ROOT, "reports/chapter-order.md"), md);

let km = `# KTH 先修交叉核对（自动生成）\n\n由 \`scripts/build-data.mjs\` 依据 \`data/kth-evidence.yaml\` 生成，请勿手改。KTH 课程页 “Specific prerequisites” 原文读取于 ${kthDoc.fetched}。\n\n“一致”表示 KTH 要求的先修课对应的技能，落在技能树为该技能要求的必须前置链里（含它自己）。\n\n| KTH 课程 | 对应技能 | KTH 要求的先修 → 技能 | 一致 |\n|---|---|---|---|\n`;
for (const { c, needs } of kthRows) {
  km += `| [${c.code} ${c.name}](https://www.kth.se/student/kurser/kurs/${c.code}?l=en) | ${c.skill} ${byId[c.skill].name} | ${needs.length ? needs.map((n) => `${n.courses} → ${n.skill} ${byId[n.skill]?.name}`).join("；") : "无（" + c.quote + "）"} | ${needs.every((n) => n.inClosure) ? "✓" : "✗ " + needs.filter((n) => !n.inClosure).map((n) => n.skill).join(",")} |\n`;
}
const mismatches = kthRows.flatMap(({ c, needs }) => needs.filter((n) => !n.inClosure).map((n) => `${c.code}→${n.skill}`));
km += `\n不一致：${mismatches.length ? mismatches.join("，") : "无"}。\n`;
fs.writeFileSync(path.join(ROOT, "reports/kth-crosscheck.md"), km);
console.log(`tree: ${skills.length} skills, ${tree.meta.requiredEdges} required edges; content packs: ${Object.keys(content).length}; chapter order changed for ${moved.length} skills (${JSON.stringify(basisCount)})`);
