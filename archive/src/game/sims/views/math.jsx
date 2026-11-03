// Views for the math / ML sims. Each: { View({params, goal, value, setValue, locked}), Demo({params}), initial }.
import { useMemo, useState } from "preact/hooks";
import { fx, compile } from "../expr.js";
import { plot as plotLogic, integrate, riemann, taylor, seriesFn, det, sample, descend, LOGIC, neuronAccuracy, dataset, trainMlp, kmeansRun, matrix2d as mLogic, descent as dLogic, neuron as nLogic, mlp as mlpLogic, kmeans as kLogic, sampler as sLogic } from "../logic/math.js";
import { scales, Frame, fnPath, autoRange, fmt } from "./plot-kit.jsx";
import { Md } from "../../ui/md.jsx";

const demoOf = (View, initial) => function Demo({ params }) {
  const [v, setV] = useState(() => initial(params, {}));
  return <View params={params} goal={{}} value={v} setValue={setV} demo />;
};

// ---------- plot ----------
function PlotView({ params: p, goal, value, setValue, locked, demo }) {
  if (p.mode === "secant") return <Secant p={p} value={value} setValue={setValue} locked={locked} />;
  if (p.mode === "riemann") return <Riemann p={p} goal={goal} value={value} setValue={setValue} locked={locked} />;
  if (p.mode === "taylor") return <Taylor p={p} goal={goal} value={value} setValue={setValue} locked={locked} />;
  return <Limit p={p} value={value} setValue={setValue} locked={locked} demo={demo} />;
}

function Secant({ p, value, setValue, locked }) {
  const f = useMemo(() => fx(p.f), [p.f]);
  const hMax = p.hMax ?? 1;
  const h = Number(value.h);
  const xd = p.xRange || [p.a - 2 * hMax, p.a + 2 * hMax];
  const s = scales(xd, p.yRange || autoRange([f], xd));
  const slope = (f(p.a + h) - f(p.a)) / h;
  const line = (x) => f(p.a) + slope * (x - p.a);
  // slider position t ∈ [0, 1] maps to h = hMax · 10^(−4t): fine control near 0
  const t = Math.log10(hMax / h) / 4;
  return (
    <div class="sim sim-plot">
      <Frame s={s} label={`f(x) = ${p.f} 的割线`} readout={(x) => [["f(x)", f(x)]]}>
        <path class="fn" d={fnPath(f, s)} />
        <path class="fn-2" d={fnPath(line, s)} />
        <circle class="dot" cx={s.sx(p.a)} cy={s.sy(f(p.a))} r="5" />
        <circle class="dot dot-2" cx={s.sx(p.a + h)} cy={s.sy(f(p.a + h))} r="5" />
      </Frame>
      <label class="slider">h = {fmt(h, 5)}
        <input type="range" min="0" max="1" step="0.001" value={t} disabled={locked} onInput={(e) => setValue({ h: hMax * 10 ** (-4 * Number(e.currentTarget.value)) })} />
      </label>
      <p class="stat"><Md inline text={String.raw`割线斜率 $\dfrac{f(a+h)-f(a)}{h}$ = **${fmt(slope, 5)}**（a = ${p.a}）`} /></p>
    </div>
  );
}

