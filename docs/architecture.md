# 架构与接口

```text
../cs-math-skill-tree/output/skilltree.json ─┐                     （只读）
../cs-math-skill-tree/output/outlines.json  ─┤
data/extra-skills.yaml  data/kth-evidence.yaml ─┼─ scripts/build-data.mjs ─→ src/gen/tree.json      ─┐
data/routes.yaml  data/content/*.yaml          ─┘                        src/gen/content.json   ─┼─ scripts/build-web.mjs ─→ output/web/
                                                                          src/web/outlines.js    ─┘   （esbuild，一个 IIFE，双击即开）
output/web/ ─ npx cap sync android ─→ src/android/（Capacitor 安卓工程）─ gradlew assembleRelease ─→ output/apk/*.apk
```

安卓 App 只是同一份网页装进 WebView，见 [android.md](android.md)。网页代码里只有 `src/game/app/native.js`（`NATIVE`、返回键）和 `src/game/ui/Profile.jsx` 的导出存档区分 App 和浏览器。

模块按“谁拥有状态”分层，下层不知道上层：

| 层 | 目录 | 职责 | 依赖 |
|---|---|---|---|
| 数据 | `src/gen/`（生成） | 技能、前置、章、资料、路线、内容包 | — |
| 核心 | `src/game/core/` | 图查询、规则、存档、复习、判题：全是纯函数 | ts-fsrs |
| 组件逻辑 | `src/game/sims/logic/` | 每个交互组件的模拟与判题（node 与网页共用） | core/check |
| 应用 | `src/game/app/` | 全局状态、动作（唯一改存档的地方）、路由 | core |
| 界面 | `src/game/ui/`、`src/game/sims/views/` | Preact 组件，只渲染核心算出来的东西 | app |

## 1. 技能数据（`src/gen/tree.json`）

```ts
tree = { meta, levels, lanes: Lane[], routes: Route[], skills: Skill[] }
Skill = {
  id, name, en, domain, lane, step, x, y,          // step = 最长必须前置链 + 1；x/y 是地图坐标
  optional, scope, desc, levels,
  required:    { id, why }[],                       // 必须前置（有课程证据）
  recommended: { id, why }[],                       // 推荐前置（支线，不挡路）
  unlocks: id[], reach,                             // reach = 学完能解锁的后续技能数
  courses: { school, course, url, prereq, kind, content? }[],  // 原技能树的先修原文
  kth?: { code, name, credits, url, quote, fit, needs: { courses, skill, inClosure }[], fetched }[],
  chapterOrder: { basis: "zh1" | "en1" | … | "original" | "extension", source },
  chapters: { no, title, stage: "core" | "extension", note, zh: Ref[], en: Ref[] }[],   // no = 1..n
  sources: { key, lang, role, title, url, tier, free, access, publisher }[],
  readingSteps, routeStatus,
  exercise: { question, answer, covers, minutes, level } | null,  // 综合练习：原技能树已验算
  hasOutline, origin: "cs-math-skill-tree" | "game-extension",
}
Ref = { source: sources[].key, section: string, extent: "covered" | "partial" }
```

`src/web/outlines.js` 按需加载：`window.__OUTLINES__[id] = { sources, branches: [{ no, sourceRef, title, zh, items: [{ no: "1.2", sourceRef, … }] }] }`。`no` 是技能内编号，`sourceRef` 是教材自己的节号。

## 2. 内容包（`data/content/<id>.yaml`）

构建只读 `data/content/`；不达标的旧版包归档在 `archive/data/content/`，不进游戏（见 `archive/README.md`）。格式由 `data/content.schema.json` 定义，写法见 [content-authoring.md](content-authoring.md)。要点：`lessons[].chapter` 必须等于某个 `chapters[].title`；每个核心章都要有课；题目 `type ∈ choice | number | text | order | match | sim`。

## 3. 交互组件接口

逻辑（`src/game/sims/logic/*.js`，纯函数）：

```ts
Sim = {
  name: string,
  validate(params, goal): void,                // 写错参数/目标不可达时抛错（check-pack 调用）
  initial(params, goal): Response,             // 玩家作答的初始值
  check(params, goal, response): { correct: boolean, detail: object },
}
```

