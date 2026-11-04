# F.1.2 算法分析与设计：覆盖表

规则见 `docs/content-authoring.md` 的“知识覆盖面标准”。依据：skill-tree 大纲 `../cs-math-skill-tree/data/outlines/F.1.2.json`：A = Dasgupta、Papadimitriou、Vazirani《Algorithms》（DPV，2006 年 7 月 18 日排版稿）的 0.2–0.3、第 2、5、6 章；B = Sedgewick、Wayne《Algorithms, 4th Edition》配套网站的 §1.4、§4.1–4.4、§5.2–5.4、§6.3–6.4；C = MIT 6.046J（2015 春）第 14 讲。共 35 节。“节”是技能内部编号，“原文”是原书的节号和标题。

必须前置是数据结构 F.1.1 和证明方法与离散结构 M.5.3，两站都已有内容包。这一站直接用它们教过的东西：数组、链表、栈、队列、哈希表、二叉树、二叉堆和优先队列、图的邻接表、BFS 和 DFS、摊还和翻倍扩容（F.1.1）；归纳和强归纳、反证、不变式、偏序和拓扑排序、递推式、归并排序的比较次数、对数、主定理的 $n^d$ 形式（M.5.3）。代码用程序设计基础 P.1.1 的 Python（F.1.1 的必须前置）。

`node scripts/check-coverage.mjs F.1.2` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | A 0.2 Enter Fibonacci | `fibonacci`, `recursion-iteration` |
| 1.2 | A 0.3 Big-O notation | `big-o` |
| 2.1 | A 2.1 Multiplication | `karatsuba` |
| 2.2 | A 2.2 Recurrence relations | `recursion-tree`, `master-theorem` |
| 2.3 | A 2.3 Mergesort | `sorting-bound` |
| 2.4 | A 2.4 Medians | `quickselect` |
| 2.5 | A 2.5 Matrix multiplication | `strassen` |
| 2.6 | A 2.6 The fast Fourier transform | `fft` |
| 3.1 | A 5.1 Minimum spanning trees | `mst-cut`, `union-find`, `prim` |
| 3.2 | A 5.2 Huffman encoding | `huffman` |
| 3.3 | A 5.3 Horn formulas | `horn` |
| 3.4 | A 5.4 Set cover | `set-cover` |
| 4.1 | A 6.1 Shortest paths in dags, revisited | `dag-dp` |
| 4.2 | A 6.2 Longest increasing subsequences | `lis` |
| 4.3 | A 6.3 Edit distance | `edit-distance`, `lcs` |
| 4.4 | A 6.4 Knapsack | `knapsack` |
| 4.5 | A 6.5 Chain matrix multiplication | `chain-matrix` |
| 4.6 | A 6.6 Shortest paths | `hops-tsp`, `floyd-warshall` |
| 4.7 | A 6.7 Independent sets in trees | `tree-independent-set` |
| 5.1 | B 1.4 Mathematical models | `count-steps` |
| 5.2 | B 1.4 Tilde approximations | `tilde` |
| 5.3 | B 1.4 Order-of-growth classifications | `growth-classes` |
| 5.4 | B 1.4 Worst-case performance guarantees | `growth-classes` |
| 5.5 | B 1.4 Amortized analysis | `amortized-counter`, `potential-method` |
| 5.6 | B 1.4 Memory usage | `memory` |
| 6.1 | B 4.1 Undirected Graphs | `components` |
| 6.2 | B 4.2 Directed Graphs | `topo-dfs`, `scc`, `floyd-warshall` |
| 6.3 | B 4.3 Minimum Spanning Trees | `mst-cut`, `union-find`, `prim` |
| 6.4 | B 4.4 Shortest Paths | `dijkstra`, `negative-edges`, `dag-dp` |
| 7.1 | B 5.2 Tries | `tries` |
| 7.2 | B 5.3 Substring Search | `substring-search`, `prefix-function`, `kmp-search` |
| 7.3 | B 5.4 Regular Expressions | `regex` |
| 8.1 | B 6.3 Suffix Arrays | `suffix-array` |
| 8.2 | B 6.4 Maxflow | `max-flow`, `min-cut`, `bipartite-matching` |
| 9 | C L14 Incremental Improvement: Matching | `bipartite-matching` |

