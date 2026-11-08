// 纯音乐 PV《一条路，一棵树》（竖屏 1080×1920，约 69 s）：一个看不见的玩家每天学一小课，路上的关卡一颗颗亮起来，
// 越学越深，考过结业挑战，最后整棵技能树亮了。没有配音，靠画面、音乐和上方的短字卡说明（用户 2026-11-05）。
// 画面卡配乐 The World Is Ours 的拍点（public/build/beats-world.json 的恒定速度网格，150 BPM，一小节 1.6 s）：
//   原曲 5.44 s 起播（开头只留 1 秒，用户 2026-11-05）→ 第 32 小节骤停（结业挑战，只剩心跳）→ 3 小节后接高潮乐句（第 56–64 小节）
//   → 整棵树全亮时在第 64 小节线上戛然而止 → 落版。音乐剪辑表在 data/promo/music.json（pv-a、pv-b）。
// 竖屏三层：上方字卡（0–380）+ 导师；中间游戏画面（手机版真实截图，带像素边框）；背景是游戏的像素场景。分镜见 data/promo/storyboard.md。
import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame } from "remotion";
import beats from "../../public/build/beats-world.json";
import { DARK, FONT, FPS, H, W, clamp01, easeInOutCubic, easeOutBack, easeOutCubic } from "../lib/core";
import { Burst, Confetti, Flash, PixelFrame, PixelIcon, Sfx, Stars, punch, shake } from "../lib/fx";
import { Box, Shot, target, SHOTS } from "../lib/shot";
import { STAGE, Sprite, Who } from "../lib/sprite";
import { BigTitle, Node, PixelBg, ROUTE, SkillTree, TextCard, skillName } from "../lib/world";

// ---------- 时间：原曲的小节 → 视频帧 ----------
const G = beats.grid;
const tBar = (bar: number, beat = 0) => G.t0 + (bar * 4 + beat) * G.beat;
const OFF = tBar(4) - 1.0;                       // 视频第 0 秒 = 原曲这一刻（第 4 小节前 1 秒）
/** 前段（原曲第 bar 小节第 beat 拍）的帧号 */
export const fb = (bar: number, beat = 0) => Math.round((tBar(bar, beat) - OFF) * FPS);
const BEAT_F = G.beat * FPS;                     // 一拍多少帧（12）
export const EXAM = fb(32);                      // 音乐骤停，结业挑战
const EXAM_BARS = 3;
export const CLIMAX = EXAM + Math.round(EXAM_BARS * 4 * BEAT_F);
/** 高潮段（接原曲第 56 小节）第 bar 小节第 beat 拍的帧号 */
export const cb = (bar: number, beat = 0) => CLIMAX + Math.round((bar * 4 + beat) * BEAT_F);
export const END = cb(8);                        // 第 64 小节线：戛然而止，进落版
export const PV_LEN = END + 6 * FPS;

// ---------- 镜头件 ----------
type Cut = { from: number; to: number; el: React.ReactNode; top?: React.ReactNode };
const NIGHT: React.FC<{ pan?: number }> = ({ pan = 0 }) => <><PixelBg src="title.png" dim={0.55} pan={pan} /><Stars n={70} seed="day" opacity={0.35} /></>;

