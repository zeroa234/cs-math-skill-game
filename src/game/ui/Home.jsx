// 营地 (home): one big "continue" for the campaign you are on, today's numbers, reviews that are due,
// and what else is open. Choosing or changing a campaign happens on 选远征 (#/pick).
import { g, packs, store, useProgress, routeNext, dueCards, stateOf, activeRoute } from "../app/state.js";
import { href } from "../app/router.js";
import { levelOf, streak } from "../core/progress.js";
import { nextUp } from "../core/rules.js";
import { todayXp } from "../app/actions.js";
import { Bar, StatusBadge, LaneDot, unitLabel } from "./common.jsx";
import { Sprite } from "./cast.jsx";
import { artFor } from "../app/art.js";
import { KIND_LABEL } from "../core/route-text.js";
import { Icon } from "./icons.jsx";
import { VERSION, useFoundUpdate, dismissUpdate } from "../app/update.js";

export function nextAction(p, st) {
  if (!st) return null;
  if (!st.hasContent) return { label: "互动课开发中，可查看自学资料", hash: href("skill", st.skill.id), no: <Icon name="book" size={36} /> };
  if (st.status === "locked") return { label: "先学它要求的技能", hash: href("skill", st.skill.id) };
  if (st.nextChapter) {
    const ch = st.nextChapter;
    return ch.kind === "lesson"
      ? { label: `${unitLabel(ch)}：${ch.lesson.title}`, hash: href("lesson", st.skill.id, ch.key), no: ch.no }
      : { label: `${unitLabel(ch)}：${ch.chapter.title}（读教材）`, hash: href("skill", st.skill.id), no: ch.no };
  }
  return { label: "结业挑战", hash: href("boss", st.skill.id), no: <Icon name="crown" size={36} /> };
}

export function Home() {
  const p = useProgress();
  const lv = levelOf(p.xp);
  const due = dueCards(p).length;
  const upd = useFoundUpdate();
  const active = activeRoute(p);
  const fresh = !Object.keys(p.lessons).length && !Object.values(p.skills).some((s) => s.lit);
  const open = nextUp(g, packs, p).slice(0, 6);
  const st = active ? routeNext(p, active) : null;
  const act = nextAction(p, st);
  const lit = active ? active.stops.filter((id) => stateOf(p, id).status === "lit").length : 0;
  return (
    <div class="page home">
      <section class="camp-hero pixel-bg" style={{ backgroundImage: `url(${artFor(active)})` }}>
        <div>
          <h1>{fresh ? "欢迎参加计算机大学习！" : "营地"}</h1>
          <p>{active ? `正在进行：${active.name}（${KIND_LABEL[active.kind]}）` : `${g.tree.skills.length} 个技能、每一条“要先学”的连线都有大学课程作证据。一次一小课，把技能一个个点亮。`}</p>
          <div class="camp-stats">
            <span class="stat-chip" title="学徒等级"><Icon name="zap" /> Lv.{lv.level} · {lv.into}/{lv.span}</span>
            <span class="stat-chip" title="今天获得的经验">今天 +{todayXp(p)}</span>
            <span class="stat-chip" title="连续学习天数"><Icon name="fire" /> {streak(p)} 天</span>
            <a class="stat-chip" href={href("review")} title="到期的复习题"><Icon name="reload" /> 复习 {due}</a>
          </div>
        </div>
        <div class="mentors" aria-hidden="true">
          <Sprite who="black" action="idle" scale={2} />
          <Sprite who="blue" action="wave" then="idle" scale={2} flip />
        </div>
      </section>

      {active ? (
        <section class="card continue" style={{ "--lane": st ? g.lanes.get(st.skill.lane).color : "var(--gold)" }}>
          <div class="unit-icon" aria-hidden="true">{st ? act.no : <Icon name="sparkle" size={36} />}</div>
          <div>
            <div class="small muted">{active.name}{st ? ` · 第 ${active.stops.indexOf(st.skill.id) + 1} 站` : ""}</div>
            {st ? <><h2>{st.skill.name}</h2><div>{act.label}</div></> : <><h2>这条远征完成了！</h2><div>去换一条远征，或者自己定一个新目标。</div></>}
            <Bar value={lit / active.stops.length} label="远征进度" />
            <div class="small muted">已点亮 {lit} / {active.stops.length} 站</div>
            <div class="row">
              <a class="btn small" href={href("route", active.id)}>看整条路线</a>
              {st && <a class="btn small" href={href("pick")}>换一条远征</a>}
            </div>
          </div>
          {st ? <a class="btn primary big" href={act.hash}>继续</a> : <a class="btn primary big" href={href("pick")}>选新远征</a>}
        </section>
      ) : (
        <section class="card continue" style={{ "--lane": "var(--accent)" }}>
          <div class="unit-icon" aria-hidden="true">?</div>
          <div><h2>还没选远征</h2><div>挑一个目标，游戏会排好从零到目标的每一站。</div></div>
          <a class="btn primary big" href={href("pick")}>选远征</a>
        </section>
      )}

      {upd && <section class="card review-banner"><span><b>有新版本 {upd.latest}</b>（现在是 {VERSION}）。下载后点开安装，进度不会丢。</span><span class="row"><a class="btn primary" href={upd.download} target="_blank" rel="noopener">下载</a><button type="button" class="btn ghost" onClick={dismissUpdate}>以后再说</button></span></section>}
      {due > 0 && !fresh && <section class="card review-banner"><span><b>有 {due} 道题到了复习时间。</b> 隔一段时间再想起来，记得最牢。</span><a class="btn primary" href={href("review")}>开始复习</a></section>}

      {!fresh && open.length > 0 && (
        <section>
          <h2>现在能学</h2>
          <p class="small muted">要先学的技能都已完成的技能，学完能解锁更多后续的排在前面。</p>
          <ul class="open-list">
            {open.map((s) => <li><a href={href("skill", s.skill.id)}><LaneDot skill={s.skill} />{s.skill.name}</a> <StatusBadge status={s.status} /></li>)}
          </ul>
        </section>
      )}

      <p class="small muted center" style={{ marginTop: "2rem" }}>
        <a href={href("map")}>完整技能地图</a> · <a href={href("lab")}>实验室：玩课里出现过的实验</a> · <a href={href("intro")} onClick={() => store.update((d) => { d.settings.introSeen = false; })}>重看开场</a>
      </p>
    </div>
  );
}
