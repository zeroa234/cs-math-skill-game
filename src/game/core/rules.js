// Game rules: what is locked, what can be played, when a skill lights up, mastery tiers, stars, XP.
// Pure functions of (graph, content, progress); the UI only renders what these return.

import { PASS_SHARE } from "./lesson.js";

export const XP = { lessonBase: 10, perStar: 5, boss: 30, testOut: 40, review: 2 };

// A prerequisite counts once it is lit (by its final challenge or a passed test-out).
export const satisfied = (p, id) => !!p.skills[id]?.lit;

export const lessonKey = (skillId, lessonId) => `${skillId}/${lessonId}`;
export const cardKey = (skillId, lessonId, itemId) => `${skillId}/${lessonId}/${itemId}`;

// Chapters a skill is played through. With a content pack: its lessons (in chapter order).
// Without one: one freely browsable reading chapter per must-learn topic, without completion marks.
export function playableChapters(skill, pack) {
  if (!pack) return skill.chapters.map((c) => ({ kind: "self", no: c.no, chapter: c, key: String(c.no), core: c.stage === "core" }));
  const order = new Map(skill.chapters.map((c) => [c.title, c.no]));
  return [...pack.lessons]
    .sort((a, b) => order.get(a.chapter) - order.get(b.chapter))
    .map((l, i) => {
      const chapter = skill.chapters.find((c) => c.title === l.chapter);
      return { kind: "lesson", no: i + 1, chapter, lesson: l, key: l.id, core: chapter.stage === "core" };
    });
}

export function chapterDone(p, skill, ch) {
  return ch.kind === "lesson" && !!p.lessons[lessonKey(skill.id, ch.key)]?.done;
}

// Lessons open one after another (a beginner never wonders where to start); the boss opens when
// every core chapter is done. A test-out (boss first) is always offered once the skill is open.
export function skillState(g, content, p, id) {
  const skill = g.byId.get(id);
  const pack = content[id] || null;
  const missing = skill.required.filter((r) => !satisfied(p, r.id)).map((r) => r.id);
  const chapters = playableChapters(skill, pack);
  const done = chapters.map((c) => chapterDone(p, skill, c));
  const coreDone = chapters.every((c, i) => !c.core || done[i]);
  const rec = p.skills[id] || {};
  let status;
  if (!pack) status = "dev";
  else if (rec.lit) status = "lit";
  else if (missing.length) status = "locked";
  else if (done.some(Boolean) || rec.boss) status = "learning";
  else status = "open";
  const nextIndex = done.findIndex((d) => !d);
  return {
    skill, pack, chapters, done, missing, status,
    nextChapter: !pack || nextIndex === -1 ? null : chapters[nextIndex],
    chapterOpen: (i) => !pack || (status !== "locked" && (i === 0 || done[i - 1] || done[i])),
    bossOpen: !pack || (status !== "locked" && coreDone),
    progress: chapters.length ? done.filter(Boolean).length / chapters.length : 0,
    hasContent: !!pack,
  };
}

// Mastery tiers for lit skills, from the FSRS memory state of the skill's review cards:
//  lit (点亮) → solid (熟练: every card has been reviewed again after learning and holds ≥ 7 days)
//  → mastered (精通: every card holds ≥ 30 days). Skills without cards stay at "lit".
export function mastery(p, id) {
  if (!p.skills[id]?.lit) return null;
  const cards = Object.entries(p.cards).filter(([k]) => k.startsWith(id + "/")).map(([, c]) => c);
  if (!cards.length) return "lit";
  const reviewed = cards.every((c) => c.reps >= 2);
  const minStab = Math.min(...cards.map((c) => c.stability || 0));
  if (reviewed && minStab >= 30) return "mastered";
  if (reviewed && minStab >= 7) return "solid";
  return "lit";
}

// Stars for a lesson from first-try accuracy over graded items.
export function starsFor(firstTryCorrect, total) {
  const r = total ? firstTryCorrect / total : 0;
  return r >= 0.9 ? 3 : r >= 0.6 ? 2 : 1;
}

export const lessonXp = (stars) => XP.lessonBase + XP.perStar * stars;

// Skills the player can act on now, best first: open/learning before others; among them the ones
// that unblock the most future skills (the tree's precomputed reach), then by step.
export function nextUp(g, content, p, ids = [...g.byId.keys()]) {
  return ids
    .map((id) => skillState(g, content, p, id))
    .filter((s) => s.status === "open" || s.status === "learning")
    .sort((a, b) => (b.status === "learning") - (a.status === "learning") || (b.skill.reach || 0) - (a.skill.reach || 0) || a.skill.step - b.skill.step);
}

// Light a skill only on evidence the game can check. A graded challenge (content packs) needs
// PASS_SHARE of its checks right on the first try, with every core chapter done, or without them as a
// test-out. A skill without a content pack only offers reading and an ungraded exercise; it never lights.
// bossResult: { graded, auto: 0..1, testOut }
export function shouldLight(state, bossResult) {
  return !!(bossResult?.graded && state.hasContent && state.status !== "locked" &&
    (bossResult.testOut || state.bossOpen) && bossResult.auto >= PASS_SHARE);
}
