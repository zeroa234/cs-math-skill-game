<!-- pi 子代理 2026-11-18 为 H.3.2 查证的一手出处与逐字引文；写课时只用了标为 CONFIRMED 的说法。 -->
﻿# RTOS 事实核查报告（H.3.2 嵌入式 / FreeRTOS）

核查日期：2026-11-18（本地时区）。原则：只引primary source（freertos.org 官方文档、FreeRTOS/FreeRTOS-Kernel 源码、ARM 官方文档/CMSIS、ST 官方源码与文档、Liu & Layland 1973 原文、Glenn Reeves 本人邮件、NASA、Android AOSP、docs.mcuboot.com）。
"引用"为逐字摘录（<25 词，长句用 `…` 截断）。源码行号为 `main` 分支当前 HEAD。

---

## A. Cortex-M 裸机启动

**1a. 向量表第 0 个字是初始 MSP 值，第 1 个字是 Reset 处理函数地址** — CONFIRMED
- https://arm-software.github.io/CMSIS_5/Core/html/startup_s_pg.html
- 引："`.long __INITIAL_SP /* Initial Stack Pointer */` / `.long Reset_Handler /* Reset Handler */`"（CMSIS `__Vectors` 表模板）
- 旁证：https://raw.githubusercontent.com/STMicroelectronics/cmsis-device-f4/master/Source/Templates/gcc/startup_stm32f407xx.s — 引："`g_pfnVectors:  .word  _estack` … `.word  Reset_Handler`"

**1b. 复位时处理器从这两个字装载 MSP 与 PC** — PARTIALLY CONFIRMED（未能取到可逐字引用的 ARM 原文）
- 找到的替代证据：Arm CMSIS 文档同页："The reset handler which is executed after CPU reset and typically calls the SystemInit function." 与 "The setup values for the Main Stack Pointer (MSP)."
- Arm 官方页（developer.arm.com / support.arm.com）对本环境全部返回 403，无法直接取证；Arm DUI0553 该节检索摘要为："The vector table contains the reset value of the stack pointer"（未直连验证，仅作线索）。
- Cortex-M4 TRM（ARM DDI 0439B，PDF：https://documentation-service.arm.com/static/5f19da2a20b7cf4bc524d99a）只说明 "The processor enters Thread mode on Reset"，未写 MSP/PC 的装载过程。

**2. GCC 启动流程：Reset_Handler → SystemInit → 拷 .data → 清零 .bss → __libc_init_array → main** — CONFIRMED
- https://raw.githubusercontent.com/STMicroelectronics/cmsis-device-f4/master/Source/Templates/gcc/startup_stm32f407xx.s
- 引（顺序即为文件内顺序）："`bl  SystemInit`"（注释 "Call the clock system initialization function."）；"Copy the data segment initializers from flash to SRAM"；"Zero fill the bss segment"；"`bl __libc_init_array`"（注释 "Call static constructors"）；"`bl  main`"（注释 "Call the application's entry point."）
- `__libc_init_array` 语义（newlib 实现）：https://sourceware.org/git/?p=newlib-cygwin.git;a=blob_plain;f=newlib/libc/misc/init.c;hb=HEAD — 引："Handle ELF .{pre_init,init,fini}_array sections."；函数逐一调用 `__init_array_start[i]()`（即 C++ 静态构造）。

**3. 链接符号 `_sidata / _sdata / _edata / _sbss / _ebss`** — CONFIRMED
- 同上 startup_stm32f407xx.s — 引："start address for the initialization values of the .data section. defined in linker script"（对应 `.word _sidata`；`_sdata/_edata/_sbss/_ebss` 各有同款注释）
- 备注：注释里写的是"defined in linker script"，LMA/VMA 这套术语本身出自 GNU ld 文档，本次未逐字取到 ST 链接脚本（st.com 在本网络不可达）。

## B. FreeRTOS 任务与调度

**4. `xTaskCreate(..., uxStackDepth, ...)` 的栈深度以"字"为单位（不是字节）** — CONFIRMED
- https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/task.h#L341 — 引："The size of the task stack specified as the number of variables the stack can hold - not the number of bytes."（21 词）
- 官网同义："The number of words (not bytes!) to allocate for use as the task's stack." — https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate
- 源码示例注释亦有 "STACK_SIZE,      // Stack size in words, not bytes."（task.h:507）

**5. 优先级：0 最低（idle 任务 = tskIDLE_PRIORITY = 0）；数值越大优先级越高；范围 0 … configMAX_PRIORITIES − 1** — CONFIRMED
- https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/03-Task-priorities — 引："Each task is assigned a priority from 0 to ( configMAX_PRIORITIES - 1 )"；"Low priority numbers denote low priority tasks. The idle task has priority zero (tskIDLE_PRIORITY)."
- 源码：`#define tskIDLE_PRIORITY    ( ( UBaseType_t ) 0U )`（include/task.h:210）

**6. 默认固定优先级抢占调度；同优先级 Ready 任务按时间片轮转；时间片 = 一个 tick 周期（configUSE_PREEMPTION / configUSE_TIME_SLICING）** — CONFIRMED
- https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/04-Task-scheduling — 引："By default, FreeRTOS uses a fixed-priority preemptive scheduling policy, with round-robin time-slicing of equal priority tasks"；引："'Time sliced' means the scheduler will switch between tasks of equal priority on each tick interrupt"（该句后半即 "the time between tick interrupts being one time slice"）
- 默认值：`configUSE_TIME_SLICING` 未定义时默认为 1（include/FreeRTOS.h:2771-2773）；`configUSE_PREEMPTION` 必须在 FreeRTOSConfig.h 中显式给出（FreeRTOS.h:190-192）

