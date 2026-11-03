// View for the algorithms-route sim `graph`. Same { View, Demo, initial } shape as views/os.jsx.
// In a lesson card (demo) or with params.help the algorithm's own bookkeeping is shown (queue,
// stack, which nodes may come next) and a "next step" button plays it; in an exercise the player
// keeps that bookkeeping in their head and the order is judged on submit.
import { useState, useRef, useEffect } from "preact/hooks";
import { graph as gLogic, adjacency, orderState, judgeOrder, dijkstraState, bellmanFord, residual, augment, replayFlow, flowValue, residualReach, byId } from "../logic/algo.js";

const R = 17;
const MODE = { bfs: "广度优先搜索（BFS）", dfs: "深度优先搜索（DFS）", dijkstra: "Dijkstra 最短路", topo: "拓扑排序", flow: "最大流（Ford–Fulkerson）" };

function frame(p) {
  const xs = p.nodes.map((n) => n.x), ys = p.nodes.map((n) => n.y), pad = R + 18;
  const x0 = Math.min(...xs) - pad, y0 = Math.min(...ys) - pad;
  const w = Math.max(...xs) - Math.min(...xs) + 2 * pad, h = Math.max(...ys) - Math.min(...ys) + 2 * pad;
  return { viewBox: `${x0} ${y0} ${w} ${h}`, w, pos: Object.fromEntries(p.nodes.map((n) => [n.id, n])) };
}

// Text keeps about the same on-screen size whatever width the drawing gets: u = user units per CSS
// pixel, measured from the rendered svg, scales font sizes (in CSS) and label offsets (here).
function useUnit(w) {
  const ref = useRef(null);
  const [u, setU] = useState(1);
  useEffect(() => {
    const el = ref.current;
    if (!el || typeof ResizeObserver === "undefined") return;
    const ro = new ResizeObserver(() => { const cw = el.getBoundingClientRect().width; if (cw > 0) setU(Math.min(1.8, Math.max(0.6, w / cw))); });
    ro.observe(el);
    return () => ro.disconnect();
  }, [w]);
  return [ref, u];
}

// A straight edge between two node circles, an arrowhead when directed, and a label beside its middle.
function Edge({ a, b, directed, label, cls, u = 1 }) {
  const dx = b.x - a.x, dy = b.y - a.y, L = Math.hypot(dx, dy) || 1, ux = dx / L, uy = dy / L;
  const nx = -uy, ny = ux, side = ny > 0 || (ny === 0 && nx > 0) ? -1 : 1; // put the label above the line
  const x1 = a.x + ux * R, y1 = a.y + uy * R, tx = b.x - ux * (R + 1), ty = b.y - uy * (R + 1);
  const bx = directed ? tx - ux * 10 : tx, by = directed ? ty - uy * 10 : ty;
  const off = 5 + 7 * u, mx = (a.x + b.x) / 2 + side * nx * off, my = (a.y + b.y) / 2 + side * ny * off;
  return (
    <g class={"gedge " + (cls || "")}>
      <line x1={x1} y1={y1} x2={bx} y2={by} />
      {directed && <polygon points={`${tx},${ty} ${bx + nx * 5},${by + ny * 5} ${bx - nx * 5},${by - ny * 5}`} />}
      {label !== undefined && <text class="elabel" x={mx} y={my} dominant-baseline="central" text-anchor="middle">{label}</text>}
    </g>
  );
}

function Node({ n, cls, badge, sub, onClick, u = 1 }) {
  return (
    <g class={"gnode " + (cls || "")} onClick={onClick}>
      <circle cx={n.x} cy={n.y} r={R} />
      <text class="nlabel" x={n.x} y={n.y} dominant-baseline="central" text-anchor="middle">{n.id}</text>
      {badge !== undefined && <text class="nbadge" x={n.x + R} y={n.y - R} dominant-baseline="central" text-anchor="middle">{badge}</text>}
      {sub !== undefined && <text class="nsub" x={n.x} y={n.y + R + 9 * u} dominant-baseline="central" text-anchor="middle">{sub}</text>}
    </g>
  );
}

const list = (xs) => (xs.length ? xs.join(" ") : "（空）");
const edgeLabel = (e) => (e.length > 2 ? e[2] : undefined);

