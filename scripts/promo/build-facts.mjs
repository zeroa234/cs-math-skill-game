// 宣传片画面上的数字和曲线都从游戏自己的数据、代码算出来，不手写：
// - 技能数、必须前置数（src/gen/tree.json）；我的远征的每一站、每站几课（src/game/core/graph.js 的 planRoute，和游戏里排路线是同一个函数）
// - 先猜 / 讲解卡 / 练习 / 结业挑战题数、交互组件种类（src/gen/content.json）
// - 复习曲线：用游戏的 src/game/core/review.js（ts-fsrs）给一道题排期，每次到期都答对，记下每次的间隔和回忆概率
// 旁白（data/promo/script.json）里念到的数字写在 SAID；数据变了、对不上就报错，提醒去改文稿重合成。
// 输出 src/promo/public/build/facts.json。用法：node scripts/promo/build-facts.mjs
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { indexTree, planRoute } from "../../src/game/core/graph.js";
import { newCard, reviewCard, recall } from "../../src/game/core/review.js";
import { PASS_SHARE } from "../../src/game/core/lesson.js";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const read = (p) => JSON.parse(fs.readFileSync(path.join(ROOT, p), "utf8"));
const tree = read("src/gen/tree.json"), content = read("src/gen/content.json");
const g = indexTree(tree);

// 旁白里念的数（文稿 data/promo/script.json）
const SAID = { skills: 183, stops: 5, lessons: 124, sims: 9, bossPass: 0.8 };

const route = planRoute(g, tree.routes.find((r) => r.id === "goal:C.2.1"));
const lane = (id) => g.lanes.get(g.byId.get(id).lane);
const stops = route.stops.map((id) => ({ id, name: g.byId.get(id).name, lane: lane(id).id, color: lane(id).color, lessons: content[id]?.lessons.length ?? 0, boss: content[id]?.boss?.items.length ?? 0 }));
let guesses = 0, cards = 0, items = 0, simItems = 0;
const sims = new Set();
for (const id of route.stops) for (const l of content[id].lessons) for (const s of l.flow) {
  if (s.kind === "guess") guesses++;
  else if (s.kind === "card") cards++;
  else if (s.kind === "item") { items++; if (s.item.type === "sim") { simItems++; sims.add(s.item.sim); } }
}
const passRule = PASS_SHARE;

// 复习：2026-11-01 学过的一道题，此后每次到期都第一次就答对（Good）
const DAY = 864e5, t0 = new Date("2026-11-01T12:00:00Z");
let card = await newCard(t0);
card = (await reviewCard(card, { correct: true, firstTry: true }, t0)).card;
const reviews = [{ day: 0 }];
for (let k = 0; k < 4; k++) {
  const due = new Date(card.dueAt);
  reviews.push({ day: +((due - t0) / DAY).toFixed(2) });
  card = (await reviewCard(card, { correct: true, firstTry: true }, due)).card;
}
// 每次复习之间的回忆概率曲线（复习那一刻回到 1，之后按 FSRS 的遗忘曲线往下掉）
const horizon = reviews.at(-1).day * 1.25;
let replay = await newCard(t0);
replay = (await reviewCard(replay, { correct: true, firstTry: true }, t0)).card;
const curve = [];
for (let i = 1; i < reviews.length + 1; i++) {
  const a = reviews[i - 1].day, b = i < reviews.length ? reviews[i].day : horizon;
  for (let s = 0; s <= 40; s++) {
    const d = a + ((b - a) * s) / 40;
    curve.push([+d.toFixed(3), +(await recall(replay, new Date(t0.getTime() + d * DAY))).toFixed(4)]);
  }
  if (i < reviews.length) replay = (await reviewCard(replay, { correct: true, firstTry: true }, new Date(t0.getTime() + b * DAY))).card;
}

const facts = {
  skills: tree.skills.length,
  required: tree.skills.reduce((n, s) => n + s.required.length, 0),
  lanes: tree.lanes.length,
  route: { id: route.id, goal: route.goal, stops },
  lessons: stops.reduce((n, s) => n + s.lessons, 0),
  guesses, cards, items, simItems, sims: [...sims].sort(), bossItems: stops.reduce((n, s) => n + s.boss, 0), bossPass: passRule,
  bg: fs.readdirSync(path.join(ROOT, "assets/bg")).filter((f) => f.endsWith(".png")).length,
  music: fs.readdirSync(path.join(ROOT, "assets/music")).filter((f) => f.endsWith(".ogg")).length,
  fsrs: { reviews, curve, retention: 0.9 },
};
const bad = [];
if (facts.skills !== SAID.skills) bad.push(`技能 ${facts.skills} ≠ 旁白 ${SAID.skills}`);
if (stops.length !== SAID.stops) bad.push(`远征 ${stops.length} 站 ≠ 旁白 ${SAID.stops}`);
if (facts.lessons !== SAID.lessons) bad.push(`课 ${facts.lessons} ≠ 旁白 ${SAID.lessons}`);
if (facts.sims.length !== SAID.sims) bad.push(`交互组件 ${facts.sims.length} 种 ≠ 旁白 ${SAID.sims}`);
if (facts.bossPass !== SAID.bossPass) bad.push(`结业挑战点亮线不是 80%`);
if (bad.length) { console.error("数据和旁白对不上，改 data/promo/script.json 重合成旁白：\n" + bad.join("\n")); process.exit(1); }
fs.mkdirSync(path.join(ROOT, "src/promo/public/build"), { recursive: true });
fs.writeFileSync(path.join(ROOT, "src/promo/public/build/facts.json"), JSON.stringify(facts, null, 1));
console.log(`facts.json：${facts.skills} 技能 · ${stops.length} 站 ${facts.lessons} 课 · ${facts.sims.length} 种组件（${facts.sims.join(" ")}）· 复习间隔 ${reviews.map((r) => r.day).join(" / ")} 天`);