另有一课不对应大纲的某一节：

- `activity-selection`（活动安排、贪心和交换论证）：原技能树综合练习 (3) 要求“按结束时间贪心并用交换论证说明为什么正确”，DPV 第 5 章用最小生成树的割性质讲交换，没有单独讲活动安排；技能的章列的 Erickson《Algorithms》第 4 章、Hello 算法第 15 章都从这类简单例子讲贪心。放在贪心一章的第一课，先把“贪心选择 + 交换论证”讲清，再学最小生成树。

教到什么深度（入门层）：
- 渐近分析讲到 DPV 0.3 的 $O$、$\Omega$、$\Theta$ 定义（带常数 $c$）和四条化简规则，algs4 §1.4 的代价模型、波浪号近似、倍增实验、七种增长阶、最好、平均、最坏情况和上界、下界、最优算法，以及按原书的 Java 模型估算内存。$o$、$\omega$ 和用极限判断阶不教：原书这几节都没有，属于实分析 M.1.6 的极限。
- 递归讲到 DPV 0.2 的两种斐波那契算法、调用栈和递归深度、递归和迭代互换（Hello 算法 2.2）、递归树求和和主定理的证明。原书的递推式求解只到主定理；Erickson 附录 II 的 Akra–Bazzi、换元法和“湮灭子”方法不教，M.5.3 已说明 Akra–Bazzi 是推广。
- 分治讲到 DPV 2.1–2.6：三次乘法（用十进制演示，原书用二进制）、比较排序的 $\log_2(n!)$ 下界、随机选择和“好的支点”、快速排序（原书 2.4 节末尾和习题 2.24 提到，后继技能 F.1.4 的综合练习要用，最坏和平均情况讲结论、不证）、分块矩阵乘法和 Strassen 只给子问题个数和递推式（7 个乘积的公式原书不推导，课里也不要求记）、FFT 讲到“在 ±x 成对的点上求值”的分治和为什么要用复数。FFT 的单位根矩阵、插值公式 $M_n(\omega)^{-1} = \frac1n M_n(\omega^{-1})$ 和蝶形电路不教，要用线性代数和复数的指数形式，属于信号处理一类的后继技能；课里只说它存在、作用是什么。
- 贪心讲到 DPV 5.1–5.4 全部：割性质和它的交换证明、Kruskal、并查集（按秩合并和路径压缩，$\log^* n$ 只讲是什么、不证）、Prim、Huffman 编码和前缀码、Horn 公式的“能不设就不设”算法、集合覆盖的贪心和 $k \ln n$ 的界（证明讲思路）。另加 Hello 算法的分数背包（按单价贪心，交换论证）和硬币找零的反例。熵的方框和随机最小割的方框不教：熵属于信息论，随机最小割属于随机、近似与在线算法 F.1.4。
- 动态规划讲到 DPV 6.1–6.7 的每一个问题：DAG 上的最短路、最长递增子序列、编辑距离、背包（可重复和不可重复，伪多项式）、矩阵链乘法、最多 $k$ 条边的最短路、Floyd–Warshall、旅行商的 $O(n^2 2^n)$、树上的最大独立集；另加最长公共子序列（综合练习 (2)）和记忆化。摊还分析讲到 algs4 的“对一串操作的最坏情况保证”和三种方法（聚合、记账、势能），例子是二进制计数器、多次弹出的栈和翻倍扩容。
- 图的遍历在 F.1.1 的 BFS、DFS 之上讲 algs4 §4.1–4.2：连通分量、二分图判定、DFS 的后序和逆后序、用逆后序做拓扑排序和它的三种情况证明、强连通分量（Kosaraju–Sharir 两遍 DFS）。传递闭包讲定义、algs4 的代价和用 Floyd–Warshall 的“或、且”版本求它（放在 `floyd-warshall`）；桥、双连通、平面性只在原书列举里出现，不教，属于图论 M.5.5。
- 最短路讲到 algs4 §4.4：松弛、Dijkstra 和它为什么不能有负权、按拓扑序松弛的 DAG 算法（能处理负权和最长路）、Bellman–Ford 和负环、套利换成取负对数；加上 DPV 6.6 的 Floyd–Warshall。Johnson 算法只讲思路（OI Wiki 有），A* 和差分约束不教，属于搜索与规划 A.1.1。
- 网络流与匹配讲到流网络、增广路和残量网络（含反向边）、Ford–Fulkerson、最大流最小割定理和从可达集找最小割、整数性、Edmonds–Karp（最短增广路）和 Ford–Fulkerson 的坏例子、二分图匹配归约成最大流、二分图里最大匹配等于最小点覆盖（Kőnig 定理，6.046J 的 Recitation 7 和 OI Wiki 都有）。Dinic、预流推进、最小费用流、一般图匹配不教：只在原文的年表和列举里，属于组合优化一类的后继技能。
- 字符串讲到暴力匹配和它的最坏情况、Rabin–Karp 指纹、Boyer–Moore 的坏字符规则、KMP 的前缀函数和匹配（以及“有限状态机”的看法）、R 路字典树的查找、前缀匹配和最长前缀、正则表达式的三种运算和 NFA 同时跟踪一组状态的 $O(MN)$ 模拟（和回溯实现的指数爆炸对比）、后缀数组、相邻后缀的最长公共前缀和最长重复子串。三叉搜索树（TST）只讲是什么；后缀数组的倍增构造、Kasai 算法和 Burrows–Wheeler 变换不教，属于搜索与信息检索系统 D.2.3；NFA 的构造细节属于形式语言与自动机 F.2.1。

