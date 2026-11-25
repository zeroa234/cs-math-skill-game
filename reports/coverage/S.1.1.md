# S.1.1 安全原理、威胁建模与风险：覆盖表

**状态（2026-11-22）：已写完。** 依据 `vendor/cs-math-skill-tree/output/outlines.json` 与 `vendor/cs-math-skill-tree/output/skilltree.json`，主来源为 UC Berkeley CS 161 *Computer Security* 第 1 章（Security Principles）与 Ross Anderson *Security Engineering* 第 1.5 节（Definitions）、第 3 章（Passwords）和第 4 章（Access Controls），并对照中科大《信息安全导论》、Microsoft Learn STRIDE、最小特权原则教程、CERNET 高校攻击面管理实践与香港政府《信息技术安全风险管理实务指南》补齐授权模型、STRIDE 威胁建模、最小权限落地、攻击面收缩与 SLE/ALE 风险量化。

游戏内部章序：`1. 机密性/完整性/可用性`、`2. 认证授权`、`3. 最小权限`、`4. 攻击面与风险管理`。本技能的唯一必须前置是 `P.1.1`（程序设计基础）；操作系统、计算机网络与体系结构仅为推荐前置，因此凡涉及内存、内核、并发与竞态条件、原子操作等概念均在本包从零定义。

`node scripts/check-coverage.mjs S.1.1` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | 1.1 Know your threat model | `threat-modeling-and-stride`, `attack-surface-reduction` |
| 1.2 | 1.2 Consider Human Factors | `password-psychology-and-systems` |
| 1.3 | 1.3 Security is economics | `attack-surface-reduction`, `risk-economics-and-quantification` |
| 1.4 | 1.4 Detect if you can't prevent | `detect-respond-and-governance` |
| 1.5 | 1.5 Defense in depth | `security-design-principles` |
| 1.6 | 1.6 Least privilege | `least-privilege-and-separation` |
| 1.7 | 1.7 Separation of responsibility | `least-privilege-and-separation` |
| 1.8 | 1.8 Ensure complete mediation | `mediation-defaults-and-tcb` |
| 1.9 | 1.9 Shannon's Maxim | `security-design-principles` |
| 1.10 | 1.10 Use fail-safe defaults | `mediation-defaults-and-tcb` |
| 1.11 | 1.11 Design security in from the start | `security-design-principles` |
| 1.12 | 1.12 The Trusted Computing Base (TCB) | `mediation-defaults-and-tcb` |
| 1.13 | 1.13 TOCTTOU Vulnerabilities | `tocttou-vulnerabilities` |
| 2 | 1.5 Definitions | `cia-triad` |
| 3.1 | 3.1 Basics | `authn-and-mfa` |
| 3.2 | 3.2 Applied Psychology Issues | `password-psychology-and-systems` |
| 3.3 | 3.3 System Issues | `password-psychology-and-systems` |
| 3.4 | 3.4 Technical Protection of Passwords | `password-protection` |
| 3.5 | 3.5 Summary | `password-protection` |
| 4.1 | 4.1 Introduction | `access-control-models` |
| 4.2 | 4.2 Operating System Access Controls | `access-control-models` |
| 4.3 | 4.2.1 Groups and Roles | `access-control-models` |
| 4.4 | 4.2.2 Access Control Lists | `access-control-models` |
| 4.5 | 4.2.5 Capabilities | `access-control-models` |
| 4.6 | 4.2.7 Granularity | `granularity-sandbox-and-pitfalls` |
| 4.7 | 4.2.8 Sandboxing and Proof-Carrying Code | `granularity-sandbox-and-pitfalls` |
| 4.8 | 4.3 Hardware Protection | `granularity-sandbox-and-pitfalls` |
| 4.9 | 4.4 What Goes Wrong | `granularity-sandbox-and-pitfalls` |
| 4.10 | 4.5 Summary | `granularity-sandbox-and-pitfalls` |

## 核心主题（C2）

对照 ACM/IEEE CS2023 安全核心主题（SEC）与 CE2016 信息安全（SEC）：

| 知识点 | 对应主题 | 课 |
|---|---|---|
| 机密性/完整性/可用性 | CIA 三要素、真实性、不可抵赖性、可控性、安全策略与机制、纵深防御、香农准则与内生安全 | `cia-triad`、`security-design-principles` |
| 认证授权 | 认证与授权区分、多因素认证、口令心理学与熵、加盐慢哈希、访问控制矩阵、ACL 与能力、DAC/MAC/RBAC/ABAC、粒度、沙箱与硬件隔离 | `authn-and-mfa`、`password-psychology-and-systems`、`password-protection`、`access-control-models`、`granularity-sandbox-and-pitfalls` |
| 最小权限 | 最小权限原则与落地机制（RBAC/JIT/零信任）、职责分离、完全中介、失效安全默认值、可信计算基（TCB）、TOCTTOU 竞态漏洞 | `least-privilege-and-separation`、`mediation-defaults-and-tcb`、`tocttou-vulnerabilities` |
| 攻击面与风险管理 | 威胁模型、信任边界、STRIDE 分类法、攻击面梳理与暴露面收缩、安全经济学、SLE/ALE 量化与四类风险处置、预防-检测-响应闭环与 KRI/KPI | `threat-modeling-and-stride`、`attack-surface-reduction`、`risk-economics-and-quantification`、`detect-respond-and-governance` |

