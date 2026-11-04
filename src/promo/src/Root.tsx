import React from "react";
import { Composition, continueRender, delayRender, staticFile } from "remotion";
import { loadFont } from "@remotion/fonts";
import { FPS, H, TL, W } from "./lib/core";
import { Promo } from "./Promo";
import { Cover } from "./Cover";

export const COVERS = { "16x9": [1920, 1080], "4x3": [1440, 1080], "3x4": [1080, 1440], "9x16": [1080, 1920] } as const;

// 游戏自己的像素字体（public/fonts/，scripts/promo/assets.mjs 从 assets/fonts 复制；Fusion Pixel 12px，OFL-1.1）
const wait = delayRender("fonts");
Promise.all([
  loadFont({ family: "Fusion Pixel", url: staticFile("fonts/fusion-pixel-12px-proportional-zh_hans.otf.woff2") }),
  loadFont({ family: "Fusion Pixel Mono", url: staticFile("fonts/fusion-pixel-12px-monospaced-zh_hans.otf.woff2") }),
]).then(() => continueRender(wait));

export const Root: React.FC = () => (
  <>
    <Composition id="Promo" component={Promo} durationInFrames={TL.frames} fps={FPS} width={W} height={H} />
    {Object.entries(COVERS).map(([k, [w, h]]) => <Composition key={k} id={`Cover-${k}`} component={Cover} durationInFrames={1} fps={FPS} width={w} height={h} defaultProps={{ w, h }} />)}
  </>
);
