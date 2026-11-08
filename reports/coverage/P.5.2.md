# P.5.2 课程覆盖表

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
| 12.3 | Write platform-specific code | `platform-code`, `device` |
| 12.4 | Bind to native code | `platform-code`, `device` |
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

## CS2023 与原综合练习

- SPD-Mobile KA Core 的界面设计与状态见 `compose-counter`、`lists-theme`、自适应布局和导航各课；移动平台约束见 `lifecycle`、`device`、`platform-code` 和离线同步。 [Android Compose 基础](https://developer.android.com/courses/android-basics-compose/course) · [Flutter 文档](https://docs.flutter.dev/)
- 原题 1 和 5 在 `stacks` 比较原生、Flutter、React Native、Electron 和 Qt；原题 2 区分旋转、系统终止后的恢复和持久数据；原题 3 提供 Compose 模板中的计数器；原题 4 用本地事务和待发送队列处理断网、重复发送和冲突。 [Android 保存状态](https://developer.android.com/topic/libraries/architecture/viewmodel/viewmodel-savedstate) · [离线优先](https://developer.android.com/topic/architecture/data-layer/offline-first) · [Electron 安全](https://www.electronjs.org/docs/latest/tutorial/security)
- 验证脚本运行独立 Kotlin 与 Dart 片段和 SQLite 模型。Compose 界面片段依赖 Android Studio 的 Compose 项目，移动平台生命周期与插件能力按平台资料核对。 [Compose 状态](https://developer.android.com/develop/ui/compose/state) · [Flutter 平台通道](https://docs.flutter.dev/platform-integration/platform-channels) · [Flutter 发布自动化](https://docs.flutter.dev/deployment/cd)
