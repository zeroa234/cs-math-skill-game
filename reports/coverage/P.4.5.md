# P.4.5 软件测试、质量与可靠性：覆盖表

**状态（2026-11-17）：已写完。** 依据 `../cs-math-skill-tree/data/outlines/P.4.5.json` 与 `../cs-math-skill-tree/output/outlines.json`，主来源为 Google *Software Engineering at Google*（ch11–14）、*SWEBOK v4.0a* ch5 及 CMU 17-313 *Recitation 7: Property-Based Testing*。

必须前置仅为 `P.1.1 程序设计基础`；内部 4 章（`original` 顺序）：`1. 单元/集成/系统测试`、`2. 性质测试`、`3. 覆盖率`、`4. 故障注入与质量评估`。

`node scripts/check-coverage.mjs P.4.5` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | A Testing Overview | `evidence` |
| 1.2 | A Why Do We Write Tests? | `evidence` |
| 1.3 | A Benefits of Testing Code | `evidence` |
| 1.4 | A Designing a Test Suite | `levels` |
| 1.5 | A Test Size | `levels` |
| 1.6 | A Test Scope | `levels` |
| 1.7 | A The Beyoncé Rule | `evidence`、`maintainable` |
| 1.8 | A A Note on Code Coverage | `line-coverage` |
| 1.9 | A Testing at Google Scale | `levels` |
| 2.1 | A Unit Testing | `unit-python` |
| 2.2 | A The Power of Maintainability | `maintainable` |
| 2.3 | A Preventing Brittle Tests | `maintainable` |
| 2.4 | A Strive for Unchanging Tests | `maintainable` |
| 2.5 | A Test via Public APIs | `maintainable` |
| 2.6 | A Test State, Not Interactions | `doubles`、`maintainable` |
| 2.7 | A Writing Clear Tests | `unit-python` |
| 2.8 | A Make Your Tests Complete and Concise | `unit-python` |
| 2.9 | A Tests as Documentation | `unit-python` |
| 3.1 | A Test Doubles | `doubles` |
| 3.2 | A The Impact of Test Doubles on Software Development | `doubles` |
| 3.3 | A Test Doubles at Google | `doubles` |
| 3.4 | A Basic Concepts | `doubles` |
| 3.5 | A Techniques for Using Test Doubles | `doubles` |
| 3.6 | A Real Implementations | `doubles` |
| 3.7 | A Faking | `doubles` |
| 3.8 | A Stubbing | `doubles` |
| 3.9 | A Interaction Testing | `doubles` |
| 4.1 | A Larger Testing | `integration`、`system-test` |
| 4.2 | A What Are Larger Tests? | `integration` |
| 4.3 | A Fidelity | `integration` |
| 4.4 | A Common Gaps in Unit Tests | `integration` |
| 4.5 | A Why Not Have Only Larger Tests? | `levels`、`system-test` |
| 4.6 | A Larger Tests at Google | `system-test` |
| 4.7 | A Larger Tests and Time | `system-test` |
| 4.8 | A The Structure of a Larger Test | `system-test` |
| 4.9 | A The System Under Test | `integration` |
| 4.10 | A Test Data | `system-test` |
| 4.11 | A Verification | `system-test` |
| 4.12 | A Types of Larger Tests | `integration`、`system-test` |
| 4.13 | A Functional Testing of One or More Interacting Services | `integration` |
| 4.14 | A Browser and Device Testing | `system-test` |
| 4.15 | A Performance, Load, and Stress Testing | `system-test` |
| 5.1 | B Software Testing Fundamentals | `quality` |
| 5.2 | B Testing-Related Terminology | `evidence` |
| 5.3 | B Key Issues | `quality` |
| 6.1 | B Test Levels | `levels` |
| 6.2 | B Unit Testing | `unit-python` |
| 6.3 | B Integration Testing | `integration` |
| 6.4 | B System Testing | `system-test` |
| 6.5 | B Acceptance Testing | `system-test` |
| 6.6 | B Regression Testing | `evidence`、`maintainable` |
| 6.7 | B Alpha and Beta Testing | `system-test` |
| 6.8 | B Conformance Testing | `system-test` |
| 7.1 | B Test Techniques | `test-classes` |
| 7.2 | B Based on the Tester's Intuition and Experience | `test-classes` |
| 7.3 | B Input Domain-Based Techniques | `test-classes`、`boundaries` |
| 7.4 | B Code-Based Techniques | `line-coverage`、`properties` |
| 7.5 | B Fault-Based Techniques | `mutation`、`line-coverage` |
| 7.6 | B Usage-Based Techniques | `quality` |
| 7.7 | B Model-Based Testing Techniques | `boundaries` |
| 7.8 | B Techniques Based on the Nature of the Application | `fault-injection` |
| 7.9 | B Selecting and Combining Techniques | `levels`、`quality` |
| 8.1 | B Test-Related Measures | `quality` |
| 8.2 | B Evaluation of the Program Under Test | `quality`、`availability` |
| 8.3 | B Fault Density | `quality` |
| 8.4 | B Life Testing, Reliability Evaluation | `availability` |
| 8.5 | B Coverage/Thoroughness Measures | `line-coverage`、`branches`、`paths` |
| 8.6 | B Fault Seeding | `mutation`、`fault-injection` |
| 8.7 | B Mutation Score | `mutation` |
| 9.1 | C Recitation 7: Property-Based Testing | `properties` |
| 9.2 | C Why Write Properties? | `properties` |
| 9.3 | C Generators and Shrinking | `hypothesis` |
| 9.4 | C Designing Good Properties | `properties`、`property-lab` |
| 9.5 | C Stateful & Metamorphic Testing | `property-lab` |
| 9.6 | C Combining Examples and Properties | `property-lab` |

