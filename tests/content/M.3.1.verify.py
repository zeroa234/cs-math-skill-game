# Checks every number data/content/M.3.1.yaml states, with exact sympy matrices and numpy for floats.
# usage: .venv/Scripts/python.exe -I tests/content/M.3.1.verify.py   (prints "N/N claims hold"; exit 1 on a mismatch)
import inspect, math, sys
import numpy as np
import sympy as sp
from fractions import Fraction as F

checks = []
def add(got, want, tol=1e-9):
    line = inspect.stack()[1].lineno
    if isinstance(got, (float, np.floating)) or isinstance(want, float):
        ok = abs(float(got) - float(want)) <= tol
    else:
        ok = got == want
    checks.append((ok, got, want, line))
M = sp.Matrix
def vec(*a): return M(a)
def rref(A): return A.rref()

# ---------------- vectors
add(vec(3, 1) + vec(1, 2), vec(4, 3))
v, w = vec(1, 2), vec(3, -1)
add(v + w, vec(4, 1)); add(2 * v, vec(2, 4)); add(2 * v - w, vec(-1, 5)); add(2 * v + w, vec(5, 3))
add(3 * vec(1, 1) + 2 * vec(1, -1), vec(5, 1))
c, d = sp.symbols("c d"); add(sp.solve([c + d - 5, c - d - 1], [c, d]), {c: 3, d: 2})

# ---------------- two-pictures
x, y, z = sp.symbols("x y z")
add(sp.solve([x - 2 * y - 1, 3 * x + 2 * y - 11], [x, y]), {x: 3, y: 1})
add([3 - 2 * 1 == 1, 3 * 3 + 2 * 1 == 11], [True, True])
add([(1 - 0) == 1, (3 - 2 * 1) == 1, 3 * 3 + 2 * 1 == 11, 3 * 1 + 2 * 4 == 11], [True] * 4)   # points on the lines
add(3 * vec(1, 3) + 1 * vec(-2, 2), vec(1, 11)); add(1 * vec(1, 3) + 3 * vec(-2, 2), vec(-5, 9))
A = M([[1, -2], [3, 2]]); add(A * vec(3, 1), vec(1, 11)); add(vec(1, -2).dot(vec(3, 1)), 1)
add(M([[2, 1], [1, 3]]) * vec(1, 2), vec(4, 7))
add(M([[1, 0, 2], [0, 1, 1]]) * vec(1, 2, 3), vec(7, 5))

# ---------------- elimination
add(sp.solve([x + y - 5, 2 * x + 3 * y - 13], [x, y]), {x: 2, y: 3})
add(sp.solve([x + 2 * y + z - 4, 2 * x + 5 * y + 3 * z - 9, x + 3 * y + 3 * z - 6], [x, y, z]), {x: 3, y: 0, z: 1})
add(sp.solve([x + y + z - 6, 2 * x + 3 * y + z - 11, x + 2 * y + 3 * z - 14], [x, y, z]), {x: 1, y: 2, z: 3})
add(sp.expand((2 * x + 3 * y + z) - 2 * (x + y + z)), y - z); add(11 - 12, -1)
add(sp.solve([x - 2 * y - 1, 2 * x - 4 * y - 11], [x, y]), []); add(11 - 2 * 1, 9)
add(len(sp.solve([x - 2 * y - 1, 2 * x - 4 * y - 2], [x, y], dict=True)[0]), 1)  # one free variable: a line of solutions
add(sp.solve([2 * y - 4, 3 * x + 2 * y - 5], [x, y]), {x: sp.Rational(1, 3), y: 2})

# ---------------- elimination-matrices
E = M([[1, 0], [-3, 1]]); add(E * M([[1, 2], [3, 8]]), M([[1, 2], [0, 2]]))
P23 = M([[1, 0, 0], [0, 0, 1], [0, 1, 0]]); B = M([[1, 2, 3], [4, 5, 6], [7, 8, 9]]); add(P23 * B, M([[1, 2, 3], [7, 8, 9], [4, 5, 6]]))
add(M([[0, 1], [1, 0]]) * M([[0, 2], [3, 2]]), M([[3, 2], [0, 2]]))

