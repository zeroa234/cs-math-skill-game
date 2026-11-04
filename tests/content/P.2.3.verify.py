# Checks every output, number and error message data/content/P.2.3.yaml states, by running the code for real:
# plain Python for the language lessons (scripts are run as separate processes with their command-line
# arguments, in a scratch folder), IPython's own shell for the magic commands, and NumPy, SciPy, pandas,
# Matplotlib, seaborn and statsmodels for the rest (versions printed below).
# Every graded number item's `answer` and every text item's `answers` is read from the pack and compared with
# the value computed here (NUM / TEXT below); choice items whose right option is an output are checked the
# same way (CHOICE). The run fails if a number or text item has no computed value, or anything disagrees.
# usage: .venv/Scripts/python.exe -I tests/content/P.2.3.verify.py   (prints "N/N claims hold", exit 1 on a mismatch)
# The .venv needs numpy scipy pandas matplotlib seaborn statsmodels ipython pyyaml
# (pip install with PIP_CACHE_DIR on the project drive).
import contextlib, inspect, io, math, os, shutil, subprocess, sys, textwrap, warnings
import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SCRATCH = os.path.join(ROOT, "temp", "p23-verify")
shutil.rmtree(SCRATCH, ignore_errors=True)
os.makedirs(SCRATCH)
os.chdir(SCRATCH)

checks = []
def add(got, want, tol=1e-9):
    line = inspect.stack()[1].lineno
    if isinstance(want, float) or isinstance(got, float):
        try: ok = abs(float(got) - float(want)) <= tol
        except (TypeError, ValueError): ok = False
    else:
        ok = got == want
    checks.append((bool(ok), got, want, line))

def run(code, stdin=""):
    """Run code in a fresh namespace; return what it printed (an uncaught exception becomes 'Name: message')."""
    out, old_in = io.StringIO(), sys.stdin
    sys.stdin = io.StringIO(stdin)
    try:
        with contextlib.redirect_stdout(out):
            try: exec(textwrap.dedent(code), {"__name__": "__main__"})
            except Exception as e: print(f"{type(e).__name__}: {e}")
    finally:
        sys.stdin = old_in
    return out.getvalue()

def write(name, src):
    with open(name, "w", encoding="utf-8") as f: f.write(textwrap.dedent(src))

def script(name, *args):
    """Run python <name> <args> as its own process; return (exit code, stdout + stderr)."""
    r = subprocess.run([sys.executable, "-X", "utf8", name, *args], capture_output=True, text=True, encoding="utf-8",
                       env={**os.environ, "NO_COLOR": "1", "PYTHON_COLORS": "0"})
    return r.returncode, r.stdout + r.stderr

NUM, TEXT, CHOICE = {}, {}, {}   # "lesson/item" -> computed value / string / text of the right option
print("Python", sys.version.split()[0])

# ================= 脚本
# ---------------- ecosystem
r = subprocess.run([sys.executable, "-I", "-c", "import numpy"], capture_output=True, text=True,
                   env={"PYTHONPATH": "", "SYSTEMROOT": os.environ.get("SYSTEMROOT", "")}, cwd=SCRATCH)
add(r.returncode == 0, True)   # the .venv has numpy; the lesson's claim is about a bare python.org install (not checkable here)

# ---------------- ipython (IPython's own shell)
from IPython.core.interactiveshell import InteractiveShell
sh = InteractiveShell.instance()
write("my_file.py", "s = 'Hello world'\nprint(s)\n")
def ipy(cell):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        res = sh.run_cell(cell)
    return res.result, out.getvalue()
add(ipy("print('Hello world')")[1].strip(), "Hello world")
add(ipy("2 ** 10")[0], 1024)
ipy("a = 3"); ipy("b = 2 * a")
add(ipy("type(b)")[0], int)
add(ipy("type(b)")[1].strip().endswith(": int"), True)        # IPython shows Out[n]: int
ipy("b = 'hello'"); add(ipy("type(b)")[1].strip().endswith(": str"), True)
add(repr(ipy("2 * b")[0]), "'hellohello'"); TEXT["ipython/str-times"] = repr(ipy("2 * b")[0])
add("Return the number of items in a container." in ipy("len?")[1], True)
add("len(obj, /)" in ipy("len?")[1], True)
add("Return the number of items" in ipy("?len")[1], True)    # ? in front also works
add(ipy("%run my_file.py")[1].strip(), "Hello world")
add(ipy("s")[0], "Hello world")
whos = ipy("%whos")[1]
add("Variable   Type    Data/Info" in whos and "s          str     Hello world" in whos, True)
write("total.py", "total = 42\n"); ipy("%run total.py"); add(ipy("total")[0], 42)
import timeit
import numpy as np
L = range(1000); arr = np.arange(1000)
t_list = min(timeit.repeat(lambda: [i**2 for i in L], number=200, repeat=5)) / 200
t_arr = min(timeit.repeat(lambda: arr**2, number=2000, repeat=5)) / 2000
add(t_list / t_arr > 10, True)              # "差了五十多倍" on the machine the card was written on; at least 10× anywhere
ti = ipy("%timeit -n 100 -r 7 x = 10")[1]
add("per loop (mean +- std. dev. of 7 runs, 100 loops each)" in ti.replace("±", "+-"), True)   # ± on a UTF-8 terminal, +- here
NUM["ipython/timeit-ratio"] = 40 / 0.8
add(ipy(">>> 1 + 1")[0], 2); add(ipy("In [3]: 2 * 3")[0], 6)    # IPython strips pasted prompts
r = subprocess.run([sys.executable, "-I", "-c", "from IPython.terminal.interactiveshell import TerminalInteractiveShell as T; s = T.instance(); print('cpaste' in s.magics_manager.magics['line'], all(m in s.magics_manager.magics['line'] for m in ['run','whos','timeit','debug','quickref','magic']))"],
                   capture_output=True, text=True)
add(r.stdout.split(), ["True", "True"])
r = subprocess.run([sys.executable, "-I", "-c", ">>> print(1)"], capture_output=True, text=True)
add("SyntaxError" in r.stderr, True)          # plain python chokes on a pasted prompt

# ---------------- run-scripts
write("test.py", '''\
    message = "Hello how are you?"
    for word in message.split():
        print(word)
    ''')
add(script("test.py")[1].split("\n")[:4], ["Hello", "how", "are", "you?"])
NUM["run-scripts/split-lines"] = len("one two three four five".split())
write("file.py", "import sys\nprint(sys.argv)\n")
add(script("file.py", "test", "arguments")[1].strip(), "['file.py', 'test', 'arguments']")
write("add.py", "import sys\nprint(int(sys.argv[1]) + int(sys.argv[2]))\n")
NUM["run-scripts/argv-add"] = int(script("add.py", "3", "4")[1])
rc, out = script("add.py", "3"); add(rc != 0 and "IndexError" in out, True)
CHOICE["run-scripts/argv-missing"] = "报 IndexError：sys.argv 只有 2 个元素，没有下标 2"
write("add2.py", "import sys\nprint(sys.argv[1] + sys.argv[2])\n")
CHOICE["run-scripts/argv-str"] = script("add2.py", "3", "4")[1].strip()
add(sys.platform, "win32") if os.name == "nt" else None
CHOICE["run-scripts/platform"] = "win32"
add(sys.version.startswith("3.14"), True)
write("total2.py", "import sys\nargs = sys.argv[1:]\nnums = [float(x) for x in args]\nprint(sum(nums))\n")
add(script("total2.py", "1.5", "2", "3")[1].strip(), "6.5")
NUM["run-scripts/total-run"] = float(script("total2.py", "10", "0.5", "-2")[1])

# ---------------- argparse
write("square.py", '''\
    import argparse
    parser = argparse.ArgumentParser(description="求一个数的平方")
    parser.add_argument("x", type=float, help="要平方的数")
    args = parser.parse_args()
    print(args.x ** 2)
    ''')
add(script("square.py", "3")[1].strip(), "9.0")
NUM["argparse/square-25"] = float(script("square.py", "2.5")[1])
rc, out = script("square.py")
add((rc, out.strip().split("\n")), (2, ["usage: square.py [-h] x", "square.py: error: the following arguments are required: x"]))
rc, out = script("square.py", "abc")
add((rc, out.strip().split("\n")), (2, ["usage: square.py [-h] x", "square.py: error: argument x: invalid float value: 'abc'"]))
rc, out = script("square.py", "-h"); add(rc == 0 and "求一个数的平方" in out and "要平方的数" in out, True)
write("greet.py", '''\
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--times", type=int, default=1)
    parser.add_argument("--shout", action="store_true")
    args = parser.parse_args()
    text = (args.name + "!") * args.times
    print(text.upper() if args.shout else text)
    ''')
TEXT["argparse/greet-times"] = script("greet.py", "Ann", "--times", "3")[1].strip()
TEXT["argparse/greet-shout"] = script("greet.py", "bo", "--shout")[1].strip()
rc, out = script("greet.py", "Ann", "--times", "abc")
add((rc, out.strip().split("\n")[-1]), (2, "greet.py: error: argument --times: invalid int value: 'abc'"))
import argparse
pa = argparse.ArgumentParser(); pa.add_argument("--max-rows", type=int, default=10)
TEXT["argparse/dash-name"] = "args." + [k for k in vars(pa.parse_args([]))][0]
pa = argparse.ArgumentParser(); pa.add_argument("-n", "--times", type=int, default=1)
add(pa.parse_args(["-n", "3"]).times, pa.parse_args(["--times", "3"]).times)
write("backup.py", '''\
    import argparse
    parser = argparse.ArgumentParser(prog="backup")
    parser.add_argument("outfile")
    parser.add_argument("-u", "--user", required=True)
    args = parser.parse_args()
    print(args.user, args.outfile)
    ''')
rc, out = script("backup.py", "x.sql")
add((rc, out.strip().split("\n")), (2, ["usage: backup [-h] -u USER outfile", "backup: error: the following arguments are required: -u/--user"]))
add(script("backup.py", "-u", "root", "data.sql")[1].strip(), "root data.sql")

# ---------------- own-modules
write("demo2.py", '''\
    def print_a():
        print('a')

    def print_b():
        print('b')

    print_b()

    if __name__ == '__main__':
        print_a()
    ''')
write("imp2.py", "import demo2\nimport demo2\n")
NUM["own-modules/import-twice"] = len(script("imp2.py")[1].split())
add(script("demo2.py")[1].split(), ["b", "a"])
write("reload_demo.py", "x = 1\n")
write("reload_test.py", '''\
    import importlib
    import reload_demo
    open("reload_demo.py", "w").write("x = 20\\n")   # a different size: a same-size edit in the same second can hit the stale .pyc
    import reload_demo
    print(reload_demo.x)
    importlib.reload(reload_demo)
    print(reload_demo.x)
    ''')
add(script("reload_test.py")[1].split(), ["1", "20"])
os.makedirs("A", exist_ok=True); os.makedirs("B", exist_ok=True)
write("A/greet.py", "def greet(name):\n    print(f'Hello, {name}!')\n")
r_a = subprocess.run([sys.executable, "-c", "from greet import greet; greet('World')"], capture_output=True, text=True, cwd="A")
r_b = subprocess.run([sys.executable, "-c", "from greet import greet; greet('World')"], capture_output=True, text=True, cwd="B")
add((r_a.stdout.strip(), "No module named 'greet'" in r_b.stderr), ("Hello, World!", True))
add(run("print(sum(range(5), -1))\nfrom numpy import *\nprint(sum(range(5), -1))").split(), ["9", "10"])
star = run("from numpy import *\nfrom math import *\nprint(sqrt([1, 4]))")
add(star.startswith("TypeError"), True)
add(run("import numpy as np\nprint(np.sqrt([1, 4]))").strip(), "[1. 2.]")

