// The whole tree on one pan/zoom canvas: lanes stacked, steps left→right (the prototype's layout).
// Hover or focus a card to light its required-prerequisite chain; click to open it. Touch has no hover:
// the first tap selects a card (and lights its chain), a second tap on it opens it.
import { useEffect, useMemo, useRef, useState } from "preact/hooks";
import Panzoom from "@panzoom/panzoom";
import { g, activeRoute, useProgress, useSkillStates } from "../app/state.js";
import { href, go } from "../app/router.js";
import { requiredClosure } from "../core/graph.js";
import { STATUS } from "./common.jsx";
import { Icon } from "./icons.jsx";

const CARD = g.tree.meta.card;
const HEAD = 64, PAD = 16, LEFT = 16;
// Phones have no wheel or hover: the hint names the gestures they do have.
const TOUCH = typeof matchMedia === "function" && matchMedia("(hover: none)").matches;
// Zoom and pan when the map was last left (for this session), restored when it opens again.
let lastView = null;

// Lanes are packed into `cols` columns (each lane goes to the currently shorter column, in tree
// order), so "fit everything" uses a wide screen instead of one very tall strip.
function layout(cols) {
  const laneW = LEFT + Math.max(...g.tree.skills.map((s) => s.x)) + CARD.w + 24;
  const colY = Array(cols).fill(0);
  const lanes = [], pos = new Map();
  for (const l of g.tree.lanes) {
    const skills = g.tree.skills.filter((s) => s.lane === l.id);
    const h = HEAD + Math.max(...skills.map((s) => s.y)) + CARD.h + PAD;
    const c = colY.indexOf(Math.min(...colY));
    const x0 = c * (laneW + 40), y0 = colY[c];
    lanes.push({ lane: l, x: x0, y: y0, h, w: laneW });
    for (const s of skills) pos.set(s.id, { x: x0 + LEFT + s.x, y: y0 + HEAD + s.y });
    colY[c] += h + 14;
  }
  return { lanes, pos, W: cols * laneW + (cols - 1) * 40, H: Math.max(...colY) };
}

