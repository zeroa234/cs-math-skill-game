<!-- pi 子代理 2026-11-18 为 H.3.2 查证的一手出处与逐字引文；写课时只用了标为 CONFIRMED 的说法。 -->
# H.3.2 Linux 嵌入式/实时 — 事实核查报告（一手来源）

核查方式：只用一手文档（docs.kernel.org / kernel.org / docs.u-boot.org / devicetree-specification / man7.org / trustedfirmware-a.readthedocs.io / uefi.org / lwn.net）。
每条：**结论 — 事实句 — 来源 URL — 原文引文（<25 词）**。凡无法用一手来源原文确认者标 **UNCONFIRMED**，并说明实际找到什么。

---

## A. 启动链

**1. [CONFIRMED]** U-Boot SPL 的作用是初始化 DRAM 并加载完整 U-Boot。
- https://docs.u-boot.org/en/latest/develop/spl.html
- "SPL: Secondary program loader. Sets up SDRAM and loads U-Boot proper."

**1b. [CONFIRMED]** TPL 是最早阶段，负责加载 SPL（串起 ROM→TPL→SPL→U-Boot 的链条）。
- https://docs.u-boot.org/en/latest/develop/spl.html
- "TPL: Very early init, as tiny as possible. This loads SPL (or VPL if enabled)."

**1c. [UNCONFIRMED]** “片上 ROM code 把一级 loader 载入内部 SRAM”这一具体表述。
- 实际找到：U-Boot xPL 文档只说到 SPL 在 SRAM/早期环境运行、设置 SDRAM 并加载 U-Boot proper，未出现 “on-chip ROM code 载入 SPL 到 internal SRAM” 的原文；Bootlin 培训 PDF 本次未能机读抽取（PDF 抓取失败），故不作确认。

**2. [CONFIRMED]** TF-A 的 AArch64 冷启动阶段名为 BL1、BL2、BL31、BL32（可选）、BL33。
- https://trustedfirmware-a.readthedocs.io/en/latest/design/firmware-design.html
- "Boot Loader stage 1 (BL1) AP Trusted ROM … Boot Loader stage 2 (BL2) Trusted Boot Firmware"

**2b. [CONFIRMED]** BL31 是 EL3 运行时固件。
- https://trustedfirmware-a.readthedocs.io/en/latest/design/firmware-design.html
- "Boot Loader stage 3-1 (BL31) *EL3 Runtime Software*"

**2c. [CONFIRMED]** BL33 是非可信固件（如 U-Boot）。
- https://trustedfirmware-a.readthedocs.io/en/latest/design/firmware-design.html
- "Boot Loader stage 3-3 (BL33) *Non-trusted Firmware*"

**2d. [CONFIRMED]** U-Boot SPL 可以启动 BL31，再由 BL31 把主 U-Boot 当作 BL33 启动。
- https://docs.u-boot.org/en/latest/develop/spl.html
- "Launching BL31 of ARM Trusted Firmware which invokes main U-Boot as BL33"

**3a. [CONFIRMED]** UEFI 从 EFI System Partition 加载 EFI 可执行文件（须为 `.efi` 扩展名）。
- https://docs.kernel.org/admin-guide/efi-stub.html
- "must be copied to the EFI System Partition (ESP) and renamed with the extension “.efi”"

**3b. [UNCONFIRMED]** “ESP 是 FAT 文件系统”这一点。
- 实际找到：kernel EFI stub 文档只说文件必须在 ESP 上、EFI 固件不支持普通 Linux 文件系统（"EFI firmware doesn’t have support for them"），未见 “ESP 使用 FAT” 原文（该定义在 UEFI spec 的 ESP 章节，本次未抓取该页）。

**3c. [UNCONFIRMED]** “传统 BIOS 读取 MBR（前 512 字节扇区）”这一点。
- 实际找到：docs.kernel.org/arch/x86/boot.html 只提到 “kernel real-mode block (boot sector, setup, and stack/heap)”，未给出 BIOS 读 MBR/512 字节的原文。

**4a. [CONFIRMED]** `printenv` 打印环境变量。
- https://docs.u-boot.org/en/latest/usage/cmd/printenv.html
- "The printenv command is used to print environment or UEFI variables."

**4b. [CONFIRMED]** `setenv`（=`env set`）设置变量，`saveenv`（=`env save`）写入持久存储。
- https://docs.u-boot.org/en/latest/usage/environment.html
- "Environment variables are set using “env set” (alias “setenv”), printed using “env print”"

**4b2. [CONFIRMED]** `saveenv` 保存到持久存储。
- https://docs.u-boot.org/en/latest/usage/environment.html
- "saved to persistent storage using “env save” (alias “saveenv”)"

**4c. [CONFIRMED]** `bootcmd` 是开机延时结束后自动执行的命令。
- https://docs.u-boot.org/en/latest/usage/environment.html
- "The command that is run if the user does not enter the shell during the boot delay."

**4d. [CONFIRMED]** `bootargs` 是传给被启动 OS 的命令行。
- https://docs.u-boot.org/en/latest/usage/environment.html
- "Command line arguments passed when booting an operating system or binary image"

**4e. [CONFIRMED]** `bootz` 启动 zImage 格式内核。
- https://docs.u-boot.org/en/latest/usage/cmd/bootz.html
- "The bootz command is used to boot a Linux kernel in ‘zImage’ format."

**4f. [CONFIRMED]** `booti` 启动 arm64 的 flat（或压缩）Image。
- https://docs.u-boot.org/en/latest/usage/cmd/booti.html
- "The booti command is used to boot a Linux kernel in flat or compressed ‘Image’ format."

**4g. [CONFIRMED]** `bootm` 启动 OS 镜像，支持 FIT（推荐）与传统 legacy uImage。
- https://docs.u-boot.org/en/latest/usage/cmd/bootm.html
- "U-Boot supports a legacy image format, enabled by CONFIG_LEGACY_IMAGE_FORMAT."

**4h. [CONFIRMED]** `load` 从文件系统读文件进内存（`fatload` 是 FAT 专用封装）。
- https://docs.u-boot.org/en/latest/usage/cmd/load.html
- "The load command is used to read a file from a filesystem into memory."

**4h2. [CONFIRMED]** `fatload` 从 FAT 文件系统读文件；结果字节数存入 `filesize`。
- https://docs.u-boot.org/en/latest/usage/cmd/fatload.html
- "The number of transferred bytes is saved in the environment variable filesize."

**4h3. [UNCONFIRMED]** `ext4load` 这个命令名。
- 实际找到：`/usage/cmd/ext4load.html` 为 404；文档只有通用 `load` 与 `fatload` 页，未见 `ext4load` 页面。建议写作 “`load`（`ext4`/`fat` 等接口）”。

**4i. [CONFIRMED]** 网络加载命令名是 `tftpboot`（tftp 引导）。
- https://docs.u-boot.org/en/latest/usage/environment.html
- "tftpboot - boot image via network using TFTP protocol"

**4j. [CONFIRMED]** `fdt addr` 设置工作 FDT 的地址（无参则显示）。
- https://docs.u-boot.org/en/latest/usage/cmd/fdt.html
- "If the addr argument is provided, then this sets the address of the working or control FDT"

**4k. [CONFIRMED]** distro boot 在启动分区上找 `/extlinux/extlinux.conf`（或 `/boot/extlinux/extlinux.conf`）。
- https://docs.u-boot.org/en/latest/develop/distro.html
- "U-Boot searches for /extlinux/extlinux.conf then /boot/extlinux/extlinux.conf on disk"

**4l. [CONFIRMED]** distro boot 也支持 `boot.scr` 脚本作为启动配置。
- https://docs.u-boot.org/en/latest/develop/distro.html
- "enables distros to generate a U-Boot-specific boot.scr script rather than extlinux.conf"

