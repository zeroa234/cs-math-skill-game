// Inputs for every item type. Each gets { item, value, setValue, locked, result } and only collects a
// response; checking happens in the lesson player through core/check.js.
import { useMemo } from "preact/hooks";
import { Md } from "./md.jsx";
import { SIM_VIEWS } from "../sims/views/index.jsx";

// Deterministic shuffle per item id, so a re-render never reorders options under the player's finger.
function seededOrder(n, key) {
  let h = 2166136261;
  for (const c of key) h = Math.imul(h ^ c.charCodeAt(0), 16777619);
  const idx = [...Array(n).keys()];
  for (let i = n - 1; i > 0; i--) {
    h = Math.imul(h ^ (h >>> 13), 1274126177);
    const j = (h >>> 0) % (i + 1);
    [idx[i], idx[j]] = [idx[j], idx[i]];
  }
  if (n > 1 && idx.every((v, i) => v === i)) idx.push(idx.shift());
  return idx;
}

export function initialValue(item) {
  if (item.type === "choice") return item.multi ? [] : null;
  if (item.type === "order" || item.type === "match") return [];
  if (item.type === "sim") return SIM_VIEWS[item.sim]?.initial?.(item.params || {}, item.goal || {}) ?? null;
  return "";
}

export function isAnswerable(item, value) {
  if (item.type === "choice") return item.multi ? value.length > 0 : value !== null;
  if (item.type === "order") return value.length === item.steps.length;
  if (item.type === "match") return value.length === item.pairs.length && value.every((v) => v !== undefined && v !== null);
  if (item.type === "sim") return value !== null && value !== undefined;
  return String(value).trim() !== "";
}

export function ItemInput(props) {
  const { item } = props;
  const C = { choice: Choice, number: NumberIn, text: TextIn, order: Order, match: Match, sim: Sim }[item.type];
  return (
    <div class={"item item-" + item.type}>
      <Md text={item.prompt} class="prompt" />
      {item.code && <pre class="code"><code>{item.code}</code></pre>}
      <C {...props} />
    </div>
  );
}

function Choice({ item, value, setValue, locked, result }) {
  const order = useMemo(() => seededOrder(item.options.length, item.id), [item.id]);
  const picked = (i) => (item.multi ? value.includes(i) : value === i);
  const toggle = (i) => {
    if (locked) return;
    if (item.multi) setValue(picked(i) ? value.filter((x) => x !== i) : [...value, i]);
    else setValue(i);
  };
  return (
    <div class="options" role={item.multi ? "group" : "radiogroup"}>
      {item.multi && <p class="muted small">可多选</p>}
      {order.map((i, k) => {
        const o = item.options[i];
        const cls = ["option", picked(i) && "picked", result && o.correct && "is-correct", result && picked(i) && !o.correct && "is-wrong"].filter(Boolean).join(" ");
        return (
          <button type="button" class={cls} aria-pressed={picked(i)} onClick={() => toggle(i)} disabled={locked}>
            <span class="key">{k + 1}</span>
            <span class="otext"><Md text={o.text} inline /></span>
            {result && picked(i) && o.why && !o.correct && <span class="why"><Md text={o.why} inline /></span>}
          </button>
        );
      })}
    </div>
  );
}

function NumberIn({ item, value, setValue, locked, result }) {
  return (
    <label class={"answer-line" + (result ? (result.correct ? " is-correct" : " is-wrong") : "")}>
      <input type="text" inputmode="decimal" value={value} disabled={locked} placeholder="输入数字，可写 3/2、50%、2^10" onInput={(e) => setValue(e.currentTarget.value)} aria-label="答案" />
      {item.unit && <span class="unit">{item.unit}</span>}
    </label>
  );
}

function TextIn({ item, value, setValue, locked, result }) {
  return (
    <label class={"answer-line" + (result ? (result.correct ? " is-correct" : " is-wrong") : "")}>
      <input type="text" value={value} disabled={locked} placeholder={item.placeholder || "输入答案"} onInput={(e) => setValue(e.currentTarget.value)} aria-label="答案" autocomplete="off" spellcheck={false} />
    </label>
  );
}

function Order({ item, value, setValue, locked, result }) {
  const pool = useMemo(() => seededOrder(item.steps.length, item.id), [item.id]);
  const left = pool.filter((i) => !value.includes(i));
  return (
    <div class="order">
      <ol class="order-answer">
        {value.map((i, k) => (
          <li><button type="button" class={"chip" + (result ? (i === k ? " is-correct" : " is-wrong") : "")} disabled={locked} onClick={() => setValue(value.filter((x) => x !== i))}><code>{item.steps[i]}</code></button></li>
        ))}
        {!value.length && <li class="muted small placeholder">按正确顺序点下面的卡片</li>}
      </ol>
      <div class="order-pool">
        {left.map((i) => <button type="button" class="chip" disabled={locked} onClick={() => setValue([...value, i])}><code>{item.steps[i]}</code></button>)}
      </div>
      {result && !result.correct && <p class="small">正确顺序：{item.steps.map((s, i) => <code class="inline-step">{i + 1}. {s}</code>)}</p>}
    </div>
  );
}

function Match({ item, value, setValue, locked, result }) {
  const rights = useMemo(() => seededOrder(item.pairs.length, item.id + "/r"), [item.id]);
  const active = value.findIndex((v) => v === undefined || v === null);
  const current = active === -1 ? (value.length < item.pairs.length ? value.length : -1) : active;
  const choose = (r) => {
    if (locked || current === -1) return;
    const next = [...value];
    const was = next.indexOf(r);
    if (was !== -1) next[was] = null;
    next[current] = r;
    setValue(next);
  };
  const clear = (i) => { if (locked) return; const next = [...value]; next[i] = null; setValue(next); };
  return (
    <div class="match">
      <ul class="match-left">
        {item.pairs.map((p, i) => {
          const r = value[i];
          const st = result ? (r === i ? " is-correct" : " is-wrong") : "";
          return (
            <li class={(i === current && !locked ? "current " : "") + st}>
              <span class="ml"><Md text={p[0]} inline /></span>
              <span class="arrow">→</span>
              {r !== undefined && r !== null ? <button type="button" class="chip" onClick={() => clear(i)} disabled={locked}><Md text={item.pairs[r][1]} inline /></button> : <span class="slot">{i === current ? "选右边一项" : "…"}</span>}
              {result && r !== i && <span class="small muted">应为 <Md text={p[1]} inline /></span>}
            </li>
          );
        })}
      </ul>
      <div class="match-right">
        {rights.map((r) => <button type="button" class={"chip" + (value.includes(r) ? " used" : "")} disabled={locked} onClick={() => choose(r)}><Md text={item.pairs[r][1]} inline /></button>)}
      </div>
    </div>
  );
}

function Sim({ item, value, setValue, locked, result }) {
  const V = SIM_VIEWS[item.sim];
  if (!V) return <p class="bad">缺少交互组件 {item.sim}</p>;
  return <V.View params={item.params || {}} goal={item.goal || {}} value={value} setValue={setValue} locked={locked} result={result} />;
}

export function SimDemo({ sim }) {
  const V = SIM_VIEWS[sim.name];
  if (!V) return null;
  return <V.Demo params={sim.params || {}} />;
}
