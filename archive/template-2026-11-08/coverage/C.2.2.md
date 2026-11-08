# C.2.2 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Exceptions | `syscalls` |
| 1.2 | Processes | `syscalls` |
| 1.3 | System Call Error Handling | `syscalls` |
| 1.4 | Process Control | `syscalls` |
| 1.5 | Signals | `pipe` |
| 1.6 | Nonlocal Jumps | 不教：非局部跳转的栈恢复细节超出此处的系统调用入门范围。 |
| 1.7 | Tools for Manipulating Processes | `syscalls` |
| 2.1 | Unix I/O | `syscalls` |
| 2.2 | Files | `syscalls` |
| 2.3 | Opening and Closing Files | `syscalls` |
| 2.4 | Reading and Writing Files | `io` |
| 2.5 | Robust Reading and Writing with the Rio Package | `io` |
| 2.6 | Reading File Metadata | `io` |
| 2.7 | Reading Directory Contents | `io` |
| 2.8 | Sharing Files | `io` |
| 2.9 | I/O Redirection | `io` |
| 2.10 | Standard I/O | `io` |
| 2.11 | Putting It Together: Which I/O Functions Should I Use? | `io` |
| 3.1 | The Client-Server Programming Model | `multiplex` |
| 3.2 | Networks | 不教：以 C.3.2 的网络分层、IP 和 HTTP 课程为主，此包用套接字接口示范。 |
| 3.3 | The Global IP Internet | 不教：以 C.3.2 的网络分层、IP 和 HTTP 课程为主，此包用套接字接口示范。 |
| 3.4 | The Sockets Interface | `multiplex` |
| 3.5 | Web Servers | 不教：以 C.3.2 的网络分层、IP 和 HTTP 课程为主，此包用套接字接口示范。 |
| 3.6 | Putting It Together: The Tiny Web Server | 不教：以 C.3.2 的网络分层、IP 和 HTTP 课程为主，此包用套接字接口示范。 |
| 4.1 | Concurrent Programming with Processes | `pipe` |
| 4.2 | Concurrent Programming with I/O Multiplexing | `multiplex` |
| 4.3 | Concurrent Programming with Threads | `threads` |
| 4.4 | Shared Variables in Threaded Programs | `memory` |
| 4.5 | Synchronizing Threads with Semaphores | `mutex` |
| 4.6 | Using Threads for Parallelism | `threads` |
| 4.7.1 | Thread Safety | `threads` |
| 4.7.2 | Reentrancy | `threads` |
| 4.7.3 | Races | `race` |
| 4.7.4 | Deadlocks | `threads` |
| 5.1 | Building Working Spin Locks with Test-And-Set | `atomic` |
| 5.2 | Compare-And-Swap | `atomic` |
| 5.3 | Load-Linked and Store-Conditional | `atomic` |
| 5.4 | Fetch-And-Add | `atomic` |
| 6 | Eraser | `race` |

## 核心主题、综合练习与后继技能

核心主题依次在 `syscalls`（系统调用）、`mutex` / `threads`（信号量、互斥锁、条件变量）、`atomic`（原子指令）、`memory`（内存一致性）、`pipe` / `multiplex` / `race`（IPC 与检测）。原综合练习的管道、分段求和、死锁、有界队列和数据竞争分别由 `pipe`、`threads`、`threads`、`mutex`、`atomic` / `race` 准备。C.4.1 所需的并发进程、线程与通信由 `threads`、`pipe`、`multiplex` 打底。正式内存序另参考 [C++ 内存模型综述](https://arxiv.org/abs/1803.04432)，动态检测另参考 [LLVM ThreadSanitizer](https://clang.llvm.org/docs/ThreadSanitizer.html)。