## 学习资源的章节（C3）

| 来源 | 章节与概念 | 课 / 说明 |
|---|---|---|
| `en1` CS 161 Ch. 1 | 1.1–1.13 全部安全原则与 TOCTTOU 漏洞 | 分散在 `security-design-principles`、`password-psychology-and-systems`、`least-privilege-and-separation`、`mediation-defaults-and-tcb`、`tocttou-vulnerabilities`、`threat-modeling-and-stride`、`attack-surface-reduction`、`risk-economics-and-quantification`、`detect-respond-and-governance` |
| `B` Ross Anderson *Security Engineering* | 1.5 Definitions、Ch. 3 Passwords（3.1–3.5）、Ch. 4 Access Controls（4.1–4.5） | 对应 `cia-triad`、`authn-and-mfa`、`password-psychology-and-systems`、`password-protection`、`access-control-models`、`granularity-sandbox-and-pitfalls` |
| `zh1` 中科大《信息安全导论》 | CIA 扩展属性（真实性、不可抵赖性、可控性）、Kerberos 与 PKI 认证思路、DAC/MAC/RBAC/ABAC 模型 | 对应 `cia-triad`、`authn-and-mfa`、`access-control-models` |
| `zh3` Microsoft Learn | STRIDE 六类威胁与信任边界威胁建模 | 对应 `threat-modeling-and-stride` |
| `r7-zh1` 最小特权原则教程 | 最小权限的定义、作用、RBAC/JIT/特权隔离/零信任落地、清理冗余与硬编码凭据、权限漂移 | 对应 `least-privilege-and-separation`、`granularity-sandbox-and-pitfalls` |
| `r7-zh2` 高校攻击面管理实践 | 外部与内部资产梳理、漏洞优先级评估（VPT）、按门户/API/服务器/终端收缩暴露面、蜜罐与攻击面混淆 | 对应 `attack-surface-reduction` |
| `r7-zh3` 信息技术安全风险管理实务指南 | 风险背景、风险偏好与承受能力、资产-威胁-漏洞-可能性-影响五要素、四类风险处置、残余风险、KPI/KRI 监察 | 对应 `risk-economics-and-quantification`、`detect-respond-and-governance` |

## 综合练习（C4）

| 小题 | 要用到的 | 课 |
|---|---|---|
| (1) 以“校园一卡通系统”为例，举出破坏机密性、完整性、可用性的威胁 | CIA 三要素定义及具体场景对应 | `cia-triad` |
| (2) 用 STRIDE 对“用户上传头像”做威胁建模及缓解措施 | STRIDE 六类威胁、EXIF 元数据清除、随机文件名、重编码与不可执行目录、限流限大小、审计日志 | `threat-modeling-and-stride` |
| (3) 认证和授权区别；多因素认证三类因素；最小权限与纵深防御举例 | 认证 vs 授权、MFA 三因素、最小权限与纵深防御的定义与工程实例 | `security-design-principles`、`authn-and-mfa`、`least-privilege-and-separation` |
| (4) 资产 50 万、暴露因子 40%、ARO=0.5 求 SLE 与 ALE；3 万控制降 ARO 至 0.1 是否值得 | SLE = AV × EF、ALE = SLE × ARO、控制前后净收益对比 | `risk-economics-and-quantification` |
| (5) 举出三种缩小攻击面的方法 | 关多余服务与端口、删不用功能与默认账号、后台限内网/VPN、精简并更新第三方依赖 | `attack-surface-reduction` |

## 后继技能（C5）

本技能有 4 个必须后继技能（尚无互动课，对照其大纲与综合练习核对衔接）：

| 后继技能 | 直接用到的概念与方法 | 本包对应课 |
|---|---|---|
| `S.2.4` 云安全与容器安全 | 最小权限授权、RBAC、配置错误与硬编码凭据根源、审计日志排查可疑调用 | `access-control-models`、`granularity-sandbox-and-pitfalls`、`least-privilege-and-separation`、`detect-respond-and-governance` |
| `S.4.1` 渗透测试、道德黑客与反制 | 资产梳理、暴露面与资产价值优先级排序、威胁识别与授权边界意识 | `threat-modeling-and-stride`、`attack-surface-reduction`、`risk-economics-and-quantification` |
| `S.4.2` 计算机取证与事件响应 | 预防-检测-响应-恢复闭环、不可抵赖性、集中异地审计日志防篡改与时间戳完整性 | `cia-triad`、`detect-respond-and-governance` |
| `S.4.4` 安全运营、检测与攻防评估 | 暴力破解与密码喷洒的区分、失败次数与告警误报/漏报权衡、检测度量（MTTD/MTTR） | `password-psychology-and-systems`、`detect-respond-and-governance` |
