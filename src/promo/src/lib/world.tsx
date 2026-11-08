// 两部片子共用的“游戏世界”画面件：像素背景、关卡点、PV 的字卡、技能树、像素大标题。
import React from "react";
import { AbsoluteFill, Img, staticFile, useCurrentFrame } from "remotion";
import treeJson from "../../public/build/tree.json";
import { DARK, FONT, H, W, clamp01, easeOutBack, easeOutCubic } from "./core";
import { PixelIcon } from "./fx";

/** 480×270 的像素场景放大 scale 倍铺满（竖屏只露出中间一段），pan = 左右平移 */
export const PixelBg: React.FC<{ src: string; dim?: number; pan?: number; y?: number; scale?: number }> = ({ src, dim = 0, pan = 0, y = 0, scale = 8 }) => (
  <AbsoluteFill style={{ overflow: "hidden" }}>
    <Img src={staticFile(`bg/${src}`)} style={{ position: "absolute", left: Math.round((W - 480 * scale) / 2 + pan), top: Math.round((H - 270 * scale) / 2 + y), width: 480 * scale, height: 270 * scale, maxWidth: "none", imageRendering: "pixelated" }} />
    {dim > 0 && <AbsoluteFill style={{ background: `rgba(8,8,24,${dim})` }} />}
  </AbsoluteFill>
);

/** 游戏关卡点的八角形（.lv 的样子） */
export const OCT = "polygon(30% 0,70% 0,70% 6%,85% 6%,85% 15%,94% 15%,94% 30%,100% 30%,100% 70%,94% 70%,94% 85%,85% 85%,85% 94%,70% 94%,70% 100%,30% 100%,30% 94%,15% 94%,15% 85%,6% 85%,6% 70%,0 70%,0 30%,6% 30%,6% 15%,15% 15%,15% 6%,30% 6%)";
export const Node: React.FC<{ x: number; y: number; size: number; lit: number; label?: string; press?: number }> = ({ x, y, size, lit, label, press = 0 }) => {
  const sq = 1 - 0.12 * press;
  const dim = { fill: "#2a2a4c", edge: "#1b1b3a", ink: "#7f7cab" }, on = { fill: DARK.gold, edge: DARK.goldEdge, ink: "#fff8de" };
  const c = lit > 0.5 ? on : dim;
  return (
    <div style={{ position: "absolute", left: x - size / 2, top: y - size / 2, width: size, height: size, transform: `scale(${1 / sq}, ${sq})`, transformOrigin: "50% 100%" }}>
      <div style={{ position: "absolute", inset: 0, top: size * 0.08, background: c.edge, clipPath: OCT }} />
      <div style={{ position: "absolute", inset: 0, bottom: size * 0.08, background: c.fill, clipPath: OCT, display: "grid", placeItems: "center" }}>
        {lit > 0.5 ? <PixelIcon name="star" size={Math.round(size * 0.5 / 24) * 24} color={c.ink} /> :
          <span style={{ fontFamily: FONT, fontSize: Math.round(size * 0.42 / 12) * 12, color: c.ink, lineHeight: 1 }}>{label}</span>}
      </div>
    </div>
  );
};

/** PV 的字卡：上方左对齐的像素大字，[ ] 里的词用金色，small = 上面一行小字；底下压一层渐变保证读得清 */
export const TextCard: React.FC<{ small?: string; big: string[]; at?: number }> = ({ small, big, at = 0 }) => {
  const f = useCurrentFrame();
  const line = (s: string, k: number) => {
    const t = clamp01((f - at - k * 4) / 6);
    const parts = s.split(/(\[[^\]]+\])/).filter(Boolean);
    return (
      <div key={k} style={{ fontFamily: FONT, fontSize: 96, lineHeight: 1.18, color: "#fff", textShadow: "6px 6px 0 #0b0b1e", whiteSpace: "nowrap", opacity: t > 0 ? 1 : 0, transform: `translateY(${(1 - easeOutBack(t, 2)) * 30}px)` }}>
        {parts.map((p, i) => p.startsWith("[") ? <span key={i} style={{ color: DARK.gold }}>{p.slice(1, -1)}</span> : <span key={i}>{p}</span>)}
      </div>
    );
  };
  return (
    <>
      <div style={{ position: "absolute", left: 0, top: 0, width: W, height: 460, background: "linear-gradient(rgba(5,5,15,0.78), rgba(5,5,15,0.5) 60%, rgba(5,5,15,0))", opacity: f >= at ? 1 : 0 }} />
      <div style={{ position: "absolute", left: 64, top: 96 }}>
        {small && <div style={{ fontFamily: FONT, fontSize: 48, color: DARK.ink2, textShadow: "4px 4px 0 #0b0b1e", marginBottom: 12, opacity: f >= at ? 1 : 0 }}>{small}</div>}
        {big.map(line)}
      </div>
    </>
  );
};

