# D.1.2 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Data Structures | `hash-index` |
| 1.2 | Hash Table | `hash-index` |
| 1.3 | Hash Functions | `hash-index` |
| 1.4 | Static Hashing Schemes | `hash-index` |
| 1.5 | Dynamic Hashing Schemes | `hash-index` |
| 2.1 | Indexes | `bplus` |
| 2.2 | B+Tree | `bplus` |
| 2.3 | B+Tree Design Choices | `bplus` |
| 2.4 | Optimizations | `bplus`, `selectivity` |
| 3.1 | Index vs. Filters | `filters` |
| 3.2 | Bloom filter | `filters` |
| 3.3 | Skip List | `filters` |
| 3.4 | Trie | `filters` |
| 3.5 | Inverted Index | `filters` |
| 3.6 | Vector Index | `filters` |
| 3.7 | Optimizations | `filters` |
| 4.1 | Index Concurrency Control | `latches` |
| 4.2 | Locks vs. Latches | `latches` |
| 4.3 | Latch Implementations | `latches` |
| 4.4 | Hash Table Latching | `latches` |
| 4.5 | B+Tree Latching | `latches` |
| 5.1 | Query Plan | `operators` |
| 5.2 | Sorting | `sort-group` |
| 5.3 | Aggregations | `sort-group` |
| 6.1 | Introduction | `joins` |
| 6.2 | Join Operators | `joins` |
| 6.3 | Nested Loop Join | `joins` |
| 6.4 | Sort-Merge Join | `join-costs` |
| 6.5 | Hash Join | `join-costs` |
| 7.1 | Query Plan | `operators` |
| 7.2 | Processing Models | `operators` |
| 7.3 | Access Methods | `operators`, `selectivity` |
| 7.4 | Modification Queries | `operators` |
| 7.5 | Expression Evaluation | `operators` |
| 8.1 | Background | `parallel` |
| 8.2 | Parallel vs Distributed Databases | `parallel` |
| 8.3 | Process Models | `parallel` |
| 8.4 | Inter-Query Parallelism | `parallel` |
| 8.5 | Intra-Query parallelism | `parallel` |
| 8.6 | I/O Parallelism | `parallel` |
| 9.1 | Overview | `rewrite` |
| 9.2 | Relational Algebra Equivalence | `rewrite` |
| 9.3 | Types of Query Optimization | `rewrite` |
| 9.4 | Logical Query Optimization | `rewrite` |
| 9.5 | Cost-Based Query Optimization | `rewrite`, `selectivity` |
| 9.6 | Cost Estimations | `selectivity` |
| 9.7 | Search Termination | `plans` |
| 9.8 | Access Path Transformation | `selectivity` |
| 9.9 | Single-Relation Query Plans | `selectivity`, `plans` |
| 9.10 | Multi-Relation Query Plans | `plans` |
| 9.11 | Bottom-up optimization example - System R | `plans` |
| 9.12 | Top-down optimization example - Volcano | `plans` |
| 9.13 | Nested Sub-Queries | `rewrite` |
| 9.14 | Expression Rewriting | `rewrite` |
| 10.1 | Multi-Relation Query Plans | `plans` |
| 10.2 | Data Statistics | `selectivity` |
| 10.3 | Cost Estimations | `selectivity` |
| 11.1 | Motivation | `acid` |
| 11.2 | Transactions | `acid` |
| 11.3 | Definitions | `acid`, `conflicts` |
| 11.4 | ACID: Atomicity | `acid` |
| 11.5 | ACID: Consistency | `acid` |
| 11.6 | ACID: Isolation | `acid`, `conflicts` |
| 11.7 | ACID: Durability | `acid`, `wal` |
| 12.1 | Transaction Locks | `two-phase` |
| 12.2 | Two-Phase Locking | `two-phase` |
| 12.3 | Deadlock Handling | `two-phase` |
| 12.4 | Lock Granularities | `two-phase` |
| 12.5 | Locking in Practice | `two-phase`, `isolation` |
| 13.1 | Timestamp Ordering Concurrency Control | `timestamps` |
| 13.2 | Optimistic Concurrency Control (OCC) | `timestamps` |
| 13.3 | Dynamic Databases and The Phantom Problem | `isolation` |
| 13.4 | Isolation Levels | `isolation` |
| 14.1 | Multi-Version Concurrency Control | `mvcc` |
| 14.2 | Design consideration: Version Storage | `mvcc` |
| 14.3 | Design consideration: Garbage Collection | `mvcc` |
| 14.4 | Design consideration: Index Management | `mvcc` |
| 14.5 | Design consideration: Deletes | `mvcc` |
| 15.1 | Crash Recovery | `buffers` |
| 15.2 | Buffer Pool Management Policies | `buffers` |
| 15.3 | Naive NO-STEAL + FORCE | `buffers` |
| 15.4 | Shadow Paging (Smarter NO-STEAL + FORCE) | `buffers` |
| 15.5 | Journal File (SQLite Pre-2010) | `buffers` |
| 15.6 | Write-Ahead Logging | `wal` |
| 15.7 | Logging Schemes | `wal` |
| 15.8 | Checkpoints | `wal` |
| 16.1 | Crash Recovery | `aries` |
| 16.2 | WAL Records | `wal`, `aries` |
| 16.3 | Normal Execution | `wal` |
| 16.4 | Checkpointing | `wal`, `aries` |
| 16.5 | ARIES Recovery | `aries` |

## CS2023、教材与综合练习

- CS2023 的 DM-Internals 并发控制和恢复管理分别对应 `acid` 至 `mvcc` 及 `buffers` 至 `aries`；DM-Processing 的索引结构对应 `hash-index` 至 `latches`，执行计划构造对应 `operators` 至 `parallel`、`plans`，选择率估计对应 `selectivity`。按清华课程事务、恢复、索引、执行和优化的顺序组织。[清华数据库管理系统](https://dbgroup.cs.tsinghua.edu.cn/ligl/courses_cn.html) · [CMU 15-445 课程进度](https://15445.courses.cs.cmu.edu/fall2026/schedule.html)
- 原题 1 的页数与点查见 `bplus`。按题设 200 路扇出和 200 个叶条目估计，区分冷缓存、已有上层缓存和非覆盖索引访问。原题 2 见 `joins`、`join-costs`，分别给定输入页数、缓冲页预算、物化与不递归分区假设。[Berkeley 连接算法练习](https://cs186berkeley.net/projects/3/part-1-join-algorithms/)
- 原题 3 见 `rewrite`、`selectivity`、`plans`。索引与全表扫描的选择用统计、行数、页访问和覆盖情况解释，未沿用原题给的经验百分比阈值。`plans` 用 SQLite 查看真实计划，代价模型中的页数练习是另行明示假设的教学模型。[SQLite EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html)
- 原题 4 的冲突边、环和严格两阶段锁由 `conflicts`、`two-phase` 讲解。原题 5 区分 WAL 的持久化顺序、缓冲页的写回与 ARIES 重复历史后撤销的过程，见 `buffers`、`wal`、`aries`。SQLite WAL 用于观察实际快照，不用其输出代替 ARIES。[ARIES 原论文](https://cs.uwaterloo.ca/~david/cs448/aries-mohan.pdf) · [SQLite WAL](https://www.sqlite.org/wal.html)
- 必须后继 D.1.3 的事务、一致性、版本、持久日志与多节点区别由 `acid`、`isolation`、`mvcc`、`wal`、`parallel` 奠基。复制与共识留给 D.1.3。
