// 导师精灵：和游戏的 src/game/ui/cast.jsx 同一套摆法（同一个“舞台”里脚踩同一点，动作换了脚不挪），
// 只是帧号按视频的帧算，不靠浏览器动画：第 f 帧放动画条（assets/cast/sprites/<谁>/<动作>.webp）的第几格由 fps 定。
// seq = 依次播放的动作，前面的各放一遍，最后一个循环（循环动作）或停在最后一格。
import React from "react";
import { staticFile, useCurrentFrame } from "remotion";
import metaJson from "../../public/cast/sprites.json";
import { FPS } from "./core";

type Act = { file: string; w: number; h: number; frames: number; fps: number; loop: boolean; foot: [number, number] };
const META = (metaJson as unknown as { packs: Record<string, Record<string, Act>> }).packs;
export const STAGE = Object.fromEntries(Object.entries(META).map(([who, acts]) => {
  const list = Object.values(acts);
  return [who, { w: 2 * Math.max(...list.map((a) => Math.max(a.foot[0], a.w - a.foot[0]))), h: Math.max(...list.map((a) => a.foot[1])) }];
})) as Record<string, { w: number; h: number }>;

/** f 帧（相对 from）时在播哪个动作的第几格 */
function frameOf(who: string, seq: string[], t: number) {
  let left = t;
  for (let i = 0; i < seq.length; i++) {
    const a = META[who][seq[i]] ?? META[who].idle;
    const n = Math.floor((left * a.fps) / FPS);
    const last = i === seq.length - 1;
    if (last) return { a, k: a.loop ? n % a.frames : Math.min(n, a.frames - 1) };
    if (n < a.frames) return { a, k: n };
    left -= Math.ceil((a.frames * FPS) / a.fps);
  }
  const a = META[who].idle;
  return { a, k: 0 };
}

/** 一个导师。x, y = 舞台左上角（屏幕 px），scale = 一个精灵像素放大几倍 */
export const Sprite: React.FC<{ who: string; seq: string[]; from?: number; x: number; y: number; scale: number; flip?: boolean; opacity?: number }> =
  ({ who, seq, from = 0, x, y, scale, flip = false, opacity = 1 }) => {
    const f = useCurrentFrame();
    if (opacity <= 0.001) return null;
    const st = STAGE[who];
    const { a, k } = frameOf(who, seq, Math.max(0, f - from));
    return (
      <div style={{ position: "absolute", left: x, top: y, width: st.w * scale, height: st.h * scale, opacity, pointerEvents: "none" }}>
        <div style={{ position: "absolute", width: a.w * scale, height: a.h * scale, left: (st.w / 2 - a.foot[0]) * scale, top: (st.h - a.foot[1]) * scale,
          backgroundImage: `url(${staticFile("cast/" + a.file)})`, backgroundSize: `${a.w * a.frames * scale}px ${a.h * scale}px`,
          backgroundPosition: `${-k * a.w * scale}px 0`, imageRendering: "pixelated",
          transform: flip ? "scaleX(-1)" : undefined, transformOrigin: `${a.foot[0] * scale}px 0` }} />
      </div>
    );
  };

/** 截图里记下的精灵：放回原位（舞台框按镜头换算），scale 由舞台宽度反推 */
export const spriteScale = (who: string, stageW: number) => stageW / STAGE[who].w;
