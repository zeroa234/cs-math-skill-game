// 结业挑战：说明（第一次就答对 80% 才点亮）→ 全部答对 → 点亮（导师施法、跳舞，像素彩带，号角音）→ “没有自评”。
// 点亮那张截图是真的在页面里按标准答案答完 15 道题得到的（capture-game.mjs 第 8 段）。
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { C, F, PX, beat, box, steps, tw, w } from "../lib/core";
import { AppWindow, CAM0, Confetti, Cursor, Glow, Sfx, Shot, Tag, camAt, frame, project } from "../lib/ui";

export const Boss: React.FC = () => {
  const f = useCurrentFrame();
  const A = beat("boss").start, Z = beat("review").start;
  if (f < A - 12 || f > Z + 12) return null;
  const tRule = w("boss", "八成"), tLit = w("boss", "点亮"), tTick = w("boss", "打勾");
  const clickStart = tLit - 12;
  const lit = f >= tLit;
  const cam = camAt(f, [[A, { x: 608, y: 300, z: 1.15 }], [clickStart, { x: 608, y: 300, z: 1.15 }], [tLit, CAM0]]);
  const sb = box("boss-brief", "start");
  return (
    <AbsoluteFill>
      <AppWindow enter={tw(f, A - 8, 0.3)} exit={tw(f, Z - 6, 0.3)}>
        <Shot name={lit ? "boss-lit" : "boss-brief"} cam={cam} actFrom={tLit} acts={{ black: ["cast", "idle"], blue: ["dance", "idle"] }} />
        {!lit && <Glow box={box("boss-brief", "rule")} cam={cam} color={C.gold} o={steps(tw(f, tRule - 4, 0.15), 3)} pad={4} at={tRule - 4} />}
        {!lit && (() => { const p = project({ x: 1060, y: 205 }, cam); return <Tag x={p.x} y={p.y} at={tRule} color={C.gold} text={`第一次就答对 ≥ ${Math.round(F.bossPass * 100)}%`} anchor="right" />; })()}
        <Cursor cam={cam} show={[A + 10, tLit - 2]} clicks={[clickStart]} path={[[A + 10, { x: 800, y: 500 }], [clickStart - 8, { x: sb.x + sb.w / 2, y: sb.y + sb.h / 2 }]]} />
        {lit && <Confetti at={tLit + 2} x={912} y={420} n={80} />}
        {lit && <Glow box={box("boss-lit", "mark")} cam={cam} color={C.gold} o={1} pad={10} at={tLit} />}
      </AppWindow>
      {/* 没有自评：一个“我学会了”的勾选框被打叉 */}
      <NoSelfTick at={tTick} out={Z - 6} />
      <Sfx at={clickStart} name="select" />
      <Sfx at={tLit} name="fanfare" v={0.45} />
      <Sfx at={tLit + 2} name="star" v={0.35} />
      <Sfx at={tTick + 6} name="locked" v={0.4} />
    </AbsoluteFill>
  );
};

const NoSelfTick: React.FC<{ at: number; out: number }> = ({ at, out }) => {
  const f = useCurrentFrame();
  const t = steps(tw(f, at - 4, 0.2), 3), x = steps(tw(f, at + 6, 0.15), 3), o = 1 - steps(tw(f, out - 4, 0.2), 3);
  if (t <= 0) return null;
  return (
    <div style={{ position: "absolute", left: 1220, top: 700, opacity: Math.min(t, o), display: "flex", alignItems: "center", gap: 24, padding: "18px 30px",
      background: C.panel, boxShadow: frame(6, C.bad, "rgba(0,0,0,0.5)") }}>
      <div style={{ position: "relative", width: 60, height: 60, boxShadow: frame(6, C.ink2, C.rimDeep), background: C.bg }}>
        {x > 0 && <svg width={60} height={60} style={{ position: "absolute", left: 0, top: 0 }} shapeRendering="crispEdges">
          {[0, 1, 2, 3, 4, 5, 6, 7, 8].map((i) => <React.Fragment key={i}><rect x={6 + i * 6} y={6 + i * 6} width={6} height={6} fill={C.bad} /><rect x={48 - i * 6} y={6 + i * 6} width={6} height={6} fill={C.bad} /></React.Fragment>)}
        </svg>}
      </div>
      <div style={{ fontFamily: PX, fontSize: 42, lineHeight: "54px", color: C.ink, textDecoration: x > 0 ? "line-through" : "none", textDecorationColor: C.bad, textDecorationThickness: 6 }}>我学会了</div>
      <div style={{ fontFamily: PX, fontSize: 30, lineHeight: "40px", color: C.bad, opacity: x }}>不能自己打勾</div>
    </div>
  );
};
