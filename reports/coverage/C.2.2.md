# C.2.2 系统编程与并发同步：覆盖表

**状态（2026-11-09）：已写完。** `data/content/C.2.2.yaml`（version 2）28 课，结业挑战 15 题。`node scripts/check-coverage.mjs C.2.2`：39 节里 37 节有课，2 节写明不教的理由。课里的程序输出、数值和报错由 `tests/content/C.2.2.verify.py` 核对：C 程序用 WSL 的 gcc 15 在 64 位 Linux 上编译运行（进程、信号、文件、线程、信号量、原子操作、内存序实验、管道、套接字服务器、ThreadSanitizer），交错、进度图、加速比、锁集等数值用 Python 重算。引用的说法对照了原文：OSTEP 第 28 章、Eraser 论文（TOCS 1997）、MIT 6.033 REC 5 页面、CMU 15-213 的 CS:APP 课件、Linux man-pages、Intel SDM 的内存序一节、Lamport 1979、Pöter & Träff（arXiv:1803.04432）、clang 的 ThreadSanitizer 文档（摘录在写作时的 `temp/research/`，由 pi 子代理抓取、主代理逐条核对）。旧的模板包在 `archive/template-2026-11-08/`。

规则见 `docs/content-authoring.md` 的“知识覆盖面标准”。依据：skill-tree 大纲 `../cs-math-skill-tree/data/outlines/C.2.2.json`：A 是《Computer Systems: A Programmer's Perspective》第 3 版（CS:APP，第 8 章异常控制流、第 10 章系统级 I/O、第 11 章网络编程、第 12 章并发编程），B 是《Operating Systems: Three Easy Pieces》第 28 章的 28.7–28.11（原子指令），C 是 MIT 6.033（2022 春）的 Eraser 讨论课。“节”是技能内部编号，“原文”是书自己的节号和标题。

必须前置是 C.1.1 和 P.2.2（以及它们的前置 P.1.1）。这些包讲过的术语（系统调用、内核、文件描述符、中断、指针、结构体、缓冲区、链接……）可以直接用。操作系统 C.2.1 只是推荐前置，不能假设学过：进程、线程、地址空间、上下文切换、竞态条件、临界区、互斥锁、信号量、死锁、自旋锁、条件变量这些词，本包要重新从头讲。代码用 C，在 64 位 Linux 上用 gcc 编译运行核对（`tests/content/C.2.2.verify.py`）。

