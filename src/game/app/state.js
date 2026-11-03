// App-wide context: the skill graph, content packs, the progress store and the selected route.
import { createContext } from "preact";
import { useContext, useMemo } from "preact/hooks";
import { useSyncExternalStore } from "preact/compat";
import tree from "../../gen/tree.json";
import content from "../../gen/content.json";
import { indexTree, planRoute } from "../core/graph.js";
import { goalRouteText } from "../core/route-text.js";
import { createStore, localStorageAdapter } from "../core/progress.js";
import { skillState } from "../core/rules.js";
import { normalizeLesson } from "../core/lesson.js";
import { isDue } from "../core/review.js";
import "../sims/logic/index.js";

export const g = indexTree(tree);
// Lessons arrive as a flow (core/lesson.js); the graded items are derived once here.
export const packs = Object.fromEntries(Object.entries(content).map(([k, p]) => [k, { ...p, lessons: p.lessons.map(normalizeLesson) }]));
export const store = createStore(localStorageAdapter());
// Three kinds of route (data/routes.yaml): "own" — the goals the author picked for themself (我的远征);
// "recommended" — written by hand from career evidence; "custom" — any skill a player picks as a goal.
// Own and custom routes are both "goal:<skill id>" and get their name, tagline and story from the
// tree (core/route-text.js), so a picked goal reads the same way as the author's own.
const withText = (r) => (r.kind === "recommended" ? { ...r, story: [].concat(r.story) } : { ...r, ...goalRouteText(g, r) });
export const routes = tree.routes.map((r) => withText(planRoute(g, r)));
export const routeById = Object.fromEntries(routes.map((r) => [r.id, r]));
export const ownRoutes = routes.filter((r) => r.kind === "own");
export const recommendedRoutes = routes.filter((r) => r.kind === "recommended");
export const customGoalsOpen = tree.customGoals === "open";

const goalRoutes = new Map();
export const routeIdForGoal = (skillId) => routes.find((r) => r.goal === skillId && !r.also?.length)?.id || "goal:" + skillId;
export function routeFor(id) {
  if (!id) return null;
  if (routeById[id]) return routeById[id];
  if (!id.startsWith("goal:") || !g.byId.has(id.slice(5))) return null;
  if (!goalRoutes.has(id)) goalRoutes.set(id, withText(planRoute(g, { id, goal: id.slice(5), kind: "custom", status: customGoalsOpen ? "open" : "dev" })));
  return goalRoutes.get(id);
}
// A route marked 开发中 can be looked at but not set off on.
export const playable = (r) => !!r && r.status === "open";
// The route the player is on, or null when none is chosen or it is still in development.
export const activeRoute = (p) => { const r = routeFor(p.settings.route); return playable(r) ? r : null; };

// What a campaign asks of you: stops, how many have interactive lessons, and their minutes;
// `beginner` counts the stops whose lessons meet both standards in docs/content-authoring.md: the
// beginner standard (pack version 2) and knowledge coverage (its coverage table passes rule C1,
// checked by the build); that is what a route waits for before it opens.
export function routeStats(r) {
  let lessons = 0, minutes = 0, withContent = 0, beginner = 0;
  for (const id of r.stops) {
    const pack = packs[id];
    if (!pack) continue;
    withContent++;
    if (pack.version >= 2 && pack.coverage) beginner++;
    for (const l of pack.lessons) { lessons++; minutes += l.minutes || 8; }
  }
  return { stops: r.stops.length, withContent, beginner, lessons, minutes };
}
export const laneOf = (skill) => g.lanes.get(skill.lane);

export const AppCtx = createContext(null);
export const useApp = () => useContext(AppCtx);

export function useProgress() {
  return useSyncExternalStore(store.subscribe, store.get);
}

export const stateOf = (p, id) => skillState(g, packs, p, id);

export function useSkillStates(p) {
  return useMemo(() => {
    const m = new Map();
    for (const id of g.byId.keys()) m.set(id, skillState(g, packs, p, id));
    return m;
  }, [p]);
}

export const dueCards = (p, now = new Date()) =>
  Object.entries(p.cards)
    .filter(([, c]) => isDue(c, now))
    .sort((a, b) => new Date(a[1].dueAt) - new Date(b[1].dueAt))
    .map(([key]) => key);

// Finds the item a review card points at: "skill/lesson/item".
export function itemForCard(key) {
  const [skill, ...rest] = key.split("/");
  const itemId = rest.pop();
  const lessonId = rest.join("/");
  const pack = packs[skill];
  const lesson = pack?.lessons.find((l) => l.id === lessonId);
  const item = lesson?.items.find((i) => i.id === itemId);
  return item ? { skill: g.byId.get(skill), lesson, item } : null;
}

// The next thing to do on a route: first stop not lit, and inside it the next chapter.
export function routeNext(p, route) {
  for (const id of route.stops) {
    const st = skillState(g, packs, p, id);
    if (st.status === "lit") continue;
    return st;
  }
  return null;
}

// A rewritten content pack can leave review cards whose question no longer exists. Drop them on load,
// so they neither come due nor hold a skill back from 熟练 / 精通.
{
  const orphans = Object.keys(store.get().cards).filter((k) => !itemForCard(k));
  if (orphans.length) store.update((d) => { for (const k of orphans) delete d.cards[k]; });
}

// A route that changed its id (routes.yaml `was`, e.g. the old curated "os" is now the own goal
// "goal:C.2.1") keeps the player on it; an id that no longer exists is dropped, so 营地 asks again.
{
  const saved = store.get().settings.route;
  if (saved && !routeFor(saved)) {
    const now = routes.find((r) => r.was?.includes(saved));
    store.update((d) => { d.settings.route = now?.id; });
  }
}
