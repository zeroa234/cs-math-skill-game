# I.2.1 计算伦理、社会影响与专业责任：覆盖表

**状态（2026-11-22）：已写完。** 依据 `vendor/cs-math-skill-tree/output/outlines.json` 与 `vendor/cs-math-skill-tree/output/skilltree.json`，主来源为 Michael J. Quinn *Ethics for the Information Age*（第 4–6、8–10 章）、Barocas / Hardt / Narayanan *Fairness and Machine Learning*（第 2–4 章）及 Green Software Foundation *Green Software Practitioner*（碳效率与碳感知两个模块），并补充对照上海交通大学 CS3309、MIT 6.805 及 OpenStax *Introduction to Intellectual Property*。

游戏内部章序：`1. 隐私`、`2. 知识产权`、`3. 偏见`、`4. 可持续性`、`5. 责任与公共利益`。本技能无必须前置，所有概念均从零讲起。

`node scripts/check-coverage.mjs I.2.1` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | 4.2 Intellectual Property Rights | `ip-four-pillars` |
| 1.2 | 4.3 Protecting Intellectual Property | `ip-four-pillars` |
| 1.3 | 4.4 Fair Use | `fair-use-and-drm` |
| 1.4 | 4.5 New Restrictions on Use | `fair-use-and-drm` |
| 1.5 | 4.6 Peer-to-Peer Networks and Cyberlockers | `fair-use-and-drm` |
| 1.6 | 4.7 Protections for Software | `ip-four-pillars` |
| 1.7 | 4.8 Open-Source Software | `open-source-and-cc` |
| 1.8 | 4.9 Legitimacy of Intellectual Property Protection for Software | `fair-use-and-drm` |
| 1.9 | 4.10 Creative Commons | `open-source-and-cc` |
| 2.1 | 5.2 Perspectives on Privacy | `privacy-frameworks` |
| 2.2 | 5.3 Information Disclosures | `disclosure-and-consent` |
| 2.3 | 5.4 Data Mining | `reidentification-and-mining` |
| 2.4 | 5.5 Examples of Consumer Backlash | `disclosure-and-consent` |
| 3.1 | 6.2 US Legislation Restricting Information Collection | 不教：属美国国内特定历史时期的隐私立法明细，具体法规须依地区与时间另行核验；政府信息收集的通用分析原则在 `government-surveillance` 讲授 |
| 3.2 | 6.3 Information Collection by the Government | `government-surveillance` |
| 3.3 | 6.4 Covert Government Surveillance | `government-surveillance` |
| 3.4 | 6.5 US Legislation Authorizing Wiretapping | 不教：属美国国内窃听授权法条演进明细，具体法规须依地区与时间另行核验；监控授权与制衡框架在 `government-surveillance` 讲授 |
| 3.5 | 6.6 USA PATRIOT Act | 不教：属美国 2001 年特定法案条文细节，具体法规须依地区与时间另行核验；紧急权扩张与隐私监督的通用权衡在 `government-surveillance` 讲授 |
| 3.6 | 6.7 Regulation of Public and Private Databases | `government-surveillance` |
| 3.7 | 6.8 Data Mining by the Government | `government-surveillance` |
| 3.8 | 6.9 National Identification Card | 不教：属美国国内关于统一身份证件的特定政策争论，依地区国情差异较大；集中式身份数据库的风险在 `government-surveillance` 顺带说明 |
| 3.9 | 6.10 Information Dissemination | `government-surveillance` |
| 3.10 | 6.11 Invasion | `government-surveillance` |
| 4.1 | 8.2 Data Entry or Data Retrieval Errors | `software-failures` |
| 4.2 | 8.3 Software and Billing Errors | `software-failures` |
| 4.3 | 8.4 Notable Software System Failures | `software-failures` |
| 4.4 | 8.5 Therac-25 | `software-failures` |
| 4.5 | 8.6 Computer Simulations | `software-failures` |
| 4.6 | 8.7 Software Engineering | `engineering-and-liability` |
| 4.7 | 8.8 Software Warranties and Vendor Liability | `engineering-and-liability` |
| 5.1 | 9.2 How Well Developed Are the Computing Professions? | `professional-ethics-whistleblowing` |
| 5.2 | 9.3 Software Engineering Code of Ethics | `professional-ethics-whistleblowing` |
| 5.3 | 9.4 Analysis of the Code | `professional-ethics-whistleblowing` |
| 5.4 | 9.5 Case Studies | `professional-ethics-whistleblowing` |
| 5.5 | 9.6 Whistle-Blowing | `professional-ethics-whistleblowing` |
| 6.1 | 10.2 Automation and Employment | `work-wealth-public-interest` |
| 6.2 | 10.3 Workplace Changes | `work-wealth-public-interest` |
| 6.3 | 10.4 Globalization | `work-wealth-public-interest` |
| 6.4 | 10.5 The Digital Divide | `work-wealth-public-interest` |
| 6.5 | 10.6 The Winner-Take-All Society | `work-wealth-public-interest` |
| 7.1 | Machine learning is not a replacement for human decision making | `automation-legitimacy` |
| 7.2 | Bureaucracy as a bulwark against arbitrary decision making | `automation-legitimacy` |
| 7.3 | Three Forms of Automation | `automation-legitimacy` |
| 7.4 | Mismatch between target and goal | `targets-proxies-recourse` |
| 7.5 | Failing to consider relevant information | `targets-proxies-recourse` |
| 7.6 | The limits of induction | `targets-proxies-recourse` |
| 7.7 | A right to accurate predictions? | `targets-proxies-recourse` |
| 7.8 | Agency, recourse, and culpability | `targets-proxies-recourse` |
| 8.1 | Modeling populations as probability distributions | `classification-and-groups` |
| 8.2 | Formalizing classification | `classification-and-groups` |
| 8.3 | Supervised learning | `classification-and-groups` |
| 8.4 | Groups in the population | `classification-and-groups` |
| 8.5 | Statistical non-discrimination criteria | `fairness-criteria` |
| 8.6 | Independence | `fairness-criteria` |
| 8.7 | Separation | `fairness-criteria` |
| 8.8 | Sufficiency | `fairness-criteria` |
| 8.9 | How to satisfy a non-discrimination criterion | `fairness-criteria` |
| 8.10 | Relationships between criteria | `fairness-criteria` |
| 8.11 | Case study: Credit scoring | `fairness-criteria` |
| 9.1 | Systematic relative disadvantage | `relative-fairness` |
| 9.2 | Six accounts of the wrongfulness of discrimination | `relative-fairness` |
| 9.3 | Intentionality and indirect discrimination | `relative-fairness` |
| 9.4 | Equality of opportunity | `relative-fairness` |
| 9.5 | Tensions between the different views | `relative-fairness` |
| 9.6 | Merit and desert | `relative-fairness` |
| 9.7 | The cost of fairness | `relative-fairness` |
| 10.1 | Global warming vs climate change | `carbon-and-greenhouse` |
| 10.2 | Climate vs weather | `carbon-and-greenhouse` |
| 10.3 | Greenhouse gases and the greenhouse effect | `carbon-and-greenhouse` |
| 10.4 | Carbon and CO2eq | `carbon-and-greenhouse` |
| 11.1 | Carbon intensity | `carbon-intensity` |
| 11.2 | Variability of carbon intensity | `carbon-intensity` |
| 11.3 | Dispatchability & curtailment | `carbon-intensity` |
| 11.4 | Marginal carbon intensity | `carbon-intensity` |
| 11.5 | Demand shifting | `demand-shifting-shaping` |
| 11.6 | Spatial shifting | `demand-shifting-shaping` |
| 11.7 | Temporal shifting | `demand-shifting-shaping` |
| 11.8 | Demand shaping | `demand-shifting-shaping` |

