// 广告向《两位导师告诉你》（竖屏 1080×1920，约 65 s）：鲸鱼姐姐（活泼）和鲸鱼妹妹（沉稳）当主持人演小剧场，像多邻国的广告那样：
// 一句一个画面，屏幕上的大字和配音一字不差，角色一直在演，界面放在像素手机里。
// 竖屏布局：上方大字（说话人名牌 + 台词框），下半是两位导师的立绘，书塔、手机、技能树在中间。
// 台词在 data/promo/ad.json，配音由 scripts/promo/voice.py 合成（姐姐 blue-direct、妹妹 black-design，用户看过样片后定）。
// 开头（书塔、手机、姐姐弹回来）是用户认可过的样片，时间不动；后面每句的开始时间 = 上一句结束 + 停顿（停顿里演动作）。
import React from "react";
import { AbsoluteFill, Audio, Img, Sequence, interpolate, random, staticFile, useCurrentFrame } from "remotion";
import { useAudioData } from "@remotion/media-utils";
import adJson from "../../../../data/promo/ad.json";
import blueMan from "../../public/build/voice/blue-direct/manifest.json";
import blackMan from "../../public/build/voice/black-design/manifest.json";
import treeJson from "../../public/build/tree.json";
import { DARK, FONT, H, LIGHT, W, clamp01, easeInOutCubic, easeOutBack, easeOutCubic, sec } from "../lib/core";
import { Burst, Confetti, Flash, PixelFrame, PixelIcon, Sfx, Stars, punch, shake } from "../lib/fx";
import { Box, Shot, SHOTS, target } from "../lib/shot";
import { STAGE, Sprite, Who } from "../lib/sprite";
import { BigTitle, OCT, SkillTree } from "../lib/world";

const VOICE = { blue: "blue-direct", black: "black-design" } as const;
const MAN: Record<string, Record<string, { sec: number }>> = { blue: blueMan, black: blackMan };
type Line = { id: string; who: string; text: string; mark?: string };
const LINES = Object.fromEntries((adJson.lines as Line[]).map((l) => [l.id, l]));
const lenOf = (id: string) => { const w = LINES[id].who; return w === "both" ? Math.max(sec(MAN.blue[id].sec), sec(MAN.black[id].sec)) : sec(MAN[w][id].sec); };

// ---------- 时间表 ----------
// 样片部分（用户认可过）：固定帧；之后每句 = 上一句结束 + 停顿（帧）
const FIXED: Record<string, number> = { a01: 54, a02: 152, a03: 226, a04: 312 };
const GAP: Record<string, number> = { a05: 56, a06: 30, a07: 34, a08: 66, a09: 50, a10: 50, a11: 40, a12: 46, a13: 64, a14: 30, a15: 36 };
const ORDER = ["a01", "a02", "a03", "a04", "a05", "a06", "a07", "a08", "a09", "a10", "a11", "a12", "a13", "a14", "a15"];
const AT: Record<string, number> = {};
ORDER.forEach((id, i) => { AT[id] = FIXED[id] ?? AT[ORDER[i - 1]] + lenOf(ORDER[i - 1]) + GAP[id]; });
const END_OF = (id: string) => AT[id] + lenOf(id);
export const AD_LEN = END_OF("a15") + 96;
// 样片里的动作时刻
const FALL = 128, IMPACT = FALL + 8, BLACK_IN = 140, PHONE_IN = 214, POP = 304;
// 后面各场
const LESSON_IN = END_OF("a04") + 20;            // 手机第二次升上来：一课
const TREE_IN = AT.a08 - 30;                     // 技能树面板
const SKILL_IN = AT.a09 - 26;                    // 技能页“去哪深入”
const LAB_IN = AT.a10 - 30;                      // 你来当调度器
const BOSS_IN = AT.a12 - 24;                     // 结业挑战已点亮
const TITLE_IN = AT.a13 - 6;                     // 落版

const FLOOR = 1880;
const FIG_H = 1150;

