# P.5.3 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1 | How SRE Relates to DevOps | `integrate` |
| 2.1 | Why SREs Need SLOs | `indicator` |
| 2.2 | What to Measure: Using SLIs | `indicator` |
| 2.3 | Measuring the SLIs | `indicator` |
| 2.4 | Calculating the SLIs | `indicator` |
| 2.5 | Using the SLIs to Calculate Starter SLOs | `indicator` |
| 2.6 | Choosing an Appropriate Time Window | `budget` |
| 2.7 | Establishing an Error Budget Policy | `budget` |
| 2.8 | Documenting the SLO and Error Budget Policy | `budget` |
| 2.9 | Dashboards and Reports | `budget` |
| 3.1 | Desirable Features of a Monitoring Strategy | `signals`, `monitor` |
| 3.2 | Sources of Monitoring Data | `signals` |
| 3.3 | Managing Your Monitoring System | `monitor` |
| 3.4.1 | Intended Changes | `monitor` |
| 3.4.2 | Dependencies | `monitor` |
| 3.4.3 | Saturation | `monitor` |
| 3.4.4 | Status of Served Traffic | `indicator`, `monitor` |
| 3.5 | Implementing Purposeful Metrics | `monitor` |
| 3.6 | Testing Alerting Logic | `monitor`, `burn` |
| 4.1.1 | Precision | `burn` |
| 4.1.2 | Recall | `burn` |
| 4.1.3 | Detection time | `burn` |
| 4.1.4 | Reset time | `burn` |
| 4.2.1 | Target Error Rate ≥ SLO Threshold | `burn` |
| 4.2.2 | Increased Alert Window | `burn` |
| 4.2.3 | Incrementing Alert Duration | `burn` |
| 4.2.4 | Alert on Burn Rate | `burn` |
| 4.2.5 | Multiple Burn Rate Alerts | `burn` |
| 4.2.6 | Multiwindow, Multi-Burn-Rate Alerts | `burn` |
| 4.3 | Low-Traffic Services and Error Budget Alerting | `burn` |
| 4.4 | Alerting at Scale | `burn` |
| 5 | On-Call | `incident` |
| 6 | Incident Response | `incident` |
| 7 | Postmortem Culture: Learning from Failure | `incident` |
| 8 | Managing Load | `capacity` |
| 9 | Configuration Design and Best Practices | `config` |
| 10.1 | Balancing Release Velocity and Reliability | `rollouts`, `canary` |
| 10.2 | Separating Components That Change at Different Rates | `rollouts` |
| 10.3 | Release Engineering and Canarying | `canary` |
| 10.4 | Our Example Setup | `canary` |
| 10.5 | A Roll Forward Deployment Versus a Simple Canary Deployment | `canary` |
| 10.6 | Canary Implementation | `canary` |
| 10.7 | Minimizing Risk to SLOs and the Error Budget | `canary`, `budget` |
| 10.8 | Choosing a Canary Population and Duration | `canary` |
| 10.9 | Selecting and Evaluating Metrics | `canary` |
| 10.10 | Dependencies and Isolation | `canary` |
| 10.11 | Canarying in Noninteractive Systems | `canary` |
| 10.12 | Requirements on Monitoring Data | `canary` |
| 10.13.1 | Blue/Green Deployment | `rollouts` |
| 10.13.2 | Artificial Load Generation | `canary` |
| 10.13.3 | Traffic Teeing | `canary` |
| 11 | Identifying and Recovering from Overload | `capacity` |
| 12.1 | Use continuous integration | `integrate`, `workflow` |
| 12.2 | Shift testing left with unit tests | `integrate`, `workflow` |
| 13.1 | What is continuous delivery? | `integrate` |
| 13.2 | What is infrastructure as code (IaC)? | `iac` |
| 13.3 | Deploy to Azure infrastructure with GitHub Actions | `iac` |
| 13.4 | Shift right to test in production | `canary` |
| 14.1 | What is monitoring? | `monitor` |
| 14.2 | Progressive experimentation with feature flags | `rollouts` |
| 14.3 | Eliminate downtime through versioned service updates | `rollouts` |
| 14.4 | How Microsoft operates reliable systems with DevOps | `integrate`, `incident` |
| 15.1 | What is SLSA? | `provenance` |
| 15.2 | Why SLSA is needed | `provenance` |
| 15.3 | SLSA in layperson’s terms | `provenance` |
| 15.4 | Who is SLSA for? | `provenance` |
| 15.5 | How SLSA works | `provenance` |
| 15.6 | What SLSA doesn’t cover | `provenance` |
| 16.1 | Build levels | `provenance` |
| 16.2 | Security Best Practices | `provenance` |
| 16.3 | Producer | `provenance` |
| 16.4 | Choose an appropriate build platform | `provenance` |
| 16.5 | Follow a consistent build process | `repro`, `provenance` |
| 16.6 | Distribute provenance | `provenance` |
| 16.7 | Build Platform | `provenance` |
| 16.8 | Provenance generation | `provenance` |
| 16.9 | Isolation strength | `provenance` |
| 17.1 | Build provenance | `provenance` |
| 17.2 | Source provenance | `provenance` |
| 18.1 | Variations in the build environment | `repro` |
| 18.2 | SOURCE_DATE_EPOCH | `repro` |
| 18.3 | Volatile inputs can disappear | `repro` |
| 18.4 | Stable order for inputs | `repro` |
| 18.5 | Stripping of unreproducible information | `repro` |
| 18.6 | Version information | `repro` |
| 18.7 | Timestamps | `repro` |
| 18.8 | Timezones | `repro` |
| 18.9 | Locales | `repro` |
| 18.10 | Archive metadata | `repro` |
| 18.11 | Stable order for outputs | `repro` |
| 18.12 | Randomness | `repro` |
| 18.13 | Build path | `repro` |
| 18.14 | System images | `repro` |
| 19.1 | What's in a build environment? | `repro` |
| 19.2 | Recording the build environment | `repro` |
| 19.3 | Definition strategies | `repro` |
| 19.4 | Proprietary operating systems | `repro` |
| 20.1 | BOM Identity | `sbom` |
| 20.2 | The Anatomy of a CycloneDX BOM | `sbom` |
| 20.3 | Serialization Formats | `sbom` |
| 21.1 | NTIA Minimum Elements | `sbom` |
| 21.2 | SCVS BOM Maturity Model | `sbom` |
| 21.3 | SBOM Quality | `sbom` |