# ---------------- complex-numbers
add(repr((-1) ** 0.5), "(6.123233995736766e-17+1j)")
with warnings.catch_warnings(record=True):
    warnings.simplefilter("always"); add(math.isnan(np.sqrt(-1.0)), True)
z = 1.5 + 0.5j; add((z.real, z.imag, type(z).__name__, repr(1j * 1j)), (1.5, 0.5, "complex", "(-1+0j)"))
NUM["complex-numbers/imag"] = (3 + 4j).imag
add(run("print(j)").startswith("NameError"), True)
add(repr((1 + 2j) * (3 - 1j)), "(5+5j)"); add(abs(3 + 4j), 5.0)
NUM["complex-numbers/abs-5-12"] = abs(5 + 12j)
add(repr((1 + 1j) ** 2), "2j"); NUM["complex-numbers/square-1j"] = ((1 + 1j) ** 2).imag
zs, z = [], 1 + 1j
while abs(z) < 100:
    z = z**2 + 1; zs.append(z)
add([repr(v) for v in zs], ["(1+2j)", "(-2+4j)", "(-11-16j)", "(-134+352j)"])
add((round(abs(zs[0]), 2), round(abs(zs[1]), 2), round(abs(zs[3]))), (2.24, 4.47, 377))
NUM["complex-numbers/loop-count"] = len(zs)
add(str(np.array([1 + 2j, 3j]).dtype), "complex128")
CHOICE["complex-numbers/complex-type"] = type(2 + 0j).__name__; add(2 + 0j == 2, True)

# ---------------- in-place
add(run("a = [1, 2, 3]\nb = a\na = [4, 5, 6]\nprint(b)").strip(), "[1, 2, 3]")
CHOICE["in-place/guess"] = "[1, 2, 3]"
add(run("a = [1, 2, 3]\nb = a\na[:] = [4, 5, 6]\nprint(b)").strip(), "[4, 5, 6]")
add(run("a = [1, 2, 3]\nb = a\na[:] = [7, 8]\nprint(b)\na = [0]\nprint(b)").split("\n")[:2], ["[7, 8]", "[7, 8]"])
add(run("a = [1, 2, 3]\nbefore = id(a)\na[:] = [4, 5]\nprint(id(a) == before)\na = [4, 5]\nprint(id(a) == before)").split(), ["True", "False"])
CHOICE["in-place/append-id"] = run("x = [1]\nn = id(x)\nx.append(2)\nprint(id(x) == n)").strip()
CHOICE["in-place/sort-none"] = run("xs = [3, 1, 2]\nys = xs.sort()\nprint(xs, ys)").strip()
add(run("s = 'cat'\ns[0] = 'b'").strip(), "TypeError: 'str' object does not support item assignment")
add(("b" + "cat"[1:], "cat".replace("c", "b")), ("bat", "bat"))
add(run("xs = [1, 2, 2, 3]\nfor x in xs:\n    if x == 2:\n        xs.remove(x)\nprint(xs)").strip(), "[1, 2, 3]")
CHOICE["in-place/remove-loop"] = run("xs = [5, 5, 5, 1]\nfor x in xs:\n    if x == 5:\n        xs.remove(x)\nprint(xs)").strip()
tel = {'emmanuelle': 5752, 'sebastian': 5578}; tel['francis'] = 5915
add(('francis' in tel, 5915 in tel), (True, False))
CHOICE["in-place/in-dict"] = str(2 in {"a": 1, "b": 2}); add(2 in {"a": 1, "b": 2}.values(), True)
d = {"b": 2, "c": 3, "a": 1}; TEXT["in-place/sorted-items"] = str([k for k, v in sorted(d.items())])

# ---------------- functions-as-values
f = len; NUM["functions-as-values/guess"] = f("hello")
add(run("def double(x):\n    return 2 * x\ng = double\nprint(g(4))\nfor f in [min, max, sum]:\n    print(f([3, 1, 2]))").split(), ["8", "1", "3", "6"])
NUM["functions-as-values/func-list"] = [abs, len, round][1]("abc")
apply_twice = lambda f, x: f(f(x))
add(apply_twice(lambda x: 2 * x, 5), 20)
NUM["functions-as-values/apply-add3"] = int(run("def apply_twice(f, x):\n    return f(f(x))\n\ndef add3(x):\n    return x + 3\n\nprint(apply_twice(add3, 1))"))
add(run("def double(x):\n    return 2 * x\ndef apply_twice(f, x):\n    return f(f(x))\napply_twice(double(5), 5)").strip(), "TypeError: 'int' object is not callable")
add(run(inspect.cleandoc('''
    def try_to_modify(x, y, z):
        x = 23
        y.append(42)
        z = [99]

    a = 77
    b = [99]
    c = [28]
    try_to_modify(a, b, c)
    print(a, b, c)''')).strip(), "77 [99, 42] [28]")
add(run("def grow(xs, k):\n    xs.append(k)\n    k = k + 1\n    xs = []\n\nnums = [1]\nn = 5\ngrow(nums, n)\nprint(nums, n)").strip(), "[1, 5] 5")
add(run("bigx = 10\ndef double_it(x=bigx):\n    return x * 2\n\nbigx = 1e9\nprint(double_it())").strip(), "20")
n_ = 3
def f_(x=n_): return x + 1
n_ = 100; NUM["functions-as-values/default-time"] = f_()
add_to_dict = run(inspect.cleandoc('''
    def add_to_dict(args={'a': 1, 'b': 2}):
        for i in args.keys():
            args[i] += 1
        print(args)
    add_to_dict(); add_to_dict(); add_to_dict()''')).strip().split("\n")
add(add_to_dict, ["{'a': 2, 'b': 3}", "{'a': 3, 'b': 4}", "{'a': 4, 'b': 5}"])
CHOICE["functions-as-values/default-dict"] = add_to_dict[1]

# ---------------- file-lines
with open("workfile", "w") as fh: fh.write("This is a test\nand another test")
add(run("for line in open('workfile'):\n    print(line)"), "This is a test\n\nand another test\n")
add(run("with open('workfile', encoding='utf-8') as f:\n    for line in f:\n        print(line.rstrip('\\n'))"), "This is a test\nand another test\n")
with open("abc.txt", "w") as fh: fh.write("abc\ndef\n")
with open("abc.txt") as fh: TEXT["file-lines/line-repr"] = repr(next(iter(fh)))
NUM["file-lines/count-nonblank"] = int(run('lines = ["x\\n", "\\n", "y\\n", "  \\n", "z"]\nn = 0\nfor line in lines:\n    if line.strip():\n        n = n + 1\nprint(n)'))
add(run("f = open('w.txt', 'w')\nf.write(3)").startswith("TypeError"), True)
with open("log.txt", "w") as fh: fh.write("x\n")
with open("log.txt", "a") as fh: fh.write("y\n")
add(open("log.txt").read(), "x\ny\n")
NUM["file-lines/utf8-bytes"] = len("中文".encode("utf-8")); add(len("中文"), 2)
import pickle
with open("test.pkl", "wb") as fh: pickle.dump([1, None, "Stan"], fh)
with open("test.pkl", "rb") as fh: add(pickle.load(fh), [1, None, "Stan"])
add(run("import pickle\nwith open('t2.pkl', 'w') as f:\n    pickle.dump([1], f)").startswith("TypeError"), True)

# ---------------- eafp
ps = "def print_sorted(collection):\n    try:\n        collection.sort()\n    except AttributeError:\n        pass\n    print(collection)\n"
add(run(ps + "print_sorted([1, 3, 2])\nprint_sorted('132')\nprint_sorted({3, 1, 2})").split("\n")[:3], ["[1, 2, 3]", "132", "{1, 2, 3}"])
retry = 'while True:\n    try:\n        x = int(input())\n        break\n    except ValueError:\n        print("不是整数，再来")\nprint(x * 2)\n'
add(run(retry, "abc\n12\n"), "不是整数，再来\n24\n")
add(run(retry, "2.5\n七\n7\n"), "不是整数，再来\n不是整数，再来\n14\n")
add(run("try:\n    x = int('a')\nfinally:\n    print('Thank you for your input')").split("\n")[:2],
    ["Thank you for your input", "ValueError: invalid literal for int() with base 10: 'a'"])
x, k = 0, 0
while abs(x - 1) >= 1e-3:
    x = 1 - (1 - x) / 2.; k += 1
add(x, 0.9990234375); NUM["eafp/arrow-steps"] = k
add((round(0.5**9, 5), round(0.5**10, 5)), (0.00195, 0.00098))

# ---------------- os-paths
import os.path as op, ntpath, posixpath
from pathlib import Path, PurePosixPath
add(ntpath.join("data", "2026", "a.txt"), "data\\2026\\a.txt")
add((op.split("/home/ann/junk.txt"), op.basename("/home/ann/junk.txt"), op.splitext("junk.txt")), (("/home/ann", "junk.txt"), "junk.txt", ("junk", ".txt")))
CHOICE["os-paths/splitext-gz"] = str(op.splitext("archive.tar.gz"))
add(os.name in ("nt", "posix"), True)
os.makedirs("sub1", exist_ok=True); write("f1.txt", "x")
add([x for x in os.listdir('.') if op.isdir(x)].count("sub1") == 1 and "f1.txt" not in [x for x in os.listdir('.') if op.isdir(x)], True)
p = PurePosixPath("notes") / "2026" / "todo.txt"; add((p.name, p.stem, p.suffix, str(p.parent)), ("todo.txt", "todo", ".txt", "notes/2026"))
TEXT["os-paths/path-stem"] = Path("data/raw/sensor_07.csv").stem
p = Path("img/cat.png"); add((p.name, p.stem, p.suffix, p.with_suffix(".jpg").name), ("cat.png", "cat", ".png", "cat.jpg"))
os.environ.pop("DATA_DIR", None); CHOICE["os-paths/getenv-default"] = repr(os.getenv("DATA_DIR", "data"))
add((os.getenv("MY_DEBUG_NOT_SET"), os.getenv("MY_DEBUG_NOT_SET", "0")), (None, "0"))
os.environ["N_JOBS"] = "4"; CHOICE["os-paths/env-strings"] = repr(os.getenv("N_JOBS") * 2)

# ---------------- batch-files
import glob
for name in ["data_1.csv", "data_10.csv", "data_a.csv", "data.csv"]: write(name, "")
CHOICE["batch-files/glob-question"] = sorted(glob.glob("data_?.csv"))
add(glob.glob("*.nothing"), [])
for d in ["proj/sub/deep"]: os.makedirs(d, exist_ok=True)
write("proj/a.py", ""); write("proj/sub/b.py", ""); write("proj/sub/deep/c.txt", "")
NUM["batch-files/walk-count"] = sum(1 for _ in os.walk("proj"))
from datetime import date, timedelta
add(date(2026, 3, 5).strftime('%Y%m%d'), "20260305"); add(date(2026, 10, 31) + timedelta(days=1), date(2026, 11, 1))
TEXT["batch-files/timedelta"] = (date(2026, 2, 27) + timedelta(days=2)).isoformat()
add(len(date.today().isoformat()), 10)
os.makedirs("notes", exist_ok=True); write("notes/todo.txt", ""); write("notes/a.csv", "")
def add_prefix(prefix):
    folder = Path("notes")
    for f in folder.glob("*.txt"):
        if not f.name.startswith(prefix):
            f.rename(f.with_name(f"{prefix}_{f.name}"))
