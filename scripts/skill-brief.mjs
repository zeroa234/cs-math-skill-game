// Prints what a content author needs about one skill: chapters (game order) with source sections,
// sources, prerequisites, the original exercise and its verified answer.
// usage: node scripts/skill-brief.mjs C.2.1
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const tree = JSON.parse(fs.readFileSync(path.join(ROOT, "src/gen/tree.json"), "utf8"));
const byId = Object.fromEntries(tree.skills.map((s) => [s.id, s]));
for (const id of process.argv.slice(2)) {
  const s = byId[id];
  if (!s) { console.log(`unknown skill ${id}`); continue; }
  const L = [];
  L.push(`# ${s.id} ${s.name} (${s.en})`, `简介：${s.desc}`, `层级：${s.levels.join("–")}；${s.optional ? "选修" : "主干"}`);
  L.push(`必须前置：${s.required.map((r) => `${r.id} ${byId[r.id].name}`).join("；") || "无"}`);
  L.push(`推荐前置：${s.recommended.map((r) => `${r.id} ${byId[r.id].name}`).join("；") || "无"}`);
  L.push(`直接解锁：${s.unlocks.map((u) => `${u} ${byId[u].name}`).join("；") || "无"}`);
  L.push("", `## 章（游戏顺序，依据：${s.chapterOrder.basis}${s.chapterOrder.source ? " " + s.chapterOrder.source : ""}）`);
  for (const c of s.chapters) {
    L.push(`${c.no}. ${c.title}${c.stage === "extension" ? "（选学）" : ""}`);
    for (const r of c.zh) L.push(`   zh ${r.source}: ${r.section} [${r.extent}]`);
    for (const r of c.en) L.push(`   en ${r.source}: ${r.section} [${r.extent}]`);
    if (c.note) L.push(`   注：${c.note}`);
  }
  L.push("", "## 来源");
  for (const x of s.sources) L.push(`${x.key} [${x.lang}/${x.role}] ${x.title} — ${x.url}`);
  if (s.exercise) L.push("", `## 原综合练习（约 ${s.exercise.minutes} 分钟，覆盖：${s.exercise.covers.join("、")}）`, s.exercise.question, "", "### 已验算的答案", s.exercise.answer);
  console.log(L.join("\n") + "\n");
}
