# 同类产品 / 游戏 + 学习科学 调研笔记

> 用途：为「计算机 + 数学技能树网页游戏」（192 技能、必修/推荐前置、每技能 4–9 个知识项 + 1 道综合练习）做设计参考。
> 目标路线：① 程序设计基础 → C/底层 → 数据结构 + 计算机组成 → 操作系统；② 极限/导数/积分/线代/概率/多元微分/Python/机器学习 → 深度学习。
> 原则：只写查得到出处的内容，链接均可打开；查不到的条目明确写「未查到」，不编数字与年份。
> 调研时间：**2026-11-02**（所有「最新版本 / 最近更新」均以此日为准；文中「抓取于」标注的即为该日）。

---

## A. 同类产品与游戏

### A1. Duolingo

**1) 技能树（tree）→ 单线路径（path）的改版**

- **时间线（有官方出处）**：官方博客《Introducing the new Duolingo learning path》发布于 **2022-05-06**（页面记录的日期；CNET 于 **2022-05-07** 报道同一改版，可交叉印证），文中明确「新的首页体验于 **2022 年 11 月 1 日** 面向所有学习者上线」。官方 X（Twitter）账号在 **2022-08-29** 发帖预热同一改版：「许多人的学习路径正在发生大变化……新的首页设计是为了更好地引导你逐课前进，且**不会丢失任何进度**」。
  - 官方博客：https://blog.duolingo.com/new-duolingo-home-screen-design
  - 官方 X 帖子：https://x.com/duolingo/status/1564270050734997505
  - CNET 报道（2022-05-07）：https://www.cnet.com/tech/services-and-software/8-changes-duolingo-made-for-easier-language-learning-in-2022

- **官方给出的原因（原文可查）**：
  1. 「我们经常听到学习者说，他们不确定自己是否在用『正确/最佳』的方式使用 Duolingo」——即**降低选择成本、消除「我是不是学错了」的焦虑**。
  2. **间隔重复**：「路径中课程的排序基于 spaced repetition……先学一个概念后应较快复习，然后逐步拉长间隔」，把原来需要玩家自己执行的「hover / waterfall 学习法」变成**默认排课**。原文：「if your approach has been to completely 'level up' a skill and turn it gold before moving on, the new path may feel a bit different」。
  3. **课程混排**：旧版是「技能 → 5 个 crown level → 若干 lesson」的纵向堆叠；新版「路径上的一个圆点 = 旧版某技能的 1 个 crown level」，**不同技能的 level 被交错铺在路径上**（这正是交错练习/间隔练习的工程化）。
  4. **练习内建**：「Practice is built into your path」，复习不再是「倒回去」，而是「前进的一部分」。
  5. 内容零改动：「Lesson content is the **same**」，只是重排 + 分组为更小的 unit。
  - 出处：同上官方博客。

- **代价（官方自己承认的）**：路径变长（因为 level 被摊开 + 插入 practice 和 Stories），长列表导航困难（官方加了右下角「跳回当前位置」浮动按钮，并称「正在探索更好的长课程导航」）。

**2) skill decay /「裂开的技能」（cracked skills）是否被移除、为什么**

- **已移除，且是官方明说的**：官方博客在「Quick overview」里直接写「**Practice is built into your path (so you won't have to worry about jumping around or going back to "cracked" skills)**」。即：不是「取消了遗忘」这件事，而是**把复习从「玩家自己发现技能裂开、手动点进去修」改成「系统排进路径，你不必操心」**。
- 旧机制的技术描述（第三方存档，可查）：「Duolingo 的机器学习会感知你已掌握但开始生锈的技能，这些技能会在该复习时** visibly 'crack'**」——https://duolingo.hobune.stream/comment/34982948/Restoring-skills-and-why-it-s-a-problem （Duolingo 官方论坛存档）；机制条目见 https://duolingo.fandom.com/wiki/Skill
- **社区反应（争议点）**：一部分老用户不喜欢裂开的技能（觉得像被惩罚、像强制复习），另一部分用户认为「不复习就会忘」才是对的（r/duolingo 讨论：https://www.reddit.com/r/duolingo/comments/ujgdcc/why_the_hate_for_the_cracked_skills ）。
- **对我们的关键启示**：遗忘衰减机制本身没被证伪，Duolingo 放弃的是**「把 decay 可视化成一个需要玩家手动修补的破洞」这种表现方式**（它制造负罪感且把复习变成负担），改为**系统排程 + 复习算作前进**。这是一个 UI/心理层结论，不是学习科学层结论。

**3) XP / 连胜（streak）/ 红心（Hearts）机制及争议**

- **Hearts 机制与其被替换**：官方 2025-07-03 博客《Why Duolingo switched to Energy and how it helps you learn》说明：旧 Hearts 机制下「免费学习者每错一次扣 1 颗心」，官方自评「**这不是支持学习的最有效方式**」，尤其是初学者「**在一节课中途耗尽红心的概率是 2 倍**」，并承认「犯错是学习的自然组成部分」。新机制 Energy：满格开始、每节课消耗少量、**连续答对可以回能**、**课末复习错题不消耗能量**、约一天充满。官方称数据表明「更多学习者能完成课程」。
  - 官方：https://blog.duolingo.com/duolingo-energy
  - 注意：官方原文写「Energy is only available to a small number of users right now」（2025-07 时点），Class Central 报道称 2025 年 4 月起从小范围开始替换 Hearts（https://www.classcentral.com/report/duolingo-breaks-hearts-for-energy ，更新于 2025-10-16）。
- **争议（负面证据，重要）**：
  - Class Central（2025-10）：用户反馈 Energy 比 Hearts **更限制免费学习**——「以前只要不犯太多错就能一直练；现在即使全对，能量也比以前掉得快」，免费用户占 Duolingo 用户基数约 90%（该文引 Duolingo 投资者材料），并质疑「免费教育」承诺。链接同上。
  - 对 Hearts 的长期批评（更早，2021-06-10）：duoplanet 的《It's Time For Duolingo To DITCH The Heart System》认为「如果进步依赖于犯错……红心机制如何可能有帮助？它制造了一种恐惧氛围」。https://duoplanet.com/its-time-for-duolingo-to-ditch-the-heart-system
  - XP / streak 的批评：媒体与研究性讨论普遍指出「围绕 points 与 streaks 的强烈聚焦会推动用户**优先游戏指标而非真正学会**，很多人连续打卡数月却几乎不会说」。可查的公开讨论举例：YouTube 调查报道《AI Fatigue: Why Millions Are Deleting Duolingo》（2025-11-10）https://www.youtube.com/watch?v=CEue-CvyRoA 。**说明：这一类「streak 有害」的量化结论未查到权威同行评审出处，本条只作为「存在广泛批评」的定性记录，不引用任何具体数字。**
- **我们对这条要吸收的判断**：把「错误」当作**信息**而不是**惩罚资源**；如果要做体力/次数限制，**复习与纠错必须免费**（Duolingo 自己也这么做：课末复习不耗能）；**不要用单一 streak 计数器代表学习成果**（它衡量的是「有没有打开 App」）。

**4) 对初学者友好的设计（可复用清单）**
- 每个 unit 有 guidebook（Tips 集中存放），避免知识点散落。
- 圆点不写字，点开才显示「你将学什么」，unit 头部用**行为动词**描述目标（官方把 "City 3" 改成 "get directions"、"Travel 2" 改成 "discuss destinations"）。
- 完成过的圆点可以随时点回去复习；Stories 可以重看。
- Legendary 挑战从「单技能」上移到「整 unit」，减少碎片化刷分。
- 角色配音/动画被官方明确当作**听力材料**而非纯装饰（「our characters' voices are featured in your speaking and listening exercises」）。
- 出处：官方博客（同 A1-1）。

**5) 已知问题（除上面已列的）**
- 进度迁移不完美：官方 FAQ 承认「若某些 skill level 未完成，可能会把你安排在路径更早的位置」；Legendary 用「>50% 的 level 属于已 Legendary 技能则整个 unit 记 Legendary」的近似规则。
- 课程内容大改版会破坏学习者连续感：Android Authority 评论《Duolingo is breaking users' language courses, and it's exactly why I quit》指出「课程更新后，当前 lesson 突然出现全新词汇，App 却把它当作已学，要求你直接翻译，错了还要扣分」。https://www.androidauthority.com/duolingo-broken-updated-courses-why-i-quit-3686405
- 设计视角复盘（含「用户抱怨丢失进度、Legendary 被重置」「不能跳到自己已会的部分」）：https://medium.com/@farahhariri/duolingos-app-update-2022-breaking-boundaries-f4abbde429d0

**6) 我们可吸收 / 不适合吸收**

| 可吸收 | 不适合 |
|---|---|
| 路径 = 主视图，但**每一格都标注「这格在练什么」**（Duolingo 恰恰因为不标字被吐槽，我们要反过来做） | 完全取消选择权。Duolingo 能做单线是因为它课程线性；我们的树有**必修/推荐前置 + 两条路线**，强行单线会毁掉「技能树」这个核心卖点 |
| 复习排进主路径、复习也算进度（不显示「你在倒退」） | 用「裂开的技能」这种**破损隐喻**表达遗忘（负罪感驱动） |
| 交错排课（不同技能的 level 混排）作为**可选的「智能路径」模式** | 用 streak / XP 作为主要成就指标（易被刷、与「真的学会」脱钩） |
| 错误不消耗资源、复习免费 | 体力/红心式资源限制（对零基础最劝退，官方自己承认初学者 2 倍耗尽率） |
| unit 级「通关挑战」（Legendary 上移），对应我们的「每技能 1 道综合练习题」放成**单元 boss** | 内容大改版时不给「已学」映射（会造成「被当成已会却考你」） |

**7) 未查到**
- Duolingo 官方对「移除 cracked skills」的**独立专门说明文章/数据**：未查到。目前唯一官方表述是 A1-1 博客里那一句括号说明。
- 「streak 对学习效果的量化影响」的权威研究：未查到（见上）。

---

### A2. Brilliant.org

**1) 核心玩法循环**

官方自述（About 页，2025 年抓取）：
- 「**We don't teach how to do something before asking questions. Instead, we pretest on the material, letting the learner try to find a solution before learning the procedure. Based on our testing to date, we believe this is the optimal approach.**」——即**先让学习者动手猜/试，再给概念**（pretesting + 生成效应）。
- 「Each lesson focuses on a **single concept** and has a mix of **direct instruction and blocked problem solving**（同类题集中练）。」
- 「We first build intuition with **visual explanations, hands-on manipulation, and concrete computation**. We start with the **simplest version** of an idea, **minimizing cognitive load**. Each interactive problem gives **instant, custom feedback** based on your answer.」
- 「As concepts build on one another, we challenge learners to try **more advanced computations and combine ideas**.」
- 出处：https://brilliant.org/about

**2) 如何解锁 / 进阶**

- 官方：「Learners progress through **levels of progressively more difficult problem solving** in a topic. The leveling system **intentionally displays a more reductive view of concept connections and prerequisites than the underlying reality**. It is focused on providing learners with **clear and satisfying milestones** to work toward.」
  - **这一句极其关键**：Brilliant 明说它把「前置关系」画得**比真实更简单**，目的是给清晰里程碑。→ 我们的 192 节点 + 必修/推荐前置恰恰相反（要真实），所以**必须做「简化视图 / 真实视图」双视图切换**。
- XP、pass/fail 反馈与路由也被游戏化；官方称正在测试「延长单次学习时长」的机制。
- 出处：https://brilliant.org/about

**3) 如何复习**

- 官方：「Every lesson has associated **practice sets**……The frequency, timing, and composition of practice sets are an area of **active experimentation**, to maximize effective **retrieval and automaticity**.」
- 「In practice sets, **the scaffolding falls away** — you're being tested on your independent ability……so there are **no more visual aids or hints**.」→ 明确的**脚手架渐隐（fading）**。
- 「We predict **the optimal next problem X** to ask, so that you are adequately prepared to answer a future question Y.」→ 用模型选下一题。
- 「we test **spaced repetition (especially in weak areas)**, **mixing practice problems from different concepts**（so that the learner must identify what approach to use……rather than just applying the same procedure to every problem）, determining level of **effective automaticity (fast solving speed with no mistakes)**, and optimal length and difficulty per set.」
- 「**Review sets** that combine problems from preceding lessons are currently being rolled out on a course-by-course basis.」→ 即复习集是**后来才补的**，不是一开始就有。
- 出处：https://brilliant.org/about

