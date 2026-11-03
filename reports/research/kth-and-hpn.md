# KTH 课程先修原文 + 「高性能网络」技能依据

> 上游同步复核（2026-11-03）：C.3.5 已进入 tree，游戏直接导入。按 tree 的 CS2023 逐项证据，拓扑、RDMA、拥塞控制命中 KA Core（3/6），该节点已改为主干；当前中文教学覆盖 4/6。下文保留为初次调研记录，最终数据与限制见 [同步说明](../tree-sync-2026-11-03.md) 和相邻 tree 的增补报告。

- 抓取日期：2026-11-03（本机时区，`curl` 直接取 KTH 静态页；页面为服务端渲染，无需登录）
- 数据来源：KTH 课程页 `https://www.kth.se/student/kurser/kurs/<课程代码>?l=en`
- 每门课页面上都同时给出「Course syllabus as PDF」，形如 `.../kursplan/<代码>-<版本号>.pdf`；版本号编码学期（`20262` = Autumn 2026，`20201` = Spring 2020）。
- 下文 `Specific prerequisites` 一律**逐字**抄录英文原文（含原文的 `/`、逗号与逗号小数写法）。「—」表示该字段在页面上就是 `No information inserted`。

---

## 任务 1：KTH 课程先修原文

### a. 操作系统

#### a-1. ID1206 Operating Systems — 7.5 credits
- 链接：https://www.kth.se/student/kurser/kurs/ID1206?l=en
- 页面可见课纲版本：**Course syllabus ID1206 (Autumn 2026–)**，PDF：https://www.kth.se/student/kurser/kurs/kursplan/ID1206-20262.pdf
- 开课学期（页面 "Information per course offering"）：Autumn 2026，P2，26 Oct 2026 – 11 Jan 2027，50% 进度
- 开课单位：EECS/Computational Science and Technology；教育周期：First cycle

**Specific prerequisites（逐字）**

> - Knowledge and skills in programming, 6 credits, equivalent to completed course DD1337/DD1310-DD1319/DD1321/DD1331/DD1333/DD100N/ID1018/ID1022.
> - Knowledge in algorithms and data structures, 6 credits, equivalent to completed course DD1338/DD1320-DD1328/DD2325/ID1020/ID1021 or completed exam modules KONT and LABD in DD1326.
> - Knowledge in computer technology equivalent to completed course IS1200/IS1500/EP1200 or completed exam module LAB1 in IS1200.

**要点**：OS 课的先修 = 编程 + 数据结构与算法 + 计算机组成（IS1200/IS1500）。没有出现「计算机网络」先修。

课程内容（原文摘录，用于判断知识项边界）：

> The course provides knowledge of the principles of and how one can implement
> - abstractions of hardware
> - virtualisation of resources and timetabling of assignments; mainly as regards execution, memory and persistent storage.

---

### b. 计算机组成 / 计算机体系结构

#### b-1. IS1500 Computer Organization and Components — 9.0 credits
- 链接：https://www.kth.se/student/kurser/kurs/IS1500?l=en
- 页面可见课纲版本：**Course syllabus IS1500 (Autumn 2026–)**，PDF：https://www.kth.se/student/kurser/kurs/kursplan/IS1500-20262.pdf

**Specific prerequisites（逐字）**

> Knowledge and skills in programming, 6 credits, equivalent to completed course DD1337/DD1310-DD1319/DD1321/DD1331/DD1333/DD100N/ID1018/ID1022.

**Recommended prerequisites（逐字）**

> The student must be able to write, explain and debug programs in imperative programming-languages, such as Java, C, or C++, up to program-sizes around 100 lines of code.

课程内容（原文摘录）：

> The course gives basic knowledge of how a computer functions and is built-up both from a hardware and from a software perspective The course is divided into six different modules ...
> - C-programming and assembler language: pointers, functions, stack, assembly language, machine language, instruction encoding and processor registers.
> - I/O system: timers, interrupts and memory mapped I/O.
> - Processor construction: arithmetic-logic unit, data path, control unit and pipeline.
> - Memory architectures: instruction cache, data cache and virtual memory.
> - Parallel processors and programs: Amdahl's law, different specialisations of parallelism as well as multicore.

#### b-2. IS1200 Computer Hardware Engineering — 7.5 credits
- 链接：https://www.kth.se/student/kurser/kurs/IS1200?l=en
- 页面可见课纲版本：**Course syllabus IS1200 (Spring 2020–)**，PDF：https://www.kth.se/student/kurser/kurs/kursplan/IS1200-20201.pdf
- 开课：Autumn 2026，开始 24 Aug 2026（页面 "Choose course offering"）

**Specific prerequisites（逐字）**

> No information inserted

**Recommended prerequisites（逐字）**

> Fundamental knowledge of programming and digital electronics.

**要点**：IS1200 是 KTH 的「入门级硬件课」，**没有硬性先修**——这正好可以作为技能树里「C.1.1 计算机组成原理」是**根节点**的证据。而 ID1206 把 IS1200/IS1500 列为 OS 的先修，形成 `硬件 → OS` 边。

---

### c. C 语言 / 程序设计入门、数据结构与算法

#### c-1. DD1337 Programming — 7.0 credits
- 链接：https://www.kth.se/student/kurser/kurs/DD1337?l=en
- 页面可见课纲版本：**Course syllabus DD1337 (Spring 2019–)**，PDF：https://www.kth.se/student/kurser/kurs/kursplan/DD1337-20191.pdf

**Specific prerequisites（逐字）**

> No information inserted

