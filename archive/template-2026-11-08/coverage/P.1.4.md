# P.1.4 课程覆盖表

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
| 14.9 | Implementation of Profiling | `profile` |

## CS2023 与原综合练习

- FPL-Systems CS Core 的资源管理见 `cleanup`、`ownership`、`borrowing`。FPL-OOP KA Core 的元编程与反射见 `meta`，类型和泛型见 `typing`、`generics`、`recursive`。FPL-Parallel CS Core 的异步等待见 `await`、`promises`、`locks`。 [MIT 6.102](https://web.mit.edu/6.102/www/sp25/) · [Rust 所有权](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html) · [TypeScript 类型收窄](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)
- 原题 1 核对异常时的文件与锁清理。原题 2 用有意安排的交错重现丢失更新，再用锁保持结果；不依赖某次调度或某种 GIL 实现。原题 3 区分可重叠 I/O 等待与 CPU 工作，实际时间随环境变化。原题 4 比较相同输入的容器查询，说明缓存空间和递归深度。 [Python threading](https://docs.python.org/3/library/threading.html) · [Python asyncio](https://docs.python.org/3/library/asyncio-task.html) · [GNU gprof 手册](https://sourceware.org/binutils/docs/gprof/)
