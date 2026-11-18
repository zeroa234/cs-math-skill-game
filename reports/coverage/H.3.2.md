# H.3.2 嵌入式系统、驱动与 RTOS：覆盖表

**状态（2026-11-18）：已写完（v2，按零基础与知识覆盖面两条标准）。** 依据 `../cs-math-skill-tree/data/outlines/H.3.2.json`（Bootlin 三门免费课程的 agenda：A 嵌入式 Linux 系统开发、B 内核与驱动开发、C PREEMPT_RT 实时 Linux）、`data/curation/scope.json`、`data/curation/learning-paths/H.3.2.json`。24 课分 6 章；数值和程序输出由 `tests/content/H.3.2.verify.py` 核对，事实的出处见文末。

旧稿（2026-11-08 起草的 13 课）没有通过 B1、B3、B8 和 C1 深度检查，而且干扰项不是初学者真会犯的错、课名和题干里塞满大纲节号，已整份重写，没有沿用。

## 大纲逐节（C1：70/70 节有课教）

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Booting process of embedded platforms, focus on the x86 and ARM architectures | `boot-mcu`、`boot-linux` |
| 1.2 | Boot process and bootloaders on x86 platforms (legacy and UEFI) | `boot-linux` |
| 1.3 | Boot process on ARM platforms: ROM code, bootloaders, ARM Trusted Firmware | `boot-linux` |
| 1.4 | Focus on U-Boot: configuration, installation, and usage. | `u-boot` |
| 1.5 | U-Boot commands, U-Boot environment, U-Boot scripts, U-Boot generic distro boot mechanism | `u-boot` |
| 2.1 | How to access hardware on popular busses: USB, SPI, I2C, PCI | `hw-access` |
| 2.2 | Usage of kernel drivers and direct user-space access | `hw-access` |
| 2.3 | The Device Tree syntax, and how to use it to describe additional devices and pin-muxing | `device-tree` |
| 2.4 | Finding Linux kernel drivers for specific hardware devices | `device-tree` |
| 2.5 | Using kernel modules | `kernel-module` |
| 2.6 | Hardware access using /dev and /sys | `hw-access`、`device-model` |
| 2.7 | User-space interfaces for the most common hardware devices: storage, network, GPIO, LEDs, audio, graphics, video | `hw-access` |
| 3.1 | Linux device drivers | `kernel-module`、`char-driver` |
| 3.2 | A simple module | `kernel-module` |
| 3.3 | Programming constraints | `kernel-module` |
| 3.4 | Loading, unloading modules | `kernel-module` |
| 3.5 | Module dependencies | `kernel-module` |
| 3.6 | Adding sources to the kernel tree | `kernel-module` |
| 4.1 | Understand the pinctrl framework of the kernel | `device-tree` |
| 4.2 | Understand how to configure the muxing of pins | `device-tree` |
| 5.1 | Understand how the kernel is designed to support device drivers | `device-model` |
| 5.2 | The device model | `device-model` |
| 5.3 | Binding devices and drivers | `device-model` |
| 5.4 | Platform devices, Device Tree | `device-model`、`device-tree` |
| 5.5 | Interface in user space: /sys | `device-model` |
| 6.1 | Process management in the Linux kernel. | `tasks` |
| 6.2 | The Linux kernel scheduler and how processes sleep. | `tasks` |
| 6.3 | Interrupt handling in device drivers: interrupt handler registration and programming, scheduling deferred work | `irq-halves` |
| 7.1 | Issues with concurrent access to shared resources | `locks` |
| 7.2 | Locking primitives: mutexes, semaphores, spinlocks. | `locks`、`queues` |
| 7.3 | Atomic operations. | `locks` |
| 7.4 | Typical locking issues. | `locks` |
| 7.5 | Using the lock validator to identify the sources of locking problems. | `locks` |
| 8.1 | Linux: memory management - Physical and virtual (kernel and user) address spaces. | `kernel-memory` |
| 8.2 | Linux memory management implementation. | `kernel-memory` |
| 8.3 | Allocating with kmalloc(). | `kernel-memory` |
| 8.4 | Allocating by pages. | `kernel-memory` |
| 8.5 | Allocating with vmalloc(). | `kernel-memory` |
| 9.1 | Debugging with printing functions | `debugging` |
| 9.2 | Using Debugfs | `debugging` |
| 9.3 | Analyzing a kernel oops | `debugging` |
| 9.4 | Using kgdb, a kernel debugger | `debugging` |
| 9.5 | Using the Magic SysRq commands | `debugging` |
| 10.1 | Overview of the power management features of the kernel | `power` |
| 10.2 | Topics covered: clocks, suspend and resume, dynamic frequency scaling, saving power during idle, runtime power management, regulators, etc. | `power` |
| 11.1 | Definition of a Real-Time Operating System | `realtime` |
| 11.2 | Specificities of multi-task systems | `tasks`、`periodic`、`schedulability` |
| 11.3 | Common locking and prioritizing patterns | `schedulability`、`priority-inversion` |
| 11.4 | Overview of existing Real-Time Operating Systems | `realtime` |
| 11.5 | Approaches to bring Real-Time capabilities to Linux | `linux-rt` |
| 12.1 | History and future of the PREEMPT_RT patch | `linux-rt` |
| 12.2 | Real-Time improvements from PREEMPT_RT in mainline Linux | `linux-rt` |
| 12.3 | The internals of PREEMPT_RT | `linux-rt` |
| 12.4 | Interrupt handling: threaded interrupts, softirqs | `irq-halves`、`linux-rt` |
| 12.5 | Locking primitives: mutexes and spinlocks, sleeping spinlocks | `linux-rt` |
| 12.6 | Preemption models | `linux-rt` |
| 13.1 | Interrupts and deep firmware | `rt-latency` |
| 13.2 | Interaction with power management features: CPU frequency scaling and sleep states | `rt-latency`、`power` |
| 13.3 | DMA | `rt-latency` |
| 14.1 | Good practices when writing Linux kernel drivers | `irq-halves` |
| 14.2 | Scheduling policies and priorities: SCHED_FIFO, SCHED_RR, SCHED_DEADLINE | `linux-rt` |
| 14.3 | CPU and IRQ Affinity | `rt-latency` |
| 14.4 | Memory management | `rt-memory`、`kernel-memory` |
| 14.5 | CPU isolation with isolcpus | `rt-latency` |
| 15.1 | POSIX real-time API | `periodic`、`linux-rt` |
| 15.2 | Thread management and configuration | `linux-rt` |
| 15.3 | Memory management: memory allocation and memory locking, stack | `rt-memory` |
| 15.4 | Locking patterns: mutexes, priority inheritance | `priority-inversion` |
| 15.5 | Inter-Process Communication | `queues` |
| 15.6 | Signaling | `queues` |

