# 归档的旧内容包（不在游戏里）

2026-11-03 从 `data/content/` 挪到 `data/content-legacy/`，2026-11-04 和它们用到的组件一起挪到这里（见 `archive/README.md`）。原来有 13 个包，都是早期写的 version 1 旧写法：一课先讲完再练、讲解短、没有术语表，也没有对照 skill-tree 大纲查过漏讲。它们不满足 `docs/content-authoring.md` 的两条标准（写给零基础、知识覆盖面）。

游戏不读这个目录。已经按新标准重写的技能，旧包按下面的规定删掉了：M.1.1、M.1.2、M.3.1、P.2.3、M.5.3、F.1.2（2026-11-04 删，旧文件在提交 d48c5baa 及以前的历史里）。C.3.2 的旧包在 2026-11-07 重写完成后删除。其余旧包保留作历史参考。人工智能远征使用 `data/content/` 下的新版课程，C.3.5 仍可通过技能页自学。

谁写的：A.2.3（以及已删的 M.5.3、F.1.2）由主代理编写，其余由 pi 子代理起草、主代理逐题复核（修正记录见 git 提交信息）。C.3.5 的每个事实都核对过原文（fat-tree、DCQCN、Falcon、NCCL 等论文，NVIDIA DOCA RDMA 指南，RFC 5040，DPDK 文档），数字（如 48 端口胖树 27,648 台主机、Ring AllReduce 每卡发送 2(k−1)/k·S）都用 Python 算过，没写各代 NVLink 带宽。

| 技能 | 课 |
|---|---|
| A.2.1 监督、无监督与半监督学习 | 5 |
| A.2.3 深度学习 | 4 |
| C.3.5 数据中心与高性能网络 | 6 |
| M.1.3 一元积分学 | 3 |
| M.1.4.1 多元微分学 | 9 |
| M.6.1 概率论 | 5 |

**以后重写某个技能时**：可以参考这里的事实、例题和上面说的已经核对过的数字（提交记录里有核对方法），但不要照它的写法写。按 `docs/content-authoring.md` 先写覆盖表 `reports/coverage/<技能ID>.md`，再写 `version: 2` 的新包放进 `data/content/`，并写 `tests/content/<技能ID>.verify.py` 核对每个数。新包写好后把这里的旧文件删掉。

这些旧包对照零基础标准的差距，最后一次统计在提交 97c3236d 的 `reports/beginner-audit.md`（`git show 97c3236d:projects/cs-math-skill-game/reports/beginner-audit.md`）。

它们用到的交互组件（函数图像、2×2 矩阵、抽样、梯度下降、单个神经元、小神经网络、k-means，图组件的 Dijkstra、拓扑排序、最大流）已经全部挪回游戏（参数表在 `docs/content-authoring.md`），实验室条目在 `src/game/app/lab.js`。
