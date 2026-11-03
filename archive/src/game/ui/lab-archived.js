// The 实验室 entries of the archived sims, as they were in src/game/ui/Lab.jsx (2026-11-04). When a
// rewritten lesson uses one of these sims again, move the sim back and put its entry back into LAB.
export const LAB_ARCHIVED = [
  { group: "数学与机器学习", items: [
    { name: "plot", title: "割线逼近切线", try: "把 h 调小，看割线斜率怎样逼近导数 2。", params: { mode: "secant", f: "x^2", a: 1, hMax: 1 } },
    { name: "plot", title: "黎曼和", try: "增加矩形个数，误差怎么变？", params: { mode: "riemann", f: "x^2", a: 0, b: 1, rule: "left", nMax: 200 } },
    { name: "plot", title: "泰勒多项式", try: "阶数越高，sin x 在多宽的范围里被贴住？", params: { mode: "taylor", series: "sin", xMax: 6, maxOrder: 15 } },
    { name: "plot", title: "极限的数值表", try: "x 靠近 0 时 sin(x)/x 靠近多少？", params: { mode: "limit", f: "sin(x)/x", a: 0 } },
    { name: "matrix2d", title: "矩阵就是变换", try: "试试 [[0,−1],[1,0]]（旋转）、[[2,0],[0,1]]（拉伸）、[[1,2],[2,4]]（压扁）。", params: { start: [[1, 1], [0, 1]] } },
    { name: "sampler", title: "大数定律", try: "抽得越多，频率越接近理论概率吗？", params: { dist: "twoDice" } },
    { name: "descent", title: "梯度下降（一维）", try: "学习率 0.1、0.9、1.1 各走 20 步，看会发生什么。", params: { f: "(x-3)^2", x0: 0, lr: 0.1 } },
    { name: "descent", title: "梯度下降（二维、狭长山谷）", try: "x²+10y² 在 y 方向陡得多：学习率稍大就来回震荡。", params: { f: "x^2 + 10y^2", vars: ["x", "y"], x0: [2.5, 1.5], lr: 0.05 } },
    { name: "neuron", title: "一个神经元", try: "调出 AND；再试试 XOR——为什么怎么调都差一个点？", params: { gate: "xor" } },
    { name: "mlp", title: "小小神经网络", try: "隐藏层为 0 时只能画直线；加到 4–6 个 tanh 神经元再训练。", params: { dataset: "circle", hidden: 0, epochs: 400, lr: 1 } },
    { name: "kmeans", title: "k-means 聚类", try: "一步步看中心怎样移到三团点的中间。", params: { dataset: "blobs3", k: 3 } },
  ] },
  { group: "算法与离散数学", items: [
    { name: "graph", title: "Dijkstra 最短路", try: "每次确定暂定距离最小的点，再用它更新邻居。", params: { mode: "dijkstra", directed: true, start: "s", nodes: [{ id: "s", x: 40, y: 110 }, { id: "a", x: 160, y: 40 }, { id: "b", x: 160, y: 180 }, { id: "c", x: 280, y: 110 }, { id: "t", x: 400, y: 40 }], edges: [["s", "a", 4], ["s", "b", 1], ["b", "a", 2], ["a", "c", 1], ["b", "c", 5], ["c", "t", 3], ["a", "t", 6]] } },
    { name: "graph", title: "拓扑排序（偏序的线性扩展）", try: "整除关系的哈斯图：每个数都要排在它的倍数前面。有几种排法？", params: { mode: "topo", directed: true, nodes: [{ id: "1", x: 150, y: 250 }, { id: "2", x: 90, y: 170 }, { id: "3", x: 210, y: 170 }, { id: "4", x: 40, y: 90 }, { id: "6", x: 150, y: 90 }, { id: "12", x: 95, y: 15 }], edges: [["1", "2"], ["1", "3"], ["2", "4"], ["2", "6"], ["3", "6"], ["4", "12"], ["6", "12"]] } },
    { name: "graph", title: "最大流", try: "先走 s→a→b→t，然后还能再送吗？试试沿 a→b 反着走。", params: { mode: "flow", directed: true, start: "s", sink: "t", nodes: [{ id: "s", x: 40, y: 100 }, { id: "a", x: 160, y: 30 }, { id: "b", x: 160, y: 170 }, { id: "t", x: 280, y: 100 }], edges: [["s", "a", 1], ["s", "b", 1], ["a", "b", 1], ["a", "t", 1], ["b", "t", 1]] } },
  ] },
];
