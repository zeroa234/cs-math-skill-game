# C.4.2 云计算：覆盖表

**状态（2026-11-17）：已写完。** 依据 `../cs-math-skill-tree/data/outlines/C.4.2.json` 与 `../cs-math-skill-tree/output/outlines.json`，主来源为 Cornell CS5412（Fall 2022）、NIST SP 800-146（第 6–8 章）与 Kubernetes Concepts 文档；补充参考河海大学《云计算技术与应用》、Kubernetes 官方中文文档（多租户、HPA）与阿里云函数计算文档。游戏内部章序：`1. IaaS/PaaS`、`2. 弹性`、`3. 多租户`、`4. 编排`、`5. 无服务器与成本模型`。

必须前置为 `C.2.2 系统编程与并发同步`（及其传递前置 `P.1.1`、`P.2.2`、`C.1.1`）：可直接假设程序、函数、进程、线程、地址空间、锁、信号量、文件描述符、套接字、字节与十六进制。`C.2.1 操作系统`、`C.2.3 容器与虚拟化`、`C.3.2 网络协议`、`C.4.1 分布式系统` 仅是推荐前置，因此虚拟机/容器、命名空间、负载均衡、区域与可用区、分片、一致性权衡、弹性伸缩与按量计费均在本包内从零讲起。

`node scripts/check-coverage.mjs C.4.2` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1 | A:1. Cloud Overview. Internet of Things and the Cloud IoT Edge | `iaas-foundation`、`paas-saas-edge` |
| 2 | A:2. Scalability and Key-Value Sharding | `sharding-stateless` |
| 3 | A:3. Stateless Programming | `sharding-stateless`、`serverless-faas` |
| 4 | A:4. Customizable platform services. | `paas-saas-edge` |
| 5 | A:11. Strongly Consistent Geoscale Computing | `availability-geoscale` |
| 6 | A:13. Case studies in disaster: How datacenter gossip can go wrong! | `availability-geoscale` |
| 7 | A:17. Privacy in Cloud Computing | `privacy-compliance` |
| 8 | A:24. Fault tolerance in practice | `availability-geoscale` |
| 9 | A:28. Wrapup: How the Business of Cloud Computing Shapes the Future of Cloud Computing | `cloud-economics` |
| 10.1 | B:6.1 Abstract Interaction Dynamics | `paas-saas-edge` |
| 10.2 | B:6.2 Software Stack and Provider/Consumer Scope of Control | `paas-saas-edge` |
| 10.3 | B:6.3 Benefits | `paas-saas-edge` |
| 10.4 | B:6.4 Issues and Concerns | `paas-saas-edge`、`multitenancy-isolation` |
| 10.5 | B:6.5 Candidate Application Classes | `paas-saas-edge` |
| 10.6 | B:6.6 Recommendations for Platform as a Service | `paas-saas-edge` |
| 11.1 | B:7.1 Abstract Interaction Dynamics | `iaas-foundation` |
| 11.2 | B:7.2 Software Stack and Provider/Consumer Scope of Control | `iaas-foundation` |
| 11.3 | B:7.3 Operational View | `iaas-foundation` |
| 11.4 | B:7.4 Benefits | `elasticity-capacity` |
| 11.5 | B:7.5 Issues and Concerns | `multitenancy-isolation` |
| 11.6 | B:7.6 Recommendations for Infrastructure as a Service | `iaas-foundation` |
| 12.1 | B:8.1 Computing Performance | `elasticity-capacity` |
| 12.2 | B:8.2 Cloud Reliability | `availability-geoscale` |
| 12.3 | B:8.3 Economic Goals | `cloud-economics` |
| 12.4 | B:8.4 Compliance | `privacy-compliance` |
| 12.5.1 | B:8.5.4 Multi-tenancy | `multitenancy-isolation` |
| 13.1 | C Nodes | `k8s-architecture` |
| 13.2 | C Communication between Nodes and the Control Plane | `k8s-architecture` |
| 13.3 | C Controllers | `k8s-architecture` |
| 13.4 | C Cloud Controller Manager | `k8s-architecture` |
| 14.1 | C Pods | `k8s-workloads` |
| 14.2.1 | C Deployments | `k8s-workloads` |
| 14.2.2 | C ReplicaSet | `k8s-workloads` |
| 14.2.3 | C StatefulSets | `k8s-workloads` |
| 14.2.4 | C DaemonSet | `k8s-workloads` |
| 14.2.5 | C Jobs | `k8s-workloads` |
| 14.2.6 | C CronJob | `k8s-workloads` |
| 14.3.1 | C Horizontal Pod Autoscaling | `elasticity-capacity` |
| 15.1 | C Kubernetes Scheduler | `k8s-architecture` |