// ---------- 技能树：游戏真实数据（src/gen/tree.json 的 183 个技能、242 条必须前置） ----------
// 按“前置链有多深”分层，最底下是不用先学别的技能，往上一层层长；同一层按领域排，颜色是领域色。
// 这是视频里为竖屏重排的样子（游戏的技能地图是按领域分块的横图），点和线都对应真实的技能和前置关系。
type Sk = { id: string; name: string; lane: string; step: number; required: { id: string }[] };
const TREE = treeJson as unknown as { lanes: { id: string; color: string }[]; skills: Sk[] };
const LANE_ORDER = TREE.lanes.map((l) => l.id);
const LANE_COLOR = Object.fromEntries(TREE.lanes.map((l) => [l.id, l.color]));
const byId = new Map(TREE.skills.map((s) => [s.id, s]));
const req = (s: Sk) => s.required.map((r) => r.id).filter((id) => byId.has(id));
const depth = new Map<string, number>();
const dOf = (id: string): number => {
  if (depth.has(id)) return depth.get(id)!;
  const r = req(byId.get(id)!);
  const d = r.length ? 1 + Math.max(...r.map(dOf)) : 0;
  depth.set(id, d);
  return d;
};
TREE.skills.forEach((s) => dOf(s.id));
export const TREE_LEVELS = Math.max(...depth.values()) + 1;
const levels = Array.from({ length: TREE_LEVELS }, (_, L) => TREE.skills.filter((s) => depth.get(s.id) === L)
  .sort((a, b) => LANE_ORDER.indexOf(a.lane) - LANE_ORDER.indexOf(b.lane) || a.id.localeCompare(b.id)));
// 每层最多一行 19 个，多了分两行交错
const ROWS = levels.map((lv) => (lv.length > 19 ? 2 : 1));
const ROW_TOTAL = ROWS.reduce((a, b) => a + b, 0);
/** 每个技能在单位方框里的位置（0..1，y 向下）和点亮顺序（0..1） */
export const TREE_POS = (() => {
  const pos = new Map<string, { x: number; y: number; order: number; lane: string }>();
  let row = 0;
  levels.forEach((lv, L) => {
    const rows = ROWS[L];
    lv.forEach((s, i) => {
      const r = rows === 2 ? i % 2 : 0;
      const k = rows === 2 ? Math.floor(i / 2) : i, n = rows === 2 ? Math.ceil(lv.length / 2) : lv.length;
      const span = Math.min(1, 0.12 + n * 0.05);
      const x = 0.5 + (n === 1 ? 0 : (k / (n - 1) - 0.5) * span) + (rows === 2 && r === 1 ? 0.5 * span / Math.max(1, n - 1) : 0);
      const y = 1 - (row + r + 0.5) / ROW_TOTAL;
      pos.set(s.id, { x, y, order: (L + i / lv.length) / TREE_LEVELS, lane: s.lane });
    });
    row += rows;
  });
  return pos;
})();
// “我的远征”：操作系统和它的全部必须前置，排法照抄游戏的 src/game/core/graph.js topoOrder：
// 没有未学前置的先出；同时能学的按（层级 step，领域顺序，编号）排
export const ROUTE = (() => {
  const need = new Set<string>();
  const walk = (id: string) => { if (need.has(id)) return; need.add(id); req(byId.get(id)!).forEach(walk); };
  walk("C.2.1");
  const rank = (id: string) => [byId.get(id)!.step, LANE_ORDER.indexOf(byId.get(id)!.lane), id] as const;
  const cmp = (a: string, b: string) => { const ra = rank(a), rb = rank(b); return ra[0] - rb[0] || ra[1] - rb[1] || (ra[2] < rb[2] ? -1 : ra[2] > rb[2] ? 1 : 0); };
  const indeg = new Map([...need].map((id) => [id, req(byId.get(id)!).filter((r) => need.has(r)).length]));
  const ready = [...need].filter((id) => indeg.get(id) === 0).sort(cmp);
  const out: string[] = [];
  while (ready.length) {
    const id = ready.shift()!;
    out.push(id);
    for (const x of need) if (req(byId.get(x)!).includes(id)) { indeg.set(x, indeg.get(x)! - 1); if (indeg.get(x) === 0) { ready.push(x); ready.sort(cmp); } }
  }
  return out;
})();
export const skillName = (id: string) => byId.get(id)?.name ?? id;

