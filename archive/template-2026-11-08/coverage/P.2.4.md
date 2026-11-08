# P.2.4 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | What is the shell? | `shell` |
| 1.2 | Navigating in the shell | `shell` |
| 1.3 | What is available in the shell? | `shell` |
| 1.4 | The shell language (bash) | `shell`, `automation` |
| 1.5 | Next steps | 不教：课程导览，无独立知识点 |
| 2.1 | The Command Line Interface | `shell` |
| 2.2 | Arguments | `shell` |
| 2.3 | Streams | `shell` |
| 2.4 | Environment variables | `automation` |
| 2.5 | Return codes | `automation` |
| 2.6 | Signals | `automation` |
| 2.7 | Remote Machines | `automation` |
| 2.8 | Terminal Multiplexers | `automation` |
| 2.9 | Customizing the Shell | `automation` |
| 2.10 | AI in the Shell | 不教：生成命令的工具超出入门范围，先学会阅读和核对命令 |
| 2.11 | Terminal Emulators | `shell` |
| 3.1 | Text editing and Vim | 不教：可用任意文本编辑器，编辑器操作超出入门范围 |
| 3.2 | Modal editing | 不教：Vim 的操作方式超出工具链入门范围 |
| 3.3 | Vim's interface is a programming language | 不教：Vim 的组合指令超出工具链入门范围 |
| 3.4 | Learning Vim | 不教：Vim 学习资源导览 |
| 3.5 | Code intelligence and language servers | 不教：语言服务器实现超出工具链入门范围 |
| 3.6 | AI-powered development | 不教：生成式开发辅助超出工具链入门范围 |
| 3.7 | Coding agents | 不教：编码智能体工作方式超出工具链入门范围 |
| 3.8 | Extensions and other IDE functionality | `debugger` |
| 4.1 | Debugging | `debugger` |
| 4.2 | Printf Debugging and Logging | `debugger`, `diagnose` |
| 4.3 | Debuggers | `debugger`, `breakpoint` |
| 4.4 | System Call Tracing | `diagnose` |
| 4.5 | Memory Debugging | `diagnose` |
| 4.6 | Profiling | `profile` |
| 4.7 | Timing | `profile` |
| 4.8 | Resource Monitoring | `profile` |
| 4.9 | CPU Profilers | `profile` |
| 4.10 | Memory Profilers | `profile` |
| 4.11 | Benchmarking | `profile` |
| 5.1 | Git's data model | `snapshots` |
| 5.2 | Snapshots | `snapshots` |
| 5.3 | Modeling history: relating snapshots | `snapshots`, `branches` |
| 5.4 | Objects and content-addressing | `snapshots` |
| 5.5 | References | `branches` |
| 5.6 | Repositories | `snapshots` |
| 5.7 | Staging area | `snapshots` |
| 5.8 | Git command-line interface | `snapshots` |
| 5.9 | Basics | `snapshots` |
| 5.10 | Branching and merging | `branches`, `conflicts` |
| 5.11 | Remotes | `remotes` |
| 5.12 | Undo | `undo` |
| 5.13 | Advanced Git | `undo` |
| 6.1 | Dependencies & Environments | `packages` |
| 6.2 | Artifacts & Packaging | `packages` |
| 6.3 | Releases & Versioning | `locks` |
| 6.4 | Reproducibility | `locks`, `build-graph` |
| 6.5 | VMs & Containers | `packages` |
| 6.6 | Configuration | `automation` |
| 6.7 | Services & Orchestration | `checks` |
| 6.8 | Publishing | `locks` |
| 7.1 | Formatting | `checks` |
| 7.2 | Linting | `checks` |
| 7.3 | Testing | `checks` |
| 7.4 | Code coverage | `checks` |
| 7.5 | Pre-commit hooks | `checks` |
| 7.6 | Continuous integration | `checks` |
| 7.7 | Continuous deployment | `checks` |
| 7.8 | Command runners | `automation`, `checks` |
| 8.1 | Getting Started with Makefiles | `make-rules` |
| 8.2 | Using Makefiles to Compile Code | `make-rules`, `build-graph` |

## CS2023 与综合练习

- SE-Tools 软件配置管理与版本控制由 `snapshots` 至 `undo` 教授。综合练习 1 的两次提交、快进与分叉合并、冲突和 rebase 见 `branches`、`conflicts`、`remotes`。综合练习 2 的 amend、soft reset 与 revert 见 `undo`。
- SDF-Practices 通用 IDE 与调试器由 `debugger`、`breakpoint` 教授。综合练习 3 的差一案例包含重现、断点条件、单步、检查实际边界及回归检查。
- SE-Tools 构建、依赖管理与过程自动化由 `make-rules` 至 `checks` 教授。综合练习 4 的两个 C 文件、共享头、增量重建和锁定范围由 `make-rules`、`build-graph`、`locks` 覆盖。

## 双语补充与后续远征

- [Pro Git](https://git-scm.com/book/zh/v2) 第 2、3、5 章的基本操作、分支和分布式协作见 `snapshots` 至 `undo`。交互式整理只示范在自己的历史上使用，复杂分布式维护留给实际协作时深入。
- [Makefile 教程](https://liaoxuefeng.com/books/makefile/introduction/index.html) 第 3–9 节的基础规则、隐式和模式规则、变量、自动生成依赖、伪目标见 `make-rules` 与 `build-graph`。[Google 的构建系统章节](https://abseil.io/resources/swe-book/html/ch18.html) 的任务与产物、依赖图、增量、并行和可重现输入见 `build-graph`。分布式构建和远程缓存的运维留给有大规模项目经验的读者。
- [MIT Missing Semester](https://missing.csail.mit.edu/) 的命令行、性能、打包和质量检查逐节对应上表。断点语法与 npm 安装行为分别按 [pdb 文档](https://docs.python.org/3/library/pdb.html) 和 [npm ci 文档](https://docs.npmjs.com/cli/v11/commands/npm-ci/) 核对。
- 技能树没有必须后继。后续远征会用到的干净安装、共享分支和流水线故障定位已经在 `remotes`、`locks`、`checks` 给出例子。容器机制、测试设计和上线策略分别由 C.2.3、P.4.5 和 P.5.3 深入。
