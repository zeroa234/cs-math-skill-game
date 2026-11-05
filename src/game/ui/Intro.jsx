// Opening scene, shown once on the first visit (and from 我的 → 重看开场): a title card, then the two
// mentors explain in four lines what the game is and how a lesson works, and hand over to the route
// picker. Every step can be skipped; click, Enter or Space finishes a line, then advances.
import { useEffect, useRef, useState } from "preact/hooks";
import { g, store } from "../app/state.js";
import { go } from "../app/router.js";
import { play } from "../app/sound.js";
import { CAST, Portrait, Sprite } from "./cast.jsx";

const LINES = [
  { who: "black", text: `欢迎来到星图学院。天上那棵由星星连成的树，就是计算机和数学要学的 ${g.tree.skills.length} 个技能。` },
  { who: "blue", text: "每颗星都要先点亮它下面连着的星——就像先会写程序，才学得动操作系统！" },
  { who: "black", text: "每次只学一小课：先猜一猜，再看讲解，再动手做。答错不扣任何东西，我们会告诉你错在哪。" },
  { who: "blue", text: "每一章还会告诉你去哪本书、哪门公开课深入。准备好了吗？挑一条远征出发吧！" },
];

const done = () => store.update((d) => { d.settings.introSeen = true; });

export function Intro() {
  const [k, setK] = useState(-1); // -1: title card
  const [shown, setShown] = useState(0);
  const line = LINES[k];
  const typing = line && shown < line.text.length;
  const reduce = store.get().settings.reduceMotion;
  const timer = useRef(null);

  useEffect(() => {
    if (!line) return;
    if (reduce) { setShown(line.text.length); return; }
    setShown(0);
    let i = 0;
    timer.current = setInterval(() => {
      i++;
      setShown(i);
      if (i % 3 === 1) play("blip");
      if (i >= line.text.length) clearInterval(timer.current);
    }, 32);
    return () => clearInterval(timer.current);
  }, [k]);

  const finish = () => { done(); play("unlock"); go("pick"); };
  const advance = () => {
    if (k < 0) { play("select"); setK(0); return; }
    if (typing) { clearInterval(timer.current); setShown(line.text.length); return; }
    if (k < LINES.length - 1) { play("page"); setK(k + 1); } else finish();
  };

  useEffect(() => {
    // Enter or Space on a focused button (跳过开场, 开始) is that button's own click, not "next line".
    const on = (e) => {
      if ((e.key === "Enter" || e.key === " ") && !e.repeat && !e.target.closest?.("button, a, input, select, textarea")) { e.preventDefault(); advance(); }
      if (e.key === "Escape") finish();
    };
    window.addEventListener("keydown", on);
    return () => window.removeEventListener("keydown", on);
  });

  return (
    <div class="intro" role="dialog" aria-modal="true" aria-label="开场">
      <div class="sky" style={{ backgroundImage: "url(assets/bg/title.png)" }} />
      <button type="button" class="btn small skip" onClick={finish}>跳过开场</button>
      {k < 0 ? (
        <div class="title-card">
          <h1>计算机大学习！</h1>
          <p>计算机与数学的星图 · 一次一小课，一路点亮</p>
          <div class="row center" style={{ alignItems: "flex-end", gap: "1.6rem", margin: "1rem 0 1.4rem" }}>
            <Sprite who="black" action="wave" then="idle" scale={2} />
            <Sprite who="blue" action="wave" then="idle" scale={2} flip />
          </div>
          <button type="button" class="btn primary big" onClick={advance} autofocus>开始</button>
        </div>
      ) : (
        <>
          <div class="stage" aria-hidden="true">
            <Portrait who="black" class={"who" + (line.who === "black" ? "" : " dim")} />
            <Portrait who="blue" class={"who" + (line.who === "blue" ? "" : " dim")} />
          </div>
          <div class="dialog" onClick={advance}>
            <span class="name">{CAST[line.who].name}</span>
            <p class="line" aria-hidden="true">{line.text.slice(0, shown)}</p>
            <p class="sr-only" aria-live="polite">{line.text}</p>
            {k === LINES.length - 1 && !typing ? (
              <div class="row"><button type="button" class="btn primary big" onClick={(e) => { e.stopPropagation(); finish(); }}>挑一条远征</button></div>
            ) : (
              <span class="next" aria-hidden="true">{typing ? "" : "▼ 点击继续"}</span>
            )}
          </div>
        </>
      )}
    </div>
  );
}
