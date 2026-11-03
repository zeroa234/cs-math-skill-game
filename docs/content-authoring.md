# 内容包编写规范（content pack）

每个技能一份 `data/content/<技能ID>.yaml`，格式由 `data/content.schema.json` 定义。没有内容包的技能显示为开发中，教材、前后置指引、原技能树综合练习和参考答案可直接看，供自学，不记录完成、不点亮。内容包让它变成有自动判分和正式结业挑战的互动课。

新写或重写的内容包要同时满足两条标准：

1. **写给零基础**（下面的 B、R 规则）：从零讲得懂。
2. **知识覆盖面**（C 规则，见“知识覆盖面标准”）：把 [cs-math-skill-tree](../../cs-math-skill-tree/) 给这个技能列出的内容教全。参考依据是 skill-tree 本身，以及它附带的课程和教材目录。

两条缺一不可。只顾零基础，课会好懂但不全。2026-11-03 对照 skill-tree 发现两个已按零基础标准重写的包都有漏：P.1.1 没讲元组、集合、异常处理、读写文件；P.2.2 没讲结构体、链表、void * 和动态链接（`reports/coverage-audit.md`）。

文件里声明 `version: 2`（现在只认这一种写法），构建会按能自动检查的部分检查。零基础写法的参考范例：`data/content/P.1.1.yaml`（2026-11-03 重写）。

## 写给零基础的标准（version: 2）

**为什么有这个标准**：用户试玩后指出，原来的课“像站在已经学会了的人的视角上写的”，单课内容量不够让小白真学懂。这在研究里叫**专家盲点（expert blind spot）**：懂的人记不起自己学会之前需要经过哪些步骤。按下面的规则审计原来的 18 个内容包（当时的审计脚本和结果已归档：`archive/scripts/beginner-audit.mjs`、`archive/reports/beginner-audit.md`）：每个包都有“术语先用后讲”，旧 P.1.1 有 30 个，C.2.1 有 29 个；每课的讲解只有几百字，后面紧跟一串练习。

规则分两类：能自动检查的（`scripts/lib/beginner.mjs`，check-pack 和构建都会跑，违反就失败），和要人读的（写完按下面的流程自查）。

