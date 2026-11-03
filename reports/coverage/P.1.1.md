# P.1.1 程序设计基础：覆盖表

规则见 `docs/content-authoring.md` 的“知识覆盖面标准”。依据：skill-tree 大纲 `../cs-math-skill-tree/data/outlines/P.1.1.json`（Python 官方教程第 3–8 章 + CS50x 三个调试短片，2026-11-01 核对原文）。“节”是技能内部编号（游戏知识导览里的编号），“原文”是教程自己的节号和标题。

`node scripts/check-coverage.mjs P.1.1` 自动检查：每一节都有一行；写的课 id 都在内容包里；大纲 `coverage` 点名的节都有课。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | 3.1 Using Python as a Calculator | `first-program`, `numbers` |
| 1.2 | 3.1.1 Numbers | `numbers`, `text-and-truth` |
| 1.3 | 3.1.2 Text | `text-and-truth`, `slicing` |
| 1.4 | 3.1.3 Lists | `lists-dicts`, `aliasing`, `slicing` |
| 1.5 | 3.2 First Steps Towards Programming | `naming`, `while-loops` |
| 2.1 | 4.1 if Statements | `if-else` |
| 2.2 | 4.2 for Statements | `for-loops` |
| 2.3 | 4.3 The range() Function | `for-loops` |
| 2.4 | 4.4 break and continue Statements | `while-loops`, `loop-control` |
| 2.5 | 4.5 else Clauses on Loops | `loop-control` |
| 2.6 | 4.6 pass Statements | `loop-control` |
| 2.7 | 4.7 match Statements | `match` |
| 2.8 | 4.8 Defining Functions | `functions` |
| 2.9 | 4.9 More on Defining Functions | `scope-defaults`, `more-functions` |
| 2.10 | 4.10 Intermezzo: Coding Style | `more-functions` |
| 3.1 | 5.1 More on Lists | `list-methods`, `loop-techniques` |
| 3.2 | 5.2 The del statement | `list-methods` |
| 3.3 | 5.3 Tuples and Sequences | `tuples-sets` |
| 3.4 | 5.4 Sets | `tuples-sets` |
| 3.5 | 5.5 Dictionaries | `lists-dicts`, `tuples-sets`, `loop-techniques` |
| 3.6 | 5.6 Looping Techniques | `loop-techniques` |
| 3.7 | 5.7 More on Conditions | `if-else`, `conditions-more` |
| 3.8 | 5.8 Comparing Sequences and Other Types | `conditions-more` |
| 4.1 | 6.1 More on Modules | `modules`, `modules-packages` |
| 4.2 | 6.2 Standard Modules | `modules`, `modules-packages` |
| 4.3 | 6.3 The dir() Function | `modules-packages` |
| 4.4 | 6.4 Packages | `modules-packages` |
| 5.1 | 7.1 Fancier Output Formatting | `input-output` |
| 5.2 | 7.2 Reading and Writing Files | `files` |
| 6.1 | 8.1 Syntax Errors | `first-program`, `debugging` |
| 6.2 | 8.2 Exceptions | `debugging`, `exceptions` |
| 6.3 | 8.3 Handling Exceptions | `exceptions` |
| 6.4 | 8.4 Raising Exceptions | `exceptions` |
| 6.5 | 8.5 Exception Chaining | `cleanup` |
| 6.6 | 8.6 User-defined Exceptions | `cleanup` |
| 6.7 | 8.7 Defining Clean-up Actions | `cleanup` |
| 6.8 | 8.8 Predefined Clean-up Actions | `files`, `cleanup` |
| 7 | CS50x Debugging: Step Into | `call-stack` |
| 8 | CS50x Debugging: Step Through | `debugging`, `call-stack` |
| 9 | CS50x Call Stacks | `call-stack` |

