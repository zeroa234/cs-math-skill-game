// 宣传片用的游戏截图（真实画面）：系统 Edge 无头（scripts/lib/edge.mjs），打开构建好的游戏（先 npm run build）。
// 存档里打开“减少动画”：角色不动、不放彩带、文字直接显示，每张图可复现；要动的部分在视频里补。
// 截图前把导师精灵藏起来，记下谁、什么动作、站在哪（CSS px），视频里在原位按帧播放动画条。
// 一课的每一屏都截：用游戏自己的 tests/lib/play.mjs 按正确答案往前走（playLesson 的 onStep 每屏回调一次）。
// 输出：src/promo/public/build/shots/<名>.png 和 shots.json（每张图的尺寸、像素倍数、元素框、精灵位置）。
// 用法：node scripts/promo/capture.mjs [只截名字含这些词的组，逗号分隔]
import fs from "node:fs";
import path from "node:path";
import { ROOT, GAME_URL, launchEdge } from "../lib/edge.mjs";
import { playLesson, answerCorrectly } from "../../tests/lib/play.mjs";

const OUT = path.join(ROOT, "src/promo/public/build/shots");
fs.mkdirSync(OUT, { recursive: true });
const metaPath = path.join(OUT, "shots.json");
const meta = fs.existsSync(metaPath) ? JSON.parse(fs.readFileSync(metaPath, "utf8")) : {};
const only = process.argv[2]?.split(",");
const packs = JSON.parse(fs.readFileSync(path.join(ROOT, "src/gen/content.json"), "utf8"));
const KEY = "cs-math-skill-game/progress";
const DESK = { width: 1280, height: 720 }, PHONE = { width: 390, height: 844 };
const errors = [];

// 存档：streak = 连续学习的天数（到今天为止每天都有学习记录）；lit = 已点亮的技能（课全学过）
function progress({ streak = 5, lit = ["P.1.1", "P.2.2"], partial = { "F.1.1": 7 } } = {}) {
  const day = (d) => new Date(Date.now() - d * 864e5);
  const at = day(Math.max(streak, 3)).toISOString();
  const p = { v: 3, createdAt: at, xp: 640, days: {}, achievements: { "first-lesson": at, "first-light": at }, skills: {}, lessons: {}, cards: {},
    settings: { introSeen: true, route: "goal:C.2.1", sound: false, sourceLang: "zh", reduceMotion: true } };
  for (let d = 0; d < streak; d++) p.days[day(d).toISOString().slice(0, 10)] = 60;
  for (const id of lit) {
    p.skills[id] = { lit: at, boss: { at, graded: true, auto: 1 } };
    for (const l of packs[id].lessons) p.lessons[`${id}/${l.id}`] = { done: at, stars: 3, best: 1, attempts: 1 };
  }
  for (const [id, n] of Object.entries(partial)) for (const l of packs[id].lessons.slice(0, n)) p.lessons[`${id}/${l.id}`] ||= { done: at, stars: 2, best: 0.8, attempts: 1 };
  return p;
}

const browser = await launchEdge(path.join(ROOT, "temp/browser"));
async function open(hash, { view = DESK, dpr = 3, dark = false, prog = progress() } = {}) {
  const phone = view.width < 500;
  const ctx = await browser.newContext({ viewport: view, deviceScaleFactor: dpr, colorScheme: dark ? "dark" : "light", isMobile: phone, hasTouch: phone });
  await ctx.addInitScript(([k, s]) => { localStorage.setItem(k, JSON.stringify(s)); }, [KEY, prog]);
  const p = await ctx.newPage();
  p.setDefaultTimeout(8000);
  p.on("pageerror", (e) => errors.push(`${hash}: ${e.message}`));
  p.on("console", (m) => { if (m.type() === "error") errors.push(`${hash}: ${m.text()}`); });
  await p.goto(GAME_URL + hash);
  await p.waitForTimeout(900);
  return { ctx, p, dpr };
}
const boxOf = (p, sel) => p.evaluate((sel) => [...document.querySelectorAll(sel)].map((e) => e.getBoundingClientRect())
  .filter((r) => r.width > 0 && r.height > 0).map((r) => ({ x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) })), sel);
