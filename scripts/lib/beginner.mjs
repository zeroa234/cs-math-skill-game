// The beginner standard (docs/content-authoring.md), as checks a machine can run; every content pack
// must pass it. Each rule names the problem it guards against; the sources are in the doc.
//  B1 jargon before definition (expert blind spot; pre-training): a word from data/jargon.yaml may be
//     used only after a card defines it as **word**, or when a prerequisite skill's pack defines it, or
//     when the pack lists it under `assumes`. Defined jargon must be in `terms` (for the look-up button).
//  B2 explain a little, practise a little (segmenting; retrieval): at most 2 cards in a row without a
//     question.
//  B3 one idea per card: card prose (code, tables and formulas not counted) at most CARD_CHARS characters.
//  B4 worked example before an operated problem: a graded sim item needs an earlier card in the same
//     lesson that demonstrates the sim or reveals a worked example step by step.
//  B5 no skipped steps: words like 显然 / 不难看出 are not allowed.
//  B6 no self-assessment anywhere.
//  B7 the final challenge has enough checks: at least max(5, core chapters).
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import * as yaml from "js-yaml";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
export const JARGON = yaml.load(fs.readFileSync(path.join(ROOT, "data/jargon.yaml"), "utf8")).terms;
export const CARD_CHARS = 240;
const SKIPPED = ["显然", "易知", "易得", "不难看出", "不难发现", "同理可得", "众所周知", "简单地说就是"];
const SELF = ["自评", "你掌握得怎么样", "全做对了", "我已经会了", "如实评价"];

