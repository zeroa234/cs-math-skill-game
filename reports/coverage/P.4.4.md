# P.4.4 软件架构：覆盖表

**状态（2026-11-18）：已写完（v2 重写，按零基础与知识覆盖面标准重写）。** 依据 `../cs-math-skill-tree/data/outlines/P.4.4.json`、`output/outlines.json`、`data/curation/learning-paths/P.4.4.json`，主来源为昆士兰大学 UQ CSSE6400《Software Architecture》与 IEEE SWEBOK v4.0a 第 2 章（Software Architecture）与第 7 章（Software Maintenance），辅以 Microsoft Learn Azure 体系结构中心、adr.github.io、RIT SWEN-440 质量属性讲义与 Martin Fowler《Patterns of Legacy Displacement》，对齐 `P.4.4` 综合练习 4 问，本地核对脚本 `tests/content/P.4.4.verify.py`（Python 3 实测）。

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | What is Software Architecture? | `system-boundaries` |
| 1.2 | High Quality Software | `system-boundaries` |
| 1.3 | Quality Attributes | `quality-scenarios` |
| 2.1 | Functional Requirements | `system-boundaries` |
| 2.2 | Constraints | `system-boundaries` |
| 2.3 | Principles | `system-boundaries` |
| 2.4 | Quality Attributes | `quality-scenarios`、`tactics-latency` |
| 2.5 | Documentation | `c4-and-views` |
| 3.1 | C4 Model | `c4-and-views` |
| 3.2 | Sahara C4 Model | `c4-and-views`（以校园二手书店和媒体网站案例等价讲解） |
| 3.3 | Software Architecture in Practice Views | `c4-and-views` |
| 3.4 | 4+1 Views | `c4-and-views` |
| 4 | Architecture Decision Records | `adr-records` |
| 5.1 | Monolith Architecture | `monolith-layered`、`style-comparison` |
| 5.2 | Layered Architecture | `monolith-layered`、`style-comparison` |
| 5.3 | Layered Design Principles | `monolith-layered` |
| 6 | Pipeline Architecture | `pipeline-microkernel` |
| 7.1 | Media Server Example | `partitioning-boundaries` |
| 7.2 | C4 Model | `partitioning-boundaries` |
| 7.3 | Technical vs Domain Partitioning | `partitioning-boundaries` |
| 8 | Service-Based Architecture | `service-based`、`style-comparison` |
| 9 | Event-driven Architecture | `event-driven`、`style-comparison` |
| 10.1 | Message Queues | `event-driven` |
| 11 | Serverless Architecture | `serverless`、`style-comparison` |
| 12.1 | Release Branching | `release-deployments` |
| 12.2 | Recreate Deployment | `release-deployments` |
| 12.3 | Rolling Deployment | `release-deployments` |
| 12.4 | Blue/green Deployment | `release-deployments` |
| 12.5 | Canary Deployment | `release-deployments` |
| 12.6 | A/B Deployment | `release-deployments` |
| 12.7 | Shadow Deployment | `release-deployments` |
| 13 | Decomposing Monoliths | `decomposing-monoliths`、`impact-reengineering` |
| 14.1 | The Senses of “Architecture” | `system-boundaries` |
| 14.2 | Stakeholders and Concerns | `system-boundaries` |
| 14.3 | Architecture Views and Viewpoints | `c4-and-views` |
| 14.4 | Architecture Patterns, Styles and Reference Architectures | `monolith-layered`、`pipeline-microkernel`、`service-based`、`style-comparison` |
| 14.5 | Architecture as Significant Decisions | `adr-records` |
| 14.6 | Goodness in Architecture | `quality-scenarios`、`tactics-latency`、`architecture-review` |
| 14.7 | Architecture Reviews | `architecture-review` |
| 15.1 | Evolution of Software | `evolution-maintenance` |
| 15.2 | Categories of Software Maintenance | `evolution-maintenance` |
| 15.3 | Impact Analysis | `impact-reengineering` |
| 15.4 | Software Reengineering | `impact-reengineering` |

## CS2023 核心主题（C2）

`data/curation/scope.json` 为 `P.4.4` 匹配的 3 项 CS2023 核心主题全部落课（第 4 个知识点“架构决策和系统演化”无 CS2023 对应条目，也一并完整覆盖）：

| 知识点 | KA / 要求 | 课 |
|---|---|---|
| 组件与边界 | SE-Design / CS Core：Software architecture | `system-boundaries`、`c4-and-views`、`partitioning-boundaries`、`decomposing-monoliths` |
| 架构风格 | SE-Design / CS Core：Design paradigms | `monolith-layered`、`pipeline-microkernel`、`service-based`、`event-driven`、`serverless`、`style-comparison` |
| 质量属性 | SE-Design / KA Core：Evaluating design tradeoffs | `quality-scenarios`、`tactics-latency`、`cap-pacelc`、`architecture-review` |

## 综合练习与前置/后继映射（C3 / C4 / C5）

- **综合练习 4 问映射（C4）**：
  - 第 (1) 问比较分层架构、微服务架构、事件驱动架构的优缺点，并给出 5 人初创电商的选型理由 → `monolith-layered`、`service-based`、`event-driven`、`style-comparison`（模块化单体、可独立演化的模块边界、运维与分布式代价对比）。
  - 第 (2) 问为“峰值 1000 次/秒时 99% 请求在 300 ms 内返回”写出完整质量属性场景六要素，并列出两种以上架构策略 → `quality-scenarios`（六要素与 p99 计算）、`tactics-latency`（无状态水平扩展、读缓存、消息队列异步剥离电子发票与通知等非阻塞步骤、读写分离、限流降级）。
  - 第 (3) 问双数据中心购物车在网络分区时选 CP 还是 AP，以及用户看到的现象对比 → `cap-pacelc`（CP 拒绝少数派写入 vs AP 两边可写恢复后合并及删掉商品复活现象，对比支付选 CP）。
  - 第 (4) 问写出订单存储 PostgreSQL vs MongoDB 的简短 ADR（背景、决策、后果） → `adr-records`（ADR-007 订单存储完整背景、决策与迁移/分库后果）。
- **前后继状态（C3 / C5）**：
  - 必须前置为 `P.4.3 软件设计与面向对象分析设计`（沿必须前置链递归继承 `P.4.3`、`P.1.2`、`P.1.1` 全部术语，含 `内聚`、`耦合`、`视图`、`契约`、`依赖倒置`、`依赖注入`、`限界上下文`、`策略模式`、`观察者模式`、`编译器`、`进程`、`线程`、`互斥锁`、`死锁`、`断言` 等）。涉及数据库表、事务、`SQL`/`JOIN`、`JSONB`、缓存过期（TTL）、熔断与 Saga 补偿等运维与存储细节时，均已在文中随用随释、不预设 `D.1.1`/`C.3.2` 先修。
  - `P.4.4` 无必须或推荐后继技能（`unlocks: []`）；与 `C.4.1` 分布式系统有相关主题呼应（无前置依赖，C5 无未覆盖缺口）。
