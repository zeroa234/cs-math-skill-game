// 实验室: the experiments (interactive widgets) the player has met in lessons, to play with again,
// not graded. It grows by one entry each time a finished lesson brings an experiment the player had
// not met before; experiments not met yet are simply not listed. Entries match lessons by
// core/lesson.js simKey. Sims no lesson uses any more are archived with their entries
// (archive/src/game/ui/lab-archived.js).
import { simKey, lessonSims } from "../core/lesson.js";
import { lessonKey } from "../core/rules.js";

const RACE = { shared: { x: 0 }, threads: [{ name: "T1", locals: { t: 0 }, steps: ["t = x", "t = t + 1", "x = t"] }, { name: "T2", locals: { t: 0 }, steps: ["t = x", "t = t + 1", "x = t"] }] };
const G6 = [{ id: "a", x: 40, y: 100 }, { id: "b", x: 140, y: 40 }, { id: "c", x: 140, y: 160 }, { id: "d", x: 240, y: 100 }, { id: "e", x: 240, y: 220 }, { id: "f", x: 340, y: 160 }];
const G6E = [["a", "b"], ["a", "c"], ["b", "d"], ["c", "d"], ["c", "e"], ["d", "f"], ["e", "f"]];

export const LAB = [
  // trace has no fixed program: it steps through the card programs of the lessons finished (programs())
  { group: "编程", items: [
    { name: "trace", title: "Python 单步执行", try: "选一段课里见过的程序，一步一步执行，看每一步之后变量的值和输出。" },
  ] },
  { group: "数学", items: [
    { name: "matrix2d", title: "矩阵就是变换", try: "试试 [[0,−1],[1,0]]（转 90°）、[[2,0],[0,1]]（横向拉长）、[[1,2],[2,4]]（压成一条线）。", params: { start: [[1, 1], [0, 1]] } },
    { name: "plot", title: "极限的数值表", try: "x 靠近 0 时 sin(x)/x 靠近多少？表格里左右两边的值越来越像。", params: { mode: "limit", f: "sin(x)/x", a: 0 } },
    { name: "plot", title: "割线逼近切线", try: "把 h 调小，看割线斜率怎样逼近导数 2。", params: { mode: "secant", f: "x^2", a: 1, hMax: 1 } },
    { name: "plot", title: "泰勒多项式", try: "阶数越高，sin x 在多宽的范围里被贴住？", params: { mode: "taylor", series: "sin", xMax: 6, maxOrder: 15 } },
    { name: "plot", title: "黎曼和", try: "增加矩形个数，误差怎么变？", params: { mode: "riemann", f: "x^2", a: 0, b: 1, rule: "left", nMax: 200 } },
    { name: "descent", title: "梯度下降（一维）", try: "x² + 10 sin x 有两个山谷。从 x = 3 出发走 40 步，停在哪里？它是最低的那个吗？", params: { f: "x^2 + 10*sin(x)", x0: 3, lr: 0.05 } },
  ] },
  { group: "计算机组成", items: [
    { name: "bits", title: "位与补码", try: "拨出 −1、−128、127；看同一串位按有符号/无符号读的差别。", params: { bits: 8, signed: true, start: 0 } },
  ] },
  { group: "数据结构", items: [
    { name: "stackqueue", title: "栈", try: "push 1、2、3 再 pop 三次：取出的顺序和放进去的顺序相反。", params: { kind: "stack", start: [], pushable: [1, 2, 3] } },
    { name: "stackqueue", title: "队列", try: "同样的操作换成队列：先进先出。", params: { kind: "queue", start: [], pushable: [1, 2, 3] } },
    { name: "hash", title: "哈希表（线性探测）", try: "10、17、3、24 的 h(k) 都是 3，看它们怎样一个个往后挤。", params: { size: 7, keys: [10, 17, 3, 24, 5], probe: "linear" } },
    { name: "graph", title: "广度优先搜索", try: "点“让算法走一步”看队列怎么变；再自己按 BFS 的顺序点一遍。", params: { mode: "bfs", start: "a", nodes: G6, edges: G6E } },
    { name: "graph", title: "深度优先搜索", try: "同一张图换成 DFS：一路走到底，走不动才退回上一个点。", params: { mode: "dfs", start: "a", nodes: G6, edges: G6E } },
  ] },
  { group: "算法与离散数学", items: [
    { name: "graph", title: "拓扑排序（偏序的线性扩展）", try: "整除关系的哈斯图：每个数都要排在它的倍数前面。有几种排法？", params: { mode: "topo", directed: true, nodes: [{ id: "1", x: 150, y: 250 }, { id: "2", x: 90, y: 170 }, { id: "3", x: 210, y: 170 }, { id: "4", x: 40, y: 90 }, { id: "6", x: 150, y: 90 }, { id: "12", x: 95, y: 15 }], edges: [["1", "2"], ["1", "3"], ["2", "4"], ["2", "6"], ["3", "6"], ["4", "12"], ["6", "12"]] } },
    { name: "graph", title: "Dijkstra 最短路", try: "每次确定暂定距离最小的点，再用它更新邻居。", params: { mode: "dijkstra", directed: true, start: "s", nodes: [{ id: "s", x: 30, y: 110 }, { id: "a", x: 140, y: 40 }, { id: "b", x: 140, y: 180 }, { id: "c", x: 240, y: 110 }, { id: "t", x: 330, y: 40 }], edges: [["s", "a", 4], ["s", "b", 1], ["b", "a", 2], ["a", "c", 1], ["b", "c", 5], ["c", "t", 3], ["a", "t", 6]] } },
    { name: "graph", title: "最大流", try: "先走 s→a→b→t，然后还能再送吗？试试沿 a→b 反着走。", params: { mode: "flow", directed: true, start: "s", sink: "t", nodes: [{ id: "s", x: 40, y: 100 }, { id: "a", x: 160, y: 30 }, { id: "b", x: 160, y: 170 }, { id: "t", x: 280, y: 100 }], edges: [["s", "a", 1], ["s", "b", 1], ["a", "b", 1], ["a", "t", 1], ["b", "t", 1]] } },
  ] },
  { group: "操作系统", items: [
    { name: "scheduler", title: "CPU 调度（时间片轮转）", try: "这是 RR、时间片 2 排出的时间线，看看平均等待时间。", params: { procs: [{ name: "A", arrive: 0, burst: 5 }, { name: "B", arrive: 1, burst: 3 }, { name: "C", arrive: 2, burst: 1 }], algo: "RR", quantum: 2 } },
    { name: "paging", title: "分页地址转换", try: "把虚拟地址 9029 拆成页号和偏移，查页表得到物理地址。", params: { pageSize: 4096, vaddr: 9029, table: [5, null, 7] } },
    { name: "threads", title: "你来当调度器", try: "两个线程各把 x 加 1。你能让最后 x 等于 1 吗？", params: RACE },
    { name: "replace", title: "页面置换", try: "Belady 找到的引用串，FIFO、3 个页框：缺页 9 次。同一串给 4 个页框，FIFO 反而缺页 10 次。", params: { frames: 3, refs: [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], policy: "FIFO" } },
  ] },
];
const ENTRIES = LAB.flatMap((g) => g.items.map((it) => ({ ...it, group: g.group, key: simKey(it.name, it.params) })));

