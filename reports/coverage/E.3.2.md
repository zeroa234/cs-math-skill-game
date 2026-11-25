# E.3.2 电机与电力拖动：覆盖表

**状态（2026-11-23）：已写完，15 课，等用户验收。** 依据 `../cs-math-skill-tree/data/outlines/E.3.2.json`（主来源 Fitzgerald & Kingsley《Electric Machinery》第 7 版第 1–10 章；MIT 6.685 Electric Machines 2013 讲座表的相关讲次）、`data/curation/learning-paths/E.3.2.json`（浙江大学《电机与拖动》、中国石油大学（华东）《运动控制系统》、四川轻化工大学《机电传动控制》的步进电机一章）和原技能树综合练习 7 小题。数值核对脚本 `tests/content/E.3.2.verify.py`。

前置：必须前置 N.1.2（磁场、磁通、法拉第电磁感应定律、安培环路定理、安培力、涡流、反电动势、电感可直接用）和 H.1.1（电压、电流、欧姆定律、方均根可直接用）。H.1.1 没有讲相量、功率因数和三相电路，本包在第一次用到时现讲：功率因数在 `transformer-ideal`，线电压和相电压、电角度在 `rotating-field`，相量和无功功率在 `synchronous-machine`。

## 课的安排

| 课 | 章 | 内容 |
|---|---|---|
| `magnetic-circuits` | 磁路与变压器 | 磁路欧姆定律、磁阻、铁芯和气隙、磁化曲线和饱和、磁滞和涡流损耗、电感 |
| `transformer-ideal` | 磁路与变压器 | 理想变压器的电压比、电流比、阻抗变换；感应电动势 $E = 4.44fN\Phi_m$；额定值和额定电流（综合练习 1） |
| `transformer-equivalent` | 磁路与变压器 | 等效电路、空载和短路试验、效率和电压调整率、标幺值、三相变压器 |
| `energy-conversion` | 磁路与变压器 | 机电能量转换：磁场储能、电磁力 $f = \frac12 i^2\frac{dL}{dx}$、磁阻力矩 |
| `rotating-field` | 同步电机 | 旋转电机的基本结构、三相绕组产生旋转磁场、同步转速 $n_s = 60f/p$、绕组感应电动势 |
| `synchronous-machine` | 同步电机 | 同步电机的结构和等效电路、功角特性、励磁和功率因数（V 形曲线）、同步调相机（综合练习 4） |
| `synchronous-dynamics` | 同步电机 | 双反应理论和派克变换的思想、同步电机的转子运动方程和功角振荡 |
| `dc-machines` | 直流电机 | 换向器、反电动势和电磁转矩、电压方程、励磁方式、起动电流（综合练习 2） |
| `reluctance-stepper` | 永磁与步进电机 | 磁阻电机原理、步进电机的步距角、整步和半步（综合练习 5） |
| `pm-brushless` | 永磁与步进电机 | 永磁材料的剩磁和矫顽力、永磁同步电机和无刷直流电机、霍尔传感器换相 |
| `induction-basics` | 感应电机 | 涡流和感应原理、转差率、转子频率、等效电路（综合练习 3 前半） |
| `induction-torque` | 感应电机 | 功率流、转矩—转差率曲线、起动转矩和最大转矩、鼠笼转子；单相电动机为什么需要辅助绕组（综合练习 3 后半） |
| `drive-steady-state` | 电力拖动的稳态特性 | 运动方程、负载转矩特性、稳定运行条件；直流电动机的机械特性、起动、制动和调速（综合练习 6） |
| `vf-control` | 变频调速与矢量控制初步 | 交-直-交变频器、恒压频比控制和低频转矩提升、转差频率控制（综合练习 7 前半） |
| `vector-control` | 变频调速与矢量控制初步 | 坐标变换、磁场定向、励磁电流和转矩电流分开控制（综合练习 7 后半） |

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1 | Magnetic Circuits and Magnetic Materials | `magnetic-circuits` |
| 2 | Transformers | `transformer-ideal`、`transformer-equivalent` |
| 3 | Electromechanical-Energy-Conversion Principles | `energy-conversion` |
| 4 | Introduction to Rotating Machines | `rotating-field` |
| 5 | Synchronous Machines | `synchronous-machine` |
| 6 | Polyphase Induction Machines | `induction-basics`、`induction-torque` |
| 7 | DC Machines | `dc-machines` |
| 8 | Variable-Reluctance Machines and Stepping Motors | `reluctance-stepper` |
| 9 | Single-and Two-Phase Motors | `induction-torque` |
| 10 | Speed and Torque Control | `drive-steady-state`、`vf-control`、`vector-control` |
| 11 | Synchronous Machines (Round Rotor), Magnetic Circuits | `synchronous-machine`、`magnetic-circuits` |
| 12 | Transformers, Materials, Machine Size, Power Density, Surface Current View | `transformer-equivalent`、`magnetic-circuits` |
| 13 | Classical Synchronous Machine Theory: Sizing and Rating | `synchronous-machine` |
| 14 | Two Reaction Theory: Park’s Transform | `synchronous-dynamics` |
| 15 | Park’s Transform and Implications | `synchronous-dynamics`、`vector-control` |
| 16 | Induced Currents: Eddy Currents, Linear Induction Machine Model | `induction-basics` |
| 17 | Induction Machines: Transformer Model | `induction-basics` |
| 18 | Torque-Speed, Squirrel Cage Machines | `induction-torque` |
| 19 | DC Machines: Faraday’s Law | `dc-machines` |
| 20 | Variable Reluctance Machine Principles | `reluctance-stepper` |
| 21 | Synchronous Machine Dynamics | `synchronous-dynamics` |
| 22 | Induction Motor Drives and Control | `vf-control`、`vector-control` |
| 23 | Permanent Magnets in Machine Systems | `pm-brushless` |
| 24 | Brushless DC Motors | `pm-brushless` |

## CS2023 核心主题（C2）

`scope.json` 对 E.3.2 没有 CS2023 主题；7 个章由上表的课负责。

## 原技能树综合练习（C4）

| 小题 | 内容 | 由哪一课教到 |
|---|---|---|
| (1) | 磁路欧姆定律、变压器匝比和额定电流、空载和短路试验 | `magnetic-circuits`、`transformer-ideal`、`transformer-equivalent` |
| (2) | 直流电动机的反电动势、$k\Phi$、电磁转矩、起动电流 | `dc-machines` |
| (3) | 同步转速、转差率、转子频率、转矩—转差率曲线 | `induction-basics`、`induction-torque` |
| (4) | 同步电机的转速和励磁对功率因数的影响 | `synchronous-machine` |
| (5) | 永磁同步电机和步进电机产生转矩的原理、步距角 | `reluctance-stepper`、`pm-brushless` |
| (6) | 电力拖动稳定运行条件、负载转矩特性 | `drive-steady-state` |
| (7) | 恒压频比、低频转矩提升、矢量控制思想 | `vf-control`、`vector-control` |

## 后继技能用到的写法（C5）

必须后继 E.3.3 电力系统分析还没有内容包；按它的大纲，同步发电机的等效电路和功角特性、转子运动方程（摇摆方程）、变压器等效电路和标幺值由 `synchronous-machine`、`synchronous-dynamics`、`transformer-equivalent` 负责。