## 和原文的核对

写课前，pi 子代理读了四份原文笔记（都不入库）：`temp/research/F.1.2-dpv-notes.md`（DPV 2006 年 7 月 18 日排版稿的 0.2–0.3、第 2、5、6 章，19 节全读到）、`F.1.2-algs4-notes.md`（algs4 配套网站 §1.4、§4.1–4.4、§5.2–5.4、§6.3–6.4 和同站讲义，6.046J 第 14 讲讲义和 Recitation 7）、`F.1.2-erickson-notes.md`（Erickson《Algorithms》13 章全读到）、`F.1.2-zh-notes.md`（Hello 算法 5 章、OI Wiki 8 页、中国大学 MOOC 山东财经大学课程大纲）。课里说“原书……”的地方都对照过这些笔记；数都由 `tests/content/F.1.2.verify.py` 独立重算。

几处原文和来源本身的情况：

- **algs4 的 §5.2–5.4、§6.3、§6.4 是“施工中”的占位页**，只有提纲式要点，没有书的正文。这几节的数字取自同站讲义（字典树、子串查找、最大流）和页面链接的源码注释（后缀数组的 ABRACADABRA! 表）；正则表达式一页只有运行时间的结论和实测表，课里按页面说的 $O(MN)$ 讲“同时跟踪一组状态”，构造细节不教（属于形式语言与自动机 F.2.1）。
- **6.046J 的“第 14 讲 匹配”链到的讲义实际是“网络流与应用”**，匹配只在应用清单里有一行。匹配的内容改用同一门课的 Recitation 7（二分图点覆盖归约到最小割）、algs4 讲义（匹配归约到最大流）、Erickson 第 11 章（交替路）和 OI Wiki（Kőnig 定理）。
- **DPV 有三个数和事实不符，课里没用或改了**：0.2 节说“$F_{30}$ 超过一百万”，按原书 $F_0 = 0$ 的编号 $F_{30} = 832{,}040$（$F_{31}$ 才超过）；说 fib1(200) 的步数 $\ge F_{200} \ge 2^{138}$，实际 $\log_2 F_{200} \approx 137.7$（“至少要 $2^{92}$ 秒”这一句仍然成立，课里只用了这一句）；5.2 节说 Huffman 的例子“省了 17%”，$1 - 213/260 = 18.1\%$，课里写“约 18%”。
- **DPV 的 Horn 公式例子只演示到“依此类推”，没给结论**。课里的例题按算法做完：$x$、$y$、$w$ 被迫为真，纯否定子句 $\bar w \vee \bar x \vee \bar y$ 不成立，所以不可满足（核对脚本另用暴力枚举 16 种赋值确认），课里写明这是“按算法做完”，不是原书的话。
- **algs4 的 tinyDAG7 边表笔记里少了一条 1→4**（讲义的递归片段写着 dfs(1) 里调用了 dfs(4)）。补上这条后按 algs4 的邻接表顺序跑 DFS，正好得到讲义的后序 4 1 2 5 0 6 3 和拓扑序 3 6 0 5 2 1 4（核对脚本里有这一条）；课里没用这张图，用的是自己的例子。
- **algs4 讲义里“读完 txt[0..6] 后状态机在状态 3”的那句**，配的演示文本在笔记里对不上（按笔记里的文本读完是状态 1），课里没引用这句，状态机的题用自己的文本 BCBAABA。转移表本身（模式 ABABAC）由核对脚本按 algs4 的构造代码重新算出，和讲义一致。