# ---------------- matrix-rules
A, B = M([[1, 2], [3, 4]]), M([[5, 6], [7, 8]])
add(A * B, M([[19, 22], [43, 50]])); add((B * A)[0, 0], 23); add(B * A, M([[23, 34], [31, 46]]))
add(M([[0, 1], [0, 0]]) * M([[0, 0], [1, 0]]), M([[1, 0], [0, 0]])); add(M([[0, 0], [1, 0]]) * M([[0, 1], [0, 0]]), M([[0, 0], [0, 1]]))
U = M([[1, 1], [0, 1]]); add(U**2, M([[1, 2], [0, 1]])); add(U**3, M([[1, 3], [0, 1]])); add((U**5)[0, 1], 5)
add(sp.shape(sp.zeros(2, 3) * sp.zeros(3, 4)), (2, 4))

# ---------------- inverse
add(M([[1, 2], [2, 4]]) * vec(2, -1), vec(0, 0))
A = M([[2, 1], [5, 3]]); add(A.inv(), M([[3, -1], [-5, 2]])); add(A.det(), 1); add(A.inv() * vec(1, 2), vec(1, -1))
add(M([[1, 2], [2, 4]]).det(), 0)
add(M([[2, 1], [1, 1]]).inv(), M([[1, -1], [-1, 2]]))
add(M([[2, 1, 1, 0], [1, 1, 0, 1]]).rref()[0], M([[1, 0, 1, -1], [0, 1, -1, 2]]))
add(M([[2, 1, 1, 0], [0, sp.Rational(1, 2), -sp.Rational(1, 2), 1]]).row(0) - 2 * M([[0, sp.Rational(1, 2), -sp.Rational(1, 2), 1]]), M([[2, 0, 2, -2]]))

# ---------------- lu
A = M([[2, 1], [6, 8]]); L, Uu, _ = A.LUdecomposition(); add((L, Uu), (M([[1, 0], [3, 1]]), M([[2, 1], [0, 5]])))
L, Uu, _ = M([[1, 2], [4, 9]]).LUdecomposition(); add((L[1, 0], Uu), (4, M([[1, 2], [0, 1]])))
A3 = M([[2, 1, 0], [1, 2, 1], [0, 1, 2]]); L, Uu, _ = A3.LUdecomposition()
add(L, M([[1, 0, 0], [sp.Rational(1, 2), 1, 0], [0, sp.Rational(2, 3), 1]])); add(Uu, M([[2, 1, 0], [0, sp.Rational(3, 2), 1], [0, 0, sp.Rational(4, 3)]]))
add(L * Uu, A3)
L, Uu, _ = M([[1, 1, 0], [1, 2, 1], [0, 1, 2]]).LUdecomposition(); add(Uu, M([[1, 1, 0], [0, 1, 1], [0, 0, 1]]))
L, Uu = M([[1, 0], [3, 1]]), M([[2, 1], [0, 5]]); cc = L.solve(vec(3, 19)); add(cc, vec(3, 10)); xx = Uu.solve(cc); add(xx, vec(sp.Rational(1, 2), 2))
add(M([[2, 1], [6, 8]]) * xx, vec(3, 19))
add(round(1000**3 / 3 / 1e8, 1), 3.3); add(1000**2, 1000000); add(round(100**3 / 3), 333333); add(100**2, 10000)

# ---------------- transpose
A = M([[1, 2, 3], [0, 6, 4]]); add(A.T, M([[1, 0], [2, 6], [3, 4]])); add(A.T[2, 0], 3)
R = M([[1, 2], [3, 4], [5, 6]]); add(R.T * R, M([[35, 44], [44, 56]]))
add(math.factorial(3), 6)
P = M([[0, 1, 0], [0, 0, 1], [1, 0, 0]]); add(P.T * P, sp.eye(3)); add(P * P == sp.eye(3), False); add(P**3, sp.eye(3))
AA, BB = sp.Matrix(2, 2, sp.symbols("a0:4")), sp.Matrix(2, 2, sp.symbols("b0:4")); add(sp.simplify((AA * BB).T - BB.T * AA.T), sp.zeros(2, 2))

# ---------------- determinant
add(M([[2, 0], [0, 3]]).det(), 6); add(M([[3, 1], [2, 4]]).det(), 10); add(M([[1, 2], [2, 4]]).det(), 0)
add(A3.det(), 4); add(2 * sp.Rational(3, 2) * sp.Rational(4, 3), 4)
X = sp.Matrix(3, 3, sp.symbols("m0:9")); add(sp.expand((2 * X).det() - 8 * X.det()), 0); add(2**3 * 5, 40)
add(3 * (-2), -6)