// The experiment keys of every lesson the player has finished.
export function metKeys(packs, p) {
  const keys = new Set();
  for (const [skill, pack] of Object.entries(packs)) for (const l of pack.lessons) if (p.lessons[lessonKey(skill, l.id)]?.done) for (const k of lessonSims(l)) keys.add(k);
  return keys;
}

// The programs the trace experiment offers: every Python program shown on a card of a finished lesson,
// in the order the player finished those lessons.
export function programs(packs, p) {
  const out = [];
  for (const [skill, pack] of Object.entries(packs)) for (const l of pack.lessons) {
    const done = p.lessons[lessonKey(skill, l.id)]?.done;
    if (!done) continue;
    for (const s of l.flow) if (s.card?.sim?.name === "trace") out.push({ label: l.title, params: s.card.sim.params, done });
  }
  return out.sort((a, b) => a.done.localeCompare(b.done)).map(({ done, ...x }) => x);
}

// What the 实验室 shows: its groups with only the experiments met.
export const labGroups = (met) => LAB.map((g) => ({ group: g.group, items: ENTRIES.filter((e) => e.group === g.group && met.has(e.key)) })).filter((g) => g.items.length);

// Entries that are in the lab with `after` but were not with `before` (e.g. around finishing a lesson).
export const labNew = (before, after) => ENTRIES.filter((e) => after.has(e.key) && !before.has(e.key));
