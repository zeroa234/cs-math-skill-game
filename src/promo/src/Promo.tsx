// 成片：各段按旁白时间轴叠在一起（每段自己按帧号决定出没出现），段与段之间是像素溶解转场；加字幕、旁白、音效。
// BGM 渲染后再混（scripts/promo/render.sh）。
import React from "react";
import { AbsoluteFill, Html5Audio, staticFile } from "remotion";
import { C, beat, w } from "./lib/core";
import { Bg, Sfx, Subtitles, Wipe } from "./lib/ui";
import { Intro } from "./scenes/Intro";
import { Desk } from "./scenes/Desk";
import { Lab } from "./scenes/Lab";
import { Boss } from "./scenes/Boss";
import { Review } from "./scenes/Review";
import { Tree } from "./scenes/Tree";
import { Check } from "./scenes/Check";
import { Outro } from "./scenes/Outro";

export const Promo: React.FC = () => (
  <AbsoluteFill style={{ background: C.night }}>
    <Bg />
    <Desk />
    <Lab />
    <Boss />
    <Review />
    <Tree />
    <Check />
    <Intro />
    <Outro />
    {/* 段与段之间：像素一块块盖住再揭开 */}
    {["cast", "lab", "boss", "review", "tree", "check", "outro"].map((id) => <Wipe key={id} at={beat(id).start - 4} />)}
    {/* 屏幕上已经有同样大字的拍不出字幕 */}
    <Subtitles hide={["hook", "title"]} />
    <Html5Audio src={staticFile("build/narration.wav")} />
    <Sfx at={0} name="riser" v={0.2} />
    <Sfx at={w("title", "点亮之路") - 4} name="whoomp" v={0.3} />
    {["cast", "lab", "boss", "review", "tree", "check"].map((id) => <Sfx key={id} at={beat(id).start - 10} name="page" v={0.25} />)}
  </AbsoluteFill>
);