# ---------------- cofactors
C = M([[1, 2, 3], [0, 4, 5], [1, 0, 6]]); add(C.det(), 22)
add([M([[4, 5], [0, 6]]).det(), M([[0, 5], [1, 6]]).det(), M([[0, 4], [1, 0]]).det()], [24, -5, -4]); add(24 + 10 - 12, 22)
add(M([[2, 0, 1], [1, 3, 2], [0, 1, 1]]).det(), 3)
add(math.factorial(4), 24); add(math.factorial(10), 3628800)
A = M([[2, 1], [1, 3]]); add(A.det(), 5); add(M([[5, 1], [5, 3]]).det(), 10); add(M([[2, 5], [1, 5]]).det(), 5); add(A.solve(vec(5, 5)), vec(2, 1))
add(M([[1, 0, 0], [0, 2, 0], [1, 1, 3]]).det(), 6)
add(abs(M([[4, 1], [1, 3]]).det()) / sp.Integer(2), sp.Rational(11, 2))
add(C.inv(), C.adjugate() / C.det())

# ---------------- subspaces
A = M([[1, 0], [4, 3], [2, 3]])
add(A * vec(1, 1), vec(1, 7, 5))
add(A.col_insert(2, vec(1, 0, 0)).rank(), 3)        # (1,0,0) not in C(A)
add(A.col_insert(2, vec(0, 0, 1)).rank(), 3)
add(4 + 3 * sp.Rational(-4, 3), 0); add(2 + 3 * sp.Rational(-4, 3), -2)
add(A.rank(), 2)

# ---------------- nullspace
A = M([[1, 2], [2, 4]]); add(A * vec(2, -1), vec(0, 0))
A = M([[1, 2, 3], [2, 4, 6], [1, 0, 1]])
R, piv = A.rref(); add(R, M([[1, 0, 1], [0, 1, 1], [0, 0, 0]])); add(piv, (0, 1)); add(A.rank(), 2)
add(A.nullspace(), [vec(-1, -1, 1)])
add(A.row(1) - 2 * A.row(0), M([[0, 0, 0]])); add(M([[1, 0, 1]]) - M([[1, 2, 3]]), M([[0, -2, -2]]))
A4 = M([[1, 2, 2, 4], [3, 8, 6, 16]]); R4, piv4 = A4.rref(); add(R4, M([[1, 0, 2, 0], [0, 1, 0, 2]])); add(piv4, (0, 1))
add(A4.nullspace(), [vec(-2, 0, 1, 0), vec(0, -2, 0, 1)])
add(R4 * vec(-2, -2, 1, 1), vec(0, 0)); add(R4 * vec(2, 0, 1, 0), vec(4, 0)); add(R4 * vec(1, 1, 1, 1), vec(3, 3))
add(5 - 3, 2)

# ---------------- complete-solution
add([3 + 2 * 0 == 3, 1 + 2 * 1 == 3], [True, True]); add(vec(3, 0) + vec(-2, 1), vec(1, 1))
A = M([[1, 3, 0, 2], [0, 0, 1, 4], [1, 3, 1, 6]]); b = vec(1, 6, 7)
Rb, _ = A.row_join(b).rref(); add(Rb, M([[1, 3, 0, 2, 1], [0, 0, 1, 4, 6], [0, 0, 0, 0, 0]]))
add(A * vec(1, 0, 6, 0), b); add(A.nullspace(), [vec(-3, 1, 0, 0), vec(-2, 0, -4, 1)])
add(A.row_join(vec(1, 6, 8)).rank(), 3); add(A.rank(), 2)
add(M([[1, 1, 1], [1, 2, 3], [1, 3, 5], [1, 4, 7], [1, 5, 9]]).nullspace() == [], False)  # an example 5x3 of rank 2 has a nullspace
T = sp.randMatrix(5, 3, -3, 3, seed=3); add(T.rank(), 3); add(T.nullspace(), [])