**7. 任务状态：Running / Ready / Blocked / Suspended** — CONFIRMED
- https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states — 引："A task can exist in one of the following states:" + 四条状态名；"When a task is actually executing it is said to be in the Running state."；"A task is said to be in the Blocked state if it is currently waiting for either a temporal or external event."

**8. `vTaskDelay` 相对调用时刻；`vTaskDelayUntil/xTaskDelayUntil(pxPreviousWakeTime, xTimeIncrement)` 给固定频率；`xTaskDelayUntil` 未真正延时返回 pdFALSE；`pdMS_TO_TICKS` 转毫秒；configTICK_RATE_HZ 常见 1000** — CONFIRMED
- https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/01-vTaskDelay — 引："`vTaskDelay()` specifies a time at which the task wishes to unblock relative to the time at which `vTaskDelay()` is called."
- https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/03-xTaskDelayUntil — 引："Returns pdFALSE to indicate the task was not delayed"；"The macro pdMS_TO_TICKS() can be used to calculate the number of ticks from a time specified in milliseconds"
- 源码：`#define pdMS_TO_TICKS( xTimeInMs ) ( ( TickType_t ) ( ( ( uint64_t ) ( xTimeInMs ) * ( uint64_t ) configTICK_RATE_HZ ) / ( uint64_t ) 1000U ) )`（include/projdefs.h:41-43）
- configTICK_RATE_HZ=1000 的实例（ST/FreeRTOS 官方 STM32F407 demo）：https://raw.githubusercontent.com/FreeRTOS/FreeRTOS/main/FreeRTOS/Demo/CORTEX_M4F_STM32F407ZG-SK/FreeRTOSConfig.h — 引："`#define configTICK_RATE_HZ				( ( TickType_t ) 1000 )`"

**9. tick 中断驱动调度；Cortex-M 端口在 PendSV 中做上下文切换；SysTick 常用作 tick 源** — CONFIRMED
- https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/GCC/ARM_CM4F/port.c#L560 — 引（xPortSysTickHandler 内）："Increment the RTOS tick."；"Context switching is performed in the PendSV interrupt.  Pend the PendSV interrupt."
- 同文件 vPortSetupTimerInterrupt：引："Setup the systick timer to generate the tick interrupts at the required frequency."；"Configure SysTick to interrupt at the requested rate."
- `portYIELD()`：引："Set a PendSV to request a context switch."（portable/GCC/ARM_CM4F/portmacro.h:88-91）

## C. 队列、信号量、互斥量、ISR

**10. `xQueueCreate(uxQueueLength, uxItemSize)` 按值拷贝；`xQueueSend(xQueue, pvItemToQueue, xTicksToWait)` 返回 pdPASS 或 errQUEUE_FULL；xTicksToWait=0 时队列满立即返回；INCLUDE_vTaskSuspend 为 1 时 portMAX_DELAY 永久阻塞** — CONFIRMED（一处措辞差异见"矛盾"节）
- https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate — 引："Items are queued by copy, not by reference"；"The size, in bytes, required to hold each item in the queue."
- https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/03-xQueueSend — 引："`pdPASS` if the item was successfully posted, otherwise `errQUEUE_FULL`."；"The call will return immediately if the queue is full and `xTicksToWait` is set to 0."；"specifying the block time as `portMAX_DELAY` will cause the task to block indefinitely (without a timeout)."
- 源码：queue.h:107（"Items are queued by copy, not by reference, so this is the number of bytes"）；`pdPASS` 即 `pdTRUE`（include/projdefs.h:59 `#define pdPASS ( pdTRUE )`）

**11. `xQueueReceive` 收到项返回 pdPASS/pdTRUE，并把该项从队列移除** — CONFIRMED
- https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/queue.h#L837 — 引："Successfully received items are removed from the queue."
- 官网：https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/09-xQueueReceive — 引："`pdPASS` if an item was successfully received from the queue, otherwise `errQUEUE_EMPTY`."

**12. ISR 内必须用 `xQueueSendFromISR(..., &xHigherPriorityTaskWoken)` 再 `portYIELD_FROM_ISR(xHigherPriorityTaskWoken)`；非 FromISR API 不得在 ISR 调用；只有优先级在 configMAX_SYSCALL_INTERRUPT_PRIORITY 及其之下（Cortex-M 上数值 ≥）的中断才能调 FromISR API** — CONFIRMED
- https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/04-xQueueSendFromISR — 引："It is safe to use this function from within an interrupt service routine."；"a context switch should be requested before the interrupt is exited."
- 非 ISR 版本禁用：https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/03-xQueueSend — 引："This function must not be called from an interrupt service routine."
- 优先级规则：https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization — 引："Any interrupt that uses the FreeRTOS API must be set to the same priority as the RTOS kernel … or at or below configMAX_SYSCALL_INTERRUPT_PRIORITY"；"ARM Cortex-M3 cores use numerically low priority numbers to represent HIGH priority interrupts"
- 源码：`#define portYIELD_FROM_ISR( x )    portEND_SWITCHING_ISR( x )`（portable/GCC/ARM_CM4F/portmacro.h:114）；port.c 中断言注释："ISR safe FreeRTOS API functions must *only* be called from interrupts that have been assigned a priority at or below configMAX_SYSCALL_INTERRUPT_PRIORITY."

