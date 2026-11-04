# M.5.3 证明方法与离散结构：覆盖表

规则见 `docs/content-authoring.md` 的“知识覆盖面标准”。依据：skill-tree 大纲 `../cs-math-skill-tree/data/outlines/M.5.3.json`：A = MIT 6.042J 的教材 Mathematics for Computer Science（Lehman、Leighton、Meyer）的第 1、2、5、6、7 章和 10.6–10.11、第 22 章，共 38 节。大纲的节号和 2018 年 6 月 6 日修订版逐条对得上（2015 版的章号不同：状态机在 5.4，递归数据类型是第 6 章，偏序是第 9 章，递推是第 21 章）。“节”是技能内部编号，“原文”是原书的节号和标题。技能的章另列了北京大学陈斌《离散数学概论》、火炉课堂《离散数学》第十二章和《2-6 循环不变量》，也按它们核对（见“学习资源的章节”）。

这一站没有必须前置的技能，从“什么是命题”讲起，只假设会中学的算术和代数：解一元二次方程、解两个未知数的方程组、分数、乘方。用到的整数、集合、函数、对数、二叉树都在课里先讲再用。

`node scripts/check-coverage.mjs M.5.3` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | A 1.1 Propositions | `propositions` |
| 1.2 | A 1.2 Predicates | `propositions` |
| 1.3 | A 1.3 The Axiomatic Method | `axioms-implications` |
| 1.4 | A 1.4 Our Axioms | `axioms-implications` |
| 1.5 | A 1.5 Proving an Implication | `axioms-implications`, `contrapositive` |
| 1.6 | A 1.6 Proving an “If and Only If” | `iff-and-cases` |
| 1.7 | A 1.7 Proof by Cases | `iff-and-cases` |
| 1.8 | A 1.8 Proof by Contradiction | `contradiction` |
| 1.9 | A 1.9 Good Proofs in Practice | `good-proofs` |
| 2.1 | A 2.1 Well Ordering Proofs | `well-ordering` |
| 2.2 | A 2.2 Template for WOP Proofs | `well-ordering` |
| 2.3 | A 2.3 Factoring into Primes | `well-ordering` |
| 2.4 | A 2.4 Well Ordered Sets | `well-ordered-sets` |
| 3.1 | A 5.1 Ordinary Induction | `induction`, `induction-practice`, `stronger-hypothesis` |
| 3.2 | A 5.2 Strong Induction | `strong-induction` |
| 3.3 | A 5.3 Strong Induction vs. Induction vs. Well Ordering | `strong-induction`, `well-ordered-sets` |
| 4.1 | A 6.1 States and Transitions | `state-machines` |
| 4.2 | A 6.2 The Invariant Principle | `invariants`, `die-hard` |
| 4.3 | A 6.3 Partial Correctness & Termination | `termination` |
| 4.4 | A 6.4 The Stable Marriage Problem | `stable-matching` |
| 5.1 | A 7.1 Recursive Definitions and Structural Induction | `recursive-data` |
| 5.2 | A 7.2 Strings of Matched Brackets | `brackets` |
| 5.3 | A 7.3 Recursive Functions on Nonnegative Integers | `recursive-functions` |
| 5.4 | A 7.4 Arithmetic Expressions | `expressions` |
| 5.5 | A 7.5 Games as a Recursive Data Type | `games` |
| 5.6 | A 7.6 Search Trees | `search-trees` |
| 5.7 | A 7.7 Induction in Computer Science | `search-trees` |
| 6.1 | A 10.6 Partial Orders | `partial-orders` |
| 6.2 | A 10.7 Representing Partial Orders by Set Containment | `hasse` |
| 6.3 | A 10.8 Linear Orders | `linear-product` |
| 6.4 | A 10.9 Product Orders | `linear-product` |
| 6.5 | A 10.10 Equivalence Relations | `equivalence`, `partitions` |
| 6.6 | A 10.11 Summary of Relational Properties | `relations`, `linear-product` |
| 7.1 | A 22.1 The Towers of Hanoi | `hanoi` |
| 7.2 | A 22.2 Merge Sort | `merge-sort` |
| 7.3 | A 22.3 Linear Recurrences | `linear-recurrences` |
| 7.4 | A 22.4 Divide-and-Conquer Recurrences | `divide-conquer` |
| 7.5 | A 22.5 A Feel for Recurrences | `divide-conquer` |

另有一课不对应大纲的某一节：

