// Unit tests for the pure game core. Run: npm test (needs src/gen/tree.json from npm run data).
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import { indexTree, planRoute, requiredClosure, topoOrder, routeGoals } from "../../src/game/core/graph.js";
import { goalRouteText } from "../../src/game/core/route-text.js";
import { skillState, satisfied, starsFor, mastery, shouldLight, playableChapters } from "../../src/game/core/rules.js";
import { checkItem, parseNumber, normalizeText } from "../../src/game/core/check.js";
import { createStore, memoryStorage, emptyProgress, migrate, streak, levelOf, addXp, dayKey, VERSION } from "../../src/game/core/progress.js";
import { newCard, reviewCard, isDue, gradeFor } from "../../src/game/core/review.js";
import { sectionKey } from "../../scripts/lib/sections.mjs";
import { normalizeLesson, leanLesson, firstTryShare, lessonSims } from "../../src/game/core/lesson.js";
import { completeLesson, submitBoss } from "../../src/game/app/actions.js";
import { LAB, metKeys, labGroups, labNew, programs } from "../../src/game/app/lab.js";

const tree = JSON.parse(fs.readFileSync(new URL("../../src/gen/tree.json", import.meta.url)));
const content = JSON.parse(fs.readFileSync(new URL("../../src/gen/content.json", import.meta.url)));
const g = indexTree(tree);

test("cross-domain lane X is excluded and no edge points into it", () => {
  assert.ok(!tree.skills.some((s) => s.domain === "X"));
  for (const s of tree.skills) for (const r of [...s.required, ...s.recommended]) assert.ok(g.byId.has(r.id), `${s.id} → ${r.id}`);
});

test("chapters are numbered 1..n in every skill", () => {
  for (const s of tree.skills) assert.deepEqual(s.chapters.map((c) => c.no), s.chapters.map((_, i) => i + 1), s.id);
});

test("route stops respect every required prerequisite and cover every goal", () => {
  for (const r of tree.routes) {
    const plan = planRoute(g, r);
    const pos = new Map(plan.stops.map((id, i) => [id, i]));
    for (const id of plan.stops) for (const req of g.byId.get(id).required) assert.ok(pos.get(req.id) < pos.get(id), `${req.id} before ${id}`);
    const closure = new Set(routeGoals(r).flatMap((id) => [...requiredClosure(g, id)]));
    assert.deepEqual(new Set(plan.stops), closure, r.id);
    if (!r.also?.length) assert.equal(plan.stops.at(-1), r.goal);
  }
});

test("routes.yaml: the author's own route is OS; recommended routes carry evidence; ids are unique", () => {
  const own = tree.routes.filter((r) => r.kind === "own");
  assert.deepEqual(own.map((r) => r.id), ["goal:C.2.1"]);
  assert.ok(own[0].was.includes("os"), "the old curated id still finds it");
  const plan = planRoute(g, own[0]);
  assert.deepEqual(new Set(plan.stops), new Set(["P.1.1", "P.2.2", "F.1.1", "C.1.1", "C.2.1"]));
  assert.equal(plan.stops[0], "P.1.1");
  for (const r of tree.routes.filter((r) => r.kind === "recommended")) assert.ok(r.evidence.line && r.evidence.sources.length, r.id);
  assert.equal(new Set(tree.routes.map((r) => r.id)).size, tree.routes.length);
  assert.ok(["open", "dev"].includes(tree.customGoals));
});

test("a goal route's text is written from the tree: goal chapters, the stops by lane, the courses", () => {
  const r = planRoute(g, { id: "goal:C.2.1", goal: "C.2.1" });
  const t = goalRouteText(g, r);
  assert.equal(t.name, "操作系统");
  assert.equal(t.tagline, "从“程序设计基础”走到“操作系统”，共 5 站");
  assert.match(t.story[0], /^终点“操作系统”要学：进程\/线程、调度/);
  assert.match(t.story[1], /4 个技能/);
  assert.match(t.story[1], /程序设计（程序设计基础、C\/C\+\+与底层编程）/);
  assert.match(t.story[2], /UC Berkeley CS 162/);
  const alone = goalRouteText(g, planRoute(g, { id: "goal:P.1.1", goal: "P.1.1" }));
  assert.equal(alone.tagline, "目标：点亮“程序设计基础”");
  for (const s of tree.skills) { const x = goalRouteText(g, planRoute(g, { id: "goal:" + s.id, goal: s.id })); assert.ok(x.story.every((p) => p && !p.includes("undefined")), s.id); }
});