# ---------------- basis
add(2 * vec(1, 2) - vec(2, 4), vec(0, 0))
add(M([[1, 0, 1], [0, 1, 1]]).nullspace() != [], True)       # three vectors in R^2 are dependent
add(M([[1, 1, 1]]).nullspace(), [vec(-1, 1, 0), vec(-1, 0, 1)])
add(5 * vec(1, 0) + 1 * vec(0, 1), vec(5, 1)); add(3 * vec(1, 1) + 2 * vec(1, -1), vec(5, 1))
add(M([[1, 1], [1, -1]]).solve(vec(4, 2)), vec(3, 1))
add(M([[1, 2, 3], [2, 4, 6], [1, 0, 1]]).columnspace(), [vec(1, 2, 1), vec(2, 4, 0)])

# ---------------- four-subspaces
add((5 - 2, 3 - 2), (3, 1)); add(4 - 3, 1)
A = M([[1, 2, 3], [2, 4, 6], [1, 0, 1]])
add(A.rowspace() is not None, True); add(A.rref()[0][:2, :], M([[1, 0, 1], [0, 1, 1]]))
add(A.T.nullspace(), [vec(-2, 1, 0)]); add((vec(-2, 1, 0).T * A), M([[0, 0, 0]]))
add(6 - 3, 3)

# ---------------- linear-maps / map-matrix / change-basis
add(3 * vec(2, 1) + 2 * vec(-1, 3), vec(4, 9))
TT = M([[2, 1], [-1, 3]]).T; add(TT * vec(3, 2), vec(4, 9))
add(M([[2, 0], [1, 1]]) * vec(3, 5), vec(6, 8))
Rot = M([[0, -1], [1, 0]]); add(Rot * vec(1, 0), vec(0, 1)); add(Rot * vec(0, 1), vec(-1, 0)); add(Rot**2, M([[-1, 0], [0, -1]]))
Prj = M([[1, 0], [0, 0]]); add(Prj * vec(1, 0), vec(1, 0)); add(Prj * vec(0, 1), vec(0, 0)); add(Prj.det(), 0)
Ref = M([[0, 1], [1, 0]]); add(Ref * vec(3, 5), vec(5, 3)); add(Rot * vec(0, 1) == vec(1, 0), False)
add(M([[1, 0], [0, -1]]) * vec(3, 5), vec(3, -5))
A = M([[2, 1], [1, 2]]); add(A * vec(1, 1), vec(3, 3)); add(A * vec(1, -1), vec(1, -1)); add(A * vec(1, 0), vec(2, 1))
Bm = M([[1, 1], [1, -1]]); add(Bm.inv() * A * Bm, sp.diag(3, 1))
add(Bm.solve(vec(4, 2)), vec(3, 1)); add(9 * vec(1, 1) + 1 * vec(1, -1), vec(10, 8)); add(A * vec(4, 2), vec(10, 8))
add(Bm.solve(vec(6, 2)), vec(4, 2)); add(12 * vec(1, 1) + 2 * vec(1, -1), A * vec(6, 2)); add(A * vec(6, 2), vec(14, 10))
add((Bm.inv() * A * Bm).det(), A.det())

# ---------------- length-angle
add(sp.sqrt(3**2 + 4**2), 5); add(vec(3, 4) / 5, vec(sp.Rational(3, 5), sp.Rational(4, 5)))
add(round(1 / 3, 3), 0.333); add(sp.sqrt(1 + 4 + 4), 3)
add(math.degrees(math.acos(1 / math.sqrt(2))), 45.0, 1e-9); add(round(1 / math.sqrt(2), 4), 0.7071)
add(vec(1, 2, -1).dot(vec(2, -1, 0)), 0)
add(vec(1, 2).dot(vec(3, 1)), 5); add(round(5 / math.sqrt(50), 3), 0.707)

# ---------------- orthogonal
add(vec(1, 0, 1).dot(vec(-1, -1, 1)), 0); add(vec(1, 2, 3).dot(vec(-1, -1, 1)), 0)
add(M([[1, 1, 1]]).nullspace(), [vec(-1, 1, 0), vec(-1, 0, 1)]); add(vec(1, 1, 1).dot(vec(1, 1, 1)), 3)
A = M([[1, 2, 3], [2, 4, 6], [1, 0, 1]]); xr = vec(1, 1, 1); xn = vec(-1, -1, 1); add(A * (xr + 5 * xn), A * xr)

