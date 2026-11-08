// 按 data/promo/music.json 的 edits 剪配乐：每段 [from, to) 秒首尾相接（接缝处 15 ms 交叉淡化防咔哒），
// 输出 src/promo/public/build/music/<名>.wav（48 kHz 立体声 16 bit）。每步一个 ffmpeg，带 -t 和超时（长滤镜图会卡住不退出）。
// 用法：node scripts/promo/music.mjs [名字,…]
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const cfg = JSON.parse(fs.readFileSync(path.join(ROOT, "data/promo/music.json"), "utf8"));
const out = path.join(ROOT, "src/promo/public/build/music"), tmp = path.join(ROOT, "temp/promo/music-edit");
fs.mkdirSync(out, { recursive: true }); fs.mkdirSync(tmp, { recursive: true });
const ff = (args) => execFileSync("ffmpeg", ["-nostdin", "-v", "error", "-y", ...args], { timeout: 120000 });
const want = process.argv[2]?.split(",");
for (const [name, parts] of Object.entries(cfg.edits)) {
  if (want && !want.includes(name)) continue;
  const pieces = parts.map((p, i) => {
    const f = path.join(tmp, `${name}-${i}.wav`);
    ff(["-ss", String(p.from), "-t", String(p.to - p.from), "-i", path.join(ROOT, cfg.tracks[p.track].file), "-ac", "2", "-ar", "48000", "-af", "afade=t=in:d=0.015,afade=t=out:st=" + (p.to - p.from - 0.015) + ":d=0.015", f]);
    return f;
  });
  const total = parts.reduce((s, p) => s + p.to - p.from, 0);
  const list = path.join(tmp, `${name}.txt`);
  fs.writeFileSync(list, pieces.map((f) => `file '${f.split(path.sep).join("/")}'`).join("\n"));
  ff(["-f", "concat", "-safe", "0", "-i", list, "-t", String(total), "-c:a", "pcm_s16le", path.join(out, `${name}.wav`)]);
  console.log(name, total.toFixed(2) + " s");
}
