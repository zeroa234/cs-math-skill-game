// 实验室 entries no lesson uses yet (the sims themselves are back in src/game/sims). The lab test wants every
// LAB entry used by a lesson, so when a lesson first uses one of these, move its entry into src/game/app/lab.js.
export const LAB_ARCHIVED = [
  { group: "数学与机器学习", items: [
    { name: "sampler", title: "大数定律", try: "抽得越多，频率越接近理论概率吗？", params: { dist: "twoDice" } },
    { name: "descent", title: "梯度下降（二维、狭长山谷）", try: "x²+10y² 在 y 方向陡得多：学习率稍大就来回震荡。", params: { f: "x^2 + 10y^2", vars: ["x", "y"], x0: [2.5, 1.5], lr: 0.05 } },
    { name: "neuron", title: "一个神经元", try: "调出 AND；再试试 XOR——为什么怎么调都差一个点？", params: { gate: "xor" } },
    { name: "mlp", title: "小小神经网络", try: "隐藏层为 0 时只能画直线；加到 4–6 个 tanh 神经元再训练。", params: { dataset: "circle", hidden: 0, epochs: 400, lr: 1 } },
    { name: "kmeans", title: "k-means 聚类", try: "一步步看中心怎样移到三团点的中间。", params: { dataset: "blobs3", k: 3 } },
  ] },
];
