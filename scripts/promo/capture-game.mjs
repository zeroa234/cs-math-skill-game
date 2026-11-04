// 宣传片用的游戏截图：系统 Edge 无头、深色主题、“减少动画”打开（角色不动、不放彩带、开场文字直接显示，每张图可复现）。
// 电脑 1216×684 视口、3 倍像素（成片窗口 1824 px 宽，正好缩一半，推近到 2 倍也不糊）；很高的页面用 2 倍像素。
// 每张图同时记下要指的元素在视口里的位置（CSS px）和页面里导师精灵的位置，写进 shots.json：
// 截图里把精灵藏起来，视频里在同一位置播放 assets/cast/sprites/ 的动画条，导师照样会动（src/promo/src/lib/sprite.tsx）。
// 开场对白的文字也藏起来、记下文字和框，视频里逐字打出来（和游戏的打字机一样）。
// 用法：node scripts/promo/capture-game.mjs [输出目录，默认 src/promo/public/shots]     需要先 npm run build
import fs from "node:fs";
import path from "node:path";
import { ROOT, GAME_URL, launchEdge } from "../lib/edge.mjs";
import { answerCorrectly, answerAnything } from "../../tests/lib/play.mjs";

const out = path.resolve(process.argv[2] || path.join(ROOT, "src/promo/public/shots"));
fs.mkdirSync(out, { recursive: true });
const packs = JSON.parse(fs.readFileSync(path.join(ROOT, "src/gen/content.json"), "utf8"));
const lessonOf = (skill, id) => packs[skill].lessons.find((l) => l.id === id);
const VIEW = { width: 1216, height: 684 }, PHONE = { width: 390, height: 844 };
const KEY = "cs-math-skill-game/progress";
const meta = {};
const errors = [];

// 存档：前两站已点亮、第三站学了 7 课（和 README 截图同一个玩家）；extra 里的课也算学过
function progress({ lit = ["P.1.1", "P.2.2"], extra = [], cards = {} } = {}) {
  const at = new Date(Date.now() - 3 * 864e5).toISOString();
  const p = { v: 3, createdAt: at, xp: 640, days: {}, achievements: { "first-lesson": at, "first-light": at }, skills: {}, lessons: {}, cards,
    settings: { introSeen: true, route: "goal:C.2.1", sound: false, sourceLang: "zh", reduceMotion: true } };
  for (let d = 0; d < 5; d++) p.days[new Date(Date.now() - d * 864e5).toISOString().slice(0, 10)] = 60;
  for (const id of lit) {
    p.skills[id] = { lit: at, boss: { at, graded: true, auto: 1 } };
    for (const l of packs[id].lessons) p.lessons[`${id}/${l.id}`] = { done: at, stars: 3, best: 1, attempts: 1 };
  }
  for (const l of packs["F.1.1"].lessons.slice(0, 7)) p.lessons[`F.1.1/${l.id}`] ||= { done: at, stars: 2, best: 0.8, attempts: 1 };
  for (const k of extra) p.lessons[k] ||= { done: at, stars: 3, best: 1, attempts: 1 };
  return p;
}

const browser = await launchEdge(path.join(ROOT, "temp/browser"));
async function open(hash, { view = VIEW, dpr = 3, prog = progress() } = {}) {
  const phone = view.width < 500;
  const ctx = await browser.newContext({ viewport: view, deviceScaleFactor: dpr, colorScheme: "dark", isMobile: phone, hasTouch: phone });
  await ctx.addInitScript(([k, s]) => { if (!localStorage.getItem(k)) localStorage.setItem(k, JSON.stringify(s)); }, [KEY, prog]);
  const p = await ctx.newPage();
  p.setDefaultTimeout(8000);
  p.on("pageerror", (e) => errors.push(`${hash}: ${e.message}`));
  p.on("console", (m) => { if (m.type() === "error") errors.push(`${hash}: ${m.text()}`); });
  await p.goto(GAME_URL + hash);
  await p.waitForTimeout(1000);
  return { ctx, p, dpr };
}
const rect = (r) => ({ x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) });
async function box(p, sel) {
  const loc = typeof sel === "string" ? p.locator(sel) : sel;
  const b = await loc.first().boundingBox();
  if (!b) throw new Error(`没找到 ${sel}`);
  return rect(b);
}
const allBoxes = (p, sel) => p.evaluate((sel) => [...document.querySelectorAll(sel)].map((e) => e.getBoundingClientRect())
  .filter((r) => r.width > 0 && r.height > 0).map((r) => ({ x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) })), sel);

