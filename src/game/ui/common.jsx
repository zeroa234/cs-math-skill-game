// Small shared pieces: status badge, stars, progress bar, source links, toasts.
import { useEffect, useState } from "preact/hooks";
import { g, laneOf } from "../app/state.js";
import { href } from "../app/router.js";
import { mastery } from "../core/rules.js";
import { Icon } from "./icons.jsx";

export const STATUS = {
  dev: { icon: "book", label: "开发中" },
  locked: { icon: "lock", label: "未解锁" },
  open: { icon: "play", label: "现在能学" },
  learning: { icon: "book", label: "学习中" },
  lit: { icon: "sparkle", label: "已点亮" },
};
// A playable step of a skill: lessons are counted as 课 (a chapter can have several), reading
// chapters of a skill without a pack as 章.
export const unitLabel = (c) => (c.kind === "lesson" ? `第 ${c.no} 课` : `第 ${c.no} 章`);
export const MASTERY = { lit: "已点亮", solid: "熟练", mastered: "精通" };

export function StatusBadge({ status, p, id }) {
  const s = STATUS[status];
  const m = status === "lit" && p ? mastery(p, id) : null;
  return <span class={"badge st-" + status}><Icon name={s.icon} /> {m && m !== "lit" ? MASTERY[m] : s.label}</span>;
}

export function Stars({ n, max = 3 }) {
  return <span class="stars" aria-label={`${n} 颗星`}>{Array.from({ length: max }, (_, i) => <Icon name="star" class={i < n ? "on" : "off"} />)}</span>;
}

export function Bar({ value, label }) {
  return <div class="bar-track" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow={Math.round(value * 100)} aria-label={label}><div class="bar-fill" style={{ width: `${Math.round(value * 100)}%` }} /></div>;
}

export function SkillLink({ id, children }) {
  const s = g.byId.get(id);
  return <a href={href("skill", id)} class="skill-link" style={{ "--lane": laneOf(s).color }}>{children || s.name}</a>;
}

export function LaneDot({ skill }) {
  return <span class="lane-dot" style={{ background: laneOf(skill).color }} title={laneOf(skill).name} />;
}

const TIER = { video: "视频", website: "网页", book: "书", paper: "论文", course: "课程" };
// One chapter's sources, by the player's language preference.
export function ChapterSources({ skill, chapter, lang = "zh" }) {
  const byKey = Object.fromEntries(skill.sources.map((s) => [s.key, s]));
  const langs = lang === "both" ? ["zh", "en"] : [lang, lang === "zh" ? "en" : "zh"];
  const groups = langs.map((l) => [l, chapter[l] || []]).filter(([, refs]) => refs.length);
  const shown = lang === "both" ? groups : groups.slice(0, 1);
  if (!shown.length) return <p class="small muted">这一章还没有找到可核对的学习资料。</p>;
  return (
    <ul class="sources">
      {shown.map(([l, refs]) => refs.map((r) => {
        const src = byKey[r.source];
        if (!src) return null;
        return (
          <li>
            <span class={"tag lang-" + l}>{l === "zh" ? "中文" : "英文"}</span>
            {src.tier && <span class="tag">{TIER[src.tier] || src.tier}</span>}
            {src.free === false && <span class="tag warn">付费</span>}
            {r.extent === "partial" && <span class="tag">部分覆盖</span>}
            <a href={src.url} target="_blank" rel="noopener">{src.title}</a>
            <div class="small">读：{r.section}</div>
          </li>
        );
      }))}
      {lang !== "both" && groups.length > 1 && <li class="small muted">另有{groups[1][0] === "zh" ? "中文" : "英文"}资料，可在“我的 → 设置”里改成双语显示。</li>}
    </ul>
  );
}

// Achievement / XP toasts.
let pushToast = () => {};
export const toast = (t) => pushToast(t);
export function Toasts() {
  const [list, setList] = useState([]);
  useEffect(() => {
    pushToast = (t) => {
      const id = Math.random();
      setList((l) => [...l, { ...t, id }]);
      setTimeout(() => setList((l) => l.filter((x) => x.id !== id)), 4200);
    };
  }, []);
  return <div class="toasts" role="status" aria-live="polite">{list.map((t) => <div class="toast"><b>{t.title}</b>{t.body && <span>{t.body}</span>}</div>)}</div>;
}