对照一致、课里用到的原文内容：fib1 和 fib2、$T(n) = T(n-1) + T(n-2) + 3$、$F_n \approx 2^{0.694n}$、$F_{100}$ 有 21 位、大数加法不是一步（0.2）；$O$、$\Omega$、$\Theta$ 的定义、$n^2$ 和 $2n + 20$ 在 $n = 5$、6 的比较、比值 $\le 22$ 和 $c = 20$、四条化简规则（0.3）；习题 0.1、0.2、2.3、2.4、2.5、5.13、5.14 的题目（答案都由脚本算）；三次乘法、复数乘法的高斯技巧、脚注 $3T(n/2 + 1)$、不必拆到 1 位（2.1）；主定理的 DPV 写法和证明思路、二分查找（2.2）；归并排序、用队列的写法、比较树和 $\log(n!)$、$n! \ge (n/2)^{n/2}$、计数排序的例外（2.3）；中位数 25 的例子、三分和 selection(S, 8) = selection(S_R, 3)、好支点、抛硬币 $E = 2$、$T(n) \le T(3n/4) + O(n)$、最坏 $\Theta(n^2)$、中位数对极端值稳、快速排序的最坏和平均（2.4）；分块公式、8 和 7 个子问题、Strassen 的七个乘积（脚本用不可交换的符号逐格验证了四个格子）、1969（2.5）；$(1+2x+3x^2)(2+x+4x^2)$、$d + 1$ 个点确定多项式、奇偶拆分的例子、平方后还要正负成对所以用复数、$O(n \log n)$（2.6）；树的三条性质、割性质和它的交换证明、Kruskal、并查集的三个操作和按秩合并、秩为 $k$ 的根至少 $2^k$ 个元素、路径压缩不改秩、$\log^* 1000 = 4$、Figure 5.6 的一串 union（脚本按原书的规则重放）、Prim、前缀码和 {0, 01, 11, 001} 的歧义、A 70、B 3、C 20、D 37 的 260 和 213、Huffman 算法和交换论证、Horn 公式的两类子句、吝啬算法和不变式、集合覆盖的定义、11 个镇贪心 4 所对最优 3 所、$k \ln n$ 的证明思路和紧性（5.1–5.4）；第 6 章每节的子问题和关系式、5、2、8、6、3、6、9、7 的 2、3、6、9、“递归？不了，谢谢”、SNOWY 和 SUNNY 的对齐、EXPONENTIAL 和 POLYNOMIAL 是 6、编辑距离的表是一张 DAG、背包的 48 和 46、伪多项式、矩阵链的三种顺序 120,200、60,200、7,000 和贪心选第二种、$O(n^3)$、最多 $k$ 条边的最短路、Floyd–Warshall 和 $k$ 放最外层、旅行商的 $O(n^2 2^n)$、树上独立集的关系式（6.1–6.7）。algs4：代价模型、2-SUM 和 3-SUM 的计数、倍增实验表 0.1、0.8、6.4、51.1 和预测 408.1、实测 410.8、波浪号和 166,666,667 对 166,167,000、增长阶分类表、倍增看不出对数因子、大 O 不是近似模型、最好平均最坏、上界下界最优、1-SUM、3-SUM 的未解决问题、二分查找最多 $1 + \lg N$ 次、Java 的内存模型和日期对象 32 字节、摊还的两条命题（§1.4）；tinyG 的 3 个连通分量、tinyCG 的 distTo、DFS 的应用、逆后序是拓扑序和三种情况的证明、Kosaraju–Sharir、tinyDG 的 5 个强连通分量、传递闭包的代价、几道带答案的习题（§4.1–4.2）；tinyEWG 的 MST 1.81、Prim 的 $V^2$ 版、加常数不改 MST（§4.3）；松弛、Dijkstra、tinyEWD 的 0 到 6 是 1.51、DAG 按拓扑序松弛能处理负权和最长路、Bellman–Ford、负环、加常数会改最短路、套利 1007.14497（§4.4）；字典树的例子 by、sea、sells、she、shells、shore、the 和以 sh 开头、shellsort 的最长前缀、out of memory、三叉搜索树（§5.2）；暴力 $\sim MN$、KMP 最多 $M + N$、ABABAC 的状态表、Boyer–Moore 的 right[] 和 NEEDLE 的跳跃（脚本重放了讲义的 (0,5)、(5,5)、(11,4)、15）、Rabin–Karp 的 613 和 508、201、715、971、442、929、蒙特卡洛和拉斯维加斯（§5.3）；(a|aa)*b 的实测表（§5.4）；ABRACADABRA! 的后缀数组表、最长重复子串、KWIC 的 $O(K \log N)$（§6.3）；最大流的定义、流值引理、弱对偶、三条等价、从可达集读最小割、整数性、坏例子和 2 billion、Edmonds–Karp、tinyFN（最大流 4 是我们算的，原书没给）（§6.4）。6.046J：Edmonds–Karp 的 $O(VE)$ 次增广、流整性、点覆盖在一般图上 NP 难、二分图上归约到最小割。

