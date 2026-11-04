// 片尾：Blender 像素塔整条路变金；先是三台手机（安卓 App 的营地、远征、上课，真实截图）和“离线、不用注册”，
// 再落到标题、两位导师和署名（角色设计 ZipZipPipe，CC BY-NC 4.0，许可要求署名；背景音乐 CC0）。
import React from "react";
import { AbsoluteFill, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame } from "remotion";
import { C, PX, SHOTS, TL, beat, say, steps, tw, w } from "../lib/core";
import { Sfx, Tag, TypeText, big, frame } from "../lib/ui";
import { Sprite } from "../lib/sprite";

const PH = { w: 300, h: 649 };   // 手机屏幕（390×844 视口按比例缩）

export const Outro: React.FC = () => {
  const f = useCurrentFrame();
  const O = beat("outro").start;
  if (f < O - 14) return null;
  const S1 = say("outro", 1), tLight = w("outro", "一路点亮");
  const vid = steps(tw(f, O - 10, 0.3), 4);
  const black = tw(f, TL.frames - 24, 0.75);
  const phonesO = steps(tw(f, O + 2, 0.25), 3) * (1 - steps(tw(f, S1 - 8, 0.25), 3));
  const chips: [string, string][] = [["安卓", "安卓 App"], ["电脑版", "电脑版：解压双击"], ["离线玩", "离线可玩"], ["不用注册", "不用注册"]];
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: vid }}>
        <Sequence from={O} layout="none">
          <OffthreadVideo src={staticFile("blender/outro.mp4")} muted style={{ width: "100%", height: "100%", imageRendering: "pixelated" }} />
        </Sequence>
      </AbsoluteFill>
      <AbsoluteFill style={{ opacity: vid, background: "linear-gradient(90deg, rgba(14,13,36,0.82) 0%, rgba(14,13,36,0.5) 42%, transparent 64%)" }} />
      {/* 三台手机 */}
      <div style={{ position: "absolute", left: 110, top: 120, display: "flex", gap: 40, opacity: phonesO }}>
        {["phone-camp", "phone-route", "phone-lesson"].map((n, i) => {
          const t = steps(tw(f, O + 4 + i * 6, 0.3), 4);
          return (
            <div key={n} style={{ position: "relative", width: PH.w + 24, height: PH.h + 60, transform: `translateY(${(1 - t) * 120 + (i === 1 ? -30 : 0)}px)`, opacity: t, background: "#0b0b1c",
              boxShadow: frame(6, C.rim, C.rimDeep), padding: "36px 12px 24px" }}>
              <div style={{ position: "absolute", left: "50%", top: 14, width: 72, height: 10, marginLeft: -36, background: C.rimDeep }} />
              <div style={{ width: PH.w, height: PH.h, overflow: "hidden", background: C.bg }}>
                <Img src={staticFile(`shots/${SHOTS[n].file}`)} style={{ width: PH.w, height: (PH.w * SHOTS[n].h) / SHOTS[n].w }} />
              </div>
            </div>
          );
        })}
      </div>
      <div style={{ position: "absolute", left: 110, top: 876, display: "flex", gap: 24, opacity: 1 - steps(tw(f, S1 - 8, 0.25), 3) }}>
        {chips.map(([word, text], i) => <div key={word} style={{ position: "relative", width: [190, 330, 210, 200][i], height: 60 }}>
          <Tag x={0} y={30} at={w("outro", word)} color={i < 2 ? C.accent : C.good} text={text} size={32} />
        </div>)}
      </div>
      {/* 落版 */}
      <div style={{ position: "absolute", left: 132, top: 200, opacity: steps(tw(f, S1 - 2, 0.25), 3) }}>
        <div style={{ ...big(48, C.ink2) }}><TypeText text="从第一课开始" at={S1} rate={0.6} /></div>
        <div style={{ ...big(192, C.gold), marginTop: 16, textShadow: "16px 16px 0 #1a1003" }}>
          {[..."点亮之路"].map((ch, i) => {
            const t = steps(tw(f, tLight + i * 4, 0.2), 4);
            return <span key={i} style={{ display: "inline-block", opacity: t > 0 ? 1 : 0, transform: `scale(${0.6 + 0.4 * t})` }}>{ch}</span>;
          })}
        </div>
        <div style={{ ...big(36, C.ink), marginTop: 18, opacity: steps(tw(f, tLight + 16, 0.2), 3) }}>github.com/zeroa234/cs-math-skill-game · 安卓 App / 网页版</div>
        <div style={{ position: "relative", height: 300, marginTop: 34 }}>
          <Sprite who="black" seq={["cast", "idle"]} from={tLight} x={0} y={0} scale={4} opacity={steps(tw(f, tLight, 0.2), 3)} />
          <Sprite who="blue" seq={["wave", "idle"]} from={tLight + 6} x={300} y={0} scale={4} flip opacity={steps(tw(f, tLight + 6, 0.2), 3)} />
        </div>
      </div>
      <div style={{ position: "absolute", left: 132, bottom: 40, fontFamily: PX, fontSize: 24, lineHeight: "32px", color: C.muted, opacity: steps(tw(f, tLight + 10, 0.3), 3) }}>
        导师角色设计：ZipZipPipe（CC BY-NC 4.0） · 背景音乐：Juhani Junkala《Grasslands》（CC0） · 像素字体：Fusion Pixel（OFL）
      </div>
      <AbsoluteFill style={{ background: "#000", opacity: black }} />
      <Sfx at={tLight} name="fanfare" v={0.4} />
      <Sfx at={O - 6} name="whoomp" v={0.3} />
    </AbsoluteFill>
  );
};
