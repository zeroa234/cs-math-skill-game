// The beginner standard (docs/content-authoring.md), as checks a machine can run; every content pack
// must pass it. Each rule names the problem it guards against; the sources are in the doc.
//  B1 jargon before definition (expert blind spot; pre-training): a word from data/jargon.yaml may be
//     used only after a card defines it as **word**, or when a prerequisite skill's pack defines it, or
//     when the pack lists it under `assumes`. Defined jargon must be in `terms` (for the look-up button).
//     Programs count too: code using a keyword listed under `code` in data/jargon.yaml (for → 循环) uses
//     that term, except inside the lesson that defines it.
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
const JARGON_FILE = yaml.load(fs.readFileSync(path.join(ROOT, "data/jargon.yaml"), "utf8"));
export const JARGON = JARGON_FILE.terms;
// B1 for programs: a shown program that uses a loop uses the idea 循环 even when no prose names it
// (P.1.1's dictionary lesson counted words with a for loop two lessons before for was taught). Keywords
// are matched as whole words in fenced code blocks, items' `code` and traced programs, after string
// literals and comments are removed. Inline code is not scanned: it often names a keyword rather than
// using it ("不能用 `for` 当名字").
// Keys may list alternatives ("模块 / 第三方库"): any one of them taught is enough.
export const CODE_JARGON = Object.entries(JARGON_FILE.code || {}).map(([terms, kws]) => [terms.split(/\s*\/\s*/), new RegExp(`\\b(${kws.join("|")})\\b`)]);
const COMMENTS = { "#": /#.*$/gm, "//": /\/\/.*$|\/\*[\s\S]*?\*\//gm };
const commentStyle = (lang) => (/^(python|py|pycon|sh|bash|shell|r)$/i.test(lang || "python") ? "#" : /^(c|cpp|c\+\+|h|java|js|javascript|ts|typescript|go|rust|csharp|cs)$/i.test(lang) ? "//" : null);
const bareCode = (src, lang) => {
  const s = String(src || "").replace(/"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'/g, '""');
  const style = commentStyle(lang);
  return style ? s.replace(COMMENTS[style], "") : s;
};
const fencedCode = (t) => [...String(t || "").matchAll(/```([^\n`]*)\n([\s\S]*?)```/g)].map((m) => [m[2], m[1].trim()]);
const cardCode = (c) => [...[c.body, ...(c.reveal || []).map((r) => r.body)].flatMap(fencedCode), ...(c.sim?.name === "trace" ? [[c.sim.params?.code, "python"]] : [])];
const itemCode = (it) => [...(it.code ? [[it.code, it.lang]] : []), ...(it.sim === "trace" && it.params?.code ? [[it.params.code, "python"]] : []), ...[it.prompt, it.explain].flatMap(fencedCode)];
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
  // here: terms the current lesson defines. A lesson may show the keyword it is teaching before the card
  // that names the idea (the opening guess predicts it, PRIMM; "if：条件成立才做" comes before 分支); what
  // must not happen is code using an idea that a later lesson teaches.
  const useCode = (sources, where, here = new Set()) => {
    for (const [src, lang] of sources) {
      const code = bareCode(src, lang);
      for (const [terms, re] of CODE_JARGON) {
        const m = code.match(re);
        const key = terms.join(" / ");
        if (!m || terms.some((t) => known.has(t) || here.has(t)) || reported.has(key)) continue;
        reported.add(key);
        out.push(`B1 ${where}: the code uses \`${m[1]}\` (${key}) before any card teaches it — move the item after the lesson that does, rewrite the code without it, or list the term under assumes if a prerequisite skill teaches it`);
      }
    }
  };
  const definesIn = (l) => new Set(l.flow.filter((s) => s.card).flatMap((s) => [s.card.body, ...(s.card.reveal || []).map((r) => r.body)].flatMap(definedIn)).flatMap((d) => JARGON.filter((w) => d.startsWith(w))));
  for (const l of lessons) {
    let cardsInRow = 0, demoSeen = false;
    const lessonTeaches = definesIn(l);
    l.flow.forEach((s, i) => {
      const where = `${l.id} step ${i + 1}`;
      if (s.kind === "card") {
        const c = s.card;
        const texts = [c.body, ...(c.reveal || []).flatMap((r) => [r.title, r.body])];
        for (const d of texts.flatMap(definedIn)) for (const w of JARGON) if (d.startsWith(w) && !known.has(w)) { known.add(w); definedSomewhere.add(w); }
        for (const t of [c.title, ...texts]) use(t, where);
        useCode(cardCode(c), where, lessonTeaches);
        const chars = [...tableless(prose(c.body)).replace(/[\s*#>\-|]/g, "")].length;
        if (chars > CARD_CHARS) out.push(`B3 ${where}: card "${c.title || ""}" has ${chars} characters of prose (limit ${CARD_CHARS}) — split it into two cards with a question between`);
        if (++cardsInRow > 2) out.push(`B2 ${where}: three cards in a row without a question — ask something about what was just explained`);
        if (c.sim || c.reveal) demoSeen = true;
      } else {
        cardsInRow = 0;
        for (const t of itemTexts(s.item)) use(t, where);
        useCode(itemCode(s.item), where, lessonTeaches);
        if (s.kind === "item" && s.item.type === "sim" && !demoSeen) out.push(`B4 ${where}: graded sim "${s.item.id}" comes before any demo or worked example in this lesson`);
      }
    });
  }
  for (const it of pack.boss?.items || []) { for (const t of itemTexts(it)) use(t, `boss/${it.id}`); useCode(itemCode(it), `boss/${it.id}`); }
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