**4m. [CONFIRMED]** 新的 standard boot（bootstd）是 distro boot 的泛化/替代。
- https://docs.u-boot.org/en/latest/develop/bootstd/overview.html
- "Standard boot is a generalisation of distro boot."

**5a. [CONFIRMED]** `root=` 指定用作根文件系统的设备。
- https://man7.org/linux/man-pages/man7/bootparam.7.html
- "This argument tells the kernel what device is to be used as the root filesystem"

**5b. [CONFIRMED]** `init=` 指定内核执行的第一个程序；缺省/失败时依次尝试 `/sbin/init` 等。
- https://man7.org/linux/man-pages/man7/bootparam.7.html
- "the kernel will try /sbin/init, then /etc/init, then /bin/init, then /bin/sh"

**5c. [CONFIRMED]** 未被内核消费的命令行参数会传给 PID 1（通常是 init）。
- https://man7.org/linux/man-pages/man7/bootparam.7.html
- "are then passed onto PID 1, which is usually the init(1) program"

**5d. [UNCONFIRMED]** “先挂载根文件系统、再以 PID 1 运行 init”的先后顺序原文。
- 实际找到：admin-guide/init.html 只说 rootfs 挂载失败或 `root=` 指向错误分区会导致 “No working init found”，未给出顺序句式。

---

## B. 设备树与 pinctrl

**6a. [CONFIRMED]** .dts 由 dtc 编译为二进制 DTB。
- https://devicetree-specification.readthedocs.io/en/latest/chapter2-devicetree-basics.html
- "The DTC tool automatically inserts the phandle properties when the DTS is compiled into the binary DTB format."

**6b. [CONFIRMED]** 32 位 ARM 上 bootloader 通过 r2 传 DTB 物理地址。
- https://docs.kernel.org/arch/arm/booting.html
- "The physical address of the boot data is passed to the kernel in register r2."

**6c. [CONFIRMED]** arm64 上通过 x0 传 DTB 物理地址。
- https://docs.kernel.org/arch/arm64/booting.html
- "x0 = physical address of device tree blob (dtb) in system RAM."

**7a. [CONFIRMED]** `compatible` 是驱动选择用的字符串列表（最具体→最通用）。
- https://devicetree-specification.readthedocs.io/en/latest/chapter2-devicetree-basics.html
- "This list of strings should be used by a client program for device driver selection."

**7b. [CONFIRMED]** `reg` 给出设备在其父总线地址空间中的地址与长度。
- https://devicetree-specification.readthedocs.io/en/latest/chapter2-devicetree-basics.html
- "The reg property describes the address of the device’s resources within the address space defined by its parent bus."

**7c. [CONFIRMED]** `interrupts` 描述该设备的一个或多个中断源（配合 interrupt-parent）。
- https://devicetree-specification.readthedocs.io/en/latest/chapter2-devicetree-basics.html
- "Each interrupt generating device contains an interrupts property with a value describing one or more interrupt sources"

**7d. [CONFIRMED]** `status` 取 "okay"/"disabled" 等值；缺省视作 "okay"。
- https://devicetree-specification.readthedocs.io/en/latest/chapter2-devicetree-basics.html
- "The lack of a status property should be treated as if the property existed with the value of “okay”."

**7e. [CONFIRMED]** `#address-cells`/`#size-cells` 定义子节点 reg 中地址/长度各占几个 cell。
- https://devicetree-specification.readthedocs.io/en/latest/chapter2-devicetree-basics.html
- "The #address-cells property defines the number of cells used to encode the address field"

**7f. [UNCONFIRMED]** “compatible 与驱动的 `of_match_table` 匹配”这一具体字段名。
- 实际找到：docs.kernel.org/driver-api/driver-model/platform.html 只说绑定在 device/driver 匹配后调用 probe（"invoking driver probe() after finding a match between device and driver"），未出现 `of_match_table` 原文。

**8a. [CONFIRMED]** pinctrl 客户端绑定用 `pinctrl-names` + `pinctrl-0 = <&state>` 映射状态。
- https://www.kernel.org/doc/Documentation/devicetree/bindings/pinctrl/pinctrl-bindings.txt
- "pinctrl-names: The list of names to assign states. List entry 0 defines the name for integer state ID 0"

**8b. [UNCONFIRMED]** “pinctrl core 在 probe 之前自动应用 default 状态”这一点。
- 实际找到：docs.kernel.org/driver-api/pin-control.html 只描述状态/映射机制与 pinmux 约定，未出现 “default state is applied before probe” 的原文。

**9. [CONFIRMED]** 设备树 overlay 用于在运行时修改（活动的）设备树，从而支持附加板卡/新节点。
- https://docs.kernel.org/devicetree/overlay-notes.html
- "A Devicetree’s overlay purpose is to modify the kernel’s live tree"

**9b. [UNCONFIRMED]** `.dtbo` 这个文件扩展名。
- 实际找到：overlay-notes 只出现 `bar.dtso` 源文件示例与 of_overlay_fdt_apply()，未见 `.dtbo` 扩展名原文。

---

## C. 内核模块与驱动

**10a. [CONFIRMED]** `insmod` 直接插入一个模块（不解析依赖，推荐用 modprobe）。
- https://man7.org/linux/man-pages/man8/insmod.8.html
- "insmod is a trivial program to insert a module into the kernel."

**10b. [CONFIRMED]** `modprobe` 可加载/卸载模块，并能处理依赖。
- https://man7.org/linux/man-pages/man8/modprobe.8.html
- "modprobe intelligently adds or removes a module from the Linux kernel"

**10c. [CONFIRMED]** `depmod` 生成 `modules.dep`（模块依赖表）。
- https://man7.org/linux/man-pages/man8/depmod.8.html
- "depmod creates a list of module dependencies by reading each module … This list is written to modules.dep"

**10d. [CONFIRMED]** `lsmod` 显示当前已加载模块（格式化 /proc/modules）。
- https://man7.org/linux/man-pages/man8/lsmod.8.html
- "showing what kernel modules are currently loaded"

**10e. [CONFIRMED]** `dmesg` 读取/控制内核环形缓冲区，即 printk 的输出。
- https://man7.org/linux/man-pages/man1/dmesg.1.html
- "dmesg is used to examine or control the kernel ring buffer."

**10f. [UNCONFIRMED]** `module_init` / `module_exit` / `MODULE_LICENSE` 宏的一手文档说明。
- 实际找到：本轮抓取的 kernel-hacking/hacking.html 未覆盖这些宏；未找到 docs.kernel.org 上对应的说明段落。

**10g. [UNCONFIRMED]** `rmmod` 命令页。
- 实际找到：仅从 insmod(8) 的 SEE ALSO 见到 rmmod 名称（"modprobe(8), rmmod(8), lsmod(8)"），未抓取其正文。

**11a. [CONFIRMED]** 树外模块构建命令是 `make -C $KDIR M=$PWD`。
- https://docs.kernel.org/kbuild/modules.html
- "make -C $KDIR M=$PWD"

**11b. [CONFIRMED]** 树外模块用 Kbuild/Makefile 的 `obj-m` 一行声明要构建的模块。
- https://docs.kernel.org/kbuild/modules.html
- "The file may be as simple as a single line … The kbuild system will build .o from .c"

**11c. [CONFIRMED]** 内核配置项由 Kconfig 语言的 `config` 条目定义。
- https://docs.kernel.org/kbuild/kconfig-language.html
- "“config” starts a new config entry."

**11d. [UNCONFIRMED]** 树内 `obj-$(CONFIG_FOO) += foo.o` 写法原文。
- 实际找到：kbuild/modules.html 只涉树外模块；未抓取 kbuild/makefiles.html 的 `obj-$(CONFIG_...)` 段落。

