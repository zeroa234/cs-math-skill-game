// 公共部件，全部按游戏的像素风来：像素字体、四道硬阴影的切角边框（style.css 的 .dialog / .start-pop 同一个做法）、
// 像素鼠标、一格一格的动画；页面截图窗口（镜头推拉 + 页面里的导师照样动）、字幕、音效、逐字打出、像素溶解转场。
import React from "react";
import { AbsoluteFill, Html5Audio, Img, Sequence, staticFile, useCurrentFrame } from "remotion";
import { Box, C, FPS, H, PX, SHOTS, TL, VW, W, clamp01, ease, lerp, rnd, steps, tw } from "./core";
import { Sprite, spriteScale } from "./sprite";

/** 像素边框：上下左右四道硬阴影留出切角，底下一道更深的“厚度”（游戏 .dialog 的写法），p = 一个像素多宽 */
export const frame = (p: number, rim: string, deep: string, extra = "") =>
  `0 ${-p}px 0 0 ${rim}, 0 ${p}px 0 0 ${rim}, ${-p}px 0 0 0 ${rim}, ${p}px 0 0 0 ${rim}, 0 ${3 * p}px 0 0 ${deep}${extra ? ", " + extra : ""}`;

// ── 背景：游戏开场的夜空（assets/bg/title.png，480×270 像素图按整数倍放大）+ 一闪一闪的像素星 ──
export const Bg: React.FC = () => {
  const f = useCurrentFrame();
  const stars = React.useMemo(() => Array.from({ length: 70 }, (_, i) => ({ x: Math.floor(rnd("sx" + i) * 320) * 6, y: Math.floor(rnd("sy" + i) * 120) * 6, s: rnd("ss" + i) < 0.25 ? 12 : 6, ph: rnd("sp" + i) * 90 })), []);
  return (
    <AbsoluteFill style={{ background: C.night }}>
      <Img src={staticFile("bg/title.png")} style={{ position: "absolute", left: 0, top: 0, width: W, height: H, imageRendering: "pixelated", opacity: 0.32,
        transform: `translateX(${-Math.round((f / 12) % 4) * 0}px)` }} />
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(14,13,36,0.55) 0%, rgba(14,13,36,0.85) 100%)" }} />
      {stars.map((s, i) => {
        const on = Math.floor((f + s.ph) / 18) % 5 !== 0;
        return <div key={i} style={{ position: "absolute", left: s.x, top: s.y, width: s.s, height: s.s, background: "#cfd8ff", opacity: on ? 0.55 : 0.15 }} />;
      })}
    </AbsoluteFill>
  );
};

/** 字幕：游戏对白框的配色（金色边框），像素字 36 px（12 px 字形的 3 倍，不糊）。屏幕上已经有同样大字的拍（hide）不出 */
export const Subtitles: React.FC<{ hide: string[] }> = ({ hide }) => {
  const f = useCurrentFrame();
  const hidden = TL.beats.filter((b) => hide.includes(b.id)).map((b) => [b.start, b.end]);
  const i = TL.subs.findIndex((s) => f >= s.start - 2 && f < s.end + 4);
  if (i < 0) return null;
  const s = TL.subs[i];
  if (hidden.some(([a, b]) => s.start >= a && s.start < b)) return null;
  const prev = TL.subs[i - 1], next = TL.subs[i + 1];
  const joinIn = prev && prev.end >= s.start - 1, joinOut = next && next.start <= s.end + 1;
  const o = Math.min(joinIn ? 1 : steps(tw(f, s.start - 2, 0.15), 3), joinOut ? 1 : 1 - steps(tw(f, s.end + 1, 0.12), 3));
  return (
    <div style={{ position: "absolute", left: 0, right: 0, bottom: 52, display: "flex", justifyContent: "center", opacity: o }}>
      <div style={{ fontFamily: PX, fontSize: 36, lineHeight: "48px", color: C.ink, padding: "8px 30px", background: "rgba(29,24,48,0.94)",
        boxShadow: frame(6, C.dialog, C.dialogDeep) }}>{s.text}</div>
    </div>
  );
};

/** 在 at 帧放一个音效（public/sfx/<name>.wav：游戏自己的 ZzFX 音效，scripts/promo/sfx.mjs 合成） */
export const Sfx: React.FC<{ at: number; name: string; v?: number }> = ({ at, name, v = 0.35 }) => (
  <Sequence from={Math.round(at)} durationInFrames={FPS * 3} layout="none">
    <Html5Audio src={staticFile(`sfx/${name}.wav`)} volume={v} />
  </Sequence>
);