`node scripts/check-coverage.mjs C.2.2` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | A 8.1 Exceptions | `exceptions` |
| 1.2 | A 8.2 Processes | `processes` |
| 1.3 | A 8.3 System Call Error Handling | `fork` |
| 1.4 | A 8.4 Process Control | `fork`、`wait-exec` |
| 1.5 | A 8.5 Signals | `signals`、`signal-handlers` |
| 1.6 | A 8.6 Nonlocal Jumps | `signal-handlers` |
| 1.7 | A 8.7 Tools for Manipulating Processes | `wait-exec` |
| 2.1 | A 10.1 Unix I/O | `unix-io` |
| 2.2 | A 10.2 Files | `unix-io` |
| 2.3 | A 10.3 Opening and Closing Files | `unix-io` |
| 2.4 | A 10.4 Reading and Writing Files | `unix-io` |
| 2.5 | A 10.5 Robust Reading and Writing with the Rio Package | `rio-metadata` |
| 2.6 | A 10.6 Reading File Metadata | `rio-metadata` |
| 2.7 | A 10.7 Reading Directory Contents | `rio-metadata` |
| 2.8 | A 10.8 Sharing Files | `sharing-redirect` |
| 2.9 | A 10.9 I/O Redirection | `sharing-redirect` |
| 2.10 | A 10.10 Standard I/O | `sharing-redirect` |
| 2.11 | A 10.11 Putting It Together: Which I/O Functions Should I Use? | `sharing-redirect` |
| 3.1 | A 11.1 The Client-Server Programming Model | `sockets` |
| 3.2 | A 11.2 Networks | `sockets` |
| 3.3 | A 11.3 The Global IP Internet | `sockets` |
| 3.4 | A 11.4 The Sockets Interface | `sockets` |
| 3.5 | A 11.5 Web Servers | 不教：HTTP 请求和响应的格式、静态和动态内容属于 C.3.2 的“名称系统与应用协议”，写网站属于 P.5.1；本包只用套接字写回显服务器 |
| 3.6 | A 11.6 Putting It Together: The Tiny Web Server | 不教：它把 11.5 的 HTTP 和本包的 rio、套接字拼成一个 Web 服务器，HTTP 部分属于 C.3.2 和 P.5.1；拼装要用到的 rio、套接字、fork 和 dup2 本包都教 |
| 4.1 | A 12.1 Concurrent Programming with Processes | `pipes`、`concurrent-servers` |
| 4.2 | A 12.2 Concurrent Programming with I/O Multiplexing | `select-server` |
| 4.3 | A 12.3 Concurrent Programming with Threads | `threads` |
| 4.4 | A 12.4 Shared Variables in Threaded Programs | `shared-vars` |
| 4.5 | A 12.5 Synchronizing Threads with Semaphores | `progress-graph`、`semaphores`、`prodcons` |
| 4.6 | A 12.6 Using Threads for Parallelism | `parallel` |
| 4.7.1 | A 12.7.1 Thread Safety | `thread-safety` |
| 4.7.2 | A 12.7.2 Reentrancy | `thread-safety` |
| 4.7.3 | A 12.7.4 Races | `races` |
| 4.7.4 | A 12.7.5 Deadlocks | `deadlock` |
| 5.1 | B 28.7 Building Working Spin Locks with Test-And-Set | `test-and-set` |
| 5.2 | B 28.9 Compare-And-Swap | `cas-llsc` |
| 5.3 | B 28.10 Load-Linked and Store-Conditional | `cas-llsc` |
| 5.4 | B 28.11 Fetch-And-Add | `fetch-add` |
| 6 | C REC 5 Eraser | `eraser` |

## CS2023 核心主题（C2）

| 主题 | 课 |
|---|---|
| OS-Principles：Concept of system calls | `exceptions`、`fork` |
| OS-Concurrency：semaphores, mutex locks, condition variables | `semaphores`、`prodcons` |
| PDC-Coordination：Atomic instructions | `test-and-set`、`cas-llsc`、`fetch-add` |
| FPL-Parallel：memory-consistency models | `reordering`、`acquire-release` |
| OS-Process：Interprocess communication | `pipes`、`sockets`、`concurrent-servers`、`select-server` |

## 综合练习（C4）

| 小题 | 要用到的 | 课 |
|---|---|---|
| (1) 管道 + fork，父读子写；为什么关掉不用的一端，read 何时返回 0 | pipe、fork、wait、read 返回 0 的含义、SIGPIPE | `fork`、`wait-exec`、`unix-io`、`pipes` |
| (2) 4 个线程分段求和，局部和比加锁累加好在哪 | pthread_create / join、互斥锁的开销、伪共享 | `threads`、`semaphores`、`parallel` |
| (3) 死锁的四个必要条件，A→B 和 B→A，两种预防 | 死锁、加锁顺序、trylock | `deadlock` |
| (4) 条件变量的 wait 为什么放在 while 里；有界队列的 put / get | 互斥锁、条件变量、虚假唤醒、有界缓冲区 | `prodcons` |
| (5) 数据竞争是什么，C11 atomic_fetch_add 解决了什么 | 数据竞争、原子操作、内存序 | `reordering`、`fetch-add` |

## 后继技能（C5）

必须后继是 C.4.1 分布式系统、C.4.2 云计算，现在都还没有内容包。C.4.2 的综合练习用到的是服务模型、容量和成本估算，不直接用本包的写法；C.4.1 会用到进程、线程、套接字通信和锁，这些在 `processes`、`threads`、`sockets`、`semaphores` 教到。
