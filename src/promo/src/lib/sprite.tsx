// 导师精灵：和游戏 src/game/ui/cast.jsx 同一套摆法——同一个角色的所有动作画在同一个“舞台”上，
// 脚踩同一点，换动作脚不挪。区别是帧号按视频帧算（不靠浏览器动画），渲染可复现。
// seq = 依次播放的动作：前面的各放一遍，最后一个循环（循环动作）或停在最后一格。
import React from "react";
import { staticFile, useCurrentFrame } from "remotion";
import metaJson from "../../public/cast/sprites.json";
import { FPS } from "./core";

type Act = { file: string; w: number; h: number; frames: number; fps: number; loop: boolean; foot: [number, number] };
export type Who = "black" | "blue";
const META = (metaJson as unknown as { packs: Record<Who, Record<string, Act>> }).packs;
export const STAGE = Object.fromEntries(Object.entries(META).map(([who, acts]) => {
  const list = Object.values(acts);
  return [who, { w: 2 * Math.max(...list.map((a) => Math.max(a.foot[0], a.w - a.foot[0]))), h: Math.max(...list.map((a) => a.foot[1])) }];
})) as Record<Who, { w: number; h: number }>;

/** 动作序列 seq 开始后第 t 帧（视频帧）播到哪个动作的第几格 */
function frameOf(who: Who, seq: string[], t: number) {
  let left = t;
  for (let i = 0; i < seq.length; i++) {
    const a = META[who][seq[i]] ?? META[who].idle;
    const n = Math.floor((left * a.fps) / FPS);
    if (i === seq.length - 1) return { a, k: a.loop ? n % a.frames : Math.min(n, a.frames - 1) };
    if (n < a.frames) return { a, k: n };
    left -= Math.ceil((a.frames * FPS) / a.fps);
  }
  return { a: META[who].idle, k: 0 };
}
/** 一个动作放一遍要多少视频帧 */
export const actLen = (who: Who, act: string) => Math.ceil((META[who][act].frames * FPS) / META[who][act].fps);

/** 一个导师：footX, footY = 脚踩的点（屏幕 px），scale = 一个精灵像素放大几倍 */
export const Sprite: React.FC<{ who: Who; seq: string[]; from?: number; footX: number; footY: number; scale: number; flip?: boolean; style?: React.CSSProperties }> =
  ({ who, seq, from = 0, footX, footY, scale, flip = false, style }) => {
    const f = useCurrentFrame();
    const st = STAGE[who];
    const { a, k } = frameOf(who, seq, Math.max(0, f - from));
    return (
      <div style={{ position: "absolute", left: footX - (st.w / 2) * scale, top: footY - st.h * scale, width: st.w * scale, height: st.h * scale, pointerEvents: "none", ...style }}>
        <div style={{
          position: "absolute", width: a.w * scale, height: a.h * scale, left: (st.w / 2 - a.foot[0]) * scale, top: (st.h - a.foot[1]) * scale,
          backgroundImage: `url(${staticFile("cast/" + a.file)})`, backgroundSize: `${a.w * a.frames * scale}px ${a.h * scale}px`,
          backgroundPosition: `${-k * a.w * scale}px 0`, imageRendering: "pixelated",
          transform: flip ? "scaleX(-1)" : undefined, transformOrigin: `${a.foot[0] * scale}px 0`,
        }} />
      </div>
    );
  };
