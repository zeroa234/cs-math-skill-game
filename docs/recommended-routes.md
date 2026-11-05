# 推荐远征怎么选（2026-11-03）

用户要求：“操作系统”是用户自己选的远征（我的远征），其余推荐路线要“结合实际”。下面是选方向的规则、每条路线的目标技能是怎么从公开路线图推出来的，以及没收进来的东西。数据在 `data/routes.yaml`，调研原文在 [reports/research/routes/](../reports/research/routes/)（pi 抓取，主代理核对过关键数字；Stack Overflow 和 BLS 的数字见 so-bls.md）。

推荐路线要等路线上每一站的课都按零基础和知识覆盖面两条标准（`docs/content-authoring.md`）重写好再开放。已开放：算法（2026-11-04）；其余 7 条开发中。重写按站进行，一个技能的课写好后，所有经过它的路线共用。

## 1. 选哪些方向

两个来源，满足一个就收：

1. **现在做这行的人多**：Stack Overflow 2025 开发者调查“Developer roles”一题（43,560 人作答，<https://survey.stackoverflow.co/2025/developers>）里占 2% 以上的职业。学生、退休、其他、管理层、创始人、教育者、学术研究者、架构师不算入门职业方向，不参与。前端、后端、全栈合成“网站开发”。
2. **岗位在快速增长**：美国劳工统计局 Occupational Outlook Handbook（2025 年数据，2025–2035 预测）里“much faster than average”且岗位超过 10 万的计算机职业。

另加“算法”：它不是职业方向，而是各方向共用的基本功（F.1.2 的 9 个知识点全部属于 ACM/IEEE CS2023 的核心主题）。

| 方向 | 依据 | 路线 |
|---|---|---|
| 网站开发 | SO：全栈 27%、后端 14.2%、前端 4.3% | web |
| 企业与桌面应用 | SO：4.3% | enterprise |
| 手机应用 | SO：3% | mobile |
| 嵌入式 | SO：2.8% | embedded |
| DevOps | SO：2.3%（系统管理员、云基础设施各约 1%） | devops |
| 数据科学 / AI | BLS 数据科学家：27.56 万岗位，+35%；SO 里 AI/ML 工程师、数据科学家等合计 3.7% | ai |
| 网络安全 | BLS 信息安全分析师：19.29 万岗位，+21%；SO 里 1.1% | security |
| 算法 | CS2023 核心 | algo |

没收的：游戏/图形（SO 0.9%）、测试（0.8%）、数据工程师（1.7%）、数据分析师（0.9%）；BLS 的“软件开发者、测试人员”（190.54 万岗位，+10%）由网站、企业、手机三条覆盖。原来的“高性能网络”（C.3.5）不是多数初学者的方向，它的 7 站包含操作系统路线全部 5 站，算是“我的远征”走完后的延伸；“自己定目标”开放后可以直接选它。

## 2. 每条路线要到哪些技能

规则：

1. 用这个职业在 roadmap.sh 上的路线图；roadmap.sh 有“初学者版”就用初学者版（只有后端、前端、DevOps 有）。嵌入式用 GitHub 上的 Embedded Engineering Roadmap（13,761 star），只取它标成 required 的主题，不取“软技能”一栏（其他路线图都不含软技能，口径统一）。
2. 路线图的每个顶层主题（标了可选、备选、“继续学习”的不算）对应到技能树里讲它的技能；一个主题横跨几个技能时，取覆盖它下面子主题最多的那个。
3. 技能树里没有的（办公软件、测试仪器、具体厂商的服务）记为“不在树里”，不收。
4. 这些技能就是路线的目标；站点是目标的全部必须前置，由 `planRoute` 推出。

