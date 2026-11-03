// Hash router: every view has its own address (#/skill/C.2.1), so it can be bookmarked or shared and
// the browser's back button works. Works on file:// where the History API cannot.
import { useEffect, useState } from "preact/hooks";

// A part that is not valid percent-encoding (a hand-typed "%") stays as typed instead of throwing.
const decode = (s) => { try { return decodeURIComponent(s); } catch { return s; } };
export function parseHash(hash = location.hash) {
  const parts = hash.replace(/^#\/?/, "").split("/").filter(Boolean).map(decode);
  return { name: parts[0] || "home", args: parts.slice(1) };
}

export function useRoute() {
  const [r, setR] = useState(parseHash());
  useEffect(() => {
    const on = () => { setR(parseHash()); window.scrollTo(0, 0); };
    window.addEventListener("hashchange", on);
    return () => window.removeEventListener("hashchange", on);
  }, []);
  return r;
}

// The last overview screen the player was on (营地, 远征, 地图, 选远征), so a skill page's back link
// returns there: a skill opened from the map goes back to the map, not to the route. Lessons,
// challenges and other skills opened on the way do not change it.
const HUBS = { home: "营地", route: "路线", map: "地图", pick: "选远征" };
let hub = null;
const noteHub = () => { const r = parseHash(); if (HUBS[r.name]) hub = { hash: location.hash || "#/", label: HUBS[r.name] }; };
if (typeof window !== "undefined") { noteHub(); window.addEventListener("hashchange", noteHub); }
export const lastHub = () => hub;

export const href = (...parts) => "#/" + parts.map(encodeURIComponent).join("/");
export const go = (...parts) => { location.hash = href(...parts); };
