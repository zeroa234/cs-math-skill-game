// The knowledge-coverage standard's rule C1 (docs/content-authoring.md), as a check a machine can run.
// A pack's coverage table reports/coverage/<skill>.md has one row per section of the skill-tree outline
// (../cs-math-skill-tree/output/outlines.json, keyed by the skill-internal section number):
//   | 2.4 | 4.4 break and continue Statements | `if-else`, `loop-control` |
//   | 2.10 | 4.10 Intermezzo: Coding Style | 不教：…理由… |
// The third cell names the lessons that teach it (lesson ids in backticks) or starts with 不教 and gives
// the reason (which skill teaches it, or why it is beyond the beginner level).
// Checks: every leaf section has a row; every lesson id exists in the pack; a section the outline's
// `coverage` names is taught (a named chapter: at least one of its sections is taught). The other
// columns and the sections below the table (CS2023, exercises, successors: C2–C5) are read by people.
// Depth (added 2026-11-08): a table can hand 70 sections to 13 two-card lessons and still pass, so the
// pack's explanation (beginner.mjs explanationChars) must come to at least SECTION_CHARS characters per
// taught section. The 12 packs kept after reports/quality-audit-2026-11-08.md have 233–1266; the 35
// archived template packs had 24–206.
import fs from "node:fs";
import { explanationChars } from "./beginner.mjs";

export const SECTION_CHARS = 200;

// Leaf sections in outline order: a chapter's items, or the chapter itself when it has none.
export function outlineLeaves(outline) {
  const out = [];
  const walk = (nodes) => { for (const n of nodes) (n.items?.length ? walk(n.items) : out.push(n)); };
  walk(outline.outline || []);
  return out;
}

export function parseCoverageTable(md) {
  const rows = new Map();
  for (const line of md.split("\n")) {
    const cells = line.split("|").slice(1, -1).map((c) => c.trim());
    if (cells.length < 3 || !/^\d+(\.\d+)*$/.test(cells[0])) continue;
    const where = cells[cells.length - 1];
    rows.set(cells[0], { lessons: [...where.matchAll(/`([a-z0-9-]+)`/g)].map((m) => m[1]), skip: /^不教/.test(where), text: where });
  }
  return rows;
}

// Returns { issues: [...], taught, skipped, total }.
export function coverageIssues(skillId, outline, pack, md) {
  const issues = [];
  if (!outline) return { issues: [`${skillId}: the skill tree has no outline`], taught: 0, skipped: 0, total: 0 };
  if (md == null) return { issues: [`${skillId}: no coverage table reports/coverage/${skillId}.md`], taught: 0, skipped: 0, total: 0 };
  const rows = parseCoverageTable(md);
  const lessonIds = new Set((pack?.lessons || []).map((l) => l.id));
  const leaves = outlineLeaves(outline);
  let taught = 0, skipped = 0;
  for (const n of leaves) {
    const r = rows.get(n.number);
    if (!r) { issues.push(`C1 ${n.number} ${n.title}: no row in the coverage table`); continue; }
    if (r.skip) { skipped++; if (r.text.replace(/^不教[：:]?\s*/, "").length < 4) issues.push(`C1 ${n.number}: 不教 needs a reason`); continue; }
    if (!r.lessons.length) { issues.push(`C1 ${n.number} ${n.title}: name the lessons that teach it, or write 不教：<reason>`); continue; }
    taught++;
    for (const id of r.lessons) if (!lessonIds.has(id)) issues.push(`C1 ${n.number}: lesson \`${id}\` is not in the pack`);
  }
  const leafNumbers = new Set(leaves.map((n) => n.number));
  for (const k of rows.keys()) if (!leafNumbers.has(k)) issues.push(`C1 ${k}: not a section of the outline`);
  const isTaught = (no) => { const r = rows.get(no); return !!r && !r.skip && r.lessons.length > 0; };
  for (const c of outline.coverage || []) {
    for (const no of c.sections || []) {
      const ok = leafNumbers.has(no) ? isTaught(no) : leaves.some((n) => n.number.startsWith(no + ".") && isTaught(n.number));
      if (!ok) issues.push(`C1 ${no}: the outline's coverage names it for "${c.topic}", so a lesson must teach it`);
    }
  }
  const chars = (pack?.lessons || []).reduce((n, l) => n + explanationChars(l), 0);
  if (taught && chars / taught < SECTION_CHARS) issues.push(`C1 depth: ${Math.round(chars / taught)} characters of explanation per taught section (at least ${SECTION_CHARS}) — the table names more sections than the lessons teach`);
  return { issues, taught, skipped, total: leaves.length };
}

export const readCoverageTable = (file) => (fs.existsSync(file) ? fs.readFileSync(file, "utf8") : null);
