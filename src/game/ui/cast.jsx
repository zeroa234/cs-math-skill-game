// The two mentors: high-res pixelized Q-chibi sprites (animation strips from scripts/cast/build-chibi-sprites.py)
// and painted portraits. Everything about who they are lives here and in assets/cast/, so the cast can be
// swapped without touching the screens that use it.
import { useEffect, useLayoutEffect, useRef, useState } from "preact/hooks";
import meta from "../../../assets/cast/sprites.json";
import { store } from "../app/state.js";

// The whale sisters (designs by ZipZipPipe, CC BY-NC 4.0; credits in assets/cast/README.md and the Profile page):
// black = the younger, composed one (opening talk, review); blue = the elder, lively one (practice).
export const CAST = {
  black: { name: "鲸鱼妹妹", portrait: "assets/cast/portraits/black.webp", celebrate: "cast" },
  blue: { name: "鲸鱼姐姐", portrait: "assets/cast/portraits/blue.webp", celebrate: "dance" },
};

// Built without the characters (CAST=none, or no assets/cast/): no sprites, no portraits,
// and <html class="no-cast"> lets the stylesheet close the gaps they leave.
export const HAS_CAST = Object.keys(meta.packs).length > 0;
if (!HAS_CAST && typeof document !== "undefined") document.documentElement.classList.add("no-cast");

const UNIT = meta.unit || 1;
const reduced = () => store.get().settings.reduceMotion || matchMedia("(prefers-reduced-motion: reduce)").matches;
const preloaded = new Set();
function preloadPack(who) {
  if (typeof Image === "undefined" || preloaded.has(who) || !meta.packs[who]) return;
  preloaded.add(who);
  for (const a of Object.values(meta.packs[who])) {
    const img = new Image();
    img.src = `assets/cast/${a.file}`;
    img.decode?.().catch(() => {});
  }
}
if (HAS_CAST) {
  for (const who of Object.keys(meta.packs)) preloadPack(who);
}

// Every action of a character is drawn on one stage so the feet stay on the same spot when the action
// changes: the stage is as wide as the widest pose on either side of the foot and as tall as the
// tallest pose above it.
const stages = Object.fromEntries(Object.entries(meta.packs).map(([who, acts]) => {
  const list = Object.values(acts);
  return [who, { w: 2 * Math.max(...list.map((a) => Math.max(a.foot[0], a.w - a.foot[0]))), h: Math.max(...list.map((a) => a.foot[1])) }];
}));

// <Sprite who="blue" action="wave" /> plays `action` (once if it does not loop) and then `then`.
// `action` can also be a list, played in order, each once except the last, e.g.
// ["jump_start", "jump_land", "idle"]. Change `cue` to replay.
export function Sprite(props) {
  return HAS_CAST ? <CastSprite {...props} /> : null;
}
function CastSprite({ who, action = "idle", then = "idle", scale = 2, flip = false, cue = 0, class: cls = "", label }) {
  const seq = Array.isArray(action) ? action : [action, then];
  const seqKey = `${who}|${seq.join(",")}|${cue}`;
  const [step, setStep] = useState({ key: seqKey, i: 0 });
  const i = step.key === seqKey ? step.i : 0;
  const el = useRef(null);
  useEffect(() => { preloadPack(who); }, [who]);
  useEffect(() => {
    if (step.key !== seqKey) setStep({ key: seqKey, i: 0 });
  }, [seqKey]);
  const cur = seq[Math.min(i, seq.length - 1)];
  const last = i >= seq.length - 1 || (!Array.isArray(action) && (meta.packs[who][cur]?.loop || cur === then));
  const a = meta.packs[who][cur] || meta.packs[who].idle;
  const s = scale / UNIT;
  useLayoutEffect(() => {
    const node = el.current;
    if (!node) return;
    if (reduced() || a.frames <= 1) { node.style.backgroundPositionX = "0px"; return; }
    const fw = a.w * s;
    const duration = (a.frames / a.fps) * 1000;
    const frames = [];
    for (let k = 0; k < a.frames; k++) frames.push({ backgroundPositionX: `${-k * fw}px`, offset: k / a.frames, easing: "steps(1, end)" });
    frames.push({ backgroundPositionX: `${-(a.frames - 1) * fw}px`, offset: 1 });
    const anim = node.animate(frames, { duration, iterations: last && a.loop ? Infinity : 1, fill: "forwards" });
    let alive = true;
    const advance = () => { if (alive) setStep({ key: seqKey, i: i + 1 }); };
    if (!last) anim.onfinish = advance;
    const t = last ? null : setTimeout(advance, duration + 20);
    return () => { alive = false; anim.onfinish = null; anim.cancel(); clearTimeout(t); };
  }, [a, s, i, last, seqKey]);
  const st = stages[who];
  return (
    <div class={"sprite " + cls} role={label ? "img" : undefined} aria-label={label} aria-hidden={label ? undefined : "true"} style={{ width: st.w * s + "px", height: st.h * s + "px" }}>
      <div
        key={`${seqKey}-${i}-${a.file}`}
        ref={el}
        class="sprite-frame"
        style={{
          width: a.w * s + "px", height: a.h * s + "px",
          left: (st.w / 2 - a.foot[0]) * s + "px", top: (st.h - a.foot[1]) * s + "px",
          backgroundImage: `url(assets/cast/${a.file})`, backgroundSize: `${a.w * a.frames * s}px ${a.h * s}px`,
          transform: flip ? "scaleX(-1)" : undefined, transformOrigin: `${a.foot[0] * s}px 0`,
        }}
      />
    </div>
  );
}

export function Portrait({ who, class: cls = "" }) {
  if (!HAS_CAST) return null;
  return <img class={"portrait " + cls} src={CAST[who].portrait} alt={CAST[who].name} draggable={false} />;
}
