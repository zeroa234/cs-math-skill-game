// One player for everything that is played a step at a time: lessons, final challenges, reviews.
// Same layout everywhere (H4 consistency): the mentor beside the content reacts to each answer; the
// check / continue button and the verdict sit in a bar fixed to the bottom of the screen.
//
// flow: [{ kind: "guess" | "item", item } | { kind: "card", card }] (see core/lesson.js).
// A wrong graded item is explained right away and comes back once at the end; nothing is taken away.
// onFinish(results) gets { [itemId]: { item, correct, firstTry, usedHint } } for graded items.
import { useEffect, useMemo, useState } from "preact/hooks";
import { checkItem } from "../core/check.js";
import { play } from "../app/sound.js";
import { ItemInput, initialValue, isAnswerable, SimDemo } from "./items.jsx";
import { Md } from "./md.jsx";
import { Sprite } from "./cast.jsx";
import { Icon } from "./icons.jsx";

const PRAISE = ["答对了！", "太棒了！", "漂亮！", "完全正确！"];
const pickOne = (list, seed) => list[Math.abs([...seed].reduce((h, c) => h * 31 + c.charCodeAt(0), 7)) % list.length];

export function StepPlayer({ kicker, title, closeHref, flow, coach = "blue", itemLabel = "练习", leaveText = "这一课的进度不会保存。", onFinish }) {
  const steps = useMemo(() => flow.map((s, i) => ({ ...s, key: (s.item?.id || "card") + "-" + i })), [flow]);
  const [pos, setPos] = useState(0);
  const [retries, setRetries] = useState([]);
  const [results, setResults] = useState({});
  const [mood, setMood] = useState({ action: "idle", say: "一起来吧！", cue: 0 });
  const [leaving, setLeaving] = useState(false);
  const total = steps.length + retries.length;
  const cur = pos < steps.length ? steps[pos] : { kind: "item", item: retries[pos - steps.length], retry: true, key: "retry-" + pos };
  const progress = Math.min(1, pos / total);
  const cardCount = steps.filter((s) => s.kind === "card").length;
  const cardIndex = steps.slice(0, pos).filter((s) => s.kind === "card").length;

  const advance = (nextRetries = retries, nextResults = results) => {
    if (pos + 1 >= steps.length + nextRetries.length) onFinish(nextResults);
    else setPos(pos + 1);
  };
  const react = (result, guess, key) => {
    if (result.correct) setMood({ action: ["jump_start", "jump_land", "idle"], say: guess ? "猜对了！" : pickOne(PRAISE, key), cue: Math.random() });
    else setMood({ action: ["coy", "idle"], say: guess ? "没关系，看完讲解就懂了" : "差一点点，看看解析～", cue: Math.random() });
  };
  const onItemDone = (step, result, usedHint) => {
    if (step.kind === "guess") { setMood({ action: "idle", say: "来看看讲解", cue: Math.random() }); return advance(); }
    const id = step.item.id;
    const prev = results[id];
    const next = { ...results, [id]: { item: step.item, correct: result.correct, firstTry: step.retry ? prev.firstTry : result.correct, usedHint: usedHint || prev?.usedHint || false } };
    setResults(next);
    const nextRetries = !result.correct && !step.retry ? [...retries, step.item] : retries;
    setRetries(nextRetries);
    setMood({ action: "idle", say: "下一题！", cue: Math.random() });
    advance(nextRetries, next);
  };

  return (
    <div class="player">
      <header class="player-head">
        {leaving ? (
          <div class="row leave-row">
            <span><b>现在退出？</b> {leaveText}</span>
            <span class="row"><button type="button" class="btn small" onClick={() => setLeaving(false)}>接着学</button><a class="btn small warn" href={closeHref}>退出</a></span>
          </div>
        ) : (
          <>
            <button type="button" class="close" aria-label="退出" onClick={() => (pos === 0 ? (location.hash = closeHref) : setLeaving(true))}><Icon name="close" /></button>
            <div class="ptitle"><span class="small muted">{kicker}</span><b>{title}</b></div>
            <span class="pcount" aria-label={`第 ${pos + 1} 步，共 ${total} 步`}>{pos + 1} / {total}</span>
          </>
        )}
        <div class="pbar" role="progressbar" aria-label="进度" aria-valuenow={Math.round(progress * 100)} aria-valuemin="0" aria-valuemax="100"><div style={{ width: `${progress * 100}%` }} /></div>
      </header>
      <div class="player-stage">
        <aside class="coach" aria-hidden="true">
          <div class="say">{mood.say}</div>
          <Sprite who={coach} action={mood.action} cue={mood.cue} scale={2} />
        </aside>
        <main class="player-body">
          {cur.kind === "card"
            ? <CardStep key={cur.key} card={cur.card} index={cardIndex} count={cardCount} onNext={() => { play("page"); advance(); }} onBack={pos > 0 && steps[pos - 1].kind === "card" ? () => setPos(pos - 1) : null} />
            : <ItemStep key={cur.key} item={cur.item} label={cur.kind === "guess" ? "先猜一猜（不计分）" : cur.retry ? "再来一次" : itemLabel} guess={cur.kind === "guess"} retry={cur.retry} onResult={(r) => react(r, cur.kind === "guess", cur.item.id)} onDone={(r, h) => onItemDone(cur, r, h)} />}
        </main>
      </div>
    </div>
  );
}

