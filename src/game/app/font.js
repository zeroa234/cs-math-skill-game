// Font preference (settings.font): lets players switch away from the 12px pixel font when reading
// long lessons or code is tiring, while keeping the pixel look as the default.
import { store } from "./state.js";
import { FONTS, fontMeta, fontOf, nextFont } from "../core/font.js";

export { FONTS, fontMeta, fontOf, nextFont };

export function applyFont(id) {
  if (typeof document === "undefined") return;
  const f = fontMeta(id).id;
  if (f === "pixel") delete document.documentElement.dataset.font;
  else document.documentElement.dataset.font = f;
}

export function cycleFont() {
  const next = nextFont(fontOf(store.get()));
  store.update((d) => { d.settings.font = next.id; });
  return next;
}

if (typeof document !== "undefined") {
  applyFont(fontOf(store.get()));
  store.subscribe((s) => applyFont(fontOf(s)));
}
