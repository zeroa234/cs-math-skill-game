# P.1.2 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Java Interlude 6—Mutable and Immutable Objects | `references` |
| 1.2 | Object Diagram Rules | `references` |
| 2.1 | Prelude—Designing Classes | `account`, `design-tests` |
| 2.2 | Appendix B—Java Classes | `access` |
| 3 | Lecture 5: Interfaces, subtyping | `interfaces` |
| 4.1 | Appendix C—Creating Classes from Other Classes | `inheritance`, `dispatch` |
| 5.1 | Java Interlude 1—Generics | `generic-stack`, `wildcards` |
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
| 8.5.1 | Learning object-oriented programming | `objects`, `account` |
| 8.5.2 | Removing repetitive code (overloading methods and constructors) | `overload` |
| 8.5.3 | Primitive and reference variables | `references`, `value-types` |
| 8.5.4 | Objects and references | `references` |
| 8.6.1 | Objects on a list and a list as part of an object | `composition` |
| 8.6.2 | Separating the user interface from program logic | `design-tests` |
| 8.6.3 | Introduction to testing | `design-tests` |
| 8.6.4 | Complex programs | `design-tests`, `composition` |
| 9.1.1 | Short recap | `objects`, `references` |
| 9.1.2 | Hash Map | `hashing` |
| 9.1.3 | Similarity of objects | `hashing` |
| 9.1.4 | Grouping data using hash maps | `grouping` |
| 9.1.5 | Fast data fetching and grouping information | `grouping` |
| 9.2.1 | Class inheritance | `inheritance` |
| 9.2.2 | Interfaces | `interfaces` |
| 9.2.3 | Object polymorphism | `dispatch` |
| 9.3.1 | Handling collections as streams | `stream-sort` |
| 9.3.2 | The Comparable Interface | `stream-sort` |
| 9.3.3 | Other useful techniques | `java-flow`, `text-tools`, `value-types`, `collections` |
| 9.4.1 | Class diagrams | `design-tests` |
| 9.4.2 | Packages | `access` |
| 9.4.3 | Exceptions | `exceptions` |
| 9.4.4 | Processing files | `text-io`, `byte-io` |
| 9.5.1 | Type parameters | `generic-stack`, `wildcards` |
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

## CS2023 与原综合练习

- FPL-OOP CS Core 的面向对象设计、封装、继承、子类型、组合取舍与异常，分别见 `objects`、`account`、`inheritance`、`interfaces`、`composition`、`exceptions`。FPL-Types CS Core 的泛型见 `generic-stack`、`generic-bag`、`wildcards`。FPL-OOP KA Core 的集合与迭代器见 `collections`。 [Cornell CS 2110](https://www.cs.cornell.edu/courses/cs2110/2023fa/) · [Dev.java](https://dev.java/learn/)
- SDF-Fundamentals CS Core 的文件与 API I/O 见 `text-io`、`byte-io`。FPL-Parallel CS Core 的线程见 `threads`、`synchronization`、`executors`。Maven 独立补齐生命周期、阶段、目标与绑定。 [Java Concurrency](https://docs.oracle.com/javase/tutorial/essential/concurrency/) · [Maven Build Lifecycle](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html)
- 原题 1–6 依次在 `account`、`dispatch`、`composition`、`generic-stack`、`hashing`、`exceptions`。账户检查起始余额和正数金额，正向加款还检查溢出。正方形问题明确限定矩形的宽高可分别修改。空栈行为和泛型的编译期约束分别验证。 [赫尔辛基大学 Java MOOC](https://java-programming.mooc.fi/) · [廖雪峰 Java 教程](https://liaoxuefeng.com/books/java/introduction/index.html)

## 后续技能

- P.4.3 将使用类图、接口协作、组合与委托。这里从简单的借书台对象、可换的通知服务和可测试的业务方法开始。