视图（`src/game/sims/views/*.jsx`）：

```ts
SimView = {
  View({ params, goal, value, setValue, locked, result }),  // 练习题里：收集作答
  Demo({ params }),                                        // 讲解卡里：不计分，随便玩
  initial,
}
```

**加一个组件**：在 `logic/` 写 `{name, validate, initial, check}` 并加进 `logic/index.js`；在 `views/` 写 `{View, Demo, initial}` 并加进 `views/index.jsx`；在 `tests/unit/sims.test.mjs` 加教科书例题；在 `docs/content-authoring.md` 的组件表里写参数和作答格式；在 `src/game/app/lab.js` 的 `LAB` 加一个示例（玩家学完第一节用到它的课，实验室就多出它；单元测试要求课里的每个实验都在 `LAB` 里，`LAB` 的每一条也都有课用到）。只有归档内容用到的组件跟着归档（`archive/README.md`）。内容包里的 `solution` 会被 check-pack 用你的 `check` 验证。

`trace` 特殊：构建时 `scripts/lib/pytrace.py` 用 `sys.settrace` 真实运行 Python，把每一步写进 `params.steps`，所以网页里不需要 Python。它以 `python -I -X utf8` 运行：`-I` 会忽略 PYTHONIOENCODING，不开 UTF-8 模式时，课里的代码带中文（如 P.2.3 的 `print("不是整数，再来")`）在 Windows 上会因编码出错。

## 4. 核心 API（`src/game/core/`）

| 模块 | 函数 | 说明 |
|---|---|---|
| graph.js | `indexTree(tree)` → `g` | `g.byId`、`g.lanes`、`g.laneOrder` |
| | `requiredClosure(g, id)` | 必须前置闭包（含自身） |
| | `topoOrder(g, ids)` | Kahn 拓扑序，平局按步骤、领域顺序、id |
| | `planRoute(g, route)` | `{…route, stops, sideQuests}` |
| rules.js | `skillState(g, content, p, id)` | `{status, chapters, done, missing, nextChapter, chapterOpen(i), bossOpen, progress, hasContent}`；`status ∈ dev | locked | open | learning | lit`；没有内容包时为 `dev`，章节和综合练习全部可看，不记录完成 |
| | `mastery(p, id)` | `lit | solid | mastered`，来自该技能复习卡的 FSRS 稳定性 |
| | `starsFor`、`lessonXp`、`shouldLight`、`nextUp`、`XP` | 星级、经验、点亮条件（只认能核对的证据，见 `docs/design.md`“结业挑战”）、推荐顺序 |
| lesson.js | `normalizeLesson(l)` → `{…, flow, items}` | 把写在内容包里的 `flow` 统一成一条步骤序列：`{kind: guess|card|item}`；`items` 是计分题。构建时存 `leanLesson`（只有 flow），`app/state.js` 载入时再派生 items |
| | `bossFlow(skill, pack)` → `{graded, flow, items}` | 结业挑战放什么：有内容包时是它的自动判分题；没有时返回空流程，由资料页直接显示原技能树综合练习及可展开的参考答案 |
| | `firstTryShare(items, results)`、`PASS_SHARE` | 第一次就答对（不看提示）的比例；点亮门槛 0.8 |
| progress.js | `createStore(adapter)` | `get / update(fn) / replace / subscribe / exportJson / importJson`；适配器 `localStorageAdapter()`、`memoryStorage()` |
| | `migrate`、`streak`、`addXp`、`levelOf` | 存档版本迁移（拒绝更新的版本）、连续天数、等级 |
| review.js | `newCard`、`reviewCard(card, {correct, firstTry, usedHint})`、`isDue`、`recall` | ts-fsrs 封装；Good / Hard / Again 的映射见 `gradeFor` |
| check.js | `checkItem(item, response)` | 各题型判题；`registerSimChecker` 由组件注册 |

存档（v3；v1 读档时去掉 `known` 和 `boss.self`；v2 读档时去掉 `selfChapters`、“自学者”成就和没有判分的 `lit/boss`，保留互动课结果、复习卡、经验和学习天数。导入旧存档也走同一迁移）：

