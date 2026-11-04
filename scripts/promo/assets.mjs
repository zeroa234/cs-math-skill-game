// 把画面要用的素材副本放进 src/promo/public/（Remotion 只读 public/；副本不入库，见 src/promo/.gitignore）：
// 像素字体（assets/fonts，OFL）、导师精灵和立绘（assets/cast，CC BY-NC 4.0，署名 ZipZipPipe）、像素背景（assets/bg）、
// 开场和片尾的两个过渡音（os-review-bilingual 的 scripts/sfx.py 用代码合成的 riser / whoomp）。
// 用法：node scripts/promo/assets.mjs
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const PUB = path.join(ROOT, "src/promo/public");
const copy = (from, to) => {
  const a = path.join(ROOT, from), b = path.join(PUB, to);
  fs.mkdirSync(path.dirname(b), { recursive: true });
  fs.cpSync(a, b, { recursive: true });
};
copy("assets/fonts/fusion-pixel-12px-proportional-zh_hans.otf.woff2", "fonts/fusion-pixel-12px-proportional-zh_hans.otf.woff2");
copy("assets/fonts/fusion-pixel-12px-monospaced-zh_hans.otf.woff2", "fonts/fusion-pixel-12px-monospaced-zh_hans.otf.woff2");
copy("assets/cast/sprites", "cast/sprites");
copy("assets/cast/sprites.json", "cast/sprites.json");
copy("assets/cast/portraits", "cast/portraits");
for (const f of ["title.png", "lane-c.png", "lane-p.png", "lane-f.png"]) copy(`assets/bg/${f}`, `bg/${f}`);
// 上一部宣传片（技能树）的封面，开场“上一集”的缩略图
fs.copyFileSync(path.join(ROOT, "../cs-math-skill-tree/docs/images/cover.webp"), path.join(PUB, "bg/tree-cover.webp"));
const OSR = path.join(ROOT, "../os-review-bilingual/video/public/sfx");
for (const f of ["riser.wav", "whoomp.wav"]) {
  if (!fs.existsSync(path.join(OSR, f))) throw new Error(`找不到 ${path.join(OSR, f)}（os-review-bilingual 的合成音效）`);
  fs.copyFileSync(path.join(OSR, f), path.join(PUB, "sfx", f));
}
console.log("素材副本 →", PUB);
