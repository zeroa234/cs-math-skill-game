// Checks coverage tables against the skill-tree outline (rule C1, scripts/lib/coverage.mjs).
// usage: node scripts/check-coverage.mjs P.1.1 [more skill ids…]   (no ids: every pack)
// Exit code 1 when any table has issues.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadPack } from "./lib/packs.mjs";
import { coverageIssues, readCoverageTable } from "./lib/coverage.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outlines = JSON.parse(fs.readFileSync(path.join(ROOT, "../cs-math-skill-tree/output/outlines.json"), "utf8"));
const dir = path.join(ROOT, "data/content");
const packs = Object.fromEntries(fs.readdirSync(dir).filter((f) => f.endsWith(".yaml")).map((f) => { const p = loadPack(path.join(dir, f)); return [p.skill, p]; }));
const ids = process.argv.slice(2).length ? process.argv.slice(2) : Object.values(packs).map((p) => p.skill);
let bad = 0;
for (const id of ids) {
  const r = coverageIssues(id, outlines[id], packs[id], readCoverageTable(path.join(ROOT, "reports/coverage", id + ".md")));
  if (r.issues.length) { bad++; console.log(`ERR ${id}\n  - ` + r.issues.join("\n  - ")); }
  else console.log(`ok  ${id}: ${r.taught} sections taught, ${r.skipped} not taught with a reason, ${r.total} in the outline`);
}
process.exit(bad ? 1 : 0);
