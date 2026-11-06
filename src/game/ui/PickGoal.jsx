// 选远征: 我的远征 (the author's own goals) first, then the recommended routes, then 自己定目标.
// A route still being written (status: dev in data/routes.yaml) is shown greyed out as 开发中: it
// can be read, not set off on. Its card says how many of its stops already meet the beginner
// standard, so the wait is visible. Picking a goal previews the route the tree implies first.
import { useMemo, useState } from "preact/hooks";
import { g, packs, store, useProgress, stateOf, routeFor, routeIdForGoal, routeStats, ownRoutes, recommendedRoutes, customGoalsOpen, playable } from "../app/state.js";
import { href, go } from "../app/router.js";
import { play } from "../app/sound.js";
import { artFor } from "../app/art.js";
import { Bar, LaneDot } from "./common.jsx";
import { Sprite } from "./cast.jsx";

const hours = (min) => (min >= 90 ? `约 ${Math.round(min / 60)} 小时` : `约 ${min} 分钟`);
const litCount = (p, r) => r.stops.filter((id) => stateOf(p, id).status === "lit").length;

export function setRoute(id) {
  play("unlock");
  store.update((d) => { d.settings.route = id; });
  go("route", id);
}

export const DevTag = () => <span class="dev-tag">开发中</span>;

// One route as a card. `wide` lays the banner beside the text and adds the route's introduction
// (used for 我的远征, the one a player is most likely on).
export function RouteCard({ r, p, wide }) {
  const s = routeStats(r);
  const lit = litCount(p, r);
  const open = playable(r);
  const active = open && p.settings.route === r.id;
  return (
    <article class={"route-card card" + (active ? " active" : "") + (open ? "" : " dev") + (wide ? " wide" : "")} aria-label={r.name + (open ? "" : "（开发中）")}>
      <div class="banner pixel-bg" style={{ backgroundImage: `url(${artFor(r)})` }}>
        <p class="tagline">{r.tagline}</p>
        {!open && <DevTag />}
      </div>
      <div class="body">
        <h3>{r.name}</h3>
        <div class="facts">{s.stops} 站 · {s.withContent} 站有互动课 · 互动课{hours(s.minutes)}</div>
        {wide && r.story.map((t) => <p class="small">{t}</p>)}
        {r.evidence && <p class="small evidence">{r.evidence.line}</p>}
        {!open && <p class="small muted">课程正按零基础和覆盖面两条标准重写：已写好 {s.beginner} / {s.stops} 站。</p>}
        {lit > 0 && <Bar value={lit / s.stops} label={`${r.name} 进度`} />}
        {!open ? <button type="button" class="btn" disabled>开发中，暂不能选</button>
          : active ? <a class="btn primary" href={href("route", r.id)}>继续这条</a>
          : <button type="button" class="btn primary" onClick={() => setRoute(r.id)}>{p.settings.route ? "换到这条" : "出发"}</button>}
      </div>
    </article>
  );
}

export function PickGoal() {
  const p = useProgress();
  return (
    <div class="page pick">
      <header class="page-head">
        <h1>选一场远征</h1>
        <p class="lead">远征就是一条从零走到目标的路：游戏从技能树里找出目标要先学的全部技能，按先后排好，每一站都是一个技能。</p>
      </header>
      <section>
        <h2>我的远征</h2>
        <p class="small muted">自己选定的目标。路线和介绍由技能树按目标自动生成。</p>
        <div class="routes mine">{ownRoutes.map((r) => <RouteCard r={r} p={p} wide />)}</div>
      </section>
      <section style={{ marginTop: "2rem" }}>
        <h2>推荐远征 <DevTag /></h2>
        <p class="small muted">按 2025 年开发者调查里人数较多的工作方向挑选，每条路线要学的技能对照了这个方向公开的学习路线图（依据见每条的“关于这条路线”）。要等路线上每一站的课都按零基础和覆盖面两条标准写好，才开放。</p>
        <div class="routes">{recommendedRoutes.map((r) => <RouteCard r={r} p={p} />)}</div>
      </section>
      <section style={{ marginTop: "2rem" }}>
        <h2>自己定目标{!customGoalsOpen && <> <DevTag /></>}</h2>
        {customGoalsOpen ? <GoalPicker p={p} /> : (
          <div class="card custom-dev">
            <p>开放以后，{g.tree.skills.length} 个技能里任选一个当目标。和“我的远征”一样，游戏会排好从零到目标的每一站，背景图用目标所在领域的主题图，路线介绍由技能树自动写好。</p>
          </div>
        )}
      </section>
    </div>
  );
}

