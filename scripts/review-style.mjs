// Review aid for the human-read rules of docs/content-authoring.md (R5 distractors, beginner wording,
// glossary links). Not a gate: it lists candidates for a person (or the writing AI) to read and judge.
// usage: npm run data && node scripts/review-style.mjs <skillId>... [--out file.md]
//
// 1. Single-choice items whose correct option is the longest one: a player who always picks the
//    longest option wins. Packs read and accepted earlier sit at 58–63 % (P.1.1, M.1.1, M.6.1, M.1.4.1).
// 2. Glossary links inherited from prerequisite packs ([[word|definition]] in src/gen/content.json):
//    the definition comes from another skill and may mean something else here (切片 in a distributed-
//    computing card pops the Python slicing definition).
// 3. Latin-letter terms (AUC, OOM, Group Split…) used in a pack without a **bold definition** or a
//    `terms` entry in that pack: candidates for "used before explained" that data/jargon.yaml misses.
// 4. Exaggerated words that docs/collaboration.md rules out for lesson text ("陈述句，不用感叹号和夸张词").
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const outAt = args.indexOf("--out");
const outFile = outAt >= 0 ? args.splice(outAt, 2)[1] : null;
const packs = JSON.parse(fs.readFileSync(path.join(ROOT, "src/gen/content.json"), "utf8"));
const HYPE = ["！", "竟然", "神奇", "狂", "死死", "彻底", "绝对", "足足", "赫然", "暴跌", "飙", "红利", "铁律", "真真实实", "天生", "轻松", "极其", "极度", "当场", "罪魁祸首", "毁掉", "十万八千里", "一毫秒", "吐出"];

const LINK = /\[\[([^|\]]+)\|([^\]]*)\]\]/g;
const plain = (t) => String(t || "").replace(LINK, "$1");
const prose = (t) => plain(t).replace(/\$\$[\s\S]*?\$\$|\$[^$]*\$|`[^`]*`/g, " ");

function texts(pack) {
  const out = []; // [where, text]
  const item = (where, it) => {
    for (const k of ["prompt", "explain", "hint"]) if (it[k]) out.push([where, it[k]]);
    for (const o of it.options || []) { out.push([where, o.text]); if (o.why) out.push([where, o.why]); }
    for (const pr of it.pairs || []) out.push([where, pr.join(" ")]);
    for (const s of it.steps || []) out.push([where, s]);
  };
  for (const l of pack.lessons) for (const s of l.flow) {
    if (s.item) item(`${l.id}/${s.item.id}`, s.item);
    else if (s.card) {
      const w = `${l.id}/卡「${(s.card.title || "").slice(0, 14)}」`;
      if (s.card.title) out.push([w, s.card.title]);
      if (s.card.body) out.push([w, s.card.body]);
      for (const r of s.card.reveal || []) out.push([w, (r.title || "") + "\n" + (r.body || "")]);
    }
  }
  for (const it of pack.boss?.items || []) item(`结业/${it.id}`, it);
  return out;
}

function review(id) {
  const pack = packs[id];
  if (!pack) return `## ${id}\n\n没有这个内容包（先 npm run data）。\n`;
  const lines = [`## ${id}`, ""];
  const items = [...pack.lessons.flatMap((l) => l.flow.filter((s) => s.item).map((s) => [`${l.id}/${s.item.id}`, s.item])), ...(pack.boss?.items || []).map((it) => [`结业/${it.id}`, it])];
  const single = items.filter(([, it]) => it.type === "choice" && !it.multi);
  const longest = single.filter(([, it]) => {
    const len = it.options.map((o) => plain(o.text).length);
    return len[it.options.findIndex((o) => o.correct)] === Math.max(...len);
  });
  const boss = longest.filter(([w]) => w.startsWith("结业/")).length, bossAll = single.filter(([w]) => w.startsWith("结业/")).length;
  lines.push(`### 1. 正确项是最长的选项：${longest.length}/${single.length}（${Math.round((100 * longest.length) / Math.max(1, single.length))}%；结业挑战 ${boss}/${bossAll}）`, "");
  lines.push(longest.map(([w]) => "`" + w + "`").join("、") || "无", "");

  const own = new Set(pack.terms.map((t) => t.term));
  const inherited = new Map();
  for (const [w, t] of texts(pack)) for (const m of String(t).matchAll(LINK)) {
    if (own.has(m[1]) || inherited.has(m[1])) continue;
    let def = m[2]; try { def = decodeURIComponent(m[2]); } catch {}
    inherited.set(m[1], [w, def]);
  }
  lines.push(`### 2. 从前置技能继承的查词（${inherited.size} 个，逐个确认在这里意思对得上）`, "");
  for (const [term, [w, def]] of inherited) lines.push(`- **${term}**（首次 \`${w}\`）：${def}`);
  lines.push("");

  const all = texts(pack);
  const bold = all.map(([, t]) => [...plain(t).matchAll(/\*\*([^*]+)\*\*/g)].map((m) => m[1]).join(" ")).join(" ") + " " + pack.terms.map((t) => t.term + " " + t.def).join(" ");
  const latin = new Map();
  for (const [w, t] of all) for (const m of prose(t).matchAll(/\b(?:[A-Z]{2,}[A-Za-z0-9]*|[A-Z][a-z]+(?:[ -][A-Z][a-z]+)+)\b/g)) {
    const tok = m[0];
    if (latin.has(tok) || bold.includes(tok)) continue;
    latin.set(tok, w);
  }
  lines.push(`### 3. 本包没有加粗讲解、也不在 terms 里的英文词（${latin.size} 个，候选“没讲就用”）`, "");
  lines.push([...latin].map(([t, w]) => `${t}（\`${w}\`）`).join("、") || "无", "");

  const hype = new Map();
  for (const [w, t] of all) for (const word of HYPE) if (prose(t).includes(word)) { if (!hype.has(word)) hype.set(word, []); hype.get(word).push(w); }
  lines.push(`### 4. 夸张词（${[...hype.values()].reduce((a, b) => a + b.length, 0)} 处）`, "");
  for (const [word, ws] of hype) lines.push(`- 「${word}」${ws.length} 处：${[...new Set(ws)].slice(0, 6).map((w) => "`" + w + "`").join("、")}${ws.length > 6 ? " 等" : ""}`);
  lines.push("");
  return lines.join("\n");
}

const md = args.map(review).join("\n");
if (outFile) { fs.mkdirSync(path.dirname(path.resolve(outFile)), { recursive: true }); fs.writeFileSync(outFile, md); console.log("wrote " + outFile); }
else console.log(md);
