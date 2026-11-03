// What a lesson or a final challenge plays, as one ordered list of steps. Pure; shared by the build
// (scripts/lib/packs.mjs normalises every pack before writing src/gen/content.json) and the game.
//
// Authoring format (data/content.schema.json): flow: [{ guess }, { card }, { item }, …], played top
// to bottom; explanation and practice alternate, one idea at a time.
// Runtime lesson: { id, chapter, title, minutes, flow: [{ kind: "guess" | "card" | "item", … }],
//   items: [graded items in play order] }. Wrong graded items come back once at the end.

export const PASS_SHARE = 0.8; // final challenge: share of checks answered right on the first try

export function normalizeLesson(l) {
  const flow = l.flow[0]?.kind
    ? l.flow // already normalised
    : l.flow.map((s) => (s.guess ? { kind: "guess", item: s.guess } : s.card ? { kind: "card", card: s.card } : { kind: "item", item: s.item }));
  const { items, ...rest } = l;
  return { ...rest, flow, items: flow.filter((s) => s.kind === "item").map((s) => s.item) };
}

// What the build stores: the flow only (items are derived again when the game loads).
export const leanLesson = (l) => { const { items, ...rest } = normalizeLesson(l); return rest; };

// Every item a lesson shows (guesses included), for id checks and tests.
export const allItems = (lesson) => normalizeLesson(lesson).flow.filter((s) => s.item).map((s) => s.item);

// Which experiment a sim with these params is: the sim, plus its mode or kind where one sim plays
// several (graph bfs / dfs, stackqueue stack / queue). The 实验室 lists one entry per key.
export const simKey = (name, params = {}) => `${name}:${params.mode || params.kind || ""}`;

// The experiments a lesson uses: graded sim items and the demos on its cards.
export function lessonSims(lesson) {
  const keys = new Set();
  for (const s of normalizeLesson(lesson).flow) {
    if (s.item?.type === "sim") keys.add(simKey(s.item.sim, s.item.params));
    if (s.card?.sim) keys.add(simKey(s.card.sim.name, s.card.sim.params));
  }
  return keys;
}

// Final challenge: auto-graded checks from the content pack. Without one, the UI shows the tree's
// exercise and answer directly, outside the step player and its completion callback.
export function bossFlow(skill, pack) {
  const items = pack?.boss?.items || [];
  if (items.length) return { graded: true, flow: items.map((item) => ({ kind: "item", item })), items };
  return { graded: false, flow: [], items: [] };
}

// results: { [itemId]: { firstTry, usedHint } } for graded items. Right on the first try, no hint.
export function firstTryShare(items, results) {
  if (!items.length) return 1;
  return items.filter((it) => results[it.id]?.firstTry && !results[it.id]?.usedHint).length / items.length;
}
