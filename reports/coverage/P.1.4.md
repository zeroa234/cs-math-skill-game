# P.1.4 高级程序设计：覆盖表

**状态（2026-11-18）：已写完（v2 重写，按零基础与知识覆盖面标准重写）。** 依据 `../cs-math-skill-tree/data/outlines/P.1.4.json`、`output/outlines.json`、`../cs-math-skill-tree/data/curation/learning-paths/P.1.4.json`，主来源为 MIT 6.102 Software Construction（Spring 2025）、Rust 官方书《The Rust Programming Language》第 4 章（所有权/借用/切片）与 GNU `gprof` 手册，辅以 Python 官方文档（上下文管理器、`threading`、`asyncio`、`functools.lru_cache`、`timeit`）及 C++ RAII 实践，对齐 `P.1.4` 综合练习 4 问，本地核对脚本 `tests/content/P.1.4.verify.py`（Python 3 + WSL `gcc`/`g++`/`gprof` + 便携 `rustc 1.93` 实测）。

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Static typing | `typing` |
| 1.2 | Static checking, dynamic checking, no checking | `typing` |
| 1.3 | Mutating values vs. reassigning variables | `typing` |
| 1.4 | Hacking vs. engineering | `typing` |
| 2.1 | Test-first programming | `testing` |
| 2.2 | Systematic testing | `testing` |
| 2.3 | Choosing test cases by partitioning | `testing` |
| 2.4 | Automated unit testing | `testing` |
| 2.5 | Black box and glass box testing | `testing` |
| 2.6 | Automated regression testing | `testing` |
| 3.1 | Behavioral equivalence | `specs` |
| 3.2 | Specification structure | `specs` |
| 3.3 | Specifications in TypeScript | `specs` |
| 3.4 | Specifications for mutating functions | `specs` |
| 4.1 | What abstraction means | `abstraction` |
| 4.2 | Classifying types and operations | `abstraction` |
| 4.3 | An abstract type is defined by its operations | `abstraction` |
| 4.4 | Designing an abstract type | `abstraction` |
| 4.5 | Representation independence | `abstraction` |
| 5.1 | Invariants | `representation` |
| 5.2 | Rep invariant and abstraction function | `representation` |
| 5.3 | Benevolent side-effects | `representation` |
| 5.4 | Documenting the AF, RI, and safety from rep exposure | `representation` |
| 6.1 | Interfaces | `generics` |
| 6.2 | Subtypes | `generics` |
| 6.3 | Generic types | `generics` |
| 6.4 | Enumerations | `generics` |
| 6.5 | ADTs in non-OOP languages | `recursive` |
| 6.6 | ADTs in TypeScript | `recursive` |
| 7.1 | Recursive data type definitions | `recursive` |
| 7.2 | Functions over recursive data types | `recursive` |
| 7.3 | Dynamic type inspection | `recursive` |
| 7.4 | Immutability and performance | `recursive` |
| 8.1 | A rogue’s gallery of bugs | `debugging` |
| 8.2 | First defense: make bugs impossible | `debugging` |
| 8.3 | Second defense: make bugs easy to find | `debugging` |
| 8.4 | Reproduce the bug | `debugging` |
| 8.5 | Find the bug using the scientific method | `debugging` |
| 9.1 | Two models for concurrent programming | `shared` |
| 9.2 | Processes, threads, time-slicing | `shared` |
| 9.3 | Interleaving | `shared` |
| 9.4 | Race condition | `shared` |
| 9.5 | Message passing example | `messages` |
| 10.1 | Await | `await` |
| 10.2 | Asynchronous functions | `await` |
| 10.3 | Aggregating promises | `promises` |
| 10.4 | Never busy-wait | `await` |
| 10.5 | Promises and exception handling | `promises` |
| 11.1 | Asynchronous methods | `locks` |
| 11.2 | Race conditions | `locks` |
| 11.3 | Deadlock | `locks` |
| 11.4 | Interleaving and mutual exclusion | `locks` |
| 11.5 | Other techniques for mutual exclusion | `locks` |
| 12.1 | Message passing between workers | `messages` |
| 12.2 | Client/server design pattern | `messages` |
| 12.3 | Networking basics | `messages` |
| 12.4 | Web APIs | `messages` |
| 13.1 | What is Ownership? | `ownership` |
| 13.2 | References and Borrowing | `borrowing` |
| 13.3 | The Slice Type | `borrowing` |
| 14.1 | Introduction to Profiling | `profile` |
| 14.2 | Compiling a Program for Profiling | `profile` |
| 14.3 | Executing the Program | `profile` |
| 14.4 | Interpreting gprof’s Output | `profile` |
| 14.5 | The Flat Profile | `profile-reading` |
| 14.6 | The Call Graph | `profile-reading` |
| 14.7 | Line-by-line Profiling | `profile-reading` |
| 14.8 | Statistical Sampling Error | `profile-reading` |
| 14.9 | Implementation of Profiling | `profile`（另设 `complexity` 补齐 C4 第 4 问容器对比与记忆化缓存） |

