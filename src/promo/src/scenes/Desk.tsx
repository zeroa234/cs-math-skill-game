// 真实游戏画面，同一个像素窗口连着演：开场对白（cast）→ 选远征、看路线（route）→ 一课的先猜 / 讲解 / 练习（lesson）
// → 你来当调度器（race）→ 你来当页面置换算法（replace）。
// 截图由 scripts/promo/capture-game.mjs 拍（深色主题、减少动画），按钮、选项、精灵的位置也是那时量的（shots.json）；
// 点击都按游戏里的标准答案点（race 的 solution、replace 的 solution），截图就是点完那一下的真实页面。
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Box, C, F, PX, SHOTS, beat, box, boxes, say, sayEnd, steps, tw, w } from "../lib/core";
import { AppWindow, CAM0, Cam, Cursor, Glow, Sfx, Shot, Tag, TypeBlips, TypeText, WIN, camAt, frame, project } from "../lib/ui";

const mid = (b: Box) => ({ x: b.x + b.w / 2, y: b.y + b.h / 2 });
/** 时间表里 f 帧时该显示哪张截图 */
const current = (f: number, list: [number, string][]) => list.reduce((cur, [t, n]) => (f >= t ? n : cur), list[0][1]);
/** 视口坐标的点 → 窗口里的位置（给 Tag 用） */
const at = (p: { x: number; y: number }, cam: Cam) => project(p, cam);

export function deskTimes() {
  const A = beat("cast").start, Z = beat("lab").start;
  const clickStart = w("cast", "从零开始") - 6, clickLine = w("cast", "一次一小课") - 14;
  const clickGo = w("route", "选好目标") + 16, routeIn = w("route", "路线自动排好");
  const lesson = beat("lesson").start, tGuess = w("lesson", "先猜"), tCard = w("lesson", "再看"), tItem = w("lesson", "再做"), s2 = say("lesson", 1);
  const pickOpt = w("lesson", "不计分", true) + 4, clickCheck = w("lesson", "答完") + 2;
  const race = beat("race").start, raceClicks0 = w("race", "两个线程") + 10, raceClicks1 = w("race", "竞态") - 4;
  const raceCheck = sayEnd("race") + 2;
  const rep = beat("replace").start, repClicks0 = w("replace", "每次缺页"), repClicks1 = sayEnd("replace") + 6;
  return { A, Z, clickStart, clickLine, clickGo, routeIn, lesson, tGuess, tCard, tItem, s2, pickOpt, clickCheck, race, raceClicks0, raceClicks1, raceCheck, rep, repClicks0, repClicks1 };
}