**4) 对初学者友好的设计**
- 起点门槛极低：官方 FAQ「只要你 Four operations 熟练就可以开始」（https://brilliant.org/help/using-brilliant/who-is-brilliant-for ）。
- 「Koji」AI 导师嵌进**题目内部**：讲解、分步推理、在 interactive 上叠加图形与提示；「never, ever just hands you the answer」；「asks instead of tells」；「Good tutoring **makes itself unnecessary**」。https://brilliant.org/about
- 官方明确「Gamification 层只是动机脚手架」：「We **avoid packing too many game incentives** into the product to keep the focus on the learning content……These include **Streaks and Leagues**。」→ 少而精的元游戏，而不是满屏奖励。
- 官方明确「内容本身要好到『你会自愿每天学』」：「We've grown on the strength of being **so good that you'll voluntarily learn each day**. This is very hard to do for math.」
- 出处：https://brilliant.org/about

**5) 已知问题 / 被批评之处**
- **付费墙**：Brilliant 是订阅制，免费内容有限（第三方评测多次提到，如 https://learnopoly.com/brilliant-org-review ）。这是「可持续性 vs 普惠」的取舍，不是学习效果问题。
- **「看起来懂了」的风险**：因为题目给即时、定制的分支反馈，学习者可能靠**试错 + 反馈排除**过关而不建立内部模型；官方对策就是在 practice set 里**撤掉脚手架**（见上）。→ 这一条是逻辑推论，**不是**查到的批评文章，标注为「我们自己的判断」。
- 官方关于「leveling 视图比真实前置关系更简化」的自述，本身就是一个**已被承认的简化**（见 A2-2）。
- **未查到**：Brilliant 第三方独立的学习效果 RCT/同行评审研究（官方称获 WASC 认证，但那只是认证不是效果研究）。https://brilliant.org/about

**6) 可吸收 / 不适合**

| 可吸收 | 不适合 |
|---|---|
| **先抛问题、再讲概念**（pretest），把「先动手」做成每个知识项的第一步 | 「把前置关系画得比真实更简单」——我们的卖点就是**真实前置图** |
| **同一知识项内先给可视化/可拖拽的直觉，再给符号化计算** | 复习集「后补」的做法（我们应该一开始就把复习集当一等公民） |
| **脚手架渐隐**：第 1 题给提示，第 n 题撤掉全部提示 | 无提示的硬考（对零基础太硬，Duolingo 的教训） |
| 练习集里**混不同概念的题**，逼学习者「先判断用哪个方法」 | 只做「同类题集中练」（blocked practice），会形成「看题型套公式」 |
| 「自动性」作为掌握判据之一：**又快又不出错**（不是「做过一次」） | 用单一「完成/未完成」二元状态 |
| 元游戏**少而精**（streak + league 级别），不堆满屏奖励 | 满屏 XP 数字、每日任务、多币种 |

**7) 未查到**
- Brilliant 官方发布的**学习效果数据**（如「学完 X 课程的人提升 Y%」）：未查到具体数字。
- 官方对「pretesting 为什么有效」的**独立长文**：未查到（只有 About 页那句结论 + blog 的零散表述，如 https://blog.brilliant.org/thinking-in-code 「we learn by struggling」）。

---

### A3. Khan Academy

**1) 掌握度等级（官方定义）**

- 官方帮助中心《What are Course and Unit Mastery?》：等级为 **Not started → Attempted → Familiar → Proficient → Mastered**，并明确「**Your skill level can move up or down** based on your performance as you continue practicing.」（**可升可降**，这是关键设计）「Proficient 和 Mastered 才计入 Course / Unit Mastery 百分比」。
  - https://support.khanacademy.org/hc/en-us/articles/115002552631-What-are-Course-and-Unit-Mastery
- 官方教学视频（Khan for Educators）给出的**量化阈值**：Attempted = 试过但**正确率低于 70%**；Familiar = **70%–99%**；Proficient = 在**单个技能练习中 100% 正确**；Mastered = 在**更严格的混合技能测评**中成功应用。
  - https://www.khanacademy.org/khan-for-educators/k4e-us-demo/xb78db74671c953a7:get-to-know-khan-academy/xb78db74671c953a7:find-the-right-fit/v/mastery-learning-vs-traditional-grades
  - 注意：阈值来自**视频讲解**而非帮助文档正文；帮助文档只给语义描述。引用时建议说「官方教学视频给出 70%/100% 阈值」。

**2) mastery learning 的设计逻辑与官方证据**

- 定义（官方博文，作者为 Khan Academy Efficacy Research Manager Bogdan Yamkovenko，2023-09-25）：「Khan Academy is designed based on principles of **mastery learning**, which encourages learners to engage in instruction and practice **until they reach high levels of success** …… **before moving on to the next skill**.」
- **为什么用 "skills to proficient" 当指标**：他们用全国常模的 **MAP Growth** 数学测评做外部效标，发现「**达到 proficient/mastered 的技能比例**与 MAP Growth 分数相关，且**与总技能数、总使用时长无关**」。这叫 convergent validity。
- **广度 vs 深度**：官方结论「**it is better to focus on fewer skills but reach at least proficient levels than to work on multiple skills but only reach familiar**」；并给出可操作建议：「典型 30 分钟会话里，一个学习者能做 2 个练习并把 2 个技能升到 proficient」；「如果第一次没到 proficient，建议**再试一次**同一技能而不是往下走」。
- 理论依据引用：Block, J. H., & Burns, R. B. (1976). *Mastery learning*. Review of Research in Education, 4, 3–49.
- 出处：https://blog.khanacademy.org/why-khan-academy-will-be-using-skills-to-proficient-to-measure-learning-outcomes
- 相关的效果宣称（同一机构的宣传口径）：「把 60 个技能带到 proficient，一年内可提升约 30 个百分点」（来自官方视频《Mastery learning vs traditional grades》https://www.youtube.com/watch?v=SRFpPSFM980 ）。**注意：这是 Khan 自己的口径，未查到独立复现。**

**3) 如何「复习」**

- 因为等级**会掉**（官方帮助文档原文 "can move up or down"），复习不是独立按钮，而是**等级系统的内生压力**；Mastered 必须在**混合技能测评**里达成，这本身就是交错练习。
- **未查到**：Khan Academy 是否使用显式间隔重复排程（类似 FSRS/SM-2 的到期队列）的官方说明。查到的是「mastery 会随时间/表现下降」这种行为层描述，没有算法层文档。

**4) 对初学者友好的设计**
- 免费、非营利（官方 About：https://www.khanacademy.org/about ）。
- 一个技能可反复尝试，等级是**进度信号而非永久标签**（官方视频原话：「which function as signals of progress, **not permanent labels**」）。
- 大量 hint / 视频 / 分步提示（练习内可求助），与 Brilliant 的「practice set 撤掉提示」形成对照。

**5) 已知问题 / 批评**
- 「mastery 会掉」对部分学习者是**负反馈**：辛苦刷到 Mastered 后掉回 Proficient 会打击积极性（这是 mastery 系统的通病，Duolingo 的 cracked skill 被骂也是同一心理机制）。
- 内容以「视频讲授 + 练习」为主，**动手/交互弱**；Brilliant 官方对比页即以此作为差异点（https://brilliant.org/resources/choosing-brilliant/brilliant-vs-khan-academy ）。**注意：这是竞品说法，不是中立评测。**
- **未查到**：独立的、针对 Khan Academy 掌握度等级的负面研究结论。

**6) 可吸收 / 不适合**

| 可吸收 | 不适合 |
|---|---|
| **5 档状态机**（Not started / Attempted / Familiar / Proficient / Mastered），其中「Proficient = 单技能满分」「Mastered = 混合测评通过」 | 让状态**悄悄掉级**而不提示原因 |
| 「**Proficient 才计入进度**」→ 进度条分母只算「已掌握」，不算「已浏览」 | 把「看过/做过」算成「学会」 |
| 「Mastered 必须跨技能混合考」——正好对应我们的「每技能 1 道综合练习题」 | 用「完成课时数」当唯一指标 |
| 官方那条实证结论：**少而精 > 多而浅**（可作为「推荐前置」提示语的依据） | 纯视频 + 刷题（交互太薄） |
| 掉级时**给出「为什么掉 / 怎么补」的具体入口**（Duolingo 的失败点） | 把掉级做成无声的、只改颜色的变化 |

**7) 未查到**
- Khan Academy 掌握度阈值的**官方文档正文**（只有视频里有 70%/100%）。
- Khan Academy 内部是否用 FSRS/间隔排程的官方技术说明。

---

### A4. nandgame.com 与 Turing Complete（Steam）

#### A4-1. nandgame.com

**1) 核心玩法循环**
- 官方站点 meta description：「An educational puzzle game. Solve a series of tasks where you build **increasingly powerful components**. Starts with the simplest logical components and **ends up with a programmable computer**.」（站点为 JS 应用，正文抓不到，此段为 HTML meta 原文，本站已用 curl 抓取 `<meta name="description">` 验证）
- 关卡结构（第三方逐关攻略仓库，含全部关卡截图/解法）：「The Nand Game is an educational puzzle game where you can solve a series of tasks by building increasingly powerful components. **Starting with a single component, the NAND gate, you will build a simple computer.**」https://github.com/timlg07/NandGame-Solutions
- 通关录像式说明（视频转录）：「The game consists of a series of levels……We're in **logic gates** to start. In each level, you are tasked with **building a component that behaves according to a specification. This component can be used as a building block for the next level.**」https://www.youtube.com/watch?v=ER-3gLl8A-Q （2025-08-11）
- 关卡层级（从攻略仓库目录可见的推进顺序）：Logic gates → Arithmetic（half/full adder、ALU）→ Memory（SR latch、DFF、Register、RAM）→ Processor → 汇编/机器码。
- **关键机制**：你的产出**立刻成为下一关的可用零件**——「造出来的东西变成工具箱里的工具」。这是整个游戏的设计灵魂。

**2) 如何解锁/进阶**
- 严格线性：完成第 N 关才能在第 N+1 关使用新零件。

**3) 如何复习**
- **未查到**任何复习/间隔机制（无账号、无到期队列）。设计上是「一次性通关」。
- 但隐含复习：后面的关卡**不得不复用**前面的零件（如 ALU 关要用全加器），**复用即复习**。

**4) 对初学者友好的设计**
- 起点极简：只有一个 NAND 门，没有语法、没有环境配置。
- 每关有规格说明（spec），把「要做什么」与「怎么做」分离。
- 有社区解法仓库、视频、以及 r/WebGames / Lobsters 上的讨论（https://lobste.rs/s/fqeiw5/nandgame_build_computer_from_scratch ，2018-08-19），可供卡关者参考。

**5) 已知问题**
- Lobsters 讨论中有玩家报告**某关「impossible」**（原话 "I think condition is impossible! I did every other level though. I emailed the author"）——说明规格表述/判定边界可能不清。https://lobste.rs/s/fqeiw5/nandgame_build_computer_from_scratch
- 无进度云同步、无复习、无提示系统（超出社区攻略就卡死）。
- **未查到**官方自述的设计文档或失败率数据。

**6) 可吸收 / 不适合**
- 可吸收：**「你造的东西变成下一关的工具」**——这对我们「192 技能树」是极强的隐喻：技能不是打勾，是**变成可用工具**（例如「学会递归」后，后续题目的解法栏里出现「递归」这个积木）。**这是本报告最重要的一条可吸收机制。**
- 可吸收：spec 驱动（给行为规范而非给做法），天然支持一题多解 + 自动判分。
- 不适合：完全无复习、无提示；对零基础而言，纯 NAND 起步的门槛其实很高（要先接受二进制/布尔代数）。

#### A4-2. Turing Complete（Steam，LevelHead 开发/发行）

- 官方站点自述的四阶段教学结构（原文）：
  1. **LOGIC GATES**：「Given only a **NAND gate** you create the rest.」
  2. **COMPONENTS**：「Building on logic gates and introducing **memory**, more complex constructions are possible.」
  3. **ARCHITECTURE**：「Assemble your components into real computers. **Turing complete** computers are the gold standard……」
  4. **汇编**：「Computers are programmed with binary codes. **Create assembly instructions** to simplify this and solve **programming puzzles on your own hardware**.」
  - https://turingcomplete.game