function Riemann({ p, goal, value, setValue, locked }) {
  const f = useMemo(() => fx(p.f), [p.f]);
  const n = Math.max(1, Math.round(value.n));
  const pad = (p.b - p.a) * 0.1;
  const xd = [p.a - pad, p.b + pad];
  const s = scales(xd, p.yRange || autoRange([f, () => 0], xd));
  const w = (p.b - p.a) / n;
  const off = p.rule === "right" ? 1 : p.rule === "mid" ? 0.5 : 0;
  const approx = riemann(f, p.a, p.b, n, p.rule), exact = integrate(f, p.a, p.b);
  const rects = n <= 400 ? Array.from({ length: n }, (_, i) => { const x = p.a + i * w, y = f(x + off * w); return { x, y }; }) : [];
  return (
    <div class="sim sim-plot">
      <Frame s={s} label={`${p.f} 在 [${p.a}, ${p.b}] 上的黎曼和`} readout={(x) => [["f(x)", f(x)]]}>
        {rects.map((r) => <rect class="bar" x={s.sx(r.x)} width={Math.max(0.5, s.sx(r.x + w) - s.sx(r.x) - (n < 60 ? 1 : 0))} y={Math.min(s.sy(r.y), s.sy(0))} height={Math.abs(s.sy(r.y) - s.sy(0))} />)}
        <path class="fn" d={fnPath(f, s)} />
      </Frame>
      <label class="slider">矩形个数 n = {n}
        <input type="range" min="1" max={p.nMax || 200} step="1" value={n} disabled={locked} onInput={(e) => setValue({ n: Number(e.currentTarget.value) })} />
      </label>
      <p class="stat">近似值 <b>{fmt(approx, 6)}</b> · 精确值 {fmt(exact, 6)} · 误差 {fmt(Math.abs(approx - exact), 6)}{goal.errorBelow ? `（目标 < ${goal.errorBelow}）` : ""}</p>
    </div>
  );
}

function Taylor({ p, goal, value, setValue, locked }) {
  const f = seriesFn(p.series);
  const order = Math.round(value.order);
  const xm = p.xMax || 3;
  const xd = [-xm, xm];
  const s = scales(xd, p.yRange || autoRange([f], xd, 0.3));
  const T = (x) => taylor(p.series, order, x);
  const at = goal.at;
  const names = { exp: "e^x", sin: "sin x", cos: "cos x", ln1p: "ln(1+x)" };
  return (
    <div class="sim sim-plot">
      <Frame s={s} label={`${names[p.series]} 与它的 ${order} 阶泰勒多项式`} readout={(x) => [["f", f(x)], ["Tₙ", T(x)]]}>
        <path class="fn" d={fnPath(f, s)} />
        <path class="fn-2" d={fnPath(T, s)} />
        {at !== undefined && <line class="marker" x1={s.sx(at)} x2={s.sx(at)} y1={s.pad.t} y2={s.H - s.pad.b} />}
      </Frame>
      <div class="legend"><span class="li"><span class="sw sw-fn" />{names[p.series]}</span><span class="li"><span class="sw sw-1" />{order} 阶泰勒多项式（在 0 处展开）</span></div>
      <label class="slider">阶数 n = {order}
        <input type="range" min="0" max={p.maxOrder || 12} step="1" value={order} disabled={locked} onInput={(e) => setValue({ order: Number(e.currentTarget.value) })} />
      </label>
      {at !== undefined && <p class="stat">在 x = {at}：f = {fmt(f(at), 6)}，Tₙ = {fmt(T(at), 6)}，误差 <b>{fmt(Math.abs(f(at) - T(at)), 6)}</b>{goal.errorBelow ? `（目标 < ${goal.errorBelow}）` : ""}</p>}
    </div>
  );
}