```ts
{ v: 3, createdAt, xp, days: { "YYYY-MM-DD": xp }, achievements: { id: iso },
  skills:  { [id]: { lit?, boss?: { at, graded, auto, testOut } } },
  lessons: { ["skill/lesson"]: { done, stars, best, attempts } },
  cards:   { ["skill/lesson/item"]: FSRS card },
  settings: { route?, sourceLang: "zh" | "en" | "both", reduceMotion?, sound, introSeen? } }
```

## 5. 应用动作（`src/game/app/actions.js`）

唯一改学习进度的动作：`completeLesson`、`submitBoss`、`answerReview`。每个动作返回界面要展示的东西（星级、经验、新成就；`completeLesson` 还返回这一课让实验室新增的实验 `lab`）。

没有内容包的技能（状态 `dev`）不经过这些动作：`BossView` 在检查前置之前直接显示综合练习和折叠的参考答案，不进播放器、不结算；`submitBoss` 也拒收没有内容包或没有判分的结果。规则的理由见 [design.md](design.md)“结业挑战”。

课和题的 id 是存档键：内容不变才沿用 id，重写成别的课或题要换 id（否则旧的完成记录和复习卡会挂到新题上）。

## 6. 路线

`data/routes.yaml` 分三部分：`own`（我的远征，只写目标）、`recommended`（推荐路线：`id, status, name, goal, also, art?, tagline, story, evidence`）、`customGoals`（自己定目标是否开放）。构建时合成一个扁平列表 `tree.routes`，每条带 `kind`（own / recommended）和 `status`（open / dev）。站点由 `planRoute` 从 `goal` 和 `also` 的必须前置闭包推出（`routeGoals`）。**加一条推荐路线**：按 [recommended-routes.md](recommended-routes.md) 的规则定目标，写一条 YAML，`npm run build`。

“我的远征”和玩家自己定的目标都用路线 id `goal:<技能 id>`，名字、一句话和介绍由 `src/game/core/route-text.js` 的 `goalRouteText` 从技能树写出（纯函数，有单元测试），背景图由 `src/game/app/art.js` 的 `artFor` 按目标所在领域选（路线自带 `art` 时用它自己的）。`routeFor(id)`（`src/game/app/state.js`）对列表里的路线返回 `routeById[id]`，对其他 `goal:` 现场推出并缓存。`playable(r)` 只看 `status`；`activeRoute(p)` 给出玩家当前能走的路线，开发中的路线不会成为当前远征（营地、顶栏、地图、技能页的返回都用它）。路线改过 id 时，`was` 让旧存档继续指向它（旧的 `os` → `goal:C.2.1`）。`routeStats(r)` 给出站数、有互动课的站数、已按零基础和覆盖面两条标准写好的站数（`beginner`：包是 `version: 2`，而且构建时覆盖表通过了 C1，`pack.coverage` 为 true）、课数和分钟数。

## 7. 地址

`#/`（第一次打开时是开场）、`#/intro`、`#/pick`、`#/route/<id>`（`id` 可以是 `goal:<技能>`）、`#/map`、`#/skill/<id>`、`#/lesson/<skill>/<lesson>`、`#/boss/<id>`（`/test` 为跳级）、`#/review`、`#/me`、`#/lab`。

技能页的“返回”去玩家最后待过的总览界面（营地、远征、地图、选远征，`router.js` 的 `lastHub`）；直接打开技能页时回当前远征。地图离开时记下缩放和位置，本次打开期间回来时恢复。

## 8. 画面、角色和声音