- `relations`（二元关系、画成有向图、自反、对称、传递）：等价关系和偏序都建立在“关系”上，原书在 10.1–10.5 讲有向图和关系，大纲没收这几节，但 10.10 以后处处要用，按 B1 先讲后用补一课。只讲到 10.6–10.11 要用的部分（关系是什么、怎么画、几条性质怎么在图上看），有向图的路径、邻接矩阵、DAG 的调度不讲，属于图论 M.5.5。

教到什么深度（入门层）：
- 证明写法讲到能独立写出原书第 1、2、5 章的证明：直接证明、逆否、反证、分情形、当且仅当（两个方向或一串等价）、良序原理的五步模板、普通归纳和强归纳的五步模板、加强归纳假设。逻辑本身只讲到写证明要用的程度（命题、谓词、蕴含、逆否、推理规则可靠），形式系统、真值表的完整理论和量词的推理规则属于数理逻辑 M.5.2。
- 状态机讲到原书 6.1–6.4 的主要例子：99 计数器、斜着走的机器人、倒水（3 和 5、3 和 9，课里用“升”）、快速求幂的不变式和终止、严格递减的量、稳定匹配的求婚算法和它的不变式。另加了循环不变量的“初始化、保持、终止”三步（技能章列的《2-6 循环不变量》）。原书的东南跳机器人（要用 $\mathbb{N} + F$ 这种良序集证明终止）和 2.4.1 的 $\mathbb{N} + F$ 不讲，属于集合论 M.5.1 的序数。
- 递归数据讲到原书 7.1–7.5 的定义和结构归纳：串、匹配括号串（含“有歧义的定义”这个坑）、非负整数、算术表达式的求值和代入、Nim。7.6 搜索树只讲“二叉树是递归数据”、大小 $\le 2^{\text{深度}+1}-1$ 的结构归纳证明、搜索树的定义和查找；原书用选择子序列（selector sequence）定义子树、证明“有限树 = 递归树”、AVL 树插入的完整证明不讲，这些属于数据结构 F.1.1 和算法分析与设计 F.1.2。
- 关系讲到 10.6–10.11 的全部定义：自反、反自反、对称、非对称、反对称、传递，严格偏序和非严格偏序，整除，用集合包含表示偏序，线性序和可比，积序，等价关系、等价类、同余、$\equiv_f$、划分。原书用 DAG（有向无环图）和路径关系 $G^+$、$G^*$ 刻画偏序的那几条定理只讲“严格偏序的箭头图里没有圈”这一点；10.9 例子里用到的 Dilworth 引理不讲，这两样属于图论 M.5.5。综合练习 (4) 要的哈斯图、最小元和最大元原书这几节没有，按综合练习和陈斌第 54 讲的标题补在 `hasse`，另加了极小元、极大元。
- 递推讲到 22.1–22.5：猜了再用归纳验证、上界陷阱、展开（plug and chug）、归并排序比较次数 $n\log_2 n - n + 1$、齐次线性递推的特征方程（含重根）、非齐次递推猜特解、主定理的三种情形。主定理按 $g(n) = n^d$ 的简化形式教（比较 $d$ 和 $\log_b a$），并说明原书的一般形式允许 $g(n)$ 带对数因子。原书的 Akra–Bazzi 公式要用积分，只说它是主定理的推广、什么时候要用它，不教计算（积分在一元积分学 M.1.3）。

## 和原文的核对

写课前，pi 子代理读了 38 节的原文（MCS 2018 年 6 月 6 日修订版 PDF，笔记 `temp/research/M.5.3-mcs-notes.md`，不入库）。PDF 转出的文字会丢掉减号（pdftotext 和 PyMuPDF 都这样），笔记里有的式子因此少了负号，比如 Theorem 1.5.1 原文是 $-x^3 + 4x + 1 > 0$（原文写着“$x^3$ which is negative”），笔记写成了 $x^3 + 4x + 1 > 0$。所以课里的式子没有照抄笔记，都对照原书上下文定下来，再由 `tests/content/M.5.3.verify.py` 用 Python 和 sympy 重算。