| 规则 | 要求 | 依据 | 怎么查 |
|---|---|---|---|
| B1 先讲后用 | `data/jargon.yaml` 里的术语，第一次出现前必须有一张卡用 `**术语（英文）**` 讲清楚它，并写进本包的 `terms`；前置技能的内容包已经讲过的可以直接用；前置技能还没有内容包的，写进 `assumes` | 专家盲点（Nathan & Petrosino 2003）；预训练原则：先给出关键概念的名字和特征（Mayer 2014，16 个实验里 13 个支持） | 自动 |
| B2 讲一点、练一点 | 连续讲解卡不超过 2 张，之后必须有一个问题（先猜或练习） | 分段原则：学习者自己控制节奏的小段比连续讲解学得更深（Mayer 2014，10/10 个实验支持）；检索练习（研究报告 B1） | 自动 |
| B3 一张卡一个想法 | 一张卡的讲解文字（不算代码、表格、公式）不超过 240 字；超了就拆成两张，中间加一个问题 | 同上；工作记忆有限，同时出现的新元素越少越好（认知负荷，研究报告 B4） | 自动 |
| B4 先看例子再动手 | 要操作交互组件的计分题，之前同一课里必须有演示（卡片带 `sim`）或分步例题（卡片带 `reveal`） | 例题效应（Sweller & Cooper 1985）；从完整例题到独立解题逐步撤掉支架（Renkl & Atkinson 2003） | 自动 |
| B5 不跳步 | 不写“显然”“易知”“不难看出”“同理可得”这类词，把那一步写出来 | 专家盲点 | 自动 |
| B6 不自评 | 不出现任何让玩家给自己打分的内容 | 用户要求（2026-11-03）；自评不是学会的证据 | 自动 |
| B7 结业挑战够分量 | 结业挑战至少 max(5, 核心章数) 道自动判分题，每个核心章至少一道 | 点亮门槛是第一次答对 80%（掌握式学习，研究报告 B6），题太少时一题定生死 | 自动 |
| R1 先具体，再抽象 | 先给一个看得见的例子（一段能运行的代码、一个日常场景），再给它起名字，最后说一般规则 | 具体到抽象的渐隐（concreteness fading，Fyfe et al. 2014） | 人读 |
| R2 多步的题先给分步例题 | 需要好几步才能算出的题（算等待时间、拆地址、写循环），先给一张 `reveal` 例题：每一步的标题写“这一步要达成什么”，再给一道做了一半的题，最后才是独立的题 | 子目标标注（Margulieux, Guzdial & Catrambone 2012；后续重复实验结果不一，Morrison et al. 2015，所以只当写法，不当保证）；例题渐隐（Renkl & Atkinson 2003） | 人读 |
| R3 编程：先预测，再运行 | 代码先让人猜它会显示什么，再单步运行看真实结果，再改一改 | PRIMM（Sentance, Waite & Kallia 2019） | 人读 |
| R4 一课 10–15 分钟 | 一章内容多就拆成几课（`chapter` 写同一章即可），不要为了“每章一课”把讲解压缩成提纲 | 掌握式学习会拉长学习时间，这是代价不是缺陷（Kulik et al. 1990） | 人读 |
| R5 讲误解 | 选择题的错误项用初学者真实会犯的错，`why` 写清错在哪一步 | 信息性反馈（研究报告 B5） | 人读 |
| R6 每个数都算过 | 题里和卡片里出现的每个数值、输出、报错，用 Python 实际运行核对，写成 `tests/content/<技能ID>.verify.py` | 只写能查证的内容 | 脚本 |

**动笔前**：先按“知识覆盖面标准”写好覆盖表 `reports/coverage/<技能ID>.md`，决定每一节由哪一课教。

**写完的检查流程**：

```bash
node scripts/check-pack.mjs data/content/P.1.1.yaml     # 格式 + 判题 + 标准 B1–B7
node scripts/check-coverage.mjs P.1.1                    # C1：覆盖表对上大纲的每一节
python -I tests/content/P.1.1.verify.py                 # R6：每个数值、输出、报错都由真实 Python 核对
npm run build && npm run e2e                             # 每一课按正确答案玩一遍（E2E_PACKS=P.1.1 只玩这一个包）
```

然后做一遍**零基础通读**：
- 假装只学过前置技能，从第一课读到最后一课；
- 把每一个“没讲过就用了”的词、每一处“跳了一步”的地方记下来改掉；
- 新发现的术语加进 `data/jargon.yaml`，让以后的包自动查到它。

最后做一遍**覆盖面核对**：
- 拿覆盖表逐行对课；
- 用这些课教过的东西，把原技能树的综合练习做一遍。

### 来源

- Nathan, M. J., & Petrosino, A. J. (2003). Expert blind spot among preservice teachers. *American Educational Research Journal*, 40(4), 905–928. doi:10.3102/00028312040004905
- Mayer, R. E. (& Pilegard, C.) (2014). Principles for managing essential processing in multimedia learning: Segmenting, pre-training, and modality principles. In *The Cambridge Handbook of Multimedia Learning* (2nd ed.), ch. 13. 摘要：分段原则 10/10 个实验支持（中位效应量 0.79），预训练原则 13/16（0.75）。
- Sweller, J., & Cooper, G. A. (1985). The use of worked examples as a substitute for problem solving in learning algebra. *Cognition and Instruction*, 2(1), 59–89.
- Renkl, A., & Atkinson, R. K. (2003). Structuring the transition from example study to problem solving in cognitive skill acquisition. *Educational Psychologist*, 38(1), 15–22.
- Margulieux, L. E., Guzdial, M., & Catrambone, R. (2012). Subgoal-labeled instructional material improves performance and transfer in learning to develop mobile applications. （Morrison, Margulieux & Guzdial 2015 在大学入门课里没有完全重复出效果。）
- Sentance, S., Waite, J., & Kallia, M. (2019). Teaching computer programming with PRIMM: a sociocultural perspective. *Computer Science Education*, 29(2–3). doi:10.1080/08993408.2019.1608781
- Fyfe, E. R., McNeil, N. M., Son, J. Y., & Goldstone, R. L. (2014). Concreteness fading in mathematics and science instruction: a systematic review. *Educational Psychology Review*, 26(1), 9–25. doi:10.1007/s10648-014-9249-3
- Kulik, C.-L. C., Kulik, J. A., & Bangert-Drowns, R. L. (1990). Effectiveness of mastery learning programs: A meta-analysis. *Review of Educational Research*, 60(2), 265–299.

