# A.4.1 机器学习工程与 MLOps：课程覆盖表

**状态（2026-11-20）：已定稿并核验（v2，按零基础与知识覆盖面标准）。** 依据 `../cs-math-skill-tree/output/outlines.json` 的 A.4.1 大纲（Made With ML MLOps 课程 1.1–8.5），并结合技能树中文与补充来源（Google Cloud MLOps 持续交付文档、Microsoft Learn MLOps 简介、Azure ML 模型注册表文档、Hopsworks Feature Store FTI 教程及 FastAPI 请求体文档）编排。全包共 10 课，覆盖全部 28 个大纲小节；11 项核对断言（含 PSI 计算、FastAPI AST 语法与校验逻辑）及全部 9 道数值题已由 `tests/content/A.4.1.verify.py` 独立核对通过。

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Setup | `ml-systems-and-versioning` |
| 1.2 | Product | `ml-systems-and-versioning` |
| 1.3 | Systems | `ml-systems-and-versioning` |
| 2.1 | Preparation | `data-prep-and-exploration` |
| 2.2 | Exploration | `data-prep-and-exploration` |
| 2.3 | Preprocessing | `data-prep-and-exploration` |
| 2.4 | Distributed | `distributed-feature-processing` |
| 2.5 | Feature Store | `feature-store-and-skew` |
| 3.1 | Training | `training-tracking-and-pipelines` |
| 3.2 | Tracking | `training-tracking-and-pipelines` |
| 3.3 | Tuning | `training-tracking-and-pipelines` |
| 3.4 | Evaluation | `training-tracking-and-pipelines` |
| 3.5 | Serving | `serving-patterns-and-rollouts`、`fastapi-inference-service` |
| 4.1 | Scripting | `reproducible-code-and-quality` |
| 4.2 | Command-line | `reproducible-code-and-quality` |
| 5.1 | Logging | `monitoring-drift-and-psi` |
| 5.2 | Documentation | `reproducible-code-and-quality` |
| 5.3 | Styling | `reproducible-code-and-quality` |
| 5.4 | Pre-commit | `reproducible-code-and-quality` |
| 6.1 | Code | `reproducible-code-and-quality` |
| 6.2 | Data | `data-model-checks-and-cicd` |
| 6.3 | Models | `data-model-checks-and-cicd` |
| 7.1 | Versioning | `ml-systems-and-versioning` |
| 8.1 | Jobs & Services | `serving-patterns-and-rollouts` |
| 8.2 | CI/CD workflows | `data-model-checks-and-cicd` |
| 8.3 | Monitoring | `monitoring-drift-and-psi` |
| 8.4 | Data engineering | `training-tracking-and-pipelines` |
| 8.5 | Orchestration | `training-tracking-and-pipelines` |

## 写法上的取舍

- 按照技能树 5 个核心章的顺序展开：第 1 章「数据/模型版本」（`ml-systems-and-versioning`）、第 2 章「特征服务」（`data-prep-and-exploration`、`distributed-feature-processing`、`feature-store-and-skew`）、第 3 章「训练管线」（`reproducible-code-and-quality`、`training-tracking-and-pipelines`、`data-model-checks-and-cicd`）、第 4 章「部署」（`serving-patterns-and-rollouts`、`fastapi-inference-service`）、第 5 章「监测与漂移」（`monitoring-drift-and-psi`）。
- 尽管 A.4.1 大纲中“实验搭建与系统架构（1.1–1.3）”和“版本管理（7.1）”分列首尾，游戏章序以“数据/模型版本”开头：把系统工程组件全景与数据血缘/模型注册表统一放在第 1 课，在随后第 2–5 章依次建立特征存储（消解训练–服务偏差）、可复现训练流水线、多模式上线与 FastAPI 接口检验，以及生产漂移 PSI 监控的完整闭环。
- `fastapi-inference-service` 在没有安装第三方 Web 框架的轻量沙盒中配合 Python 执行追踪（`trace`），模拟一次带范围检验与模型打分的推理请求处理过程。

## 核心主题（C2）

`../cs-math-skill-tree/data/curation/scope.json` 未为 A.4.1 列出强制 CS2023 核心主题（该技能在路径中标记为 `optional: true`），核心能力全盘对照 Made With ML MLOps 课程、Google Cloud MLOps 架构与 Hopsworks FTI 管线展开：版本与血缘（Ch.1）、特征服务（Ch.2）、训练管线与自动测试（Ch.3）、部署与接口服务（Ch.4）、漂移监控与 PSI（Ch.5）。

## 学习资源的章节（C3）

- Made With ML [MLOps Course](https://madewithml.com/courses/mlops/) 1.1–8.5 全 28 节：对应课见上表。
- Google Cloud《MLOps：持续交付和自动化流水线》与 Hopsworks Feature Store FTI 教程：`feature-store-and-skew`、`training-tracking-and-pipelines`、`monitoring-drift-and-psi`。
- Microsoft Learn / Azure ML 模型管理与注册表：`ml-systems-and-versioning`。
- [FastAPI 请求体文档](https://fastapi.tiangolo.com/tutorial/body/)：`fastapi-inference-service`。

## 综合练习（C4）

| 小题 | 内容 | 课 |
|---|---|---|
| (1) | 真实机器学习系统“模型代码只占一小部分”的其他工程组件，以及训练–服务偏差的成因与规避 | `ml-systems-and-versioning`、`feature-store-and-skew` |
| (2) | 数据集快照与模型版本的元数据记录要素，以及模型注册表的阶段审批与回滚追溯作用 | `ml-systems-and-versioning` |
| (3) | 批量预测、在线实时服务与流式预测的适用场景，以及影子部署与金丝雀发布的本质区别 | `serving-patterns-and-rollouts` |
| (4) | 数据漂移 vs 概念漂移辨析，以及 PSI 公式与实算（$e=[0.25]^4, a=[0.1,0.2,0.3,0.4] \implies 0.228 > 0.2$） | `monitoring-drift-and-psi` |
| (5) | 最小 FastAPI 推理服务骨架（启动一次加载、Pydantic 边界校验并返回版本号） | `fastapi-inference-service` |

## 后继技能（C5）

A.4.1 为人工智能推荐远征的终点选修站，无直接后继技能；学完即贯通从建模实验、特征一致、自动流水线到线上部署与漂移告警的生产全流程。