function Limit({ p, value, setValue, locked, demo }) {
  const f = useMemo(() => fx(p.f), [p.f]);
  const ks = [1, 2, 3, 4, 5, 6];
  const safe = (x) => { try { return f(x); } catch { return NaN; } };
  const xd = p.xRange || [p.a - 2, p.a + 2];
  const s = scales(xd, p.yRange || autoRange([f], xd));
  return (
    <div class="sim sim-plot">
      <Frame s={s} label={`${p.f} 在 x → ${p.a} 附近`} readout={(x) => [["f(x)", safe(x)]]}>
        <path class="fn" d={fnPath(f, s)} />
        <circle class="hole" cx={s.sx(p.a)} cy={s.sy(Number.isFinite(safe(p.a)) ? safe(p.a) : (safe(p.a + 1e-6) + safe(p.a - 1e-6)) / 2)} r="5" />
      </Frame>
      <table class="values">
        <thead><tr><th>x</th><th>f(x)</th><th>x</th><th>f(x)</th></tr></thead>
        <tbody>{ks.map((k) => <tr><td>{p.a} − 10<sup>−{k}</sup></td><td>{fmt(safe(p.a - 10 ** -k), 8)}</td><td>{p.a} + 10<sup>−{k}</sup></td><td>{fmt(safe(p.a + 10 ** -k), 8)}</td></tr>)}</tbody>
      </table>
      {!demo && <label class="answer-line">你认为极限是 <input type="text" inputmode="decimal" value={value.guess} disabled={locked} onInput={(e) => setValue({ guess: e.currentTarget.value })} /></label>}
    </div>
  );
}

// ---------- matrix2d ----------
function MatrixView({ params, value, setValue, locked }) {
  const A = value;
  const set = (i, j, v) => { const B = A.map((r) => [...r]); B[i][j] = v; setValue(B); };
  const s = scales([-3, 3], [-3, 3], 320, 320, { l: 10, r: 10, t: 10, b: 10 });
  const T = ([x, y]) => [A[0][0] * x + A[0][1] * y, A[1][0] * x + A[1][1] * y];
  const lines = [];
  for (let k = -3; k <= 3; k++) { lines.push([T([k, -3]), T([k, 3])]); lines.push([T([-3, k]), T([3, k])]); }
  const sq = [[0, 0], [1, 0], [1, 1], [0, 1]].map(T);
  const e1 = T([1, 0]), e2 = T([0, 1]);
  return (
    <div class="sim sim-matrix">
      <div class="matrix-in" role="group" aria-label="2×2 矩阵">
        <span class="bracket">[</span>
        <div class="mgrid">{[0, 1].map((i) => [0, 1].map((j) => <input type="number" step="0.1" value={A[i][j]} disabled={locked} aria-label={`第 ${i + 1} 行第 ${j + 1} 列`} onInput={(e) => set(i, j, Number(e.currentTarget.value))} />))}</div>
        <span class="bracket">]</span>
        <p class="stat">行列式 det = <b>{fmt(det(A), 4)}</b></p>
      </div>
      <div class="plot square">
        <svg viewBox="0 0 320 320" role="img" aria-label="矩阵把网格变成什么样">
          {[...Array(7).keys()].map((i) => <><line class="grid" x1={s.sx(i - 3)} x2={s.sx(i - 3)} y1={s.sy(-3)} y2={s.sy(3)} /><line class="grid" y1={s.sy(i - 3)} y2={s.sy(i - 3)} x1={s.sx(-3)} x2={s.sx(3)} /></>)}
          {lines.map(([a, b]) => <line class="tgrid" x1={s.sx(a[0])} y1={s.sy(a[1])} x2={s.sx(b[0])} y2={s.sy(b[1])} />)}
          <polygon class="unit" points={sq.map((q) => `${s.sx(q[0])},${s.sy(q[1])}`).join(" ")} />
          <line class="vec v1" x1={s.sx(0)} y1={s.sy(0)} x2={s.sx(e1[0])} y2={s.sy(e1[1])} />
          <line class="vec v2" x1={s.sx(0)} y1={s.sy(0)} x2={s.sx(e2[0])} y2={s.sy(e2[1])} />
        </svg>
        <div class="legend"><span class="li"><span class="sw sw-1" />第 1 列 = (1,0) 的像 ({fmt(e1[0], 2)}, {fmt(e1[1], 2)})</span><span class="li"><span class="sw sw-2" />第 2 列 = (0,1) 的像 ({fmt(e2[0], 2)}, {fmt(e2[1], 2)})</span></div>
      </div>
    </div>
  );
}

