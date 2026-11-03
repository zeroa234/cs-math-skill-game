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