// 页面里看得见的精灵：谁、哪个动作、整个“舞台”的框、放大倍数、是否镜像；然后藏起来
const takeSprites = (p) => p.evaluate(() => [...document.querySelectorAll(".sprite")].map((s) => {
  const fr = s.querySelector(".sprite-frame");
  const m = /sprites\/(\w+)\/(\w+)\.webp/.exec(fr.style.backgroundImage);
  const r = s.getBoundingClientRect();
  s.style.visibility = "hidden";
  // 放大倍数由舞台宽度 / sprites.json 算出的舞台原始宽度得到（视频里算，见 sprite.tsx）
  return m && r.width > 0 ? { who: m[1], action: m[2], x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height), flip: /scaleX\(-1\)/.test(fr.style.transform) } : null;
}).filter(Boolean));

async function shot(ctxp, name, targets = {}, opts = {}) {
  const { p, dpr } = ctxp;
  await p.waitForTimeout(opts.wait ?? 500);
  if (opts.prep) await opts.prep(p);
  const t = {};
  // 选择器以 all: 开头的取所有匹配元素的框（数组），否则取第一个；也可以直接给 locator
  for (const [k, sel] of Object.entries(targets)) t[k] = typeof sel === "string" && sel.startsWith("all:") ? await allBoxes(p, sel.slice(4)) : await box(p, sel);
  const sprites = await takeSprites(p);
  const file = `${name}.png`;
  await p.screenshot({ path: path.join(out, file), fullPage: !!opts.full });
  const vp = p.viewportSize();
  const h = opts.full ? await p.evaluate(() => document.documentElement.scrollHeight) : vp.height;
  meta[name] = { file, w: vp.width, h, dpr, targets: t, sprites, ...(opts.extra || {}) };
  await p.evaluate(() => document.querySelectorAll(".sprite").forEach((s) => (s.style.visibility = "")));
  console.log(name, Object.keys(t).join(" "), sprites.map((s) => s.who + "/" + s.action).join(" "));
}
const bottomBtn = (p) => p.locator(".answer-bar .inner > .btn");
async function press(p) { await bottomBtn(p).click(); await p.waitForTimeout(350); }
// 课程往前走到 flow 里 id 为 target 的那道题（之前的题都按正确答案答）
async function advanceTo(p, lesson, target) {
  const byId = Object.fromEntries(lesson.flow.filter((s) => s.item).map((s) => [s.item.id, s.item]));
  for (let guard = 0; guard < 60; guard++) {
    const id = await p.$eval(".lcard", (el) => el.dataset.item || "").catch(() => "");
    if (id === target) return;
    const label = (await bottomBtn(p).textContent()).trim();
    if (label === "检查") {
      const item = byId[id];
      if (!item || !(await answerCorrectly(p, item))) await answerAnything(p);
      await press(p);
    }
    await press(p);
  }
  throw new Error(`没走到 ${target}`);
}