// ── 页面截图：窗口 + 镜头 ───────────────────────────────
/** 镜头：(x, y) = 看向截图视口里的哪一点（CSS px），z = 放大倍数（1 = 视口宽度放满窗口） */
export type Cam = { x: number; y: number; z: number };
export const CAM0: Cam = { x: VW / 2, y: 342, z: 1 };
/** 关键帧插值；缩放按对数插（推近的速度看起来均匀） */
export function camAt(f: number, keys: [number, Cam][], e = ease): Cam {
  if (f <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) {
    const [f0, a] = keys[i - 1], [f1, b] = keys[i];
    if (f <= f1) {
      const t = e(clamp01((f - f0) / Math.max(1, f1 - f0)));
      return { x: lerp(a.x, b.x, t), y: lerp(a.y, b.y, t), z: Math.exp(lerp(Math.log(a.z), Math.log(b.z), t)) };
    }
  }
  return keys[keys.length - 1][1];
}
export type Rect = { x: number; y: number; w: number; h: number };
// 16:9 窗口，下面留出字幕的位置（字幕不压住游戏底部的反馈栏）
export const WIN: Rect = { x: 168, y: 22, w: 1584, h: 891 };
/** 截图视口坐标 → 窗口内坐标 */
export function project(p: { x: number; y: number }, cam: Cam, rect: Rect = WIN) {
  const k = (rect.w / VW) * cam.z;
  return { x: rect.w / 2 + (p.x - cam.x) * k, y: rect.h / 2 + (p.y - cam.y) * k, k };
}
export const projBox = (b: Box, cam: Cam, rect: Rect = WIN) => {
  const p = project(b, cam, rect);
  return { x: p.x, y: p.y, w: b.w * p.k, h: b.h * p.k };
};

/** 一张截图按镜头摆进窗口；截图里藏起来的导师在原位动起来（acts 按谁覆盖动作序列） */
export const Shot: React.FC<{ name: string; cam: Cam; opacity?: number; rect?: Rect; acts?: Record<string, string[]>; actFrom?: number }> =
  ({ name, cam, opacity = 1, rect = WIN, acts = {}, actFrom = 0 }) => {
    if (opacity <= 0.001) return null;
    const m = SHOTS[name];
    if (!m) throw new Error("没有截图 " + name);
    const k = (rect.w / VW) * cam.z;
    return (
      <div style={{ position: "absolute", inset: 0, opacity }}>
        <Img src={staticFile(`shots/${m.file}`)} style={{ position: "absolute", left: 0, top: 0, width: m.w, height: m.h,
          transformOrigin: "0 0", transform: `translate(${rect.w / 2 - cam.x * k}px, ${rect.h / 2 - cam.y * k}px) scale(${k})` }} />
        {m.sprites.map((s, i) => {
          const p = project(s, cam, rect);
          const seq = acts[s.who] ?? (s.action === "wave" ? ["wave", "idle"] : s.action === "jump_start" ? ["jump_start", "jump_air", "jump_land", "idle"] : [s.action]);
          return <Sprite key={i} who={s.who} seq={seq} from={actFrom} x={p.x} y={p.y} scale={spriteScale(s.who, s.w) * p.k} flip={s.flip} />;
        })}
      </div>
    );
  };

/** 应用窗口：游戏的像素边框；enter 0→1 时一格一格放大出现 */
export const AppWindow: React.FC<{ enter?: number; exit?: number; rect?: Rect; children: React.ReactNode }> = ({ enter = 1, exit = 0, rect = WIN, children }) => {
  const t = steps(clamp01(enter), 5), x = steps(clamp01(exit), 5);
  if (t <= 0 || x >= 1) return null;
  const sc = lerp(0.9, 1, t) * lerp(1, 0.9, x);
  return (
    <div style={{ position: "absolute", left: rect.x, top: rect.y, width: rect.w, height: rect.h, opacity: Math.min(t, 1 - x), transform: `scale(${sc})`,
      boxShadow: frame(6, C.rim, C.rimDeep, "0 36px 0 6px rgba(0,0,0,0.35)"), background: C.bg }}>
      <div style={{ position: "absolute", inset: 0, overflow: "hidden" }}>{children}</div>
    </div>
  );
};

// ── 像素鼠标 ─────────────────────────────────────────
const ARROW = ["X..........", "XX.........", "XWX........", "XWWX.......", "XWWWX......", "XWWWWX.....", "XWWWWWX....", "XWWWWWWX...", "XWWWWWWWX..",
  "XWWWWWWWWX.", "XWWWWWXXXXX", "XWWXWWX....", "XWX.XWWX...", "XX..XWWX...", "X....XWWX..", ".....XWWX..", "......XX..."];
