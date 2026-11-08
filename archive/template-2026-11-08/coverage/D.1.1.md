# D.1.1 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1 | Data Modelling | `design`, `mapping` |
| 2.1 | Relation | `relations` |
| 2.2 | Table | `relations` |
| 2.3 | Column | `relations` |
| 2.4 | Domain | `relations`, `constraints` |
| 2.5 | Records | `relations` |
| 2.6 | Degree | `relations` |
| 2.7 | Properties of a Table | `relations` |
| 3 | The Entity Relationship Data Model | `entities`, `mapping` |
| 4.1 | Domain Integrity | `constraints` |
| 4.2 | Entity integrity | `constraints` |
| 4.3 | Referential integrity | `references` |
| 4.4 | Referential integrity in Microsoft Access | `dialects` |
| 4.5 | Referential integrity using Transact-SQL (MS SQL Server) | `dialects` |
| 4.6 | Foreign key rules | `references` |
| 4.7 | Enterprise Constraints | `constraints`, `dialects` |
| 4.8 | Business Rules | `design`, `constraints` |
| 4.9 | Cardinality and connectivity | `entities` |
| 4.10 | Relationship Types | `entities`, `mapping` |
| 4.11 | Optional relationships | `entities`, `references` |
| 4.12 | Mandatory relationships | `entities`, `references` |
| 5 | ER Modelling | `design`, `entities`, `mapping` |
| 6.1 | Rules of Functional Dependencies | `dependencies` |
| 6.2 | Inference Rules | `dependencies` |
| 6.3 | Axiom of reflexivity | `dependencies` |
| 6.4 | Axiom of augmentation | `dependencies` |
| 6.5 | Axiom of transitivity | `dependencies` |
| 6.6 | Union | `dependencies` |
| 6.7 | Decomposition | `dependencies` |
| 6.8 | Dependency Diagram | `closure`, `normal-forms` |
| 7.1 | What Is Normalization? | `normal-forms` |
| 7.2 | Normal Forms | `normal-forms`, `bcnf` |
| 7.3 | First Normal Form (1NF) | `normal-forms` |
| 7.4 | Second Normal Form (2NF) | `normal-forms` |
| 7.5 | Third Normal Form (3NF) | `normal-forms`, `decomposition-tradeoff` |
| 7.6 | Boyce-Codd Normal Form (BCNF) | `bcnf` |
| 7.7 | BCNF Example 1 | `bcnf` |
| 7.8 | BCNF Example 2 | `decomposition-tradeoff` |
| 8 | SQL Structured Query Language | `schema`, `views` |
| 9 | SQL Data Manipulation Language | `rows`, `joins`, `groups`, `subqueries` |
| 10 | Relational Model & Algebra | `relations`, `algebra`, `sets` |

## CS2023、双语资源与综合练习

- CS2023 的 DM-Modeling 概念模型对应 `design`、`entities`、`mapping`；DM-Querying 的关系代数和 SQL 分别对应 `algebra`、`sets` 与 `rows` 至 `views`；DM-Relational 的实体和参照完整性见 `constraints`、`references`；DM-Core 的规范化见 `dependencies` 至 `decomposition-tradeoff`。设计流程按需求、概念、逻辑、物理和运行维护衔接。[厦门大学数据库系统原理](https://dblab.xmu.edu.cn/post/database2020/) · [BCcampus 数据库设计教材](https://opentextbc.ca/dbdesign01/)
- 原题 1 的选课关系、可选性和主外键见 `entities`、`mapping`、`schema`；原题 2 的四个查询见 `joins`、`groups`、`subqueries`；原题 3 的选择、连接和投影见 `algebra`。例子明确区分 SQL 的重复行和关系代数的集合语义；平均分忽略 NULL；按学生身份去重时保留学号。`sets` 介绍除法和关系演算的存在/全称视角。[Berkeley CS186 笔记](https://cs186berkeley.net/notes/) · [SQLite SELECT](https://www.sqlite.org/lang_select.html) · [SQLite 聚合函数](https://www.sqlite.org/lang_aggfunc.html)
- 原题 4 用 `closure` 求键，`normal-forms` 识别部分依赖，`bcnf` 分解并验证无损、保持依赖。`decomposition-tradeoff` 用第二例讲 3NF 与 BCNF 的取舍，并给出多值依赖与连接依赖的继续阅读边界。`dialects` 对照 Access 的关系窗口与 SQL Server 的外键声明，也区分 CHECK、SQL 标准断言和实际产品的触发器。原题 5 的级联与保留历史在 `references`。[BCcampus 完整性约束](https://opentextbc.ca/dbdesign01/chapter/chapter-9-integrity-rules-and-constraints/) · [SQLite 外键](https://www.sqlite.org/foreignkeys.html)
- 必须后继中，D.1.2 需要查询、连接和主外键作为执行计划基础；D.1.4 需要可执行的建表、写入和约束；D.4.1 用实体及关联的建模词汇。分别由 `schema`、`rows`、`joins`、`groups`、`views` 和 `entities`、`mapping` 承接。
