// 核对：终端里一行行跑出 tests/content/*.verify.py 的真实命令和最后一行输出（scripts/promo/verify-log.mjs 真跑一遍记下来的），
// 再合计“几处数值、输出、报错都对上”。顺序按远征的站。
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { C, F, MONO, PX, V, beat, steps, tw, w } from "../lib/core";
import { Counter, Sfx, TypeText, big, frame } from "../lib/ui";

export const Check: React.FC = () => {
  const f = useCurrentFrame();
  const A = beat("check").start, Z = beat("outro").start;
  if (f < A - 8 || f > Z + 12) return null;
  const order = F.route.stops.map((s) => V.runs.find((r) => r.id === s.id)!).filter(Boolean);
  const t0 = A + 8, gap = Math.round((w("check", "核对") - 8 - t0) / order.length);
  const out = 1 - steps(tw(f, Z - 8, 0.25), 3);
  const tTotal = w("check", "核对") - 2;
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <div style={{ position: "absolute", left: 160, top: 120, width: 1600, height: 640, background: "#0b0b1c", boxShadow: frame(6, C.rim, C.rimDeep, "0 36px 0 6px rgba(0,0,0,0.35)"),
        opacity: steps(tw(f, A - 6, 0.2), 3) }}>
        <div style={{ height: 54, background: C.panel2, display: "flex", alignItems: "center", gap: 14, paddingLeft: 24 }}>
          {[C.bad, C.gold, C.good].map((c) => <div key={c} style={{ width: 18, height: 18, background: c }} />)}
          <span style={{ fontFamily: PX, fontSize: 24, color: C.muted, marginLeft: 16 }}>cs-math-skill-game · 内容核对</span>
        </div>
        <div style={{ padding: "26px 40px", fontFamily: MONO, fontSize: 30, lineHeight: "50px" }}>
          {order.map((r, i) => {
            const a = t0 + i * gap;
            if (f < a) return null;
            return <div key={r.id} style={{ display: "flex", gap: 24, whiteSpace: "nowrap" }}>
              <span style={{ color: C.good }}>$</span>
              <span style={{ color: C.ink2, width: 860 }}><TypeText text={r.cmd} at={a} rate={4} /></span>
              {f >= a + 10 && <span style={{ color: C.good }}>✓ {r.last}</span>}
              {f >= a + 10 && <span style={{ fontFamily: PX, color: C.muted, fontSize: 24 }}>{r.name} · {r.tool}</span>}
            </div>;
          })}
        </div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 800, textAlign: "center", opacity: steps(tw(f, tTotal, 0.2), 3) }}>
        <span style={{ ...big(84, C.gold) }}><Counter n={V.total} at={tTotal} dur={0.6} /> 处数值、输出、报错，全部对上</span>
      </div>
      {order.map((r, i) => <Sfx key={r.id} at={t0 + i * gap + 10} name="correct" v={0.22} />)}
      <Sfx at={tTotal} name="star" v={0.35} />
    </AbsoluteFill>
  );
};