**要点**：DD1337 无先修，是整棵树「编程入口」的证据。ID1206 / IS1500 / DD1338 / DD2421 / DD2424 都把它列为先修，是 KTH 计算机课程的事实根。

#### c-2. ID1021 Algorithms and Data Structures — 7.5 credits
- 链接：https://www.kth.se/student/kurser/kurs/ID1021?l=en
- 页面可见课纲版本：**Course syllabus ID1021 (Spring 2027–)**，PDF：https://www.kth.se/student/kurser/kurs/kursplan/ID1021-20271.pdf
- 开课：Spring 2027，开始 12 Jan 2027（页面 "Choose course offering"）

**Specific prerequisites（逐字）**

> Knowledge and skills in programming, 7,5 credits, corresponding to completed course ID1022/ID1018.
> Active participation in ID1022 during study period 2 of the same academic year is considered equivalent to completed course. Registered students are expected and considered to be actively participating.

**Recommended prerequisites（逐字）**

> The course structure is based on the participants having programming skills and being able to edit without help, compile and run simpler programs even in languages they may not normally use or have used before.

#### c-3. DD1338 Algorithms and Data Structures — 6.0 credits
- 链接：https://www.kth.se/student/kurser/kurs/DD1338?l=en
- 页面可见课纲版本：**Course syllabus DD1338 (Autumn 2026–)**，PDF：https://www.kth.se/student/kurser/kurs/kursplan/DD1338-20262.pdf

**Specific prerequisites（逐字）**

> Knowledge and skills in object-oriented programming, 7 credits, corresponding to completed course DD1337 alternatively both courses DD1310 and DD1380.
> Active participation in DD1337 or DD1380 during study period 1 of the same academic year is equated with completed course. Anyone who is registered is expected and considered to be actively participating.

**Recommended prerequisites（逐字）**

> DD1337 Programming.

**要点**：KTH 的两条「数据结构」路线可对照——ID1021 走 ID1022/ID1018（ID 系），DD1338 走 DD1337/DD1380（D 系）。ID1206 同时接受两者，说明它们是**等价节点**，技能树里只需一个「数据结构与算法」节点，不必拆两条线。

---

### d. 机器学习 / 深度学习

#### d-1. DD2421 Machine Learning — 7.5 credits
- 链接：https://www.kth.se/student/kurser/kurs/DD2421?l=en
- 页面可见课纲版本：**Course syllabus DD2421 (Autumn 2024–)**，PDF：https://www.kth.se/student/kurser/kurs/kursplan/DD2421-20242.pdf

**Specific prerequisites（逐字）**

> Knowledge and skills in programming, 6 credits, equivalent to completed course DD1337/DD1310-DD1319/DD1321/DD1331/DD100N/ID1018.
> Knowledge in linear algebra, 7,5 credits, equivalent to completed course SF1624/SF1672/SF1684.
> Knowledge in multivariable calculus, 7,5 credits, equivalent to completed course SF1626/SF1674.
> Knowledge in probability theory and statistics, 6 credits, equivalent to completed course SF1910-SF1924/SF1935.

**要点**：ML 的先修是**三门数学课齐上**（线性代数 + 多变量微积分 + 概率统计），这是技能树里「数学 → ML」三条独立边的直接证据。

#### d-2. DD2424 Deep Learning in Data Science — 7.5 credits
- 链接：https://www.kth.se/student/kurser/kurs/DD2424?l=en
- 页面可见课纲版本：**Course syllabus DD2424 (Autumn 2024–)**，PDF：https://www.kth.se/student/kurser/kurs/kursplan/DD2424-20242.pdf

**Specific prerequisites（逐字）**

> Knowledge and skills in programming, 6 credits, equivalent to completed course DD1337/DD1310-DD1319/DD1321/DD1331/DD100N/ID1018.
> Knowledge in linear algebra, 7,5 higher education credits, equivalent to completed course SF1624/SF1672/SF1684.
> Knowledge in multivariable analysis, 7,5 higher education credits, equivalent to completed course SF1626/SF1674.
> Knowledge in probability theory and statistics, 6 higher education credits, equivalent to completed course SF1910-SF1924/SF1935.
> Knowledge in machine learning or artificial intelligence, 6 higher education credits, equivalent to completed course DD1420/DD2421 or DD2380/ID1214.
> Active participation in a course offering where the final examination is not yet reported in LADOK is considered equivalent to completion of the course.
> Registering for a course is counted as active participation.
> The term 'final examination' encompasses both the regular examination and the first re-examination.

**要点**：DL 在 ML 之上，多了 `DD2421/DD2380/ID1214` 这一条「ML 先修」，其余三条数学先修完全相同。→ `数学 → ML → DL` 是可证的链。

---

### e. 微积分 / 线性代数 / 概率统计

#### e-1. SF1625 Calculus in One Variable — 7.5 credits
- 链接：https://www.kth.se/student/kurser/kurs/SF1625?l=en
- 页面可见课纲版本：**Course syllabus SF1625 (Autumn 2019–)**，PDF：https://www.kth.se/student/kurser/kurs/kursplan/SF1625-20192.pdf

**Specific prerequisites（逐字）**

> Basic requirements.

#### e-2. SF1672 Linear Algebra — 7.5 credits
- 链接：https://www.kth.se/student/kurser/kurs/SF1672?l=en
- 页面可见课纲版本：**Course syllabus SF1672 (Autumn 2019–)**，PDF：https://www.kth.se/student/kurser/kurs/kursplan/SF1672-20192.pdf

**Specific prerequisites（逐字）**

> Basic requirements.

