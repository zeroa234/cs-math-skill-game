# C.2.3 虚拟化、容器与资源管理：覆盖表

**状态（2026-11-17）：已写完。** 依据 `../cs-math-skill-tree/data/outlines/C.2.3.json` 与 `../cs-math-skill-tree/output/outlines.json`，主来源为 MIT 6.033（LEC 6 虚拟机）、Linux Kernel cgroup v2 文档与 Kubernetes Concepts（Containers、Scheduling/Preemption/Eviction、Resource Management）；补充参考 Harvard CS 161（LEC 23）、《Docker 从入门到实践》、iximiuz *Learning Containers From The Bottom Up* 与 man 7 namespaces。游戏内部章序：`1. 虚拟机`、`2. 容器隔离`、`3. 资源控制`、`4. 调度和镜像运行`。

必须前置为 `C.2.1 操作系统`（及其传递前置 `P.1.1`、`P.2.2`、`F.1.1`、`C.1.1`）：可直接假设进程、地址空间、用户态/内核态、陷入、陷入表、页表、缺页、时钟中断、调度与文件系统 inode。本包在此之上从零讲清虚拟机监控程序、Trap-and-Emulate、VT-x/EPT 二维页表、六类 Linux 命名空间、cgroup v2、Dockerfile 分层、非 root 安全、资源请求/限制与 K8s 调度驱逐。

`node scripts/check-coverage.mjs C.2.3` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | A Container images | `container-images`、`image-registry-digest` |
| 1.2 | A Container runtimes | `containers-vs-vms`、`container-images`、`image-registry-digest` |
| 2.1 | A Kubernetes Scheduler | `k8s-scheduler-placement` |
| 2.2 | A Running Multiple Schedulers | `k8s-scheduler-placement` |
| 2.3 | A Assigning Pods to Nodes | `k8s-scheduler-placement` |
| 2.4 | A Pod Overhead | `k8s-scheduler-placement` |
| 2.5 | A Pod Topology Spread Constraints | `k8s-scheduler-placement` |
| 2.6 | A Taints and Tolerations | `k8s-scheduler-placement` |
| 2.7 | A Scheduling Framework | `k8s-scheduler-placement` |
| 2.8 | A Pod Scheduling Readiness | `k8s-scheduler-placement` |
| 2.9 | A Pod Priority and Preemption | `k8s-scheduler-placement` |
| 2.10 | A Node-pressure Eviction | `k8s-requests-limits` |
| 2.11 | A API-initiated Eviction | `k8s-requests-limits` |
| 3.1 | A Requests and limits | `k8s-requests-limits` |
| 3.2 | A Resource types | `k8s-requests-limits` |
| 3.3 | A Huge pages | `k8s-requests-limits` |
| 3.4 | A Resource requests and limits of Pod and container | `k8s-requests-limits` |
| 3.5 | A Pod-level resource specification | `k8s-requests-limits` |
| 3.6 | A Resource units in Kubernetes | `k8s-requests-limits` |
| 3.7 | A How Pods with resource requests are scheduled | `k8s-requests-limits` |
| 3.8 | A How Kubernetes applies resource requests and limits | `k8s-requests-limits` |
| 3.9 | A Resizing container resources | `k8s-requests-limits` |
| 3.10 | A Local ephemeral storage | `k8s-requests-limits` |
| 3.11 | A Extended resources | `k8s-requests-limits` |
| 3.12 | A PID limiting | `k8s-requests-limits` |
| 4 | B:LEC 6 OS structure, Virtual Machines | `vm-basics`、`vm-traps-ept` |
| 5.1 | C What is cgroup? | `cgroups-hierarchy` |
| 6.1 | C Weights | `cgroups-hierarchy` |
| 6.2 | C Limits | `cgroups-hierarchy` |
| 6.3 | C Protections | `cgroups-hierarchy` |
| 6.4 | C Allocations | `cgroups-hierarchy` |
| 7.1 | C CPU | `cpu-memory-io-pid` |
| 7.2 | C Memory | `cpu-memory-io-pid` |
| 7.3 | C IO | `cpu-memory-io-pid` |
| 7.4 | C PID | `cpu-memory-io-pid` |
| 7.5 | C Cpuset | `cpu-memory-io-pid` |
| 8.1 | C The Root and Views | `containers-vs-vms`、`linux-namespaces` |
| 8.2 | C Migration and setns(2) | `linux-namespaces` |

## CS2023 核心主题（C2）

| 主题 | KA / 要求 | 课 |
|---|---|---|
| Containers and their comparison to virtual machines | OS-Virtualization · KA Core | `vm-basics`、`containers-vs-vms` |
| Using virtualization and isolation | OS-Virtualization · KA Core | `vm-traps-ept`、`linux-namespaces` |
| Common resource allocation/scheduling algorithms | SF-Resource · CS Core | `cgroups-hierarchy`、`cpu-memory-io-pid`、`k8s-scheduler-placement` |

## 学习资源的章节（C3）

| 来源 | 章节与概念 | 课 / 说明 |
|---|---|---|
| `en1` iximiuz / `r7-en1` Harvard CS161 LEC 23 | Popek–Goldberg、Trap-and-Emulate、二进制翻译与 VT-x/EPT、Linux namespaces 与 cgroups 拼装容器 | `vm-basics`、`vm-traps-ept`、`containers-vs-vms`、`linux-namespaces` |
| `zh1`《Docker 从入门到实践》 | 镜像分层、Dockerfile 缓存顺序、仓库标签与摘要、非 root 运行与容器隔离 | `container-images`、`image-registry-digest` |
| `r7-zh1` / `r7-en2` Kubernetes Concepts | Requests/Limits、QoS 与驱逐、kube-scheduler 过滤与打分、污点容忍与抢占 | `k8s-requests-limits`、`k8s-scheduler-placement` |

## 综合练习（C4）

| 小题 | 要用到的 | 课 |
|---|---|---|
| (1) Type 1 / Type 2 hypervisor 与容器对比 | 隔离边界、启动耗时、镜像体积与是否共享宿主机内核 | `vm-basics`、`containers-vs-vms` |
| (2) namespaces（PID/NET/MNT/UTS/IPC/USER）与 cgroups 职责及 `unshare` / `--memory` | 看得见什么 vs 能吃多少资源 | `linux-namespaces`、`cgroups-hierarchy` |
| (3) 最小 Dockerfile 打包 Flask + `requirements.txt` 与缓存层顺序 | 先 `COPY requirements.txt` + `pip install` 再 `COPY .`、非 root `USER` | `container-images` |
| (4) 8 核 32 GB 主机上 `cpu.max="200000 100000"` 与 `memory.max=4G` 含义、超限结果 | 2 核配额、CPU 只节流不被杀、内存超限先回收页缓存再触发 OOM 杀手 | `cpu-memory-io-pid` |
| (5) VT-x / AMD-V 与 EPT / NPT 解决纯软件虚拟化的什么问题 | 消除敏感非特权指令漏洞、取消影子页表并由硬件完成两维地址翻译 | `vm-traps-ept` |

## 后继技能（C5）

`unlocks` 为空。推荐后继为 `C.4.2 云计算`、`S.2.4 云与基础设施安全` 与 `H.4.4 边缘计算`：`S.2.4` 综合练习直接考查非 root 运行、固定镜像版本与摘要、capabilities 裁剪、ResourceQuota/Requests/Limits 防耗尽及 K8s 资源声明，本包在 `image-registry-digest` 与 `k8s-requests-limits` 已提前做好完整铺垫。