const ArrowSvg: React.FC<{ s: number }> = ({ s }) => (
  <svg width={11 * s} height={17 * s} shapeRendering="crispEdges">
    {ARROW.flatMap((row, y) => [...row].map((c, x) => c === "." ? null : <rect key={`${x},${y}`} x={x * s} y={y * s} width={s} height={s} fill={c === "X" ? "#1f1d33" : "#ffffff"} />))}
  </svg>
);
/** 鼠标：path = [[帧, 视口坐标], ...]；clicks = 点击帧（按下缩一下 + 一圈方框一格一格扩开）。放在 AppWindow 里面，坐标相对窗口 */
export const Cursor: React.FC<{ path: [number, { x: number; y: number }][]; cam: Cam; clicks?: number[]; show: [number, number]; rect?: Rect }> = ({ path, cam, clicks = [], show, rect = WIN }) => {
  const f = useCurrentFrame();
  if (f < show[0] || f > show[1]) return null;
  let p = path[0][1];
  for (let i = 1; i < path.length; i++) {
    const [f0, a] = path[i - 1], [f1, b] = path[i];
    if (f >= f0) {
      const t = ease(clamp01((f - f0) / Math.max(1, f1 - f0)));
      p = { x: lerp(a.x, b.x, t), y: lerp(a.y, b.y, t) };
    }
  }
  const s = project(p, cam, rect);
  const down = clicks.some((c) => f >= c - 1 && f < c + 3);
  return (
    <>
      {clicks.filter((c) => f >= c && f < c + 12).map((c) => {
        const r = 18 + 14 * Math.floor((f - c) / 3);
        return <div key={c} style={{ position: "absolute", left: s.x - r, top: s.y - r, width: 2 * r, height: 2 * r, boxSizing: "border-box",
          border: `6px solid rgba(255,244,194,${1 - (f - c) / 12})` }} />;
      })}
      <div style={{ position: "absolute", left: s.x - 3, top: s.y - 3 + (down ? 3 : 0), filter: "drop-shadow(6px 6px 0 rgba(0,0,0,0.45))" }}><ArrowSvg s={4} /></div>
    </>
  );
};

/** 截图上某个框的像素描边（窗口内坐标）：硬边框，一亮一暗地闪两下 */
export const Glow: React.FC<{ box: Box; cam: Cam; color: string; o: number; pad?: number; rect?: Rect; at?: number }> = ({ box, cam, color, o, pad = 6, rect = WIN, at }) => {
  const f = useCurrentFrame();
  if (o <= 0.001) return null;
  const b = projBox(box, cam, rect);
  const blink = at !== undefined && f >= at && f < at + 12 && Math.floor((f - at) / 3) % 2 === 1 ? 0.35 : 1;
  return <div style={{ position: "absolute", left: b.x - pad, top: b.y - pad, width: b.w + pad * 2, height: b.h + pad * 2, opacity: o * blink, boxSizing: "border-box",
    border: `6px solid ${color}`, boxShadow: `6px 6px 0 rgba(0,0,0,0.45), inset 0 0 0 9999px ${color}14` }} />;
};

/** 标注：像素框的小牌子，弹出时一格一格放大 */
export const Tag: React.FC<{ x: number; y: number; at: number; color: string; text: React.ReactNode; size?: number; out?: number; anchor?: "left" | "right" | "center"; icon?: string }> =
  ({ x, y, at, color, text, size = 36, out, anchor = "left", icon }) => {
    const f = useCurrentFrame();
    const t = steps(tw(f, at, 0.2), 4);
    const o = out === undefined ? t : Math.min(t, 1 - steps(tw(f, out, 0.15), 3));
    if (o <= 0.001) return null;
    const tx = anchor === "right" ? "-100%" : anchor === "center" ? "-50%" : "0";
    return (
      <div style={{ position: "absolute", left: x, top: y, opacity: o, transform: `translate(${tx}, -50%) scale(${lerp(0.6, 1, t)})`, transformOrigin: "center",
        display: "flex", alignItems: "center", gap: 14, padding: `6px ${size * 0.5}px`, whiteSpace: "nowrap", background: C.panel,
        boxShadow: frame(6, color, "rgba(0,0,0,0.5)"), fontFamily: PX, fontSize: size, lineHeight: `${size * 1.34}px`, color: C.ink }}>
        {icon && <span style={{ color }}>{icon}</span>}
        <span>{text}</span>
      </div>
    );
  };

