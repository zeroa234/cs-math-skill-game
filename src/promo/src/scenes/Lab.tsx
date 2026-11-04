// 实验室：9 种交互组件拼成九宫格（每格是实验室页面里那个实验的真实截图，顶部一段）。
// 实验室按“课里遇到过的”列出 11 个实验：栈和队列、BFS 和 DFS 各算一种组件的两种用法，这里各取一个，标题用组件名（README“现在有多少内容”）。
import React from "react";
import { AbsoluteFill, Img, staticFile, useCurrentFrame } from "remotion";
import { C, F, LAB, PX, beat, steps, tw, w } from "../lib/core";
import { Counter, Sfx, big, frame } from "../lib/ui";

// 组件 → 实验室里的哪一个实验（按标题找）、格子上写的名字
const PICK: [string, string, string][] = [
  ["threads", "你来当调度器", "你来当调度器"], ["replace", "页面置换", "页面置换"], ["trace", "Python 单步执行", "Python 单步执行"],
  ["scheduler", "CPU 调度（时间片轮转）", "CPU 调度"], ["paging", "分页地址转换", "分页地址转换"], ["bits", "位与补码", "位与补码"],
  ["stackqueue", "栈", "栈和队列"], ["hash", "哈希表（线性探测）", "哈希表"], ["graph", "广度优先搜索", "BFS / DFS"],
];

export const Lab: React.FC = () => {
  const f = useCurrentFrame();
  const A = beat("lab").start, Z = beat("boss").start;
  if (f < A - 2 || f > Z + 12) return null;
  if (PICK.length !== F.sims.length || PICK.some(([s]) => !F.sims.includes(s))) throw new Error("实验室九宫格和游戏的组件种类对不上：" + F.sims.join(" "));
  const t0 = w("lab", "九种");
  const out = 1 - steps(tw(f, Z - 8, 0.25), 3);
  const TW = 540, TH = 206, GX = 36, GY = 26, X0 = (1920 - (3 * TW + 2 * GX)) / 2, Y0 = 236;
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <div style={{ position: "absolute", left: X0, top: 80, display: "flex", alignItems: "baseline", gap: 26, opacity: steps(tw(f, A, 0.2), 3) }}>
        <span style={{ ...big(72, C.ink) }}>实验室</span>
        <span style={{ ...big(72, C.gold) }}><Counter n={F.sims.length} at={t0} dur={0.5} /> 种实验</span>
        <span style={{ ...big(36, C.ink2), opacity: steps(tw(f, w("lab", "随时再玩") - 4, 0.2), 3) }}>课里遇到过的都在这里，随时再玩，不计分</span>
      </div>
      {PICK.map(([sim, title, label], i) => {
        const item = LAB.items.find((x) => x.title === title);
        if (!item) throw new Error("实验室截图里没有 " + title);
        const a = t0 + i * 3;
        const t = steps(tw(f, a, 0.18), 3);
        const x = X0 + (i % 3) * (TW + GX), y = Y0 + Math.floor(i / 3) * (TH + GY);
        const sc = TW / item.w;
        return (
          <div key={sim} style={{ position: "absolute", left: x, top: y, width: TW, height: TH, opacity: t, transform: `scale(${0.7 + 0.3 * t})`,
            background: C.panel, boxShadow: frame(6, i < 2 ? C.gold : C.rim, C.rimDeep), overflow: "hidden" }}>
            <Img src={staticFile(`shots/${item.file}`)} style={{ position: "absolute", left: 0, top: 0, width: TW, height: item.h * sc }} />
            <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, padding: "4px 14px", background: "rgba(20,20,43,0.92)", fontFamily: PX, fontSize: 30, lineHeight: "40px", color: C.ink }}>{label}</div>
          </div>
        );
      })}
      {PICK.map((_, i) => <Sfx key={i} at={t0 + i * 3} name="tap" v={0.3} />)}
    </AbsoluteFill>
  );
};
