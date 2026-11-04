// 公共：尺寸、配色（游戏深色主题的变量）、数据、按旁白取时刻、缓动。
// 画面代码只按“拍”和“旁白里的词”取帧号（timeline.json / words.json 由 scripts/promo/ 生成），不写死秒数：
// 旁白重合成、拍长变了，画面跟着走。做法照 cs-math-skill-tree 的宣传片（src/promo/src/lib/core.ts）。
import { Easing, interpolate } from "remotion";
import tlJson from "../../public/build/timeline.json";
import wordsJson from "../../public/build/words.json";
import factsJson from "../../public/build/facts.json";
import verifyJson from "../../public/build/verify.json";
import shotsJson from "../../public/shots/shots.json";

export const W = 1920, H = 1080, FPS = 30;
// src/web/style.css 深色主题（:root[data-theme="dark"]）
export const C = {
  bg: "#14142b", bg2: "#1b1b3a", panel: "#1f1f3f", panel2: "#26264c", ink: "#eceaf7", ink2: "#c8c5e2", muted: "#a9a5c9", line: "#35355f",
  accent: "#7187ff", accentStrong: "#a9b6ff", good: "#52c46a", bad: "#f07a7f", gold: "#f2bd3a", goldEdge: "#b08415",
  rim: "#7474b4", rimDeep: "#4a4a85", dialog: "#c9b88a", dialogDeep: "#8f7f52", night: "#0e0d24",
};
export const PX = '"Fusion Pixel", "Microsoft YaHei", sans-serif';
export const MONO = '"Fusion Pixel Mono", "Fusion Pixel", Consolas, monospace';

// ── 数据 ──────────────────────────────────────────────
export type Speech = { start: number; end: number; text: string };
export type Beat = { id: string; start: number; end: number; speech: Speech[] };
export type Sub = { start: number; end: number; text: string };
export const TL = tlJson as unknown as { fps: number; frames: number; beats: Beat[]; subs: Sub[]; title: { zh: string } };
type WordSent = { text: string; start: number; end: number; words: [number, number, number, number][] };
const WORDS = wordsJson as unknown as Record<string, WordSent[]>;
export type Box = { x: number; y: number; w: number; h: number };
export type SpriteAt = Box & { who: string; action: string; flip: boolean };
export type ShotMeta = { file: string; w: number; h: number; dpr: number; targets: Record<string, Box & Box[]>; sprites: SpriteAt[];
  line?: { text: string; x: number; y: number; w: number; h: number; size: number; lh: number; color: string } };
const SJ = shotsJson as unknown as { view: { width: number; height: number }; shots: Record<string, ShotMeta> & Record<string, any> };
export const SHOTS = SJ.shots as Record<string, ShotMeta>;
export const LAB = (SJ.shots as any).lab as { items: { file: string; title: string; w: number; h: number }[] };
export const VW = SJ.view.width, VH = SJ.view.height;      // 截图视口（CSS px）
export const box = (shot: string, k: string) => {
  const b = SHOTS[shot]?.targets[k];
  if (!b) throw new Error(`截图 ${shot} 里没有 ${k}`);
  return b as Box;
};
export const boxes = (shot: string, k: string) => (SHOTS[shot]?.targets[k] as unknown as Box[]) ?? [];
export type Stop = { id: string; name: string; lane: string; color: string; lessons: number; boss: number };
export const F = factsJson as unknown as {
  skills: number; required: number; lanes: number; route: { stops: Stop[] }; lessons: number; guesses: number; cards: number; items: number;
  sims: string[]; bossItems: number; bossPass: number; bg: number; music: number;
  fsrs: { reviews: { day: number }[]; curve: [number, number][]; retention: number };
};
export const V = verifyJson as unknown as { runs: { id: string; name: string; cmd: string; last: string; claims: number; tool: string }[]; total: number };

// ── 时刻 ──────────────────────────────────────────────
const BEATS = new Map(TL.beats.map((b) => [b.id, b]));
export const beat = (id: string) => {
  const b = BEATS.get(id);
  if (!b) throw new Error("没有这一拍：" + id);
  return b;
};
export const say = (id: string, i = 0) => { const s = beat(id).speech; return s[(i + s.length) % s.length].start; };
export const sayEnd = (id: string, i = -1) => { const s = beat(id).speech; return s[(i + s.length) % s.length].end; };
/** 旁白说到某个词的那一帧（end = true 取这个词说完）。找不到就报错，免得静默对错位置 */
export function w(id: string, word: string, end = false): number {
  for (const s of WORDS[id] ?? []) {
    const i = s.text.indexOf(word);
    if (i < 0) continue;
    const j = end ? i + word.length - 1 : i;
    const hit = s.words.find(([c, n]) => c <= j && j < c + n) ?? s.words.reduce((a, b) => (Math.abs(b[0] - j) < Math.abs(a[0] - j) ? b : a));
    return end ? hit[3] : hit[2];
  }
  throw new Error(`旁白里没有“${word}”（拍 ${id}）`);
}

// ── 缓动 ──────────────────────────────────────────────
export const ease = Easing.bezier(0.45, 0, 0.2, 1);
export const easeOut = Easing.bezier(0.16, 0.8, 0.3, 1);
export const backOut = Easing.bezier(0.3, 1.5, 0.5, 1);
/** f 帧时，从 start 帧起 dur 秒内由 a 走到 b */
export function tw(f: number, start: number, dur: number, a = 0, b = 1, e = ease) {
  return interpolate(f, [start, start + Math.max(1, dur * FPS)], [a, b], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: e });
}
/** 像素游戏式的“一格一格”动：把 0..1 量化成 n 档 */
export const steps = (t: number, n: number) => Math.round(t * n) / n;
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const clamp01 = (x: number) => Math.max(0, Math.min(1, x));
/** 按字符串定的稳定伪随机 [0,1) */
export function rnd(s: string, salt = 0) {
  let h = 2166136261 ^ salt;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619);
  return ((h >>> 0) % 100000) / 100000;
}