// Any skill as the goal, with a preview of the route before setting off (shown once customGoals is open).
function GoalPicker({ p }) {
  const [q, setQ] = useState("");
  const [lane, setLane] = useState(null);
  const [goal, setGoal] = useState(null);
  const lanes = [...g.lanes.values()];
  const list = useMemo(() => {
    const k = q.trim().toLowerCase();
    return g.tree.skills
      .filter((s) => (!lane || s.lane === lane) && (!k || s.name.toLowerCase().includes(k) || s.en.toLowerCase().includes(k) || s.desc.includes(q.trim())))
      .map((s) => ({ s, n: routeFor(routeIdForGoal(s.id)).stops.length }))
      .sort((a, b) => a.n - b.n || a.s.step - b.s.step);
  }, [q, lane]);
  const preview = goal ? routeFor(routeIdForGoal(goal)) : null;
  const ps = preview ? routeStats(preview) : null;
  return (
    <>
      <p class="small muted">任何一个技能都能当目标。先选一个，右边会显示要走的路。</p>
      <div class="pick-layout">
        <div>
          <div class="pick-tools">
            <label class="sr-only" for="goal-q">搜索技能</label>
            <input id="goal-q" type="search" placeholder="搜索：图形学、数据库、密码学……" value={q} onInput={(e) => setQ(e.currentTarget.value)} />
          </div>
          <div class="lane-chips" role="group" aria-label="按领域筛选">
            <button type="button" class="lane-chip" aria-pressed={!lane} style={{ "--lane": "var(--accent)" }} onClick={() => setLane(null)}>全部</button>
            {lanes.map((l) => <button type="button" class="lane-chip" aria-pressed={lane === l.id} style={{ "--lane": l.color }} onClick={() => setLane(lane === l.id ? null : l.id)}>{l.short}</button>)}
          </div>
          <p class="small muted" aria-live="polite">{list.length} 个技能，按“要走的站数”从少到多排</p>
          <ul class="goal-list">
            {list.map(({ s, n }) => (
              <li>
                <button type="button" class="goal-item" aria-pressed={goal === s.id} onClick={() => { play("select"); setGoal(s.id); }}>
                  <LaneDot skill={s} />
                  <span><span class="gname">{s.name}</span><br /><span class="gmeta">{s.desc.slice(0, 40)}{s.desc.length > 40 ? "…" : ""}</span></span>
                  <span class="gmeta">{n} 站{packs[s.id] ? " · 有互动课" : ""}</span>
                </button>
              </li>
            ))}
          </ul>
        </div>
        <aside class="card preview" aria-live="polite">
          {preview ? (
            <>
              <div class="small muted">目标</div>
              <h3 style={{ margin: "0 0 0.3rem" }}>{g.byId.get(goal).name}</h3>
              <p class="small">{g.byId.get(goal).desc}</p>
              <p class="small"><b>{ps.stops} 站</b> · {ps.withContent} 站有互动课（{hours(ps.minutes)}），{g.tree.meta.edition === "toy" ? "其余可查看章节。" : "其余是“按章读资料 + 综合练习”。"}</p>
              <ol>{preview.stops.map((id) => <li class={packs[id] ? "has-lessons" : ""}>{g.byId.get(id).name}{packs[id] ? "" : g.tree.meta.edition === "toy" ? "（开发中）" : "（自学）"}</li>)}</ol>
              <button type="button" class="btn primary wide" disabled={!playable(preview)} onClick={() => setRoute(preview.id)}>以它为目标出发</button>
            </>
          ) : (
            <div class="center">
              <Sprite who="black" action="idle" scale={2} />
              <p class="small muted">从左边选一个技能，看看要走哪些站。</p>
            </div>
          )}
        </aside>
      </div>
    </>
  );
}
