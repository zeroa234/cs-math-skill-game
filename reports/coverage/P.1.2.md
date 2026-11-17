# P.1.2 面向对象程序设计：覆盖表

**状态（2026-11-17）：已写完。** 依据 `../cs-math-skill-tree/data/outlines/P.1.2.json`、`../cs-math-skill-tree/output/outlines.json` 与 `../cs-math-skill-tree/data/curation/learning-paths/P.1.2.json`，主来源为 Cornell CS 2110、University of Helsinki *Java Programming*、Oracle *Java Tutorials* 与 Apache Maven 指南，并由 `tests/content/P.1.2.verify.py` 使用本地 JDK 21（`javac` + `java`）实测全部示例、契约拒绝与类型报错。

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Java Interlude 6—Mutable and Immutable Objects | `references` |
| 1.2 | Object Diagram Rules | `references` |
| 2.1 | Prelude—Designing Classes | `account`、`design-tests` |
| 2.2 | Appendix B—Java Classes | `access` |
| 3 | Lecture 5: Interfaces, subtyping | `interfaces` |
| 4.1 | Appendix C—Creating Classes from Other Classes | `inheritance`、`dispatch` |
| 5.1 | Java Interlude 1—Generics | `generic-stack`、`wildcards` |
| 5.2 | Chapter 1—Bags | `generic-bag` |
| 5.3 | Chapter 2—Bag Implementations That Use Arrays | `generic-bag` |
| 6.1 | What Is an Object? | `objects` |
| 6.2 | What Is a Class? | `objects` |
| 6.3 | What Is Inheritance? | `inheritance` |
| 6.4 | What Is an Interface? | `interfaces` |
| 6.5 | What Is a Package? | `access` |
| 7 | Objects on a list and a list as part of an object | `composition` |
| 8.1.1 | Getting started with programming | `java-start` |
| 8.1.2 | Printing | `java-start` |
| 8.1.3 | Reading input | `java-start` |
| 8.1.4 | Variables | `java-start` |
| 8.1.5 | Calculating with numbers | `java-start` |
| 8.1.6 | Conditional statements and conditional operation | `java-flow` |
| 8.2.1 | Recurring problems and patterns to solve them | `java-flow` |
| 8.2.2 | Repeating functionality | `java-flow` |
| 8.2.3 | More loops | `java-flow` |
| 8.2.4 | Methods and dividing the program into smaller parts | `java-flow` |
| 8.3.1 | Discovering errors | `design-tests` |
| 8.3.2 | Lists | `collections` |
| 8.3.3 | Arrays | `arrays` |
| 8.3.4 | Using strings | `arrays` |
| 8.4.1 | Introduction to object-oriented programming | `objects` |
| 8.4.2 | Objects in a list | `composition` |
| 8.4.3 | Files and reading data | `text-io` |
| 8.5.1 | Learning object-oriented programming | `objects`、`account` |
| 8.5.2 | Removing repetitive code (overloading methods and constructors) | `overload` |
| 8.5.3 | Primitive and reference variables | `references`、`value-types` |
| 8.5.4 | Objects and references | `references` |
| 8.6.1 | Objects on a list and a list as part of an object | `composition` |
| 8.6.2 | Separating the user interface from program logic | `design-tests` |
| 8.6.3 | Introduction to testing | `design-tests` |
| 8.6.4 | Complex programs | `design-tests`、`composition` |
| 9.1.1 | Short recap | `objects`、`references` |
| 9.1.2 | Hash Map | `hashing` |
| 9.1.3 | Similarity of objects | `hashing` |
| 9.1.4 | Grouping data using hash maps | `grouping` |
| 9.1.5 | Fast data fetching and grouping information | `grouping` |
| 9.2.1 | Class inheritance | `inheritance` |
| 9.2.2 | Interfaces | `interfaces` |
| 9.2.3 | Object polymorphism | `dispatch` |
| 9.3.1 | Handling collections as streams | `stream-sort` |
| 9.3.2 | The Comparable Interface | `stream-sort` |
| 9.3.3 | Other useful techniques | `java-flow`、`text-tools`、`value-types`、`collections` |
| 9.4.1 | Class diagrams | `design-tests` |
| 9.4.2 | Packages | `access` |
| 9.4.3 | Exceptions | `exceptions` |
| 9.4.4 | Processing files | `text-io`、`byte-io` |
| 9.5.1 | Type parameters | `generic-stack`、`wildcards` |
| 9.5.2 | ArrayList and hash table | `container-storage` |
| 9.5.3 | Randomness | `arrays` |
| 9.5.4 | Multidimensional data | `arrays` |
| 10.1 | Processes and Threads | `threads` |
| 10.2 | Defining and Starting a Thread | `threads` |
| 10.3 | Interrupts | `threads` |
| 10.4 | Joins | `threads` |
| 10.5 | Synchronization | `synchronization` |
| 10.6 | Thread Interference | `synchronization` |
| 10.7 | Synchronized Methods | `synchronization` |
| 10.8 | Liveness | `executors` |
| 10.9 | Deadlock | `synchronization` |
| 10.10 | High Level Concurrency Objects | `executors` |
| 10.11 | Thread Pools | `executors` |
| 11.1 | Build Lifecycle Basics | `maven` |
| 11.2 | A Build Lifecycle is Made Up of Phases | `maven` |
| 11.3 | Usual Command Line Calls | `maven` |
| 11.4 | A Build Phase is Made Up of Plugin Goals | `maven` |
| 11.5 | Built-in Lifecycle Bindings | `maven` |

