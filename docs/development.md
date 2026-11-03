# 开发说明

README 只放玩家和第一次来的人要看的东西；这里是内容明细、界面地址、目录、测试、内容来源和自写部分。为什么这样设计见 [design.md](design.md)，数据模型和接口见 [architecture.md](architecture.md)。

## 内容明细

| | |
|---|---|
| 技能 | **183** 个：当前技能树 193 个去掉“交叉应用与前沿专题”10 个；“数据中心与高性能网络”已在上游 tree 中 |
| 前置 | **242** 条必须前置（没点亮不能学下一个）、推荐前置作为“支线” |
| 远征 | **我的远征：操作系统**（5 个技能：程序设计基础 → C/C++ → 数据结构 → 计算机组成原理 → 操作系统），可玩；**八条推荐远征**（网站、企业应用、手机应用、嵌入式、DevOps、AI、网络安全、算法，4–20 站）已按 Stack Overflow 2025 调查、美国劳工统计局预测和 roadmap.sh 等公开路线图选定，开发中（灰色）；**自己定目标**开发中。选法和逐项对应：[recommended-routes.md](recommended-routes.md)。任何目标的路线都由技能树自动排出，介绍从技能树写出，背景图按目标所在领域取（12 个领域共 10 张，另有 3 条路线的专属图） |
| 互动课 | 5 个技能、124 课，就是“我的远征”经过的 5 站：P.1.1 28 课、P.2.2 23 课、F.1.1 22 课、C.1.1 22 课、C.2.1 29 课。都按“写给零基础的标准”和“知识覆盖面标准”写好（点术语看解释，逐节覆盖表在 `reports/coverage/`）。共 125 道“先猜”、605 张讲解卡（54 张是逐步揭开的例题）、694 道即时判题的练习（其中 34 道要操作交互组件），另有 59 道结业挑战题（第一次答对 ≥ 80% 才点亮，没有自评）。早期另写过 13 个技能的旧版互动课，不达标，2026-11-03 归档（现在在 `archive/data/content/`），游戏不再读取，重写时只当参考 |
| 交互组件 | 9 种，课里都用到：位与补码、栈/队列、哈希表、图（你来当 BFS / DFS）、CPU 调度甘特图、分页地址转换、“你来当调度器”（竞态与死锁）、“你来当置换算法”（FIFO / LRU / 最优，每次缺页时点要换出的页）、真实 Python 单步执行。学完一课遇到新的实验，实验室就多一个。只有旧课用过的 7 种（函数图像、矩阵、抽样、梯度下降、神经元、小神经网络、k-means）和图组件的 Dijkstra、拓扑排序、最大流已归档（`archive/README.md`） |
| 其余 178 个技能 | 显示“开发中”：章节教材、前后置、综合练习和参考答案都能看，供自学；不记录完成、不点亮（理由见 [design.md](design.md)“结业挑战”） |
| 复习 | FSRS-7（ts-fsrs）间隔复习，跨技能混排 |
| 画面与声音 | 像素奇幻风，文字、界面、图标和美术统一成同一种像素风（像素字体、像素切角边框、像素图标）：开场动画（标题 + 两位导师对白）、多邻国式的蜿蜒关卡路径、答题后底部反馈栏和导师反应、庆祝页；8-bit 合成音效；背景音乐 4 种风格可选（像素 RPG、8-bit 芯片、中世纪奇幻、Lo-fi 学习），开场、营地和路线、上课和复习、结业挑战各放不同的曲子（25 首，全部 CC0）；声音、音乐、风格和音量都能在“我的”里调，顶栏喇叭一键全关；14 张生成的像素背景（10 张领域图、标题画面、3 条路线的专属图）、2 位导师（鲸鱼娘姐妹，角色设计 ZipZipPipe，CC BY-NC 4.0）的像素小人（9 个动作）和立绘 |

## 界面一览

每个界面都有自己的地址（如 `#/skill/C.2.1`、`#/lesson/P.1.1/first-program`，全部见 [architecture.md](architecture.md)“地址”），可以收藏。