**12a. [CONFIRMED]** 内核代码默认不能用浮点（需定点运算）。
- https://docs.kernel.org/kernel-hacking/hacking.html
- "No floating point or MMX … It is generally a bad idea; use fixed point arithmetic first."

**12b. [CONFIRMED]** 内核栈很小（32 位约 3K–6K，64 位约 14K），要避免深递归与大局部数组。
- https://docs.kernel.org/kernel-hacking/hacking.html
- "the kernel stack is about 3K to 6K for most 32-bit architectures: it’s about 14K on most 64-bit archs"

**12c. [CONFIRMED]** 睡眠锁只能在可抢占的任务上下文获取（即原子上下文不能睡）。
- https://docs.kernel.org/locking/locktypes.html
- "Sleeping locks can only be acquired in preemptible task context."

**12d. [UNCONFIRMED]** “内核没有 libc / 不能用 printf”的原文。
- 实际找到：kernel-hacking/hacking.html 有 “No memory protection”“No floating point or MMX”“A rigid stack limit” 三条，但本轮抽取文本中未见 “no libc/printf” 段落。

**13. [UNCONFIRMED]** `alloc_chrdev_region`/`cdev_init`/`cdev_add`/`file_operations` 的字段清单，以及 `copy_to_user` 返回“未拷贝字节数、成功为 0”。
- 实际找到：本轮未取得字符设备驱动的官方文档页（docs.kernel.org 无 driver-api/cdev.html）；kernel-api.html 体量过大未能命中该函数说明。**不能凭印象确认。**

**14a. [CONFIRMED]** platform 驱动提供 `probe()`/`remove()`，由驱动核心在匹配到设备后调用。
- https://docs.kernel.org/driver-api/driver-model/platform.html
- "drivers provide probe() and remove() methods"

**14b. [CONFIRMED]** 绑定发生在 device/driver 匹配之后（内含 probe 调用）。
- https://docs.kernel.org/driver-api/driver-model/platform.html
- "invoking driver probe() after finding a match between device and driver"

**14c. [CONFIRMED]** devm_* 托管资源在驱动 detach 时自动释放。
- https://docs.kernel.org/driver-api/driver-model/devres.html
- "No matter what, all devres entries are released on driver detach."

**15a. [CONFIRMED]** LED 通过 `/sys/class/leds/` 下的 `brightness` 文件控制，取值 0..max_brightness。
- https://docs.kernel.org/leds/leds-class.html
- "LEDs appear in /sys/class/leds/. The maximum brightness of the LED is defined in max_brightness file."

**15b. [CONFIRMED]** 旧的 `/sys/class/gpio` sysfs 接口已废弃，新代码应用 GPIO 字符设备 API。
- https://docs.kernel.org/userspace-api/gpio/sysfs.html
- "This API is obsoleted by the GPIO Character Device Userspace API"

**15c. [CONFIRMED]** GPIO 字符设备是 `/dev/gpiochipX`。
- https://docs.kernel.org/userspace-api/gpio/chardev.html
- "The Chip represents a single GPIO chip and is exposed to userspace using device files of the form /dev/gpiochipX."