## 知识覆盖面标准

**为什么有这个标准**：用户 2026-11-03 问“为什么我没看到元组”。零基础标准只管讲得懂，不管讲全没有。P.1.1 和 P.2.2 是按自己列的学习目标写的，B1–B7 全过，却漏了教材里的整节。用户的要求是：以后不仅考虑新手，也要考虑知识覆盖面，以 skill-tree 和它附带的课程内容作为覆盖面参考。

**参考什么**：下面的文件都在 `../cs-math-skill-tree/`，只读。构建已经从它的 `output/` 读进了大纲和技能树。

| 文件 | 内容 | 用途 |
|---|---|---|
| `data/outlines/<技能ID>.json`（构建读的是 `output/outlines.json`） | `sources`：这个技能依据的课程或教材（如 P.1.1 是 Python 官方教程第 3–8 章和 CS50x 调试短片，P.2.2 是 Stanford CS107 和 B&O《深入理解计算机系统》第 7、10 章）；`outline`：逐节目录，已对照原文核对；`coverage`：每个知识点对应哪几节；`omitted`：整章不收的部分和理由 | 主标准 |
| `data/curation/scope.json` | 这个技能的知识点匹配到的 CS2023 核心主题 | 必须教到 |
| `data/curation/learning-paths/<技能ID>.json` | 每个知识点的中英文学习资源和具体章节，也就是本项目技能的 `chapters[].zh/en` | 补充参考 |
| `output/skilltree.json` 里的综合练习（游戏里的“原技能树的综合练习”） | 每个技能的综合题和参考答案 | 学完要做得出 |

| 规则 | 要求 | 怎么查 |
|---|---|---|
| C1 大纲每一节都有去处 | 大纲 `outline` 列出的每一节（有 `items` 的按小节算），要么有一课教它，要么写明不教的理由：属于哪个技能（写技能 ID），或超出入门层。`coverage` 点名的节必须有课讲到，可以只讲到入门需要的深度，但不能不讲 | 自动：`node scripts/check-coverage.mjs <技能ID>`（`scripts/lib/coverage.mjs`；构建也会跑，结果决定路线卡片是否计入） |
| C2 CS2023 核心主题 | `scope.json` 给这个技能匹配的 CS2023 主题都要有课讲到 | 人读 |
| C3 学习资源的章节 | `chapters[].zh/en` 引用的资源小节里讲到的概念要逐条核对，缺的补上，或写明为什么不收 | 人读 |
| C4 综合练习做得出 | 只用这些课和前置技能的课教过的东西，就能做出原技能树给这个技能的综合练习 | 人读 |
| C5 后继技能接得上 | 读必须后继技能（`unlocks` 里以它为必须前置的技能）已有的内容包和综合练习：它们直接用到、又不打算自己教的写法和概念，这一站要教到。这和 B1 先讲后用是一个道理，只是跨了技能 | 人读 |