## CS2023 核心主题（C2）

`scope.json` 在 `P.1.2` 的 11 个知识点中共匹配 10 个 CS2023 主题；其中第 11 章里的“构建工具（Maven）”在 CS2023 中无单列条目，依据本技能大纲补齐：

| 知识点 | KA / 要求 | 课 |
|---|---|---|
| 对象 / 封装 / 继承 / 接口 / 组合 | FPL-OOP · CS Core（OOP design, encapsulation, inheritance, subtyping, composition） | `objects`、`account`、`inheritance`、`interfaces`、`composition` |
| 泛型与对象协作 | FPL-Types · CS Core（Generic types / parametric polymorphism） | `generic-stack`、`generic-bag`、`wildcards` |
| 集合 | FPL-OOP · KA Core（Collection classes, iterators） | `collections`、`hashing`、`container-storage`、`grouping`、`stream-sort` |
| 异常 / I/O | FPL-OOP / SDF-Fundamentals · CS Core（Exception handling; Input and output） | `exceptions`、`text-io`、`byte-io` |
| 并发基础与构建工具 | FPL-Parallel · CS Core（Threads）＋ Maven 补齐 | `threads`、`synchronization`、`executors`、`maven` |

## 综合练习与前置/后继映射（C3 / C4 / C5）

- **综合练习 6 问映射**：(1) `BankAccount` 封装与不变量（构造拒负初始额、存取拒非正金额、取款防超额、溢出保护）→ `account`；(2) `Shape` 多态统一面积调用与运行期动态分派 → `dispatch`；(3) 组合 vs 继承与正方形–长方形（Square–Rectangle）里氏替换违反解析 → `composition`；(4) 泛型 `Stack<T>` 抽象与编译期类型隔离 → `generic-stack`；(5) `==` 引用相等 vs `.equals()` 内容相等与 `hashCode` 协同契约 → `hashing`；(6) 受检异常（`InsufficientFundsException`）与非受检异常（编程错误）权衡取舍 → `exceptions`。
- **前后继状态（C3 / C5）**：承接 `P.1.1` 过程式编程基础；作为必选前置向 `P.4.3`（软件设计与面向对象分析设计）交付封装不变量、接口与子类型多态、委托组合及泛型协变协作等核心概念。