**15d. [UNCONFIRMED]** libgpiod 工具名 `gpiodetect` / `gpioget` / `gpioset`。
- 实际找到：docs.kernel.org/tools/gpio-tools.html 为 404；chardev 页只提到 “Basic examples … can be found in tools/gpio/*”，未列这三个工具名。

**15e. [UNCONFIRMED]** “网络接口不出现在 /dev 下”。
- 实际找到：未找到任何一手文档原文表述。

---

## D. 中断、锁、内存

**16a. [CONFIRMED]** `request_irq()` 注册的中断处理函数在 PREEMPT_RT 下作为线程化 handler 运行（第二级）。
- https://docs.kernel.org/core-api/real-time/theory.html
- "the threaded handler, is the function passed to request_irq() as the interrupt handler"

**16b. [UNCONFIRMED]** `request_irq` / `request_threaded_irq` 的参数含义，以及返回值 `IRQ_HANDLED` / `IRQ_NONE` / `IRQ_WAKE_THREAD` 的语义。
- 实际找到：genericirq.html 抽取部分只列高层 API 与 flow handler，未出现这三个返回值的原文定义。

**16c. [CONFIRMED]** 延迟工作手段包括 softirq、tasklet、workqueue，以及线程化中断。
- https://docs.kernel.org/kernel-hacking/hacking.html
- "tasklets (include/linux/interrupt.h) are more often used"

**16d. [CONFIRMED]** workqueue 也支持 BH（softirq 上下文）workqueue。
- https://docs.kernel.org/core-api/workqueue.html
- "A BH workqueue can be considered a convenience interface to softirq."

**16e. [UNCONFIRMED]** “tasklet 正在被废弃、改用 workqueue/BH workqueue”的官方表述。
- 实际找到：workqueue 文档只说明 BH workqueue 与 softirq 的关系，未出现 “tasklets are deprecated/being removed” 原句；未检索到相应段落。

**17a. [CONFIRMED]** PREEMPT_RT 下 `spinlock_t` 被转换成睡眠锁。
- https://docs.kernel.org/locking/locktypes.html
- "On PREEMPT_RT kernels, these lock types are converted to sleeping locks: … spinlock_t"

**17b. [CONFIRMED]** `raw_spinlock_t` 在任何配置下都是自旋锁。
- https://docs.kernel.org/locking/locktypes.html
- "Spinning locks: raw_spinlock_t; bit spinlocks"

**17c. [CONFIRMED]** 自旋锁隐式关抢占，`_irqsave` 会保存并关闭本地中断，`_bh` 关下半部。
- https://docs.kernel.org/locking/locktypes.html
- "_irqsave/restore() Save and disable / restore interrupt disabled state"

**17d. [CONFIRMED]** mutex 等睡眠锁只能在可抢占任务上下文使用（不能在中断上下文用）。
- https://docs.kernel.org/locking/locktypes.html
- "Sleeping locks can only be acquired in preemptible task context."

**17e. [CONFIRMED]** `atomic_*()` 操作是原子的（同一 CPU 上按程序序执行）。
- https://docs.kernel.org/core-api/refcount-vs-atomic.html
- "each atomic_*() and refcount_*() operation is atomic and instructions are executed in program order"

**17f. [CONFIRMED]** lockdep 是 “runtime locking correctness validator”，能发现反向获取顺序导致的死锁。
- https://docs.kernel.org/locking/lockdep-design.html
- "Runtime locking correctness validator … The validator will find such dependency circle in arbitrary complexity"

**17g. [CONFIRMED]** lockdep 报告会指出“两把锁不能以相反顺序获取”（AB-BA）。
- https://docs.kernel.org/locking/lockdep-design.html
- "Furthermore, two locks can not be taken in inverse order … referred to as lock inversion deadlock"

**17h. [CONFIRMED]** CONFIG_PROVE_LOCKING 是影响实时最坏延迟的调试选项之一。
- https://docs.kernel.org/core-api/real-time/kernel-configuration.html
- "CONFIG_PROVE_LOCKING"（原文为该页 "Kernel Debug Options" 下的小节标题，非句子）

**18a. [CONFIRMED]** kmalloc 总是分配物理连续内存，最大单块受 `KMALLOC_MAX_SIZE` 限制。
- https://docs.kernel.org/core-api/memory-allocation.html
- "kmalloc always allocates physically contiguous memory and the maximal size of a chunk that can be allocated with kmalloc is limited by KMALLOC_MAX_SIZE"

**18b. [CONFIRMED]** GFP_KERNEL 可能触发直接回收，因此调用上下文必须允许睡眠。
- https://docs.kernel.org/core-api/memory-allocation.html
- "using GFP_KERNEL implies GFP_RECLAIM … the calling context must be allowed to sleep"

**18c. [CONFIRMED]** GFP_ATOMIC 是不睡眠的分配，常用于中断/下半部上下文。
- https://docs.kernel.org/core-api/memory-allocation.html
- "(aka GFP_ATOMIC) - non sleeping allocation with an expensive fallback"

**18d. [CONFIRMED]** vmalloc 的内存不是物理连续的。
- https://docs.kernel.org/core-api/memory-allocation.html
- "The memory allocated by vmalloc and related functions is not physically contiguous."

**18e. [UNCONFIRMED]** “vmalloc 可能睡眠、更慢”。
- 实际找到：上述文档只说明非物理连续，并建议大分配/不确定大小时用 kvmalloc；未出现 “vmalloc may sleep / slower” 原文。

**18f. [UNCONFIRMED]** `alloc_pages` / `__get_free_pages(order)` 分配 2^order 个页。
- 实际找到：文档只说可直接向页分配器申请页（"directly request pages from the page allocator with alloc_pages"），未出现 2^order 的表述。

**19a. [CONFIRMED]** printk 有 0–7 级日志等级，KERN_ERR=3、KERN_INFO=6 等，并有 pr_err/pr_info 别名。
- https://docs.kernel.org/core-api/printk-basics.html
- 表格逐行给出等级/字符串/别名，如 "KERN_INFO “6” pr_info()"（0–7 共 8 级，KERN_ERR=3）

**19b. [CONFIRMED]** printk 消息进入内核环形缓冲区，通常用 dmesg 读取。
- https://docs.kernel.org/core-api/printk-basics.html
- "The usual way to read it is using dmesg."

**19c. [CONFIRMED]** dynamic debug 通过 `/proc/dynamic_debug/control` 动态开关 pr_debug。
- https://docs.kernel.org/admin-guide/dynamic-debug-howto.html
- "If /proc/dynamic_debug/control exists, your kernel has dynamic debug."

**19d. [CONFIRMED]** debugfs 通常挂载在 `/sys/kernel/debug`。
- https://docs.kernel.org/admin-guide/dynamic-debug-howto.html
- "dynamic_debug/control is also under the mount-dir, typically /sys/kernel/debug/"

**19e. [UNCONFIRMED]** “Oops 消息包含寄存器、调用栈（Call Trace）”。
- 实际找到：bug-hunting.html 说明 Oops 是栈回溯、可由 EIP/函数偏移定位（"you can simply copy the EIP value from the OOPS"），但抽取正文中未出现 “registers / Call Trace” 字样（示例块未被抽取）。

**19f. [CONFIRMED]** kgdb 可经单个串口（kgdboc）与 gdb 联调。
- https://docs.kernel.org/process/debugging/kgdb.html
- "For kgdb/gdb, kgdboc is designed to work with a single serial port."

**19g. [CONFIRMED]** Magic SysRq：`b` 立即重启，`c` 触发 crash（可留 crashdump）。
- https://docs.kernel.org/admin-guide/sysrq.html
- "b Will immediately reboot the system without syncing or unmounting your disks."

**19h. [CONFIRMED]** `t` 打印当前任务列表；`/proc/sysrq-trigger` 总是可用，`/proc/sys/kernel/sysrq` 控制键盘触发权限。
- https://docs.kernel.org/admin-guide/sysrq.html
- "Invocation of any operation via /proc/sysrq-trigger is always allowed"

**20a. [CONFIRMED]** cpufreq 有 performance / powersave 等 governor（实时系统建议固定频率）。
- https://docs.kernel.org/core-api/real-time/kernel-configuration.html
- "If a low CPU frequency is desired, then CONFIG_CPU_FREQ_DEFAULT_GOV_POWERSAVE can be set."

**20b. [UNCONFIRMED]** `schedutil` governor 名称与其定位。
- 实际找到：实时配置文档谈 performance/powersave/userspace/ondemand，未提 schedutil；cpufreq.html 抽取部分未含 governor 清单。

**20c. [CONFIRMED]** cpuidle 的 C-states 是 CPU 低功耗空闲状态。
- https://docs.kernel.org/core-api/real-time/kernel-configuration.html
- "CPU idle states (C-states) allow the processor to enter low-power modes during periods of inactivity."

**20d. [CONFIRMED]** 存在 runtime PM 框架（dev_pm_ops 的三个 runtime 回调）。
- https://docs.kernel.org/power/runtime_pm.html
- "There are three device runtime PM callbacks defined in ‘struct dev_pm_ops’"

**20e. [UNCONFIRMED]** `pm_runtime_get_sync()` / `pm_runtime_put()` 这两个函数名。
- 实际找到：runtime_pm.html 抽取部分未含第 4 节的 helper 函数清单原文。

**20f. [UNCONFIRMED]** `/sys/power/state` 写入 `mem` 表示 suspend-to-RAM。
- 实际找到：sleep-states.html 只描述 Suspend-to-RAM(STR/S2RAM) 语义与 CONFIG_SUSPEND，未出现 `/sys/power/state` 与 `mem` 字样的原文片段。

**20g. [CONFIRMED]** regulator 框架提供控制电压/电流调节器的标准内核接口。
- https://docs.kernel.org/driver-api/regulator.html
- "This framework is designed to provide a standard kernel interface to control voltage and current regulators."

**20h. [CONFIRMED]** 存在 common clk framework 用于时钟节点控制。
- https://docs.kernel.org/driver-api/clk.html
- "The common clk framework is an interface to control the clock nodes available on various devices today."

**20i. [UNCONFIRMED]** `clk_prepare_enable()` 函数名。
- 实际找到：clk.html 抽取部分只到引言，未含该 API 名。

---

## E. 实时 Linux

**21. [CONFIRMED]** PREEMPT_RT 在 Linux 6.12（2024-11 发布）合入主线。
- https://lwn.net/Articles/997958
- "Headline features in this release include: … the last pieces of realtime preemption support"（Posted November 17, 2024）

**22. [UNCONFIRMED]** Kconfig 中四个抢占模型及其菜单文字（PREEMPT_NONE “No Forced Preemption (Server)” 等）。
- 实际找到：`git.kernel.org/.../plain/init/Kconfig?h=v6.12` 抓取失败（Error fetching content）；未找到其他一手页面列出这四个菜单字符串。

**23a. [CONFIRMED]** PREEMPT_RT 把 spinlock_t 换成可抢占、带优先级继承的 rtmutex。
- https://docs.kernel.org/core-api/real-time/theory.html
- "replacing locking primitives, such as spinlock_t, with a preemptible and priority-inheritance aware implementation known as rtmutex"

**23b. [CONFIRMED]** PREEMPT_RT 强制中断线程化：主 handler 只唤醒线程，其余在进程上下文运行。
- https://docs.kernel.org/core-api/real-time/theory.html
- "the primary handler … Its sole responsibility is to wake the associated threaded handler."

**23c. [CONFIRMED]** PREEMPT_RT 下 rtmutex（含 spinlock_t/mutex）提供优先级继承。
- https://docs.kernel.org/core-api/real-time/theory.html
- "spinlock_t and mutex_t in a PREEMPT_RT enabled kernel are implemented on top of rtmutex, which provides support for priority inheritance"

**24a. [CONFIRMED]** SCHED_FIFO / SCHED_RR 的静态优先级范围是 1（低）到 99（高）。
- https://man7.org/linux/man-pages/man7/sched.7.html
- "have a sched_priority value in the range 1 (low) to 99 (high)"

**24b. [UNCONFIRMED]** “SCHED_RR 默认时间片 100 ms（sched_rr_timeslice_ms）”。
- 实际找到：sched_rr_get_interval(2) 与 sched(7) 抓取到的正文为空/无该句；未确认 100 ms 默认值。

**24c. [CONFIRMED]** SCHED_DEADLINE 参数关系为 runtime ≤ deadline ≤ period，用 sched_setattr 设置。
- https://man7.org/linux/man-pages/man1/chrt.1.html
- "The relation between the options required by the kernel is runtime ⇐ deadline ⇐ period."

**24d. [CONFIRMED]** chrt 可通过 `-f` 设 SCHED_FIFO 并带优先级运行命令。
- https://man7.org/linux/man-pages/man1/chrt.1.html
- "chrt [options] [priority] command [argument...]"（`-f, --fifo` 选项）

**25a. [CONFIRMED]** `isolcpus=` 启动参数可把 CPU 从调度域隔离。
- https://docs.kernel.org/admin-guide/cpu-isolation.html
- "The ‘isolcpus=’ kernel boot parameter with the ‘domain’ flag"

**25b. [CONFIRMED]** IRQ 亲和性用 `/proc/irq/<N>/smp_affinity`（位掩码）或 `smp_affinity_list`（CPU 列表）。
- https://docs.kernel.org/core-api/irq/irq-affinity.html
- "It’s a bitmask (smp_affinity) or CPU list (smp_affinity_list) of allowed CPUs."

**25c. [CONFIRMED]** `taskset` 设置/查询进程 CPU 亲和性。
- https://man7.org/linux/man-pages/man1/taskset.1.html
- "The taskset command is used to set or retrieve the CPU affinity of a running process"

**26a. [CONFIRMED]** `mlockall(MCL_CURRENT|MCL_FUTURE)` 锁定现有与将来映射的页，避免换页延迟。
- https://man7.org/linux/man-pages/man2/mlock.2.html
- "MCL_FUTURE Lock all pages which will become mapped into the address space of the process in the future."

**26b. [CONFIRMED]** 实时程序应在进入临界区前“预热”栈页，避免缺页。
- https://man7.org/linux/man-pages/man2/mlock.2.html
- "should reserve enough locked stack pages before entering the time-critical section, so that no page fault can be caused"

**26c. [UNCONFIRMED]** “实时循环里避免 malloc”的官方表述。
- 实际找到：mlock(2) 只警告 fork(2) 会引发 COW 缺页（"it is crucial not to invoke fork(2) after an mlockall()"），未直接说避免 malloc。

**26d. [UNCONFIRMED]** cyclictest（rt-tests）测量唤醒延迟。
- 实际找到：man7 无 cyclictest 页；未从一手文档取得该工具说明。

**26e. [CONFIRMED]** 周期循环应用 `clock_nanosleep` 的 `TIMER_ABSTIME` 绝对时间以避免累积漂移。
- https://man7.org/linux/man-pages/man2/clock_nanosleep.2.html
- "Using an absolute timer is useful for preventing timer drift problems"

**27a. [UNCONFIRMED]** `pthread_mutexattr_setprotocol(&attr, PTHREAD_PRIO_INHERIT)`。
- 实际找到：man7 该页两次抓取均为空正文（返回 404 或空内容），无法取得原文引文；未用其他一手来源替代。

**27b. [CONFIRMED]** 要让线程使用 attr 中的调度策略，必须设 `PTHREAD_EXPLICIT_SCHED`（默认是继承创建者）。
- https://man7.org/linux/man-pages/man3/pthread_attr_setinheritsched.3.html
- "PTHREAD_EXPLICIT_SCHED Threads … take their scheduling attributes from the values specified by the attributes object."

**27c. [CONFIRMED]** POSIX 消息队列有 `mq_open` / `mq_send`（接收端 `mq_receive`）。
- https://man7.org/linux/man-pages/man3/mq_open.3.html
- "mq_open() creates a new POSIX message queue or opens an existing queue."

**27d. [CONFIRMED]** `mq_send` 按优先级递减排队，队满默认阻塞。
- https://man7.org/linux/man-pages/man3/mq_send.3.html
- "Messages are placed on the queue in decreasing order of priority"

**27e. [CONFIRMED]** `sigwait` 等待集合中的信号（需先阻塞），成功返回 0 并取出信号号。
- https://man7.org/linux/man-pages/man3/sigwait.3.html
- "For a signal to become pending, it must first be blocked with sigprocmask(2)."

**28a. [UNCONFIRMED]** x86 上 SMI/固件可引起 OS 不可见的延迟。
- 实际找到：docs.kernel.org/core-api/real-time/hardware.html 的 “Firmware” 小节在抽取中被截断（页面 15.7k 字符，仅取到 Networking 之前），未取得 SMI 原文句子。

**28b. [CONFIRMED]** 外设通过 DMA 与 CPU 争用内存/缓存，会影响确定性。
- https://docs.kernel.org/core-api/real-time/hardware.html
- "Memory is used not only by the CPU but also by peripheral devices via DMA"

**28c. [CONFIRMED]** cpuidle 的 `stateN/latency` 属性给出退出该空闲状态的延迟（微秒）。
- https://www.kernel.org/doc/Documentation/ABI/testing/sysfs-devices-system-cpu
- "latency: (RO) The latency to exit out of this idle state (in microseconds)."

**28d. [UNCONFIRMED]** “越深的 C-state 退出延迟越大”的原文表述。
- 实际找到：上述 ABI 文件只给 latency 属性语义；cpuidle.html 抽取部分未含该比较句。

---

## 与原始表述冲突/需修正的地方

1. **内核栈大小不是“8 KB 或 16 KB 固定值”**：kernel-hacking 原文是 “about 3K to 6K for most 32-bit architectures … about 14K on most 64-bit archs”（随配置/架构变化），且常与中断共享。写死 8/16 KB 不准确。
2. **`ext4load`、`tftp`**：U-Boot 官方命令页里分别是通用 `load`（配 `ext4` 接口）与 `tftpboot`；`/usage/cmd/ext4load.html`、`/usage/cmd/tftp.html` 均为 404。写命令名时应写 `load`/`fatload` 与 `tftpboot`。
3. **`.dtbo` / `.dtso`**：kernel overlay 文档示例用 `.dtso`（源）与“base DT 需 `-@` 编译”，未见 `.dtbo` 原文；写扩展名时应注明是工具约定而非该文档用词。
4. **SMI 与 DMA 抖动**：一手 RT 文档确认 DMA 与 CPU 争用缓存/内存会影响确定性；“SMI 造成 OS 不可见延迟”在本轮抓取中未能取到原文，**不要当作已核实事实引用**。
5. **PREEMPT_RT 合入版本**：LWN 的措辞是 6.12 含 “the last pieces of realtime preemption support”，与“6.12 完整合入”一致（2024-11-17 发布），但严格说是“最后部分合入”的表述。

---


---

## Follow-up (kernel source)

本轮改为直接读内核源码（git.kernel.org `plain/`，默认 master）与 Documentation 的 `.rst` 源文件。代码行按约定算作引文。

**F1. [CONFIRMED — 代码语义]** `copy_to_user()` 失败时返回未拷贝的字节数 n，全部成功时返回 0。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/uaccess.h
- "if (!check_copy_size(from, n, true)) return n;"
- 同文件 `_inline_copy_to_user()`：`n = raw_copy_to_user(to, from, n);` 之后 `return n;`（n 为剩余未拷贝字节）；`_inline_copy_from_user()` 显式 `if (likely(!res)) return 0;` … `return res;`。`copy_to_user()` 最后一行是 `return _copy_to_user(to, from, n);`。
- 备注：当前源码已无 “Returns number of bytes that could not be copied.” 这句注释；我查了 include/linux/uaccess.h、lib/usercopy.c（含 v6.6/v5.10/v4.19）与多个 Documentation 候选页，均无该句，故按代码语义确认。

**F2a. [CONFIRMED]** `IRQ_NONE`/`IRQ_HANDLED`/`IRQ_WAKE_THREAD` 的含义写在枚举注释里。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/irqreturn.h
- "@IRQ_WAKE_THREAD:	handler requests to wake the handler thread"

**F2b. [CONFIRMED]** `request_irq()` 是内联封装，转发到 `request_threaded_irq(..., NULL, flags | IRQF_COND_ONESHOT, ...)`。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/interrupt.h
- "return request_threaded_irq(irq, handler, NULL, flags | IRQF_COND_ONESHOT, name, dev);"

**F2c. [CONFIRMED]** `request_threaded_irq` 原型为 (irq, handler, thread_fn, flags, name, dev)。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/interrupt.h
- "request_threaded_irq(unsigned int irq, irq_handler_t handler, irq_handler_t thread_fn, unsigned long flags, const char *name, void *dev);"

**F2d. [CONFIRMED]** `IRQF_SHARED` 允许共享中断线；`IRQF_ONESHOT` 表示硬中断处理完后不重新使能。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/interrupt.h
- "IRQF_ONESHOT - Interrupt is not reenabled after the hardirq handler finished."

**F3a. [CONFIRMED]** `module_init()` 是驱动初始化入口点，`module_exit()` 是清理入口点。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/module.h
- "module_init() - driver initialization entry point"
- 同处：`module_exit() - driver exit entry point`、`#define module_init(x)	__initcall(x);`

**F3b. [CONFIRMED]** `MODULE_LICENSE` 通过 `MODULE_INFO(license, ...)` 记录许可证。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/module.h
- "#define MODULE_LICENSE(_license) MODULE_FILE MODULE_INFO(license, _license)"

**F3c. [CONFIRMED]** `EXPORT_SYMBOL` / `EXPORT_SYMBOL_GPL` 分别导出普通符号与 GPL-only 符号。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/export.h
- "#define EXPORT_SYMBOL_GPL(sym)		_EXPORT_SYMBOL(sym, "GPL")"

**F4a. [CONFIRMED]** `struct device_driver` 有 `of_match_table` 字段。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/device/driver.h
- "const struct of_device_id	*of_match_table;"
- 同处注释：`@of_match_table: The open firmware table.`

**F4b. [CONFIRMED]** `struct file_operations` 含 read/write/poll/unlocked_ioctl/open/release。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/fs.h
- "ssize_t (*read) (struct file *, char __user *, size_t, loff_t *);"
- 同处：`__poll_t (*poll) (struct file *, struct poll_table_struct *);`、`long (*unlocked_ioctl) (struct file *, unsigned int, unsigned long);`、`int (*release) (struct inode *, struct file *);`

**F4c. [CONFIRMED]** `cdev_init` / `cdev_add` 原型。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/cdev.h
- "void cdev_init(struct cdev *, const struct file_operations *);"
- 同处：`int cdev_add(struct cdev *, dev_t, unsigned);`

**F4d. [CONFIRMED]** `alloc_chrdev_region` 原型。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/fs.h
- "extern int alloc_chrdev_region(dev_t *, unsigned, unsigned, const char *);"

**F4e. [CONFIRMED]** `MINORBITS` 为 20，MAJOR/MINOR 由移位与掩码得到。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/kdev_t.h
- "#define MINORBITS	20"
- 同处：`#define MAJOR(dev)	((unsigned int) ((dev) >> MINORBITS))`

**F5. [CONFIRMED，措辞与假设不同]** 四个抢占模型 prompt 原文为 `No Forced Preemption (Server)`、`Voluntary Kernel Preemption (Desktop)`、`Preemptible Kernel (Low-Latency Desktop)`、`Fully Preemptible Kernel (Real-Time)`；另有第五种 `PREEMPT_LAZY`。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/kernel/Kconfig.preempt
- 'bool "No Forced Preemption (Server)"'
- 同处：'bool "Voluntary Kernel Preemption (Desktop)"'、'bool "Preemptible Kernel (Low-Latency Desktop)"'、'bool "Fully Preemptible Kernel (Real-Time)"'、'bool "Scheduler controlled preemption model"'

**F6a. [CONFIRMED]** 设备核心在 probe 之前调用 `pinctrl_bind_pins()`。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/base/dd.c
- "/* If using pinctrl, bind pins now before probing */"

