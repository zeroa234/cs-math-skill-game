// End-to-end check in the system Edge (headless, playwright-core; no browser download).
// usage: node tests/e2e.mjs [out-dir]     E2E_PACKS=P.1.1,P.2.2 limits step 2 to those packs;
//        FULL=1 walks every lesson (before a release, after changing lesson content), otherwise a sample
//        E2E_SESSIONS=self-study,self-study-phone runs only the import/reference-material checks
//  1. intro → pick a route → route → first lesson → celebration, skill page, map, profile, lab growing
//     by the experiment of a finished lesson (screenshots)
//  2. every lesson of every content pack answered CORRECTLY from the pack data (non-sim items):
//     any correct answer graded wrong is an error — proves each input hands the checker the right shape
//  3. phone width in dark mode
// Fails (exit 1) on console errors, page errors or a lesson that cannot be finished.
import fs from "node:fs";
import path from "node:path";
import { answerAnything, playLesson as play, lessonsToWalk } from "./lib/play.mjs";
import { ROOT, GAME_URL as url, launchEdge } from "../scripts/lib/edge.mjs";

const out = path.resolve(process.argv[2] || path.join(ROOT, "temp/shots"));
fs.mkdirSync(out, { recursive: true });
const browser = await launchEdge();
const packs = JSON.parse(fs.readFileSync(path.join(ROOT, "src/gen/content.json"), "utf8"));
// A maths skill with no content pack yet (its exercise has formulas), for the self-study and music checks.
// Picked from the tree, not named: these checks used M.1.1 and went stale when its pack was written.
const TREE_SKILLS = JSON.parse(fs.readFileSync(path.join(ROOT, "src/gen/tree.json"), "utf8")).skills;
const MATH_NO_PACK = TREE_SKILLS.find((s) => s.id.startsWith("M.") && !packs[s.id] && s.exercise).id;
// The same for a computing-foundations skill (the check used F.1.2 until its pack was written).
const FOUNDATION_NO_PACK = TREE_SKILLS.find((s) => s.id.startsWith("F.") && !packs[s.id] && s.exercise).id;
const errors = [];
// The game never asks players to grade themselves or to declare a skill known (removed 2026-11-03).
for (const banned of ["自评", "全做对了", "大多没做出来", "我已经会了", "已会（跳过）"]) {
  if (fs.readFileSync(path.join(ROOT, "output/web/app.js"), "utf8").includes(banned)) errors.push(`[static] the build still contains "${banned}"`);
}
const DESK = { width: 1366, height: 860 }, PHONE = { width: 390, height: 844 };

async function session(name, viewport, fn, scheme = "light") {
  if (process.env.E2E_SESSIONS && !process.env.E2E_SESSIONS.split(",").includes(name)) return;
  const { touch, ...size } = viewport;
  const ctx = await browser.newContext({ viewport: size, colorScheme: scheme, deviceScaleFactor: 1, isMobile: !!touch, hasTouch: !!touch });
  const p = await ctx.newPage();
  p.setDefaultTimeout(6000);
  p.on("console", (m) => { if (m.type() === "error") errors.push(`[${name}] console: ${m.text()}`); });
  p.on("pageerror", (e) => errors.push(`[${name}] pageerror: ${e.message}`));
  const shot = async (n, full = false) => { await p.waitForTimeout(250); await p.screenshot({ path: path.join(out, `${name}-${n}.png`), fullPage: full }); };
  await p.goto(url);
  await p.waitForSelector(".topbar, .player, .intro");
  try { await fn(p, shot); } catch (e) { errors.push(`[${name}] step failed: ${e.message.split("\n")[0]}`); await shot("fail"); }
  await ctx.close();
}

// Lesson walking and answering live in tests/lib/play.mjs (shared with tests/phone-fit.mjs).
const playLesson = (p, tag, lesson) => play(p, tag, lesson, { errors });