大纲没有收、但这个技能的六个知识点要用的内容，也有课教：单片机上的 RTOS 主线（FreeRTOS 任务、`vTaskDelayUntil`、队列、信号量、互斥锁、堆 heap_1 到 heap_5、栈高水位，来自学习资源 zh1 和 en2）在 `tasks`、`periodic`、`queues`、`priority-inversion`、`rt-memory`；可调度性分析（利用率、Liu–Layland 上界、响应时间分析，en2 的 real-time scheduling）在 `schedulability`；可靠性（看门狗、栈溢出检测、A/B 升级、CRC 冗余、复位原因记录、软硬件协同，r7-zh2）在 `watchdog`、`recovery`。

## CS2023 核心主题（C2）

`scope.json` 给 H.3.2 匹配的 4 项都有课：

| 知识点 | CS2023 | 课 |
|---|---|---|
| 驱动 | OS-Devices / KA Core：Device driver purpose | `hw-access`、`kernel-module`、`device-model`、`char-driver` |
| 实时调度 | OS-Real-time / KA Core：Process and task scheduling | `tasks`、`periodic`、`schedulability`、`linux-rt` |
| 中断 | SPD-Embedded / KA Core：Interrupt handlers | `irq-halves`、`queues`（FromISR） |
| 资源 | SPD-Embedded / KA Core：Real-time resource management | `rt-memory`、`kernel-memory`、`priority-inversion`、`power` |

## 学习资源的章节（C3）

| 资源 | 讲到的概念 | 课 |
|---|---|---|
| zh1 野火 FreeRTOS 内核实现与应用开发 | 任务定义与切换、临界段、空闲任务与阻塞延时、多优先级、时间片；队列、信号量、互斥量、内存管理、中断 | `tasks`、`periodic`、`queues`、`locks`、`priority-inversion`、`rt-memory` |
| zh2 野火 i.MX6ULL 驱动开发 | 内核模块、字符设备、设备模型、平台驱动、设备树、pinctrl/gpio、I²C/SPI/中断子系统 | `kernel-module`、`char-driver`、`device-model`、`device-tree`、`irq-halves`；设备树例题用 i.MX6ULL 的 uart1 节点 |
| r7-zh1 野火 i.MX6ULL 基础教程第 5 章 | U-Boot 启动流程、加载设备树与内核 | `boot-linux`、`u-boot` |
| r7-zh2 苏州大学《嵌入式系统及应用》 | 复位与看门狗、稳定性问题、外接传感器与执行部件的构件化编程 | `watchdog`、`recovery` |
| en1 Bootlin 三门课 | 即大纲 A、B、C | 见上表 |
| en2 UT Austin ECE 445M | 上下文切换、实时调度、同步通信、内存管理、latency/jitter/deadline、调试测试 | `tasks`、`schedulability`、`queues`、`rt-latency`、`debugging` |

zh2 的 input、PWM、Framebuffer 子系统和 en2 的文件系统、网络没有单独成课：大纲把它们放在不收的部分（B 中的 input 子系统、I/O 内存、misc 子系统、DMA、mmap 等），用户空间接口在 `hw-access` 的表里各给了一行。

## 原技能树综合练习（C4）