- **开场**：第一次打开时播放，可跳过；营地页底部能重看。
- **选远征**（`#/pick`）：我的远征可选；推荐远征和自己定目标是灰色的“开发中”。
- **营地**：继续当前远征（旁边是“看整条路线”“换一条远征”）、今天该复习几题、现在能学的技能。
- **远征**：每个技能一条色带，章节是蜿蜒排列的圆形关卡，下一关弹出“开始”，导师站在旁边；旁边是“顺路推荐”。
- **地图**：全部 183 个技能，滚轮或双指缩放、拖动移动，点卡片打开技能页；电脑上悬停看要先学的技能链。从技能页返回时回到地图原来的缩放和位置。
- **技能页**：学完你能做什么、章节 1…n（每章“去哪深入”）、结业挑战（没有互动课的是综合练习）、要先学的技能及理由、课程证据（含 KTH 课程先修原文）、知识地图（主教材目录）。
- **实验室**（`#/lab`）：课里遇到过的实验，随便玩；学完一课遇到新的实验就多一个，没遇到的不显示。
- **我的**：等级、成就、声音和音乐、存档导出导入、角色来源、版本和检查更新。

## 目录

| 路径 | 内容 |
|---|---|
| `data/content/*.yaml` | 内容包（每个技能一份，目前 5 个）；旧版不达标的 13 个已归档；格式 `data/content.schema.json`，写法 [content-authoring.md](content-authoring.md) |
| `data/music.yaml`、`scripts/music/encode-music.mjs` | 背景音乐清单（来源、许可证、每种风格每个场景放哪几首）和处理脚本（下载、统一响度、转 Opus），成品在 `assets/music/`（见其 README） |
| `data/routes.yaml` | 我的远征（操作系统）、八条推荐远征（开发中，选法见 [recommended-routes.md](recommended-routes.md)）、自己定目标的开关；路线由前置自动推出 |
| `data/kth-evidence.yaml`、`data/extra-skills.yaml` | KTH 先修原文、游戏独有扩展入口（当前为空，C.3.5 已上游化） |
| `scripts/build-data.mjs` | 从 `../cs-math-skill-tree/output/*.json`（只读）生成 `src/gen/`、`src/web/outlines.js` 和两份报告 |
| `scripts/build-web.mjs` | esbuild 打包到 `output/web/` |
| `scripts/check-pack.mjs` | 校验内容包：格式、章名、选择题正确项、每个交互题的 `solution` 能否通过判题、代码能否在 Python 里跑通、YAML 双引号吃掉 LaTeX 反斜杠；`version: 2` 的包再按“写给零基础的标准”检查（`scripts/lib/beginner.mjs`，术语表 `data/jargon.yaml`） |
| `scripts/check-coverage.mjs` | 互动课对原技能树给这个技能列出的知识点是否逐节覆盖（覆盖面标准 C1） |
| `tests/content/*.verify.py` | 内容包里每个数值、输出、报错的核对：P.1.1 用真实 Python 运行；P.2.2 和 C.2.1 用 gcc 编译运行（本机没有 gcc 时用 WSL 的；`python -I tests/content/C.2.1.verify.py`，C.2.1 的链接和权限实验在 WSL 自己的 /tmp 里做，Windows 盘上 chmod 不生效）；F.1.1、C.1.1 和 C.2.1 的数值用 Python 独立重算 |
| `scripts/skill-brief.mjs`、`scripts/pack-digest.mjs` | 给作者看技能资料、给审稿人看内容包摘要 |
| `src/game/core/` | 纯逻辑：技能图与路线、解锁规则、进度存档、FSRS 复习、判题 |
| `src/game/sims/logic/` | 交互组件的纯逻辑（node 和网页共用，判题也用它） |
| `src/game/sims/views/`、`src/game/ui/` | Preact 界面 |
| `src/game/app/` | 路由（`router.js`）、存档和玩家操作（`state.js`、`actions.js`）、实验室（`lab.js`）、背景图（`art.js`）、音效和背景音乐（`sound.js`、`music.js`）、更新检查（`update.js`）、App 里才生效的部分（`native.js`） |
| `tests/` | 见下面“测试” |
| `scripts/publish-github.mjs`、`scripts/release-github.mjs`、`scripts/readme-images.mjs`、`.github/workflows/pages.yml`、`docs/releases/` | 发布到 GitHub：源码快照去掉导师素材、重新构建无导师的网页版并检查；建发布、附 APK（更新说明在 `docs/releases/<版本>.md`）；README 截图；Pages 部署 `output/web`（步骤见 [android.md](android.md)“发新版本”） |
| `scripts/lib/edge.mjs` | 所有要开浏览器的测试和脚本共用：找系统 Edge、把它的临时文件放进 `temp/`、构建后游戏的地址 |
| `assets/` | 像素背景（`bg/`，来源和提示词见其 README）、导师素材（`cast/`，来源、处理和限制见其 README）、像素字体（`fonts/`，OFL）、背景音乐（`music/`，CC0，来源见其 README） |
| `scripts/cast/` | 背景像素化、导师立绘的裁切；导师精灵的提取脚本和角色素材只在作者本地，不进公开仓库（见 README“已知限制”） |
| `capacitor.config.json`、`src/android/`、`scripts/android/`、`assets/app-icon/` | 安卓 App：Capacitor 配置、生成的安卓工程、打包和画图标的脚本、图标源图（见 [android.md](android.md)）；签名密钥在 `config/android/`，不进 git |
| `archive/` | 不在游戏里、留着重写时参考的东西：13 个旧内容包和只有它们用过的组件、样式、测试（见其 README）。游戏、构建和 `npm test` 都不读 |
| `reports/` | 启发式评估和手机版复查（`hci/`）、逐节覆盖表（`coverage/`）、章节排序、KTH 交叉核对、调研 |

