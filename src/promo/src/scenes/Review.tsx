// 复习：左边是一道题的“还记得的概率”曲线，右边是游戏的复习页。曲线不是画的示意图：
// scripts/promo/build-facts.mjs 用游戏自己的 src/game/core/review.js（ts-fsrs，目标记住率 90%）给一道题排期、每次到期都答对，
// 记下每次复习的日子和中间的回忆概率；横轴按天数开方（间隔从几天长到一年多，开方后都看得见）。
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { C, F, PX, beat, clamp01, steps, tw, w } from "../lib/core";
import { AppWindow, Cam, Sfx, Shot, Tag, big, frame } from "../lib/ui";

const CH = { x: 120, y: 230, w: 900, h: 520 };
const RECT = { x: 1070, y: 230, w: 800, h: 450 };

export const Review: React.FC = () => {
  const f = useCurrentFrame();
  const A = beat("review").start, Z = beat("tree").start;
  if (f < A - 10 || f > Z + 12) return null;
  const out = 1 - steps(tw(f, Z - 8, 0.25), 3);
  const tDraw = w("review", "记忆规律"), tForget = w("review", "快忘"), tBack = w("review", "回来找你复习");
  const curve = F.fsrs.curve, reviews = F.fsrs.reviews.map((r) => r.day);
  const maxD = curve.at(-1)![0];
  const X = (d: number) => CH.x + (Math.sqrt(d) / Math.sqrt(maxD)) * CH.w;
  const Y = (r: number) => CH.y + 24 + ((1 - r) / 0.15) * (CH.h - 24);       // 纵轴 85%–100%
  const drawn = clamp01((f - tDraw + 6) / (tBack - tDraw + 10));
  const n = Math.floor(drawn * curve.length);
  // 像素线：每隔 6 px 一个方点
  const dots: [number, number][] = [];
  for (let i = 1; i < n; i++) {
    const [d0, r0] = curve[i - 1], [d1, r1] = curve[i];
    const x0 = X(d0), y0 = Y(r0), x1 = X(d1), y1 = Y(r1);
    const len = Math.max(1, Math.hypot(x1 - x0, y1 - y0) / 6);
    for (let s = 0; s < len; s++) dots.push([Math.round((x0 + ((x1 - x0) * s) / len) / 6) * 6, Math.round((y0 + ((y1 - y0) * s) / len) / 6) * 6]);
  }
  const shownReviews = reviews.filter((d) => curve.findIndex((c) => c[0] >= d) <= n);
  const cam: Cam = { x: 700, y: 250, z: 1.3 };
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <div style={{ position: "absolute", left: CH.x, top: 96, opacity: steps(tw(f, A, 0.2), 3) }}>
        <span style={{ ...big(64, C.ink) }}>间隔复习</span>
        <span style={{ ...big(36, C.ink2), marginLeft: 26 }}>同一道题，每次到期都答对</span>
      </div>
      {/* 坐标框 */}
      <div style={{ position: "absolute", left: CH.x - 12, top: CH.y - 20, width: CH.w + 40, height: CH.h + 40, background: "rgba(20,20,43,0.85)", boxShadow: frame(6, C.rim, C.rimDeep), opacity: steps(tw(f, A + 2, 0.2), 3) }} />
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }} shapeRendering="crispEdges">
        {/* 90% 线：快忘了 */}
        {Array.from({ length: Math.floor(CH.w / 24) }, (_, i) => <rect key={i} x={CH.x + i * 24} y={Math.round(Y(F.fsrs.retention) / 6) * 6} width={12} height={6}
          fill={f >= tForget - 2 && f < tForget + 14 && Math.floor((f - tForget) / 3) % 2 === 0 ? C.bad : "#8a4a5a"} />)}
        {dots.map(([x, y], i) => <rect key={i} x={x} y={y} width={6} height={6} fill={C.gold} />)}
        {shownReviews.map((d, i) => <rect key={"r" + i} x={Math.round(X(d) / 6) * 6 - 9} y={Math.round(Y(1) / 6) * 6 - 9} width={24} height={24} fill={i === 0 ? C.accent : C.good} />)}
      </svg>
      <div style={{ position: "absolute", left: CH.x + 10, top: CH.y + CH.h - 56, fontFamily: PX, fontSize: 30, lineHeight: "40px", color: C.bad, opacity: steps(tw(f, tForget - 4, 0.15), 3) }}>
        快忘了（还记得的概率降到 {Math.round(F.fsrs.retention * 100)}%）→ 回来复习
      </div>
      {shownReviews.map((d, i) => (
        <div key={i} style={{ position: "absolute", left: X(d) + (i === 0 ? -6 : 0), top: i === 0 ? Y(1) - 58 : Y(F.fsrs.retention) + 14, transform: i === 0 ? "none" : "translateX(-50%)", fontFamily: PX, fontSize: 30, lineHeight: "40px", color: i === 0 ? C.accentStrong : C.good, whiteSpace: "nowrap" }}>
          {i === 0 ? "学会" : `第 ${Math.round(d)} 天`}
        </div>
      ))}
      <div style={{ position: "absolute", left: CH.x, top: CH.y + CH.h + 36, fontFamily: PX, fontSize: 24, lineHeight: "32px", color: C.muted }}>
        排期：游戏里的 FSRS（ts-fsrs），目标记住率 {Math.round(F.fsrs.retention * 100)}%；横轴按天数开方
      </div>
      {/* 游戏里的复习页 */}
      <AppWindow rect={RECT} enter={tw(f, A + 6, 0.3)}>
        <Shot name="review" cam={cam} rect={RECT} actFrom={A} acts={{ black: ["idle"] }} />
      </AppWindow>
      <Tag x={RECT.x + RECT.w / 2} y={RECT.y + RECT.h + 70} at={tBack} color={C.accent} text="复习 · 跨技能混在一起" anchor="center" />
      {shownReviews.map((d, i) => <Sfx key={i} at={tDraw - 6 + Math.round((curve.findIndex((c) => c[0] >= d) / curve.length) * (tBack - tDraw + 10))} name={i ? "correct" : "select"} v={0.25} />)}
    </AbsoluteFill>
  );
};