/** 冷开场：黑里一颗关卡“叮”地点亮，镜头拉开，是一条往夜空里走的路（整段约 1 秒） */
const ORIGIN = { x: 540, y: 1180 };
const pathPt = (i: number) => ({ x: ORIGIN.x + Math.sin(i * 0.85) * 230, y: ORIGIN.y - i * 250 });
const PathDots: React.FC<{ n: number; litUpTo: number }> = ({ n, litUpTo }) => (
  <>
    {Array.from({ length: n - 1 }, (_, i) => Array.from({ length: 5 }, (_, k) => {
      const a = pathPt(i), b = pathPt(i + 1), t = (k + 1) / 6;
      return <div key={`${i}-${k}`} style={{ position: "absolute", left: Math.round(a.x + (b.x - a.x) * t) - 8, top: Math.round(a.y + (b.y - a.y) * t) - 8, width: 16, height: 16, background: i < litUpTo ? DARK.gold : "#3a3a66" }} />;
    }))}
  </>
);
const ColdOpen: React.FC<{ hit: number; end: number }> = ({ hit, end }) => {
  const f = useCurrentFrame();
  const lit = f >= hit ? 1 : 0;
  const press = f >= hit - 3 && f < hit ? 1 : 0;
  const pull = easeInOutCubic(clamp01((f - (hit + 4)) / Math.max(1, end - hit - 5)));
  const sh = shake(f, hit, 5, 10);
  return (
    <AbsoluteFill style={{ background: "#05050f" }}>
      <AbsoluteFill style={{ opacity: pull }}><PixelBg src="title.png" dim={0.25} pan={-200 * pull} y={(1 - pull) * 160} /></AbsoluteFill>
      <Stars n={150} seed="cold" opacity={0.5 * (1 - pull * 0.5)} />
      <AbsoluteFill style={{ transform: `translate(${sh.x}px, ${sh.y + pull * 420}px) scale(${1 - 0.62 * pull})`, transformOrigin: `${ORIGIN.x}px ${ORIGIN.y}px` }}>
        <div style={{ opacity: pull }}><PathDots n={12} litUpTo={0} /></div>
        {Array.from({ length: 11 }, (_, i) => i + 1).map((i) => { const p = pathPt(i); return <div key={i} style={{ opacity: pull }}><Node x={p.x} y={p.y} size={216} lit={0} label={String(i + 1)} /></div>; })}
        <div style={{ opacity: Math.min(1, (f + 1) / 3) }}><Node x={ORIGIN.x} y={ORIGIN.y} size={216} lit={lit} label="1" press={press} /></div>
        {f >= hit && f < hit + 16 && (() => {
          const t = (f - hit) / 16, r = 120 + 420 * easeOutCubic(t);
          const pts = [[30, 0], [70, 0], [100, 30], [100, 70], [70, 100], [30, 100], [0, 70], [0, 30]].map(([x, y]) => `${x},${y}`).join(" ");
          return <svg viewBox="-4 -4 108 108" style={{ position: "absolute", left: ORIGIN.x - r, top: ORIGIN.y - r, width: 2 * r, height: 2 * r, opacity: 1 - t }} shapeRendering="crispEdges"><polygon points={pts} fill="none" stroke={DARK.gold} strokeWidth={4} /></svg>;
        })()}
        <Burst at={hit} x={ORIGIN.x} y={ORIGIN.y} n={22} colors={[DARK.gold, "#fff8de", "#ffd56b"]} speed={560} size={16} seed="cold" />
      </AbsoluteFill>
      <Flash at={hit} len={4} color="#fff8de" max={0.4} />
    </AbsoluteFill>
  );
};

/** 连续 N 天：营地的齿轮塔满屏，游戏里那枚“连续学习天数”的牌子放大，姐妹站在下面 */
const Streak: React.FC<{ n: number; big?: boolean; who?: [string, string] }> = ({ n, big = false, who = ["idle", "wave"] }) => {
  const f = useCurrentFrame();
  const m = SHOTS[`streak-dark-${n}`];
  const w = big ? 900 : 760;
  const s = punch(f, 0, 6, 0.8) * (1 + 0.04 * clamp01(f / 40));
  return (
    <AbsoluteFill>
      <PixelBg src="lane-c.png" dim={0.35} pan={-260} />
      <div style={{ position: "absolute", left: (W - w) / 2, top: 820 - (w * m.h / m.w) / 2, transform: `scale(${s})` }}>
        <Shot name={`streak-dark-${n}`} width={w} style={{ imageRendering: "pixelated" }} />
      </div>
      <Sprite who="black" seq={[who[0]]} footX={340} footY={1820} scale={7} />
      <Sprite who="blue" seq={[who[1]]} footX={760} footY={1820} scale={7} flip />
    </AbsoluteFill>
  );
};

// 游戏画面区：字卡下面，带像素边框
const UI = { top: 410, bottom: 1880 };
const PHONE_TOP = 112;
const uiScale = (crop: Box) => Math.min((UI.bottom - UI.top) / crop.h, 980 / crop.w);
const Screen: React.FC<{ children: React.ReactNode; w: number; h: number; s: number; top?: number }> = ({ children, w, h, s, top = UI.top }) => (
  <div style={{ position: "absolute", left: (W - w) / 2 - 12, top: top - 12, transform: `scale(${s})`, transformOrigin: "50% 20%" }}>
    <PixelFrame px={12} rim={DARK.rim} deep={DARK.rimDeep} fill={DARK.bg} style={{ width: w + 24, height: h + 36, boxShadow: "18px 18px 0 rgba(0,0,0,0.45)", overflow: "hidden" }}>{children}</PixelFrame>
  </div>
);