> 注：瑞典语页标题为 `SF1672 Linjär algebra 7,5 hp`（https://www.kth.se/student/kurser/kurs/SF1672?l=sv ）。而 SF1922 的 Recommended prerequisites 里把 SF1672 写成 "Algebra and Geometry"，那是 KTH 页面的历史残留名（SF1624 的英文名才是 Algebra and Geometry）。以 SF1672 自身页面标题 `Linear Algebra` 为准。

#### e-3. SF1624 Algebra and Geometry — 7.5 credits
- 链接：https://www.kth.se/student/kurser/kurs/SF1624?l=en
- 页面可见课纲版本：**Course syllabus SF1624 (Autumn 2019–)**，PDF：https://www.kth.se/student/kurser/kurs/kursplan/SF1624-20192.pdf

**Specific prerequisites（逐字）**

> Basic requirements.

#### e-4. SF1922 Probability Theory and Statistics — 6.0 credits
- 链接：https://www.kth.se/student/kurser/kurs/SF1922?l=en
- 页面可见课纲版本：**Course syllabus SF1922 (Spring 2020–)**，PDF：https://www.kth.se/student/kurser/kurs/kursplan/SF1922-20201.pdf

**Specific prerequisites（逐字）**

> Active participation in SF1673 Analysis in one variable or SF1625 Calculus in one variable.

**Recommended prerequisites（逐字）**

> SF1672 Algebra and Geometry, SF1674 Calculus in Several Variables

**要点（重要）**：
1. 三门数学基础课（SF1625 / SF1672 / SF1624）的先修都只写 `Basic requirements.`（= 瑞典高中资格），**这支持「数学基础」作为根节点**，而不是互相成链。
2. 概率统计 SF1922 **硬性要求单变量微积分**（SF1625 或 SF1673），推荐里才有线代与多变量微积分。→ 技能树里 `微积分 → 概率统计` 是**必须前置**；`线性代数 → 概率统计` 只能算**推荐/弱边**，不能写成必须。
3. 与 d-1/d-2 对照：DD2421 要 SF1910-SF1924（含 SF1922）/SF1935 作为「概率统计 6 credits」，所以 `概率统计 → ML` 是必须前置。

---

### f. 计算机网络 / 数据中心 / 高性能网络

#### f-1. IK1203 Networks and Communication — 7.5 credits
- 链接：https://www.kth.se/student/kurser/kurs/IK1203?l=en
- 页面可见课纲版本：**Course syllabus IK1203 (Spring 2027–)**，PDF：https://www.kth.se/student/kurser/kurs/kursplan/IK1203-20271.pdf
- 开课：Spring 2027，开始 12 Jan 2027

**Specific prerequisites（逐字）**

> Knowledge and skills in programming corresponding to completed course ID1022/ID1018/DD1337/DD1310-DD1319/DD1321/DD1331/DD1333/DD100N/DD100V.
> Knowledge in Boolean algebra corresponding completed course IE1204/IE1205/IS1500, or completed course component ANN1 in IS1500, or at least 3.5 credits of completed course components in IE1204/IE1205.

课程内容里有数据中心网络（原文）：

> - Local area networks: topologies, access control, Ethernet, wireless local area networks, switched local area networks, link protocols. Network in data centers. Detection of transmission errors.
> - Flow regulation, congestion control and error handling. Stop-and-wait, Go-Back-N as well as window handling and congestion control in TCP.

**要点**：KTH 的基础网络课先修 = 编程 + **布尔代数/数字电路（IS1500）**，不要求 OS。这与「网络在 OS 之前就能上」的现实一致，技能树里 `C.1.1 计算机组成 → 网络` 有据可依（经 IS1500 的布尔代数）。

#### f-2. IK2215 Advanced Internetworking — 7.5 credits
- 链接：https://www.kth.se/student/kurser/kurs/IK2215?l=en
- 页面可见课纲版本：**Course syllabus IK2215 (Autumn 2022–)**，PDF：https://www.kth.se/student/kurser/kurs/kursplan/IK2215-20222.pdf

**Specific prerequisites（逐字）**

> Knowledge in Internet technique, 6 higher education credits, equivalent completed course IK1552.

**Recommended prerequisites（逐字）**

> Experience of working in Unix environments.

课程内容（原文）：

> The course focuses on communications protocol for Internet, and the emphasis lies on generic mechanisms on the different protocols in the protocol stack TCP/IP. ... To further illustrate different principles and to give practical experience contains the course in addition to theoretical items as lectures, a set labs and a project task.

> 注：IK2215 的先修写的是 **IK1552 Internetworking**（https://www.kth.se/student/kurser/kurs/IK1552?l=en ，7.5 credits，课纲版本 *Spring 2020–*，`Specific prerequisites` = `No information inserted`），不是 IK1203。KTH 的 IK1203 与 IK1552 是两条并存的基础网络课，IK2215 只认 IK1552。

#### f-3. IK2220 Software Defined Networking (SDN) and Network Functions Virtualization (NFV) — 7.5 credits
- 链接：https://www.kth.se/student/kurser/kurs/IK2220?l=en
- 页面可见课纲版本：**Course syllabus IK2220 (Spring 2024–)**，PDF：https://www.kth.se/student/kurser/kurs/kursplan/IK2220-20241.pdf

**Specific prerequisites（逐字）**

> Students who attend this course are required to have passed IK2215 (Advanced Internetworking) or have equivalent knowledge in Internetworking and Computer Communications.
> Good programming knowledge (C++, Java, or Python but preferably all).

课程内容（原文）：