# ---------------- projection
b, u = vec(1, 2, 2), vec(1, 0, 1)
add((u.dot(b), u.dot(u)), (3, 2)); p = u.dot(b) / u.dot(u) * u; add(p, vec(sp.Rational(3, 2), 0, sp.Rational(3, 2)))
e = b - p; add(e, vec(-sp.Rational(1, 2), 2, sp.Rational(1, 2))); add(e.dot(u), 0)
a = vec(1, 2, 2); add((a.dot(vec(1, 1, 1)), a.dot(a)), (5, 9)); add(round(5 / 9, 3), 0.556)
a = vec(1, 1); Pm = a * a.T / a.dot(a); add(Pm, M([[sp.Rational(1, 2)] * 2] * 2)); add(Pm**2, Pm)

# ---------------- least-squares
A = M([[1, 0], [1, 1], [1, 2]]); b = vec(6, 0, 0)
add(A.T * A, M([[3, 3], [3, 5]])); add(A.T * b, vec(6, 0)); xh = (A.T * A).solve(A.T * b); add(xh, vec(5, -3))
add(A * xh, vec(5, 2, -1)); add(b - A * xh, vec(1, -2, 1)); add((b - A * xh).dot(b - A * xh), 6)
add((A.T * (b - A * xh)), vec(0, 0))
b2 = vec(1, 3, 4); add(A.T * b2, vec(8, 11)); x2 = (A.T * A).solve(A.T * b2); add(x2, vec(sp.Rational(7, 6), sp.Rational(3, 2)))
add(np.polyfit([0, 1, 2], [6, 0, 0], 1).round(9).tolist(), [-3.0, 5.0])

# ---------------- gram-schmidt
Q = M([[1, 1], [1, -1]]) / sp.sqrt(2); add(sp.simplify(Q.T * Q), sp.eye(2)); add(sp.simplify(Q.inv() - Q.T), sp.zeros(2, 2)); add(sp.simplify(Q - Q.T), sp.zeros(2, 2))
a, bb = vec(3, 4), vec(1, 0); B2 = bb - a.dot(bb) / a.dot(a) * a; add(B2, vec(sp.Rational(16, 25), -sp.Rational(12, 25))); add([float(t) for t in B2], [0.64, -0.48]); add(a.dot(B2), 0)
a, bb = vec(1, 1, 0), vec(1, 0, 1); add((a.dot(a), a.dot(bb)), (2, 1)); B3 = bb - a.dot(bb) / a.dot(a) * a; add(B3, vec(sp.Rational(1, 2), -sp.Rational(1, 2), 1)); add(a.dot(B3), 0)
add(B3.dot(B3), sp.Rational(3, 2))
Qn, Rn = np.linalg.qr(np.array([[1, 1], [1, 0], [0, 1]], float)); add(abs(Rn[1, 0]) < 1e-12, True)

# ---------------- eigen
A = M([[2, 1], [1, 2]]); add(sorted(A.eigenvals().keys()), [1, 3])
add(sp.factor((A - sp.Symbol("l") * sp.eye(2)).det()), sp.factor((2 - sp.Symbol("l"))**2 - 1))
add(A * vec(1, 1), 3 * vec(1, 1)); add(A * vec(1, -1), vec(1, -1))
A = M([[4, 1], [2, 3]]); add(sorted(A.eigenvals().keys()), [2, 5]); add(A.trace(), 7); add(A.det(), 10)
add(A * vec(1, 1), 5 * vec(1, 1)); add(A * vec(1, -2), vec(2, -4)); add(A * vec(1, 0), vec(4, 2))
add(sorted(M([[3, 0], [0, -1]]).eigenvals().keys()), [-1, 3])
a = vec(1, 2); Pm = a * a.T / a.dot(a); add(sorted(Pm.eigenvals().keys()), [0, 1])
add(M([[2, 1], [1, 2]]) * vec(1, 1), vec(3, 3))

# ---------------- diagonalize
A = M([[4, 1], [2, 3]]); X = M([[1, 1], [1, -2]]); Lm = sp.diag(5, 2); add(X * Lm * X.inv(), A)
add(A**2, M([[18, 7], [14, 11]])); add((A**2).trace(), 29); add((A**2).det(), 100); add(18 * 11 - 7 * 14, 100)
add(sorted((A**3).eigenvals().keys()), [8, 125])
J = M([[1, 1], [0, 1]]); add(J.is_diagonalizable(), False); add((J - sp.eye(2)).nullspace(), [vec(1, 0)])
Fm = M([[1, 1], [1, 0]]); ev = sorted(Fm.eigenvals().keys(), key=lambda t: float(t))
add(ev, sorted([(1 - sp.sqrt(5)) / 2, (1 + sp.sqrt(5)) / 2], key=lambda t: float(t))); add(round(float(ev[1]), 3), 1.618); add(round(float(ev[0]), 3), -0.618)
fib = [0, 1]
for _ in range(25): fib.append(fib[-1] + fib[-2])
add(fib[:7], [0, 1, 1, 2, 3, 5, 8]); add(fib[20], 6765); add(round(((1 + 5**0.5) / 2)**20 / 5**0.5), 6765)
add((Fm**5) * vec(1, 0), vec(fib[6], fib[5]))
add(0.5**10, 1 / 1024)