// Old reading saves import cleanly; unfinished skills remain freely browsable reference material.
for (const [name, viewport, scheme] of [["self-study", DESK, "light"], ["self-study-phone", { width: 360, height: 780 }, "dark"]]) {
  await session(name, viewport, async (p, shot) => {
    await p.click(".intro .skip");
    await p.goto(url + "#/me");
    const at = "2026-11-01T00:00:00.000Z";
    const old = { v: 2, xp: 123, days: { "2026-11-01": 123 }, achievements: { "self-study": at }, settings: { introSeen: true, reduceMotion: true, sound: false }, skills: {
      "P.1.1": { lit: at, boss: { graded: false }, selfChapters: { 1: at } },
      "C.3.5": { lit: at, boss: { graded: false }, selfChapters: { 1: at } },
      "C.1.1": { lit: at, boss: { graded: true, auto: 1 } },
    } };
    await p.setInputFiles('input[type="file"]', { name: "old-save.json", mimeType: "application/json", buffer: Buffer.from(JSON.stringify({ app: "cs-math-skill-game", progress: old })) });
    await p.waitForFunction(() => {
      const s = JSON.parse(localStorage.getItem("cs-math-skill-game/progress"));
      return s.v === 3 && s.xp === 123;
    });
    const saved = await p.evaluate(() => localStorage.getItem("cs-math-skill-game/progress"));
    const state = JSON.parse(saved);
    if (state.xp !== 123 || state.skills["C.3.5"].lit || state.skills["P.1.1"].lit || state.skills["C.3.5"].selfChapters || state.skills["C.1.1"].lit !== at) errors.push(`[${name}] old save migration changed the wrong progress`);
    await p.waitForFunction(() => document.querySelector(".stats li b")?.textContent.trim() === "1");
    for (const id of [MATH_NO_PACK, "C.3.5", FOUNDATION_NO_PACK]) {
      await p.goto(url + `#/skill/${id}`);
      await p.waitForSelector(".skill .badge.st-dev");
      if (await p.$('.chapters input, .skill-head [role="progressbar"], .reading-history')) errors.push(`[${name}] ${id} still offers reading progress`);
      await p.click(`.chapter.boss a[href="#/boss/${id}"]`);
      await p.waitForSelector(".self-study-exercise");
      if (await p.$(".player, .boss-brief, .lit-mark")) errors.push(`[${name}] ${id} opens a scored challenge`);
      await p.click(".exercise-answer summary");
      await p.waitForSelector(".exercise-answer[open]");
      if ((await p.locator(".exercise-answer .md").innerText()).trim().length < 10) errors.push(`[${name}] ${id} answer is missing`);
      const fit = await p.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth);
      if (!fit) errors.push(`[${name}] ${id} exercise is wider than the screen`);
      if (id === "C.3.5") await shot("exercise-answer", true);
    }
    if (await p.evaluate(() => localStorage.getItem("cs-math-skill-game/progress")) !== saved) errors.push(`[${name}] browsing self-study material changed progress`);
    await p.goto(url + "#/map");
    await p.waitForSelector(".mcard.st-dev");
    if ((await p.$$(".mcard.st-dev")).length !== treeSkillsWithoutContent()) errors.push(`[${name}] the map mislabels unfinished skills`);
    await p.goto(url + "#/skill/P.1.1");
    await p.waitForSelector(".skill .badge.st-open");
    await shot("interactive-skill");
  }, scheme);
}

function treeSkillsWithoutContent() {
  const tree = JSON.parse(fs.readFileSync(path.join(ROOT, "src/gen/tree.json"), "utf8"));
  return tree.skills.filter((s) => !packs[s.id]).length;
}