**F6b. [CONFIRMED]** `pinctrl_bind_pins()` 的 kernel-doc 明说由设备核心在 probe 前调用。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/base/pinctrl.c
- "pinctrl_bind_pins() - called by the device core before probe"

**F6c. [CONFIRMED]** 它查找 `PINCTRL_STATE_DEFAULT` 并使能该状态（无 init 状态时选 default）。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/base/pinctrl.c
- "dev->pins->default_state = pinctrl_lookup_state(dev->pins->p, PINCTRL_STATE_DEFAULT);"
- 同处：`ret = pinctrl_select_state(dev->pins->p, dev->pins->default_state);`

**F7a. [CONFIRMED]** 分配 order 页即 2^order 页（代码 `1 << order`）。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/page_alloc.c
- "int nr_pages = 1 << order;"
- 同文件注释：`Higher-order pages are called "compound pages".`

**F7b. [CONFIRMED]** `alloc_pages` / `__get_free_pages` 的 order 参数含义一致，单页为 order 0。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/gfp.h
- "#define alloc_page(gfp_mask) alloc_pages(gfp_mask, 0)"
- 同处：`extern unsigned long get_free_pages_noprof(gfp_t gfp_mask, unsigned int order);`

**F7c. [UNCONFIRMED]** “PAGE_SIZE 在常见配置下为 4096”的文档原句。
- 实际找到：`arch/x86/include/asm/page_types.h` 只有 `#define PAGE_SHIFT CONFIG_PAGE_SHIFT` 与 `#define PAGE_SIZE (_AC(1,UL) << PAGE_SHIFT)`；`arch/Kconfig` 有 `default 12 if PAGE_SIZE_4KB`；`Documentation/admin-guide/mm/concepts.rst` 只说 "The size of each page is architecture specific."。缺“x86 选中 4KB 页”这一环的原文，故 4096 不作确认。