/** 画技能树：box = 屏幕上的方框；p = 点亮进度（0..1，按层从下往上），routeP = 远征那几站亮了多少（0..1） */
export const SkillTree: React.FC<{ box: { x: number; y: number; w: number; h: number }; p: number; routeP?: number; dimColor?: string; star?: number; labels?: boolean }> =
  ({ box, p, routeP = 0, dimColor = "#34345e", star = 18, labels = false }) => {
    const at = (id: string) => { const q = TREE_POS.get(id)!; return { x: box.x + q.x * box.w, y: box.y + q.y * box.h }; };
    const litNode = (id: string) => TREE_POS.get(id)!.order < p || (ROUTE.includes(id) && ROUTE.indexOf(id) < routeP * ROUTE.length);
    return (
      <>
        <svg width={W} height={H} style={{ position: "absolute", left: 0, top: 0 }} shapeRendering="crispEdges">
          {TREE.skills.flatMap((s) => req(s).map((r) => {
            const a = at(r), b = at(s.id), on = litNode(s.id) && litNode(r);
            return <line key={`${r}-${s.id}`} x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke={on ? LANE_COLOR[s.lane] : dimColor} strokeOpacity={on ? 0.75 : 0.5} strokeWidth={on ? 3 : 2} />;
          }))}
          {ROUTE.slice(1).map((id, i) => {
            const a = at(ROUTE[i]), b = at(id), t = clamp01(routeP * ROUTE.length - (i + 1));
            return t > 0 ? <line key={`r${id}`} x1={a.x} y1={a.y} x2={a.x + (b.x - a.x) * t} y2={a.y + (b.y - a.y) * t} stroke={DARK.gold} strokeWidth={8} /> : null;
          })}
        </svg>
        {TREE.skills.map((s) => {
          const q = at(s.id), on = litNode(s.id), onRoute = ROUTE.includes(s.id) && ROUTE.indexOf(s.id) < routeP * ROUTE.length;
          const sz = onRoute ? star * 1.8 : star;
          const u = Math.round(sz / 3);
          // 像素十字星：亮着是领域色、中心白；没亮是暗点
          return on ? (
            <div key={s.id} style={{ position: "absolute", left: Math.round(q.x - 1.5 * u), top: Math.round(q.y - 1.5 * u), width: 3 * u, height: 3 * u }}>
              <div style={{ position: "absolute", left: u, top: 0, width: u, height: 3 * u, background: onRoute ? DARK.gold : LANE_COLOR[s.lane] }} />
              <div style={{ position: "absolute", left: 0, top: u, width: 3 * u, height: u, background: onRoute ? DARK.gold : LANE_COLOR[s.lane] }} />
              <div style={{ position: "absolute", left: u, top: u, width: u, height: u, background: "#fffbe8" }} />
            </div>
          ) : <div key={s.id} style={{ position: "absolute", left: Math.round(q.x - u / 2), top: Math.round(q.y - u / 2), width: u, height: u, background: dimColor }} />;
        })}
        {labels && ROUTE.map((id, i) => {
          if (ROUTE.indexOf(id) >= routeP * ROUTE.length) return null;
          const q = at(id), right = i % 2 === 0;
          return <div key={`l${id}`} style={{ position: "absolute", top: q.y - 22, left: right ? q.x + 30 : undefined, right: right ? undefined : W - q.x + 30, fontFamily: FONT, fontSize: 36, color: "#fff8de", textShadow: "4px 4px 0 #0b0b1e", whiteSpace: "nowrap" }}>{skillName(id)}</div>;
        })}
      </>
    );
  };

/** 像素大标题《计算机大学习！》：砸下来（大→小、带一点过冲），at 帧开始 */
export const BigTitle: React.FC<{ at: number; y: number; color?: string; shadow?: string; size?: number }> = ({ at, y, color = "#fff", shadow = "#0b0b1e", size = 156 }) => {
  const f = useCurrentFrame();
  if (f < at) return null;
  const t = clamp01((f - at) / 7);
  const s = 2.2 - 1.2 * easeOutCubic(t) + (t >= 1 ? 0 : 0);
  return (
    <div style={{ position: "absolute", left: 0, width: W, top: y, textAlign: "center", transform: `scale(${s})`, transformOrigin: "50% 50%", opacity: Math.min(1, t * 2.5) }}>
      <span style={{ fontFamily: FONT, fontSize: size, color, textShadow: `10px 10px 0 ${shadow}`, whiteSpace: "nowrap", letterSpacing: 4 }}>计算机大学习！</span>
    </div>
  );
};
