// Screenshots of the main screens at a real display setting, for checking the look by eye.
// usage: node tests/look.mjs [out-dir] [--dark] [--phone]   (needs npm run build; uses the system Edge)
// Default: 1440 × 900 CSS px at 200 % scaling (devicePixelRatio 2), the author's laptop setting.
import fs from "node:fs";
import path from "node:path";
import { ROOT, GAME_URL as url, launchEdge } from "../scripts/lib/edge.mjs";

const args = process.argv.slice(2);
const out = path.resolve(args.find((a) => !a.startsWith("--")) || path.join(ROOT, "temp/look"));
fs.mkdirSync(out, { recursive: true });
const dark = args.includes("--dark"), phone = args.includes("--phone");
const browser = await launchEdge();
const ctx = await browser.newContext({ viewport: phone ? { width: 390, height: 844 } : { width: 1440, height: 900 }, deviceScaleFactor: phone ? 3 : 2, colorScheme: dark ? "dark" : "light" });
const p = await ctx.newPage();
const tag = (dark ? "dark-" : "") + (phone ? "phone-" : "");
const shot = async (name, full = false) => { await p.waitForTimeout(400); await p.screenshot({ path: path.join(out, `${tag}${name}.png`), fullPage: full }); };
await p.goto(url);
await p.evaluate(() => localStorage.setItem("cs-math-skill-game/progress", JSON.stringify({ v: 2, settings: { introSeen: true, route: "goal:C.2.1", sound: false, sourceLang: "zh" }, skills: {}, lessons: {}, cards: {}, days: {}, achievements: {}, xp: 0 })));
const screens = [["home", "#/"], ["pick", "#/pick"], ["route", "#/route/goal:C.2.1"], ["route-dev", "#/route/web"], ["skill", "#/skill/P.1.1"], ["boss", "#/boss/P.1.1/test"], ["map", "#/map"], ["review", "#/review"], ["lab", "#/lab"]];
for (const [name, hash] of screens) { await p.goto(url + hash); await p.reload(); await shot(name); }
await p.goto(url + "#/lesson/P.1.1/first-program");
await p.reload();
await shot("lesson-guess");
await p.click(".qcard .option");
await p.click(".answer-bar .btn.primary");
await shot("lesson-verdict");
await p.click(".answer-bar .inner > .btn");
await shot("lesson-card");
// Walks a lesson to the first card or question matching `until`, answering anything on the way.
async function walkTo(hash, until) {
  await p.goto(url + hash);
  await p.reload();
  for (let i = 0; i < 40 && !(await until()); i++) {
    if (await p.$(".qcard .option") && !(await p.$(".answer-bar.is-good, .answer-bar.is-bad"))) await p.click(".qcard .option");
    else if (await p.$(".qcard .answer-line input") && !(await p.$(".answer-bar.is-good, .answer-bar.is-bad"))) await p.fill(".qcard .answer-line input", "1");
    else if (await p.$(".qcard .chip") && !(await p.$(".answer-bar.is-good, .answer-bar.is-bad"))) { while (await p.$(".qcard .order-pool .chip, .qcard .match-right .chip:not(.used)")) await p.click(".qcard .order-pool .chip, .qcard .match-right .chip:not(.used)"); }
    const b = await p.$(".answer-bar .inner > .btn:not([disabled])");
    if (b) await b.click();
  }
}
// a worked example half revealed
await walkTo("#/lesson/P.1.1/numbers", async () => !!(await p.$(".lcard h2:has-text('例题')")));
await p.click(".answer-bar .btn.primary");
await p.click(".answer-bar .btn.primary");
await shot("lesson-worked-example");
// a glossary look-up opened inside a question
await walkTo("#/lesson/P.1.1/for-loops", async () => !!(await p.$(".qcard .prompt .term")));
await p.click(".qcard .prompt .term");
await shot("lesson-term");
await browser.close();
console.log("screenshots in " + path.relative(ROOT, out));
