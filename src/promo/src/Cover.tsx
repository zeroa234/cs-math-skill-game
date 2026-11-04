// 封面（静帧）：像素 3D 塔的片尾一帧（整条路已点亮的金色）做底，左边像素大字标题，右边鲸鱼娘姐妹的半身立绘。
// 四种尺寸和“竖版内容只放中间 3:4”的规矩同 cs-math-skill-tree / os-review-bilingual 的封面（B 站 / 抖音的封面位）。
// 背景帧由 scripts/promo/cover.mjs 从 Blender 的 PNG 帧复制到 public/blender/cover-bg.png（640×360，整数倍最近邻放大）。
import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { C, F, PX } from "./lib/core";
import { frame } from "./lib/ui";

// 立绘（assets/cast/portraits，透明底、已裁紧）：原图尺寸，取头顶到腰
const ART = { black: { w: 593, h: 1200 }, blue: { w: 664, h: 1200 } };
const WAIST = 0.46;

const Half: React.FC<{ who: "black" | "blue"; h: number; x: number; y: number; flip?: boolean }> = ({ who, h, x, y, flip }) => {
  const a = ART[who], full = h / WAIST, w = (a.w * full) / a.h;
  return (
    <div style={{ position: "absolute", left: x, top: y, width: w, height: h, overflow: "hidden" }}>
      <Img src={staticFile(`cast/portraits/${who}.webp`)} style={{ width: w, height: full, transform: flip ? "scaleX(-1)" : undefined,
        filter: `drop-shadow(0 0 ${h / 40}px ${who === "blue" ? "#6f8fff" : "#b9a6ff"}) drop-shadow(0 0 ${h / 18}px rgba(113,135,255,0.55))` }} />
    </div>
  );
};

export const Cover: React.FC<{ w: number; h: number }> = ({ w, h }) => {
  const portrait = h > w;
  const safeH = portrait ? Math.min(h, (w * 4) / 3) : h;   // 9:16 只用中间 3:4
  const top = (h - safeH) / 2;
  const u = Math.min(w, safeH) / 1080;
  // 背景：640×360 像素帧放大到整数倍、盖满画面，塔靠右（竖版靠下）
  const k = Math.ceil(Math.max(w / 640, h / 360));
  const bw = 640 * k, bh = 360 * k;
  const bx = portrait ? w - bw * 0.78 : w - bw, by = portrait ? h - bh : (h - bh) / 2;
  const title = Math.round((portrait ? 168 : 192) * u / 12) * 12;      // 像素字的整数倍
  const sub = Math.round(48 * u / 12) * 12, small = Math.round(36 * u / 12) * 12;
  const herH = (portrait ? 0.46 : 0.6) * safeH;
  // 半身的宽 = 原图宽高比 × 整身高（herH / WAIST）
  const bw0 = (ART.black.w / ART.black.h / WAIST) * herH, bw1 = (ART.blue.w / ART.blue.h / WAIST) * herH;
  return (
    <AbsoluteFill style={{ background: C.night }}>
      <Img src={staticFile("blender/cover-bg.png")} style={{ position: "absolute", left: bx, top: by, width: bw, height: bh, imageRendering: "pixelated" }} />
      <AbsoluteFill style={{ background: portrait
        ? "linear-gradient(180deg, rgba(14,13,36,0.88) 0%, rgba(14,13,36,0.55) 40%, rgba(14,13,36,0.05) 62%)"
        : "linear-gradient(90deg, rgba(14,13,36,0.9) 0%, rgba(14,13,36,0.6) 38%, transparent 60%)" }} />
      {/* 姐妹：右边（竖版右下），妹妹在后 */}
      <Half who="black" h={herH} x={portrait ? -0.04 * w : w - bw0 - bw1 * 0.55} y={h - herH} />
      <Half who="blue" h={herH * 1.02} x={portrait ? w - bw1 * 1.02 + 0.04 * w : w - bw1 * 1.02 + 0.05 * w} y={h - herH * 1.02} />
      <div style={{ position: "absolute", left: 90 * u, top: top + (portrait ? 110 * u : safeH * 0.2), fontFamily: PX }}>
        <div style={{ display: "inline-block", fontSize: small, lineHeight: `${small * 1.4}px`, color: C.ink, padding: `${6 * u}px ${18 * u}px`, background: C.panel,
          boxShadow: frame(Math.max(3, Math.round(6 * u)), C.accent, "rgba(0,0,0,0.5)") }}>像素风学习游戏 · 安卓 / 网页</div>
        <div style={{ fontSize: sub, lineHeight: 1.3, color: C.ink, marginTop: 40 * u, textShadow: `${sub / 12}px ${sub / 12}px 0 #000`, whiteSpace: "nowrap" }}>我把计算机专业做成了一款游戏</div>
        <div style={{ fontSize: title, lineHeight: 1.2, color: C.gold, marginTop: 12 * u, textShadow: `${title / 12}px ${title / 12}px 0 #1a1003`, whiteSpace: "nowrap" }}>点亮之路</div>
        <div style={{ fontSize: small, lineHeight: 1.4, color: C.ink2, marginTop: 18 * u, textShadow: `${small / 12}px ${small / 12}px 0 #000`, whiteSpace: "nowrap" }}>
          {F.route.stops.length} 站 {F.lessons} 课 · {F.sims.length} 种互动实验 · {F.skills} 个技能
        </div>
      </div>
    </AbsoluteFill>
  );
};