> Software Defined Networking (SDN). SDN control plane. Programming large SDNs. Examples of SDN Deployments. Debugging and verifying SDNs. Role of middleboxes in the dataplane. Network Functions Virtualization (NFV). Efficient use of all available hardware for NFV dataplane processing. Load balancing for NFV. Programmable control and dataplane for machine learning applications.

#### f-4. FIK3221 Networked Systems for Machine Learning — 7.5 credits ★（本任务最关键的一门）
- 链接：https://www.kth.se/student/kurser/kurs/FIK3221?l=en
- 页面可见课纲版本：该页**没有** `Course syllabus ... (term–)` 抬头、也没有 kursplan PDF 链接（博士/third-cycle 课程，走单独课纲流程）；页面仍完整给出 Course contents / ILO / Specific prerequisites / Examination。
- 开课单位：EECS（third-cycle，`l=en` 页面无常规 offering 表格）

**Specific prerequisites（逐字）**

> Knowledge in advanced Internet technique, 7.5 higher education credits, equivalent completed course IK2215. Knowledge and skills in programming in C++, Java or Python, 6 higher education credits, equivalent completed course DD1310-DD1319/DD1331/DD1337/DD100N/ID1018.

**Recommended prerequisites（逐字）**

> Knowledge in advanced Internet technique, 7.5 higher education credits, equivalent completed course IK2215. Knowledge and skills in programming in C++, Java or Python, 6 higher education credits, equivalent completed course DD1310-DD1319/DD1331/DD1337/DD100N/ID1018.

**Course contents（逐字，这就是「高性能网络」技能点的课程级证据）**

> Network functions. Virtualisation. Kernel bypass technologies (e.g. DPDK) for networks with over 100 gigabits per second. Offloading to Smart Network Interface Cards (SmartNIC). Fast networking with little or no CPU intervention using remote direct memory access (RDMA). Network aspects of machine learning inference using graphics processing units (GPUs). Load estimation and load balancing. Request for dispatch and scheduling. Efficient, large-scale machine learning inference. Inference with large language models (LLM).

**Intended learning outcomes（逐字节选）**

> - describe and analyze an example of a service using virtualization of network functions (NFV)
> - explain and differentiate the important advantages of remote direct memory access (RDMA) and how it operates
> - analyze methods for performing network I/O directly to/from graphics processors (GPU)
> - describe and analyze the role of the load balancing for servers
> - describe and analyze examples of current research problems with serving machine learning workloads in data centers

**要点**：KTH 把 DPDK / kernel bypass / SmartNIC / RDMA / GPU 网络 / 数据中心 ML 服务**打包成一门独立课**，先修是 `IK2215（高级互联网技术）+ C/C++/Java/Python 编程`，**不要求 OS 课**。这是任务 2 建议的重要依据：KTH 认为「数据中心与高性能网络」的硬前置是**网络（IK2215 级）**，OS 只是隐性背景。

---

### 任务 1 抓取情况汇总

| 方向 | 课程 | 代码 | 学分 | 课纲版本 | 抓到先修？ |
|---|---|---|---|---|---|
| a OS | Operating Systems | ID1206 | 7.5 | Autumn 2026– | ✅ |
| b 组成 | Computer Organization and Components | IS1500 | 9.0 | Autumn 2026– | ✅ |
| b 组成 | Computer Hardware Engineering | IS1200 | 7.5 | Spring 2020– | ✅（`No information inserted`） |
| c 编程 | Programming | DD1337 | 7.0 | Spring 2019– | ✅（`No information inserted`） |
| c 算法 | Algorithms and Data Structures | ID1021 | 7.5 | Spring 2027– | ✅ |
| c 算法 | Algorithms and Data Structures | DD1338 | 6.0 | Autumn 2026– | ✅ |
| d ML | Machine Learning | DD2421 | 7.5 | Autumn 2024– | ✅ |
| d DL | Deep Learning in Data Science | DD2424 | 7.5 | Autumn 2024– | ✅ |
| e 微积分 | Calculus in One Variable | SF1625 | 7.5 | Autumn 2019– | ✅（`Basic requirements.`） |
| e 线代 | Linear Algebra | SF1672 | 7.5 | Autumn 2019– | ✅（`Basic requirements.`） |
| e 线代/几何 | Algebra and Geometry | SF1624 | 7.5 | Autumn 2019– | ✅（`Basic requirements.`） |
| e 概率 | Probability Theory and Statistics | SF1922 | 6.0 | Spring 2020– | ✅ |
| f 网络 | Networks and Communication | IK1203 | 7.5 | Spring 2027– | ✅ |
| f 网络 | Internetworking | IK1552 | 7.5 | Spring 2020– | ✅（`No information inserted`） |
| f 高级网络 | Advanced Internetworking | IK2215 | 7.5 | Autumn 2022– | ✅ |
| f SDN/NFV | SDN and NFV | IK2220 | 7.5 | Spring 2024– | ✅ |
| f 高性能网络 | Networked Systems for Machine Learning | FIK3221 | 7.5 | 无 PDF 课纲（third-cycle） | ✅ |

**抓取失败的项**：无（17/17 全部成功，无需登录）。唯一「不完整」的是 FIK3221 没有 `Course syllabus (term–)` 抬头与 PDF，属页面本身不提供，非抓取失败。

**方法备注**：KTH 的课程检索页 `https://www.kth.se/student/kurser/sokkurs?l=en` 是纯前端渲染，`curl` 只能拿到 41KB 的空壳；其内部接口 `https://www.kth.se/student/kurser/intern-api/sok/sokUtbildningsinstans?pattern=...` 需要一组受限参数，直接调用返回 `errorCode: "no-restrictions"` 且结果为空。所以本报告是**按课程代码直接抓课程页**（服务端渲染，HTML 里 `Specific prerequisites` 段可直接解析），课程代码来自 KTH 页面互相引用的先修链（如 ID1206 → DD1337/DD1338/IS1200；IK2215 → IK1552；FIK3221 → IK2215）。