// ---------- 屏幕上的字：[mark] 换颜色；按标点断行（一行最多 9 个字，放不下就把字缩到 84 px、一行 10 个字）；和配音一字不差 ----------
const KEY = { blue: LIGHT.accent, black: "#7a5bd6", both: LIGHT.gold };
function wrap(text: string, max: number): string[] {
  const chunks = text.match(/[^，。？！、…]+[，。？！、…]*/g) ?? [text];
  const out: string[] = [];
  for (const c of chunks) {
    const last = out[out.length - 1];
    if (last !== undefined && [...last].length + [...c].length <= max) out[out.length - 1] = last + c;
    else out.push(c);
  }
  return out;
}
function layout(text: string) {
  const a = wrap(text, 9), b = wrap(text, 10);
  return b.length < a.length || a.some((l) => [...l].length > 9) ? { lines: b, fs: 84 } : { lines: a, fs: 96 };
}
const Caption: React.FC<{ id: string; at: number; until: number }> = ({ id, at, until }) => {
  const f = useCurrentFrame();
  if (f < at - 2 || f >= until) return null;
  const l = LINES[id];
  const who = l.who as "blue" | "black" | "both";
  const s = punch(f, at - 2, 6, 0.7);
  const mark = l.mark ?? "";
  const { lines, fs } = id === "a14" ? { lines: wrap(l.text, 10), fs: 72 } : layout(l.text);
  const paint = (t: string) => {
    const i = mark ? t.indexOf(mark) : -1;
    return i < 0 ? t : <>{t.slice(0, i)}<span style={{ color: KEY[who] }}>{mark}</span>{t.slice(i + mark.length)}</>;
  };
  return (
    <div style={{ position: "absolute", left: 0, width: W, top: id === "a14" ? 110 : 150, display: "flex", flexDirection: "column", alignItems: "center", transform: `scale(${s})`, transformOrigin: "50% 100%" }}>
      <div style={{ fontFamily: FONT, fontSize: 48, color: "#fff", background: who === "blue" ? LIGHT.accent : LIGHT.ink, padding: "8px 24px", marginBottom: 20 }}>{who === "blue" ? "鲸鱼姐姐" : who === "black" ? "鲸鱼妹妹" : "鲸鱼姐妹"}</div>
      <PixelFrame px={6} rim={LIGHT.rim} deep={LIGHT.rimDeep} fill={LIGHT.panel} style={{ padding: "26px 44px" }}>
        {lines.map((t, k) => <div key={k} style={{ fontFamily: FONT, fontSize: fs, lineHeight: 1.2, color: LIGHT.ink, whiteSpace: "nowrap" }}>{paint(t)}</div>)}
      </PixelFrame>
    </div>
  );
};

/** 说话时立绘跟着声音一上一下（取配音每帧的音量） */
function useTalk(who: "blue" | "black") {
  const f = useCurrentFrame();
  const mine = ORDER.filter((id) => LINES[id].who === who || LINES[id].who === "both");
  const cur = mine.find((id) => f >= AT[id] && f < END_OF(id) + 2) ?? mine[0];
  const data = useAudioData(staticFile(`build/voice/${VOICE[who]}/${cur}.wav`));
  if (!data || f < AT[cur]) return 0;
  const ch = data.channelWaveforms[0], sr = data.sampleRate;
  const i0 = Math.floor(((f - AT[cur]) / 30) * sr), n = Math.floor(sr / 30);
  if (i0 >= ch.length) return 0;
  let s = 0;
  for (let i = i0; i < Math.min(ch.length, i0 + n); i++) s += ch[i] * ch[i];
  return Math.min(1, Math.sqrt(s / n) * 5);
}

const Portrait: React.FC<{ who: "blue" | "black"; x: number; h: number; talk: number; sx?: number; sy?: number; rot?: number }> = ({ who, x, h, talk, sx = 1, sy = 1, rot = 0 }) => {
  const f = useCurrentFrame();
  const w = h * (who === "blue" ? 664 / 1200 : 593 / 1200);
  const breathe = 1 + 0.006 * Math.sin(f / 14 + (who === "blue" ? 0 : 2));
  return (
    <Img src={staticFile(`cast/portraits/${who}.webp`)} style={{
      position: "absolute", left: x - w / 2, top: FLOOR + 10 - h, width: w, height: h,
      transform: `rotate(${rot}deg) scale(${sx}, ${sy * breathe * (1 + 0.03 * talk)})`, transformOrigin: "50% 100%",
    }} />
  );
};

