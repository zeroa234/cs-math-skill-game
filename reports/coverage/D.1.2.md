# D.1.2 数据库内核与查询优化：覆盖表

**状态（2026-11-17）：已写完。** 依据 `../cs-math-skill-tree/data/outlines/D.1.2.json` 与 `../cs-math-skill-tree/output/outlines.json`，主来源为 CMU 15-445/645（Fall 2026 #07–11、#13–17 及 Fall 2025 #18–23 讲义），辅助参考清华《数据库管理系统》与 OceanBase 讲义。

必须前置为 `D.1.1`、`F.1.1`、`C.1.1`（均可继承）；`P.2.2`、`C.2.1` 与 `C.2.4` 为推荐前置，因此本包在卡中定义 `缓冲池`、`闩锁`、`冲突可串行化`、`两阶段锁`、`死锁`、`事务`、`WAL`、`MVCC` 等并发与恢复术语。内部 5 章按游戏章序排列：`1. 并发控制`、`2. 日志与恢复`、`3. 索引`、`4. 执行计划`、`5. 代价模型`。

`node scripts/check-coverage.mjs D.1.2` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | A Data Structures | `hash-index` |
| 1.2 | A Hash Table | `hash-index` |
| 1.3 | A Hash Functions | `hash-index` |
| 1.4 | A Static Hashing Schemes | `hash-index` |
| 1.5 | A Dynamic Hashing Schemes | `hash-index` |
| 2.1 | A Indexes | `bplus` |
| 2.2 | A B+Tree | `bplus` |
| 2.3 | A B+Tree Design Choices | `bplus` |
| 2.4 | A Optimizations | `bplus`、`selectivity` |
| 3.1 | A Index vs. Filters | `filters` |
| 3.2 | A Bloom filter | `filters` |
| 3.3 | A Skip List | `filters` |
| 3.4 | A Trie | `filters` |
| 3.5 | A Inverted Index | `filters` |
| 3.6 | A Vector Index | `filters` |
| 3.7 | A Optimizations | `filters` |
| 4.1 | A Index Concurrency Control | `latches` |
| 4.2 | A Locks vs. Latches | `latches` |
| 4.3 | A Latch Implementations | `latches` |
| 4.4 | A Hash Table Latching | `latches` |
| 4.5 | A B+Tree Latching | `latches` |
| 5.1 | A Query Plan | `operators` |
| 5.2 | A Sorting | `operators` |
| 5.3 | A Aggregations | `operators` |
| 6.1 | A Introduction | `joins` |
| 6.2 | A Join Operators | `joins` |
| 6.3 | A Nested Loop Join | `joins` |
| 6.4 | A Sort-Merge Join | `joins` |
| 6.5 | A Hash Join | `joins` |
| 7.1 | A Query Plan | `operators` |
| 7.2 | A Processing Models | `operators` |
| 7.3 | A Access Methods | `operators`、`selectivity` |
| 7.4 | A Modification Queries | `operators` |
| 7.5 | A Expression Evaluation | `operators` |
| 8.1 | A Background | `parallel` |
| 8.2 | A Parallel vs Distributed Databases | `parallel` |
| 8.3 | A Process Models | `parallel` |
| 8.4 | A Inter-Query Parallelism | `parallel` |
| 8.5 | A Intra-Query parallelism | `parallel` |
| 8.6 | A I/O Parallelism | `parallel` |
| 9.1 | A Overview | `rewrite` |
| 9.2 | A Relational Algebra Equivalence | `rewrite` |
| 9.3 | A Types of Query Optimization | `rewrite` |
| 9.4 | A Logical Query Optimization | `rewrite` |
| 9.5 | A Cost-Based Query Optimization | `rewrite`、`selectivity` |
| 9.6 | A Cost Estimations | `selectivity` |
| 9.7 | A Search Termination | `plans` |
| 9.8 | A Access Path Transformation | `selectivity` |
| 9.9 | A Single-Relation Query Plans | `plans` |
| 9.10 | A Multi-Relation Query Plans | `plans` |
| 9.11 | A Bottom-up optimization example - System R | `plans` |
| 9.12 | A Top-down optimization example - Volcano | `plans` |
| 9.13 | A Nested Sub-Queries | `rewrite` |
| 9.14 | A Expression Rewriting | `rewrite` |
| 10.1 | A Multi-Relation Query Plans | `plans` |
| 10.2 | A Data Statistics | `selectivity` |
| 10.3 | A Cost Estimations | `selectivity` |
| 11.1 | A Motivation | `acid` |
| 11.2 | A Transactions | `acid` |
| 11.3 | A Definitions | `acid`、`conflicts` |
| 11.4 | A ACID: Atomicity | `acid` |
| 11.5 | A ACID: Consistency | `acid` |
| 11.6 | A ACID: Isolation | `acid`、`conflicts` |
| 11.7 | A ACID: Durability | `acid`、`wal` |
| 12.1 | A Transaction Locks | `two-phase` |
| 12.2 | A Two-Phase Locking | `two-phase` |
| 12.3 | A Deadlock Handling | `two-phase` |
| 12.4 | A Lock Granularities | `two-phase` |
| 12.5 | A Locking in Practice | `two-phase`、`isolation` |
| 13.1 | A Timestamp Ordering Concurrency Control | `timestamps` |
| 13.2 | A Optimistic Concurrency Control (OCC) | `timestamps` |
| 13.3 | A Dynamic Databases and The Phantom Problem | `isolation` |
| 13.4 | A Isolation Levels | `isolation` |
| 14.1 | A MVCC | `mvcc` |
| 14.2 | A Design consideration: Version Storage | `mvcc` |
| 14.3 | A Design consideration: Garbage Collection | `mvcc` |
| 14.4 | A Design consideration: Index Management | `mvcc` |
| 14.5 | A Design consideration: Deletes | `mvcc` |
| 15.1 | A Crash Recovery | `buffers` |
| 15.2 | A Buffer Pool Management Policies | `buffers` |
| 15.3 | A Naive NO-STEAL + FORCE | `buffers` |
| 15.4 | A Shadow Paging (Smarter NO-STEAL + FORCE) | `buffers` |
| 15.5 | A Journal File (SQLite Pre-2010) | `buffers` |
| 15.6 | A Write-Ahead Logging | `wal` |
| 15.7 | A Logging Schemes | `wal` |
| 15.8 | A Checkpoints | `wal` |
| 16.1 | A Crash Recovery | `aries` |
| 16.2 | A WAL Records | `wal`、`aries` |
| 16.3 | A Normal Execution | `wal` |
| 16.4 | A Checkpointing | `wal`、`aries` |
| 16.5 | A ARIES Recovery | `aries` |