// ---------- sampler ----------
function SamplerView({ params, value, setValue, locked }) {
  const n = value.n || 0;
  const draws = useMemo(() => sample(params.dist, n, params.seed || 7), [params.dist, n]);
  const faces = params.dist === "coin" ? [0, 1] : params.dist === "die" ? [1, 2, 3, 4, 5, 6] : [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
  const label = params.dist === "coin" ? (v) => (v ? "正" : "反") : (v) => v;
  const expected = (v) => (params.dist === "coin" ? 0.5 : params.dist === "die" ? 1 / 6 : (6 - Math.abs(v - 7)) / 36);
  const counts = faces.map((v) => draws.filter((d) => d === v).length);
  const maxP = Math.max(0.3, ...faces.map(expected), ...counts.map((c) => (n ? c / n : 0)));
  const W = 480, H = 220, bw = (W - 40) / faces.length;
  return (
    <div class="sim sim-sampler">
      <div class="btns">{[1, 10, 100, 1000].map((k) => <button type="button" class="btn small" disabled={locked} onClick={() => setValue({ n: n + k })}>再抽 {k} 次</button>)}<button type="button" class="btn small ghost" disabled={locked} onClick={() => setValue({ n: 0 })}>清零</button></div>
      <div class="plot"><svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label="频率直方图">
        {faces.map((v, i) => {
          const fr = n ? counts[i] / n : 0, x = 30 + i * bw, y = (p) => H - 24 - (p / maxP) * (H - 40);
          return <g><rect class="bar" x={x + 2} width={bw - 4} y={y(fr)} height={H - 24 - y(fr)} rx="4" /><line class="expect" x1={x} x2={x + bw} y1={y(expected(v))} y2={y(expected(v))} /><text class="tick" x={x + bw / 2} y={H - 8} text-anchor="middle">{label(v)}</text><title>{label(v)}：{counts[i]} 次，频率 {fmt(fr, 3)}，理论概率 {fmt(expected(v), 3)}</title></g>;
        })}
      </svg></div>
      <p class="stat">已抽 <b>{n}</b> 次。柱子是频率，横线是理论概率。</p>
    </div>
  );
}

// ---------- descent ----------
function DescentView({ params: p, goal, value, setValue, locked }) {
  const vars = p.vars || ["x"];
  const lr = Number(value.lr), steps = value.steps || 0;
  const run = useMemo(() => descend(p, lr, steps), [p.f, lr, steps]);
  const t = Math.log10(lr / 0.001) / Math.log10(2 / 0.001);
  const controls = (
    <>
      <label class="slider">学习率 η = {fmt(lr, 4)}
        <input type="range" min="0" max="1" step="0.001" value={t} disabled={locked} onInput={(e) => setValue({ lr: +(0.001 * (2 / 0.001) ** Number(e.currentTarget.value)).toPrecision(3), steps: 0 })} />
      </label>
      <div class="btns">
        <button type="button" class="btn small" disabled={locked || run.diverged} onClick={() => setValue({ lr, steps: steps + 1 })}>走一步</button>
        <button type="button" class="btn small" disabled={locked || run.diverged} onClick={() => setValue({ lr, steps: steps + 10 })}>走 10 步</button>
        <button type="button" class="btn small ghost" disabled={locked} onClick={() => setValue({ lr, steps: 0 })}>回到起点</button>
      </div>
      <p class="stat">已走 <b>{steps}</b> 步{goal.maxSteps ? `（最多 ${goal.maxSteps}）` : ""} · 当前位置 ({run.x.map((v) => fmt(v, 4)).join(", ")}){run.diverged ? <b class="bad"> · 发散了！步子太大</b> : ` · f = ${fmt(run.value, 5)}`}</p>
    </>
  );
  if (vars.length === 1) {
    const f = fx(p.f);
    const xs = run.path.map((q) => q[0]).filter((v) => Number.isFinite(v) && Math.abs(v) < 50);
    let m = p.x0, fm = Infinity;
    for (let i = 0; i <= 400; i++) { const x = p.x0 - 6 + (12 * i) / 400, v = f(x); if (v < fm) { fm = v; m = x; } }
    const xd = p.xRange || [Math.min(p.x0, m, ...xs) - 1, Math.max(p.x0, m, ...xs) + 1];
    const s = scales(xd, autoRange([f], xd));
    return (
      <div class="sim sim-descent">
        <Frame s={s} label={`在 ${p.f} 上做梯度下降`} readout={(x) => [["f(x)", f(x)]]}>
          <path class="fn" d={fnPath(f, s)} />
          <polyline class="path" points={run.path.filter((q) => Number.isFinite(q[0]) && q[0] >= xd[0] && q[0] <= xd[1]).map((q) => `${s.sx(q[0])},${s.sy(f(q[0]))}`).join(" ")} />
          {run.path.slice(-1).map((q) => Number.isFinite(q[0]) && <circle class="dot dot-2" cx={s.sx(q[0])} cy={s.sy(f(q[0]))} r="5" />)}
        </Frame>
        {controls}
      </div>
    );
  }
  const F = compile(p.f);
  const val = (x, y) => F({ [vars[0]]: x, [vars[1]]: y });
  const R = p.range || 3;
  const s = scales([-R, R], [-R, R], 320, 320, { l: 10, r: 10, t: 10, b: 10 });
  const N = 32, cells = [];
  let lo = Infinity, hi = -Infinity;
  for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) { const x = -R + (2 * R * (i + 0.5)) / N, y = -R + (2 * R * (j + 0.5)) / N, v = val(x, y); cells.push([x, y, v]); lo = Math.min(lo, v); hi = Math.max(hi, v); }
  const shade = (v) => Math.sqrt((v - lo) / (hi - lo || 1));
  return (
    <div class="sim sim-descent">
      <div class="plot square"><svg viewBox="0 0 320 320" role="img" aria-label={`在 ${p.f} 上做梯度下降（颜色越深函数值越大）`}>
        {cells.map(([x, y, v]) => <rect x={s.sx(x - R / N)} y={s.sy(y + R / N)} width={300 / N} height={300 / N} class="heat" shape-rendering="crispEdges" style={{ opacity: 0.08 + 0.75 * shade(v) }} />)}
        <polyline class="path" points={run.path.filter((q) => q.every(Number.isFinite) && Math.abs(q[0]) <= R && Math.abs(q[1]) <= R).map((q) => `${s.sx(q[0])},${s.sy(q[1])}`).join(" ")} />
        {run.path.slice(-1).map((q) => q.every(Number.isFinite) && <circle class="dot dot-2" cx={s.sx(q[0])} cy={s.sy(q[1])} r="5" />)}
      </svg></div>
      {controls}
    </div>
  );
}