- Steam 商店页：https://store.steampowered.com/app/1444480/Turing_Complete/
- **与 nandgame 的关键差异（这是我们最该抄的）**：Turing Complete 让你**自己设计指令集**，然后**在你亲手造的 CPU 上做编程谜题**。教学闭环是「硬件 → 指令集 → 程序」，而不是「硬件 → 硬件」。
- **已知问题（社区一手反馈）**：
  - Steam 高赞评测里被反复提到的是**难度陡增**：有玩家把体验总结成一张「流程表」，其中「Reach the programming levels → Everything **stops** clicking → Brute force it → Works at first → **Spend seven hours on one of the levels**（not joking）」。https://steamcommunity.com/app/1444480/reviews
  - Hacker News 讨论（2024-01-09）：一位家长说 14 岁儿子通关后在游戏教的伪汇编里写了「走迷宫」程序，评价极高（"This game ROCKS"），但**主要抱怨是「没有哪怕稍微类似的东西」**——即品类稀缺。https://news.ycombinator.com/item?id=38925307
  - 同一 HN 帖与 Steam 评测提到「元件布局/连线」在大设计里会变成**体力活与屎山**（红元件锁定、空间不够、mess 会跨关卡保留）。
  - 独立评测（Puzzlebyrinth，2021-10-02，40 小时通关，8.8/10，难度 4/5）：https://puzzlebyrinth.com/en/reviews/turing-complete
- **未查到**：官方公布的关卡数、通关率、学习效果研究。

**A4 小结：可吸收 / 不适合**

| 可吸收 | 不适合 |
|---|---|
| **产物即工具**（造出的组件进入下一关工具箱），技能树节点 = 可用积木 | 纯线性无复习的课程结构 |
| **spec 驱动 + 自动判分**（给行为规范，允许多解） | 让玩家做「连线/摆元件」的体力活（我们的抽象层应更高，如拖逻辑块或写伪代码） |
| **闭环到「用自己造的东西写程序」**（硬件→指令集→程序），对应我们的「知识项→技能→综合练习」 | 难度曲线陡增（Turing Complete 的「七小时一关」是警示，不是目标） |
| 四阶段命名（Gates → Components → Architecture → 汇编）可类比为我们的「概念 → 组件 → 系统 → 应用」 | 无提示系统（对零基础必须给分层提示） |

---

### A5. Human Resource Machine / 7 Billion Humans / Zachtronics（TIS-100、Exapunks）

#### A5-1. Human Resource Machine（Tomorrow Corporation，2015-10-15 发售）

**1) 核心玩法循环（官方原文）**
- 官方页面：「**Human Resource Machine is a puzzle game.** In each level, your boss gives you a job. Automate it by programming your little office worker! **If you succeed, you'll be promoted up to the next level for another year of work** in the vast office building.」
- 教学递进（官方，非常关键的量化设计）：「**You start the game with just 2 commands**, and gradually earn more as you're promoted. **The entire language contains only 11 total commands** — but they're enough to simulate almost any computer algorithm in the world!」
- 世界观即计算机（官方）：「**Your office is a simple computer.** You have an inbox and an outbox（inputs and outputs）, and **a few slots on the floor to store stuff for later (memory)**. Your little office worker can **hold exactly one box in his or her hands at a time (like an accumulator)**.」官方自评架构：「**Harvard Architecture with a single accumulator**」。
- 面向纯新手的话术（官方，值得抄的文案策略）：「**Don't worry if you've never programmed before — programming is just puzzle solving.** If you strip away all the 1's and 0's and scary squiggly brackets, programming is actually simple, logical, beautiful……」
- 出处：https://tomorrowcorporation.com/humanresourcemachine

**2) 如何解锁 / 进阶**
- 关卡线性晋升（promotion = level），指令集**随关卡逐步解锁**（2 → 11 条）。
- **额外的可选难度层**：官方「Each level comes with **Optimization Challenges** — difficult (**and optional**) challenges that test how well your solution optimizes for **program size and execution speed**.」
  - → **这是双层目标设计**：过关（必须） / 优化（可选、竞争性）。对我们「每技能 4–9 个知识项 + 1 道综合练习」的直接映射：知识项 = 过关线，综合练习 = 优化线。

**3) 如何复习**
- **未查到**任何间隔重复/复习机制。设计上是通关即止。
- 隐含复习靠「后续关卡必须用到前面指令」+「优化挑战要求你回头重写旧解」。

**4) 对初学者友好的设计**
- 只有 11 条指令、无语法错误、无环境配置，全部 drag & drop。
- 老板的台词用「clear to understand but still has 'a little bit of sassiness'」的语言一致贯穿全游戏（Wikipedia 对开发的记述），即**叙事语气本身就是降低门槛的手段**。
- Boing Boing 的 Laura Hudson 评价：游戏对编程的处理与画风「helps to **avoid scaring off would-be players**」，且部分谜题「designed to help make the player **feel smart** after completing them」。

**5) 已知问题 / 被批评之处（这是本节最有价值的部分）**
- **后半段缺乏讲解**：PC Gamer 的 Angus Morrison 认为关卡推进与概念教学都很好，但「**would have appreciated more instruction on some of the advanced approaches**」；Destructoid 的 Laura Kate Dale 同样认为「the lack of **instructional material for advanced concepts in the second half** of the game」是问题，并进一步批评「the game **didn't fully commit to either** being a good instructional game for new programmers **or** a difficult challenge for advanced ones」。
- 剧情/设定被浪费：Morrison 认为设定与故事「under utilized」。
- 以上均引自 Wikipedia 的 Reception 段（聚合自 PC Gamer / Destructoid / Boing Boing 原评测）：https://en.wikipedia.org/wiki/Human_Resource_Machine
- **对我们的直接警示**：**难度爬到中后段时，如果只加难度不加讲解，玩家就会从「学习者」变成「猜谜者」**，而「既不彻底教学、也不彻底挑战」是这类游戏最常见的失败模式。我们的 192 技能树后半段（操作系统、深度学习）必须**显式补讲解层**，不能靠「更难」来代替「讲清」。

**6) 续作 7 Billion Humans**
- 2018-01 公布，**2018-08-23 发售**；「based on the **same visual programming principles** as Human Resource Machine, but now sees the player **controlling multiple human agents**」。
- 出处：Wikipedia 同页（Sequel 段）。
- → 从「单线程/单工人」到「多工人并行」正是 HRM → 并发的自然延伸，与我们「操作系统」路线里的并发主题高度对应。

#### A5-2. Zachtronics：TIS-100 / EXAPUNKS / Shenzhen I/O / Opus Magnum

**1) 核心玩法循环**
- TIS-100（2015-07 发售，Win/macOS/Linux；2016-01 iPad 版）：「the player develop **mock assembly language code** to perform certain tasks on a fictional, virtualized **1970s computer that has been corrupted**」。https://en.wikipedia.org/wiki/TIS-100
- EXAPUNKS（2018）：「a programming puzzle game about **writing computer viruses** in a cyberpunk reimagining of 1997. Players will learn to program using the included **printable "hacking zine" TRASH WORLD NEWS** and hack a variety of simulated networks including banks, universities, factories, TV stations, highway signs, and game consoles.」https://www.zachtronics.com/zachademics
- 官方对全系列的定性：「Like all of our games, it **reinforces iterative problem solving and the design feedback loop**」（原文出现在 Infinifactory 条下，但作者说 "all of our games"）。

**2) 解锁 / 进阶：**关卡解锁 + **三/多指标排行榜式优化**。EXAPUNKS 的玩家总结（Steam 高赞评测）：「there are lots of **simply-stated levels with many ways to approach**, there are **three metrics** to try to optimize for, and **the debugging is very visual**」。https://steamcommunity.com/app/716490/reviews
- → 关键词：**题面极简 + 多解 + 多指标优化 + 可视化调试**。这四点可以直接搬到我们的「综合练习题」。

**3) 复习：**未查到任何间隔重复机制。

**4) 对初学者友好（以及官方的诚实警告）**
- 官方在教育页 `Zachademics` 上明确写：「these games are **probably not the kind of thing you can sit a student in front of without some amount of introduction and scaffolding from a real human being**. This isn't to say you need to have beaten the games (most of our players don't), but you should at least understand how to play them yourself before introducing them to students.」
  - **这是一句罕见的、来自开发者的自我否定式诚实评价**，直接反驳「把游戏丢给学生就能学」的幻想。
- 官方给每款游戏标了教育难度（DIFFICULTY，满分 5）：Opus Magnum **2/5**、Infinifactory **2/5**、EXAPUNKS **2/5**、TIS-100 **2/5**（本节抓到页面可见的四条）。
- 官方提供**公立学校免费授权**（公立学校与非营利机构免费；私立/营利学校 25%–75% 折扣；不覆盖家庭学校）——这是商业模式层面可参考的「教育普惠」策略。
- 内容分级提示：所有有分级的作品都是 **ESRB T**，含脏话与暴力/性/酒精/毒品的文字提及（官方自述）。
- 出处：https://www.zachtronics.com/zachademics

**5) 已知问题 / 被批评之处**
- **初次通关难度 vs 优化难度错位**：Hacker News 讨论里有玩家对比 Opus Magnum 与 TIS-100：「Opus Magnum……**solving the levels is easy, but optimizing is challenging and rewarding**. TIS-100 on the other hand has a **higher difficulty to initially solve** the puzzles and **optimization becomes a little bit of a guessing game**. Also **having only 3 saved solutions per level** makes it hard to optimize without losing [them]」。https://news.ycombinator.com/item?id=21176831
  - → 设计教训：**「过关」和「优化」应该是两条难度曲线**，不能都陡；存档位太少会惩罚实验（我们要允许无限版本历史）。
- 玩家对 EXAPUNKS 的具体抱怨（Steam 高赞评测中提到的「把银行 ATM 清空」关）：「you're only allowed to empty **one bill at a time** from a given ATM and fail if you request some [more]」——即**规则约束过于刁钻**会让人卡在理解题意而非算法上。
- TIS-100 的定位：据 scifiempire.net 转述「**Zachtronics has labeled TIS-100 as the 'assembly game no one asked for'**」（https://scifiempire.net/wordpress/programming-games-what-are-they-are-they-any-fun ，2019-06-05；**未在 Zachtronics 官方页面核实到原话**）——即它是「为极客做的」，不是为大众做的，我们不该照搬其门槛。

**6) 可吸收 / 不适合**

| 可吸收 | 不适合 |
|---|---|
| **极小的指令集**（HRM 的 11 条）——我们的「程序设计基础」第一屏也应该只有 3–5 个积木 | 后半段无讲解（HRM 被两家媒体同时批评） |
| **双层目标**：过关（必做）+ 优化（可选，多指标） | 多指标排行榜导致「刷分焦虑」/只优化不学 |
| **题面极简 + 多解 + 可视化调试**（Zachtronics 公式） | 只给 3 个存档位、不允许试错回滚 |
| **产品内的「手册」**（EXAPUNKS 的 TRASH WORLD NEWS zine）——教程可以是叙事道具，不一定是一段弹窗 | 把「更难」当成「更教学」 |
| 官方那句「**不能不给脚手架就把学生丢进去**」应写进我们的设计前提 | 照搬 Zachtronics 的门槛（它是给极客做的） |
| 多智能体并行（7 Billion Humans）= 并发的天然入口 | 刁钻的规则约束（把难度放在「读懂题意」而非「想通原理」） |

---

### A6. The Deadlock Empire（deadlockempire.github.io）

**1) 核心玩法循环（角色反转是本作唯一也是最强的设计）**
- 官方站点：「**You take the role of the Scheduler — and a cunning one! Your objective is to exploit flaws in the programs to make them crash or otherwise malfunction.**」https://deadlockempire.github.io
- 叙事包装（Reddit r/programming 标题即官方宣传语）：「**Slay dragons, learn concurrency!** Play the cunning Scheduler, **exploit flawed programs and defeat the armies of the Parallel Wizard**.」https://www.reddit.com/r/programming/comments/44wfww/the_deadlock_empire_slay_dragons_learn_concurrency
- 关卡规模：Hackathon 提交页（2016-01-31）自述「We have **a campaign of 16 concurrency** [challenges]」。https://devpost.com/software/the-deadlock-empire （注：这是开发期数字，现站可能已扩充；**未查到**官网给出的当前关卡数）
- 玩法细节（第三方教学博客）：「The core idea of this game is for you to act as an **evil scheduler**. Your goal is to guide the execution of threads into a bad state, such as a **deadlock** or two [threads racing]」。https://aoli.al/blogs/deadlock-empire

**2) 如何解锁 / 进阶：**关卡线性推进（每关一个「两线程 + 一段有 bug 的共享状态代码」），你必须**手动决定每一次线程切换的时机**，直到构造出违反不变式的交错。

**3) 如何复习：**未查到任何复习机制。

