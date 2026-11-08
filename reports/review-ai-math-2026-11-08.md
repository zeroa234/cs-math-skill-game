# AI math/content review — M.1.1, M.1.2, M.3.1

> 2026-11-08 由 pi 子代理逐课查错的原始记录（英文）。下面每一条都由主代理核实属实，并已在内容包和核对脚本里改正；改了什么见 docs/development.md“课程验收状态”。行号是改之前的。

Read-only review. Findings only (no style/difficulty/coverage notes). Line numbers are YAML file lines.

## M.1.1 — limits & continuity

### 1. `临界点` definition claims all local extrema are critical points (missing endpoint condition) — medium

- Pack / line: `data/content/M.1.1.yaml:105` (term `临界点`); related card `extreme-value` / “极值出在哪里” around lines 1900–1904.
- Quote: “区间内部、切线水平或没有确定切线（尖角、竖直切线）的点；局部极值只会出现在这些点”
- Why it is wrong: the second clause fails at endpoints. The pack's own definition of `局部极大值` (line 102–103: “f(c) 不小于 c 附近所有点的函数值”) does not exclude endpoints. Example: `f(x) = x` on `[0, 1]`. With one-sided neighbourhoods in the domain, `f(0) = 0` is a local minimum and `f(1) = 1` is a local maximum, but `f'(x) = 1` everywhere and neither endpoint is an interior critical point (also `f'` never vanishes). So a student who trusts “局部极值只会出现在这些点” will miss endpoint local extrema.
- Suggested fix: “区间内部的局部极值只会出现在这些点；端点也可能是局部极值，要单独检查”. Alternatively state explicitly that this pack defines local extrema only at interior points.
- Confidence: medium (depends on whether the course counts endpoint extrema as local extrema; the pack's own wording suggests it does).

M.1.1: no other findings after reading all 21 lessons and the boss.

Verification note (not a finding): the previously flagged `sin x < x < tan x` card (line 1006) now states `0 < x < π/2` and handles `x < 0` by the `-x` symmetry argument; that defect is fixed. All numeric keys in M.1.1 were checked.

## M.1.2 — single-variable differential calculus

### 1. Inverse-function derivative formula is missing the condition `f'(y) ≠ 0` — high

- Pack / line: `data/content/M.1.2.yaml:1160-1162`, lesson `inverse-functions`, card “反函数的导数”.
- Quote: “设 $y = f^{-1}(x)$，那么 $f(y) = x$。两边对 $x$ 求导（左边用链式法则）：$f'(y) \cdot y' = 1$，所以 $$(f^{-1})'(x) = \frac{1}{f'(y)}$$”
- Why it is wrong: the formula only holds when `f'(y) ≠ 0` (and the inverse is differentiable there). If `f'(y) = 0`, the derivation would divide by zero and the inverse has a vertical tangent, not a finite derivative. Concrete example: `f(x) = x^3`, `y = 0`. `f'(0) = 0`, so the formula would give `(f^{-1})'(0) = 1/0`; but `f^{-1}(x) = ∛x`, which this same pack correctly says is not differentiable at 0 (`differentiable` lesson, “∛x 在 0 处连续，差商 … 趋于 +∞，切线是竖直的，也不可导”). The card states the formula as a general rule, so the condition is needed.
- Suggested fix: add “只要 $f'(y) \ne 0$；若 $f'(y) = 0$，反函数在对应点不可导（切线竖直）”.
- Confidence: high.

### 2. “可导函数的局部极值只会出现在驻点” ignores endpoints — medium

