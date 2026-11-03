// Views for the systems-route sims. Each is { View, Demo, initial } (docs/architecture.md "交互组件接口").
import { useState } from "preact/hooks";
import { bits as bLogic, bitsValue, stackqueue as sqLogic, replayContainer, hash as hLogic, hashPlacement, scheduler as schLogic, schedule, paging as pgLogic, threads as thLogic, threadsInit, canStep, stepThread, replace as rpLogic, replaceRun } from "../logic/os.js";

const demoOf = (View, initial) => function Demo({ params }) {
  const [v, setV] = useState(() => initial(params, {}));
  return <View params={params} goal={{}} value={v} setValue={setV} demo />;
};
const hex = (n, w) => "0x" + (n >>> 0).toString(16).toUpperCase().padStart(w, "0");

// ---------- bits ----------
function BitsView({ params: p, value, setValue, locked }) {
  const n = p.bits;
  const u = bitsValue(value, false), sgn = bitsValue(value, true);
  return (
    <div class="sim sim-bits">
      <div class="bitrow" role="group" aria-label={`${n} 位寄存器`}>
        {value.map((b, i) => (
          <button type="button" class={"bit" + (b ? " on" : "")} aria-pressed={!!b} disabled={locked} onClick={() => setValue(value.map((x, j) => (j === i ? 1 - x : x)))}>
            <span class="bv">{b}</span>
            <span class="bw">{i === 0 && p.signed ? `−2^${n - 1}` : `2^${n - 1 - i}`}</span>
          </button>
        ))}
      </div>
      <p class="stat">无符号：<b>{u}</b> · {p.signed ? <>补码（有符号）：<b>{sgn}</b> · </> : null}十六进制：<b>{hex(u, Math.ceil(n / 4))}</b></p>
      <p class="small muted">点一位翻转 0/1。{p.signed ? "最高位的权重是负的：这就是补码。" : ""}</p>
    </div>
  );
}

// ---------- stackqueue ----------
function SQView({ params: p, value, setValue, locked }) {
  const ops = value.ops || [];
  const res = replayContainer(p.kind, p.start || [], ops);
  const st = res.state || [];
  const push = (v) => setValue({ ops: [...ops, { op: "push", v }] });
  const pop = () => setValue({ ops: [...ops, { op: "pop" }] });
  return (
    <div class="sim sim-sq">
      <div class={"container " + p.kind} aria-label={p.kind === "stack" ? "栈，右边是栈顶" : "队列，左边是队头"}>
        {p.kind === "queue" && <span class="end">队头 →</span>}
        {st.map((v) => <span class="cell">{v}</span>)}
        {!st.length && <span class="muted small">（空）</span>}
        {p.kind === "stack" ? <span class="end">← 栈顶</span> : <span class="end">← 队尾</span>}
      </div>
      <div class="btns">
        {(p.pushable || []).map((v) => <button type="button" class="btn small" disabled={locked} onClick={() => push(v)}>{p.kind === "stack" ? "push" : "enqueue"} {v}</button>)}
        <button type="button" class="btn small" disabled={locked || !st.length} onClick={pop}>{p.kind === "stack" ? "pop" : "dequeue"}</button>
        <button type="button" class="btn small ghost" disabled={locked || !ops.length} onClick={() => setValue({ ops: ops.slice(0, -1) })}>撤销</button>
      </div>
      <p class="stat">取出的顺序：{(res.outputs || []).join(", ") || "—"}</p>
      {res.error && <p class="bad small">{res.error}</p>}
    </div>
  );
}

