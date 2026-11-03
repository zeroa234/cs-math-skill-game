# P.2.2 C/C++ 与底层编程：覆盖表

规则见 `docs/content-authoring.md` 的“知识覆盖面标准”。依据：skill-tree 大纲 `../cs-math-skill-tree/data/outlines/P.2.2.json`：Stanford CS107（2026 秋季，第 1–23 讲）和 B&O《深入理解计算机系统》（CS:APP 第 3 版）第 7 章“链接”、第 10 章“系统级 I/O”。“节”是技能内部编号，“原文”是来源自己的编号和标题。

`node scripts/check-coverage.mjs P.2.2` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | CS107 Lecture 1 Welcome to CS107! | `hello-c` |
| 1.2 | CS107 Lecture 2 Unix and C | `hello-c`, `c-basics`, `syscalls` |
| 2.1 | CS107 Lecture 3 Integers, Bits and Bytes | `bytes-addresses`（字节、十六进制、sizeof）；整数的二进制和补码在 C.1.1 讲 |
| 2.2 | CS107 Lecture 4 Bitwise Operators | 不教：位运算属于 C.1.1 计算机组成原理的“运算器”一章（这条路线上 C.1.1 是操作系统的必须前置，C 和 Python 的位运算符写法相同）；本站只用到“用 `\|` 合并几个选项”，在 `file-io` 里讲 |
| 2.3 | CS107 Lecture 5 More Bitwise Operators | 不教：同上，属于 C.1.1 |
| 3.1 | CS107 Lecture 6 Chars and C Strings | `c-strings` |
| 3.2 | CS107 Lecture 7 C Strings, Buffer Overflows and Security | `c-strings`, `memory-bugs`, `machine-stack` |
| 3.3 | CS107 Lecture 8 Introduction to Pointers | `bytes-addresses`, `pointers`, `arrays` |
| 4.1 | CS107 Lecture 9 Stack and Heap | `memory-map`, `stack-frames`, `heap` |
| 4.2 | CS107 Lecture 10 Heap Wrap, Generics and void * | `heap`, `void-pointers` |
| 4.3 | CS107 Lecture 11 Generics, void *, and Function Pointers | `void-pointers`, `function-pointers` |
| 5.1 | CS107 Lecture 12 Function Pointers, Continued | `function-pointers` |
| 5.2 | CS107 Lecture 13 Introduction to x86-64 | `machine-stack` |
| 5.3 | CS107 Lecture 14 Introduction to x86-64, Take II | 不教：x86-64 的数据传送和寻址方式属于 C.1.2 计算机体系结构（指令集）与 C.1.3（ABI 与汇编）；本站只在 `machine-stack` 里认识寄存器、mov、call、ret |
| 6.1 | CS107 Lecture 15 Introduction to x86-64, Take III | 不教：同上，属于 C.1.2 / C.1.3 |
| 6.2 | CS107 Lecture 16 Introduction to x86-64 ALU Operations | 不教：算术和逻辑指令属于 C.1.2 / C.1.3；运算器本身在 C.1.1 讲 |
| 6.3 | CS107 Lecture 17 x86-64 Condition Codes and Control Flow | 不教：条件码和跳转指令属于 C.1.2 / C.1.3 |
| 7.1 | CS107 Lecture 18 x86-64 Control Flow, Continued | 不教：同上，属于 C.1.2 / C.1.3 |
| 7.2 | CS107 Lecture 19 x86-64 Runtime Stack | `machine-stack` |
| 7.3 | CS107 Lecture 20 Privacy, Trust and Managing the Heap | `allocator`（管理堆的部分）；隐私与信任的伦理讨论不教，属于 S.1.1 安全原理 |
| 8.1 | CS107 Lecture 21 Managing the Heap | `allocator` |
| 8.2 | CS107 Lecture 22 Managing the Heap, Continued | `allocator` |
| 8.3 | CS107 Lecture 23 Explicit Free List Allocator | `allocator` |
| 9.1 | CS:APP 7.1 Compiler Drivers | `multi-file` |
| 9.2 | CS:APP 7.2 Static Linking | `multi-file`, `symbols` |
| 9.3 | CS:APP 7.3 Object Files | `multi-file`, `symbols` |
| 9.4 | CS:APP 7.4 Relocatable Object Files | `symbols` |
| 9.5 | CS:APP 7.5 Symbols and Symbol Tables | `symbols` |
| 9.6 | CS:APP 7.6 Symbol Resolution | `symbols`, `shared-libs` |
| 9.7 | CS:APP 7.7 Relocation | `symbols` |
| 9.8 | CS:APP 7.8 Executable Object Files | `shared-libs` |
| 9.9 | CS:APP 7.9 Loading Executable Object Files | `shared-libs` |
| 9.10 | CS:APP 7.10 Dynamic Linking with Shared Libraries | `shared-libs` |
| 9.11 | CS:APP 7.11 Loading and Linking Shared Libraries from Applications | `shared-libs` |
| 9.12 | CS:APP 7.12 Position-Independent Code (PIC) | `shared-libs` |
| 9.13 | CS:APP 7.13 Library Interpositioning | 不教：超出入门层（替换库函数是调试和安全分析的进阶技巧，属于 S.4.3 逆向工程） |
| 9.14 | CS:APP 7.14 Tools for Manipulating Object Files | `symbols`, `shared-libs` |
| 10.1 | CS:APP 10.1 Unix I/O | `syscalls`, `file-io` |
| 10.2 | CS:APP 10.2 Files | `file-io` |
| 10.3 | CS:APP 10.3 Opening and Closing Files | `file-io` |
| 10.4 | CS:APP 10.4 Reading and Writing Files | `file-io` |
| 10.5 | CS:APP 10.5 Robust Reading and Writing with the Rio Package | `file-io`（“读到的可能比要的少，要循环读”这一条）；Rio 包本身不教 |
| 10.6 | CS:APP 10.6 Reading File Metadata | 不教：stat 和文件元数据在 C.2.1 操作系统的“文件和目录”一课讲 |
| 10.7 | CS:APP 10.7 Reading Directory Contents | 不教：目录在 C.2.1 的“文件和目录”一课讲 |
| 10.8 | CS:APP 10.8 Sharing Files | 不教：打开文件表、fork 和 dup 共享文件在 C.2.1 讲 |
| 10.9 | CS:APP 10.9 I/O Redirection | `file-io`（`>` 让 1 号文件描述符指向文件）；dup2 在 C.2.1 讲 |
| 10.10 | CS:APP 10.10 Standard I/O | `file-io` |
| 10.11 | CS:APP 10.11 Putting It Together: Which I/O Functions Should I Use? | `file-io` |