---

## 任务 2：高性能网络作为技能点的依据（4 门公开课程）

> 说明：本次 Tavily 配额用尽（`/search HTTP 432: exceeds plan's set usage limit`），以下页面全部用 `curl` 直连抓取并人工核对，链接均验证过 HTTP 200（标 ⚠️ 的除外）。

### 2.1 University of Washington — CSE 561 Computer Communication and Networks（Autumn 2026）

- 课程主页：https://courses.cs.washington.edu/courses/cse561/26au/
- 教务目录页（先修原文出处）：https://courses.cs.washington.edu/courses/cse561/
- 授课：Ratul Mahajan，Mon/Wed 3:00–4:20 pm，CSE2 271

**先修要求原文（逐字）**

> Prerequisites: CSE or E E major and CSE 451 or equivalent.
> （逐字取自目录页 https://courses.cs.washington.edu/courses/cse561/ 的 "Prerequisites" 字段）

其中 **CSE 451 就是操作系统课**：https://courses.cs.washington.edu/courses/cse451/
> CSE451: Introduction to Operating Systems
> Catalog Description: Principles of operating systems. Process management, memory management, auxiliary storage management, resource allocation. No credit to students who have completed CSE 410. Prerequisite: CSE 351; CSE 332; CSE 333.

CSE 451 自己的先修（同样是逐字）：`CSE 351; CSE 332; CSE 333`，其中
- CSE 351 *The Hardware/Software Interface*：`Prerequisites: CSE 123 or CSE 143.`（计算机组成/底层抽象）
- CSE 333 *Systems Programming*：`Prerequisite: CSE 351.`（C/C++、显式内存管理）

⇒ **UW 的官方链条是：CSE 351（组成）→ CSE 333（系统编程）→ CSE 451（OS）→ CSE 561（网络）**，即高性能网络课的**硬先修就是操作系统**。这条链是本报告里最干净的一条可引用证据。

**课表讲次标题原文（Autumn 2026，直接抄录）**

| 日期 | 讲次标题（原文） | Deep read 论文（原文） |
|---|---|---|
| Oct 7 | `DC topology and network virtualization` | `VL2: A Scalable and Flexible Data Center Network`；shallow: `A Scalable, Commodity Data Center Network Architecture`、`Network Virtualization in Multi-tenant Datacenters` |
| Oct 12 | `Guest lecture: Flat network topologies` | `RNG: Flat Datacenter Networks at Scale`；shallow: `Jellyfish: Networking Data Centers Randomly`、`Xpander: Towards Optimal-Performance Datacenters` |
| Oct 14 | `Optical switching` | `Beyond the Mega-Data Center: Networking Multi-Data Center Regions` |
| Oct 19 | `Collective communication` | `TACCL: Guiding Collective Algorithm Synthesis using Communication Sketches`；shallow: `Demystifying NCCL: An In-depth Analysis of GPU Communication Protocols and Algorithms` |
| Oct 21 | `ML networks` | `RDMA over Ethernet for Distributed AI Training at Meta Scale`；shallow: `An Introduction to the InfiniBand Architecture`、`InfiniBand Credit-Based Link-Layer Flow-Control` |
| Oct 26 | `End host stack` | `Falcon: A Reliable, Low Latency Hardware Transport`；shallow: `Snap: A Microkernel Approach to Host Networking` |
| Oct 28 | `Guest lecture: Multipath Reliable Connection` | `Resilient AI Supercomputer Networking using MRC and SRv6` |
| Nov 16 | `Guest lecture: A whistlestop tour through AWS's networking evolution` | `Jupiter Evolving: Transforming Google's Datacenter Network via Optical Circuit Switches and Software-Defined Networking`、`Datacenter Networks Are In My Way` |
| Dec 2 | `Guest lecture: Network Switches and Interconnects – The Lego blocks of Network` | `Data Center Switch Architecture in the Age of Merchant Silicon` |

**覆盖情况**
- ✅ 数据中心拓扑（fat-tree / VL2 / Jellyfish / RNG / 光交换 OCS）
- ✅ RDMA（`RDMA over Ethernet ... at Meta Scale` 即 RoCE 部署）、InfiniBand（两篇 shallow read）
- ✅ kernel bypass / 用户态网络栈（`Snap: A Microkernel Approach to Host Networking`、`Falcon` 硬件 transport）
- ✅ SmartNIC 类（Falcon 属硬件卸载型传输层）
- ✅ 集合通信（GPU 上）：`TACCL`、`Demystifying NCCL`
- ❌ 课表里**没有**显式 DPDK 讲次，也没有 NVLink/NVSwitch 讲次
- ❌ 没有 DCQCN 讲次（Stanford CS244 的拥塞控制讲次也只讲经典 Internet CC，同样无 DCQCN，见 2.3）

---

### 2.2 KTH — FIK3221 Networked Systems for Machine Learning（third-cycle，7.5 credits）

- 课程页：https://www.kth.se/student/kurser/kurs/FIK3221?l=en

**先修要求原文（逐字）**

> Knowledge in advanced Internet technique, 7.5 higher education credits, equivalent completed course IK2215. Knowledge and skills in programming in C++, Java or Python, 6 higher education credits, equivalent completed course DD1310-DD1319/DD1331/DD1337/DD100N/ID1018.