**怎么记录**：先写覆盖表，再写课。表放在 `reports/coverage/<技能ID>.md`（范例：`reports/coverage/P.1.1.md`）：
- 大纲的每一节一行：`| 节 | 原文 | 课 |`。“节”用技能内部编号（大纲里每一节的 `number`，如 `2.4`），“课”写课 id（反引号括起来，可以写几个），或者写 `不教：理由`；
- 下面列出 CS2023 主题、综合练习各小题和后继技能用到的写法，各自由哪一课负责。

写完课再逐行核对一遍。覆盖表不全的包不算写完，也不计入路线卡片上的“已写好”：构建按 C1 检查每个包，通过才给它标上 `coverage: true`（`src/game/app/state.js` 的 `routeStats` 只数两条都满足的站）。

**现状**：2026-11-03 先对照了 P.1.1 和 P.2.2，结果在 `reports/coverage-audit.md`，两站随后补齐。“我的远征”的 5 站（P.1.1、P.2.2、F.1.1、C.1.1、C.2.1）都已按两条标准写完，覆盖表全部通过 C1。另外 13 个技能的旧版包不达标，已归档到 `archive/data/content/`，这些技能现在和其他没有互动课的技能一样。

## 一课的结构

一课 10–15 分钟，用 `flow` 从上到下写，玩的顺序就是写的顺序。每一项是三种之一：

- `guess`：先猜（不计星）。讲之前问一个能凭直觉猜的问题；答错正常，后面的卡会回答它。猜的题和它的解析里不要用还没讲的术语。
- `card`：讲解卡。一张一个想法，可带一个不计分的演示（`sim`），或者 `reveal`：几部分内容点一次“下一步”出现一部分，用来写分步例题（每部分的 `title` 写这一步的目标）或“先自己做，再看答案”。
- `item`：练习，即时判题，每题都有 `explain`。答错的本课最后再出一次。

典型的节奏：先猜 → 卡 → 题 → 卡 → 题 → 分步例题 → 做一半的题 → 独立的题 → 换个情境的题（迁移）。一章可以有好几课，`chapter` 写同一个章名；游戏里课按“第 N 课”编号，并显示它属于哪一章。

旧格式（`version: 1`，`warmup` + `cards` + `items`，先讲完再练）只在归档的旧包里（`archive/data/content/`，游戏和构建都不读，也不再认得这种写法）。重写某个技能时可以参考里面核对过的事实和数字，但不要照它的写法写。

## 术语和查词

- 在定义术语的那张卡里写 `**术语（英文）**`，同时在包顶部的 `terms` 里写一条 `{ term, def }`。`def` 是一句话（90 字以内），游戏里所有题目、解析、后面几课的卡片中，这个术语第一次出现的地方都会自动变成可以点开的词，点一下显示 `def`（复习时也一样）。同一课的卡片里不加，因为那一课自己就在讲它。
- 前置技能的内容包里 `terms` 讲过的词，可以直接用，也会自动带查词。
- 想在某处强制加查词，写 `[[术语]]`；选项和配对卡片里不会出现查词按钮（按钮里不能放按钮）。
- `data/jargon.yaml` 是“初学者不认识的词”清单，B1 只查清单里的词。读者发现漏网的词就加进去，清单只增不减；太常见、有日常含义的词（如“方法”“对象”“类型”）不放进去，以免误报。

## 写作要求

- 中文，面向零基础。术语第一次出现时给英文原词，如“进程（process）”。用“你”说话，像一位耐心的助教。
- 只写能查证的内容。教到哪里以 skill-tree 大纲为准（见“知识覆盖面标准”）；事实、数字、定义以该技能 `chapters[].zh/en` 列出的教材章节为准；数值答案必须用 Python 算过（在提交说明里写你怎么算的）。不确定就不写。
- 讲解卡里不要出现模块编号、“本章”“下一节”这种指向别处的说法；章节号由游戏统一编，教材自己的节号（如 OpenStax 2.2）只在“去哪深入”里出现，由游戏自动显示。
- 选择题：干扰项用初学者真实会犯的错误（例如把“并发”当成“并行”），每个错误项写 `why` 说明错在哪；不用“以上都对/都不对”。
- `explain` 要说清“为什么”，不是重复答案。答错的人读完能明白自己错在哪一步。
- `hint` 是一个推动思路的小问题，不是答案。
- 练习题会在几天后单独出现在复习里，看不到讲解卡和前一题。题干要自带全部条件；实在离不开前一题（“接上题”“上面那个”）就写 `review: false`，check-pack 会检查。
- 数学用 KaTeX：行内 `$...$`，独立公式 `$$...$$`。写在 `|` 块里，反斜杠不用转义。
- 代码放进题目的 `code` 字段（`lang: python` / `c`），不要塞进 prompt 文本。

