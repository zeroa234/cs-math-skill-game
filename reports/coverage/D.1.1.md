# D.1.1 数据建模、关系模型与 SQL：覆盖表

**状态（2026-11-17）：已写完。** 依据 `../cs-math-skill-tree/data/outlines/D.1.1.json` 与 `../cs-math-skill-tree/output/outlines.json`，主来源为 BCcampus *Database Design – 2nd Edition*（第 5/8/9/10/11/12/15/16 章）与 CMU 15-445 #01 *Relational Model & Algebra*。

必须前置仅为 `P.1.1 程序设计基础`；内部 5 章（与 `scope.json` / `learning-paths/D.1.1.json` 顺序一致）：`1. 实体关系`、`2. 关系代数`、`3. 约束`、`4. 查询与数据建模`、`5. 规范化`。

`node scripts/check-coverage.mjs D.1.1` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1 | A Data Modelling | `design` |
| 2.1 | A Relation | `mapping` |
| 2.2 | A Table | `mapping` |
| 2.3 | A Column | `mapping` |
| 2.4 | A Domain | `mapping` |
| 2.5 | A Records | `mapping` |
| 2.6 | A Degree | `mapping` |
| 2.7 | A Properties of a Table | `mapping` |
| 3 | A The Entity Relationship Data Model | `entities` |
| 4.1 | A Domain Integrity | `constraints` |
| 4.2 | A Entity integrity | `constraints` |
| 4.3 | A Referential integrity | `references` |
| 4.4 | A Referential integrity in Microsoft Access | `dialects` |
| 4.5 | A Referential integrity using Transact-SQL (MS SQL Server) | `dialects` |
| 4.6 | A Foreign key rules | `references` |
| 4.7 | A Enterprise Constraints | `constraints`、`dialects` |
| 4.8 | A Business Rules | `constraints` |
| 4.9 | A Cardinality and connectivity | `entities` |
| 4.10 | A Relationship Types | `entities` |
| 4.11 | A Optional relationships | `entities` |
| 4.12 | A Mandatory relationships | `entities` |
| 5 | A ER Modelling | `entities` |
| 6.1 | A Rules of Functional Dependencies | `dependencies` |
| 6.2 | A Inference Rules | `dependencies` |
| 6.3 | A Axiom of reflexivity | `dependencies` |
| 6.4 | A Axiom of augmentation | `dependencies` |
| 6.5 | A Axiom of transitivity | `dependencies` |
| 6.6 | A Union | `dependencies` |
| 6.7 | A Decomposition | `dependencies` |
| 6.8 | A Dependency Diagram | `dependencies`、`bcnf` |
| 7.1 | A What Is Normalization? | `bcnf` |
| 7.2 | A Normal Forms | `bcnf` |
| 7.3 | A First Normal Form (1NF) | `bcnf` |
| 7.4 | A Second Normal Form (2NF) | `bcnf` |
| 7.5 | A Third Normal Form (3NF) | `bcnf` |
| 7.6 | A Boyce-Codd Normal Form (BCNF) | `bcnf` |
| 7.7 | A BCNF Example 1 | `bcnf` |
| 7.8 | A BCNF Example 2 | `bcnf` |
| 8 | A SQL Structured Query Language | `schema` |
| 9 | A SQL Data Manipulation Language | `joins`、`groups`、`subqueries` |
| 10 | B Relational Model & Algebra | `relations`、`algebra`、`sets` |

## CS2023 核心主题（C2）

注：`outlines.json` `coverage` 将“查询”与“数据建模”单列，本游戏章节按 `scope.json` 与 `learning-paths/D.1.1.json` 合为 `查询与数据建模` 共 5 章，5/5 项均匹配 CS2023 核心主题：

| 知识点 | KA / 要求 | 课 |
|---|---|---|
| 实体关系 | DM-Modeling · KA Core（Conceptual models, e.g. ER） | `design`、`entities`、`mapping` |
| 关系代数 | DM-Querying · KA Core（Relational Algebra） | `relations`、`algebra`、`sets` |
| 约束 | DM-Relational · CS Core（Entity and referential integrity） | `constraints`、`references`、`dialects` |
| 查询与数据建模 | DM-Querying · CS Core（SQL Query Formation） | `schema`、`joins`、`groups`、`subqueries` |
| 规范化 | DM-Core · CS Core（Normalization） | `dependencies`、`bcnf` |

## 学习路径、综合练习与后继衔接（C3 / C4 / C5）

- 对应 `learning-paths/D.1.1.json` 5 个核心模块（中英双语 `status = complete`）：BCcampus、Berkeley CS186 notes / CMU 15-445（关系代数）、战德臣/王珊与厦大林子雨/国家高教智慧平台讲义。
- **综合练习 5 问映射**：(1) Student/Course/Enroll ER、基数与三关系主键/外键 → `entities`、`mapping`；(2) 4 条 SQL（选课名、按专业人数、平均分 > 85、`NOT EXISTS` 零选课学生）→ `joins`、`groups`、`subqueries`；(3) 关系代数 $\pi_{\text{name}}(\text{Student} \bowtie \text{Enroll} \bowtie \sigma_{\text{title}=\text{'Databases'}}(\text{Course}))$ → `algebra`、`sets`；(4) `R(sid,name,cid,title,grade)` 候选键 `(sid,cid)`、只到 1NF 判别及分解至 BCNF → `dependencies`、`bcnf`；(5) `ON DELETE CASCADE` 含义与误删连锁风险 → `references`。
- **后继衔接（C5）**：向 `D.1.2 数据库内核与查询优化` 交接关系代数等价改写、索引依托的键与约束、真实 SQLite 执行方案对比；向 `D.1.4`、`D.1.5`、`D.4.1`、`X.2.4` 及推荐线 `P.5.1` 交接安全参数绑定查询（防注入）、`GROUP BY HAVING COUNT(*)>1` 质量断言与三值 `NULL` 语义。