test("topoOrder rejects nothing valid and is deterministic", () => {
  const ids = [...requiredClosure(g, "A.2.3")];
  assert.deepEqual(topoOrder(g, ids), topoOrder(g, [...ids].reverse()));
});

test("locks follow required prerequisites; only a lit skill satisfies one", () => {
  const p = emptyProgress();
  assert.equal(skillState(g, content, p, "C.2.1").status, "locked");
  assert.equal(skillState(g, content, p, "P.1.1").status, "open");
  for (const id of ["P.2.2", "F.1.1"]) p.skills[id] = { lit: "x" };
  p.skills["C.1.1"] = { known: "x" }; // a v1 "already know it" mark no longer counts
  assert.ok(!satisfied(p, "C.1.1"));
  assert.equal(skillState(g, content, p, "C.2.1").status, "locked");
  p.skills["C.1.1"] = { lit: "x" };
  assert.equal(skillState(g, content, p, "C.2.1").status, "open");
});

test("lighting needs checkable evidence, never a self-grade", () => {
  const p = emptyProgress();
  const fresh = skillState(g, content, p, "P.1.1");
  assert.equal(fresh.hasContent, true);
  assert.equal(fresh.bossOpen, false);
  // Neither old reading logs nor browsing the ungraded exercise can light a skill.
  assert.ok(!shouldLight(fresh, { graded: false }));
  assert.ok(!shouldLight(fresh, { graded: false, testOut: true }));
  p.skills["P.1.1"] = { selfChapters: Object.fromEntries(fresh.chapters.map((c) => [c.key, "x"])) };
  assert.equal(skillState(g, content, p, "P.1.1").bossOpen, false);
  for (const c of fresh.chapters) p.lessons[`P.1.1/${c.key}`] = { done: "x" };
  const read = skillState(g, content, p, "P.1.1");
  assert.equal(read.bossOpen, true);
  assert.ok(!shouldLight(read, { graded: false }));
  // Graded: the share right on the first try decides, before (test-out) or after the chapters.
  assert.ok(!shouldLight(read, { graded: true, auto: 2 / 3 }));
  assert.ok(shouldLight(read, { graded: true, auto: 0.8 }));
  assert.ok(!shouldLight(fresh, { graded: true, auto: 1 }));
  assert.ok(shouldLight(fresh, { graded: true, auto: 1, testOut: true }));
  assert.ok(!shouldLight(fresh, { graded: true, auto: 0.5, testOut: true }));
  assert.ok(!shouldLight(skillState(g, content, emptyProgress(), "C.2.1"), { graded: true, auto: 1, testOut: true }), "locked skills never light");
  assert.ok(!shouldLight(skillState(g, {}, p, "P.1.1"), { graded: true, auto: 1, testOut: true }), "skills without content never light, even with a forged graded result");
});

test("v1 saves lose the known mark and the self-grade on load", () => {
  const p = migrate({ v: 1, skills: { "P.1.1": { known: "x" }, "M.1.1": { lit: "y", boss: { self: "right", auto: 1 } } } });
  assert.equal(p.v, VERSION);
  assert.equal(p.skills["P.1.1"].known, undefined);
  assert.deepEqual(p.skills["M.1.1"], { lit: "y", boss: { auto: 1 } });
});

test("a lesson flow normalises to kinds and graded items; first-try share ignores hinted answers", () => {
  const a = { id: "q1", type: "number", prompt: "", explain: "", answer: 1 }, b = { ...a, id: "q2" }, w = { ...a, id: "w" }, card = { body: "x" };
  const flow = normalizeLesson({ id: "l", flow: [{ guess: w }, { card }, { item: a }, { card }, { item: b }] });
  assert.deepEqual(flow.flow.map((s) => s.kind), ["guess", "card", "item", "card", "item"]);
  assert.deepEqual(flow.items.map((i) => i.id), ["q1", "q2"]);
  assert.deepEqual(normalizeLesson(leanLesson({ id: "l", flow: [{ card }, { item: a }] })).items.map((i) => i.id), ["q1"]);
  assert.equal(firstTryShare([a, b], { q1: { firstTry: true }, q2: { firstTry: true, usedHint: true } }), 0.5);
});

test("content pack lessons follow chapter order", () => {
  const skill = g.byId.get("C.2.1");
  const pack = { lessons: [...skill.chapters].reverse().map((c, i) => ({ id: "l" + i, chapter: c.title, flow: [] })) };
  assert.deepEqual(playableChapters(skill, pack).map((c) => c.chapter.no), skill.chapters.map((c) => c.no));
});

