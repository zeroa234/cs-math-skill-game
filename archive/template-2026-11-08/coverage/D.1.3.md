# D.1.3 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Motivation and History | `workloads` |
| 1.2 | OLTP and OLAP | `workloads` |
| 1.3 | NoSQL: Scaling Databases for Web 2.0 | `workloads`, `key-value` |
| 1.4 | Methods for Scaling Databases | `workloads`, `shards`, `replicas` |
| 1.5 | Partitioning | `shards`, `ring` |
| 1.6 | Replication | `replicas`, `quorum` |
| 1.7 | CAP Theorem | `cap` |
| 1.8 | NoSQL Data Models | `key-value`, `wide-column`, `documents`, `graph` |
| 1.9 | Key-Value Stores | `key-value`, `cache` |
| 1.10 | Wide-Column Stores | `wide-column` |
| 1.11 | Document Stores | `documents` |
| 1.12 | Document vs Relational Data Models | `documents` |
| 2.1 | Distributed Locking | `distributed-locks` |
| 2.2 | Two Phase Commit (2 PC) | `commit` |
| 2.3 | Distributed Recovery (2PC) | `recovery` |
| 2.4 | Distributed Recovery (2PC with Presumed Abort) | `recovery` |
| 3 | Parallel Query Processing | `parallel-shards` |
| 4 | Consensus | `consensus` |
| 5.1 | Node | `graph` |
| 5.2 | Node labels | `graph` |
| 5.3 | Relationship | `graph` |
| 5.4 | Relationship type | `graph` |
| 5.5 | Properties | `graph` |
| 5.6 | Traversals and paths | `graph` |

## CS2023、双语资料与综合练习

- CS2023 DM-Internals 的分布式事务见 `distributed-locks`、`commit`、`recovery`；DM-NoSQL 的键值和文档模型见 `key-value`、`cache`、`documents`。分片与复制按本技能要求覆盖。范围、散列、环与迁移算例由 `shards`、`ring` 负责，跨分片查询见 `parallel-shards`，补充 TiKV/HBase Region 的范围概念。[厦门大学大数据技术原理](https://dblab.xmu.edu.cn/post/bigdata3/) · [Berkeley CS186](https://cs186berkeley.net/notes/) · [TiDB 架构](https://docs.pingcap.com/zh/tidb/stable/tidb-architecture/)
- 原题 2 的同步/异步、读己之写与 N/W/R 见 `replicas`、`quorum`。严格法定集合的相交仅说明读写相交，不直接推出线性一致性。原题 5 的 CAP 和 PACELC 见 `cap`，不将可调配置的整个产品固定成一种标签。[Dynamo 论文](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf) · [Raft 论文](https://raft.github.io/raft.pdf) · [Abadi 的 PACELC 论文](https://www.cs.umd.edu/~abadi/papers/abadi-pacelc.pdf)
- 原题 3 的 2PC 和协调者失联、恢复及 presumed abort 见 `commit`、`recovery`。`consensus` 区分跨参与者原子提交与单一副本组的日志一致性。TiDB 的两类机制作为实际架构对照。
- 原题 4 的会话、目录、时序和社交关系分别见 `key-value`、`documents`、`wide-column`、`graph`。网站路线所需的缓存更新与 TTL 见 `cache`。[Redis SET](https://redis.io/docs/latest/commands/set/) · [MongoDB 数据建模](https://www.mongodb.com/docs/manual/data-modeling/) · [Apache Cassandra 数据建模](https://cassandra.apache.org/doc/latest/cassandra/developing/data-modeling/intro.html) · [Neo4j Fundamentals](https://graphacademy.neo4j.com/courses/neo4j-fundamentals/)
