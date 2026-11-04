// 开场：Blender 像素 3D 的远征塔（scripts/promo/blender-route.py）一课课亮起来；左边像游戏开场一样逐字打出提问，
// 再出“点亮之路”大标题和两位导师。上一部宣传片（技能树）的封面作为“上次”的缩略图。
import React from "react";
import { AbsoluteFill, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame } from "remotion";
import { C, PX, beat, steps, tw, w } from "../lib/core";
import { Sfx, TypeBlips, TypeText, big, frame } from "../lib/ui";
import { Sprite } from "../lib/sprite";

const L = [
  { text: "上次，我把计算机专业", at: () => w("hook", "上次"), color: C.ink },
  { text: "做成了一棵技能树。", at: () => w("hook", "做成"), color: C.ink },
  { text: "这次，我想让你", at: () => w("hook", "这次"), color: C.gold },
  { text: "真的一步一步走完它。", at: () => w("hook", "真的"), color: C.gold },
];

export const Intro: React.FC = () => {
  const f = useCurrentFrame();
  const T = beat("title"), end = T.end;
  if (f > end + 24) return null;
  const tTitle = w("title", "点亮之路"), tGame = w("title", "游戏");
  const shade = tw(f, w("hook", "上次") - 12, 0.6);
  const hookOut = 1 - steps(tw(f, T.start - 6, 0.25), 3);
  const prevO = steps(tw(f, L[0].at() + 6, 0.25), 3) * (1 - steps(tw(f, L[2].at() - 6, 0.25), 3));
  return (
    <AbsoluteFill>
      <Sequence from={0} durationInFrames={end + 24} layout="none">
        <OffthreadVideo src={staticFile("blender/intro.mp4")} muted style={{ width: "100%", height: "100%", imageRendering: "pixelated" }} />
      </Sequence>
      <AbsoluteFill style={{ opacity: shade, background: "linear-gradient(90deg, rgba(14,13,36,0.86) 0%, rgba(14,13,36,0.55) 40%, transparent 62%)" }} />
      {/* hook：两句，像游戏开场的打字机一样逐字出来 */}
      <div style={{ position: "absolute", left: 132, top: 230, opacity: hookOut }}>
        {L.map((l, i) => (
          <div key={i} style={{ ...big(72, l.color), height: 96, marginTop: i === 2 ? 300 : 0 }}>
            <TypeText text={l.text} at={l.at()} rate={0.75} caret />
          </div>
        ))}
      </div>
      {/* 上次：技能树宣传片的封面 */}
      <div style={{ position: "absolute", left: 132, top: 450, opacity: prevO * hookOut, display: "flex", alignItems: "center", gap: 30 }}>
        <div style={{ width: 384, height: 216, boxShadow: frame(6, C.rim, C.rimDeep), background: C.bg, overflow: "hidden" }}>
          <Img src={staticFile("bg/tree-cover.webp")} style={{ width: 384, height: 216, objectFit: "cover" }} />
        </div>
        <div style={{ fontFamily: PX, fontSize: 36, lineHeight: "48px", color: C.ink2 }}>上一集<br /><span style={{ color: C.accentStrong }}>CS × 数学技能树</span></div>
      </div>
      {L.map((l, i) => <TypeBlips key={i} text={l.text} at={l.at()} rate={0.75} v={0.12} />)}
      {/* title：大标题 + 两位导师 */}
      <div style={{ position: "absolute", left: 132, top: 196, opacity: steps(tw(f, T.start, 0.2), 3) * (1 - steps(tw(f, end + 4, 0.3), 3)) }}>
        <div style={{ ...big(48, C.ink2) }}><TypeText text="我把它做成了一款游戏" at={T.start + 4} rate={0.9} /></div>
        <div style={{ display: "flex", marginTop: 26 }}>
          {[..."点亮之路"].map((ch, i) => {
            const t = steps(tw(f, tTitle + i * 4, 0.2), 4);
            return <span key={i} style={{ ...big(192, C.gold), display: "inline-block", opacity: t > 0 ? 1 : 0, transform: `translateY(${(1 - t) * -60}px) scale(${0.6 + 0.4 * t})`,
              textShadow: "16px 16px 0 #1a1003" }}>{ch}</span>;
          })}
        </div>
        <div style={{ ...big(42, C.ink), marginTop: 18, opacity: steps(tw(f, tTitle + 18, 0.25), 3) }}>计算机与数学的星图 · 一次一小课，一路点亮</div>
        <div style={{ position: "relative", height: 330, marginTop: 30 }}>
          <Sprite who="black" seq={["wave", "idle"]} from={tGame} x={0} y={0} scale={4} opacity={steps(tw(f, tGame, 0.2), 3)} />
          <Sprite who="blue" seq={["jump_start", "jump_air", "jump_land", "idle"]} from={tGame + 6} x={300} y={0} scale={4} flip opacity={steps(tw(f, tGame + 6, 0.2), 3)} />
        </div>
      </div>
      <Sfx at={tTitle} name="star" v={0.45} />
      <Sfx at={tTitle + 12} name="unlock" v={0.4} />
    </AbsoluteFill>
  );
};