await session("home", DESK, async (p, shot) => {
  await shot("0-title");
  await p.locator(".intro .title-card .btn").press("Enter");
  await p.waitForSelector(".intro .dialog");
  await shot("0-dialog");
  for (let i = 0; i < 12 && !(await p.$(".page.pick")); i++) {
    const last = await p.$(".dialog .row .btn");
    if (last) await last.click(); else await p.click(".dialog");
    await p.waitForTimeout(60);
  }
  await p.waitForSelector(".page.pick");
  await shot("1-pick", true);
  // 我的远征 and the recommended routes whose every stop is written (算法, opened 2026-11-04) can be chosen;
  // the other recommended routes and 自己定目标 say 开发中.
  const dev = await p.$$eval(".route-card.dev", (cs) => cs.map((c) => !!c.querySelector("button[disabled]")));
  if (dev.length < 5 || dev.some((d) => !d)) errors.push(`[home] expected greyed-out recommended routes with disabled buttons, got ${JSON.stringify(dev)}`);
  const openRec = await p.$$eval(".routes:not(.mine) .route-card:not(.dev)", (cs) => cs.map((c) => [c.getAttribute("aria-label"), !!c.querySelector(".btn.primary")]));
  if (JSON.stringify(openRec) !== JSON.stringify([["算法", true]])) errors.push(`[home] expected the 算法 route open with a start button, got ${JSON.stringify(openRec)}`);
  if ((await p.$$(".routes.mine .route-card:not(.dev) .btn.primary")).length !== 1) errors.push("[home] 我的远征 should offer exactly one start button");
  if (await p.$(".goal-list")) errors.push("[home] the goal picker is open although 自己定目标 is in development");
  await p.click(".routes.mine .route-card .btn.primary");
  await p.waitForSelector(".trail");
  await shot("2-route");
  await p.click(".trail li.current .start-pop .btn");
  await p.waitForSelector(".player");
  await shot("3-lesson");
  if (!(await playLesson(p, "home"))) errors.push("[home] lesson did not reach the celebration");
  await shot("4-summary");
  await p.goto(url + "#/skill/P.1.1");
  await p.waitForSelector(".chapters");
  await shot("5-skill");
  await p.goto(url + "#/map");
  await p.waitForSelector(".mcard");
  await shot("6-map");
  // The wheel zooms about the pointer: the map point under the cursor stays under the cursor.
  {
    const card = p.locator('.mcard[href="#/skill/C.2.1"]');
    const b0 = await card.boundingBox();
    const px = b0.x + b0.width * 0.3, py = b0.y + b0.height * 0.5;
    await p.mouse.move(px, py);
    for (let i = 0; i < 3; i++) { await p.mouse.wheel(0, -120); await p.waitForTimeout(60); }
    await p.waitForTimeout(300);
    const b1 = await card.boundingBox();
    const k = b1.width / b0.width;
    const drift = Math.hypot(b1.x + (px - b0.x) * k - px, b1.y + (py - b0.y) * k - py);
    if (!(k > 1.05)) errors.push(`[map] wheel did not zoom in (×${k.toFixed(3)})`);
    if (drift > 3) errors.push(`[map] wheel zoom drifted ${drift.toFixed(1)} px away from the pointer`);
  }
  // A card opens with a click, also after the map was panned (moving the mouse or panning used to
  // block every click); its skill page leads back to the map, which keeps its zoom and place.
  {
    const card = p.locator('.mcard[href="#/skill/C.2.1"]');
    const w = await p.locator(".map-wrap").boundingBox();
    await p.mouse.move(w.x + 40, w.y + w.height - 40);
    await p.mouse.down();
    await p.mouse.move(w.x + 90, w.y + w.height - 70, { steps: 6 });
    await p.mouse.up();
    const before = await card.boundingBox();
    await p.mouse.click(before.x + before.width / 2, before.y + before.height / 2);
    await p.waitForTimeout(300);
    if ((await p.evaluate(() => location.hash)) !== "#/skill/C.2.1") errors.push("[map] clicking a card after panning did not open it");
    else {
      const back = p.locator(".skill .back");
      if ((await back.getAttribute("href")) !== "#/map" || !(await back.innerText()).includes("地图")) errors.push("[map] a skill opened from the map does not lead back to it");
      await back.click();
      await p.waitForSelector(".mcard");
      const after = await card.boundingBox();
      if (Math.hypot(after.x - before.x, after.y - before.y) > 2 || Math.abs(after.width - before.width) > 1) errors.push("[map] coming back did not keep the zoom and place");
    }
  }
  await p.goto(url + "#/me");
  await shot("7-me");
  // 实验室: empty at first; finishing a lesson with a new experiment adds it and says so
  await p.goto(url + "#/lab");
  await p.waitForSelector(".lab-empty");
  await p.goto(url + "#/lesson/C.1.1/twos-complement");
  await p.waitForSelector(".player");
  if (!(await playLesson(p, "home/bits", packs["C.1.1"].lessons.find((l) => l.id === "twos-complement")))) errors.push("[home] the 位与补码 lesson did not finish");
  else if (!(await p.locator(".toast", { hasText: "实验室多了一个实验：位与补码" }).count())) errors.push("[home] finishing the first lesson with 位与补码 did not say the lab grew");
  await p.goto(url + "#/lab");
  await p.waitForSelector(".lab-item");
  const lab = await p.locator(".lab-item h3").allInnerTexts();
  if (lab.join() !== "位与补码") errors.push(`[home] the lab lists ${lab.join("、")} after one lesson with 位与补码`);
  await shot("8-lab", true);
});

