// 封面：Remotion 静帧（src/promo/src/Cover.tsx），四种尺寸 → output/promo/cover-{16x9,4x3,3x4,9x16}.png 和 cover.jpg（16:9）。
// 背景用 Blender 片尾镜头第 300 帧（整条路已经点亮成金色）的原始 640×360 PNG（先跑 scripts/promo/render-blender.sh）。
// 用法（项目根目录）：node scripts/promo/cover.mjs
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const PROMO = path.join(ROOT, "src/promo");
const req = createRequire(path.join(PROMO, "package.json"));
process.chdir(PROMO);   // Remotion 把它的无头浏览器下载到 cwd 的 node_modules/.remotion：用 src/promo 那份
const { bundle } = await import(pathToFileURL(req.resolve("@remotion/bundler")).href);
const { renderStill, selectComposition } = await import(pathToFileURL(req.resolve("@remotion/renderer")).href);
const BG = path.join(ROOT, "temp/promo/blender/outro/0300.png");
if (!fs.existsSync(BG)) throw new Error("没有 " + BG + "：先跑 bash scripts/promo/render-blender.sh outro");
fs.copyFileSync(BG, path.join(PROMO, "public/blender/cover-bg.png"));
const tmp = path.join(ROOT, "temp/promo/tmp");
fs.mkdirSync(tmp, { recursive: true });
process.env.TEMP = process.env.TMP = tmp;   // Remotion 的打包副本、Chrome 配置别写系统盘
const OUT = path.join(ROOT, "output/promo");
fs.mkdirSync(OUT, { recursive: true });
const bundleDir = path.join(ROOT, "temp/promo/cover-bundle");
const serveUrl = await bundle({ entryPoint: path.join(PROMO, "src/index.ts"), outDir: bundleDir });
try {
  for (const k of ["16x9", "4x3", "3x4", "9x16"]) {
    const comp = await selectComposition({ serveUrl, id: `Cover-${k}` });
    const out = path.join(OUT, `cover-${k}.png`);
    await renderStill({ composition: comp, serveUrl, frame: 0, output: out, imageFormat: "png" });
    console.log(path.relative(ROOT, out));
  }
  execFileSync("ffmpeg", ["-nostdin", "-y", "-loglevel", "error", "-i", path.join(OUT, "cover-16x9.png"), "-q:v", "2", path.join(OUT, "cover.jpg")]);
  console.log("output/promo/cover.jpg");
} finally {
  fs.rmSync(bundleDir, { recursive: true, force: true });
}