/** 逐字打出（游戏开场的打字机）：rate = 每帧几个字；blip = 每几个字一声 */
export const TypeText: React.FC<{ text: string; at: number; rate?: number; style?: React.CSSProperties; caret?: boolean }> = ({ text, at, rate = 1, style, caret = false }) => {
  const f = useCurrentFrame();
  const n = Math.max(0, Math.min(text.length, Math.floor((f - at) * rate)));
  if (f < at) return null;
  return <span style={{ whiteSpace: "pre-wrap", ...style }}>{text.slice(0, n)}{caret && n < text.length && Math.floor(f / 6) % 2 === 0 ? "▌" : ""}</span>;
};
/** 打字机的音效：每 every 个字一声 blip（游戏 Intro.jsx 是每 3 个字） */
export const TypeBlips: React.FC<{ text: string; at: number; rate?: number; every?: number; v?: number }> = ({ text, at, rate = 1, every = 3, v = 0.2 }) => (
  <>{Array.from({ length: Math.ceil(text.length / every) }, (_, i) => <Sfx key={i} at={at + (i * every) / rate} name="blip" v={v} />)}</>
);

/** 大数字：从 0 数到 n */
export const Counter: React.FC<{ n: number; at: number; dur?: number; style?: React.CSSProperties }> = ({ n, at, dur = 0.8, style }) => {
  const f = useCurrentFrame();
  const v = Math.round(n * tw(f, at, dur, 0, 1));
  return <span style={{ fontVariantNumeric: "tabular-nums", ...style }}>{v}</span>;
};

/** 像素溶解转场：at 帧前 dur 秒里方格（有序抖动的次序）一块块盖住画面，at 帧后再一块块揭开 */
const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
export const Wipe: React.FC<{ at: number; dur?: number; color?: string; cell?: number }> = ({ at, dur = 0.4, color = C.night, cell = 60 }) => {
  const f = useCurrentFrame();
  const d = dur * FPS;
  if (f < at - d || f > at + d) return null;
  const p = f < at ? (f - (at - d)) / d : 1 - (f - at) / d;
  const cols = Math.ceil(W / cell), rows = Math.ceil(H / cell);
  const rects: string[] = [];
  for (let y = 0; y < rows; y++) for (let x = 0; x < cols; x++) {
    const th = (BAYER[(y % 4) * 4 + (x % 4)] / 16) * 0.55 + ((x + y) / (cols + rows)) * 0.45;
    if (th < p) rects.push(`M${x * cell} ${y * cell}h${cell}v${cell}h-${cell}z`);
  }
  return <svg width={W} height={H} style={{ position: "absolute", left: 0, top: 0 }} shapeRendering="crispEdges"><path d={rects.join("")} fill={color} /></svg>;
};

/** 像素彩带：方块从 (x, y) 炸开往下落，一格一格转（canvas-confetti 的像素版；游戏开了“减少动画”时截图里没有彩带） */
export const Confetti: React.FC<{ at: number; x: number; y: number; n?: number }> = ({ at, x, y, n = 70 }) => {
  const f = useCurrentFrame();
  const t = (f - at) / FPS;
  if (t < 0 || t > 3) return null;
  const cols = [C.gold, C.accent, C.good, C.bad, "#f08cc0", "#ffffff"];
  return <>{Array.from({ length: n }, (_, i) => {
    const a = -Math.PI / 2 + (rnd("ca" + i) - 0.5) * 2.2, v = 700 + 700 * rnd("cv" + i);
    const px = x + Math.cos(a) * v * t, py = y + Math.sin(a) * v * t + 900 * t * t;
    const s = rnd("cs" + i) < 0.5 ? 12 : 18, spin = Math.floor(f / 4 + i) % 2;
    return <div key={i} style={{ position: "absolute", left: Math.round(px / 6) * 6, top: Math.round(py / 6) * 6, width: spin ? s : s / 2, height: spin ? s / 2 : s,
      background: cols[i % cols.length], opacity: t > 2.4 ? (3 - t) / 0.6 : 1 }} />;
  })}</>;
};

/** 一句大字（像素字，带一道硬阴影） */
export const big = (size: number, color: string = C.ink): React.CSSProperties => ({
  fontFamily: PX, fontSize: size, lineHeight: 1.25, color, textShadow: `${size / 12}px ${size / 12}px 0 rgba(0,0,0,0.55)`, whiteSpace: "nowrap",
});