// ---------- bfs / dfs / dijkstra / topo: click the nodes in the order the algorithm handles them ----------
function OrderView({ params: p, value, setValue, locked, result, demo }) {
  const help = demo || p.help;
  const seq = Array.isArray(value) ? value : [];
  const adj = adjacency(p);
  const j = judgeOrder(p, seq);
  const good = j.firstWrong < 0 ? seq : seq.slice(0, j.firstWrong);
  const st = orderState(p, good, adj);
  const dj = p.mode === "dijkstra" ? dijkstraState(adj, p.start, seq) : null;
  const tree = (dj || st).parent || {};
  const done = j.firstWrong < 0 && j.complete;
  const { viewBox, w, pos } = frame(p);
  const [svgRef, u] = useUnit(w);
  const pick = (id) => { if (!locked && !seq.includes(id)) setValue([...seq, id]); };
  const wrongAt = result && !result.correct ? result.detail.firstWrong : -1;
  const isTree = (u, v) => tree[v] === u || (!p.directed && tree[u] === v);
  const showDist = p.mode === "dijkstra" && !p.hideDist;
  const neg = p.mode === "dijkstra" && p.edges.some((e) => e[2] < 0);
  const truth = neg && done ? bellmanFord(p) : null;
  const cur = p.mode === "bfs" ? st.head : p.mode === "dfs" ? st.stack[st.stack.length - 1] : null;
  return (
    <div class="sim sim-graph">
      <p class="stat">算法：<b>{MODE[p.mode]}</b>{p.start && p.mode !== "topo" ? <>，从 <b>{p.start}</b> 出发</> : null}。{
        p.mode === "dijkstra" ? "按“确定最短距离”的先后顺序点节点。" : p.mode === "topo" ? "按排好的先后顺序点节点：每条箭头的起点都要排在终点前面。" : "按第一次访问到的先后顺序点节点。"
      }</p>
      <div class="plot graph" style={{ maxWidth: Math.min(560, Math.max(260, w * 1.25)) + "px" }}>
        <svg ref={svgRef} style={{ "--u": u }} viewBox={viewBox} role="img" aria-label={`${p.directed ? "有向" : "无向"}图：${p.nodes.length} 个节点，${p.edges.length} 条边`}>
          {p.edges.map((e) => <Edge u={u} a={pos[e[0]]} b={pos[e[1]]} directed={p.directed} label={edgeLabel(e)} cls={isTree(e[0], e[1]) ? "tree" : ""} />)}
          {p.nodes.map((n) => {
            const k = seq.indexOf(n.id);
            const cls = [k >= 0 ? "visited" : "", n.id === cur ? "current" : "", help && !done && st.next.includes(n.id) ? "candidate" : "", k >= 0 && (k === wrongAt || (help && k === j.firstWrong)) ? "wrong" : "", !locked && k < 0 ? "clickable" : ""].join(" ");
            const d = dj?.dist[n.id];
            return <Node u={u} n={n} cls={cls} badge={k >= 0 ? k + 1 : undefined} sub={showDist ? (d === undefined ? "∞" : d) : undefined} onClick={() => pick(n.id)} />;
          })}
        </svg>
      </div>
      <div class="btns" role="group" aria-label="按顺序点节点">
        {[...p.nodes].sort((a, b) => byId(a.id, b.id)).map((n) => <button type="button" class="btn small" disabled={locked || seq.includes(n.id)} onClick={() => pick(n.id)}>{n.id}</button>)}
        <button type="button" class="btn small ghost" disabled={locked || !seq.length} onClick={() => setValue(seq.slice(0, -1))}>撤销</button>
        <button type="button" class="btn small ghost" disabled={locked || !seq.length} onClick={() => setValue([])}>重来</button>
        {demo && <button type="button" class="btn small" disabled={done || j.firstWrong >= 0} onClick={() => setValue([...seq, st.next[0]])}>让算法走一步</button>}
      </div>
      <p class="stat">你的顺序：<b>{seq.length ? seq.join(" → ") : "—"}</b></p>
      {showDist && <p class="small">暂定距离：{[...p.nodes].sort((a, b) => byId(a.id, b.id)).map((n) => `${n.id} ${dj.dist[n.id] ?? "∞"}${seq.includes(n.id) ? "（已确定）" : ""}`).join(" · ")}</p>}
      {help && j.firstWrong < 0 && !done && (
        <p class="small">
          {p.mode === "bfs" && <>队列（先进先出）：{list(st.queue)}{st.head ? <> · 正在展开 <b>{st.head}</b> 的邻居</> : null} · 下一步可以选：</>}
          {p.mode === "dfs" && <>栈（当前这条路）：{list(st.stack)} · 下一步可以选：</>}
          {p.mode === "dijkstra" && <>还没确定的点里，暂定距离最小（{dj.dist[st.next[0]]}）的：</>}
          {p.mode === "topo" && <>入边都已排好、可以排下一个的点：</>}
          <b>{st.next.join("、")}</b>
        </p>
      )}
      {help && j.firstWrong >= 0 && <p class="small bad">第 {j.firstWrong + 1} 个（{seq[j.firstWrong]}）这时还轮不到；那一步可以选：{orderState(p, good, adj).next.join("、")}。点“撤销”回去再试。</p>}
      {done && <p class="stat">{p.mode === "topo" ? "排完了。" : `所有从 ${p.start} 能到达的点都处理完了。`}{p.mode !== "topo" && p.nodes.length > seq.length ? ` 到不了的点：${p.nodes.map((n) => n.id).filter((id) => !seq.includes(id)).join("、")}。` : ""}{p.mode === "bfs" || p.mode === "dfs" ? " 粗线是搜索树：每个点是被谁发现的。" : p.mode === "dijkstra" ? " 粗线是最短路径树。" : ""}</p>}
      {truth && <p class="stat bad">有负权边：真正的最短距离（Bellman–Ford）是 {Object.keys(truth).sort(byId).map((v) => `${v} = ${truth[v]}`).join("，")}；Dijkstra 给出的是 {Object.keys(dj.dist).sort(byId).map((v) => `${v} = ${dj.dist[v]}`).join("，")}。</p>}
      {wrongAt >= 0 && <p class="small">从第 {wrongAt + 1} 个开始不对。一种正确顺序：{result.detail.sample.join(" → ")}</p>}
      {result && !result.correct && wrongAt < 0 && <p class="small">还没处理完所有的点。一种正确顺序：{result.detail.sample.join(" → ")}</p>}
    </div>
  );
}

