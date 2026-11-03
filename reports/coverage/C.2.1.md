# C.2.1 操作系统：覆盖表

**状态（2026-11-03）：已写完。** `data/content/C.2.1.yaml`（version 2）29 课、189 道练习、14 道结业挑战。`node scripts/check-coverage.mjs C.2.1`：68 节全部有课。课里的数值、C 程序的输出、报错原文由 `tests/content/C.2.1.verify.py` 核对（C 用 WSL 的 gcc 编译运行，数值用 Python 独立重算）。

规则见 `docs/content-authoring.md` 的“知识覆盖面标准”。依据：skill-tree 大纲 `../cs-math-skill-tree/data/outlines/C.2.1.json`：A 是《Operating Systems: Three Easy Pieces》（OSTEP，v1.10），B 是 CS:APP 第 12.4 节“多线程程序中的共享变量”。“节”是技能内部编号，“原文”是书自己的节号和标题。

必须前置是 P.2.2、F.1.1、C.1.1，这些包定义过的术语（指针、结构体、链表、队列、寄存器、中断、cache、二进制……）可以直接用。代码用 C。

`node scripts/check-coverage.mjs C.2.1` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | A 4.1 The Abstraction: A Process | `process` |
| 1.2 | A 4.2 Process API | `process` |
| 1.3 | A 4.3 Process Creation: A Little More Detail | `process` |
| 1.4 | A 4.4 Process States | `process` |
| 1.5 | A 4.5 Data Structures | `process` |
| 2.1 | A 5.1 The fork() System Call | `fork-wait-exec` |
| 2.2 | A 5.2 The wait() System Call | `fork-wait-exec` |
| 2.3 | A 5.3 Finally, The exec() System Call | `fork-wait-exec` |
| 2.4 | A 5.5 Process Control And Users | `fork-wait-exec` |
| 3.1 | A 6.1 Basic Technique: Limited Direct Execution | `lde` |
| 3.2 | A 6.2 Problem #1: Restricted Operations | `lde` |
| 3.3 | A 6.3 Problem #2: Switching Between Processes | `lde` |
| 3.4 | A 6.4 Worried About Concurrency? | `lde` |
| 4.1 | A 7.1 Workload Assumptions | `sched-metrics` |
| 4.2 | A 7.2 Scheduling Metrics | `sched-metrics` |
| 4.3 | A 7.4 Shortest Job First (SJF) | `sjf-stcf` |
| 4.4 | A 7.5 Shortest Time-to-Completion First (STCF) | `sjf-stcf` |
| 4.5 | A 7.7 Round Robin | `rr-io` |
| 4.6 | A 7.8 Incorporating I/O | `rr-io` |
| 5.1 | A 13.2 Multiprogramming and Time Sharing | `address-space` |
| 5.2 | A 13.3 The Address Space | `address-space` |
| 5.3 | A 13.4 Goals | `address-space` |
| 6.1 | A 15.1 Assumptions | `base-bounds` |
| 6.2 | A 15.3 Dynamic (Hardware-based) Relocation | `base-bounds` |
| 6.3 | A 15.4 Hardware Support: A Summary | `base-bounds` |
| 6.4 | A 15.5 Operating System Issues | `base-bounds` |
| 7.1 | A 18.1 A Simple Example And Overview | `paging` |
| 7.2 | A 18.2 Where Are Page Tables Stored? | `paging` |
| 7.3 | A 18.3 What’s Actually In The Page Table? | `paging` |
| 7.4 | A 18.4 Paging: Also Too Slow | `paging` |
| 8.1 | A 19.1 TLB Basic Algorithm | `tlb` |
| 8.2 | A 19.3 Who Handles The TLB Miss? | `tlb` |
| 8.3 | A 19.5 TLB Issue: Context Switches | `tlb` |
| 8.4 | A 19.6 Issue: Replacement Policy | `tlb` |
| 9.1 | A 26.1 Why Use Threads? | `threads-intro` |
| 9.2 | A 26.3 Why It Gets Worse: Shared Data | `race` |
| 9.3 | A 26.4 The Heart Of The Problem: Uncontrolled Scheduling | `race` |
| 9.4 | A 26.5 The Wish For Atomicity | `race` |
| 10.1 | A 28.1 Locks: The Basic Idea | `locks` |
| 10.2 | A 28.3 Building A Lock | `locks` |
| 10.3 | A 28.7 Building Working Spin Locks with Test-And-Set | `locks` |
| 10.4 | A 28.9 Compare-And-Swap | `cas-queues` |
| 10.5 | A 28.12 Too Much Spinning: What Now? | `cas-queues` |
| 10.6 | A 28.14 Using Queues: Sleeping Instead Of Spinning | `cas-queues` |
| 11.1 | A 32.1 What Types Of Bugs Exist? | `concurrency-bugs` |
| 11.2 | A 32.2 Non-Deadlock Bugs | `concurrency-bugs` |
| 11.3 | A 32.3 Deadlock Bugs | `concurrency-bugs` |
| 12.1 | A 36.1 System Architecture | `io-devices` |
| 12.2 | A 36.2 A Canonical Device | `io-devices` |
| 12.3 | A 36.3 The Canonical Protocol | `io-devices` |
| 12.4 | A 36.4 Lowering CPU Overhead With Interrupts | `io-devices`, `rr-io` |
| 12.5 | A 36.5 More Efficient Data Movement With DMA | `dma-drivers` |
| 12.6 | A 36.7 Fitting Into The OS: The Device Driver | `dma-drivers` |
| 13.1 | A 39.1 Files And Directories | `files-api` |
| 13.2 | A 39.2 The File System Interface | `files-api` |
| 13.3 | A 39.4 Reading And Writing Files | `files-api` |
| 13.4 | A 39.6 Shared File Table Entries: fork() And dup() | `files-api`, `file-sharing` |
| 13.5 | A 39.14 Hard Links | `links-permissions` |
| 13.6 | A 39.15 Symbolic Links | `links-permissions` |
| 13.7 | A 39.16 Permission Bits And Access Control Lists | `links-permissions` |
| 14.1 | A 40.2 Overall Organization | `fs-layout` |
| 14.2 | A 40.3 File Organization: The Inode | `fs-layout` |
| 14.3 | A 40.4 Directory Organization | `fs-access` |
| 14.4 | A 40.6 Access Paths: Reading and Writing | `fs-access` |
| 14.5 | A 40.7 Caching and Buffering | `fs-access` |
| 15.1 | B 12.4.1 Threads Memory Model | `memory-model` |
| 15.2 | B 12.4.2 Mapping Variables to Memory | `memory-model` |
| 15.3 | B 12.4.3 Shared Variables | `memory-model` |