**覆盖情况（Course contents 逐字，见任务 1 的 f-4）**：`Kernel bypass technologies (e.g. DPDK) for networks with over 100 gigabits per second` → ✅ DPDK / kernel bypass；`Offloading to Smart Network Interface Cards (SmartNIC)` → ✅ SmartNIC；`remote direct memory access (RDMA)` → ✅ RDMA；`Network aspects of machine learning inference using graphics processing units (GPUs)` → ✅ GPU 网络。
- ❌ 课纲没有点名 InfiniBand / RoCE / iWARP / NVLink（RDMA 是唯一被点名的具体协议族）
- ✅ 先修**不要求操作系统课**，只要求 IK2215（高级互联网技术）

---

### 2.3 Stanford — CS 244 Advanced Topics in Networking（Spring 2025）

- 课程主页：https://web.stanford.edu/class/cs244/
- 授课：Philip Levis

**先修要求原文（逐字）**

> Prerequisites: This course assumes a basic understanding of topics in networking, such as packet-switching, routing, socket programming, and congestion control. It is also helpful to know how to program in Python. We suggest taking CS 144, EE 284, or equivalent. For a refresher, you could look at the textbook "Computer Networking: A Top-Down Approach" by J. Kurose and K. Ross or "Computer Networks: A Systems Approach" by L. Peterson and B. Davie.

⇒ 这类"研究型网络课"的先修是**基础网络（CS 144 级）**，**不点 OS**。对照 UW CSE 561（明确要 OS），说明「要不要把 OS 作为高性能网络的必须前置」在名校之间**并不统一**。

**课表讲次标题原文（Spring 2025 相关部分）**

| 日期 | 讲次标题（原文） | 论文（原文） |
|---|---|---|
| 4/18 | `LANs` | `A Scalable, Commodity Data Center Network Architecture`（Al-Fares et al., SIGCOMM 2008，即 fat-tree） |
| 4/21 | `LANs` | `Jupiter Evolving: Transforming Google's Datacenter Network via Optical Circuit Switches and Software-Defined Networking`（Poutievski et al., SIGCOMM 2022） |
| 4/23 | `Congestion Control` | `Congestion Avoidance and Control`（Jacobson and Karels, SIGCOMM 1988） |
| 4/25 | `Congestion Control` | `Analysis of the Increase and Decrease Algorithms for Congestion Avoidance in Computer Networks`（Chiu and Jain） |
| 4/30 | `Congestion Control` | `TCP Vegas`、`BBR`（Cardwell et al., ACM Queue 2016） |
| 5/5 | `Queueing` | `Analysis and simulation of a fair queueing algorithm`、`BBQ: a fast and scalable integer priority queue for hardware packet scheduling` |

**覆盖情况**
- ✅ 数据中心拓扑（fat-tree / Clos、Jupiter 光交换）
- ✅ 拥塞控制（但是**经典 Internet 拥塞控制**：Jacobson、Chiu-Jain、Vegas、BBR）
- ❌ 本学期的讲次里**没有** RDMA / DCQCN / DPDK / SmartNIC / NVLink

---

### 2.4 CMU — 15-712 Advanced and Distributed Operating Systems（Fall 2026）

- 课程主页：https://www.cs.cmu.edu/~15712/
- 课表：https://www.cs.cmu.edu/~15712/schedule.html
- 授课：David G. Andersen

**先修类原文（逐字，取自 Overview 段）**

> 15-712 is a PhD course in operating systems. ...
> This course assumes a basic familiarity with operating systems concepts.

**相关讲次（逐字）**

> `Fri 8/28 dga` — `Ensō: A Streaming Interface for NIC-Application Communication`（OSDI '23 Best Paper，readings: `Sadok23`）

**覆盖情况**
- ✅ 只覆盖 kernel bypass 的**NIC–应用接口**这一小角（Ensō 是用户态直接收发 NIC 队列的经典工作）
- ❌ RDMA / DPDK / SmartNIC / DC 拓扑 / NVLink 均**不在**本学期讲次里
- 用途：作为「**OS 视角**看网络 I/O 抽象」的补充证据，不作为「高性能网络课」的主证据

---

### 2.5 覆盖矩阵小结

| 主题 | UW CSE 561 (26au) | KTH FIK3221 | Stanford CS 244 (25sp) | CMU 15-712 (26fa) |
|---|---|---|---|---|
| RDMA（语义/实现） | ✅ Meta RoCE 论文 | ✅ 明确写进课纲 | ❌ | ❌ |
| InfiniBand | ✅（2 篇 shallow） | ❌ 未点名 | ❌ | ❌ |
| RoCE / RoCEv2 | ✅（RoCE 论文） | ❌ 未点名 | ❌ | ❌ |
| iWARP | ❌ | ❌ | ❌ | ❌ |
| DPDK | ❌ | ✅ 明确写进课纲 | ❌ | ❌ |
| kernel bypass | ✅（Snap/Falcon） | ✅ | ❌ | ✅（Ensō） |
| zero-copy | 间接（Snap / Falcon / RDMA） | 间接（RDMA 定义内含） | ❌ | 间接（Ensō） |
| SmartNIC | ✅（Falcon） | ✅ 明确写进课纲 | ❌ | ❌ |
| NVLink / NVSwitch | ❌ | ❌（只写 GPU 网络） | ❌ | ❌ |
| DC 拓扑 fat-tree/Clos | ✅（VL2 / fat-tree / Jupiter） | ❌ | ✅（fat-tree / Jupiter） | ❌ |
| 拥塞控制 DCQCN | ❌ | ❌ | ❌（只讲经典 CC） | ❌ |
| 集合通信 / NCCL | ✅ | ❌ | ❌ | ❌ |