export const Desk: React.FC = () => {
  const f = useCurrentFrame();
  const t = deskTimes();
  if (f < t.A - 14 || f > t.Z + 14) return null;
  const race = SHOTS.race as unknown as { solution: number[] }, repSol = (SHOTS.replace as unknown as { solution: number[] }).solution;
  const raceAt = race.solution.map((_, i) => Math.round(t.raceClicks0 + ((t.raceClicks1 - t.raceClicks0) * i) / (race.solution.length - 1)));
  const repAt = repSol.map((_, i) => Math.round(t.repClicks0 + ((t.repClicks1 - t.repClicks0) * i) / (repSol.length - 1)));

  // ── 截图时间表 ──
  const list: [number, string][] = [
    [t.A, "intro-title"], [t.clickStart + 3, "intro-l0"], [t.clickLine + 3, "intro-l2"],
    [beat("route").start, "pick"], [t.routeIn, "route"],
    [t.lesson, "lesson-guess"], [t.tCard, "lesson-card"], [t.tItem, "lesson-item-right"], [t.s2 - 2, "lesson-guess"], [t.pickOpt, "lesson-guess-pick"], [t.clickCheck + 2, "lesson-guess-wrong"],
    [t.race, "race-0"], ...raceAt.map((c, i) => [c + 2, `race-${i + 1}`] as [number, string]), [t.raceCheck + 2, "race-done"],
    [t.rep, "replace-0"], ...repAt.map((c, i) => [c + 2, `replace-${i + 1}`] as [number, string]),
  ];
  const shot = current(f, list);
  const since = list.filter(([, n]) => n === shot).reduce((a, [tt]) => (f >= tt ? tt : a), 0);

  // ── 镜头 ──
  const raceCam: Cam = { x: 700, y: 330, z: 1.12 }, repCam: Cam = { x: 700, y: 330, z: 1.12 };
  const routeBanner = box("route", "banner");
  const cam = camAt(f, [
    [t.A, CAM0], [t.clickStart, { x: 608, y: 360, z: 1.06 }], [t.clickStart + 6, CAM0], [t.clickLine, { x: 608, y: 400, z: 1.08 }],
    [beat("route").start - 1, { x: 608, y: 400, z: 1.08 }], [beat("route").start, CAM0], [t.routeIn - 1, CAM0],
    [t.routeIn, { x: 608, y: routeBanner.y + 150, z: 1.25 }], [w("route", "五站") - 10, { x: 608, y: routeBanner.y + 180, z: 1.18 }],
    [beat("lesson").start - 2, { x: 608, y: 1180, z: 1.0 }],
    [beat("lesson").start, CAM0], [t.s2 - 3, CAM0], [t.s2 + 8, { x: 640, y: 300, z: 1.12 }], [t.clickCheck, { x: 640, y: 300, z: 1.12 }],
    [t.clickCheck + 14, { x: 608, y: 400, z: 1.06 }], [t.race - 1, { x: 608, y: 400, z: 1.06 }],
    [t.race, raceCam], [raceAt.at(-1)! + 2, raceCam], [t.raceCheck - 6, CAM0], [t.rep - 1, CAM0],
    [t.rep, repCam], [beat("lab").start, repCam],
  ]);

  // ── 鼠标：各段一个 ──
  const btn = (s: string, k: string) => mid(box(s, k));
  const steps2 = boxes("race-0", "steps");
  const slotOf = (k: number) => {
    const labels = (SHOTS[`replace-${k}`] as unknown as { labels: string[] }).labels;
    const i = labels.indexOf(`换出 ${repSol[k]}`);
    return mid(boxes(`replace-${k}`, "slots")[i]);
  };
  const enter = tw(f, t.A - 10, 0.35), exit = tw(f, t.Z - 6, 0.3);
  const lessonSteps = [["先猜", t.tGuess, C.gold], ["再看", t.tCard, C.accent], ["再做", t.tItem, C.good]] as const;
  return (
    <AbsoluteFill>
      <AppWindow enter={enter} exit={exit}>
        <Shot name={shot} cam={cam} actFrom={since}
          acts={shot === "lesson-guess-wrong" ? { blue: ["coy", "idle"] } : shot === "race-done" || shot === "lesson-item-right" ? { blue: ["jump_start", "jump_air", "jump_land", "idle"] } : {}} />
        {/* 开场对白逐字打出（游戏 Intro.jsx 每 32 ms 一个字，每 3 个字一声 blip） */}
        {(shot === "intro-l0" || shot === "intro-l2") && (() => {
          const l = SHOTS[shot].line!;
          const p = project(l, cam);
          return <div style={{ position: "absolute", left: p.x, top: p.y, width: l.w * p.k, fontFamily: PX, fontSize: l.size * p.k, lineHeight: `${l.lh * p.k}px`, color: l.color }}>
            <TypeText text={l.text} at={since + 4} rate={1.1} />
          </div>;
        })()}
        {/* cast：两位导师 */}
        {shot.startsWith("intro-l") && (() => {
          // 立绘头顶（截图里妹妹在左、姐姐在右）；性格写法见 assets/cast/README.md
          const pb = at({ x: 175, y: 170 }, cam), pk = at({ x: 1040, y: 170 }, cam);
          return <>
            <Tag x={pb.x} y={pb.y} at={Math.max(w("cast", "鲸鱼娘"), t.clickStart + 6)} out={beat("route").start - 8} color="#9aa0c8" text="鲸鱼妹妹 · 沉稳" size={30} anchor="center" />
            <Tag x={pk.x} y={pk.y} at={Math.max(w("cast", "鲸鱼娘"), t.clickStart + 6) + 6} out={beat("route").start - 8} color="#6f8fff" text="鲸鱼姐姐 · 活泼" size={30} anchor="center" />
          </>;
        })()}
        {/* route：横幅（共 5 站）、5 站和每站几课（数据见 facts.json，和游戏排路线同一个函数） */}
        <Glow box={routeBanner} cam={cam} color={C.gold} o={shot === "route" ? steps(tw(f, w("route", "操作系统这一条") - 2, 0.15), 3) * (1 - tw(f, w("route", "五站") - 6, 0.2)) : 0} at={w("route", "操作系统这一条") - 2} />
        <StopStrip at={w("route", "五站")} total={w("route", "一百二十四课")} out={beat("lesson").start - 4} />
        {/* lesson：先猜、再看、再做 */}
        <div style={{ position: "absolute", right: 36, top: 120, display: "flex", gap: 18, opacity: f >= t.tGuess - 4 && f < t.s2 + 30 ? 1 : 0 }}>
          {lessonSteps.map(([txt, a, col], i) => {
            const on = f >= a && (i === 2 || f < lessonSteps[i + 1][1]) && f < t.s2;
            const o = steps(tw(f, a - 4, 0.15), 3);
            return <div key={txt} style={{ opacity: o, fontFamily: PX, fontSize: 42, lineHeight: "56px", padding: "4px 22px", color: on ? "#14142b" : C.ink,
              background: on ? col : C.panel, boxShadow: frame(6, col, "rgba(0,0,0,0.5)") }}>{i + 1} {txt}</div>;
          })}
        </div>
        {shot.startsWith("lesson-guess") && <>
          <Glow box={box("lesson-guess", "kind")} cam={cam} color={C.gold} o={steps(tw(f, w("lesson", "先猜一猜") - 2, 0.15), 3) * (1 - tw(f, t.pickOpt, 0.2))} pad={4} at={w("lesson", "先猜一猜")} />
          {(() => { const p = at({ x: 560, y: 142 }, cam); return <Tag x={p.x} y={p.y} at={w("lesson", "不计分")} out={t.clickCheck} color={C.gold} text="不计分" />; })()}
          {f >= t.clickCheck + 2 && <>
            <Glow box={box("lesson-guess-wrong", "bar")} cam={cam} color={C.bad} o={steps(tw(f, w("lesson", "对错") - 2, 0.15), 3)} pad={0} at={w("lesson", "对错")} />
            <Glow box={boxes("lesson-guess-wrong", "opts")[2]} cam={cam} color={C.good} o={steps(tw(f, w("lesson", "为什么") - 2, 0.15), 3)} pad={4} at={w("lesson", "为什么")} />
            {(() => { const p = at({ x: 1080, y: 520 }, cam); return <Tag x={p.x} y={p.y} at={w("lesson", "答错也不扣")} out={beat("race").start - 4} color={C.good} text="答错不扣任何东西" anchor="right" />; })()}
          </>}
        </>}
        <Cursor cam={cam} show={[t.lesson + 30, t.clickCheck + 20]} clicks={[t.pickOpt, t.clickCheck]}
          path={[[t.lesson + 30, { x: 1000, y: 520 }], [t.pickOpt - 8, mid(boxes("lesson-guess", "opts")[0])], [t.pickOpt + 6, mid(boxes("lesson-guess", "opts")[0])], [t.clickCheck - 6, btn("lesson-guess", "check")]]} />
        {/* cast / route 的点击 */}
        <Cursor cam={cam} show={[t.A + 20, t.clickLine + 16]} clicks={[t.clickStart, t.clickLine]}
          path={[[t.A + 20, { x: 900, y: 600 }], [t.clickStart - 8, btn("intro-title", "start")], [t.clickStart + 10, { x: 760, y: 560 }], [t.clickLine - 8, { x: 820, y: 620 }]]} />
        <Cursor cam={cam} show={[beat("route").start + 4, t.routeIn - 2]} clicks={[t.clickGo]}
          path={[[beat("route").start + 4, { x: 1000, y: 420 }], [t.clickGo - 8, btn("pick", "go")]]} />
        {/* race：你来当调度器 */}
        {shot.startsWith("race") && <>
          {(() => { const p = at({ x: 300, y: 80 }, cam); return <Tag x={p.x} y={p.y} at={w("race", "你来当调度器")} out={raceAt[0] + 10} color={C.accent} text="你来当调度器" size={42} />; })()}
          {boxes("race-0", "threads").map((b, i) => <Glow key={i} box={b} cam={cam} color={C.accent} o={steps(tw(f, w("race", "两个线程") + i * 4, 0.15), 3) * (1 - tw(f, raceAt[0] - 4, 0.2))} pad={2} />)}
          <Glow box={box("race-0", "shared")} cam={cam} color={C.bad} o={steps(tw(f, raceAt.at(-1)! + 4, 0.15), 3)} pad={2} at={raceAt.at(-1)! + 4} />
          {(() => { const p = at({ x: 520, y: 407 }, cam); return <Tag x={p.x} y={p.y} at={raceAt.at(-1)! + 6} out={t.raceCheck} color={C.bad} text="x = 1：两次加 1，只加上了一次" size={32} />; })()}
        </>}
        <Cursor cam={cam} show={[t.race + 10, t.raceCheck + 14]} clicks={[...raceAt, t.raceCheck]}
          path={[[t.race + 10, { x: 900, y: 560 }], ...raceAt.flatMap((c, i) => [[c - 7, mid(steps2[race.solution[i]])], [c + 2, mid(steps2[race.solution[i]])]] as [number, { x: number; y: number }][]),
            [t.raceCheck - 6, btn("race-0", "check")]]} />
        {/* replace：你来当页面置换算法（FIFO） */}
        {shot.startsWith("replace") && <>
          {(() => { const p = at({ x: 300, y: 60 }, cam); return <Tag x={p.x} y={p.y} at={w("replace", "页面置换")} out={repAt[0] - 2} color={C.accent} text="FIFO：换出最早进来的那一页" size={36} />; })()}
          {(() => {
            const k = Math.min(repSol.length - 1, repAt.filter((c) => f >= c + 2).length);
            const s = SHOTS[`replace-${k}`];
            const sl = boxes(`replace-${k}`, "slots");
            return f >= repAt[0] - 10 && sl.length > 0 && <Glow box={{ x: sl[0].x, y: sl[0].y, w: sl.at(-1)!.x + sl.at(-1)!.w - sl[0].x, h: sl[0].h }} cam={cam} color={C.gold} o={s ? 1 : 0} pad={6} />;
          })()}
        </>}
        <Cursor cam={cam} show={[t.rep + 10, beat("lab").start - 2]} clicks={repAt}
          path={[[t.rep + 10, { x: 900, y: 600 }], ...repAt.flatMap((c, i) => [[c - 7, slotOf(i)], [c + 2, slotOf(i)]] as [number, { x: number; y: number }][])]} />
      </AppWindow>
      {/* 音效：游戏自己的 */}
      <Sfx at={t.clickStart} name="select" />
      <Sfx at={t.clickLine} name="page" />
      {(["intro-l0", "intro-l2"] as const).map((n) => {
        const s = list.find(([, x]) => x === n)![0];
        return <TypeBlips key={n} text={SHOTS[n].line!.text} at={s + 4} rate={1.1} v={0.14} />;
      })}
      <Sfx at={t.clickGo} name="select" />
      <Sfx at={t.routeIn} name="unlock" v={0.3} />
      <Sfx at={t.tGuess} name="page" v={0.25} />
      <Sfx at={t.tCard} name="page" v={0.25} />
      <Sfx at={t.tItem} name="correct" v={0.3} />
      <Sfx at={t.pickOpt} name="tap" v={0.4} />
      <Sfx at={t.clickCheck + 2} name="wrong" v={0.35} />
      {raceAt.map((c) => <Sfx key={c} at={c} name="tap" v={0.4} />)}
      <Sfx at={t.raceCheck + 2} name="correct" v={0.35} />
      {repAt.map((c) => <Sfx key={c} at={c} name="tap" v={0.4} />)}
      <Sfx at={repAt.at(-1)! + 4} name="correct" v={0.3} />
    </AbsoluteFill>
  );
};