// ---------- hash ----------
function HashView({ params: p, value, setValue, locked, result }) {
  const placed = value || [];
  const next = placed.length;
  const table = Array.from({ length: p.size }, () => []);
  placed.forEach((slot, i) => table[slot]?.push(p.keys[i]));
  const want = result && !result.correct ? hashPlacement(p) : null;
  return (
    <div class="sim sim-hash">
      <p class="stat">h(k) = k mod {p.size}，{p.probe === "linear" ? "冲突时往后找下一个空槽（线性探测，到末尾绕回 0）" : "冲突时挂在同一个槽的链表上"}。</p>
      <p class="stat">{next < p.keys.length ? <>下一个要放的键：<b>{p.keys[next]}</b>（点它该去的槽）</> : "全部放好了。"}</p>
      <div class="slots">
        {table.map((ks, i) => (
          <button type="button" class="slot" disabled={locked || next >= p.keys.length || (p.probe === "linear" && ks.length > 0)} onClick={() => setValue([...placed, i])}>
            <span class="idx">{i}</span><span class="keys">{ks.join(" → ") || "·"}</span>
          </button>
        ))}
      </div>
      <div class="btns"><button type="button" class="btn small ghost" disabled={locked || !placed.length} onClick={() => setValue(placed.slice(0, -1))}>撤销</button></div>
      {want && <p class="small">正确放法：{p.keys.map((k, i) => `${k}→${want[i]}`).join("，")}</p>}
    </div>
  );
}

// ---------- scheduler ----------
const ALGO = { FCFS: "先来先服务 FCFS", SJF: "最短作业优先 SJF（不抢占）", SRTF: "最短剩余时间优先 SRTF（抢占）", RR: "时间片轮转 RR" };
function SchedView({ params: p, value, setValue, locked, result, demo }) {
  const sol = schedule(p);
  const T = sol.timeline.length;
  const tl = demo ? sol.timeline : value;
  const setCell = (t, name) => { const next = [...value]; next[t] = next[t] === name ? undefined : name; setValue(next); };
  const wrongAt = result && !result.correct ? result.detail.firstWrong : -1;
  return (
    <div class="sim sim-sched">
      <table class="procs"><thead><tr><th>进程</th><th>到达时间</th><th>运行时间</th></tr></thead>
        <tbody>{p.procs.map((q) => <tr><td>{q.name}</td><td>{q.arrive}</td><td>{q.burst}</td></tr>)}</tbody></table>
      <p class="stat">算法：<b>{ALGO[p.algo]}{p.algo === "RR" ? `，时间片 = ${p.quantum}` : ""}</b>。{demo ? "下面是它排出的时间线。" : "每个时间格点一下“这一格谁在用 CPU”；都不在就点“空闲”。"}</p>
      <div class="gantt" style={{ "--cols": T }} role="group" aria-label="甘特图：每一格是一个时间单位">
        <div class="ghead"><span />{Array.from({ length: T }, (_, t) => <span class="tnum">{t}</span>)}</div>
        {[...p.procs.map((q) => q.name), null].map((name) => (
          <div class="grow">
            <span class="gname">{name ?? "空闲"}</span>
            {Array.from({ length: T }, (_, t) => {
              const on = tl[t] === name && (tl[t] !== undefined);
              const cls = "gcell" + (on ? " on" : "") + (t === wrongAt ? " wrong" : "") + (name === null ? " idle" : "");
              return <button type="button" class={cls} aria-label={`时间 ${t}：${name ?? "空闲"}`} aria-pressed={on} disabled={locked || demo} onClick={() => setCell(t, name)} />;
            })}
          </div>
        ))}
      </div>
      <p class="small muted">规则：平局先到先得、再按表格顺序；SRTF 剩余时间相同时正在运行的继续；RR 中同一时刻新到达的进程排在刚用完时间片的进程前面。</p>
      {wrongAt >= 0 && <p class="small">从时间 {wrongAt} 开始不对。正确时间线：{sol.timeline.map((x) => x ?? "空").join(" ")}</p>}
      {(demo || (result && result.correct)) && <p class="stat">平均等待时间 {+sol.avgWait.toFixed(3)} · 平均周转时间 {+sol.avgTurnaround.toFixed(3)}</p>}
    </div>
  );
}