## 测试

```bash
npm test             # 单元测试
npm run e2e          # 端到端（需要先 npm run build；用系统自带的 Edge）；FULL=1 npm run e2e 走全部 124 课
node tests/a11y.mjs  # 无障碍审计
node tests/phone-fit.mjs [360]  # 手机宽度下有没有东西撑出屏幕（FIT_PACKS=P.1.1 只走这个包）
node tests/glossary-fit.mjs     # 术语解释框在手机和电脑上不被裁掉
node tests/tree-sync.mjs        # 上游技能树同步后技能、互动课和知识地图的每一层都还在
node tests/look.mjs [--dark] [--phone]  # 按真实缩放（200%）截主要界面，肉眼检查
node scripts/check-pack.mjs data/content/*.yaml
```

| 测试 | 查什么 |
|---|---|
| `tests/unit/` | 46 项单元测试（零基础标准的每条规则各有正反例、教科书调度例题、竞态可达性、分页、页面置换（OSTEP 的例子、原技能树练习、Belady 异常）、补码、真实 Python 轨迹、FSRS 存档往返、BFS/DFS 任意合法顺序、实验室怎么增长、更新检查的版本比较和 GitHub 回应…）；归档组件的 12 项在 `archive/tests/unit/` |
| `tests/e2e.mjs` | 系统 Edge 无头测试：内容包里的课按正确答案玩一遍（任何正确答案被判错即失败；平时只走覆盖每种题型、每种交互组件和代码最宽的 16 课左右，`FULL=1` 走全部 124 课，发版前和改课程内容后用），再完整走一遍“学完全部章 → 结业挑战 → 点亮 → 后续解锁 → 到期复习”；地图拖动后点卡片（鼠标和触屏）、背景音乐、更新检查；旧存档导入和开发中技能的资料页；截图写到 `temp/shots/` |
| `tests/a11y.mjs` | axe-core 按 WCAG 2.2 AA 审计 18 个界面 × 明暗两种主题，外加课程里答对/答错之后的状态 |
| `tests/phone-fit.mjs` | 360px 手机模拟（触屏、移动视口）走开场、各主界面、每个技能页、抽样课程（`FULL=1` 为全部课）的每一步和庆祝页、结业挑战、复习；页面比屏幕宽（能被左右拖动、缩小）就失败，并检查开场两张立绘都在屏幕内 |
| `tests/lib/play.mjs` | e2e 和手机检查共用的答题、走课程代码 |

## 内容是怎么来的

- 技能、前置、学习资料、综合练习和答案、知识地图：全部来自原技能树（各自附证据）。
- 互动课：“我的远征”的 5 站于 2026-11-03 由主代理按“写给零基础的标准”和“知识覆盖面标准”重写，每站先写逐节覆盖表（`reports/coverage/<技能ID>.md`）再写课。P.1.1（28 课，从“程序是什么”讲起；427 处数值、输出、报错由 `tests/content/P.1.1.verify.py` 用真实 Python 核对）。P.2.2（23 课，从“C 程序要先编译”讲到分配器；151 处输出、类型大小、报错原文、地址顺序、段错误和 AddressSanitizer 的报告由 `tests/content/P.2.2.verify.py` 用 gcc 15 在 64 位 Linux 上编译运行核对）。F.1.1（22 课，照 ODS 讲；145 处由 Python 核对）。C.1.1（22 课，照 MIT 6.004 讲；106 处由 Python 核对）。C.2.1（29 课，照 OSTEP 讲，线程内存模型照 CS:APP 12.4；128 处由 `tests/content/C.2.1.verify.py` 核对：fork、exec、线程、锁、信号量、文件、链接和权限的 C 程序用 gcc 编译运行，调度、分页、TLB、页面置换、文件系统的数字用 Python 独立重算；引用的说法对照 OSTEP 原书和 CMU 18-613 的 CS:APP 课件）。所有交互题的标准答案由判题代码自动验证，所有代码单步题由真实 Python 运行生成。归档的 13 个旧包是谁写的、怎么核对的，见 `archive/data/content/README.md`。
- 同类产品与学习科学调研：[reports/research/similar-games.md](../reports/research/similar-games.md)。