课里自己出的例子（不声称出自原书）：各道计数题、47 × 53、AB 和 BA 的表、P、Q、R、S 和 A–E 的最小生成树、并查集的 parent 字典、各个 Horn 公式、集合覆盖的 {1..6}、分数背包、各个 DAG、序列、背包和矩阵链的数、限边数的图、4 城旅行商、各棵树、计数器和栈的操作串、课程先修图、各个 Dijkstra、Bellman–Ford、Floyd–Warshall 的图、流网络和二分图、字符串题、结业的 12 道题。每个数都由核对脚本独立算出：474 处，其中 120 道数字题和文字题的答案、49 道选择题和排序题的正确项逐题从课包里读出来比较；能枚举的都枚举了（活动安排、集合覆盖、Horn 公式、独立集、编辑距离、旅行商都用暴力或宽度优先搜索另算一遍；KMP、前缀函数、并查集的秩、逆后序是拓扑序、快速排序、Kőnig 定理在随机的小例子上各试了几十到几百次）。

## CS2023（`data/curation/scope.json`）

| 知识点 | CS2023 主题（scope.json 匹配原文） | 课 |
|---|---|---|
| 渐近分析 | AL-Complexity，CS Core：Asymptotic complexity analysis | `count-steps`、`tilde`、`big-o`、`growth-classes`、`memory` |
| 递归 | AL-Strategies，CS Core：Iteration vs recursion | `fibonacci`、`recursion-iteration` |
| 分治 | AL-Strategies，CS Core：Divide-and-Conquer | `recursion-tree`、`master-theorem`、`karatsuba`、`sorting-bound`、`quickselect`、`strassen`、`fft` |
| 贪心 | AL-Strategies，CS Core：Greedy | `activity-selection`、`mst-cut`、`prim`、`huffman`、`horn`、`set-cover` |
| 动态规划与摊还分析 | AL-Strategies，CS Core：Dynamic programming；AL-Complexity，KA Core：Amortized analysis | `dag-dp` 到 `tree-independent-set` 共 8 课；`amortized-counter`、`potential-method` |
| 图的遍历 | SDF-Algorithms，CS Core：graph traversal | `components`、`topo-dfs`、`scc` |
| 最短路 | AL-Foundational，CS Core：Shortest path | `dag-dp`、`dijkstra`、`negative-edges`、`floyd-warshall` |
| 网络流与匹配 | AL-Strategies，KA Core：Ford-Fulkerson | `max-flow`、`min-cut`、`bipartite-matching` |
| 字符串匹配与索引 | AL-Foundational，KA Core：Efficient string matching | `substring-search`、`prefix-function`、`kmp-search`、`tries`、`regex`、`suffix-array` |

