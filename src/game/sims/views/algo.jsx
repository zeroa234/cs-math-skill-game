// View for the sim `graph` (BFS / DFS). Same { View, Demo, initial } shape as views/os.jsx.
// In a lesson card (demo) or with params.help the algorithm's own bookkeeping is shown (queue,
// stack, which nodes may come next) and a "next step" button plays it; in an exercise the player
// keeps that bookkeeping in their head and the order is judged on submit.
import { useState, useRef, useEffect } from "preact/hooks";
import { graph as gLogic, adjacency, orderState, judgeOrder, byId } from "../logic/algo.js";

const R = 17;
const MODE = { bfs: "广度优先搜索（BFS）", dfs: "深度优先搜索（DFS）" };

function frame(p) {
  const xs = p.nodes.map((n) => n.x), ys = p.nodes.map((n) => n.y), pad = R + 18;
  const x0 = Math.min(...xs) - pad, y0 = Math.min(...ys) - pad;
  const w = Math.max(...xs) - Math.min(...xs) + 2 * pad, h = Math.max(...ys) - Math.min(...ys) + 2 * pad;
  return { viewBox: `${x0} ${y0} ${w} ${h}`, w, pos: Object.fromEntries(p.nodes.map((n) => [n.id, n])) };
}

// Text keeps about the same on-screen size whatever width the drawing gets: u = user units per CSS
// pixel, measured from the rendered svg, scales the font sizes (in CSS).
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

// A straight edge between two node circles, with an arrowhead when directed.
function Edge({ a, b, directed, cls }) {
  const dx = b.x - a.x, dy = b.y - a.y, L = Math.hypot(dx, dy) || 1, ux = dx / L, uy = dy / L;
  const nx = -uy, ny = ux;
  const x1 = a.x + ux * R, y1 = a.y + uy * R, tx = b.x - ux * (R + 1), ty = b.y - uy * (R + 1);
  const bx = directed ? tx - ux * 10 : tx, by = directed ? ty - uy * 10 : ty;
  return (
    <g class={"gedge " + (cls || "")}>
      <line x1={x1} y1={y1} x2={bx} y2={by} />
      {directed && <polygon points={`${tx},${ty} ${bx + nx * 5},${by + ny * 5} ${bx - nx * 5},${by - ny * 5}`} />}
    </g>
  );
}

function Node({ n, cls, badge, onClick }) {
  return (
    <g class={"gnode " + (cls || "")} onClick={onClick}>
      <circle cx={n.x} cy={n.y} r={R} />
      <text class="nlabel" x={n.x} y={n.y} dominant-baseline="central" text-anchor="middle">{n.id}</text>
      {badge !== undefined && <text class="nbadge" x={n.x + R} y={n.y - R} dominant-baseline="central" text-anchor="middle">{badge}</text>}
    </g>
  );
}

const list = (xs) => (xs.length ? xs.join(" ") : "（空）");

// Click the nodes in the order the algorithm first reaches them.
function GraphView({ params: p, value, setValue, locked, result, demo }) {
  const help = demo || p.help;
  const seq = Array.isArray(value) ? value : [];
  const adj = adjacency(p);
  const j = judgeOrder(p, seq);
  const good = j.firstWrong < 0 ? seq : seq.slice(0, j.firstWrong);
  const st = orderState(p, good, adj);
  const tree = st.parent || {};
  const done = j.firstWrong < 0 && j.complete;
  const { viewBox, w, pos } = frame(p);
  const [svgRef, u] = useUnit(w);
  const pick = (id) => { if (!locked && !seq.includes(id)) setValue([...seq, id]); };
  const wrongAt = result && !result.correct ? result.detail.firstWrong : -1;
  const isTree = (u, v) => tree[v] === u || (!p.directed && tree[u] === v);
  const cur = p.mode === "bfs" ? st.head : st.stack[st.stack.length - 1];
  return (
    <div class="sim sim-graph">
      <p class="stat">算法：<b>{MODE[p.mode]}</b>，从 <b>{p.start}</b> 出发。按第一次访问到的先后顺序点节点。</p>
      <div class="plot graph" style={{ maxWidth: Math.min(560, Math.max(260, w * 1.25)) + "px" }}>
        <svg ref={svgRef} style={{ "--u": u }} viewBox={viewBox} role="img" aria-label={`${p.directed ? "有向" : "无向"}图：${p.nodes.length} 个节点，${p.edges.length} 条边`}>
          {p.edges.map((e) => <Edge a={pos[e[0]]} b={pos[e[1]]} directed={p.directed} cls={isTree(e[0], e[1]) ? "tree" : ""} />)}
          {p.nodes.map((n) => {
            const k = seq.indexOf(n.id);
            const cls = [k >= 0 ? "visited" : "", n.id === cur ? "current" : "", help && !done && st.next.includes(n.id) ? "candidate" : "", k >= 0 && (k === wrongAt || (help && k === j.firstWrong)) ? "wrong" : "", !locked && k < 0 ? "clickable" : ""].join(" ");
            return <Node n={n} cls={cls} badge={k >= 0 ? k + 1 : undefined} onClick={() => pick(n.id)} />;
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
      {help && j.firstWrong < 0 && !done && (
        <p class="small">
          {p.mode === "bfs" && <>队列（先进先出）：{list(st.queue)}{st.head ? <> · 正在展开 <b>{st.head}</b> 的邻居</> : null} · 下一步可以选：</>}
          {p.mode === "dfs" && <>栈（当前这条路）：{list(st.stack)} · 下一步可以选：</>}
          <b>{st.next.join("、")}</b>
        </p>
      )}
      {help && j.firstWrong >= 0 && <p class="small bad">第 {j.firstWrong + 1} 个（{seq[j.firstWrong]}）这时还轮不到；那一步可以选：{orderState(p, good, adj).next.join("、")}。点“撤销”回去再试。</p>}
      {done && <p class="stat">所有从 {p.start} 能到达的点都处理完了。{p.nodes.length > seq.length ? ` 到不了的点：${p.nodes.map((n) => n.id).filter((id) => !seq.includes(id)).join("、")}。` : ""} 粗线是搜索树：每个点是被谁发现的。</p>}
      {wrongAt >= 0 && <p class="small">从第 {wrongAt + 1} 个开始不对。一种正确顺序：{result.detail.sample.join(" → ")}</p>}
      {result && !result.correct && wrongAt < 0 && <p class="small">还没处理完所有的点。一种正确顺序：{result.detail.sample.join(" → ")}</p>}
    </div>
  );
}

function GraphDemo({ params }) {
  const [v, setV] = useState(() => gLogic.initial(params));
  return <GraphView params={params} goal={{}} value={v} setValue={setV} demo />;
}

export default {
  graph: { View: GraphView, Demo: GraphDemo, initial: gLogic.initial },
};
