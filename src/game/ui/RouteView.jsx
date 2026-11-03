// One campaign as a path: every stop is a unit, every chapter a round level button on a winding
// trail, the final challenge a crown. The next level shows a "start" bubble and a mentor stands
// beside it. The route's story and evidence are folded away under "关于这条路线". A route still in
// development (开发中) shows its stops as a plain list instead of a playable trail.
import { g, packs, store, useProgress, stateOf, routeNext, routeFor, routeStats, playable } from "../app/state.js";
import { KIND_LABEL } from "../core/route-text.js";
import { DevTag } from "./PickGoal.jsx";
import { href } from "../app/router.js";
import { lessonKey } from "../core/rules.js";
import { play } from "../app/sound.js";
import { SkillLink, Bar, unitLabel } from "./common.jsx";
import { Sprite } from "./cast.jsx";
import { artFor } from "../app/art.js";
import { Icon } from "./icons.jsx";
import { PASS_SHARE } from "../core/lesson.js";

const WAVE = [0, 46, 72, 46, 0, -46, -72, -46]; // px sideways for consecutive levels

export function RouteView({ id }) {
  const p = useProgress();
  const r = routeFor(id);
  if (!r) return <div class="page"><p>没有这条远征。<a href={href("pick")}>去选一条</a></p></div>;
  const open = playable(r);
  if (open && p.settings.route !== id) queueMicrotask(() => store.update((d) => { d.settings.route = id; }));
  const current = routeNext(p, r);
  const goal = g.byId.get(r.goal);
  const kth = goal.kth || [];
  const stats = routeStats(r);
  const lit = r.stops.filter((sid) => stateOf(p, sid).status === "lit").length;
  let level = 0; // running index along the whole trail, for the winding offsets
  return (
    <div class="page route">
      <header class="route-banner pixel-bg" style={{ backgroundImage: `url(${artFor(r)})` }}>
        <a class="back" href={open ? href() : href("pick")}><Icon name="back" /> {open ? "营地" : "选远征"}</a>
        <div class="kicker">{KIND_LABEL[r.kind]}{!open && <> <DevTag /></>}</div>
        <h1>{r.name}</h1>
        <p>{r.tagline}</p>
        <Bar value={lit / r.stops.length} label="远征进度" />
        <div class="small">已点亮 {lit} / {r.stops.length} 站 · 互动课共 {stats.lessons} 课</div>
        {open && <a class="btn small change-route" href={href("pick")}>换一条远征 / 自己定目标</a>}
      </header>
      <details class="about-route card">
        <summary>关于这条路线</summary>
        {r.story.map((t) => <p>{t}</p>)}
        {r.evidence?.sources && <p class="evidence small">依据：{r.evidence.sources.map((src, i) => <>{i ? "；" : ""}<a href={src.url} target="_blank" rel="noopener">{src.name}</a></>)}</p>}
        {r.kind === "recommended" && <p class="small muted">站点是这些目标要先学的全部技能：{[...(r.also || []), r.goal].map((x) => g.byId.get(x).name).join("、")}，由技能树按先后自动排好。</p>}
        {kth.length > 0 && (
          <p class="evidence small">
            对照：KTH <a href={kth[0].url} target="_blank" rel="noopener">{kth[0].code} {kth[0].name}</a> 要求先学的课（{kth[0].needs.map((n) => g.byId.get(n.skill).name).join("、")}）都在这条路线上。
          </p>
        )}
      </details>
      {!open && <DevStops r={r} stats={stats} />}
      {open && <div class="route-layout">
        <div class="units">
          {r.stops.map((sid, i) => {
            const st = stateOf(p, sid);
            const lane = g.lanes.get(st.skill.lane);
            const isCur = current && current.skill.id === sid;
            const levels = [...st.chapters.map((c, k) => ({ c, k })), { boss: true }];
            return (
              <section class={"unit" + (st.status === "locked" ? " locked" : "")} style={{ "--lane": lane.color }} aria-label={`第 ${i + 1} 站：${st.skill.name}`}>
                <div class="unit-head">
                  <div>
                    <div class="kicker">第 {i + 1} 站 · {lane.short} · {st.skill.chapters.length} 章{st.hasContent ? ` · ${st.chapters.length} 课` : " · 互动课开发中"}</div>
                    <h2>{st.skill.name}</h2>
                  </div>
                  <a class="btn small" href={href("skill", sid)}>技能详情</a>
                </div>
                {st.status === "locked" && <p class="unit-note">要先学：{st.missing.map((m) => g.byId.get(m).name).join("、")}</p>}
                {st.status === "lit" && <p class="unit-note"><Icon name="sparkle" /> 已点亮</p>}
                <ol class="trail">
                  {levels.map((lv, k) => {
                    // A skill with lessons groups them by chapter: a label marks where each chapter starts.
                    const mark = lv.c?.kind === "lesson" && lv.c.chapter.no !== levels[k - 1]?.c?.chapter.no && <li class="ch-mark"><span>第 {lv.c.chapter.no} 章 · {lv.c.chapter.title}</span></li>;
                    const dx = WAVE[level++ % WAVE.length];
                    if (lv.boss) return <Level key="boss" dx={dx} boss sid={sid} st={st} p={p} cur={isCur && !st.nextChapter && st.status !== "locked"} who={i % 2 ? "blue" : "black"} />;
                    return <>{mark}<Level key={lv.c.key} dx={dx} sid={sid} st={st} p={p} c={lv.c} k={lv.k} cur={isCur && st.nextChapter?.key === lv.c.key && st.status !== "locked"} who={i % 2 ? "blue" : "black"} /></>;
                  })}
                </ol>
              </section>
            );
          })}
        </div>
        <aside class="card side-quests">
          <h3>顺路推荐</h3>
          <p class="small muted">不挡路，学了会更顺。理由来自技能树的课程证据。</p>
          {r.sideQuests.length ? (
            <ul>{r.sideQuests.map((q) => <li><SkillLink id={q.id} /> <span class="small muted">对 {q.for.map((f) => g.byId.get(f.id).name).join("、")} 有帮助</span></li>)}</ul>
          ) : <p class="small">这条路线没有推荐的顺路技能。</p>}
        </aside>
      </div>}
    </div>
  );
}