## 题型

| type | 必填 | 玩家怎么答 | 说明 |
|---|---|---|---|
| choice | `options: [{text, correct?, why?}]`，多选加 `multi: true` | 点选 | 单选恰好一个 correct |
| number | `answer`，可选 `tolerance`、`unit` | 输入数字（支持 `3/2`、`50%`、`2^10`） | 默认容差是答案的百万分之一 |
| text | `answers: [...]`，可选 `caseSensitive` | 输入短文本 | 比较时忽略首尾空格、全角半角、大小写 |
| order | `steps: [...]`（按正确顺序写） | 拖动/点击排序 | 游戏会打乱 |
| match | `pairs: [[左, 右], ...]` | 连线配对 | 右侧文字不能重复 |
| sim | `sim`、`params`、`goal`、`solution` | 操作交互组件 | 见下表；`solution` 是一个能通过判题的答案，构建时会验证 |

题目默认进入间隔复习卡组（sim 题默认不进）；不想进就写 `review: false`。

## 交互组件（sim）

判题都在 `src/game/sims/logic/` 里，纯函数，node 和网页共用。

| sim | params | goal | solution（玩家的作答格式） |
|---|---|---|---|
| bits | `{bits: 8, signed: true, start: 0}` | `{value: -5}` | 位数组，高位在前，如 `[1,1,1,1,1,0,1,1]` |
| stackqueue | `{kind: stack\|queue, start: [1,2], pushable: [3,4]}` | `{state: [...]}` 和/或 `{outputs: [...]}` | `{ops: [{op: push, v: 3}, {op: pop}]}` |
| hash | `{size: 7, keys: [10,17,3], probe: linear\|chain}` | `{}` | 每个键放进的槽位 `[3,4,5]` |
| scheduler | `{procs: [{name, arrive, burst}], algo: FCFS\|SJF\|SRTF\|RR, quantum: 2}` | `{}` | 每个时间单位运行的进程名，空闲写 `null`，如 `[A,A,B,null]` |
| paging | `{pageSize: 4096, vaddr: 9029, table: [5, null, 7]}`（下标是页号，null 是未映射） | `{}` | `{vpn: 2, offset: 837, paddr: 29509}`，缺页写 `{vpn, offset, fault: true}` |
| threads | `{shared: {x: 0}, locks: [m], sems: {s: 0}, threads: [{name, locals: {t: 0}, steps: ["t = x", "t = t + 1", "x = t"]}]}` | `{final: {x: 1}}` 或 `{deadlock: true}` | 每一步选哪个线程（从 0 数），如 `[0,1,0,0,1,1]` |
| replace | `{frames: 3, refs: [7, 0, 1, 2, …], policy: FIFO\|LRU\|OPT}`（引用串最多 24 个，页框 1–6；`help: true` 在练习里也显示每页的进来时间 / 上次使用 / 下次使用） | `{}` 或 `{misses: 10}` | 每次“缺页且页框已满”时换出的页，按先后，如 `[7, 0, 1]`。OPT 下几页一样远（比如都不再用到）时任选一个都算对 |
| graph（bfs/dfs） | `{mode: bfs, start: a, directed: false, nodes: [{id: a, x: 40, y: 100}, …], edges: [[a, b], [b, c], …]}`（坐标是像素，整张图宽不超过约 360；`help: true` 在练习里也显示队列/栈/候选点） | `{}` | 节点第一次访问到的先后顺序 `[a, b, c]`。平局任选，算法能产生的任何一种顺序都算对 |
| trace | `{code: "...python...", stdin: ""}` | `{ask: [{line: 3, var: total, hit: 2}]}`（`var: "@out"` 问已打印的输出） | 不需要；构建时真的运行代码记录每一步 |

