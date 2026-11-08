# C.2.3 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Container images | `images`, `docker-build`, `registry` |
| 1.2 | Container runtimes | `images`, `isolation` |
| 2.1 | Kubernetes Scheduler | `schedule` |
| 2.2 | Running Multiple Schedulers | `schedule` |
| 2.3 | Assigning Pods to Nodes | `placement` |
| 2.4 | Pod Overhead | `requests` |
| 2.5 | Pod Topology Spread Constraints | `placement` |
| 2.6 | Taints and Tolerations | `placement` |
| 2.7 | Scheduling Framework | `schedule` |
| 2.8 | Pod Scheduling Readiness | `placement` |
| 2.9 | Pod Priority and Preemption | `eviction` |
| 2.10 | Node-pressure Eviction | `eviction` |
| 2.11 | API-initiated Eviction | `eviction` |
| 3.1 | Requests and limits | `requests` |
| 3.2 | Resource types | `controllers`, `requests` |
| 3.3 | Huge pages | `controllers` |
| 3.4 | Resource requests and limits of Pod and container | `requests` |
| 3.5 | Pod-level resource specification | `requests` |
| 3.6 | Resource units in Kubernetes | `requests` |
| 3.7 | How Pods with resource requests are scheduled | `requests`, `schedule` |
| 3.8 | How Kubernetes applies resource requests and limits | `cpu-memory`, `requests` |
| 3.9 | Resizing container resources | `controllers` |
| 3.10 | Local ephemeral storage | `controllers` |
| 3.11 | Extended resources | `controllers` |
| 3.12 | PID limiting | `controllers` |
| 4 | OS structure, Virtual Machines | `machines`, `traps` |
| 5.1 | What is cgroup? | `groups` |
| 6.1 | Weights | `groups` |
| 6.2 | Limits | `groups`, `cpu-memory` |
| 6.3 | Protections | `groups`, `cpu-memory` |
| 6.4 | Allocations | `groups`, `controllers` |
| 7.1 | CPU | `cpu-memory` |
| 7.2 | Memory | `cpu-memory` |
| 7.3 | IO | `controllers` |
| 7.4 | PID | `controllers` |
| 7.5 | Cpuset | `controllers` |
| 8.1 | The Root and Views | `cgroup-view` |
| 8.2 | Migration and setns(2) | `cgroup-view` |

## 学习资源与综合练习

- `machines`、`traps` 覆盖宿主与客体、两类 VMM、Popek–Goldberg 的经典可虚拟化条件、陷入模拟、软件翻译与硬件辅助，两级地址翻译对应原练习 1 和 5。启动时间和大小按工作负载讨论。[Harvard CS 161 虚拟机讲义](https://read.seas.harvard.edu/cs161/2019/lectures/lecture23/)
- `isolation`、`cgroup-view`、`groups` 解释六类命名空间与控制组，给出 `unshare` 和 Docker 限制例子。`cpu-memory` 对应原练习 2 和 4，核对 8 核主机的 CPU 配额、4 GiB 上限、回收与节流。[Linux namespaces 手册](https://man7.org/linux/man-pages/man7/namespaces.7.html) · [Linux cgroup v2 文档](https://docs.kernel.org/admin-guide/cgroup-v2.html)
- `images`、`docker-build`、`registry` 对应原练习 3，包含 Dockerfile、构建缓存、数据卷、端口、镜像仓库、摘要、多平台 Buildx 与 Compose 的用途。[Docker 构建缓存指南](https://docs.docker.com/build/cache/optimize/) · [Kubernetes 镜像](https://kubernetes.io/docs/concepts/containers/images/)
- `requests`、`schedule`、`placement`、`eviction` 对照 Kubernetes 的资源、放置与驱逐内容。实际调度按申请量和限制条件，区别优先级抢占、节点压力驱逐和维护驱逐。[Kubernetes 资源管理](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) · [Kubernetes 调度器](https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/)
- CS2023 的 OS-Virtualization 虚拟机与容器比较、虚拟化和隔离分别见 `machines`、`traps`、`isolation`、`cgroup-view`，SF-Resource 的资源分配与调度见 `groups`、`cpu-memory`、`schedule`。上游无必须后继。DevOps 工作流已介绍构建镜像，本技能补上镜像运行、限额与调度。