// ---------- flow: pick augmenting paths in the residual graph ----------
function FlowView({ params: p, value, setValue, locked, result, demo }) {
  const help = demo || p.help;
  const [showResidual, setShowResidual] = useState(false);
  const paths = value?.paths || [];
  const cur = value?.cur?.length ? value.cur : [p.start];
  const { flow } = replayFlow(p, paths);
  const last = cur[cur.length - 1];
  const canGo = (v) => last !== p.sink && !cur.includes(v) && residual(p, flow, last, v) > 0;
  const go = (v) => { if (!locked && canGo(v)) setValue({ paths, cur: [...cur, v] }); };
  const caps = cur.slice(1).map((v, i) => residual(p, flow, cur[i], v));
  const ready = last === p.sink && cur.length > 1;
  const push = () => { if (ready && !augment(p, flow, cur).error) setValue({ paths: [...paths, cur], cur: [p.start] }); };
  const undo = () => setValue(cur.length > 1 ? { paths, cur: cur.slice(0, -1) } : { paths: paths.slice(0, -1), cur: [p.start] });
  const reach = residualReach(p, flow);
  const stuck = !reach.has(p.sink);
  const onPath = (u, v) => cur.some((x, i) => i > 0 && ((cur[i - 1] === u && x === v) || (cur[i - 1] === v && x === u)));
  const backward = (u, v) => cur.some((x, i) => i > 0 && cur[i - 1] === v && x === u);
  const cut = (u, v) => stuck && (help || result?.correct) && reach.has(u) && !reach.has(v);
  const { viewBox, w, pos } = frame(p);
  const [svgRef, u] = useUnit(w);
  const val = flowValue(p, flow);
  const cutCap = p.edges.filter(([u, v]) => reach.has(u) && !reach.has(v)).reduce((a, e) => a + e[2], 0);
  return (
    <div class="sim sim-graph">
      <p class="stat">从源点 <b>{p.start}</b> 往汇点 <b>{p.sink}</b> 送流。边上写的是“流量/容量”。从 {p.start} 起一个点一个点点出一条还有剩余容量的路，再按“推流”。</p>
      <div class="plot graph" style={{ maxWidth: Math.min(560, Math.max(260, w * 1.25)) + "px" }}>
        <svg ref={svgRef} style={{ "--u": u }} viewBox={viewBox} role="img" aria-label={`流网络：${p.nodes.length} 个节点，${p.edges.length} 条有向边`}>
          {p.edges.map(([a, b, c]) => {
            const f = flow[`${a}>${b}`] || 0;
            const label = showResidual ? `剩${c - f}${f ? ` 退${f}` : ""}` : `${f}/${c}`;
            return <Edge u={u} a={pos[a]} b={pos[b]} directed label={label} cls={[onPath(a, b) ? (backward(a, b) ? "aug back" : "aug") : "", f === c ? "full" : "", cut(a, b) ? "cut" : ""].join(" ")} />;
          })}
          {p.nodes.map((n) => <Node u={u} n={n} cls={[cur.includes(n.id) ? "visited" : "", n.id === last ? "current" : "", help && canGo(n.id) ? "candidate" : "", !locked && canGo(n.id) ? "clickable" : ""].join(" ")} onClick={() => go(n.id)} />)}
        </svg>
      </div>
      <div class="btns" role="group" aria-label="沿剩余容量走到下一个点">
        {[...p.nodes].sort((a, b) => byId(a.id, b.id)).map((n) => <button type="button" class="btn small" disabled={locked || !canGo(n.id)} onClick={() => go(n.id)}>{n.id}</button>)}
        <button type="button" class="btn small primary" disabled={locked || !ready} onClick={push}>推流 {ready ? Math.min(...caps) : ""}</button>
        <button type="button" class="btn small ghost" disabled={locked || (cur.length <= 1 && !paths.length)} onClick={undo}>撤销</button>
        <button type="button" class="btn small ghost" disabled={locked || (cur.length <= 1 && !paths.length)} onClick={() => setValue({ paths: [], cur: [p.start] })}>重来</button>
      </div>
      <label class="check"><input type="checkbox" checked={showResidual} onChange={(e) => setShowResidual(e.currentTarget.checked)} /> 显示残量（“剩”= 还能往前送多少，“退”= 能沿反方向退回多少）</label>
      <p class="stat">当前路径：<b>{cur.join(" → ")}</b>{caps.length ? <>（瓶颈 {Math.min(...caps)}）</> : null} · 总流量 <b>{val}</b>{paths.length ? ` · 已推 ${paths.length} 次` : ""}</p>
      {help && !stuck && last !== p.sink && <p class="small">从 {last} 还能走到：{p.nodes.map((n) => n.id).filter(canGo).sort(byId).join("、") || "（没有了，撤销换一条）"}。沿一条已经有流量的边反着走，等于把那部分流量退回去。</p>}
      {stuck && <p class="stat">残量网络里已经走不到 {p.sink} 了：没有增广路，流量 {val} 就是最大流。{help || result?.correct ? ` 虚线是最小割：从 ${p.start} 还能走到的点 {${[...reach].sort(byId).join(", ")}} 和其余点之间的边，容量合计 ${cutCap}，正好等于最大流。` : ""}</p>}
      {result && !result.correct && <p class="small">{result.detail.error ? result.detail.error + "。" : ""}还没到最大流：最大流是 {result.detail.best}，你送到了 {result.detail.value ?? val}。</p>}
    </div>
  );
}

function GraphView(props) {
  return props.params.mode === "flow" ? <FlowView {...props} /> : <OrderView {...props} />;
}
function GraphDemo({ params }) {
  const [v, setV] = useState(() => gLogic.initial(params));
  return <GraphView params={params} goal={{}} value={v} setValue={setV} demo />;
}

export default {
  graph: { View: GraphView, Demo: GraphDemo, initial: gLogic.initial },
};