// ---------- 课本塔（样片）：书脊上是技能树里真实的技能名，颜色取它所在领域的颜色 ----------
const BOOKS = ["操作系统", "计算机组成原理", "数据结构", "C/C++与底层编程", "程序设计基础", "证明方法与离散结构", "线性代数", "算法分析与设计", "网络协议、路由与传输", "深度学习", "数据库内核与查询优化", "分布式系统"];
const TREE = treeJson as { lanes: { id: string; color: string }[]; skills: { name: string; lane: string }[] };
const bookColor = (name: string, i: number) => {
  const sk = TREE.skills.find((s) => s.name === name);
  const lane = sk && TREE.lanes.find((l) => l.id === sk.lane);
  return lane?.color ?? ["#1f9d74", "#d9539a", "#2f7fd1", "#7a5bd6", "#e0a210"][i % 5];
};
const BOOK_W = 460, BOOK_H = 70, TOWER_X = 560;
export const Book: React.FC<{ name: string; i: number; style?: React.CSSProperties }> = ({ name, i, style }) => (
  <div style={{ position: "absolute", width: BOOK_W, height: BOOK_H, ...style }}>
    <PixelFrame px={6} rim={LIGHT.ink} deep={LIGHT.ink} fill={bookColor(name, i)} style={{ width: "100%", height: "100%", display: "flex", alignItems: "center" }}>
      <div style={{ width: 22, alignSelf: "stretch", background: "rgba(255,255,255,0.25)", marginRight: 16 }} />
      <span style={{ fontFamily: FONT, fontSize: 36, color: "#fff", whiteSpace: "nowrap", textShadow: "3px 3px 0 rgba(0,0,0,0.35)" }}>{name}</span>
      <div style={{ marginLeft: "auto", width: 30, alignSelf: "stretch", background: LIGHT.panel, borderLeft: `6px solid ${LIGHT.line}` }} />
    </PixelFrame>
  </div>
);
const wob = (i: number) => Math.round((random(`bk${i}`) * 2 - 1) * 22);
const BookTower: React.FC = () => {
  const f = useCurrentFrame();
  if (f >= IMPACT) return null;
  const tilt = f < 111 ? 0 : f < FALL ? Math.sin((f - 111) / 2.2) * 2.5 * ((f - 111) / 17) : -80 * Math.pow(clamp01((f - FALL) / 8), 2);
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: W, height: H, transform: `rotate(${tilt}deg)`, transformOrigin: `${TOWER_X - 20}px ${FLOOR}px` }}>
      {BOOKS.map((name, i) => {
        const land = 6 + i * 4;
        if (f < land - 8) return null;
        const t = clamp01((f - (land - 8)) / 8);
        const y = FLOOR - (i + 1) * BOOK_H;
        const bounce = f >= land && f < land + 4 ? -6 * Math.sin(((f - land) / 4) * Math.PI) : 0;
        return <Book key={i} name={name} i={i} style={{ left: TOWER_X + wob(i), top: -200 + (y + 200) * t * t + bounce }} />;
      })}
    </div>
  );
};
const FLAT = 0.28;
const BookPile: React.FC<{ out: number }> = ({ out }) => {
  const f = useCurrentFrame();
  if (f < IMPACT || out >= 1) return null;
  const topOfBlue = FLOOR - FIG_H * FLAT;
  return (
    <>
      {BOOKS.map((name, i) => {
        const onTop = i < 6;
        const col = onTop ? i % 2 : (i - 6) % 3, row = onTop ? Math.floor(i / 2) : Math.floor((i - 6) / 3);
        const x = onTop ? 20 + col * 250 + wob(i + 20) : 540 + col * 170 + wob(i + 40), y = onTop ? topOfBlue + 16 - BOOK_H - row * 58 : FLOOR - BOOK_H - row * 62;
        const r = (random(`pr${i}`) * 2 - 1) * 9;
        const dx = (random(`fx${i}`) * 2 - 1) * 700 * out, dy = -900 * out + 2000 * out * out;
        return <Book key={i} name={name} i={i} style={{ left: x + dx, top: y + dy, transform: `rotate(${r + 200 * out * (i % 2 ? 1 : -1)}deg)` }} />;
      })}
    </>
  );
};

// ---------- 像素手机：游戏手机版的真实截图放进去；screen = 屏幕上显示的内容 ----------
const SW = 600;
const PhoneFrame: React.FC<{ x: number; y: number; h: number; children: React.ReactNode }> = ({ x, y, h, children }) => (
  <div style={{ position: "absolute", left: x - SW / 2 - 30, top: y }}>
    <PixelFrame px={6} rim={LIGHT.ink} deep="#000" fill={LIGHT.ink} style={{ padding: "60px 24px 0", width: SW + 60, height: h + 126, boxShadow: "18px 18px 0 rgba(31,29,51,0.25)" }}>
      <div style={{ position: "absolute", left: "50%", top: 24, width: 110, height: 14, marginLeft: -55, background: "#47445f" }} />
      <div style={{ position: "relative", width: SW, height: h, overflow: "hidden", background: LIGHT.bg }}>{children}</div>
    </PixelFrame>
  </div>
);
/** 手机里放一张截图的一块（crop 用截图的 CSS px）；返回屏幕高度给外框用 */
const phoneShot = (name: string, crop: Box) => ({ h: crop.h * (SW / crop.w), el: <Shot name={name} crop={crop} width={SW} /> });

