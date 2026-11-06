# 归档（不在游戏里）

这里放已经不在游戏里、但以后重写时可以参考的东西。游戏、构建和 `npm test` 都不读这个目录。归档沿用项目目录结构。

规则：只服务已归档内容的东西跟着内容一起归档，不留在游戏里。重写某个技能、又用到这里的东西时，把它挪回去。

| 内容 | 位置 | 说明 |
|---|---|---|
| 6 个旧版内容包 | `data/content/` | 2026-11-03 归档（原 13 个，6 个技能的旧包于 2026-11-04 删除，C.3.2 的旧包于 2026-11-07 删除），不满足零基础和覆盖面两条标准，写法是 version 1（`warmup` + `cards` + `items`，先讲完再练）。谁写的、怎么核对的、重写时怎么用，见该目录的 README |
| 数学与机器学习实验 | `../src/game/app/lab.js` | AI 远征的新版课程已经使用这些实验，条目已回到游戏实验室 |
| 零基础标准差距表 | `scripts/beginner-audit.mjs`、`reports/beginner-audit.md` | 当时用来衡量旧包离零基础标准有多远。现在每个内容包都必须通过 `scripts/check-pack.mjs` 里的同一套检查，这张表全是 0，不再需要。脚本引用的 `./lib/…` 在 `scripts/lib/`，挪回去就能跑 |

version 1 写法的支持（构建和游戏把 `warmup` + `cards` + `items` 转成 `flow`）也在 2026-11-04 去掉了：`flow` 按 “先猜 `{guess}`、讲解卡 `{card}`、练习 `{item}`” 的顺序写，旧包的 `warmup` 就是开头的 `guess`，`cards` 和 `items` 依次排在后面。重写时按 `docs/content-authoring.md` 写新的 `version: 2` 包，不要照旧包的写法。