// Prose only: code blocks, inline code, math and look-up links' definitions are not scanned.
export const prose = (t) => String(t || "")
  .replace(/```[\s\S]*?```/g, " ")
  .replace(/`[^`]*`/g, " ")
  .replace(/\$\$[\s\S]*?\$\$/g, " ")
  .replace(/\$[^$\n]*\$/g, " ")
  .replace(/\[\[([^\]|]+)(\|[^\]]*)?\]\]/g, "$1");
const tableless = (t) => t.split("\n").filter((l) => !/^\s*\|/.test(l)).join("\n");
const definedIn = (t) => [...String(t || "").matchAll(/\*\*([^*]+)\*\*/g)].map((m) => m[1]);

function itemTexts(it) {
  return [it.prompt, ...(it.options || []).flatMap((o) => [o.text, o.why]), ...(it.pairs || []).flat(), ...(it.type === "order" ? it.steps : []), it.hint, it.explain];
}

// lessons: normalised, in play order. inherited: terms taught by prerequisite skills' packs.
export function beginnerIssues(pack, lessons, { inherited = new Set(), coreChapters = 1 } = {}) {
  const out = [];
  const listed = new Set((pack.terms || []).map((t) => t.term));
  const known = new Set([...inherited, ...(pack.assumes || [])]);
  const definedSomewhere = new Set();
  const reported = new Set();
  const use = (text, where) => {
    const t = prose(text);
    for (const w of JARGON) {
      if (!t.includes(w) || known.has(w) || reported.has(w)) continue;
      reported.add(w);
      out.push(`B1 ${where}: "${w}" is used before any card defines it — define it as **${w}** in a card first (and add it to terms), or list it under assumes if a prerequisite skill teaches it`);
    }
    for (const p of SKIPPED) if (t.includes(p)) out.push(`B5 ${where}: "${p}" skips a step for a beginner — write the step out`);
    for (const p of SELF) if (String(text || "").includes(p)) out.push(`B6 ${where}: self-assessment ("${p}") is not allowed`);
  };
  for (const l of lessons) {
    let cardsInRow = 0, demoSeen = false;
    l.flow.forEach((s, i) => {
      const where = `${l.id} step ${i + 1}`;
      if (s.kind === "card") {
        const c = s.card;
        const texts = [c.body, ...(c.reveal || []).flatMap((r) => [r.title, r.body])];
        for (const d of texts.flatMap(definedIn)) for (const w of JARGON) if (d.startsWith(w) && !known.has(w)) { known.add(w); definedSomewhere.add(w); }
        for (const t of [c.title, ...texts]) use(t, where);
        const chars = [...tableless(prose(c.body)).replace(/[\s*#>\-|]/g, "")].length;
        if (chars > CARD_CHARS) out.push(`B3 ${where}: card "${c.title || ""}" has ${chars} characters of prose (limit ${CARD_CHARS}) — split it into two cards with a question between`);
        if (++cardsInRow > 2) out.push(`B2 ${where}: three cards in a row without a question — ask something about what was just explained`);
        if (c.sim || c.reveal) demoSeen = true;
      } else {
        cardsInRow = 0;
        for (const t of itemTexts(s.item)) use(t, where);
        if (s.kind === "item" && s.item.type === "sim" && !demoSeen) out.push(`B4 ${where}: graded sim "${s.item.id}" comes before any demo or worked example in this lesson`);
      }
    });
  }
  for (const it of pack.boss?.items || []) for (const t of itemTexts(it)) use(t, `boss/${it.id}`);
  for (const w of definedSomewhere) if (!listed.has(w)) out.push(`B1 terms: "${w}" is defined in a card but missing from terms (the look-up button needs it)`);
  const bolded = lessons.flatMap((l) => l.flow.filter((s) => s.card).flatMap((s) => [s.card.body, ...(s.card.reveal || []).map((r) => r.body)].flatMap(definedIn)));
  for (const t of pack.terms || []) if (!bolded.some((d) => d.startsWith(t.term))) out.push(`B1 terms: "${t.term}" is never defined as **${t.term}** in a card`);
  const need = Math.max(5, coreChapters);
  if ((pack.boss?.items || []).length < need) out.push(`B7 boss: ${(pack.boss?.items || []).length} checks; the final challenge needs at least ${need} (one per core chapter, at least 5)`);
  return out;
}

// Look-up links, so a term met again in a review weeks later is one tap from its definition (recognition
// rather than recall). The first time each glossary term appears in a question's prompt, hint or
// explanation it becomes [[term|definition]] (definition URI-encoded, so brackets in it are safe), which
// md.jsx renders as a button. Cards link only terms defined in an earlier lesson or a prerequisite skill;
// the lesson that defines a term already shows it. Never inside code, math, bold or an existing link,
// never single-character terms (too common), and never inside option buttons or match chips (a button
// cannot hold a button): there a hand-written [[term]] becomes the plain term.
// glossary: { term: definition } of this pack's prerequisites; the pack's own terms are added here.
const SKIP = /(```[\s\S]*?```|`[^`\n]*`|\$\$[\s\S]*?\$\$|\$[^$\n]*\$|\[\[[^\]]*\]\]|\*\*[^*]+\*\*)/;
export function resolveTerms(pack, lessons, glossary = {}) {
  const defs = { ...glossary, ...Object.fromEntries((pack.terms || []).map((t) => [t.term, t.def])) };
  const auto = Object.keys(defs).filter((w) => [...w].length > 1).sort((a, b) => b.length - a.length);
  const token = (w) => `[[${w}|${encodeURIComponent(defs[w])}]]`;
  const link = (t, except = new Set()) => {
    if (typeof t !== "string") return t;
    const done = new Set(except);
    return t.replace(/\[\[([^\]|]+)\]\]/g, (m, w) => (defs[w] ? token(w) : m)).split(SKIP).map((seg, i) => {
      if (i % 2) { const m = seg.match(/^\[\[([^\]|]+)\|/); if (m) done.add(m[1]); return seg; }
      const taken = [];
      for (const w of auto) {
        if (done.has(w)) continue;
        let at = seg.indexOf(w);
        while (at !== -1 && taken.some(([a, b]) => at < b && at + w.length > a)) at = seg.indexOf(w, at + 1);
        if (at === -1) continue;
        taken.push([at, at + w.length, w]);
        done.add(w);
      }
      let out = "", pos = 0;
      for (const [a, b, w] of taken.sort((x, y) => x[0] - y[0])) { out += seg.slice(pos, a) + token(w); pos = b; }
      return out + seg.slice(pos);
    }).join("");
  };
  const plain = (t) => (typeof t === "string" ? t.replace(/\[\[([^\]|]+)\]\]/g, (m, w) => (defs[w] ? w : m)) : t);
  const item = (it) => ({ ...it, prompt: link(it.prompt), hint: link(it.hint), explain: link(it.explain), options: it.options?.map((o) => ({ ...o, text: plain(o.text), why: plain(o.why) })), pairs: it.pairs?.map((p) => p.map(plain)), ...(it.type === "order" ? { steps: it.steps.map(plain) } : {}) });
  const own = new Set((pack.terms || []).map((t) => t.term));
  return {
    lessons: lessons.map((l) => {
      // terms this lesson defines are not linked in its own cards
      const here = new Set(l.flow.filter((s) => s.card).flatMap((s) => [s.card.body, ...(s.card.reveal || []).map((r) => r.body)].flatMap(definedIn)).flatMap((d) => [...own].filter((w) => d.startsWith(w))));
      const card = (c) => ({ ...c, body: link(c.body, here), reveal: c.reveal?.map((r) => ({ ...r, body: link(r.body, here) })) });
      return { ...l, flow: l.flow.map((s) => (s.card ? { ...s, card: card(s.card) } : { ...s, item: item(s.item) })) };
    }),
    boss: pack.boss ? { ...pack.boss, items: pack.boss.items.map(item) } : pack.boss,
  };
}