**结论（诚实版）**：没有任何**一门**课把题目列的 10 个关键词全讲到。**RDMA + kernel bypass + SmartNIC + DC 拓扑 + GPU 网络**这 5 块，UW CSE 561（26au）一门就覆盖 4 块半；DPDK 只有 KTH FIK3221 明写；NVLink/NVSwitch 与 DCQCN 需要靠官方文档 + 论文补，不属于任何一门的课表内容。

---

### 2.6 免费权威学习资料（链接均已验证 200，⚠️ 标注者除外）

**RDMA**
- NVIDIA《RDMA Aware Networks Programming User Manual》v17（verbs 编程手册，官方免费 HTML）：https://docs.nvidia.com/networking/display/rdmaawareprogrammingv17
- IBTA 官方规范（InfiniBand Architecture Specification，含 RoCE / RoCEv2 Annex）：https://www.infinibandta.org/ibta-specification/
- iWARP：IETF RFC 5040（+ RFC 5041/5042/5043/5044 系列）：https://datatracker.ietf.org/doc/rfc5040/

**DPDK / kernel bypass / zero-copy**

- DPDK 官方文档总入口：https://doc.dpdk.org/guides/
- DPDK Programmer's Guide（含 PMD、hugepage、zero-copy、mbuf 设计）：https://doc.dpdk.org/guides/prog_guide/
- （官方**没有**中文版：`https://doc.dpdk.org/guides-zh/prog_guide/` 返回 404）

**数据中心网络 / 拓扑**

- Fat-tree 原始论文免费 PDF（Al-Fares, Loukissas, Vahdat, SIGCOMM 2008；已用 `pdftotext` 核对首页标题 = `A Scalable, Commodity Data Center Network Architecture`）：http://ccr.sigcomm.org/online/files/p63-alfares.pdf
- ACM DOI 记录（浏览器可开，curl 直连被反爬 403 ⚠️）：https://dl.acm.org/doi/10.1145/1402958.1402967

**拥塞控制（DCQCN）**

- Microsoft Research 官方论文页（SIGCOMM 2015, "Congestion Control for Large-Scale RDMA Deployments"）：https://www.microsoft.com/en-us/research/publication/congestion-control-for-large-scale-rdma-deployments/
- ACM DOI（curl 403 ⚠️）：https://dl.acm.org/doi/10.1145/2785956.2787484

**RPC / 端主机栈**

- eRPC（NSDI 2019）USENIX 官方页（含 PDF 与 slides）：https://www.usenix.org/conference/nsdi19/presentation/kalia

**GPU 互连**

- NVIDIA NVLink 官方页：https://www.nvidia.com/en-us/data-center/nvlink/

**中文资料（可验证的）**

- 阿里云《弹性 RDMA（eRDMA）》官方中文文档（讲了 RDMA 相对 TCP/IP 的拷贝开销、协议栈处理、上下文切换问题、自研 CC 算法）：https://help.aliyun.com/zh/ecs/user-guide/erdma-overview
- openEuler 中文文档站（含内核/RDMA 相关文档入口）：https://docs.openeuler.org/zh/
- 说明：**没有**找到可验证的、系统讲 RDMA/DPDK 的中文教材或中文公开课页面（Tavily 配额耗尽后无法继续检索，这一点属于**未完成**，不要当作「中文资料不存在」的结论）。

---

### 2.7 建议：技能树里怎么挂

#### 建议 1 个技能，不拆 2 个

**技能名建议**：`C.x 数据中心与高性能网络（Data Center & High-Performance Networking）`

理由：

1. **有现成的一门课作为锚点**：KTH FIK3221 把 kernel bypass(DPDK) + SmartNIC + RDMA + GPU 网络 + 数据中心负载均衡打包成一门 7.5 hp 课，官方课纲就是这个技能的内容清单。
2. **拓扑与协议不可分**：UW CSE 561 的 10/7（DC topology）与 10/21（ML networks / RDMA）是同一门课相邻两周，拆成两个技能会产生重复的「数据中心」描述。
3. **拆开会缺人**：如果拆成「RDMA 编程」+「数据中心网络」，前者只有 KTH FIK3221 一门课支撑，后者只有 UW/Stanford 的拓扑部分，两边都单薄。

若一定要拆，建议拆成**同一技能下的两个模块**（不作为独立节点）：

- 模块 A：拓扑与拥塞（fat-tree/Clos、Jellyfish、OCS、DCQCN、集合通信）
- 模块 B：端主机与卸载（verbs/RDMA、DPDK/kernel bypass、zero-copy、SmartNIC、NVLink/GPUDirect）

#### 必须前置（按证据强度排序）

| 前置技能 | 建议 | 证据 |
|---|---|---|
| **C.3.2 网络协议、路由与传输** | **必须**（强） | KTH FIK3221 要求 IK2215 `Advanced Internetworking`；IK2220 要求 `passed IK2215`；Stanford CS 244 要求 `basic understanding of topics in networking ... We suggest taking CS 144, EE 284, or equivalent.` |
| **C.2.1 操作系统** | **必须**（强，但注意校际分歧） | UW CSE 561 目录原文 `CSE or E E major and CSE 451 or equivalent.`，CSE 451 = *Introduction to Operating Systems*；CMU 15-712 `assumes a basic familiarity with operating systems concepts`。**反例**：KTH FIK3221 与 Stanford CS 244 都**不要求** OS 课。→ 仍建议设必须，因为 verbs/DMA 注册、page pinning、用户态驱动都需要 OS 内存管理与驱动模型；但请把这条边标注为「UW/CMU 口径」。 |
| **C.1.1 计算机组成原理** | **必须**（中强） | KTH IK1203 先修含 `Knowledge in Boolean algebra corresponding completed course IE1204/IE1205/IS1500`；UW 链路的根是 CSE 351 *The Hardware/Software Interface*（`Prerequisites: CSE 123 or CSE 143.`）。PCIe/DMA/缓存一致性/NUMA 是 RDMA 与 SmartNIC 的前置物理知识。 |
| **C.2.4 并行与分布式系统** | **推荐，不建议设必须** | 三门课的先修原文里**都没有**出现它。但 `TACCL`、`Demystifying NCCL`、eRPC 的阅读门槛确实需要它。→ 用「推荐边」（虚线）表达。 |

