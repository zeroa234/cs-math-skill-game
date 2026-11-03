# 归档的旧内容包（不在游戏里）

2026-11-03 从 `data/content/` 挪到 `data/content-legacy/`，2026-11-04 和它们用到的组件一起挪到这里（见 `archive/README.md`）。这 13 个包是早期写的 version 1 旧写法：一课先讲完再练、讲解短、没有术语表，也没有对照 skill-tree 大纲查过漏讲。它们不满足 `docs/content-authoring.md` 的两条标准（写给零基础、知识覆盖面）。

游戏不读这个目录。这 13 个技能现在和其他没有互动课的技能一样显示为“开发中”，只供自学。

谁写的：A.2.3、M.5.3、F.1.2 由主代理编写（M.5.3、F.1.2 的每个数字都用 Python 算过，图算法题另用 networkx 独立核对），其余由 pi 子代理起草、主代理逐题复核（修正记录见 git 提交信息）。C.3.5 的每个事实都核对过原文（fat-tree、DCQCN、Falcon、NCCL 等论文，NVIDIA DOCA RDMA 指南，RFC 5040，DPDK 文档），数字（如 48 端口胖树 27,648 台主机、Ring AllReduce 每卡发送 2(k−1)/k·S）都用 Python 算过，没写各代 NVLink 带宽。

| 技能 | 课 |
|---|---|
| A.2.1 监督、无监督与半监督学习 | 5 |
| A.2.3 深度学习 | 4 |
| C.3.2 网络协议、路由与传输 | 4 |
| C.3.5 数据中心与高性能网络 | 6 |
| F.1.2 算法分析与设计 | 9 |
| M.1.1 极限与连续 | 4 |
| M.1.2 一元微分学 | 4 |
| M.1.3 一元积分学 | 3 |
| M.1.4.1 多元微分学 | 9 |
| M.3.1 线性代数 | 6 |
| M.5.3 证明方法与离散结构 | 6 |
| M.6.1 概率论 | 5 |
| P.2.3 Python与科学计算工具 | 4 |

**以后重写某个技能时**：可以参考这里的事实、例题和上面说的已经核对过的数字（提交记录里有核对方法），但不要照它的写法写。按 `docs/content-authoring.md` 先写覆盖表 `reports/coverage/<技能ID>.md`，再写 `version: 2` 的新包放进 `data/content/`，并写 `tests/content/<技能ID>.verify.py` 核对每个数。新包写好后把这里的旧文件删掉。

这些旧包对照零基础标准的差距，最后一次统计在提交 97c3236d 的 `reports/beginner-audit.md`（`git show 97c3236d:projects/cs-math-skill-game/reports/beginner-audit.md`）。

它们用到的 7 种交互组件（函数图像、2×2 矩阵、抽样、梯度下降、单个神经元、小神经网络、k-means）和图组件的 Dijkstra、拓扑排序、最大流也归档了（`archive/src/game/sims/`，参数表在 `archive/README.md`），重写时挪回游戏再用。
