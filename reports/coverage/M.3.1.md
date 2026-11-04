# M.3.1 线性代数：覆盖表

规则见 `docs/content-authoring.md` 的“知识覆盖面标准”。依据：skill-tree 大纲 `../cs-math-skill-tree/data/outlines/M.3.1.json`：Gilbert Strang《Introduction to Linear Algebra》第 5 版第 1–8 章和第 11 章（大纲第 9 组对应书的 11.1–11.3）。“节”是技能内部编号，“原文”是书的节号和标题。

这一站没有必须前置，课从“向量是一列数”讲起，只假设中学代数（解二元一次方程组、勾股定理、平面直角坐标）。书的顺序是先讲向量和消元、再讲矩阵运算；游戏的章按 18.06 的单元排（线性方程组 → 矩阵 → 向量空间 → 线性映射 → 内积与正交分解 → 特征值），课按章排，书里第 5 章行列式放进“矩阵”，第 7 章 SVD 和第 11 章数值线性代数放到“特征值”之后（SVD 要用 $A^TA$ 的特征值，条件数要用奇异值）。第 1.2 节长度与点积的计算在第一章的 `two-pictures` 先用到（行乘列），几何意义在“内积与正交分解”的 `length-angle` 讲。

`node scripts/check-coverage.mjs M.3.1` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | 1.1 Vectors and Linear Combinations | `vectors` |
| 1.2 | 1.2 Lengths and Dot Products | `length-angle`, `two-pictures` |
| 1.3 | 1.3 Matrices | `two-pictures` |
| 2.1 | 2.1 Vectors and Linear Equations | `two-pictures` |
| 2.2 | 2.2 The Idea of Elimination | `elimination` |
| 2.3 | 2.3 Elimination Using Matrices | `elimination-matrices` |
| 2.4 | 2.4 Rules for Matrix Operations | `matrix-rules` |
| 2.5 | 2.5 Inverse Matrices | `inverse` |
| 2.6 | 2.6 Elimination = Factorization: A = LU | `lu` |
| 2.7 | 2.7 Transposes and Permutations | `transpose` |
| 3.1 | 3.1 Spaces of Vectors | `subspaces` |
| 3.2 | 3.2 The Nullspace of A: Solving Ax = 0 and Rx = 0 | `nullspace` |
| 3.3 | 3.3 The Complete Solution to Ax = b | `complete-solution` |
| 3.4 | 3.4 Independence, Basis and Dimension | `basis` |
| 3.5 | 3.5 Dimensions of the Four Subspaces | `four-subspaces` |
| 4.1 | 4.1 Orthogonality of the Four Subspaces | `orthogonal` |
| 4.2 | 4.2 Projections | `projection` |
| 4.3 | 4.3 Least Squares Approximations | `least-squares` |
| 4.4 | 4.4 Orthonormal Bases and Gram-Schmidt | `gram-schmidt` |
| 5.1 | 5.1 The Properties of Determinants | `determinant` |
| 5.2 | 5.2 Permutations and Cofactors | `cofactors` |
| 5.3 | 5.3 Cramer's Rule, Inverses, and Volumes | `cofactors` |
| 6.1 | 6.1 Introduction to Eigenvalues | `eigen` |
| 6.2 | 6.2 Diagonalizing a Matrix | `diagonalize` |
| 6.3 | 6.3 Systems of Differential Equations | 不教：要先会导数和指数函数 $e^{\lambda t}$（一元微分学 M.1.2），属于常微分方程 M.2.1；这一站只讲特征值和对角化，`diagonalize` 用差分方程 $u_{k+1} = Au_k$（斐波那契）讲同一个想法 |
| 6.4 | 6.4 Symmetric Matrices | `symmetric` |
| 6.5 | 6.5 Positive Definite Matrices | `positive-definite` |
| 7.1 | 7.1 Image Processing by Linear Algebra | `svd-uses` |
| 7.2 | 7.2 Bases and Matrices in the SVD | `svd` |
| 7.3 | 7.3 Principal Component Analysis (PCA by the SVD) | `svd-uses` |
| 7.4 | 7.4 The Geometry of the SVD | `svd` |
| 8.1 | 8.1 The Idea of a Linear Transformation | `linear-maps` |
| 8.2 | 8.2 The Matrix of a Linear Transformation | `map-matrix` |
| 8.3 | 8.3 The Search for a Good Basis | `change-basis` |
| 9.1 | 11.1 Gaussian Elimination in Practice | `numerical` |
| 9.2 | 11.2 Norms and Condition Numbers | `numerical` |
| 9.3 | 11.3 Iterative Methods and Preconditioners | `numerical` |

