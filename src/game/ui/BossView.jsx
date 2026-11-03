// Final challenge, played in the same step player as a lesson. What it contains and when it lights
// come from core/lesson.js (bossFlow) and core/rules.js (shouldLight); this view only shows them.
//  - graded (the skill has a content pack): auto-checked questions; lights at PASS_SHARE right on the
//    first try. mode "test" is the test-out: the same questions before the chapters.
//  - no pack yet: freely browse the tree's exercise and its answer, without grading or progress.
import { useEffect, useState } from "preact/hooks";
import confetti from "canvas-confetti";
import { g, packs, store, useProgress, stateOf, activeRoute } from "../app/state.js";
import { href } from "../app/router.js";
import { bossFlow, firstTryShare, PASS_SHARE } from "../core/lesson.js";
import { submitBoss } from "../app/actions.js";
import { play } from "../app/sound.js";
import { Md } from "./md.jsx";
import { toast } from "./common.jsx";
import { CAST, Sprite } from "./cast.jsx";
import { artFor } from "../app/art.js";
import { StepPlayer } from "./StepPlayer.jsx";
import { Icon } from "./icons.jsx";

const need = (n) => Math.ceil(n * PASS_SHARE - 1e-9);

export function BossView({ id, mode }) {
  const p = useProgress();
  const skill = g.byId.get(id);
  const [phase, setPhase] = useState({ at: "brief", attempt: 0 });
  if (!skill) return null;
  const st = stateOf(p, id);
  const testOut = mode === "test";
  const boss = bossFlow(skill, packs[id]);
  const back = <a class="btn" href={href("skill", id)}>回技能页</a>;
  if (!st.hasContent) return <SelfStudyExercise skill={skill} back={back} />;
  if (st.status === "locked") return <Notice title="还没解锁">先学完它要求的技能：{st.missing.map((m) => g.byId.get(m).name).join("、")}。{back}</Notice>;
  if (!testOut && !st.bossOpen) return <Notice title="结业挑战还没开放">学完全部核心章后开放。{boss.graded && <> 已经会了？可以试试<a href={href("boss", id, "test")}>跳级挑战</a>。</>}{back}</Notice>;

  const finish = (res) => {
    const auto = firstTryShare(boss.items, res);
    const out = submitBoss(store, g, packs, id, { graded: boss.graded, auto, testOut });
    for (const a of out.achievements) toast({ title: "成就：" + a.name, body: a.desc });
    setPhase({ at: "done", attempt: phase.attempt, out, right: Math.round(auto * boss.items.length) });
  };
  if (phase.at === "done") return <BossResult skill={skill} boss={boss} phase={phase} testOut={testOut} retry={() => setPhase({ at: "play", attempt: phase.attempt + 1 })} />;
  if (phase.at === "play" && boss.flow.length) return <StepPlayer key={phase.attempt} kicker={skill.name} title={testOut ? "跳级挑战" : "结业挑战"} closeHref={href("skill", id)} flow={boss.flow} coach="black" itemLabel="挑战" leaveText="这次挑战不会记录。" onFinish={finish} />;

  const n = boss.items.length;
  return (
    <div class="page boss">
      <div class="card boss-brief">
        <a class="back" href={href("skill", id)}><Icon name="back" /> {skill.name}</a>
        <h1>{testOut ? "跳级挑战" : "结业挑战"}：{skill.name}</h1>
        <ul class="rules">
            <li>{n} 道题，和课里一样一题一题做，答完马上判对错、给解析。</li>
            <li><b>第一次就答对至少 {need(n)} 道</b>（{Math.round(PASS_SHARE * 100)}%），并且没有看提示，就点亮。</li>
            <li>答错的题最后会再练一次，但不算进点亮。没过可以马上再挑战，不扣任何东西。</li>
            {testOut && <li>跳级：不用先学各章。点亮后它就算作后面技能的前置。</li>}
        </ul>
        <div class="row">
          <button type="button" class="btn primary big" onClick={() => { play("select"); boss.flow.length ? setPhase({ at: "play", attempt: 0 }) : finish({}); }}>开始</button>
          {back}
        </div>
      </div>
    </div>
  );
}

