// One skill: briefing, chapters 1..n with where to read more, final challenge, prerequisites with
// evidence, and the knowledge map (outline) renumbered within the skill.
import { useEffect, useState } from "preact/hooks";
import { g, packs, useProgress, stateOf, laneOf, activeRoute } from "../app/state.js";
import { href, lastHub } from "../app/router.js";
import { lessonKey, satisfied } from "../core/rules.js";
import { bossFlow, PASS_SHARE } from "../core/lesson.js";
import { StatusBadge, Stars, SkillLink, ChapterSources, Bar, unitLabel } from "./common.jsx";
import { Icon } from "./icons.jsx";
import { Md } from "./md.jsx";

function useOutline(id) {
  const [o, setO] = useState(window.__OUTLINES__?.[id] || null);
  useEffect(() => {
    if (window.__OUTLINES__) { setO(window.__OUTLINES__[id] || null); return; }
    const sc = document.createElement("script");
    sc.src = "outlines.js";
    sc.onload = () => setO(window.__OUTLINES__?.[id] || null);
    document.head.appendChild(sc);
  }, [id]);
  return o;
}

export function SkillView({ id }) {
  const p = useProgress();
  const skill = g.byId.get(id);
  const [openCh, setOpenCh] = useState(null);
  const [showMap, setShowMap] = useState(false);
  if (!skill) return <div class="page"><p>没有这个技能。<a href={href("map")}>去地图</a></p></div>;
  const st = stateOf(p, id);
  const lane = laneOf(skill);
  const pack = packs[id];
  const lang = p.settings.sourceLang || "zh";
  const lit = st.status === "lit";
  const boss = bossFlow(skill, pack);
  // Back to where the player came from; opened directly (a bookmark), back to the route or the map.
  const route = activeRoute(p);
  const back = lastHub() || (route ? { hash: href("route", route.id), label: "路线" } : { hash: href("map"), label: "地图" });
  return (
    <div class="page skill" style={{ "--lane": lane.color }}>
      <header class="page-head skill-head">
        <a class="back" href={back.hash}><Icon name="back" /> {back.label}</a>
        <div class="kicker">{lane.name} · {skill.id}{skill.optional ? " · 选修" : ""}{skill.origin === "game-extension" ? " · 游戏新增" : ""}</div>
        <h1>{skill.name} <span class="en">{skill.en}</span></h1>
        <StatusBadge status={st.status} p={p} id={id} />
        <p class="lead">{pack?.brief?.why || skill.desc}</p>
        {pack?.brief?.outcomes && <div class="outcomes"><b>学完你能：</b><ul>{pack.brief.outcomes.map((o) => <li><Md text={o} inline /></li>)}</ul></div>}
        {pack && <Bar value={st.progress} label="章节进度" />}
        <div class="row">
          {st.status === "locked" ? <span class="muted">先学：{st.missing.map((m) => <SkillLink id={m} />)}</span> : st.nextChapter?.kind === "lesson" ? <a class="btn primary big" href={href("lesson", id, st.nextChapter.key)}>{st.done.some(Boolean) ? "继续" : "开始"}：{unitLabel(st.nextChapter)}</a> : st.bossOpen && !lit ? <a class="btn primary big" href={href("boss", id)}>{pack ? "结业挑战" : "综合练习"}</a> : null}
          {st.status !== "locked" && !lit && boss.graded && <a class="btn ghost" href={href("boss", id, "test")} title="已经会了？直接做结业挑战，答对 80% 就点亮">跳级挑战</a>}
        </div>
        {skill.extensionNote && <p class="small muted">{skill.extensionNote}</p>}
      </header>

      <section>
        <h2>章节</h2>
        {!pack && <p class="small muted">互动课开发中。可以按前后置指引和“去哪深入”的教材自学，也可以直接查看综合练习与参考答案；自学不记录完成、不点亮技能。</p>}
        <ol class="chapters">
          {st.chapters.map((c, i) => {
            const done = st.done[i];
            const canOpen = st.chapterOpen(i);
            const rec = c.kind === "lesson" ? p.lessons[lessonKey(id, c.key)] : null;
            return (
              <li class={"chapter" + (done ? " done" : "") + (canOpen ? "" : " locked")}>
                <div class="ch-row">
                  <span class="ch-no">{c.no}</span>
                  <div class="ch-main">
                    <div class="ch-title">{c.kind === "lesson" ? c.lesson.title : c.chapter.title}{!c.core && <span class="tag">选学</span>}</div>
                    {c.kind === "lesson" && <div class="small muted">学：{c.chapter.title} · 约 {c.lesson.minutes || 8} 分钟 · {c.lesson.items.length} 题</div>}
                  </div>
                  {rec?.stars ? <Stars n={rec.stars} /> : null}
                  {c.kind === "lesson" ? (
                    canOpen ? <a class={"btn small" + (done ? " ghost" : " primary")} href={href("lesson", id, c.key)}>{done ? "再练" : "开始"}</a> : <span class="small muted lock"><Icon name="lock" label="未解锁" /></span>
                  ) : null}
                  <button type="button" class="btn small ghost" aria-expanded={openCh === i} onClick={() => setOpenCh(openCh === i ? null : i)}>去哪深入</button>
                </div>
                {openCh === i && (
                  <div class="ch-more">
                    {c.chapter.note && <p class="small muted">{c.chapter.note}</p>}
                    <ChapterSources skill={skill} chapter={c.chapter} lang={lang} />
                  </div>
                )}
              </li>
            );
          })}
          <li class={"chapter boss" + (lit ? " done" : "") + (st.bossOpen ? "" : " locked")}>
            <div class="ch-row">
              <span class="ch-no"><Icon name="crown" /></span>
              <div class="ch-main"><div class="ch-title">{pack ? "结业挑战" : "综合练习"}</div><div class="small muted">{boss.graded ? `${boss.items.length} 道题，第一次答对 ${Math.round(PASS_SHARE * 100)}% 点亮` : skill.exercise ? `约 ${skill.exercise.minutes} 分钟，覆盖 ${skill.exercise.covers.join("、")}，不计分` : "资料整理中"}</div></div>
              {!pack ? <a class="btn small primary" href={href("boss", id)}>查看题目与答案</a> : lit ? <span class="badge st-lit"><Icon name="sparkle" /> 已点亮</span> : st.bossOpen ? <a class="btn small primary" href={href("boss", id)}>挑战</a> : <span class="small muted">学完全部核心章后开放</span>}
            </div>
          </li>
        </ol>
        {skill.chapterOrder.basis !== "original" && skill.chapterOrder.basis !== "extension" && <p class="small muted">章节顺序按主教材《{skill.chapterOrder.source}》的讲授顺序排列。</p>}
      </section>

      <section class="grid2">
        <div class="card">
          <h3>必须先学</h3>
          {skill.required.length ? <ul class="prereqs">{skill.required.map((r) => <li><SkillLink id={r.id} /> {satisfied(p, r.id) ? <Icon name="check" label="已点亮" /> : ""}<div class="small">{r.why}</div></li>)}</ul> : <p class="small">没有：这是起点。{skill.prereqSummary}</p>}
          {skill.recommended.length > 0 && <><h4>推荐先学（不挡路）</h4><ul class="prereqs">{skill.recommended.map((r) => <li><SkillLink id={r.id} /><div class="small">{r.why}</div></li>)}</ul></>}
        </div>
        <div class="card">
          <h3>课程证据</h3>
          <ul class="evidence-list">
            {skill.courses.map((c) => <li><a href={c.url} target="_blank" rel="noopener">{c.school} · {c.course}</a><blockquote class="small">{c.prereq}</blockquote>{c.content && <div class="small muted">课程内容：{c.content}</div>}</li>)}
            {(skill.kth || []).map((k) => <li><a href={k.url} target="_blank" rel="noopener">KTH · {k.code} {k.name}（{k.credits} 学分）</a><blockquote class="small">{k.quote}</blockquote><div class="small muted">{k.fit}。{k.needs.length ? "先修与技能树一致：" + k.needs.map((n) => `${n.courses} → ${g.byId.get(n.skill).name}${n.inClosure ? " ✓" : " ✗"}`).join("；") : ""}{k.note ? " " + k.note : ""}（{k.fetched} 读取）</div></li>)}
          </ul>
          {skill.unlocks.length > 0 && <><h4>后续技能</h4><p>{skill.unlocks.map((u) => <SkillLink id={u} />)}</p></>}
        </div>
      </section>

      {skill.hasOutline && (
        <section>
          <button type="button" class="btn ghost" aria-expanded={showMap} onClick={() => setShowMap(!showMap)}>{showMap ? "收起" : "展开"}知识地图（主教材目录）</button>
          {showMap && <OutlineMap id={id} />}
        </section>
      )}
    </div>
  );
}

function OutlineMap({ id }) {
  const o = useOutline(id);
  if (!o) return <p class="small muted">加载中…</p>;
  const srcs = Object.fromEntries(o.sources.map((s) => [s.key, s]));
  const items = (list) => list.length > 0 && <ul>{list.map((it) => <li><span class="small">{it.no} {it.zh || it.title}</span>{it.sourceRef && <span class="tag">§{it.sourceRef}</span>}{items(it.items || [])}</li>)}</ul>;
  return (
    <div class="outline card">
      <p class="small muted">来源：{o.sources.map((s) => <a href={s.url} target="_blank" rel="noopener">{s.title}{s.by ? `（${s.by}）` : ""}</a>)}。编号是本技能内部的顺序；灰色标签是教材自己的节号。</p>
      <ol>
        {o.branches.map((b) => (
          <li>
            <b>{b.no}. {b.zh || b.title}</b> {b.sourceRef && <span class="tag">{o.sources.length > 1 ? b.src + " " : ""}§{b.sourceRef}</span>} <span class="small muted">{b.zh && b.title}</span>
            {items(b.items)}
          </li>
        ))}
      </ol>
    </div>
  );
}
