# F.1.1 数据结构：覆盖表

规则见 `docs/content-authoring.md` 的“知识覆盖面标准”。依据：skill-tree 大纲 `../cs-math-skill-tree/data/outlines/F.1.1.json`：Pat Morin《Open Data Structures》（Java 版，AU Press 2013，免费全文）第 2、3、5、6、9、10、12 章。“节”是技能内部编号，“原文”是教材自己的节号和标题。

这一站的课用 Python 写（它的必须前置只有 P.1.1）。教材用 Java，课里的代码按教材的算法改写成 Python，名字保留教材的（ArrayStack、SLList……）。

`node scripts/check-coverage.mjs F.1.1` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | 2.1 ArrayStack: Fast Stack Operations Using an Array | `array-basics`, `array-stack`, `amortized`, `invariants` |
| 1.2 | 2.2 FastArrayStack: An Optimized ArrayStack | `array-stack` |
| 1.3 | 2.3 ArrayQueue: An Array-Based Queue | `array-queue` |
| 1.4 | 2.4 ArrayDeque: Fast Deque Operations Using an Array | `array-queue` |
| 1.5 | 2.5 DualArrayDeque: Building a Deque from Two Stacks | `two-stacks` |
| 1.6 | 2.6 RootishArrayStack: A Space-Efficient Array Stack | `rootish` |
| 2.1 | 3.1 SLList: A Singly-Linked List | `sllist` |
| 2.2 | 3.2 DLList: A Doubly-Linked List | `dllist` |
| 2.3 | 3.3 SEList: A Space-Efficient Linked List | `selist` |
| 3.1 | 5.1 ChainedHashTable: Hashing with Chaining | `hash-chaining` |
| 3.2 | 5.2 LinearHashTable: Linear Probing | `linear-probing` |
| 3.3 | 5.3 Hash Codes | `hash-codes` |
| 4.1 | 6.1 BinaryTree: A Basic Binary Tree | `binary-trees` |
| 4.2 | 6.2 BinarySearchTree: An Unbalanced Binary Search Tree | `bst` |
| 5.1 | 9.1 2-4 Trees | `two-four` |
| 5.2 | 9.2 RedBlackTree: A Simulated 2-4 Tree | `red-black`, `invariants` |
| 5.3 | 9.3 Summary | `red-black` |
| 6.1 | 10.1 BinaryHeap: An Implicit Binary Tree | `binary-heap` |
| 6.2 | 10.2 MeldableHeap: A Randomized Meldable Heap | `meldable-heap` |
| 7.1 | 12.1 AdjacencyMatrix: Representing a Graph by a Matrix | `graph-storage` |
| 7.2 | 12.2 AdjacencyLists: A Graph as a Collection of Lists | `graph-storage` |
| 7.3 | 12.3 Graph Traversal | `graph-traversal` |

另有三课不对应单独的一节，是读懂这些节要先会的：`array-basics`（内存、数组、按下标一步找到、大 O 的直观意思）、`stack-queue-adt`（栈、队列、双端队列这几个接口，教材第 1.2 节，大纲判为通用铺垫没收）、`invariants`（把每个结构的不变量写成检查函数，大纲 `coverage` 的“不变量”一项）。

教到什么深度（入门层）：
- 运行时间用“要走多少步”和 O(1)、O(log n)、O(n) 的直观意思来讲；渐近记号的定义和证明属于 F.1.2 算法分析与设计。
- ArrayStack 的摊还分析讲到“m 次操作里复制的元素总数不超过 2m 左右”，用具体的数算；势能法等一般方法属于 F.1.2。
- RootishArrayStack 讲块的大小、按下标找块的公式（用具体的 i 算）、浪费的空间只有大约 √n；不讲 grow / shrink 的细节。
- SEList 讲“每个节点放一小块元素、块的大小在 b − 1 到 b + 1 之间”和它在时间、空间上的折中；不讲 spread / gather 的步骤。
- 哈希讲取余和教材的乘法哈希（用小的数算一次），拉链法和线性探测的期望 O(1) 只讲结论和直观原因；线性探测的删除标记讲清楚。
- 2-4 树讲高度和度数两条性质、加叶子时的分裂；删叶子时的借和合并只讲做法。红黑树讲黑高和“没有相邻的红节点”两条性质、教材的左倾规则、和 2-4 树的对应、高度不超过 2 log n；不讲插入和删除时的颜色修复细节。
- MeldableHeap 讲 merge 的递归做法和“随机往左或往右”；期望 O(log n) 只讲结论。