图组件的约定会显示给玩家：BFS 的“访问顺序”指第一次发现的顺序；DFS 指先序（第一次到达）。

只有旧课用过的组件（函数图像、矩阵、抽样、梯度下降、神经元、小神经网络、k-means）和图组件的 Dijkstra、拓扑排序、最大流已经归档，参数表在 `archive/README.md`；新课要用时先按那里说的挪回来。

**加了新的交互组件或新的模式**：在 `src/game/app/lab.js` 的 `LAB` 里加一条，玩家第一次学完用到它的课，实验室就多出这个实验（单元测试会检查课里的每个实验都在实验室里）。

页面置换组件的规则会显示给玩家：命中和“还有空页框”的缺页自动处理，只在页框满了时让玩家选；选错了当场提示“这一步不会换出它”，按“检查”之后才显示应该换出哪一页。

调度器的规则会显示给玩家：时间按整数单位；平局先到先得、再按表格顺序；SJF 不抢占，SRTF 抢占（剩余时间相同时正在运行的继续）；RR 中同一时刻新到达的进程排在时间片刚用完的进程前面。

## YAML 小抄

```yaml
skill: C.2.1
version: 2
brief:
  why: 两三句话：学它有什么用，从哪里讲起。
  outcomes:
    - 能说出进程和程序的区别
    - 能手算 FCFS 的平均等待时间
terms:
  - term: 进程
    def: '正在运行的程序：一份内存里的代码和数据，加上它执行到哪一步'
assumes: [寄存器]          # 前置技能讲过、但那个技能还没有内容包的术语
lessons:
  - id: process            # 小写字母、数字、连字符
    chapter: 进程/线程      # 必须和技能的章名完全一致；一章可以有几课
    title: 程序跑起来以后
    minutes: 12
    flow:
      - guess:
          id: guess
          type: choice
          prompt: 你同时开着浏览器和音乐播放器，电脑只有一个 CPU 核心。猜猜它们怎么“同时”运行？
          options:
            - text: 轮流用 CPU，切换得非常快
              correct: true
            - text: CPU 一半电路跑一个程序
              why: 一个核心同一时刻只做一件事
          explain: 它们在轮流，只是快到你察觉不到。
      - card:
          title: 程序和进程
          body: |
            磁盘上的程序是一个文件；把它运行起来，就有了一个**进程（process）**……
      - item:
          id: q1
          type: choice
          prompt: ……
          options: [...]
          explain: ……
      - card:
          title: 例题：……
          body: 题目……一步一步来。
          reveal:
            - title: 第 1 步：这一步要达成什么
              body: ……
            - title: 第 2 步：……
              body: ……
```

**引号的坑**（写完 check-pack 会报，但先知道省时间）：

- 冒号、`#`、`- `、反引号开头的文字要加引号或用 `|` 块。
- **值里有“英文冒号 + 空格”**（比如代码 `def f(x): return x`、字典 `{"a": 1}`）必须整句加引号，否则 YAML 会把它当成又一层键值。
- `{ text: …, why: … }` 这种一行写法里，值含英文逗号、`[ ]`、`{ }` 时必须加引号；一律用多行写法（如上）最省心。
- 单引号里的单引号写两遍：`'it''s'`。LaTeX 的反斜杠只放在单引号或 `|` 块里。

查一个技能的章、来源和原综合练习：`node scripts/skill-brief.mjs C.2.1`；看一个包的全部内容摘要：`node scripts/pack-digest.mjs data/content/C.2.1.yaml --cards`。参考范例：`data/content/P.1.1.yaml`。