**4) 对初学者友好**
- 没有真并发环境、不需要写代码就能理解「交错执行」——把不可见的调度器**变成一个可操作的角色**。
- 反直觉但极有效的动机设计：**你的目标是让程序出错**。学习者从「怕 bug」变成「主动找 bug」，这正是「理解并发为什么难」的最短路径。
- 学术旁证：Inggs, Gadd & Giffard, *Learning Concurrency Concepts while Playing Games*（CSEDU 2017, pp. 597–602, DOI 10.5220/0006374705970602）在 Related Work 中写：「Deadlock Empire is the only game-oriented application for teaching concurrency concepts that we could find available to play online (Hudecek and Pokorny, 2016). The Deadlock Empire requires a user to complete a sequence of tutorials/challenges; in each the player is presented with **two threads** and the objective of the player is to **schedule the instructions**……」，并把「需要编程语言知识」列为它的局限。PDF：https://www.scitepress.org/papers/2017/63747/63747.pdf
- 同一论文的立场与本作互补：他们主张用**可视化积木语法**做并发游戏，并认为「a child of eight or nine years old, mature enough to think abstractly」就可能学会并发概念——即并发**不必**等到大学。

**5) 已知问题 / 被批评之处**
- 论文点出的局限：**需要读懂 C# 风格代码**才能玩（"those that were found available online require programming language knowledge"）。对零基础是硬门槛。
- 无提示、无复习、无进度持久化（**未查到**账号系统）。
- 只覆盖「坏交错」的识别，**不训练「如何写出正确的同步」**——它是诊断训练，不是建构训练。

**6) 可吸收 / 不适合**

| 可吸收 | 不适合 |
|---|---|
| **角色反转**：让玩家扮演「调度器 / 攻击者 / 编译器 / GC」，把不可见机制变成可操作对象 | 需要读懂真实语言代码才能开始 |
| 「**让程序出错**」作为正向任务（把 bug 从惩罚变成目标） | 只训练「找出错误」，不训练「构造正确」 |
| 每个概念一个**极小可交互模型**（2 线程 + 1 个共享变量） | 无提示 / 无复习 |
| 叙事包装（Parallel Wizard / 恶龙）降低枯燥感 | 关卡数量少、玩完即止 |

**→ 对我们「操作系统」路线的具体建议**：调度器、页表替换（LRU/Clock）、文件系统崩溃一致性、生产者-消费者，都可以用「**你来当那个机制**」的关卡形态实现，比「读代码 + 选择题」有效得多。

---

### A7. TensorFlow Playground / Distill / CNN Explainer（神经网络交互可视化）

#### A7-1. TensorFlow Playground（playground.tensorflow.org）

- 官方页面口号（极强的「安全失败」文案）：「**Tinker With a Neural Network Right Here in Your Browser. Don't Worry, You Can't Break It.**」——即**零成本试错**被写在第一行。
  - 出处：https://playground.tensorflow.org （页面 Credits 段：created by **Daniel Smilkov and Shan Carter**；并注明是 "a continuation of many people's previous work — most notably **Andrej Karpathy's convnet.js** demo and **Chris Olah's articles** about neural networks"）
- 学术版本：Smilkov, Carter, Sculley, Viegas, Wattenberg, *Direct-Manipulation Visualization of Deep Networks*，**ICML 2016 Workshop on Visualization for Deep Learning**；正文标注 2016-05-17，arXiv 版本 2017-08-12 提交。
  - arXiv：https://arxiv.org/abs/1708.03788
  - 摘要要点（原文）：「We describe TensorFlow Playground, an interactive, open sourced visualization that allows users to experiment via **direct manipulation rather than coding**」。
- 教学用途的第三方确认：AI4K12（CS 教育倡议）把它列为「Engaging Learning Demos」，标注适用年级 11–12、Apache 开源许可、描述为「In-browser implementation of **backpropagation learning with excellent visualization**. Network is **reconfigurable**（units/layers/activation……）」。https://ai4k12.org/tensorflow-playground
- Google Cloud 官方博客的用法示范（2018-06-20）：「an awesome tool to help you grasp the idea of neural networks **without any hard math**……lets you play with a **real neural network running in your browser** and click buttons and tweak parameters to see how it works.」https://cloud.google.com/blog/products/ai-machine-learning/understanding-neural-networks-with-tensorflow-playground
- **未查到**：官方发布日期的权威一手出处。有第三方博客称「shipped in April 2016」（https://ai.growthgear.com.au/deep-learning/tensorflow-playground-guide ），此日期我**未能用一手来源核实**，故不作为结论。

#### A7-2. Distill（distill.pub）

- 定位（官方 About）：「**Distill is dedicated to making machine learning clear and dynamic**……**New notations, visualizations, and mental models can deepen our understanding.** By nurturing the development of such new ways of thinking, Distill will enable new discoveries.」https://distill.pub/about
- 它是**同行评审**期刊（站点标注 "Peer-reviewed"），ISSN **2476-0757**，2016 年由 Google 与 OpenAI、DeepMind、YC Research 等合作发起。Google Research 官方博客公告：https://research.google/blog/distill-supporting-clarity-in-machine-learning
- 代表作（可直接作为我们「深度学习」路线的视觉参考）：
  - 《Feature Visualization》，Olah, Mordvintsev, Schubert，**2017**，DOI 10.23915/distill.00007 — https://distill.pub/2017/feature-visualization
  - 《The Building Blocks of Interpretability》，Olah 等，**2018**，DOI 10.23915/distill.00010 — https://distill.pub/2018/building-blocks
- 可吸收点：**「文章本身就是可交互的」**——滑块、可点选的图、可运行的小模型嵌在正文里，而不是「看视频 + 做练习」两段分离。

#### A7-3. CNN Explainer

- 官方：「An **interactive visualization system** designed to help **non-experts** learn about Convolutional Neural Networks (CNNs).」https://poloclub.github.io/cnn-explainer
- 论文：*CNN Explainer: Learning Convolutional Neural Networks with Interactive Visualization*，**IEEE TVCG 2020**，DOI **10.1109/TVCG.2020.3030418**。代码：https://github.com/poloclub/cnn-explainer
- 佐治亚理工官方报道（2020-10-30）：「Created by **Georgia Tech and Oregon State University** researchers over the course of a year……**uniquely developed for deep learning beginners**」，并称它在 GitHub/Twitter/LinkedIn 上「viral」。https://www.cc.gatech.edu/news/640835/why-new-deep-learning-visualization-going-viral
- 设计要点：把一个小 CNN 的**每一层、每一个卷积核、每一次激活**都做成可点开、可悬停的对象；输入图像上叠加卷积核窗口的滑动。

**A7 小结：可吸收 / 不适合**

| 可吸收 | 不适合 |
|---|---|
| **「Don't Worry, You Can't Break It」**——把「不可能搞坏」明说出来，降低零基础动手恐惧 | 只给「玩」，不给「解释为什么这样变化」 |
| **直接操纵**（拖层数/学习率/激活函数看决策边界变化），代替先讲公式 | 参数空间对完全新手过大（TF Playground 一屏有 6 类超参） |
| **可视化是正文**而不是配图（Distill 模式） | 纯阅读式长文（我们做游戏，需要任务驱动） |
| 对「不可见过程」（前向传播、梯度、卷积滑窗）做**逐帧可点查**（CNN Explainer） | 只展示结果不展示中间态 |
| 每个可视化配一个**「先预测、再看结果」**的小任务 | 让可视化变成「看动画」而不产生预测/检验 |

---

### A8. DragonBox（代数游戏）

**1) 核心玩法循环：把符号藏起来，再逐步换回来**
- 机制描述（Common Sense Media 评测，家长向、描述准确）：「exposes kids to basic algebra concepts by having them **drag and drop little "cards" onto two trays** on the screen. The goal is to **isolate the sparkling box by itself**, which is **analogous to solving for x**, but the algebraic concepts are presented in a way that makes them seem like **rules to a game rather than mathematical concepts**. **It isn't until later that numbers, letters, and mathematical symbols start to appear gradually.**」https://www.commonsensemedia.org/app-reviews/kahoot-algebra-by-dragonbox
- **官方 Google Play 描述（这就是「符号渐显」的官方表述）**：「By manipulating cards and trying to isolate the DragonBox on one side of the game board, the player gradually learns the operations required to isolate X……**Little by little, the cards are replaced with numbers and variables**……」https://play.google.com/store/apps/details?id=com.kahoot.algebra5
- 官方 App Store 文案：「**The game that secretly teaches algebra**」「Children **as young as five** can begin to grasp basic processes involved in solving linear equations……**without even realizing that they are learning**.」https://apps.apple.com/us/app/kahoot-algebra-by-dragonbox/id1550574178
- 时间线（官方 About 页）：DragonBox Algebra **2012** 首作；2013-04 出 **Algebra 12+**；2015-11 出 DragonBox Numbers；2015-12 起做 DragonBox School 课程；后并入 **Kahoot!**（现名 Kahoot! Algebra by DragonBox）。https://dragonbox.com/about/story-story ，https://dragonbox.com/about

**2) 如何解锁/进阶：**线性关卡，随关卡推进「卡面」逐步从图形替换为数字/字母/运算符（即**表征逐渐符号化**）。

**3) 如何复习：**未查到显式的间隔重复机制。

**4) 对初学者友好：**把「等式两边同操作」的约束**编码进可拖拽对象的物理直觉**里；无文字说明、无术语先行。

**5) 效果证据（本报告里最硬的一条教育实证）**
- **随机对照试验（RCT）**：Decker-Woodrow, Mason, Lee, Chan, Sales, Liu, Tu，*The Impacts of Three Educational Technologies on Algebraic Understanding in the Context of COVID-19*，**AERA Open, 2023-04-21**, 9:23328584231165919，DOI **10.1177/23328584231165919**，PMID 37123170。
  - 设计：**3,600+ 名七年级学生**，9 所实体校 + 1 所线上校，四条件随机分配（FH2T / **DragonBox 12+** / ASSISTments 即时反馈 / 无即时反馈的主动对照），**2020-09 至 2021-03 共 9 次 30 分钟**干预。
  - 结果（最终分析样本 N=1,850，HLM 分析）：「significantly higher posttest scores for students who used **From Here to There** and **DragonBox 12+** compared to the **Active Control** condition. **No significant difference** was found for the **Immediate Feedback** condition.」
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC10125888
  - **对 B 节的重要含义**：**「游戏化交互」有效，而「单纯的即时反馈」在同等条件下没有显著效果**。这条直接反驳「加了即时反馈就等于学会了」。
- **成本效益**（ERIC ED634628, 2023，同一 RCT 的成本效益分析，分析样本 1,850 人 / 9 校 / 34 教师 / 127 班）：FH2T **$39/学生、平均效应 0.135**；**DragonBox $55/学生、平均效应 0.269**。https://eric.ed.gov/?id=ED634628
  - **注意**：这是 ERIC 摘要给出的数字，我**未逐页核对全文表格**；引用时请标为「ERIC 摘要数据」。
- **效果并非一致**：ICLS 2023 短论文《How and for Whom Does DragonBox12+ Support Math [Learning]》写道：「Although developers of DragonBox claim that it may help students improve their algebraic performance (Siew et al., 2016), **the empirical findings are mixed (Long & Aleven, 2017)**. Recent analyses in a year-long randomized controlled trial (RCT) suggested that DragonBox positively impacted seventh graders' algebraic performance (Decker-Woodrow et al., in press). **However, it is unclear whether the positive effect was** [由游戏本身还是其他因素带来]……」https://repository.isls.org/bitstream/1/10000/1/ICLS2023_1749-1750.pdf
  - → 结论应写成：**有 RCT 支持「有效」，但效应量与机制仍有争议，且存在「对谁有效」的调节变量**。
- 厂方自宣（**不可当独立证据**）：「Students who played **1.5 hours** reached **92.9% mastery**……Nearly 93% of students were able to master concepts to solve linear equations in under two hours」，来自与华盛顿大学 Center for Game Science 合作的 Algebra Challenge。https://dragonbox.com/about/algebra-challenge

**6) 已知问题 / 被批评之处**
- 「藏符号」有**迁移风险**：玩家可能精通「推卡片」却不能迁移到纸笔方程。上述 ICLS 论文的「for whom」框架正指向这一点。（**这是我的推论**，论文本身讨论的是效应异质性。）
- 并入 Kahoot! 后转为**订阅制**（「an app included in a Kahoot! Kids subscription」），免费可玩范围受限。
- **未查到**官方公布的关卡数、留存率。

**7) 可吸收 / 不适合**