## 和原技能树相比改了什么

1. **去掉跨领域 X**：10 个“交叉应用与前沿专题”技能和所有指向它们的连线。没有任何保留技能依赖它们，其余技能的步骤数不变（构建脚本会检查）。
2. **章节重新编号**：tree 和游戏的知识导览均使用技能内部编号，教材原章号单独关联（如技能第 1 章对应 OpenStax 2.2）；第三级小节也完整保留。游戏里每个技能的章就是它的必学知识项，编号 1…n；顺序取主教材的讲授顺序，但只有当一本主教材能定位**每一个**必学知识项时才重排，否则保留技能简介里的原顺序（183 个技能里 41 个重排）。规则和逐项结果：[reports/chapter-order.md](../reports/chapter-order.md)。
3. **KTH 交叉核对**：观众推荐了 KTH 课程检索（先修写得很清楚）。15 门 KTH 课程的“Specific prerequisites”原文（2026-11-03 读取）逐门对应到技能，构建脚本检查 KTH 要求的先修是否都在技能树的必须前置链里：**15/15 一致**。结果：[reports/kth-crosscheck.md](../reports/kth-crosscheck.md)，数据：`data/kth-evidence.yaml`。
4. **“数据中心与高性能网络”（C.3.5）**：观众指出缺 RDMA、DPDK、SmartNIC、数据中心网络等内容。这个技能先在游戏里加出来（依据 KTH FIK3221 和 UW CSE 561，必须前置为网络协议与操作系统），后来已同步到上游 tree，`data/extra-skills.yaml` 不再重复添加。调研：[reports/research/kth-and-hpn.md](../reports/research/kth-and-hpn.md)；同步说明：[reports/tree-sync-2026-11-03.md](../reports/tree-sync-2026-11-03.md)。

## 自写的部分

用到的现成组件见 README“用到的开源组件”。自己写的：精灵动画播放（`src/game/ui/cast.jsx`，Web Animations 按帧步进，几十行）、开场打字机、背景音乐播放（`src/game/app/music.js`，两个 `<audio>` 交叉淡入淡出，约 100 行）和音乐处理脚本（`scripts/music/encode-music.mjs`，调 ffmpeg 的胶水代码）、更新检查（`src/game/app/update.js`，读 GitHub Releases API，几十行）、线程交错的状态搜索、调度器和分页的模拟、Python 单步轨迹记录（`scripts/lib/pytrace.py`，基于 `sys.settrace`）、图组件的逻辑（`src/game/sims/logic/algo.js`：判断一个点击顺序是不是 BFS/DFS“可能产生的”顺序，约 100 行）、实验室的增长规则（`src/game/app/lab.js`）。图算法考察过 graphology（MIT）：它的 traversal 只给出一种结果，不给“下一步哪些点合法”和队列/栈的中间状态，而“你来当算法”恰恰要判断每一步，所以没有引入。归档组件里自写的部分（函数表达式解析器、小神经网络训练、Dijkstra、最大流）见 `archive/README.md`。

## 其他说明

- 互动课要同时满足两条标准：从零讲得懂，并且把原技能树给这个技能列出的内容教全（[content-authoring.md](content-authoring.md)）。“我的远征”的 5 站都已满足（覆盖表 `reports/coverage/`，`node scripts/check-coverage.mjs` 自动检查 C1）；路线卡片上的“已写好 x / n 站”要两条都满足才计数。C2–C5（CS2023 主题、学习资源、综合练习、后继技能）靠人读，记录在各站的覆盖表里。
- 推荐远征（8 条）和自己定目标还是“开发中”：要等路线上每一站的课按两条标准写好才开放；现在只重写了“我的远征”经过的 5 个技能。原来的“高性能网络”远征已撤下（它是操作系统路线的延伸，不是多数初学者的方向），它的技能还在（旧课已归档），自己定目标开放后可以选。
- 存档 v3 读档时会去掉旧版的教材打卡和自学点亮。