/** 一课（或结业挑战）里的一屏，手机版：有结果栏的裁到底、栏从底下滑上来；没有的只裁到卡片下沿 */
const LessonCut: React.FC<{ shot: string; bar?: boolean; good?: boolean; push?: boolean; bg?: React.ReactNode; fromY?: number }> = ({ shot, bar = false, good = false, push = false, bg, fromY = PHONE_TOP }) => {
  const f = useCurrentFrame();
  const b = bar ? target(shot, "bar") : null;
  const cardKey = SHOTS[shot].targets.card ? "card" : "brief";
  const card = target(shot, cardKey);
  const crop: Box = { x: 8, y: fromY, w: 374, h: (b ? 844 : card.y + card.h + 16) - fromY };
  const sc = uiScale(crop), w = crop.w * sc, h = crop.h * sc;
  const s = punch(f, 0, 5, 0.95) * (push ? 1 + 0.03 * clamp01(f / 45) : 1);
  const slide = b ? (1 - easeOutCubic(clamp01(f / 5))) * b.h * sc : 0;
  return (
    <AbsoluteFill>
      {bg ?? <NIGHT />}
      <Screen w={w} h={h} s={s}>
        <Shot name={shot} crop={b ? { ...crop, h: b.y - crop.y } : crop} width={w} />
        {b && <div style={{ position: "absolute", left: 0, top: (b.y - crop.y) * sc + slide }}><Shot name={shot} crop={{ x: crop.x, y: b.y, w: crop.w, h: 844 - b.y }} width={w} /></div>}
      </Screen>
      {good && <Burst at={2} x={W / 2} y={UI.top + h * 0.35} n={14} colors={[DARK.good, "#c9ffd2", DARK.gold]} speed={420} size={12} seed={shot} />}
    </AbsoluteFill>
  );
};

/** 字卡旁边的导师（画在字卡那层之上，不被渐变压暗），跟着答对、答错反应 */
const Mentor: React.FC<{ who?: Who; mood?: "idle" | "good" | "bad" | "cheer" }> = ({ who = "blue", mood = "idle" }) => {
  const seq = mood === "good" ? ["jump_start", "jump_land", "idle"] : mood === "bad" ? ["coy"] : mood === "cheer" ? [who === "black" ? "cast" : "dance"] : ["idle"];
  return <Sprite who={who} seq={seq} footX={900} footY={UI.top - 24} scale={4} flip />;
};

/** 一课学完（手机版结算页）：三颗星在 starsAt 的帧上一颗颗弹出来，姐妹在面板上方庆祝 */
const DoneCut: React.FC<{ starsAt: number[] }> = ({ starsAt }) => {
  const f = useCurrentFrame();
  const name = "lesson-phone-dark-done-nostars", ref = "lesson-phone-dark-done";
  const crop: Box = { x: 0, y: 100, w: 390, h: 640 };
  const sc = uiScale(crop), w = crop.w * sc, x0 = (W - w) / 2;
  const at = (bx: number, by: number) => ({ x: x0 + (bx - crop.x) * sc, y: UI.top + (by - crop.y) * sc });
  const sp = SHOTS[name].sprites as { who: Who; action: string; x: number; y: number; w: number; h: number; flip: boolean }[];
  return (
    <AbsoluteFill>
      <NIGHT pan={-120} />
      <Screen w={w} h={crop.h * sc} s={punch(f, 0, 5, 0.95)}><Shot name={name} crop={crop} width={w} /></Screen>
      {sp.map((s, i) => { const p = at(s.x + s.w / 2, s.y + s.h); return <Sprite key={i} who={s.who} seq={[s.action]} footX={p.x} footY={p.y} scale={(s.w / STAGE[s.who].w) * sc} flip={s.flip} />; })}
      {[0, 1, 2].map((i) => {
        const b = target(ref, "stars", i);
        if (f < starsAt[i]) return null;
        const t = clamp01((f - starsAt[i]) / 8), size = 120;
        const c = at(b.x + b.w / 2, b.y + b.h / 2);
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: c.x - size / 2, top: c.y - size / 2, transform: `scale(${0.2 + 0.8 * easeOutBack(t, 2.6)}) rotate(${-25 * (1 - t)}deg)`, opacity: Math.min(1, t * 3) }}>
              <PixelIcon name="star" size={size} color={DARK.gold} style={{ filter: `drop-shadow(0 8px 0 ${DARK.goldEdge})` }} />
            </div>
            <Burst at={starsAt[i]} x={c.x} y={c.y} n={10} colors={[DARK.gold, "#fff8de"]} speed={260} size={10} seed={`st${i}`} />
          </React.Fragment>
        );
      })}
    </AbsoluteFill>
  );
};