**13. 互斥量含优先级继承、二值信号量不含；互斥量不得在中断中使用；有递归互斥量；直接任务通知是更轻量的替代（xTaskNotifyGive / ulTaskNotifyTake），官方称快 45%** — CONFIRMED
- https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes — 引："Mutexes are binary semaphores that include a priority inheritance mechanism."；"Mutexes should not be used from an interrupt because:"（下一条即"含优先级继承机制，只在任务间才说得通"）
- 二值信号量无继承：include/semphr.h:71-72 — 引："semaphore does not use a priority inheritance mechanism.  For an alternative that does use priority inheritance see xSemaphoreCreateMutex()."
- 递归互斥量：`xSemaphoreCreateRecursiveMutex()` / `xSemaphoreTakeRecursive()` / `xSemaphoreGiveRecursive()`（include/semphr.h；文档页 …/10-Semaphore-and-Mutexes/08-xSemaphoreCreateRecursiveMutex）
- 45% 声明：https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications — 引："Unblocking an RTOS task with a direct notification is 45% faster† and uses less RAM than unblocking a task using an intermediary object"（原文 "45% faster" 为加粗，带脚注 †）

**14. 计数信号量：用于计数事件 / 管理资源** — CONFIRMED
- https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/03-Counting-semaphores — 引："Counting semaphores are typically used for two things:" + "Counting events." + "Resource management."

**15. 临界区 `taskENTER_CRITICAL/taskEXIT_CRITICAL`；Cortex-M 上把中断屏蔽到 configMAX_SYSCALL_INTERRUPT_PRIORITY；`taskDISABLE_INTERRUPTS`；`vTaskSuspendAll` 挂起调度器** — CONFIRMED
- 源码：portable/GCC/ARM_CM4F/portmacro.h:213-228 — `vPortRaiseBASEPRI()` 内联汇编 `msr basepri, %0 : "=r"(...) : "i"( configMAX_SYSCALL_INTERRUPT_PRIORITY )`；`#define portDISABLE_INTERRUPTS() vPortRaiseBASEPRI()`（同文件:122）
- include/task.h:231-241 — 引："Macro to mark the start of a critical code region.  Preemptive context switches cannot occur when in a critical region."
- include/task.h:275 `#define taskDISABLE_INTERRUPTS() portDISABLE_INTERRUPTS()`，注释 "Macro to disable all maskable interrupts."
- include/task.h:1657-1660 — 引："Suspends the scheduler without disabling interrupts.  Context switches will not occur while the scheduler is suspended."

**16. FreeRTOS 优先级继承的局限（"basic priority inheritance"；持有者释放互斥量/释放所有互斥量后才恢复原优先级）** — CONFIRMED
- https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes — 引："FreeRTOS implements a basic priority inheritance mechanism which was designed to optimize both space and execution cycles."；"A task remains at its highest inherited priority until it has released all the mutexes it holds."；"Priority inheritance does not cure priority inversion! It just minimises its effect in some situations."

## D. 内存与可靠性

**17. heap_1（只分配不释放）/ heap_2（可释放但不合并，已属 legacy）/ heap_3（包装 malloc/free，线程安全）/ heap_4（合并相邻空闲块 + first fit）/ heap_5（同 heap_4 但可跨不连续区域，用 vPortDefineHeapRegions）；静态分配 xTaskCreateStatic + configSUPPORT_STATIC_ALLOCATION** — CONFIRMED
- https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management — 引："heap_2 is now considered legacy as the newer heap_4 implementation is preferred."；"This scheme uses a first fit algorithm and, unlike scheme 2, it does combine adjacent free memory blocks"；"allows the heap to span multiple non adjacent (non-contiguous) memory regions"；heap_3 "The wrapper simply makes the malloc() and free() functions thread safe."
- heap_1.c 文件头：portable/MemMang/heap_1.c:31-32 — 引："The simplest possible implementation of pvPortMalloc().  Note that this implementation does NOT allow allocated memory to be freed again."
- heap_2.c 文件头：portable/MemMang/heap_2.c:31-33 — 引："does not combine adjacent free blocks into a single larger block (and so will fragment memory)"
- 静态分配：include/FreeRTOS.h:2841-2844 `#ifndef configSUPPORT_STATIC_ALLOCATION` → 默认 0（"Defaults to 0 for backward compatibility."）；`xTaskCreateStatic()` 文档见 include/task.h（引："allows a task to be created without using any dynamic memory allocation."）

**18. `uxTaskGetStackHighWaterMark` 返回任务启动以来剩余栈空间最小值（以字为单位）；configCHECK_FOR_STACK_OVERFLOW 方法 1/2（方法 2 检查末尾 16 字节，填充值为 0xA5）；vApplicationStackOverflowHook** — CONFIRMED
- https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/04-uxTaskGetStackHighWaterMark — 引："returns the minimum amount of remaining stack space that was available to the task since the task started executing"；"The value returned is the high water mark in words"
- https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking — 引（方法 2）："check the last 16 bytes within the valid stack range to ensure that these known values have not been overwritten"；"Set configCHECK_FOR_STACK_OVERFLOW to 2 to use this method."
- 0xA5 证据：tasks.c:121 `#define tskSTACK_FILL_BYTE ( 0xa5U )`，tasks.c:1835 任务创建时 `memset( pxNewTCB->pxStack, ( int ) tskSTACK_FILL_BYTE, uxStackDepth * sizeof( StackType_t ) )`
- 备注：官方页另列"方法 3"（部分端口支持 ISR 栈检查，触发 assert 而非 hook）。

**19. configUSE_MALLOC_FAILED_HOOK / vApplicationMallocFailedHook** — CONFIRMED
- include/FreeRTOS.h:93-95 `#ifndef configUSE_MALLOC_FAILED_HOOK` → 默认 0
- portable/MemMang/heap_4.c:336-341 — 引："`#if ( configUSE_MALLOC_FAILED_HOOK == 1 )` … if( pvReturn == NULL ) { vApplicationMallocFailedHook(); }"

## E. 实时理论