test("unfinished skills freely expose materials and exercises, without progress or lighting", () => {
  const p = emptyProgress();
  const st = skillState(g, content, p, "C.3.5");
  assert.ok(st.missing.length > 0, "prerequisites are still shown as self-study guidance");
  assert.equal(st.status, "dev");
  assert.equal(st.nextChapter, null);
  assert.equal(st.progress, 0);
  assert.equal(st.bossOpen, true);
  assert.ok(st.chapters.every((_, i) => st.chapterOpen(i)));
  const store = createStore(memoryStorage());
  const before = structuredClone(store.get());
  assert.deepEqual(submitBoss(store, g, content, "C.3.5", { graded: false, auto: 1 }), { lit: false, xp: 0, achievements: [] });
  assert.deepEqual(submitBoss(store, g, content, "C.3.5", { graded: true, auto: 1, testOut: true }), { lit: false, xp: 0, achievements: [] });
  assert.deepEqual(store.get(), before);
});

test("adding a content pack starts interactive progress fresh after old reading logs", () => {
  const skill = g.byId.get("P.1.1");
  const pack = { lessons: skill.chapters.map((c, i) => ({ id: "new-" + i, chapter: c.title, flow: [] })) };
  const p = migrate({ v: 2, skills: { [skill.id]: { selfChapters: { 1: "2026-11-01T00:00:00Z" } } } });
  const before = structuredClone(p);
  assert.equal(skillState(g, {}, p, skill.id).status, "dev");
  const st = skillState(g, { [skill.id]: pack }, p, skill.id);
  assert.equal(st.status, "open");
  assert.equal(st.progress, 0);
  assert.ok(st.done.every((done) => !done));
  assert.equal(st.nextChapter.key, "new-0");
  assert.equal(st.chapterOpen(0), true);
  assert.equal(st.chapterOpen(1), false);
  assert.equal(st.bossOpen, false);
  assert.equal(p.skills[skill.id].selfChapters, undefined);
  assert.deepEqual(p, before, "state is derived without rewriting the save");
});

test("v2 import removes self-study lights, preserves real lessons and global XP, then accepts new courses", async () => {
  const skill = g.byId.get("P.1.1");
  const pack = { lessons: skill.chapters.map((c, i) => ({ id: "new-" + i, chapter: c.title, flow: [] })) };
  const content = { [skill.id]: pack };
  const at = "2026-11-01T00:00:00.000Z";
  const p = emptyProgress(new Date(at));
  p.v = 2;
  p.xp = 123;
  p.days["2026-11-01"] = 123;
  p.achievements["self-study"] = at;
  p.skills[skill.id] = { lit: at, boss: { at, graded: false }, selfChapters: Object.fromEntries(skill.chapters.map((c) => [c.no, at])) };
  p.skills["C.1.1"] = { lit: at, boss: { at, graded: true, auto: 1 }, selfChapters: { 1: at } };
  p.lessons["C.1.1/real-lesson"] = { done: at, stars: 3 };
  const store = createStore(memoryStorage());
  store.importJson(JSON.stringify({ app: "cs-math-skill-game", progress: p }));
  assert.equal(p.skills[skill.id].lit, at, "migration leaves the source object intact");
  assert.equal(store.get().v, VERSION);
  const st = skillState(g, content, store.get(), skill.id);
  assert.equal(st.status, "open");
  assert.equal(st.progress, 0);
  assert.equal(skillState(g, { ...content, "P.2.2": { lessons: [] } }, store.get(), "P.2.2").status, "locked");
  assert.equal(store.get().skills["C.1.1"].lit, at);
  assert.equal(store.get().skills["C.1.1"].selfChapters, undefined);
  assert.deepEqual(store.get().lessons["C.1.1/real-lesson"], p.lessons["C.1.1/real-lesson"]);
  const failed = submitBoss(store, g, content, skill.id, { graded: true, testOut: true, auto: 0 }, new Date(at));
  assert.equal(failed.lit, false);
  assert.equal(failed.xp, 0);
  assert.equal(store.get().skills[skill.id].lit, undefined);
  assert.equal(store.get().xp, 123);
  assert.equal(store.get().achievements["self-study"], undefined);
  const completed = await completeLesson(store, g, content, skill.id, pack.lessons[0], [], new Date(at));
  assert.equal(completed.state.done[0], true);
  assert.equal(completed.state.chapterOpen(1), true);
  assert.equal(store.get().skills[skill.id].lit, undefined);
  for (const l of pack.lessons.slice(1)) await completeLesson(store, g, content, skill.id, l, [], new Date(at));
  const passed = submitBoss(store, g, content, skill.id, { graded: true, auto: 1 }, new Date(at));
  assert.equal(passed.lit, true);
  assert.equal(passed.xp, 30);
  assert.equal(store.get().skills[skill.id].lit, at);
});

