# P.4.3 软件设计与面向对象分析设计：覆盖表

**状态（2026-11-18）：已写完。** 依据 `../cs-math-skill-tree/data/outlines/P.4.3.json`、`output/outlines.json`、`data/curation/learning-paths/P.4.3.json`，主来源为 Refactoring.Guru（22 种设计模式、6 类代码坏味、6 组重构手法）、IEEE SWEBOK v4.0a 第 3 章（Software Design）与 Cornell CS 5150（Program Design），辅以 Craig Larman GRASP 九条职责分配原则、Robert C. Martin SOLID 原则与 UML 2.5 规范，对齐 `P.4.3` 综合练习 5 问与后继 `P.4.4` 需要，本地核对脚本 `tests/content/P.4.3.verify.py`（Python 3 实测）。

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Factory Method | `creational-factories` |
| 1.2 | Abstract Factory | `creational-factories` |
| 1.3 | Builder | `creational-build-copy` |
| 1.4 | Prototype | `creational-build-copy` |
| 1.5 | Singleton | `creational-build-copy` |
| 2.1 | Adapter | `adapter-facade-proxy` |
| 2.2 | Bridge | `structural-bridge-decorator` |
| 2.3 | Composite | `structural-composite-flyweight` |
| 2.4 | Decorator | `structural-bridge-decorator` |
| 2.5 | Facade | `adapter-facade-proxy` |
| 2.6 | Flyweight | `structural-composite-flyweight` |
| 2.7 | Proxy | `adapter-facade-proxy` |
| 3.1 | Chain of Responsibility | `behavioral-command-chain` |
| 3.2 | Command | `behavioral-command-chain` |
| 3.3 | Iterator | `behavioral-iterator-mediator-visitor` |
| 3.4 | Mediator | `behavioral-iterator-mediator-visitor` |
| 3.5 | Memento | `behavioral-state-memento` |
| 3.6 | Observer | `behavioral-observer` |
| 3.7 | State | `behavioral-state-memento` |
| 3.8 | Strategy | `behavioral-strategy-template` |
| 3.9 | Template Method | `behavioral-strategy-template` |
| 3.10 | Visitor | `behavioral-iterator-mediator-visitor` |
| 4.1 | Bloaters | `code-smells` |
| 4.2 | OO Abusers | `code-smells` |
| 4.3 | Change Preventers | `code-smells` |
| 4.4 | Dispensables | `code-smells` |
| 4.5 | Couplers | `code-smells` |
| 4.6 | Other Smells | `code-smells` |
| 5.1 | Composing Methods | `refactorings` |
| 5.2 | Moving Features between Objects | `refactorings` |
| 5.3 | Organizing Data | `refactorings` |
| 5.4 | Simplifying Conditional Expressions | `refactorings` |
| 5.5 | Simplifying Method Calls | `refactorings` |
| 5.6 | Dealing with Generalization | `refactorings` |
| 6.1 | 1.1 Design Thinking | `design-context` |
| 6.2 | 1.2 Context of Software Design | `design-context` |
| 6.3 | 1.3 Key Issues in Software Design | `design-decisions` |
| 6.4 | 1.4 Software Design Principles | `ownership`、`api-contracts`、`dependency-injection`、`srp-ocp`、`lsp-isp` |
| 7.1 | 2.1 High-Level Design | `design-context`、`api-contracts`、`dependency-injection` |
| 7.2 | 2.2 Detailed Design | `ownership` |
| 8.1 | 4.1 Model-Based Design | `uml-views` |
| 8.2 | 4.2 Structural design descriptions | `class-diagrams`、`api-contracts` |
| 8.3 | 4.3 Behavioral design descriptions | `sequence-diagrams`、`activity-state` |
| 8.4 | 4.4 Design Patterns and Styles | `behavioral-strategy-template` |
| 8.5 | 4.5 Design Rationale | `design-decisions` |
| 9.1 | 5.4 Object-Oriented Design | `ownership` |
| 9.2 | 5.10 Domain-Driven Design | `domain-modeling` |
| 10.1 | Design steps | `design-context` |
| 10.2 | Program design models | `design-context` |
| 10.3 | Heavyweight vs. Lightweight design | `design-context` |
| 10.4 | Program design | `ownership` |
| 10.5 | UML models for design | `uml-views` |
| 10.6 | UML model choices | `uml-views` |
| 10.7 | Class diagram | `class-diagrams` |
| 10.8 | Relationships | `class-diagrams` |
| 10.9 | Class design | `ownership`、`grasp-roles` |
| 10.10 | Application and solution classes | `grasp-roles` |
| 10.11 | Moving towards final design | `design-loop` |

## CS2023 核心主题（C2）

`data/curation/scope.json` 为 `P.4.3` 匹配的 4 项 CS2023 主题全部落课：

| 知识点 | KA / 要求 | 课 |
|---|---|---|
| UML | DM-Modeling / KA Core：UML diagrams | `uml-views`、`class-diagrams`、`sequence-diagrams`、`activity-state` |
| 接口 | SE-Design / KA Core：API design principles | `api-contracts`、`dependency-injection`、`adapter-facade-proxy` |
| 设计原则 | SE-Design / CS Core：System design principles | `ownership`、`grasp-roles`、`srp-ocp`、`lsp-isp`、`design-decisions` |
| 模式与重构 | SE-Refactoring / KA Core：Standard refactoring patterns | `creational-factories` 至 `refactorings`（全部 11 课） |

## 综合练习与前置/后继映射（C3 / C4 / C5）

- **综合练习 5 问映射（C4）**：
  - 第 (1) 问诊断 `ReportGenerator.generate(fmt)` 违反的 SOLID 原则及后果 → `srp-ocp`（SRP 与 OCP 违背分析）、`dependency-injection`（DIP 违背分析）。
  - 第 (2) 问将输出格式重构为策略模式 `Formatter(Protocol)` 并说明新增 `PdfFormatter` 需改哪些代码 → `behavioral-strategy-template`。
  - 第 (3) 问用依赖倒置与依赖注入解耦数据库（`SalesRepository` + `FakeRepo` 单元测试返回 `"total,7"`）→ `dependency-injection`。
  - 第 (4) 问实现股票价格观察者模式（`Observer(Protocol)` + `Stock.attach/set_price`）→ `behavioral-observer`。
  - 第 (5) 问用文字描述下单流程（`OrderController`、`OrderService`、`Inventory`、`Payment`）含失败释放库存补偿分支的 UML 时序图 → `sequence-diagrams`。
- **前后继状态（C3 / C5）**：
  - 必须前置为 `P.1.2`（及递归 `P.1.1`，共继承 86 个术语，含 `封装`、`不变量`、`接口`、`子类型`、`多态`、`组合`、`委托`、`泛型`、`迭代器` 等）。`data/jargon.yaml` 中的 `信息专家`、`变化预防`、`限界上下文`、`依赖倒置`、`里氏替换`、`代码坏味`、`视图` 等术语均在首次使用前由卡片正式定义并列入 `terms`。
  - 必须后继技能为 `P.4.4 软件架构`（C5）：本包在 `design-context`（高层设计）、`uml-views`（多视图）、`activity-state`（组件与部署视图）、`api-contracts`（稳定接口契约）和 `design-decisions`（设计理由记录）中完整铺垫 `P.4.4` 所需基础。推荐后继 `P.4.6`。
