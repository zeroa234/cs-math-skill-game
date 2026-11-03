// The two mentors: pixel sprites (animation strips from scripts/cast/extract-sprites.py) and painted
// portraits. Everything about who they are lives here and in assets/cast/, so the cast can be swapped
// without touching the screens that use it.
import { useEffect, useRef, useState } from "preact/hooks";
import meta from "../../../assets/cast/sprites.json";
import { store } from "../app/state.js";

// The whale sisters (designs by ZipZipPipe, CC BY-NC 4.0; credits in assets/cast/README.md and the Profile page):
// black = the younger, composed one (opening talk, review); blue = the elder, lively one (practice).
export const CAST = {
  black: { name: "鲸鱼妹妹", portrait: "assets/cast/portraits/black.webp", celebrate: "cast" },
  blue: { name: "鲸鱼姐姐", portrait: "assets/cast/portraits/blue.webp", celebrate: "dance" },
};

// Built without the characters (CAST=none, as in the public repository): no sprites, no portraits,
// and <html class="no-cast"> lets the stylesheet close the gaps they leave.
export const HAS_CAST = Object.keys(meta.packs).length > 0;
if (!HAS_CAST && typeof document !== "undefined") document.documentElement.classList.add("no-cast");

const reduced = () => store.get().settings.reduceMotion || matchMedia("(prefers-reduced-motion: reduce)").matches;

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
  const [i, setI] = useState(0);
  const el = useRef(null);
  useEffect(() => { setI(0); }, [seq.join(), cue]);
  const cur = seq[Math.min(i, seq.length - 1)];
  const last = i >= seq.length - 1 || (!Array.isArray(action) && (meta.packs[who][cur]?.loop || cur === then));
  const a = meta.packs[who][cur] || meta.packs[who].idle;
  useEffect(() => {
    const node = el.current;
    if (!node) return;
    const total = a.w * a.frames * scale;
    const duration = (a.frames / a.fps) * 1000;
    if (reduced()) { node.style.backgroundPositionX = "0px"; return; }
    const anim = node.animate([{ backgroundPositionX: "0px" }, { backgroundPositionX: `-${total}px` }], { duration, iterations: last && a.loop ? Infinity : 1, easing: `steps(${a.frames})`, fill: "forwards" });
    const t = last ? null : setTimeout(() => setI((n) => n + 1), duration);
    return () => { anim.cancel(); clearTimeout(t); };
  }, [a, scale, i, last]);
  const st = stages[who];
  return (
    <div class={"sprite " + cls} role={label ? "img" : undefined} aria-label={label} aria-hidden={label ? undefined : "true"} style={{ width: st.w * scale + "px", height: st.h * scale + "px" }}>
      <div
        ref={el}
        class="sprite-frame"
        style={{
          width: a.w * scale + "px", height: a.h * scale + "px",
          left: (st.w / 2 - a.foot[0]) * scale + "px", top: (st.h - a.foot[1]) * scale + "px",
          backgroundImage: `url(assets/cast/${a.file})`, backgroundSize: `${a.w * a.frames * scale}px ${a.h * scale}px`,
          transform: flip ? "scaleX(-1)" : undefined, transformOrigin: `${a.foot[0] * scale}px 0`,
        }}
      />
    </div>
  );
}

export function Portrait({ who, class: cls = "" }) {
  if (!HAS_CAST) return null;
  return <img class={"portrait " + cls} src={CAST[who].portrait} alt={CAST[who].name} draggable={false} />;
}