**F8. [CONFIRMED]** Oops 输出包含错误行、`Oops: ...`、寄存器行、`IP:`/`RIP:` 与 `Call Trace:`。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/bug-hunting.rst
- "BUG: unable to handle kernel NULL pointer dereference at   (null)"
- 同文件：`Oops: 0002 [#1] PREEMPT SMP`、`Call Trace:`、`IP: [<c06969d4>] iret_exc+0x7d0/0xa59`

**F9. [CONFIRMED — 原文未用 SMI 缩写]** 固件可抢先/拦截内核执行，形成内核被中断的时间段，可用 hardware latency detector 观测。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/core-api/real-time/hardware.rst
- "Firmware can also intercept kernel execution by providing services that temporarily take control of the system."
- 同文件：`During this time, the kernel is effectively interrupted.`
- C-state 部分：该文件只在 virtualization 段提到 `idle=poll`，无 C-state 退出延迟论述（该内容在 admin-guide/pm/cpuidle.rst）。

**F10. [CONFIRMED，但替代建议写错了]** tasklet API 官方标注 deprecated，建议改用 **threaded IRQs**（不是 workqueue/BH workqueue）。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/interrupt.h
- "This API is deprecated. Please consider using threaded IRQs instead:"

**F11. [CONFIRMED — 用 rt-tests 上游 man page]** cyclictest 测量线程唤醒/间隔的实际延迟并统计 min/avg/max；linuxfoundation wiki 被 Cloudflare 拦截（403/JS 挑战），未采用。
- https://git.kernel.org/pub/scm/utils/rt-tests/rt-tests.git/plain/src/cyclictest/cyclictest.8
- "Align measurement thread wakeups to a specific offset in microseconds"
- 同文件：`compared against the actual latencies of the test`；源码 cyc.c：`# Max Latencies:`