await session("packs", DESK, async (p, shot) => {
  const only = process.env.E2E_PACKS ? new Set(process.env.E2E_PACKS.split(",")) : null;
  const walk = lessonsToWalk(packs);
  console.log(`packs: ${Object.values(walk).flat().length} lessons${process.env.FULL === "1" ? " (FULL)" : " (every item type and component, and the widest code; FULL=1 for all)"}`);
  for (const [skill] of Object.entries(packs)) {
    if (only && !only.has(skill)) continue;
    for (const l of walk[skill]) {
      await p.goto(url + `#/lesson/${skill}/${l.id}`);
      await p.waitForSelector(".player");
      if (!(await playLesson(p, `${skill}/${l.id}`, l))) errors.push(`[packs] ${skill}/${l.id} did not finish`);
    }
    await p.goto(url + `#/skill/${skill}`);
    await p.waitForSelector(".chapters");
    await shot(skill);
  }
});

// The whole loop on one skill: every chapter → final challenge → lit → next stops open →
// cards come due (moved into the past in storage) → a review session runs to completion.
await session("flow", DESK, async (p, shot) => {
  const pack = packs["P.1.1"];
  // The first three lessons through the screens (21 review cards); FULL=1 plays all, otherwise the
  // rest are marked done in the save, which is all the final challenge asks of them.
  const played = process.env.FULL === "1" ? pack.lessons : pack.lessons.slice(0, 3);
  for (const l of played) {
    await p.goto(url + `#/lesson/P.1.1/${l.id}`);
    await p.waitForSelector(".player");
    if (!(await playLesson(p, `flow/${l.id}`, l))) errors.push(`[flow] ${l.id} did not finish`);
  }
  await p.evaluate((ids) => {
    const key = "cs-math-skill-game/progress", s = JSON.parse(localStorage.getItem(key)), at = new Date().toISOString();
    for (const id of ids) s.lessons[`P.1.1/${id}`] ||= { done: at, stars: 3, best: 1, attempts: 1 };
    localStorage.setItem(key, JSON.stringify(s));
  }, pack.lessons.map((l) => l.id));
  await p.reload();
  // Final challenge: same player as a lesson; all checks right on the first try lights the skill.
  await p.goto(url + "#/boss/P.1.1");
  await p.click(".boss-brief .btn.primary");
  await p.waitForSelector(".player");
  if (!(await playLesson(p, "flow/boss", { flow: pack.boss.items.map((item) => ({ kind: "item", item })) }))) errors.push("[flow] final challenge did not finish");
  await p.waitForSelector(".lit-mark");
  await shot("1-lit");
  await p.goto(url + "#/route/goal:C.2.1");
  await p.waitForSelector(".units");
  const open = await p.$$eval(".unit:not(.locked) h2", (hs) => hs.map((h) => h.textContent));
  if (!open.includes("C/C++与底层编程") || !open.includes("数据结构") || !open.includes("计算机组成原理")) errors.push(`[flow] after lighting P.1.1 the open stops are ${open.join(", ")}`);
  await shot("2-route-after");
  const due = await p.evaluate(() => {
    const key = "cs-math-skill-game/progress";
    const s = JSON.parse(localStorage.getItem(key));
    for (const c of Object.values(s.cards)) c.dueAt = new Date(Date.now() - 864e5).toISOString();
    localStorage.setItem(key, JSON.stringify(s));
    return Object.keys(s.cards).length;
  });
  if (due <= 12) throw new Error(`expected at least two review rounds, got ${due} cards`);
  await p.goto(url + "#/review");
  await p.reload();
  await p.waitForSelector(".player");
  await shot("3-review");
  for (let guard = 0; guard < 60 && !(await p.$("text=这一组复习完了")); guard++) {
    const btn = p.locator(".answer-bar .inner > .btn");
    if ((await btn.textContent()).trim() === "检查") await answerAnything(p);
    await btn.click();
  }
  await p.getByRole("heading", { name: "这一组复习完了" }).waitFor();
  const after = await p.evaluate(() => Object.values(JSON.parse(localStorage.getItem("cs-math-skill-game/progress")).cards).filter((c) => new Date(c.dueAt) <= new Date()).length);
  if (after > due - 12) errors.push(`[flow] review did not reschedule cards (${after} still due of ${due})`);
  await shot("4-review-done");
  await p.getByRole("button", { name: "再来一组" }).click();
  await p.locator('.player [aria-label="复习进度"][aria-valuenow="0"]').waitFor();
});

