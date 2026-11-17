# P.5.3 DevOps、持续交付与 SRE：覆盖表

**状态（2026-11-17）：已写完。** 依据 `../cs-math-skill-tree/data/outlines/P.5.3.json` 与 `../cs-math-skill-tree/output/outlines.json`，主来源为 *The Site Reliability Workbook*（ch1/2/4/5/8/9/10/11/14/16/17）、*Microsoft Learn DevOps resource center*、*SLSA v1.2*、*Reproducible Builds* 与 *OWASP CycloneDX SBOM Guide*。

必须前置仅为 `P.1.1 程序设计基础`（`P.2.4`、Linux、网络与威胁建模均为推荐而非强制前置）；因此诸如持续集成、`锁文件`、`分支`、镜像、YAML、`SLI`、`燃烧速率`、`构建溯源` 与 `SBOM` 等核心概念与术语均在本包内从零定义。内部章序（共 8 个全核心章节）：`1. CI/CD`、`2. 配置`、`3. 可观测性`、`4. SLO`、`5. 发布策略`、`6. 故障恢复与容量`、`7. 制品与依赖锁定`、`8. 构建溯源与软件物料清单`。

`node scripts/check-coverage.mjs P.5.3` 自动检查本表（注：内部节号按 `outlines.json` 顺排 1–21，不等同于原书章号）。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1 | A How SRE Relates to DevOps | `integrate` |
| 2.1 | A Why SREs Need SLOs | `indicator` |
| 2.2 | A What to Measure: Using SLIs | `indicator` |
| 2.3 | A Measuring the SLIs | `indicator` |
| 2.4 | A Calculating the SLIs | `indicator` |
| 2.5 | A Using the SLIs to Calculate Starter SLOs | `indicator` |
| 2.6 | A Choosing an Appropriate Time Window | `budget` |
| 2.7 | A Establishing an Error Budget Policy | `budget` |
| 2.8 | A Documenting the SLO and Error Budget Policy | `budget` |
| 2.9 | A Dashboards and Reports | `budget` |
| 3.1 | A Desirable Features of a Monitoring Strategy | `signals`、`monitor` |
| 3.2 | A Sources of Monitoring Data | `signals` |
| 3.3 | A Managing Your Monitoring System | `monitor` |
| 3.4.1 | A Intended Changes | `monitor` |
| 3.4.2 | A Dependencies | `monitor` |
| 3.4.3 | A Saturation | `monitor` |
| 3.4.4 | A Status of Served Traffic | `indicator`、`monitor` |
| 3.5 | A Implementing Purposeful Metrics | `monitor` |
| 3.6 | A Testing Alerting Logic | `monitor`、`burn` |
| 4.1.1 | A Precision | `burn` |
| 4.1.2 | A Recall | `burn` |
| 4.1.3 | A Detection time | `burn` |
| 4.1.4 | A Reset time | `burn` |
| 4.2.1 | A Target Error Rate ≥ SLO Threshold | `burn` |
| 4.2.2 | A Increased Alert Window | `burn` |
| 4.2.3 | A Incrementing Alert Duration | `burn` |
| 4.2.4 | A Alert on Burn Rate | `burn` |
| 4.2.5 | A Multiple Burn Rate Alerts | `burn` |
| 4.2.6 | A Multiwindow, Multi-Burn-Rate Alerts | `burn` |
| 4.3 | A Low-Traffic Services and Error Budget Alerting | `burn` |
| 4.4 | A Alerting at Scale | `burn` |
| 5 | A On-Call | `incident` |
| 6 | A Incident Response | `incident` |
| 7 | A Postmortem Culture: Learning from Failure | `incident` |
| 8 | A Managing Load | `capacity` |
| 9 | A Configuration Design and Best Practices | `config` |
| 10.1 | A Balancing Release Velocity and Reliability | `rollouts`、`canary` |
| 10.2 | A Separating Components That Change at Different Rates | `rollouts` |
| 10.3 | A Release Engineering and Canarying | `canary` |
| 10.4 | A Our Example Setup | `canary` |
| 10.5 | A Roll Forward Deployment Versus a Simple Canary Deployment | `canary` |
| 10.6 | A Canary Implementation | `canary` |
| 10.7 | A Minimizing Risk to SLOs and the Error Budget | `canary`、`budget` |
| 10.8 | A Choosing a Canary Population and Duration | `canary` |
| 10.9 | A Selecting and Evaluating Metrics | `canary` |
| 10.10 | A Dependencies and Isolation | `canary` |
| 10.11 | A Canarying in Noninteractive Systems | `canary` |
| 10.12 | A Requirements on Monitoring Data | `canary` |
| 10.13.1 | A Blue/Green Deployment | `rollouts` |
| 10.13.2 | A Artificial Load Generation | `canary` |
| 10.13.3 | A Traffic Teeing | `canary` |
| 11 | A Identifying and Recovering from Overload | `capacity` |
| 12.1 | B Use continuous integration | `integrate`、`workflow` |
| 12.2 | B Shift testing left with unit tests | `integrate`、`workflow` |
| 13.1 | B What is continuous delivery? | `integrate` |
| 13.2 | B What is infrastructure as code (IaC)? | `iac` |
| 13.3 | B Deploy to Azure infrastructure with GitHub Actions | `iac` |
| 13.4 | B Shift right to test in production | `canary` |
| 14.1 | B What is monitoring? | `monitor` |
| 14.2 | B Progressive experimentation with feature flags | `rollouts` |
| 14.3 | B Eliminate downtime through versioned service updates | `rollouts` |
| 14.4 | B How Microsoft operates reliable systems with DevOps | `integrate`、`incident` |
| 15.1 | C What is SLSA? | `provenance` |
| 15.2 | C Why SLSA is needed | `provenance` |
| 15.3 | C SLSA in layperson's terms | `provenance` |
| 15.4 | C Who is SLSA for? | `provenance` |
| 15.5 | C How SLSA works | `provenance` |
| 15.6 | C What SLSA doesn't cover | `provenance` |
| 16.1 | C Build levels | `provenance` |
| 16.2 | C Security Best Practices | `provenance` |
| 16.3 | C Producer | `provenance` |
| 16.4 | C Choose an appropriate build platform | `provenance` |
| 16.5 | C Follow a consistent build process | `repro`、`provenance` |
| 16.6 | C Distribute provenance | `provenance` |
| 16.7 | C Build Platform | `provenance` |
| 16.8 | C Provenance generation | `provenance` |
| 16.9 | C Isolation strength | `provenance` |
| 17.1 | C Build provenance | `provenance` |
| 17.2 | C Source provenance | `provenance` |
| 18.1 | D Variations in the build environment | `repro` |
| 18.2 | D SOURCE_DATE_EPOCH | `repro` |
| 18.3 | D Volatile inputs can disappear | `repro` |
| 18.4 | D Stable order for inputs | `repro` |
| 18.5 | D Stripping of unreproducible information | `repro` |
| 18.6 | D Version information | `repro` |
| 18.7 | D Timestamps | `repro` |
| 18.8 | D Timezones | `repro` |
| 18.9 | D Locales | `repro` |
| 18.10 | D Archive metadata | `repro` |
| 18.11 | D Stable order for outputs | `repro` |
| 18.12 | D Randomness | `repro` |
| 18.13 | D Build path | `repro` |
| 18.14 | D System images | `repro` |
| 19.1 | D What's in a build environment? | `repro` |
| 19.2 | D Recording the build environment | `repro` |
| 19.3 | D Definition strategies | `repro` |
| 19.4 | D Proprietary operating systems | `repro` |
| 20.1 | E BOM Identity | `sbom` |
| 20.2 | E The Anatomy of a CycloneDX BOM | `sbom` |
| 20.3 | E Serialization Formats | `sbom` |
| 21.1 | E NTIA Minimum Elements | `sbom` |
| 21.2 | E SCVS BOM Maturity Model | `sbom` |
| 21.3 | E SBOM Quality | `sbom` |

