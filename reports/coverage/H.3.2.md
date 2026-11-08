# H.3.2 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Booting process of embedded platforms, focus on the x86 and ARM architectures | `boot-mcu` |
| 1.2 | Boot process and bootloaders on x86 platforms (legacy and UEFI) | `boot-linux` |
| 1.3 | Boot process on ARM platforms: ROM code, bootloaders, ARM Trusted Firmware | `boot-linux` |
| 1.4 | Focus on U-Boot: configuration, installation, and usage. | `boot-linux` |
| 1.5 | U-Boot commands, U-Boot environment, U-Boot scripts, U-Boot generic distro boot mechanism | `boot-linux` |
| 2.1 | How to access hardware on popular busses: USB, SPI, I2C, PCI | `device-tree` |
| 2.2 | Usage of kernel drivers and direct user-space access | `device-tree` |
| 2.3 | The Device Tree syntax, and how to use it to describe additional devices and pin-muxing | `device-tree` |
| 2.4 | Finding Linux kernel drivers for specific hardware devices | `device-tree` |
| 2.5 | Using kernel modules | `linux-driver` |
| 2.6 | Hardware access using /dev and /sys | `linux-driver` |
| 2.7 | User-space interfaces for the most common hardware devices: storage, network, GPIO, LEDs, audio, graphics, video | `linux-driver` |
| 3.1 | Linux device drivers | `linux-driver` |
| 3.2 | A simple module | `linux-driver` |
| 3.3 | Programming constraints | `linux-driver` |
| 3.4 | Loading, unloading modules | `linux-driver` |
| 3.5 | Module dependencies | `linux-driver` |
| 3.6 | Adding sources to the kernel tree | `linux-driver` |
| 4.1 | Understand the pinctrl framework of the kernel | `device-tree` |
| 4.2 | Understand how to configure the muxing of pins | `device-tree` |
| 5.1 | Understand how the kernel is designed to support device drivers | `device-tree` |
| 5.2 | The device model | `device-tree` |
| 5.3 | Binding devices and drivers | `device-tree` |
| 5.4 | Platform devices, Device Tree | `device-tree` |
| 5.5 | Interface in user space: /sys | `linux-driver` |
| 6.1 | Process management in the Linux kernel. | `periodic-tasks` |
| 6.2 | The Linux kernel scheduler and how processes sleep. | `periodic-tasks` |
| 6.3 | Interrupt handling in device drivers: interrupt handler registration and programming, scheduling deferred work | `interrupt-context` |
| 7.1 | Issues with concurrent access to shared resources | `priority-inheritance` |
| 7.2 | Locking primitives: mutexes, semaphores, spinlocks. | `priority-inheritance` |
| 7.3 | Atomic operations. | `priority-inheritance` |
| 7.4 | Typical locking issues. | `priority-inheritance` |
| 7.5 | Using the lock validator to identify the sources of locking problems. | `priority-inheritance` |
| 8.1 | Linux: memory management - Physical and virtual (kernel and user) address spaces. | `resource-bounds` |
| 8.2 | Linux memory management implementation. | `resource-bounds` |
| 8.3 | Allocating with kmalloc(). | `resource-bounds` |
| 8.4 | Allocating by pages. | `resource-bounds` |
| 8.5 | Allocating with vmalloc(). | `resource-bounds` |
| 9.1 | Debugging with printing functions | `power-debug` |
| 9.2 | Using Debugfs | `power-debug` |
| 9.3 | Analyzing a kernel oops | `power-debug` |
| 9.4 | Using kgdb, a kernel debugger | `power-debug` |
| 9.5 | Using the Magic SysRq commands | `power-debug` |
| 10.1 | Overview of the power management features of the kernel | `power-debug` |
| 10.2 | Topics covered: clocks, suspend and resume, dynamic frequency scaling, saving power during idle, runtime power management, regulators, etc. | `power-debug` |
| 11.1 | Definition of a Real-Time Operating System | `periodic-tasks` |
| 11.2 | Specificities of multi-task systems | `periodic-tasks` |
| 11.3 | Common locking and prioritizing patterns | `priority-inheritance` |
| 11.4 | Overview of existing Real-Time Operating Systems | `periodic-tasks` |
| 11.5 | Approaches to bring Real-Time capabilities to Linux | `deadline` |
| 12.1 | History and future of the PREEMPT_RT patch | `latency-sources` |
| 12.2 | Real-Time improvements from PREEMPT_RT in mainline Linux | `latency-sources` |
| 12.3 | The internals of PREEMPT_RT | `latency-sources` |
| 12.4 | Interrupt handling: threaded interrupts, softirqs | `interrupt-context` |
| 12.5 | Locking primitives: mutexes and spinlocks, sleeping spinlocks | `interrupt-context` |
| 12.6 | Preemption models | `deadline` |
| 13.1 | Interrupts and deep firmware | `latency-sources` |
| 13.2 | Interaction with power management features: CPU frequency scaling and sleep states | `latency-sources` |
| 13.3 | DMA | `latency-sources` |
| 14.1 | Good practices when writing Linux kernel drivers | `interrupt-context` |
| 14.2 | Scheduling policies and priorities: SCHED_FIFO, SCHED_RR, SCHED_DEADLINE | `deadline` |
| 14.3 | CPU and IRQ Affinity | `deadline` |
| 14.4 | Memory management | `resource-bounds` |
| 14.5 | CPU isolation with isolcpus | `deadline` |
| 15.1 | POSIX real-time API | `periodic-tasks` |
| 15.2 | Thread management and configuration | `periodic-tasks` |
| 15.3 | Memory management: memory allocation and memory locking, stack | `resource-bounds` |
| 15.4 | Locking patterns: mutexes, priority inheritance | `priority-inheritance` |
| 15.5 | Inter-Process Communication | `queue-tasks` |
| 15.6 | Signaling | `queue-tasks` |

## CS2023、原综合练习与后续技能

- CS2023 的驱动用途、任务调度、中断处理和实时资源分别在 linux-driver、periodic-tasks/deadline、interrupt-context、resource-bounds。参考 [Bootlin 培训资料](https://bootlin.com/docs/) · [Linux PREEMPT_RT](https://docs.kernel.org/core-api/real-time/index.html) · [FreeRTOS API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/00-Task-creation)
- 原练习 (1) 见 boot-mcu、boot-linux，(2) 见 periodic-tasks、queue-tasks，(3) 见 priority-inheritance，(4) 见 linux-driver、interrupt-context，(5) 见 resource-bounds、recovery。Linux 与微控制器的执行环境分开讲，周期示例使用简化离散模型。
