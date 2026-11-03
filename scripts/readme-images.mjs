// Screenshots for README.md → docs/images/*.webp, taken from a built game (default output/web; the
// publish script passes its build without the mentor characters, which is what the public repository
// shows). Desktop 1280×800 and phone 390×844 at 2× pixel density, light theme, a player with some
// progress on 我的远征. PNG from Edge, WebP by ffmpeg (on PATH).
// usage: node scripts/readme-images.mjs [web-dir]          (self-written glue)
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { pathToFileURL } from "node:url";
import { ROOT, launchEdge } from "./lib/edge.mjs";

const web = path.resolve(process.argv[2] || path.join(ROOT, "output/web"));
const url = pathToFileURL(path.join(web, "index.html")).href;
const out = path.join(ROOT, "docs/images");
const tmp = path.join(ROOT, "temp/readme-images");
fs.mkdirSync(out, { recursive: true });
fs.mkdirSync(tmp, { recursive: true });
const packs = JSON.parse(fs.readFileSync(path.join(ROOT, "src/gen/content.json"), "utf8"));

// First two stops lit, the third one under way, a few review cards due; `extra` lessons also done.
function progress(extra = []) {
  const at = new Date(Date.now() - 3 * 864e5).toISOString();
  const p = { v: 3, createdAt: at, xp: 640, days: {}, achievements: { "first-lesson": at, "first-light": at, perfect: at }, skills: {}, lessons: {}, cards: {}, settings: { introSeen: true, route: "goal:C.2.1", sound: false, sourceLang: "zh" } };
  for (let d = 0; d < 5; d++) p.days[new Date(Date.now() - d * 864e5).toISOString().slice(0, 10)] = 60;
  for (const id of ["P.1.1", "P.2.2"]) {
    p.skills[id] = { lit: at, boss: { at, graded: true, auto: 1 } };
    for (const l of packs[id].lessons) p.lessons[`${id}/${l.id}`] = { done: at, stars: 3, best: 1, attempts: 1 };
  }
  for (const l of packs["F.1.1"].lessons.slice(0, 7)) p.lessons[`F.1.1/${l.id}`] = { done: at, stars: 2, best: 0.8, attempts: 1 };
  for (const k of extra) p.lessons[k] = { done: at, stars: 3, best: 1, attempts: 1 };
  return p;
}

const browser = await launchEdge();
async function shoot(name, viewport, hash, prep, prog = progress()) {
  const ctx = await browser.newContext({ viewport, deviceScaleFactor: 2, colorScheme: "light", isMobile: viewport.width < 500, hasTouch: viewport.width < 500 });
  await ctx.addInitScript((p) => { if (!localStorage.getItem("cs-math-skill-game/progress")) localStorage.setItem("cs-math-skill-game/progress", JSON.stringify(p)); }, prog);
  const p = await ctx.newPage();
  await p.goto(url + hash);
  await p.waitForTimeout(900);
  if (prep) await prep(p);
  const png = path.join(tmp, name + ".png");
  await p.screenshot({ path: png });
  execFileSync("ffmpeg", ["-hide_banner", "-loglevel", "error", "-y", "-i", png, "-c:v", "libwebp", "-quality", "86", path.join(out, name + ".webp")]);
  await ctx.close();
  console.log("docs/images/" + name + ".webp");
}
const DESK = { width: 1280, height: 800 }, PHONE = { width: 390, height: 844 };
const answer = async (p) => { await p.click(".lcard .option"); await p.click(".answer-bar .inner > .btn"); await p.waitForTimeout(500); };

await shoot("banner", { width: 1280, height: 600 }, "#/intro");
await shoot("camp", DESK, "#/");
await shoot("route", DESK, "#/route/goal:C.2.1", (p) => p.evaluate(() => document.querySelector(".lv.current, .trail li.current")?.scrollIntoView({ block: "center" })));
await shoot("lesson", DESK, "#/lesson/P.1.1/first-program", answer);
// the 实验室 lists only experiments met: this player has also finished the lesson with 你来当调度器
await shoot("sim", DESK, "#/lab", (p) => p.evaluate(() => [...document.querySelectorAll(".lab-item")].find((a) => a.querySelector("h3")?.textContent === "你来当调度器")?.scrollIntoView({ block: "start" })), progress(["C.2.1/race"]));
await shoot("skill", DESK, "#/skill/C.2.1");
await shoot("map", DESK, "#/map");
await shoot("phone-camp", PHONE, "#/");
await shoot("phone-lesson", PHONE, "#/lesson/C.2.1/replacement");
await shoot("phone-route", PHONE, "#/route/goal:C.2.1", (p) => p.evaluate(() => document.querySelector(".trail li.current")?.scrollIntoView({ block: "center" })));
await browser.close();