export function MapView() {
  const p = useProgress();
  const states = useSkillStates(p);
  const [cols] = useState(() => (window.innerWidth > 1000 ? 2 : 1));
  const L = useMemo(() => layout(cols), [cols]);
  const wrap = useRef(null), canvas = useRef(null), pz = useRef(null), moved = useRef(false), pointer = useRef(""), fitAll = useRef(() => {}), zoomBy = useRef(() => {});
  const [hover, setHover] = useState(null);
  const [sel, setSel] = useState(null);
  const route = activeRoute(p);
  const onRoute = new Set(route?.stops || []);
  const lit = hover || sel;
  const chain = useMemo(() => (lit ? requiredClosure(g, lit) : null), [lit]);

  useEffect(() => {
    const el = canvas.current, box = wrap.current;
    // Start as close to "the whole tree" as possible while every card stays a usable target
    // (≥ 24 px tall, WCAG 2.2 target size); "看全部" then fits everything.
    const fit = Math.min(box.clientWidth / L.W, box.clientHeight / L.H, 1);
    const scale = Math.max(fit, 24 / CARD.h);
    // Panzoom's focal-point zoom (wheel, pinch, zoomToPoint) needs its default transform-origin
    // (50% 50%), so the canvas is placed with the pan that puts its top edge at the top of the box
    // and centres it horizontally when it is narrower than the box: with transform
    // scale(s) translate(x, y) about the centre c, the top-left lands at c·(1 − s) + s·(x, y).
    const placed = (s) => ({ x: (Math.max(0, (box.clientWidth - L.W * s) / 2) - (L.W / 2) * (1 - s)) / s, y: (-(L.H / 2) * (1 - s)) / s });
    // Coming back from a skill page opened here: the same zoom and place as when it was left.
    const start = lastView?.cols === cols ? lastView : { scale, ...placed(scale) };
    const minScale = Math.min(0.1, fit), maxScale = 2;
    const panzoom = Panzoom(el, { maxScale, minScale, startScale: start.scale, startX: start.x, startY: start.y, cursor: "grab" });
    // Panzoom works out each zoom's focal point from the canvas's size on screen, but writes the new
    // transform only on the next animation frame. A second zoom event in the same frame (a fast wheel,
    // a touchpad, a pinch) then read the old size against the new scale, and every such event pushed
    // the map further to the top left. Writing the same transform at once keeps every reading current.
    const sync = () => { const { x, y } = panzoom.getPan(); el.style.transform = `scale(${panzoom.getScale()}) translate(${x}px, ${y}px)`; };
    fitAll.current = () => { const at = placed(fit); panzoom.zoom(fit, { animate: false }); panzoom.pan(at.x, at.y, { animate: false }); sync(); };
    // ＋/－ zoom about the middle of what you are looking at, like the wheel zooms about the pointer.
    // The scale is clamped first, as zoomWithWheel does: zoomToPoint places the focal point for the
    // scale it is asked for, so asking past the limit shifted the map at the last step.
    zoomBy.current = (f) => {
      const r = box.getBoundingClientRect();
      panzoom.zoomToPoint(Math.min(maxScale, Math.max(minScale, panzoom.getScale() * f)), { clientX: r.left + r.width / 2, clientY: r.top + r.height / 2 });
      sync();
    };
    pz.current = panzoom;
    const wheel = (e) => { e.preventDefault(); panzoom.zoomWithWheel(e); sync(); };
    box.addEventListener("wheel", wheel, { passive: false });
    // Pinches (and pans) are handled by Panzoom's own listener on document; this one on window runs
    // after it in the bubbling order.
    window.addEventListener("pointermove", sync);
    // A press that moves more than a finger's slop is a pan, not a tap on a card. Listened to in the
    // capture phase: Panzoom stops pointerdown from bubbling out of the canvas, so a bubbling listener
    // never saw a press on a card. `moved` was then never reset: after one pan no card opened again,
    // and with a mouse, merely moving over the map counted as a pan.
    let sx = 0, sy = 0, pressed = false;
    const down = (e) => { sx = e.clientX; sy = e.clientY; pressed = true; moved.current = false; pointer.current = e.pointerType; };
    const move = (e) => { if (pressed && Math.hypot(e.clientX - sx, e.clientY - sy) > 10) moved.current = true; };
    const up = () => { pressed = false; };
    box.addEventListener("pointerdown", down, true);
    box.addEventListener("pointermove", move, true);
    window.addEventListener("pointerup", up, true);
    window.addEventListener("pointercancel", up, true);
    return () => {
      lastView = { cols, scale: panzoom.getScale(), ...panzoom.getPan() };
      box.removeEventListener("wheel", wheel); box.removeEventListener("pointerdown", down, true); box.removeEventListener("pointermove", move, true);
      window.removeEventListener("pointerup", up, true); window.removeEventListener("pointercancel", up, true);
      window.removeEventListener("pointermove", sync);
      panzoom.destroy();
    };
  }, []);

  const edges = [];
  for (const s of g.tree.skills) for (const r of s.required) {
    const a = L.pos.get(r.id), b = L.pos.get(s.id);
    const x1 = a.x + CARD.w, y1 = a.y + CARD.h / 2, x2 = b.x, y2 = b.y + CARD.h / 2;
    const hot = chain && chain.has(s.id) && chain.has(r.id);
    const mx = (x1 + x2) / 2;
    edges.push(<path class={"edge" + (hot ? " hot" : "") + (chain && !hot ? " dim" : "")} d={x2 > x1 ? `M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}` : `M${x1},${y1} C${x1 + 40},${y1} ${x2 - 40},${y2} ${x2},${y2}`} />);
  }
  // A click from the keyboard has no pointer type and opens at once, like a mouse click.
  const tapFirst = (e) => ["touch", "pen"].includes(e.pointerType ?? pointer.current);
  const open = (id, e) => {
    if (moved.current) return;
    if (tapFirst(e) && sel !== id) setSel(id);
    else go("skill", id);
  };
  const letGo = (e) => { if (!moved.current && !e.target.closest(".mcard")) setSel(null); };
  return (
    <div class="mapview">
      <div class="map-tools">
        <span class="small">{g.tree.skills.length} 个技能 · {TOUCH ? "双指缩放、拖动移动 · 点一下看要先学的技能链，再点一下打开" : "滚轮缩放、拖动平移 · 悬停看要先学的技能链 · 点开查看"}</span>
        <span class="legend small">{Object.entries(STATUS).map(([k, v]) => <span class={"badge st-" + k}><Icon name={v.icon} /> {v.label}</span>)}{route && <span class="badge route-ring"><Icon name="target" /> {route.name}</span>}</span>
        <span class="row"><button type="button" class="btn small ghost" aria-label="放大" onClick={() => zoomBy.current(1.25)}>＋</button><button type="button" class="btn small ghost" aria-label="缩小" onClick={() => zoomBy.current(0.8)}>－</button><button type="button" class="btn small ghost" onClick={() => fitAll.current()}>看全部</button></span>
      </div>
      <div class="map-wrap" ref={wrap} onClick={letGo}>
        <div class="map-canvas" ref={canvas} style={{ width: L.W + "px", height: L.H + "px" }}>
          {L.lanes.map(({ lane, x, y, h, w }) => <div class="lane" style={{ left: x + "px", top: y + "px", height: h + "px", width: w + "px", "--lane": lane.color }}><div class="lane-title">{lane.name}</div></div>)}
          <svg class="edges" width={L.W} height={L.H}>{edges}</svg>
          {g.tree.skills.map((s) => {
            const st = states.get(s.id);
            const ps = L.pos.get(s.id);
            const cls = ["mcard", "st-" + st.status, s.optional && "optional", onRoute.has(s.id) && "on-route", chain && (chain.has(s.id) ? "hot" : "dim"), st.hasContent && "has-content", sel === s.id && "selected"].filter(Boolean).join(" ");
            return (
              <a href={href("skill", s.id)} class={cls} style={{ left: ps.x + "px", top: ps.y + "px", width: CARD.w + "px", height: CARD.h + "px", "--lane": g.lanes.get(s.lane).color }}
                onMouseEnter={() => setHover(s.id)} onMouseLeave={() => setHover(null)} onFocus={() => setHover(s.id)} onBlur={() => setHover(null)}
                onClick={(e) => { e.preventDefault(); open(s.id, e); }}>
                <span class="mc-name">{s.name}</span>
                {sel === s.id ? <span class="mc-meta"><Icon name="next" /> 再点一下打开</span> : <span class="mc-meta"><Icon name={STATUS[st.status].icon} /> {STATUS[st.status].label} · {st.hasContent ? "互动课" : `${s.chapters.length} 章`}{st.progress > 0 && st.status !== "lit" ? ` · ${Math.round(st.progress * 100)}%` : ""}</span>}
              </a>
            );
          })}
        </div>
      </div>
    </div>
  );
}
