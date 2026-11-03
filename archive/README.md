# 归档（不在游戏里）

这里放已经不在游戏里、但以后重写时可以参考的东西。游戏、构建和 `npm test` 都不读这个目录。目录结构和项目本身一一对应：`archive/src/game/sims/logic/math.js` 原来就在 `src/game/sims/logic/math.js`，要用时挪回同一个位置。

规则：只服务已归档内容的代码、样式和测试，跟着内容一起归档，不留在游戏里。重写某个技能、又用到这里的东西时，把它挪回去，接上它的测试和实验室条目。

| 内容 | 位置 | 说明 |
|---|---|---|
| 13 个旧内容包 | `data/content/` | 2026-11-03 归档，不满足零基础和覆盖面两条标准，写法是 version 1（`warmup` + `cards` + `items`，先讲完再练）。谁写的、怎么核对的、重写时怎么用，见该目录的 README |
| 7 种交互组件 | `src/game/sims/logic/math.js`、`src/game/sims/views/math.jsx`、`plot-kit.jsx`、`expr.js` | 函数图像（割线、黎曼和、泰勒、极限 4 种模式）、2×2 矩阵变换、抽样、梯度下降（一维、二维）、单个神经元、小神经网络、k-means。只有旧课用过，2026-11-04 归档 |
| 图组件的 3 种模式 | `src/game/sims/logic/algo.js`、`src/game/sims/views/algo.jsx` | 归档前的完整版本：Dijkstra（含负权边时和 Bellman–Ford 对比）、拓扑排序、最大流（Ford–Fulkerson / Edmonds–Karp、最小割）。游戏里的 `algo.js` 只留下课里用的 BFS 和 DFS |
| 它们的实验室条目 | `src/game/ui/lab-archived.js` | 挪回去时放进 `src/game/app/lab.js` 的 `LAB`。单元测试要求实验室的每一条都有课用到、课里的每个实验都在实验室里 |
| 它们的样式 | `src/web/style-archived.css` | 从 `src/web/style.css` 拿出来的规则；标着 “from:” 的是选择器列表里拿掉了归档的那部分 |
| 它们的单元测试 | `tests/unit/sims-archived.test.mjs` | 引用的是这里的副本，所以还能跑：`node --test archive/tests/unit/*.test.mjs`（12 项） |
| 零基础标准差距表 | `scripts/beginner-audit.mjs`、`reports/beginner-audit.md` | 当时用来衡量旧包离零基础标准有多远。现在每个内容包都必须通过 `scripts/check-pack.mjs` 里的同一套检查，这张表全是 0，不再需要。脚本引用的 `./lib/…` 在 `scripts/lib/`，挪回去就能跑 |

version 1 写法的支持（构建和游戏把 `warmup` + `cards` + `items` 转成 `flow`）也在 2026-11-04 去掉了：`flow` 按 “先猜 `{guess}`、讲解卡 `{card}`、练习 `{item}`” 的顺序写，旧包的 `warmup` 就是开头的 `guess`，`cards` 和 `items` 依次排在后面。重写时按 `docs/content-authoring.md` 写新的 `version: 2` 包，不要照旧包的写法。

## 归档组件的参数

原来写在 `docs/content-authoring.md` 的组件表里：

| sim | params | goal | solution（玩家的作答格式） |
|---|---|---|---|
| plot（secant） | `{mode: secant, f: "x^2", a: 1, hMax: 1}` | `{slope: {target: 2, tol: 0.05}}` | `{h: 0.01}` |
| plot（riemann） | `{mode: riemann, f: "x^2", a: 0, b: 1, rule: left\|right\|mid, nMax: 200}` | `{errorBelow: 0.01}` | `{n: 50}` |
| plot（taylor） | `{mode: taylor, series: exp\|sin\|cos\|ln1p, xMax: 3}` | `{at: 1, errorBelow: 0.001}` | `{order: 5}` |
| plot（limit） | `{mode: limit, f: "sin(x)/x", a: 0}` | `{value: 1, tol: 1e-6}` | `{guess: 1}` |
| matrix2d | `{start: [[1,0],[0,1]]}` | `{matrix}` / `{det: 0}` / `{maps: [[[1,0],[0,1]]]}` / `{eigvec: [1,1]}`，可加 `tol` | 2×2 数组 `[[0,-1],[1,0]]` |
| sampler | `{dist: coin\|die\|twoDice}` | `{samples: 1000}` | `{n: 1000}` |
| descent | `{f: "(x-3)^2", x0: 0}`，二元加 `vars: [x, y]`、`x0: [2, 1]` | `{target: 3, tol: 0.01, maxSteps: 30}` | `{lr: 0.3, steps: 20}` |
| neuron | `{gate: and\|or\|nand\|xor}` | `{accuracy: 1}` | `{w1: 1, w2: 1, b: -1.5}` |
| mlp | `{dataset: circle\|xor\|linear, hidden: 0}` | `{accuracy: 0.9}` | `{hidden: 6, activation: tanh, lr: 1, epochs: 600, seed: 1}` |
| kmeans | `{dataset: blobs3, k: 3}` | `{}` | `{iterations: 10}` |
| graph（dijkstra/topo） | 同 BFS，边第三项是权重：`edges: [[a, b, 4], …]` | `{}` | Dijkstra 是确定最短距离的顺序，topo 是排好的顺序；平局任选。Dijkstra 默认在节点下显示暂定距离，`hideDist: true` 隐藏 |
| graph（flow） | `{mode: flow, directed: true, start: s, sink: t, nodes, edges: [[s, a, 3], …]}`（容量是正整数，不能同时有 u→v 和 v→u） | `{}` | `{paths: [[s, a, t], [s, b, a, t]]}`：残量网络里的增广路，依次推瓶颈流量；送到最大流即对 |

Dijkstra 只更新还没确定的点（有负权边时会在结束后显示 Bellman–Ford 的真实距离做对比）；flow 里沿一条已有流量的边反着走等于退回流量。

函数表达式（`expr.js`）支持 `+ - * / ^`、括号、`2x` 这种省略乘号、`sin cos tan exp log ln sqrt abs tanh sigmoid relu`、常数 `pi e`。没用现成库的原因：只需四则运算和少数函数，expr-eval 自 2022 年未更新，math.js 约 9 MB。