**20. RM（周期越短优先级越高）在"独立周期任务、D=T"下对固定优先级最优；Liu & Layland 界 U ≤ n(2^{1/n} − 1)，n=2 ≈0.828、n=3 ≈0.780、n→∞ → ln2 ≈0.693** — CONFIRMED
- 原文：https://www.cs.ru.nl/~hooman/DES/liu-layland.pdf — 引："THEOREM 2. If a feasible priority assignment exists for some task set, the rate-monotonic priority assignment is feasible for that task set."；"tasks with higher request rates will have higher priorities"；"THEOREM 5. … the least upper bound to processor utilization is U = m (2 i/m - 1)"；"For m = 3, eq. (6) becomes U = 3(2^{1/3}) - 1) ≈ 0.78 and for large m, U → ln 2"（PDF OCR 原样，符号为 ≈/→）；两任务情形 "U = 2(2½ - 1) ≈ 0.83"
- 综述（Univ. of York, R. Davis）：https://www-users.york.ac.uk/~rd17/papers/SingleProcessorSchedulingReview.pdf — 引："with a shorter period implying a higher priority, is the optimal priority assignment policy for such task sets."；"total utilisation U ≤ ln(2) ≈ 0.693"

**21. 响应时间分析 R_i = C_i + Σ_{j∈hp(i)} ceil(R_i/T_j)·C_j，迭代至收敛；R_i ≤ D_i 则可行** — CONFIRMED（公式在我取到的 PDF 里是排版公式，文本层无法逐字引用）
- https://www-users.york.ac.uk/~rd17/papers/SingleProcessorSchedulingReview.pdf — 引："The length of the busy period wi , can be computed using the following fixed point iteration"（式 (1)，含求和项与 blocking B_i）；"task τi is schedulable if and only if Ri ≤ Di"；归属："Exact schedulability tests … were introduced by Joseph and Pandya in 1986 [48], Lehoczky et al. in 1989 [55], and Audsley et al. in 1993 [5]."
- 讲义（TU/e, R.J. Bril）：https://johanl.win.tue.nl/educ/RTcourse/RT-course-OOTIs-FPPS-analysis.pdf — 引："Iterative procedure"…"the same value is found for two successive iterations; or the deadline WDi is exceeded (hence, not schedulable)"
- 注：该讲义与本综述的公式均为排版数学，pdftotext 取出的文本层已失真，故 R_i 递归式的"逐字符引用"未取得；结构与上述文字描述一致。

**22. EDF 在单处理器、D=T、U ≤ 1 时最优** — CONFIRMED
- https://www.cs.ru.nl/~hooman/DES/liu-layland.pdf — 引："THEOREM 7. For a given set of m tasks, the deadline driven scheduling algorithm is feasible if and only if"（后接 Σ C_i/T_i ≤ 1）
- https://www-users.york.ac.uk/~rd17/papers/SingleProcessorSchedulingReview.pdf — 引："Liu and Layland [56] also showed that that EDF can schedule any task set that has a total utilisation U ≤ 1"；"In 1974, Dertouzos [41] showed that pre-emptive EDF is an optimal single processor scheduling algorithm"

**23. Mars Pathfinder 1997：VxWorks；低优先级气象任务持锁；高优先级总线任务阻塞；中优先级通信任务运行；看门狗/监视机制导致整机复位；修法是打开该互斥量的优先级继承并从地球上传；着陆日期 1997-07-04** — CONFIRMED（细节有一处偏差，见"矛盾"节）
- Glenn Reeves 本人邮件（RISKS 转载）：https://users.cs.duke.edu/~carla/mars.html — 引："The failure turned out to be a case of priority inversion"；"The reaction to this by the spacecraft was to reset the computer."；"change the creation flags for the semaphore so as to enable the priority inheritance."；"the 'options' parameter for the semCreate used by the select service"
- Mike Jones 摘要（Cornell 存放）：https://www.cs.cornell.edu/courses/cs614/1999sp/papers/pathfinder.html — 引："a watchdog timer would go off, notice that the data bus task had not been executed for some time"；"its July 4th, 1997 landing on the Martian surface"
- NASA：https://science.nasa.gov/mission/mars-pathfinder — 引："Mars Landing | July 4, 1997"

## F. 看门狗与升级

**24a. STM32 IWDG：由 LSI（约 32 kHz）驱动；预分频可选 4…256；12 位重装寄存器（最大 0xFFF）** — CONFIRMED
- ST 官方培训材料：https://www.st.com/resource/en/product_training/STM32WB-WDG_TIMERS-Independent-Watchdog-IWDG.pdf — 引："independent 32-kHz low-speed internal RC oscillator (LSI)"；"The IWDG_PR prescaler register can divide the LSI clock frequency by 4 up to 256."；"The watchdog counter reload value is a 12-bit value written in the IWDG_RLR register."
- ST HAL 源码（STM32F4）：https://raw.githubusercontent.com/STMicroelectronics/stm32f4xx-hal-driver/master/Inc/stm32f4xx_hal_iwdg.h — 引：`IWDG_PRESCALER_4 … IWDG_PRESCALER_256`；reload "between Min_Data = 0 and Max_Data = 0x0FFF"

**24b. 超时公式 timeout = (4·2^PR)·(RLR+1)/f_LSI** — UNCONFIRMED（未取到可逐字引用的 ST 公式）
- 找到的替代证据：ST 培训 PPT 用图片给出公式（文字层只有 "A formula can be used determine the independent watchdog timeout."），HAL 默认超时宏用 `6UL * 256UL * 1000UL / (LSI_VALUE / 128U)`（即最高档 256 = 4·2^6 的写法相吻合），硬件默认 PR=0 时"a division by 4 on the input clock"。RM0090（st.com）在本网络不可达（多个 URL 均超时），故公式本身只能标为未逐字确认。

**24c. WWDG 由 APB 时钟驱动** — CONFIRMED
- https://raw.githubusercontent.com/STMicroelectronics/stm32f4xx-hal-driver/master/Src/stm32f4xx_hal_wwdg.c — 引："The WWDG counter input clock is derived from the APB clock divided …"；"WWDG clock (Hz) = PCLK1 / (4096 * Prescaler)"

