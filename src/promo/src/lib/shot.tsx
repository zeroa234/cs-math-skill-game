// 游戏截图（scripts/promo/capture.mjs 截的真实画面）：只裁出要看的那块。
// crop 用截图里的 CSS px（shots.json 记的元素框也是 CSS px），width = 裁出的这块在屏幕上多宽。
import React from "react";
import { Img, staticFile } from "remotion";
import shotsJson from "../../public/build/shots/shots.json";

export type Box = { x: number; y: number; w: number; h: number };
type Meta = { file: string; w: number; h: number; dpr: number; clip: Box | null; targets: Record<string, Box[]>; sprites: unknown[] };
export const SHOTS = shotsJson as unknown as Record<string, Meta>;

/** 某张图里某个元素的框（CSS px，相对截图左上角；元素截图要减去元素自己的位置） */
export function target(name: string, key: string, i = 0): Box {
  const m = SHOTS[name];
  const b = m.targets[key][i];
  return m.clip ? { x: b.x - m.clip.x, y: b.y - m.clip.y, w: b.w, h: b.h } : b;
}
export const pad = (b: Box, p: number, q = p): Box => ({ x: b.x - p, y: b.y - q, w: b.w + 2 * p, h: b.h + 2 * q });

export const Shot: React.FC<{ name: string; crop?: Box; width: number; style?: React.CSSProperties }> = ({ name, crop, width, style }) => {
  const m = SHOTS[name];
  const c = crop ?? { x: 0, y: 0, w: m.w, h: m.h };
  const s = width / c.w;
  return (
    <div style={{ position: "relative", width, height: c.h * s, overflow: "hidden", ...style }}>
      <Img src={staticFile(`build/shots/${m.file}`)} style={{ position: "absolute", left: -c.x * s, top: -c.y * s, width: m.w * s, height: m.h * s, maxWidth: "none" }} />
    </div>
  );
};