> 若技能树要求「必须前置只能是硬证据」，那么**唯一无争议的必须前置是 C.3.2**；C.2.1 与 C.1.1 建议标为必须，但在节点说明里附上「依据 UW CSE 561 / KTH IK1203」的出处，让观众能自己核对。

#### 建议的 4–6 个必学知识项

1. **数据中心拓扑与交换架构**：fat-tree / Clos、VL2、Jellyfish / RNG 随机正则图、光路交换（Jupiter OCS）—— 对应 UW 10/7、10/12、10/14；Stanford 4/18、4/21。
2. **RDMA 语义与三种落地**：verbs 编程模型（QP/CQ/MR）、RC/UD、InfiniBand vs RoCEv2 vs iWARP 的差异与取舍 —— 对应 KTH FIK3221 课纲、UW 10/21。
3. **数据中心拥塞控制与负载均衡**：DCQCN、PFC/ECN、集中式调度与 ECMP —— 课表未直接覆盖，须用 MSR 的 DCQCN 论文 + IBTA 规范补；UW 课里的 `InfiniBand Credit-Based Link-Layer Flow-Control` 是链路层信用流控的入口。
4. **内核旁路与零拷贝端主机栈**：DPDK PMD、hugepage、AF_XDP/io_uring、Snap/Ensō 类用户态协议栈 —— 对应 KTH FIK3221 课纲、UW 10/26、CMU 8/28。
5. **SmartNIC / DPU 与卸载**：可编程流水线、硬件 transport（Falcon）、卸载边界在哪里 —— 对应 KTH FIK3221 课纲、UW 10/26。
6. **GPU 互连与集合通信**：NVLink/NVSwitch、PCIe P2P、GPUDirect RDMA、NCCL 的 ring/tree —— 对应 UW 10/19（TACCL / NCCL）；NVLink 本身需靠 NVIDIA 官方页补。

（可选第 7 项：**可编程数据平面与网络内计算**（P4/INT），对应 KTH IK2220 的 SDN 线；不列进 6 项以内，避免技能点过宽。）

#### 一句话结论

把「高性能网络」挂成**一个**技能节点、**必须前置 = C.3.2 网络 + C.2.1 OS + C.1.1 组成**（C.2.4 用推荐边），下设 6 个知识项；其中 **RDMA / 内核旁路 / SmartNIC** 有 KTH FIK3221 课纲直接背书，**DC 拓扑 / 集合通信** 有 UW CSE 561 课表直接背书，**NVLink 与 DCQCN** 只能靠厂商文档/IBTA 规范/论文补，**iWARP 没有任何一门课覆盖**（只能引 RFC 5040 系列）。

---

## 附：本次调研的失败与未完成项（如实列出）

1. **Tavily 搜索配额耗尽**：所有 `tavily_search` 调用返回 `HTTP 432: This request exceeds your plan's set usage limit`。任务 1/2 全部改用 `curl` 直连 + 本地解析完成，没有影响主结论，但**无法做「广度」检索**（例如"还有哪些大学开了数据中心网络课"、"中文教材/中文公开课"）。
2. **KTH 官方课程检索页 `/student/kurser/sokkurs` 不可抓**：纯前端渲染，`curl` 只得 41 KB 空壳；内部 API `/student/kurser/intern-api/sok/sokUtbildningsinstans` 缺参数时返回 `errorCode: "no-restrictions"` 且结果为空数组。→ 改用"按课程代码直接抓课程页"策略。
3. **ETH Zurich 课程页 / TUM DPOMH 课程页**：`systems.ethz.ch` 对未登录请求只返回导航壳（内容被剥离）；`db.in.tum.de` 直接 403。→ 放弃 ETH/TUM 这两门本来很适合"Data Processing on Modern Hardware"（含 RDMA/SmartNIC/DPDK 讲次）的候选课，**没有**写进报告，也没有编造其课表。
4. **MIT 6.829**：官网已迁至 Canvas，`web.mit.edu/6.829/www/` 返回 403，`currentsemester/index.html` 只剩一句 "We have moved to Canvas."。→ 放弃。
5. **Princeton COS 561**：可用镜像只有 `fall20` 版且页面无正式先修表述，`fall21` 403、其余年份 404。→ 放弃。
6. **CMU 15-744 / Berkeley CS 268 (2019)**：前者 404，后者页面存在但全文 **0 次**出现 RDMA / datacenter / InfiniBand。→ 放弃。
7. **FIK3221 无 PDF 课纲**：该 third-cycle 课程页面不提供 `Course syllabus (term–)` 抬头与 kursplan PDF，只有正文段落；因此无法给出"课纲版本/学期"，这属页面自身限制，非抓取失败。
8. **中文资料未穷尽**：只验证了阿里云 eRDMA 与 openEuler 两个入口；DPDK 官方无中文版（`guides-zh` 404）。中文教材/中文课程**未检索**，不要据此下结论。