test("实验室: every experiment a lesson uses has an entry, and every entry is used by a lesson", () => {
  const used = new Set(Object.values(content).flatMap((pack) => pack.lessons.flatMap((l) => [...lessonSims(l)])));
  const listed = labNew(new Set(), used);
  assert.equal(listed.length, LAB.reduce((n, g) => n + g.items.length, 0), "an entry no lesson uses (archive it with its sim)");
  assert.deepEqual([...used].filter((k) => !listed.some((e) => e.key === k)), [], "a lesson experiment the lab does not list");
});

test("实验室 grows by the experiments a finished lesson brings, once", async () => {
  const store = createStore(memoryStorage());
  assert.deepEqual(labGroups(metKeys(content, store.get())), []);
  const f = content["F.1.1"].lessons;
  const sq = f.find((l) => l.id === "stack-queue-adt");
  const first = await completeLesson(store, g, content, "F.1.1", sq, [], new Date());
  assert.deepEqual(first.lab.map((e) => e.title), ["栈", "队列"]);
  assert.deepEqual((await completeLesson(store, g, content, "F.1.1", sq, [], new Date())).lab, [], "the same lesson again");
  assert.deepEqual(labGroups(metKeys(content, store.get())).map((x) => x.group), ["数据结构"]);
  // Python stepping: one entry; its programs are the card programs of the finished lessons
  const two = f.find((l) => l.id === "two-stacks");
  assert.deepEqual((await completeLesson(store, g, content, "F.1.1", two, [], new Date())).lab.map((e) => e.title), ["Python 单步执行"]);
  assert.deepEqual(programs(content, store.get()).map((x) => x.label), [two.title]);
  assert.deepEqual((await completeLesson(store, g, content, "F.1.1", f.find((l) => l.id === "binary-trees"), [], new Date())).lab, []);
  assert.equal(programs(content, store.get()).length, 2);
});

test("stars and levels", () => {
  assert.equal(starsFor(9, 10), 3);
  assert.equal(starsFor(6, 10), 2);
  assert.equal(starsFor(1, 10), 1);
  assert.deepEqual(levelOf(0), { level: 1, into: 0, span: 50 });
  assert.equal(levelOf(50).level, 2);
  assert.equal(levelOf(149).level, 2);
  assert.equal(levelOf(150).level, 3);
});

test("number parsing and checking", () => {
  assert.equal(parseNumber("3/2"), 1.5);
  assert.equal(parseNumber("１．５"), 1.5);
  assert.equal(parseNumber("50%"), 0.5);
  assert.equal(parseNumber("2^10"), 1024);
  assert.equal(parseNumber("1,024"), 1024);
  assert.ok(Number.isNaN(parseNumber("abc")));
  assert.ok(checkItem({ type: "number", answer: 0.5, tolerance: 0.01 }, "1/2").correct);
  assert.ok(!checkItem({ type: "number", answer: 0.5, tolerance: 0.01 }, "0.6").correct);
});

test("choice, text, order, match checking", () => {
  const ch = { type: "choice", options: [{ text: "a" }, { text: "b", correct: true }, { text: "c", correct: true }], multi: true };
  assert.ok(checkItem(ch, [2, 1]).correct);
  assert.ok(!checkItem(ch, [1]).correct);
  assert.ok(checkItem({ type: "text", answers: ["Hello World"] }, "  hello   world ").correct);
  assert.ok(!checkItem({ type: "text", answers: ["Hi"], caseSensitive: true }, "hi").correct);
  assert.equal(normalizeText("Ａ－Ｂ"), "a-b");
  const list = { type: "text", answers: ["[1, 3, 7]"] };
  for (const r of ["[1,3,7]", "1, 3, 7", "1 3 7", "1，3，7"]) assert.ok(checkItem(list, r).correct, r);
  assert.ok(!checkItem(list, "1 7 3").correct);
  assert.ok(!checkItem({ type: "text", answers: ["3 2"] }, "3, 2").correct);
  assert.ok(checkItem({ type: "order", steps: ["x", "y", "z"] }, [0, 1, 2]).correct);
  assert.ok(!checkItem({ type: "order", steps: ["x", "y", "z"] }, [1, 0, 2]).correct);
  assert.ok(checkItem({ type: "match", pairs: [["a", "1"], ["b", "2"]] }, [0, 1]).correct);
});