// An explanation card. `reveal` parts (a worked example's steps, or a reference answer) appear one at
// a time on the same button, so the player thinks about each step before seeing the next.
function CardStep({ card, index, count, onNext, onBack }) {
  const parts = card.reveal || [];
  const [shown, setShown] = useState(0);
  const more = shown < parts.length;
  const next = () => { if (more) { play("tap"); setShown(shown + 1); } else onNext(); };
  useKey("Enter", next);
  useEffect(() => { if (shown) document.querySelector(".reveal-part:last-of-type")?.scrollIntoView({ block: "nearest", behavior: "smooth" }); }, [shown]);
  return (
    <>
      <article class="lcard">
        <div class="step-kind">讲解 {index + 1} / {count}</div>
        {card.title && <h2>{card.title}</h2>}
        <Md text={card.body} />
        {card.sim && <SimDemo sim={card.sim} />}
        {parts.slice(0, shown).map((r, i) => (
          <section class="reveal-part">
            {r.title && <h3>{r.title}</h3>}
            <Md text={r.body} />
          </section>
        ))}
      </article>
      <div class="answer-bar">
        <div class="inner">
          <div class="verdict">{onBack && <button type="button" class="btn ghost" onClick={onBack}>上一步</button>}</div>
          <button type="button" class="btn primary" onClick={next}>{more ? parts[shown].button || "下一步" : "继续"}</button>
        </div>
      </div>
    </>
  );
}

export function ItemStep({ item, label, guess, retry, onDone, onResult, verdicts }) {
  const [value, setValue] = useState(() => initialValue(item));
  const [result, setResult] = useState(null);
  const [hint, setHint] = useState(false);
  const ready = isAnswerable(item, value);
  const pickSound = ["choice", "order", "match"].includes(item.type);
  const set = (v) => { if (pickSound) play("select"); setValue(v); };
  const check = () => {
    if (!ready || result) return;
    const r = checkItem(item, value);
    setResult(r);
    play(r.correct ? "correct" : "wrong");
    onResult?.(r);
  };
  const next = () => onDone(result, hint);
  useKey("Enter", result ? next : check);
  useDigits(item, result, set);
  const v = verdicts || { right: guess ? "猜对了！" : "答对了！", wrong: guess ? "没关系，看完讲解就明白了" : retry ? "这次也没对，看一下解析" : "还差一点" };
  return (
    <>
      <article class={"lcard qcard" + (result ? (result.correct ? " is-good" : " is-bad") : "")} data-item={item.id}>
        {label && <div class="step-kind">{label}</div>}
        <ItemInput item={item} value={value} setValue={set} locked={!!result} result={result} />
        {item.hint && !result && (hint ? <p class="hint"><Icon name="bulb" /> <Md text={item.hint} inline /></p> : <button type="button" class="btn ghost small" onClick={() => { play("tap"); setHint(true); }}>提示</button>)}
      </article>
      <div class={"answer-bar" + (result ? (result.correct ? " is-good slide" : " is-bad slide") : "")}>
        <div class="inner">
          <div class="verdict" role="status">
            {result && <>
              <b><Icon name={result.correct ? "check" : "close"} /> {result.correct ? v.right : v.wrong}</b>
              <Md text={item.explain} />
              {!result.correct && !guess && !retry && v.again !== false && <p class="small muted">这题最后会再出现一次。</p>}
            </>}
          </div>
          {!result ? <button type="button" class="btn primary" disabled={!ready} onClick={check}>检查</button> : <button type="button" class={"btn " + (result.correct ? "good" : "warn")} onClick={next}>继续</button>}
        </div>
      </div>
    </>
  );
}

export function useKey(key, fn) {
  useEffect(() => {
    const on = (e) => {
      if (e.key !== key || e.isComposing) return;
      const t = e.target;
      if (t && (t.tagName === "TEXTAREA" || (t.tagName === "BUTTON" && key === "Enter"))) return;
      e.preventDefault();
      fn();
    };
    window.addEventListener("keydown", on);
    return () => window.removeEventListener("keydown", on);
  }, [key, fn]);
}

// 1–9 pick a choice option (in the order shown).
function useDigits(item, result, setValue) {
  useEffect(() => {
    if (item.type !== "choice" || result) return;
    const on = (e) => {
      if (!/^[1-9]$/.test(e.key) || e.target?.tagName === "INPUT") return;
      const btns = [...document.querySelectorAll(".qcard .option")];
      btns[Number(e.key) - 1]?.click();
    };
    window.addEventListener("keydown", on);
    return () => window.removeEventListener("keydown", on);
  }, [item, result]);
}
