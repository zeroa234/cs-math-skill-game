// "减少动画" (settings.reduceMotion) also turns CSS animations off, like the system setting does:
// style.css matches :root[data-motion="reduce"]. Sprites and confetti read the setting themselves.
import { store } from "./state.js";

export function applyMotion(reduce) {
  if (typeof document === "undefined") return;
  if (reduce) document.documentElement.dataset.motion = "reduce";
  else delete document.documentElement.dataset.motion;
}

if (typeof document !== "undefined") {
  applyMotion(store.get().settings.reduceMotion);
  store.subscribe((s) => applyMotion(s.settings.reduceMotion));
}