// ---------- paging ----------
function PagingView({ params: p, value, setValue, locked, result }) {
  const bitsOff = Math.log2(p.pageSize);
  const set = (k, v) => setValue({ ...value, [k]: v });
  const d = result?.detail;
  return (
    <div class="sim sim-paging">
      <p class="stat">页大小 {p.pageSize} 字节（= 2^{bitsOff}，低 {bitsOff} 位是页内偏移）。虚拟地址 <b>{p.vaddr}</b>（{hex(p.vaddr, 4)}）。</p>
      <table class="ptable"><thead><tr><th>虚拟页号 VPN</th><th>物理页框号 PFN</th></tr></thead>
        <tbody>{p.table.map((f, i) => <tr><td>{i}</td><td>{f === null ? "未映射（缺页）" : f}</td></tr>)}</tbody></table>
      <div class="fields">
        <label>VPN = <input type="text" inputmode="numeric" value={value.vpn} disabled={locked} onInput={(e) => set("vpn", e.currentTarget.value)} class={d ? (d.vpnOk ? "is-correct" : "is-wrong") : ""} /></label>
        <label>偏移 = <input type="text" inputmode="numeric" value={value.offset} disabled={locked} onInput={(e) => set("offset", e.currentTarget.value)} class={d ? (d.offOk ? "is-correct" : "is-wrong") : ""} /></label>
        <label><input type="checkbox" checked={!!value.fault} disabled={locked} onChange={(e) => set("fault", e.currentTarget.checked)} /> 这是缺页</label>
        {!value.fault && <label>物理地址 = <input type="text" inputmode="numeric" value={value.paddr} disabled={locked} onInput={(e) => set("paddr", e.currentTarget.value)} class={d ? (d.tailOk ? "is-correct" : "is-wrong") : ""} /></label>}
      </div>
      <p class="small muted">都用十进制填写。</p>
      {d && !result.correct && <p class="small">正确：VPN {d.want.vpn}，偏移 {d.want.offset}，{d.want.fault ? "缺页" : `物理地址 ${d.want.paddr}（${hex(d.want.paddr, 4)}）`}</p>}
    </div>
  );
}

// ---------- threads (you are the scheduler) ----------
function ThreadsView({ params: p, goal, value, setValue, locked }) {
  let s = threadsInit(p);
  for (const ti of value) s = stepThread(p, s, ti);
  const finished = s.pc.every((pc, i) => pc >= p.threads[i].steps.length);
  const stuck = !finished && p.threads.every((_, i) => !canStep(p, s, i));
  return (
    <div class="sim sim-threads">
      <div class="threads" style={{ "--n": p.threads.length }}>
        {p.threads.map((th, i) => (
          <div class="thread">
            <h4>{th.name}</h4>
            <ol class="tcode">{th.steps.map((line, k) => <li class={k === s.pc[i] ? "pc" : k < s.pc[i] ? "done" : ""}><code>{line}</code></li>)}</ol>
            {Object.keys(s.locals[i]).length > 0 && <p class="small">局部：{Object.entries(s.locals[i]).map(([k, v]) => `${k} = ${v}`).join("，")}</p>}
            <button type="button" class="btn small" disabled={locked || !canStep(p, s, i)} onClick={() => setValue([...value, i])}>{s.pc[i] >= th.steps.length ? "已结束" : canStep(p, s, i) ? `让 ${th.name} 走一步` : "被挡住了"}</button>
          </div>
        ))}
      </div>
      <p class="stat">共享：{Object.entries(s.shared).map(([k, v]) => <b>{k} = {v} </b>)}{Object.entries(s.locks).map(([m, o]) => <span> · 锁 {m}：{o === null ? "空闲" : `被 ${p.threads[o].name} 持有`}</span>)}{Object.entries(s.sems).map(([k, v]) => <span> · 信号量 {k} = {v}</span>)}</p>
      <p class="stat">{finished ? "所有线程都结束了。" : stuck ? <b class="bad">死锁：没有线程能继续。</b> : "你来决定下一步让谁执行。"}</p>
      <div class="btns"><button type="button" class="btn small ghost" disabled={locked || !value.length} onClick={() => setValue(value.slice(0, -1))}>撤销一步</button><button type="button" class="btn small ghost" disabled={locked || !value.length} onClick={() => setValue([])}>重来</button></div>
    </div>
  );
}