## 核心主题（C2）

对照 ACM/IEEE CE2016 职业实践准备（PPP）与 CS2023 社会与专业实践（SEP）：

| 知识点 | 对应主题 | 课 |
|---|---|---|
| 隐私 | Privacy & civil liberties、政府与企业信息收集、知情同意与再识别 | `privacy-frameworks`、`disclosure-and-consent`、`reidentification-and-mining`、`government-surveillance` |
| 知识产权 | Intellectual property、开源许可与知识共享、合理使用与 DRM | `ip-four-pillars`、`fair-use-and-drm`、`open-source-and-cc` |
| 偏见 | Algorithmic fairness、自动化决策正当性、统计非歧视判据与不可兼得、相对公平观 | `automation-legitimacy`、`targets-proxies-recourse`、`classification-and-groups`、`fairness-criteria`、`relative-fairness` |
| 可持续性 | Sustainability、温室效应与 CO2eq、碳强度与碳感知计算 | `carbon-and-greenhouse`、`carbon-intensity`、`demand-shifting-shaping` |
| 责任与公共利益 | Reliability & liability、ACM/IEEE 专业伦理准则、吹哨与社会影响 | `software-failures`、`engineering-and-liability`、`professional-ethics-whistleblowing`、`work-wealth-public-interest` |