// 1. 开场：标题卡 → 第 1 句（妹妹：星图学院）、第 3 句（妹妹：一次一小课）对白（文字藏起来，视频里逐字打出）
{
  const c = await open("#/intro");
  await shot(c, "intro-title", { title: ".title-card h1", start: ".title-card .btn" });
  await c.p.click(".title-card .btn");
  let at = 0;
  for (const [k, name] of [[0, "intro-l0"], [2, "intro-l2"]]) {
    for (; at < k; at++) { await c.p.click(".dialog"); await c.p.waitForTimeout(250); }
    await c.p.waitForTimeout(400);
    const line = await c.p.evaluate(() => {
      const el = document.querySelector(".dialog .line"), cs = getComputedStyle(el), r = el.getBoundingClientRect();
      const text = el.textContent;
      el.style.visibility = "hidden";
      return { text, x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height), size: parseFloat(cs.fontSize), lh: parseFloat(cs.lineHeight), color: cs.color };
    });
    await shot(c, name, { dialog: ".dialog", name: ".dialog .name" }, { extra: { line } });
  }
  await c.ctx.close();
}
// 2. 选远征 → 远征路线（整页很高，2 倍像素；视频里镜头往下扫）
{
  const c = await open("#/pick");
  await shot(c, "pick", { mine: ".route-card", go: ".route-card .btn" });
  await c.ctx.close();
  const r = await open("#/route/goal:C.2.1", { dpr: 2 });
  await r.p.setViewportSize({ width: VIEW.width, height: 3000 });
  await shot(r, "route", { banner: ".route-banner", heads: "all:.unit-head", lv: "all:.trail .lv", current: ".trail li.current .lv" }, { wait: 800 });
  await r.ctx.close();
}
// 3. 营地
{
  const c = await open("#/");
  await shot(c, "camp", { hero: ".camp-hero", cont: ".continue", go: ".continue .btn.primary" });
  await c.ctx.close();
}
// 4. 一课：先猜（选错 → 没关系）→ 讲解卡 → 练习（答对）
{
  const L = lessonOf("P.1.1", "first-program");
  const c = await open("#/lesson/P.1.1/first-program");
  const { p } = c;
  await shot(c, "lesson-guess", { card: ".lcard", kind: ".lcard .step-kind", opts: "all:.lcard .option", check: ".answer-bar .inner > .btn" });
  await p.locator(".lcard .option").nth(0).click();
  await shot(c, "lesson-guess-pick", { opts: "all:.lcard .option", check: ".answer-bar .inner > .btn" });
  await press(p);
  await shot(c, "lesson-guess-wrong", { bar: ".answer-bar", opts: "all:.lcard .option", go: ".answer-bar .inner > .btn" });
  await press(p);
  await shot(c, "lesson-card", { card: ".lcard", go: ".answer-bar .inner > .btn" });
  await advanceTo(p, L, "order-of-lines");
  await shot(c, "lesson-item", { card: ".lcard", opts: "all:.lcard .option", check: ".answer-bar .inner > .btn" });
  await answerCorrectly(p, L.flow.find((s) => s.item?.id === "order-of-lines").item);
  await shot(c, "lesson-item-pick", { opts: "all:.lcard .option", check: ".answer-bar .inner > .btn" });
  await press(p);
  await shot(c, "lesson-item-right", { bar: ".answer-bar", opts: "all:.lcard .option" });
  await c.ctx.close();
}
// 5. 你来当调度器：按标准答案（T1 T2 T1 T1 T2 T2）一步步点，做出竞态，x 最后是 1
{
  const L = lessonOf("C.2.1", "race");
  const item = L.flow.find((s) => s.item?.id === "race-sim").item;
  const c = await open("#/lesson/C.2.1/race");
  const { p } = c;
  await advanceTo(p, L, "race-sim");
  await p.evaluate(() => document.querySelector(".lcard .sim").scrollIntoView({ block: "center" }));
  const T = { card: ".lcard", sim: ".lcard .sim", steps: "all:.lcard .thread .btn", threads: "all:.lcard .thread", shared: ".lcard .sim-threads > .stat", check: ".answer-bar .inner > .btn" };
  await shot(c, "race-0", T);
  for (const [k, th] of item.solution.entries()) {
    await p.locator(".lcard .thread .btn").nth(th).click();
    await shot(c, `race-${k + 1}`, T, { wait: 250 });
  }
  await press(p);
  await shot(c, "race-done", { bar: ".answer-bar", shared: ".lcard .sim-threads > .stat" });
  meta.race = { solution: item.solution, prompt: item.prompt };
  await c.ctx.close();
}
// 6. 你来当页面置换算法（FIFO）：每次缺页点要换出的页
{
  const L = lessonOf("C.2.1", "replacement");
  const item = L.flow.find((s) => s.item?.id === "fifo-sim").item;
  const c = await open("#/lesson/C.2.1/replacement");
  const { p } = c;
  await advanceTo(p, L, "fifo-sim");
  await p.evaluate(() => document.querySelector(".lcard .sim").scrollIntoView({ block: "center" }));
  const T = { card: ".lcard", sim: ".lcard .sim", refs: "all:.lcard .ref", slots: "all:.lcard .slot", check: ".answer-bar .inner > .btn" };
  const labels = () => p.$$eval(".lcard .slot .keys", (ks) => ks.map((k) => k.textContent.trim()));
  await shot(c, "replace-0", T, { extra: { labels: await labels() } });
  for (const [k, pg] of item.solution.entries()) {
    await p.locator(".lcard .slot", { hasText: `换出 ${pg}` }).first().click();
    await p.waitForTimeout(250);
    await shot(c, `replace-${k + 1}`, k + 1 < item.solution.length ? T : { card: ".lcard", sim: ".lcard .sim", refs: "all:.lcard .ref", check: ".answer-bar .inner > .btn" }, { wait: 0, extra: { labels: await labels() } });
  }
  await press(p);
  await shot(c, "replace-done", { bar: ".answer-bar" });
  meta.replace = { solution: item.solution, refs: item.params.refs };
  await c.ctx.close();
}
// 7. 实验室：所有课都学过，9 种实验全在；每个实验单独截一张（视频里拼成九宫格）
{
  const all = Object.entries(packs).flatMap(([s, pk]) => pk.lessons.map((l) => `${s}/${l.id}`));
  const c = await open("#/lab", { prog: progress({ extra: all }), dpr: 2 });
  const items = await c.p.$$eval(".lab-item h3", (hs) => hs.map((h) => h.textContent.trim()));
  meta.lab = { items: [] };
  for (const [i, title] of items.entries()) {
    const el = c.p.locator(".lab-item").nth(i);
    await el.scrollIntoViewIfNeeded();
    await c.p.evaluate(() => document.querySelectorAll(".sprite").forEach((s) => (s.style.visibility = "hidden")));
    const b = await el.boundingBox();
    await el.screenshot({ path: path.join(out, `lab-${i}.png`) });
    meta.lab.items.push({ file: `lab-${i}.png`, title, w: Math.round(b.width), h: Math.round(b.height) });
  }
  console.log("lab", items.join(" · "));
  await c.ctx.close();
}
// 8. 结业挑战：程序设计基础的课都学过、还没点亮 → 说明 → 第一题答对 → 全部答对 → 点亮
{
  const P11 = packs["P.1.1"];
  const prog = progress({ lit: [], extra: P11.lessons.map((l) => `P.1.1/${l.id}`) });
  prog.settings.route = "goal:C.2.1";
  const c = await open("#/boss/P.1.1", { prog });
  const { p } = c;
  await shot(c, "boss-brief", { brief: ".boss-brief", rule: ".boss-brief li:nth-child(2)", start: ".boss-brief .btn.primary" });
  await p.click(".boss-brief .btn.primary");
  await p.waitForSelector(".player");
  const items = P11.boss.items;
  await answerCorrectly(p, items[0]);
  await press(p);
  await shot(c, "boss-q1", { card: ".lcard", bar: ".answer-bar" });
  await press(p);
  for (let guard = 0; guard < 80 && !(await p.$(".lit-mark")); guard++) {
    const btn = bottomBtn(p);
    if (!(await btn.count())) { await p.waitForTimeout(150); continue; }
    if ((await btn.textContent()).trim() === "检查") {
      const id = await p.$eval(".lcard", (el) => el.dataset.item || "");
      const it = items.find((x) => x.id === id);
      if (!it || !(await answerCorrectly(p, it))) await answerAnything(p);
    }
    await press(p);
  }
  await p.waitForSelector(".lit-mark");
  await shot(c, "boss-lit", { panel: ".celebrate .panel", mark: ".lit-mark" }, { wait: 900 });
  // 点亮后路线上后面几站解锁（营地“现在能学”）
  await p.goto(GAME_URL + "#/");
  await shot(c, "boss-camp", { cont: ".continue" }, { wait: 800 });
  await c.ctx.close();
}
// 9. 复习：先在页面里学两课（产生复习卡），把卡的到期时间挪到昨天，再进复习
{
  const c = await open("#/", { prog: progress() });
  const { p } = c;
  const { playLesson } = await import("../../tests/lib/play.mjs");
  for (const l of packs["F.1.1"].lessons.slice(7, 9)) {
    await p.goto(GAME_URL + `#/lesson/F.1.1/${l.id}`);
    await p.waitForSelector(".player");
    await playLesson(p, l.id, l);
  }
  const n = await p.evaluate((k) => {
    const s = JSON.parse(localStorage.getItem(k));
    for (const c of Object.values(s.cards)) c.dueAt = new Date(Date.now() - 864e5).toISOString();
    localStorage.setItem(k, JSON.stringify(s));
    return Object.keys(s.cards).length;
  }, KEY);
  await p.goto(GAME_URL + "#/");
  await p.reload();
  await shot(c, "review-camp", { hero: ".camp-hero", chips: "all:.camp-hero .stat-chip" }, { wait: 800 });
  await p.goto(GAME_URL + "#/review");
  await p.waitForSelector(".player");
  await shot(c, "review", { card: ".lcard", head: ".player-head" }, { wait: 600 });
  meta.reviewCards = n;
  await c.ctx.close();
}
// 10. 地图（悬停一张卡看先学链）、技能页（整页，视频里往下扫）
{
  const c = await open("#/map");
  await shot(c, "map", {}, { wait: 1200 });
  const os = c.p.locator('.mcard[data-id="C.2.1"]');
  if (await os.count()) {
    await os.first().hover();
    await shot(c, "map-hover", { os: '.mcard[data-id="C.2.1"]' }, { wait: 500 });
  }
  await c.ctx.close();
  // 技能页：开头 → 展开“换出谁”这一章的“去哪深入” → 必须先学（理由）和课程证据（官方先修原文）
  const s = await open("#/skill/C.2.1");
  await shot(s, "skill-top", { title: ".page h1" }, { wait: 800 });
  const ch = s.p.locator(".chapter", { hasText: "换出谁" }).first();
  await ch.getByText("去哪深入").click();
  await s.p.waitForTimeout(400);
  await ch.evaluate((el) => el.scrollIntoView({ block: "center" }));
  await shot(s, "skill-deep", { ch, books: ch.locator(".sources, ul, ol").first() });
  await s.p.locator("h3", { hasText: "必须先学" }).first().evaluate((el) => scrollTo(0, el.getBoundingClientRect().top + scrollY - 90));
  await shot(s, "skill-evidence", { need: s.p.locator("h3", { hasText: "必须先学" }).first().locator("xpath=.."), proof: s.p.locator("h3", { hasText: "课程证据" }).first().locator("xpath=..") });
  await s.ctx.close();
}
// 11. 手机：营地、远征、上课
for (const [name, hash] of [["phone-camp", "#/"], ["phone-route", "#/route/goal:C.2.1"], ["phone-lesson", "#/lesson/C.2.1/replacement"]]) {
  const c = await open(hash, { view: PHONE, dpr: 3 });
  if (name === "phone-route") await c.p.evaluate(() => document.querySelector(".trail li.current")?.scrollIntoView({ block: "center" }));
  await shot(c, name, {}, { wait: 700 });
  await c.ctx.close();
}

fs.writeFileSync(path.join(out, "shots.json"), JSON.stringify({ view: VIEW, phone: PHONE, shots: meta }, null, 1));
await browser.close();
if (errors.length) { console.error("页面报错：\n" + errors.join("\n")); process.exit(1); }
console.log("ok →", out);