## CS2023 核心主题（C2）

`../cs-math-skill-tree/data/curation/scope.json` 为 `P.1.4` 匹配的 3 项 CS2023 核心主题全部落课（“性能剖析与工程化抽象”无 CS2023 对应条目，也一并完整覆盖）：

| 知识点 | KA / 要求 | 课 |
|---|---|---|
| 资源管理 | FPL-Systems / CS Core：Memory management | `cleanup`、`ownership`、`borrowing` |
| 泛型元编程 | FPL-OOP / KA Core：Metaprogramming and reflection | `typing`、`generics`、`recursive`、`meta` |
| 异步/并发 | FPL-Parallel / CS Core：Async await | `shared`、`await`、`promises`、`locks`、`messages` |

## 综合练习与前置/后继映射（C3 / C4 / C5）

- **综合练习 4 问映射（C4）**：
  - 第 (1) 问 `with` 上下文管理器或 C++ RAII 异常安全清理 → `cleanup`（`__enter__` / `__exit__` 退出顺序、异常保证及 C++ RAII 析构机制）。
  - 第 (2) 问多线程竞态、`counter += 1` 丢失更新、加锁修复及 GIL 原因 → `shared`、`locks`（`Barrier` 复现竞态、`with lock:` 修复、GIL 字节码切换解释）。
  - 第 (3) 问 `asyncio` 并发 I/O vs 顺序 vs 多线程，以及纯 CPU 计算对比多进程 → `await`、`shared`、`locks`（I/O 等待重叠与释放 GIL vs `multiprocessing` 多进程计算）。
  - 第 (4) 问 `timeit` 对比 10⁶ 长度 `list` vs `set` 查找复杂度与 `lru_cache` 记忆化递归 `fib` → `complexity`（$O(n)$ vs $O(1)$ 哈希查找、`@lru_cache(maxsize=None)` 从指数降为 $O(n)$ 及空间代价）。
- **前后继状态（C3 / C5）**：
  - 必须前置仅为 `P.1.1 程序设计基础`（推荐前置 `P.1.2`、`F.1.1`、`P.2.4` 仅作参考，本包在缺少推荐前置时依然自包含）。`terms` 收录了 `作用域`、`上下文管理器`、`内存`、`编译`、`编译器`、`所有权`、`借用`、`字节`、`数组`、`泛型`、`抽象数据类型`、`递归`、`反射`、`元编程`、`进程`、`线程`、`竞态条件`、`异步等待`、`互斥锁`、`死锁`、`规格`、`表示不变量`、`抽象函数`、`性能剖析` 共 24 项，而随文用到的栈/堆、哈希、大 O 记号、装饰器、事件循环与 Python `class`/`__init__`/TypeScript/Rust/C++ 语法均在对应卡片与揭示栏内按零基础随用随释。
  - `P.1.4` 在技能树中无下游必须前置依赖（没有任何技能把 `P.1.4` 列为必须前置）；而在 `reports/coverage/P.2.4.md:109` 中，`P.2.4` 将 `P.1.4` 作为其下游推荐去向之一（承接 `P.2.4` `profile-benchmark` 的基础计时，本包进一步展开至 `gprof` 平坦剖面、调用图与采样误差，C5 无未覆盖缺口）。