## 和原文的核对

2026-11-03 用 web-fetch 子代理逐条对照 ODS 的 HTML 版（opendatastructures.org/ods-java/，版本 0.1G）核对了课里引用的 20 条教材规则：扩容和缩小的条件、循环数组的下标、DualArrayDeque 的 3 倍平衡、RootishArrayStack 的块号公式、DLList 的哑节点和 addBefore 的顺序、SEList 的块大小、ChainedHashTable 的 n ≤ t.length 和乘法哈希、LinearHashTable 的 del 和“至少一半空”、BST 删除用右子树最小值、2-4 树的分裂、红黑树的三条性质和 2 log n、BinaryHeap 的下标公式、MeldableHeap 的 log(n + 1)、邻接表的代价。19 条和原文一致；字符串哈希码一处改了说法（教材用随机系数的多项式对质数 2^32 − 5 取余，31 是 Java 的做法）。“邻接矩阵上遍历是 O(n²)”教材没有直接写，课里写明是由“列出一个顶点的邻居要 O(n)”推出来的。数值和数组状态由 `tests/content/F.1.1.verify.py` 用 Python 按课里的代码运行核对。

## CS2023（`data/curation/scope.json`）

| 知识点 | CS2023 主题（scope.json 匹配原文） | 课 |
|---|---|---|
| 数组 | AL-Foundational，CS Core：Arrays | `array-basics`, `array-stack`, `amortized`, `rootish` |
| 链表 | AL-Foundational，CS Core：Linked lists | `sllist`, `dllist`, `selist` |
| 栈队列 | AL-Foundational，CS Core：Queues and deques | `stack-queue-adt`, `array-queue`, `two-stacks` |
| 哈希 | AL-Foundational，CS Core：Hash tables/maps | `hash-chaining`, `linear-probing`, `hash-codes` |
| 树 | AL-Foundational，CS Core：Binary, n-ary, and search trees | `binary-trees`, `bst`, `two-four`, `red-black` |
| 堆 | AL-Foundational，CS Core：Heap-based priority queue | `binary-heap`, `meldable-heap` |
| 图存储与不变量 | AL-Foundational，CS Core：Graphs (e.g., [un]directed | `graph-storage`, `graph-traversal` |

## 综合练习（原技能树，约 45 分钟）

| 小题 | 要用到 | 课 |
|---|---|---|
| (1) 两个栈实现队列，摊还 O(1) | 栈、每个元素最多搬一次 | `two-stacks` |
| (2) 5, 3, 8, 1, 4, 7, 9 插入 BST：形状、中序、树高 | BST 插入、中序遍历、高度按边数 | `binary-trees`, `bst` |
| (3) 同一组数插入最小堆、再 extract-min | 上浮、下沉、数组表示 | `binary-heap` |
| (4) 容量 7、h(k) = k mod 7 的线性探测；负载因子的影响 | 线性探测、聚集、扩容 | `linear-probing` |
| (5) 5 个顶点的图：邻接表和邻接矩阵，比较空间和判相邻的时间 | 两种表示的代价 | `graph-storage` |

## 后继技能用到的写法（C5）

这条路线上以 F.1.1 为必须前置的是 C.2.1 操作系统（另外 F.1.2 算法分析与设计也以它为必须前置）。

| 后继 | 用到的 | 课 |
|---|---|---|
| C.2.1 | 队列（就绪队列）、循环数组 | `stack-queue-adt`, `array-queue` |
| C.2.1 | 链表（空闲块、进程表） | `sllist`, `dllist` |
| C.2.1 | 树（多级页表、目录树） | `binary-trees` |
| C.2.1 | 哈希表（打开文件表、页缓存的查找） | `hash-chaining` |
| F.1.2 | 栈、队列、堆（优先队列）、邻接表、BFS / DFS、递归 | `stack-queue-adt`, `binary-heap`, `graph-storage`, `graph-traversal`, `binary-trees` |
| F.1.2 | 渐近记号的定义、递推式、摊还分析的一般方法 | 不在这一站：F.1.2 自己教 |
