// "Is there a newer version?" against the latest GitHub release of the public repository (the APK is
// attached to each release). Only asks; installing stays with the player, as Android requires for
// apps outside a store. The app checks by itself at most once a day (checkInBackground, from
// native.js); 我的 has a button for any time. Nothing is sent but the request itself.
import { useSyncExternalStore } from "preact/compat";

export const VERSION = typeof __APP_VERSION__ === "string" ? __APP_VERSION__ : "0.0.0"; // package.json, set by scripts/build-web.mjs
export const REPO = "zeroa234/cs-math-skill-game";
export const RELEASES_PAGE = `https://github.com/${REPO}/releases`;
const API = `https://api.github.com/repos/${REPO}/releases/latest`;
const KEY = "cs-math-skill-game/update"; // { checkedAt, dismissed } — not part of the save
const DAY = 864e5;

// 1.0.10 > 1.0.9; a leading "v" in the tag is ignored.
export function isNewer(a, b) {
  const pa = String(a).replace(/^v/, "").split(".").map(Number), pb = String(b).replace(/^v/, "").split(".").map(Number);
  for (let i = 0; i < Math.max(pa.length, pb.length); i++) if ((pa[i] || 0) !== (pb[i] || 0)) return (pa[i] || 0) > (pb[i] || 0);
  return false;
}

// → { latest, newer, notes, download, page }; throws a message for the player when it cannot tell.
export async function checkUpdate(fetchImpl = fetch) {
  const ctl = new AbortController();
  const timer = setTimeout(() => ctl.abort(), 10000);
  let res;
  try { res = await fetchImpl(API, { headers: { Accept: "application/vnd.github+json" }, signal: ctl.signal }); }
  catch { throw new Error("连不上 GitHub，检查一下网络再试"); }
  finally { clearTimeout(timer); }
  if (res.status === 404) throw new Error("还没有发布过版本");
  if (!res.ok) throw new Error(`GitHub 暂时没有回应（${res.status}），过一会儿再试`);
  const rel = await res.json();
  const latest = String(rel.tag_name || "").replace(/^v/, "");
  const apk = (rel.assets || []).find((a) => a.name.endsWith(".apk"));
  return { latest, newer: isNewer(latest, VERSION), notes: (rel.body || "").trim(), download: apk?.browser_download_url || rel.html_url, page: rel.html_url };
}

// A newer release found in the background, shown on the camp until the player dismisses that version.
let found = null;
const subs = new Set();
const set = (v) => { found = v; for (const s of subs) s(); };
export const useFoundUpdate = () => useSyncExternalStore((s) => (subs.add(s), () => subs.delete(s)), () => found);

const memo = () => { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch { return {}; } };
const remember = (patch) => { try { localStorage.setItem(KEY, JSON.stringify({ ...memo(), ...patch })); } catch {} };

export function dismissUpdate() {
  if (found) remember({ dismissed: found.latest });
  set(null);
}

// The release found is remembered with the day's check, so the banner is still there after the app
// is reopened the same day (until it is dismissed, or this version is that release or newer).
export async function checkInBackground(now = Date.now()) {
  const m = memo();
  const show = (u) => { if (u && isNewer(u.latest, VERSION) && m.dismissed !== u.latest) set(u); };
  if (now - (m.checkedAt || 0) < DAY) return show(m.found);
  try {
    const u = await checkUpdate();
    remember({ checkedAt: now, found: u.newer ? { latest: u.latest, download: u.download } : null });
    show(u);
  } catch { /* offline or rate-limited: try again next launch */ }
}
