// 宣传片音效：离线合成成 wav（src/promo/public/build/sfx/<名>.wav）。
// 游戏里的 8-bit 音效直接读 src/game/app/sound.js 的 ZzFX 参数（改了游戏音效，这里重跑就跟上）；
// 宣传片额外要的几声（书砸下来、心跳、嗖）是自己配的参数，起点取 ZzFX README 里的 Drum 预设。
// ZzFX 1.4.0 的 buildSamples 用 Math.random 做随机抖动，这里换成固定种子，每次合成结果一样。
// 用法：node scripts/promo/sfx.mjs
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const out = path.join(ROOT, "src/promo/public/build/sfx");
fs.mkdirSync(out, { recursive: true });

globalThis.AudioContext = class { }; // ZzFX 一加载就 new AudioContext；离线合成用不到它
let seed = 1;
Math.random = () => ((seed = (seed * 16807) % 2147483647) - 1) / 2147483646;
const { ZZFX } = await import("zzfx");

// 从 sound.js 里取出 SFX 表和 FANFARE（它是给浏览器的模块，直接 import 会拉进游戏状态）
const src = fs.readFileSync(path.join(ROOT, "src/game/app/sound.js"), "utf8");
const table = /const SFX = \{([\s\S]*?)\n\};/.exec(src)[1];
const SFX = Object.fromEntries([...table.matchAll(/(\w+): \[([^\]]*)\]/g)].map((m) => [m[1], m[2].split(",").map((s) => (s.trim() === "" ? undefined : Number(s)))]));
const FANFARE = /const FANFARE = \[([^\]]*)\]/.exec(src)[1].split(",").map(Number);

const PROMO = {
  thud: [1.2, 0, 70, 0, 0.02, 0.35, 0, 1, -1, 0, 0, 0, 0, 6],      // 书砸下来：低频 + 噪声
  heart: [0.9, 0, 55, 0, 0.03, 0.12, 0, 1, -0.5, 0, 0, 0, 0, 1],   // 心跳的一下（结业挑战的低音）
  whoosh: [0.5, 0, 200, 0.08, 0.05, 0.2, 4, 1, 3, 0, 0, 0, 0, 3],  // 嗖：滑音噪声
  pop: [0.5, 0, 900, 0, 0.01, 0.06, 0, 1.4, 8],                    // 字弹出来
};

const SR = ZZFX.sampleRate;
function writeWav(file, samples) {
  const pcm = Int16Array.from(samples, (v) => Math.max(-32767, Math.min(32767, Math.round(v * 32767 * 0.9))));
  const head = Buffer.alloc(44);
  head.write("RIFF", 0); head.writeUInt32LE(36 + pcm.length * 2, 4); head.write("WAVE", 8);
  head.write("fmt ", 12); head.writeUInt32LE(16, 16); head.writeUInt16LE(1, 20); head.writeUInt16LE(1, 22);
  head.writeUInt32LE(SR, 24); head.writeUInt32LE(SR * 2, 28); head.writeUInt16LE(2, 32); head.writeUInt16LE(16, 34);
  head.write("data", 36); head.writeUInt32LE(pcm.length * 2, 40);
  fs.writeFileSync(file, Buffer.concat([head, Buffer.from(pcm.buffer)]));
}
const build = (p) => ZZFX.buildSamples(...p);

for (const [name, p] of Object.entries({ ...SFX, ...PROMO })) writeWav(path.join(out, `${name}.wav`), build(p));
// 号角：和游戏一样四个音隔 110 ms
const notes = FANFARE.map((f) => build([0.55, 0, f, 0.01, 0.07, 0.22, 0, 1.6]));
const step = Math.round(0.11 * SR), mix = new Float32Array(step * 3 + Math.max(...notes.map((n) => n.length)));
notes.forEach((n, i) => n.forEach((v, k) => (mix[i * step + k] += v)));
writeWav(path.join(out, "fanfare.wav"), mix);
console.log("sfx:", [...Object.keys(SFX), ...Object.keys(PROMO), "fanfare"].join(" "));