**F12. [CONFIRMED]** libgpiod 工具确为 gpiodetect / gpioinfo / gpioget / gpioset（另有 gpiomon、gpionotify）。
- https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/tree/tools
- 目录含 `gpiodetect.c`、`gpioinfo.c`、`gpioget.c`、`gpioset.c`、`gpiomon.c`、`gpionotify.c`
- https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/plain/tools/gpiodetect.c
- "List GPIO chips, print their labels and number of GPIO lines."

**F13. [CONFIRMED]** SysRq `s` 同步已挂载文件系统，`u` 重新挂载为只读。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/sysrq.rst
- "``s``	    Will attempt to sync all mounted filesystems."
- 同文件：``u`` — Will attempt to remount all mounted filesystems read-only.

**F14. [UNCONFIRMED]** “UEFI 的 ESP 使用 FAT32”的规范原句。
- 实际找到：uefi.org 直连返回 Cloudflare（403 / “Just a moment…”）；Tavily 抓 `13_Protocols_Media_Access.html` 只回约 6k 字符目录导航（整页 347k），未取到 13.3.1.1 File System Format 的句子。故仍不确认。

**F15. [CONFIRMED]** 网络接口在 `/dev` 下没有设备节点。
- https://lwn.net/images/pdf/LDD3/ch17.pdf
- "a disk exists as a special file in the /dev directory, whereas a network interface has no such entry point"

**F16. [CONFIRMED]** 总线用 `match()` 比对设备与驱动 ID，匹配后设置 driver 并调用 probe。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/driver-api/driver-model/binding.rst
- "If a match is found, the device's driver field is set to the driver and the driver's probe callback is called."

**F17. [CONFIRMED]** platform_device 正是为“硬件无法探测”的 memory/IO 映射设备而设。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/devicetree/usage-model.rst
- "used by Linux for memory or I/O mapped devices which cannot be detected by hardware"
- 备注：USB/PCI“动态发现”在该文件只以总线层级出现（`Similarly for USB, PCI, MDIO, etc.`）；DT spec 2.1 另有 "the architecture of PCI enables a client to probe and detect attached devices"。

**F18. [CONFIRMED]** 等待队列：`wait_event_interruptible()` 条件不成立则睡眠，改变条件后需 `wake_up()`；被信号打断返回 -ERESTARTSYS。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/wait.h
- "wake_up() has to be called after changing any variable that could change the result of the wait condition."
- 同处：`The function will return -ERESTARTSYS if it was interrupted by a signal`

### 本轮新增的修正

1. **PREEMPT_VOLUNTARY** 的菜单文字是 `Voluntary Kernel Preemption (Desktop)`；**PREEMPT** 是 `Preemptible Kernel (Low-Latency Desktop)`；主线另有第五种 **PREEMPT_LAZY**（Scheduler controlled preemption model）。
2. **tasklet 的官方替代建议是 threaded IRQs**（interrupt.h 原文），不是 workqueue/BH workqueue；BH workqueue 文档本身并未声称取代 tasklet。
3. **PAGE_SIZE=4096** 不可作“文档明说”引用：x86 走 `#define PAGE_SHIFT CONFIG_PAGE_SHIFT`，`PAGE_SIZE = 1 << PAGE_SHIFT`，`arch/Kconfig` 仅给 `default 12 if PAGE_SIZE_4KB`；mm 文档强调 page size 依架构而定。

---

## Follow-up 2

**G1. [CONFIRMED]** 板级配置通过 `make <board>_defconfig` 生成 `.config`。
- https://docs.u-boot.org/en/latest/build/gcc.html
- "Instead their name serves as a make target to generate the actual configuration file .config."
- 同页示例：`make odroid-c2_defconfig`

**G2. [CONFIRMED]** `bootdelay` 是自动执行 `bootcmd` 前的等待。
- https://docs.u-boot.org/en/latest/usage/environment.html
- "Delay before automatically running bootcmd."
- 备注：该页未写 “seconds” 字样，单位由默认值/CONFIG_BOOTDELAY 体现（同页 “0 to autoboot with no delay”）。

**G3. [CONFIRMED，语法比题述更长]** `load` 完整语法含 `bytes`/`pos` 两个可选参数。
- https://docs.u-boot.org/en/latest/usage/cmd/load.html
- "load <interface> [<dev[:part]> [<addr> [<filename> [bytes [pos]]]]]"
- 同页：`part partition number, defaults to 0 (whole device)`（故 `mmc 0:1` = 设备 0、分区 1）

**G4. [CONFIRMED]** `booti` 语法，`-` 表示不带 initrd。
- https://docs.u-boot.org/en/latest/usage/cmd/booti.html
- "booti [<addr> [<initrd>[:<size>]] [<fdt>]]"
- 同页：`Use ‘-’ to boot a kernel with a device tree but without an initial RAM disk.`

**G5. [CONFIRMED]** `kernel_addr_r` / `fdt_addr_r` 是标准环境变量名，文档专门讨论其地址约束。
- https://docs.u-boot.org/en/latest/usage/environment.html
- "When setting the RAM addresses for kernel_addr_r, fdt_addr_r and ramdisk_addr_r there are several types of constraints to keep in mind."

**G6a. [CONFIRMED]** `source` 执行内存中的脚本文件，脚本镜像由 mkimage 生成。
- https://docs.u-boot.org/en/latest/usage/cmd/source.html
- "The source command is used to execute a script file from memory."
- 同页：`Both formats can be created with the mkimage tool.`

**G6b. [UNCONFIRMED]** “`mkimage -T script` 生成 boot.scr”的 `-T script` 字面原文。
- 实际找到：U-Boot mkimage.1（master）只文档化 `-T type` 与 `-T list`，正文没有 script 类型说明；`develop/distro.html` 提到 boot.scr 但不给 mkimage 命令；source.html 只说 mkimage 能生成脚本格式。故 `-T script` 这一具体选项不作确认。

**G7. [CONFIRMED]** `rootwait` 无限期等待根设备出现（常用于 USB/MMC 等异步设备）。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/kernel-parameters.txt
- "rootwait	[KNL] Wait (indefinitely) for root device to show up."
- 同处：`Useful for devices that are detected asynchronously (e.g. USB and MMC devices).`

**G8. [CONFIRMED]** “No working init found.” 文档列出的原因含 root= 分区不对、init 不存在、二进制架构不符。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/init.rst
- "Explaining the "No working init found." boot hang message"
- 同文件：`init binary doesn't exist on rootfs`、`the ``root=`` kernel parameter points to the correct partition`、`Make sure the binary's architecture matches your hardware.`

**G9. [CONFIRMED]** `/dev/ttyS0` 属 char major 4、minor 64。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/devices.txt
- "4 char	TTY devices"
- 同处：`64 = /dev/ttyS0		First UART serial port`

**G10a. [CONFIRMED]** DRM 主节点为 `/dev/dri/card0`（char 226）。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/devices.txt
- "0 = /dev/dri/card0		First graphics card"

**G10b. [CONFIRMED]** V4L2 视频设备节点为 `/dev/video0`…`/dev/video63`。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/userspace-api/media/v4l/dev-capture.rst
- "device special files named ``/dev/video`` and ``/dev/video0`` to ``/dev/video63``"

**G10c. [CONFIRMED]** i2c-dev 提供 `/dev/i2c-N`。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/i2c/dev-interface.rst
- "snprintf(filename, 19, "/dev/i2c-%d", adapter_nr);"

**G10d. [CONFIRMED]** spidev 节点为 `/dev/spidevB.C`（B=bus，C=chip select）。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/spi/spidev.rst
- "For a SPI device with chipselect C on bus B, you should see: /dev/spidevB.C ..."

**G10e. [CONFIRMED]** ALSA 节点位于 `/dev/snd/`（如 pcmC0D0）。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/sound/alsa-configuration.rst
- "/dev/snd/pcmC0D0[c|p]  -> /dev/audio0 (/dev/audio) -> minor 4"