| 可吸收 | 不适合 |
|---|---|
| **先给「没有符号的规则」，再逐步把符号换回来**——这是把「极限/导数」这类抽象概念做成游戏的最强范式 | 永久停在「无符号」状态（会造成「会玩不会算」） |
| 把「等式两边同操作」这类**不变式**做成可拖拽对象的物理约束 | 靠「卡片可爱」掩饰机制单薄 |
| 每个概念设计一个**「显式符号切换时刻」**（第 3 关之后，图形换成 x） | 无文字说明 → 家长/教师无法接续课堂 |
| 「secretly teaches」的低门槛入口，但**出口必须显式考试**（我们的综合练习题就是那个出口） | 不做迁移检验（应把「同一概念换成纸笔形式」作为必考） |

---

### A9. 文明/策略游戏的科技树 + Learn Git Branching / Oh My Git!

#### A9-1. 策略游戏的科技树（tech tree）

- 定义（Wikipedia，准确可用）：「a technology/tech/research tree is a **hierarchical visual representation of the possible sequences of upgrades a player can unlock**……Because these trees are technically directed and acyclic, they can more accurately be described as a **directed acyclic graph (DAG)** of technologies.」
- 关键结构要素（可直接搬到我们的技能树）：
  - **tier（层级）**：「Each level is called a **tier** and is often used to describe the technological strength of a player.」
  - **起点稀疏**：「at the beginning……a player will start at **tier 1**, which offers **only a few options** for research.」
  - **前置关系**：「Each technology that a player researches will normally **open up one or more new options**, but may also, **depending on the computer game, close off the paths to other options**.」
  - **复杂度谱系**：「In the simplest cases (e.g. *Master of Orion*) there are several **completely separate research areas**……In more complex cases (e.g. ***Civilization***) **every technology above the starting level has more than one prerequisite** and one has to research most of the lower-level technologies in order to research any of the top-level technologies.」
  - **规模参照**：「Major 4X games like Civilization and Master of Orion have a much larger technology tree……as an extreme example, **Space Empires III has over 200 technologies**.」→ **我们的 192 个技能正好落在「大型 4X 科技树」量级**：这个规模玩家能接受，但必须靠 tier 与分支来管理。
  - 出处：https://en.wikipedia.org/wiki/Technology_tree
- **历史归属**：桌游 *Civilization*（Francis Tresham，**1980**）被认为引入了科技树；《Sid Meier's Civilization》（**1991**）让它成为标志性机制。同上 Wikipedia 条目。
- **已知问题 / 批评**：
  1. **最优解固化 / build order 记忆化**：Wikipedia 直接写「Analysis of a tech tree can lead players to **memorize and use specific build orders**」。→ 风险：玩家会去背「最短通关顺序」绕过理解。**对策：把考核放在「这个技能能解决什么问题」而不是「解锁顺序」。**
  2. **史观扭曲**：Historical Games Network《The Digital Dark Ages and the Trouble with Tech Trees》（2024-12-17）批评科技树把历史呈现为**线性进步**，并制造「黑暗时代」这类错误框架。https://www.historicalgames.net/digital-dark-ages-tech-trees
     - → 映射到我们：**技术不是线性进步**。`必修 / 推荐` 前置必须允许「多条路走进同一个技能」（例如「操作系统」既可从「计算机组成」也可从「C/底层」进入），否则就是在教一种虚假的线性知识观。
  3. **"盲研究"（blind research）的尝试**：《Will Civilization VII Finally Get the Tech Tree Right?》（SUPERJUMP）提到系列早期就有 blind research 选项，并讨论玩家是否接受「不知道自己在研究什么」。https://www.superjumpmagazine.com/will-civilization-vii-finally-get-the-tech-tree-right
     - → 启示：**完全透明的树**会让玩家「查表通关」；适度「雾化」（只显示下一步轮廓、不显示全图）能保留探索感，可作为**可选「探索模式」**。

#### A9-2. Learn Git Branching（learngitbranching.js.org）

- 定位（作者 Peter Cottle 仓库自述）：「LearnGitBranching is a **git repository visualizer, sandbox, and a series of educational tutorials and challenges**. Its primary purpose is to help developers understand git through the power of **visualization**（something that's absent when working on the command line）. This is achieved through **a game with different levels** to get acquainted with the different git commands.」https://github.com/pcottle/learnGitBranching
- 站点：https://learngitbranching.js.org
- **最值得抄的一条**：它把「关卡」做成了**可编写的内容格式**：「You can **build levels with the `build level` command**. A dialog will walk you [through it]」——即**教学关卡是一等公民、可由非程序员以数据形式创作**。直接对应我们「192 技能 × 4–9 知识项」的内容生产需求：**先把关卡 schema 定下来，再谈做多少内容。**
- 玩法：左「命令区」右「提交图实时变化」，另有 sandbox 自由实验；判定方式是「目标状态」（例如把 HEAD/main/bugFix 移到指定 commit）。
- 已知问题：命令是**真 Git 语法**（`git checkout HEAD^`、`git branch -f`），零基础仍需先懂「提交/分支」是什么；社区存在专门的「答案与笔记」仓库（如 https://github.com/blentz100/Learn-Git-Branching-Solutions-and-Notes ），说明**卡关时玩家会直接去抄答案**——这是「目标态判定」类关卡的通病。**未查到**官方对关卡数的说明。

#### A9-3. Oh My Git!（ohmygit.org，开源）

- 定位（官方）：「An **open source** game about learning Git!」https://ohmygit.org/
- 三条官方特性（每条都可搬）：
  1. 「*Oh My Git!* **visualizes the internal structures** of Git repositories **in realtime**. The player can **immediately see the results of their actions**.」
  2. 「To accommodate people who are **new to Git**, the game features a **custom-designed playing card interface**! The cards help **remember newly introduced Git commands**, but also **contain a short description and an icon**. Therefore, they **combine both action as well as documentation**.」
     - → **「技能卡 = 可执行动作 + 说明书」二合一**，这正是我们「技能树节点」该有的形态：点开一个技能，既能看到「怎么用」，也能直接「用它」。
  3. 「For more advanced or curious players, the game offers an **integrated terminal**, where they can execute **arbitrary Git commands**. There's a **'real' Git integrated into the game**」——**渐进式抽象**：卡牌（新手）→ 终端（进阶），同一游戏内两条通道。
  - 另外它明确以「**团队协作 / remotes**」为重点：「*Oh My Git!* puts a focus on how to **interact with remotes**, and which workflows exist when dealing with **multiple repositories**」。
- 资助方（官方页面可见）：**德国联邦教育科研部（BMBF）**、**Prototype Fund**、**Open Knowledge Foundation Deutschland** —— 说明这类教学游戏主要靠公共/公益资金而非市场收入。
- 已知问题：官方页面自己写「**Our current funding will run out at the end of February**」——**开源教学游戏的可持续性问题是真实存在的**。

**A9 小结：可吸收 / 不适合**

| 可吸收 | 不适合 |
|---|---|
| **DAG + tier**：起手只给少数几个可选，逐层展开（Civ 的 tier 1 只有少量选项） | 单一「最优 build order」（玩家会背表通关） |
| **技能卡 = 动作 + 文档二合一**（Oh My Git! 卡牌） | 只显示名字、点开才看到说明（Duolingo 圆点被吐槽的点） |
| **实时可视化内部状态**（Oh My Git! 的 repo 图、Learn Git Branching 的提交图） | 教「命令语法」而不教「状态怎么变」 |
| **关卡是数据、可被作者/教师编写**（Learn Git Branching 的 `build level`） | 硬编码关卡逻辑（内容量一大就做不动） |
| **渐进抽象**：卡牌 → 终端（同一游戏两条通道） | 一上来就给真终端/真语言（零基础劝退） |
| **多入口前置**（一个技能允许多条路径进入，避免虚假线性） | 把技术史写成单线进步（史观问题） |
| 可选「雾化/探索模式」（Civ 的 blind research） | 全图透明导致的「查表式通关」 |

---

## B. 学习科学依据（每条给出处）

> 说明：本节优先引用**元分析/综述/顶刊实验**。凡是只有「某产品博客自述」的结论，会明确标注。
> 数值均抄自可查的摘要原文；**凡我未能核对原文摘要的数字，一律不写**。

### B1. 检索练习 / 测试效应（retrieval practice / testing effect）

- **经典实验**：Roediger & Karpicke, *Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention*，**Psychological Science 17(3):249–255, 2006**，DOI 10.1111/j.1467-9280.2006.01693.x。
  - 关键结论（摘要原文）：最终测试在 **5 分钟后**进行时，反复**学习**优于反复**测试**；但在**延迟测试（2 天、1 周）**上，「先前测试」带来的保持量**大幅高于**反复学习——「**even though repeated studying increased students' confidence in their ability to remember the material**」。
  - **双重含义**：①测试本身就是学习；②**反复阅读会让你「感觉学会了」而实际没学会**（元认知错觉）。
  - https://pubmed.ncbi.nlm.nih.gov/16507066/
- **检索 > 精加工学习**：Karpicke & Blunt, *Retrieval Practice Produces More Learning than Elaborative Studying with Concept Mapping*，**Science 331(6018):772–775, 2011**，DOI 10.1126/science.1199327。摘要原文：「practicing retrieval produces **greater gains in meaningful learning** than elaborative studying with concept mapping」，且优势在**理解题与推理题**上同样存在。https://pubmed.ncbi.nlm.nih.gov/21252317/
- **元分析**：Rowland, *The effect of testing versus restudy on retention: A meta-analytic review of the testing effect*，**Psychological Bulletin 140(6):1432–1463, 2014**，DOI 10.1037/a0037559。摘要原文：「**initial recall tests yielding larger testing benefits than recognition tests**」（**自由回忆 > 再认**）。https://pubmed.ncbi.nlm.nih.gov/25150680/
- **元分析（教育情境）**：Adesope, Trevisan & Sundararajan, *Rethinking the Use of Tests: A Meta-Analysis of Practice Testing*，**Review of Educational Research 87(3):659–701, 2017**，DOI 10.3102/0034654316689306。摘要原文：「practice tests are **more beneficial for learning than restudying and all other comparison conditions**」。https://doi.org/10.3102/0034654316689306
- **权威评级**：Dunlosky, Rawson, Marsh, Nathan & Willingham, *Improving Students' Learning With Effective Learning Techniques*，**Psychological Science in the Public Interest 14(1):4–58, 2013**，DOI 10.1177/1529100612453266。
  - 该专著评了 10 种技巧（elaborative interrogation、self-explanation、summarization、highlighting、keyword mnemonic、imagery、rereading、**practice testing**、**distributed practice**、**interleaved practice**），并按「跨学习条件/学生特征/材料/判据任务是否泛化」评效用等级。**其中 practice testing 与 distributed practice 被评为「high utility」；highlighting 与 rereading 为「low utility」**（这是该文最广为引用的结论，原文表格可查）。
  - https://pubmed.ncbi.nlm.nih.gov/26173288/
- **对我们**：每个知识项的「必学」环节必须以**主动产出**结束（写出来/选出来/解释出来），不能用「读过一遍 + 打个勾」。

### B2. 间隔重复（spacing effect）

- **最大规模元分析**：Cepeda, Pashler, Vul, Wixted & Rohrer, *Distributed Practice in Verbal Recall Tasks: A Review and Quantitative Synthesis*，**Psychological Bulletin 132(3):354–380, 2006**，DOI 10.1037/0033-2909.132.3.354。
  - 样本量（摘要原文）：「**839 assessments of distributed practice in 317 experiments located in 184 articles**」。
  - 核心结论（摘要原文）：「**ISI and retention interval operate jointly**……the ISI producing maximal retention **increased as retention interval increased**」。
  - **工程含义**：**「间隔多久复习」没有统一答案，取决于你想记住多久**。想保 1 周 → 间隔短；想保 1 年 → 间隔长。这正是 FSRS/Anki 用「目标保持率」而不是固定间隔的原因（见 C 节）。
  - https://pubmed.ncbi.nlm.nih.gov/16719566/
- **元认知错觉（很关键的一条）**：Kornell & Bjork, *Learning Concepts and Categories: Is Spacing the "Enemy of Induction"?*，**Psychological Science 19(6):585–592, 2008**，DOI 10.1111/j.1467-9280.2008.02127.x。
  - 摘要原文：「induction **profited from spacing**, even though massing apparently created a sense of **fluent learning**: participants **rated massing as more effective than spacing, even after their own test performance had demonstrated the opposite**」。
  - **对我们的直接设计含义**：玩家会**更喜欢**「一口气练完一个技能」（集中），并**误以为那样更有效**。因此游戏的默认排法必须是「交错+间隔」，但**必须用界面解释为什么**，否则玩家会觉得「这游戏不让我好好学」。
  - https://pubmed.ncbi.nlm.nih.gov/18578849/

### B3. 交错练习（interleaved practice）

