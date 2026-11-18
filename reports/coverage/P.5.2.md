# P.5.2 移动应用开发：覆盖表

**状态（2026-11-18）：已写完（v2 重写，按零基础与知识覆盖面标准重写）。** 依据 `../cs-math-skill-tree/data/outlines/P.5.2.json`、`output/outlines.json`、`../cs-math-skill-tree/data/curation/learning-paths/P.5.2.json`，主来源为 Google《Android Basics with Compose》与 Flutter 官方文档（UI 自适应、网络与持久存储、平台通道与多端发布），辅以 Android 官方运行时权限/传感器/离线优先架构与 Play 发布指南以及 Electron 安全加固指南，重点针对旧包审计指出的 `device` 空泛问题补全实际平台权限 API，并对齐 `P.5.2` 综合练习 5 问，本地核对脚本 `tests/content/P.5.2.verify.py`（Python 3 + `sqlite3` 实测）。

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Introduction to Kotlin | `toolchain` |
| 1.2 | Setup Android Studio | `toolchain` |
| 1.3 | Build a basic layout | `compose-counter` |
| 2.1 | Kotlin fundamentals | `kotlin-state` |
| 2.2 | Add a button to an app | `compose-counter` |
| 2.3 | Interacting with UI and state | `compose-counter` |
| 3.1 | More Kotlin fundamentals | `kotlin-state` |
| 3.2 | Build a scrollable list | `lists-theme` |
| 3.3 | Build beautiful apps | `lists-theme` |
| 4.1 | Architecture Components | `lifecycle` |
| 4.2 | Navigation in Jetpack Compose | `navigation` |
| 4.3 | Adapt for different screen sizes | `adaptive-android` |
| 5.1 | Get data from the internet | `network` |
| 5.2 | Load and display images from the internet | `network` |
| 6.1 | Introduction to SQL | `local-data` |
| 6.2 | Use Room for data persistence | `local-data` |
| 6.3 | Store and access data using keys with DataStore | `local-data` |
| 7.1 | Schedule tasks with WorkManager | `background-sync` |
| 8.1 | Android Views and Compose in Views | `adaptive-android` |
| 9.1 | Overview | `adaptive-flutter` |
| 9.2 | General approach | `adaptive-flutter` |
| 9.3 | SafeArea & MediaQuery | `adaptive-flutter` |
| 9.4 | Large screens & foldables | `adaptive-flutter` |
| 9.5 | User input & accessibility | `adaptive-flutter` |
| 9.6 | Capabilities & policies | `adaptive-flutter` |
| 9.7 | Automatic platform adaptations | `adaptive-flutter` |
| 10.1 | Overview | `network` |
| 10.2 | Fetch data from the internet | `network` |
| 10.3 | Make authenticated requests | `network` |
| 10.4 | Send data to the internet | `api-writes` |
| 10.5 | Update data over the internet | `api-writes` |
| 10.6 | Delete data on the internet | `api-writes` |
| 11.1 | Choose a database | `flutter-storage` |
| 11.2 | Store key-value data on disk | `flutter-storage` |
| 11.3 | Read and write files | `flutter-storage` |
| 11.4 | Persist data with SQLite | `flutter-storage` |
| 12.1 | Supported platforms | `stacks` |
| 12.2 | Build desktop apps with Flutter | `stacks` |
| 12.3 | Write platform-specific code | `platform-code`、`device` |
| 12.4 | Bind to native code | `platform-code`、`device` |
| 13.1 | Obfuscate Dart code | `release` |
| 13.2 | Create app flavors for Android | `release` |
| 13.3 | Create app flavors for iOS and macOS | `release` |
| 13.4 | Create app flavors for Linux | `multi-release` |
| 13.5 | Create app flavors for Windows | `multi-release` |
| 13.6 | Build and release an Android app | `release` |
| 13.7 | Build and release an iOS app | `release` |
| 13.8 | Build and release a macOS app | `multi-release` |
| 13.9 | Build and release a Linux app | `multi-release` |
| 13.10 | Build and release a Windows app | `multi-release` |
| 13.11 | Build and release a web app | `multi-release` |
| 13.12 | Set up continuous deployment | `multi-release` |

## CS2023 核心主题（C2）

`../cs-math-skill-tree/data/curation/scope.json` 为 `P.5.2` 匹配的 2 项 CS2023 核心主题全部落课（其余“平台生命周期”与“离线同步与发布”围绕 Android/Flutter 课程及官方指南一并完整覆盖）：

| 知识点 | KA / 要求 | 课 |
|---|---|---|
| 界面状态 | SPD-Mobile / KA Core：User interface design | `kotlin-state`、`compose-counter`、`lists-theme`、`adaptive-android`、`adaptive-flutter` |
| 设备能力 | SPD-Mobile / KA Core：Mobile platform constraints | `device`、`stacks`、`platform-code`、`network`、`api-writes` |

## 综合练习与前置/后继映射（C3 / C4 / C5）

- **综合练习 5 问映射（C4）**：
  - 第 (1) 问对比原生（Swift/Kotlin）、跨平台（Flutter/React Native）与桌面（Electron/Qt）优缺点 → `stacks`、`platform-code`。
  - 第 (2) 问 Android Activity 生命周期六步回调顺序、屏幕旋转销毁重建及 `ViewModel` / `onSaveInstanceState` / `SavedStateHandle` / 数据库状态保存分层 → `lifecycle`。
  - 第 (3) 问 Compose / Flutter 计数器与声明式 UI“状态驱动界面”解释 → `compose-counter`（完整 Kotlin Compose 代码与重组数据流）。
  - 第 (4) 问移动端约束（断网、电量流量、小内存、权限、后台杀进程）与“离线可用待办”同步方案 → `local-data`、`background-sync`（单可信本地源、待发送队列表 `Pending` 事务、版本冲突与 LWW/字段合并/CRDT、`WorkManager` 联网充电约束调度）。
  - 第 (5) 问 Electron 体积/内存偏大原因与安全配置加固 → `stacks`（Chromium + Node.js 双打包、多渲染进程及关闭 `nodeIntegration`、启用 `contextIsolation` 与 `sandbox`、`preload` + `contextBridge`、CSP 与 IPC 参数校验）。
- **前后继状态（C3 / C5）**：
  - 必须前置仅为 `P.1.1 程序设计基础`（推荐前置 `P.1.2`、`P.5.1`、`V.2.1`；本包对 Kotlin/Dart 基础语法、Compose 与 Electron 基础写法、HTTP/JSON/API 认证概念与 SQLite 关系表操作均从零开始随用随释，不假设已完成推荐前置）。
  - `P.5.2` 无下游必须前置依赖；它被 `S.2.3 移动应用与设备安全`（以及 `V.2.4`）列为推荐前置，本包铺垫的清单配置、运行时权限流、本地存储分工、硬编码密钥防线与签名混淆发布为 `S.2.3` 提供了部分直接前置铺垫（`S.2.3` 所需的导出 `Intent` 权限边界与 TLS 证书固定校验会在 `S.2.3` 自身课程内从零独立讲授）。