## 原技能树的综合练习

| 小题 | 课 |
|---|---|
| (1) 用主定理解 $2T(n/2) + n$、$4T(n/2) + n$、$T(n/2) + 1$ | `master-theorem`（连线题就是这三个式子） |
| (2) LCS 的递推式，LCS("ABCBDAB", "BDCABA") 的长度和一个 LCS | `lcs`（分步例题就是这一题） |
| (3) 活动安排按结束时间贪心，用交换论证说明为什么对 | `activity-selection`（数字题就是这一组活动，交换论证一张卡） |
| (4) 翻倍扩容 $n$ 次 append 总代价 $O(n)$ | `amortized-counter`（聚合分析）、`potential-method`（势能法、16 次的总数），结业 `b-doubling`；F.1.1 的 `amortized` 也讲过 |
| (5) Dijkstra 求最短距离、出队顺序，为什么不能有负权 | `dijkstra`（开头的猜题和演示就是这张图）、`negative-edges`，结业 `b-dijkstra` |
| (6) ABABCABAB 的前缀函数和在文本里的所有出现 | `prefix-function`（分步例题算 π）、`kmp-search`（分步例题找出 5 和 10） |

## 学习资源的章节（C3）

技能的章列了 9 份资源。pi 子代理读到的情况：Hello 算法的网站返回 429，改读官方仓库的同一份 markdown（第 2、9、12、14、15 章全读到，图里的数据读不到）；OI Wiki 8 页读到原文（代码块没逐行读）；中国大学 MOOC 只有课程大纲的章节标题，视频、课件要登录，没读到；Erickson 13 章全读到；algs4 §5.2、5.3、6.3 见上面“占位页”的说明。下表列出资源里讲到的概念和去处；没有专门讲的写明原因。核对时补了三样：Hello 算法的分数背包（`activity-selection`）、algs4 的传递闭包（`floyd-warshall`）、快速排序（`quickselect`）。

