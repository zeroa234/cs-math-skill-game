// Accessibility audit (axe-core, WCAG 2.2 AA tags) of the main screens in the system Edge.
// usage: node tests/a11y.mjs   — prints violations; exit 1 if any serious/critical ones remain.
import fs from "node:fs";
import path from "node:path";
import { ROOT, GAME_URL as url, launchEdge } from "../scripts/lib/edge.mjs";
import { finishAllLessons } from "./lib/play.mjs";

const axe = fs.readFileSync(path.join(ROOT, "node_modules/axe-core/axe.min.js"), "utf8");
const packs = JSON.parse(fs.readFileSync(path.join(ROOT, "src/gen/content.json"), "utf8"));
const browser = await launchEdge();
// The intro shows on a fresh profile: audit it first, then skip it so "" is the camp.
const views = ["#/intro", "#/pick", "", "#/route/goal:C.2.1", "#/route/ai", "#/route/algo", "#/skill/F.1.2", "#/skill/C.2.1", "#/skill/M.1.1", "#/lesson/P.1.1/first-program", "#/lesson/C.2.1/replacement", "#/boss/C.2.1/test", "#/boss/M.1.1", "#/boss/C.3.5", "#/review", "#/me", "#/lab", "#/map"];
let bad = 0;
for (const scheme of ["light", "dark"]) {
  const ctx = await browser.newContext({ viewport: { width: 1366, height: 860 }, colorScheme: scheme });
  const p = await ctx.newPage();
  for (const v of views) {
    await p.goto(url + v);
    await p.waitForTimeout(v === "#/intro" ? 900 : 300);
    if (await p.$(".exercise-answer summary")) await p.click(".exercise-answer summary");
    await p.addScriptTag({ content: axe });
    const res = await p.evaluate(() => window.axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"] } }));
    for (const r of res.violations) {
      const serious = r.impact === "serious" || r.impact === "critical";
      if (serious) bad++;
      console.log(`${scheme} ${v || "#/"} [${r.impact}] ${r.id}: ${r.help} — ${r.nodes.length} nodes, e.g. ${r.nodes[0].target.join(" ")}`);
    }
    if (v === "#/intro") await p.click(".intro .skip");
    // a lesson after an answer: the verdict bar and its button are only there in this state
    if (v === "#/lesson/P.1.1/first-program") {
      for (const pick of [0, 2]) {
        await p.goto(url + "#/review"); await p.goto(url + v); await p.waitForSelector(".lcard .option");
        await p.locator(".lcard .option").nth(pick).click(); await p.click(".answer-bar .btn"); await p.waitForTimeout(400);
        const res2 = await p.evaluate(() => window.axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"] } }));
        for (const r of res2.violations) {
          if (r.impact === "serious" || r.impact === "critical") bad++;
          console.log(`${scheme} ${v} answered [${r.impact}] ${r.id}: ${r.help} — ${r.nodes.length} nodes, e.g. ${r.nodes[0].target.join(" ")}`);
        }
      }
    }
  }
  // the 实验室 with every experiment met (on a fresh profile it is empty)
  await finishAllLessons(p, packs);
  await p.goto(url + "#/lab");
  await p.waitForSelector(".lab-item");
  await p.addScriptTag({ content: axe });
  for (const r of (await p.evaluate(() => window.axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"] } }))).violations) {
    if (r.impact === "serious" || r.impact === "critical") bad++;
    console.log(`${scheme} #/lab (every experiment) [${r.impact}] ${r.id}: ${r.help} — ${r.nodes.length} nodes, e.g. ${r.nodes[0].target.join(" ")}`);
  }
  await p.evaluate(() => {
    Storage.prototype.setItem = () => { throw new DOMException("Test quota", "QuotaExceededError"); };
  });
  await p.locator(".topbar button[aria-pressed]").click();
  await p.waitForSelector(".save-warning");
  const contrast = await p.evaluate(async () => {
    const result = await window.axe.run(".save-warning", { runOnly: ["color-contrast"] });
    const nodes = result.passes.flatMap((rule) => rule.nodes);
    const tags = nodes.map((node) => document.querySelector(node.target[0])?.tagName);
    return { tags, violations: result.violations.length, incomplete: result.incomplete.length };
  });
  if (contrast.violations || !["DIV", "B", "A"].every((tag) => contrast.tags.includes(tag))) {
    bad++;
    console.log(`${scheme} .save-warning contrast did not pass: ${JSON.stringify(contrast)}`);
  } else {
    console.log(`${scheme} .save-warning text and link passed WCAG AA contrast`);
  }
  await ctx.close();
}
await browser.close();
console.log(bad ? `${bad} serious/critical violation groups` : "no serious/critical violations");
process.exit(bad ? 1 : 0);