/** 样片里的远征路线屏：“开始”那块弹一下 */
const RouteScreen: React.FC = () => {
  const f = useCurrentFrame();
  const view = { x: 0, y: 40, w: 390, h: 600 }, k = SW / 390;
  const pop = punch(f, PHONE_IN + 22, 7, 0.6);
  const card = { x: 96, y: 238, w: 200, h: 146 };
  return (
    <>
      <Shot name="route-phone-light" crop={view} width={SW} />
      {f >= PHONE_IN + 22 && <div style={{ position: "absolute", left: (card.x - view.x) * k, top: (card.y - view.y) * k, transform: `scale(${pop})`, transformOrigin: "50% 100%" }}><Shot name="route-phone-light" crop={card} width={card.w * k} /></div>}
    </>
  );
};

/** 一课：先猜（选错）→ 红色反馈栏 → 讲解卡 → 结算页三颗星弹出来 */
const LESSON_VIEW: Box = { x: 0, y: 100, w: 390, h: 650 };
const LessonScreen: React.FC = () => {
  const f = useCurrentFrame();
  const wrongAt = AT.a05 + 40;                  // “啊，错了”
  const cardAt = AT.a06 + 44;                   // “讲解会告诉你错在哪”
  const doneAt = AT.a07 - 18;
  const L = (s: string) => `lesson-phone-light-${s}`;
  const name = f < AT.a05 ? L("00") : f < wrongAt ? L("wrong-pick") : f < cardAt ? L("wrong") : f < doneAt ? L("03") : L("done-nostars");
  const k = SW / LESSON_VIEW.w;
  const starsAt = [doneAt + 10, doneAt + 18, doneAt + 26];
  return (
    <>
      <Shot name={name} crop={LESSON_VIEW} width={SW} />
      {f >= doneAt && [0, 1, 2].map((i) => {
        const b = target(L("done"), "stars", i);
        if (f < starsAt[i]) return null;
        const t = clamp01((f - starsAt[i]) / 8), size = 72;
        const cx = (b.x + b.w / 2 - LESSON_VIEW.x) * k, cy = (b.y + b.h / 2 - LESSON_VIEW.y) * k;
        return <div key={i} style={{ position: "absolute", left: cx - size / 2, top: cy - size / 2, transform: `scale(${0.2 + 0.8 * easeOutBack(t, 2.6)}) rotate(${-25 * (1 - t)}deg)`, opacity: Math.min(1, t * 3) }}><PixelIcon name="star" size={size} color={LIGHT.gold} style={{ filter: `drop-shadow(0 5px 0 ${LIGHT.goldEdge})` }} /></div>;
      })}
      {f >= doneAt && (SHOTS[L("done")].sprites as { who: Who; action: string; x: number; y: number; w: number; h: number; flip: boolean }[]).map((s, i) => (
        <Sprite key={i} who={s.who} seq={[s.action]} from={doneAt} footX={(s.x + s.w / 2 - LESSON_VIEW.x) * k} footY={(s.y + s.h - LESSON_VIEW.y) * k} scale={(s.w / STAGE[s.who].w) * k} flip={s.flip} />
      ))}
    </>
  );
};

/** 技能页的一章：点开“去哪深入”，教材那几行用金框圈出来 */
const SkillScreen: React.FC = () => {
  const f = useCurrentFrame();
  const m = SHOTS["skill-light-ch1"], k = SW / m.w;
  const hl = { x: 12, y: 160, w: 334, h: 118 };
  const on = f >= AT.a09 + 30;                  // “去哪本书”
  const blink = on ? 0.6 + 0.4 * Math.abs(Math.sin((f - AT.a09) / 6)) : 0;
  return (
    <>
      <Shot name="skill-light-ch1" width={SW} />
      {on && <div style={{ position: "absolute", left: hl.x * k, top: hl.y * k, width: hl.w * k, height: hl.h * k, border: `8px solid ${LIGHT.gold}`, opacity: blink }} />}
    </>
  );
};