对照一致的说法：命题、谓词和“谓词的值是真假、函数的值是数”的提醒（1.1、1.2）；$n^2 + n + 41$ 在 $n = 40$ 失败、欧拉猜想的反例（1.1）；公理、定理、引理、推论，推理规则可靠的定义，$\neg P \Rightarrow \neg Q$ 推不出 $P \Rightarrow Q$（1.3、1.4）；证明蕴含的两种方法和 Theorem 1.5.1、1.5.2（1.5）；当且仅当的两种证法和标准差为 0 的定理（1.6）；6 个人里一定有 3 人熟人组或生人组（1.7）；反证法四步和 $\sqrt2$ 的证明（1.8）；1.9 的写作建议和三种坏证明；良序原理、五步模板、最简分数、素数分解的存在性（2.1–2.3）；良序集、下界和上界、Corollary 2.4.3、2.4.4、有限集有最小元（2.4）；归纳原理和五步模板、L 形砖要加强归纳假设、马的错误证明错在 $P(1) \Rightarrow P(2)$，以及“错在假设了假的 $P(n)$”这种解释为什么不对（5.1）；强归纳、3 和 5 凑硬币、拆积木得分 $n(n-1)/2$、第一步 5 加 5 得 25 分（5.2）；三种方法能机械互改，$Q(n) := \forall k \le n.\ P(k)$（5.3）；99 计数器、执行和可达、确定性（6.1）；斜着走的机器人两步后 9 个位置、坐标和的奇偶、不变式原理、倒水 3 和 5 能量出 4、3 和 9 的不变式、$(1, 0) \to (0, 0)$ 说明不变式的反面不一定是不变式（6.2）；快速求幂的状态机、不变式 $yx^z = a^b$、部分正确和终止、Theorem 6.3.2、只“不增加”不能保证终止（6.3）；阻塞对、求婚仪式、不变式 $P$、最多 $n^2$ 天、男方得到最好的稳定搭档而女方得到最差的、稳定匹配不唯一、室友配对可能没有稳定解（6.4）；字符串、长度、连接和 $|s \cdot t| = |s| + |t|$（7.1）；RecMatch、左右括号一样多、AmbRecMatch 上 $f(\lambda)$ 既是 0 又是 1（7.2）；$\mathbb{N}$ 的递归定义、阶乘、$f_1$ 到 $f_4$ 四种坏定义、考拉兹从 3 出发的链和“验证到 $10^{18}$ 以上”（7.3）；Aexp、eval、subst、Theorem 7.4.4 要对 $e$ 归纳、代入模型多算一次乘法（7.4）；Nim⟨3, 2⟩ 的 5 种第一步、博弈的递归定义、一方必胜的定理及其证明不告诉你是哪一方（7.5）；二叉树大小不超过 $2^{d+1} - 1$、搜索树的定义和查找 3.7 的例子（7.6）；7.7 的总结；10.6–10.11 的全部定义、$\{1, 3, 4, 6, 8, 12\}$ 换成集合的那张表、积序的 $(240, 68)$ 和 $(228, 72)$ 不可比、同余模 5 的 $[7]$、等价类构成划分、性质总表；汉诺塔 $2^n - 1$、上界陷阱、展开法（22.1）；归并排序的例子 10、7、23、5、2、8、6、9，$T_n = n\log_2 n - n + 1$ 和 0、1、5、17、49（22.2）；楼梯 4 级 5 种走法、特征方程、Theorem 22.3.1、$\varphi^{20}/\sqrt5 = 6765.00003\ldots$、重根、汉诺塔变体 $2^{n+1} - n - 2$、猜特解的经验（22.3）；分治递推、主定理、Akra–Bazzi 例子的 $\Theta(n^2 \log n)$、15 分成 7 和 8（22.4）；$a$ 从 1.99 到 2.01 解的形式跳变、子问题“小一个常数”时是指数级（22.5）。

课里自己出的例子（不声称出自原书）：$2^n + 1$ 的反例、能被 6 整除不能被 4 整除的 6、3 对 3 的稳定匹配偏好表、4 升和 6 升的壶、5 人围坐一圈、集合 $\{2, 3, 4, 5, 6, 12\}$、18 和 30 的因数、各道递推和主定理的题、结业的 4 元和 7 元邮票等。每个数都由核对脚本独立算出：323 处，其中 61 道数字题的答案逐题从课包里读出来比较；能枚举的都枚举了（6 个人的 $2^{15}$ 种认识关系、3 个和 4 个元素上的全部关系、8 个数的全部 $8!$ 种排列跑归并排序、按证明的递归构造真的铺出 $2^n \times 2^n$ 院子的每一种雕像位置）。

写完第一次运行核对脚本，查出的两处错都在脚本本身（一个符号式没化简就比较、一个比值收敛太慢），课里的数没有错。

## CS2023（`data/curation/scope.json`）

| 知识点 | CS2023 主题（scope.json 匹配原文） | 课 |
|---|---|---|
| 归纳、反证 | MSF-Discrete，CS Core：Proof techniques (induction, proof by contradiction) | `induction`、`induction-practice`、`strong-induction`、`contradiction`、`well-ordering` |
| 不变式 | AL-Models，CS Core：Algorithmic correctness a. Invariants | `invariants`、`termination`（循环不变量的初始化、保持、终止） |
| 递推与结构化证明 | MSF-Discrete，CS Core：Recursive mathematical definitions | `recursive-data`、`recursive-functions`、`expressions`、`hanoi`、`linear-recurrences` |

