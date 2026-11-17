# D.1.3 分布式数据库与 NoSQL：覆盖表

**状态（2026-11-17）：已写完。** 依据 `../cs-math-skill-tree/data/outlines/D.1.3.json` 与 `../cs-math-skill-tree/output/outlines.json`，主来源为 UC Berkeley CS186 *NoSQL*、*Distributed Transactions*、*Parallel Query Processing*、*Consensus* 讲义，补充 Neo4j *Graph database concepts*。

必须前置仅为 `D.1.2 数据库内核与查询优化`（继承 `D.1.1`、`F.1.1`、`C.1.1`、`P.1.1` 与 `D.1.2` 术语）；`C.4.1 分布式系统` 为推荐前置而非强制，因此 `分片`、`一致性哈希`、`复制`、`读己之写`、`法定集合`、`网络分区`、`线性一致性`、`最终一致性`、`共识`、`两阶段提交`、`TTL` 与 `缓存` 均在本包卡中从零定义。内部 4 章（`original` 顺序）：`1. 分片`、`2. 复制`、`3. 分布式事务`、`4. 键值/文档/列族/图数据模型`。

`node scripts/check-coverage.mjs D.1.3` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | A Motivation and History 动机与历史 | `workloads` |
| 1.2 | A OLTP and OLAP | `workloads` |
| 1.3 | A NoSQL: Scaling Databases for Web 2.0 | `workloads`、`key-value` |
| 1.4 | A Methods for Scaling Databases 扩展数据库的方法 | `shards`、`replicas` |
| 1.5 | A Partitioning 分区（分片） | `shards`、`ring` |
| 1.6 | A Replication 复制 | `replicas`、`quorum` |
| 1.7 | A CAP Theorem | `cap` |
| 1.8 | A NoSQL Data Models | `key-value`、`wide-column`、`documents`、`graph` |
| 1.9 | A Key-Value Stores | `key-value`、`cache` |
| 1.10 | A Wide-Column Stores | `wide-column` |
| 1.11 | A Document Stores | `documents` |
| 1.12 | A Document vs Relational Data Models | `documents` |
| 2.1 | A Distributed Locking | `distributed-locks` |
| 2.2 | A Two Phase Commit (2 PC) | `commit` |
| 2.3 | A Distributed Recovery (2PC) | `recovery` |
| 2.4 | A Distributed Recovery (2PC with Presumed Abort) | `recovery` |
| 3 | A Parallel Query Processing 并行查询处理 | `parallel-shards` |
| 4 | A Consensus 共识 | `consensus` |
| 5.1 | B Node | `graph` |
| 5.2 | B Node labels | `graph` |
| 5.3 | B Relationship | `graph` |
| 5.4 | B Relationship type | `graph` |
| 5.5 | B Properties | `graph` |
| 5.6 | B Traversals and paths | `graph` |

## CS2023 核心主题（C2）

`scope.json` 在 `D.1.3` 的 4 个章节中共匹配 2 个 CS2023 核心主题；**分片**与**复制**在 CS2023 中属 DM 的 Non-core 主题，按本技能与推荐“网站开发”路线要求照常全覆盖：

| 知识点 | KA / 要求 | 课 |
|---|---|---|
| 分布式事务 | DM-Internals · KA Core（Distributed Transactions） | `distributed-locks`、`commit`、`recovery` |
| 键值/文档/列族/图数据模型 | DM-NoSQL · KA Core（Key-Value and Document data model） | `key-value`、`cache`、`wide-column`、`documents`、`graph` |
| 分片与复制（Non-core 按技能覆盖） | DM Non-core | `workloads`、`shards`、`ring`、`parallel-shards`、`replicas`、`quorum`、`cap`、`consensus` |

## 学习路径、综合练习、重要边界与后继状态（C3 / C4 / C5）

- 对应 `learning-paths/D.1.3.json` 全部 4 个模块（按当前 `topics` 与补充材料，中英双语均 `complete`）：CS186、CMU 15-445 #24、Neo4j Graph Fundamentals、厦大林子雨教材第 3–5 章、PingCAP TiDB 101/204（TiKV MVCC/Percolator/Raft）与北理工分布式事务讲纲。
- **综合练习 5 问映射**：(1) 哈希分片 vs 范围分片、一致性哈希迁移 `K/(N+1)` 与 `hash(key) mod N` 对比 → `shards`、`ring`；(2) 同步/异步复制代价、读己之写与 Dynamo `N=3, W=2, R=2` 含义 → `replicas`、`quorum`；(3) 2PC 两阶段流程与协调者收集同意后崩溃阻塞问题 → `commit`、`recovery`；(4) 用户会话（键值）、属性各异商品目录（文档）、社交多跳（图）、设备时序（宽列/列族）模型选型 → `key-value`、`documents`、`graph`、`wide-column`；(5) PACELC（Dynamo PA/EL vs Spanner PC/EC）→ `cap`。另有 `cache`（`1.9`）专项呼应“网站开发”推荐远征中“缓存与回源策略”挂载。
- **三条严谨边界声明**：
  1. 法定集合相交条件 $W + R > N$ 仅证明最新写入副本集合与本次读取副本集合至少存在一个交集副本，不能由 $W + R > N$ 单方面直接推出强线性一致性（还需最新版本比对、读修复与防并发交错读写机制）；
  2. CAP 与 PACELC 针对特定复制/并发控制机制及其默认可调配置而讨论，不将支持按策略切换配置的产品贴成僵化单一标签；
  3. 在 `consensus` 与 `commit` 间明确区分：**2PC** 解决的是跨不同数据分片协调“全体参与者同提交或同回滚”的原子提交问题，而 **Paxos / Raft 共识** 解决的是同一副本组内多个副本节点对操作日志排序保持一致并消除单点阻塞的问题。
- **后继状态（C5）**：`D.1.3` 无下游必选后继（`unlocks: []`、`reach: 0`），是数据库链路 `D.1.1 → D.1.2 → D.1.3` 终点，故 C5 不适用。