## 学习资源的章节（C3）

| 来源 | 章节与概念 | 课 / 说明 |
|---|---|---|
| `zh1` 上交 CS3309 | CE07 技术变革、CE08 专业责任、CE09 指导准则、CE11 自由尊重、CE12 隐私保护、CE13 公平公正、CE15 产权利益 | 对应第 1、2、3、5 章各课 |
| `en1` MIT 6.805 | Unit A 政策制定与法律结构、Unit B 监控与画像风险、Unit C 匿名与个人信息 | 对应 `privacy-frameworks`、`disclosure-and-consent`、`reidentification-and-mining`、`government-surveillance`、`targets-proxies-recourse` |
| `r7-en1` OpenStax IP | 专利、版权、商标、商业秘密四类保护对象与条件 | 对应 `ip-four-pillars`、`fair-use-and-drm`、`open-source-and-cc` |
| `r7-en2` fairmlbook | 第 2–4 章自动化决策、分类与统计非歧视判据、相对公平观 | 对应 `automation-legitimacy`、`targets-proxies-recourse`、`classification-and-groups`、`fairness-criteria`、`relative-fairness` |
| `zh2` / `en2` Green Software Practitioner | 碳效率（全球变暖/气候变化/温室气体/CO2eq）与碳感知（碳强度/弃电/边际碳强度/需求转移与塑形） | 对应 `carbon-and-greenhouse`、`carbon-intensity`、`demand-shifting-shaping` |

## 综合练习（C4）

| 小题 | 要用到的 | 课 |
|---|---|---|
| (1) 用后果主义、义务论、美德伦理分析 App 公司是否应出售用户位置数据 | 三种伦理框架的定义、权衡维度与位置数据风险 | `privacy-frameworks` |
| (2) “告知与同意”的局限；为何去掉姓名仍可能被再识别 | 隐私政策冗长/捆绑/未来用途不可预见/一次性同意；准标识符组合与位置轨迹再识别 | `disclosure-and-consent`、`reidentification-and-mining` |
| (3) 招聘简历筛选模型对女性评分系统性偏低的来源与治理措施 | 历史偏见、样本不足、代理特征、目标标签偏差；群体审计、去代理/补数据、人工复核与申诉、无法消除则停用 | `targets-proxies-recourse`、`classification-and-groups`、`fairness-criteria`、`relative-fairness` |
| (4) 版权、专利、商业秘密的区别；GPL 与 MIT 的区别；商业使用开源代码注意事项 | 四类 IP 保护对象与失效条件；强著佐权 vs 宽松许可 vs AGPL；SBOM、署名与兼容性核查 | `ip-four-pillars`、`open-source-and-cc` |
| (5) ACM 职业道德准则核心原则；上级要求隐瞒已知安全缺陷时应如何应对 | 公共利益优先与核心条款；书面评估风险、逐级向安全合规反映、保留记录、必要时依法向监管报告而不泄密 | `professional-ethics-whistleblowing` |

## 后继技能（C5）

本技能在技能树中没有必须后继（`unlocks: []`），是计算机工程推荐远征中对应 CE2016 职业实践准备（PPP）的独立基石站。