// ---------- neuron ----------
function NeuronView({ params: p, value, setValue, locked }) {
  const pts = p.gate ? LOGIC[p.gate] : dataset(p.dataset, p.n, p.seed);
  const v = { w1: Number(value.w1), w2: Number(value.w2), b: Number(value.b) };
  const acc = neuronAccuracy(pts, v);
  const lo = p.gate ? -0.5 : -1.2, hi = p.gate ? 1.5 : 1.2;
  const s = scales([lo, hi], [lo, hi], 300, 300, { l: 30, r: 10, t: 10, b: 26 });
  // decision boundary w1 x + w2 y + b = 0, clipped to the box by sampling
  const N = 24, cells = [];
  for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) { const x = lo + ((hi - lo) * (i + 0.5)) / N, y = lo + ((hi - lo) * (j + 0.5)) / N; cells.push([x, y, v.w1 * x + v.w2 * y + v.b > 0]); }
  const slider = (k, label) => <label class="slider">{label} = {fmt(v[k], 2)}<input type="range" min="-3" max="3" step="0.1" value={v[k]} disabled={locked} onInput={(e) => setValue({ ...v, [k]: Number(e.currentTarget.value) })} /></label>;
  return (
    <div class="sim sim-neuron">
      <div class="plot square"><svg viewBox="0 0 300 300" role="img" aria-label="单个神经元的分类结果">
        {cells.map(([x, y, pos]) => <rect x={s.sx(x - (hi - lo) / N / 2)} y={s.sy(y + (hi - lo) / N / 2)} width={s.sx(lo + (hi - lo) / N) - s.sx(lo)} height={s.sy(lo) - s.sy(lo + (hi - lo) / N)} shape-rendering="crispEdges" class={pos ? "region-1" : "region-0"} />)}
        {pts.map(([x, y, t]) => <circle cx={s.sx(x)} cy={s.sy(y)} r={p.gate ? 9 : 4} class={"pt pt-" + t} />)}
        {p.gate && pts.map(([x, y, t]) => <text class="ptlabel" x={s.sx(x)} y={s.sy(y) + 4} text-anchor="middle">{t}</text>)}
      </svg></div>
      <div class="controls">
        <p class="stat"><Md inline text="输出 1 当且仅当 $w_1x_1 + w_2x_2 + b > 0$（浅色区域）" /></p>
        {slider("w1", "w₁")}{slider("w2", "w₂")}{slider("b", "b")}
        <p class="stat">分对 <b>{Math.round(acc * pts.length)}</b> / {pts.length}</p>
      </div>
    </div>
  );
}

