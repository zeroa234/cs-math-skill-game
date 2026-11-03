// 8-bit sound effects, synthesized at play time by ZzFX (MIT, no audio files). ZzFX makes its
// AudioContext when its module first runs, so it is loaded on the first sound, which always follows a
// click or a key press (browsers only start audio after a user gesture). Muted with settings.sound.
import { store } from "./state.js";

// ZzFX parameters: volume, randomness, frequency, attack, sustain, release, shape, shapeCurve, slide,
// deltaSlide, pitchJump, pitchJumpTime, repeatTime, noise, modulation, bitCrush, delay, sustainVolume.
const SFX = {
  tap: [0.35, 0, 520, 0, 0.005, 0.03, 1, 1.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.6],
  select: [0.4, 0, 700, 0, 0.01, 0.05, 0, 1.2],
  correct: [0.7, 0, 660, 0.01, 0.07, 0.2, 0, 1.6, 0, 0, 330, 0.07],
  wrong: [0.55, 0, 220, 0.01, 0.06, 0.2, 1, 1.4, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0.7],
  star: [0.6, 0, 1046, 0.01, 0.04, 0.25, 0, 2, 0, 0, 523, 0.04, 0, 0, 0, 0, 0.08],
  unlock: [0.45, 0, 300, 0.03, 0.15, 0.25, 0, 1.2, 12],
  blip: [0.18, 0.05, 880, 0, 0.005, 0.02, 0, 1.5],
  locked: [0.4, 0, 120, 0, 0.03, 0.08, 2, 1],
  page: [0.3, 0, 400, 0, 0.02, 0.06, 0, 1, 4],
};
const FANFARE = [523.25, 659.25, 783.99, 1046.5]; // C5 E5 G5 C6

let zz = null;
const load = () => (zz ||= import("zzfx").then((m) => m.ZZFX).catch(() => null));
const enabled = () => store.get().settings.sound !== false && typeof AudioContext !== "undefined";

export function play(name) {
  if (!enabled()) return;
  load().then((Z) => {
    if (!Z) return;
    if (Z.audioContext.state === "suspended") Z.audioContext.resume();
    if (name === "fanfare") FANFARE.forEach((f, i) => setTimeout(() => Z.play(0.55, 0, f, 0.01, 0.07, 0.22, 0, 1.6), i * 110));
    else if (SFX[name]) Z.play(...SFX[name]);
  });
}
