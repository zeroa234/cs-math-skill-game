import React from "react";
import { AbsoluteFill, Img, staticFile, useVideoConfig } from "remotion";
import { DARK, FONT, H, LIGHT, W } from "./lib/core";
import { PixelFrame, PixelIcon, Stars } from "./lib/fx";
import { Sprite } from "./lib/sprite";
import { Node, PixelBg, SkillTree } from "./lib/world";
import { Book, Backdrop } from "./ad/Ad";

const Heading: React.FC<{ ad?: boolean }> = ({ ad = false }) => (
  <div style={{ position: "absolute", top: 348, left: 0, right: 0, textAlign: "center", fontFamily: FONT }}>
    <div style={{ color: ad ? LIGHT.ink : "#fff9e7", fontSize: 120, whiteSpace: "nowrap", textShadow: ad ? "8px 8px 0 #f2bd3a" : "8px 8px 0 #0a081d" }}>
      计算机大学习！
    </div>
    <div style={{ marginTop: 36, color: ad ? LIGHT.ink : "#ffdc81", fontSize: 64 }}>
      {ad ? "这些……全都要学？" : "从一颗星，到一棵树"}
    </div>
  </div>
);

const pile = [
  { name: "数据结构", x: 170, y: 1094, angle: 8 },
  { name: "操作系统", x: 85, y: 1168, angle: 9 },
  { name: "计算机组成原理", x: 440, y: 1150, angle: 4 },
  { name: "程序设计基础", x: 112, y: 1027, angle: -12 },
  { name: "C/C++与底层编程", x: 402, y: 1072, angle: -8 },
  { name: "证明方法与离散结构", x: 334, y: 960, angle: 7 },
];

const AdArt: React.FC = () => (
  <AbsoluteFill>
    <Img src={staticFile("cast/portraits/black.webp")} style={{ position: "absolute", width: 450, right: -16, bottom: 310 }} />
    <Img src={staticFile("cast/portraits/blue.webp")} style={{ position: "absolute", width: 650, left: 65, bottom: 339, transform: "scaleY(0.35)", transformOrigin: "50% 100%" }} />
    {pile.map(({ name, x, y, angle }, i) => (
      <Book key={name} name={name} i={i} style={{ left: x, top: y - 142, transform: `rotate(${angle}deg) scale(1.12)`, transformOrigin: "left center" }} />
    ))}
    <PixelIcon name="star" size={72} color={DARK.gold} style={{ position: "absolute", left: 45, top: 1250, transform: "rotate(-18deg)" }} />
    <PixelIcon name="sparkle" size={48} color={DARK.gold} style={{ position: "absolute", left: 626, top: 1275 }} />
  </AbsoluteFill>
);

const route = [[438, 1432], [624, 1240], [419, 1055], [664, 871]] as const;

const PVArt: React.FC = () => (
  <AbsoluteFill>
    <div style={{ position: "absolute", inset: "610px 36px 320px", background: "radial-gradient(ellipse,#59428066,transparent 68%)" }} />
    <AbsoluteFill style={{ opacity: 0.28 }}>
      <SkillTree box={{ x: 72, y: 740, w: 936, h: 650 }} p={1} star={13} />
    </AbsoluteFill>
    <svg width="1080" height="1920" style={{ position: "absolute", inset: 0 }}>
      <polyline points={route.map((pt) => pt.join(",")).join(" ")} fill="none" stroke="#1b1637" strokeWidth="23" />
      <polyline points={route.map((pt) => pt.join(",")).join(" ")} fill="none" stroke="#ffd56b" strokeWidth="12" strokeDasharray="18 14" />
    </svg>
    {route.map(([x, y], i) => <Node key={x} x={x} y={y} size={i === 3 ? 152 : 96} lit={1} />)}
    <Sprite who="black" seq={["cast"]} footX={260} footY={1600} scale={6} />
    <Sprite who="blue" seq={["dance"]} footX={825} footY={1600} scale={6} flip />
  </AbsoluteFill>
);

export const COVER_SIZES = [
  { suffix: "", width: W, height: H },
  { suffix: "-3x4", width: 1080, height: 1440 },
  { suffix: "-4x5", width: 1080, height: 1350 },
  { suffix: "-1x1", width: 1080, height: 1080 },
  { suffix: "-4x3", width: 1440, height: 1080 },
  { suffix: "-16x9", width: 1920, height: 1080 },
];

const Cover: React.FC<{ ad?: boolean }> = ({ ad = false }) => {
  const { width, height } = useVideoConfig();
  const wide = width > height;
  const native = width === W && height === H;
  const artScale = wide ? Math.min(0.88, width * 0.53 / W) : native ? 1 : height / 1740;
  const artX = wide ? width * 0.45 : (width - W * artScale) / 2;
  const artY = wide ? height * 0.92 - 1600 * artScale : native ? 0 : height * 0.85 - 1600 * artScale;
  const headingScale = wide ? Math.min(0.93, width * 0.51 / W) : native ? 1 : height / 1920 + 0.14;
  const headingX = wide ? (width * 0.5 - W * headingScale) / 2 : (width - W * headingScale) / 2;
  const headingY = native ? 0 : height * (wide ? 0.29 : 0.10) - 250 * headingScale;
  return (
    <AbsoluteFill style={{ overflow: "hidden", background: ad ? LIGHT.bg : "#141127" }}>
      {ad ? <Backdrop /> : <><PixelBg src="title.png" dim={0.44} pan={-140} /><Stars n={72} seed="cover" opacity={0.52} /></>}
      <AbsoluteFill style={{ background: ad
        ? "linear-gradient(180deg,#fff8e7 7%,transparent 60%)"
        : wide ? "linear-gradient(90deg,#141127 10%,#141127dd 34%,transparent 73%)"
          : "linear-gradient(180deg,#141127 5%,#141127e8 28%,transparent 49%,transparent 76%,#141127 100%)" }} />
      <div style={{ position: "absolute", left: artX, top: artY, width: W, height: H, transform: `scale(${artScale})`, transformOrigin: "0 0" }}>
        {ad ? <AdArt /> : <PVArt />}
      </div>
      <div style={{ position: "absolute", left: headingX, top: headingY, width: W, height: H, transform: `scale(${headingScale})`, transformOrigin: "0 0" }}>
        <Heading ad={ad} />
      </div>
      {!ad && (wide || native) && (
        <div style={{ position: "absolute", width: wide ? width * 0.5 : width, top: wide ? height * 0.69 : 1630, display: "flex", justifyContent: "center" }}>
          <PixelFrame px={4} fill="#242046" rim="#665387" deep="#211736" style={{ padding: "12px 22px", color: "#fff0ca", font: `42px "${FONT}"` }}>
            每天一小课 · 学计算机专业
          </PixelFrame>
        </div>
      )}
    </AbsoluteFill>
  );
};

export const AdCover: React.FC = () => <Cover ad />;
export const PVCover: React.FC = () => <Cover />;