await session("save", DESK, async (p) => {
  const key = "cs-math-skill-game/progress";
  const corrupt = '{"v":';
  await p.locator(".intro .skip").press("Space");
  await p.waitForSelector(".page.pick");
  await p.evaluate(({ key, corrupt }) => localStorage.setItem(key, corrupt), { key, corrupt });
  await p.reload();
  await p.waitForSelector(".save-problem");
  await p.getByRole("button", { name: "从头开始…" }).click();
  await p.getByRole("button", { name: "取消" }).click();
  if (await p.evaluate((k) => localStorage.getItem(k), key) !== corrupt) throw new Error("corrupt save was overwritten");
  await p.getByRole("button", { name: "从头开始…" }).click();
  await p.getByRole("button", { name: "清掉，从头开始" }).click();
  await p.waitForSelector(".topbar");

  const peer = await p.context().newPage();
  await peer.goto(url + "#/pick");
  await peer.locator('.topbar button[aria-pressed="true"]').click();
  await p.locator('.topbar button[aria-pressed="false"]').waitFor();
  await peer.close();

  await p.evaluate(() => {
    const original = Storage.prototype.setItem;
    Storage.prototype.setItem = () => { throw new DOMException("Test quota", "QuotaExceededError"); };
    window.restoreSaveWrites = () => { Storage.prototype.setItem = original; };
  });
  await p.locator('.topbar button[aria-pressed="false"]').click();
  await p.waitForSelector(".save-warning");
  await p.evaluate(() => window.restoreSaveWrites());
  await p.locator('.topbar button[aria-pressed="true"]').click();
  await p.locator(".save-warning").waitFor({ state: "hidden" });
});

