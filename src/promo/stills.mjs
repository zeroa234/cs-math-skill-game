// 抽帧检查：打包一次，按帧号出 PNG（temp/promo/stills/<合成>-<帧>.png），用完删掉打包副本。
// 用法（在 src/promo 里）：node stills.mjs PVSample 60,150,200 [AdSample 30,90]
// Remotion 的临时文件（打包副本、浏览器配置）写到项目 temp/promo/tmp，不写 C 盘。
import fs from "node:fs";
import path from "node:path";
const ROOT = path.resolve(import.meta.dirname, "../..");
const TMP = path.join(ROOT, "temp/promo/tmp");
fs.mkdirSync(TMP, { recursive: true });
process.env.TEMP = process.env.TMP = TMP;
const { bundle } = await import("@remotion/bundler");
const { renderStill, selectComposition } = await import("@remotion/renderer");

const out = path.join(ROOT, "temp/promo/stills");
fs.mkdirSync(out, { recursive: true });
const args = process.argv.slice(2);
const serveUrl = await bundle({ entryPoint: path.join(import.meta.dirname, "src/index.ts") });
try {
  for (let i = 0; i < args.length; i += 2) {
    const id = args[i];
    const comp = await selectComposition({ serveUrl, id });
    for (const frame of args[i + 1].split(",").map(Number)) {
      const file = path.join(out, `${id}-${frame}.png`);
      await renderStill({ composition: comp, serveUrl, output: file, frame });
      console.log(file);
    }
  }
} finally {
  fs.rmSync(serveUrl, { recursive: true, force: true });
}