add_prefix("2026-10-31"); add_prefix("2026-10-31")
add(sorted(os.listdir("notes")), ["2026-10-31_todo.txt", "a.csv"])
TEXT["batch-files/new-name"] = "2026-10-31_todo.txt"

# ---------------- classes / inheritance
cls = '''
class Student:
    def __init__(self, name):
        self.name = name
    def set_age(self, age):
        self.age = age
'''
add(run(cls + "anna = Student('anna')\nanna.set_age(21)\nprint(anna.name, anna.age)").strip(), "anna 21")
NUM["classes/two-instances"] = int(run(cls + "a = Student('a')\nb = Student('b')\na.set_age(20)\nb.set_age(30)\na.set_age(a.age + 1)\nprint(a.age + b.age)"))
add(run(cls + "c = Student('c')\nprint(c.age)").strip(), "AttributeError: 'Student' object has no attribute 'age'")
counter = "class Counter:\n    def __init__(self):\n        self.n = 0\n    def add(self, k=1):\n        self.n = self.n + k\n        return self.n\n"
add(run(counter + "c = Counter()\nc.add()\nc.add(5)\nprint(c.n)").strip(), "6")
NUM["classes/counter"] = int(run(counter + "c1 = Counter()\nc2 = Counter()\nc1.add(3)\nc2.add()\nc1.add()\nprint(c1.n * 10 + c2.n)"))
add(run("class Student:\n    def set_age(age):\n        self.age = age\nanna = Student()\nanna.set_age(21)").strip(),
    "TypeError: Student.set_age() takes 1 positional argument but 2 were given")
ms = cls + "class MasterStudent(Student):\n    internship = 'mandatory, from March to June'\n"
add(run(ms + "james = MasterStudent('james')\nprint(james.internship)\njames.set_age(23)\nprint(james.age)\nprint(james.name)").split("\n")[:3],
    ["mandatory, from March to June", "23", "james"])
add(run(ms + "print(Student('anna').internship)").strip(), "AttributeError: 'Student' object has no attribute 'internship'")
add(run(ms + "a = MasterStudent('a')\nb = MasterStudent('b')\nprint(a.internship == b.internship)").strip(), "True")
add(run("class Animal:\n    def speak(self):\n        return '...'\nclass Dog(Animal):\n    def speak(self):\n        return 'Woof'\nprint(Animal().speak(), Dog().speak())\nprint(isinstance(Dog(), Animal))").split("\n")[:2], ["... Woof", "True"])
TEXT["inheritance/override"] = run(inspect.cleandoc('''
    class Shape:
        def area(self):
            return 0
        def describe(self):
            return 'area=' + str(self.area())

    class Square(Shape):
        def __init__(self, side):
            self.side = side
        def area(self):
            return self.side * self.side

    print(Square(3).describe())''')).strip()
add(run("class BadData(ValueError):\n    pass\ntry:\n    raise BadData('x')\nexcept ValueError:\n    print('caught')").strip(), "caught")
add(run(ms + "print(isinstance(MasterStudent('j'), Student), isinstance(Student('a'), MasterStudent))").strip(), "True False")

# ================= 数组与数据框
P = lambda v: str(v)    # what print() shows for an array
# ---------------- ndarray
a = np.array([0, 1, 2, 3]); add((repr(a), a.ndim, a.shape, len(a)), ("array([0, 1, 2, 3])", 1, (4,), 4))
b = np.array([[0, 1, 2], [3, 4, 5]]); add((b.ndim, b.shape, len(b), b.size), (2, (2, 3), 2, 6))
TEXT["ndarray/shape-32"] = str(np.array([[1, 2], [3, 4], [5, 6]]).shape)
NUM["ndarray/len-vs-size"] = len(np.array([[1, 2, 3, 4], [5, 6, 7, 8]])); add(np.array([[1, 2, 3, 4], [5, 6, 7, 8]]).size, 8)
add((np.zeros((2, 3, 4)).shape, np.zeros((2, 3, 4)).ndim), ((2, 3, 4), 3))
add((str(np.array([1, 2, 3]).dtype), str(np.array([1., 2., 3.]).dtype), str(np.array([True, False]).dtype), repr(np.array([1, 2, 3], dtype=float))),
    ("int64", "float64", "bool", "array([1., 2., 3.])"))
CHOICE["ndarray/mixed-dtype"] = str(np.array([1, 2, 3.5]).dtype); add(repr(np.array([1, 2, 3.5])), "array([1. , 2. , 3.5])")
NUM["ndarray/ndim3"] = np.zeros((4, 5, 6)).ndim; add(np.zeros((4, 5, 6)).size, 120)

# ---------------- make-arrays
add((P(np.arange(10)), P(np.arange(1, 9, 2)), P(np.arange(0, 1, 0.25)), P(np.linspace(0, 1, 6)), P(np.linspace(0, 1, 5, endpoint=False))),
    ("[0 1 2 3 4 5 6 7 8 9]", "[1 3 5 7]", "[0.   0.25 0.5  0.75]", "[0.  0.2 0.4 0.6 0.8 1. ]", "[0.  0.2 0.4 0.6 0.8]"))
CHOICE["make-arrays/guess"] = P(np.arange(1, 9, 2))
NUM["make-arrays/arange-len"] = len(np.arange(0, 2, 0.5)); NUM["make-arrays/linspace-second"] = np.linspace(0, 10, 5)[1]
add((np.zeros((2, 3)).shape, np.ones(4).shape, np.eye(2).tolist(), np.diag([5, 6]).tolist()), ((2, 3), (4,), [[1.0, 0.0], [0.0, 1.0]], [[5, 0], [0, 6]]))
add(str(np.ones((3, 3)).dtype), "float64")
rng = np.random.default_rng(0); add((rng.random(3).shape, rng.normal(size=(1000, 3)).shape), ((3,), (1000, 3)))
dice = np.random.default_rng(1).integers(1, 7, size=100000); add((dice.min(), dice.max()), (1, 6))
add((np.random.default_rng(5).random(3) == np.random.default_rng(5).random(3)).all(), True)

# ---------------- index-slice
a = np.arange(10); TEXT["index-slice/guess"] = P(a[2:5])
add((a[0], a[-1], P(a[2:9:3]), P(a[::-1])), (0, 9, "[2 5 8]", "[9 8 7 6 5 4 3 2 1 0]")); TEXT["index-slice/step3"] = P(a[::3])
t = np.arange(6) + np.arange(0, 51, 10)[:, np.newaxis]
add((t[2, 3], P(t[1]), P(t[:, 2]), t[4:, 4:].tolist()), (23, "[10 11 12 13 14 15]", "[ 2 12 22 32 42 52]", [[44, 45], [54, 55]]))
NUM["index-slice/t-pick"] = t[5, 1]
add((P(t[0, 3:5]), " ".join(P(t[2::2, ::2]).split()), P(t[:, 0])), ("[3 4]", "[[20 22 24] [40 42 44]]", "[ 0 10 20 30 40 50]"))
a = np.arange(10); a[5:] = 10; add(repr(a), "array([ 0,  1,  2,  3,  4, 10, 10, 10, 10, 10])")
a = np.zeros(6); a[::2] = 5; NUM["index-slice/slice-assign"] = a.sum()
a = np.arange(10); b = a[::2]; b[0] = 12; add((np.may_share_memory(a, np.arange(10)[::2]), a[0]), (False, 12))
a = np.arange(5); b = a[1:3]; b[0] = 100; NUM["index-slice/view-change"] = a[1]
a = np.arange(5); c = a[1:3].copy(); c[0] = 100; NUM["index-slice/copy-indep"] = a[1]
xs = [0, 1, 2, 3]; ys = xs[1:3]; ys[0] = 100; add(xs, [0, 1, 2, 3])

# ---------------- masks
a = np.array([3, 8, 1, 9]); TEXT["masks/guess"] = P(a[a > 5]); add((P(a > 5), int((a > 5).sum())), ("[False  True False  True]", 2))
NUM["masks/count-true"] = int((np.array([5, 12, 7, 20, 3]) >= 7).sum())
np.random.seed(3); a = np.random.randint(0, 21, 15)
add((P(a), P(a[a % 3 == 0])), ("[10  3  8  0 19 10 11  9 10  6  0 20 12  7 14]", "[ 3  0  9  6  0 12]"))
a[a % 3 == 0] = -1; add(P(a), "[10 -1  8 -1 19 10 11 -1 10 -1 -1 20 -1  7 14]")
a = np.array([4, -2, 7, -5, 1]); a[a < 0] = 0; NUM["masks/clip-neg"] = a.sum()
a = np.arange(10); add(P(a[(a > 2) & (a < 8)]), "[3 4 5 6 7]")
add(run("import numpy as np\na = np.arange(10)\na[(a > 2) and (a < 8)]").strip(), "ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()")
add(run("import numpy as np\na = np.arange(10)\na[a > 2 & a < 8]").startswith("ValueError: The truth value"), True)
a = np.array([1, 5, 9]); add(P(a[(a > 2) & (a < 8)]), "[5]")
a = np.arange(10); NUM["masks/or-mask"] = a[(a < 2) | (a > 7)].sum()
a = np.arange(0, 100, 10); add(P(a[[2, 3, 2, 4, 2]]), "[20 30 20 40 20]"); a[[9, 7]] = -100; add((a[9], a[7], a[8]), (-100, -100, 80))
add(np.arange(10)[np.array([[3, 4], [9, 7]])].shape, (2, 2))
NUM["masks/fancy-pick"] = np.array([5, 6, 7, 8])[[3, 0, 3]].sum()
a = np.arange(5); b = a[a > 2]; b[0] = 100; add(P(a), "[0 1 2 3 4]")

# ---------------- elementwise
TEXT["elementwise/guess"] = P(np.array([1, 2, 3]) * np.array([4, 5, 6]))
a = np.array([1, 2, 3, 4]); add((P(a + 1), P(2 ** a), P(a * a)), ("[2 3 4 5]", "[ 2  4  8 16]", "[ 1  4  9 16]"))
add(([1, 2] * 2, P(np.array([1, 2]) * 2)), ([1, 2, 1, 2], "[2 4]"))
x = np.array([0, 1, 2, 3]); NUM["elementwise/poly-eval"] = (x**2 - 2*x + 1).sum()
add(P(np.sin(np.arange(5))), "[ 0.          0.84147098  0.90929743  0.14112001 -0.7568025 ]")
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    add(P(np.log(np.arange(5))), "[      -inf 0.         0.69314718 1.09861229 1.38629436]")
    add(str(w[-1].message), "divide by zero encountered in log")
    add(P(np.log(np.array([1.0, 0.0]))), "[  0. -inf]"); add(bool(np.isnan(np.sqrt(np.array([-1.0]))[0])), True)