- **元分析（本报告里最细致的一条）**：Brunmair & Richter, *Similarity matters: A meta-analysis of interleaved learning and its moderators*，**Psychological Bulletin 145(11):1029–1052, 2019**，DOI 10.1037/bul0000209。
  - 规模：「**59 studies with 238 effect sizes nested in 158 samples**」。
  - 总体效应：**Hedges' g = 0.42**（中等）。
  - **调节变量（这才是能用的部分）**：
    - 绘画/视觉材料 **g = 0.67**（最强）；
    - **数学任务 g = 0.34**（小效应，但为正）；
    - 说明性文本、味觉材料：**不显著**；
    - **词汇类材料：集中（blocking）反而更好，g = −0.39**；
    - 效应更强的情形：**类别之间更相似、类别内部更不相似、材料更复杂**。
  - 结论原文：「interleaving can effectively foster inductive learning **but that the setting and the type of learning material must be considered**……should be used **with caution** in certain conditions, especially for expository texts and words」。
  - https://pubmed.ncbi.nlm.nih.gov/31556629/
  - **对我们的含义**：我们教的是**数学 + 计算机**（正是 g≈0.34 的正效应区），交错**值得做**；但**不能无脑交错**——前置技能未掌握就交错会变成「认不出该用哪招」。交错必须发生在**单个技能已达到 Proficient 之后**（对应 Khan 的 Mastered 要求混合测评，A3）。
- **数学情境的原始实验**：Rohrer & Taylor, *The shuffling of mathematics problems improves learning*，**Instructional Science 35:481–498, 2007**，DOI 10.1007/s11251-007-9015-8。标题即结论。https://doi.org/10.1007/s11251-007-9015-8

### B4. 例子学习（worked example）与提示渐隐（fading）

- **worked example effect 的原始研究**：Sweller & Cooper, *The Use of Worked Examples as a Substitute for Problem Solving in Learning Algebra*，**Cognition and Instruction 2(1):59–89, 1985**，DOI 10.1207/s1532690xci0201_3。标题即结论：**在初学阶段用「看例题」替代「自己解题」更有效**（因为新手的工作记忆被搜索解法的过程占满）。https://doi.org/10.1207/s1532690xci0201_3
- **fading 的框架**：Renkl & Atkinson, *Structuring the Transition From Example Study to Problem Solving in Cognitive Skill Acquisition: A Cognitive Load Perspective*，**Educational Psychologist 38(1):15–22, 2003**，DOI 10.1207/s15326985ep3801_3。核心是「**从完整例题 → 部分填空 → 独立解题**」的连续过渡（即 fading / completion problems）。https://doi.org/10.1207/s15326985ep3801_3
- **专家反转效应（必须知道的边界）**：Kalyuga, Ayres, Chandler & Sweller, *The Expertise Reversal Effect*，**Educational Psychologist 38(1):23–31, 2003**，DOI 10.1207/S15326985EP3801_4。
  - 含义：**对新手有效的支持（详细讲解、例题、提示），对已具备知识的人会变成干扰**——同一份教学设计，效果随专长水平反转。
  - **对我们的含义（极重要，因为我们有 192 个技能、玩家水平差异巨大）**：**提示与例题必须能「按人/按技能状态自动降级」**。已经 Proficient 的技能不该再弹教学弹窗，否则会烦；零基础的新技能不该直接给无提示练习。这正好解释了 Brilliant「practice set 撤掉脚手架」（A2）与 Khan「等级会掉」（A3）的设计动机。
- **实践版（产品化）**：Brilliant 官方自述「In practice sets, **the scaffolding falls away**……there are **no more visual aids or hints**」（见 A2）。这是我们能找到的、把 fading 做进商业产品的最清晰表述。

### B5. 反馈（feedback）

- **权威综述**：Hattie & Timperley, *The Power of Feedback*，**Review of Educational Research 77(1):81–112, 2007**，DOI 10.3102/003465430298487。提出 feedback 的三问框架（Where am I going? How am I going? Where to next?）与四个层级（task / process / self-regulation / self）。https://doi.org/10.3102/003465430298487
- **更新的元分析（有具体数字）**：Wisniewski, Zierer & Hattie, *The Power of Feedback Revisited: A Meta-Analysis of Educational Feedback Research*，**Frontiers in Psychology 10:3087, 2020**，DOI 10.3389/fpsyg.2019.03087。
  - 规模：「**435 studies, k = 994, N > 61,000**」。
  - 总体效应：**d = 0.48**（中等）。
  - **但**：摘要原文「**the significant heterogeneity in the data shows that feedback cannot be understood as a single consistent form of treatment**」；「feedback has **higher impact on cognitive and motor skills outcomes than on motivational and behavioral outcomes**」；「the necessity of interpreting **different forms of feedback as independent measures**」。
  - https://pubmed.ncbi.nlm.nih.gov/32038429/
  - **对我们的含义**：不能写「我们会给即时反馈，所以有效」。**反馈的类型（针对任务 vs 针对人）× 内容（信息量）**才是决定因素；**对「人」的表扬（"你真聪明"）与对「任务」的信息反馈不是一回事**。
- **反例（反馈不总是有益）**：Kluger & DeNisi, *The effects of feedback interventions on performance: A historical review, a meta-analysis, and a preliminary feedback intervention theory*，**Psychological Bulletin 119(2):254–284, 1996**，DOI 10.1037/0033-2909.119.2.254。
  - 该文的核心立场是：**反馈干预的平均效应为正，但存在相当比例（原文强调超过三分之一）的干预使表现下降**，并因此提出「反馈干预理论」来解释何时会害人。
  - **诚实标注**：我**未能抓取到原文摘要全文**（APA 站点拒绝抓取，Semantic Scholar 限流），因此**不引用其具体效应量与比例数字**；上述「存在大量负向案例」的定性结论请以原文为准。
  - https://doi.org/10.1037/0033-2909.119.2.254
- **最强的反例证据（实验，不是综述）**：Decker-Woodrow 等 2023 的 RCT（见 A8）中，**「ASSISTments 即时反馈」组与「无即时反馈的主动对照」组之间没有显著差异**，而同实验里的两个游戏化交互组（FH2T、DragonBox 12+）显著优于对照。
  - → **「即时反馈」本身不是学习增益的来源；交互式的问题表征 + 游戏机制才可能是。**
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC10125888

### B6. 掌握式学习（mastery learning）

- **元分析**：Kulik, Kulik & Bangert-Drowns, *Effectiveness of Mastery Learning Programs: A Meta-Analysis*，**Review of Educational Research 60(2):265–299, 1990**，DOI 10.3102/00346543060002265。
  - 摘要原文（可查）：「A meta-analysis of findings from **108 controlled evaluations** showed that mastery learning programs have **positive effects** on the examination performance of students in colleges, high schools, and the upper grades in elementary schools. The effects appear to be **stronger on the weaker students** in a class……Mastery programs have positive effects on student **attitudes** toward course content and instruction **but may increase student time on instructional tasks**. In addition, **self-paced mastery programs often reduce the completion rates** in college classes.」
  - **三个可直接用的结论**：①掌握式学习**对基础弱的学生帮助更大**（正合我们「零基础」定位）；②**会拉长学习时间**（要做好「比刷视频慢」的心理预期）；③**自定进度 + 掌握要求 = 完课率下降**（要防退出，见 B7 的短期激励）。
  - https://doi.org/10.3102/00346543060002265
- **产品化实例与官方证据**：Khan Academy 的 5 档掌握度 + 「skills to proficient」指标 + 与 MAP Growth 的相关性（见 A3）。其官方结论「**少而精 > 多而浅**」与上面 Kulik 的「对弱学生效应更强」是同向的。

### B7. 游戏化（积分 / 徽章 / 排行榜）的元分析结论（含负面）

- **Sailer & Homner, *The Gamification of Learning: A Meta-analysis*，Educational Psychology Review 32:77–112, 2020**（**开放获取**），DOI 10.1007/s10648-019-09498-w。
  - 摘要原文数字：**认知结果 g = .49（95% CI [0.30, 0.69], k = 19, N = 1686）；动机结果 g = .36（[0.18, 0.54], k = 16, N = 2246）；行为结果 g = .25（[0.04, 0.46], k = 9, N = 951）**。
  - **读法**：**都是「小效应」且置信区间很宽**；**动机提升 ≈ 认知提升**，即「更好玩」并不自动等于「学得更好」。
  - PDF：https://link.springer.com/content/pdf/10.1007/s10648-019-09498-w.pdf
- **Li, Ma & Shi, *Examining the effectiveness of gamification as a tool promoting teaching and learning in educational settings: a meta-analysis*，Frontiers in Psychology 14:1253549, 2023**，DOI 10.3389/fpsyg.2023.1253549。
  - 「**41 studies with 49 independent samples involving more than 5,071 participants**」，总体 **g = 0.822 [0.567, 1.078]**（大效应——**与上一条 g≈0.49 差异很大，说明设计异质性与发表偏倚风险显著**）；显著调节变量：**用户类型、学科、游戏化设计原则、"gameful" 体验时长、学习环境**。
  - https://pubmed.ncbi.nlm.nih.gov/37876838/
- **时长是关键调节变量（负面结论，很重要）**：Kim & Castelli, *Effects of Gamification on Behavioral Change in Education: A Meta-Analysis*，**IJERPH 18(7):3550, 2021**，DOI 10.3390/ijerph18073550。
  - 摘要原文数字：总体 **d = 0.48**；**「Brief interventions delivered in days or less than 1 week were significantly more effective (ES = 1.57) than interventions lasting up to 20 weeks (ES = 0.30)」**；且「**Interventions incorporating gamification elements across years (ES = −0.20) was adversely associated with behavioral change**」。
  - 原文结语：「**short-term over longer-term gamified interventions might be a promising way to initiate changes**」。
  - https://pubmed.ncbi.nlm.nih.gov/33805530/
  - **对我们的含义（本报告最重要的警告之一）**：游戏化效果**随持续时间衰减，跨年使用甚至转负**。**「新奇感」是有限资源**。→ 不能靠不断加码新机制维持长期学习；长期留存必须靠「技能真的变强 + 记得住」的实证体验。这也解释了 Duolingo 不断改机制（Hearts→Energy、Quests）却持续被批「在玩指标游戏」（A1-3）。
- **外在奖励侵蚀内在动机（经典元分析，有数字）**：Deci, Koestner & Ryan, *A meta-analytic review of experiments examining the effects of extrinsic rewards on intrinsic motivation*，**Psychological Bulletin 125(6):627–668, 1999**，DOI 10.1037/0033-2909.125.6.627。
  - 摘要原文数字：**128 项实验**；**engagement-contingent / completion-contingent / performance-contingent 奖励显著削弱「自由选择」的内在动机，d 分别为 −0.40、−0.36、−0.28**；engagement-/completion-contingent 奖励也削弱自报兴趣（d = −0.15、−0.17）。
  - **但**：「**Positive feedback enhanced both free-choice behavior (d = 0.33) and self-reported interest (d = 0.31)**」；「**Tangible rewards tended to be more detrimental for children than college students**」。
  - https://pubmed.ncbi.nlm.nih.gov/10589297/
  - **对我们的设计规则**：**「做完给金币/给分」这类有形、可预期的奖励会削弱内在动机**（对低龄尤甚）；**「这一步对了，因为……」这类信息性正向反馈会增强内在动机**。→ **奖励应该是「信息」而不是「货币」**；徽章的语义应描述「你会了什么」，而不是「你攒了多少」。
- **严肃游戏元分析（范围参考）**：Wouters, van Nimwegen, van Oostendorp & van der Spek, *A meta-analysis of the cognitive and motivational effects of serious games*，**Journal of Educational Psychology 105(2):249–265, 2013**，DOI 10.1037/a0031311。
  - 该文的框架是**把「认知结果」与「动机结果」分开评估**——这本身就是应采纳的评估原则：**不要用「玩家说好玩」代替「玩家学会了」**。**具体效应量我未核实，故不引用数字。**
  - https://doi.org/10.1037/a0031311

### B 节「一句话总结」

> **有证据能提升长期保持的**：主动检索（B1）、间隔（B2）、在**掌握之后**交错（B3）、初学看例题并逐步撤掉支持（B4）、针对任务的信息性反馈（B5）、以掌握为门槛（B6）。
> **不能想当然的**：加游戏化（效应小且随时间衰减，B7）、加即时反馈（B5 的 RCT 反例）、把「好玩」当「学会」（B7）。

---

## C. 间隔重复算法：FSRS

> 本节所有版本号、许可证、API 名称均**直接读自官方仓库 / npm registry / 包内类型声明**，不是凭记忆。

### C1. FSRS 是什么、官方仓库在哪

