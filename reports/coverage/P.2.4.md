# P.2.4 版本控制、调试与构建工具：覆盖表

**状态（2026-11-17）：已写完。** 依据 `../cs-math-skill-tree/data/outlines/P.2.4.json` 与 `../cs-math-skill-tree/output/outlines.json`，主来源为 MIT *The Missing Semester of Your CS Education (2026)* 与 CMU 15-131（Makefiles）；补充参考 *Software Engineering at Google* 第 18 章（Build Systems）、Pro Git 中文版与廖雪峰 Makefile 教程。游戏内部章序：`1. Git`、`2. 调试器`、`3. 构建`、`4. 包管理`、`5. 依赖与自动化工作流`。

`required` 为空（`P.1.1` 为推荐前置），因此基础编程术语（变量、分支、循环、函数、参数、列表、字典等）在 `assumes` 声明，其余 Git、调试、C 编译链接、Makefile、虚拟环境、锁文件与 Shell 概念均在本包从零讲清。

`node scripts/check-coverage.mjs P.2.4` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | A:1/12/26 What is the shell? | `shell-cli-pipes` |
| 1.2 | A:1/12/26 Navigating in the shell | `shell-cli-pipes` |
| 1.3 | A:1/12/26 What is available in the shell? | `shell-cli-pipes` |
| 1.4 | A:1/12/26 The shell language (bash) | `shell-cli-pipes` |
| 1.5 | A:1/12/26 Next steps | 不教：课程导览过渡页，无具体工具知识点 |
| 2.1 | A:1/13/26 The Command Line Interface | `shell-cli-pipes` |
| 2.2 | A:1/13/26 Arguments | `shell-cli-pipes` |
| 2.3 | A:1/13/26 Streams | `shell-cli-pipes` |
| 2.4 | A:1/13/26 Environment variables | `shell-cli-pipes` |
| 2.5 | A:1/13/26 Return codes | `shell-cli-pipes` |
| 2.6 | A:1/13/26 Signals | `shell-cli-pipes` |
| 2.7 | A:1/13/26 Remote Machines | `shell-cli-pipes` |
| 2.8 | A:1/13/26 Terminal Multiplexers | `shell-cli-pipes` |
| 2.9 | A:1/13/26 Customizing the Shell | `shell-cli-pipes` |
| 2.10 | A:1/13/26 AI in the Shell | 不教：属 AI 辅助终端技巧，超出本工具链核心标准 |
| 2.11 | A:1/13/26 Terminal Emulators | `shell-cli-pipes` |
| 3.1 | A:1/14/26 Text editing and Vim | 不教：Vim 编辑器专项操作，不属于通用版本控制与构建核心 |
| 3.2 | A:1/14/26 Modal editing | 不教：Vim 模态编辑专项操作，不属于本技能核心要求 |
| 3.3 | A:1/14/26 Vim's interface is a programming language | 不教：Vim 编辑语法专项，不属于本技能核心要求 |
| 3.4 | A:1/14/26 Learning Vim | 不教：Vim 练习导引，不属于本技能核心要求 |
| 3.5 | A:1/14/26 Code intelligence and language servers | 不教：LSP 编辑器功能拓展，超出入门工具链范围 |
| 3.6 | A:1/14/26 AI-powered development | 不教：AI 编码助手话题，超出本技能核心工具链 |
| 3.7 | A:1/14/26 Coding agents | 不教：编码智能体工作流，超出本技能核心工具链 |
| 3.8 | A:1/14/26 Extensions and other IDE functionality | `debug-mindset-print` |
| 4.1 | A:1/15/26 Debugging | `debug-mindset-print` |
| 4.2 | A:1/15/26 Printf Debugging and Logging | `debug-mindset-print` |
| 4.3 | A:1/15/26 Debuggers | `debug-mindset-print` |
| 4.4 | A:1/15/26 System Call Tracing | `debug-trace-mem` |
| 4.5 | A:1/15/26 Memory Debugging | `debug-trace-mem` |
| 4.6 | A:1/15/26 Profiling | `profile-benchmark` |
| 4.7 | A:1/15/26 Timing | `profile-benchmark` |
| 4.8 | A:1/15/26 Resource Monitoring | `profile-benchmark` |
| 4.9 | A:1/15/26 CPU Profilers | `profile-benchmark` |
| 4.10 | A:1/15/26 Memory Profilers | `profile-benchmark` |
| 4.11 | A:1/15/26 Benchmarking | `profile-benchmark` |
| 5.1 | A:1/16/26 Git's data model | `git-snapshots` |
| 5.2 | A:1/16/26 Snapshots | `git-snapshots` |
| 5.3 | A:1/16/26 Modeling history: relating snapshots | `git-snapshots` |
| 5.4 | A:1/16/26 Objects and content-addressing | `git-snapshots` |
| 5.5 | A:1/16/26 References | `git-branches` |
| 5.6 | A:1/16/26 Repositories | `git-snapshots` |
| 5.7 | A:1/16/26 Staging area | `git-snapshots` |
| 5.8 | A:1/16/26 Git command-line interface | `git-snapshots` |
| 5.9 | A:1/16/26 Basics | `git-snapshots` |
| 5.10 | A:1/16/26 Branching and merging | `git-branches`、`git-conflicts-rebase` |
| 5.11 | A:1/16/26 Remotes | `git-remotes-undo` |
| 5.12 | A:1/16/26 Undo | `git-remotes-undo` |
| 5.13 | A:1/16/26 Advanced Git | `git-conflicts-rebase` |
| 6.1 | A:1/20/26 Dependencies & Environments | `envs-packages`、`semver-lockfiles` |
| 6.2 | A:1/20/26 Artifacts & Packaging | `artifacts-repro` |
| 6.3 | A:1/20/26 Releases & Versioning | `artifacts-repro`、`semver-lockfiles` |
| 6.4 | A:1/20/26 Reproducibility | `artifacts-repro`、`semver-lockfiles` |
| 6.5 | A:1/20/26 VMs & Containers | `envs-packages` |
| 6.6 | A:1/20/26 Configuration | `envs-packages` |
| 6.7 | A:1/20/26 Services & Orchestration | `envs-packages` |
| 6.8 | A:1/20/26 Publishing | `envs-packages` |
| 7.1 | A:1/23/26 Formatting | `quality-ci-cd` |
| 7.2 | A:1/23/26 Linting | `quality-ci-cd` |
| 7.3 | A:1/23/26 Testing | `quality-ci-cd` |
| 7.4 | A:1/23/26 Code coverage | `quality-ci-cd` |
| 7.5 | A:1/23/26 Pre-commit hooks | `quality-ci-cd` |
| 7.6 | A:1/23/26 Continuous integration | `quality-ci-cd` |
| 7.7 | A:1/23/26 Continuous deployment | `quality-ci-cd` |
| 7.8 | A:1/23/26 Command runners | `quality-ci-cd` |
| 8.1 | B Getting Started with Makefiles | `make-compile-link`、`make-build-graph` |
| 8.2 | B Using Makefiles to Compile Code | `make-compile-link`、`make-build-graph` |