A = np.array([[1, 2], [3, 4]]); B = np.array([[5, 6], [7, 8]])
add(((A * B).tolist(), (A @ B).tolist(), A.dot(B).tolist()), ([[5, 12], [21, 32]], [[19, 22], [43, 50]], [[19, 22], [43, 50]]))
NUM["elementwise/matmul-entry"] = (A @ B)[1, 0]; NUM["elementwise/star-entry"] = (A * B)[1, 0]
add((np.ones((3, 3)) @ np.ones((3, 3)))[0, 0], 3.0)
add(run("import numpy as np\nnp.arange(4) + np.array([1, 2])").strip(), "ValueError: operands could not be broadcast together with shapes (4,) (2,)")
CHOICE["elementwise/equal-arrays"] = str(np.array_equal(np.array([1, 2, 3]), np.array([1, 2, 4]))); add(P(np.array([1, 2, 3]) == np.array([1, 2, 4])), "[ True  True False]")
add(run("import numpy as np\nnp.array([1, 2, 3]) + np.array([10, 20])").strip(), "ValueError: operands could not be broadcast together with shapes (3,) (2,)")

# ---------------- reductions
x = np.array([[1, 1], [2, 2]]); add((x.sum(), P(x.sum(axis=0)), P(x.sum(axis=1))), (6, "[3 3]", "[2 4]")); CHOICE["reductions/guess"] = P(x.sum(axis=0))
y = np.array([1, 3, 2]); add((y.sum(), y.mean(), y.min(), y.max(), y.argmin(), y.argmax(), np.median(y), round(y.std(), 3)), (6, 2.0, 1, 3, 0, 1, 2.0, 0.816))
NUM["reductions/argmax"] = np.array([4, 9, 2, 9]).argmax()
add((np.ones((2, 3)).sum(axis=0).shape, np.ones((2, 3)).sum(axis=1).shape), ((3,), (2,)))
TEXT["reductions/axis-shape"] = str(np.ones((1000, 3)).mean(axis=0).shape)
TEXT["reductions/row-max"] = P(np.array([[1, 7, 3], [8, 2, 4]]).max(axis=1))
add((P(np.cumsum([1, 2, 3, 4])), np.all([True, True, False]), np.any([True, True, False]), P(np.gradient(np.array([1., 4., 9., 16.])))), ("[ 1  3  6 10]", False, True, "[3. 4. 6. 7.]"))
TEXT["reductions/cumsum-last"] = P(np.cumsum([2, 0, 5, 1]))
n = np.arange(1, 10**6 + 1, dtype=np.int64); add(int((n * n).sum()), 333333833333500000); add(int((n * n).sum()), sum(i * i for i in range(1, 10**6 + 1)))
n32 = np.arange(1, 10**6 + 1, dtype=np.int32); add(int((n32 * n32).sum()), 16866193336416); add((np.iinfo(np.int32).max, 46341**2 > 2**31 - 1, 46340**2 <= 2**31 - 1), (2147483647, True, True))
n = np.arange(1, 101); NUM["reductions/squares-100"] = (n * n).sum(); add(100 * 101 * 201 // 6, 338350)

# ---------------- broadcasting
col = np.array([[0], [10], [20], [30]]); row = np.array([0, 1, 2]); add((col + row).tolist(), [[0, 1, 2], [10, 11, 12], [20, 21, 22], [30, 31, 32]])
CHOICE["broadcasting/guess"] = "得到一个 4 行 3 列的数组"; add((np.ones((4, 1)) + np.ones(3)).shape, (4, 3))
add([(np.ones(s1) + np.ones(s2)).shape for s1, s2 in [((4, 1), (3,)), ((2, 3), (3,)), ((3, 1), (1, 4))]], [(4, 3), (2, 3), (3, 4)])
add(run("import numpy as np\nnp.ones((2, 3)) + np.ones(2)").strip(), "ValueError: operands could not be broadcast together with shapes (2,3) (2,)")
TEXT["broadcasting/bc-shape"] = str((np.ones((5, 1)) + np.ones((1, 2))).shape)
CHOICE["broadcasting/bc-error"] = "np.ones((2, 3)) + np.ones(2)"; add((np.ones((2, 3)) + 5).shape, (2, 3))
add(np.arange(0, 40, 10)[:, np.newaxis].shape, (4, 1))
xg, yg = np.arange(5), np.arange(5)[:, np.newaxis]; dd = np.sqrt(xg**2 + yg**2); add((dd.shape, dd[3, 4]), ((5, 5), 5.0)); NUM["broadcasting/dist-entry"] = dd[0, 4]
X = np.random.default_rng(0).normal(size=(1000, 3)); mu, sd = X.mean(axis=0), X.std(axis=0); Z = (X - mu) / sd
add((mu.shape, sd.shape, np.allclose(Z.mean(axis=0), 0), np.allclose(Z.std(axis=0), 1)), ((3,), (3,), True, True))
add(run("import numpy as np\nX = np.ones((1000, 3))\nX - X.mean(axis=1)").startswith("ValueError: operands could not be broadcast"), True)
add((X - X.mean(axis=1)[:, np.newaxis]).shape, (1000, 3))
TEXT["broadcasting/row-scale"] = " ".join(P(np.array([[1, 2], [3, 4]]) * np.array([10, 100])).split())

# ---------------- reshape-sort
TEXT["reshape-sort/guess"] = str(np.arange(6).reshape(2, 3).shape)
a = np.array([[1, 2, 3], [4, 5, 6]]); add((P(a.ravel()), a.reshape(3, 2).tolist(), a.reshape(3, -1).tolist()), ("[1 2 3 4 5 6]", [[1, 2], [3, 4], [5, 6]], [[1, 2], [3, 4], [5, 6]]))
TEXT["reshape-sort/reshape-minus1"] = str(np.arange(12).reshape(-1, 4).shape)
add((a.T.tolist(), P(a.T.ravel()), a.T.shape), ([[1, 4], [2, 5], [3, 6]], "[1 4 2 5 3 6]", (3, 2)))
at = a.T; at[0, 1] = 999; add(a[1, 0], 999)
a = np.array([[1, 2, 3], [4, 5, 6]]); f = a.flatten(); f[0] = 100; add(a[0, 0], 1)
NUM["reshape-sort/transpose-entry"] = np.array([[1, 2, 3], [4, 5, 6]]).T[2, 1]
TEXT["reshape-sort/t-ravel"] = P(np.array([[1, 2], [3, 4]]).T.ravel())
a = np.array([[4, 3, 5], [1, 2, 1]]); add(np.sort(a, axis=1).tolist(), [[3, 4, 5], [1, 1, 2]]); r_ = a.sort(axis=1); add((r_, a.tolist()), (None, [[3, 4, 5], [1, 1, 2]]))
b = np.array([4, 3, 1, 2]); j = np.argsort(b); add((P(j), P(b[j])), ("[2 3 1 0]", "[1 2 3 4]"))
TEXT["reshape-sort/argsort"] = P(np.argsort(np.array([30, 10, 20])))
names = np.array(["甲", "乙", "丙"]); scores = np.array([82, 95, 70]); add(names[np.argsort(scores)].tolist(), ["丙", "甲", "乙"]); add(P(np.argsort(scores)), "[2 0 1]")

# ---------------- dtypes
a = np.array([1, 2, 3]); a[0] = 1.9; add((P(np.array([1, 2, 3]) + 1.5), P(a)), ("[2.5 3.5 4.5]", "[1 2 3]")); CHOICE["dtypes/guess"] = str(a[0])
a = np.zeros(3, dtype=int); a[1] = 7.99; NUM["dtypes/int-assign"] = a.sum()
bb = np.array([1.2, 1.5, 1.6, 2.5, 3.5, 4.5])
add((P(np.array([1.7, 1.2, 1.6]).astype(int)), P(np.around(bb)), P(np.around(bb).astype(int)), round(2.5)), ("[1 1 1]", "[1. 2. 2. 2. 4. 4.]", "[1 2 2 2 4 4]", 2))
TEXT["dtypes/around-half"] = P(np.around(np.array([0.5, 1.5, 2.5]))); NUM["dtypes/astype-neg"] = np.array([-1.7]).astype(int)[0]
add((np.iinfo(np.int8).min, np.iinfo(np.int8).max, np.iinfo(np.uint8).max, np.iinfo(np.int32).max, np.dtype(np.int32).itemsize, np.dtype(np.int64).itemsize), (-128, 127, 255, 2147483647, 4, 8))
add((P(np.array([127], dtype=np.int8) + 1), P(np.array([250], dtype=np.uint8) + 10)), ("[-128]", "[4]"))
NUM["dtypes/uint8-wrap"] = (np.array([200], dtype=np.uint8) + 100)[0]
add((repr(float(np.finfo(np.float64).eps)), str(np.finfo(np.float32).eps), bool(np.float32(1e-8) + np.float32(1) == 1), bool(np.float64(1e-8) + np.float64(1) == 1)),
    ("2.220446049250313e-16", "1.1920929e-07", True, False))
s32 = np.float32(1)
for _ in range(10000): s32 = s32 + np.float32(1e-8)
add(float(s32), 1.0); CHOICE["dtypes/float32-lost"] = "1"
NUM["dtypes/bytes-size"] = np.zeros(1000, dtype=np.float32).nbytes; add(np.zeros(1000).nbytes, 8000)

# ---------------- structured-masked
samples = np.zeros((6,), dtype=[('sensor_code', 'U4'), ('position', float), ('value', float)])
samples[:] = [('ALFA', 1, 0.37), ('BETA', 1, 0.11), ('TAU', 1, 0.13), ('ALFA', 1.5, 0.37), ('ALFA', 3, 0.11), ('TAU', 1.2, 0.13)]
add((samples.dtype.names, P(samples['value']), P(samples[samples['sensor_code'] == 'ALFA']['position'])),
    (('sensor_code', 'position', 'value'), "[0.37 0.11 0.13 0.37 0.11 0.13]", "[1.  1.5 3. ]"))
NUM["structured-masked/alfa-sum"] = samples[samples['sensor_code'] == 'ALFA']['value'].sum()
v = np.array([1., np.nan, 3.]); add((bool(np.isnan(v.mean())), np.nanmean(v), P(np.isnan(v))), (True, 2.0, "[False  True False]"))
NUM["structured-masked/nanmean"] = np.nanmean(np.array([4., np.nan, 8., np.nan]))
xm = np.ma.array([1, 2, 3, 4], mask=[0, 1, 0, 1]); ym = np.ma.array([1, 2, 3, 4], mask=[0, 1, 1, 1])
add((P(xm), xm.mean(), P(xm + ym), P(np.ma.sqrt([1, -1, 2, -2]))), ("[1 -- 3 --]", 2.0, "[2 -- -- --]", "[1.0 -- 1.4142135623730951 --]"))
NUM["structured-masked/masked-sum"] = np.ma.array([10, 20, 30, 40], mask=[1, 0, 0, 1]).sum()
NUM["structured-masked/masked-add"] = int((np.ma.array(np.zeros(4), mask=[0, 1, 0, 1]) + np.ma.array(np.zeros(4), mask=[0, 0, 1, 1])).mask.sum())

# ---------------- polynomials
p = np.poly1d([3, 2, -1]); add((p(0), p(2), p.order, np.allclose(sorted(p.roots), [-1, 1 / 3])), (-1, 15, 2, True))
NUM["polynomials/poly-eval"] = np.poly1d([1, 0, -4])(3); add(np.allclose(sorted(np.poly1d([1, 0, -4]).roots), [-2, 2]), True)
xx = np.array([0., 1, 2, 3]); add(np.allclose(np.polyfit(xx, 2 * xx + 1, 1), [2, 1]), True); add(round(np.poly1d(np.polyfit(xx, 2 * xx + 1, 1))(10), 9), 21.0)
NUM["polynomials/polyfit-coef"] = round(np.polyfit([0, 1, 2], [5, 2, -1], 1)[0], 9); add(np.allclose(np.polyfit([0, 1, 2], [5, 2, -1], 1), [-3, 5]), True)
Pn = np.polynomial.Polynomial([-1, 2, 3]); add((Pn(0), Pn.degree(), np.allclose(sorted(Pn.roots()), [-1, 1 / 3]), hasattr(Pn, "order")), (-1.0, 2, True, False))
add(np.allclose(np.polynomial.Polynomial([6, -5, 1]).coef[::-1], np.poly1d([1, -5, 6]).coeffs), True)
add((np.polynomial.Polynomial([6, -5, 1])(4), np.poly1d([1, -5, 6])(4)), (2.0, 2))
add(callable(Pn.roots), True)

# ---------------- save-load
with open("populations.txt", "w") as fh:
    fh.write("# year  hare    lynx    carrot\n1900    30e3    4e3     48300\n1901    47.2e3  6.1e3   48200\n1902    70.2e3  9.8e3   41500\n1903    77.4e3  35.2e3  38200\n")
data = np.loadtxt("populations.txt"); add((data.shape, str(data.dtype), P(data[0])), ((4, 4), "float64", "[ 1900. 30000.  4000. 48300.]"))
NUM["save-load/hare-mean"] = data[:, 1].mean()
np.savetxt("pop2.txt", data); add(np.allclose(np.loadtxt("pop2.txt"), data), True)
with open("gaps.csv", "w") as fh: fh.write("1,2,3\n4,,6\n")
add(run("import numpy as np\nnp.loadtxt('gaps.csv', delimiter=',')").startswith("ValueError"), True)
g = np.genfromtxt("gaps.csv", delimiter=","); add((g.shape, int(np.isnan(g).sum()), bool(np.isnan(g[1, 1]))), ((2, 3), 1, True))
np.save("pop.npy", data); add(np.array_equal(np.load("pop.npy"), data), True)
from scipy import io as spio
spio.savemat("file.mat", {"a": np.ones((3, 3))}); add(spio.loadmat("file.mat")["a"].shape, (3, 3))
spio.savemat("file1.mat", {"a": np.ones(3)}); add(spio.loadmat("file1.mat")["a"].shape, (1, 3))
spio.savemat("f.mat", {"v": np.arange(5)}); TEXT["save-load/mat-shape"] = str(spio.loadmat("f.mat")["v"].shape)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from PIL import Image
Image.fromarray(np.full((200, 300, 3), 128, dtype=np.uint8)).save("photo.png")
img = plt.imread("photo.png"); add((img.shape, str(img.dtype), 0 <= img.min() <= img.max() <= 1), ((200, 300, 3), "float32", True))
plt.imsave("rgba.png", np.random.default_rng(0).random((10, 12))); add(plt.imread("rgba.png").shape, (10, 12, 4))
Image.fromarray(np.full((4, 4, 3), 30, dtype=np.uint8)).save("dark.jpg"); jpg = plt.imread("dark.jpg"); add((str(jpg.dtype), jpg.ndim), ("uint8", 3))
NUM["save-load/invert-pixel"] = int(255 - np.uint8(30)); add(int((255 - jpg)[0, 0, 0]) in (224, 225, 226), True)   # JPEG may shift a value by one
CHOICE["save-load/channel-pick"] = str(img[:, :, 2].shape); add(img[:, :, 2:3].shape, (200, 300, 1))
plt.imsave("red.png", img[:, :, 0], cmap="gray"); add(os.path.exists("red.png"), True)

# ---------------- plotting
plt.close("all"); x = np.linspace(0, 2 * np.pi, 200)
plt.plot(x, np.sin(x), label="sin"); plt.plot(x, np.cos(x), label="cos"); plt.xlabel("x"); plt.ylabel("y"); plt.title("sin and cos"); plt.legend()
plt.savefig("trig.png", dpi=150)
add(([t_.get_text() for t_ in plt.gca().get_legend().get_texts()], plt.gca().get_title(), Image.open("trig.png").size), (["sin", "cos"], "sin and cos", (960, 720)))
add(list(plt.rcParams["figure.figsize"]), [6.4, 4.8])
plt.close("all"); plt.plot([1, 2, 3]); plt.savefig("d100.png", dpi=100); NUM["plotting/dpi-size"] = Image.open("d100.png").size[0]
plt.close("all"); ln = plt.plot([1, 2, 3], [4, 5, 6], "o")[0]; add((ln.get_marker(), ln.get_linestyle()), ("o", "None"))
ln2 = plt.plot([1, 2], [1, 2], "o-")[0]; add((ln2.get_marker(), ln2.get_linestyle()), ("o", "-"))
plt.close("all"); plt.plot(x, np.sin(x)); plt.close("all"); plt.savefig("after.png")   # what show() leaves behind: a new, empty figure
add(np.asarray(Image.open("after.png").convert("L")).min(), 255)

# ---------------- dataframe / pandas-ops / groupby
import pandas as pd
print("numpy", np.__version__, "pandas", pd.__version__, "matplotlib", matplotlib.__version__)
TEXT["dataframe/df-shape"] = str(pd.DataFrame({"a": [1, 2, 3, 4], "b": [5, 6, 7, 8], "c": list("wxyz")}).shape)
tt = np.linspace(-6, 6, 20); add(pd.DataFrame({'t': tt, 'sin': np.sin(tt), 'cos': np.cos(tt)}).shape, (20, 3))
brain = '''"";"Gender";"FSIQ";"VIQ";"PIQ";"Weight";"Height";"MRI_Count"
"1";"Female";133;132;124;"118";"64.5";816932
"2";"Male";140;150;124;".";"72.5";1001121
"3";"Male";139;123;150;"143";"73.3";1038437
"4";"Male";133;129;128;"172";"68.8";965353
"5";"Female";137;132;134;"147";"65.0";951545
'''
with open("brain_size.csv", "w") as fh: fh.write(brain)
data = pd.read_csv("brain_size.csv", sep=";", na_values=".")
add((data.shape, list(data.columns)[:3], bool(np.isnan(data.loc[1, "Weight"])), str(data["Weight"].dtype)), ((5, 8), ["Unnamed: 0", "Gender", "FSIQ"], True, "float64"))
add(pd.read_csv("brain_size.csv").shape, (5, 1))
nona = pd.read_csv("brain_size.csv", sep=";"); add((str(nona["Weight"].dtype) in ("str", "object"), nona.loc[1, "Weight"]), (True, "."))
add(run("import pandas as pd\npd.read_csv('brain_size.csv', sep=';')['Weight'].mean()").startswith("TypeError"), True)
add(list(pd.read_csv("brain_size.csv", sep=";", na_values=".", index_col=0).columns)[:2], ["Gender", "FSIQ"])
NUM["dataframe/weight-mean"] = data["Weight"].mean(); add(int(data["Weight"].count()), 4)
NUM["dataframe/female-viq"] = data[data["Gender"] == "Female"]["VIQ"].mean()
add(data[(data["Gender"] == "Male") & (data["VIQ"] > 125)]["VIQ"].tolist(), [150, 129])
add(run("import pandas as pd\nd = pd.read_csv('brain_size.csv', sep=';')\nd[d['Gender'] == 'Male' and d['VIQ'] > 125]").startswith("ValueError"), True)
s = pd.Series([9, 8, 7], index=["a", "b", "c"]); add(s["b"], 8)
s1 = pd.Series([1, 2, 3], index=["a", "b", "c"]); s2 = pd.Series([10, 20, 30], index=["b", "c", "d"]); r_ = s1 + s2
add((bool(np.isnan(r_["a"])), r_["b"], r_["c"], bool(np.isnan(r_["d"])), str(r_.dtype)), (True, 12.0, 23.0, True, "float64"))
NUM["pandas-ops/align-sum"] = (pd.Series([5, 6], index=["x", "y"]) + pd.Series([1, 1], index=["y", "z"])).sum()
add(data.sort_values("VIQ", ascending=False)["VIQ"].tolist(), [150, 132, 132, 129, 123]); add(data["VIQ"].tolist(), [132, 150, 123, 129, 132])
NUM["pandas-ops/cumsum-viq"] = data["VIQ"].cumsum().iloc[2]; add(data.drop(columns=["Unnamed: 0"]).shape, (5, 7))
add(round(data["FSIQ"].corr(data["PIQ"]), 2), 0.42); add(data[["VIQ", "PIQ"]].corr().shape, (2, 2))
NUM["pandas-ops/corr-self"] = data["VIQ"].corr(data["VIQ"])
gb = data.groupby("Gender")
add([f"{k} {v.mean()}" for k, v in gb["VIQ"]], ["Female 132.0", "Male 134.0"]); NUM["groupby/male-viq"] = gb["VIQ"].mean()["Male"]
add((int(gb["Weight"].count()["Male"]), int(gb.size()["Male"])), (2, 3))
temps = pd.DataFrame({"date": ["2026-01-03", "2026-01-20", "2026-02-05", "2026-02-18", "2026-01-10", "2026-02-11"],
                      "city": ["Oslo", "Oslo", "Oslo", "Oslo", "Rome", "Rome"], "temp": [-4.0, -8.0, -1.0, 3.0, 9.0, 14.0]})
temps.to_csv("temps.csv", index=False)
df = pd.read_csv("temps.csv", parse_dates=["date"])
monthly = df.groupby(["city", df["date"].dt.to_period("M")])["temp"].mean()
add([(c, str(m), v) for (c, m), v in monthly.items()], [("Oslo", "2026-01", -6.0), ("Oslo", "2026-02", 1.0), ("Rome", "2026-01", 9.0), ("Rome", "2026-02", 14.0)])
NUM["groupby/oslo-jan"] = monthly[("Oslo", pd.Period("2026-01"))]
hottest = df.loc[df.groupby("city")["temp"].idxmax(), ["city", "date", "temp"]]
add([(r.city, r.date.strftime("%Y-%m-%d"), r.temp) for r in hottest.itertuples()], [("Oslo", "2026-02-18", 3.0), ("Rome", "2026-02-11", 14.0)])
ag = df.groupby("city")["temp"].agg(["mean", "max", "count"])
add(ag.loc["Oslo"].tolist() + ag.loc["Rome"].tolist(), [-2.5, 3.0, 4, 11.5, 14.0, 2])

# ================= 科学计算
import scipy
from scipy import special, linalg, optimize, interpolate, integrate, stats, sparse, signal, ndimage, fft
print("scipy", scipy.__version__)
# ---------------- scipy-tour
add(hasattr(scipy, "cos"), False); add(run("import scipy\nscipy.cos(0)").startswith("AttributeError"), True)
add((special.gamma(5), special.gamma(0.5), math.sqrt(math.pi)), (24.0, 1.7724538509055159, 1.7724538509055159))
NUM["scipy-tour/gamma6"] = special.gamma(6)
add((math.isinf(special.gamma(172)), round(float(special.gammaln(172)), 11)), (True, 711.71472580229))
with warnings.catch_warnings():
    warnings.simplefilter("ignore"); add(bool(np.isnan(special.gamma(201) / special.gamma(199))), True)
add(round(float(np.exp(special.gammaln(201) - special.gammaln(199)))), 39800); add(200 * 199, 39800)
add((special.comb(5, 2), special.comb(5, 2, exact=True), round(float(special.erf(1 / np.sqrt(2))), 4)), (10.0, 10, 0.6827))
NUM["scipy-tour/comb62"] = special.comb(6, 2, exact=True)
add(math.factorial(170) < 1.79e308 < math.factorial(171), True)

# ---------------- linear-systems
A = np.array([[2, 1], [1, 3]]); b = np.array([5, 10]); xs_ = linalg.solve(A, b); add((P(xs_), bool(np.allclose(xs_, [1, 3])), bool(np.allclose(A @ xs_, b))), ("[1. 3.]", True, True))
CHOICE["linear-systems/guess"] = "x = 1，y = 3"
NUM["linear-systems/solve-x"] = linalg.solve(np.array([[1, 1], [1, -1]]), np.array([10, 2]))[0]
add(0.1 + 0.2 == 0.3, False)
add((np.dot([1, 2, 3], [4, 5, 6]), np.linalg.norm([3, 4])), (32, 5.0))
NUM["linear-systems/dot32"] = np.dot([2, 0, -1], [3, 5, 4]); NUM["linear-systems/norm68"] = np.linalg.norm([6, 8])
u_, v_ = np.array([5., 1.]), np.array([4., 1.]); NUM["linear-systems/cosine"] = u_ @ v_ / (np.linalg.norm(u_) * np.linalg.norm(v_))
add(round(21 / math.sqrt(26 * 17), 3), 0.999)

# ---------------- det-inv-svd
add((linalg.det(np.array([[1, 2], [3, 4]])), linalg.det(np.array([[3, 2], [6, 4]]))), (-2.0, 0.0))
add(run("import numpy as np\nfrom scipy import linalg\nlinalg.det(np.ones((3, 4)))").strip(), "ValueError: Last 2 dimensions of the array must be square but received shape (3, 4).")
NUM["det-inv-svd/det-21"] = linalg.det(np.array([[2, 1], [1, 3]]))
iarr = linalg.inv(np.array([[1, 2], [3, 4]])); add((" ".join(P(iarr).split()), bool(np.allclose(iarr, [[-2, 1], [1.5, -0.5]])), bool(np.allclose(np.array([[1, 2], [3, 4]]) @ iarr, np.eye(2)))), ("[[-2. 1. ] [ 1.5 -0.5]]", True, True))
NUM["det-inv-svd/inv-diag"] = linalg.inv(np.array([[2, 0], [0, 4]]))[0, 0]
add(run("import numpy as np\nfrom scipy import linalg\nlinalg.inv(np.array([[3, 2], [6, 4]]))").strip(), "LinAlgError: A singular matrix detected: slice(s) [0] are singular.")
arr = np.arange(9).reshape((3, 3)) + np.diag([1, 0, 1]); U_, s_, Vh_ = linalg.svd(arr)
add((P(s_), bool(np.allclose(U_ @ np.diag(s_) @ Vh_, arr)), round(linalg.det(arr), 6) != 0), ("[14.88982544  0.45294236  0.29654967]", True, True))
S_ = sparse.csr_matrix(np.array([[0, 0, 0, 0, 0, 1, 1, 0, 2]])); add((P(S_.data), S_.nnz), ("[1 1 2]", 3))
big = sparse.eye(10000, format="csr"); add((10000 * 10000 * 8, big.data.nbytes + big.indices.nbytes + big.indptr.nbytes), (800000000, 160004))
NUM["det-inv-svd/nnz"] = sparse.csr_matrix(np.array([[0, 0, 3], [4, 0, 0], [0, 0, 0]])).nnz
NUM["det-inv-svd/density"] = 5000 / (1000 * 1000) * 100

# ---------------- interpolate
NUM["interpolate/guess"] = float(interpolate.interp1d([2, 3], [4, 9])(2.2))
xi = np.array([0., 1, 2, 3]); yi = xi**2
add((float(interpolate.interp1d(xi, yi)(1.5)), float(interpolate.interp1d(xi, yi, kind="cubic")(1.5)), float(np.interp(1.5, xi, yi))), (2.5, 2.25, 2.5))
NUM["interpolate/interp-mid"] = float(interpolate.interp1d([0, 10], [100, 300])(2.5))
add(run("import numpy as np\nfrom scipy.interpolate import interp1d\nx = np.array([0., 1, 2, 3])\ninterp1d(x, x**2)(4)").strip(), "ValueError: A value (4.0) in x_new is above the interpolation range's maximum value (3.0).")
add(float(np.interp(4, xi, yi)), 9.0)
add("legacy" in interpolate.interp1d.__doc__.lower(), True)
NUM["interpolate/cubic-call"] = float(interpolate.CubicSpline(xi, xi**3)(2.5)); add(float(interpolate.interp1d(xi, xi**3)(2.5)), 17.5)

# ---------------- minimize / curve-fit (and the descent sim, checked by the build)
f_min = lambda x: x**2 + 10 * np.sin(x)
r0 = optimize.minimize(f_min, x0=0); add((round(float(r0.x[0]), 8), round(float(r0.fun), 15), bool(r0.success), int(r0.nfev)), (-1.30644012, -7.945823375615215, True, 12))
add(round(float(optimize.minimize(f_min, x0=3, method="L-BFGS-B").x[0]), 8), 3.83746709)
add(float(optimize.minimize(f_min, x0=1, bounds=((0, 10),)).x[0]), 0.0)
bh = optimize.basinhopping(f_min, 0, rng=np.random.default_rng(0)); add((round(float(bh.x[0]), 4), bh.nfev > 1000), (-1.3064, True))
cons = optimize.minimize(lambda p_: p_[0]**2 + p_[1]**2, x0=[1, 1], constraints={"type": "eq", "fun": lambda p_: p_[0] + p_[1] - 1})
add(np.allclose(cons.x, [0.5, 0.5]), True); NUM["minimize/constrained"] = round(float(cons.fun), 9)
add(round(float(optimize.minimize(f_min, x0=0, method="Nelder-Mead").x[0]), 3), -1.306)
add(optimize.minimize(f_min, x0=0).message.startswith("Optimization terminated successfully"), True)   # BFGS, the default without bounds
rng = np.random.default_rng(0); xd = np.linspace(-5, 5, num=50); yd = 2.9 * np.sin(1.5 * xd) + rng.normal(size=50)
tf = lambda x, a, b: a * np.sin(b * x)
add(P(optimize.curve_fit(tf, xd, yd, p0=[2, 2])[0]), "[2.64198155 1.51346571]")
add(P(optimize.curve_fit(tf, xd, yd, p0=[2, 5])[0]), "[-0.36480338  4.97498667]")
add(np.allclose(optimize.curve_fit(tf, xd, 2.9 * np.sin(1.5 * xd), p0=[2, 2])[0], [2.9, 1.5]), True)
NUM["curve-fit/fit-line"] = round(float(optimize.curve_fit(lambda x, m, c: m * x + c, [0, 1, 2, 3], [1, 3, 5, 7])[0][0]), 9)
add((float(optimize.root(f_min, x0=1).x[0]), P(optimize.root(f_min, x0=-2.5).x), P(optimize.fsolve(f_min, -2.5))), (0.0, "[-2.47948183]", "[-2.47948183]"))
NUM["curve-fit/root-sqrt2"] = float(optimize.root(lambda x: x**2 - 2, x0=1).x[0]); add(round(float(optimize.root(lambda x: x**2 - 2, x0=-1).x[0]), 4), -1.4142)

# ---------------- integrate / ode
res_, err_ = integrate.quad(np.sin, 0, np.pi / 2); add((res_, err_), (0.9999999999999999, 1.1102230246251564e-14))
add(round(sum((k / 50)**2 for k in range(50)) / 50, 4), 0.3234)        # the riemann sim at its solution n = 50
NUM["integrate/quad-3x2"] = integrate.quad(lambda x: 3 * x**2, 0, 2)[0]
add(integrate.quad(lambda x: np.exp(-x**2), -np.inf, np.inf)[0], math.sqrt(math.pi), 1e-12)
add((hasattr(integrate, "quadrature"), hasattr(integrate, "romberg"), hasattr(integrate, "fixed_quad")), (False, False, True))
add(len(integrate.quad(np.sin, 0, np.pi)), 2); add(round(integrate.quad(np.sin, 0, np.pi)[0], 12), 2.0)
tv = np.linspace(0, 4, 40); yo = integrate.odeint(lambda y, t: -2 * y, y0=1, t=tv); add((yo.shape, bool(np.allclose(yo[:, 0], np.exp(-2 * tv), atol=1e-6))), ((40, 1), True))
sv = integrate.solve_ivp(lambda t, y: -2 * y, (0, 4), [1], t_eval=[0, 1, 2]); add(P(sv.y), "[[1.         0.13549331 0.01834723]]")
NUM["ode/y-at-1"] = float(integrate.odeint(lambda y, t: -2 * y, y0=1, t=[0, 1])[1, 0]); add(round(math.exp(-2), 4), 0.1353)
add("solve_ivp" in integrate.odeint.__doc__, True)
mass, kspring, cviscous = 0.5, 4, 0.4; eps = cviscous / (2 * mass * np.sqrt(kspring / mass)); omega = np.sqrt(kspring / mass)
add((round(eps, 3), round(omega, 2), bool(eps < 1)), (0.141, 2.83, True)); NUM["ode/eps-value"] = eps
yarr = integrate.odeint(lambda yv, t, e, w: (yv[1], -2.0 * e * w * yv[1] - w**2 * yv[0]), (1, 0), np.linspace(0, 10, 100), args=(eps, omega))
add(yarr.shape, (100, 2)); add(bool((np.diff(np.sign(yarr[:, 0])) != 0).sum() >= 4 and abs(yarr[-1, 0]) < 0.5), True)   # it oscillates and dies down

# ---------------- distributions
add((round(stats.norm.pdf(0), 4), stats.norm.cdf(0), round(stats.norm.cdf(1.96), 3), round(stats.norm.ppf(0.975), 3)), (0.3989, 0.5, 0.975, 1.96))
NUM["distributions/cdf-1sd"] = stats.norm.cdf(1) - stats.norm.cdf(-1)
add((round(stats.norm.cdf(12, loc=10, scale=2), 4), round(stats.norm(loc=10, scale=2).cdf(12), 4)), (0.8413, 0.8413))
NUM["distributions/cdf-loc"] = stats.norm.cdf(90, loc=70, scale=10)
smp = np.random.default_rng(0).normal(size=1000); fl = stats.norm.fit(smp); add((round(float(fl[0]), 3), round(float(fl[1]), 3)), (-0.048, 0.977))
add(bool(np.isclose(np.histogram(smp, bins=np.arange(-4, 5), density=True)[0].sum(), 1.0)), True)
TEXT["distributions/hist-counts"] = P(np.histogram([1, 2, 2, 3, 3, 3], bins=[0.5, 1.5, 2.5, 3.5])[0])
add(stats.scoreatpercentile(smp, 50), float(np.median(smp)), 1e-12)
ds = stats.describe([1, 2, 3, 4, 10]); add((int(ds.nobs), tuple(int(v) for v in ds.minmax), float(ds.mean), float(ds.variance), round(float(ds.skewness), 3), round(float(ds.kurtosis), 3)), (5, (1, 10), 4.0, 12.5, 1.138, -0.212))
add(float(np.var([1, 2, 3, 4, 10])), 10.0)
CHOICE["distributions/robust-median"] = f"平均数 {np.mean([1, 2, 3, 4, 100]):g}，中位数 {np.median([1, 2, 3, 4, 100]):g}"
NUM["distributions/var-ddof"] = float(np.var([2, 4, 6], ddof=1)); add(round(float(np.var([2, 4, 6])), 2), 2.67)
inc = np.random.default_rng(0).lognormal(size=2000); add((bool(stats.skew(inc) > 0), bool(inc.mean() > np.median(inc))), (True, True))

# ---------------- t-tests / paired-tests
a_ = np.array([20.1, 22.3, 19.8, 21.5, 20.9, 22.0]); b_ = np.array([23.2, 24.1, 22.8, 25.0, 23.9, 24.4])
add((round(a_.mean(), 1), round(b_.mean(), 1)), (21.1, 23.9))
r_ = stats.ttest_ind(a_, b_); add((round(float(r_.statistic), 2), round(float(r_.pvalue), 5)), (-5.31, 0.00034))
add(round(float(stats.ttest_ind([1, 2, 3, 4, 5], [3, 4, 5, 6, 7]).pvalue), 4), 0.0805)
add(round(float(stats.ttest_ind([1, 2, 3, 4, 5], [3, 4, 5, 6, 7], alternative="less").pvalue), 4), 0.0403)
add(float(stats.ttest_ind([1, 2, 3, 4, 5], [3, 4, 5, 6, 7], alternative="less").pvalue) * 2, float(stats.ttest_ind([1, 2, 3, 4, 5], [3, 4, 5, 6, 7]).pvalue), 1e-12)
viq = np.array([132, 150, 123, 129, 132]); NUM["t-tests/one-sample"] = float(stats.ttest_1samp(viq, 130).pvalue); add(viq.mean(), 133.2)
NUM["t-tests/one-sided"] = 0.10 / 2
before = np.array([82, 75, 90, 68, 77, 85, 80, 72]); after = np.array([85, 79, 91, 74, 80, 86, 84, 75])
add((round(float(stats.ttest_ind(after, before).pvalue), 2), round(float(stats.ttest_rel(after, before).pvalue), 4)), (0.35, 0.001))
add(float(stats.ttest_rel(after, before).pvalue), float(stats.ttest_1samp(after - before, 0).pvalue), 1e-15)
NUM["paired-tests/mean-diff"] = float((after - before).mean()); add((after - before).tolist(), [3, 4, 1, 6, 3, 1, 4, 3])
add(float(stats.wilcoxon(after, before).pvalue), 0.0078125)
xn = np.random.default_rng(0).normal(size=200); un = np.random.default_rng(0).uniform(size=200)
add((round(float(stats.kstest(xn, "norm").pvalue), 2), float(stats.kstest(un, "norm").pvalue) < 1e-40, round(float(stats.normaltest(xn).pvalue), 2)), (0.95, True, 0.25))
add(f"{float(stats.kstest(un, 'norm').pvalue):.1e}", "5.6e-47")
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always"); add(bool(np.isnan(stats.normaltest([1, 2, 3, 4, 5, 6, 7]).pvalue)), True); add(any("too small" in str(x_.message) for x_ in w), True)

# ---------------- ols / seaborn
import statsmodels
from statsmodels.formula.api import ols
print("statsmodels", statsmodels.__version__)
xo_ = np.linspace(-5, 5, 20); np.random.seed(1); yo_ = -5 + 3 * xo_ + 4 * np.random.normal(size=xo_.shape)
mdl = ols("y ~ x", pd.DataFrame({"x": xo_, "y": yo_})).fit()
add((round(float(mdl.params["Intercept"]), 4), round(float(mdl.params["x"]), 4), round(float(mdl.rsquared), 3)), (-5.5335, 2.9369, 0.804))
add((round(float(mdl.bse["Intercept"]), 3), round(float(mdl.bse["x"]), 3), round(float(mdl.tvalues["Intercept"]), 3), round(float(mdl.tvalues["x"]), 3), round(float(mdl.pvalues["x"]), 3)), (1.036, 0.341, -5.342, 8.604, 0.0))
NUM["ols/predict"] = round(-5.5335 + 2.9369 * 2, 4)
mg = ols("VIQ ~ Gender", data).fit()
add((round(float(mg.params["Intercept"]), 6), round(float(mg.params["Gender[T.Male]"]), 6)), (132.0, 2.0))
add(float(mg.pvalues["Gender[T.Male]"]), float(stats.ttest_ind(data[data.Gender == "Male"]["VIQ"], data[data.Gender == "Female"]["VIQ"]).pvalue), 1e-12)
add(ols("VIQ ~ C(Gender)", data).fit().params.index.tolist(), ["Intercept", "C(Gender)[T.Male]"])
NUM["ols/dummy-mean"] = 109.45 + 5.80; add((109.45, 115.25), (109.45, 115.25))   # the 40-person table, from the source notes
add(len(ols("VIQ ~ FSIQ - 1", data).fit().params), 1)
import seaborn as sns
before_rc = dict(plt.rcParams)   # seaborn is imported above already in this run; check in a fresh process instead
r = subprocess.run([sys.executable, "-I", "-c", "import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; a = dict(plt.rcParams); import seaborn as sns; b = dict(plt.rcParams); sns.set_theme(); c = dict(plt.rcParams); print(sum(a[k] != b[k] for k in a), sum(a[k] != c[k] for k in a) > 0, sns.__version__)"], capture_output=True, text=True)
add(r.stdout.split()[:2], ["0", "True"]); print("seaborn", r.stdout.split()[2])
rng_ = np.random.default_rng(0); wdf = pd.DataFrame({"WAGE": rng_.normal(10, 2, 60), "AGE": rng_.integers(20, 60, 60), "EDUCATION": rng_.integers(8, 18, 60), "SEX": rng_.choice(["F", "M"], 60)})
add(sns.pairplot(wdf, vars=["WAGE", "AGE", "EDUCATION"], kind="reg", hue="SEX").axes.shape, (3, 3)); add(type(sns.lmplot(y="WAGE", x="EDUCATION", data=wdf, robust=True, n_boot=20)).__name__, "FacetGrid")
plt.close("all")

# ---------------- fft / signal / ndimage
fs = 100; t_ = np.arange(0, 1, 1 / fs); sig = np.sin(2 * np.pi * 5 * t_) + 0.5 * np.sin(2 * np.pi * 20 * t_)
F_ = fft.fft(sig); freqs = fft.fftfreq(sig.size, d=1 / fs); power = np.abs(F_); pos = freqs > 0
add((len(F_), str(F_.dtype), float(freqs[pos][power[pos].argmax()]), freqs[:3].tolist(), float(freqs[49]), float(freqs[50]), float(freqs[-1])), (100, "complex128", 5.0, [0.0, 1.0, 2.0], 49.0, -50.0, -1.0))
add(sorted(float(v) for v in freqs[pos][np.argsort(power[pos])[-2:]]), [5.0, 20.0]); CHOICE["fft/two-peaks"] = "20 Hz"
add(round(float(power[5] / power[20]), 6), 2.0)
add(bool(np.allclose(power[1:50], power[99:50:-1])), True)
s8 = np.sin(2 * np.pi * 8 * t_); p8 = np.abs(fft.fft(s8)); NUM["fft/main-freq"] = float(freqs[pos][p8[pos].argmax()])
fr1 = fft.fftfreq(100); add(round(float(fr1[fr1 > 0][p8[fr1 > 0].argmax()]), 6), 0.08)
F2 = F_.copy(); F2[np.abs(freqs) > 10] = 0; cl = fft.ifft(F2); add((bool(np.abs(cl.imag).max() < 1e-12), bool(np.allclose(cl.real, np.sin(2 * np.pi * 5 * t_)))), (True, True))
from scipy import fftpack
add((bool(np.allclose(fftpack.fft(sig), F_)), "legacy" in fftpack.__doc__.lower()), (True, True))
s3 = np.sin(2*np.pi*3*t_) + np.sin(2*np.pi*15*t_) + np.sin(2*np.pi*40*t_); G = fft.fft(s3); G[np.abs(freqs) > 20] = 0
add(bool(np.allclose(fft.ifft(G).real, np.sin(2*np.pi*3*t_) + np.sin(2*np.pi*15*t_))), True)
ts = np.linspace(0, 5, 100); add((signal.resample(np.sin(ts), 25).shape, ts[::4].shape), ((25,), (25,)))
xtr = ts + np.random.default_rng(0).normal(size=100); xdt = signal.detrend(xtr)
NUM["signal/detrend-slope"] = round(float(np.polyfit(ts, xdt, 1)[0]), 9); add(bool(abs(xdt.mean()) < 1e-10), True)
add(P(signal.medfilt(np.array([2., 80, 3, 4, 100, 5]), 3)), "[2. 3. 4. 4. 5. 5.]")
TEXT["signal/medfilt-out"] = P(signal.medfilt(np.array([1., 1, 9, 1, 1]), 3))
f_w, Pxx = signal.welch(sig, fs=fs, nperseg=100); add(float(f_w[Pxx.argmax()]), 5.0)
add(len(signal.spectrogram(np.sin(2 * np.pi * 5 * np.arange(0, 10, 0.01)), fs=100)), 3)   # frequencies, times, values
add((ndimage.zoom(np.ones((10, 20)), 2).shape, ndimage.rotate(np.ones((10, 20)), 90).shape, P(ndimage.shift(np.arange(5), 2))), ((20, 40), (20, 10), "[0 0 0 1 2]"))
TEXT["ndimage/zoom-shape"] = str(ndimage.zoom(np.ones((30, 40)), 0.5).shape)
gf = ndimage.gaussian_filter(np.array([0., 0, 10, 0, 0]), sigma=1); add((P(gf.round(3)), round(float(gf.sum()), 9)), ("[0.584 2.421 3.989 2.421 0.584]", 10.0))
dot = np.zeros((5, 5)); dot[2, 2] = 100; NUM["ndimage/median-dot"] = float(ndimage.median_filter(dot, size=3).max())
add(ndimage.generate_binary_structure(2, 1).astype(int).tolist(), [[0, 1, 0], [1, 1, 1], [0, 1, 0]])
sq7 = np.zeros((7, 7), dtype=bool); sq7[1:6, 1:6] = True; add(int(ndimage.binary_erosion(sq7).sum()), 9)
sq9 = np.zeros((9, 9), dtype=bool); sq9[1:8, 1:8] = True; NUM["ndimage/erode-area"] = int(ndimage.binary_erosion(sq9).sum())
d1 = np.zeros((5, 5), dtype=bool); d1[2, 2] = True; NUM["ndimage/dilate-dot"] = int(ndimage.binary_dilation(d1).sum())
mk = np.zeros((8, 8), dtype=bool); mk[1:4, 1:4] = True; mk[6, 6] = True; mk[0, 7] = True
lab_, nb_ = ndimage.label(mk); NUM["ndimage/label-count"] = nb_; add(ndimage.sum(mk, lab_, range(1, nb_ + 1)).tolist(), [1.0, 9.0, 1.0])   # labels go in reading order: the corner dot comes first
op_ = ndimage.binary_opening(mk); add((int(op_.sum()), ndimage.label(op_)[1]), (5, 1)); CHOICE["ndimage/opening-left"] = "1 块：两个单点被去掉，方块变成 5 个像素的十字"

# ================= 环境管理与自动化
# ---------------- install-pip
add(run("python3 --version").strip(), "NameError: name 'python3' is not defined")
add(run('print "hello"').startswith("SyntaxError"), True)
from pip._vendor.packaging.specifiers import SpecifierSet
from pip._vendor.packaging.version import Version
ok_ = lambda spec, vs: [v for v in vs if Version(v) in SpecifierSet(spec)]
CHOICE["install-pip/compatible"] = ok_("~=1.4.2", ["1.4.2", "1.4.9", "1.5.0", "1.4.1"])
add(ok_("~=2.1", ["2.0.9", "2.1", "2.5.3", "3.0"]), ["2.1", "2.5.3"]); add(ok_(">=1,<2", ["0.9", "1.0", "1.9.9", "2.0"]), ["1.0", "1.9.9"])
add(ok_("~=2.1.0", ["2.1.0", "2.1.7", "2.2.0"]), ["2.1.0", "2.1.7"])
import importlib.util
add([importlib.util.find_spec(m) is not None for m in ("sklearn", "PIL")], [importlib.util.find_spec("sklearn") is not None, True])   # pillow is imported as PIL
# ---------------- venv (a real one, without pip so it is quick)
r = subprocess.run([sys.executable, "-m", "venv", "--without-pip", "envdemo"], capture_output=True, text=True); add(r.returncode, 0)
lay = sorted(os.listdir("envdemo")); add("pyvenv.cfg" in lay and ("Scripts" in lay if os.name == "nt" else "bin" in lay), True)
env_py = os.path.join("envdemo", "Scripts" if os.name == "nt" else "bin", "python.exe" if os.name == "nt" else "python")
r = subprocess.run([env_py, "-c", "import sys; print(sys.prefix != sys.base_prefix, sys.prefix)"], capture_output=True, text=True)
add((r.stdout.split()[0], os.path.abspath("envdemo").lower() in r.stdout.lower()), ("True", True))
add(os.path.exists(os.path.join("envdemo", "Scripts" if os.name == "nt" else "bin", "activate")), True)
# ---------------- dependencies
CHOICE["dependencies/conflict-pick"] = ok_(">=1.16.0,<1.19.0,>=1.16.5", ["1.16.5", "1.18.5", "1.16.0", "1.19.0"])
add(ok_(">=1.16.0,<1.19.0,>=1.16.5,>=1.19", ["1.16.5", "1.18.5", "1.19.0", "1.20"]), [])
# ---------------- shell (Git Bash on this machine)
BASH = shutil.which("bash")
def sh_(cmd):
    r = subprocess.run([BASH, "-c", cmd], capture_output=True, text=True, cwd=SCRATCH)
    return r.returncode, r.stdout, r.stderr
if BASH:
    rc, out, err = sh_("foo = bar"); add((rc != 0, "foo" in err), (True, True))
    add(sh_("foo=bar; echo \"$foo\"; echo '$foo'")[1].split("\n")[:2], ["bar", "$foo"])
    add(sh_("name=Ann; echo 'Hello $name'")[1].strip(), "Hello $name")
    os.makedirs("folder", exist_ok=True); sh_("touch folder/{a,b,c}.py"); add(sorted(os.listdir("folder")), ["a.py", "b.py", "c.py"])
    sh_("touch report_{jan,feb,mar}.txt"); NUM["shell/brace"] = len(glob.glob("report_*.txt"))
    add(sh_("echo rm *.py")[1].strip().startswith("rm ") and "*.py" not in sh_("touch x.py; echo rm *.py")[1], True)
    add(sh_("export DEBUG=1; bash -c 'echo $DEBUG'")[1].strip(), "1")
    add(sh_("DEBUG=7 bash -c 'echo $DEBUG'; echo \"[$DEBUG]\"")[1].split("\n")[:2], ["7", "[]"])
    add(sh_("false; echo $?; true; echo $?")[1].split(), ["1", "0"])
    py_ = sys.executable.replace("\\", "/")
    write("boom.py", "print('a')\nprint('b')\n1 / 0\n")
    rc, out, err = sh_(f"'{py_}' boom.py; echo $?"); NUM["shell/exit-uncaught"] = int(out.split()[-1])
    add(sh_(f"'{py_}' -c 'raise SystemExit(0)' && echo next")[1].strip(), "next")
    add(sh_(f"'{py_}' boom.py > /dev/null && echo next")[1].strip(), "")
    add(sh_(f"'{py_}' boom.py || echo failed")[1].split()[-1], "failed")
    rc, out, err = sh_(f"'{py_}' boom.py > out.txt"); add((out, "ZeroDivisionError" in err, open("out.txt").read().split()), ("", True, ["a", "b"]))
    rc, out, err = sh_("ls /nonexistent 2>/dev/null"); add((out, err, rc != 0), ("", "", True))
    rc, out, err = sh_("ls /nonexistent | grep pattern"); add("nonexistent" in err, True)
    add(sh_(f"'{py_}' -c 'import sys; sys.exit(0)' && echo ran")[1].strip(), "ran")
    CHOICE["boss/b-exit"] = "会，退出状态 0 表示成功"
else:
    checks.append((False, "bash", "a bash to run the shell examples", inspect.stack()[0].lineno))
write("argfail.py", "import argparse\np = argparse.ArgumentParser()\np.add_argument('x', type=int)\np.parse_args()\n"); add(script("argfail.py", "abc")[0], 2)
# ---------------- subprocess
r = subprocess.run([sys.executable, '-c', 'print(1 + 1)'], capture_output=True, text=True); add((r.returncode, r.stdout.strip(), r.stderr), (0, "2", ""))
NUM["subprocess/returncode"] = subprocess.run([sys.executable, "-c", "import sys; sys.exit(3)"]).returncode
rb_ = subprocess.run([sys.executable, "-c", "print(42)"], capture_output=True); add((type(rb_.stdout).__name__, rb_.stdout.strip()), ("bytes", b"42"))
try:
    subprocess.run([sys.executable, "-c", "import sys; sys.exit(1)"], check=True); add("no error", "CalledProcessError")
except subprocess.CalledProcessError: add(True, True)
add(os.system("exit 5") if os.name == "nt" else 5, 5)
add((sys._is_gil_enabled(), sys.getswitchinterval()), (True, 0.005))
write("pool.py", "from multiprocessing import Pool\n\ndef square(x):\n    return x * x\n\nif __name__ == '__main__':\n    with Pool(4) as p:\n        print(p.map(square, range(10)))\n")
add(script("pool.py")[1].strip(), "[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]")
write("cube.py", "from multiprocessing import Pool\n\ndef cube(x):\n    return x ** 3\n\nif __name__ == '__main__':\n    with Pool(4) as p:\n        print(sum(p.map(cube, range(4))))\n")
NUM["subprocess/pool-sum"] = int(script("cube.py")[1])

# ---------------- boss
write("calc.py", "import sys\nprint(float(sys.argv[1]) * int(sys.argv[2]))\n"); NUM["boss/b-argv"] = float(script("calc.py", "2.5", "4")[1])
CHOICE["boss/b-default"] = run("def add(x, box=[]):\n    box.append(x)\n    return box\nadd(1)\nprint(add(2))").strip()
NUM["boss/b-class"] = int(run(inspect.cleandoc('''
    class Account:
        def __init__(self, balance):
            self.balance = balance
        def deposit(self, amount):
            self.balance = self.balance + amount

    a = Account(100)
    b = Account(50)
    a.deposit(30)
    b.deposit(a.balance)
    print(b.balance)''')))
a = np.arange(6); b = a[2:5]; b[1] = 99; NUM["boss/b-view"] = a.sum()
TEXT["boss/b-axis"] = P(np.array([[1, 2, 3], [4, 5, 6]]).mean(axis=0))
add(run("import numpy as np\nX = np.ones((100, 4))\nX - X.mean(axis=1)").startswith("ValueError"), True); CHOICE["boss/b-broadcast"] = "X - X.mean(axis=0)"
NUM["boss/b-groupby"] = pd.DataFrame({"city": list("AABBB"), "sales": [10, 20, 5, 5, 20]}).groupby("city")["sales"].mean()["B"]
NUM["boss/b-solve"] = linalg.solve(np.array([[3, 1], [1, 2]]), np.array([9, 8]))[0]
NUM["boss/b-quad"] = integrate.quad(lambda x: 2 * x, 0, 3)[0]
t200 = np.arange(0, 1, 1 / 200); p30 = np.abs(fft.fft(np.sin(2 * np.pi * 30 * t200))); fr200 = fft.fftfreq(200, d=1 / 200)
NUM["boss/b-fft"] = float(fr200[fr200 > 0][p30[fr200 > 0].argmax()])

# ================= compare with the pack
pack = yaml.safe_load(open(os.path.join(ROOT, "data", "content", "P.2.3.yaml"), encoding="utf8"))
items = {}
for les in pack["lessons"]:
    for step in les["flow"]:
        it = step.get("item") or step.get("guess")
        if it: items[f"{les['id']}/{it['id']}"] = it
for it in (pack.get("boss") or {}).get("items", []): items[f"boss/{it['id']}"] = it
here = inspect.stack()[0].lineno
for k, it in items.items():
    if it["type"] == "number":
        if k not in NUM: checks.append((False, k, "a computed value in NUM", here)); continue
        ans = float(it["answer"]); tol = float(it.get("tolerance", max(1e-9, abs(ans) * 1e-6)))
        checks.append((abs(ans - float(NUM[k])) <= tol, f"{k} = {it['answer']}", float(NUM[k]), here))
    elif it["type"] == "text":
        if k not in TEXT: checks.append((False, k, "a computed value in TEXT", here)); continue
        sp_ = lambda s: " ".join(str(s).split())      # the game collapses runs of spaces too
        checks.append((sp_(TEXT[k]) in [sp_(a) for a in it["answers"]], f"{k} answers {it['answers']}", TEXT[k], here))
    elif it["type"] == "choice" and k in CHOICE:
        right = [o["text"] for o in it["options"] if o.get("correct")]
        want = CHOICE[k] if isinstance(CHOICE[k], list) else [CHOICE[k]]
        norm = lambda s: str(s).strip("`'\"")
        checks.append(([norm(r) for r in right] == [norm(w) for w in want], f"{k} right option {right}", want, here))
for d, kind in [(NUM, "number"), (TEXT, "text"), (CHOICE, "choice")]:
    for k in d:
        if k not in items or items[k]["type"] != kind: checks.append((False, k, f"a {kind} item in the pack", here))

bad = [(ln, g, w) for (ok, g, w, ln) in checks if not ok]
for ln, g, w in bad:
    print(f"line {ln}: got {g!r}, want {w!r}")
n_items = sum(1 for it in items.values() if it["type"] in ("number", "text"))
print(f"{len(checks) - len(bad)}/{len(checks)} claims hold ({n_items} number and text items, {len(CHOICE)} choice items compared with the pack)")
os.chdir(ROOT); shutil.rmtree(SCRATCH, ignore_errors=True)
sys.exit(1 if bad else 0)
