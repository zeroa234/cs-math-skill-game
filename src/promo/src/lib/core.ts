// 两部片子共用的常量：画幅、帧率、游戏的配色（src/web/style.css 的颜色变量）、像素字体、时间换算。
import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

export const FPS = 30;
export const W = 1080; // 竖屏（用户 2026-11-05：做成竖屏）
export const H = 1920;

// 游戏的颜色：浅色主题（广告用）和深色主题“夜里的学院”（PV 用）
export const LIGHT = {
  bg: "#f3eddf", bg2: "#ebe2cc", panel: "#fffdf7", ink: "#1f1d33", ink2: "#47445f", muted: "#5c5874", line: "#ded3bb",
  accent: "#4257d6", accentEdge: "#2c3a99", good: "#247a32", bad: "#c2353d", gold: "#e0a210", goldEdge: "#a87600",
  rim: "#8c7a55", rimDeep: "#6b5b3a", pink: "#d9539a", edge: "#cbbd9c",
};
export const DARK = {
  bg: "#14142b", bg2: "#1b1b3a", panel: "#1f1f3f", ink: "#eceaf7", ink2: "#c8c5e2", muted: "#a9a5c9", line: "#35355f",
  accent: "#7187ff", good: "#52c46a", bad: "#f07a7f", gold: "#f2bd3a", goldEdge: "#b08415", rim: "#7474b4", rimDeep: "#4a4a85",
};

// Fusion Pixel 12 px（OFL）：像素字只在 12 的整数倍字号下笔画落在整像素上
export const FONT = "Fusion Pixel";
export const MONO = "Fusion Pixel Mono";
export const fontsReady = Promise.all([
  loadFont({ family: FONT, url: staticFile("fonts/fusion-pixel-12px-proportional-zh_hans.otf.woff2") }),
  loadFont({ family: MONO, url: staticFile("fonts/fusion-pixel-12px-monospaced-zh_hans.otf.woff2") }),
]);

export const sec = (s: number) => Math.round(s * FPS);

// 缓动：像素动画常用的“弹一下”
export const easeOutBack = (t: number, k = 1.70158) => 1 + (k + 1) * Math.pow(t - 1, 3) + k * Math.pow(t - 1, 2);
export const easeOutCubic = (t: number) => 1 - Math.pow(1 - t, 3);
export const easeInOutCubic = (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
export const clamp01 = (t: number) => Math.max(0, Math.min(1, t));
export const prog = (f: number, from: number, len: number) => clamp01((f - from) / Math.max(1, len));