教到什么深度（入门层）：
- 链接：认识 `nm` 的符号种类（T、D、B、U，小写表示只在本文件可见）、`multiple definition` 和 `undefined reference` 两种链接报错、`static` 和 `extern`；重定位只讲“链接器把调用处填上真正的地址”；静态库 `.a` 和共享库 `.so` 的区别、`-l` 选项、`ldd`、程序启动时由动态链接器 `ld-linux` 把共享库装进来、找不到共享库时的报错和 `LD_LIBRARY_PATH`；PIC 只讲“为什么共享库要编译成和位置无关”；`dlopen` 只讲“程序运行中也能按名字装载共享库”。
- 系统级 I/O：`open` 的几个标志、权限 `0644` 的意思、返回 -1 和 `perror`、`read` 返回 0 表示读完、读到的可能比要的少；`printf` 先放进缓冲区而 `write` 直接交给内核。
- x86-64：只认识寄存器（`%rdi`、`%rsi`、`%rax`、`%rsp`、`%rip`）、`mov`、`call` 把返回地址压栈、`ret` 弹出返回地址，以及为什么栈上的缓冲区溢出能改掉返回地址。
- 分配器：按 CS107 作业的教学模型讲（每块前面 8 字节的头记着块大小和“占用”标记、隐式空闲链表、首次适配、分割、合并、显式空闲链表），并说明 glibc 的 malloc 细节不同但思路相同。

## CS2023（`data/curation/scope.json`）

| 知识点 | CS2023 主题（scope.json 匹配原文） | 课 |
|---|---|---|
| 内存布局 | AR-Assembly，KA Core：Heap, static, stack, and code segments | `memory-map`, `stack-frames`, `machine-stack` |
| 指针 | FPL-Systems，CS Core：Direct, indirect, and indexed access to memory location | `pointers`, `arrays`, `structs`, `void-pointers` |
| 生命周期 | FPL-Systems，CS Core：Memory management | `lifetime`, `heap`, `memory-bugs`, `growing-arrays`, `linked-lists`, `allocator` |
| 链接与系统接口 | OS-Process，KA Core：shared libraries, and dynamic linking | `shared-libs` |

## 综合练习（原技能树，约 50 分钟）

| 小题 | 要用到 | 课 |
|---|---|---|
| (1) make_greeting 的两个问题和修正 | 返回局部数组的地址、sprintf 溢出、malloc + snprintf | `memory-bugs` |
| (2) g、s、a、p、*p 各在哪里 | data / BSS / 栈 / 堆 | `memory-map`, `heap` |
| (3) `*(p + 2)`、`p[-1]`、`sizeof(a) / sizeof(a[0])`、swap | 指针运算、按值传参 | `arrays`, `pointers` |
| (4) extern 变量和 static 函数的链接属性；undefined reference 是哪一步的错 | 外部链接、内部链接、链接阶段 | `multi-file`, `symbols` |
| (5) 用 std::string / unique_ptr 改写，说明 RAII | 析构时自动释放 | `memory-bugs` |

## 后继技能用到的写法（C5）

这条路线上以 P.2.2 为必须前置的是 C.2.1 操作系统。

| C.2.1 用到的 | 课 |
|---|---|
| 结构体和 `->`（进程表、页表项、inode 都用结构体写） | `structs` |
| 链表（就绪队列、空闲块链表） | `linked-lists` |
| `fork`、`wait`、`exec` | 不在这一站：C.2.1 自己教 |
| `open`、`read`、`write`、`close`、文件描述符、`perror` | `syscalls`, `file-io` |
| 函数指针（`pthread_create` 要传一个函数） | `function-pointers` |
| `void *`（线程函数的参数和返回值） | `void-pointers` |
| 栈帧、返回地址、寄存器（上下文切换要保存寄存器） | `stack-frames`, `machine-stack` |
| 位运算（拆虚拟地址、页表项里的标志位） | 不在这一站：C.1.1 讲（C.2.1 的必须前置） |
