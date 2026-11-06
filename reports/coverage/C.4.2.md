# C.4.2 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1 | Cloud Overview. Internet of Things and the Cloud IoT Edge | `models` |
| 2 | Scalability and Key-Value Sharding | `elasticity` |
| 3 | Stateless Programming | `serverless` |
| 4 | Customizable platform services. | `models` |
| 5 | Strongly Consistent Geoscale Computing | `availability` |
| 6 | Case studies in disaster: How datacenter gossip can go wrong! | `availability` |
| 7 | Privacy in Cloud Computing | `tenants` |
| 8 | Fault tolerance in practice | `availability` |
| 9 | Wrapup: How the Business of Cloud Computing Shapes the Future of Cloud Computing | `cost` |
| 10.1 | Abstract Interaction Dynamics | `models` |
| 10.2 | Software Stack and Provider/Consumer Scope of Control | `models` |
| 10.3 | Benefits | `models` |
| 10.4 | Issues and Concerns | `models` |
| 10.5 | Candidate Application Classes | `models` |
| 10.6 | Recommendations for Platform as a Service | `models` |
| 11.1 | Abstract Interaction Dynamics | `models` |
| 11.2 | Software Stack and Provider/Consumer Scope of Control | `models` |
| 11.3 | Operational View | `models` |
| 11.4 | Benefits | `elasticity` |
| 11.5 | Issues and Concerns | `tenants` |
| 11.6 | Recommendations for Infrastructure as a Service | `tenants` |
| 12.1 | Computing Performance | `elasticity` |
| 12.2 | Cloud Reliability | `availability` |
| 12.3 | Economic Goals | `cost` |
| 12.4 | Compliance | `tenants` |
| 12.5.1 | Multi-tenancy | `tenants` |
| 13.1 | Nodes | `cluster` |
| 13.2 | Communication between Nodes and the Control Plane | `cluster` |
| 13.3 | Controllers | `cluster` |
| 13.4 | Cloud Controller Manager | `cluster` |
| 14.1 | Pods | `cluster` |
| 14.2.1 | Deployments | `workloads` |
| 14.2.2 | ReplicaSet | `workloads` |
| 14.2.3 | StatefulSets | `workloads` |
| 14.2.4 | DaemonSet | `workloads` |
| 14.2.5 | Jobs | `workloads` |
| 14.2.6 | CronJob | `workloads` |
| 14.3.1 | Horizontal Pod Autoscaling | `workloads` |
| 15.1 | Kubernetes Scheduler | `cluster` |

## 核心主题、综合练习与后继技能

CS2023 的 SaaS 和弹性供给分别见 `models` 和 `elasticity` / `workloads`。原综合练习依次由 `models` / `serverless`、`elasticity`、`cost`、`serverless`、`availability` 准备。课程用教学费率及容量模型，控制平面和隔离按 [Kubernetes 工作负载文档](https://kubernetes.io/docs/concepts/workloads/) 与 [多租户文档](https://kubernetes.io/docs/concepts/security/multi-tenancy/) 核对。服务模型参考 [NIST SP 800-145](https://csrc.nist.gov/pubs/sp/800/145/final)，可扩展性和可靠性案例参考 [Cornell CS5412](https://www.cs.cornell.edu/courses/cs5412/2022fa/)。
