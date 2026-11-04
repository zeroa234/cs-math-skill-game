// Screenshots every screen of the lessons named, at a real display setting, for checking new content
// by eye (formulas, tables, sims, long options) before it ships.
// usage: node tests/look-lesson.mjs M.1.1/limit-intuition [M.1.1/squeeze …] [--phone] [--dark] [--out=dir]
// (needs npm run build; uses the system Edge). Desktop: 1440 × 900 CSS px at 200 %; phone: 390 × 844 at 300 %.
// Writes temp/look-lesson/<skill>-<lesson>/<nn>-<step>.png.
import fs from "node:fs";
import path from "node:path";
import { ROOT, GAME_URL as url, launchEdge } from "../scripts/lib/edge.mjs";
import { playLesson } from "./lib/play.mjs";

const args = process.argv.slice(2);
const dark = args.includes("--dark"), phone = args.includes("--phone");
const outArg = args.find((a) => a.startsWith("--out="));
const out = path.resolve(outArg ? outArg.slice(6) : path.join(ROOT, "temp/look-lesson"));
const targets = args.filter((a) => !a.startsWith("--"));
if (!targets.length) { console.error("usage: node tests/look-lesson.mjs <skill>/<lesson> … [--phone] [--dark]"); process.exit(2); }
const content = JSON.parse(fs.readFileSync(path.join(ROOT, "src/gen/content.json"), "utf8"));

const browser = await launchEdge();
const ctx = await browser.newContext({ viewport: phone ? { width: 390, height: 844 } : { width: 1440, height: 900 }, deviceScaleFactor: phone ? 3 : 2, colorScheme: dark ? "dark" : "light" });
const p = await ctx.newPage();
await p.goto(url);
await p.evaluate(() => localStorage.setItem("cs-math-skill-game/progress", JSON.stringify({ v: 3, settings: { introSeen: true, sound: false, music: false, sourceLang: "zh" }, skills: {}, lessons: {}, cards: {}, days: {}, achievements: {}, xp: 0 })));
const errors = [];
for (const t of targets) {
  const [skill, id] = t.split("/");
  const lesson = content[skill]?.lessons.find((l) => l.id === id);
  if (!lesson) { errors.push(`${t}: no such lesson`); continue; }
  const dir = path.join(out, `${dark ? "dark-" : ""}${phone ? "phone-" : ""}${skill}-${id}`);
  fs.rmSync(dir, { recursive: true, force: true });
  fs.mkdirSync(dir, { recursive: true });
  await p.goto(url + `#/lesson/${skill}/${id}`);
  await p.reload();
  await p.waitForSelector(".player");
  let k = 0;
  const onStep = async (label) => { await p.waitForTimeout(250); await p.screenshot({ path: path.join(dir, `${String(++k).padStart(2, "0")}-${label.replace(/[^\w-]+/g, "_")}.png`) }); };
  if (!(await playLesson(p, t, { ...lesson, flow: lesson.flow }, { errors, onStep }))) errors.push(`${t}: did not finish`);
  console.log(`${t}: ${k} screens in ${path.relative(ROOT, dir)}`);
}
await browser.close();
if (errors.length) { console.log(errors.join("\n")); process.exit(1); }