await session("phone", PHONE, async (p, shot) => {
  await shot("0-title");
  await p.click(".intro .skip");
  await p.waitForSelector(".page.pick");
  await shot("1-pick");
  await p.goto(url + "#/");
  await p.waitForSelector(".page.home");
  await shot("1-home");
  await p.goto(url + "#/route/web");
  await p.waitForSelector(".dev-stops");
  if (await p.$(".trail")) errors.push("[phone] a route in development shows a playable trail");
  if (await p.evaluate(() => JSON.parse(localStorage.getItem("cs-math-skill-game/progress")).settings.route === "web")) errors.push("[phone] opening a route in development made it the active route");
  await shot("2-route-dev");
  await p.goto(url + "#/skill/C.2.1");
  await shot("3-skill");
  await p.goto(url + "#/lesson/P.1.1/naming");
  await p.waitForSelector(".player");
  for (let i = 0; i < 3; i++) { const b = await p.$(".answer-bar .inner > .btn"); if (b && !(await b.isDisabled())) await b.click(); else await answerAnything(p); }
  await shot("4-lesson");
}, "dark");

// Background music: silent until the first tap, then each scene plays one of its own tracks; the
// style and volume settings apply and the sound switch stops it. Audio elements are watched by
// wrapping HTMLMediaElement.play (they are not in the DOM).
await session("music", DESK, async (p) => {
  const music = JSON.parse(fs.readFileSync(path.join(ROOT, "src/gen/music.json"), "utf8"));
  await p.addInitScript(() => {
    window.__audio = new Set();
    const play = HTMLMediaElement.prototype.play;
    HTMLMediaElement.prototype.play = function () { window.__audio.add(this); return play.call(this); };
  });
  await p.reload();
  const audible = () => p.evaluate(() => [...window.__audio].filter((a) => !a.paused && a.volume > 0.02).map((a) => ({ id: a.src.match(/music\/([\w-]+)\.ogg$/)?.[1], volume: +a.volume.toFixed(2) })));
  const go = async (hash) => { await p.evaluate((h) => { location.hash = h; }, hash); await p.waitForTimeout(1300); };
  const expect = async (tag, scene, style = music.styles[0].id) => {
    const ids = music.styles.find((s) => s.id === style).scenes[scene];
    const now = await audible();
    if (now.length !== 1 || !ids.includes(now[0].id)) errors.push(`[music] ${tag}: playing ${JSON.stringify(now)}, expected one of ${style}/${scene}: ${ids.join(", ")}`);
    return now[0];
  };
  await p.waitForTimeout(1300);
  if ((await audible()).length) errors.push("[music] music started before the first tap");
  await p.click(".intro .title-card .btn");
  await p.waitForTimeout(1300);
  await expect("intro", "title");
  await p.click(".intro .skip");
  await p.click(".page.pick .btn.primary");
  await go("#/");
  await expect("camp", "explore");
  await go("#/lesson/P.1.1/first-program");
  await expect("lesson", "focus");
  await go("#/boss/C.2.1");
  await expect("final challenge", "challenge");
  await go(`#/boss/${MATH_NO_PACK}`);
  await expect("exercise of a skill without lessons", "explore");
  await go("#/me");
  await p.selectOption(".music-settings select", "chip");
  await p.waitForTimeout(1300);
  await expect("style 8-bit", "explore", "chip");
  await p.$eval(".music-settings input[type=range]", (el) => { el.value = "20"; el.dispatchEvent(new Event("input", { bubbles: true })); });
  await p.waitForTimeout(200);
  const quiet = await expect("volume 20", "explore", "chip");
  if (quiet && Math.abs(quiet.volume - 0.2) > 0.01) errors.push(`[music] volume 20 % plays at ${quiet.volume}`);
  await p.click(".topbar .icon-btn");
  await p.waitForTimeout(1300);
  if ((await audible()).length) errors.push("[music] the sound switch did not stop the music");
});