## CS2023 核心主题（C2）

`scope.json` 在 `P.4.5` 的 4 个章节中共匹配 3 个 CS2023 主题；**性质测试** 在 `scope.json` 中无对应条目，按学习路径与技能核心章节照常全覆盖：

| 知识点 | KA / 要求 | 课 |
|---|---|---|
| 单元/集成/系统测试 | SE-Construction · CS Core / KA Core（Unit testing；Larger-scale testing） | `unit-python`、`integration`、`system-test` |
| 覆盖率 | SE-Validation · KA Core（Verification and validation tooling and automation） | `line-coverage`、`branches`、`paths` |
| 故障注入与质量评估 | SE-Reliability · KA Core（Defect injection and removal cycle） | `mutation`、`fault-injection`、`quality`、`availability` |
| 性质测试（按技能与学习路径覆盖） | — | `properties`、`hypothesis`、`property-lab` |

## 学习路径、综合练习与后继状态（C3 / C4 / C5）

- 对应 `learning-paths/P.4.5.json` 全部 4 个模块（中英双语 `status = complete`）：*SE at Google* ch11–14、测试金字塔分层表、白盒覆盖率指南（语句/判定/条件/MC/DC 与插桩）、Hypothesis 属性测试文档及混沌工程 4 步受控演练（含错误预算与稳态假说）。
- **综合练习 5 问映射**：(1) `classify_triangle(a,b,c)` 等价类 + 边界值（含 `(1,2,3)` 非法）≥8 用例 → `test-classes`、`boundaries`；(2) `pytest` `@pytest.mark.parametrize` 与 Arrange–Act–Assert → `unit-python`；(3) `if a > 0 and b > 0` 语句/分支/条件（按真实短路求值区分真值表）/MC/DC 最小 `3` 例 → `line-coverage`、`branches`、`paths`；(4) 测试金字塔分层、`Mock` vs `Fake` 与过度 Mock 脆弱耦合风险 → `levels`、`doubles`、`maintainable`；(5) `MTBF = 500h, MTTR = 2h` 得可用性 `500/502 ≈ 99.60%` 及 `99.99%` 年停机 `52.56` 分钟 → `availability`（注：明晰无故障均值口径并对比故障植入与变异得分）。
- **后继状态（C5）**：`P.4.5` 无下游必选后继（`unlocks: []`）；作为推荐前置向 `P.4.6` 交接“回归测试”“测试防护网”与基础 `Seams` 概念。