## 双语资料、CS2023 与综合练习

- CS2023 的 SE-Construction DevOps 实践对应 `integrate`、`workflow`；SE-Tools 配置、发布、依赖与构建系统对应 `config`、`iac`、`rollouts`、`locks`、`repro`；SE-Reliability 遥测与告警对应 `signals`、`monitor`、`burn`；SEC-Engineering 软件签名与验证对应 `provenance`。综合练习 1 见 `workflow`，练习 2 见 `integrate`、`rollouts`、`canary`。[GitHub Actions 工作流语法](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions) · [持续集成](https://martinfowler.com/articles/continuousIntegration.html) · [持续交付](https://martinfowler.com/bliki/ContinuousDelivery.html)
- 练习 3 的 30 天、99.9% 可用率和剩余预算由 `indicator`、`budget` 计算。练习 4 的三种信号、燃烧速率和低流量情形由 `signals`、`monitor`、`burn` 负责。配置、故障复盘与容量依次见 `config`、`iac`、`incident`、`capacity`。[SRE Workbook](https://sre.google/workbook/table-of-contents/) · [OpenTelemetry 可观测性](https://opentelemetry.io/zh/docs/concepts/observability-primer/) · [Twelve-Factor 配置](https://12factor.net/config)
- 练习 5 的独立重建、受控输入和摘要比较由 `repro`、`provenance` 负责。练习 6 的 pip 哈希校验、npm 干净安装和软件物料清单由 `locks`、`sbom` 负责。SLSA 在入门层讲生成与验证、隔离和等级差异，不要求实施组织级认证。[Reproducible Builds](https://reproducible-builds.org/docs/) · [SLSA 构建要求](https://slsa.dev/spec/v1.2/build-requirements) · [CycloneDX](https://cyclonedx.org/specification/overview/)
- 上游无必须后继。与下一站 C.2.3 的交接在 `workflow` 和 `repro`。这里建立“镜像是带明确输入的构建产物”的概念，后续再讲隔离机制、资源限制和镜像运行策略。