// ---------- mlp (a tiny playground) ----------
function MlpView({ params: p, value, setValue, locked }) {
  const pts = useMemo(() => dataset(p.dataset, p.n, p.seed), [p.dataset]);
  const [res, setRes] = useState(null);
  const cfg = value;
  const train = () => { const r = trainMlp(pts, cfg); setRes({ ...r, cfg: JSON.stringify(cfg) }); };
  const fresh = res && res.cfg === JSON.stringify(cfg);
  const s = scales([-1.2, 1.2], [-1.2, 1.2], 300, 300, { l: 10, r: 10, t: 10, b: 10 });
  const N = 30, cells = [];
  if (fresh) for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) { const x = -1.2 + (2.4 * (i + 0.5)) / N, y = -1.2 + (2.4 * (j + 0.5)) / N; cells.push([x, y, res.predict([x, y])]); }
  const set = (k, v) => setValue({ ...cfg, [k]: v });
  return (
    <div class="sim sim-mlp">
      <div class="plot square"><svg viewBox="0 0 300 300" role="img" aria-label="训练数据与网络的判断">
        {cells.map(([x, y, q]) => <rect x={s.sx(x - 1.2 / N)} y={s.sy(y + 1.2 / N)} width={280 / N} height={280 / N} shape-rendering="crispEdges" class={q > 0.5 ? "region-1" : "region-0"} style={{ opacity: 0.25 + 0.6 * Math.abs(q - 0.5) * 2 }} />)}
        {pts.map(([x, y, t]) => <circle cx={s.sx(x)} cy={s.sy(y)} r="4" class={"pt pt-" + t} />)}
      </svg></div>
      <div class="controls">
        <label class="slider">隐藏层神经元 = {cfg.hidden}{cfg.hidden == 0 ? "（没有隐藏层：只能画一条直线）" : ""}<input type="range" min="0" max="8" step="1" value={cfg.hidden} disabled={locked} onInput={(e) => set("hidden", Number(e.currentTarget.value))} /></label>
        <label class="select">激活函数 <select value={cfg.activation} disabled={locked} onChange={(e) => set("activation", e.currentTarget.value)}><option value="tanh">tanh</option><option value="relu">ReLU</option><option value="sigmoid">sigmoid</option></select></label>
        <label class="select">学习率 <select value={cfg.lr} disabled={locked} onChange={(e) => set("lr", Number(e.currentTarget.value))}>{[0.03, 0.1, 0.3, 1, 3].map((v) => <option value={v}>{v}</option>)}</select></label>
        <label class="select">训练轮数 <select value={cfg.epochs} disabled={locked} onChange={(e) => set("epochs", Number(e.currentTarget.value))}>{[50, 100, 200, 400, 600, 1000].map((v) => <option value={v}>{v}</option>)}</select></label>
        <button type="button" class="btn" disabled={locked} onClick={train}>训练</button>
        {fresh ? <p class="stat">准确率 <b>{fmt(res.accuracy * 100, 1)}%</b> · 损失 {fmt(res.loss, 4)}</p> : <p class="stat muted">调好参数后点“训练”。</p>}
      </div>
    </div>
  );
}