const takeSprites = (p) => p.evaluate(() => [...document.querySelectorAll(".sprite")].map((s) => {
  const fr = s.querySelector(".sprite-frame");
  const m = fr && /sprites\/(\w+)\/(\w+)\.webp/.exec(fr.style.backgroundImage);
  const r = s.getBoundingClientRect();
  s.style.visibility = "hidden";
  return m && r.width > 0 ? { who: m[1], action: m[2], x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height), flip: /scaleX\(-1\)/.test(fr.style.transform) } : null;
}).filter(Boolean));

// 截一张：targets = { 名字: 选择器 }，记下每个选择器所有匹配元素的框；el = 只截这个元素
async function shot({ p, dpr }, name, { targets = {}, el, wait = 400 } = {}) {
  await p.waitForTimeout(wait);
  const t = {};
  for (const [k, sel] of Object.entries(targets)) t[k] = await boxOf(p, sel);
  const sprites = await takeSprites(p);
  const file = `${name}.png`;
  let clip = null;
  if (el) { clip = (await boxOf(p, el))[0]; await p.locator(el).first().screenshot({ path: path.join(OUT, file) }); }
  else await p.screenshot({ path: path.join(OUT, file) });
  await p.evaluate(() => document.querySelectorAll(".sprite").forEach((s) => (s.style.visibility = "")));
  const vp = p.viewportSize();
  meta[name] = { file, w: clip ? clip.w : vp.width, h: clip ? clip.h : vp.height, dpr, clip, targets: t, sprites };
  console.log(name, sprites.map((s) => s.who + "/" + s.action).join(" "));
}
const want = (group) => !only || only.some((w) => group.includes(w));

// 营地：连续 N 天（PV 的“每天一课”）
if (want("camp")) {
  for (const dark of [false, true]) for (const n of [1, 2, 3, 4, 5, 6, 7, 14, 30, 31]) {
    // 6 倍像素：PV 里“连续 N 天”那枚小牌子要放到很大
    const c = await open("#/", { dark, dpr: 6, prog: progress({ streak: n }) });
    await shot(c, `camp-${dark ? "dark" : "light"}-${n}`, { el: ".camp-hero", targets: { chips: ".camp-hero .stat-chip" } });
    await shot(c, `streak-${dark ? "dark" : "light"}-${n}`, { el: '.camp-hero .stat-chip[title="连续学习天数"]', wait: 50 });
    await c.ctx.close();
  }
}

// 一课的每一屏（电脑和手机各一遍）：先按正确答案走完；再从头开一次，第一道题故意选错，截“答错”
const LESSON = ["P.1.1", "first-program"];
for (const [tag, view] of [["desk", DESK], ["phone", PHONE]]) {
  if (!want(`lesson-${tag}`)) continue;
  for (const dark of [false, true]) {
    const theme = dark ? "dark" : "light";
    const lesson = packs[LESSON[0]].lessons.find((l) => l.id === LESSON[1]);
    // 第一次学这一课的存档：结算页才有经验和星星（学过的课重做，经验是 +0）
    const fresh = progress({ streak: 2, lit: [], partial: {} });
    const c = await open(`#/lesson/${LESSON.join("/")}`, { view, dark, prog: fresh });
    let k = 0;
    await playLesson(c.p, "promo", lesson, { errors, onStep: async (label) => {
      await shot(c, `lesson-${tag}-${theme}-${String(k++).padStart(2, "0")}`, { targets: { card: ".lcard", options: ".lcard .option", bar: ".answer-bar", btn: ".answer-bar .inner > .btn" }, wait: 250 });
    } });
    // 结算页：星星有入场动画（第 3 颗 1.4 s 才开始），等 2.5 s 再截；另截一张不带星星的，视频里按拍点自己让星星弹出来
    const doneTargets = { panel: ".celebrate .panel", stars: ".big-stars span", rewards: ".reward" };
    await shot(c, `lesson-${tag}-${theme}-done`, { targets: doneTargets, wait: 2500 });
    await c.p.evaluate(() => document.querySelectorAll(".big-stars span").forEach((s) => (s.style.visibility = "hidden")));
    await shot(c, `lesson-${tag}-${theme}-done-nostars`, { targets: doneTargets, wait: 100 });
    await c.ctx.close();
    // 答错的那一下：第一道题选一个错的选项
    const w = await open(`#/lesson/${LESSON.join("/")}`, { view, dark, prog: fresh });
    const first = lesson.flow.find((s) => s.item)?.item;
    const texts = await w.p.$$eval(".lcard .option .otext", (els) => els.map((e) => e.textContent.trim()));
    const wrongIdx = first.options.findIndex((o) => !o.correct);
    const k2 = texts.findIndex((t) => t && first.options[wrongIdx] && t.includes(String(first.options[wrongIdx].text).slice(0, 4)));
    await w.p.locator(".lcard .option").nth(Math.max(0, k2)).click();
    await shot(w, `lesson-${tag}-${theme}-wrong-pick`, { targets: { card: ".lcard", options: ".lcard .option", bar: ".answer-bar", btn: ".answer-bar .inner > .btn" } });
    await w.p.locator(".answer-bar .inner > .btn").click();
    await shot(w, `lesson-${tag}-${theme}-wrong`, { targets: { card: ".lcard", options: ".lcard .option", bar: ".answer-bar" } });
    await w.ctx.close();
  }
}