## CS2023 核心主题（C2）

依据 `../cs-math-skill-tree/data/curation/scope.json`：

| 主题 | KA / 要求 | 课 |
|---|---|---|
| Software as a Service (SaaS) | SPD-Web · KA Core | `paas-saas-edge` |
| Clusters, clouds; elastic provisioning | PDC-Programs · KA Core | `elasticity-capacity`、`k8s-architecture` |

## 学习资源的章节（C3）

| 来源 | 章节与概念 | 课 / 说明 |
|---|---|---|
| `zh1` 河海大学《云计算技术与应用》 | IaaS/PaaS/SaaS 服务体系、虚拟化、分布式存储与平台应用 | `iaas-foundation`、`paas-saas-edge`、`sharding-stateless` |
| `en1` Cornell CS5412 | 云概述与 IoT Edge、键值分片、无状态编程、可定制平台、跨地域强一致、gossip 故障案例、隐私、容错、云商业模式 | `iaas-foundation`、`paas-saas-edge`、`sharding-stateless`、`availability-geoscale`、`privacy-compliance`、`serverless-faas`、`cloud-economics` |
| `r7-zh1` Kubernetes 官方中文文档（多租户、HPA） | 共享/独立命名空间与 RBAC/NetworkPolicy/资源配额/独立集群三种隔离权衡；HPA 利用率与期望副本数计算 | `multitenancy-isolation`、`elasticity-capacity` |
| `r7-zh2` 阿里云函数计算文档 | 事件驱动全托管 FaaS、Serverless vs Serverful、CU/GB-s 用量与常驻实例对比 | `serverless-faas`、`cloud-economics` |
| `r7-en1` Kubernetes Multi-tenancy | Control-plane vs data-plane isolation、shared vs dedicated cluster cost/isolation trade-offs | `multitenancy-isolation` |

## 综合练习（C4）

| 小题 | 要用到的 | 课 |
|---|---|---|
| (1) IaaS、PaaS、SaaS、FaaS 的区别、例子与共享责任模型 | 四种模型的软件栈控制边界、“云本身的安全”与“云中内容的安全” | `iaas-foundation`、`paas-saas-edge`、`serverless-faas` |
| (2) 每实例 200 req/s、目标利用率 70%、峰值 5000 req/s 需要多少实例 | 有效容量 = 上限 × 目标利用率，向上取整得出副本数 | `elasticity-capacity` |
| (3) 按需 $0.10/h 与预留 $0.06/h：基线 10 台 7×24 + 高峰 20 台每天 4h（30 天）最省组合与节省额 | 预留给基线、按需给波峰、全按需与全预留对照 | `cloud-economics` |
| (4) 为什么云原生服务要无状态？会话、上传文件、数据库放在哪 | 无状态水平扩缩与故障替换、外部缓存/对象存储/托管数据库 | `sharding-stateless` |
| (5) 区域与可用区定义；承受单个可用区故障的 Web 应用设计 | 区域与独立供电/网络可用区、多可用区负载均衡、自动伸缩组、主备同步复制与对象存储+CDN | `availability-geoscale` |

## 后继技能（C5）

`unlocks` 为空，全树无技能以 `C.4.2` 为必须前置。`S.2.4 云安全与容器安全` 将 `C.4.2` 列为推荐前置，并在其综合练习第 (1) 题考查 IaaS 共享责任模型下用户负责哪些安全；本包在 `iaas-foundation`、`multitenancy-isolation` 与 `privacy-compliance` 已把控制范围、共享责任、租户隔离和审计边界讲清。