| 资料 | 讲到的概念 | 去处 |
|---|---|---|
| Hello 算法第 2 章 | 迭代和递归、调用栈、尾递归、递归树、时间和空间复杂度、最好最坏平均 | `recursion-iteration`、`fibonacci`、`count-steps`、`big-o`（含 $n_0$ 的写法）、`growth-classes`、`memory` |
| Hello 算法第 9 章 | 图的表示、BFS、DFS | F.1.1 的 `graph-storage`、`graph-traversal`；本站 `components` |
| Hello 算法第 12 章 | 分治的判据、二分查找、由前序和中序构建二叉树、汉诺塔 | 二分查找在 `master-theorem`、`growth-classes`，汉诺塔在 M.5.3 的 `hanoi`；“构建二叉树”是分治在二叉树上的一道练习，思路和归并排序相同，不单独讲 |
| Hello 算法第 14 章 | 重叠子问题、最优子结构、记忆化、爬楼梯、最小路径和、0-1 背包、完全背包、零钱兑换、编辑距离、滚动数组 | `dag-dp`、`lis`、`knapsack`、`edit-distance`，爬楼梯在 M.5.3 的 `linear-recurrences`；零钱兑换是可重复背包把 max 换成 min（或计数），子问题相同，不单独讲；滚动数组（只留两行省空间）是实现技巧，不讲 |
| Hello 算法第 15 章 | 贪心的两条性质、零钱兑换的反例、分数背包、最大容量、最大切分乘积 | `activity-selection`（含硬币反例和分数背包）；最大容量、最大切分乘积是练习题，方法（贪心选择 + 证明）已讲 |
| OI Wiki 均摊复杂度 | 聚合、记账、势能，动态数组和多次弹出的栈 | `amortized-counter`、`potential-method` |
| OI Wiki 最短路 | Floyd、Bellman–Ford 和负环、SPFA、Dijkstra 和正确性证明、Johnson、输出路径 | `dijkstra`、`negative-edges`（algs4 的队列版就是 SPFA 的思路）、`floyd-warshall`（Johnson 讲思路）；0-1 BFS、分层图是竞赛技巧，不教 |
| OI Wiki 网络流简介、最大流 | 流网络、残量网络、反向边、最大流最小割定理和证明、Edmonds–Karp、Dinic、ISAP、预流推进、HLPP | `max-flow`、`min-cut`；Dinic、ISAP、预流推进、HLPP 只讲到“有更快的算法”，不教，属于组合优化一类的后继内容 |
| OI Wiki 二分图、二分图最大匹配 | 二分图和奇圈、Kuhn、Hopcroft–Karp、归约为最大流、线性规划和对偶、Kőnig 定理、最大独立集、DAG 最小路径覆盖 | `components`（二分图判定）、`bipartite-matching`（交替路就是 Kuhn 的增广、归约、Kőnig）；Hopcroft–Karp、线性规划对偶、最小路径覆盖不教：线性规划在 DPV 第 7 章，大纲没收 |
| OI Wiki 前缀函数与 KMP、后缀数组 | π 的定义和 $O(n)$ 算法、KMP、前缀函数自动机、周期、后缀数组的倍增构造、height 数组、不同子串个数 | `prefix-function`、`kmp-search`（状态机）、`suffix-array`（相邻后缀的 LCP 就是 height）；周期、构造算法、不同子串个数不教，属于搜索与信息检索 D.2.3 一类的进阶 |
| 中国大学 MOOC（只读到大纲标题） | 算法分析、枚举、贪心（背包、区间、MST、哈夫曼）、递推方程、分治的三种改进、动态规划（数字三角形、区间动归、DAG、树形、序列比对）、回溯、分支限界、网络流（含最小费用流、最佳匹配）、随机算法、P 与 NP、近似算法 | 按标题能对上的都在本站；回溯、分支限界不教（原技能树的大纲没有，属于搜索与规划 A.1.1）；最小费用流、带权最佳匹配不教（组合优化）；随机算法、近似算法属于 F.1.4，P 与 NP 属于 F.2.3（集合覆盖只讲到近似比） |
| Erickson《Algorithms》 | 递归（汉诺塔、归并、快排、线性时间选择即中位数的中位数、Karatsuba、快速幂）、递推式求解、贪心（磁带存文件、活动安排、Huffman、稳定匹配）、动态规划（文本切分、LIS、编辑距离、子集和、最优二叉搜索树、树上 DP）、摊还、图、DFS、最短路、全源最短路、最大流和应用、字符串匹配 | 大部分都在上面的课里，稳定匹配在 M.5.3；确定性的“中位数的中位数”不教（DPV 只给随机版，入门讲随机版）；文本切分、子集和、最优二叉搜索树是同样的子问题形状（前缀、区间），不单独讲；最大流的其他应用（不相交路径、棒球淘汰、项目选择）不教，只讲二分图匹配这一种归约 |
| algs4 §5.2、5.3、6.3 | 见上 | `tries`、`substring-search`、`kmp-search`、`suffix-array` |

## 后继技能要用的

必须后继（计算几何 M.4.4、符号计算 M.8.6、随机近似在线算法 F.1.4、并行外存流算法 F.1.5、计算复杂性 F.2.3、分布式算法 C.4.3、搜索与信息检索 D.2.3、数据挖掘 D.3.2、概率图模型 A.1.2）都还没有内容包，按它们的综合练习核对：F.1.4 要随机快速排序（`quickselect` 末尾补讲了快速排序和它的最坏情况）、割（`min-cut`）、顶点覆盖（`bipartite-matching`）和近似比（`set-cover`）；F.1.5 要归并排序、二分查找和 $O$ 记号；F.2.3 要多项式时间、归约（匹配归约成最大流是第一个例子）和可满足（`horn`）；D.2.3 要合并有序列表、字典树和后缀数组；A.1.2 的变量消去复杂度要树上的动态规划；C.4.3 要 $O(n^2)$、$O(n \log n)$ 这类分析。这些这一站都教到了。