// The stops of a route that is not open yet: what it will ask for, and which stops are ready.
function DevStops({ r, stats }) {
  return (
    <section class="card dev-stops">
      <h2>这条远征还在开发中</h2>
      <p class="small">路线上每一站的课都按零基础和覆盖面两条标准写好以后开放，现在已写好 {stats.beginner} / {stats.stops} 站。下面是它要走的站；其中的技能也能先从地图单独学。</p>
      <ol>
        {r.stops.map((sid) => {
          const pack = packs[sid];
          return <li><a href={href("skill", sid)}>{g.byId.get(sid).name}</a> <span class="small muted">{pack ? (pack.version >= 2 ? "互动课 · 已按新标准写好" : "互动课 · 待重写") : "互动课开发中 · 可看自学资料"}</span></li>;
        })}
      </ol>
    </section>
  );
}

function Level({ dx, sid, st, p, c, k, boss, cur, who }) {
  const lesson = c?.kind === "lesson";
  const done = boss ? !!p.skills[sid]?.lit : st.done[k];
  const open = boss ? st.bossOpen : st.chapterOpen(k);
  const stars = lesson ? p.lessons[lessonKey(sid, c.key)]?.stars || 0 : 0;
  const to = boss ? href("boss", sid) : lesson ? href("lesson", sid, c.key) : href("skill", sid);
  const title = boss ? (st.hasContent ? "结业挑战" : "综合练习") : lesson ? c.lesson.title : c.chapter.title;
  const label = boss ? title : unitLabel(c);
  const icon = boss ? <Icon name="crown" size={36} /> : done ? <Icon name="star" size={36} /> : !open ? <Icon name="lock" size={36} /> : lesson ? c.no : <Icon name="book" size={36} />;
  const cls = "lv" + (boss ? " boss" : "") + (done ? " done" : "") + (!open ? " locked" : "") + (!lesson && !boss ? " self" : "");
  const onClick = (e) => { if (!open) { e.preventDefault(); play("locked"); } else play("tap"); };
  const name = `${label}：${title}${done ? "（已完成）" : !open ? "（未解锁）" : ""}`;
  return (
    <li class={cur ? "current" : ""} style={{ "--dx": `calc(${dx}px * var(--wave, 1))` }}>
      {cur && (
        <div class="start-pop">
          <div class="t">{title}</div>
          <div class="m">{boss ? (st.hasContent ? `答对 ${Math.round(PASS_SHARE * 100)}% 点亮` : "综合练习") : lesson ? `${label} · 约 ${c.lesson.minutes || 8} 分钟` : `${label} · 读教材`}</div>
          <button type="button" class="btn primary small" onClick={() => { play("select"); location.hash = to; }}>{boss ? "挑战" : done ? "再练" : "开始"}</button>
        </div>
      )}
      <a class={cls} href={open ? to : undefined} role="link" aria-disabled={!open} aria-label={name} title={name} onClick={onClick} tabIndex={0}>{icon}</a>
      {cur && <div class={"mascot " + (dx >= 0 ? "left" : "right")}><Sprite who={who} action="idle" scale={2} flip={dx < 0} /></div>}
      {lesson && done && <span class="lv-stars" aria-hidden="true">{[0, 1, 2].map((i) => <Icon name="star" class={i < stars ? "on" : "off"} />)}</span>}
      {!cur && <span class="lv-label" aria-hidden="true">{title.length > 12 ? title.slice(0, 11) + "…" : title}</span>}
    </li>
  );
}
