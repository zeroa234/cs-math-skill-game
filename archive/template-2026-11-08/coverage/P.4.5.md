# P.4.5 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Why Do We Write Tests? | `evidence` |
| 1.2 | Benefits of Testing Code | `evidence` |
| 1.3 | Designing a Test Suite | `levels`, `system-test` |
| 1.4 | Test Size | `levels` |
| 1.5 | Test Scope | `levels` |
| 1.6 | The Beyoncé Rule | `evidence` |
| 1.7 | A Note on Code Coverage | `line-coverage` |
| 1.8 | The Pitfalls of a Large Test Suite | `levels`, `maintainable` |
| 1.9 | The Limits of Automated Testing | `evidence`, `system-test` |
| 2.1 | The Importance of Maintainability | `maintainable` |
| 2.2 | Preventing Brittle Tests | `maintainable`, `doubles` |
| 2.3 | Strive for Unchanging Tests | `maintainable` |
| 2.4 | Test via Public APIs | `maintainable` |
| 2.5 | Test State, Not Interactions | `maintainable`, `doubles` |
| 2.6 | Test Behaviors, Not Methods | `maintainable` |
| 2.7 | Don't Put Logic in Tests | `maintainable` |
| 2.8 | Write Clear Failure Messages | `unit-python`, `maintainable` |
| 2.9 | Tests and Code Sharing: DAMP, Not DRY | `maintainable` |
| 3.1 | The Impact of Test Doubles on Software Development | `doubles` |
| 3.2 | Test Doubles at Google | `doubles` |
| 3.3 | Basic Concepts | `doubles` |
| 3.4 | Seams | `doubles` |
| 3.5 | Mocking Frameworks | `doubles` |
| 3.6 | Faking | `doubles` |
| 3.7 | Stubbing | `doubles` |
| 3.8 | Interaction Testing | `doubles` |
| 3.9 | Prefer Realism Over Isolation | `doubles`, `integration` |
| 4.1 | What Are Larger Tests? | `integration`, `system-test` |
| 4.2 | Fidelity | `integration` |
| 4.3 | Common Gaps in Unit Tests | `integration` |
| 4.4 | Why Not Have Larger Tests? | `levels`, `integration` |
| 4.5 | Structure of a Large Test | `integration` |
| 4.6 | The System Under Test | `integration` |
| 4.7 | Test Data | `integration` |
| 4.8 | Verification | `integration` |
| 4.9 | Types of Larger Tests | `system-test` |
| 4.10 | Functional Testing of One or More Interacting Binaries | `integration` |
| 4.11 | Browser and Device Testing | `system-test` |
| 4.12 | Performance, Load, and Stress testing | `system-test` |
| 4.13 | Deployment Configuration Testing | `system-test` |
| 4.14 | Exploratory Testing | `system-test` |
| 4.15 | A/B Diff Regression Testing | `system-test` |
| 5.1 | Faults vs. Failures | `evidence`, `mutation` |
| 5.2 | Key Issues | `levels`, `test-classes` |
| 5.3 | Relationship of Testing to Other Activities | `evidence`, `quality` |
| 6.1 | The Target of the Test | `levels` |
| 6.2 | Unit Testing | `levels`, `unit-python` |
| 6.3 | Integration Testing | `integration` |
| 6.4 | System Testing | `system-test` |
| 6.5 | Acceptance Testing | `system-test` |
| 6.6 | Objectives of Testing | `evidence`, `levels` |
| 6.7 | Regression Testing | `evidence`, `system-test` |
| 6.8 | Non-functional Testing | `system-test` |
| 7.1 | Specification-Based Techniques | `test-classes` |
| 7.2 | Equivalence Partitioning | `test-classes` |
| 7.3 | Boundary-Value Analysis | `boundaries` |
| 7.4 | Random Testing | `properties`, `hypothesis` |
| 7.5 | Structure-Based Test Techniques | `line-coverage`, `branches` |
| 7.6 | Control Flow Testing | `branches`, `paths` |
| 7.7 | Data Flow Testing | `paths` |
| 7.8 | Fault-Based and Mutation Techniques | `mutation` |
| 7.9 | Usage-Based Techniques | `system-test` |
| 8.1 | Evaluation of the SUT | `quality` |
| 8.2 | Fault Density | `quality` |
| 8.3 | Life Test, Reliability Evaluation | `availability` |
| 8.4 | Reliability Growth Models | `quality` |
| 8.5 | Evaluation of the Tests Performed | `line-coverage`, `quality`, `mutation` |
| 8.6 | Fault Injection | `fault-injection` |
| 8.7 | Mutation Score | `mutation` |
| 9.1 | Before recitation: setup (5 min) | `property-lab` |
| 9.2 | Commands | `property-lab` |
| 9.3 | How you'll know your properties are any good | `property-lab`, `mutation` |
| 9.4 | Part 1: Wordle (follow along) | `property-lab` |
| 9.5 | Part 2: Merging intervals (groups of 2–3) | `property-lab` |
| 9.6 | fast-check cheat sheet | `property-lab` |

## 学习资源与综合练习

- CS2023 的 SE-Construction 单元测试与大规模测试对应 `unit-python`、`integration`、`system-test`，SE-Validation 验证工具及自动化对应 `unit-python`、`hypothesis`、`paths`，SE-Reliability 缺陷注入与移除循环对应 `mutation`、`fault-injection`、`quality`。上游无必须后继。课程按必修前置 P.1.1 起步，例题用 pytest、Hypothesis、coverage.py 和 Python 标准库。CMU 的 fast-check 练习保留性质设计与变异体验证的操作路径。[CMU 17-313 性质测试讨论课](https://cmu-313.github.io/recitations/reci7-pbt/) · [Hypothesis 教程](https://hypothesis.readthedocs.io/en/latest/)
- 原题 1 的边类、非法值、退化和参数位置由 `test-classes`、`boundaries` 覆盖；原题 2 的参数化与安排—执行—断言由 `unit-python` 覆盖。`maintainable`、`doubles`、`integration`、`system-test` 补原题 4 的分层、替身及真实环境差异。[pytest 参数化文档](https://docs.pytest.org/en/stable/how-to/parametrize.html) · [Software Engineering at Google 测试篇](https://abseil.io/resources/swe-book/html/ch11.html)
- 原题 3 的语句、分支、条件和 MC/DC 在 `line-coverage`、`branches`。原答案将两个条件的布尔取值与运行中实际求值混在一起；课程区分真值表和短路时的执行记录。真实执行时，左边为假就跳过右边。`paths` 讲控制流、数据流和 JaCoCo 报告的计数口径。[coverage.py 分支覆盖](https://coverage.readthedocs.io/en/latest/branch.html) · [JaCoCo 计数器](https://www.jacoco.org/jacoco/trunk/doc/counters.html)
- `fault-injection` 和 `mutation` 分开讲运行故障演练与改动测试对象来衡量测试；`quality`、`availability` 区分产品质量和测试充分性。原题 5 以 500 小时为平均运行时间、2 小时为平均修复时间计算长期可用性，另用 365 天换算允许的停机分钟。[SWEBOK 软件测试](https://www.computer.org/education/bodies-of-knowledge/software-engineering) · [混沌工程原则](https://principlesofchaos.org/)
