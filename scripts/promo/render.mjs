// 出片：Remotion 渲染（H.264 + AAC，1080×1920 30 fps），再用 ffmpeg loudnorm 两遍把整片响度统一到 -16 LUFS（真峰值 ≤ -1.5 dBTP），
// 视频流直接拷贝不重编码。最后用 ffprobe 量时长。
// 用法：node scripts/promo/render.mjs PV,Ad [输出目录，默认 output/promo]
// Remotion 的临时文件写到 temp/promo/tmp（不写 C 盘），打包副本用完删掉。
import fs from "node:fs";
import path from "node:path";
import { execFileSync, spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const PROMO = path.join(ROOT, "src/promo");
const TMP = path.join(ROOT, "temp/promo/tmp");
fs.mkdirSync(TMP, { recursive: true });
const START_CWD = process.cwd();
process.env.TEMP = process.env.TMP = TMP;
process.chdir(PROMO); // 无头浏览器装在 src/promo/node_modules/.remotion（Remotion 按当前目录找），只装一份
const req = createRequire(path.join(PROMO, "package.json"));
const { bundle } = req("@remotion/bundler");
const { renderMedia, selectComposition } = req("@remotion/renderer");

const ids = (process.argv[2] || "PV,Ad").split(",");
// 输出目录按启动时的当前目录解析（下面会切到 src/promo）
const outDir = path.resolve(START_CWD, process.argv[3] || path.join(ROOT, "output/promo"));
fs.mkdirSync(outDir, { recursive: true });
const ff = (args) => execFileSync("ffmpeg", ["-nostdin", "-hide_banner", "-y", ...args], { timeout: 300000, encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });

const serveUrl = await bundle({ entryPoint: path.join(PROMO, "src/index.ts") });
try {
  for (const id of ids) {
    const composition = await selectComposition({ serveUrl, id });
    const raw = path.join(TMP, `${id}-raw.mp4`);
    const t0 = Date.now();
    await renderMedia({ composition, serveUrl, codec: "h264", crf: 16, audioCodec: "aac", audioBitrate: "256k", outputLocation: raw, concurrency: 6,
      onProgress: ({ progress }) => process.stdout.write(`\r${id} ${(progress * 100).toFixed(0)}%   `) });
    console.log(`\n${id} rendered in ${((Date.now() - t0) / 1000).toFixed(0)} s`);
    // loudnorm 第一遍量，第二遍按量出的值线性校正
    const LN = "I=-16:TP=-1.5:LRA=11";
    // ffmpeg 把量出来的 JSON 打在 stderr
    const probe = spawnSync("ffmpeg", ["-nostdin", "-hide_banner", "-i", raw, "-af", `loudnorm=${LN}:print_format=json`, "-f", "null", "-"], { timeout: 300000, encoding: "utf8" });
    const measured = JSON.parse(/\{[^{}]*"input_i"[^{}]*\}/.exec(probe.stderr)[0]);
    const out = path.join(outDir, `${id}.mp4`);
    ff(["-i", raw, "-c:v", "copy", "-af", `loudnorm=${LN}:measured_I=${measured.input_i}:measured_TP=${measured.input_tp}:measured_LRA=${measured.input_lra}:measured_thresh=${measured.input_thresh}:offset=${measured.target_offset}:linear=true`, "-ar", "48000", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out]);
    const dur = execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], { encoding: "utf8" }).trim();
    console.log(`${path.relative(ROOT, out)}  ${Number(dur).toFixed(2)} s  (输入 ${measured.input_i} LUFS → -16)`);
    fs.rmSync(raw, { force: true });
  }
} finally {
  fs.rmSync(serveUrl, { recursive: true, force: true });
}
