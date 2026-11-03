// Phone-width layout check in the system Edge with mobile emulation (touch, mobile viewport rules).
// Nothing may stick out sideways: on a phone, a page wider than the screen can be dragged and
// zoomed out (seen 2026-11-03 on the lesson celebration and a skill page). Walks the intro, every
// main screen, the sampled lessons (FULL=1: every lesson) step by step (before and after each answer and
// its celebration), a final challenge to its result, a review session and the lab, and fails if the
// page is wider than the screen anywhere. Also checks both intro portraits stay on the screen.
// usage: node tests/phone-fit.mjs [width=360]   (360 = the narrowest common Android width)
//        FIT_PACKS=P.1.1,C.2.1 limits the lesson walk to those packs; FULL=1 walks every lesson,
//        otherwise the sample from tests/lib/play.mjs (every item type and component, the widest code)
import fs from "node:fs";
import path from "node:path";
import { answerAnything, playLesson, lessonsToWalk, finishAllLessons } from "./lib/play.mjs";
import { ROOT, GAME_URL as url, launchEdge } from "../scripts/lib/edge.mjs";

const W = Number(process.argv[2] || 360);
const out = path.join(ROOT, "temp/phone-fit");
fs.mkdirSync(out, { recursive: true });
const packs = JSON.parse(fs.readFileSync(path.join(ROOT, "src/gen/content.json"), "utf8"));
const browser = await launchEdge();
const ctx = await browser.newContext({ viewport: { width: W, height: 780 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
const p = await ctx.newPage();
p.setDefaultTimeout(6000);
const errors = [];
p.on("pageerror", (e) => errors.push(`pageerror: ${e.message}`));
let checks = 0;

// The page is wider than the screen? Name the outermost elements that stick out and are not
// inside something that clips or scrolls sideways.
async function fit(tag) {
  checks++;
  const r = await p.evaluate(() => {
    const W = document.documentElement.clientWidth, sw = document.documentElement.scrollWidth;
    if (sw <= W) return null;
    const name = (el) => el.tagName.toLowerCase() + (typeof el.className === "string" && el.className.trim() ? "." + el.className.trim().split(/\s+/).join(".") : "");
    const bad = [];
    for (const el of document.querySelectorAll("body *")) {
      const b = el.getBoundingClientRect();
      if (!b.width || (b.right <= W + 0.5 && b.left >= -0.5) || bad.some((x) => x.el.contains(el))) continue;
      let a = el.parentElement, clipped = false;
      while (a && a !== document.body) { if (getComputedStyle(a).overflowX !== "visible") { const ab = a.getBoundingClientRect(); if (ab.right <= W + 0.5 && ab.left >= -0.5) { clipped = true; break; } } a = a.parentElement; }
      if (!clipped) bad.push({ el, s: `${name(el)} [${Math.round(b.left)}..${Math.round(b.right)}]` });
    }
    return { W, sw, bad: bad.slice(0, 4).map((x) => x.s) };
  });
  if (!r) return;
  const msg = `${tag}: page ${r.sw}px wide on a ${r.W}px screen — ${r.bad.join(", ")}`;
  if (!errors.includes(msg)) { errors.push(msg); await p.screenshot({ path: path.join(out, `fail-${errors.length}.png`) }); }
}
const go = async (h, wait = 400) => { await p.goto(url + h); await p.waitForTimeout(wait); };

// Intro: title card, then each dialogue line; both portraits must be fully on the screen.
await go("", 700);
await fit("intro title");
await p.click(".intro .title-card .btn");
for (let i = 0; i < 12 && !(await p.$(".page.pick")); i++) {
  await p.waitForTimeout(150);
  await fit(`intro line ${i + 1}`);
  const off = await p.$$eval(".intro .who", (els) => els.map((e) => { const b = e.getBoundingClientRect(); return { alt: e.alt, l: Math.round(b.left), r: Math.round(b.right) }; }).filter((b) => b.l < -1 || b.r > innerWidth + 1));
  for (const o of off) errors.push(`intro line ${i + 1}: portrait ${o.alt} at ${o.l}..${o.r} is partly off the ${W}px screen`);
  const last = await p.$(".dialog .row .btn");
  if (last) await last.click(); else await p.click(".dialog");
}

for (const h of ["#/pick", "#/", "#/route/goal:C.2.1", "#/route/web", "#/route/ai", "#/map", "#/review", "#/me", "#/lab"]) { await go(h); await fit(h); }
for (const id of [...Object.keys(packs), "M.1.1", "C.3.5", "F.1.2"]) { await go(`#/skill/${id}`); await fit(`#/skill/${id}`); }

// Every lesson, every step, and its celebration.
const only = process.env.FIT_PACKS ? new Set(process.env.FIT_PACKS.split(",")) : null;
const walk = lessonsToWalk(packs);
for (const [skill] of Object.entries(packs)) {
  if (only && !only.has(skill)) continue;
  for (const l of walk[skill]) {
    await go(`#/lesson/${skill}/${l.id}`, 200);
    const tag = `${skill}/${l.id}`;
    try {
      const ok = await playLesson(p, tag, l, { errors, onStep: (s) => fit(`${tag} ${s}`) });
      if (!ok) errors.push(`${tag}: did not finish`);
      await p.waitForTimeout(300);
      await fit(`${tag} celebration`);
    } catch (e) {
      errors.push(`${tag}: ${e.message.split("\n")[0]} — ${(e.message.match(/<[^>]+>[^\n]*intercepts pointer events/) || [""])[0]}`);
      await p.screenshot({ path: path.join(out, `fail-${errors.length}.png`) });
    }
  }
  await go(`#/boss/${skill}`);
  await fit(`#/boss/${skill}`);
}

// A final challenge to its result (the lessons above opened it), then review with cards due.
// (the sample may skip P.1.1's lessons; the challenge opens once they are all done)
await p.evaluate((ids) => {
  const key = "cs-math-skill-game/progress", s = JSON.parse(localStorage.getItem(key)), at = new Date().toISOString();
  for (const id of ids) s.lessons[`P.1.1/${id}`] ||= { done: at, stars: 3, best: 1, attempts: 1 };
  localStorage.setItem(key, JSON.stringify(s));
}, packs["P.1.1"].lessons.map((l) => l.id));
await p.reload();
await go("#/boss/P.1.1");
await p.click(".boss-brief .btn.primary");
await playLesson(p, "boss P.1.1", { flow: packs["P.1.1"].boss.items.map((item) => ({ kind: "item", item })) }, { errors, onStep: (s) => fit(`boss P.1.1 ${s}`), done: ".lit-mark, .celebrate" });
await p.waitForTimeout(500);
await fit("boss P.1.1 result");
await p.evaluate(() => {
  const key = "cs-math-skill-game/progress";
  const s = JSON.parse(localStorage.getItem(key));
  for (const c of Object.values(s.cards)) c.dueAt = new Date(Date.now() - 864e5).toISOString();
  localStorage.setItem(key, JSON.stringify(s));
});
await go("#/review");
await p.reload();
await p.waitForSelector(".player");
for (let guard = 0; guard < 60 && !(await p.$("text=复习完成")); guard++) {
  const btn = await p.$(".answer-bar .inner > .btn");
  if (!btn) { await p.waitForTimeout(100); continue; }
  if ((await btn.textContent()).trim() === "检查" && (await btn.isDisabled())) await answerAnything(p);
  await fit(`review step ${guard}`);
  await btn.click();
}
await fit("review done");
for (const h of ["#/", "#/route/goal:C.2.1", "#/me", "#/map"]) { await go(h); await fit(`${h} (with progress)`); }
// The 实验室 with every experiment met, and each program its Python stepper offers.
await finishAllLessons(p, packs);
await go("#/lab");
await fit("#/lab (every experiment)");
const programs = await p.$$eval(".lab-item select option", (o) => o.length);
for (let i = 1; i < programs; i++) { await p.selectOption(".lab-item select", String(i)); await fit(`#/lab program ${i + 1}`); }

await browser.close();
if (errors.length) { console.log(`ERRORS (${errors.length}, screenshots in temp/phone-fit/):\n` + errors.join("\n")); process.exit(1); }
console.log(`ok — ${checks} screens at ${W}px fit the screen`);
