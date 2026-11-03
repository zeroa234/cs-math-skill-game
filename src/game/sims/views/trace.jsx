// Code stepper for real Python runs (steps recorded at build time). As a lesson card it is a free
// stepper; as an exercise the player predicts first and the stepper opens after checking.
import { useState } from "preact/hooks";
import { trace as tLogic } from "../logic/trace.js";

function Stepper({ params: p, start = 0 }) {
  const steps = p.steps || [];
  const [i, setI] = useState(start);
  const lines = p.code.replace(/\n$/, "").split("\n");
  const st = steps[i] || { vars: {}, out: "" };
  const prevVars = i > 0 ? steps[i - 1].vars : {};
  return (
    <div class="stepper">
      <ol class="codelines">
        {lines.map((l, k) => <li class={st.line === k + 1 ? "cur" : ""}><span class="ln">{k + 1}</span><code>{l || " "}</code></li>)}
      </ol>
      <div class="state">
        <p class="small muted">{st.line ? <>即将执行第 <b>{st.line}</b> 行{st.func !== "<module>" ? `（在函数 ${st.func} 里）` : ""}</> : st.ret !== undefined && st.func !== "<module>" ? <>函数 {st.func} 执行完，交回 <code>{st.ret}</code></> : "程序结束"}</p>
        {st.stack && <p class="small callstack">调用栈（最早的在左）：{st.stack.map((f) => (f === "<module>" ? "主程序" : f)).join(" → ")}</p>}
        <table class="vars"><tbody>
          {Object.entries(st.vars).map(([k, v]) => <tr class={prevVars[k] !== v ? "changed" : ""}><th>{k}</th><td><code>{v}</code></td></tr>)}
          {!Object.keys(st.vars).length && <tr><td class="muted small">（还没有变量）</td></tr>}
        </tbody></table>
        {st.out && <pre class="console">{st.out}</pre>}
        <div class="btns">
          <button type="button" class="btn small ghost" disabled={i === 0} onClick={() => setI(0)}>从头</button>
          <button type="button" class="btn small ghost" disabled={i === 0} onClick={() => setI(i - 1)}>上一步</button>
          <button type="button" class="btn small" disabled={i >= steps.length - 1} onClick={() => setI(i + 1)}>下一步</button>
          <span class="small muted">{i + 1} / {steps.length}</span>
        </div>
      </div>
    </div>
  );
}

const askText = (a) => (a.var === "@out" ? `第 ${a.line} 行执行完时，屏幕上一共打印了什么？` : `第 ${a.line} 行${a.hit > 1 ? `第 ${a.hit} 次` : ""}执行完后，${a.var} 的值是？`);

function TraceView({ params: p, goal, value, setValue, locked, result }) {
  const lines = p.code.replace(/\n$/, "").split("\n");
  const set = (i, v) => { const a = [...value.answers]; a[i] = v; setValue({ answers: a }); };
  return (
    <div class="sim sim-trace">
      {!result ? <ol class="codelines">{lines.map((l, k) => <li><span class="ln">{k + 1}</span><code>{l || " "}</code></li>)}</ol> : <Stepper params={p} />}
      <div class="asks">
        {goal.ask.map((a, i) => (
          <label class={"answer-line" + (result ? (result.detail.each[i] ? " is-correct" : " is-wrong") : "")}>
            <span>{askText(a)}</span>
            {a.var === "@out" ? <textarea rows="2" value={value.answers[i]} disabled={locked} onInput={(e) => set(i, e.currentTarget.value)} /> : <input type="text" value={value.answers[i]} disabled={locked} onInput={(e) => set(i, e.currentTarget.value)} spellcheck={false} />}
            {result && !result.detail.each[i] && <span class="small">实际是 <code>{result.detail.want[i]}</code></span>}
          </label>
        ))}
      </div>
      {result && <p class="small muted">上面可以单步看实际运行过程。</p>}
    </div>
  );
}

export default {
  trace: { View: TraceView, Demo: ({ params }) => <div class="sim sim-trace"><Stepper params={params} /></div>, initial: tLogic.initial },
};
