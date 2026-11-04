// 宣传片的音效 = 游戏自己的 8-bit 音效：从 src/game/app/sound.js 读出 ZzFX 参数表（SFX、FANFARE），
// 用同一个 ZzFX 1.4.0 的 buildSamples 离线合成，存成 wav（src/promo/public/sfx/<名字>.wav），视频里和游戏里听到的是同一种声音。
// sound.js 会连带载入整个游戏的状态（JSON 导入、localStorage），node 里直接 import 不了，所以按文字取出那两张表再求值；
// 表的写法变了取不到就报错。ZzFX 的 randomness 用 Math.random，这里换成固定种子，每次合成结果一样。
// 用法：node scripts/promo/sfx.mjs
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const OUT = path.join(ROOT, "src/promo/public/sfx");
const src = fs.readFileSync(path.join(ROOT, "src/game/app/sound.js"), "utf8");
const grab = (re, what) => {
  const m = re.exec(src);
  if (!m) throw new Error(`sound.js 里找不到 ${what}`);
  return Function(`return (${m[1]})`)();
};
const SFX = grab(/const SFX = (\{[\s\S]*?\n\});/, "SFX 表");
const FANFARE = grab(/const FANFARE = (\[[^\]]*\]);/, "FANFARE");
// 和 play("fanfare") 一样：四个音每 110 ms 一个
const FANFARE_NOTE = (f) => [0.55, 0, f, 0.01, 0.07, 0.22, 0, 1.6];

let seed = 20261104;
Math.random = () => ((seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0) / 2 ** 32);
globalThis.AudioContext = class {};   // ZzFX 载入时会 new AudioContext；离线合成用不到
const { ZZFX } = await import("zzfx");
const SR = ZZFX.sampleRate;

function wav(samples) {
  const n = samples.length, buf = Buffer.alloc(44 + n * 2);
  buf.write("RIFF", 0); buf.writeUInt32LE(36 + n * 2, 4); buf.write("WAVE", 8);
  buf.write("fmt ", 12); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(1, 22);
  buf.writeUInt32LE(SR, 24); buf.writeUInt32LE(SR * 2, 28); buf.writeUInt16LE(2, 32); buf.writeUInt16LE(16, 34);
  buf.write("data", 36); buf.writeUInt32LE(n * 2, 40);
  for (let i = 0; i < n; i++) buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, samples[i])) * 32767), 44 + i * 2);
  return buf;
}
fs.mkdirSync(OUT, { recursive: true });
for (const [name, params] of Object.entries(SFX)) {
  const s = ZZFX.buildSamples(...params);
  fs.writeFileSync(path.join(OUT, `${name}.wav`), wav(s));
  console.log(`${name}.wav ${(s.length / SR).toFixed(2)} s`);
}
const notes = FANFARE.map((f) => ZZFX.buildSamples(...FANFARE_NOTE(f)));
const step = Math.round(0.11 * SR), mix = new Float32Array(step * (notes.length - 1) + Math.max(...notes.map((x) => x.length)));
notes.forEach((x, i) => x.forEach((v, j) => (mix[i * step + j] += v)));
fs.writeFileSync(path.join(OUT, "fanfare.wav"), wav(mix));
console.log(`fanfare.wav ${(mix.length / SR).toFixed(2)} s`);