/** 你来当调度器：T1 读 x → T2 读 x → T1 加一写回 → T2 加一写回，最后 x = 1；两句台词里一步步走完 */
const LabScreen: React.FC = () => {
  const f = useCurrentFrame();
  const steps = [0, 1, 2, 3, 4, 5, 6];
  const t0 = AT.a10 - 10, stepLen = Math.round((lenOf("a10") - 6) / 6);
  const k = Math.max(0, Math.min(6, Math.floor((f - t0) / stepLen)));
  const name = `lab-light-threads-${steps[k]}`;
  const m = SHOTS[name];
  const done = f >= t0 + 6 * stepLen;
  return (
    <>
      <Shot name={name} width={SW} />
      {done && <div style={{ position: "absolute", inset: 0, background: LIGHT.bad, opacity: 0.25 * Math.max(0, 1 - (f - t0 - 6 * stepLen) / 12) }} />}
      <div style={{ display: "none" }}>{m.h}</div>
    </>
  );
};

/** 结业挑战结算：“程序设计基础 已点亮”，截图里藏起来的姐妹在原位放施法、跳舞 */
const BOSS_VIEW: Box = { x: 0, y: 110, w: 390, h: 300 };
const BossScreen: React.FC = () => {
  const k = SW / BOSS_VIEW.w;
  const sp = SHOTS["boss-light-done"].sprites as { who: Who; action: string; x: number; y: number; w: number; h: number; flip: boolean }[];
  return (
    <>
      <Shot name="boss-light-done" crop={BOSS_VIEW} width={SW} />
      {sp.map((s, i) => <Sprite key={i} who={s.who} seq={[s.action]} from={BOSS_IN} footX={(s.x + s.w / 2 - BOSS_VIEW.x) * k} footY={(s.y + s.h - BOSS_VIEW.y) * k} scale={(s.w / STAGE[s.who].w) * k} flip={s.flip} />)}
    </>
  );
};

/** 技能树面板：游戏的夜空技能树（真实的 183 个技能和必须前置），妹妹说着话一层层亮起来，远征那条路是金线 */
const TreePanel: React.FC = () => {
  const f = useCurrentFrame();
  const s = punch(f, TREE_IN, 8, 0.6);
  const p = clamp01((f - AT.a08 - 10) / (lenOf("a08") + 10));
  const box = { x: 60, y: 660, w: 960, h: 1160 };
  const inner = { x: box.x + 40, y: box.y + 60, w: box.w - 80, h: box.h - 120 };
  return (
    <div style={{ position: "absolute", inset: 0, transform: `scale(${s})`, transformOrigin: `${W / 2}px ${box.y + box.h / 2}px` }}>
      <PixelFrame px={8} rim={LIGHT.ink} deep="#000" fill={DARK.bg} style={{ position: "absolute", left: box.x, top: box.y, width: box.w, height: box.h, boxShadow: "18px 18px 0 rgba(31,29,51,0.25)", overflow: "hidden" }}>
        <div style={{ position: "absolute", inset: 0, transform: `translate(${-box.x - 8}px, ${-box.y - 8}px)` }}>
          <Stars n={110} seed="adtree" opacity={0.45} />
          <SkillTree box={inner} p={p} routeP={clamp01((f - AT.a08) / 30)} star={18} />
        </div>
      </PixelFrame>
    </div>
  );
};

const Spot: React.FC<{ x: number; at: number; until: number; color: string }> = ({ x, at, until, color }) => {
  const f = useCurrentFrame();
  if (f < at - 4 || f >= until) return null;
  const s = punch(f, at - 4, 8, 0.3) * (f > until - 6 ? clamp01((until - f) / 6) : 1);
  const r = 300;
  return <div style={{ position: "absolute", left: x - r, top: FLOOR - FIG_H * 0.62 - r, width: 2 * r, height: 2 * r, background: color, clipPath: OCT, transform: `scale(${s})` }} />;
};

