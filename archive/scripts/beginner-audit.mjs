// Runs the beginner standard (scripts/lib/beginner.mjs) over every content pack, whatever its version,
// and writes reports/beginner-audit.md: how far each pack is from being learnable from zero.
// usage: node scripts/beginner-audit.mjs   (needs src/gen/tree.json: npm run data)
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadPack, playOrder, inheritedTerms } from "./lib/packs.mjs";
import { beginnerIssues, prose, CARD_CHARS } from "./lib/beginner.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const tree = JSON.parse(fs.readFileSync(path.join(ROOT, "src/gen/tree.json"), "utf8"));
const byId = Object.fromEntries(tree.skills.map((s) => [s.id, s]));
const dir = path.join(ROOT, "data/content");
const packs = Object.fromEntries(fs.readdirSync(dir).filter((f) => f.endsWith(".yaml")).map((f) => loadPack(path.join(dir, f))).map((p) => [p.skill, p]));
const rows = [];
const examples = [];
for (const [id, pack] of Object.entries(packs).sort()) {
  const skill = byId[id];
  const lessons = playOrder(pack, skill);
  const issues = beginnerIssues(pack, lessons, { inherited: inheritedTerms(id, byId, packs), coreChapters: skill.chapters.filter((c) => c.stage === "core").length });
  const count = (k) => issues.filter((m) => m.startsWith(k + " ")).length;
  const cards = lessons.flatMap((l) => l.flow.filter((s) => s.card));
  const chars = cards.map((s) => [...prose(s.card.body).replace(/\s/g, "")].length);
  const words = lessons.reduce((n, l) => n + l.flow.reduce((m, s) => m + (s.card ? [...prose(s.card.body).replace(/\s/g, "")].length : 0), 0), 0);
  rows.push(`| ${id} ${skill.name} | v${pack.version} | ${lessons.length} | ${cards.length} | ${Math.round(words / lessons.length)} | ${count("B1")} | ${count("B2")} | ${count("B3")} | ${count("B4")} | ${count("B5")} | ${count("B7")} |`);
  examples.push(`### ${id} ${skill.name}\n\n` + (issues.filter((m) => m.startsWith("B1")).slice(0, 6).map((m) => "- " + m).join("\n") || "- 没有 B1 问题"));
}
const md = `# 零基础标准审计（beginner audit）

由 \`node scripts/beginner-audit.mjs\` 生成，规则见 \`docs/content-authoring.md\`“写给零基础的标准”，检查代码 \`scripts/lib/beginner.mjs\`。旧格式（version 1）的课按“先猜 → 全部讲解卡 → 全部练习”的顺序检查。

列：课数；讲解卡数；每课讲解文字（字，不算代码和公式）；B1 术语先用后讲（每个术语只记第一次）；B2 连续三张卡没有提问；B3 一张卡超过 ${CARD_CHARS} 字；B4 操作题之前没有演示或分步例题；B5 “显然”类跳步词；B7 结业挑战题太少。

| 技能 | 版本 | 课 | 卡 | 字/课 | B1 | B2 | B3 | B4 | B5 | B7 |
|---|---|---|---|---|---|---|---|---|---|---|
${rows.join("\n")}

## 每个包最先出现的几处“术语先用后讲”

${examples.join("\n\n")}
`;
fs.writeFileSync(path.join(ROOT, "reports/beginner-audit.md"), md);
console.log(rows.join("\n"));
