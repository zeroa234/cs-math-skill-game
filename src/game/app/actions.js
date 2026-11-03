// Game actions: the only place that changes progress. Each takes the store and facts about what the
// player did, applies the rules from core/rules.js, and returns what the UI should celebrate.
import { addXp, dayKey, streak } from "../core/progress.js";
import { XP, lessonKey, cardKey, starsFor, lessonXp, skillState, shouldLight, mastery } from "../core/rules.js";
import { reviewable } from "../core/check.js";
import { newCard, reviewCard } from "../core/review.js";
import { metKeys, labNew } from "./lab.js";

export const ACHIEVEMENTS = [
  { id: "first-lesson", name: "第一步", desc: "完成第一课" },
  { id: "first-light", name: "点亮", desc: "点亮第一个技能" },
  { id: "perfect", name: "一次都对", desc: "一课里每题第一次就答对" },
  { id: "first-review", name: "温故", desc: "完成第一次间隔复习" },
  { id: "streak-3", name: "三天不断", desc: "连续 3 天学习" },
  { id: "streak-7", name: "一周不断", desc: "连续 7 天学习" },
  { id: "route-os", name: "看懂操作系统", desc: "点亮“操作系统”" },
  { id: "solid", name: "记得牢", desc: "第一个技能达到“熟练”" },
];

function grant(draft, id, now, out) {
  if (draft.achievements[id]) return;
  draft.achievements[id] = now.toISOString();
  out.push(ACHIEVEMENTS.find((a) => a.id === id));
}

function afterAny(draft, g, now, out) {
  const s = streak(draft, now);
  if (s >= 3) grant(draft, "streak-3", now, out);
  if (s >= 7) grant(draft, "streak-7", now, out);
  if (draft.skills["C.2.1"]?.lit) grant(draft, "route-os", now, out);
  for (const id of Object.keys(draft.skills)) if (mastery(draft, id) === "solid" || mastery(draft, id) === "mastered") grant(draft, "solid", now, out);
}

// results: [{ item, correct, firstTry, usedHint }] for the graded items of the lesson
export async function completeLesson(store, g, content, skillId, lesson, results, now = new Date()) {
  const firstTry = results.filter((r) => r.firstTry && r.correct && !r.usedHint).length;
  const stars = starsFor(firstTry, results.length);
  // FSRS cards for reviewable items: first time a card is created and graded by this attempt.
  const cards = {};
  for (const r of results) {
    if (!reviewable(r.item)) continue;
    const key = cardKey(skillId, lesson.id, r.item.id);
    const existing = store.get().cards[key];
    const base = existing || (await newCard(now));
    cards[key] = (await reviewCard(base, r, now)).card;
  }
  const out = [];
  let gained = 0;
  const metBefore = metKeys(content, store.get());
  store.update((d) => {
    const k = lessonKey(skillId, lesson.id);
    const prev = d.lessons[k];
    const first = !prev?.done;
    d.lessons[k] = { done: prev?.done || now.toISOString(), stars: Math.max(prev?.stars || 0, stars), best: Math.max(prev?.best || 0, results.length ? firstTry / results.length : 1), attempts: (prev?.attempts || 0) + 1 };
    gained = first ? lessonXp(stars) : Math.max(0, lessonXp(stars) - lessonXp(prev?.stars || 0));
    addXp(d, gained, now);
    Object.assign(d.cards, cards);
    d.skills[skillId] ||= {};
    grant(d, "first-lesson", now, out);
    if (stars === 3 && firstTry === results.length) grant(d, "perfect", now, out);
    afterAny(d, g, now, out);
  });
  // firstTry is what the stars count; hinted: right on the first try, but after a hint (not counted)
  const hinted = results.filter((r) => r.firstTry && r.correct && r.usedHint).length;
  return { stars, firstTry, hinted, xp: gained, achievements: out, lab: labNew(metBefore, metKeys(content, store.get())), state: skillState(g, content, store.get(), skillId) };
}

// bossResult: { graded, auto: 0..1 (share of checks right on the first try), testOut }
export function submitBoss(store, g, content, skillId, bossResult, now = new Date()) {
  const state = skillState(g, content, store.get(), skillId);
  if (!state.hasContent || !bossResult?.graded) return { lit: false, xp: 0, achievements: [] };
  const light = shouldLight(state, bossResult);
  const out = [];
  let gained = 0;
  store.update((d) => {
    const s = (d.skills[skillId] ||= {});
    s.boss = { at: now.toISOString(), graded: !!bossResult.graded, auto: bossResult.auto, testOut: !!bossResult.testOut };
    if (light && !s.lit) {
      s.lit = now.toISOString();
      gained = bossResult.testOut ? XP.testOut : XP.boss;
      addXp(d, gained, now);
      grant(d, "first-light", now, out);
    }
    afterAny(d, g, now, out);
  });
  return { lit: light, xp: gained, achievements: out };
}

export async function answerReview(store, key, outcome, now = new Date()) {
  const card = store.get().cards[key];
  if (!card) return;
  const next = (await reviewCard(card, outcome, now)).card;
  const out = [];
  store.update((d) => {
    d.cards[key] = next;
    addXp(d, XP.review, now);
    grant(d, "first-review", now, out);
    afterAny(d, null, now, out);
  });
  return { card: next, achievements: out };
}

export const todayXp = (p, now = new Date()) => p.days[dayKey(now)] || 0;