test("progress store round-trips through export/import and refuses future versions", () => {
  const store = createStore(memoryStorage());
  store.update((d) => { addXp(d, 15); d.skills["P.1.1"] = { lit: "2026-11-03" }; });
  const text = store.exportJson();
  const other = createStore(memoryStorage());
  other.importJson(text);
  assert.equal(other.get().xp, 15);
  assert.throws(() => migrate({ v: 99 }));
  assert.throws(() => other.importJson(JSON.stringify({ app: "x" })));
});

test("streak counts consecutive days and survives until the end of today", () => {
  const p = emptyProgress();
  const d0 = new Date(2026, 10, 3, 9);
  for (let i = 1; i <= 3; i++) p.days[dayKey(new Date(2026, 10, 3 - i, 9))] = 10;
  assert.equal(streak(p, d0), 3);
  p.days[dayKey(d0)] = 5;
  assert.equal(streak(p, d0), 4);
});

test("FSRS review: grades map and stored cards survive JSON", async () => {
  assert.equal(gradeFor({ correct: false }), 1);
  assert.equal(gradeFor({ correct: true, firstTry: true }), 3);
  assert.equal(gradeFor({ correct: true, firstTry: false }), 2);
  const now = new Date("2026-11-03T00:00:00Z");
  const c0 = await newCard(now);
  const { card } = await reviewCard(JSON.parse(JSON.stringify(c0)), { correct: true, firstTry: true }, now);
  assert.ok(!isDue(card, now));
  const later = new Date(card.dueAt);
  assert.ok(isDue(card, later));
  const again = await reviewCard(JSON.parse(JSON.stringify(card)), { correct: false }, later);
  assert.ok(again.card.lapses >= 1);
});

test("mastery tiers come from card stability", () => {
  const p = emptyProgress();
  p.skills["P.1.1"] = { lit: "x" };
  assert.equal(mastery(p, "P.1.1"), "lit");
  p.cards["P.1.1/a/b"] = { reps: 3, stability: 40 };
  assert.equal(mastery(p, "P.1.1"), "mastered");
  p.cards["P.1.1/a/c"] = { reps: 2, stability: 8 };
  assert.equal(mastery(p, "P.1.1"), "solid");
  assert.equal(mastery(p, "C.2.1"), null);
});

test("section numbers: pages, years and lecture parts are not chapters", () => {
  assert.deepEqual(sectionKey("2.2 The Limit of a Function"), [2, 2]);
  assert.deepEqual(sectionKey("第 1 章 极限 (1)–(3)"), [1]);
  assert.deepEqual(sectionKey("第二章 线性方程组"), [2]);
  assert.deepEqual(sectionKey("Unit 3: Vector Spaces"), [3]);
  assert.equal(sectionKey("Introduction（20 页，渐近记号）"), null);
  assert.equal(sectionKey("2023 Spring lecture"), null);
});

test("update check: version order, and what GitHub's answer means", async () => {
  const { isNewer, checkUpdate } = await import("../../src/game/app/update.js");
  assert.equal(isNewer("1.0.10", "1.0.9"), true);
  assert.equal(isNewer("v1.1.0", "1.0.9"), true);
  assert.equal(isNewer("1.1.0", "1.1.0"), false);
  assert.equal(isNewer("1.0.2", "1.1.0"), false);
  const reply = (status, body) => async () => ({ ok: status === 200, status, json: async () => body });
  const rel = { tag_name: "v9.0.0", body: "新课", html_url: "https://github.com/x/releases/tag/v9.0.0", assets: [{ name: "点亮之路-9.0.0.apk", browser_download_url: "https://example.org/a.apk" }] };
  assert.deepEqual(await checkUpdate(reply(200, rel)), { latest: "9.0.0", newer: true, notes: "新课", download: "https://example.org/a.apk", page: rel.html_url });
  assert.equal((await checkUpdate(reply(200, { ...rel, tag_name: "v0.0.0" }))).newer, false);
  await assert.rejects(checkUpdate(reply(404, {})), /还没有发布过版本/);
  await assert.rejects(checkUpdate(reply(403, {})), /403/);
  await assert.rejects(checkUpdate(async () => { throw new TypeError("Failed to fetch"); }), /连不上 GitHub/);
});
