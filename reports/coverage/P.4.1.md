# P.4.1 软件工程基础与开发方法：覆盖表

**状态（2026-11-17）：已写完。** 依据 `../cs-math-skill-tree/data/outlines/P.4.1.json`、`../cs-math-skill-tree/output/outlines.json` 与 `../cs-math-skill-tree/data/curation/learning-paths/P.4.1.json`，主来源为 Amy J. Ko *Cooperative Software Development*、IEEE CS *SWEBOK v4.0a*（ch10、ch11、ch14、ch18）及 *2020 Scrum Guide*，并对齐 `P.4.1` 综合练习 4 问及本地验证脚本 `tests/content/P.4.1.verify.py`。

| 节 | 原文 | 课 |
|---|---|---|
| 1 | Process | `lifecycle` |
| 2 | Organizations | `teams` |
| 3 | Communication | `teams`、`collaboration` |
| 4 | Productivity | `forecast`、`feedback` |
| 5 | Quality | `feedback`、`principles` |
| 6.1 | Software Engineering Process Definition | `lifecycle` |
| 6.2 | Life Cycle Definition, Process Categories, and Terminology | `lifecycle` |
| 6.3 | Rationale for Life Cycles | `lifecycle` |
| 6.4 | The Concepts of Process Models and Life Cycle Models | `models` |
| 6.5 | Some Paradigms for Development Life Cycle Models | `models` |
| 6.6 | Development Life Cycle Models and Their Engineering Dimension | `models` |
| 6.7 | The Management of SLCPs | `tailoring` |
| 6.8 | Software Life Cycle Adaptation | `tailoring` |
| 6.9 | Overview of Software Process Assessment and Improvement | `assessment` |
| 6.10 | Goal-Question-Metric (GQM) | `assessment` |
| 6.11 | Framework-Based Methods | `assessment` |
| 6.12 | Process Assessment and Improvement in Agile | `assessment` |
| 7.1 | Heuristic Methods | `methods` |
| 7.2 | Formal Methods | `methods` |
| 7.3 | Prototyping Methods | `methods` |
| 7.4 | Agile Methods | `scrum`、`methods` |
| 8.1 | Dynamics of Working in Teams/Groups | `teams` |
| 8.2 | Individual Cognition | `teams` |
| 8.3 | Dealing with Problem Complexity | `principles` |
| 8.4 | Interacting with Stakeholders | `feedback` |
| 8.5 | Dealing with Uncertainty and Ambiguity | `feedback` |
| 8.6 | Team and Group Communication | `collaboration` |
| 9.1 | The Engineering Process | `lifecycle` |
| 9.2 | Abstraction and Encapsulation | `principles` |
| 9.3 | Levels of Abstraction | `principles` |
| 9.4 | Encapsulation | `principles` |
| 9.5 | Hierarchy | `principles` |

## CS2023 核心主题（C2）

`scope.json` 在 `P.4.1` 的 4 个知识点中共匹配 2 个 CS2023 核心主题；**生命周期** 与 **迭代/敏捷** 在 CS2023 未单列对应条目，按本技能大纲与学习路径全覆盖：

| 知识点 | KA / 要求 | 课 |
|---|---|---|
| 工程原则 | SE-Design · CS Core（System design principles） | `principles`、`assessment` |
| 协作与方法选择 | SE-Teamwork · CS Core（Cooperative programming） | `teams`、`feedback`、`collaboration` |
| 生命周期 / 迭代与敏捷（按技能大纲补全） | — | `lifecycle`、`models`、`tailoring`、`scrum`、`forecast`、`methods` |

## 综合练习与前置/后继映射（C3 / C4 / C5）

- **综合练习 4 问映射**：(1) 高可靠医疗/硬件受审查固件（计划驱动 V 模型/瀑布）、需求高度不确定的探索型新应用（原型与短周期敏捷反馈）及多期交付业务系统（增量+过程剪裁）→ `models`、`tailoring`；(2) 三轮速度 `[21, 18, 24]` 均值 `21` 点、`130 / 21 ≈ 6.19` 须取 `7` 冲刺（`14` 周），若死锁 `10` 周（`5` 冲刺 = `105` 点，缺口 `25` 点）须削减或切分低价值范围而非硬塞加班；区分 Scrum 三角色/五事件/三承诺 → `scrum`、`forecast`；(3) 沟通路径上界 `n(n-1)/2`（`4` 人 = `6` 条、`8` 人 = `28` 条）解释 Brooks 法则、交接与团队规模摩擦 → `teams`；(4) 代码评审、持续集成与迭代演示各自盯紧的缺陷/集成/需求偏差风险 → `feedback`、`collaboration`。
- **前后继状态（C3 / C5）**：承接 `P.1.1` 基础程序术语；向必选后继 `P.4.2`、`P.4.6`（及推荐下游 `P.4.3`、`P.4.5`）交付软件过程剪裁、信息隐蔽与团队协作基础概念。