function SelfStudyExercise({ skill, back }) {
  return <div class="page boss self-study-exercise"><section class="card">
    <h1>综合练习：{skill.name}</h1>
    <p class="small muted">互动课和结业挑战开发中。这道练习供自学，可以直接查看参考答案，不计分、不点亮技能。</p>
    {skill.exercise ? <>
      <p class="small muted">约 {skill.exercise.minutes} 分钟 · 覆盖 {skill.exercise.covers.join("、")}</p>
      <Md text={skill.exercise.question} />
      <details class="exercise-answer"><summary>参考答案</summary><Md text={skill.exercise.answer} /></details>
    </> : <p>综合练习资料整理中，可以先按技能页的教材指引学习。</p>}
    {back}
  </section></div>;
}

function Notice({ title, children }) {
  return <div class="page"><div class="card center notice"><h1>{title}</h1><p>{children}</p></div></div>;
}

function BossResult({ skill, boss, phase, testOut, retry }) {
  const { out, right } = phase;
  const route = activeRoute(store.get());
  useEffect(() => {
    play(out.lit ? "fanfare" : "wrong");
    if (out.lit) {
      toast({ title: `点亮：${skill.name}`, body: `经验 +${out.xp}` });
      if (!store.get().settings.reduceMotion) confetti({ particleCount: 140, spread: 90, origin: { y: 0.6 }, disableForReducedMotion: true });
    }
  }, []);
  // Newly open skills: the current route's stops first, then the rest (a root skill opens many).
  const opened = skill.unlocks.filter((u) => stateOf(store.get(), u).status === "open");
  const onRoute = opened.filter((u) => route?.stops.includes(u));
  const unlocked = [...onRoute, ...opened.filter((u) => !onRoute.includes(u))].slice(0, Math.max(4, onRoute.length));
  const more = opened.length - unlocked.length;
  const n = boss.items.length;
  return (
    <div class="celebrate pixel-bg" style={{ backgroundImage: `url(${artFor(route)})` }}>
      <div class="panel">
        <div class="mentors" aria-hidden="true">
          <Sprite who="black" action={out.lit ? [CAST.black.celebrate, "idle"] : "idle"} scale={2} />
          <Sprite who="blue" action={out.lit ? [CAST.blue.celebrate, "idle"] : ["coy", "idle"]} scale={2} flip />
        </div>
        {out.lit ? <>
          <div class="lit-mark" aria-hidden="true"><Icon name="sparkle" size={48} /></div>
          <h1>{skill.name} 已点亮</h1>
          {boss.graded && <p>第一次就答对 {right} / {n}</p>}
          {unlocked.length > 0 && <p>新解锁：{unlocked.map((u) => <a class="skill-link" href={href("skill", u)}>{g.byId.get(u).name}</a>)}{more > 0 && <span class="muted">等另外 {more} 个（在地图上看）</span>}</p>}
          <p class="small muted">做过的题会进入间隔复习；复习稳了，它会升到“熟练”“精通”。</p>
        </> : <>
          <h1>还差一点</h1>
          <p>第一次就答对 {right} / {n}，点亮需要 {need(n)} 道。</p>
          <p class="small muted">{testOut ? "可以先学几章再来，或者马上再试一次。" : "刚才的解析看过了，可以马上再挑战；也可以回到对应的章再练练。"}</p>
        </>}
        <div class="row">
          {!out.lit && <button type="button" class="btn primary big" onClick={retry}><Icon name="reload" /> 再挑战</button>}
          {out.lit && route && <a class="btn primary big" href={href("route", route.id)}>回路线</a>}
          <a class="btn" href={href("skill", skill.id)}>回技能页</a>
        </div>
        {out.lit && boss.graded && skill.exercise && (
          <details class="extra">
            <summary>延伸：原技能树的综合练习（约 {skill.exercise.minutes} 分钟，不计分）</summary>
            <Md text={skill.exercise.question} />
            <details><summary>参考答案</summary><Md text={skill.exercise.answer} /></details>
          </details>
        )}
      </div>
    </div>
  );
}
