// 背后的技能树：地图（183 个技能）→ 技能页里一章的“去哪深入”（教材哪几章）→ 必须先学（理由）和课程证据（大学官网先修原文）。
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { C, F, beat, box, steps, tw, w } from "../lib/core";
import { AppWindow, CAM0, Glow, Sfx, Shot, Tag, Counter, camAt, project, big } from "../lib/ui";

export const Tree: React.FC = () => {
  const f = useCurrentFrame();
  const A = beat("tree").start, Z = beat("check").start;
  if (f < A - 12 || f > Z + 12) return null;
  const tN = w("tree", "一百八十三"), tCh = w("tree", "每一章"), tBook = w("tree", "教材"), tNeed = w("tree", "要先学什么"), tUni = w("tree", "大学课程");
  const shot = f < tCh - 2 ? "map" : f < tNeed - 2 ? "skill-deep" : "skill-evidence";
  const cam = camAt(f, [
    [A, { x: 608, y: 380, z: 1.25 }], [tCh - 3, { x: 608, y: 342, z: 1.0 }], [tCh - 2, { x: 608, y: 342, z: 1.0 }], [tBook, { x: 608, y: 330, z: 1.12 }],
    [tNeed - 3, { x: 608, y: 330, z: 1.12 }], [tNeed - 2, { x: 600, y: 380, z: 1.0 }], [Z, { x: 600, y: 340, z: 1.04 }],
  ]);
  const p = project({ x: 608, y: 300 }, CAM0);
  return (
    <AbsoluteFill>
      <AppWindow enter={tw(f, A - 8, 0.3)} exit={tw(f, Z - 6, 0.3)}>
        <Shot name={shot} cam={cam} actFrom={A} />
        {shot === "map" && <div style={{ position: "absolute", left: p.x, top: p.y, transform: "translate(-50%, -50%)", textAlign: "center", opacity: steps(tw(f, tN - 4, 0.2), 3),
          background: "rgba(20,20,43,0.86)", padding: "18px 46px", boxShadow: `0 -6px 0 0 ${C.gold}, 0 6px 0 0 ${C.gold}, -6px 0 0 0 ${C.gold}, 6px 0 0 0 ${C.gold}, 0 18px 0 0 rgba(0,0,0,0.5)` }}>
          <div style={{ ...big(120, C.gold) }}><Counter n={F.skills} at={tN - 6} dur={0.5} /> 个技能</div>
          <div style={{ ...big(36, C.ink2) }}>{F.required} 条“必须先学”，没点亮不能学下一个</div>
        </div>}
        {shot === "skill-deep" && <>
          <Glow box={box("skill-deep", "ch")} cam={cam} color={C.accent} o={1} pad={4} at={tCh - 2} />
          <Glow box={box("skill-deep", "books")} cam={cam} color={C.gold} o={steps(tw(f, tBook - 3, 0.15), 3)} pad={6} at={tBook - 3} />
          {(() => { const q = project({ x: 1060, y: 250 }, cam); return <Tag x={q.x} y={q.y} at={tBook} color={C.gold} text="去哪本教材的哪几章深入" anchor="right" />; })()}
        </>}
        {shot === "skill-evidence" && <>
          <Glow box={box("skill-evidence", "need")} cam={cam} color={C.accent} o={1} pad={4} at={tNeed - 2} />
          <Glow box={box("skill-evidence", "proof")} cam={cam} color={C.gold} o={steps(tw(f, tUni - 3, 0.15), 3)} pad={4} at={tUni - 3} />
          {(() => { const q = project({ x: 367, y: 120 }, cam); return <Tag x={q.x} y={q.y} at={tNeed} color={C.accent} text="要先学什么、为什么" anchor="center" size={32} />; })()}
          {(() => { const q = project({ x: 849, y: 120 }, cam); return <Tag x={q.x} y={q.y} at={tUni} color={C.gold} text="大学官网的先修原文" anchor="center" size={32} />; })()}
        </>}
      </AppWindow>
      <Sfx at={tN} name="star" v={0.3} />
      <Sfx at={tCh - 2} name="page" v={0.3} />
      <Sfx at={tNeed - 2} name="page" v={0.3} />
    </AbsoluteFill>
  );
};