# ---------------- symmetric
B = M([[2, 1], [1, 2]]); Q = M([[1, 1], [1, -1]]) / sp.sqrt(2); add(sp.simplify(Q * sp.diag(3, 1) * Q.T), B)
add(round(1 / math.sqrt(2), 3), 0.707)
S = M([[3, 4], [4, -3]]); add(sorted(S.eigenvals().keys()), [-5, 5]); add((S.trace(), S.det()), (0, -25))
q1, q2 = vec(1, 1) / sp.sqrt(2), vec(1, -1) / sp.sqrt(2); add(sp.simplify(3 * q1 * q1.T + 1 * q2 * q2.T), B)
Sr = np.array([[4, 1, 0], [1, 3, 1], [0, 1, 5]], float); wv, Vv = np.linalg.eigh(Sr); add(np.allclose(Vv.T @ Vv, np.eye(3)), True)

# ---------------- positive-definite
xs, ys = sp.symbols("xs ys"); add(sp.expand(2 * xs**2 + 2 * xs * ys + 2 * ys**2 - (xs**2 + ys**2 + (xs + ys)**2)), 0)
add(2 - 2 + 2, 2)
add(sorted(M([[2, 1], [1, 2]]).eigenvals().keys()), [1, 3]); add(M([[2, 1], [1, 2]]).is_positive_definite, True)
add(sorted(M([[1, 2], [2, 1]]).eigenvals().keys()), [-1, 3]); add(M([[-1, 0], [0, -1]]).is_negative_definite, True)
add(M([[2, 1], [1, 2]]).det(), 3)
xv = vec(1, -1); add(M([[2, 1], [1, 2]]) * xv, vec(1, -1)); add((xv.T * M([[2, 1], [1, 2]]) * xv)[0], 2)
add([M([[1, bv], [bv, 9]]).is_positive_definite for bv in (-3, -2, 0, 2, 3, 4)], [False, True, True, True, False, False])
T = sp.randMatrix(5, 3, -3, 3, seed=3); add((T.T * T).shape, (3, 3)); add((T.T * T).is_positive_definite, True)

# ---------------- svd
add(np.linalg.svd(np.array([[3, 0], [0, -2]], float), compute_uv=False).round(9).tolist(), [3.0, 2.0])
A = M([[3, 0], [4, 5]]); add(A.T * A, M([[25, 20], [20, 25]])); add(sorted((A.T * A).eigenvals().keys()), [5, 45])
add(round(math.sqrt(45), 3), 6.708); add(round(math.sqrt(5), 3), 2.236); add(sp.sqrt(45), 3 * sp.sqrt(5))
v1 = vec(1, 1) / sp.sqrt(2); add(sp.simplify(A * v1 / sp.sqrt(45) - vec(1, 3) / sp.sqrt(10)), vec(0, 0))
add(sp.sqrt(45) * sp.sqrt(5), 15); add(abs(A.det()), 15)
add(np.prod(np.linalg.svd(np.array([[2, 1], [0, 3]], float), compute_uv=False)), 6.0, 1e-9)
add(round(np.linalg.svd(np.array([[3, 0], [4, 5]], float), compute_uv=False)[0], 3), 6.708)
add(np.linalg.norm(np.array([[3, 0], [4, 5]], float), 2), math.sqrt(45), 1e-9)