## CS2023 核心主题（C2）

| 主题 | KA / 要求 | 课 |
|---|---|---|
| Software configuration management and version control | SE-Tools · CS Core | `git-snapshots`、`git-branches`、`git-conflicts-rebase`、`git-remotes-undo` |
| Use of a general-purpose IDE, including its debugger | SDF-Practices · CS Core | `debug-mindset-print`、`debug-trace-mem`、`profile-benchmark` |
| Build systems | SE-Tools · KA Core | `make-compile-link`、`make-build-graph`、`artifacts-repro` |
| Dependency management | SE-Tools · KA Core | `envs-packages`、`semver-lockfiles` |
| Software process automation | SE-Tools · KA Core | `shell-cli-pipes`、`quality-ci-cd` |

## 学习资源的章节（C3）

| 来源 | 章节与概念 | 课 / 说明 |
|---|---|---|
| `en1` / `zh1` Missing Semester 2026 | Shell/命令行环境、Debugging/Profiling、Version Control & Git、Packaging & Shipping、Code Quality | 全部对应 `shell-cli-pipes`、`debug-*`、`profile-benchmark`、`git-*`、`envs-packages`、`artifacts-repro`、`quality-ci-cd` |
| `zh2` Pro Git 中文版 | 第 2/3/5/7 章 Git 基础、分支合并、撤销重写 | `git-snapshots`、`git-branches`、`git-conflicts-rebase`、`git-remotes-undo` |
| `en2` SE at Google ch18 / `zh3` 廖雪峰 Makefile | 依赖图（DAG）、时间戳增量构建、Makefile 规则与自动变量 | `make-compile-link`、`make-build-graph` |

## 综合练习（C4）

| 小题 | 要用到的 | 课 |
|---|---|---|
| (1) `git switch -c feature` 两次提交切回 main 合并、解冲突、merge vs rebase | 分支指针切换、三方合并、冲突标记 `<<<<<<<`/`=======`/`>>>>>>>`、rebase 线性历史 | `git-branches`、`git-conflicts-rebase` |
| (2) 未推送用 `--amend`/`reset --soft` vs 已推送共享分支用 `revert` | 本地改写提交哈希 vs 公共历史追加反向提交 | `git-remotes-undo` |
| (3) 用 pdb/gdb 定位差一错误、条件断点、printf 调试局限 | 断点暂停、查看栈帧变量、条件表达式、无需反复改源码重编译 | `debug-mindset-print` |
| (4) `main.c` + `util.c` → `app` 最小 Makefile、锁文件作用、`^1.2.3` 范围 | 目标:依赖+Tab 命令行、mtime 增量重编、锁文件精确版本与哈希校验、`>=1.2.3 && <2.0.0` | `make-build-graph`、`semver-lockfiles` |

## 后继技能（C5）

`unlocks` 为空。推荐后继包括 `P.5.3 DevOps、持续交付与 SRE`、`P.1.4 资源管理、并发与性能`、`P.4.6 软件演化与技术债` 与 `A.4.1 MLOps`。本包在 `quality-ci-cd` 讲透提交触发自动检查与产物对应提交，`semver-lockfiles` 讲透锁文件与精确复现安装，`profile-benchmark` 讲透计时剖析与基准测试，完全支撑四条下游路线无缝衔接。
