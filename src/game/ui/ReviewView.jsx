// Spaced review: due cards from every skill, mixed together (FSRS decides when each comes back).
import { useState } from "preact/hooks";
import { g, store, useProgress, dueCards, itemForCard } from "../app/state.js";
import { href } from "../app/router.js";
import { answerReview } from "../app/actions.js";
import { toast } from "./common.jsx";
import { Sprite } from "./cast.jsx";
import { ItemStep } from "./StepPlayer.jsx";
import { Icon } from "./icons.jsx";

const SESSION = 12;

export function ReviewView() {
  const p = useProgress();
  const [session] = useState(() => dueCards(store.get()).filter((k) => itemForCard(k)).slice(0, SESSION));
  const [i, setI] = useState(0);
  const [right, setRight] = useState(0);
  if (!session.length) {
    const upcoming = Object.values(p.cards).map((c) => new Date(c.dueAt)).sort((a, b) => a - b)[0];
    return (
      <div class="page"><div class="card center">
        <h1>现在没有要复习的</h1>
        <p>{upcoming ? `下一题在 ${upcoming.toLocaleString("zh-CN", { month: "numeric", day: "numeric", hour: "2-digit", minute: "2-digit" })} 到期。` : "学完第一课后，做过的题会按记忆规律排进这里。"}</p>
        <p class="small muted">间隔复习：刚学完很快忘，隔一段时间再想起一次，下一次间隔就能拉长。排程用的是开源的 FSRS 算法。</p>
        <a class="btn primary" href={href()}>回营地</a>
      </div></div>
    );
  }
  if (i >= session.length) return (
    <div class="page"><div class="card center">
      <h1>复习完成</h1>
      <p>答对 {right} / {session.length}。答错的题会更快再出现。</p>
      <a class="btn primary" href={href()}>回营地</a>
    </div></div>
  );
  const key = session[i];
  const found = itemForCard(key);
  return (
    <div class="player">
      <header class="player-head">
        <a class="close" href={href()} aria-label="退出复习"><Icon name="close" /></a>
        <div class="ptitle"><span class="small muted">复习 · {found.skill.name}</span><b>{found.lesson.title}</b></div>
        <div class="pbar" role="progressbar" aria-label="复习进度" aria-valuenow={Math.round((i / session.length) * 100)} aria-valuemin="0" aria-valuemax="100"><div style={{ width: `${(i / session.length) * 100}%` }} /></div>
      </header>
      <div class="player-stage">
      <aside class="coach" aria-hidden="true"><div class="say">还记得吗？</div><Sprite who="black" action="idle" scale={2} /></aside>
      <main class="player-body">
        <ItemStep key={key} item={found.item} label="复习" verdicts={{ right: "记得！", wrong: "忘了一点", again: false }} onDone={async (r, usedHint) => {
          const out = await answerReview(store, key, { correct: r.correct, firstTry: true, usedHint });
          if (r.correct) setRight(right + 1);
          for (const a of out?.achievements || []) toast({ title: "成就：" + a.name, body: a.desc });
          setI(i + 1);
        }} />
      </main>
      </div>
    </div>
  );
}
