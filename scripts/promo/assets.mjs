// 把宣传片要用的游戏素材同步进 Remotion 的 public/（不进 git，见 src/promo/.gitignore）：
// 导师精灵和立绘、像素背景、像素字体、游戏音乐；配乐候选从 temp/promo/music-dl（OpenGameArt 下载，许可证见 data/promo/music.json）。
// 用法：node scripts/promo/assets.mjs
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const PUB = path.join(ROOT, "src/promo/public");
const copy = (from, to) => { fs.mkdirSync(path.dirname(to), { recursive: true }); fs.copyFileSync(from, to); };
const copyDir = (from, to) => fs.cpSync(from, to, { recursive: true });

copyDir(path.join(ROOT, "assets/cast/sprites"), path.join(PUB, "cast/sprites"));
copy(path.join(ROOT, "assets/cast/sprites.json"), path.join(PUB, "cast/sprites.json"));
copyDir(path.join(ROOT, "assets/cast/portraits"), path.join(PUB, "cast/portraits"));
copyDir(path.join(ROOT, "assets/bg"), path.join(PUB, "bg"));
for (const f of fs.readdirSync(path.join(ROOT, "assets/fonts"))) copy(path.join(ROOT, "assets/fonts", f), path.join(PUB, "fonts", f));
// 像素图标：和游戏同一套 pixelarticons（MIT，24×24 网格），只取 path，视频里画成内联 SVG
const ICONS = ["star", "fire", "sparkle", "book-open", "lock", "zap", "lightbulb", "trophy", "map", "check", "close", "heart", "code", "cpu", "chart", "flag"];
const icons = {};
for (const name of ICONS) {
  const f = path.join(ROOT, "node_modules/pixelarticons/svg", `${name}.svg`);
  if (fs.existsSync(f)) icons[name] = [...fs.readFileSync(f, "utf8").matchAll(/<path[^>]*\sd="([^"]+)"/g)].map((m) => m[1]);
}
fs.mkdirSync(path.join(PUB, "build"), { recursive: true });
fs.writeFileSync(path.join(PUB, "build/icons.json"), JSON.stringify(icons));
// 技能树（PV 结尾整棵树亮起来）：游戏构建出的 src/gen/tree.json 里每个技能的 id、领域、地图坐标和必须前置
const tree = JSON.parse(fs.readFileSync(path.join(ROOT, "src/gen/tree.json"), "utf8"));
fs.writeFileSync(path.join(PUB, "build/tree.json"), JSON.stringify({
  lanes: tree.lanes.map(({ id, domain, short, color }) => ({ id, domain, short, color })),
  skills: tree.skills.map(({ id, name, domain, lane, step, x, y, required }) => ({ id, name, domain, lane, step, x, y, required })),
}));
console.log("promo assets synced to", path.relative(ROOT, PUB), "icons:", Object.keys(icons).join(" "));