// ---------- kmeans ----------
function KmeansView({ params: p, value, setValue, locked }) {
  const pts = useMemo(() => dataset(p.dataset || "blobs3", p.n, p.seed), [p.dataset]);
  const full = useMemo(() => kmeansRun(pts, p.k, p.kmSeed), [pts, p.k]);
  const it = Math.min(value.iterations || 0, full.history.length - 1);
  const cents = full.history[it];
  const assign = pts.map((q) => cents.reduce((best, c, j) => ((q[0] - c[0]) ** 2 + (q[1] - c[1]) ** 2 < (q[0] - cents[best][0]) ** 2 + (q[1] - cents[best][1]) ** 2 ? j : best), 0));
  const done = it >= full.iterations;
  const s = scales([-1.2, 1.2], [-1.2, 1.2], 300, 300, { l: 10, r: 10, t: 10, b: 10 });
  return (
    <div class="sim sim-kmeans">
      <div class="plot square"><svg viewBox="0 0 300 300" role="img" aria-label="k-means 聚类过程">
        {pts.map((q, i) => <circle cx={s.sx(q[0])} cy={s.sy(q[1])} r="4" class={"pt pt-" + assign[i]} />)}
        {cents.map((c, j) => <g class={"centroid c-" + j}><line x1={s.sx(c[0]) - 8} x2={s.sx(c[0]) + 8} y1={s.sy(c[1])} y2={s.sy(c[1])} /><line y1={s.sy(c[1]) - 8} y2={s.sy(c[1]) + 8} x1={s.sx(c[0])} x2={s.sx(c[0])} /></g>)}
      </svg></div>
      <div class="controls">
        <p class="stat">每一步：①每个点归到最近的中心（十字）；②每个中心移到自己那组点的平均位置。</p>
        <div class="btns"><button type="button" class="btn small" disabled={locked || done} onClick={() => setValue({ iterations: it + 1 })}>下一步</button><button type="button" class="btn small ghost" disabled={locked} onClick={() => setValue({ iterations: 0 })}>重来</button></div>
        <p class="stat">已迭代 <b>{it}</b> 次{done ? " · 中心不再移动：收敛了" : ""}</p>
      </div>
    </div>
  );
}

export default {
  plot: { View: PlotView, Demo: demoOf(PlotView, plotLogic.initial), initial: plotLogic.initial },
  matrix2d: { View: MatrixView, Demo: demoOf(MatrixView, mLogic.initial), initial: mLogic.initial },
  sampler: { View: SamplerView, Demo: demoOf(SamplerView, sLogic.initial), initial: sLogic.initial },
  descent: { View: DescentView, Demo: demoOf(DescentView, dLogic.initial), initial: dLogic.initial },
  neuron: { View: NeuronView, Demo: demoOf(NeuronView, nLogic.initial), initial: nLogic.initial },
  mlp: { View: MlpView, Demo: demoOf(MlpView, mlpLogic.initial), initial: mlpLogic.initial },
  kmeans: { View: KmeansView, Demo: demoOf(KmeansView, kLogic.initial), initial: kLogic.initial },
};