/** 远征的 5 站：每站一块像素牌子（领域色 + 站名 + 课数），最后合计 */
const StopStrip: React.FC<{ at: number; total: number; out: number }> = ({ at: a, total, out }) => {
  const f = useCurrentFrame();
  if (f < a - 2 || f > out + 6) return null;
  const o = 1 - steps(tw(f, out - 4, 0.2), 3);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: WIN.h - 210, height: 170, display: "flex", justifyContent: "center", alignItems: "center", gap: 18, opacity: o,
      background: "rgba(14,13,36,0.9)", boxShadow: `0 -6px 0 0 ${C.rim}` }}>
      {F.route.stops.map((s, i) => {
        const t = steps(tw(f, a + i * 5, 0.18), 3);
        return <React.Fragment key={s.id}>
          {i > 0 && <div style={{ width: 24, height: 6, background: C.rim, opacity: t }} />}
          <div style={{ opacity: t, transform: `translateY(${(1 - t) * 24}px)`, background: C.panel, boxShadow: frame(6, s.color, "rgba(0,0,0,0.5)"), padding: "8px 16px", minWidth: 190 }}>
            <div style={{ fontFamily: PX, fontSize: 24, lineHeight: "30px", color: C.muted }}>第 {i + 1} 站</div>
            <div style={{ fontFamily: PX, fontSize: 30, lineHeight: "40px", color: C.ink, whiteSpace: "nowrap" }}>{s.name}</div>
            <div style={{ fontFamily: PX, fontSize: 30, lineHeight: "40px", color: s.color === "#d1792f" ? "#f0a25e" : s.color === "#7a5bd6" ? "#b49bff" : "#5fd3a6" }}>{s.lessons} 课</div>
          </div>
        </React.Fragment>;
      })}
      <div style={{ marginLeft: 16, opacity: steps(tw(f, total - 2, 0.2), 3), fontFamily: PX, fontSize: 60, lineHeight: "72px", color: C.gold, textShadow: "5px 5px 0 rgba(0,0,0,0.6)", whiteSpace: "nowrap" }}>= {F.lessons} 课</div>
    </div>
  );
};
