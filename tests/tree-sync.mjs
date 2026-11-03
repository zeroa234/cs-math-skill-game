// Upstream promotion must preserve the skill, interactive lessons and all outline depths.
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { emptyProgress } from "../src/game/core/progress.js";
import { ROOT as root, GAME_URL, launchEdge } from "../scripts/lib/edge.mjs";

const read = p => JSON.parse(fs.readFileSync(path.join(root, p), "utf8"));
const tree = read("../cs-math-skill-tree/output/skilltree.json");
const game = read("src/gen/tree.json");
const sourceMaps = read("../cs-math-skill-tree/output/outlines.json");
const sandbox = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(root, "src/web/outlines.js"), "utf8"), sandbox);
const gameMaps = sandbox.window.__OUTLINES__;
assert.deepEqual(game.skills.map(s => s.id).sort(), tree.skills.filter(s => s.domain !== "X").map(s => s.id).sort());
const skill = game.skills.find(s => s.id === "C.3.5");
const original = tree.skills.find(s => s.id === skill.id);
assert.equal(skill.optional, false);
assert.equal(skill.optional, original.optional);
assert.equal(skill.origin, "cs-math-skill-tree");
assert.deepEqual(skill.required.map(r => r.id), original.required.map(r => r.id));
assert(skill.exercise && skill.hasOutline);
assert.equal(skill.chapters.length, 6);
const flatten = (items, field, ref) => items.flatMap(it => [{ number: String(it[field]), ref: it[ref] || null, title: it.title }, ...flatten(it.items || [], field, ref)]);
for (const s of game.skills) {
  if (!sourceMaps[s.id]) continue;
  const expected = flatten(sourceMaps[s.id].outline, "number", "ref");
  const actual = flatten(gameMaps[s.id].branches, "no", "sourceRef");
  assert.equal(JSON.stringify(actual), JSON.stringify(expected), `${s.id}: lost or changed an upstream outline section`);
}
const count = flatten(sourceMaps[skill.id].outline, "number", "ref").length;
const tmp = path.join(root, "temp/tree-sync");
const browser = await launchEdge(tmp);
const errors = [];
try {
  for (const viewport of [{ width: 1366, height: 860 }, { width: 390, height: 844 }]) {
    const context = await browser.newContext({ viewport });
    const progress = emptyProgress();
    progress.settings.introSeen = true;
    await context.addInitScript(p => localStorage.setItem("cs-math-skill-game/progress", JSON.stringify(p)), progress);
    const page = await context.newPage();
    page.on("pageerror", e => errors.push(e.message));
    await page.goto(GAME_URL + "#/skill/C.3.5");
    await page.waitForSelector(".skill h1");
    assert(!(await page.locator(".skill-head .kicker").innerText()).includes("选修"));
    await page.getByRole("button", { name: "展开知识地图（主教材目录）" }).click();
    await page.waitForSelector(".outline li");
    assert.equal(await page.locator(".outline li").count(), count, "rendered outline lost nested sections");
    assert(await page.locator(".outline").innerText().then(t => t.includes("3.1.1") || t.includes("3.2.1") || /\d+\.\d+\.\d+/.test(t)));
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), "page overflows horizontally");
    await page.screenshot({ path: path.join(tmp, `hpn-${viewport.width}.png`), fullPage: true });
    await context.close();
  }
  assert.deepEqual(errors, []);
} finally { await browser.close(); }
console.log(`PASS: ${game.skills.length} unique upstream skills; C.3.5 core, 6 chapters, ${count} outline sections; desktop/mobile`);
