# P.1.3 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Expressions | `expressions` |
| 1.2 | Functions | `expressions` |
| 1.3 | Debugging | `expressions` |
| 2.1 | Lists | `immutable` |
| 2.2 | Variants | `variants` |
| 2.3 | Records and Tuples | `structured` |
| 2.4 | Advanced Pattern Matching | `structured` |
| 2.5 | Options | `variants` |
| 2.6 | Algebraic Data Types | `trees` |
| 2.7 | Example: Natural Numbers | `trees` |
| 3.1 | Higher-Order Functions | `higher` |
| 3.2 | Map | `map-filter` |
| 3.3 | Filter | `map-filter` |
| 3.4 | Fold | `fold` |
| 3.5 | Beyond Lists | `pipeline` |
| 3.6 | Pipelining | `pipeline` |
| 3.7 | Currying | `higher` |
| 3.8 | Algebraic Laws for Higher-Order Functions | `pipeline` |
| 4.1 | Refs | `mutation` |
| 4.2 | Mutable Fields | `mutation` |
| 4.3 | Arrays and Loops | `mutation` |
| 5.1 | Logic Programming Concepts | `prolog` |
| 5.2 | Prolog | `prolog` |
| 5.3 | Resolution and Unification | `unification-search` |
| 5.4 | Lists | `lists-db` |
| 5.5 | Search/Execution Order | `unification-search` |
| 5.6 | Database Manipulation | `lists-db` |
| 5.7 | Logic Programming in Perspective | `lists-db`, `sql` |

## CS2023 与原综合练习

- FPL-Functional CS Core 的无副作用编程、高阶函数和结构化数据处理分别见 `immutable`、`higher` 至 `pipeline`、`variants` 至 `trees`。保留可变引用、字段与数组的对照。 [Cornell OCaml 教材](https://cs3110.github.io/textbook/cover.html)
- FPL-Logic KA Core 的 Horn 子句、事实、目标与子目标见 `prolog` 和 `unification-search`。用祖先查询练习合一、回溯、目标顺序及有限搜索条件。 [Programming Language Pragmatics](https://www.cs.rochester.edu/u/scott/pragmatics/) · [SWI-Prolog 入门](https://www.swi-prolog.org/pldoc/man?section=quickstart)
- 原题 1 的递归、变换、筛选与折叠见 `map-filter`、`fold`；原题 2 的树深与镜像见 `trees`，明确空树深度为零。原题 3 的按课分组、筛组和排序见 `sql`；原题 4 的祖先解和查找顺序见 `unification-search`。 [SQLite SELECT](https://www.sqlite.org/lang_select.html)