## CS2023 核心主题（C2）

`scope.json` 在 `D.1.2` 的 5 个章节均完整匹配 CS2023 KA Core（5/5 全覆盖）：

| 知识点 | KA / 要求 | 课 |
|---|---|---|
| 并发控制 | DM-Internals · KA Core（Concurrency Control） | `acid`、`conflicts`、`two-phase`、`timestamps`、`isolation`、`mvcc` |
| 日志与恢复 | DM-Internals · KA Core（Recovery Manager） | `buffers`、`wal`、`aries` |
| 索引 | DM-Processing · KA Core（Index structures） | `hash-index`、`bplus`、`filters`、`latches` |
| 执行计划 | DM-Processing · KA Core（Query plan construction） | `operators`、`joins`、`parallel` |
| 代价模型 | DM-Processing · KA Core（Selectivity estimation） | `rewrite`、`selectivity`、`plans` |

## 学习路径、综合练习与后继衔接（C3 / C4 / C5）

- 对应 `learning-paths/D.1.2.json` 5 个核心模块（中英双语 `status = complete`）：CMU 15-445、Berkeley CS186 notes、战德臣/清华大学李国良讲义及 OceanBase 实现讲义。
- **综合练习 5 问映射**：(1) $10^7$ 行 8KB 页、200 扇出 B+ 树共 4 层索引（50,000 → 250 → 2 → 1 根；点查树路径 4 次 I/O，非聚簇取行再 +1；全表扫描 $10^5$ 页）→ `bplus`；(2) $R=1000, S=500, B=102$ 块嵌套循环 5,500、排序归并 7,500（合趟优化可至 4,500）、Grace 哈希 4,500 → `joins`；(3) `status='refunded'` 索引扫描 vs 全表扫描取舍（按选择率、聚簇度与页 I/O 代价估算，弃用模糊经验百分比阈值）与投影/选择下推 → `selectivity`、`rewrite`；(4) 调度优先图成环 (`T1↔T2`)、非冲突可串行化与 Strict 2PL 阻断 → `conflicts`、`two-phase`；(5) WAL 顺序写、`STEAL/NO-FORCE` 与 `Redo/Undo` → `buffers`、`wal`、`aries`。
- **后继衔接（C5）**：向 `D.1.3 分布式数据库与 NoSQL` 交接事务原子性、隔离语义、锁表/冲突检测与 WAL 持久日志根基，以支撑两阶段提交、跨节点锁与复制状态机。
