# 归档（不在游戏里）

这里放已经不在游戏里、但以后重写时可以参考的东西。游戏、构建和 `npm test` 都不读这个目录。目录结构和项目本身一一对应：`archive/src/game/ui/lab-archived.js` 的条目原来就在 `src/game/app/lab.js`，要用时挪回同一个位置。

规则：只服务已归档内容的东西跟着内容一起归档，不留在游戏里。重写某个技能、又用到这里的东西时，把它挪回去。

| 内容 | 位置 | 说明 |
|---|---|---|
| 7 个还没重写的旧内容包 | `data/content/` | 2026-11-03 归档（原 13 个，已重写的 6 个技能的旧包 2026-11-04 删除），不满足零基础和覆盖面两条标准，写法是 version 1（`warmup` + `cards` + `items`，先讲完再练）。谁写的、怎么核对的、重写时怎么用，见该目录的 README |
| 还没有课用到的实验室条目 | `src/game/ui/lab-archived.js` | 抽样、二维梯度下降、单个神经元、小神经网络、k-means。组件的代码、样式和单元测试都已挪回游戏（数学组件 2026-11-04 随 M.1.1 挪回，图组件随 M.5.3 挪回，图组件的 Dijkstra、最大流两条实验室条目随 F.1.2 挪回，参数表在 `docs/content-authoring.md`）；单元测试要求实验室的每一条都有课用到，所以这几条等有课用到时再挪进 `src/game/app/lab.js` 的 `LAB` |
| 零基础标准差距表 | `scripts/beginner-audit.mjs`、`reports/beginner-audit.md` | 当时用来衡量旧包离零基础标准有多远。现在每个内容包都必须通过 `scripts/check-pack.mjs` 里的同一套检查，这张表全是 0，不再需要。脚本引用的 `./lib/…` 在 `scripts/lib/`，挪回去就能跑 |

version 1 写法的支持（构建和游戏把 `warmup` + `cards` + `items` 转成 `flow`）也在 2026-11-04 去掉了：`flow` 按 “先猜 `{guess}`、讲解卡 `{card}`、练习 `{item}`” 的顺序写，旧包的 `warmup` 就是开头的 `guess`，`cards` 和 `items` 依次排在后面。重写时按 `docs/content-authoring.md` 写新的 `version: 2` 包，不要照旧包的写法。