- 全称 **Free Spaced Repetition Scheduler**，由开源社区 **open-spaced-repetition** 维护，是 Anki 传统 **SM-2** 调度的替代方案。
- **官方参考实现仓库**：https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler
  - 描述（GitHub API 原文）：「A spaced repetition algorithm based on **DSR model**」；许可证 **MIT**；Star ≈ **730**；最近 push **2026-04-21**。（数据抓取于 2026-11-02）
- **Anki 生态的主仓库**：https://github.com/open-spaced-repetition/fsrs4anki
  - 描述：「A modern Anki custom scheduling based on Free Spaced Repetition Scheduler algorithm」；许可证 **MIT**；Star ≈ **4,122**；最近 push **2026-08-14**。
- **Rust 实现（Anki 实际内置的那个）**：https://github.com/open-spaced-repetition/fsrs-rs （Anki 的 release notes 中反复出现 "Update FSRS to [6.6.x] (fsrs-rs)"）
- **算法论文（可引用）**：
  1. Ye, Su, Cao, *A Stochastic Shortest Path Algorithm for Optimizing Spaced Repetition Scheduling*，**KDD '22**，DOI **10.1145/3534678.3539081**（2022-08-14）。https://doi.org/10.1145/3534678.3539081
  2. *Optimizing Spaced Repetition Schedule by Capturing the Dynamics of Memory*，**IEEE TKDE, 2023**，DOI **10.1109/TKDE.2023.3251721**（2023-10-01）。https://doi.org/10.1109/TKDE.2023.3251721
- **模型的核心变量（DSR）**：**D**ifficulty（难度）、**S**tability（稳定度）、**R**etrievability（可提取性）。调度决策 = 在当前 D、S 下预测 R，并选择让 R 落到「目标保持率」的时间点。

### C2. ts-fsrs（npm 包）

**基本信息（全部来自 npm registry `https://registry.npmjs.org/ts-fsrs`，抓取于 2026-11-02）**

| 项目 | 值 |
|---|---|
| 包名 | **`ts-fsrs`** |
| 许可证 | **MIT** |
| 最新稳定版（`dist-tags.latest`） | **6.0.0** |
| 6.0.0 发布时间 | **2026-10-28**（registry `time` 字段） |
| 预发布标签 | `beta` = 6.0.0-beta.15 |
| 历史版本总数 | 92（首版 2023-03-05） |
| 仓库 | https://github.com/open-spaced-repetition/ts-fsrs （monorepo 内 `packages/fsrs`） |
| 运行时要求 | **Node.js >= 24.0.0**（README 原文） |
| 模块格式 | ESM / CJS / UMD（`main: dist/index.cjs`，`types: dist/index.d.mts`） |
| 依赖 | `@open-spaced-repetition/srs-kit@1.0.0` |

- **支持的模型版本**（README 原文）：「ts-fsrs v6 supports **FSRS-3, FSRS-4, FSRS-4.5, FSRS-5, FSRS-6, and FSRS-7**. The library version and FSRS model version are **independent**.」

**API 一：经典接口（题面问的 `createEmptyCard` / `fsrs().repeat` / `next` / `Rating`）—— 在 6.0.0 中仍然存在**

从包内类型声明 `dist/index.d.mts` 直接读到的签名：

```ts
export declare function createEmptyCard(now?: DateInput): Card;

// fsrs(params?) 依然导出（index.mjs 内实现为 `const fsrs = (params) => new FSRS(params || {})`）
// 文档注释示例：const f = fsrs();  const f = fsrs(params);

export declare class FSRS implements IFSRS {
  // 预览四种评分各自会把卡片调度成什么样
  repeat(card: CardInput | Card, now: DateInput): IPreview;
  // 真正提交一次复习
  next(card: CardInput | Card, now: DateInput, grade: Grade): RecordLogItem;
}

export declare const generatorParameters: (props?: Partial<FSRSParameters>) => FSRSParameters;
```

- 类型注释里的官方示例（原文）：
  - `const emptyCard = createEmptyCard(now); const repeat = f.repeat(emptyCard, now); const { card, log } = repeat[Rating.Hard];`
  - `const recordLogItem = f.next(card, new Date(), Rating.Again);`
- **`IPreview` 的形状**：按 4 个评分索引的对象（`repeat[Rating.Good]` → `{ card, log }`），适合做「这个按钮会把下次复习推到几天后」的**预览 UI**。
- **`Rating` 枚举的取值**：包内类型声明原文注释为「**0-4: Manual, Again, Hard, Good, Easy**」，即
  `Rating.Manual = 0`、`Rating.Again = 1`、`Rating.Hard = 2`、`Rating.Good = 3`、`Rating.Easy = 4`。
  （`Grade` = 去掉 `Manual` 的那四档。）
- 同时导出 `State` 枚举与 `TypeConvert`（`TypeConvert.rating(value)` 可把外部数值转成 `Rating`）。
  - **诚实标注**：`State` 枚举的**具体成员名称未在本次抓取中逐项核实**（只确认类型声明中存在导出）。若要用，请自行 `console.log(State)` 确认。

**API 二：v6 推荐的新接口（面向「调度器对象」而非「函数式参数」）**

```ts
import { DefaultScheduler, Rating } from 'ts-fsrs'

const scheduler = await DefaultScheduler({           // 省略 version 时默认 FSRS-7
  version: 'FSRS-7',
  desiredRetention: 0.9,
  enableShortTerm: true,
  learningSteps: ['1m', '10m'],
  relearningSteps: ['10m'],
  enableFuzz: false,
  maximumInterval: 36_500,
})

const card = scheduler.newCard({ now })
const preview = scheduler.preview({ card, now })      // 可迭代，含 Again/Hard/Good/Easy
const result  = scheduler.review({ card, grade: Rating.Good, now })  // → { card, revlog }
```

- README 原文要点：「`preview()` returns an **iterable** with results for Again, Hard, Good, and Easy. `review()` returns a **new card and review log without mutating the input card**. **Save both `result.card` and `result.revlog`**」。→ **必须持久化 revlog**（否则无法做参数优化与统计）。
- 配置项语义（README 原文）：`desiredRetention` = 目标保持率，**越高复习量越大**；`maximumInterval` = 间隔天数上限；`enableFuzz` = 给长间隔加随机抖动；省略 `weights` 则用所选模型版本的预设权重。
- **迁移注意事项**：6.0.0 是**破坏性大版本**（默认模型从 FSRS-6 提到 **FSRS-7**，且要求 Node >= 24）。若要稳，生产上可先用 `5.4.2`（registry 中 6.0.0 之前的最新 5.x）。

### C3. Anki 采用 FSRS 的版本（依据 Anki 官方 release notes）

抓取自 GitHub `ankitects/anki` Releases API（2026-11-02），逐版本核对含 "FSRS" 的条目：

| Anki 版本 | 发布日期 | 与 FSRS 相关的事实（原文摘录） |
|---|---|---|
| **2.1.64** | 2023-05-24 | 首次出现 FSRS 相关功能：可按 FSRS 属性搜索，如 `prop:cdn:d>0.5`（此时 FSRS 仍需通过 custom scheduling 使用） |
| **23.10** | **2023-10-31** | 「**Support for FSRS (which improves upon the scheduling provided by SM-2) is now integrated into Anki. You can compute the model weights directly inside Anki, and no longer need to use custom scheduling**」← **FSRS 正式内置的版本** |
| 23.10.1 | 2023-11-09 | 「Rename FSRS weights to parameters」 |
| **23.12** | 2023-12-25 | 「Minor improvements to the algorithm (**FSRS 4.5**)」 |
| 24.04 | 2024-03-31 | 「Move most FSRS options into their own section of the deck options」 |
| 24.06 | 2024-06-07 | 「Update to latest FSRS」 |
| **24.11** | 2024-11-26 | 「**Add FSRS simulator to deck options**」「Let FSRS control short term schedule when no (re)learning steps are set」 |
| 25.02 | 2025-02-11 | 「FSRS updates」，修 FSRS simulator 一系列问题 |
| **25.07** | 2025-07-04 | 「**FSRS-6 brings further algorithm improvements**」「Support load balance and easy days in FSRS simulator」 |
| 26.05 / 26.08 / 26.09 | 2026 | 持续跟进 `fsrs-rs` 6.6.x；「Require three left-clicks to unlock FSRS parameter editing」；「Hide FSRS-only sort orders……when FSRS is disabled」 |

- 客户端兼容（**Anki 官方手册原文**）：「**Anki 23.10, AnkiMobile 23.10, and AnkiWeb all support it. AnkiDroid supports it in 2.17+.**」https://docs.ankiweb.net/deck-options.html#fsrs

### C4. Anki 手册中「做产品必须知道的坑」（原文可查）

出处：https://docs.ankiweb.net/deck-options.html#fsrs

1. **FSRS 是「选项」而不是默认**：手册写「**Enable FSRS under the "FSRS" section, at the bottom of the deck options page.**」「**FSRS can only be enabled globally; you cannot enable it for some presets and disable it for others.**」
   - **未查到**任何官方公告称「FSRS 已成为所有用户的默认调度器」。截至 2026-11-02 抓取的手册文本，它仍是**需显式开启**的功能。
2. **目标保持率的默认值与代价**：「the default is **90%**……**Above 90% the workload increases very quickly, and above 97% the workload can be overwhelming.**」
3. **学习步长必须短**：「Ensure that all your learning and re-learning steps are **shorter than 1d** and can be completed on the same day……Steps such as 10m or 30m are good.」
4. **「Hard 误用」会毁掉整个调度**：「FSRS can adapt to almost any habit, except for one: **pressing "Hard" instead of "Again" when you forget**……If you press "Hard" when you have failed to recall, **all intervals will be unreasonably high**.」
   - → **产品化含义**：不要把按钮做成「模糊 / 一般 / 会 / 很会」——那必然诱导用户用中间档替代「忘了」。**必须让「忘了」成为最自然、最不受惩罚的选择。**
5. **插件冲突**：「if an add-on affects intervals and scheduling in some way, **it shouldn't be used with FSRS**」→ 我们的游戏里如果还有别的进度逻辑（连胜、每日任务），**不要让它改到期时间**。

### C5. FSRS 能不能直接用在我们这棵技能树上？（判断，非事实）

**FSRS 的前提假设**（来自上面论文/README 的模型定义）：
1. 一张卡 = **一个原子记忆项**（能在几秒内回答的「是否记得」）；
2. 每次复习给出一个**离散评分**（Again/Hard/Good/Easy）；
3. 有**足够的历史复习记录**才能优化参数（Anki 要求一定条数才允许 Optimize）。

**映射到我们的结构**：

| 我们的层级 | 是否适合 FSRS | 理由 |
|---|---|---|
| **知识项**（每技能 4–9 个） | ✅ **适合** | 一个知识项本质是「一条可陈述/可判断的命题」（如「进程与线程的区别」「导数的定义」），可做成 5 秒级检索题 |
| **技能**（192 个） | ⚠️ **不适合直接用 FSRS** | 技能是「能力」而非「记忆」，其状态更接近 Khan 的 5 档掌握度（A3）：需要用**混合测评**判定，而不是用到期时间 |
| **综合练习题**（每技能 1 道） | ❌ **不适合 FSRS** | 20–40 分钟的解题过程不是一个「复习事件」；它更适合作为**掌握度判定的测评**（Khan 的 Mastered 层） |

→ **建议的双层结构**：**知识项用 FSRS 排复习（记忆层）** + **技能用掌握度状态机（能力层）**，且「能力层掉级」由「相关知识项的 FSRS 保持率下降 + 综合练习题失败」共同触发，而不是独立计时（避免 Duolingo 的 cracked skill 那种「莫名裂开」的挫败，见 A1-2）。

---

## D. 给游戏设计的建议（按优先级）

> 每条格式：**建议 → 怎么做 → 依据**。
> P0 = 不做会毁掉「真的学进去」这个目标；P1 = 决定体验成败；P2 = 加分项。

### P0（地基，必须先定）

**1. 每个知识项以「主动产出」收尾，禁止「读过 = 学会」**
- 做法：知识项的三步固定为「先猜（pretest）→ 看/玩（可视化或例题）→ 合上答案复述或重做」；最后一步必须能判对错。
- 依据：**A2**（Brilliant 「we don't teach how to do something before asking questions」，B4 同源）、**B1**（Roediger & Karpicke 2006：延迟测试上测试 > 重学，且重学只提高信心；Karpicke & Blunt 2011：检索 > 概念图；Adesope 2017 元分析：练习测试优于所有对照条件）。

