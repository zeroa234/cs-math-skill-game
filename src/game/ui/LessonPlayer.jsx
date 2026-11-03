// Lesson: the lesson's flow (core/lesson.js) in the shared step player, then the celebration.
import { useEffect, useState } from "preact/hooks";
import confetti from "canvas-confetti";
import { g, packs, store, useProgress, stateOf, activeRoute } from "../app/state.js";
import { href } from "../app/router.js";
import { completeLesson } from "../app/actions.js";
import { play } from "../app/sound.js";
import { toast, unitLabel } from "./common.jsx";
import { CAST, Sprite } from "./cast.jsx";
import { artFor } from "../app/art.js";
import { StepPlayer } from "./StepPlayer.jsx";
import { Icon } from "./icons.jsx";

export function LessonPlayer({ skillId, lessonId }) {
  const skill = g.byId.get(skillId);
  const pack = packs[skillId];
  const lesson = pack?.lessons.find((l) => l.id === lessonId);
  if (!lesson) return <div class="page"><p>找不到这一课。<a href={href("skill", skillId)}>回技能页</a></p></div>;
  return <Lesson key={skillId + "/" + lessonId} skill={skill} lesson={lesson} />;
}

function Lesson({ skill, lesson }) {
  const p = useProgress();
  const chapter = stateOf(p, skill.id).chapters.find((c) => c.key === lesson.id);
  const [done, setDone] = useState(null);
  const finish = async (res) => {
    const out = await completeLesson(store, g, packs, skill.id, lesson, lesson.items.map((it) => res[it.id]));
    setDone({ summary: out, results: res });
    for (const a of out.achievements) toast({ title: "成就：" + a.name, body: a.desc });
    for (const e of out.lab) toast({ title: "实验室多了一个实验：" + e.title, body: "营地最下面的“实验室”里可以随时再玩。" });
  };
  if (done) return <Celebration skill={skill} lesson={lesson} chapter={chapter} summary={done.summary} results={done.results} />;
  return <StepPlayer kicker={chapter ? `${skill.name} · 第 ${chapter.chapter.no} 章 · ${chapter.chapter.title}` : skill.name} title={lesson.title} closeHref={href("skill", skill.id)} flow={lesson.flow} onFinish={finish} />;
}

// Lesson complete: the stars pop in one at a time with a chime, the mentors celebrate.
function Celebration({ skill, lesson, chapter, summary, results }) {
  const st = summary.state;
  const next = st.nextChapter;
  const firstTry = Object.values(results).filter((r) => r.firstTry).length;
  const route = activeRoute(store.get());
  useEffect(() => {
    play("fanfare");
    const ts = Array.from({ length: summary.stars }, (_, i) => setTimeout(() => play("star"), 650 + i * 380));
    if (summary.stars >= 2 && !store.get().settings.reduceMotion) ts.push(setTimeout(() => confetti({ particleCount: 110, spread: 75, origin: { y: 0.65 }, disableForReducedMotion: true }), 650 + summary.stars * 380));
    return () => ts.forEach(clearTimeout);
  }, []);
  return (
    <div class="celebrate pixel-bg" style={{ backgroundImage: `url(${artFor(route)})` }}>
      <div class="panel">
        <div class="mentors" aria-hidden="true">
          <Sprite who="black" action={[CAST.black.celebrate, "idle"]} scale={2} />
          <Sprite who="blue" action={[CAST.blue.celebrate, "idle"]} scale={2} flip />
        </div>
        <div class="small muted">{skill.name} · {unitLabel(chapter)}</div>
        <h1>完成：{lesson.title}</h1>
        <div class="big-stars" aria-label={`${summary.stars} 颗星`}>{[0, 1, 2].map((i) => <span class={i < summary.stars ? "on" : ""} style={{ animationDelay: `${0.65 + i * 0.38}s` }}><Icon name="star" /></span>)}</div>
        <div class="reward-row">
          <div class="reward xp"><div class="k">经验</div><div class="v">+{summary.xp}</div></div>
          <div class="reward acc"><div class="k">一次答对</div><div class="v">{firstTry}/{lesson.items.length}</div></div>
        </div>
        <p class="small muted">这些题过几天会出现在“复习”里，帮你记牢。</p>
        <div class="row">
          {next?.kind === "lesson" ? <a class="btn primary big" href={href("lesson", skill.id, next.key)}>下一课</a> : st.bossOpen && st.status !== "lit" ? <a class="btn gold big" href={href("boss", skill.id)}>结业挑战</a> : null}
          <a class="btn" href={route ? href("route", route.id) : href("skill", skill.id)}>{route ? "回路线" : "回技能页"}</a>
        </div>
        {next?.kind === "lesson" && <p class="small muted">下一课：{next.lesson.title}</p>}
      </div>
    </div>
  );
}
