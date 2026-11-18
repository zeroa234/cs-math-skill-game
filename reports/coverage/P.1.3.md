# P.1.3 函数式、逻辑式与声明式编程：覆盖表

**状态（2026-11-18）：已写完。** 依据 `../cs-math-skill-tree/data/outlines/P.1.3.json`、`output/outlines.json`、`data/curation/learning-paths/P.1.3.json`，主来源为 Cornell CS 3110《OCaml Programming: Correct + Efficient + Beautiful》（第 2–4、6 章）与 Michael L. Scott《Programming Language Pragmatics, 4e》（第 12 章），辅以《Composing Programs》1.6/3.2/4.2/4.3、《Learn Prolog Now!》第 1–2 章与《Rust 程序设计语言》第 3–4、6、19 章思路，对齐 `P.1.3` 综合练习 4 问，本地核对脚本 `tests/content/P.1.3.verify.py`（通过 OCaml 5.4.0、SWI-Prolog 9.2.9 与 Python SQLite3 实测）。

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | 2.3 Expressions | `expressions` |
| 1.2 | 2.4 Functions | `expressions` |
| 1.3 | 2.7 Debugging | `expressions` |
| 2.1 | 3.1 Lists | `immutable` |
| 2.2 | 3.2 Variants | `variants-options` |
| 2.3 | 3.4 Records and Tuples | `records-matching` |
| 2.4 | 3.5 Advanced Pattern Matching | `records-matching` |
| 2.5 | 3.7 Options | `variants-options` |
| 2.6 | 3.9 Algebraic Data Types | `adt-trees` |
| 2.7 | 3.12 Example: Natural Numbers | `adt-trees` |
| 3.1 | 4.1 Higher-Order Functions | `higher-currying` |
| 3.2 | 4.2 Map | `map-filter` |
| 3.3 | 4.3 Filter | `map-filter` |
| 3.4 | 4.4 Fold | `fold-tail` |
| 3.5 | 4.5 Beyond Lists | `beyond-pipeline` |
| 3.6 | 4.6 Pipelining | `beyond-pipeline` |
| 3.7 | 4.7 Currying | `higher-currying` |
| 3.8 | 4.8 Algebraic Laws for Higher-Order Functions | `beyond-pipeline` |
| 4.1 | 6.1 Refs | `mutation` |
| 4.2 | 6.2 Mutable Fields | `mutation` |
| 4.3 | 6.3 Arrays and Loops | `mutation` |
| 5.1 | 12.1 Logic Programming Concepts | `prolog-basics` |
| 5.2 | 12.2 Prolog | `prolog-basics` |
| 5.3 | 12.2.1 Resolution and Unification | `unification-search` |
| 5.4 | 12.2.2 Lists | `prolog-lists-db` |
| 5.5 | 12.2.4 Search/Execution Order | `unification-search` |
| 5.6 | 12.2.7 Database Manipulation | `prolog-lists-db` |
| 5.7 | 12.4 Logic Programming in Perspective | `prolog-lists-db`、`declarative-sql` |

## CS2023 核心主题（C2）

`data/curation/scope.json` 为 `P.1.3` 匹配的 4 项 CS2023 主题全部落课：

| 知识点 | KA / 要求 | 课 |
|---|---|---|
| 不可变数据 | FPL-Functional / CS Core：Effect-free programming | `expressions`、`immutable`、`mutation` |
| 高阶函数 | FPL-Functional / CS Core：Using higher-order functions | `higher-currying`、`map-filter`、`fold-tail`、`beyond-pipeline` |
| 模式匹配 | FPL-Functional / CS Core：Processing structured data (e.g., trees) via functions | `variants-options`、`records-matching`、`adt-trees` |
| 规则与查询式表达 | FPL-Logic / KA Core：Definitions of Horn clause, facts, goals and subgoals | `prolog-basics`、`unification-search`、`prolog-lists-db`、`declarative-sql` |

## 综合练习与前置/后继映射（C3 / C4 / C5）

- **综合练习 4 问映射（C4）**：
  - 第 (1) 问不用循环和可变变量，用递归写出 `sum`、`map`、`filter`、`foldl`，并解释尾递归与栈帧复用 → `immutable`（`sum`）、`map-filter`（手写递归 `my_map` 与 `my_filter`）、`fold-tail`（`foldl` 与 `sum_tail` 对比、**尾递归**与调用栈）。
  - 第 (2) 问用代数数据类型定义二叉树 `type 'a tree = Leaf | Node of 'a tree * 'a * 'a tree`，用模式匹配写 `depth` 与 `mirror` 并依赖编译器穷尽性检查 → `variants-options`（穷尽性检查）、`adt-trees`（`depth`、`mirror` 与结构递归）。
  - 第 (3) 问声明式 SQL 查询 `Enroll` 表中平均分 ≥ 80 的课程并降序排列，解释 `AVG` 对 `NULL` 的处理及声明式与命令式差异 → `declarative-sql`（含 `Enroll` 与 `Student` 联表概念、`GROUP BY` / `HAVING` / `ORDER BY` 及查询优化器对比）。
  - 第 (4) 问 Prolog 事实 `parent(tom, bob). parent(bob, ann). parent(bob, pat).`、规则 `grandparent/2` 与递归 `ancestor/2`，追踪查询 `?- ancestor(X, ann).` 通过回溯得到 `bob` 与 `tom` → `prolog-basics`（`parent/2`、`grandparent/2`）、`unification-search`（`ancestor/2` 合一与回溯轨迹）。
- **前后继状态（C3 / C5）**：
  - 必须前置为 `P.1.1` 程序设计基础（已按 v2 写完；继承 `变量`、`赋值`、`别名`、`可变`、`不可变`、`列表`、`元组`、`函数`、`调用栈` 等 50 个术语，未继承 `递归`、`数组`，本包在首次使用前明确定义 `递归`、`数组` 等概念）。推荐前置 `M.5.3` 与 `F.1.1`（不继承术语）。
  - 无任何技能以 `P.1.3` 为必须前置（仅作 `F.3.1`、`F.3.2`、`F.3.3`、`F.3.4`、`P.3.1`、`S.5.1` 的推荐前置，C5 无硬性未覆盖缺口）。