// 我的 → 检查更新, against a stand-in for the GitHub releases API (the real one is never called).
await session("update", DESK, async (p) => {
  let reply = { status: 200, body: { tag_name: "v99.0.0", body: "测试用的更新说明", html_url: "https://github.com/zeroa234/cs-math-skill-game/releases/tag/v99.0.0", assets: [] } };
  await p.route("https://api.github.com/**", (r) => (reply ? r.fulfill({ status: reply.status, contentType: "application/json", headers: { "access-control-allow-origin": "*" }, body: JSON.stringify(reply.body) }) : r.abort()));
  await p.goto(url + "#/me");
  const check = async () => {
    await p.click(".update-check button");
    await p.locator('.update-check button[aria-disabled="true"]').waitFor({ state: "hidden" });
    return (await p.innerText(".update-check")).replace(/\s+/g, " ");
  };
  let text = await check();
  if (!text.includes("有新版本 99.0.0") || !text.includes("测试用的更新说明") || !(await p.$(".update-check a.btn.primary[href*='releases/tag/v99.0.0']"))) errors.push(`[update] a newer release is not offered: ${text}`);
  reply = { status: 200, body: { ...reply.body, tag_name: "v0.0.1" } };
  if (!(text = await check()).includes("已经是最新版本")) errors.push(`[update] an older release is offered: ${text}`);
  reply = null;
  if (!(text = await check()).includes("连不上 GitHub")) errors.push(`[update] no network gives no message: ${text}`);
  // the stand-in refused that request on purpose, and the browser logs a refused request as an error
  for (let i = errors.length - 1; i >= 0; i--) if (errors[i] === "[update] console: Failed to load resource: net::ERR_FAILED") errors.splice(i, 1);
});

// On a touch screen a card still opens with a tap after the map was dragged with a finger.
// Zooming in and out and back leaves the map where it was. Panzoom reads the canvas size for each
// zoom but applies the transform a frame later: several wheel events in one frame (a fast wheel, a
// touchpad) used to push the map ~1000 px to the top left in six rounds (fixed 2026-11-04).
await session("map-zoom", DESK, async (p) => {
  await p.goto(url + "#/map");
  await p.waitForSelector(".mcard");
  await p.waitForTimeout(500);
  const at = async () => { const b = await p.locator(".mcard").nth(40).boundingBox(); return { x: b.x, y: b.y, w: b.width }; };
  const a = await at();
  for (let c = 0; c < 6; c++) for (const dy of [-100, 100]) {
    await p.evaluate((dy) => { const t = document.elementFromPoint(500, 400); for (let i = 0; i < 4; i++) t.dispatchEvent(new WheelEvent("wheel", { deltaY: dy, clientX: 500, clientY: 400, bubbles: true, cancelable: true })); }, dy);
    await p.waitForTimeout(50);
  }
  await p.waitForTimeout(300);
  const b = await at();
  if (Math.hypot(b.x - a.x, b.y - a.y) > 1 || Math.abs(b.w - a.w) > 0.5) errors.push(`[map-zoom] wheel in and out (4 events a frame) moved the map by ${Math.round(b.x - a.x)}, ${Math.round(b.y - a.y)} px`);
  // ＋/－ zoom about the middle of the map, also on the presses that hit the smallest or largest zoom
  const w = await p.locator(".map-wrap").boundingBox();
  const mid = { x: w.x + w.width / 2, y: w.y + w.height / 2 };
  let worst = 0;
  for (const [label, n] of [["缩小", 12], ["放大", 16]]) for (let i = 0; i < n; i++) {
    const s = await at();
    await p.click(`button[aria-label="${label}"]`);
    await p.waitForTimeout(60);
    const e = await at(), k = e.w / s.w;
    worst = Math.max(worst, Math.hypot(mid.x + (s.x - mid.x) * k - e.x, mid.y + (s.y - mid.y) * k - e.y));
  }
  if (worst > 1) errors.push(`[map-zoom] ＋/－ moved the middle of the map by up to ${worst.toFixed(1)} px`);
});

