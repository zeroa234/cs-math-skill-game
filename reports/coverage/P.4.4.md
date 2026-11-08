# P.4.4 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | What is Software Architecture? | `system-boundaries` |
| 1.2 | High Quality Software | `quality-scenario` |
| 1.3 | Quality Attributes | `quality-scenario` |
| 2.1 | Functional Requirements | `system-boundaries` |
| 2.2 | Constraints | `system-boundaries` |
| 2.3 | Principles | `system-boundaries` |
| 2.4 | Quality Attributes | `quality-scenario` |
| 2.5 | Documentation | `views` |
| 3.1 | C4 Model | `views` |
| 3.2 | Sahara C4 Model | `views` |
| 3.3 | Software Architecture in Practice Views | `views` |
| 3.4 | 4+1 Views | `views` |
| 4 | Architecture Decision Records | `adr` |
| 5.1 | Monolith Architecture | `monolith` |
| 5.2 | Layered Architecture | `monolith` |
| 5.3 | Layered Design Principles | `monolith` |
| 6 | Pipeline Architecture | `pipeline` |
| 7.1 | Media Server Example | `microkernel` |
| 7.2 | C4 Model | `microkernel` |
| 7.3 | Technical vs Domain Partitioning | `microkernel` |
| 8 | Service-Based Architecture | `services` |
| 9 | Event-driven Architecture | `events` |
| 10.1 | Message Queues | `events` |
| 11 | Serverless Architecture | `serverless` |
| 12.1 | Release Branching | `rollout` |
| 12.2 | Recreate Deployment | `rollout` |
| 12.3 | Rolling Deployment | `rollout` |
| 12.4 | Blue/green Deployment | `rollout` |
| 12.5 | Canary Deployment | `rollout` |
| 12.6 | A/B Deployment | `experiments` |
| 12.7 | Shadow Deployment | `experiments` |
| 13 | Decomposing Monoliths | `evolution` |
| 14.1 | The Senses of “Architecture” | `system-boundaries` |
| 14.2 | Stakeholders and Concerns | `system-boundaries` |
| 14.3 | Architecture Views and Viewpoints | `views` |
| 14.4 | Architecture Patterns, Styles and Reference Architectures | `review` |
| 14.5 | Architecture as Significant Decisions | `system-boundaries` |
| 14.6 | Goodness in Architecture | `review` |
| 14.7 | Architecture Reviews | `review` |
| 15.1 | Evolution of Software | `evolution` |
| 15.2 | Categories of Software Maintenance | `evolution` |
| 15.3 | Impact Analysis | `evolution` |
| 15.4 | Software Reengineering | `evolution` |

## CS2023 与原综合练习

- SE-Design CS Core 的软件架构和设计范式见 `system-boundaries`、`views`、架构风格各课。质量权衡见 `quality-scenario`、`cart-partition`、`review`。 [昆士兰大学 CSSE6400](https://csse6400.uqcloud.net/) · [SWEBOK v4.0a](https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf) · [C4 模型](https://c4model.com/)
- 原题 1 在分层、服务和事件课程比较部署与一致性代价。原题 2 在 `quality-scenario` 明确量的是完成下单响应，另有百分位与部署指标的练习。原题 3 在 `cart-partition` 区分分区行为、删除标记及并发添加。原题 4 在 `adr` 对比 PostgreSQL 与 MongoDB 的访问和事务约束。 [ADR 原始说明](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) · [PostgreSQL 事务](https://www.postgresql.org/docs/current/tutorial-transactions.html) · [MongoDB 事务](https://www.mongodb.com/docs/manual/core/transactions/)
- `rollout`、`experiments`、`evolution` 使用课堂场景推演部署和迁移。验证脚本检查样本百分位、重复事件、购物车合并和回退算例。目标指标仍须在目标环境测量。
