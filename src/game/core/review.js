// Spaced review on top of ts-fsrs (FSRS-7 by default). This module only maps game outcomes to
// FSRS grades and (de)serialises cards; scheduling maths stays in the library.
import { DefaultScheduler, Rating } from "ts-fsrs";

let schedulerPromise = null;
export const getScheduler = () => (schedulerPromise ||= DefaultScheduler({ desiredRetention: 0.9, enableFuzz: false }));

// How an answer maps to a grade: right on the first try → Good; right after a hint or a retry → Hard;
// wrong → Again. Easy is never inferred; a quiz cannot tell "easy" from "good".
export function gradeFor({ correct, firstTry, usedHint }) {
  if (!correct) return Rating.Again;
  return firstTry && !usedHint ? Rating.Good : Rating.Hard;
}

const DATE_FIELDS = ["dueAt", "lastReviewAt"];
export function reviveCard(json) {
  const c = { ...json };
  for (const f of DATE_FIELDS) if (c[f]) c[f] = new Date(c[f]);
  return c;
}
export const storeCard = (card) => JSON.parse(JSON.stringify(card));

export async function newCard(now = new Date()) {
  const s = await getScheduler();
  return storeCard(s.newCard({ now }));
}

export async function reviewCard(stored, outcome, now = new Date()) {
  const s = await getScheduler();
  const { card, revlog } = s.review({ card: reviveCard(stored), grade: gradeFor(outcome), now });
  return { card: storeCard(card), revlog: storeCard(revlog) };
}

export const isDue = (stored, now = new Date()) => new Date(stored.dueAt) <= now;

// Estimated recall probability now (0..1); 1 for cards never reviewed after creation.
export async function recall(stored, now = new Date()) {
  if (!stored.lastReviewAt) return 1;
  const s = await getScheduler();
  const c = reviveCard(stored);
  return s.model.forgettingCurve(c, s.chrono.difference(c.lastReviewAt, now));
}