## CS2023 核心主题（C2）

`scope.json` 在 `P.5.3` 的 8 个章节中共匹配 6 个 CS2023 主题（`SLO` 与 `故障恢复与容量` 无对应 CS2023 条目，属 SRE 行业实践补充）：

| 知识点 | KA / 要求 | 课 |
|---|---|---|
| CI/CD | SE-Construction · KA Core（DevOps practices） | `integrate`、`workflow` |
| 配置 | SE-Tools · CS Core（Software configuration management） | `config`、`iac` |
| 可观测性 | SE-Reliability · KA Core（telemetry, monitoring and alerting） | `signals`、`monitor`、`burn` |
| 发布策略 | SE-Tools · KA Core（Release management） | `rollouts`、`canary` |
| 制品与依赖锁定 | SE-Tools · KA Core（Dependency management） | `locks`、`repro` |
| 构建溯源与软件物料清单 | SE-Tools / SEC-Engineering · KA Core（Build systems; software signing and verification） | `provenance`、`sbom` |

## 学习路径与综合练习（C3 / D2）

- 对应 `learning-paths/P.5.3.json` 全部 8 个学习模块（中英双语资源 `status = complete`）：SRE Workbook（SLI/SLO/告警/金丝雀/配置/过载）、OpenTelemetry 观测信号（Logs/Metrics/Traces）、12-Factor Config（环境变量配置分离）、MS Learn DevOps 与 IaC、Fowler CI/CD、Reproducible Builds、SLSA v1.2 构建溯源与 CycloneDX/SPDX SBOM。
- **综合练习 6 问映射**：(1) GitHub Actions `on.push.branches: ["main"]`、`permissions: {contents: read}` 与 checkout/setup-python/pytest/docker build → `workflow`；(2) 持续集成 vs 持续交付 vs 持续部署与蓝绿/金丝雀 → `integrate`、`rollouts`、`canary`；(3) 30 天 99.9% SLO（预算 `43.2` 分钟、已用 `30` 分钟余 `13.2` 分钟及耗尽冻结政策）→ `indicator`、`budget`；(4) 日志/指标/追踪三支柱与 `燃烧速率` 告警 + 低流量窗口适配 → `signals`、`monitor`、`burn`；(5) 可复现构建七项受控输入与“构建不一致不能单独证明恶意篡改” → `repro`、`provenance`；(6) `pip install --require-hashes`、`npm ci` 与 SBOM 漏洞盘点 → `locks`、`sbom`。
- **与前后站衔接**：前端镜像/容器构建流水线交接给推荐后续 `C.2.3 容器、编排与虚拟化`（在 `workflow`、`repro`）；`locks`/`provenance`/`sbom` 也与安全工程线 `S.3.2` 呼应。