**25. A/B 双备份升级与回滚：MCUboot 的 swap + 测试/回滚；RAUC（嵌入式 Linux）；Android A/B seamless** — CONFIRMED
- https://docs.mcuboot.com/design.html — 引："MCUboot will perform a "revert" swap during the next boot by swapping the image(s) back into its original location(s)"；"Test swaps are supported to provide a rollback mechanism to prevent devices from becoming "bricked" by bad firmware."
- https://source.android.com/docs/core/ota/ab — 引："Legacy A/B system updates, also known as seamless updates, ensure a workable booting system remains on the disk"；"A/B system updates use two sets of partitions referred to as slots (normally slot A and slot B)."
- RAUC：https://rauc.readthedocs.io/en/latest/ （文档存在，标题 "RAUC documentation!"；"Updating an Embedded Device"）。SWUpdate / Mender 本次未单独取证。

**26a. Cortex-M 的 MPU（ARMv7-M 上典型 8 个 region）** — CONFIRMED
- Arm 官方博客：https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/what-s-new-with-the-memory-protection-unit-mpu-in-cortex-m23-and-cortex-m33 — 引："Previously, the number of regions allowed on a Cortex-M0+, Cortex-M3, or Cortex-M4 was either 0 or 8."
- 另：FreeRTOS 配置项默认 `configTOTAL_MPU_REGIONS 8 /* Default value */`（freertos.org Customization 页）

**26b. FreeRTOS-MPU 存在** — CONFIRMED
- https://www.freertos.org/Security/04-FreeRTOS-MPU-memory-protection-unit — 引："FreeRTOS provides official Memory Protection Unit (MPU) support on ARMv7-M (Cortex-M3, Cortex-M4 and Cortex-M7 microcontrollers) and ARMv8-M"；"restricting access to resources such as RAM, … and memory beyond the limit of a task's stack"

**26c. "用 no-access 保护页（guard region）抓栈溢出"这一具体做法** — UNCONFIRMED（没有找到可逐字引用的 ARM/FreeRTOS 原文）
- 找到的替代：FreeRTOS 只说 MPU 能限制"memory beyond the limit of a task's stack"（上引）；FreeRTOS 的 ARMv7-M MPU 端口源码（portable/GCC/ARM_CM4_MPU/port.c）中检索不到 "guard"/"stack overflow" 相关说明。

---

## 与上述陈述不符 / 需要修正的地方

1. **事实 10 的返回值措辞**：官方文档写的是 `pdPASS`（"pdPASS if the item was successfully posted, otherwise errQUEUE_FULL"），不是 `pdTRUE`。两者数值相同（projdefs.h:59 `#define pdPASS ( pdTRUE )`），讲课时说 "pdPASS（等价于 pdTRUE）" 更准确。
2. **事实 23 的角色分配与官方叙述有偏差**：按 Reeves 邮件，被阻塞的是 **bc_dist**（第 3 高优先级，走 pipe/select 的 IPC，而不是 1553 信息总线的双缓冲），持锁的是 **ASI/MET 低优先级任务**，检测到"bc_dist 未在本周期完成"的是 **bc_sched（最高优先级）**；邮件里说的是"spacecraft ... reset the computer"，而"watchdog timer"这一说法来自 Mike Jones 的摘要，不是 Reeves 原文。另外 references 里提到的是 `semMCreate`（semCreate 的拼写在该邮件中为 "semMCreate"）。
3. **事实 4 的参数名**：现行内核为 `uxStackDepth`（旧文档/旧版本为 `usStackDepth`），且类型是 `configSTACK_DEPTH_TYPE`。课堂若写 `usStackDepth` 属于旧名。
4. **事实 18 的"方法 1/2"不是全部**：官方页现在还有 "Stack Overflow Detection - Method 3"（部分端口支持 ISR 栈检查，触发 assert，不调用 hook）。
5. **事实 24b 无法逐字确认**：ST 的超时公式在官方材料中是图片；RM0090 不可达。公式的各个组成（4…256 分频、12 位 RLR、32 kHz LSI）均已确认，但"4·2^PR"这一闭式写法属未验证转述。
6. **事实 1b 与 26c**：Arm 官方站点（developer.arm.com / support.arm.com）对本环境全部 403，这两点是本报告唯一没能拿到一手逐字证据的技术断言（ARMv7-M ARM 里确有相应描述，但本次未能下载到）。

---
统计（共 26 条待核事实，拆成 31 个小节）：**CONFIRMED 28 节**，**PARTIALLY 1 节**（1b：向量表布局已确认，"复位时由硬件装载 MSP/PC"未取到一手原文），**UNCONFIRMED 2 节**（24b 公式闭式、26c 用 MPU guard region 抓栈溢出的具体说法）。

---

## Follow-up

核查日期：2026-11-18。规则同上：每条给"一句英文事实 + source URL + 逐字引用（<25 词）"，源码注释也算引用，不猜。

### 1. STM32 IWDG 超时的推导（HAL "How to use this driver" 注释块）

