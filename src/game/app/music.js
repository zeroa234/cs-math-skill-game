// Background music (data/music.yaml → src/gen/music.json, files in assets/music/). Each scene of
// the chosen style has a short playlist; a scene change fades the old track out and the new one in
// on two <audio> elements. Nothing starts before the first tap or key press (browsers only allow
// sound after a user gesture), and the music pauses while the page is hidden: the app in the
// background, another tab. Off with settings.music, or with everything else via settings.sound.
import music from "../../gen/music.json";
import { store } from "./state.js";

export const STYLES = music.styles;
export const PACKS = music.packs;
export const DEFAULT_VOLUME = 0.5;

const FADE_MS = 900;
const decks = typeof Audio === "function" ? [new Audio(), new Audio()] : [];
let live = 0; // index of the deck playing (or fading in)
let playing = null; // track id on the live deck
let queue = [], pos = 0, scene = null, unlocked = false;

const settings = () => store.get().settings;
const wanted = () => settings().sound !== false && settings().music !== false;
const level = () => settings().musicVolume ?? DEFAULT_VOLUME;
const style = () => STYLES.find((s) => s.id === settings().musicStyle) || STYLES[0];

const fades = new Map();
function fade(deck, to, done) {
  clearInterval(fades.get(deck));
  const from = deck.volume, t0 = performance.now();
  fades.set(deck, setInterval(() => {
    const k = Math.min(1, (performance.now() - t0) / FADE_MS);
    deck.volume = from + (to - from) * k;
    if (k === 1) { clearInterval(fades.get(deck)); done?.(); }
  }, 40));
}

function start(id) {
  const old = decks[live];
  if (playing) fade(old, 0, () => old.pause());
  live ^= 1;
  const deck = decks[live];
  deck.src = `assets/music/${id}.ogg`;
  deck.loop = queue.length === 1;
  deck.volume = 0;
  deck.onended = () => { pos = (pos + 1) % queue.length; start(queue[pos]); };
  deck.play().catch(() => {});
  fade(deck, level());
  playing = id;
}

function stopAll() {
  if (!playing) return;
  const deck = decks[live];
  fade(deck, 0, () => deck.pause());
  playing = null;
}

// Brings what plays in line with the scene and the settings.
function sync() {
  if (!decks.length) return;
  const list = (unlocked && wanted() && scene && style().scenes[scene]) || [];
  if (!list.length) return stopAll();
  if (playing && list.includes(playing)) {
    // same track still fits (lo-fi uses one playlist everywhere): keep it, follow the new list
    queue = list; pos = list.indexOf(playing);
    decks[live].loop = list.length === 1;
    clearInterval(fades.get(decks[live]));
    decks[live].volume = level(); // a volume change follows the slider at once
    return;
  }
  queue = list;
  pos = Math.floor(Math.random() * list.length);
  start(queue[pos]);
}

export function setMusicScene(s) {
  if (s === scene) return;
  scene = s;
  sync();
}

// The Android app tells us when it goes to the background (native.js); browsers hide the page.
let backgrounded = false;
function hold() {
  if (!playing) return;
  if (backgrounded || document.hidden) decks[live].pause();
  else decks[live].play().catch(() => {});
}
export function setAppBackground(on) { backgrounded = on; hold(); }

if (decks.length) {
  const unlock = () => { if (unlocked) return; unlocked = true; sync(); };
  window.addEventListener("pointerdown", unlock, true);
  window.addEventListener("keydown", unlock, true);
  document.addEventListener("visibilitychange", hold);
  let last = "";
  store.subscribe((p) => {
    const s = p.settings, key = [s.sound, s.music, s.musicStyle, s.musicVolume].join("|");
    if (key !== last) { last = key; sync(); }
  });
}