| 小题 | 要用的内容 | 课 |
|---|---|---|
| (1) 裸机从复位到 main 前做什么；嵌入式 Linux 启动链 | 向量表、SystemInit、.data 复制、.bss 清零、C++ 构造；ROM → SPL → U-Boot → 内核和设备树 → 根文件系统 → init | `boot-mcu`、`boot-linux`；结业 `boss-chain`、`boss-bss` |
| (2) FreeRTOS 采样任务 10 ms 放队列、通信任务取出发送；优先级怎么排 | xTaskCreate、vTaskDelayUntil、pdMS_TO_TICKS、xQueueSend(…, 0)、xQueueReceive(…, portMAX_DELAY)；RM 和重要性都让采样任务优先级更高 | `periodic`、`queues`（整段参考代码）、`schedulability`；结业 `boss-queue`、`boss-rta` |
| (3) 高中低三任务加一个互斥量的优先级反转；优先级继承怎样解决 | 时间线、火星探路者号、FreeRTOS 互斥锁与 PTHREAD_PRIO_INHERIT | `priority-inversion`；结业 `boss-inversion` |
| (4) 字符设备驱动的结构；中断为什么分上半部和下半部 | 设备号、cdev、file_operations、copy_to_user、probe 和设备树匹配；上半部不能睡眠、下半部的四种形式 | `char-driver`、`device-model`、`irq-halves`；结业 `boss-copy`、`boss-probe`、`boss-irq` |
| (5) 三种提高可靠性的手段 | 看门狗、栈溢出检测（高水位、方法 1/2、MPU）、静态分配和内存池、CRC 与冗余、A/B 回滚、故障日志 | `watchdog`、`recovery`、`rt-memory`；结业 `boss-wdt`、`boss-ab` |

## 后继技能（C5）

H.3.2 没有必须后继（技能树里“直接解锁：无”），它是嵌入式远征的终点站。前置用到的写法：H.3.1 的中断、中断服务程序、原子操作、DMA、SysTick 和启动代码；F.1.1 的队列、链表。推荐前置 C.2.1 的进程、线程、调度、锁、虚拟内存等术语本包都重新讲了（B1 只认必须前置的包）。

## 事实出处与核对

- 数值和程序输出：`tests/content/H.3.2.verify.py`。WSL 里 gcc 15.2 实际编译运行：变量落在哪一段（`nm`、`size`）、`PTHREAD_PRIO_INHERIT` 的默认值和设置、无权限时 SCHED_FIFO 线程创建返回 EPERM、POSIX 消息队列按优先级出队、`clock_nanosleep` 绝对时间周期、驱动 read 函数的逻辑（把 copy_to_user 换成用户态桩函数）、FreeRTOS 风格任务代码的语法（API 用桩声明）；读真实系统：`chrt -m`、`sched_rr_timeslice_ms`、`getconf PAGESIZE`、`/proc/config.gz`。时间线、漂移、响应时间迭代、优先级反转与继承、队列长度、碎片、看门狗超时、电流和抖动用 Python 模拟或计算。
- 内核和驱动的接口语义：Linux 源码与文档（`include/linux/uaccess.h`、`irqreturn.h`、`interrupt.h`、`module.h`、`device/driver.h`、`fs.h`、`cdev.h`、`kernel/Kconfig.preempt`、`drivers/base/dd.c`、`pinctrl.c`、`Documentation/admin-guide/init.rst`、`devices.txt`、`kernel-parameters.txt`、`locking/locktypes.rst`、`core-api/real-time/`、`memory-allocation.rst`、`filesystems/debugfs.rst`、`imx6ul.dtsi`、`drivers/tty/serial/imx.c`、`drivers/hwmon/tmp102.c`）、U-Boot 文档、man7（sched、chrt、mlock、clock_nanosleep、mq_send、pthread_attr_setinheritsched）、LWN（6.12 合入 PREEMPT_RT 的最后部分）、GCC 手册（`-fzero-initialized-in-bss`）。
- FreeRTOS：官方文档与 FreeRTOS-Kernel 源码（栈深度单位、优先级、调度、vTaskDelay/xTaskDelayUntil、pdMS_TO_TICKS、队列、FromISR、互斥锁与优先级继承、任务通知快 45%、heap_1 到 heap_5、栈高水位、0xA5 填充）；ST 的启动文件和 HAL（Reset_Handler 顺序、链接符号、IWDG、复位标志）；Arm 手册（MPU 违规触发 MemManage）；MCUboot 文档；Liu & Layland 1973；Glenn Reeves 关于火星探路者号的邮件和 NASA 任务页；Koopman 的 CRC 论文。
- 逐条的出处和原文引文在 `reports/research/H.3.2/facts-linux.md`、`facts-rtos.md`（pi 子代理查证，主代理按需复核）；写课时只用了标为 CONFIRMED 的说法；查不到原文的说法（例如 ESP 用 FAT32、PAGE_SIZE 是 4096 的文档原句）没有写进课里，页大小用 WSL 实测值代替。