教到什么深度（入门层）：
- 4.9 的仅限位置参数 `/` 和仅限关键字参数 `*`（4.9.3）只讲“看到了认得出”，函数注解（4.9.8）同样只认得出；`*args`、`**kwargs`、解包实参、lambda、文档字符串都讲并练。
- 5.1 的“把列表当队列用”讲 `collections.deque` 的 `append` / `popleft`，原因（从列表头部删除很慢）留给数据结构一站细讲。
- 6.1 的“模块搜索路径”和“编译过的 .pyc 文件”只讲到“Python 先在当前文件夹找，找到的模块会缓存成 `__pycache__` 里的文件”。
- 7.1 讲 f-string 的格式说明（宽度、对齐、小数位数、千位分隔）、`str.format`、`str()` 与 `repr()`；手动格式化（`rjust` 等）和旧式 `%` 只认得出。
- 7.2 讲 `open`、`with`、读写模式、`encoding="utf-8"`、按行读，以及用 `json` 存取结构化数据。
- 8.5、8.6 讲 `raise … from …` 和 `class 名字(Exception): pass` 的最小写法；`class` 本身属于 P.1.2，这里只当固定写法用。异常组 `ExceptionGroup`（8.9）、异常注释 `add_note`（8.10）不在大纲里，不教。

## CS2023（`data/curation/scope.json`）

| 知识点 | CS2023 主题（scope.json 匹配原文） | 课 |
|---|---|---|
| 变量 | SDF-Fundamentals，CS Core：variables, primitive data types | `naming`, `numbers`, `text-and-truth` |
| 控制流 | SDF-Fundamentals，CS Core：conditional and iterative statements | `if-else`, `for-loops`, `while-loops`, `loop-control`, `loop-techniques`, `conditions-more`, `match` |
| 函数 | SDF-Fundamentals，CS Core：Key modularity constructs such as functions | `functions`, `scope-defaults`, `more-functions` |
| 模块 | SDF-Fundamentals，CS Core：Key modularity constructs | `modules`, `modules-packages` |
| 基本数据类型 | SDF-Fundamentals，CS Core：primitive data types | `numbers`, `text-and-truth`, `lists-dicts`, `slicing`, `tuples-sets`, `list-methods` |
| 输入输出与调试 | SDF-Fundamentals，CS Core：Input and output using files and APIs | `input-output`, `files`（API 这一半：读写 JSON 文件，以及 `modules-packages` 里用标准库模块的接口） |

## 综合练习（原技能树 D1，约 40 分钟）

| 小题 | 要用到 | 课 |
|---|---|---|
| (1) is_prime、打印 1–50 的素数、为什么试到 √n | while、函数、取余、列表推导式 | `while-loops`, `functions`, `loop-techniques`，结业挑战 `primes`、`sqrt-reason` |
| (2) top_words(text, k=3)：忽略大小写和标点计数，取前 k 个 | `lower`、`split`、去标点、字典计数、按次数排序 | `slicing`, `loop-techniques`, `more-functions`, `word-count` |
| (3) 修 average 的 bug、处理空列表、写两个测试 | 单步找 bug、`raise ValueError`、`assert` | `debugging`, `exceptions` |
| (4) global 的作用；默认参数 `acc=[]` 的陷阱 | 局部与全局、默认值只算一次 | `scope-defaults` |

## 后继技能用到的写法（C5）

这条路线上以 P.1.1 为必须前置的是 P.2.2、F.1.1、C.1.1。

| 后继 | 直接用到、又不自己教的 | 课 |
|---|---|---|
| F.1.1 数据结构 | 列表的增删（append、pop、insert）、切片、元组解包、`collections.deque`、字典、`in`、`for … in enumerate(…)` | `list-methods`, `slicing`, `tuples-sets`, `modules-packages`, `loop-techniques` |
| F.1.1 数据结构 | `class` 定义一个节点、递归 | 不在这一站：F.1.1 自己教（`class` 属于 P.1.2，F.1.1 只用最小写法） |
| C.1.1 计算机组成原理 | `bin()`、`hex()`、`int("1011", 2)`、位运算 | 不在这一站：C.1.1 讲二进制时一起教 |
| P.2.2 C/C++ | 函数、循环、列表、读报错 | 已有各课 |