export const Backdrop: React.FC = () => {
  const f = useCurrentFrame();
  const icons = ["star", "book-open", "lightbulb", "zap", "trophy", "map", "fire", "sparkle"];
  return (
    <AbsoluteFill style={{ background: LIGHT.bg }}>
      <AbsoluteFill style={{ backgroundImage: `linear-gradient(${LIGHT.bg2} 6px, transparent 6px), linear-gradient(90deg, ${LIGHT.bg2} 6px, transparent 6px)`, backgroundSize: "96px 96px", opacity: 0.55 }} />
      {Array.from({ length: 16 }, (_, i) => {
        const x = random(`ix${i}`) * W, y0 = random(`iy${i}`) * H;
        const y = ((y0 - f * (0.6 + random(`iv${i}`))) % (H + 100) + H + 100) % (H + 100) - 100;
        return <PixelIcon key={i} name={icons[i % icons.length]} size={72} color={LIGHT.line} style={{ position: "absolute", left: Math.round(x), top: Math.round(y) }} />;
      })}
      <div style={{ position: "absolute", left: 0, right: 0, top: FLOOR, bottom: 0, background: LIGHT.bg2, borderTop: `6px solid ${LIGHT.rim}` }} />
    </AbsoluteFill>
  );
};

/** 落版：标题砸下来（两人一起喊“计算机大学习！”），信息一行行出来，署名在最下面 */
const AD_INFO = ["免费 · 源码公开 · 非商用", "安卓 · Windows · 网页版", "下载：B 站简介，或 GitHub 搜“计算机大学习”"];
const AD_CREDITS = ["导师角色设计 ZipZipPipe（CC BY-NC 4.0）", "配音由 Breeze TTS 2 合成 · 音乐 Happy Vibes · Ruskerdax（CC0）", "像素字体 Fusion Pixel（OFL）"];
const EndInfo: React.FC = () => {
  const f = useCurrentFrame();
  const infoAt = AT.a14 + 10;
  return (
    <>
      <BigTitle at={TITLE_IN} y={560} size={132} color={LIGHT.ink} shadow={LIGHT.gold} />
      <Burst at={TITLE_IN} x={W / 2} y={650} n={30} colors={[LIGHT.gold, LIGHT.accent, LIGHT.pink, "#1baf7a"]} speed={800} size={16} seed="adtitle" />
      {AD_INFO.map((t, i) => f >= infoAt + i * 14 && (
        <div key={i} style={{ position: "absolute", left: 0, width: W, top: 770 + i * 84, textAlign: "center", fontFamily: FONT, fontSize: [60, 48, 42][i], color: i === 0 ? LIGHT.accent : LIGHT.ink, whiteSpace: "nowrap", transform: `translateY(${(1 - easeOutBack(clamp01((f - infoAt - i * 14) / 7), 2)) * 24}px)` }}>{t}</div>
      ))}
      {f >= infoAt + 40 && AD_CREDITS.map((c, i) => <div key={i} style={{ position: "absolute", left: 0, width: W, top: 1040 + i * 46, textAlign: "center", fontFamily: FONT, fontSize: 30, color: LIGHT.ink2, whiteSpace: "nowrap" }}>{c}</div>)}
    </>
  );
};