大纲没有收、但原技能树的综合练习、学习资源或前置站要求的，另有这些课（或课里的部分）：
- `sched-metrics` 里的 FIFO（A 7.3）：练习第 2 题要算 FCFS；
- `mlfq`（A 第 8 章）：学习资源 `chapters[]` 的中文和英文主资源都写着“第 7–10 章 CPU 调度（MLFQ……）”，按 C3 补上入门的五条规则；彩票调度（第 9 章）和多处理器调度（第 10 章）不教，大纲判为调度进阶；
- `multilevel`（A 第 20 章）：练习第 3 题问“为什么需要多级页表”；
- `swapping`（A 第 21 章）、`replacement`（A 第 22 章）：练习第 4 题要算 FIFO 和 LRU 的缺页次数。原计划一课，内容多（换页机制、AMAT、水位，置换策略、Belady 异常、时钟算法、抖动），按 R4 拆成两课；
- `semaphores`（A 第 31 章）：练习第 5 题要写有界缓冲区。条件变量（第 30 章）只在 `concurrency-bugs` 里作为修“违反顺序”的工具讲一张卡，细讲属于 C.2.2 系统编程与并发同步；
- `file-sharing`（A 39.6 的 dup 和 dup2）、`dirs-metadata`（A 39.9–39.13：stat、unlink、mkdir、readdir、rmdir）：P.2.2 的覆盖表把 CS:APP 10.6–10.9（文件元数据、读目录、共享文件、dup2）写明“在 C.2.1 讲”，这两课接住。