| 路线 | 路线图 | 主题 → 技能 | 站数 |
|---|---|---|---|
| web | roadmap.sh backend-beginner（8 个主题）+ frontend-beginner（9 个） | 语言 → P.1.1；Git、GitHub、npm → P.2.4；HTML、CSS、JavaScript、React、Tailwind、API（REST、JSON）→ P.5.1；认证、JWT → S.3.1；关系数据库 → D.1.1；“More about Databases”（ORM、ACID、事务、N+1）→ D.1.2（树里事务和执行计划在数据库内核）；缓存（Redis）→ D.1.3（键值数据模型）；测试、Vitest → P.4.5 | 10 |
| enterprise | roadmap.sh java（20 个，全部核心）+ software-design-architecture（9 个核心，4 个灰色不收） | Java 基础、异常、注解、模块、Optional、日期、正则、I/O、文件、并发 → P.1.2；Lambda、编程范式 → P.1.3；依赖注入、整洁代码、设计原则、设计模式 → P.4.3；架构风格、原则、模式、企业模式 → P.4.4；数据库访问 → D.1.1；Web 框架、网络 → P.5.1；构建工具 → P.2.4；测试 → P.4.5；文档 → P.4.1；日志框架 → P.5.3（可观测性）。不收：Cryptography（树里只有密码学原理 S.1.2，路线图要的是调用加密库，层次不同） | 11 |
| mobile | roadmap.sh android（15 个，无标记） | 语言（Kotlin、Java）→ P.1.2；基础、组件、界面与导航、存储、常用服务、发布 → P.5.2；Git、Lint、调试 → P.2.4；设计与架构（MVVM、模式、依赖注入）→ P.4.3；网络（Retrofit、OkHttp）→ P.5.1；异步（协程、线程）→ P.1.4；安全 → S.2.3；测试 → P.4.5 | 9 |
| embedded | Embedded Engineering Roadmap `explorer/map.json`（36 个 required） | C → P.2.2；算法与数据结构 → F.1.1、F.1.2；设计模式 → P.4.3；状态机、数字设计 → H.1.2；内存管理 → P.2.2；JTAG、GDB、Git、GCC、Make → P.2.4；TDD、单元测试 → P.4.5；RTOS 基础 → H.3.2；GPIO、ADC、定时器、PWM、中断、DMA 等 → H.3.1；UART、I2C、SPI → H.3.3；数学与微积分、电路、电子学 → H.1.1（它要先学微积分和线性代数）；计算机体系结构 → C.1.2。不在树里：万用表、逻辑分析仪 | 20 |
| devops | roadmap.sh devops-beginner（11 个） | 语言 → P.1.1；操作系统、Linux → C.2.1；网络与协议 → C.3.2；Docker → C.2.3；Git、GitHub → P.2.4；AWS → C.4.2；Terraform、Ansible、GitHub Actions → P.5.3；Nginx → P.5.1 | 12 |
| ai | roadmap.sh ai-data-scientist（1–8 号；9、10 号是“继续学习”，不收） | 数学 → M.3.1、M.1.4.1（已在前置里）；统计 → M.6.2；计量经济 → M.6.2.2（回归）；编程 → P.2.3；探索分析 → D.3.1；机器学习 → A.2.1；深度学习 → A.2.3；MLOps → A.4.1 | 14 |
| security | roadmap.sh cyber-security（6 个，全部核心） | IT 基础（硬件、连接、排错）→ C.1.1（证书、CTF、办公软件不在树里）；操作系统 → C.2.1（虚拟化子主题属于 C.2.3，覆盖较少）；网络知识 → C.3.2；安全技能（157 个子主题，防火墙、IDS/IPS、加固、安全协议、网络攻击最多）→ S.2.2；云 → C.4.2；编程 → P.1.1 | 9 |
| algo | —（基本功） | 目标 F.1.2 | 4 |

站数会随技能树的前置关系变化，以游戏里显示的为准（单元测试检查每条路线覆盖全部目标、站序满足全部前置）。

## 3. 我的远征和自己定目标

“我的远征”（`routes.yaml` 的 `own`）和玩家自己定的目标走同一条代码：路线 id 都是 `goal:<技能>`，介绍由 `src/game/core/route-text.js` 从技能树写出（终点要学的章、前面各站按领域分组、对照的大学课程），背景图按目标所在领域取（`src/game/app/art.js`，每个领域一张，见 `assets/bg/README.md`）。所以任何技能当目标，都有一张合适的图和一段说得清的介绍，不用人工逐个写。

“自己定目标”（`customGoals`）目前是开发中：入口显示为灰色，选择列表收起。固定目标、当前远征和开放自选后的保存规则见[设计说明](design.md#我的远征和当前远征)。