## 原技能树的综合练习

| 小题 | 课 |
|---|---|
| (1) 用归纳法证明 $1 + 3 + \dots + (2n-1) = n^2$ | `induction-practice`（分步例题就是这一题） |
| (2) 用反证法证明 $\sqrt2$ 是无理数 | `contradiction`（分步例题就是这一题） |
| (3) 8×8 棋盘去掉对角两个角格，能否用 31 张多米诺骨牌盖满；用染色不变式说明 | `invariants`（分步例题就是这一题） |
| (4) $\{1,2,3,4,6,12\}$ 上的整除：证明是偏序，画哈斯图，找最小元、最大元，判断是不是全序 | `partial-orders`（证明三条性质）、`hasse`（哈斯图、最小元和最大元、拓扑排序的交互题）、`linear-product`（2 和 3 不可比，所以不是线性序） |
| (5) 解 $a_n = a_{n-1} + 2a_{n-2}$，$a_0 = 0$，$a_1 = 1$ | `linear-recurrences`（分步例题就是这一题） |

## 学习资源的章节（C3）

技能的章列了三份中文资源，都是视频。pi 子代理找了能读到的文字（笔记 `temp/research/M.5.3-zh-notes.md`，不入库）：陈斌《离散数学概论》只读到 Coursera 和 B 站上每一讲的标题和时长，字幕要登录、课件要选课，都没读到；火炉课堂第十二章只有章名和两个分 P（part 1、part 2）；《2-6 循环不变量》只有标题。所以下表按讲次标题和技能大纲里写的内容核对，讲次里具体讲了哪些例题无从确认。

| 资料 | 讲次 | 课 |
|---|---|---|
| 陈斌 | 21 形式系统和证明、演绎；22 命题演算形式系统 PC；23 PC 中的定理证明；31–32 自然推理系统与定理证明 | `axioms-implications`（公理、证明、推理规则、可靠）、`contrapositive`、`contradiction`。形式系统 PC 的公理和推理规则本身、自然推理系统不教：属于数理逻辑 M.5.2 的“形式系统”“推理”两章 |
| 陈斌 | 38 归纳定义 | `recursive-data`（基础情形、构造情形） |
| 陈斌 | 39 自然数的定义 | `recursive-functions`（$\mathbb{N}$：0 和后继） |
| 陈斌 | 40 归纳原理；41 数学归纳法 | `induction`、`induction-practice`、`strong-induction`，结构归纳在 `recursive-data` |
| 陈斌 | 49 等价关系；50 等价关系与划分 | `equivalence`、`partitions` |
| 陈斌 | 51 划分之间的关系 | `partitions`（加细：一个划分的每块都落在另一个划分的某块里） |
| 陈斌 | 52 划分运算 | 不教：划分的运算属于集合论 M.5.1 的“关系”一章 |
| 陈斌 | 53 序关系 | `partial-orders`、`linear-product` |
| 陈斌 | 54 序关系中的特殊元素 | `hasse`（最小元、最大元、极小元、极大元），上界和下界在 `well-ordered-sets`。上确界、下确界（如果这一讲讲了）不教：属于集合论 M.5.1 和实分析 M.1.6 |
| 火炉课堂 | 第十二章 递推方程与生成函数 | 递推方程在 `hanoi`、`merge-sort`、`linear-recurrences`、`divide-conquer`；生成函数不教：属于组合数学 M.5.4 的“生成函数”一章（原书用生成函数推汉诺塔的递推在第 16 章，大纲也没收） |
| 《2-6 循环不变量》 | 初始化、保持、终止（技能大纲写的内容） | `termination`（求最大值和求和两个循环） |

## 后继技能要用的

必须后继里已有内容包的还没有。算法分析与设计 F.1.2 是这条“算法”路线的下一站，按它的综合练习核对：主定理（`divide-conquer`）、用归纳写正确性证明和交换论证（`induction`、`strong-induction`）、循环不变量（`termination`）、等比数列求和 $1 + 2 + 4 + \dots + 2^k < 2^{k+1}$（`induction-practice`）、$\log_2$（`merge-sort`）。其余必须后继（实分析 M.1.6、代数结构 M.3.4、数论 M.3.5、集合论 M.5.1、组合数学 M.5.4、图论 M.5.5、形式语言与自动机 F.2.1、计算逻辑 F.2.4、类型系统 F.3.2、程序验证 F.3.3、搜索与规划 A.1.1、密码学 S.1.2）都要用归纳、反证、关系和递归定义，这一站都教到了。