隔离（知识点“同步与隔离”的后一半）由 `lde`（用户态和内核态、受限的操作）、`address-space` 和 `base-bounds`（每个进程只能访问自己的地址空间）讲，`links-permissions` 补上文件的权限。

教到什么深度（入门层）：
- 进程 API 讲 fork、wait、exec、kill 和信号的作用、“只有自己和超级用户能控制一个进程”；不讲 waitpid 的选项。
- 受限直接执行讲到陷入、陷入表、从陷入返回、内核栈、时钟中断和上下文切换；不讲 xv6 的汇编代码。
- 锁讲 test-and-set、compare-and-swap、yield、队列加 park / unpark（Linux 的 futex 提一句）；不讲 LL/SC、fetch-and-add 的票锁。
- 文件系统实现用 OSTEP 的 vsfs 讲布局、inode、多级索引、目录项、读写一个文件要访问哪些块、页缓存和写缓冲；日志和崩溃一致性属于 C.2.4 存储系统与文件系统。

## 和原文的核对

2026-11-03 读了 OSTEP 第 4–8、18、19、22、31、32、36、39、40 章的原文 PDF，核对课里引用的说法：进程的三种状态、fork 的返回值、陷入表和从陷入返回、时间片是时钟中断周期的整数倍、MLFQ 最终的五条规则、TLB 的数组例子（命中、命中、缺失……命中率 70%）、硬件和软件处理 TLB 缺失、ASID、页面置换的例子（访问 0, 1, 2, 0, 1, 3, 0, 3, 1, 2, 1，三个页框：最优 6 次命中 5 次缺失，FIFO 命中率 36.4%）、Belady 异常的访问串、sem_wait 先减一再看是否为负、Lu 等人的统计（74 个非死锁、31 个死锁；97% 的非死锁 bug 是违反原子性或违反顺序）、死锁的四个条件、轮询和中断、活锁和合并中断、in / out 指令和内存映射 I/O、“Linux 内核超过 70% 的代码是设备驱动”、strace 里 open 返回 3、fork 后共享打开文件表项、vsfs 的布局（64 块、56 个数据块、80 个 inode、inode 32 在 20KB）、(12 + 1024) × 4KB = 4144KB、写缓冲 5 到 30 秒。C 代码的输出由 `tests/content/C.2.1.verify.py` 用 WSL 的 gcc 编译运行，数值用 Python 算。

## CS2023（`data/curation/scope.json`）

| 知识点 | CS2023 主题（scope.json 匹配原文） | 课 |
|---|---|---|
| 进程/线程 | OS-Concurrency，CS Core：Thread abstraction relative to concurrency | `threads-intro`, `memory-model` |
| 调度 | OS-Scheduling，KA Core：Preemptive and non-preemptive scheduling | `sjf-stcf`, `rr-io`, `mlfq` |
| 虚拟内存 | OS-Memory，KA Core：Virtual memory | `address-space`, `base-bounds`, `paging`, `tlb`, `multilevel`, `swapping`, `replacement` |
| 文件系统 | OS-Files，KA Core：Concept of a file | `files-api`, `file-sharing`, `dirs-metadata`, `links-permissions`, `fs-layout`, `fs-access` |
| I/O | OS-Devices，KA Core：Device driver purpose | `dma-drivers`（设备驱动的作用、文件系统栈、驱动占内核代码的比例） |
| 同步与隔离 | OS-Concurrency，CS Core：Race conditions, critical regions | `race`, `locks`, `cas-queues`, `semaphores`, `concurrency-bugs` |

## 综合练习（原技能树，约 50 分钟）

