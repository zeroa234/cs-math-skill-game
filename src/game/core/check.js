// Answer checking for every item type. Pure: (item, response) → { correct, detail }.
// Sims register their own checkers (src/game/sims/registry.js) and are looked up by name here.

const simCheckers = new Map();
export const registerSimChecker = (name, fn) => simCheckers.set(name, fn);

// Full-width → half-width, unify minus signs and spaces, so "１／２" and "1/2" compare equal.
export function normalizeText(s, caseSensitive = false) {
  let t = String(s ?? "")
    .replace(/[！-～]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xfee0))
    .replace(/　/g, " ")
    .replace(/[−–—]/g, "-")
    .replace(/\s+/g, " ")
    .trim();
  if (!caseSensitive) t = t.toLowerCase();
  return t;
}

// Accepts "1.5", "3/2", "-0.25", "1e-3", "50%", "2^10", "1,024". Returns NaN when unreadable.
export function parseNumber(input) {
  let t = normalizeText(input).replace(/,/g, "").replace(/\s/g, "");
  if (!t) return NaN;
  let scale = 1;
  if (t.endsWith("%")) { scale = 0.01; t = t.slice(0, -1); }
  let m;
  if ((m = t.match(/^(-?\d+(?:\.\d+)?)\/(-?\d+(?:\.\d+)?)$/))) return (Number(m[1]) / Number(m[2])) * scale;
  if ((m = t.match(/^(-?\d+(?:\.\d+)?)\^(-?\d+)$/))) return Math.pow(Number(m[1]), Number(m[2])) * scale;
  const n = Number(t);
  return Number.isFinite(n) ? n * scale : NaN;
}

const sameSet = (a, b) => a.length === b.length && a.every((x) => b.includes(x));

export function checkItem(item, response) {
  switch (item.type) {
    case "choice": {
      const want = item.options.map((o, i) => (o.correct ? i : -1)).filter((i) => i >= 0);
      const got = Array.isArray(response) ? response : [response];
      return { correct: sameSet(want, got), detail: { want } };
    }
    case "number": {
      const n = parseNumber(response);
      if (Number.isNaN(n)) return { correct: false, detail: { unreadable: true } };
      const tol = item.tolerance ?? Math.max(1e-9, Math.abs(item.answer) * 1e-6);
      return { correct: Math.abs(n - item.answer) <= tol, detail: { value: n } };
    }
    case "text": {
      const got = normalizeText(response, item.caseSensitive);
      // A list answer like "[1, 3, 7]" also accepts "1,3,7", "1 3 7" or "[1,3,7]".
      const tokens = (s) => s.replace(/^\[|\]$/g, "").split(/[\s,，、]+/).filter(Boolean).join(" ");
      const same = (a) => {
        const want = normalizeText(a, item.caseSensitive);
        return want === got || (want.startsWith("[") && tokens(want) === tokens(got));
      };
      return { correct: item.answers.some(same), detail: {} };
    }
    case "order": {
      // response: array of step indices in the order the player put them
      const ok = Array.isArray(response) && response.length === item.steps.length && response.every((v, i) => v === i);
      return { correct: ok, detail: {} };
    }
    case "match": {
      // response: array where response[i] = index of the right-hand text chosen for left i
      const ok = Array.isArray(response) && response.length === item.pairs.length && response.every((v, i) => v === i);
      return { correct: ok, detail: { wrong: Array.isArray(response) ? response.map((v, i) => v !== i) : [] } };
    }
    case "sim": {
      const fn = simCheckers.get(item.sim);
      if (!fn) throw new Error(`no checker registered for sim "${item.sim}"`);
      return fn(item.params || {}, item.goal || {}, response);
    }
    default:
      throw new Error(`unknown item type ${item.type}`);
  }
}

// Which items enter the spaced-review deck: anything gradable without a big widget, unless the
// author opted out; sims only when the author opted in.
export const reviewable = (item) => (item.type === "sim" ? item.review === true : item.review !== false);