**1a. 请求的写法 "IWDG counter clock Frequency = LsiFreq / Prescaler" / "Counter Reload Value = …" 在该文件的注释块里不存在** — PARTIALLY CONFIRMED（文件里没有这两行，只有下面这些等价内容）
- https://raw.githubusercontent.com/STMicroelectronics/stm32f4xx-hal-driver/master/Src/stm32f4xx_hal_iwdg.c
- 引（L32-33）："The IWDG is clocked by the Low-Speed Internal clock (LSI) and thus stays active even if the main clock fails."
- 引（L52）："[..] Min-max timeout value @32KHz (LSI): ~125us / ~32.7s"
- 引（L113-118，HAL_IWDG_DEFAULT_TIMEOUT 上方）："The timeout value is calculated using the highest prescaler (256) and the LSI_VALUE constant."（宏本体：`#define HAL_IWDG_DEFAULT_TIMEOUT (((6UL * 256UL * 1000UL) / (LSI_VALUE / 128U)) + ((LSI_STARTUP_TIME / 1000UL) + 1UL))`，即 timeout 由 LSI 频率、预分频、重装值共同决定）
- 说明：我也检查了 stm32l4xx / stm32g4xx / stm32h5xx / stm32u5xx / stm32h7xx 的 `*_hal_iwdg.c` 与 `*_ll_iwdg.h`，同样没有那句 "IWDG counter clock Frequency = LsiFreq / Prescaler"；能逐字引用的是上面三段。

**1b. STM32F4 HAL 中 LSI 标称值 32000 Hz（LSI_VALUE）** — CONFIRMED
- https://raw.githubusercontent.com/STMicroelectronics/stm32f4xx-hal-driver/master/Inc/stm32f4xx_hal_conf_template.h
- 引（L114-115）："`#define LSI_VALUE               32000U    /*!< LSI Typical Value in Hz */`"

**1c. IWDG 一旦启动就不能停止（LSI 被强制开启），只能靠复位** — CONFIRMED
- 同 1a 文件，L34-36："Once the IWDG is started, the LSI is forced ON and both cannot be disabled."
- ST 培训材料：https://www.st.com/resource/en/product_training/STM32WB-WDG_TIMERS-Independent-Watchdog-IWDG.pdf — 引："Once enabled, it forces the activation of the low-speed internal oscillator, and it can only be disabled by a reset."

### 2. 现有 RTOS 一览（用于一张表）

| RTOS | 一句事实 | 逐字引用 | 来源 |
|---|---|---|---|
| FreeRTOS | MIT 许可 | "MIT License"（LICENSE.md 首行） | https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/LICENSE.md |
| Zephyr | Linux Foundation 项目，Apache 2.0 | "Zephyr® Project, a Linux Foundation Project."；"Zephyr is permissively licensed using the Apache 2.0 license" | https://zephyrproject.org/ ; https://docs.zephyrproject.org/latest/introduction/index.html |
| VxWorks | Wind River 的商业 RTOS，用于 Mars Pathfinder | "VxWorks Safety certified RTOS with deterministic performance and reliability for mission-critical embedded systems."；Pathfinder："VxWorks, the real-time embedded systems kernel that was used in the Mars Pathfinder mission" | https://www.windriver.com/products/vxworks ; https://www.cs.cornell.edu/courses/cs614/1999sp/papers/pathfinder.html |
| QNX Neutrino | 微内核 RTOS | "The QNX Neutrino Microkernel … implements the core POSIX features used in embedded realtime systems" | https://www.qnx.com/developers/docs/7.1/com.qnx.doc.neutrino.sys_arch/topic/kernel.html |
| RTEMS | 开源，用于航天 | "RTEMS is an open source Real Time Operating System (RTOS) that supports open standard application programming interfaces (API) such as POSIX."；"It is used in space flight, medical, networking …" | https://www.rtems.org/ |
| Eclipse ThreadX（原 Azure RTOS ThreadX） | Eclipse 基金会下的开源项目，MIT 许可 | "Eclipse ThreadX RTOS … designed specifically for deeply embedded applications."；LICENSE 首行 "MIT License / Copyright (c) 2024 - present Microsoft Corporation" | https://github.com/eclipse-threadx/threadx ; https://raw.githubusercontent.com/eclipse-threadx/threadx/master/LICENSE.txt ; https://projects.eclipse.org/projects/iot.threadx |
| NuttX | Apache 许可，POSIX 兼容 | "Apache NuttX is a real-time operating system (RTOS) with an emphasis on standards compliance and small footprint."；"the primary governing standards in NuttX are POSIX and ANSI standards" | https://raw.githubusercontent.com/apache/nuttx/master/README.md ; https://raw.githubusercontent.com/apache/nuttx/master/LICENSE |
- 备注：VxWorks 的"商业（专有）"这一点在官网产品页只有产品定位、没有可逐字引用的许可声明；"Wind River 出品"由该页标题 "VxWorks RTOS | Real-Time Operating System | Wind River" 体现。Zephyr 的 Apache 2.0 亦可由仓库 LICENSE 首行 "Apache License Version 2.0" 佐证。

### 3. 硬实时 / 软实时 与"确定性"

**3a. 硬实时=必须在时限内完成且要保证；软实时=响应时间按统计分布可接受** — CONFIRMED
- https://www.cs.ru.nl/~hooman/DES/liu-layland.pdf（Liu & Layland 1973, p.52）
- 引："Service within this span of time must be guaranteed, categorizing the environment as \"hard-real-time\""；"in contrast to \"soft-real-time\" where a statistical distribution of response times is acceptable."

**3b. FreeRTOS 官方对 RTOS 的定性是"小且确定（deterministic）"，并强调硬实时与非硬实时的区分** — CONFIRMED
- https://www.freertos.org/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/01-RTOS-fundamentals
- 引："A Real-Time Operating System (RTOS) is a type of computer operating system designed to be small and deterministic."；"need to react to external events within strict time constraints."；软实时例："(soft real-time). If the longest acceptable period was 100ms - any response between 0 and 100ms would be acceptable."；"even when the embedded system has no hard real-time requirement at all"
- 注意：该页没有给 "hard real-time" 的形式化定义句，形式定义取自 3a。

### 4. 队列集合 / SendToBack vs SendToFront / Overwrite（长度 1 的邮箱）