export const Ad: React.FC = () => {
  const f = useCurrentFrame();
  const tBlue = useTalk("blue"), tBlack = useTalk("black");
  const sh = shake(f, IMPACT, 10, 18);
  // —— 姐姐：被砸扁（IMPACT 起），POP 时弹回来；说“几分钟？那我也行！”后跳一下 ——
  const flat = f >= IMPACT && f < POP;
  const popT = clamp01((f - POP) / 10);
  const blueSY = flat ? FLAT : f >= POP ? FLAT + (1 - FLAT) * easeOutBack(popT, 3) : 1;
  const blueSX = flat ? 1.3 : f >= POP ? 1.3 - 0.3 * easeOutCubic(popT) : 1;
  const hopAt = (at: number) => { const t = f - at; return t >= 0 && t < 18 ? -Math.abs(Math.sin((t / 9) * Math.PI)) * 50 : 0; };
  const hop = hopAt(END_OF("a04") - 6) + hopAt(END_OF("a07") - 10) + hopAt(BOSS_IN + 10);
  // “啊，错了”：姐姐缩一下、歪头
  const oops = f >= AT.a05 + 40 && f < AT.a05 + 64 ? Math.sin(((f - AT.a05 - 40) / 24) * Math.PI) : 0;
  // —— 站位：样片里姐姐在左、妹妹从右边滑进来；有手机/面板的场景两人退到两边 ——
  const side = interpolate(f, [LESSON_IN - 10, LESSON_IN + 10, TITLE_IN - 12, TITLE_IN + 6], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: easeInOutCubic });
  const blueX = 300 - 150 * side, blackBase = 790 + 140 * side;
  // 落版：两人往下沉，只露上半身，信息字不压在人身上
  const sink = interpolate(f, [TITLE_IN - 12, TITLE_IN + 6], [0, 640], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: easeInOutCubic });
  const blackX = blackBase + 600 * (1 - easeOutBack(clamp01((f - BLACK_IN) / 12), 1.4));
  // —— 中间的屏 ——
  const phoneY1 = f < POP - 6 ? interpolate(f, [PHONE_IN, PHONE_IN + 10], [H + 40, 560], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: easeOutCubic })
    : interpolate(f, [POP - 6, POP + 4], [560, H + 40], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const rise = (from: number, to: number, y: number) => interpolate(f, [from, from + 10, to - 8, to], [H + 40, y, y, H + 40], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: easeOutCubic });
  const scenes: { from: number; to: number; y: number; shot: { h: number; el: React.ReactNode } }[] = [
    { from: LESSON_IN, to: TREE_IN, y: 600, shot: { h: LESSON_VIEW.h * (SW / LESSON_VIEW.w), el: <LessonScreen /> } },
    { from: SKILL_IN, to: LAB_IN, y: 640, shot: phoneShot("skill-light-ch1", { x: 0, y: 0, w: SHOTS["skill-light-ch1"].w, h: SHOTS["skill-light-ch1"].h }) },
    { from: LAB_IN, to: BOSS_IN, y: 600, shot: { h: SHOTS["lab-light-threads-0"].h * (SW / SHOTS["lab-light-threads-0"].w), el: <LabScreen /> } },
    { from: BOSS_IN, to: TITLE_IN, y: 640, shot: { h: BOSS_VIEW.h * (SW / BOSS_VIEW.w), el: <BossScreen /> } },
  ];
  scenes[1].shot = { h: scenes[1].shot.h, el: <SkillScreen /> };
  const until = (id: string) => { const i = ORDER.indexOf(id); return i + 1 < ORDER.length ? AT[ORDER[i + 1]] - 2 : END_OF(id) + 60; };
  const speaking = (fr: number) => ORDER.some((id) => fr >= AT[id] - 4 && fr < END_OF(id) + 4);
  const captionIds = ORDER.filter((id) => id !== "a13");
  return (
    <AbsoluteFill>
      <Backdrop />
      {ORDER.filter((id) => LINES[id].who !== "both").map((id) => { const who = LINES[id].who; return <Spot key={id} x={who === "blue" ? blueX : blackX} at={AT[id]} until={Math.min(until(id), END_OF(id) + 10)} color={who === "blue" ? "#dfe3fa" : "#e6ddf3"} />; })}
      <AbsoluteFill style={{ transform: `translate(${sh.x}px, ${sh.y}px)` }}>
        <div style={{ position: "absolute", left: 0, top: hop + oops * 30 + sink, width: W, height: H }}>
          <Portrait who="blue" x={blueX} h={FIG_H} talk={tBlue} sx={blueSX} sy={blueSY * (1 - 0.04 * oops)} rot={-6 * oops} />
        </div>
        {f >= BLACK_IN && <div style={{ position: "absolute", left: 0, top: sink, width: W, height: H }}><Portrait who="black" x={blackX} h={FIG_H} talk={tBlack} /></div>}
        <BookTower />
        <BookPile out={f >= POP ? easeOutCubic(clamp01((f - POP) / 18)) : 0} />
        <Burst at={IMPACT} x={300} y={FLOOR - 60} n={20} colors={[LIGHT.line, LIGHT.edge, "#fff"]} speed={500} size={16} seed="dust" />
        {f >= IMPACT + 6 && f < POP && [0, 1, 2].map((i) => {
          const a = (f - IMPACT) / 8 + (i * Math.PI * 2) / 3;
          return <PixelIcon key={i} name="star" size={48} color={LIGHT.gold} style={{ position: "absolute", left: 300 + Math.cos(a) * 120 - 24, top: FLOOR - FIG_H * FLAT - 3 * 58 - 60 + Math.sin(a) * 30 }} />;
        })}
        {f >= PHONE_IN && f < POP + 6 && <PhoneFrame x={430} y={phoneY1} h={600 * SW / 390}><RouteScreen /></PhoneFrame>}
        {scenes.map((s, i) => f >= s.from && f < s.to && <PhoneFrame key={i} x={W / 2} y={rise(s.from, s.to, s.y)} h={s.shot.h}>{s.shot.el}</PhoneFrame>)}
        {f >= TREE_IN && f < SKILL_IN && <TreePanel />}
        {/* 打卡：“明天我还来！”时营地的火苗牌子弹出来 */}
        {f >= AT.a07 + 10 && f < TREE_IN && <div style={{ position: "absolute", left: W / 2 - 200, top: 560, transform: `scale(${punch(f, AT.a07 + 10, 6, 0.6)})` }}><Shot name="streak-light-2" width={400} style={{ imageRendering: "pixelated" }} /></div>}
        {f >= BOSS_IN && f < TITLE_IN && <Confetti at={BOSS_IN + 4} n={90} colors={[LIGHT.gold, LIGHT.accent, LIGHT.pink, "#1baf7a"]} />}
        {f >= TITLE_IN && <EndInfo />}
        {/* 最后一句：姐姐从右边探头，营地火苗 +1 */}
        {f >= AT.a15 - 8 && <div style={{ position: "absolute", left: W / 2 - 210, top: 1196, transform: `scale(${f >= AT.a15 + 40 ? punch(f, AT.a15 + 40, 6, 0.7) : punch(f, AT.a15 - 8, 6, 0.7)})` }}><Shot name={f >= AT.a15 + 40 ? "streak-light-31" : "streak-light-30"} width={420} style={{ imageRendering: "pixelated" }} /></div>}
        <Burst at={AT.a15 + 40} x={W / 2} y={1290} n={18} colors={["#ff9a3c", LIGHT.gold, "#fff1b8"]} speed={360} size={12} seed="adplus" />
      </AbsoluteFill>
      {captionIds.map((id) => <Caption key={id} id={id} at={AT[id]} until={until(id)} />)}
      <Flash at={TITLE_IN} len={6} color="#fff" max={0.8} />
      {/* 声音：垫底曲说话时压低，落版后淡出 */}
      <Audio src={staticFile("build/music/ad.wav")} volume={(fr) => (speaking(fr) ? 0.16 : 0.32) * interpolate(fr, [AD_LEN - 40, AD_LEN], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })} />
      {ORDER.flatMap((id) => (LINES[id].who === "both" ? ["blue", "black"] : [LINES[id].who])
        .map((who) => <Sequence key={`${id}-${who}`} from={AT[id]} layout="none"><Audio src={staticFile(`build/voice/${VOICE[who as "blue" | "black"]}/${id}.wav`)} volume={LINES[id].who === "both" ? 0.75 : 1} /></Sequence>))}
      {BOOKS.map((_, i) => <Sfx key={i} at={6 + i * 4} name="thud" volume={0.25} />)}
      <Sfx at={IMPACT} name="thud" volume={1} />
      <Sfx at={BLACK_IN} name="whoosh" volume={0.5} />
      <Sfx at={PHONE_IN} name="whoosh" volume={0.5} />
      <Sfx at={PHONE_IN + 22} name="pop" volume={0.5} />
      <Sfx at={POP - 6} name="whoosh" volume={0.35} />
      <Sfx at={POP} name="unlock" volume={0.6} />
      {[LESSON_IN, SKILL_IN, LAB_IN, BOSS_IN].map((t, i) => <Sfx key={`w${i}`} at={t} name="whoosh" volume={0.4} />)}
      <Sfx at={AT.a05 + 20} name="select" volume={0.5} />
      <Sfx at={AT.a05 + 40} name="wrong" volume={0.6} />
      {[0, 8, 16].map((d, i) => <Sfx key={`s${i}`} at={AT.a07 - 8 + d} name="star" volume={0.5} />)}
      <Sfx at={AT.a07 + 10} name="pop" volume={0.5} />
      <Sfx at={TREE_IN} name="unlock" volume={0.5} />
      {[1, 2, 3, 4, 5].map((k) => <Sfx key={`t${k}`} at={AT.a10 - 10 + k * Math.round((lenOf("a10") - 6) / 6)} name="tap" volume={0.5} />)}
      <Sfx at={AT.a10 - 10 + 6 * Math.round((lenOf("a10") - 6) / 6)} name="wrong" volume={0.6} />
      <Sfx at={BOSS_IN} name="fanfare" volume={0.6} />
      <Sfx at={TITLE_IN} name="thud" volume={0.9} />
      <Sfx at={AT.a15 + 40} name="star" volume={0.6} />
    </AbsoluteFill>
  );
};
