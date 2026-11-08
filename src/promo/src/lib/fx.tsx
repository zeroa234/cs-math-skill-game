// 动效小件：像素图标、像素边框、弹入、闪白、震屏、星空、像素粒子、音效。都按帧算，渲染可复现。
import React from "react";
import { Audio, Sequence, random, staticFile, useCurrentFrame } from "remotion";
import iconsJson from "../../public/build/icons.json";
import { H, W, clamp01, easeOutBack, easeOutCubic } from "./core";

const ICONS = iconsJson as Record<string, string[]>;

/** 游戏同款像素图标（pixelarticons，24 格），size 取 24 的整数倍才不糊 */
export const PixelIcon: React.FC<{ name: string; size: number; color: string; style?: React.CSSProperties }> = ({ name, size, color, style }) => (
  <svg viewBox="0 0 24 24" width={size} height={size} fill={color} shapeRendering="crispEdges" style={style}>
    {(ICONS[name] ?? []).map((d, i) => <path key={i} d={d} />)}
  </svg>
);

/** 游戏的像素边框：方框、四角各缺一个像素、底下一道硬“厚度”边。px = 一个像素多大 */
export const PixelFrame: React.FC<{ px: number; rim: string; deep: string; fill: string; style?: React.CSSProperties; children?: React.ReactNode }> =
  ({ px, rim, deep, fill, style, children }) => (
    <div style={{
      position: "relative", background: fill, border: `${px}px solid ${rim}`, borderBottomWidth: px * 2, borderBottomColor: deep,
      clipPath: `polygon(${px}px 0, calc(100% - ${px}px) 0, calc(100% - ${px}px) ${px}px, 100% ${px}px, 100% calc(100% - ${px}px), calc(100% - ${px}px) calc(100% - ${px}px), calc(100% - ${px}px) 100%, ${px}px 100%, ${px}px calc(100% - ${px}px), 0 calc(100% - ${px}px), 0 ${px}px, ${px}px ${px}px)`,
      ...style,
    }}>{children}</div>
  );

/** 从 at 帧起 len 帧内从 from 倍弹到 1 倍（略过冲） */
export function punch(f: number, at: number, len = 6, from = 0.85) {
  const t = clamp01((f - at) / len);
  return from + (1 - from) * easeOutBack(t, 2.2);
}

/** 闪白：at 帧起 len 帧淡出 */
export const Flash: React.FC<{ at: number; len?: number; color?: string; max?: number }> = ({ at, len = 6, color = "#fff", max = 0.85 }) => {
  const f = useCurrentFrame();
  const t = (f - at) / len;
  if (t < 0 || t > 1) return null;
  return <div style={{ position: "absolute", inset: 0, background: color, opacity: max * (1 - t), pointerEvents: "none" }} />;
};

/** 震屏的位移：at 帧起 len 帧，幅度 amp 线性衰减（取整，像素不糊） */
export function shake(f: number, at: number, len = 8, amp = 14) {
  const t = (f - at) / len;
  if (t < 0 || t > 1) return { x: 0, y: 0 };
  const a = amp * (1 - t);
  return { x: Math.round((random(`sx${f}`) * 2 - 1) * a), y: Math.round((random(`sy${f}`) * 2 - 1) * a) };
}

/** 夜空：一片按种子摆好的像素星，各自明暗闪 */
export const Stars: React.FC<{ n?: number; seed?: string; opacity?: number; color?: string }> = ({ n = 140, seed = "s", opacity = 1, color = "#fff6d8" }) => {
  const f = useCurrentFrame();
  return (
    <div style={{ position: "absolute", inset: 0, opacity }}>
      {Array.from({ length: n }, (_, i) => {
        const x = random(`${seed}x${i}`) * W, y = random(`${seed}y${i}`) * H, big = random(`${seed}b${i}`) < 0.15;
        const tw = 0.45 + 0.55 * Math.abs(Math.sin(f / (18 + 30 * random(`${seed}p${i}`)) + i));
        const s = big ? 8 : 4;
        return <div key={i} style={{ position: "absolute", left: Math.round(x / 4) * 4, top: Math.round(y / 4) * 4, width: s, height: s, background: color, opacity: tw }} />;
      })}
    </div>
  );
};

/** 像素粒子炸开：at 帧从 (x, y) 向四周飞 n 个方块，len 帧消失 */
export const Burst: React.FC<{ at: number; x: number; y: number; n?: number; len?: number; colors: string[]; speed?: number; size?: number; seed?: string }> =
  ({ at, x, y, n = 18, len = 22, colors, speed = 520, size = 12, seed = "b" }) => {
    const f = useCurrentFrame();
    const t = (f - at) / len;
    if (t < 0 || t > 1) return null;
    const e = easeOutCubic(t);
    return (
      <>
        {Array.from({ length: n }, (_, i) => {
          const ang = (i / n) * Math.PI * 2 + random(`${seed}a${i}`) * 0.5;
          const sp = speed * (0.55 + 0.45 * random(`${seed}s${i}`));
          const px = x + Math.cos(ang) * sp * e, py = y + Math.sin(ang) * sp * e + 160 * t * t;
          return <div key={i} style={{ position: "absolute", left: Math.round(px / 4) * 4, top: Math.round(py / 4) * 4, width: size, height: size, background: colors[i % colors.length], opacity: 1 - t * t }} />;
        })}
      </>
    );
  };

/** 像素彩带：at 帧起从上往下飘 */
export const Confetti: React.FC<{ at: number; len?: number; n?: number; colors: string[]; seed?: string }> = ({ at, len = 70, n = 70, colors, seed = "c" }) => {
  const f = useCurrentFrame();
  const t = (f - at) / len;
  if (t < 0 || t > 1.2) return null;
  return (
    <>
      {Array.from({ length: n }, (_, i) => {
        const x0 = random(`${seed}x${i}`) * W, d = random(`${seed}d${i}`) * 0.35;
        const tt = Math.max(0, t - d);
        const y = -40 + tt * (H * 0.85 + 900 * random(`${seed}v${i}`));
        const x = x0 + Math.sin(tt * 9 + i) * 40;
        const w = random(`${seed}w${i}`) < 0.5 ? 12 : 8;
        return <div key={i} style={{ position: "absolute", left: Math.round(x / 4) * 4, top: Math.round(y / 4) * 4, width: w, height: 20 - w, background: colors[i % colors.length], opacity: tt > 0 ? 1 - clamp01((tt - 0.8) / 0.4) : 0 }} />;
      })}
    </>
  );
};

/** 一声音效：public/build/sfx/<name>.wav */
export const Sfx: React.FC<{ at: number; name: string; volume?: number }> = ({ at, name, volume = 0.8 }) => (
  <Sequence from={at} layout="none"><Audio src={staticFile(`build/sfx/${name}.wav`)} volume={volume} /></Sequence>
);
