// Pixel icons from pixelarticons (MIT, 24×24 grid, no anti-aliasing): one component so every icon in
// the game shares the same grid and colour (currentColor). Emoji are not used; they break the style.
import close from "pixelarticons/svg/close.svg";
import check from "pixelarticons/svg/check.svg";
import bulb from "pixelarticons/svg/lightbulb.svg";
import lock from "pixelarticons/svg/lock.svg";
import book from "pixelarticons/svg/book-open.svg";
import crown from "pixelarticons/svg/crown.svg";
import star from "pixelarticons/svg/star.svg";
import sparkle from "pixelarticons/svg/sparkle.svg";
import volume from "pixelarticons/svg/volume-3.svg";
import mute from "pixelarticons/svg/volume-x.svg";
import back from "pixelarticons/svg/arrow-left.svg";
import next from "pixelarticons/svg/chevron-right.svg";
import fire from "pixelarticons/svg/fire.svg";
import zap from "pixelarticons/svg/zap.svg";
import reload from "pixelarticons/svg/reload.svg";
import play from "pixelarticons/svg/play.svg";
import trophy from "pixelarticons/svg/trophy.svg";
import map from "pixelarticons/svg/map.svg";
import target from "pixelarticons/svg/target.svg";

const paths = (svg) => [...svg.matchAll(/<path[^>]*\sd="([^"]+)"/g)].map((m) => m[1]);
const ICONS = Object.fromEntries(Object.entries({ close, check, bulb, lock, book, crown, star, sparkle, volume, mute, back, next, fire, zap, reload, play, trophy, map, target }).map(([k, v]) => [k, paths(v)]));

// size is in CSS px and should be a multiple of 12 (or 24) so the 24-unit grid stays on whole pixels.
export function Icon({ name, size, label, class: cls }) {
  const d = ICONS[name];
  if (!d) throw new Error(`no icon ${name}`);
  return (
    <svg class={"icon " + (cls || "")} viewBox="0 0 24 24" width={size} height={size} fill="currentColor" shape-rendering="crispEdges" role={label ? "img" : undefined} aria-label={label} aria-hidden={label ? undefined : "true"}>
      {d.map((x) => <path d={x} />)}
    </svg>
  );
}