// ---------- replace (you are the page-replacement policy) ----------
const POLICY = { FIFO: "FIFO：换出最早进来的页", LRU: "LRU：换出最久没用过的页", OPT: "最优（OPT）：换出下一次用到得最晚的页（再也不用的最晚）" };
function ReplaceView({ params: p, value, setValue, locked, result, demo }) {
  const run = demo ? replaceRun(p, [], (allowed) => allowed[0]) : replaceRun(p, value);
  const t = run.pending;
  const wrong = result && !result.correct ? result.detail : null;
  const note = (pg) => {
    if (!(demo || p.help) || t === undefined) return null;
    const rows = run.rows;
    if (p.policy === "FIFO") return `第 ${rows.findLastIndex((r) => r.ref === pg && !r.hit) + 1} 个引用时进来`;
    if (p.policy === "LRU") return `上次用在第 ${rows.findLastIndex((r) => r.ref === pg) + 1} 个引用`;
    const k = p.refs.indexOf(pg, t + 1);
    return k === -1 ? "后面不再用到" : `下次用在第 ${k + 1} 个引用`;
  };
  return (
    <div class="sim sim-replace">
      <p class="stat">内存只有 <b>{p.frames}</b> 个页框。规则：<b>{POLICY[p.policy]}</b>。</p>
      <div class="refs" role="group" aria-label="引用串">
        {p.refs.map((pg, i) => <span class={"ref" + (i === t ? " now" : "") + (i < run.rows.length ? (run.rows[i].hit ? " hit" : " miss") : "")}>{pg}</span>)}
      </div>
      <div class="rtable-wrap">
        <table class="rtable"><thead><tr><th>引用</th>{run.rows.map((r) => <th>{r.ref}</th>)}</tr></thead>
          <tbody>
            {Array.from({ length: p.frames }, (_, f) => <tr><th>页框 {f + 1}</th>{run.rows.map((r) => <td>{r.frames[f] ?? ""}</td>)}</tr>)}
            <tr class="hm"><th>结果</th>{run.rows.map((r) => <td class={r.hit ? "hit" : "miss"}>{r.hit ? "命中" : "缺页"}</td>)}</tr>
            <tr><th>换出</th>{run.rows.map((r) => <td>{r.evicted ?? ""}</td>)}</tr>
          </tbody></table>
      </div>
      {t !== undefined && !demo && (
        <div class="evict">
          <p class="stat">第 {t + 1} 个引用是 <b>{p.refs[t]}</b>：不在内存里，页框都满了。点要换出的页：</p>
          <div class="slots">{run.frames.map((pg) => <button type="button" class="slot" disabled={locked} onClick={() => setValue([...value, pg])}><span class="keys">换出 {pg}</span>{note(pg) && <span class="idx">{note(pg)}</span>}</button>)}</div>
        </div>
      )}
      {run.error && <p class="small bad">{run.error}。{locked && run.allowed ? `应该换出 ${run.allowed.join(" 或 ")}。` : "点“撤销”换一个。"}</p>}
      {run.done === p.refs.length && <p class="stat">做完了：缺页 <b>{run.misses}</b> 次，命中 <b>{run.hits}</b> 次，命中率 {+(100 * run.hits / p.refs.length).toFixed(1)}%。</p>}
      {wrong && !wrong.error && wrong.done === p.refs.length && <p class="small">缺页次数对不上目标。</p>}
      {!demo && <div class="btns"><button type="button" class="btn small ghost" disabled={locked || !value.length} onClick={() => setValue(value.slice(0, -1))}>撤销</button><button type="button" class="btn small ghost" disabled={locked || !value.length} onClick={() => setValue([])}>重来</button></div>}
    </div>
  );
}

export default {
  replace: { View: ReplaceView, Demo: demoOf(ReplaceView, rpLogic.initial), initial: rpLogic.initial },
  bits: { View: BitsView, Demo: demoOf(BitsView, bLogic.initial), initial: bLogic.initial },
  stackqueue: { View: SQView, Demo: demoOf(SQView, sqLogic.initial), initial: sqLogic.initial },
  hash: { View: HashView, Demo: demoOf(HashView, hLogic.initial), initial: hLogic.initial },
  scheduler: { View: SchedView, Demo: demoOf(SchedView, schLogic.initial), initial: schLogic.initial },
  paging: { View: PagingView, Demo: demoOf(PagingView, pgLogic.initial), initial: pgLogic.initial },
  threads: { View: ThreadsView, Demo: demoOf(ThreadsView, thLogic.initial), initial: thLogic.initial },
};