# ---------------- svd-uses
add(20 * (1 + 1000 + 1000), 40020); add(round(40020 / 1e6 * 100), 4)
add(np.var([3, 5, 7], ddof=1), 4.0); add(np.var([1, 2, 6], ddof=1), 7.0)
Ad = M([[2, -2, 1, -1], [1, -1, 1, -1]]); add(Ad * Ad.T, M([[10, 6], [6, 4]]))
ev = sorted((Ad * Ad.T).eigenvals().keys(), key=lambda t: float(t)); add(ev, [7 - sp.sqrt(45), 7 + sp.sqrt(45)])
add([round(float(t), 3) for t in ev], [0.292, 13.708]); add(round(float(ev[1]) / 14, 3), 0.979)
sv = np.linalg.svd(np.array(Ad.tolist(), float), compute_uv=False); add(np.allclose(sv**2, [float(ev[1]), float(ev[0])]), True)
# Eckart-Young on a random matrix: the rank-2 truncation is at least as close as any of 200 random rank-2 matrices
rng = np.random.default_rng(1); G = rng.normal(size=(8, 6)); Uq, sq, Vq = np.linalg.svd(G); G2 = (Uq[:, :2] * sq[:2]) @ Vq[:2]
add(all(np.linalg.norm(G - G2) <= np.linalg.norm(G - rng.normal(size=(8, 2)) @ rng.normal(size=(2, 6))) for _ in range(200)), True)

# ---------------- numerical
def r3(t):  # round to 3 significant digits
    return 0.0 if t == 0 else float(f"{t:.3g}")
# no pivoting: pivot 0.0001
l = r3(1 / 0.0001); y_ = r3(r3(2 - l * 1) / r3(1 - l * 1)); x_ = r3(r3(1 - y_) / 0.0001)
add((l, y_, x_), (10000.0, 1.0, 0.0))
# pivoting: swap rows, pivot 1
l = r3(0.0001 / 1); y2 = r3(r3(1 - l * 2) / r3(1 - l * 1)); x2_ = r3(2 - y2)
add((y2, x2_), (1.0, 1.0))
exact = np.linalg.solve([[0.0001, 1], [1, 1]], [1, 2]); add(round(exact[0], 4), 1.0001); add(round(exact[1], 4), 0.9999)
add(max([0.001, 5, -8], key=abs), -8)
add(np.linalg.cond(np.array([[1, 0], [0, 0.001]])), 1000.0, 1e-6)
add(np.linalg.solve([[1, 1], [1, 1.0001]], [2, 2.0001]).round(6).tolist(), [1.0, 1.0])
add(np.linalg.solve([[1, 1], [1, 1.0001]], [2, 2.0002]).round(6).tolist(), [0.0, 2.0])
add(np.linalg.solve([[1, 1], [1, 1.0001]], [2, 2.0003]).round(6).tolist(), [-1.0, 3.0])
add(round(np.linalg.cond(np.array([[1, 1], [1, 1.0001]])) / 1e4), 4)
add(round((2.0002 - 2.0001) / 2.0001 * 100, 3), 0.005)
xj = yj = 0.0; seqj = []
for _ in range(5): xj, yj = (1 + yj) / 2, (1 + xj) / 2; seqj.append((xj, yj))
add(seqj[:4], [(0.5, 0.5), (0.75, 0.75), (0.875, 0.875), (0.9375, 0.9375)])
Sj = np.diag([2.0, 2.0]); Aj = np.array([[2.0, -1], [-1, 2]]); add(sorted(np.linalg.eigvals(np.linalg.inv(Sj) @ (Sj - Aj)).real.round(9).tolist()), [-0.5, 0.5])
add(np.linalg.solve(Aj, [1, 1]).round(9).tolist(), [1.0, 1.0])
add(round(0.5**10, 6), 0.000977)

# ---------------- boss
add(M([[3, 2], [4, 3]]).inv(), M([[3, -2], [-4, 3]]))
add(4 - 3, 1)
add(2 * vec(1, 2) + 1 * vec(3, -1), vec(5, 3))
add(M([[4, 2], [2, 3]]).is_positive_definite, True); add(M([[1, 3], [3, 4]]).is_positive_definite, False)
add(sorted(M([[2, 2], [2, 2]]).eigenvals().keys()), [0, 4]); add(M([[1, 3], [3, 4]]).det(), -5); add(M([[4, 2], [2, 3]]).det(), 8)

bad = [(ln, g, w) for (ok, g, w, ln) in checks if not ok]
for ln, g, w in bad:
    print(f"line {ln}: got {g!r}, want {w!r}")
print(f"{len(checks) - len(bad)}/{len(checks)} claims hold")
sys.exit(1 if bad else 0)