// 远征路线（手机）：广告里手机屏幕上的关卡路径
if (want("route")) {
  for (const dark of [false, true]) {
    const c = await open("#/route/goal:C.2.1", { view: PHONE, dark });
    await c.p.evaluate(() => document.querySelector(".trail li.current")?.scrollIntoView({ block: "center" }));
    await shot(c, `route-phone-${dark ? "dark" : "light"}`, { targets: { lv: ".trail .lv", current: ".trail li.current .lv", heads: ".unit-head" }, wait: 600 });
    await c.ctx.close();
  }
}

// 截一个元素（Playwright locator）：可以比视口高，元素截图会自己滚动；精灵同样藏起来记下位置
async function shotEl({ p, dpr }, name, loc) {
  await loc.scrollIntoViewIfNeeded();
  await p.waitForTimeout(250);
  const b = await loc.boundingBox();
  const sprites = await takeSprites(p);
  // 顶栏是贴顶的，元素滚到它下面时会被挡住：截图时先藏起来
  await p.evaluate(() => { const t = document.querySelector(".topbar"); if (t) t.style.visibility = "hidden"; });
  await loc.screenshot({ path: path.join(OUT, `${name}.png`) });
  await p.evaluate(() => { document.querySelectorAll(".sprite").forEach((s) => (s.style.visibility = "")); const t = document.querySelector(".topbar"); if (t) t.style.visibility = ""; });
  meta[name] = { file: `${name}.png`, w: Math.round(b.width), h: Math.round(b.height), dpr, clip: { x: 0, y: 0, w: Math.round(b.width), h: Math.round(b.height) }, targets: {}, sprites };
  console.log(name);
}