| 小题 | 要用到 | 课 |
|---|---|---|
| (1) 进程和线程的区别；fork 程序输出 child 2、parent 1 | fork 复制地址空间、wait | `process`, `fork-wait-exec`（原题就是 `fork-x`）, `threads-intro`（`proc-vs-thread`） |
| (2) 四个进程的 FCFS、非抢占 SJF、RR（q = 4）平均等待时间 | 调度算法、等待时间 | `sched-metrics`、`sjf-stcf`、`rr-io` 各有一张分步例题，正是这道题的三问（8.75、7.75、11.75） |
| (3) 32 位、4KB 页、4 字节页表项的页表多大；0x00403ABC 的页号和偏移；为什么要 TLB 和多级页表 | 分页、TLB、多级页表 | `paging`（`pt-size`、`vpn-hex`）, `tlb`, `multilevel`（`why-multilevel`） |
| (4) 引用串 7 0 1 2 0 3 0 4 2 3 0 3 2、3 个页框的 FIFO 和 LRU 缺页次数 | 页面置换 | `replacement`（这串引用就是 `fifo-sim`、`lru-sim` 两道“你来当置换算法”的题，答案 10 和 9 由判题代码和 verify 脚本各算一遍） |
| (5) 用信号量写有界缓冲区 | 信号量、互斥和计数 | `semaphores`（分步例题就是这道题的伪代码，`wrong-order-sim` 演示顺序反了会死锁） |

## 学习资源引用、大纲没收的章（C3）

`chapters[].zh/en` 引的是 OSTEP 的整段章号（如“第 13–24 章”“第 36–37 章”）。大纲的 `omitted` 写明了哪些章不收、归哪一站，本表照办：

| 章 | 内容 | 处理 |
|---|---|---|
| 第 9、10 章 | 彩票调度、多处理器调度 | 不教：调度进阶，大纲不收 |
| 第 14 章 | 内存 API（malloc、free） | P.2.2 的 `heap` 已教 |
| 第 16、17 章 | 分段、空闲空间管理 | 分段不教（大纲判为进阶；本站从基址界限直接讲到分页）；空闲列表在 P.2.2 的 `allocator` 教过，`base-bounds` 只用到“空闲列表”这个词 |
| 第 23 章 | 完整的虚拟内存系统（VAX/VMS、Linux） | 不教：大纲判为进阶；写时复制只在 `fork-wait-exec` 提一句 |
| 第 27 章 | 线程 API | `threads-intro` 教 `pthread_create`、`pthread_join`，`locks` 教 `pthread_mutex_lock` |
| 第 29、30、33 章 | 加锁的数据结构、条件变量、事件驱动并发 | 属于 C.2.2；条件变量在 `concurrency-bugs` 讲一张卡 |
| 第 37 章 | 磁盘 | 属于 C.2.4 存储系统与文件系统（大纲写明）；旧版包里的“算磁盘访问时间”随之移走 |
| 第 41 章 | 快速文件系统 FFS | 属于 C.2.4 |

## 后继技能用到的（C5）

以 C.2.1 为必须前置、已有内容包的后继技能只有 C.3.5 数据中心与高性能网络（version 1 旧包）。它直接用到、又不自己教的：

| C.3.5 用到的 | 课 |
|---|---|
| 用户态和内核态、系统调用要陷入内核、保存上下文 | `lde` |
| 每个包一次中断、轮询代替中断、中断太多会活锁 | `io-devices` |
| DMA：设备直接把数据写进内存 | `dma-drivers` |
| 虚拟地址、页表、物理内存不连续 | `address-space`, `paging` |
| 大页让 TLB 覆盖更大范围 | `tlb`（`coverage` 一题和“TLB 满了换掉谁”一卡） |
| 内核缓冲区和用户缓冲区之间的拷贝 | 不在这一站：C.3.5 的“内核路径贵在哪里”自己讲 |
| 注册内存时“锁页”（不让页被换出） | 本站只讲到页可以被换出到磁盘（`swapping`），锁页的含义 C.3.5 重写时要自己讲 |

前置站交给这一站的（P.2.2 覆盖表里写明“在 C.2.1 讲”的）：stat 和文件元数据、读目录 → `dirs-metadata`；打开文件表、fork 和 dup 共享文件、dup2 → `files-api`, `file-sharing`；fork、wait、exec → `fork-wait-exec`。