/** 夜空里那条路：这些天学过的关卡都亮了，镜头沿着路往上飞 */
const PathRise: React.FC<{ len: number }> = ({ len }) => {
  const f = useCurrentFrame();
  const t = easeInOutCubic(clamp01(f / len));
  const n = 44, lit = Math.min(30, Math.floor(f / 1.2));
  return (
    <AbsoluteFill style={{ background: "#05050f" }}>
      <PixelBg src="title.png" dim={0.2} pan={-200} y={80 - 160 * t} />
      <Stars n={150} seed="rise" opacity={0.5} />
      <AbsoluteFill style={{ transform: `translateY(${520 + t * 5600}px) scale(0.4)`, transformOrigin: `${ORIGIN.x}px ${ORIGIN.y}px` }}>
        <PathDots n={n} litUpTo={lit} />
        {Array.from({ length: n }, (_, i) => { const p = pathPt(i); return <Node key={i} x={p.x} y={p.y} size={216} lit={i < lit ? 1 : 0} label={String(i + 1)} />; })}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/** 实验室里的一个实验：每拍换成下一下操作之后的截图（真实按钮点出来的状态），背景是这个实验所在领域的场景 */
const LabCut: React.FC<{ lab: string; states: number[]; bg: string; pan?: number; flashLast?: string }> = ({ lab, states, bg, pan = 0, flashLast }) => {
  const f = useCurrentFrame();
  const k = Math.min(states.length - 1, Math.floor(f / BEAT_F));
  const name = `lab-dark-${lab}-${states[k]}`;
  const m = SHOTS[name];
  const crop: Box = { x: 0, y: 0, w: m.w, h: m.h };
  const sc = uiScale(crop), w = crop.w * sc, h = crop.h * sc;
  const last = Math.round((states.length - 1) * BEAT_F);
  return (
    <AbsoluteFill>
      <PixelBg src={bg} dim={0.45} pan={pan} />
      <Stars n={40} seed={lab} opacity={0.25} />
      <Screen w={w} h={h} s={punch(f, 0, 5, 0.94) * (1 + 0.02 * clamp01(f / 48))}><Shot name={name} crop={crop} width={w} /></Screen>
      {flashLast && <Flash at={last} len={8} color={flashLast} max={0.55} />}
    </AbsoluteFill>
  );
};

/** 组和组之间的重音：领域场景满屏，姐妹一起跳，彩带 */
const Cheer: React.FC<{ bg: string; pan?: number }> = ({ bg, pan = 0 }) => (
  <AbsoluteFill>
    <PixelBg src={bg} dim={0.2} pan={pan} />
    <Sprite who="black" seq={["jump_start", "jump_land", "cast"]} footX={340} footY={1760} scale={8} />
    <Sprite who="blue" seq={["jump_start", "jump_land", "dance"]} footX={760} footY={1760} scale={8} flip />
    <Burst at={0} x={W / 2} y={1100} n={24} colors={[DARK.gold, "#7187ff", "#f08cc0", "#52c46a"]} speed={700} size={16} seed={bg} />
    <Flash at={0} len={5} color="#fff" max={0.6} />
  </AbsoluteFill>
);

/** “我的远征”的 5 站（游戏真实路线：操作系统的全部必须前置，按先后）：每两拍亮一站，站名在旁边 */
const RouteStops: React.FC<{ litAt: number[] }> = ({ litAt }) => {
  const f = useCurrentFrame();
  const rise = easeInOutCubic(clamp01((f - litAt[litAt.length - 1]) / 40));
  const pts = ROUTE.map((_, i) => ({ x: i % 2 ? 700 : 380, y: 1680 - i * 250 }));
  return (
    <AbsoluteFill style={{ background: "#05050f" }}>
      <PixelBg src="title.png" dim={0.3} pan={-220} y={60 - 80 * rise} />
      <Stars n={120} seed="route" opacity={0.5} />
      <AbsoluteFill style={{ transform: `translateY(${rise * 60}px)` }}>
        <svg width={W} height={H} style={{ position: "absolute" }} shapeRendering="crispEdges">
          {pts.slice(1).map((b, i) => { const a = pts[i]; const t = clamp01((f - litAt[i]) / 8); return <line key={i} x1={a.x} y1={a.y} x2={a.x + (b.x - a.x) * t} y2={a.y + (b.y - a.y) * t} stroke={DARK.gold} strokeWidth={14} strokeDasharray="20 14" />; })}
        </svg>
        {ROUTE.map((id, i) => {
          const on = f >= litAt[i];
          const p = pts[i];
          return (
            <React.Fragment key={id}>
              <div style={{ transform: on ? `scale(${punch(f, litAt[i], 6, 0.7)})` : undefined, transformOrigin: `${p.x}px ${p.y}px`, position: "absolute", inset: 0 }}>
                <Node x={p.x} y={p.y} size={160} lit={on ? 1 : 0} label={String(i + 1)} />
              </div>
              <div style={{ position: "absolute", top: p.y - 30, left: i % 2 ? undefined : p.x + 110, right: i % 2 ? W - p.x + 110 : undefined, fontFamily: FONT, fontSize: 60, color: on ? "#fff8de" : "#6f6c9c", textShadow: "5px 5px 0 #0b0b1e", whiteSpace: "nowrap" }}>{skillName(id)}</div>
              <Burst at={litAt[i]} x={p.x} y={p.y} n={14} colors={[DARK.gold, "#fff8de"]} speed={300} size={12} seed={`rs${i}`} />
            </React.Fragment>
          );
        })}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/** 结业挑战的计分条：第一次答对几题，八成那条线（游戏的规则：PASS_SHARE = 0.8；这一关 15 题，答对 12 题过线）；过线时变金 */
const BOSS_N = 15;
const NEED = Math.ceil(BOSS_N * 0.8);
const Meter: React.FC<{ marks: number[] }> = ({ marks }) => {
  const f = useCurrentFrame();
  const k = marks.filter((m) => f >= m).length;
  const passed = k >= NEED;
  const w = 760, seg = w / BOSS_N;
  return (
    <div style={{ position: "absolute", left: 64, top: 310 }}>
      <div style={{ position: "relative", width: w, height: 34, background: "#1b1b3a", border: `6px solid ${DARK.rim}` }}>
        {Array.from({ length: k }, (_, i) => <div key={i} style={{ position: "absolute", left: i * seg + 2, top: 2, width: seg - 4, height: 18, background: passed ? DARK.gold : DARK.good }} />)}
        <div style={{ position: "absolute", left: NEED * seg - 3, top: -18, width: 6, height: 58, background: passed ? DARK.gold : "#fff8de" }} />
      </div>
    </div>
  );
};

/** 高潮第一拍：结业挑战结算“程序设计基础 已点亮”，姐妹施法、跳舞，彩带 */
const BossDone: React.FC = () => {
  const f = useCurrentFrame();
  const name = "boss-dark-done";
  const crop: Box = { x: 0, y: 110, w: 390, h: 370 };
  const sc = uiScale(crop), w = crop.w * sc, x0 = (W - w) / 2, top = 560;
  const sp = SHOTS[name].sprites as { who: Who; action: string; x: number; y: number; w: number; h: number; flip: boolean }[];
  return (
    <AbsoluteFill>
      <PixelBg src="lane-c.png" dim={0.3} pan={-260} />
      <Screen w={w} h={crop.h * sc} s={punch(f, 0, 6, 0.85)} top={top}><Shot name={name} crop={crop} width={w} /></Screen>
      {sp.map((s, i) => <Sprite key={i} who={s.who} seq={[s.action]} footX={x0 + (s.x + s.w / 2 - crop.x) * sc} footY={top + (s.y + s.h - crop.y) * sc} scale={(s.w / STAGE[s.who].w) * sc} flip={s.flip} />)}
      <Confetti at={0} n={90} colors={[DARK.gold, "#7187ff", "#f08cc0", "#52c46a"]} />
      <Burst at={0} x={W / 2} y={top + 140} n={30} colors={[DARK.gold, "#fff8de"]} speed={760} size={16} seed="lit" />
    </AbsoluteFill>
  );
};

/** 高潮：镜头从远征那几站拉开到整棵技能树，按“先学的先亮”一层层亮起来 */
const TreeReveal: React.FC<{ len: number }> = ({ len }) => {
  const f = useCurrentFrame();
  const zoom = easeInOutCubic(clamp01((f - 18) / 70));
  const p = clamp01((f - 30) / (len - 40));
  const routeP = clamp01(f / 18);
  const box = { x: 60, y: 520, w: 960, h: 1300 };
  const s = 2.1 - 1.1 * zoom;
  return (
    <AbsoluteFill style={{ background: "#05050f" }}>
      <PixelBg src="title.png" dim={0.45} pan={-200} y={-40 * zoom} />
      <Stars n={160} seed="tree" opacity={0.55} />
      <AbsoluteFill style={{ transform: `scale(${s})`, transformOrigin: `${box.x + box.w * 0.35}px ${box.y + box.h * 0.8}px` }}>
        <SkillTree box={box} p={p} routeP={routeP} star={18} labels={zoom < 0.35} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/** 落版：静下来的技能树，像素大标题砸下来，信息一行行出来，最后营地的火苗 +1 */
export const END_LINES = ["免费 · 源码公开 · 非商用", "安卓 · Windows · 网页版", "下载：B 站简介，或 GitHub 搜“计算机大学习”"];
const EndCard: React.FC = () => {
  const f = useCurrentFrame();
  const lines = END_LINES.map((t, i) => ({ t, at: 22 + i * 10, size: [60, 48, 42][i], color: i === 0 ? DARK.gold : DARK.ink }));
  const credits = ["导师角色设计 ZipZipPipe（CC BY-NC 4.0）", "音乐 The World Is Ours · Zane Little Music（CC0）", "像素字体 Fusion Pixel（OFL）"];
  const plusAt = 120;
  const chip = f >= plusAt ? 31 : 30;
  const sh = shake(f, 4, 10, 16);
  return (
    <AbsoluteFill style={{ background: "#05050f" }}>
      <PixelBg src="title.png" dim={0.5} pan={-200} />
      <Stars n={160} seed="end" opacity={0.6} />
      <AbsoluteFill style={{ opacity: 0.3 }}><SkillTree box={{ x: 60, y: 300, w: 960, h: 1200 }} p={1} routeP={1} star={15} /></AbsoluteFill>
      <AbsoluteFill style={{ transform: `translate(${sh.x}px, ${sh.y}px)` }}>
        <BigTitle at={4} y={430} size={132} />
        <Burst at={4} x={W / 2} y={520} n={30} colors={[DARK.gold, "#fff8de", "#7187ff", "#f08cc0"]} speed={800} size={16} seed="title" />
      </AbsoluteFill>
      {lines.map((l, i) => f >= l.at && (
        <div key={i} style={{ position: "absolute", left: 0, width: W, top: 690 + i * 96, textAlign: "center", fontFamily: FONT, fontSize: l.size, color: l.color, textShadow: "5px 5px 0 #0b0b1e", whiteSpace: "nowrap", transform: `translateY(${(1 - easeOutBack(clamp01((f - l.at) / 7), 2)) * 24}px)` }}>{l.t}</div>
      ))}
      {f >= 56 && credits.map((c, i) => <div key={i} style={{ position: "absolute", left: 0, width: W, top: 1010 + i * 50, textAlign: "center", fontFamily: FONT, fontSize: 30, color: DARK.ink2, textShadow: "3px 3px 0 #0b0b1e", whiteSpace: "nowrap" }}>{c}</div>)}
      {f >= 70 && (
        <div style={{ position: "absolute", left: (W - 420) / 2, top: 1230, transform: `scale(${f >= plusAt ? punch(f, plusAt, 6, 0.7) : punch(f, 70, 6, 0.7)})` }}>
          <Shot name={`streak-dark-${chip}`} width={420} style={{ imageRendering: "pixelated" }} />
        </div>
      )}
      <Burst at={plusAt} x={W / 2} y={1330} n={18} colors={["#ff9a3c", DARK.gold, "#fff1b8"]} speed={360} size={12} seed="plus" />
      <Sprite who="black" seq={["cast", "idle"]} from={10} footX={300} footY={1830} scale={7} />
      <Sprite who="blue" seq={["dance", "idle"]} from={10} footX={780} footY={1830} scale={7} flip />
    </AbsoluteFill>
  );
};

export const PV: React.FC = () => {
  const L = (s: string) => `lesson-phone-dark-${s}`;
  const hit = fb(3, 2);
  const boss = (k: number) => `boss-dark-${String(k).padStart(2, "0")}`;
  // 结业挑战：第 0–1 拍是规则页；前 7 题一拍一题，后 8 题半拍一题（越来越快）
  const examMarks = [...Array.from({ length: 7 }, (_, i) => EXAM + Math.round((2 + i) * BEAT_F)), ...Array.from({ length: 8 }, (_, i) => EXAM + Math.round((9 + i * 0.375) * BEAT_F))];
  const cuts: Cut[] = [
    // —— 每天一课 ——
    { from: fb(4), to: fb(5), el: <Streak n={1} /> },
    { from: fb(5), to: fb(5, 2), el: <LessonCut shot={L("00")} />, top: <Mentor /> },
    { from: fb(5, 2), to: fb(6), el: <LessonCut shot={L("01")} bar good />, top: <Mentor mood="good" /> },
    { from: fb(6), to: fb(6, 2), el: <LessonCut shot={L("03")} push />, top: <Mentor /> },
    { from: fb(6, 2), to: fb(7), el: <LessonCut shot={L("07")} bar good />, top: <Mentor mood="good" /> },
    { from: fb(7), to: fb(8), el: <DoneCut starsAt={[12, 24, 36]} /> },
    { from: fb(8), to: fb(8, 1), el: <Streak n={2} /> },
    { from: fb(8, 1), to: fb(8, 2), el: <LessonCut shot={L("01")} bar good />, top: <Mentor mood="good" /> },
    { from: fb(8, 2), to: fb(8, 3), el: <LessonCut shot={L("11")} bar good />, top: <Mentor mood="good" /> },
    { from: fb(8, 3), to: fb(9), el: <DoneCut starsAt={[0, 3, 6]} /> },
    { from: fb(9), to: fb(9, 1), el: <Streak n={3} /> },
    { from: fb(9, 1), to: fb(9, 2), el: <LessonCut shot={L("wrong-pick")} />, top: <Mentor /> },
    { from: fb(9, 2), to: fb(10), el: <LessonCut shot={L("wrong")} bar />, top: <Mentor mood="bad" /> },
    { from: fb(10), to: fb(10, 1), el: <Streak n={4} /> },
    { from: fb(10, 1), to: fb(10, 2), el: <LessonCut shot={L("15")} bar good />, top: <Mentor mood="good" /> },
    { from: fb(10, 2), to: fb(10, 3), el: <DoneCut starsAt={[0, 2, 4]} /> },
    { from: fb(10, 3), to: fb(11), el: <Streak n={5} /> },
    { from: fb(11), to: fb(11, 1), el: <Streak n={6} /> },
    { from: fb(11, 1), to: fb(11, 2), el: <Streak n={7} /> },
    { from: fb(11, 2), to: fb(11, 3), el: <Streak n={14} /> },
    { from: fb(11, 3), to: fb(13), el: <Streak n={30} big who={["cast", "dance"]} /> },
    { from: fb(13), to: fb(15), el: <PathRise len={fb(15) - fb(13)} /> },
    // —— 越学越深：三个一组，组间一个重音（姐妹跳一下）——
    { from: fb(15), to: fb(16), el: <LabCut lab="trace" states={[0, 1, 2, 3]} bg="lane-p.png" pan={-300} />, top: <Mentor /> },
    { from: fb(16), to: fb(17), el: <LabCut lab="stack" states={[1, 2, 3, 4]} bg="lane-f.png" pan={200} />, top: <Mentor /> },
    { from: fb(17), to: fb(18), el: <LabCut lab="hash" states={[1, 2, 3, 4]} bg="lane-d.png" pan={-200} />, top: <Mentor mood="good" /> },
    { from: fb(18), to: fb(19), el: <Cheer bg="lane-p.png" pan={300} /> },
    { from: fb(19), to: fb(21), el: <LabCut lab="threads" states={[0, 1, 2, 3, 4, 5, 6]} bg="lane-c.png" pan={-260} flashLast="#f07a7f" />, top: <Mentor who="black" /> },
    { from: fb(21), to: fb(22), el: <LabCut lab="replace" states={[0]} bg="lane-c.png" pan={260} />, top: <Mentor who="black" /> },
    { from: fb(22), to: fb(23), el: <LabCut lab="sched" states={[0]} bg="lane-c.png" pan={0} />, top: <Mentor who="black" mood="good" /> },
    { from: fb(23), to: fb(24), el: <Cheer bg="lane-c.png" pan={-400} /> },
    { from: fb(24), to: fb(25), el: <LabCut lab="bfs" states={[1, 2, 3, 4]} bg="lane-f.png" pan={-250} />, top: <Mentor /> },
    { from: fb(25), to: fb(26), el: <LabCut lab="matrix" states={[0, 1, 2, 3]} bg="lane-math.png" pan={250} />, top: <Mentor /> },
    { from: fb(26), to: fb(27), el: <LabCut lab="descent" states={[0, 1, 2, 3]} bg="lane-math.png" pan={-250} />, top: <Mentor mood="good" /> },
    { from: fb(27), to: fb(28), el: <Cheer bg="lane-math.png" pan={350} /> },
    { from: fb(28), to: EXAM, el: <RouteStops litAt={[0, 2, 4, 6, 8].map((b) => Math.round(b * BEAT_F))} /> },
    // —— 结业挑战（音乐骤停）——
    { from: EXAM, to: examMarks[0], el: <LessonCut shot="boss-dark-brief" fromY={56} bg={<NIGHT pan={-300} />} />, top: <Mentor who="black" /> },
    ...examMarks.map((m, i): Cut => ({ from: m, to: examMarks[i + 1] ?? CLIMAX, el: <LessonCut shot={boss(i)} bar good fromY={56} bg={<NIGHT pan={-300} />} />, top: <Mentor who="black" mood={i >= NEED - 1 ? "good" : "idle"} /> })),
    // —— 高潮 ——
    { from: CLIMAX, to: cb(1), el: <BossDone /> },
    { from: cb(1), to: END, el: <TreeReveal len={END - cb(1)} /> },
    { from: END, to: PV_LEN, el: <EndCard /> },
  ];
  // 字卡：说清这是什么游戏（像看完的人转述给朋友的话，不喊口号）。每张停留都远长于 Netflix 中文字幕 9 字/秒的上限
  const cards: { from: number; to: number; small?: string; big: string[] }[] = [
    { from: hit + 2, to: fb(5), small: "学计算机专业", big: ["每天[一小课]"] },
    { from: fb(5), to: fb(7), big: ["先猜一猜，", "再看[讲解]"] },
    { from: fb(7), to: fb(8), big: ["学完一课，", "拿[星星]"] },
    { from: fb(9, 1), to: fb(10, 2), big: ["答错了", "也[不扣分]"] },
    { from: fb(11, 3), to: fb(13), big: ["每天来", "[打个卡]"] },
    { from: fb(13), to: fb(15), big: ["学过的每一课", "都[亮着]"] },
    { from: fb(15), to: fb(18), big: ["看不懂的地方，", "[动手试一试]"] },
    { from: fb(19), to: fb(23), big: ["两个线程各加一，", "结果却是 [1]"] },
    { from: fb(24), to: fb(27), big: ["要用的数学，", "[也一起学]"] },
    { from: fb(28), to: EXAM, big: ["从第一行程序，", "学到[操作系统]"] },
    { from: EXAM, to: CLIMAX, small: "最后一关：第一次就答对八成才点亮", big: ["[结业挑战]"] },
    { from: cb(2), to: END, big: ["整个计算机专业，", "[一棵技能树]"] },
  ];
  const tap = (f: number): [number, string, number] => [f, "tap", 0.5];
  const sfx: [number, string, number?][] = [
    [hit, "star", 0.9], [hit, "unlock", 0.5],
    [fb(5, 2), "correct"], [fb(6, 2), "correct"], [fb(7) + 12, "star"], [fb(7) + 24, "star"], [fb(7) + 36, "star"],
    [fb(8, 1), "correct"], [fb(8, 2), "correct"], [fb(8, 3), "star"],
    [fb(9, 1), "select"], [fb(9, 2), "wrong"],
    [fb(10, 1), "correct"], [fb(10, 2), "star"],
    [fb(11, 3), "fanfare", 0.7],
    ...[4, 8, 9, 10].map((b) => [fb(b), "page", 0.5] as [number, string, number]),
    // 实验：每拍一下按键声；竞态那一下 x = 1，响一声“答错”
    ...[15, 16, 17, 24, 25, 26].flatMap((b) => [1, 2, 3].map((k) => tap(fb(b, k)))),
    ...[1, 2, 3, 4, 5].map((k) => tap(fb(19) + Math.round(k * BEAT_F))),
    [fb(19) + Math.round(6 * BEAT_F), "wrong", 0.7],
    ...[18, 23, 27].map((b) => [fb(b), "fanfare", 0.5] as [number, string, number]),
    ...[0, 2, 4, 6, 8].map((k) => [fb(28) + Math.round(k * BEAT_F), "star", 0.6] as [number, string, number]),
    // 结业挑战：心跳（每两拍一下）+ 每题答对
    ...Array.from({ length: EXAM_BARS * 2 }, (_, i) => [EXAM + Math.round(i * 2 * BEAT_F), "heart", 0.9] as [number, string, number]),
    ...examMarks.map((m) => [m, "correct", 0.4] as [number, string, number]),
    [CLIMAX, "fanfare", 0.8],
    // 落版：标题砸下，火苗 +1
    [END + 4, "thud", 1], [END + 4, "star", 0.6], [END + 120, "unlock", 0.7],
  ];
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <Audio src={staticFile("build/music/pv-a.wav")} />
      <Sequence from={CLIMAX} layout="none"><Audio src={staticFile("build/music/pv-b.wav")} /></Sequence>
      <Sequence from={0} durationInFrames={fb(4)}><ColdOpen hit={hit} end={fb(4)} /></Sequence>
      {cuts.map((c, i) => <Sequence key={i} from={c.from} durationInFrames={Math.max(1, c.to - c.from)}>{c.el}</Sequence>)}
      {/* “30 天”：火苗粒子 + 彩带 */}
      <Sequence from={fb(11, 3)} durationInFrames={fb(13) - fb(11, 3)}>
        <Burst at={0} x={W / 2} y={820} n={26} colors={["#ff9a3c", DARK.gold, "#fff1b8"]} speed={640} size={16} seed="fire" />
        <Confetti at={4} colors={[DARK.gold, "#7187ff", "#f08cc0", "#52c46a"]} />
      </Sequence>
      {cards.map((c, i) => <Sequence key={`t${i}`} from={c.from} durationInFrames={c.to - c.from}><TextCard small={c.small} big={c.big} /></Sequence>)}
      <Sequence from={EXAM} durationInFrames={CLIMAX - EXAM}><Meter marks={examMarks.map((m) => m - EXAM)} /></Sequence>
      {cuts.map((c, i) => c.top && <Sequence key={`m${i}`} from={c.from} durationInFrames={Math.max(1, c.to - c.from)}>{c.top}</Sequence>)}
      <Flash at={fb(15)} len={8} color="#fff" max={0.9} />
      <Flash at={CLIMAX} len={8} color="#fff8de" max={0.9} />
      <Flash at={END} len={6} color="#fff" max={1} />
      {sfx.map(([at, n, v], i) => <Sfx key={i} at={at} name={n} volume={v ?? 0.7} />)}
    </AbsoluteFill>
  );
};
