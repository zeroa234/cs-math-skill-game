// Player progress: one plain JSON object, versioned, with a storage adapter interface so the game
// never touches localStorage directly (tests use the memory adapter).
//
// Shape (v3):
// { v, createdAt, xp, days: {YYYY-MM-DD: xp}, achievements: {id: iso},
//   skills:  { [skillId]: { lit?: iso, boss?: {at, graded, auto, testOut} } },
//   lessons: { [skillId/lessonId]: { done: iso, stars, best, attempts } },
//   cards:   { [skillId/lessonId/itemId]: storedFsrsCard },
//   settings: { route?, sourceLang: "zh"|"en"|"both", reduceMotion?, sound, introSeen? } }
//   route is a curated route id (data/routes.yaml) or "goal:<skill id>" for a goal the player picked.

export const VERSION = 3;
const KEY = "cs-math-skill-game/progress";

export function emptyProgress(now = new Date()) {
  return { v: VERSION, createdAt: now.toISOString(), xp: 0, days: {}, achievements: {}, skills: {}, lessons: {}, cards: {}, settings: { sourceLang: "zh", sound: true } };
}

// Upgrades older saves; unknown future versions are refused rather than silently mangled.
export function migrate(p) {
  if (!p || typeof p !== "object") throw new Error("存档不是 JSON 对象");
  if (p.v > VERSION) throw new Error(`存档版本 ${p.v} 比游戏新，请更新游戏后再导入`);
  const base = emptyProgress(new Date(p.createdAt || Date.now()));
  const out = { ...base, ...p, settings: { ...base.settings, ...(p.settings || {}) }, v: VERSION };
  // v1 → v2: "I already know this" and the self-grade of the final challenge were removed; a skill
  // marked known goes back to its real state (prerequisites lock again until it is lit).
  if ((p.v || 1) < 2) {
    out.skills = structuredClone(out.skills || {});
    for (const s of Object.values(out.skills)) { delete s.known; if (s.boss) delete s.boss.self; }
  }
  // v2 → v3: unfinished skills are reference material, without reading checkboxes or self-study
  // lights. Keep real interactive results and global XP; old reading logs never complete new lessons.
  if ((p.v || 1) < 3) {
    out.skills = structuredClone(out.skills);
    out.achievements = { ...out.achievements };
    for (const s of Object.values(out.skills)) {
      if (s.boss?.graded === false || (s.selfChapters && !s.boss?.graded)) { delete s.lit; delete s.boss; }
      delete s.selfChapters;
    }
    delete out.achievements["self-study"];
  }
  return out;
}

// Adapters: load() → text or null; save(text) → false when the text could not be stored;
// watch(fn), optional, calls fn(text) when another tab or window saved.
export const memoryStorage = () => {
  let data = null;
  return { load: () => data, save: (s) => { data = s; } };
};
export const localStorageAdapter = (key = KEY) => ({
  load() { try { return window.localStorage.getItem(key); } catch { return null; } },
  save(s) { try { window.localStorage.setItem(key, s); return true; } catch { return false; } },
  watch(fn) { window.addEventListener("storage", (e) => { if (e.key === key && e.newValue) fn(e.newValue); }); },
});

// health(): { unreadable?: { message, raw }, unsaved?: true }
//  - unreadable: the stored save could not be read (damaged, or from a newer version of the game).
//    It is never written over: the store keeps changes in memory only until replace() (import, or
//    starting over) — the player decides, after they could download the save as it is.
//  - unsaved: the last save did not reach storage (full, or blocked); cleared by the next one that does.
// A save from another tab replaces this tab's copy, so the two do not write over each other's progress.
export function createStore(adapter) {
  let state, health = {};
  const raw = adapter.load();
  try { state = migrate(JSON.parse(raw || "null") || emptyProgress()); }
  catch (e) { state = emptyProgress(); health = { unreadable: { message: e.message, raw } }; }
  const listeners = new Set();
  const emit = () => { for (const l of listeners) l(state); };
  const write = () => {
    if (health.unreadable) return;
    const failed = adapter.save(JSON.stringify(state)) === false;
    if (failed !== !!health.unsaved) health = failed ? { unsaved: true } : {};
  };
  adapter.watch?.((text) => {
    try { state = migrate(JSON.parse(text)); health = {}; emit(); } catch { /* unreadable there too: keep ours */ }
  });
  return {
    get: () => state,
    health: () => health,
    // update(fn): fn receives a draft copy and mutates it; listeners get the new state.
    update(fn) {
      const draft = structuredClone(state);
      fn(draft);
      state = draft;
      write();
      emit();
      return state;
    },
    replace(next) { state = migrate(next); health = {}; write(); emit(); },
    subscribe(l) { listeners.add(l); return () => listeners.delete(l); },
    exportJson: () => JSON.stringify({ app: "cs-math-skill-game", exportedAt: new Date().toISOString(), progress: state }, null, 1),
    importJson(text) {
      const doc = JSON.parse(text);
      if (doc.app !== "cs-math-skill-game" || !doc.progress) throw new Error("这不是本游戏导出的存档");
      this.replace(doc.progress);
    },
  };
}

export const dayKey = (d = new Date()) => {
  const z = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${z(d.getMonth() + 1)}-${z(d.getDate())}`;
};

// Consecutive days with any XP, ending today (or yesterday, so the streak survives until tonight).
export function streak(p, now = new Date()) {
  let n = 0;
  const d = new Date(now);
  if (!p.days[dayKey(d)]) d.setDate(d.getDate() - 1);
  while (p.days[dayKey(d)]) { n++; d.setDate(d.getDate() - 1); }
  return n;
}

export function addXp(draft, amount, now = new Date()) {
  draft.xp += amount;
  const k = dayKey(now);
  draft.days[k] = (draft.days[k] || 0) + amount;
}

// Apprentice level from total XP: level n needs 50·n·(n+1)/2 XP (50, 150, 300, …).
export function levelOf(xp) {
  let n = 0;
  while (50 * ((n + 1) * (n + 2)) / 2 <= xp) n++;
  const cur = (50 * n * (n + 1)) / 2, next = (50 * (n + 1) * (n + 2)) / 2;
  return { level: n + 1, into: xp - cur, span: next - cur };
}