教到什么深度（入门层）：
- 消元、LU、逆矩阵、行列式都用 2×2 和 3×3 的具体数字算；行列式的“大公式”讲 3×3 的 6 项和余子式展开，不讲一般 n 的排列奇偶证明。
- 向量空间讲 $\mathbb{R}^n$ 和它的子空间；矩阵空间、多项式空间只举例说明“也满足同样的规则”，不讲抽象公理的推导。
- 四个子空间讲维数公式和正交关系，用具体矩阵算出每个空间的一组基。
- 线性变换讲定义、“矩阵的列就是基向量的像”、复合等于相乘、换基 $B^{-1}AB$；不讲求导这类无穷维的例子（要先学微积分）。
- SVD 讲 $A = U\Sigma V^T$、奇异值是 $A^TA$ 特征值的平方根、旋转–拉伸–旋转的几何意义、低秩近似和 PCA 的意思；Eckart–Young 定理只讲结论。
- 数值线性代数讲部分主元、条件数 $\sigma_{\max}/\sigma_{\min}$ 的含义（用一个接近奇异的 2×2 例子算出来）、Jacobi 迭代；不讲 Krylov 方法。

## 和原文的核对

2026-11-04 由 pi 子代理逐节整理原文笔记（`temp/research/M.3.1-strang-notes.md`，不入库）：书的官网只免费放出 8 节的正文（1.3、2.5、3.5、6.1、7.1、11.1–11.3），其余 29 节读的是作者本人的 MIT 18.06SC 讲座摘要和官方习题解答。主代理用这份笔记核对了课里的定义和结论：列的组合是 $Ax$ 的主要看法（1.3 原文“With letters, columns are the good way”）、消元的乘数和主元（2.2）、$E_{21}$ 和 $P_{12}$（2.3）、$(AB)^{-1} = B^{-1}A^{-1}$（2.5）、$L$ 存乘数（2.6）、四个子空间的维数 $r, n-r, r, m-r$ 和“列空间的基取 $A$ 的主元列”（3.5）、投影和正规方程 $A^TA\hat x = A^Tb$（4.2、4.3）、Gram–Schmidt 的公式 $B = b - \frac{A^Tb}{A^TA}A$ 和 $A = QR$（4.4）、$\det(A - \lambda I) = 0$（6.1）、奇异值是 $A^TA$ 特征值的平方根、$Av_i = \sigma_iu_i$（7.2）、PCA 先按行减均值（7.3）、小主元 0.0001 的例子和部分主元规则（11.1）、$\kappa = \|A\|\|A^{-1}\|$（11.2）、Jacobi 迭代看 $S^{-1}T$ 的谱半径（11.3）。课里的具体例题（如 $\begin{bmatrix}2&1&0\\1&2&1\\0&1&2\end{bmatrix}$ 的 LU、过 $(0,6),(1,0),(2,0)$ 的直线、$\begin{bmatrix}3&0\\4&5\end{bmatrix}$ 的 SVD、四个点的 PCA）是主代理选的数，不声称出自书中某一页；每个数由 `tests/content/M.3.1.verify.py` 用 numpy 和 sympy 重算核对（289 处）。

## CS2023（`data/curation/scope.json`）

| 知识点 | CS2023 主题（scope.json 匹配原文） | 课 |
|---|---|---|
| 向量空间 | MSF-Linear，KA Core：Linear independence, span, basis | `subspaces`, `basis`, `four-subspaces` |
| 线性映射 | MSF-Linear，KA Core：geometric transformations with matrices | `linear-maps`, `map-matrix`, `change-basis` |
| 线性方程组 | MSF-Linear，KA Core：Solving equations, row-reduction | `two-pictures`, `elimination`, `elimination-matrices`, `nullspace`, `complete-solution` |
| 矩阵 | MSF-Linear，CS Core：Matrices: definition, matrix operations | `two-pictures`, `matrix-rules`, `inverse`, `lu`, `transpose` |
| 特征值 | MSF-Linear，KA Core：Eigenvectors and eigenvalues | `eigen`, `diagonalize`, `symmetric` |
| 内积与正交分解 | MSF-Linear，KA Core：Orthogonality, projection, least-squares | `length-angle`, `orthogonal`, `projection`, `least-squares`, `gram-schmidt` |

## 原技能树的综合练习

| 小题 | 课 |
|---|---|
| (1) 高斯消元解 3 元方程组 | `elimination`（分步例题就是这一题） |
| (2) rank 和零空间的一组基 | `nullspace`（分步例题就是这一题）、`four-subspaces` |
| (3) $\begin{bmatrix}2&1\\1&2\end{bmatrix}$ 的特征值、单位特征向量和正交对角化 | `eigen`、`symmetric`（分步例题） |
| (4) $b = (1,2,2)$ 在 $u = (1,0,1)$ 上的投影 | `projection`（分步例题就是这一题） |

## 后继技能要用的

必须后继里已经有路线经过的是 A.2.1 机器学习（还没有内容包）和 M.6.2.2 回归与统计建模：它们直接用矩阵乘法和转置（`matrix-rules`, `transpose`）、最小二乘的正规方程 $A^TA\hat x = A^Tb$（`least-squares`）、特征值和对称矩阵（`eigen`, `symmetric`）、正定（`positive-definite`，岭回归和凸性）、SVD 和 PCA（`svd`, `svd-uses`，降维）、秩和线性无关（`basis`，共线性）、条件数（`numerical`，病态的回归问题）。