| 模块 | 职责 |
|---|---|
| `src/game/ui/StepPlayer.jsx` | 课、结业挑战、复习共用的一题一屏播放器：`<StepPlayer kicker title closeHref flow coach itemLabel leaveText onFinish>`；`CardStep`（`reveal` 部分逐个揭示）、`ItemStep`（复习直接用它）、`useKey`。答错的计分题本轮最后再出一次。`LessonPlayer.jsx` 和 `BossView.jsx` 只负责开始前说明和结束后的结算 |
| `src/game/ui/md.jsx` | Markdown + KaTeX；`[[术语|释义]]` 渲染成可点开的查词按钮（一次只开一个，点别处或 Esc 关闭）；比内容框宽的独立公式、表格、代码块在还能滑的一边渐隐（`more-l` / `more-r` 加 CSS 遮罩，页面变化、滚动、改窗口大小时重算），并可用键盘聚焦滚动；行内公式比一行还宽（KaTeX 找不到断点）时挪到单独一行（`katex-line`），宽度变了再重新判断 |
| `scripts/lib/beginner.mjs` | 零基础标准：`beginnerIssues(pack, lessons, {inherited, coreChapters})` 返回 B1–B7 违规；`resolveTerms(pack, lessons, glossary)` 在构建时给题目和后面几课的卡片加查词（释义 URI 编码）。术语清单 `data/jargon.yaml`（`code` 把 for、if、def 等关键字对到术语，B1 也查代码块和题目的 `code`）；前置技能的术语由 `scripts/lib/packs.mjs` 的 `inheritedGlossary` 沿必须前置闭包收集 |
| `src/game/ui/icons.jsx` | `<Icon name size label>`：pixelarticons 的像素图标（24 格），全游戏只用它，不用 emoji |
| `src/game/ui/cast.jsx` | `CAST`（两位导师的名字、立绘、庆祝动作）；`<Sprite who action then scale flip cue>` 播放 `assets/cast/sprites.json` 描述的动画条（`action` 可以是动作串，最后一个循环）；所有动作画在同一个“舞台”上，脚的位置不变；`<Portrait who>` |
| `src/game/app/sound.js` | `play(name)`：tap、select、correct、wrong、star、fanfare、unlock、blip、locked、page。ZzFX 在第一次出声时才加载（它一加载就创建 AudioContext）；`settings.sound === false` 时不出声 |
| `src/game/app/update.js` | 版本和更新检查：`VERSION`（构建时由 `package.json` 写入）、`checkUpdate()` 查 GitHub 最新发布（10 秒超时，失败时给玩家看得懂的原因）、`isNewer(a, b)`、`checkInBackground()`（App 启动时调用，每天最多一次，记在 localStorage 的 `cs-math-skill-game/update`，不进存档）、`useFoundUpdate()` / `dismissUpdate()`（营地横幅，“以后再说”后同一版本不再提示） |
| `src/game/app/lab.js` | 实验室：`LAB`（每个实验的示例参数，按“计算机组成 / 数据结构 / 操作系统”等分组），`metKeys(packs, p)` 学完的课用到的实验（`core/lesson.js` 的 `simKey`：组件名加 `mode` 或 `kind`），`labGroups(met)` 实验室显示什么，`labNew(before, after)` 新增了什么；`programs(packs, p)` 是“Python 单步执行”可选的程序：学完的课里讲解卡上的程序。没遇到的实验不显示，也不上锁 |
| `src/game/app/music.js` | 背景音乐。`setMusicScene(title / explore / focus / challenge)` 由 `App.jsx` 按当前界面调用（没有内容包的结业挑战页只是读题，算 explore）；`setAppBackground(bool)` 由 `native.js` 在 App 进出后台时调用。曲目表 `src/gen/music.json` 由 `build-data` 从 `data/music.yaml` 生成并检查每首都已编码。两个 `<audio>` 交替使用，换曲时 0.9 秒交叉淡入淡出；同一场景几首轮流放，从随机一首开始，只有一首时循环。第一次点击或按键之前不出声，页面隐藏时暂停。设置：`music`（开关）、`musicStyle`、`musicVolume`（0–1，默认 0.5），`sound === false` 时也不放 |
| `src/game/ui/Intro.jsx`、`PickGoal.jsx` | 开场；选远征（推荐卡片 `RouteCard`、自定目标、`setRoute(id)`）；`artFor(route)` 给出路线背景图 |
| `scripts/build-web.mjs` | 把 `assets/{cast/sprites,cast/portraits,bg,fonts}` 拷到 `output/web/assets/`，`assets/app-icon/icon-only.png` 拷成标签页图标 `assets/icon.png`；`assets/cast/source/` 是原图，不发布 |

**换角色**：替换 `assets/cast/`（精灵用 `scripts/cast/extract-sprites.py` 的格式：每个动作一条横向 WebP + `sprites.json` 里的 `w h frames fps loop foot`），改 `CAST`。界面只通过 `Sprite`、`Portrait`、`CAST` 用到角色。