**G11. [CONFIRMED]** I2C client 的 sysfs 名为 “<bus>-<4 位十六进制地址>”。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/i2c/i2c-core-base.c
- "dev_set_name(&client->dev, "%d-%04x", i2c_adapter_id(adap),"

**G12. [CONFIRMED]** tmp102 驱动的 of_match 含 `"ti,tmp102"`。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/hwmon/tmp102.c
- "{ .compatible = "ti,tmp102" },"

**G13a. [CONFIRMED]** imx6ul.dtsi 的 uart1 节点为 `serial@2020000`，compatible 两个字符串，reg 0x2020000 长 0x4000，中断 GIC_SPI 26。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/arch/arm/boot/dts/nxp/imx/imx6ul.dtsi
- "uart1: serial@2020000 {"
- 同处：`compatible = "fsl,imx6ul-uart",` / `"fsl,imx6q-uart";`、`reg = <0x02020000 0x4000>;`、`interrupts = <GIC_SPI 26 IRQ_TYPE_LEVEL_HIGH>;`

**G13b. [CONFIRMED]** imx 串口驱动的 of_device_id 含 `"fsl,imx6q-uart"`。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/tty/serial/imx.c
- "{ .compatible = "fsl,imx6q-uart", .data = &imx_uart_imx21_devdata, },"

**G14. [CONFIRMED]** 存在 `module_platform_driver` 宏（注释即题述文字），以及 `devm_platform_ioremap_resource`、`platform_get_irq` 原型。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/platform_device.h
- "module_platform_driver() - Helper macro for drivers that don't do"
- 同处：`anything special in module init/exit.  This eliminates a lot of`、`devm_platform_ioremap_resource(struct platform_device *pdev,`、`extern int platform_get_irq(struct platform_device *, unsigned int);`

**G15. [CONFIRMED]** devres 资源在 probe 半途失败时也会释放。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/driver-api/driver-model/devres.rst
- "If a driver uses dmam_alloc_coherent(), the area is guaranteed to be freed whether initialization fails half-way or the device gets detached."

**G16. [CONFIRMED]** debugfs 没有任何规则，而 sysfs 有“一文件一值”的严格约束。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/filesystems/debugfs.rst
- "or sysfs, which has strict one-value-per-file rules, debugfs has no rules at all."

**G17. [CONFIRMED]** 日志级别（数值更小=更严重）高于 console_loglevel 的消息才输出到控制台。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/core-api/printk-basics.rst
- "If the message priority is higher (lower log level value) than the console_loglevel the message will be printed to the console."

**G18. [CONFIRMED]** arm64 Oops 依次打印 `pc : %pS` / `lr : %pS`、寄存器、`Call trace:`，缺页消息含 “Unable to handle kernel NULL pointer dereference”。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/arch/arm64/kernel/process.c
- "printk("pc : %pS\n", (void *)regs->pc);"
- 同文件：`printk("lr : %pS\n", (void *)ptrauth_strip_kernel_insn_pac(lr));`
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/arch/arm64/kernel/stacktrace.c
- "printk("%sCall trace:\n", loglvl);"
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/arch/arm64/mm/fault.c
- "msg = "NULL pointer dereference";"
- 同文件：`pr_alert("Unable to handle kernel %s at virtual address %016lx\n", msg,`

**G19. [CONFIRMED]** 未解析符号的内核日志为 “Unknown symbol %s (err %d)”。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/kernel/module/main.c
- "pr_warn("%s: Unknown symbol %s (err %d)\n","

**G20. [CONFIRMED]** 页分配器（buddy）会合并相邻 order 的伙伴页；slab 缓存小对象、把大分配下放给页分配器（kmalloc 走 slab）。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/page_alloc.c
- "check if the buddy of the next-higher order is free"
- 同文件：`more likely to be merged as a 2-level higher order page`
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/core-api/memory-allocation.rst
- "Internally, the slab allocator differentiates allocations of different orders and delegates larger allocations to the page allocator"

**G21. [CONFIRMED]** vmalloc 路径会睡眠（不可在原子/中断上下文用）。
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/vmalloc.c
- "might_sleep();"
- 紧邻注释：`Also might shootdown TLB (requires IRQs enabled on x86).`

**G22a. [CONFIRMED]** SCHED_DEADLINE 用 GEDF + CBS 实现。
- https://man7.org/linux/man-pages/man7/sched.7.html
- "This policy is currently implemented using GEDF (Global Earliest Deadline First) in conjunction with CBS (Constant Bandwidth Server)."

**G22b. [CONFIRMED]** SCHED_FIFO 线程一旦可运行就立刻抢占 SCHED_OTHER/BATCH/IDLE。
- https://man7.org/linux/man-pages/man7/sched.7.html
- "it will always immediately preempt any currently running SCHED_OTHER, SCHED_BATCH, or SCHED_IDLE thread"

**G23. [UNCONFIRMED]** Xenomai 的 dual-kernel（Cobalt）描述原句。
- 实际找到：`xenomai.org` 首页仅有 “Cobalt LTS / Cobalt latest” 导航；`doc.xenomai.org` 的 Doxygen 页面是 JS 动态加载（正文 “Loading...”）；`source.denx.de/Xenomai/xenomai/-/raw/...` 返回 502；GitHub/GitLab 镜像 README 均 404。未取得 “real-time co-kernel alongside Linux” 类原句。

**G24. [CONFIRMED]** `-fno-zero-initialized-in-bss` 语义：默认把零初始化变量放进 BSS。
- https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html
- "If the target supports a BSS section, GCC by default puts variables that are initialized to zero into BSS."
- 同页：`The default is -fzero-initialized-in-bss except in Ada.`

**G25. [UNCONFIRMED]** “实时应用应在实时循环内避免动态内存分配/缺页”的官方原文。
- 实际找到：`wiki.linuxfoundation.org` 的 realtime 页面直连与 Tavily 均被 Cloudflare 拦截（application_base 也失败）；`Documentation/core-api/real-time/*.rst` 只有锁/中断/内存分配上下文（`Memory allocation` 一节讲 GFP 语义），没有该应用层建议句。mlock(2) 只有 “reserve enough locked stack pages” 的相邻论述（已在主报告确认）。

**G26. [CONFIRMED]** STM32F4 HAL 定义 PINRST/PORRST/SFTRST/IWDGRST/WWDGRST 复位标志（另有 BORRST、LPWRRST）。
- https://raw.githubusercontent.com/STMicroelectronics/stm32f4xx-hal-driver/master/Inc/stm32f4xx_hal_rcc.h
- "#define RCC_FLAG_IWDGRST                 ((uint8_t)0x7D)"
- 同文件：`#define RCC_FLAG_PINRST                  ((uint8_t)0x7A)`、`#define RCC_FLAG_PORRST                  ((uint8_t)0x7B)`、`#define RCC_FLAG_SFTRST                  ((uint8_t)0x7C)`、`#define RCC_FLAG_WWDGRST                 ((uint8_t)0x7E)`

**G27. [UNCONFIRMED]** FreeRTOS `configCHECK_FOR_STACK_OVERFLOW` 方法 1 的官方说明（检查上下文保存后的栈指针是否仍在合法区间）。
- 实际找到：freertos.org 该页是 JS 渲染（纯文本仅 64 字符）；V10.4.6 与 main 分支 `tasks.c` 都已把检查下沉到 port 层（`portHAS_STACK_OVERFLOW_CHECKING`），不再含方法 1/2 的文字说明；论坛帖不是一手文档。故不确认。

**Follow-up 2 统计：34 条中 30 条 CONFIRMED，4 条 UNCONFIRMED（G6b、G23、G25、G27）。**