await session("map-touch", { ...PHONE, touch: true }, async (p) => {
  await p.goto(url + "#/map");
  await p.waitForSelector(".mcard");
  const w = await p.locator(".map-wrap").boundingBox();
  const cdp = await p.context().newCDPSession(p);
  const touch = (type, pts) => cdp.send("Input.dispatchTouchEvent", { type, touchPoints: pts.map(([x, y], id) => ({ x, y, id })) });
  // Pinching out and in leaves the map about where it was (four rounds moved it ~520 px to the top
  // left before 2026-11-04; what is left is the fingers' midpoint wobbling as each finger's event comes)
  const card = () => p.locator(".mcard").nth(40).boundingBox();
  const c0 = await card(), mx = w.x + w.width / 2, my = w.y + w.height / 2;
  for (let c = 0; c < 4; c++) for (const [from, to] of [[40, 120], [120, 40]]) {
    await touch("touchStart", [[mx - from, my], [mx + from, my]]);
    for (let k = 1; k <= 8; k++) { const d = from + ((to - from) * k) / 8; await touch("touchMove", [[mx - d, my], [mx + d, my]]); }
    await touch("touchEnd", []);
    await p.waitForTimeout(100);
  }
  await p.waitForTimeout(300);
  const c1 = await card();
  if (Math.abs(c1.width - c0.width) > 0.5 || Math.hypot(c1.x - c0.x, c1.y - c0.y) > 25) errors.push(`[map-touch] pinching out and in moved the map by ${Math.round(c1.x - c0.x)}, ${Math.round(c1.y - c0.y)} px`);
  // drag the map, then tap a card: the first tap selects it (its prerequisite chain lights up, as a
  // mouse hover does), a tap on the background lets go, and a second tap on the selected card opens it
  const at = (i) => [[w.x + 60 + i * 10, w.y + 220 + i * 10]];
  await touch("touchStart", at(0));
  for (let i = 1; i <= 6; i++) await touch("touchMove", at(i));
  await touch("touchEnd", []);
  // A tap within ~0.2 s of lifting the finger is swallowed by the browser itself (no click event,
  // measured 2026-11-03, also with zoom off), so tap after a human pause.
  await p.waitForTimeout(1000);
  const target = p.locator(".mcard").first();
  const tap = async () => { const b = await target.boundingBox(); await p.touchscreen.tap(b.x + b.width / 2, b.y + b.height / 2); await p.waitForTimeout(400); };
  await tap();
  if ((await p.evaluate(() => location.hash)).startsWith("#/skill/")) errors.push("[map-touch] the first tap on a card opened it instead of selecting it");
  else if (!(await target.evaluate((el) => el.classList.contains("selected") && el.textContent.includes("再点一下打开")))) errors.push("[map-touch] the first tap on a card did not select it");
  const free = await p.evaluate(() => { const r = document.querySelector(".map-wrap").getBoundingClientRect(); for (let y = r.top + 10; y < r.bottom; y += 15) for (let x = r.left + 10; x < r.right; x += 15) { const el = document.elementFromPoint(x, y); if (el && !el.closest(".mcard") && el.closest(".map-wrap")) return { x, y }; } return null; });
  await p.touchscreen.tap(free.x, free.y);
  await p.waitForTimeout(400);
  if (await p.$(".mcard.selected")) errors.push("[map-touch] tapping the background did not let go of the selected card");
  await tap();
  await tap();
  if (!(await p.evaluate(() => location.hash)).startsWith("#/skill/")) errors.push("[map-touch] a second tap on the selected card did not open it");
});

await browser.close();
if (errors.length) { console.log("ERRORS:\n" + [...new Set(errors)].join("\n")); process.exit(1); }
console.log(`ok — screenshots in ${path.relative(ROOT, out)}`);