**2. 复习由系统排程，且「复习 = 前进」，不做「裂开的技能」**
- 做法：主路径里插入 review 节点；复习完成的视觉反馈与新课完全一致（不显示「你在补课」）；**复习永不受体力/次数限制**。
- 依据：**A1-2**（Duolingo 官方把 cracked skills 移除，改为「Practice is built into your path」）、**A1-3**（官方自承 Hearts 让初学者 2 倍概率中途耗尽，课末复习不耗能）、**B2**（Cepeda 2006：最佳间隔随目标保持期变化 → 必须动态排程）。反例参照：**A3**（Khan 掉级机制若不给解释会造成挫败）。

**3. 记忆层用 FSRS 排知识项；能力层用 5 档掌握度判技能；两套状态不要混用**
- 做法：`知识项` → FSRS 卡片（Rating 四档）→ 决定「什么时候再问这个知识点」；`技能` → Not started/Attempted/Familiar/Proficient/Mastered → 由「知识项保持率 + 综合练习题」决定。
- 依据：**C1–C5**（FSRS 的假设是原子记忆项 + 离散评分；不适合 20 分钟的综合题）、**A3**（Khan 的五档 + 「Mastered 需混合测评」）、**B6**（Kulik 1990：掌握式学习对弱学生效应更强，但会拉长学习时间、降低完课率）。

**4. 提示与例题必须「按技能状态自动降级/升级」**
- 做法：`Not started` → 给完整例题 + 分步提示；`Familiar` → 给部分填空（completion problem）；`Proficient` → 撤掉全部脚手架；`Mastered` → 只给综合题与新情境。
- 依据：**B4**（Sweller & Cooper 1985 worked example effect；Renkl & Atkinson 2003 fading；**Kalyuga 2003 专家反转效应**——对新手有效的支持对熟手是干扰）、**A2**（Brilliant：practice set 里 scaffolding falls away）。

**5. 错误不是资源消耗，是信息**
- 做法：答错不扣任何「生命/体力/金币」；答错后**必须**给出「你错在哪一步 + 这一步对应哪个知识项」；用信息性反馈代替评价性反馈。
- 依据：**A1-3**（Duolingo 官方：犯错是学习的自然部分，初学者 2 倍耗尽）、**B5**（Wisniewski 2020：反馈不是单一处理，需按内容区分；Deci 1999：信息性正向反馈增强内在动机 d=0.33/0.31，而有形奖励削弱之）、**B7/Deci 1999**（负向：有形奖励 d=−0.28~−0.40）。

### P1（决定体验与留存）

**6. 技能节点 = 「可执行动作 + 说明书」二合一**
- 做法：点开技能节点，左边是「你现在能用它做什么」（可运行的迷你示例），右边是「怎么用」（签名/常见坑）；节点本身可被拖进解题面板。
- 依据：**A9-3**（Oh My Git! 的 playing card「combine both action as well as documentation」）、**A4**（nandgame / Turing Complete 的「造出来的东西变成下一关的工具」）、**A2**（Brilliant 每课单一概念 + 即时定制反馈）。

**7. 前置图必须是真 DAG，且允许「多条路进入同一技能」；另给一个「简化视图」**
- 做法：真实视图显示必修/推荐前置全貌（我们的卖点）；简化视图按当前进度只画「下一步 3–5 个可达节点」（Brilliant 承认它故意把前置画得比真实简单，正是为了清晰里程碑）。
- 依据：**A9-1**（Wikipedia：tech tree 是 DAG、tier 化、Civ 每个高级技术都有多个前置；Historical Games Network 批评单线进步史观）、**A2**（Brilliant 自述 leveling 系统「displays a more reductive view of concept connections and prerequisites than the underlying reality」）、**A1-1**（Duolingo 单线路径的代价：路径变长、导航困难、失去选择权）。

**8. 双层目标：过关（必做）+ 优化（可选、多指标）**
- 做法：知识项 = 过关线；每技能的综合练习题除了「通过」外，额外给 2–3 个可选的优化维度（更短、更快、更省内存、更可读），只展示自己的历史最好成绩，**不做全服排行榜**（或默认关闭）。
- 依据：**A5**（HRM 的 Optimization Challenges 是 optional；Zachtronics 的多指标优化；HN 玩家指出 TIS-100 的「过关难 + 优化靠猜」是缺点 → 两条曲线要分开）、**A1-3 / A9-1**（XP/streak/build order 会被刷，导致「玩指标」而非「学东西」）、**B7**（游戏化效应随时长衰减，跨年甚至为负 −0.20）。

**9. 交错练习要「先掌握、后交错」，并把理由讲给玩家**
- 做法：同一技能内部先 blocked（同类题集中练到 Proficient），跨技能复习阶段才 interleaved；进入交错阶段时用一句话解释「混着练是为了让你学会判断该用哪招」。
- 依据：**B3**（Brunmair & Richter 2019：总体 g=0.42，数学 g=0.34，但词汇类 blocked 更好 g=−0.39；只在「类间相似、类内不相似、材料复杂」时占优）、**B2**（Kornell & Bjork 2008：学习者**误以为**集中更有效，即使测完打脸 → 必须显式解释）、**A3**（Khan 的 Mastered 必须通过混合测评，是同一逻辑）。

**10. 抽象梯度：先「角色扮演一个机制」，再「写代码/公式」**
- 做法：每个难概念先给一个「你来当它」的关卡（你当调度器 / 你当页表 / 你当梯度下降），再用符号复现。
- 依据：**A6**（Deadlock Empire：扮演 Scheduler 让程序崩溃；CSEDU 2017 论文称它是当时唯一可在线玩的并发教学游戏，并指其「需要读懂代码」是局限）、**A8**（DragonBox 的「藏符号 → 逐步换回符号」；RCT 支持有效但存在迁移风险）、**A5-1**（HRM 用「办公室 = CPU、手 = 累加器」的具身隐喻）。

**11. 符号必须「显式换回来」，出口用纸笔式题目验证迁移**
- 做法：DragonBox 式图形关卡结束后，强制来一关「同样的题，但只给数字和字母」；综合练习题里至少 1/3 是符号化表述。
- 依据：**A8**（官方自述「little by little, the cards are replaced with numbers and variables」；但 ICLS 2023 指出效应「mixed」、机制不明 → 必须显式检验迁移）、**B1**（迁移与理解需要被测试，否则只是「感觉学会了」）。

**12. 可视化必须是「正文」而不是「配图」，每个可视化都要玩家先预测**
- 做法：每个可视化前插一个「你猜会发生什么」的二选一/滑块，然后再播放；可视化过程支持逐帧、可悬停查中间值。
- 依据：**A7**（TF Playground「Don't Worry, You Can't Break It」+ direct manipulation；Distill 的「可视化即正文」；CNN Explainer 逐层可点查）、**B1/B2**（预测 = 检索练习；预测错误 → 再看到正确答案，是生成效应 + 反馈的组合）。

### P2（锦上添花）

**13. 关卡是数据，不是代码**
- 做法：先定 schema（目标态 / 初始态 / 可用积木 / 判定器 / 提示链 / 知识点绑定 / 评分），让内容作者（甚至玩家）能写关卡。
- 依据：**A9-2**（Learn Git Branching 的 `build level` 命令 + 对话框引导建关）、**A9-3**（Oh My Git! 卡牌化把「动作」和「文档」都做成数据）。我们 192 技能 × 4–9 知识项 ≈ **1000–1700 个关卡单元**，硬编码必死。

**14. 提供「雾化 / 探索模式」，避免全图透明导致查表通关**
- 做法：默认只显示当前 tier 与下一步可达节点；可解锁「全图」但**不作为默认**；技能节点不写「最优顺序」。
- 依据：**A9-1**（Wikipedia：科技树会诱导玩家「memorize specific build orders」；SUPERJUMP 提到 Civ 系列早有 blind research 选项）、**A1-1**（Duolingo 官方：学习者常问「我是不是用错了方式」→ 过度自由也是负担，所以要有**受控的**迷雾而不是完全自由）。

**15. 元游戏「少而精」，奖励用「意义」而非「货币」**
- 做法：只保留 2–3 个元游戏元素（如「本技能掌握度」+「连续学习天数」+「今天复习到期数」）；徽章描述「你会了什么」（如「能解释为什么进程切换慢」），不发通用金币；**不做全服排行榜**或默认关闭。
- 依据：**A2**（Brilliant 官方：「We avoid packing too many game incentives into the product」，只保留 Streaks 与 Leagues）、**B7/Deci 1999**（有形/可预期奖励削弱内在动机；信息性正向反馈增强之）、**B7/Kim & Castelli 2021**（游戏化收益随持续时间衰减、跨年转负）。

**16. 给「已会的人」一条快速通道（但要留验证）**
- 做法：允许「跳级考试」：直接做该技能的综合练习题，过了就给 Proficient（不是 Mastered），并把它对应的知识项标为「待复习」交给 FSRS。
- 依据：**A1-1**（Duolingo 的教训：新版不允许跳到已会的部分，被用户批评）、**A1-5**（Medium 复盘：「不能跳到自己已会的部分」是主要抱怨）、**B4**（专家反转效应：给熟手讲他已经会的东西是负收益）。

**17. 难度曲线：把「读懂题意」的难度和「想出算法」的难度分开**
- 做法：题面用**最少的规则 + 最明确的判定**；复杂约束拆成渐进关卡；卡关时先给「换个说法重述题目」而不是直接给答案。
- 依据：**A5**（HRM 被 PC Gamer / Destructoid 同时批评「后半段缺乏讲解」、「既不彻底教学也不彻底挑战」；Zachtronics EXAPUNKS 被吐槽「一次只能取一张钞票」这类刁钻规则；nandgame 有玩家报告某关「impossible」）、**A5-2**（TIS-100「优化变成猜谜」）。

**18. 内容生产要有「可持续性」预案**
- 做法：别指望靠热情维护 1700 个关卡；考虑公共/公益资助、教师共创、开源关卡格式。
- 依据：**A9-3**（Oh My Git! 由德国 BMBF / Prototype Fund / OKF-DE 资助，官方页面自述「Our current funding will run out at the end of February」）、**A5-2**（Zachtronics 对公立学校免费授权的模式）。

---

## E. 明确「未查到」清单（避免后续被误引）

1. **Duolingo 官方专门解释「为什么移除 cracked skills」的独立文章/数据** —— 未查到。仅有 A1-1 官方博客中的一句括号说明。
2. **Duolingo streak / XP 对学习效果的量化研究** —— 未查到权威出处；本笔记只记录「存在广泛批评」这一事实。
3. **Brilliant 官方发布的学习效果数据（如「学完 X 提升 Y%」）** —— 未查到。仅有 WASC 认证（认证 ≠ 效果研究）。
4. **Brilliant「pretesting 为什么有效」的独立长文** —— 未查到（只有 About 页的结论句与博客的零散表述）。
5. **Khan Academy 掌握度阈值的官方文档正文** —— 帮助中心只给语义描述；**70% / 100% 的具体阈值出现在官方教学视频**中（A3-1 链接），非文档正文。
6. **Khan Academy 是否使用 FSRS/SM-2 类间隔排程的技术说明** —— 未查到。
7. **nandgame 官方关卡数、失败率、设计文档** —— 未查到（站点为 JS 应用，正文无法抓取，仅取到 meta description）。
8. **Turing Complete 官方关卡数、通关率、学习效果研究** —— 未查到。
9. **Deadlock Empire 官网给出的当前关卡数** —— 未查到（只有 2016 年 hackathon 提交页说的「16 关」，为开发期数字）。
10. **Human Resource Machine / 7 Billion Humans 官方关卡数** —— 未在本轮抓取中查到（官方页给了「11 条指令」但没有关卡数）。
11. **TensorFlow Playground 的官方发布日期** —— 未用一手来源核实（第三方博客称 2016 年 4 月，**未采信**）。可核实的是：论文为 ICML 2016 Workshop 版（正文 2016-05-17），arXiv 版本 2017-08-12。
12. **DragonBox 官方关卡数、留存率** —— 未查到。
13. **Kluger & DeNisi 1996 的具体效应量与「负向比例」** —— **未能抓到原文摘要**（APA 站点拒抓、Semantic Scholar 限流），故不引用数字，仅保留定性结论。
14. **Wouters et al. 2013 的具体效应量** —— 未核实，故不引用数字。
15. **Anki 何时把 FSRS 设为「所有用户默认开启」的官方公告** —— **未查到**。截至 2026-11-02 的官方手册仍写「Enable FSRS under the 'FSRS' section」，即**需显式开启**。
16. **ts-fsrs 6.0.0 之后的下一个稳定版** —— 抓取时 `latest` 即 6.0.0（2026-10-28 发布），无更新稳定版。
