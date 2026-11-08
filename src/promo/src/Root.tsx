import React from "react";
import { Composition, continueRender, delayRender } from "remotion";
import { FPS, H, W, fontsReady } from "./lib/core";
import { PV, PV_LEN } from "./pv/PV";
import { Ad, AD_LEN } from "./ad/Ad";
import { AdCover, COVER_SIZES, PVCover } from "./Covers";

// 像素字体加载完再出帧
const wait = delayRender("fonts");
fontsReady.then(() => continueRender(wait));

export const Root: React.FC = () => (
  <>
    <Composition id="PV" component={PV} durationInFrames={PV_LEN} fps={FPS} width={W} height={H} />
    <Composition id="Ad" component={Ad} durationInFrames={AD_LEN} fps={FPS} width={W} height={H} />
    {COVER_SIZES.flatMap(({ suffix, width, height }) => [
      <Composition key={`AdCover${suffix}`} id={`AdCover${suffix}`} component={AdCover} durationInFrames={1} fps={FPS} width={width} height={height} />,
      <Composition key={`PVCover${suffix}`} id={`PVCover${suffix}`} component={PVCover} durationInFrames={1} fps={FPS} width={width} height={height} />,
    ])}
  </>
);