// 实验室里的实验（PV“越学越深”和广告“动手”用）：所有课都算学过，实验就全列出来；每个实验按它自己的玩法点几下，
// 每一下截一张，视频里按拍点切这几张就是在“动”。操作都是游戏界面上真实的按钮。
if (want("lab")) {
  const all = progress({ streak: 7, lit: Object.keys(packs), partial: {} });
  const LABS = [
    ["trace", "Python 单步执行", async (c) => c.getByRole("button", { name: "下一步", exact: true }).click(), 4],
    ["stack", "栈", async (c, k) => c.getByRole("button", { name: k < 3 ? `push ${k + 1}` : "pop", exact: true }).click(), 4],
    ["hash", "哈希表（线性探测）", async (c, k) => c.locator(".slot").nth([3, 4, 5, 6][k]).click(), 4],
    // 你来当调度器：T1 读 x → T2 读 x → T1 加一写回 → T2 加一写回，两个都加了 1，x 却是 1（竞态）
    ["threads", "你来当调度器", async (c, k) => c.getByRole("button", { name: new RegExp(`^让 ${["T1", "T2", "T1", "T1", "T2", "T2"][k]}`) }).click(), 6],
    ["bfs", "广度优先搜索", async (c) => c.getByRole("button", { name: "让算法走一步" }).click(), 4],
    ["descent", "梯度下降（一维）", async (c) => c.getByRole("button", { name: "走 10 步" }).click(), 3],
    ["matrix", "矩阵就是变换", async (c, k) => { const v = [["0", "-1", "1", "0"], ["2", "0", "0", "1"], ["1", "2", "2", "4"]][k]; const ins = c.locator("input"); for (let i = 0; i < 4; i++) await ins.nth(i).fill(v[i]); }, 3],
    ["replace", "页面置换", null, 0],
    ["paging", "分页地址转换", null, 0],
    ["sched", "CPU 调度（时间片轮转）", null, 0],
  ];
  for (const dark of [false, true]) {
    const theme = dark ? "dark" : "light";
    const c = await open("#/lab", { view: PHONE, dark, prog: all });
    for (const [key, title, act, n] of LABS) {
      const card = c.p.locator("article.lab-item").filter({ has: c.p.getByRole("heading", { name: title, exact: true }) }).first();
      if (!(await card.count())) { errors.push(`实验室里没有“${title}”`); continue; }
      await shotEl(c, `lab-${theme}-${key}-0`, card);
      for (let k = 0; k < n; k++) {
        try { await act(card, k); } catch (e) { errors.push(`${title} 第 ${k + 1} 下：${e.message.split("\n")[0]}`); break; }
        await shotEl(c, `lab-${theme}-${key}-${k + 1}`, card);
      }
    }
    await c.ctx.close();
  }
}

// 结业挑战（程序设计基础）：每题按正确答案做，每屏截一张，最后是“已点亮”；存档里课都学完了、技能还没点亮
if (want("boss")) {
  const SK = "P.1.1";
  const prog = progress({ streak: 7, lit: [], partial: { [SK]: packs[SK].lessons.length } });
  const boss = { flow: packs[SK].boss.items.map((item) => ({ item })) };
  meta.bossInfo = { skill: SK, items: packs[SK].boss.items.length };
  for (const dark of [false, true]) {
    const theme = dark ? "dark" : "light";
    const c = await open(`#/boss/${SK}`, { view: PHONE, dark, prog });
    await shot(c, `boss-${theme}-brief`, { targets: { brief: ".boss-brief" } });
    await c.p.getByRole("button", { name: "开始", exact: true }).click();
    let k = 0;
    await playLesson(c.p, "boss", boss, { errors, onStep: async (label) => {
      if (label.startsWith("verdict")) await shot(c, `boss-${theme}-${String(k++).padStart(2, "0")}`, { targets: { card: ".lcard", bar: ".answer-bar" }, wait: 200 });
    } });
    await shot(c, `boss-${theme}-done`, { targets: { panel: ".celebrate .panel" }, wait: 1500 });
    await c.ctx.close();
  }
}

// 技能页（操作系统）：点开第一章的“去哪深入”，截这一章（广告“每一章还写了，去哪本书接着学”）
if (want("skill")) {
  for (const dark of [false, true]) {
    const theme = dark ? "dark" : "light";
    const c = await open("#/skill/C.2.1", { view: PHONE, dark });
    await shot(c, `skill-${theme}-top`, { targets: { head: ".skill-head" } });
    const ch = c.p.locator("ol.chapters > li").first();
    await ch.getByRole("button", { name: "去哪深入" }).click();
    await shotEl(c, `skill-${theme}-ch1`, ch);
    await c.ctx.close();
  }
}

// 技能地图（手机）：广告里从手机里铺开的那张图
if (want("map")) {
  for (const dark of [false, true]) {
    const c = await open("#/map", { view: PHONE, dark });
    await shot(c, `map-phone-${dark ? "dark" : "light"}`, { wait: 1200 });
    await c.ctx.close();
  }
}

fs.writeFileSync(metaPath, JSON.stringify(meta, null, 1));
await browser.close();
if (errors.length) { console.error("页面报错：\n" + errors.join("\n")); process.exitCode = 1; }