**4a. 队列集合：允许任务同时阻塞等待多个队列或信号量** — CONFIRMED
- https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/queue.h#L1698
- 引："Queue sets provide a mechanism to allow a task to block (pend) on a read operation from multiple queues or semaphores simultaneously."
- 同处亦有 "configUSE_QUEUE_SETS == 1" 条件编译与 `xQueueCreateSet()` 原型，以及提示："Blocking on a queue set that contains a mutex will not cause the mutex holder to inherit the priority"

**4b. `xQueueSendToBack` 与 `xQueueSendToFront` 都存在（数据可从队首或队尾入队）** — CONFIRMED
- 同 queue.h，L277 / L360
- 引："Post an item to the front of a queue.  The item is queued by copy, not by"；"Post an item to the back of a queue.  The item is queued by copy, not by"
- 规模划分：L1060/L1229 等 ISR 版本："It is safe to use this macro from" 中断

**4c. `xQueueOverwrite` 专用于长度为 1 的队列（邮箱），队满时覆盖旧值** — CONFIRMED
- 同 queue.h，L524-529
- 引："Only for use with queues that have a length of one - so the queue is either empty or full."；"Post an item on a queue.  If the queue is already full then overwrite the value held in the queue."
- 返回值说明："pdPASS is the only value that can be returned because xQueueOverwrite() will write to the queue even when the queue is already full."

### 5. 软件定时器跑在 timer service（daemon）任务里，回调不能阻塞

**5a. 定时器功能由 timer service / daemon 任务提供（可选组件，不属于内核核心）** — CONFIRMED
- https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/02-Timer-service-daemon-task
- 引："Timer functionality is optional, and not part of the core FreeRTOS kernel. It is instead provided by a timer service (or daemon) task."

**5b. 回调在 daemon 任务上下文执行，绝不能阻塞** — CONFIRMED
- https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers
- 引："Timer callback functions execute in the context of the timer service task. It is therefore essential that timer callback functions never attempt to block."（下句："a timer callback function must not call vTaskDelay(), vTaskDelayUntil(), or specify a non zero block time …"）

### 6. 空闲任务负责释放已删除任务的内存，不能被饿死

**6a. 空闲任务释放已删除任务的 TCB/栈；用 vTaskDelete() 时必须保证空闲任务有运行机会** — CONFIRMED
- https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/15-Idle-task
- 引："The idle task is responsible for freeing memory allocated by the RTOS to tasks that have since been deleted."
- 引："It is therefore important in applications that make use of the vTaskDelete() function to ensure the idle task is not starved of processing time."
- 引："The idle task has no other active functions so can legitimately be starved of microcontroller time under all other conditions."

### 7. MCUboot：secondary 槽的镜像按"test"方式试运行，未被确认则下次回滚

**7a. 写入 secondary 槽的镜像以 test 方式交换并运行，未确认就在下次启动回滚** — CONFIRMED
- https://docs.mcuboot.com/design.html
- 引："BOOT_SWAP_TYPE_TEST : Boot the contents of the secondary slot by swapping images. Unless the swap is made permanent, revert back on the next boot."
- 引："Test image rebooted without being confirmed; the bootloader should revert to the original image currently in the secondary slot"

**7b. 应用必须调用 boot_set_confirmed()/boot_set_confirmed_multi() 才会"转正"；trailer 的 Image OK 字节记录确认状态** — CONFIRMED
- https://raw.githubusercontent.com/mcu-tools/mcuboot/main/boot/bootutil/include/bootutil/bootutil_public.h
- 引："Marks the image with index 0 in the primary slot as confirmed."
- 引（boot_set_pending 的 permanent 参数说明）："only tested once: 0=run image once, then confirm or revert."
- trailer 字段（同 7a 页）："Image OK: A single byte indicating whether the image in this slot has been confirmed as good by the user"

### 8. CRC-32 能检出所有长度 ≤ 32 位的突发错误

**8a. 宽度为 n 的 CRC 能检出所有长度不超过 CRC 宽度 n 的 burst 错误（CRC-32 → ≤ 32 位）** — CONFIRMED
- https://users.ece.cmu.edu/~koopman/roses/dsn04/koopman04_crc_poly_embedded.pdf（Koopman & Chakravarty, DSN 2004，摘要）
- 引："An additional property of interest is burst error detection capability, but all codes we will discuss can detect burst errors up to the size of the CRC width."
- 说明：原文措辞是 "up to the size of the CRC width"，没有逐字写 "length ≤ 32 bits"；IEEE 802.3 用的是该族 32 位多项式（CRC-32/ISO-HDLC, 0x04C11DB7），Koopman 的 32 位表页：https://users.ece.cmu.edu/~koopman/crc/crc32.html

### 9. Cortex-M：MPU 违规触发 MemManage（未使能则升级为 HardFault）

**9a. MPU 不匹配 / 权限违规触发 MemManage fault（优先级可编程）** — CONFIRMED
- https://documentation-service.arm.com/static/5f19da2a20b7cf4bc524d99a（ARM DDI 0439B《Cortex-M4 Technical Reference Manual》§5.1 "About the MPU"，PDF 第 5-2 页）
- 引："MPU mismatches and permission violations invoke the programmable-priority MemManage fault handler."

**9b. 若 MemManage 未使能（或故障处理中再次出错），该故障升级为 HardFault** — CONFIRMED
- https://www.keil.com/appnotes/files/apnt209.pdf（Arm/Keil AN209 "Using Cortex-M3/M4/M7 Fault Exceptions"）
- 引："The HardFault exception is therefore executed in cases where a fault exception is disabled"
- 引（复位后默认关闭）："After reset, these exceptions are disabled and may be enabled in the system or application software using the registers in the System Control Block (SCB)."
- 引（机制名）："This is called priority escalation, and the fault is described as escalated to HardFault."