- Pack / line: `data/content/M.1.2.yaml:1763`, lesson `fermat-rolle`, card “用导数找临界点”.
- Quote: “由费马定理，可导函数的局部极值只会出现在驻点。”
- Why it is wrong: Fermat's theorem is stated two paragraphs earlier (lines 1741–1743) for an **interior** point `c`; the general sentence drops “区间内部”. Endpoint counterexample: `f(x) = x` on `[0, 1]` is differentiable, has a local minimum at 0 and a local maximum at 1 (one-sided neighbourhoods), but `f'(x) = 1` everywhere, so there is no stationary point. The pack's own `费马定理` term (line 60–61) says “区间内部某点”.
- Suggested fix: “区间内部的局部极值只会出现在驻点；端点也可能是局部极值，要单独检查。”
- Confidence: medium (same endpoint-convention caveat as M.1.1).

M.1.2: no other findings after reading all 31 lessons and the boss. All numeric keys checked (including the `''` → `'` YAML escaping in derivative notation, e.g. `f''(3)` renders as `f'(3)`).

## M.3.1 — linear algebra

### 1. Determinant sign after row swaps is wrong for an even number of swaps — high

- Pack / line: `data/content/M.3.1.yaml:856`, lesson `determinant`, card “推出来的性质”.
- Quote: “所以 $\det A$ = 主元的乘积（换过行就再乘 $-1$）。”
- Why it is wrong: after row exchanges the sign is `(-1)^k`, where `k` is the number of swaps, not a single `-1` whenever any swap occurred. Two swaps give `+1`. Example: the 3-cycle permutation matrix `A = [[0,1,0],[0,0,1],[1,0,0]]` has `det A = +1`. Reducing it to `I` needs two row swaps, and the resulting `U` has pivots `1,1,1`, so `det A = (+1)·1·1·1 = +1`; the parenthetical rule would give `-1`. (A single swap, e.g. `[[0,1],[1,0]]`, correctly gives `-1`.)
- Suggested fix: “换过奇数次行乘 $-1$，偶数次不变；更准确地说 $\det A = \det P \cdot \prod$ 主元，其中 $PA=LU$。”
- Confidence: high.

### 2. `方差` term definition uses `n`, the lesson uses `n − 1` — high

- Pack / lines: term at `data/content/M.3.1.yaml:119`; card “方差” at line 2343; item `variance` at line 2355 (and PCA card at 2351).
- Quote: term: “一组数离它们的平均值有多散：各数减平均值后平方，再平均”; card: “各数减去平均值，平方，加起来，除以（个数 − 1）”.
- Why it is wrong: “再平均” means divide by the number of terms `n` (population variance), but the card and item use the sample variance with `n − 1`. The two definitions give different answers. For `1, 2, 6`: mean 3, squared deviations `4, 1, 9`; population variance `14/3 ≈ 4.667`, sample variance `14/2 = 7` — the item's key is 7. For the card's `3, 5, 7`, population variance is `8/3 ≈ 2.667`, but the card says 4. A student who reads the clickable term definition will compute a different number from the lesson.
- Suggested fix: make the term definition “样本方差：各数减平均值后平方，加起来，除以（个数 − 1）”, or use `n` consistently in the card/item and change the key (7 would become 14/3).
- Confidence: high.

### 3. `余子式` is defined as the signed cofactor, not the minor — medium

- Pack / lines: term at `data/content/M.3.1.yaml:52-53`; card “余子式展开” at line 900.
- Quote: “$C_{ij}$ 叫**余子式（cofactor）**：去掉第 $i$ 行第 $j$ 列，剩下的 2×2 行列式，再乘 $(-1)^{i+j}$”.
- Why it is wrong (terminology/fact): in standard Chinese terminology, `余子式` (minor) `M_ij` is the determinant left after deleting row `i` and column `j`, **without** the sign. The signed quantity `(-1)^{i+j} M_ij` is the `代数余子式` (cofactor). The formulas in this pack (expansion by cofactors, `A^{-1} = C^T/\det A`) are correct only because `C` already includes the sign; a student who takes the literal `余子式` (unsigned minor) and uses it in `A^{-1} = C^T/\det A` gets wrong signs. The English gloss `cofactor` is right, but the Chinese term is not.
- Suggested fix: rename to “代数余子式（cofactor）”, or define `余子式 M_ij` without the sign and then define `代数余子式 C_ij = (-1)^{i+j} M_ij` for the expansion/inverse formulas.
- Confidence: medium (mathematical formulas are right; the defect is the term/definition mismatch).

### 4. `特解` is used for nullspace “special solutions”, colliding with the standard meaning — medium

- Pack / lines: term at `data/content/M.3.1.yaml:66-67`; card “特解” at line 1098; item `n-minus-r` at line 1122; complete-solution card uses `x_p` at line 1178.
- Quote: “令一个自由未知数为 1、其余为 0 得到的 Ax = 0 的解” / “叫**特解（special solution）**”.
- Why it is a defect: in standard Chinese linear algebra, `特解` means a particular solution of the nonhomogeneous system `Ax = b` (the `x_p` in the complete-solution card). The nullspace basis vectors obtained by setting one free variable to 1 and the rest to 0 are Strang's “special solutions”, usually called `特殊解` or `基础解` (or `基础解系`), not `特解`. As written, the item “Ax = 0 有几个特解？” (answer 2) is ambiguous/confusing to a student who learned the standard meaning, and the later `x_p` is not called `特解` even though that is the standard term.
- Suggested fix: rename these to “特殊解/基础解（special solution）” throughout, and reserve “特解” for `x_p` in `Ax = b`; or add an explicit note that this pack follows Strang's “special solution” naming.
- Confidence: medium.

### 5. SVD recipe `u_i = Av_i/σ_i` is undefined when `σ_i = 0` — high

- Pack / line: `data/content/M.3.1.yaml:2272`, lesson `svd`, card “怎么求”.
- Quote: “$u_i = \frac{Av_i}{\sigma_i}$”
- Why it is wrong (missing condition): this only works for `σ_i > 0` (and for `i ≤ min(m,n)`). The preceding card claims the SVD for **any** `m × n` matrix, including rank-deficient ones, where some singular values are 0. Example: `A = [[1,0],[0,0]]` has `σ_1 = 1`, `σ_2 = 0`; with `v_2 = (0,1)`, `Av_2 = 0`, so the recipe gives `u_2 = 0/0`. The remaining columns of `U` must be chosen as an orthonormal basis of the left nullspace, not by this formula.
- Suggested fix: “对 `σ_i > 0` 的 `i`，取 `u_i = Av_i/σ_i`；`σ_i = 0` 时从左零空间取一组标准正交向量，和已有的 `u_i` 一起补满 `U`。”
- Confidence: high.

M.3.1: no other findings after reading all 30 lessons and the boss. All numeric keys checked (determinants, ranks, projections, least squares, eigenvalues, SVD examples, condition number, Jacobi).
