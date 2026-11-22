# 两个仓库一起写课

这个项目由两边的 AI 一起写课：作者电脑上的 Claude，和云端的 Gemini（Google AI Studio）。两边看到的是不同的仓库，所以动笔前都要把两个仓库都看一遍，避免重复写同一个技能，或者把对方刚写的东西覆盖掉。

| 仓库 | 谁在写 | 是什么 |
|---|---|---|
| 工作区（作者电脑，分支 `wip/next`）与它的公开快照 [zeroa234/cs-math-skill-game](https://github.com/zeroa234/cs-math-skill-game) | Claude | 唯一的权威版本。写完、审完的技能在这里提交，再推一份快照到公开仓库（`scripts/publish-github.mjs`） |
| 私有协作仓库 [zeroa234/remote](https://github.com/zeroa234/remote) | Gemini | 内容和工作区同步（`scripts/sync-remote.mjs`，提交说明是 `sync: workspace at <工作区提交>`）。另外有 AI Studio 运行要用的 `server.mjs`、`metadata.json` 等文件，以及 `vendor/cs-math-skill-tree`（技能树数据，代替工作区里的同级项目） |

## 写之前（两边都要做）

1. 看 zeroa234/remote 最近的提交（GitHub 的 Commits 页，或 `git log`）。最新一个 `sync:` 提交之后的提交，是 Gemini 新写、工作区还没引入的。
2. 看工作区一侧的进度：`docs/development.md` 的“课程验收状态”表，以及公开仓库 zeroa234/cs-math-skill-game 的最新提交。Claude 另外看工作区 `wip/next` 的 `git log`。
3. 看下面的“进行中”表。选一个没人在写的技能，先在表里登记一行（技能、谁、开始日期），提交，再动笔。同一个技能同一时间只由一方写。

## 写的时候

- 标准见 [content-authoring.md](content-authoring.md)：零基础能看懂、覆盖技能树大纲的每一节、每个数都用脚本算过、先写覆盖表。
- 文风照已经验收的包（例如 `data/content/M.1.4.1.yaml`）：陈述句，不用感叹号和“竟然”“神奇”这类夸张词；一张卡讲一件事，连续的讲解卡不超过 2 张，之后要有一道题。
- 只改这个技能自己的文件：`data/content/<技能ID>.yaml`、`tests/content/<技能ID>.verify.py`、`reports/coverage/<技能ID>.md`；用到实验室组件时可以改 `src/game/app/lab.js` 的条目。README 和 `docs/development.md` 里的统计数字不用改，引入时由工作区一方统一重算。
- 游戏代码和其他脚本不要改；觉得需要改，写在提交说明里，由工作区一方处理。
- 文件用 UTF-8 编码、LF 换行。
- 能跑的检查尽量跑（先 `npm install`、`npm run data`）：`node scripts/check-pack.mjs data/content/<技能ID>.yaml`、`node scripts/check-coverage.mjs <技能ID>`、`python3 tests/content/<技能ID>.verify.py`。跑不了的在提交说明里写明。

## 写完以后

- **Gemini**：提交到 zeroa234/remote 的 `main`。提交说明写清写了什么、跑了哪些检查、哪些没跑。把“进行中”表里那一行的状态改成“待引入”。
- **Claude（工作区）**：
  1. `node scripts/sync-remote.mjs --status` 列出 remote 上还没引入的提交和它们改了哪些文件。
  2. 只把这个技能的文件取进工作区（不要把整个仓库拉下来），连同“进行中”表的改动。
  3. 按 content-authoring.md 审读、修改、补齐覆盖表，跑全部检查（check-pack、check-coverage、verify、`npm test`、这个包的 FULL e2e），提交到 `wip/next`，推公开仓库。
  4. `node scripts/sync-remote.mjs --accept <引入的 remote 提交> --push` 把工作区同步回 remote。同步会用工作区的版本覆盖 remote，所以必须先引入、再同步；remote 上有没引入的提交时，脚本会拒绝同步。
- 工作区自己写完的技能也照样同步到 remote，让 Gemini 看到最新状态。

## 进行中

| 技能 | 谁 | 开始 | 状态 |
|---|---|---|---|

人工智能远征全部 5 个待重写技能（M.6.2、M.6.2.2、A.2.1、A.2.3、A.4.1）已于 2026-11-20 在工作区写完并开放；同日审读、返工、复审后引入（见下面的记录）。八条推荐远征涉及的 47 个技能均已开放；其余 171 个技能以 `docs/development.md`“课程验收状态”表为准。

## 记录

- 2026-11-19 M.6.1 概率论：Gemini 在 remote 写初稿（f04dd46，16 课）；工作区引入时切卡、改文风、调整两课的章节、补覆盖表（`reports/coverage/M.6.1.md`）。
- 2026-11-20 M.6.2（17 课）、M.6.2.2（13 课）、A.2.1（17 课）、A.2.3（11 课）、A.4.1（9 课）：Gemini 在工作区按新标准重写，通过各自 `verify.py`、覆盖表与抽样 E2E（最终修改后没重跑 FULL），“人工智能”推荐远征开放。同日 Claude 审读：数学和数值没问题，人读的标准没做到，返工清单见 `reports/review-ai-route-2026-11-20.md`。
- 2026-11-20 返工（Gemini，ddd1fce…5742365）：五个包去掉夸张词、补讲术语、修好继承查词和清单里的三处错误，M.6.2、A.2.1、A.4.1 各拆出一课（现在 18、18、10 课）。Claude 复审：M.6.2、M.6.2.2 的错误选项已是真实误解；A.4.1 的错误选项仍多是一眼排除的凑数项，被加长后正确项反而 68% 是最短的，工作区重写了它全部 35 道单选的错误选项并收短正确项（e8642df）；A.2.1、A.2.3 课内还有少量凑数项，结业挑战里已没有。