---
Follow-up 统计（9 条待核事实，共 22 项可单独计数的事实点）：**CONFIRMED 21 项**，**PARTIALLY CONFIRMED 1 项**（1a：F4 HAL 的 "How to use this driver" 注释块里没有 "IWDG counter clock Frequency = LsiFreq / Prescaler" / "Counter Reload Value = ..." 这两行原文，只有等价的 LSI、预分频、重装值描述，已逐字引用替代内容），**UNCONFIRMED 0 项**。

---

## Follow-up 2

核查日期：2026-11-18。规则同上（一句英文事实 + source URL + <25 词逐字引用；源码注释算引用）。

### 1. FreeRTOS 栈溢出检查：method 1 / method 2 的内核注释

**1a. 该检查发生在任务被换出（swapped out）时，针对"当前已溢出或看起来曾经溢出"的栈** — CONFIRMED
- https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/stack_macros.h（L32-43 文件头注释）
- 引："Call the stack overflow hook function if the stack of the task being swapped out is currently overflowed"
- 引："Setting configCHECK_FOR_STACK_OVERFLOW to 1 will cause the macro to check the current stack state only"

**1b. Method 1 只比较"当前栈顶是否越过栈界限"** — CONFIRMED
- 同文件，`#if ( ( configCHECK_FOR_STACK_OVERFLOW == 1 ) && ( portSTACK_GROWTH < 0 ) …)` 分支（L67-81），条件前面还有注释 "Only the current stack state is to be checked."
- 引（宏内注释）："/* Is the currently saved stack pointer within the stack limit? */"
- 引（判定）："`if( pxCurrentTCB->pxTopOfStack <= pxCurrentTCB->pxStack + portSTACK_LIMIT_PADDING )`" → 命中即调 `vApplicationStackOverflowHook()`

**1c. Method 2 额外检查栈低端若干个"填充字"是否仍是 0xA5A5A5A5（4 个字 = 16 字节）** — CONFIRMED
- 同文件，`#if ( ( configCHECK_FOR_STACK_OVERFLOW > 1 ) && ( portSTACK_GROWTH < 0 ) …)` 分支（L101-120）
- 引："`const uint32_t ulCheckValue = ( uint32_t ) 0xa5a5a5a5U;`"
- 引（逐个比较前 4 个字）："`( pulStack[ 0 ] != ulCheckValue ) || ( pulStack[ 1 ] != ulCheckValue )` …"（到 `pulStack[ 3 ]`，即 4×4 = 16 字节）
- 文件头注释同义："will also cause the last few stack bytes to be checked to ensure the value to which the bytes were set when the task was created have not been overwritten"

**1d. 官方注释明确 method 2 也不能保证抓到所有溢出** — CONFIRMED
- 同文件头注释收尾："Note this second test does not guarantee that an overflowed stack will always be recognised."

### 2. Xenomai：双内核（dual kernel / co-kernel）与 Linux 并行

**2a. Xenomai 3 可 "side-by-side" 与 Linux 组成双内核系统；双内核核代号 Cobalt（原生版为 Mercury）** — CONFIRMED（一手：官方文档站）
- https://v3.xenomai.org/overview/
- 引："Xenomai 3 is a real-time framework which can run seamlessly side-by-side Linux as a dual kernel system"
- 引："The dual kernel core is codenamed Cobalt , the native Linux implementation is called Mercury ."
- 引（Cobalt 的定位）："By supplementing Linux with a real-time core running side-by-side with it."；"This small extension named Cobalt is built into the Linux kernel"

**2b. Xenomai 4（EVL）同样是"dual kernel"架构，靠 Dovetail 接口把高优先级实时核挂到主内核上** — CONFIRMED（一手：EVL 项目官方文档）
- https://evlproject.org/core/
- 引："the Xenomai 4 project introduces a simple, scalable and dependable dual kernel architecture for Linux"
- 引："based on the Dovetail interface for coupling a high-priority software core to the main kernel"

### 3. Linux 实时应用：RT 关键路径里不要做动态内存分配

**3a. 实时线程应避免在 RT 关键路径中 malloc/free，应在进入 RT 关键路径前预分配并锁定内存** — CONFIRMED（一手：Linux Foundation Real-Time Linux wiki；因 Cloudflare 拦截，正文取自 Wayback 存档 `web/20250106054840`）
- https://web.archive.org/web/20250106054840/https://wiki.linuxfoundation.org/realtime/documentation/howto/applications/memory （原页 https://wiki.linuxfoundation.org/realtime/documentation/howto/applications/memory 对本环境返回 403/Cloudflare 校验页）
- 引："Real-time threads should avoid doing dynamic memory allocation / freeing while in RT critical path."
- 引："the suggested recommendation for real-time threads, is to do the allocations, prior-to entering RT critical path"

**3b. 配套原因与做法：尽早 mlockall，避免在 RT 关键路径产生缺页** — CONFIRMED（同一存档页）
- 引："Real-time applications should use memory-locking APIs early in their life, prior to performing real-time activities, so as to not incur page-faults in RT critical path."
- 旁证（Bootlin PREEMPT_RT 培训幻灯片，二手但有出处）：https://bootlin.com/doc/training/preempt-rt/preempt-rt-slides.pdf — 引："Each page fault will raise an exception, preempt the process and introduce latency"；"Programs should first access all pages to populate the page-table, then pin them with mlockall()"

---
Follow-up 2 统计（3 条待核事实，拆成 8 节）：**CONFIRMED 8 节**，**PARTIALLY CONFIRMED 0 节**，**UNCONFIRMED 0 节**。唯一取证瑕疵：3a/3b 的原文页面被 Cloudflare 挡住，正文取自 2025-01-06 的 Wayback 快照（内容与官方 wiki 一致，页面标题 "Memory for Real-time Applications"）。
