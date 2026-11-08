# P.4.3 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Factory Method | `factories` |
| 1.2 | Abstract Factory | `factories` |
| 1.3 | Builder | `construction` |
| 1.4 | Prototype | `construction` |
| 1.5 | Singleton | `construction` |
| 2.1 | Adapter | `adapter-facade-proxy` |
| 2.2 | Bridge | `bridge-decorator` |
| 2.3 | Composite | `composite-flyweight` |
| 2.4 | Decorator | `bridge-decorator` |
| 2.5 | Facade | `adapter-facade-proxy` |
| 2.6 | Flyweight | `composite-flyweight` |
| 2.7 | Proxy | `adapter-facade-proxy` |
| 3.1 | Chain of Responsibility | `command-chain` |
| 3.2 | Command | `command-chain` |
| 3.3 | Iterator | `iterator-visitor` |
| 3.4 | Mediator | `mediator` |
| 3.5 | Memento | `state-memento` |
| 3.6 | Observer | `observer` |
| 3.7 | State | `state-memento` |
| 3.8 | Strategy | `strategy-template` |
| 3.9 | Template Method | `strategy-template` |
| 3.10 | Visitor | `iterator-visitor` |
| 4.1 | Bloaters | `growth-smells` |
| 4.2 | Object-Orientation Abusers | `growth-smells` |
| 4.3 | Change Preventers | `coupling-smells` |
| 4.4 | Dispensables | `growth-smells` |
| 4.5 | Couplers | `coupling-smells` |
| 4.6 | Other Smells | `coupling-smells` |
| 5.1 | Composing Methods | `local-refactor` |
| 5.2 | Moving Features between Objects | `move-refactor` |
| 5.3 | Organizing Data | `local-refactor` |
| 5.4 | Simplifying Conditional Expressions | `local-refactor` |
| 5.5 | Simplifying Method Calls | `move-refactor` |
| 5.6 | Dealing with Generalization | `move-refactor` |
| 6.1 | Design Thinking | `context` |
| 6.2 | Context of Software Design | `context` |
| 6.3 | Key Issues in Software Design | `decisions` |
| 6.4 | Software Design Principles | `ownership`, `solid`, `substitution` |
| 7.1 | High-Level Design | `context`, `contract` |
| 7.2 | Detailed Design | `design-loop`, `ownership` |
| 8.1 | Model-Based Design | `views` |
| 8.2 | Structural design descriptions | `classes`, `views`, `contract` |
| 8.3 | Behavioral design descriptions | `sequence`, `activities`, `states` |
| 8.4 | Design Patterns and Styles | `decisions`, `strategy-template` |
| 8.5 | Design Rationale | `decisions` |
| 9.1 | Object-Oriented Design | `ownership`, `classes` |
| 9.2 | Domain-Driven Design | `domain` |
| 10.1 | Design steps | `design-loop` |
| 10.2 | Program design models | `views` |
| 10.3 | Heavyweight vs. Lightweight design | `design-loop` |
| 10.4 | Program design | `ownership`, `design-loop` |
| 10.5 | UML models for design | `classes`, `sequence`, `activities`, `states`, `views` |
| 10.6 | UML model choices | `views` |
| 10.7 | Class diagram | `classes` |
| 10.8 | Relationships | `classes` |
| 10.9 | Class design | `ownership`, `design-loop` |
| 10.10 | Application and solution classes | `grasp`, `domain` |
| 10.11 | Moving towards final design | `design-loop`, `decisions` |

## CS2023 与原综合练习

- DM-Modeling KA Core 的 UML 用类、对象、时序、用例、活动、状态、包、组件和部署等视图来回答不同问题。下单时序包含库存不足、支付明确拒绝和扣款后库存确认失败的分支，区分补偿、结果未知与重试。 [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1) · [Cornell CS 5150 Program Design](https://www.cs.cornell.edu/courses/cs5150/2026sp/lecture/lec08-slides-program_design.pdf)
- SE-Design KA Core 的 API 设计见 `contract`、`injection`；CS Core 的系统设计原则见 `ownership`、`grasp`、`solid`、`substitution`、`decisions`。用订单、库存和报表讲 GRASP 九项、SOLID、接口失败约定和设计取舍。 [SWEBOK 第 3 章](https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf) · [Craig Larman 的 GRASP 章节](https://www.pearson.com/en-ca/subject-catalog/p/applying-uml-and-patterns-an-introduction-to-object-oriented-analysis-and-design-and-iterative-development/P200000000422/9780131489066) · [Fowler 的依赖注入说明](https://martinfowler.com/articles/injection.html)
- SE-Refactoring KA Core 的常用重构见 `local-refactor`、`move-refactor`。模式 22 项、坏味及重构手法的各组均在表中。模式案例以原理和辨识练习为主，常用模式另有 Java 示例。 [设计模式目录](https://refactoring.guru/design-patterns/catalog) · [代码坏味](https://refactoring.guru/refactoring/smells) · [重构手法](https://refactoring.guru/refactoring/techniques)
- 原题 1–5 分别由 `solid`、`strategy-template`、`injection`、`observer`、`sequence` 承接。用整数分累计，注入内存销售记录和格式化器。PDF 作为格式扩展示例，实际编码应委托给 PDF 库。观察者示例明确注册和取消；下单的补偿是业务操作。

## 后续技能

- P.4.4 软件架构继续使用组件、接口、部署视图与设计理由。这里用一个小型订单流程练习这些工具。
